---
name: python-uv-project-setup
description: Use when initializing a Python project or script, adding dependencies, or running commands with uv, especially to avoid pip install and direct python/pytest usage.
---

# Python uv Project Setup

## Overview

Use uv for environments, dependency management, and command execution. Core principle: always install and run through uv, not pip/python directly.

## Non-Negotiable Rules

- Install dependencies with `uv add` (never `pip install`).
- Run commands with `uv run` (never direct `python` or `pytest`).

## Quick Reference

| Task | Command |
| --- | --- |
| Initialize project | `uv init <name>` |
| Add dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |
| Run Python | `uv run python <file.py>` |
| Run pytest | `uv run pytest` |
| Sync deps | `uv sync` |

## Workflow

### Project setup (package)

```bash
uv init my-project
cd my-project
uv add loguru typer
uv add --dev ruff pytest pytest-cov ty
```

### Script setup (single file)

If you are working with a script, still install with uv and run via uv:

```bash
uv add fastapi
uv run python script.py
```

## Example

Issue: "Missing fastapi. Tests fail."

Fix:
```bash
uv add fastapi
uv run pytest
```

## Common Mistakes

- Running `pip install` first and only switching to uv after it fails.
- Running `python` or `pytest` directly instead of `uv run`.

## Rationalizations to Reject

| Excuse | Reality |
| --- | --- |
| "pip install is faster for a quick fix" | It bypasses the project environment and drifts from uv-managed state. |
| "I can run python/pytest directly this once" | Direct runs skip uv's environment and can break reproducibility. |

## Red Flags

- Any instruction that uses `pip install`, `python`, or `pytest` directly.
