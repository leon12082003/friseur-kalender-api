from pydantic import BaseModel
from typing import Optional, List

class TerminAnfrage(BaseModel):
    name: str
    friseur: str
    datum: str
    uhrzeit: str
    bemerkung: Optional[str] = None

class TerminAbsage(BaseModel):
    name: str
    friseur: str
    datum: str
    uhrzeit: str

class TerminVerschiebung(BaseModel):
    name: str
    friseur: str
    alt_datum: str
    alt_uhrzeit: str
    neu_datum: str
    neu_uhrzeit: str

class FreieZeitenAnfrage(BaseModel):
    friseur: str

class KombiPerson(BaseModel):
    name: str
    friseur: str
    datum: Optional[str]
    uhrzeit: Optional[str]
    bemerkung: Optional[str]

class KombiBuchung(BaseModel):
    kunden: List[KombiPerson]