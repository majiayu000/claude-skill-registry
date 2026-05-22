---
name: pyproject-toml
version: 1.0.0
description: Configure Python projects with pyproject.toml for modern packaging, tools, and dependency management
author: workspace-hub
category: devtools
tags: [python, pyproject, configuration, packaging, build-system]
platforms: [python]
---

# pyproject.toml Configuration Skill

Master pyproject.toml for modern Python project configuration, build systems, tool settings, and dependency management.

## When to Use This Skill

Use pyproject.toml configuration when you need:
- **Project metadata** - Name, version, description, authors
- **Dependency management** - Core and optional dependencies
- **Build configuration** - Setuptools, hatch, flit, or poetry
- **Tool configuration** - pytest, ruff, mypy, black, isort
- **Entry points** - CLI scripts and plugins
- **Package discovery** - Source directory configuration

**Avoid when:**
- Legacy projects requiring setup.py (rare, migrate instead)
- Non-Python projects

## Core Structure

### Complete pyproject.toml Template

```toml
# ============================================================
# BUILD SYSTEM
# ============================================================
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

# ============================================================
# PROJECT METADATA
# ============================================================
[project]
name = "my-project"
version = "0.1.0"
description = "A comprehensive Python project template"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
maintainers = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["python", "template", "project"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

# Core dependencies
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pyyaml>=6.0",
    "click>=8.0.0",
]

# ============================================================
# OPTIONAL DEPENDENCIES
# ============================================================
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.4.0",
    "black>=23.0.0",
    "isort>=5.12.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]
viz = [
    "plotly>=5.15.0",
    "matplotlib>=3.7.0",
]
all = [
    "my-project[dev,docs,viz]",
]

# ============================================================
# ENTRY POINTS (CLI & PLUGINS)
# ============================================================
[project.scripts]
my-cli = "my_project.cli:main"
my-tool = "my_project.tools:run"

[project.gui-scripts]
my-gui = "my_project.gui:main"

[project.entry-points."my_project.plugins"]
plugin1 = "my_project.plugins.plugin1:Plugin1"
plugin2 = "my_project.plugins.plugin2:Plugin2"

# ============================================================
# URLS
# ============================================================
[project.urls]
Homepage = "https://github.com/username/my-project"
Documentation = "https://my-project.readthedocs.io"
Repository = "https://github.com/username/my-project.git"
Issues = "https://github.com/username/my-project/issues"
Changelog = "https://github.com/username/my-project/blob/main/CHANGELOG.md"

# ============================================================
# PACKAGE DISCOVERY
# ============================================================
[tool.setuptools]
package-dir = {"" = "src"}
include-package-data = true

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_project*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
my_project = ["*.yaml", "*.json", "data/*"]

# ============================================================
# UV CONFIGURATION
# ============================================================
[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.4.0",
]

# ============================================================
# PYTEST CONFIGURATION
# ============================================================
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
    "ignore::PendingDeprecationWarning",
]

# ============================================================
# COVERAGE CONFIGURATION
# ============================================================
[tool.coverage.run]
source = ["src"]
branch = true
parallel = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/conftest.py",
]

[tool.coverage.paths]
source = ["src"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
show_missing = true
precision = 2
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"

# ============================================================
# RUFF CONFIGURATION (Linting & Formatting)
# ============================================================
[tool.ruff]
target-version = "py310"
line-length = 88
indent-width = 4
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "*.egg-info",
]

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
]
ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default argument
    "B905",   # zip strict
]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["ARG001", "S101"]
"__init__.py" = ["F401"]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]
force-single-line = false
lines-after-imports = 2

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"

# ============================================================
# MYPY CONFIGURATION
# ============================================================
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
show_column_numbers = true
pretty = true
exclude = [
    "tests/",
    "build/",
    "dist/",
]

[[tool.mypy.overrides]]
module = [
    "pandas.*",
    "numpy.*",
    "plotly.*",
    "yaml.*",
]
ignore_missing_imports = true

# ============================================================
# BLACK CONFIGURATION (if not using ruff format)
# ============================================================
[tool.black]
line-length = 88
target-version = ["py310", "py311", "py312"]
include = '\.pyi?$'
exclude = '''
/(
    \.git
    | \.venv
    | __pycache__
    | build
    | dist
)/
'''

# ============================================================
# ISORT CONFIGURATION (if not using ruff)
# ============================================================
[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["my_project"]
skip = [".venv", "build", "dist"]
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

# ============================================================
# BUMPVER (Version Management)
# ============================================================
[tool.bumpver]
current_version = "0.1.0"
version_pattern = "MAJOR.MINOR.PATCH"
commit_message = "bump version {old_version} -> {new_version}"
commit = true
tag = true
push = false

[tool.bumpver.file_patterns]
"pyproject.toml" = [
    'version = "{version}"',
    'current_version = "{version}"',
]
"src/my_project/__init__.py" = [
    '__version__ = "{version}"',
]
```

## Section-by-Section Guide

### 1. Build System

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"
```

**Alternative build backends:**
```toml
# Hatch
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Flit
[build-system]
requires = ["flit_core>=3.4"]
build-backend = "flit_core.buildapi"

# Poetry
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

# PDM
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
```

### 2. Project Metadata

```toml
[project]
name = "my-project"                    # Package name (PyPI)
version = "0.1.0"                      # Semantic version
description = "Short description"      # One-line summary
readme = "README.md"                   # Long description file
requires-python = ">=3.10"             # Python version constraint
license = {text = "MIT"}               # License identifier

# Alternative license formats
# license = {file = "LICENSE"}
# license = "MIT"

authors = [
    {name = "Name", email = "email@example.com"}
]

keywords = ["keyword1", "keyword2"]

