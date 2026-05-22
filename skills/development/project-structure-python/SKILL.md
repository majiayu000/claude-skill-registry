---
name: project-structure-python
description: >
  Structure Python projects with pyproject.toml, src layout, modern package managers
  (uv, rye, poetry), virtual environments, __init__.py, and namespace packages. Use
  when the user creates a new Python project, asks about project layout, configures
  packaging, sets up dependencies, or encounters import issues. Trigger when you see
  a Python project without proper structure.
---

# Python Project Structure

Set up Python projects with modern tooling and clear layout conventions. A well-structured
project prevents import headaches, simplifies packaging, and scales cleanly.

## When to Use
- User creates a new Python project or package
- User asks about project layout or packaging
- User encounters import errors or circular imports
- User sets up dependency management
- User configures linting, testing, or build tools

## Core Patterns

### Standard src Layout

The src layout prevents accidental imports of the uninstalled package and is the
recommended structure for libraries and applications.

```
my-project/
  pyproject.toml
  README.md
  src/
    my_project/
      __init__.py
      core/
        __init__.py
        models.py
        services.py
      api/
        __init__.py
        routes.py
        middleware.py
      utils/
        __init__.py
        helpers.py
  tests/
    __init__.py
    conftest.py
    test_models.py
    test_services.py
    test_routes.py
```

### pyproject.toml (Single Source of Truth)

`pyproject.toml` replaces `setup.py`, `setup.cfg`, `requirements.txt`, and tool-specific
config files. Everything in one place.

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A well-structured Python project"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "mypy>=1.10",
    "ruff>=0.5",
]

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Tool configuration -- all in one file
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers --cov=my_project"

[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "SIM", "TCH"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true

[tool.coverage.run]
source = ["src/my_project"]
branch = true

[tool.coverage.report]
fail_under = 80
```

### Package Manager Setup

#### uv (Recommended -- fastest)

```bash
# Create new project
uv init my-project
cd my-project

# Add dependencies
uv add httpx pydantic
uv add --dev pytest ruff mypy

# Run commands in virtual env
uv run pytest
uv run python -m my_project

# Lock dependencies
uv lock

# Sync environment from lock file
uv sync
```

#### rye

```bash
rye init my-project
cd my-project
rye add httpx pydantic
rye add --dev pytest ruff
rye sync
rye run pytest
```

#### poetry

```bash
poetry new my-project --src
cd my-project
poetry add httpx pydantic
poetry add --group dev pytest ruff
poetry install
poetry run pytest
```

### Virtual Environments

Always isolate project dependencies. Never install into the global Python.

```bash
# Standard venv (if not using uv/poetry/rye)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Verify isolation
which python  # Should point to .venv/bin/python
```

Add to `.gitignore`:
```
.venv/
__pycache__/
*.pyc
dist/
*.egg-info/
.mypy_cache/
.pytest_cache/
.ruff_cache/
.coverage
```

### __init__.py and Package Exports

Use `__init__.py` to define the public API of each package. Keep it minimal.

```python
# src/my_project/__init__.py
"""My Project -- a well-structured Python package."""

from my_project.core.models import User, Event
from my_project.core.services import UserService

__all__ = ["User", "Event", "UserService"]
```

```python
# src/my_project/core/__init__.py
# Can be empty -- just marks directory as a package
# Or re-export key names for convenience
from my_project.core.models import User, Event
```

### Namespace Packages (No __init__.py)

Use implicit namespace packages when you need to split a package across multiple
directories or distributions. Omit `__init__.py` entirely.

```
# Two separate distributions sharing the "mycompany" namespace
distribution-a/
  src/
    mycompany/          # No __init__.py
      billing/
        __init__.py
        invoices.py

distribution-b/
  src/
    mycompany/          # No __init__.py
      shipping/
        __init__.py
        tracking.py

# Both install into the same namespace
import mycompany.billing.invoices
import mycompany.shipping.tracking
```

### Configuration and Settings

```python
# src/my_project/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    log_level: str = "INFO"

    model_config = {"env_prefix": "APP_", "env_file": ".env"}

# Usage
settings = Settings()  # Reads APP_DATABASE_URL, APP_DEBUG, etc.
```

## Anti-Patterns

- **Flat layout without src/**: Causes the uninstalled package to shadow the installed
  one during development, leading to subtle import bugs.
- **requirements.txt as primary dependency spec**: Use `pyproject.toml` dependencies.
  Generate `requirements.txt` from lock files only for deployment if needed.
- **Wildcard imports in __init__.py**: `from .models import *` pollutes the namespace
  and breaks static analysis. Always use explicit imports and `__all__`.
- **Circular imports**: If module A imports from B and B imports from A, restructure.
  Extract shared code into a third module, or use late imports inside functions.
- **Global Python installs**: Never `pip install` into the system Python. Always use
  a virtual environment or tool-managed environment.

## Quick Reference

| Tool | Create | Add Dep | Run | Lock |
|---|---|---|---|---|
| uv | `uv init` | `uv add pkg` | `uv run cmd` | `uv lock` |
| rye | `rye init` | `rye add pkg` | `rye run cmd` | `rye lock` |
| poetry | `poetry new` | `poetry add pkg` | `poetry run cmd` | `poetry lock` |

| File | Purpose |
|---|---|
| `pyproject.toml` | Dependencies, build config, tool config |
| `src/pkg/__init__.py` | Package marker, public API exports |
| `tests/conftest.py` | Shared pytest fixtures |
| `.python-version` | Pin Python version for tools |
| `uv.lock` / `poetry.lock` | Reproducible dependency resolution |
