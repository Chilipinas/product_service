from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
from models import Product, Base

app = FastAPI()

# Database initialization
Base.metadata.create_all(bind=engine)

class ProductCreate(BaseModel):
    name: str
    description: str

class ProductPurchase(BaseModel):
    product_id: int
    quantity: int

@app.get("/")
def read_root():
    return {"Hello": "Product Purchase Service"}

# API endpoints for product purchase service
@app.get("/products/{product_id}")
def get_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/products")
def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.post("/products/{product_id}/purchase")
def purchase_product(product_id: int, purchase: ProductPurchase):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < purchase.quantity:
        raise HTTPException(status_code=400, detail="Insufficient quantity")
    product.quantity -= purchase.quantity
    db.commit()
    db.close()
    return {"message": f"Purchased product with ID: {product_id}"}

@app.get("/products/search")
def search_products(query: str):
    # Call product search service to search products
    return {"message": f"Searching products for query: {query}"}