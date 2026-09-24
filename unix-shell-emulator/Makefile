.PHONY: test run clean

run:
	python3 -m src.main

test:
	python3 -m pytest

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
