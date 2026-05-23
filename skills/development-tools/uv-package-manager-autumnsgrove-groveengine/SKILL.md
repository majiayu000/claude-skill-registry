---
name: uv-package-manager
description: Manage Python projects and dependencies using UV, the ultra-fast Rust-based package manager. Use when creating Python projects, managing dependencies, or running Python scripts.
---

# UV Package Manager Skill

## When to Activate

Activate this skill when:
- Creating new Python projects
- Adding or removing dependencies
- Running Python scripts or tools
- Managing virtual environments
- Setting up Python version management

## Why UV?

- **10-100x faster** than pip (Rust implementation)
- **Unified tool** - replaces pip, pip-tools, poetry, pyenv, virtualenv
- **Reliable** - lock files for reproducible builds
- **Modern** - built for current Python workflows

## Quick Commands

```bash
# Project Management
uv init                      # Create new project
uv init --package my-lib     # Create installable package

# Dependencies
uv add requests              # Add dependency
uv add --dev pytest          # Add dev dependency
uv remove package-name       # Remove dependency

# Running Code
uv run script.py             # Run Python script
uv run pytest                # Run installed tool
uv run python -m module      # Run module

# Environment
uv sync                      # Sync dependencies
uv sync --frozen             # Sync without updating lock
uv lock                      # Update lock file
uv python install 3.12       # Install Python version
```

## Creating Projects

```bash
# Standard project
uv init my-project
cd my-project

# Package project (for libraries)
uv init --package my-library

# Specify Python version
uv init --python 3.11
```

### Created Structure

```
my-project/
├── .python-version    # Python version
├── pyproject.toml     # Project config
├── .venv/             # Virtual environment (auto-created)
└── hello.py           # Sample script
```

## Adding Dependencies

```bash
# Basic add
uv add requests fastapi uvicorn

# With version constraints
uv add "django>=4.2,<5.0"
uv add "requests==2.31.0"
uv add "fastapi[all]"

# Dev dependencies
uv add --dev pytest black ruff mypy

# From git
uv add --git https://github.com/user/repo --branch develop
```

## Running Scripts

```bash
# Run Python script
uv run script.py

# Run with arguments
uv run script.py --input data.csv

# Run dev tools
uv run pytest tests/ -v
uv run black .
uv run ruff check .

# Run with temporary dependency
uv run --with httpx fetch_data.py

# Start Python REPL
uv run python
```

## Virtual Environment

UV automatically manages virtual environments:

```bash
# Created automatically on first use
uv sync          # First sync
uv add package   # First package add
uv run script.py # First run

# Manual creation
uv venv
uv venv --python 3.11

# Manual activation (rarely needed)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

## Lock Files

```bash
# Generate/update lock file
uv lock

# Sync from lock (normal)
uv sync

# Sync without updating (CI/CD)
uv sync --frozen

# Update specific package
uv lock --upgrade-package requests

# ALWAYS commit these files:
# - pyproject.toml
# - uv.lock
# - .python-version
```

## Python Version Management

```bash
# List available versions
uv python list

# Install specific version
uv python install 3.12

# Set project version
echo "3.12" > .python-version
```

## Migration from pip

```bash
# Import requirements.txt
uv init my-project
cd my-project
uv add -r requirements.txt

# Import dev requirements
uv add --dev -r requirements-dev.txt
```

## Common pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.100.0",
    "uvicorn>=0.20.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
]
```

## Best Practices

### DO ✅
- Commit `uv.lock` and `.python-version`
- Use semantic versioning for dependencies
- Use `--dev` for development tools
- Use `uv run` instead of manual activation
- Use `--frozen` in CI/CD

### DON'T ❌
- Commit `.venv/` directory
- Use `*` for version constraints
- Mix pip and uv in same project
- Skip lock file updates after changes

## Troubleshooting

```bash
# Clear cache
uv cache clean

# Verbose mode for debugging
uv --verbose add package

# Regenerate lock
uv lock
uv sync
```

## Related Resources

See `AgentUsage/uv_usage.md` for complete documentation including:
- Docker integration patterns
- Workspace support for monorepos
- CI/CD configuration
- Detailed migration guides
