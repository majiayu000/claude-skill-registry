---
name: python-venv
description: Manage Python virtual environments and dependencies. Use when setting up projects or installing packages.
---

## CRITICAL RULE
**ALWAYS use `.venv/bin/python` and `.venv/bin/pip` - NEVER bare `python` or `pip`**

This ensures you're using the project's virtual environment, not the system Python.

## Environment Setup

### Create New Environment
```bash
# Create venv
python3 -m venv .venv

# Activate (for interactive use)
source .venv/bin/activate

# Or use directly without activating
.venv/bin/python --version
```

### Install Dependencies
```bash
# From requirements.txt
.venv/bin/pip install -r requirements.txt

# From pyproject.toml (if using pip)
.venv/bin/pip install -e .

# From pyproject.toml (if using poetry)
poetry install

# Single package
.venv/bin/pip install package-name
```

### Update Dependencies
```bash
# Upgrade pip itself
.venv/bin/pip install --upgrade pip

# Upgrade a package
.venv/bin/pip install --upgrade package-name

# Freeze current state
.venv/bin/pip freeze > requirements.txt
```

## Dependency Files

### requirements.txt
```
requests>=2.28.0
pandas==2.0.0
pytest>=7.0.0
```

### pyproject.toml (modern)
```toml
[project]
dependencies = [
    "requests>=2.28.0",
    "pandas==2.0.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.0.0", "ruff"]
```

## Troubleshooting
- **"Module not found"**: Check you're using `.venv/bin/python`
- **Permission errors**: Don't use `sudo` with pip in venv
- **Conflicting versions**: Use `pip install --force-reinstall`
- **Corrupted venv**: Delete `.venv/` and recreate
