---
name: python-project
description: Use whenever working on a python project. Manage Python projects using uv package manager with modern Python project structure.
---

# UV Project Management

Guide for managing Python projects using the uv package manager with proper understanding of modern Python project structures.

## Key Concepts

### Fetch Versions of a package

For newly added dependency or when need to upgrade the version of a dependency, use pip to fetch versions.

**Use `uv pip index versions <package>` to fetch versions**

### Dependency Groups vs Optional Dependencies

Modern Python projects using uv should use `dependency-groups` instead of `[project.optional-dependencies]`:

**Use `[dependency-groups]`** (PEP 735):
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.0",
    "ruff>=0.14.0",
]
test = [
    "pytest>=9.0.0",
    "pytest-cov>=4.0.0",
]
```

**Avoid `[project.optional-dependencies]`**:
```toml
# ❌ Old pattern - don't use with uv
[project.optional-dependencies]
dev = ["pytest>=9.0.0"]
```

### Installing Dependency Groups

Install specific dependency groups:
```bash
uv sync --group dev
uv sync --group test
```

Install all groups:
```bash
uv sync --all-groups
```

Install without any groups:
```bash
uv sync --no-dev
```

## Common Patterns

### Basic pyproject.toml Structure

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[dependency-groups]
dev = [
    "pytest>=9.0.0",
    "ruff>=0.14.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

### Project Initialization

Create new project:
```bash
uv init my-project
cd my-project
```

Add dependencies:
```bash
# Production dependency
uv add requests

# Dev dependency
uv add --group dev pytest
```

### Running Commands

Run Python with project dependencies:
```bash
uv run python script.py
uv run pytest
```

Run installed tools:
```bash
uv run ruff check .
uv run mypy src/
```

### Syncing Dependencies

Sync all dependencies and groups:
```bash
uv sync --all-groups
```

Lock dependencies without installing:
```bash
uv lock
```

## Migration from Old Patterns

When updating projects from optional-dependencies to dependency-groups:

1. **Rename section**:
   ```toml
   # Change from:
   [project.optional-dependencies]
   # To:
   [dependency-groups]
   ```

2. **Update installation commands**:
   ```bash
   # Change from:
   pip install -e ".[dev]"
   # To:
   uv sync --group dev
   ```

3. **Update CI/CD scripts** to use `uv sync --all-groups` or specific groups

## Pytest

use pytest for testing. place tests under `./tests/`. And never create './tests/__init__.py`

Also follow the no `__init__.py` convention of pytest, that's no `__init__.py` in all subdirectories in `./tests`.

If anything shall be shared, use conftest.py.

options in pyproject.toml:

```toml
[tool.pytest]
addopts = ["--import-mode=importlib"]
pythonpath = ["src"]
testpaths = ["tests"]

```

Do **NOTE** that don't create folders in tests that are the same name with your bebing tested package.

So this file structure is **NOT** allowed cause it will shadow your package.

```
src/app/__init__.py
src/app/mymodule.py
tests/app/__init__.py
tests/app/test_mymodule.py # this will shadow and fail to import app.mymodule
```

## pytest fixtures

fixtures are shared test objects among all tests. 

use `@pytest.fixture def some_fixture()` to create a fixture.

declare tests with args of the same name to request the fixture. def test

```python
@pytest.fixture
def sample_data1():
    reutrn "a"

@pytest.fixture
def sample_data(sample_data1):
    """fixture can also request another fixture"""
    return f"hello {sample_data1)"

def test_ok(sample_data):
    assert "hello a" == sample_data
```

## test asset files with fixture

use `tests/conftest.py` to manage shared fixtures, and also it's a common pattern to provide file paths in conftest.py as fixtures.

The rational is you have stable file path handling if you do all the relative paths in a single conftest.py file.

```python
import pytest
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """Returns the absolute path to the directory containing test assets."""
    return Path(__file__).parent / "data"

@pytest.fixture
def sample_json(test_data_dir):
    """Provides the path to a specific asset."""
    return test_data_dir / "sample_input.json"
```

## Best Practices

1. **Always use dependency-groups** for dev/test/docs dependencies with uv
2. **Pin major versions** in dependencies: `package>=1.0.0,<2.0.0`
3. **Use uv.lock** for reproducible environments (committed to git)
4. **Run via uv run** to ensure correct environment: `uv run pytest` not `pytest`
5. **Group related dependencies**: separate dev, test, docs, lint groups as needed

## Common Commands Reference

```bash
# Project setup
uv init              # Initialize new project
uv sync              # Install dependencies from pyproject.toml
uv sync --all-groups # Install with all dependency groups

# Dependency management
uv add package       # Add production dependency
uv add --group dev package  # Add to dependency group
uv remove package    # Remove dependency
uv lock              # Update uv.lock file

# Running code
uv run python script.py    # Run Python with project deps
uv run pytest             # Run tests
uv run --with package cmd # One-off dependency

# Environment info
uv pip list          # List installed packages
uv pip show package  # Show package details
```

## Troubleshooting

**Issue**: Old `pip install -e ".[dev]"` pattern doesn't work
- **Solution**: Use `uv sync --group dev` instead

**Issue**: Dependencies not found when running scripts
- **Solution**: Use `uv run python script.py` instead of `python script.py`

**Issue**: Need to add dependency to specific group
- **Solution**: `uv add --group dev package-name`
