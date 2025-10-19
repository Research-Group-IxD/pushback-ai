.PHONY: help quality test clean

help:
	@echo "Makefile for the Push-Back AI Project"
	@echo ""
	@echo "Usage:"
	@echo "    make quality    - Run black, mypy, and pylint"
	@echo "    make test       - Run pytest"
	@echo "    make clean      - Remove temporary files"
	@echo ""

quality:
	@echo "Running code formatters and linters..."
	black src/ tests/
	mypy src/ tests/
	pylint src/ tests/

test:
	@echo "Running tests..."
	pytest

clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
