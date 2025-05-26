.PHONY: install-precommit lint format type-check check-all

install-precommit:
	pre-commit install
	pre-commit autoupdate

lint:
	ruff check .

format:
	black .
	ruff format .

type-check:
	mypy src

check-all: lint format type-check
