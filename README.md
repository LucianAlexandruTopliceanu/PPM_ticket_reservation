# Ticket Reservation System - REST API

![demo home](https://github.com/user-attachments/assets/3548a359-df81-4d50-a679-4961ca7e23c8)

Un sistema completo per la gestione di prenotazioni di biglietti per eventi, con autenticazione JWT e ruoli differenziati.

## 🚀 Funzionalità principali

- **Gestione eventi** (creazione, modifica, eliminazione)
- **Prenotazioni** con pagamento simulato
- **Autenticazione JWT** con ruoli:
  - **Utenti registrati**: Prenotano e gestiscono le proprie prenotazioni
  - **Organizzatori**: Creano e gestiscono i propri eventi
  - **Admin**: Accesso completo

## 📚 Documentazione API

Endpoint principali:

| Metodo | Endpoint                | Descrizione                      | Autenticazione |
|--------|-------------------------|----------------------------------|----------------|
| POST   | /api/auth/register      | Registrazione nuovo utente       | No             |
| POST   | /api/auth/login         | Login (ottieni JWT token)        | No             |
| GET    | /api/events/            | Lista eventi disponibili         | No             |
| POST   | /api/events/            | Crea nuovo evento                | Organizzatore  |
| POST   | /api/reservations/      | Crea prenotazione                | Utente         |
| GET    | /api/reservations/my/   | Lista prenotazioni utente        | Utente         |


## 🛠️ Tecnologie utilizzate

- **Backend**: Django + Django REST Framework
- **Autenticazione**: JWT (Simple JWT)
- **Database**: SQLite (sviluppo), PostgreSQL (produzione)
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Deploy**: Docker, Railway

## 🏗️ Struttura del progetto

<!-- TREEVIEW START -->
![struttura](https://github.com/user-attachments/assets/caae80d7-d33d-428a-ad81-f7345a1e3c4b)
<!-- TREEVIEW END -->


## 🚀 Installazione locale server API

1. Clona il repository
2. Crea e attiva un ambiente virtuale
3. Installa le dipendenze
4. Modifica in settings.py le informazioni del database con quelle locali dbsqlite
5. Esegui le migrazioni
6. Carica le fixtures : python manage.py loaddata db.json
7. Avvia il server di sviluppo
8. Accedi all'API all'indirizzo: http://localhost:8000/api/
9. Accedi all'API utilizzando il client test-api-full.html

## 🐳 Installazione locale server API Docker

1. Pull dell'immagine PostgreSQL
```
   docker pull postgres:13
 ```
3. Esegui il container PostgreSQL con le tue configurazioni
```
   docker run -d \
  --name ticket_db \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --health-cmd="pg_isready -U myuser -d mydatabase" \
  --health-interval=5s \
  --health-timeout=5s \
  --health-retries=5 \
  postgres:13
```

4. Pull della tua immagine web
```
   docker pull lualto/django-ticket-web:1.0
```
5. Esegui il container web collegandolo al DB
```
   docker run -d \
  --name ticket_web \
  -e DATABASE_URL="postgres://myuser:mypassword@ticket_db:5432/mydatabase" \
  --link ticket_db:db \
  -p 8000:8000 \
  lualto/django-ticket-web:1.0
```
6. (Opzionale) Carica dati iniziali 
```
docker exec -it ticket_web python manage.py loaddata db.json
```
7. Accedi all'API utilizzando il client test-api-full.html


## 🌐 Deployment

- Il progetto è deployato su [Railway](https://ppmticketreservation-production.up.railway.app/)
- Il databse è un database Postgres in esecuzione su Railway
- Per accedere come client al API utilizzare test-api-full.html modificando le variabili:
```js
   API_BASE_URL = 'https://ppmticketreservation-production.up.railway.app/api/auth/'
    
   EVENTS_API_URL = 'https://ppmticketreservation-production.up.railway.app/api/'
```
- **Credenziali demo:**

   - Admin: admin / testpassword
  
   - Organizzatore: staff / testpassword

   - Utente: utente / testpassword

## 🎯 Requisiti soddisfatti

- ✔️ 2 diverse app (users e tickets)
- ✔️ 2+ relazioni tra modelli (User-Event, Event-Reservation, Reservation-Payment)
- ✔️ Viste basate su classi generiche (generics.ListCreateAPIView, etc.)
- ✔️ 2+ livelli di permessi (Utente, Organizzatore, Admin)
- ✔️ Modello User esteso (CustomUser con campi aggiuntivi)
- ✔️ Client minimale incluso (test-api-full.html)
- 📄 Database pre-popolato

<div align="center"> <sub>Sviluppato per l'esercitazione di Back-end PPM 2025 - Università di Firenze</sub> </div> 
