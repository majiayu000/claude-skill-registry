---
name: python-patterns
description: Python development patterns including package manager detection (uv, poetry, pip), project structure, and idiomatic Python practices. Use when writing, reviewing, or debugging Python application code. Do NOT use for test code -- use python-testing instead.
durability: encoded-preference
---

# Python Development Patterns

## Package Manager Detection (CRITICAL)

**Before running ANY Python commands, detect the package manager:**

| File | Package Manager | Prefix |
|------|-----------------|--------|
| `uv.lock` | uv | `uv run` |
| `poetry.lock` | poetry | `poetry run` |
| `Pipfile.lock` | pipenv | `pipenv run` |
| None | pip | `python -m` |

**NEVER use `pip install` directly when lock file exists.**

## Project Structure

```
project/
├── mypackage/          # NOT src/mypackage/
│   ├── __init__.py
│   ├── __main__.py     # Entry point for python -m mypackage
│   ├── cli.py          # CLI argument parsing
│   ├── core.py         # Business logic
│   └── utils.py        # Helpers
├── tests/
├── pyproject.toml
├── uv.lock
└── Makefile
```

Flat layout (`mypackage/`) is preferred over src layout (`src/mypackage/`).

## CLI Structure (CRITICAL)

**Three-layer separation:**

```python
# mypackage/__main__.py - Minimal bootstrap
if __name__ == "__main__":
    from mypackage.cli import main
    main()

# mypackage/cli.py - CLI argument parsing only
import argparse
from mypackage.core import process_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    args = parser.parse_args()
    result = process_data(args.input)
    print(result)

# mypackage/core.py - Business logic (testable without CLI)
def process_data(input_path: str) -> str:
    ...
```

**Why:**
- `python -m mypackage` works via `__main__.py`
- Core logic is testable without invoking CLI
- Easier to reuse as library
