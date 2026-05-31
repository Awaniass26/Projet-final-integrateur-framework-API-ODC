from fastapi import FastAPI
from database import get_connection
import json
import os

app = FastAPI()

# Chemin vers le fichier JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDES_PATH = os.path.join(BASE_DIR, "data", "valides.json")

# Fonction pour lire le fichier JSON
def lire_json():
    with open(VALIDES_PATH, encoding="utf-8") as f:
        return json.load(f)

# Endpoint pour obtenir les données du fichier JSON
@app.get("/etudiants")
def get_etudiants(page: int = 1, taille: int = 5):
    conn = get_connection()
    cur = conn.cursor()

    offset = (page - 1) * taille

    cur.execute("""
        SELECT e.id, e.code, e.numero, e.nom, e.prenom,
               e.date_naissance, e.moyenne_generale, c.nom_classe
        FROM etudiant e
        JOIN classe c ON e.classe_id = c.id
        WHERE e.archive = FALSE
        LIMIT %s OFFSET %s
    """, (taille, offset))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    resultats = []
    for row in rows:
        resultats.append({
            "id": row[0], "code": row[1], "numero": row[2],
            "nom": row[3], "prenom": row[4], "date_naissance": row[5],
            "moyenne_generale": row[6], "classe": row[7], "source": "DB"
        })

    if len(resultats) < taille:
        numeros_db = [e["numero"] for e in resultats]
        json_data = lire_json()
        for etudiant in json_data:
            if len(resultats) >= taille:
                break
            if etudiant["numero"] not in numeros_db:
                resultats.append({
                    "id": None, "code": etudiant["code"],
                    "numero": etudiant["numero"], "nom": etudiant["nom"],
                    "prenom": etudiant["prenom"], "date_naissance": etudiant["date_naissance"],
                    "moyenne_generale": etudiant["moyenne_generale"],
                    "classe": etudiant["classe"], "source": "JSON"
                })

    return {"page": page, "taille": taille, "data": resultats}
