from pydantic import BaseModel

class Devoir(BaseModel):
    devoirs: list[float]
    examen: float
    moyenne: float

class EtudiantCreate(BaseModel):
    code: str
    numero: str
    nom: str
    prenom: str
    date_naissance: str
    classe: str
    matieres: dict[str, Devoir]
    moyenne_generale: float

class EtudiantUpdate(BaseModel):
    nom: str
    prenom: str
    date_naissance: str
    classe: str
    moyenne_generale: float

class EtudiantImport(BaseModel):
    numeros: list[str]