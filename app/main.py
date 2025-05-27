from fastapi import FastAPI, Request
from app.models import (
    TerminAnfrage, TerminAbsage, TerminVerschiebung,
    FreieZeitenAnfrage, KombiBuchung
)
from app.calendar_logic import *
from app.config import CALENDAR_IDS

app = FastAPI()

@app.post("/kalender-verwalten")
async def kalender_verwalten(request: Request):
    body = await request.json()
    aktion = body.get("aktion")

    if aktion == "buchen":
        data = TerminAnfrage(**body["daten"])
        kalender_id = CALENDAR_IDS.get(data.friseur)
        if not kalender_id:
            return {"status": "fehler", "info": "Friseur nicht gefunden"}
        erfolg = buche_termin(kalender_id, data.name, "Termin", data.datum, data.uhrzeit, data.bemerkung)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "abfragen":
        data = FreieZeitenAnfrage(**body["daten"])
        kalender_id = CALENDAR_IDS.get(data.friseur)
        if not kalender_id:
            return {"status": "fehler", "info": "Friseur nicht gefunden"}

        if data.datum:
            freie = []
            for stunde in range(9, 18):
                uhrzeit = f"{stunde:02d}:00"
                if pruefe_verfuegbarkeit(kalender_id, data.datum, uhrzeit):
                    freie.append(f"{data.datum} {uhrzeit}")
            return {"freie_termine": freie}
        else:
            freie_termine = finde_naechste_freie_termine(kalender_id, "Termin")
            return {"freie_termine": freie_termine}

    elif aktion == "loeschen":
        data = TerminAbsage(**body["daten"])
        kalender_id = CALENDAR_IDS.get(data.friseur)
        if not kalender_id:
            return {"status": "fehler", "info": "Friseur nicht gefunden"}
        erfolg = loesche_termin(kalender_id, data.name, data.datum, data.uhrzeit)
        return {"status": "ok" if erfolg else "fehler"}

    elif aktion == "verschieben":
        data = TerminVerschiebung(**body["daten"])
        kalender_id = CALENDAR_IDS.get(data.friseur)
        if not kalender_id:
            return {"status": "fehler", "info": "Friseur nicht gefunden"}
        erfolg = verschiebe_termin(
            kalender_id,
            data.name,
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
            friseur = kunde.get("friseur")
            kalender_id = CALENDAR_IDS.get(friseur)
            if not kalender_id:
                return {"status": f"friseur '{friseur}' nicht gefunden"}
            kalender_ids.append(kalender_id)

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
            friseur = kunde.get("friseur")
            kalender_id = CALENDAR_IDS.get(friseur)
            if not kalender_id:
                erfolge.append({"name": kunde.get("name"), "status": "friseur nicht gefunden"})
                continue
            ok = buche_termin(
                kalender_id,
                kunde.get("name"),
                "Termin",
                kunde.get("datum"),
                kunde.get("uhrzeit"),
                kunde.get("bemerkung")
            )
            erfolge.append({"name": kunde.get("name"), "status": "ok" if ok else "fehler"})

        return {"status": "fertig", "buchungen": erfolge}

    return {"status": "unbekannte aktion"}
