# Usa l'immagine ufficiale di Python
FROM python:3.9-slim

# Imposta le variabili d'ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Installa le dipendenze di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea e imposta la directory di lavoro
WORKDIR /app

# Installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il progetto
COPY . .

# Esponi la porta (Railway usa la variabile PORT)
EXPOSE $PORT

# Comando per eseguire l'applicazione
CMD bash -c "python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT myproject.wsgi:application"