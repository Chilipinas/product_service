FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY product_purchase_service .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]