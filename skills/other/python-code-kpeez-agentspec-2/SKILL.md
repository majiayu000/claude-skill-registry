---
name: python-code
description: Python coding conventions, tooling, and style guide. Auto-loads when writing or reviewing Python code.
---

# Python Conventions

Follow these conventions when working on Python code.

## Tooling

| Task         | Command                                           |
|--------------|---------------------------------------------------|
| Install deps | `uv sync`                                         |
| Run script   | `uv run <script>.py`                              |
| Add dep      | `uv add <package>`                                |
| Remove dep   | `uv remove <package>`                             |
| Lint         | `uv run ruff check` (add `--fix` only when asked) |
| Type check   | `uv run ty check`                                 |
| Test         | `uv run pytest`                                   |

Use `uv` for everything. Do not use pip/venv/poetry directly.

## Style

- Write Pythonic code; choose the simplest construct that expresses intent
- Functional for stateless transforms; dataclasses for cohesive state/config
- Use Pydantic (or TypedDict + validators) for validating external data
- Prefer composition over inheritance; keep class hierarchies shallow
- Apply DRY and YAGNI before adding a class
- Use `lower_snake_case` for files/dirs (e.g., `routers/user_routes.py`)

## Testing

- Mirror source layout under `tests/`
- Keep fixtures minimal; prefer factory helpers over deep fixture chains
- Run before handoff: `uv run ruff check && uv run ty check && uv run pytest`

## Dependencies

- Minimize new deps; justify every addition
- Prefer stdlib first, then existing project deps
- Use `uv add`/`uv remove` to manage deps—don't edit pyproject.toml by hand
- Remove dead deps when noticed
