---
name: python3-packaging
description: Configure pyproject.toml and Python packaging for distribution. Use when setting up a new Python package, when configuring build tools and dependencies, or when preparing a project for PyPI publishing.
user-invocable: true
argument-hint: "[project-path]"
---

# Python Packaging Configuration

The model configures modern Python packaging using pyproject.toml and PEP standards.

## Arguments

$ARGUMENTS

## Instructions

1. **Analyze existing project** structure and configuration
2. **Create or update** pyproject.toml with complete configuration
3. **Configure tools** (ruff, mypy, pytest, hatch/setuptools)
4. **Set up dependencies** with proper version constraints
5. **Verify configuration** by running build

---

## Modern Packaging Standards

### PEP References

| PEP                                          | Standard           | Description                          |
| -------------------------------------------- | ------------------ | ------------------------------------ |
| [PEP 517](https://peps.python.org/pep-0517/) | Build system       | Specifies build-backend interface    |
| [PEP 518](https://peps.python.org/pep-0518/) | Build requirements | Specifies [build-system] table       |
| [PEP 621](https://peps.python.org/pep-0621/) | Project metadata   | Specifies [project] table            |
| [PEP 660](https://peps.python.org/pep-0660/) | Editable installs  | Specifies editable install mechanism |
| [PEP 723](https://peps.python.org/pep-0723/) | Inline metadata    | For standalone scripts               |

---

## Complete pyproject.toml Template

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "my-package"
version = "0.1.0"
description = "A brief description of the package"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
authors = [
    { name = "Author Name", email = "author@example.com" }
]
keywords = ["keyword1", "keyword2"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]

dependencies = [
    "typer>=0.15.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.12.0",
    "pytest-asyncio>=0.23.0",
    "mypy>=1.8.0",
    "ruff>=0.9.0",
]

[project.scripts]
my-cli = "my_package.cli:app"

[project.urls]
Documentation = "https://github.com/user/my-package#readme"
Issues = "https://github.com/user/my-package/issues"
Source = "https://github.com/user/my-package"

# ============================================================================
# Tool Configuration
# ============================================================================

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.ruff]
target-version = "py311"
line-length = 100
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
    "PL",     # pylint
    "RUF",    # Ruff-specific rules
    "ANN",    # flake8-annotations
    "D",      # pydocstyle
    "S",      # flake8-bandit (security)
    "T20",    # flake8-print
]

ignore = [
    "D100",   # Missing docstring in public module
    "D104",   # Missing docstring in public package
    "D107",   # Missing docstring in __init__
    "ANN101", # Missing type annotation for self
    "ANN102", # Missing type annotation for cls
]

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "D", "ANN", "PLR2004"]
"scripts/**" = ["T201", "S"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_any_generics = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "-v",
]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
]
fail_under = 80
```

---

## Directory Structure

### Recommended Layout (src layout)

```text
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── .pre-commit-config.yaml
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── py.typed          # PEP 561 marker
│       ├── cli.py
│       └── core.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_core.py
```

### Key Files

**src/my_package/**init**.py**:

```python
"""My package description."""

from .core import main_function

__all__ = ["main_function"]
__version__ = "0.1.0"
```

**src/my_package/py.typed**:

```text
# PEP 561 marker file - indicates this package has type hints
```

---

## Build Backend Options

### Hatchling (Recommended)

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

### Setuptools

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```

### Flit

```toml
[build-system]
requires = ["flit_core>=3.4"]
build-backend = "flit_core.buildapi"

[tool.flit.module]
name = "my_package"
```

---

## Dependency Specification

### Version Constraints

```toml
dependencies = [
    # Minimum version
    "requests>=2.28.0",

    # Compatible release (2.28.x)
    "requests~=2.28.0",

    # Exact version (avoid in libraries)
    "requests==2.28.0",

    # Version range
    "requests>=2.28.0,<3.0.0",

    # With extras
    "requests[security]>=2.28.0",
]
```

### Optional Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.9.0",
    "mypy>=1.8.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]
all = [
    "my-package[dev,docs]",
]
```

---

## Entry Points

### CLI Scripts

```toml
[project.scripts]
my-cli = "my_package.cli:app"
my-other-cli = "my_package.other:main"
```

### GUI Scripts

```toml
[project.gui-scripts]
my-gui = "my_package.gui:main"
```

### Plugin Entry Points

```toml
[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins.plugin1:Plugin1"
plugin2 = "my_package.plugins.plugin2:Plugin2"
```

---

## Pre-commit Configuration

**.pre-commit-config.yaml**:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
        args: [--strict]
```

---

## Verification Commands

After configuration, verify the setup:

```bash
# Install in development mode
uv pip install -e ".[dev]"

# Run linters
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/

# Run tests
uv run pytest tests/ -v --cov=src

# Build package
uv build

# Check package metadata
uv run python -c "import my_package; print(my_package.__version__)"
```

---

## Common Issues

### Issue: Package not found after install

**Fix**: Verify `packages` in hatch config or setuptools config:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]
```

### Issue: Type hints not exported

**Fix**: Add `py.typed` marker file:

```bash
touch src/my_package/py.typed
```

### Issue: CLI not working

**Fix**: Verify entry point matches actual module path:

```toml
[project.scripts]
# Format: "command-name = module.path:function"
my-cli = "my_package.cli:app"
```

---

## References

- [Python Packaging User Guide](https://packaging.python.org/)
- [Hatchling Documentation](https://hatch.pypa.io/latest/)
- [PEP 621 - Project Metadata](https://peps.python.org/pep-0621/)
- [Ruff Configuration](https://docs.astral.sh/ruff/configuration/)
