---
name: python-cli-typer
description: Use when building or structuring Python CLI commands with Typer, including commands, options, and multi-command apps.
---

# Python CLI with Typer

## Overview

Use Typer for ergonomic CLI construction. Core principle: keep CLI entry points explicit and testable.

## Install

```bash
uv add typer
```

## Quick Reference

| Task | Pattern |
| --- | --- |
| Single command | `@app.command()` |
| Options | function args with defaults |
| Multiple commands | multiple `@app.command()` |

## Workflow

- Define a `typer.Typer()` app in `cli.py`.
- Keep command functions small; move logic into separate modules.
- Run CLI via `uv run python -m <module>` or `uv run python cli.py`.

## Example

```python
import typer

app = typer.Typer()

@app.command()
def greet(name: str, count: int = 1) -> None:
    for _ in range(count):
        typer.echo(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

Usage:
```bash
uv run python cli.py --help
uv run python cli.py Alice
uv run python cli.py Alice --count 3
```

Multiple commands:
```python
import typer

app = typer.Typer()


@app.command()
def create(name: str) -> None:
    """Create a new item."""
    typer.echo(f"Creating {name}...")


@app.command()
def delete(name: str, force: bool = False) -> None:
    """Delete an item."""
    if not force:
        if not typer.confirm(f"Delete {name}?"):
            raise typer.Abort()
    typer.echo(f"Deleted {name}")


if __name__ == "__main__":
    app()
```

## Common Mistakes

- Putting heavy business logic inside CLI functions.
- Forgetting to wire `if __name__ == "__main__"` for script entry.

## Red Flags

- CLI guidance that ignores Typer when Typer is the chosen framework.
