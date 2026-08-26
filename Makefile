include .env
export

format:
	uv run ruff check --select I --fix . && uv run ruff format .

lint:
	uv run ruff check .

db-up:
	docker compose up -d

db-down:
	docker compose down

psql:
	docker compose exec db psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

migrate:
	uv run alembic upgrade head

run:
	uv run uvicorn service.main:app --reload
