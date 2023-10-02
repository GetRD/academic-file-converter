.PHONY: black lint test type publish

format:
	poetry run isort --profile black .
	poetry run black .

lint:
	poetry run flake8

test:
	poetry run pytest

type:
	poetry run pyright

publish:
	poetry publish --build --dry-run
