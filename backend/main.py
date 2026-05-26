from fastapi import FastAPI
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


