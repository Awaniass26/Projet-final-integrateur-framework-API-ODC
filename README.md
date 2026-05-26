# Projet final intégrateur - Framework API ODC

Ce projet est une application Python avec une API FastAPI et un front-end simple.

## Structure du projet

- `projet.py` : fichier présent à la racine mais vide actuellement.
- `backend/` : dossier backend avec l’application FastAPI dans `backend/main.py`, ainsi que les fichiers `database.py` et `schemas.py`.
- `frontend/` : dossier front-end contenant `index.html` et `script.js`.
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
pip install fastapi uvicorn
```

> Si un fichier `requirements.txt` est ajouté ultérieurement, utilisez :
>
> ```bash
> pip install -r requirements.txt
> ```

## Exécution du backend

Lancer le serveur FastAPI depuis la racine du projet :

```bash
uvicorn backend.main:app --reload
```

Ouvrir ensuite dans le navigateur :

```text
http://127.0.0.1:8000
```

## Front-end

Le front-end se trouve dans `frontend/index.html`. Il peut être ouvert directement dans un navigateur ou servi par un serveur statique.

## État actuel

- Le backend expose une route GET `/` qui renvoie `{"message": "Hello World"}`.
- `backend/database.py` et `backend/schemas.py` sont présents pour les futures extensions du projet.
- `frontend/script.js` est prêt à être complété pour consommer l’API.
- `projet.py` est présent mais n’est pas utilisé.

## Améliorations possibles

- Ajouter des routes FastAPI pour gérer les données de `data/`.
- Ajouter un fichier `requirements.txt` pour versionner les dépendances.
- Compléter le front-end avec des appels `fetch` vers l’API.
- Ajouter une base de données ou un stockage local pour les données JSON.
