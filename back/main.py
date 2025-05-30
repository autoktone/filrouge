from fastapi import FastAPI
import requests
import os

app = FastAPI()
PREDICT_URL = os.getenv("PREDICT_SERVICE_URL", "http://localhost:5000")

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API gateway"}

@app.get("/predict")
def predict():
    try:
        r = requests.get(f"{PREDICT_URL}/predict")
        return r.json()
    except Exception as e:
        return {"error": str(e)}
