from datetime import time

# Öffnungszeiten
OPENING_HOURS = {
    "mo-fr": (time(9, 0), time(18, 0)),
    "sa": (time(9, 0), time(14, 0)),
}

# Kalender-IDs (Platzhalter – bitte durch echte IDs ersetzen)
CALENDAR_IDS = {
    "Karin Meier": "kalender_karin_id@google.com",
    "Marco Hauer": "kalender_marco_id@google.com",
    "Lisa Fischer": "kalender_lisa_id@google.com",
    "Max Zimmer": "kalender_max_id@google.com"
}

# Mitarbeiterprofile
MITARBEITER = {
    "Karin Meier": {
        "leistungen": ["Damenfrisur"],
        "beschreibung": ["Frau", "groß", "blonde Haare", "Brille"],
        "vertretung": ["Lisa Fischer"]
    },
    "Marco Hauer": {
        "leistungen": ["Herrenfrisur"],
        "beschreibung": ["Mann", "schwarze Haare"],
        "vertretung": ["Max Zimmer"]
    },
    "Lisa Fischer": {
        "leistungen": ["Färben", "Extensions", "Damenfrisur"],
        "beschreibung": ["Frau", "klein", "braune Haare"],
        "vertretung": ["Karin Meier"]
    },
    "Max Zimmer": {
        "leistungen": ["Kinderfrisur"],
        "beschreibung": ["Mann", "blonde Haare"],
        "vertretung": ["Marco Hauer"]
    }
}