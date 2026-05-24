---
name: uv-project-setup
description: |
  Initialize and configure new Python projects with uv, including creating projects,
  setting up pyproject.toml, managing dependency groups, and pinning Python versions.
  Use when starting new projects, configuring development environments, or standardizing
  project structure with uv. Covers `uv init`, `uv add`, `uv python pin`, and initial
  project scaffolding with proper dependency organization.
allowed-tools: Bash, Read, Write, Edit
---

# uv Project Setup

## Purpose

Initialize and configure new Python projects with uv, creating standardized, reproducible
project structures with proper dependency management, Python version pinning, and organized
dependency groups for development, testing, and production use.

## Quick Start

Initialize a new project with a single command that creates all necessary files:

```bash
# Initialize project in current directory or new directory
uv init my-project
cd my-project

# Install dependencies in isolated environment
uv sync

# Start developing
uv run python main.py
```

This creates a complete project structure with `pyproject.toml`, `.python-version`, `.venv/`,
and a sample `main.py`. Everything is ready to add dependencies and start coding.

## Instructions

### Step 1: Initialize Project Structure

```bash
# Create new project directory and initialize
uv init my-project
cd my-project

# Or initialize in current directory
mkdir my-project && cd my-project
uv init
```

This creates:
- `pyproject.toml` - Project metadata and dependencies configuration
- `.python-version` - Pinned Python version file
- `README.md` - Project documentation template
- `main.py` - Entry point script
- `.gitignore` - Git exclusion file

### Step 2: Pin Python Version to Project

```bash
# Pin to specific Python version (creates .python-version)
uv python pin 3.12

# Pin to minor version range
uv python pin 3.12.3

# Verify pinning worked
cat .python-version
```

The `.python-version` file ensures all team members use the same Python version automatically
when working in the project directory.

### Step 3: Add Project Dependencies

```bash
# Add runtime dependencies
uv add requests httpx pandas

# Add exact versions
uv add "fastapi==0.104.0"

# Add version ranges (recommended)
uv add "django>=4.2,<5.0"

# Add with extras
uv add "pandas[excel,plot]"
```

Use semantic versioning ranges to balance stability with flexibility. The `uv.lock` file
ensures reproducible installations across all environments.

### Step 4: Organize Dependencies with Groups

```toml
# In pyproject.toml, define development groups under [dependency-groups]
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
]
lint = [
    "ruff>=0.1.0",
    "mypy>=1.7.0",
    "pylint>=3.0.0",
]
docs = [
    "mkdocs>=1.5.0",
    "mkdocs-material>=9.0.0",
]
```

Then sync specific groups:

```bash
# Install all groups
uv sync --all-groups

# Install only specific groups
uv sync --group dev --group lint

# Install without dev groups (production)
uv sync --no-dev
```

### Step 5: Configure Tool Settings

Add uv-specific configuration to `pyproject.toml` under `[tool.uv]`:

```toml
[tool.uv]
# Use custom virtual environment location
# project-environment = ".venv"

# Define conflicting extras that can't be used together
conflicts = [
    [{ extra = "cuda" }, { extra = "cpu" }],
]

# Support multiple platform-specific environments
environments = [
    "sys_platform == 'darwin'",
    "sys_platform == 'linux'",
    "sys_platform == 'win32'",
]
```

### Step 6: Set Up Optional Dependencies (Extras)

For published packages, define extras that users can install:

```toml
[project]
name = "my-package"
version = "0.1.0"
dependencies = ["httpx>=0.27.0"]

[project.optional-dependencies]
# Extras for optional functionality
excel = ["openpyxl>=3.0.0"]
plot = ["matplotlib>=3.5.0"]
# Meta-extra for everything
all = ["openpyxl>=3.0.0", "matplotlib>=3.5.0"]

[project.scripts]
# CLI entry points
my-cli = "my_package.cli:main"
dev-server = "my_package.server:run"
```

Users can then install your package with:

```bash
# Install with specific extras
pip install my-package[excel,plot]

# Install with all extras
pip install my-package[all]
```

### Step 7: Test Project Setup

Verify the project is properly configured:

```bash
# View dependency tree
uv tree

# Run your project
uv run python main.py

# Create and activate environment manually (optional)
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

## Examples

### Example 1: Web Development Project Setup

```bash
# Initialize project
uv init my-api
cd my-api

# Pin Python version
uv python pin 3.12

# Add web framework and utilities
uv add fastapi uvicorn sqlalchemy pydantic

# Add development dependencies
uv add --group dev pytest pytest-asyncio black ruff mypy

# Verify setup
uv tree
uv run pytest --collect-only
```

### Example 2: Data Science Project

```bash
# Create data science project
uv init data-analysis
cd data-analysis

# Pin to Python 3.12
uv python pin 3.12

# Add data science stack
uv add "pandas>=2.2.0" "numpy>=1.26.0" "scikit-learn>=1.3.0"

# Add Jupyter and visualization
uv add jupyter matplotlib seaborn plotly

# Add development tools
uv add --group dev pytest jupyter-contrib-nbextensions

