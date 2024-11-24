FROM python:3.10-slim

WORKDIR /app

COPY ./app /app/app
COPY requirements.txt /app/app/requirements.txt

RUN pip install --no-cache-dir -r /app/app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]