# PyPI classifiers
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
```

### 3. Dependencies

```toml
[project]
# Core dependencies (always installed)
dependencies = [
    "pandas>=2.0.0",           # Minimum version
    "numpy>=1.24,<2.0",        # Version range
    "requests~=2.28",          # Compatible release
    "click==8.1.3",            # Exact version
    "pyyaml",                  # Any version
]

[project.optional-dependencies]
# Install with: pip install my-project[dev]
dev = [
    "pytest>=7.0",
    "ruff>=0.1.0",
]

# Install with: pip install my-project[viz]
viz = [
    "plotly>=5.0",
    "matplotlib>=3.7",
]

# Install all optional deps
all = [
    "my-project[dev,viz]",
]
```

### 4. Package Discovery

**Src layout (recommended):**
```toml
[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_project*"]
exclude = ["tests*"]
```

**Flat layout:**
```toml
[tool.setuptools.packages.find]
include = ["my_project*"]
exclude = ["tests*"]
```

**Include data files:**
```toml
[tool.setuptools.package-data]
my_project = [
    "*.yaml",
    "*.json",
    "data/*.csv",
    "templates/*.html",
]
```

### 5. Entry Points

**CLI scripts:**
```toml
[project.scripts]
# Creates: my-cli command
my-cli = "my_project.cli:main"

# Module with arguments
my-tool = "my_project.tools:run"
```

**Python code:**
```python
# src/my_project/cli.py
import click

@click.command()
@click.option("--name", default="World")
def main(name: str) -> None:
    """CLI entry point."""
    click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    main()
```

**Plugin system:**
```toml
[project.entry-points."my_project.plugins"]
csv = "my_project.plugins.csv:CSVPlugin"
json = "my_project.plugins.json:JSONPlugin"
```

## Tool-Specific Configurations

### pytest

```toml
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
addopts = [
    "-v",                    # Verbose
    "--tb=short",           # Short traceback
    "-ra",                  # Show extra summary
    "--strict-markers",     # Error on unknown markers
    "--cov=src",           # Coverage
    "--cov-report=html",   # HTML report
]
markers = [
    "slow: slow tests",
    "integration: integration tests",
]
```

### ruff (Modern Linter)

```toml
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

### mypy (Type Checker)

```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true

[[tool.mypy.overrides]]
module = ["pandas.*", "numpy.*"]
ignore_missing_imports = true
```

## Complete Examples

### Example 1: Data Processing Library

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "data-processor"
version = "1.0.0"
description = "Data processing utilities for engineering workflows"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "openpyxl>=3.1.0",
    "pyyaml>=6.0",
]

[project.optional-dependencies]
viz = ["plotly>=5.15.0"]
dev = ["pytest>=7.0", "ruff>=0.1.0", "mypy>=1.4"]

[project.scripts]
data-process = "data_processor.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--cov=src"]

[tool.ruff]
line-length = 88
select = ["E", "W", "F", "I"]
```

### Example 2: Web Scraping Package

```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "energy-scraper"
version = "0.1.0"
description = "BSEE and SODIR data extraction utilities"
requires-python = ">=3.10"

dependencies = [
    "scrapy>=2.12.0",
    "selenium>=4.15.0",
    "beautifulsoup4>=4.12.0",
    "pandas>=2.0.0",
    "pyyaml>=6.0",
    "aiohttp>=3.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.1.0",
]

[project.scripts]
bsee-fetch = "energy_scraper.bsee:main"
sodir-fetch = "energy_scraper.sodir:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### Example 3: Workspace-Hub Standard Template

```toml
# Standard pyproject.toml for workspace-hub repositories
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "workspace-project"
version = "0.1.0"
description = "Standardized project configuration"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Development Team"}]

dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "pyyaml>=6.0",
    "plotly>=5.15.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.4.0",
    "deepdiff>=6.0.0",
]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = ["-v", "--tb=short", "--cov=src", "--cov-report=html"]

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 80

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true

[[tool.mypy.overrides]]
module = ["pandas.*", "numpy.*", "plotly.*"]
ignore_missing_imports = true

[tool.bumpver]
current_version = "0.1.0"
version_pattern = "MAJOR.MINOR.PATCH"
commit_message = "bump version {old_version} -> {new_version}"
commit = true
tag = true
```

## Best Practices

### 1. Version Constraints

```toml
# Recommended patterns
dependencies = [
    "pandas>=2.0.0",           # Minimum version (most common)
    "numpy>=1.24,<2.0",        # Range for major version compatibility
    "requests~=2.28",          # Compatible release (~=2.28 means >=2.28,<3.0)
]

# Avoid
dependencies = [
    "pandas==2.1.3",           # Too strict, causes conflicts
    "numpy",                   # Too loose, may break with updates
]
```

### 2. Organize Optional Dependencies

```toml
[project.optional-dependencies]
# Group by purpose
dev = ["pytest", "ruff", "mypy"]
docs = ["mkdocs", "mkdocs-material"]
viz = ["plotly", "matplotlib"]

# Convenience groups
test = ["pytest", "pytest-cov"]
lint = ["ruff", "mypy"]
all = ["my-project[dev,docs,viz]"]
```

### 3. Use src Layout

```
my-project/
├── pyproject.toml
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

### 4. Keep Tools Consistent

```toml
# Use same line-length everywhere
[tool.ruff]
line-length = 88

[tool.black]
line-length = 88

[tool.isort]
line_length = 88
```

## Resources

- **PEP 517**: Build system interface
- **PEP 518**: pyproject.toml specification
- **PEP 621**: Project metadata
- **PEP 660**: Editable installs
- **Setuptools**: https://setuptools.pypa.io/
- **UV**: https://docs.astral.sh/uv/

---

**Use this template for all Python projects in workspace-hub!**
