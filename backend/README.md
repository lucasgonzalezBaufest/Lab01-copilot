# Backend – JWT Auth API

A minimal **FastAPI** service that implements JSON Web Token (JWT) authentication.  
Dependencies are managed with **Poetry**.

---

## Features

| Endpoint | Method | Description |
|---|---|---|
| `/token` | POST | Obtain an access token + refresh token |
| `/token/refresh` | POST | Exchange a refresh token for a new token pair |
| `/me` | GET | Return the current authenticated user |
| `/docs` | GET | Interactive Swagger UI |

- Access token expires in **300 seconds**.  
- Refresh token expires in **3600 seconds**.

---

## Requirements

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)

---

## Local development

```bash
# 1. Install dependencies
cd backend
poetry install

# 2. Start the server
poetry run uvicorn app.main:app --reload --port 8000
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>.

---

## Usage

### 1. Obtain tokens

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Response:**

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2. Access a protected endpoint

```bash
curl http://localhost:8000/me \
  -H "Authorization: Bearer <access_token>"
```

**Response:**

```json
{"username": "admin"}
```

### 3. Refresh the token pair

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

**Response:**

```json
{
  "access_token": "<new_JWT>",
  "refresh_token": "<new_JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

## Docker

### Build the image

```bash
cd backend
docker build -t jwt-auth-api .
```

### Run the container

```bash
docker run -p 8000:8000 \
  -e SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" \
  jwt-auth-api
```

The API will be accessible at <http://localhost:8000>.

---

## Running tests

```bash
cd backend
poetry run pytest -v
```

---

## Project structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── auth.py       # JWT helpers and user verification
│   └── main.py       # FastAPI application and routes
├── tests/
│   └── test_main.py  # Automated tests
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## Security notes

> **Important:** The `SECRET_KEY` in `app/auth.py` is a placeholder.  
> Replace it with a strong, randomly generated secret before deploying to production.  
> You can generate one with:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```
