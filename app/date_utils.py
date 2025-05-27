from datetime import datetime, timedelta
import re
from fastapi import APIRouter, Request

router = APIRouter()

# Mapping für Wochentage
weekday_map = {
    "montag": 0,
    "dienstag": 1,
    "mittwoch": 2,
    "donnerstag": 3,
    "freitag": 4,
    "samstag": 5,
    "sonntag": 6
}

def finde_naechsten_wochentag(wochentag: int, wochen_offset: int = 0):
    heute = datetime.now()
    tage_bis_gewunscht = (wochentag - heute.weekday() + 7) % 7 + 7 * wochen_offset
    if tage_bis_gewunscht == 0:
        tage_bis_gewunscht += 7
    return (heute + timedelta(days=tage_bis_gewunscht)).strftime("%Y-%m-%d")

def parse_datum(text: str):
    text = text.lower().strip()
    heute = datetime.now()

    if "heute" in text:
        return heute.strftime("%Y-%m-%d")
    if "morgen" in text:
        return (heute + timedelta(days=1)).strftime("%Y-%m-%d")
    if "übermorgen" in text:
        return (heute + timedelta(days=2)).strftime("%Y-%m-%d")

    match_tage = re.search(r"in (\d+) tagen?", text)
    if match_tage:
        tage = int(match_tage.group(1))
        return (heute + timedelta(days=tage)).strftime("%Y-%m-%d")

    for tag, index in weekday_map.items():
        if f"nächsten {tag}" in text:
            return finde_naechsten_wochentag(index)
        if f"übernächsten {tag}" in text:
            return finde_naechsten_wochentag(index, wochen_offset=1)
        if f"am {tag} in einer woche" in text:
            return finde_naechsten_wochentag(index, wochen_offset=1)

    if "nächsten monat" in text:
        naechster_monat = heute.replace(day=1) + timedelta(days=32)
        return naechster_monat.replace(day=1).strftime("%Y-%m-%d")

    return None

@router.post("/resolve-datum")
async def resolve_datum(request: Request):
    body = await request.json()
    text = body.get("text", "")
    resolved = parse_datum(text)

    if resolved:
        return {"resolved_date": resolved}
    else:
        return {
            "resolved_date": None,
            "hinweis": "Bitte nenne ein konkretes Datum, z. B. 'am 15. Juli' oder 'nächsten Dienstag'."
        }
