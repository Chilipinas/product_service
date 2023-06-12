import psycopg2
from elasticsearch import Elasticsearch


# Получить соединение с PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(
        host="POSTGRES_HOST",
        port="POSTGRES_PORT",
        dbname="POSTGRES_DB",
        user="POSTGRES_USER",
        password="POSTGRES_PASSWORD"
    )
    return connection

# Получить соединение с Elasticsearch
def get_es_connection():
    connection = Elasticsearch(hosts=[{"host": "ELASTICSEARCH_HOST", "port": "ELASTICSEARCH_PORT"}])
    return connection

# Перенести данные о продуктах из PostgreSQL в Elasticsearch
def etl_process():
    pg_connection = get_db_connection()
    es_connection = get_es_connection()

    try:
        pg_cursor = pg_connection.cursor()

        # Получить все продукты из PostgreSQL
        select_query = "SELECT id, name, description FROM products"
        pg_cursor.execute(select_query)
        products = pg_cursor.fetchall()

        # Загрузить продукты в Elasticsearch
        for product in products:
            product_id, product_name, product_description = product

            # Индексировать продукт в Elasticsearch
            es_connection.index(
                index="products",
                id=product_id,
                body={"name": product_name, "description": product_description}
            )

        pg_cursor.close()
    except Exception as e:
        raise Exception("Failed to perform ETL process")
    finally:
        pg_connection.close()
        es_connection.close()

# Запустить ETL процесс
etl_process()