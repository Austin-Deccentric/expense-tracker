# Expense Tracker

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](#) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](#)

Simple command-line expense tracker.

## Project structure

- `tracker/` - application package
  - `core.py` - main application logic
  - `models.py` - data models
  - `storage.py` - persistence layer
  - `__main__.py` - package entrypoint
- `tests/` - unit tests
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Sample Usage

```bash
python -m tracker add 12.50 food "Lunch"
python -m tracker list
python -m tracker summary
python -m tracker
```

## Running tests

Run the test suite with pytest:

```bash
pytest -v
```

## Notes

This repository is set up for simple unit testing and development. See `tests/` for examples of how functions are exercised.

