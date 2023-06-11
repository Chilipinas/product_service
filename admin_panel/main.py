from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import psycopg2

app = FastAPI()

# Модель данных для создания и обновления продукта
class ProductCreateUpdate(BaseModel):
    name: str
    description: str

# Получить соединение с PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(
        host="POSTGRES_HOST",
        port=5432,
        dbname="POSTGRES_DB",
        user="POSTGRES_USER",
        password="POSTGRES_PASSWORD"
    )
    return connection

# Создать новый продукт
@app.post("/products")
async def create_product(product: ProductCreateUpdate):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        insert_query = "INSERT INTO products (name, description) VALUES (%s, %s) RETURNING id"
        cursor.execute(insert_query, (product.name, product.description))
        product_id = cursor.fetchone()[0]
        connection.commit()
        return {"id": product_id, "name": product.name, "description": product.description}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to create product")
    finally:
        cursor.close()
        connection.close()

# Обновить существующий продукт
@app.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductCreateUpdate):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        update_query = "UPDATE products SET name = %s, description = %s WHERE id = %s"
        cursor.execute(update_query, (product.name, product.description, product_id))
        connection.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Product not found")

        return {"id": product_id, "name": product.name, "description": product.description}
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to update product")
    finally:
        cursor.close()
        connection.close()