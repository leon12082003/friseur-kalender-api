def finde_gemeinsame_freie_termine(kalender_ids: List[str], dauer_minuten: int = 30, tage: int = 14) -> List[str]:
    service = get_calendar_service()
    gemeinsame_zeiten = []

    jetzt = datetime.now().replace(minute=0, second=0, microsecond=0)

    for tag in range(tage):
        datum = (jetzt + timedelta(days=tag))
        if datum.weekday() > 5:  # Nur Montag–Samstag
            continue

        for stunde in range(9, 18):  # Öffnungszeiten Mo–Fr 9–18 Uhr
            uhrzeit = f"{stunde:02d}:00"
            start = iso_datetime(datum.strftime('%Y-%m-%d'), uhrzeit)
            end_dt = datum.replace(hour=stunde) + timedelta(minutes=dauer_minuten)
            end = end_dt.isoformat() + "+02:00"

            frei_bei_alle = True
            for kalender_id in kalender_ids:
                events = service.events().list(
                    calendarId=kalender_id,
                    timeMin=start,
                    timeMax=end,
                    singleEvents=True,
                    orderBy='startTime'
                ).execute()
                if len(events.get('items', [])) > 0:
                    frei_bei_alle = False
                    break

            if frei_bei_alle:
                gemeinsame_zeiten.append(f"{datum.strftime('%Y-%m-%d')} {uhrzeit}")
                if len(gemeinsame_zeiten) >= 5:
                    return gemeinsame_zeiten
    return gemeinsame_zeiten