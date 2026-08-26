# url-shortener

A simple URL shortener built with FastAPI and Postgres.

## Stack

- FastAPI (async)
- SQLAlchemy (async, via asyncpg) + Alembic for migrations (via psycopg)
- Postgres, via Docker Compose

## Setup

1. Copy `.env.example` to `.env` and adjust credentials if needed.
2. Start Postgres:
   ```
   make db-up
   ```
3. Apply migrations:
   ```
   make migrate
   ```
4. Run the app:
   ```
   make run
   ```

## Endpoints

- `GET /health` - checks the app can reach the database.

  ```
  curl http://localhost:8000/health
  ```

- `POST /shorten` - create a short code for a URL.

  ```
  curl -X POST http://localhost:8000/shorten \
    -H "Content-Type: application/json" \
    -d '{"long_url": "https://example.com"}'
  ```

  Returns `{"short_code": "..."}`.

- `GET /{short_code}` - 302 redirect to the original URL, or 404 if not found.

  ```
  curl -i http://localhost:8000/<short_code>
  ```

## Makefile

- `make db-up` / `make db-down` - start/stop Postgres.
- `make migrate` - apply pending Alembic migrations.
- `make psql` - open a `psql` shell against the running Postgres container.
- `make lint` / `make format` - ruff.
- `make run` - run the app.

## Status

Core shorten + redirect flow works end-to-end. Not yet implemented: click-count tracking, tests, rate limiting.
