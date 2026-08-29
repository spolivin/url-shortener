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
2. Run the tests:
   ```
   make test
   ```
   This starts `test-db` if it isn't already running, waits for it to be healthy, applies migrations, and runs `pytest`. Safe to re-run - it's a no-op to start an already-running `test-db` and to re-apply already-applied migrations.
3. Stop the test database when you're done:
   ```
   make test-db-down
   ```

`test-db` uses `tmpfs` for its data directory, so its contents don't survive a container restart/recreate - `make test` re-applies migrations automatically each time, so this is only a concern if you're inspecting the database directly (e.g. via `make psql-test`).

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
- `make test-db-up` / `make test-db-down` - start (and wait healthy + migrate) / stop `test-db`.
- `make test` - run the test suite (implies `test-db-up`).
- `make psql` - open a `psql` shell against the running Postgres container.
- `make psql-test` - open a `psql` shell against the running `test-db` container.
- `make lint` / `make format` - ruff.
- `make run` - run the app.

## Status

Core shorten + redirect flow works end-to-end, with test coverage for all three endpoints, including the `/shorten` retry-on-collision logic and click-count tracking on redirect. Not yet implemented: rate limiting.
