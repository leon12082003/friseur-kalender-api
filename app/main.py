from fastapi import FastAPI, Request
from app.models import (
    TerminAnfrage, TerminAbsage, TerminVerschiebung,
    FreieZeitenAnfrage
)
from app.calendar_logic import *
from app.config import MITARBEITER

app = FastAPI()

def finde_mitarbeiter_nach_leistung(leistung: str):
    for name, info in MITARBEITER.items():
        if leistung in info.get("leistungen", []):
            return name
    return None

@app.post("/kalender-verwalten")
async def kalender_verwalten(request: Request):
    body = await request.json()
    aktion = body.get("aktion")

    if aktion == "buchen":
        data = TerminAnfrage(**body["daten"])
        mitarbeiter = data.bevorzugt or finde_mitarbeiter_nach_leistung(data.leistung)
        if not mitarbeiter:
            return {"status": "fehler", "info": "Kein passender Friseur gefunden"}
        kalender_id = CALENDAR_IDS[mitarbeiter]
        erfolg = buche_termin(kalender_id, data.name, data.leistung, data.datum, data.uhrzeit, data.bemerkung)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "abfragen":
        data = FreieZeitenAnfrage(**body["daten"])
        mitarbeiter = finde_mitarbeiter_nach_leistung(data.leistung)
        if not mitarbeiter:
            return {"status": "fehler", "info": "Keine zuständige Person gefunden"}
        kalender_id = CALENDAR_IDS[mitarbeiter]
        freie_termine = finde_naechste_freie_termine(kalender_id, data.leistung)
        return {"freie_termine": freie_termine}

    elif aktion == "loeschen":
        data = TerminAbsage(**body["daten"])
        if not data.leistung:
            return {"status": "fehler", "info": "Leistung fehlt"}
        mitarbeiter = finde_mitarbeiter_nach_leistung(data.leistung)
        if not mitarbeiter:
            return {"status": "fehler", "info": "Kein passender Friseur gefunden"}
        kalender_id = CALENDAR_IDS.get(mitarbeiter)
        erfolg = loesche_termin(kalender_id, data.name, data.datum, data.uhrzeit)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "verschieben":
        data = TerminVerschiebung(**body["daten"])
        if not data.leistung:
            return {"status": "fehler", "info": "Leistung fehlt"}
        mitarbeiter = finde_mitarbeiter_nach_leistung(data.leistung)
        if not mitarbeiter:
            return {"status": "fehler", "info": "Kein passender Friseur gefunden"}
        kalender_id = CALENDAR_IDS.get(mitarbeiter)
        erfolg = verschiebe_termin(
            kalender_id, data.name,
            data.alt_datum, data.alt_uhrzeit,
            data.neu_datum, data.neu_uhrzeit
        )
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "kombi":
        kunden = body.get("daten", {}).get("kunden", [])
        if len(kunden) < 2:
            return {"status": "mindestens zwei kunden erforderlich"}

        kalender_ids = []
        for kunde in kunden:
            leistung = kunde.get("leistung")
            mitarbeiter = finde_mitarbeiter_nach_leistung(leistung)
            if not mitarbeiter:
                return {"status": f"keine zuständige friseur:in für '{leistung}' gefunden"}
            kalender_ids.append(CALENDAR_IDS[mitarbeiter])

        gemeinsame = finde_gemeinsame_freie_termine(kalender_ids)
        if gemeinsame:
            return {"status": "kombitermine", "slots": gemeinsame}
        else:
            return {"status": "keine gemeinsamen termine gefunden"}

    elif aktion == "kombi_buchen":
        kunden = body.get("daten", {}).get("kunden", [])
        if len(kunden) < 2:
            return {"status": "mindestens zwei kunden erforderlich"}

        erfolge = []
        for kunde in kunden:
            leistung = kunde.get("leistung")
            mitarbeiter = finde_mitarbeiter_nach_leistung(leistung)
            if not mitarbeiter:
                erfolge.append({"name": kunde.get("name"), "status": "kein friseur gefunden"})
                continue
            kalender_id = CALENDAR_IDS[mitarbeiter]
            ok = buche_termin(
                kalender_id,
                kunde.get("name"),
                kunde.get("leistung"),
                kunde.get("datum"),
                kunde.get("uhrzeit"),
                kunde.get("bemerkung")
            )
            erfolge.append({"name": kunde.get("name"), "status": "ok" if ok else "fehler"})

        return {"status": "fertig", "buchungen": erfolge}

    return {"status": "unbekannte aktion"}
