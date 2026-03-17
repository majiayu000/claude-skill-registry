---
name: "uv"
description: "how to run python files and mangage dependencies using UV package manager (pip replacement)"
---

You are working with a Python project that uses UV package manager. UV is a fast package manager serving as a drop-in replacement for pip, pip-tools, and virtualenv.

## Core Commands

### Project Setup
```bash
uv sync                           # Install all default AND dev dependencies from pyproject.toml
```

### Running Commands
```bash
uv run python script.py           # Run Python with project dependencies
```

### Adding Dependencies
```bash
uv add package-name               # Add to [project.dependencies]
uv add --dev package-name         # Add to [dependency-groups.dev]
```

## CRITICAL: Anti-Patterns

### **NEVER use bare `python`**
```bash
# FORBIDDEN:
python ...
python3 ...
```

**INSTEAD**: Always use `uv run python ...`

### **NEVER use `pip`**
```bash
# FORBIDDEN:
uv pip ...
pip ...
python -m pip ...
uv run python -m pip ...
```

**INSTEAD**: Use `uv add` and `uv sync`

## Instructions

When working with Python files in this project:
1. Always use `uv run python` instead of bare `python` commands
2. Install dependencies with `uv add`, never with `pip`
3. Sync dependencies with `uv sync` after modifying pyproject.toml
4. Run scripts and tools through `uv run` to ensure correct environment
