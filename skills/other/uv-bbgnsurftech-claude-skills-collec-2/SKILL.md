---
name: uv
description: Expert guidance for Astral's uv - an extremely fast Python package and project manager. Use when working with Python projects, managing dependencies, creating scripts with PEP 723 metadata, installing tools, managing Python versions, or configuring package indexes. Covers project initialization, dependency management, virtual environments, tool installation, workspace configuration, CI/CD integration, and migration from pip/poetry.
---

# uv: Modern Python Package and Project Manager

## Overview

uv is Astral's extremely fast Python package and project manager written in Rust, designed as a unified replacement for pip, pip-tools, pipx, poetry, pyenv, and virtualenv. It delivers 10-100x faster performance while providing modern dependency management with lockfiles and reproducible environments.

## When to Use This Skill

Use this skill when:

- Initializing new Python projects or scripts
- Managing project dependencies with pyproject.toml
- Creating portable single-file scripts with PEP 723 inline metadata
- Installing or running command-line tools (ruff, black, httpie, etc.)
- Managing Python interpreter versions
- Setting up virtual environments
- Configuring package indexes or private registries
- Migrating from pip, pip-tools, poetry, or conda
- Configuring CI/CD pipelines for Python projects
- Setting up Docker containers for Python applications
- Troubleshooting dependency resolution or build failures

## Core Capabilities

### 1. Project Initialization and Management

**Initialize new projects:**

```bash
# Standard project with recommended structure
uv init myproject

# Application project (default)
uv init myapp --app

# Library/package project (includes src/ layout)
uv init mylib --lib --build-backend hatchling

# Bare project (pyproject.toml only)
uv init --bare
```

**Project structure created:**

```text
myproject/
├── .venv/           # Virtual environment (auto-created)
├── .python-version  # Pinned Python version
├── README.md
├── main.py          # Sample entry point
├── pyproject.toml   # Project metadata and dependencies
└── uv.lock          # Lockfile (like Cargo.lock or package-lock.json)
```

### 2. Dependency Management

**Add dependencies to project:**

```bash
# Production dependencies
uv add requests 'flask>=2.0,<3.0' pydantic

# Development dependencies
uv add --dev pytest pytest-cov ruff mypy black

# Optional dependency groups
uv add --group docs sphinx sphinx-rtd-theme
uv add --group test pytest-asyncio hypothesis

# From various sources
uv add git+https://github.com/psf/requests@main
uv add --editable ./local-package
uv add ../sibling-package
```

**Remove dependencies:**

```bash
uv remove requests flask
uv remove --dev pytest
uv remove --group docs sphinx
```

**Lock and sync environments:**

```bash
# Update lockfile with latest compatible versions
uv lock

# Upgrade all packages
uv lock --upgrade

# Upgrade specific packages
uv lock --upgrade-package requests --upgrade-package flask

# Install all dependencies from lockfile
uv sync

# Install without dev dependencies (production)
uv sync --no-dev

# Install with optional groups
uv sync --extra docs --extra test

# Sync without updating lockfile (CI mode)
uv sync --frozen

# Error if lockfile out of sync (strict CI mode)
uv sync --locked
```

### 3. Running Code in Project Context

**Execute scripts and commands:**

```bash
# Run Python script in project environment
uv run python script.py

# Run module (like python -m)
uv run -m pytest
uv run -m flask run --port 8000

# Run with specific Python version
uv run --python 3.11 script.py
uv run --python pypy@3.9 test.py

# Run without syncing first (use current environment state)
uv run --frozen script.py

# Run with additional temporary dependencies
uv run --with httpx --with rich script.py

# Run without project dependencies (standalone)
uv run --no-project example.py

# Run with environment variables from file
uv run --env-file .env script.py
```

### 4. PEP 723 Inline Script Metadata

**Create portable single-file scripts with dependencies:**

```bash
# Initialize script with metadata block
uv init --script example.py --python 3.12

# Add dependencies to existing script
uv add --script example.py requests rich
```

**Example script structure:**

```python
#!/usr/bin/env -S uv --quiet run --active --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "rich>=13.0",
# ]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com/repos/astral-sh/uv")
print(f"Stars: {response.json()['stargazers_count']}")
```

**Run scripts:**

```bash
# Auto-creates isolated environment and runs
uv run example.py

# Run with additional dependencies
uv run --with beautifulsoup4 example.py

# Lock script for reproducibility
uv lock --script example.py  # Creates example.py.lock

# Make executable and run directly
chmod +x example.py
./example.py
```

**Best practices for scripts:**

