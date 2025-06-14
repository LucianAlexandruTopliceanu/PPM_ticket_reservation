FROM python:3.9-slim

WORKDIR /app

# Installa le dipendenze di sistema necessarie
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copia e installa i requirements Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comando di avvio ottimizzato
CMD ["bash", "-c", "while ! nc -z db 5432; do sleep 2; done && \
     python manage.py migrate "]