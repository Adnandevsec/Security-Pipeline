#User Management - Allows users to view, update, or delete their profile information after they are logged in.
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(root_path="/profile")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.security_db
profiles_collection = db.profiles

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/profile/{email}")
async def get_profile(email: str):
    profile = await profiles_collection.find_one({"email": email}, {"_id": 0})
    if not profile:
        return {"email": email, "bio": "No profile added yet."}
    return profile