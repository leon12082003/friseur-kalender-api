import os
import json
from datetime import datetime, timedelta
from typing import List, Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build

from app.config import CALENDAR_IDS, MITARBEITER

SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

def get_calendar_service():
    return build('calendar', 'v3', credentials=credentials)

def iso_datetime(datum: str, uhrzeit: str) -> str:
    return f"{datum}T{uhrzeit}:00+02:00"

def finde_mitarbeiter_fuer_leistung(leistung: str) -> List[str]:
    passende = []
    for name, info in MITARBEITER.items():
        if leistung in info["leistungen"]:
            passende.append(name)
    return passende

def finde_vertreter(mitarbeiter: str) -> List[str]:
    return MITARBEITER.get(mitarbeiter, {}).get("vertretung", [])

def pruefe_verfuegbarkeit(kalender_id: str, datum: str, uhrzeit: str) -> bool:
    service = get_calendar_service()
    start = iso_datetime(datum, uhrzeit)
    end_dt = (datetime.fromisoformat(f"{datum}T{uhrzeit}") + timedelta(minutes=30)).isoformat()
    end = f"{end_dt}+02:00"

    events = service.events().list(
        calendarId=kalender_id,
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return len(events.get('items', [])) == 0

def finde_naechste_freie_termine(kalender_id: str, leistung: str, anzahl: int = 3) -> List[str]:
    freie = []
    jetzt = datetime.now()
    service = get_calendar_service()

    for tag in range(1, 14):
        datum = (jetzt + timedelta(days=tag)).strftime('%Y-%m-%d')
        for stunde in range(9, 18):
            uhrzeit = f"{stunde:02d}:00"
            start = iso_datetime(datum, uhrzeit)
            end_dt = (datetime.fromisoformat(f"{datum}T{uhrzeit}") + timedelta(minutes=30)).isoformat()
            end = f"{end_dt}+02:00"

            events = service.events().list(
                calendarId=kalender_id,
                timeMin=start,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()

            if len(events.get('items', [])) == 0:
                freie.append(f"{datum} {uhrzeit}")
                if len(freie) >= anzahl:
                    return freie
    return freie

def buche_termin(kalender_id: str, name: str, leistung: str, datum: str, uhrzeit: str, bemerkung: Optional[str] = None) -> bool:
    service = get_calendar_service()
    start = iso_datetime(datum, uhrzeit)
    end_dt = (datetime.fromisoformat(f"{datum}T{uhrzeit}") + timedelta(minutes=30)).isoformat()
    end = f"{end_dt}+02:00"

    event = {
        'summary': f"{leistung} – {name}",
        'description': bemerkung or '',
        'start': {'dateTime': start},
        'end': {'dateTime': end}
    }

    try:
        service.events().insert(calendarId=kalender_id, body=event).execute()
        return True
    except:
        return False

def loesche_termin(kalender_id: str, name: str, datum: str, uhrzeit: str) -> bool:
    service = get_calendar_service()
    start = iso_datetime(datum, uhrzeit)
    end_dt = (datetime.fromisoformat(f"{datum}T{uhrzeit}") + timedelta(minutes=30)).isoformat()
    end = f"{end_dt}+02:00"

    events = service.events().list(
        calendarId=kalender_id,
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    for event in events.get('items', []):
        if name.lower() in (event.get('summary', '') + event.get('description', '')).lower():
            try:
                service.events().delete(calendarId=kalender_id, eventId=event['id']).execute()
                return True
            except:
                return False
    return False

def verschiebe_termin(kalender_id: str, name: str, alt_datum: str, alt_uhrzeit: str, neu_datum: str, neu_uhrzeit: str) -> bool:
    geloescht = loesche_termin(kalender_id, name, alt_datum, alt_uhrzeit)
    if not geloescht:
        return False
    return buche_termin(kalender_id, name, "verschoben", neu_datum, neu_uhrzeit)