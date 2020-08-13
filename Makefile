.PHONY: black lint test publish

format:
	isort --profile black .
	black .

lint:
	flake8

test:
	python -m pytest

publish:
	python setup.py publish
