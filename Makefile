.PHONY: black lint test

format:
	isort --profile black .
	black .

lint:
	flake8

test:
	python -m pytest
