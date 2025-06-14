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
- **API RESTful** documentata

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

## 🏗️ Struttura del progetto

<!-- TREEVIEW START -->
![struttura](https://github.com/user-attachments/assets/caae80d7-d33d-428a-ad81-f7345a1e3c4b)
<!-- TREEVIEW END -->


## 🚀 Installazione locale server API

1. Clona il repository
2. Crea e attiva un ambiente virtuale
3. Installa le dipendenze
4. Esegui le migrazioni
5. Carica le fixtures in ordine: python manage.py loaddata users.json tickets.json
6. Avvia il server di sviluppo
7. Accedi all'API all'indirizzo: http://localhost:8000/api/
8. Accedi al client utilizzando test-api-full.html

## 🌐 Deployment

Il progetto è deployato su Railway <!-- Sostituisci con il tuo link -->

- **Credenziali demo:** 

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

## Il repository include un file db.sqlite3 con:

    5 eventi di esempio

    3 utenti demo (admin, organizzatore, utente normale)

    10 prenotazioni di test


<div align="center"> <sub>Sviluppato per l'esercitazione di Back-end PPM 2025 - Università di Firenze</sub> </div> 
