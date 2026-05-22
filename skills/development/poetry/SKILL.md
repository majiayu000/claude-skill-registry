---
name: poetry
description: >-
  Manage Python projects with Poetry. Use when a user asks to manage Python
  dependencies, create virtual environments, publish packages to PyPI,
  handle dependency resolution, or set up a Python project structure.
license: Apache-2.0
compatibility: 'Python 3.8+'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - poetry
    - python
    - dependencies
    - packaging
    - virtual-environment
---

# Poetry

## Overview

Poetry is a Python dependency manager and build tool. It handles virtual environments, dependency resolution (with a lock file), project scaffolding, and PyPI publishing. The modern replacement for pip + setuptools + virtualenv.

## Instructions

### Step 1: New Project

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new my-api
cd my-api

# Or init in existing directory
poetry init
```

### Step 2: Manage Dependencies

```bash
# Add dependencies
poetry add fastapi uvicorn sqlalchemy
poetry add pydantic-settings

# Add dev dependencies
poetry add --group dev pytest pytest-asyncio pytest-cov ruff mypy

# Remove
poetry remove requests

# Update
poetry update                  # update all within constraints
poetry update fastapi          # update specific package
poetry lock                    # regenerate lock file without installing
```

### Step 3: pyproject.toml

```toml
# pyproject.toml — Project configuration
[tool.poetry]
name = "my-api"
version = "1.0.0"
description = "Project management API"
authors = ["Team <team@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110"
uvicorn = {extras = ["standard"], version = "^0.27"}
sqlalchemy = "^2.0"
pydantic-settings = "^2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-asyncio = "^0.23"
pytest-cov = "^4.1"
ruff = "^0.3"
mypy = "^1.8"

[tool.poetry.scripts]
serve = "my_api.main:start"
migrate = "my_api.db:run_migrations"

[tool.ruff]
target-version = "py311"
line-length = 100

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### Step 4: Use

```bash
# Activate virtual environment
poetry shell

# Run without activating
poetry run python main.py
poetry run pytest
poetry run serve              # custom script from pyproject.toml

# Export for Docker (no Poetry needed in container)
poetry export -f requirements.txt -o requirements.txt --without-hashes

# Build and publish to PyPI
poetry build
poetry publish
```

## Guidelines

- Always commit `poetry.lock` — ensures reproducible installs across environments.
- Use `poetry export` for Docker — don't install Poetry in production containers.
- Group dev dependencies with `--group dev` — they're excluded from production installs.
- `poetry.lock` resolves ALL transitive dependencies — no more "works on my machine."
- Alternative: `uv` (from Astral, makers of Ruff) — 10-100x faster, compatible with pip/Poetry.
