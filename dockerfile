FROM python:3.12-alpine

WORKDIR /app

COPY provided-tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8081"]