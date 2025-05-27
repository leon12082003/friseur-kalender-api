from datetime import time

# Öffnungszeiten
OPENING_HOURS = {
    "mo-fr": (time(9, 0), time(18, 0)),
    "sa": (time(9, 0), time(14, 0)),
}

# Kalender-IDs (Platzhalter – bitte durch echte IDs ersetzen)
CALENDAR_IDS = {
    "Karin Meier": "1e3a743874cf760bf08026e4fd7eb4a2692c5996e8de1181fd8c87837be524e7@group.calendar.google.com",
    "Marco Hauer": "00edba1ec002f208f25bbd78a7649ef0518121d31071a4fed10ecc0393e3d4b9@group.calendar.google.com",
    "Lisa Fischer": "c196fca542ff5176c62b11805596e015f5fb2aff1ec0b73c43cf555937911638@group.calendar.google.com",
    "Max Zimmer": "5b679eaf3a0999b06265e6b21dd2200800e8b2338056475e1cbd8f17ab34f861@group.calendar.google.com"
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
