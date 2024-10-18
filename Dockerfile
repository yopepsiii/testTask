FROM python:3.12-alpine

WORKDIR /usr/src/testAPI

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "alembic upgrade head ; uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload"]
