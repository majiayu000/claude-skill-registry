---
name: uv
description: This skill should be used when working with Python projects that use uv for package and project management. Use this skill for running Python scripts and CLI tools with `uv run`, managing dependencies, creating projects, handling virtual environments, and executing commands within isolated project environments. Essential for projects with pyproject.toml files.
---

# uv - Fast Python Package and Project Manager

## Overview

This skill provides guidance for using **uv**, an extremely fast Python package and project manager written in Rust. uv replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more while being 10-100x faster. The skill focuses particularly on `uv run` for executing code within isolated project environments.

## When to Use This Skill

Use this skill when:

- Working in a Python project with a `pyproject.toml` file
- Running Python scripts or CLI tools that require dependencies
- Managing project dependencies and virtual environments
- Executing commands within an isolated project environment
- Creating new Python projects or initializing scripts
- Converting from pip, poetry, or other Python tooling to uv

## Core Concept: `uv run`

The most important command in uv is `uv run`, which executes commands within an isolated project environment.

### Why Use `uv run`

**ALWAYS use `uv run` instead of bare `python` or direct script execution when:**

1. Running Python scripts that depend on project dependencies
2. Executing Python CLI tools installed in the project
3. Working within a uv-managed project (has `pyproject.toml`)
4. Running commands that need access to the project's virtual environment

**Key behavior:** `uv run` automatically ensures the project environment is current before executing the command. It installs the project into `.venv` and keeps it isolated from the system Python.

### Basic Usage

```bash
# Run a Python script
uv run example.py

# Run a Python module
uv run python -m mymodule

# Run a CLI tool from project dependencies
uv run pytest
uv run ruff check
uv run black .

# Run external commands that need project access
uv run bash scripts/deploy.sh
```

### Adding Dependencies Per-Invocation

Use `--with` to include or override dependencies for a single execution without modifying `pyproject.toml`:

```bash
# Add a dependency temporarily
uv run --with httpx python -c "import httpx; print(httpx.__version__)"

# Specify version constraints
uv run --with 'httpx==0.26.0' python script.py

# Multiple dependencies
uv run --with httpx --with rich python script.py
```

This is useful for:

- Testing code with different dependency versions
- One-off operations requiring special packages
- Running scripts without permanently adding dependencies

### Running Scripts with Inline Dependencies

Python scripts can declare their own dependencies using inline metadata. This creates isolated environments separate from the project:

```python
# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# requires-python = ">=3.12"
# ///

import requests
import rich

# Script code here...
```

**Important:** When a script has inline metadata, `uv run` uses ONLY those dependencies and ignores the project's dependencies, even when run inside a project directory.

Initialize a script with metadata:

```bash
# Create script with inline metadata
uv init --script example.py --python 3.12

# Add dependencies to script
uv add --script example.py 'requests<3' 'rich'

# Run the script (uses its own dependencies)
uv run example.py
```

## Common Tasks and Workflows

### Creating a New Project

```bash
# Create a new application project
uv init my-project
cd my-project

# Create a library project
uv init --lib my-library

# Create project in current directory
uv init

# Specify Python version
uv init --python 3.12
```

This creates:

- `pyproject.toml` - Project configuration and dependencies
- `.python-version` - Python version specification
- `README.md` - Basic documentation
- `src/my_project/` - Source code directory (for apps)

### Managing Dependencies

```bash
# Add a dependency
uv add requests

# Add with version constraint
uv add 'httpx>=0.25,<0.27'

# Add development dependency
uv add --dev pytest

# Add optional dependency group
uv add --optional docs sphinx

# Remove a dependency
uv remove requests

# Update all dependencies
uv lock --upgrade

# Sync environment to match lockfile
uv sync
```

### Virtual Environment Management

```bash
# uv automatically creates and manages .venv/
# Most operations don't require manual venv activation

# To manually create a venv (rarely needed)
uv venv

# To activate manually (usually unnecessary)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

**Best practice:** Use `uv run` instead of manually activating virtual environments. This ensures environment consistency and automatic updates.

### Python Version Management

```bash
# Install a specific Python version
uv python install 3.12

# List available Python versions
uv python list

# Find Python installations
uv python find

# Pin project to specific Python version
uv python pin 3.12
```

### Running Tools Without Installation

```bash
# Run a tool ephemerally (like pipx)
uvx ruff check .
uvx black --check .

