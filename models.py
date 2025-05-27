from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time

class TerminAnfrage(BaseModel):
    name: str
    leistung: str
    bevorzugt: Optional[str] = None  # bevorzugte Friseur:in
    datum: Optional[str] = None      # 'YYYY-MM-DD'
    uhrzeit: Optional[str] = None    # 'HH:MM'
    bemerkung: Optional[str] = None

class TerminAbsage(BaseModel):
    name: str
    datum: str
    uhrzeit: str
    leistung: Optional[str] = None

class TerminVerschiebung(BaseModel):
    name: str
    alt_datum: str
    alt_uhrzeit: str
    neu_datum: str
    neu_uhrzeit: str
    leistung: Optional[str] = None

class FreieZeitenAnfrage(BaseModel):
    leistung: str
    datum: Optional[str] = None  # z. B. "2025-05-30"

class KombiAnfrage(BaseModel):
    kunden: List[TerminAnfrage]