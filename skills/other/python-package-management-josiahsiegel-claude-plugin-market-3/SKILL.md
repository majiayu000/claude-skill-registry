---
name: python-package-management
description: Complete Python package management system. PROACTIVELY activate for: (1) uv package manager (10-100x faster), (2) pyproject.toml configuration, (3) Virtual environment setup, (4) Dependency management with uv.lock, (5) Ruff linting and formatting, (6) src layout project structure, (7) Publishing to PyPI, (8) pip and requirements.txt. Provides: uv commands, pyproject.toml templates, ruff config, pre-commit setup. Ensures modern Python project setup with fast tooling.
---

## Quick Reference

| uv Command | Purpose |
|------------|---------|
| `uv init my-project` | Create new project |
| `uv add <package>` | Add dependency |
| `uv add --dev <package>` | Add dev dependency |
| `uv sync` | Install all dependencies |
| `uv run <command>` | Run in virtual env |
| `uv lock --upgrade` | Update all deps |
| `uv python install 3.13` | Install Python version |

| Tool | Command | Speed |
|------|---------|-------|
| uv | `uv add requests` | 10-100x faster |
| pip | `pip install requests` | Baseline |

| ruff Command | Purpose |
|--------------|---------|
| `ruff check .` | Lint code |
| `ruff check --fix .` | Auto-fix issues |
| `ruff format .` | Format code |

| Project Layout | Recommended |
|----------------|-------------|
| src layout | `src/my_package/` |
| Tests | `tests/` |
| Config | `pyproject.toml` |

## When to Use This Skill

Use for **project setup and dependencies**:
- Starting new Python projects
- Setting up uv for fast package management
- Configuring pyproject.toml
- Setting up linting with ruff
- Publishing packages to PyPI

**Related skills:**
- For CI/CD: see `python-github-actions`
- For testing: see `python-testing`
- For type hints config: see `python-type-hints`

---

# Python Package Management (2025)

## Overview

Modern Python package management centers around `uv` (the fast Rust-based tool), `pip`, and `pyproject.toml`. This guide covers best practices for dependency management, virtual environments, and project configuration.

## uv - The Modern Package Manager

### Why uv?

- **10-100x faster** than pip (written in Rust)
- Replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv
- Automatic virtual environment management
- Lockfile support for reproducibility
- ~200x faster venv creation

### Installation

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# pip (works everywhere)
pip install uv

# Homebrew
brew install uv
```

### Quick Start

```bash
# Create new project
uv init my-project
cd my-project

# Add dependencies
uv add requests fastapi pydantic

# Add dev dependencies
uv add --dev pytest ruff mypy

# Sync environment (install all dependencies)
uv sync

# Run commands in the environment
uv run python main.py
uv run pytest
```

### Basic Commands

```bash
# Package management
uv add <package>              # Add dependency
uv add <package>==1.0.0       # Specific version
uv add --dev <package>        # Dev dependency
uv remove <package>           # Remove dependency
uv sync                       # Sync environment with lockfile

# Virtual environments
uv venv                       # Create .venv
uv venv --python 3.12         # Specific Python version
uv venv my-env                # Named environment

# pip compatibility
uv pip install <package>      # Install (faster pip)
uv pip install -r requirements.txt
uv pip freeze > requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# Python management
uv python install 3.13        # Install Python version
uv python list                # List installed versions
uv python pin 3.12            # Pin project Python version

# Running
uv run <command>              # Run in virtual env
uv run --with httpx python    # Run with temporary package
```

### pyproject.toml with uv

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "httpx>=0.25.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

### uv.lock

```bash
# Lockfile is auto-generated and should be committed
# Contains exact versions for reproducibility

# Update all dependencies
uv lock --upgrade

# Update specific package
uv lock --upgrade-package requests

