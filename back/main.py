from fastapi import FastAPI, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, Query
import requests
import httpx
import os
import jwt


# Gestion Token JWT
security = HTTPBearer()
JWT_SECRET = os.getenv("JWT_SECRET")

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Gestion API : "app" est utilisé dans le Dockerfile "main:app"
app = FastAPI()

# Variables d'environnement
AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://back-auth:5000")
PREDICT_URL = os.getenv("PREDICT_SERVICE_URL", "http://back-predict:5001")
PREDICT1_URL = os.getenv("PREDICT1_SERVICE_URL", "http://back-predict1:5002")
METEO_URL = os.getenv("METEO_SERVICE_URL", "http://back-meteo:5003")
EVENTS_URL = os.getenv("EVENTS_SERVICE_URL", "http://back-events:5004")

# Check statut sans sécurité
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API gateway - Accès limité"}

# Génération Token
@app.post("/auth")
async def auth_proxy(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_URL}/auth", json=data)
    return response.json()

# Services applicatifs
@app.get("/meteo")
def get_meteo(town: str = Query("Paris"), api_key: str = Query(...)):
    try:
        # Construction de l’URL avec les paramètres
        url = f"{METEO_URL}/meteo?town={town}&API_KEY={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

# services Events
@app.get("/events")
async def get_events(
    sports: str = Query(..., description="Comma-separated sports list"),
    participation: str = Query(..., description="Comma-separated participation types, e.g. spectator,participant,")
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{EVENTS_URL}/events",
                params={"sports": sports, "participation": participation}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Services Exemples GET:predict et POST:predict1
@app.get("/predict")
def predict(user=Depends(verify_jwt)):
    try:
        r = requests.get(f"{PREDICT_URL}/predict")
        return r.json()
    except Exception as e:
        return {"error": str(e)}
		
@app.post("/predict1")
async def predict1(request: Request, user=Depends(verify_jwt)):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PREDICT1_URL}/predict", json=data)
    return response.json()