# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Install dependencies: `poetry install`
- Run application: `poetry run streamlit run main.py`
- Lint code: `poetry run ruff check .`
- Format code: `poetry run ruff format .`
- Type check: `poetry run mypy main.py`

## Code Style Guidelines
- Use Python 3.11+ typing annotations for all functions
- Document functions with docstrings following Google style
- Use snake_case for variables and functions
- Use PascalCase for classes
- Import order: standard library, third-party, project-specific
- Function return types should be specified (use `Any` from typing when appropriate)
- Error handling should use try/except blocks with specific exceptions
- Follow PEP 8 style guidelines for Python code
- Maximum line length: 88 characters
- Use f-strings for string formatting
- Structure Streamlit apps with clear section organization