# Organize into pyproject.toml groups
```

**pyproject.toml:**
```toml
[project]
name = "data-analysis"
version = "0.1.0"
description = "Data analysis pipeline"
requires-python = ">=3.12"
dependencies = [
    "pandas>=2.2.0",
    "numpy>=1.26.0",
    "scikit-learn>=1.3.0",
    "matplotlib>=3.5.0",
]

[dependency-groups]
jupyter = ["jupyter>=1.0.0"]
dev = ["pytest>=8.0.0", "black>=23.0.0"]
```

### Example 3: Library Project with Extras

```bash
# Initialize library project
uv init my-library
cd my-library

# Core dependencies only
uv add "requests>=2.31.0" "click>=8.1.0"

# Add testing framework
uv add --dev pytest pytest-cov

# Add linting/formatting
uv add --group lint ruff mypy black

# Add documentation
uv add --group artifacts mkdocs mkdocs-material

# Add optional features
uv add --group async aiohttp asyncio-contextmanager
uv add --group database sqlalchemy psycopg2-binary
```

**pyproject.toml setup with extras:**
```toml
[project]
name = "my-library"
version = "0.1.0"
dependencies = ["requests>=2.31.0", "click>=8.1.0"]

[project.optional-dependencies]
async = ["aiohttp>=3.8.0"]
database = ["sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0"]
all = ["aiohttp>=3.8.0", "sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0"]

[dependency-groups]
dev = ["pytest>=8.0.0"]
lint = ["ruff>=0.1.0", "mypy>=1.7.0"]
docs = ["mkdocs>=1.5.0"]
```

### Example 4: Configure Alternative Package Sources

```toml
# In pyproject.toml - use git repository for package
[tool.uv.sources]
# Get package from git tag
httpx = { git = "https://github.com/encode/httpx", tag = "0.27.0" }

# Install local package in editable mode (for monorepos)
local-lib = { path = "../local-lib", editable = true }

# Use specific PyPI index for package
torch = { index = "pytorch" }

# Define custom index
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu118"
explicit = true  # Only use for torch package above
```

Then add the package:
```bash
uv add torch
uv sync
```

### Example 5: Create Script with Inline Dependencies

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "httpx>=0.27",
#     "rich>=13.0",
# ]
# ///

import httpx
from rich import print

def main():
    response = httpx.get("https://api.github.com")
    print(response.json())

if __name__ == "__main__":
    main()
```

Make executable and run:
```bash
chmod +x script.py
./script.py

# Or run directly
uv run script.py
```

### Example 6: Multi-Platform Project

```toml
[project]
name = "cross-platform-app"
version = "0.1.0"
dependencies = [
    "click>=8.1.0",
    "pathlib-plus>=1.0.0",
]

[tool.uv]
# Support multiple operating systems with different dependencies
environments = [
    "sys_platform == 'darwin'",
    "sys_platform == 'linux'",
    "sys_platform == 'win32'",
]

[tool.uv.sources]
# Platform-specific wheels via environment markers
[tool.uv.sources.pywin32]
version = "306"
markers = "sys_platform == 'win32'"
```

## Common Pitfalls and Solutions

### Pitfall 1: Forgetting to Pin Python Version

**Problem:** Team members using different Python versions locally.

**Solution:**
```bash
# Always pin Python version early in project
uv python pin 3.12

# Commit .python-version to repository
git add .python-version
```

### Pitfall 2: Adding Dependencies to Wrong Group

**Problem:** Development tools ending up in production installs.

**Solution:**
```bash
# Wrong: adds to main dependencies
uv add pytest

# Correct: adds to dev group
uv add --dev pytest
uv add --group lint ruff

# Then install only production deps
uv sync --no-dev
```

### Pitfall 3: Not Committing Lock File

**Problem:** Different environments have different package versions.

**Solution:**
```bash
# Always commit uv.lock to version control
git add uv.lock
git commit -m "Update dependencies"

# Use --frozen in CI to catch sync issues
uv sync --frozen
```

### Pitfall 4: Missing Build System

**Problem:** Package won't build/install properly.

**Solution:**
```toml
# Ensure build-system is defined in pyproject.toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Or use setuptools
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"
```

### Pitfall 5: Conflicting Dependency Groups

**Problem:** Incompatible packages can be installed together.

**Solution:**
```toml
[tool.uv]
# Prevent conflicting extras from being used together
conflicts = [
    [{ extra = "cuda" }, { extra = "cpu" }],
]

# In dependency-groups, don't mix conflicting versions
[dependency-groups]
# Keep compatible versions together
ml-cpu = ["torch-cpu>=2.0"]
ml-gpu = ["torch-gpu>=2.0"]
```

## See Also

- [uv-dependency-management](../uv-dependency-management/SKILL.md) - Managing dependencies, versions, and extras
- [uv-python-version-management](../uv-python-version-management/SKILL.md) - Installing and discovering Python versions
- [uv-ci-cd-integration](../uv-ci-cd-integration/SKILL.md) - Setting up CI/CD pipelines with uv
- [uv-tool-management](../uv-tool-management/SKILL.md) - Running and managing CLI tools with uvx
- [uv Documentation](https://docs.astral.sh/uv/) - Official uv reference
