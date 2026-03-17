---
name: uv
description: This skill should be used when working with Python projects that use uv for package and project management. Use this skill for running Python scripts and CLI tools with `uv run`, managing dependencies, creating projects, handling virtual environments, and executing commands within isolated project environments. Essential for projects with pyproject.toml files.
---

# uv - Python Package and Project Manager

## Contents

- [Core Concept: uv run](#core-concept-uv-run)
- [Quick Reference](#quick-reference)
- [Common Workflows](#common-workflows)
- [Dependency Management](#dependency-management)
- [Python Version Management](#python-version-management)
- [Scripts with Inline Dependencies](#scripts-with-inline-dependencies)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Core Concept: uv run

**ALWAYS use `uv run` instead of bare `python` in uv-managed projects.**

`uv run` automatically:

- Creates/updates the virtual environment
- Installs project dependencies
- Executes commands in isolation

```bash
# Run Python scripts
uv run script.py

# Run CLI tools
uv run pytest
uv run ruff check .

# Run Python modules
uv run python -m mymodule
```

## Quick Reference

### Essential Commands

| Task | Command |
|------|---------|
| Run script | `uv run script.py` |
| Run CLI tool | `uv run pytest` |
| Add dependency | `uv add requests` |
| Add dev dependency | `uv add --dev pytest` |
| Remove dependency | `uv remove requests` |
| Sync environment | `uv sync` |
| Update dependencies | `uv lock --upgrade` |
| Create project | `uv init my-project` |

### Decision Tree

| Need to... | Use |
|------------|-----|
| Run code in project | `uv run <command>` |
| Add package to project | `uv add <package>` |
| Run tool once without installing | `uvx <tool>` |
| Create new project | `uv init [name]` |
| Update all dependencies | `uv lock --upgrade` |
| Sync after pulling changes | `uv sync` |
| Install Python version | `uv python install <version>` |

## Common Workflows

### 1. Create New Project

```bash
uv init my-project        # Application
uv init --lib my-library  # Library
uv init                   # In current directory
uv init --python 3.12     # Specify Python version
```

Creates: `pyproject.toml`, `.python-version`, `README.md`, `src/`

### 2. Add Dependencies

```bash
uv add requests                    # Runtime
uv add 'httpx>=0.25,<0.27'        # With constraints
uv add --dev pytest pytest-cov    # Development
uv add --optional docs sphinx     # Optional group
```

### 3. Run Tests and Tools

```bash
uv run pytest
uv run pytest --cov
uv run ruff check .
uv run mypy src/
```

### 4. Update Dependencies

```bash
uv lock --upgrade               # Upgrade all
uv lock --upgrade-package numpy # Upgrade one
uv sync                         # Apply changes
```

### 5. Build and Publish

```bash
uv build                        # Build package
uv publish                      # Publish to PyPI
```

## Dependency Management

### Adding Dependencies

| Type | Command |
|------|---------|
| Runtime | `uv add requests` |
| Development | `uv add --dev pytest` |
| Optional group | `uv add --optional docs sphinx` |
| With constraints | `uv add 'numpy>=1.20,<2.0'` |

### Temporary Dependencies

Use `--with` for one-off operations without modifying `pyproject.toml`:

```bash
uv run --with httpx python -c "import httpx"
uv run --with rich --with httpx script.py
```

### Syncing Environment

```bash
uv sync              # Sync all
uv sync --no-dev     # Without dev deps
uv sync --all-extras # Include optional groups
```

## Python Version Management

```bash
uv python install 3.12    # Install version
uv python list            # List available
uv python pin 3.12        # Pin for project
uv python find            # Find installations
```

## Scripts with Inline Dependencies

Scripts can declare their own dependencies, isolated from the project:

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
```

### Managing Script Dependencies

```bash
uv init --script analyze.py --python 3.12   # Create script
uv add --script analyze.py pandas           # Add dependency
uv run analyze.py                           # Run (uses inline deps)
uv lock --script analyze.py                 # Lock dependencies
```

**Note:** Scripts with inline metadata ignore project dependencies.

## Tools Without Installation

```bash
uvx ruff check .          # Run tool ephemerally
uvx black --check .
uv tool install ruff      # Install globally
uv tool list              # List installed tools
```

## Troubleshooting

### Command Not Found After `uv add`

**Problem:** Added package with CLI, but command doesn't work.

**Solution:** Use `uv run`:

```bash
uv add ruff
uv run ruff check .  # Not just "ruff check ."
```

### Environment Out of Sync

**Problem:** Dependencies changed but environment hasn't updated.

**Solution:**

```bash
uv sync
```

### Wrong Python Version

**Problem:** Project requires different Python.

**Solution:**

```bash
uv python install 3.12
uv python pin 3.12
```

### Script Ignores Project Dependencies

**Problem:** Script with inline metadata doesn't use project packages.

**Solution:** This is intentional. Either:

- Remove inline metadata to use project deps
- Add needed deps to script's inline metadata

## Best Practices

1. **Always use `uv run`** - Don't manually activate venvs
2. **Commit `uv.lock`** - Ensures reproducible builds
3. **Pin Python versions** - Use `uv python pin`
4. **Use `--with` for experiments** - Test deps without modifying pyproject.toml
5. **Use `uvx` for one-off tools** - Don't pollute project deps
6. **Let uv manage envs** - Avoid manual pip installs

## References

### Project References

- [CLI Reference](references/cli_reference.md) - Complete command documentation

### External Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [CLI Reference](https://docs.astral.sh/uv/reference/cli/)
- [GitHub](https://github.com/astral-sh/uv)
