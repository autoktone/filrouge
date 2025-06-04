from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()
JWT_SECRET = os.getenv("JWT_SECRET", "changeme")

class AuthRequest(BaseModel):
    username: str
    password: str

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