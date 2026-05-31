from pydantic import BaseModel, model_validator

class Devoir(BaseModel):
    devoirs: list[float]
    examen: float
    moyenne: float = 0.0

# Calcul de la moyenne après validation des données
    @model_validator(mode='after')
    def calculer_moyenne(self):
        moyenne_devoirs = sum(self.devoirs) / len(self.devoirs)
        self.moyenne = round((moyenne_devoirs + 2 * self.examen) / 3, 2)
        return self

class EtudiantCreate(BaseModel):
    code: str
    numero: str
    nom: str
    prenom: str
    date_naissance: str
    classe: str
    matieres: dict[str, Devoir]
    moyenne_generale: float = 0.0

    @model_validator(mode='after')
    def calculer_moyenne_generale(self):
        moyennes = [m.moyenne for m in self.matieres.values()]
        self.moyenne_generale = round(sum(moyennes) / len(moyennes), 2)
        return self

class EtudiantUpdate(BaseModel):
    nom: str
    prenom: str
    date_naissance: str
    classe: str
    moyenne_generale: float = 0.0

class EtudiantImport(BaseModel):
    numeros: list[str]