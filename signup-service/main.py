#User Registration
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os

app = FastAPI(root_path="/signup")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Database connection from environment variable (Kubernetes config)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.security_db
users_collection = db.users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupRequest):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }
    
    await users_collection.insert_one(user_doc)
    return {"message": "User registered successfully", "email": user.email}