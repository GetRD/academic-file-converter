.PHONY: black lint test

format:
	black .

lint:
	flake8

test:
	python -m pytest
