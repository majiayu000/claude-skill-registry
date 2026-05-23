---
name: uv-advanced
description: Advanced usage of uv, the extremely fast Python package and project manager from Astral. Use this skill when working with uv for project management (uv init, uv add, uv run, uv lock, uv sync), workspaces and monorepos, dependency resolution strategies (universal, platform-specific, constraints, overrides), Docker containerization, PEP 723 inline script metadata, uvx tool execution, Python version management, pip interface migration, pyproject.toml configuration, or any advanced uv workflow. Covers workspaces, resolution strategies, Docker best practices, CI/CD integration, and migration from pip/poetry/pipenv.
---

# uv Advanced Usage

uv is an extremely fast Python package and project manager written in Rust. It replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv, and more with a single unified tool that's 10-100x faster.

## Quick Reference

| Task | Command |
|------|---------|
| Create project | `uv init myproject` |
| Add dependency | `uv add requests` |
| Add dev dependency | `uv add --dev pytest` |
| Run command | `uv run python main.py` |
| Lock dependencies | `uv lock` |
| Sync environment | `uv sync` |
| Run tool | `uvx ruff check .` |
| Install Python | `uv python install 3.12` |

## Core Concepts

### Project Structure

```
myproject/
├── pyproject.toml    # Project metadata and dependencies
├── uv.lock           # Universal lockfile (commit this)
├── .venv/            # Virtual environment (gitignore)
└── src/
    └── myproject/
```

### pyproject.toml Essentials

```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["requests>=2.28", "rich"]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[dependency-groups]
test = ["pytest>=8.0", "pytest-cov"]

[tool.uv]
dev-dependencies = ["ruff", "mypy"]

[tool.uv.sources]
# Use git dependency during development
mylib = { git = "https://github.com/org/mylib", branch = "main" }
# Use workspace member
shared = { workspace = true }
# Use local path
utils = { path = "../utils", editable = true }
```

## Reference Documentation

For detailed guidance on specific topics:

- **[Projects](references/projects.md)** — Project lifecycle: init, add, run, lock, sync, build, publish
- **[Workspaces](references/workspaces.md)** — Monorepo management with shared lockfiles
- **[Resolution](references/resolution.md)** — Universal resolution, constraints, overrides, conflict handling
- **[Docker](references/docker.md)** — Container images, multi-stage builds, cache optimization
- **[Scripts & Tools](references/scripts-tools.md)** — PEP 723 inline metadata, uvx, tool management
- **[Python Versions](references/python-versions.md)** — Installing and managing Python interpreters
- **[Configuration](references/configuration.md)** — pyproject.toml, uv.toml, environment variables
- **[pip Interface](references/pip-interface.md)** — Drop-in pip replacement with advanced features

## Common Workflows

### Start a New Project

```bash
uv init myproject
cd myproject
uv add fastapi uvicorn
uv run uvicorn main:app --reload
```

### Migrate from requirements.txt

```bash
uv init
uv add -r requirements.txt
uv lock
```

### Create Reproducible Builds

```bash
# Lock with timestamp for reproducibility
uv lock --exclude-newer "2025-01-01"

# Export for pip compatibility
uv export --frozen > requirements.txt
```

### Test Against Lowest Bounds

```bash
uv run --resolution lowest pytest
```

## Key Flags

| Flag | Purpose |
|------|---------|
| `--frozen` | Use exact lockfile versions, fail if outdated |
| `--locked` | Use lockfile, fail if missing or outdated |
| `--no-dev` | Exclude development dependencies |
| `--all-extras` | Include all optional dependencies |
| `--upgrade` | Allow upgrading locked dependencies |
| `--resolution lowest` | Use lowest compatible versions |
| `--universal` | Create platform-independent resolution (pip compile) |