- Always include `requires-python` for compatibility
- Use version constraints for critical dependencies
- Lock scripts before sharing for reproducibility
- Add `exclude-newer` in `[tool.uv]` for time-based pinning

### 5. Tool Management

**One-off tool execution (ephemeral environments):**

```bash
# Run tool without installing (uvx is alias)
uvx ruff check
uvx pycowsay "hello from uv"

# Run specific version
uvx ruff@0.3.0 check
uvx --from 'ruff>=0.3.0,<0.4.0' ruff check

# Run tool from different package
uvx --from httpie http GET example.com

# Run with plugin/additional dependencies
uvx --with mkdocs-material mkdocs serve
```

**Persistent tool installation:**

```bash
# Install tool globally (adds to PATH)
uv tool install ruff black mypy

# Install with version constraint
uv tool install 'httpie>0.1.0'

# Install from git
uv tool install git+https://github.com/httpie/cli

# Install with additional packages
uv tool install mkdocs --with mkdocs-material

# Upgrade tools
uv tool upgrade ruff
uv tool upgrade --all

# List installed tools
uv tool list
uv tool list --show-paths

# Uninstall tool
uv tool uninstall ruff

# Update shell configuration for tools
uv tool update-shell
```

### 6. Python Version Management

**Install and manage Python versions:**

```bash
# Install specific Python version (auto-downloads if needed)
uv python install 3.12
uv python install 3.11 3.12 3.13  # Multiple at once

# List available versions
uv python list
uv python list --all-versions

# Pin Python version for project
uv python pin 3.12  # Creates .python-version

# Find Python executable
uv python find 3.11

# Upgrade Python installations
uv python upgrade 3.11
uv python upgrade --all

# Use specific Python for command
uv run --python 3.11 script.py
uv venv --python 3.12.0
```

**Python is automatically downloaded when needed:**

- Supports CPython, PyPy, GraalPy, and other implementations
- Managed installations stored in `~/.local/share/uv/python/` (Unix)
- Preference configurable: `only-managed`, `managed`, `system`, `only-system`

### 7. Virtual Environment Management

**Create virtual environments:**

```bash
# Create in .venv directory (default)
uv venv

# Create with specific Python version
uv venv --python 3.11
uv venv --python pypy3.9

# Create with custom path
uv venv myenv

# Create with system packages access
uv venv --system-site-packages

# Create with seed packages (pip, setuptools, wheel)
uv venv --seed

# Activate (standard Python activation)
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

**Warning**: Running `uv venv` again **wipes existing environment** without confirmation.

### 8. pip-Compatible Interface

**Direct pip replacement commands:**

```bash
# Install packages
uv pip install flask requests
uv pip install -r requirements.txt
uv pip install -e .  # Editable install

# Install from git
uv pip install git+https://github.com/psf/requests
uv pip install git+https://github.com/pallets/flask@main

# Compile requirements (like pip-compile)
uv pip compile pyproject.toml -o requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip compile --upgrade-package ruff requirements.in

# Sync environment to exact requirements (like pip-sync)
uv pip sync requirements.txt

# Uninstall packages
uv pip uninstall flask requests
uv pip uninstall -r requirements.txt

# List installed packages
uv pip list
uv pip list --format json
uv pip freeze > requirements.txt

# Show package info
uv pip show requests

# Check for conflicts
uv pip check

# Display dependency tree
uv pip tree
uv pip tree --depth 2

# Check if package is installed
uv pip freeze | grep -q '^requests=='
uv pip list --format json | jq -e '.[] | select(.name == "requests")'
uv pip show requests
```

**Package check benchmarks** (76 packages installed):

| Command                     | Time  | Output Size |
| --------------------------- | ----- | ----------- |
| `uv pip freeze`             | ~8ms  | ~1.5 KB     |
| `uv pip list`               | ~10ms | ~2.5 KB     |
| `uv pip list --format json` | ~10ms | ~3.2 KB     |
| `uv pip show <pkg>`         | ~40ms | ~0.3 KB     |

`uv pip show` is slower because it resolves `Requires` and `Required-by` relationships.

### 9. Workspace Management (Monorepos)

**Configure workspaces in root pyproject.toml:**

```toml
[tool.uv.workspace]
members = ["packages/*", "apps/*"]
exclude = ["packages/deprecated"]
```

**Workspace dependency references:**

```toml
[project]
name = "myapp"
dependencies = ["shared-lib", "core-utils"]

[tool.uv.sources]
shared-lib = { workspace = true }
core-utils = { workspace = true }
```

**Workspace commands:**

```bash
# Build specific workspace package
uv build --package my-package

