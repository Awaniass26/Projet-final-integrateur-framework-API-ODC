from fastapi import FastAPI

#creation d'une instance de l'application FastAPI
app = FastAPI()

#definition d'une route pour la racine de l'application
@app.get("/")
async def root():  
    return {"message": "Hello World"}