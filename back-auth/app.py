from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta

# Création de l'application principale
app = FastAPI()

# Clé secrète récupérée depuis l'environnement
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")

# Création du routeur pour l'authentification
router = APIRouter()

# Schéma de la requête d'authentification
class AuthRequest(BaseModel):
    username: str
    password: str

# Route POST pour générer un token
@router.post("/auth")
def login(auth: AuthRequest):
    if auth.username != "admin" or auth.password != "password":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": auth.username,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {"access_token": token}

# Montage du routeur dans l'application principale
app.include_router(router)	