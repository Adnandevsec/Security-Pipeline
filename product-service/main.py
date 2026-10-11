#Core Business Logic - Example - Manages catalog items, inventory, or whatever your core app sells or displays.
from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI(title="Product Service")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.security_db
products_collection = db.products

class Product(BaseModel):
    name: str
    price: float
    description: str

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.get("/api/v1/products")
async def list_products():
    products = []
    async for product in products_collection.find({}, {"_id": 0}):
        products.append(product)
    return {"products": products}

@app.post("/api/v1/products")
async def create_product(product: Product):
    await products_collection.insert_one(product.dict())
    return {"message": "Product created successfully"}