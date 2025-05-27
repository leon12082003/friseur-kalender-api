from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import re

router = APIRouter()

WEEKDAYS = {
    "montag": 0, "dienstag": 1, "mittwoch": 2,
    "donnerstag": 3, "freitag": 4, "samstag": 5, "sonntag": 6
}

def finde_wochentag(text: str):
    for name, index in WEEKDAYS.items():
        if name in text.lower():
            return index
    return None

@router.post("/resolve-datum")
async def resolve_datum(request: Request):
    body = await request.json()
    raw = body.get("text", "").lower()

    today = datetime.now()
    weekday = finde_wochentag(raw)

    if weekday is not None:
        tage_vor = (weekday - today.weekday() + 7) % 7
        tage_vor = tage_vor or 7
        if "nächste" in raw or "kommende" in raw:
            tage_vor += 7
        zieldatum = today + timedelta(days=tage_vor)
        return {"resolved_date": zieldatum.strftime("%Y-%m-%d")}

    return {"resolved_date": None}