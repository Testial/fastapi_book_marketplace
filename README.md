# FastAPI Book Marketplace

## About
This project is a FastAPI-based backend that implements a lightweight marketplace for selling books. The app allows creating and managing sellers and books, exposing a REST API for frontend integration. The project includes application configuration, Pydantic schemas, SQLAlchemy models with PostgreSQL persistence, routers, a Docker-based local development environment and pytest-powered tests for basic coverage.

## Key features
- REST API endpoints under `/api/v1/` for frontend integration.
- Input validation and serialization with Pydantic schemas.
- Persistence via SQLAlchemy ORM and PostgreSQL running in Docker.
- `.env`-driven configuration and a `settings` module for environment variables.
- Example HTTP requests for manual verification and pytest fixtures for DB testing.

## What was done
- Project refactored into `src/` and organized according to clean-architecture principles:
  - separated serializers, handlers, and DB models into dedicated packages;
  - added PostgreSQL support via Docker for development and tests;
  - added `.env` example and a `settings` module to centralize configuration;
  - configured pytest and database fixtures and added example tests for handlers.
- Provided `docker-compose.yml` and Docker PostgreSQL setup to simplify local environment.
- Included an `api_tests.http` file with sample requests to exercise endpoints manually.

## Tech stack
- Python
- FastAPI
- Pydantic (schemas / validation)
- SQLAlchemy (ORM)
- PostgreSQL (database, via Docker)
- Docker & docker-compose (local DB)
- pytest (testing)
- uvicorn (ASGI server)
- Dependencies listed in `requirements.txt`

## Repository (high-level)
```
.
├─ .env.example           # environment variables example
├─ docker-compose.yml
├─ docker/
│  └─ postgres/           # Docker setup for Postgres
├─ requirements.txt
├─ api_tests.http         # example HTTP requests for manual testing
└─ src/                   # application code (detailed structure below)
```

## Detailed `src/` structure
The `src` package contains the full application. Below is a detailed, typical layout adapted to this repository's conventions:

```
src/
├─ main.py                 # FastAPI app instance and startup hooks
├─ pytest.ini
├─ configurations/         # layer for storing configurations, constants, parameters and project settings
│  ├─ database.py
│  └─ settings.py
├─ models/                 # ORM models (SQLAlchemy) or data classes
│  ├─ base.py
│  ├─ books.py
│  └─ sellers.py
├─ schemas/                # Pydantic schemas for request/response validation and serialization
│  ├─ books.py
│  └─ sellers.py
├─ routers/                # Routers (endpoint definitions) for different API resources
│  └─ v1/
│     ├─ books.py
│     └─ sellers.py
└─ tests/                  # pytest tests and fixtures (DB fixtures included)
   ├─ conftest.py
   ├─ test_books.py
   └─ test_sellers.py
```

## How to run
Follow these steps for a typical local development run:

1. **Copy environment example**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set values (database credentials, host, port, etc.) as needed.

2. **Start PostgreSQL (Docker)**
   ```bash
   docker-compose up -d --build
   ```
   This starts the PostgreSQL service defined under `docker/postgres`. Wait a few seconds until the DB is ready.

3. **Install Python dependencies**

   It is recommended to use a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # on Unix/macOS
   pip install -r requirements.txt
   ```

4. **Run the application**

   From repository root:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
   ```
   The interactive API docs will be available at `http://127.0.0.1:8000/docs`.

5. **Run tests**

   The repo includes pytest and DB fixtures. Run:
   ```bash
   pytest -q
   ```
   Tests use fixtures to provide an isolated DB instance (see `tests/conftest.py`).

6. **Shutdown services**
   ```bash
   docker-compose down
   ```

## Example requests
Use the included `api_tests.http` (or a tool like curl / httpie / Postman) to exercise endpoints. The `api_tests.http` file contains prepared requests for the common flows.

## Testing
- Tests are configured with pytest and include fixtures for the database to allow reproducible integration tests.
- Run `pytest` to execute unit/integration tests. Tests and fixtures are located under `src/tests/`.