# Equivalent to:
uv tool run ruff check .

# Install tool globally
uv tool install ruff
```

### pip-Compatible Commands

uv provides drop-in pip replacements:

```bash
# Install packages (like pip install)
uv pip install requests

# Generate requirements.txt (like pip freeze)
uv pip freeze > requirements.txt

# Install from requirements.txt
uv pip install -r requirements.txt

# Compile dependencies (like pip-compile)
uv pip compile pyproject.toml -o requirements.txt

# Show dependency tree
uv pip tree
```

## Decision Tree: Which Command to Use

**Need to run code in this project?**
→ Use `uv run <command>`

**Need to add a package to this project?**
→ Use `uv add <package>`

**Need to run a tool once without installing?**
→ Use `uvx <tool>` or `uv tool run <tool>`

**Need to create a new project?**
→ Use `uv init [project-name]`

**Need to update dependencies to latest versions?**
→ Use `uv lock --upgrade`

**Need to sync environment after pulling changes?**
→ Use `uv sync`

**Need to install a specific Python version?**
→ Use `uv python install <version>`

**Working with legacy pip workflows?**
→ Use `uv pip` commands as drop-in replacements

## Key Differences from Other Tools

### vs pip

- **10-100x faster** due to Rust implementation
- Automatic virtual environment management
- Built-in lockfile support
- No need for pip-tools or virtualenv

### vs poetry

- Faster dependency resolution
- Compatible with standard `pyproject.toml`
- Simpler command structure
- No separate `poetry.lock` format (uses `uv.lock`)

### vs pipx

- `uvx` provides same functionality
- Faster execution
- Better caching and deduplication

### vs pyenv

- `uv python` manages Python versions
- Integrated with project management
- Faster installation and switching

## Best Practices

1. **Always use `uv run` in projects** - Don't manually activate virtual environments; let uv handle environment management automatically.

2. **Commit lockfiles** - Include `uv.lock` in version control for reproducible builds.

3. **Pin Python versions** - Use `uv python pin` to specify project Python requirements.

4. **Use `--with` for experiments** - Test dependencies temporarily without modifying `pyproject.toml`.

5. **Leverage inline metadata for scripts** - Single-file scripts should declare dependencies inline for portability.

6. **Use `uvx` for one-off tools** - Don't pollute project dependencies with tools you run occasionally.

7. **Let uv manage environments** - Trust `uv sync` to keep environments in sync; avoid manual pip installs in uv projects.

8. **Check `.python-version` files** - Respect project Python version specifications.

## Common Patterns

### Running Tests

```bash
# Add pytest as dev dependency
uv add --dev pytest pytest-cov

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov
```

### Linting and Formatting

```bash
# Add dev tools
uv add --dev ruff black mypy

# Run tools
uv run ruff check .
uv run black .
uv run mypy src/
```

### Building and Publishing

```bash
# Build distributions
uv build

# Publish to PyPI
uv publish

# Publish to test PyPI
uv publish --index-url https://test.pypi.org/legacy/
```

### Working with Scripts

```bash
# Create standalone script with dependencies
uv init --script analyze.py
uv add --script analyze.py pandas numpy

# Run script (uses its inline dependencies)
uv run analyze.py

# Lock script dependencies for reproducibility
uv lock --script analyze.py
```

## Troubleshooting

### Command not found after `uv add`

**Problem:** Added a package with a CLI tool, but command doesn't work.

**Solution:** Use `uv run <command>` to execute within project environment:

```bash
uv add ruff
uv run ruff check .  # Not just "ruff check ."
```

### Environment out of sync

**Problem:** Dependencies changed but environment hasn't updated.

**Solution:** Run `uv sync` to synchronize:

```bash
uv sync
```

### Wrong Python version

**Problem:** Project requires different Python version.

**Solution:** Install and pin correct version:

```bash
uv python install 3.12
uv python pin 3.12
```

### Script ignores project dependencies

**Problem:** Script with inline metadata doesn't use project packages.

**Solution:** This is intentional. Scripts with inline metadata are isolated. Either:

- Remove inline metadata to use project dependencies
- Add needed dependencies to script's inline metadata

## References

For detailed command options and advanced usage, see [references/cli_reference.md](references/cli_reference.md).
