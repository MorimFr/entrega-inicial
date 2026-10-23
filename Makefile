.PHONY: install run lint test test-docker

install:
	python -m pip install -e ".[dev]"

run:
	uvicorn campusflow.api:app --reload

lint:
	python -m ruff check .

test:
	python scripts/run_harness.py

test-docker:
	docker compose --profile test run --rm --build tests

