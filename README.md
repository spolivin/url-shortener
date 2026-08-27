# url-shortener

A simple URL shortener built with FastAPI and Postgres.

## Stack

- FastAPI (async)
- SQLAlchemy (async, via asyncpg) + Alembic for migrations (via psycopg)
- Postgres, via Docker Compose

## Setup

1. Install dependencies:
   ```
   uv sync
   ```
2. Copy `.env.example` to `.env` and adjust credentials if needed.
3. Start Postgres:
   ```
   make db-up
   ```
4. Apply migrations:
   ```
   make migrate
   ```
5. Run the app:
   ```
   make run
   ```

## Testing

Tests run against a separate Postgres instance (`test-db`), kept isolated from the dev database so test runs never touch real data.

1. Copy `.env.test.example` to `.env.test` and adjust credentials if needed.
2. Start the test database:
   ```
   docker compose up -d test-db
   ```
3. Apply migrations to it:
   ```
   make migrate-test
   ```
4. Run the tests:
   ```
   uv run pytest
   ```

`test-db` uses `tmpfs` for its data directory, so its contents don't survive a container restart/recreate — migrations need to be re-applied after that.

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
- `make migrate-test` - apply pending Alembic migrations to `test-db`.
- `make psql` - open a `psql` shell against the running Postgres container.
- `make psql-test` - open a `psql` shell against the running `test-db` container.
- `make lint` / `make format` - ruff.
- `make run` - run the app.

## Status

Core shorten + redirect flow works end-to-end. `GET /health` has test coverage; `/shorten` and `/{short_code}` do not yet. Not yet implemented: click-count tracking, rate limiting.
