---
name: manage-python-env
description: Quick reference for uv (fast Python package manager) operations to save tokens. Use when creating virtual environments, installing packages, managing dependencies, or when user asks about uv commands. Provides concise patterns for Python project setup and package management.
---

# UV Management

Quick reference for uv - the fast Python package installer and environment manager.

## Installation

### Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Verify installation
uv --version
```

## Project Initialization

### Create New Project
```bash
# Initialize new project
uv init project-name

# Initialize in current directory
uv init

# With specific Python version
uv init --python 3.11
```

### Project Structure Created
```
project-name/
├── pyproject.toml    # Project configuration
├── .python-version   # Python version specification
└── src/
    └── project_name/
        └── __init__.py
```

## Virtual Environment

### Create Virtual Environment
```bash
# Create venv (automatic with uv)
uv venv

# With specific Python version
uv venv --python 3.11

# With custom name
uv venv .venv-custom

# Activate (same as regular venv)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Python Version Management
```bash
# List available Python versions
uv python list

# Install specific Python version
uv python install 3.11

# Pin Python version for project
uv python pin 3.11
```

## Package Management

### Install Packages
```bash
# Install single package
uv pip install package-name

# Install specific version
uv pip install package-name==1.2.3

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

### Add Dependencies (Modern Way)
```bash
# Add package to project
uv add numpy

# Add with version constraint
uv add "numpy>=1.24,<2.0"

# Add multiple packages
uv add numpy pandas matplotlib

# Add as dev dependency
uv add --dev pytest black ruff

# Add from git
uv add git+https://github.com/user/repo.git
```

### Remove Packages
```bash
# Remove package
uv remove package-name

# Remove dev dependency
uv remove --dev pytest
```

### Update Packages
```bash
# Update single package
uv pip install --upgrade package-name

# Update all packages
uv pip install --upgrade -r requirements.txt

# Sync dependencies (recommended)
uv sync
```

## Dependency Management

### Lock Dependencies
```bash
# Generate lock file
uv lock

# Lock and sync
uv lock --sync
```

### Export Requirements
```bash
# Export to requirements.txt
uv pip freeze > requirements.txt

# Export from pyproject.toml
uv export --format requirements-txt > requirements.txt
```

## Running Commands

### Run Python
```bash
# Run Python script
uv run python script.py

# Run module
uv run -m module_name

# Run with arguments
uv run python script.py --arg value
```

### Run Tools
```bash
# Run pytest
uv run pytest

# Run black
uv run black .

# Run ruff
uv run ruff check .

# Run any tool
uv run tool-name [args]
```

## VRP Project Setup

### Initial Project Setup
```bash
# 1. Create project directory
mkdir vrp-toolkit
cd vrp-toolkit

# 2. Initialize with uv
uv init

# 3. Create virtual environment
uv venv

# 4. Activate environment
source .venv/bin/activate

# 5. Install core dependencies
uv add numpy pandas matplotlib networkx

# 6. Install dev dependencies
uv add --dev pytest black ruff ipython jupyter

# 7. Install OSMnx (for real map support)
uv add osmnx geopandas

# 8. Install package in editable mode
uv pip install -e .
```

### pyproject.toml for VRP Toolkit
```toml
[project]
name = "vrp-toolkit"
version = "0.1.0"
description = "Reusable VRP/PDPTW solving framework"
requires-python = ">=3.8"
dependencies = [
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "networkx>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "ipython>=8.0.0",
    "jupyter>=1.0.0",
]
osmnx = [
    "osmnx>=1.6.0",
    "geopandas>=0.14.0",
    "folium>=0.15.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py38"

[tool.black]
line-length = 100
target-version = ["py38"]
```

### Install All Dependencies
```bash
# Install main dependencies
uv add numpy pandas matplotlib networkx

# Install dev tools
uv add --dev pytest black ruff ipython jupyter

# Install OSMnx group
uv add osmnx geopandas folium

# Or install from pyproject.toml
uv sync
```

## Common Workflows

### Daily Development
```bash
# Activate environment
source .venv/bin/activate

# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .

# Run Jupyter
uv run jupyter lab
```

### Add New Dependency
```bash
# Add package
uv add package-name

# Test it works
uv run python -c "import package_name; print('OK')"

# Commit updated pyproject.toml
git add pyproject.toml uv.lock
git commit -m "chore: add package-name dependency"
```

### Clean Install
```bash
# Remove existing environment
rm -rf .venv

# Recreate
uv venv

# Reinstall all dependencies
uv sync

# Verify
uv run python -c "import numpy; print(numpy.__version__)"
```

## Comparison with pip/venv

| Task | Traditional | UV |
|------|------------|-----|
| Create venv | `python -m venv .venv` | `uv venv` |
| Activate | `source .venv/bin/activate` | Same |
| Install package | `pip install package` | `uv add package` |
| Install requirements | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| Freeze deps | `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |
| Run tool | `python -m pytest` | `uv run pytest` |

**Key Advantages of UV:**
- ⚡ 10-100x faster than pip
- 🔒 Built-in dependency locking
- 🐍 Python version management
- 📦 Cleaner dependency specification in pyproject.toml

## Additional Resources

### Troubleshooting
Common issues and solutions: **See [troubleshooting.md](references/troubleshooting.md)**
- UV not found after install
- Wrong Python version
- Dependency conflicts
- Package not found

### Advanced Usage
Power user features: **See [advanced.md](references/advanced.md)**
- Multiple environments
- Dependency groups
- Build and publish
- Integration with other skills

### Migration from pip
Convert existing projects: **See [migration.md](references/migration.md)**
- Convert requirements.txt to pyproject.toml
- Migrate existing project step-by-step
- pip vs UV comparison

## Quick Reference

| Task | Command |
|------|---------|
| Init project | `uv init` |
| Create venv | `uv venv` |
| Add package | `uv add package` |
| Add dev dep | `uv add --dev tool` |
| Install all | `uv sync` |
| Run script | `uv run python script.py` |
| Run tool | `uv run pytest` |
| Update all | `uv sync --upgrade` |
| Lock deps | `uv lock` |
| Export reqs | `uv pip freeze > requirements.txt` |
| Python version | `uv python install 3.11` |
| Pin Python | `uv python pin 3.11` |
