include .env
export

MAKEFLAGS += --no-print-directory

format:
	uv run ruff check --select I --fix . && uv run ruff format .

lint:
	uv run ruff check .

db-up:
	docker compose up -d --wait db

db-down:
	docker compose down db

psql:
	docker compose exec db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

psql-test:
	. ./.env.test; docker compose exec test-db psql -U $$POSTGRES_USER -d $$POSTGRES_DB

migrate:
	uv run alembic upgrade head

migrate-test:
	set -a; . ./.env.test; set +a; POSTGRES_HOST=localhost POSTGRES_PORT=5433 uv run alembic upgrade head

test-db-up:
	docker compose up -d --wait test-db
	$(MAKE) migrate-test

test-db-down:
	docker compose down test-db

test: test-db-up
	unset POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB; uv run pytest

run:
	uv run uvicorn service.main:app --reload
