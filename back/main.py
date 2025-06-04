from fastapi import FastAPI, Request
import requests
import httpx
import os

app = FastAPI()
PREDICT_URL = os.getenv("PREDICT_SERVICE_URL", "http://localhost:5000")
PREDICT1_URL = os.getenv("PREDICT1_SERVICE_URL", "http://back-predict1:5001")

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
		
@app.post("/predict1")
async def predict1(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PREDICT1_URL}/predict", json=data)
    return response.json()