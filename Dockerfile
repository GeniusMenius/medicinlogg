FROM python:3.11-slim

WORKDIR /app

# Hämta dependencies från app/
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera all appkod
COPY app/ .

EXPOSE 5000

CMD ["python", "main.py"]
