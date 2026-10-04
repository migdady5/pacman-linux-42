PYTHON = python3
CONFIG = config.json

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install vendor/mazegenerator-2.1.0-py3-none-any.whl

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
