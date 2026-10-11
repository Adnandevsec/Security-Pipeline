#Login & Token Generation
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import jwt
import os

app = FastAPI(title="Auth Service")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
client = AsyncIOMotorClient(MONGO_URL)
db = client.security_db
users_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/login")
async def login(credentials: LoginRequest):
    user = await users_collection.find_one({"email": credentials.email})
    if not user or not pwd_context.verify(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode({"sub": user["email"], "username": user["username"]}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}