# Install from lockfile only
uv sync --frozen
```

## Project Structure

### Recommended: src Layout

```
my-project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   └── test_models.py
├── docs/
│   └── index.md
├── pyproject.toml
├── uv.lock
├── README.md
├── LICENSE
└── .gitignore
```

### Why src Layout?

1. **Prevents import confusion** - Can't accidentally import from project root
2. **Forces installation** - Must install package to test
3. **Cleaner distributions** - Only package code in wheels
4. **Semantic clarity** - Clear separation of code, tests, docs

### Flat Layout (for simpler projects)

```
my-project/
├── my_package/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── pyproject.toml
└── README.md
```

## pyproject.toml Complete Reference

```toml
[project]
name = "my-project"
version = "1.0.0"
description = "A comprehensive Python project"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
keywords = ["python", "example", "package"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
authors = [
    {name = "Your Name", email = "you@example.com"}
]
maintainers = [
    {name = "Maintainer", email = "maintainer@example.com"}
]

dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "sqlalchemy>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
    "pre-commit>=3.0.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]
all = ["my-project[dev,docs]"]

[project.scripts]
my-cli = "my_package.cli:main"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins:Plugin1"

[project.urls]
Homepage = "https://github.com/user/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/user/my-project"
Changelog = "https://github.com/user/my-project/blob/main/CHANGELOG.md"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

# Ruff configuration
[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",     # pycodestyle errors
    "W",     # pycodestyle warnings
    "F",     # Pyflakes
    "I",     # isort
    "B",     # flake8-bugbear
    "C4",    # flake8-comprehensions
    "UP",    # pyupgrade
    "ARG",   # flake8-unused-arguments
    "SIM",   # flake8-simplify
]
ignore = [
    "E501",  # line too long (handled by formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["my_package"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

# Mypy configuration
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# Pytest configuration
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--cov=src/my_package",
    "--cov-report=term-missing",
]

# Coverage configuration
[tool.coverage.run]
branch = true
source = ["src/my_package"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

## Ruff - Linting and Formatting

### Why Ruff?

- **10-100x faster** than Flake8, Black combined
- Single tool for linting AND formatting
- 800+ built-in rules
- Auto-fix capabilities
- Written in Rust (by Astral, same as uv)

### Basic Usage

```bash
# Linting
ruff check .                   # Check for issues
ruff check --fix .             # Auto-fix issues
ruff check --watch .           # Watch mode

# Formatting
ruff format .                  # Format all files
ruff format --check .          # Check formatting

# Both
ruff check --fix . && ruff format .
```

### Configuration

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented code)
    "PL",     # Pylint
    "PERF",   # Perflint
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "PLR0913", # too many arguments
]

# Per-file ignores
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # Allow assert in tests
"__init__.py" = ["F401"]    # Allow unused imports

[tool.ruff.lint.isort]
known-first-party = ["my_package"]
force-single-line = true

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - types-requests
```

## pip and requirements.txt

### When to Use pip

- Production environments requiring stability
- Legacy projects
- Simple scripts without complex dependencies

### requirements.txt Best Practices

```txt
# requirements.txt - Pinned versions for production
fastapi==0.109.0
pydantic==2.5.3
sqlalchemy==2.0.25
httpx==0.26.0

# requirements-dev.txt
-r requirements.txt
pytest==8.0.0
ruff==0.1.14
mypy==1.8.0
```

### Generating requirements.txt

```bash
# From uv
uv pip compile pyproject.toml -o requirements.txt
uv pip compile pyproject.toml --extra dev -o requirements-dev.txt

# From pip-tools
pip-compile pyproject.toml -o requirements.txt
pip-compile pyproject.toml --extra dev -o requirements-dev.txt

# Freeze current environment (not recommended for reproducibility)
pip freeze > requirements.txt
```

## Virtual Environment Best Practices

### Location

```bash
# Recommended: Project-local .venv
project/
├── .venv/        # Virtual environment here
├── src/
├── tests/
└── pyproject.toml

# uv creates .venv by default
uv venv

# Explicit location
uv venv .venv
python -m venv .venv
```

### .gitignore

```gitignore
# Virtual environments
.venv/
venv/
ENV/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Distribution
build/
dist/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.mypy_cache/

# Ruff
.ruff_cache/
```

### Activation (when needed)

```bash
# Usually not needed with uv - just use `uv run`

# Linux/macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat

# Deactivate
deactivate
```

## Publishing Packages

### Build and Publish

```bash
# Build with uv
uv build

# Publish to PyPI
uv publish

# Or with twine
pip install twine
twine upload dist/*

# Test PyPI first
twine upload --repository testpypi dist/*
```

### Version Management

```toml
# pyproject.toml - dynamic version from __init__.py
[project]
dynamic = ["version"]

[tool.hatch.version]
path = "src/my_package/__init__.py"
```

```python
# src/my_package/__init__.py
__version__ = "1.0.0"
```
