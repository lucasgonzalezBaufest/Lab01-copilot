# Lab01 – JWT Auth App

Aplicación full-stack de autenticación con **JWT** compuesta por:

- **Backend**: API REST construida con [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+), gestionada con [Poetry](https://python-poetry.org/).
- **Frontend**: SPA construida con [React 19](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/) + [Vite](https://vite.dev/).

---

## Descripción del aplicativo

El frontend presenta un formulario de inicio de sesión. Al ingresar las credenciales correctas, se realiza una petición `POST /token` al backend, que devuelve un par de tokens JWT (access + refresh). El resultado se muestra en pantalla con un mensaje de bienvenida o de error según corresponda.

### Credenciales de prueba

| Usuario | Contraseña |
|---------|------------|
| `admin` | `admin123` |

---

## Requisitos previos

| Herramienta | Versión mínima |
|-------------|---------------|
| Python | 3.11 |
| Poetry | cualquiera reciente |
| Node.js | 18+ |
| npm | 9+ |

---

## Levantar el servidor

### 1. Backend (FastAPI – puerto 8000)

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

La API quedará disponible en <http://localhost:8000>.  
Documentación interactiva (Swagger UI): <http://localhost:8000/docs>.

### 2. Frontend (React/Vite – puerto 5173)

En una terminal separada:

```bash
cd frontend
npm install
npm run dev
```

La aplicación quedará disponible en <http://localhost:5173>.

> **Importante:** el backend debe estar corriendo antes de usar el frontend, ya que éste realiza peticiones a `http://localhost:8000`.

---

## Estructura del proyecto

```
Lab01-copilot/
├── backend/              # API FastAPI con autenticación JWT
│   ├── app/
│   │   ├── auth.py       # Helpers JWT y verificación de usuario
│   │   └── main.py       # Aplicación FastAPI y rutas
│   ├── tests/
│   │   └── test_main.py  # Tests automatizados
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── README.md
├── frontend/             # SPA React + TypeScript + Vite
│   ├── src/
│   │   ├── App.tsx       # Componente principal (formulario de login)
│   │   └── main.tsx      # Punto de entrada
│   ├── package.json
│   └── README.md
└── README.md             # Este archivo
```

---

## Endpoints del backend

| Endpoint | Método | Descripción |
|---|---|---|
| `/token` | POST | Obtener access token + refresh token |
| `/token/refresh` | POST | Renovar el par de tokens con un refresh token válido |
| `/me` | GET | Retorna el usuario autenticado actualmente |
| `/docs` | GET | Swagger UI interactivo |

- El **access token** expira en **300 segundos**.
- El **refresh token** expira en **3600 segundos**.

---

## Docker (solo backend)

```bash
cd backend
docker build -t jwt-auth-api .
docker run -p 8000:8000 \
  -e SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')" \
  jwt-auth-api
```

---

## Tests

```bash
cd backend
poetry run pytest -v
```

---

## Notas de seguridad

> La `SECRET_KEY` definida en `backend/app/auth.py` es un valor de ejemplo.  
> En un entorno productivo, reemplazarla por una clave segura generada con:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```
