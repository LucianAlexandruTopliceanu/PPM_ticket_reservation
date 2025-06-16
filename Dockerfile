FROM python:3.9-slim

# Imposta le variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Installa le dipendenze di sistema (usa netcat-openbsd invece di netcat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Crea e imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia il progetto
COPY . .

# Esponi la porta
EXPOSE $PORT

# Comando per eseguire l'applicazione
CMD bash -c "python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT django_project.wsgi:application"