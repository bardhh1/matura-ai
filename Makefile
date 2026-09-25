.PHONY: setup db-up db-down migrate seed backend frontend verify

setup:
	cd backend && python3.12 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
	cd frontend && npm ci

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

migrate:
	cd backend && .venv/bin/alembic upgrade head

seed:
	cd backend && .venv/bin/python scripts/seed_demo.py

backend:
	backend/.venv/bin/python backend/scripts/run.py

frontend:
	cd frontend && npm run dev

verify:
	cd backend && .venv/bin/ruff check app migrations tests scripts && .venv/bin/ruff format --check app migrations tests scripts && .venv/bin/pytest -q
	cd frontend && npm run build
