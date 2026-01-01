.PHONY: lint test run clean

lint:
	poetry run ruff check . --fix
	poetry run ruff format .
	poetry run mypy .

test:
	poetry run pytest

run:
	poetry run python -m src.sequential_agents.agent

adk:
	cd src && adk web

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
