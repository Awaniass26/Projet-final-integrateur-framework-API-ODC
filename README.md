# Projet final intégrateur - Framework API ODC

Ce projet est une application Python avec une API FastAPI et un front-end simple.

## Structure du projet

- `projet.py` : point d’entrée principal de l’application FastAPI.
- `backend/` : dossier backend avec `main.py`, `database.py`, `schemas.py`.
- `frontend/` : dossier front-end avec `index.html` et `script.js`.
- `data/` : contient des fichiers JSON de données (`valides.json`, `invalides.json`).
- `menv/` : environnement virtuel Python du projet.

## Prérequis

- Python 3.12 ou supérieur
- `pip` installé
- Environnement virtuel recommandé

## Installation

1. Activer l’environnement virtuel :

```bash
source ./menv/bin/activate
```

2. Installer les dépendances si nécessaire :

```bash
pip install -r requirements.txt
```

> Si le fichier `requirements.txt` n’existe pas dans le projet, installez au moins `fastapi` et `uvicorn` :
>
> ```bash
> pip install fastapi uvicorn
> ```

## Exécution du backend

Lancer le serveur FastAPI :

```bash
uvicorn projet:app --reload
```

Puis ouvrir dans votre navigateur :

```text
http://127.0.0.1:8000
```

## Front-end

Le front-end se trouve dans `frontend/index.html`. Il s’agit d’une page HTML statique qui peut être ouverte directement dans un navigateur.

Si vous souhaitez servir le front-end depuis un serveur, placez les fichiers dans un répertoire accessible par votre serveur web ou utilisez un serveur statique simple.

## Notes

- Le backend actuel se réduit à une route GET `/` qui renvoie `{"message": "Hello World"}`.
- Les fichiers `backend/database.py` et `backend/schemas.py` sont présents mais vides, ils sont prêts à être utilisés pour la suite du développement.
- Le fichier `frontend/script.js` est vide et peut être complété pour interagir avec l’API.

## Améliorations possibles

- Ajouter des routes FastAPI pour gérer des données JSON.
- Implémenter une base de données ou un stockage local.
- Compléter le front-end pour appeler l’API via `fetch`.
- Ajouter un vrai `requirements.txt` pour le projet.
