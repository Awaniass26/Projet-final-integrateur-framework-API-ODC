from fastapi import FastAPI , HTTPException
from schemas import EtudiantCreate, EtudiantUpdate
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


# Endpoint pour rechercher des étudiants avec des filtres
@app.get("/etudiants/search")
def search_etudiants(
    numero: str = None,
    code: str = None,
    nom: str = None,
    classe: str = None,
    source: str = None
):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT e.id, e.code, e.numero, e.nom, e.prenom,
               e.date_naissance, e.moyenne_generale, c.nom_classe
        FROM etudiant e
        JOIN classe c ON e.classe_id = c.id
        WHERE e.archive = FALSE
    """
    params = []

    if numero:
        query += " AND e.numero ILIKE %s"
        params.append(f"%{numero}%")
    if code:
        query += " AND e.code ILIKE %s"
        params.append(f"%{code}%")
    if nom:
        query += " AND (e.nom ILIKE %s OR e.prenom ILIKE %s)"
        params.extend([f"%{nom}%", f"%{nom}%"])
    if classe:
        query += " AND c.nom_classe ILIKE %s"
        params.append(f"%{classe}%")

    cur.execute(query, params)
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

    # Si source JSON ou pas de filtre source, compléter avec JSON
    if source != "DB":
        json_data = lire_json()
        numeros_db = [e["numero"] for e in resultats]
        for etudiant in json_data:
            if etudiant["numero"] in numeros_db:
                continue
            if numero and numero.lower() not in etudiant["numero"].lower():
                continue
            if nom and nom.lower() not in etudiant["nom"].lower() and nom.lower() not in etudiant["prenom"].lower():
                continue
            if classe and classe.lower() not in etudiant["classe"].lower():
                continue
            resultats.append({**etudiant, "id": None, "source": "JSON"})

    return {"data": resultats}


#endpoint pour ajouter un étudiant
@app.post("/etudiants")
def ajouter_etudiant(etudiant: EtudiantCreate):
    conn = get_connection()
    cur = conn.cursor()

    # Vérifier doublon
    cur.execute("SELECT id FROM etudiant WHERE numero = %s", (etudiant.numero,))
    if cur.fetchone():
        raise HTTPException(status_code=400, detail="Numéro déjà existant")

    # Insérer ou récupérer classe
    cur.execute("INSERT INTO classe (nom_classe) VALUES (%s) ON CONFLICT (nom_classe) DO NOTHING", (etudiant.classe,))
    cur.execute("SELECT id FROM classe WHERE nom_classe = %s", (etudiant.classe,))
    classe_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO etudiant (code, numero, nom, prenom, date_naissance, moyenne_generale, classe_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        etudiant.code, etudiant.numero, etudiant.nom,
        etudiant.prenom, etudiant.date_naissance,
        etudiant.moyenne_generale, classe_id
    ))

    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Étudiant ajouté avec succès"}


# endpoint pour modifier un étudiant
@app.put("/etudiants/{id}")
def modifier_etudiant(id: int, etudiant: EtudiantUpdate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM etudiant WHERE id = %s AND archive = FALSE", (id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Étudiant introuvable")

    cur.execute("""
        UPDATE etudiant
        SET nom=%s, prenom=%s, date_naissance=%s, moyenne_generale=%s
        WHERE id=%s
    """, (etudiant.nom, etudiant.prenom, etudiant.date_naissance, etudiant.moyenne_generale, id))

    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Étudiant modifié avec succès"}

#endpoint pour supprimer un étudiant
@app.delete("/etudiants/{id}")
def supprimer_etudiant(id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM etudiant WHERE id = %s AND archive = FALSE", (id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Étudiant introuvable")

    cur.execute("DELETE FROM etudiant WHERE id = %s", (id,))

    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Étudiant supprimé avec succès"}

    
#endpoint pour importer des étudiants depuis le fichier JSON
@app.post("/etudiants/importer")
def importer_depuis_json(numeros: list[str]):
    json_data = lire_json()
    conn = get_connection()
    cur = conn.cursor()

    importes = []
    ignores = []

    for numero in numeros:
        etudiant = next((e for e in json_data if e["numero"] == numero), None)
        if not etudiant:
            ignores.append({"numero": numero, "raison": "Introuvable dans le JSON"})
            continue

        cur.execute("SELECT id FROM etudiant WHERE numero = %s", (numero,))
        if cur.fetchone():
            ignores.append({"numero": numero, "raison": "Doublon"})
            continue

        cur.execute("INSERT INTO classe (nom_classe) VALUES (%s) ON CONFLICT (nom_classe) DO NOTHING", (etudiant["classe"],))
        cur.execute("SELECT id FROM classe WHERE nom_classe = %s", (etudiant["classe"],))
        classe_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO etudiant (code, numero, nom, prenom, date_naissance, moyenne_generale, classe_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            etudiant["code"], etudiant["numero"], etudiant["nom"],
            etudiant["prenom"], etudiant["date_naissance"],
            etudiant["moyenne_generale"], classe_id
        ))
        etudiant_id = cur.fetchone()[0]

        for nom_matiere, details in etudiant["matieres"].items():
            cur.execute("INSERT INTO matiere (nom_matiere) VALUES (%s) ON CONFLICT (nom_matiere) DO NOTHING", (nom_matiere,))
            cur.execute("SELECT id FROM matiere WHERE nom_matiere = %s", (nom_matiere,))
            matiere_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO note (etudiant_id, matiere_id, note_examen, moyenne_matiere)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (etudiant_id, matiere_id, details["examen"], details["moyenne"]))
            note_id = cur.fetchone()[0]

            for note_devoir in details["devoirs"]:
                cur.execute("INSERT INTO devoir (note_id, note_devoir) VALUES (%s, %s)", (note_id, note_devoir))

        importes.append(numero)

    conn.commit()
    cur.close()
    conn.close()
    return {"importes": importes, "ignores": ignores}


#endpoint pour archiver un étudiant (soft delete)
@app.put("/etudiants/{id}/archiver")
def archiver_etudiant(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE etudiant SET archive = TRUE WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Étudiant archivé"}


#endpoint pour la liste des archives
@app.get("/archives")
def get_archives():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.id, e.code, e.numero, e.nom, e.prenom,
               e.date_naissance, e.moyenne_generale, c.nom_classe
        FROM etudiant e
        JOIN classe c ON e.classe_id = c.id
        WHERE e.archive = TRUE
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": [{"id": r[0], "code": r[1], "numero": r[2], "nom": r[3],
                      "prenom": r[4], "date_naissance": r[5],
                      "moyenne_generale": r[6], "classe": r[7]} for r in rows]}


#endpoint pour restaurer un étudiant archivé
@app.put("/archives/{id}/restaurer")
def restaurer_etudiant(id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE etudiant SET archive = FALSE WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Étudiant restauré"}


#endpoint pour le dashboard
@app.get("/dashboard")
def get_dashboard():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM etudiant WHERE archive = FALSE")
    total_db = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM etudiant WHERE archive = TRUE")
    total_archives = cur.fetchone()[0]

    cur.execute("""
        SELECT c.nom_classe, COUNT(e.id)
        FROM etudiant e
        JOIN classe c ON e.classe_id = c.id
        WHERE e.archive = FALSE
        GROUP BY c.nom_classe
    """)
    par_classe = [{"classe": r[0], "total": r[1]} for r in cur.fetchall()]

    cur.execute("""
        SELECT e.nom, e.prenom, e.moyenne_generale, c.nom_classe
        FROM etudiant e
        JOIN classe c ON e.classe_id = c.id
        WHERE e.archive = FALSE
        ORDER BY e.moyenne_generale DESC
        LIMIT 10
    """)
    top10 = [{"nom": r[0], "prenom": r[1], "moyenne": r[2], "classe": r[3]} for r in cur.fetchall()]

    json_data = lire_json()
    total_json = len(json_data)

    cur.close()
    conn.close()

    return {
        "total_db": total_db,
        "total_json": total_json,
        "total_archives": total_archives,
        "par_classe": par_classe,
        "top10": top10
    }