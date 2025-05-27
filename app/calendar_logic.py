from app.config import CALENDAR_IDS, MITARBEITER, OPENING_HOURS
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

# Dies sind nur Platzhalter – die Google Calendar API-Logik wird später ergänzt

def finde_mitarbeiter_fuer_leistung(leistung: str) -> List[str]:
    passende = []
    for name, info in MITARBEITER.items():
        if leistung in info["leistungen"]:
            passende.append(name)
    return passende

def finde_vertreter(mitarbeiter: str) -> List[str]:
    return MITARBEITER.get(mitarbeiter, {}).get("vertretung", [])

def pruefe_verfuegbarkeit(kalender_id: str, datum: str, uhrzeit: str) -> bool:
    # TODO: Google Calendar API aufrufen, ob Slot frei ist
    return True  # Platzhalter

def finde_naechste_freie_termine(kalender_id: str, leistung: str, anzahl: int = 3) -> List[str]:
    # TODO: Logik für nächste freie Termine implementieren
    return ["2025-05-28 10:00", "2025-05-28 11:30", "2025-05-29 09:00"]  # Platzhalter

def buche_termin(kalender_id: str, name: str, leistung: str, datum: str, uhrzeit: str, bemerkung: Optional[str] = None) -> bool:
    # TODO: Termin im Google Kalender eintragen
    return True  # Platzhalter

def loesche_termin(kalender_id: str, name: str, datum: str, uhrzeit: str) -> bool:
    # TODO: Termin löschen via Google Calendar API
    return True  # Platzhalter

def verschiebe_termin(kalender_id: str, name: str, alt_datum: str, alt_uhrzeit: str, neu_datum: str, neu_uhrzeit: str) -> bool:
    # TODO: Termin verschieben (löschen + neu buchen)
    return True  # Platzhalter

def finde_kombitermine(kalender_ids: List[str], datum: Optional[str] = None) -> List[Tuple[str, str]]:
    # TODO: Verfügbarkeit beider Kalender abgleichen
    return [("2025-05-30", "18:00")]  # Platzhalter