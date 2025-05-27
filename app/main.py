from fastapi import FastAPI, Request
from app.models import (
    TerminAnfrage, TerminAbsage, TerminVerschiebung,
    FreieZeitenAnfrage, KombiAnfrage
)
from app.calendar_logic import *

app = FastAPI()

@app.post("/kalender-verwalten")
async def kalender_verwalten(request: Request):
    body = await request.json()
    aktion = body.get("aktion")

    if aktion == "buchen":
        data = TerminAnfrage(**body["daten"])
        mitarbeiter = data.bevorzugt or finde_mitarbeiter_fuer_leistung(data.leistung)[0]
        kalender_id = CALENDAR_IDS[mitarbeiter]
        erfolg = buche_termin(kalender_id, data.name, data.leistung, data.datum, data.uhrzeit, data.bemerkung)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "abfragen":
        data = FreieZeitenAnfrage(**body["daten"])
        mitarbeiter_liste = finde_mitarbeiter_fuer_leistung(data.leistung)
        if not mitarbeiter_liste:
            return {"status": "fehler", "info": "Keine zuständige Person gefunden"}
        kalender_id = CALENDAR_IDS[mitarbeiter_liste[0]]
        freie_termine = finde_naechste_freie_termine(kalender_id, data.leistung)
        return {"freie_termine": freie_termine}

    elif aktion == "loeschen":
        data = TerminAbsage(**body["daten"])
        mitarbeiter = data.leistung and finde_mitarbeiter_fuer_leistung(data.leistung)[0]
        kalender_id = CALENDAR_IDS.get(mitarbeiter)
        erfolg = loesche_termin(kalender_id, data.name, data.datum, data.uhrzeit)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "verschieben":
        data = TerminVerschiebung(**body["daten"])
        mitarbeiter = data.leistung and finde_mitarbeiter_fuer_leistung(data.leistung)[0]
        kalender_id = CALENDAR_IDS.get(mitarbeiter)
        erfolg = verschiebe_termin(
            kalender_id, data.name,
            data.alt_datum, data.alt_uhrzeit,
            data.neu_datum, data.neu_uhrzeit
        )
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "kombi":
        data = KombiAnfrage(**body["daten"])
        kalender_ids = []
        for person in data.kunden:
            friseur = finde_mitarbeiter_fuer_leistung(person.leistung)[0]
            kalender_ids.append(CALENDAR_IDS[friseur])
        gemeinsame_termine = finde_kombitermine(kalender_ids)
        return {"kombitermine": gemeinsame_termine}

    return {"status": "unbekannte aktion"}