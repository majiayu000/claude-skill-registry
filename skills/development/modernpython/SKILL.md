---
name: modernpython
description: Apply modern Python 3.11+ best practices with proper types, DRY, SRP, and framework patterns. Use when reviewing Python code for modernization opportunities, when writing new Python code to ensure modern patterns, or when refactoring legacy Python code to use current idioms.
user-invocable: true
argument-hint: "[file-paths-or-topic]"
---

# Python Modernization Guide

The model applies modern Python 3.11+ patterns when writing or reviewing Python code.

## Arguments

$ARGUMENTS

## Instructions

If file paths provided:

1. Read each file
2. Identify legacy patterns
3. Apply modern transformations from the reference guide
4. Report changes made or recommended

If topic provided (e.g., "typing", "match-case"):

1. Provide guidance on that specific topic
2. Show before/after examples

If no arguments:

1. Ask what code to review or what topic to explain

---

## Quick Reference: Modern Patterns

### Type Hints (PEP 585, 604)

```python
# Legacy (NEVER use)
from typing import List, Dict, Optional, Union

# Modern (ALWAYS use)
items: list[str]
config: dict[str, int] | None
value: int | str
```

### Walrus Operator (PEP 572)

```python
# Legacy
data = fetch_data()
if data:
    process(data)

# Modern
if data := fetch_data():
    process(data)
```

### Match-Case (PEP 634)

Use match-case when using elif. Use if/elif only for inequalities or boolean operators.

```python
# Modern (for any elif pattern)
match status_code:
    case 200: return "OK"
    case 404: return "Not Found"
    case _: return "Unknown"
```

### Self Type (PEP 673)

```python
from typing import Self

class Builder:
    def add(self, x: int) -> Self:
        self.value += x
        return self
```

### Exception Notes (PEP 678)

```python
except FileNotFoundError as e:
    e.add_note(f"Attempted path: {path}")
    raise
```

### StrEnum (Python 3.11+)

```python
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
```

### TOML Support (Python 3.11+)

```python
import tomllib
from pathlib import Path

config = tomllib.load(Path("pyproject.toml").open("rb"))
```

---

## Testing Patterns

ALWAYS use pytest-mock, NEVER unittest.mock:

```python
# Legacy (NEVER use)
from unittest.mock import Mock, patch

# Modern (ALWAYS use)
from pytest_mock import MockerFixture

def test_feature(mocker: MockerFixture) -> None:
    mock_func = mocker.patch('module.function', return_value=42)
```

---

## Framework Patterns

### Typer CLI

ALWAYS use Annotated syntax:

```python
from typing import Annotated
import typer

@app.command()
def process(
    input_file: Annotated[Path, typer.Argument(help="Input file")],
    verbose: Annotated[bool, typer.Option("--verbose", "-v")] = False,
) -> None:
    """Process input file."""
    pass
```

### Rich Tables

Use explicit width control for production CLIs:

```python
from rich.console import Console
from rich.table import Table
from rich.measure import Measurement

def _get_table_width(table: Table) -> int:
    temp_console = Console(width=9999)
    measurement = Measurement.get(temp_console, temp_console.options, table)
    return int(measurement.maximum)
```

---

## Detailed Reference

For complete transformation rules, PEP references, and framework patterns, see:

[Complete Modernization Guide](./references/modernization-guide.md)

---

## Core Principles

1. Use Python 3.11+ as minimum baseline
2. Leverage built-in generics (PEP 585) and pipe unions (PEP 604) exclusively
3. Apply walrus operator to reduce line count
4. Use match-case for elif patterns
5. Implement comprehensive type hints with Protocol, TypeVar, TypeGuard
6. Use Self type (PEP 673) for fluent APIs
7. Follow Typer patterns with Annotated syntax for CLIs
8. Use Rich for terminal output with proper width handling
9. Write pytest tests with pytest-mock and AAA pattern
10. Apply clean architecture with dependency injection

---

## References

- [PEP 585 - Builtin Generics](https://peps.python.org/pep-0585/)
- [PEP 604 - Union Syntax](https://peps.python.org/pep-0604/)
- [PEP 634 - Structural Pattern Matching](https://peps.python.org/pep-0634/)
- [PEP 673 - Self Type](https://peps.python.org/pep-0673/)
- [PEP 678 - Exception Notes](https://peps.python.org/pep-0678/)
- [What's New in Python 3.11](https://docs.python.org/3.11/whatsnew/3.11.html)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Rich Documentation](https://rich.readthedocs.io/)
