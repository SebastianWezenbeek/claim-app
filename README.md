# Claim Portal

A simple claim management system with a **Python FastAPI backend** and a **PostgreSQL (or SQLite) database**.  
Customers can submit order claims via an API, and merchants can log in to view and update claims.

---

## Features
- **Customers**
  - Submit a claim (`/claim`) with order details.
  - Data stored in SQL database.
- **Merchants**
  - Login endpoint (`/login`) with session cookies.
  - List claims (`/claims`).
  - Update claim status (`/claims/{id}/status`).
- **Database**
  - Uses `SQLModel` (SQLAlchemy + Pydantic).
  - Supports Postgres in Docker or SQLite locally.
- **Auth**
  - Session-based auth for merchants.
  - Passwords hashed with scrypt.

---

## Instructions

Build your image with docker:
```
docker build -t {claim-api}
```
Run your container:
```
docker run -p 8000:8000 {claim-api}
```

## Development Usage
Send a POST request to create a merchant before logging in:
```
curl -X POST \
  -F 'email={admin@example.com}' \
  -F 'password={admin}' \
  http://localhost:8000/seed-merchant
```

