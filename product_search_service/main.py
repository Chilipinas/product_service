import os

from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from pydantic import BaseModel

from database import SessionLocal, engine
from models import Product, Base

app = FastAPI()

# Database initialization
Base.metadata.create_all(bind=engine)

class ProductSearch(BaseModel):
    query: str


# API endpoint to search products by name or description
@app.get("/products")
def search_products(query: str):
    db = SessionLocal()
    products = db.query(Product).filter(
        (Product.name.contains(query)) | (Product.description.contains(query))
    ).all()
    db.close()
    return products

@app.post("/products/search")
def search_products_es(search: ProductSearch):
    es = Elasticsearch(host=os.environ.get("ELASTICSEARCH_HOST"), port=os.environ.get("ELASTICSEARCH_PORT"))
    result = es.search(index="products", body={"query": {"match": {"name": search.query}}})
    hits = result["hits"]["hits"]
    products = []
    for hit in hits:
        products.append(hit["_source"])
    return products