# Run in workspace package context
uv run --package my-package python script.py

# Lock workspace (single lockfile for all members)
uv lock
```

### 10. Package Building and Publishing

**Build distributions:**

```bash
# Build wheel and source distribution
uv build

# Build only wheel
uv build --wheel

# Build specific workspace package
uv build --package my-package

# Output to custom directory
uv build --out-dir dist/
```

**Publish to PyPI:**

```bash
# Publish directly with uv
uv publish

# Publish with token
uv publish --token $PYPI_TOKEN

# Publish to test PyPI
uv publish --publish-url https://test.pypi.org/legacy/

# Smoke test before publishing
uv run --isolated --no-project --with dist/*.whl python -c "import my_package"
```

## Configuration

### pyproject.toml Structure

**Standard project configuration:**

```toml
[project]
name = "myproject"
version = "1.0.0"
description = "My awesome project"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.2",
    "pydantic>=2.5.3",
]

# Development dependencies using PEP 735 dependency groups
[dependency-groups]
dev = [
    "pytest>=8.4.2",
    "pytest-cov>=6.0.0",
    "pytest-mock>=3.15.1",
    "ruff>=0.13.3",
    "pyright>=1.1.406",
    "mypy>=1.18.2",
    "pre-commit>=4.3.0",
]
docs = ["sphinx>=7.0", "sphinx-rtd-theme>=1.3.0"]
test = ["pytest-cov>=6.0.0", "pytest-asyncio>=0.21.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# Core settings
managed = true
package = true
default-groups = ["dev"]

# Resolution
resolution = "highest"  # or "lowest", "lowest-direct"
index-strategy = "first-index"

# Build configuration
compile-bytecode = true
no-build-isolation-package = ["flash-attn"]

# Python management
python-preference = "managed"
python-downloads = "automatic"

# Custom package sources
[tool.uv.sources]
torch = { index = "pytorch-cu121" }
internal-lib = { workspace = true }

# Custom indexes
[[tool.uv.index]]
name = "pytorch-cu121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true
```

### Environment Variables

**Key environment variables:**

```bash
# Cache and directories
export UV_CACHE_DIR="/custom/cache"
export UV_PROJECT_ENVIRONMENT=".venv"

# Python management
export UV_PYTHON_PREFERENCE="managed"
export UV_PYTHON_DOWNLOADS="automatic"

# Network configuration
export UV_CONCURRENT_DOWNLOADS=20
export UV_CONCURRENT_BUILDS=8

# Index authentication
export UV_INDEX_PRIVATE_USERNAME="user"
export UV_INDEX_PRIVATE_PASSWORD="pass"

# Preview features
export UV_PREVIEW=1

# Disable cache
export UV_NO_CACHE=1

# System Python
export UV_SYSTEM_PYTHON=1
```

For complete configuration reference, see `references/configuration.md`.

## Common Workflows

### Starting a New Project

```bash
# 1. Initialize project
uv init myproject
cd myproject

# 2. Add dependencies
uv add fastapi uvicorn sqlalchemy

# 3. Add dev dependencies
uv add --dev pytest ruff mypy

# 4. Run application
uv run python main.py

# 5. Run tests
uv run pytest
```

### Creating a Portable Script

```bash
# 1. Create script with metadata
uv init --script analyze.py --python 3.11

# 2. Add dependencies
uv add --script analyze.py pandas matplotlib

# 3. Edit script content
# (add your code to analyze.py)

# 4. Lock for reproducibility
uv lock --script analyze.py

# 5. Make executable
chmod +x analyze.py

# 6. Run
./analyze.py
```

### Migrating from pip/requirements.txt

```bash
# 1. Initialize project
uv init --bare

# 2. Import dependencies
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt

# 3. Remove old files
rm requirements.txt requirements-dev.txt

# 4. Use uv commands going forward
uv sync  # Install dependencies
uv add new-package  # Add new dependency
```

### Migrating from Poetry

```bash
# Option 1: Automated migration
uvx migrate-to-uv
uvx migrate-to-uv --dry-run  # Preview first

# Option 2: Manual conversion
# - Convert [tool.poetry] to [project]
# - Convert poetry.lock to uv.lock: uv lock
# - Use uv commands instead of poetry commands
```

### CI/CD Integration (GitHub Actions)

**Basic CI workflow:**

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.11

      - name: Install dependencies
        run: uv sync --frozen --all-extras

      - name: Run tests
        run: uv run pytest

      - name: Run linters
        run: |
          uv run ruff check .
          uv run mypy .
```

**Publishing workflow with trusted publishing:**

```yaml
name: Publish
on:
  push:
    tags:
      - v*

jobs:
  publish:
    runs-on: ubuntu-latest
    environment:
      name: pypi
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v6
      - run: uv python install 3.13
      - run: uv build
      - run: uv run --isolated --no-project --with dist/*.whl tests/smoke_test.py
      - run: uv publish # Uses trusted publishing
```

### Docker Integration

```dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY . .

# Use virtual environment
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]
```

### Git Hook Integration (pre-commit / prek)

**Configure uv-managed tools in `.pre-commit-config.yaml`:**

**Note**: Both pre-commit and prek use the same configuration file with identical syntax.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: custom-hook
        name: Run Custom Hook
        entry: uv run my-hook-script
        language: system
        stages: [commit]
        pass_filenames: false
        always_run: true
```

**Benefits of uv run in git hooks:**

- Uses project's locked dependencies automatically
- No separate hook environment needed
- Ensures consistency between development and git hook checks
- Works with both pre-commit (Python) and prek (Rust)

## Troubleshooting

### "Externally Managed" Error

**Problem**: `error: The interpreter is externally managed`

**Solution**: Use virtual environments instead of `--system`:

```bash
uv venv
source .venv/bin/activate
uv pip install package
```

### Build Failures

**Problem**: Package fails to build from source

**Common causes**:

- Missing system dependencies (compilers, headers)
- Python version incompatibility
- Outdated package version

**Solutions**:

- Install system dependencies: `apt-get install python3-dev build-essential`
- Add version constraints: `uv add "numpy>=1.20"`
- Check error message for missing modules

### Lockfile Out of Sync

**Problem**: Dependencies changed but lockfile not updated

**Solutions**:

```bash
uv lock           # Regenerate lockfile
uv sync --locked  # Error if out of sync (CI mode)
uv sync --frozen  # Don't update lockfile
```

### Cache Issues

**Problem**: Stale cache causing problems

**Solutions**:

```bash
uv cache clean          # Clean entire cache
uv cache prune          # Remove unreachable entries
uv --no-cache <command> # Bypass cache temporarily
```

### Common Pitfalls

**1. Forgetting to sync after adding dependencies:**

```bash
uv add requests  # Adds to pyproject.toml and updates lockfile
uv sync          # Required to actually install the package
```

**2. Incorrect workspace glob patterns:**

- Wrong: `members = ["packages/"]` (missing asterisk)
- Correct: `members = ["packages/*"]`

**3. Missing build-system for libraries:**

Libraries and packages require a `[build-system]` section:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**4. Wrong file mode for TOML operations:**

- Use text mode `'r'` and `'w'` with tomlkit
- Do not use binary mode `'rb'` or `'wb'`

**5. Incorrect workspace source syntax:**

- Wrong: `{ workspace = "true" }` (string "true")
- Correct: `{ workspace = true }` (boolean true)

**6. Not using --frozen in CI:**

```bash
# CI should fail if lockfile is outdated
uv sync --frozen
```

**7. Incompatible Python version ranges in workspaces:**

All workspace members must have compatible `requires-python` ranges. If one member requires `>=3.11` and another requires `>=3.12`, the workspace will use `>=3.12`.

For more troubleshooting scenarios, see `references/troubleshooting.md`.

## Resources

This skill includes comprehensive reference documentation:

### references/

- `cli_reference.md` - Complete CLI commands and arguments reference
- `configuration.md` - All configuration options and environment variables
- `workflows.md` - Detailed workflow guides and examples
- `troubleshooting.md` - Common issues and solutions

### assets/

- `pyproject_templates/` - Example pyproject.toml configurations
- `script_examples/` - PEP 723 script templates
- `docker_examples/` - Docker configuration templates
- `github_actions/` - CI/CD workflow examples

## Key Principles

1. **Speed**: uv is 10-100x faster than traditional tools
2. **Reproducibility**: Lockfiles ensure consistent environments
3. **Simplicity**: Single tool replaces multiple Python tools
4. **Modern Standards**: PEP 723 scripts, standard pyproject.toml
5. **Developer Experience**: Automatic Python installation, smart defaults

## Version Information

Current latest version: **0.9.5** (October 2025)

Key recent features:

- Python 3.14 support with free-threaded builds
- Enhanced authentication system
- Advanced build configuration
- Workspace improvements
- Docker image optimizations

## External Resources

- Official docs: <https://docs.astral.sh/uv/>
- GitHub: <https://github.com/astral-sh/uv>
- Concepts guide: <https://docs.astral.sh/uv/concepts/>
- Migration guides: <https://docs.astral.sh/uv/guides/migration/>
