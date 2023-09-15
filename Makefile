.PHONY: black lint test publish

format:
	poetry run isort --profile black .
	poetry run black .

lint:
	poetry run flake8

test:
	poetry run pytest

publish:
	poetry publish --build --dry-run
