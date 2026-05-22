import psycopg #importation de la bibliothèque psycopg pour se connecter à une base de données PostgreSQL

# Fonction de Connexion
def get_connection():
    return psycopg.connect(
        host="localhost", #le host est l'adresse du serveur de base de données, localhost pour une base de données locale
        dbname="projetfinalpython",
        user="postgres",
        password="postgres",
        port=5432 #le port est le numéro de port sur lequel le serveur de base de données écoute, 5432 est le port par défaut pour PostgreSQL
    )

# Fonction de Création des tables
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS classe (
            id SERIAL PRIMARY KEY,
            nom_classe VARCHAR(20) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS etudiant (
            id SERIAL PRIMARY KEY,
            code VARCHAR(10) NOT NULL,
            numero VARCHAR(15) UNIQUE NOT NULL,
            nom VARCHAR(50) NOT NULL,
            prenom VARCHAR(50) NOT NULL,
            date_naissance VARCHAR(20) NOT NULL,
            archive BOOLEAN DEFAULT FALSE,
            classe_id INTEGER REFERENCES classe(id) 
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS matiere (
            id SERIAL PRIMARY KEY,
            nom_matiere VARCHAR(50) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS note (
            id SERIAL PRIMARY KEY,
            etudiant_id INTEGER REFERENCES etudiant(id),
            matiere_id INTEGER REFERENCES matiere(id),
            note_examen FLOAT NOT NULL,
            moyenne_matiere FLOAT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS devoir (
            id SERIAL PRIMARY KEY,
            note_id INTEGER REFERENCES note(id),
            note_devoir FLOAT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables créées avec succès")


# Point d'entrée
if __name__ == "__main__":
    create_tables()
