---
name: python-majo
description: >
  Python development standards for Mark's workflow. Use when writing Python code,
  creating Python projects, adding type annotations, setting up Python tooling,
  or working with Python files. Covers UV project management, basedpyright type
  checking, ruff formatting, meadow Docstring Format (MDF), and Python 3.10+
  syntax preferences.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
  requires: python>=3.10
---

# Python Development Standards (Mark)

Python-specific standards following modern tooling and type-safe practices.

## Goal

Guide Python development with modern tooling (UV, basedpyright, ruff) and
consistent patterns. Ensure type-safe code with proper annotations, enforce
Python 3.10+ syntax, and maintain documentation quality through Meadow
Docstring Format (MDF).

## When to Use This Skill

**Use this skill when:**
- Writing or editing Python code (.py files)
- Setting up a new Python project
- Adding type annotations to existing code
- Running Python type checkers or linters
- Working with Python package management (UV)
- Creating Python docstrings
- Refactoring Python code for type safety
- Writing Python scripts or CLI tools

**Do NOT use this skill when:**
- Working with other programming languages
- The project uses older Python (< 3.10) without migration plans
- The codebase has existing patterns that explicitly override these standards
- Project already uses poetry/pipenv with no intent to migrate
- One-off throwaway scripts without type checking requirements

## Process

### Step 1: Identify Project Context

Check the existing project structure:

```bash
# Check what the project uses
ls pyproject.toml  # UV/poetry/pipenv
ls poetry.lock     # Poetry
ls Pipfile         # Pipenv
ls requirements.txt # pip
ls .python-version  # Python version
```

- Identify Python version target (default to 3.10+)
- Check for existing `AGENTS.md` and read it
- Understand codebase patterns from existing files
- Default to UV for new projects

### Step 2: Project Management with UV

**Use UV, not pip**:

```bash
# Project setup
uv init
uv add <package>
uv remove <package>

# Running commands
uv run <command>

# Quick tool invocation without installing
uvx <tool>
```

**Do NOT use**:
- `pip install` — use `uv add` instead
- `pip freeze` — use `uv pip freeze` or check `pyproject.toml`
- `poetry add` — use `uv add` instead (unless project uses poetry)
- `pipenv install` — use `uv add` instead (unless project uses pipenv)

### Step 3: Write Type-Annotated Code

Use Python 3.10+ syntax:

```python
# ✅ CORRECT - Python 3.10+
def process(items: list[str]) -> dict[str, int | None]:
    result: list[int] = []
    value: str | None = None
    ...

# ❌ WRONG - Old syntax
from typing import List, Dict, Union, Optional
def process(items: List[str]) -> Dict[str, Optional[int]]:
    result: List[int] = []
    value: Optional[str] = None
    ...
```

### Step 4: Add File Header and Structure

**Canonical header format:**

```python
"""
project-name: brief description
  with all my heart, 2024-2025, mark joshwel <mark@joshwel.co>
  SPDX-License-Identifier: Unlicense OR 0BSD
"""

# Standard library imports
from pathlib import Path
from typing import Final, NamedTuple

# Third-party imports (prefix to avoid pollution)
from somelib import Thing as _Thing

# Local imports
from .utils import Result

# === Constants ===
VERSION: Final[str] = "1.0.0"

# === Type Aliases ===
Query: TypeAlias = str | Path

# === Data Types ===
class Config(NamedTuple):
    debug: bool = False
```

### Step 5: Run Type Checkers

Use both basedpyright and mypy:

```bash
uv run basedpyright
uv run mypy
```

**Golden rule**: Exhaust all other options before using ignores:
1. Type narrowing with `isinstance()`, `hasattr()`, or guard clauses
2. Type guards using `TypeIs` from `typing_extensions`
3. Data contracts with proper protocols or dataclasses
4. Type stubs (`.pyi` files) for untyped third-party libraries
5. Configuration fixes in `pyproject.toml`

**Only as last resort**:
- For basedpyright: `# pyright: ignore[specificDiagnostic]`
- For mypy: `# type: ignore`

### Step 6: Format with Ruff

```bash
# Sort imports first (if new modules imported)
ruff check --select I --fix

# Format code
ruff format

# Check alongside basedpyright
ruff check
```

### Step 7: Write MDF Docstrings

Use meadow Docstring Format. See `mdf-majo` skill for full specification.

**Key Points**:
- Use backticks with Python syntax: `` `variable: Type` ``
- Sections: preamble, body, attributes/arguments, methods, returns, raises, usage
- Use latest syntax even if codebase targets older Python

### Step 8: Verify Before Committing

Both type checkers must pass without sweeping errors under the rug:

```bash
uv run basedpyright
uv run mypy
ruff check --select I --fix
ruff format
ruff check
```

## Constraints

- **ALWAYS use UV** for new projects (not pip, poetry, or pipenv)
- **ALWAYS use Python 3.10+ syntax** (`list[str]` not `List[str]`, `|` not `Union`)
- **ALWAYS include file header** with SPDX identifier
- **ALWAYS use basedpyright AND mypy** — both must pass
- **ALWAYS use `NamedTuple` over `dataclass`** unless mutability is required
- **NEVER use `# noqa` for type errors** — use proper type ignores
- **NEVER use ignores without exhausting other options first**
- **NEVER write documentation unless explicitly requested**

## Key Patterns Summary

### Result Type for Error Handling

```python
class Result(NamedTuple, Generic[ResultType]):
    value: ResultType
    error: BaseException | None = None

    def __bool__(self) -> bool:
        return self.error is None

    def get(self) -> ResultType:
        if self.error is not None:
            raise self.error
        return self.value

# Usage
def parse_file(path: Path) -> Result[Data]:
    try:
        return Result(do_parsing(path))
    except Exception as exc:
        return Result(EMPTY_DATA, error=exc)

result = parse_file(some_path)
if not result:
    print(f"error: {result.cry(string=True)}", file=stderr)
    exit(1)
data = result.get()
```

### NamedTuple Over Dataclass

```python
# ✅ PREFERRED - NamedTuple (immutable, hashable)
class Behaviour(NamedTuple):
    query: str | list[str] = ""
    debug: bool = False

# ❌ AVOID - dataclass (unless mutability required)
@dataclass
class Config:
    debug: bool = False
```

### CLI Argument Handling

**Use `sys.argv` for simple scripts:**

```python
import sys

if "-h" in sys.argv or "--help" in sys.argv:
    print("Usage: script.py [-h] [-d] [-v]")
    sys.exit(0)

debug = "-d" in sys.argv or "--debug" in sys.argv
files = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
```

**Use `argparse` for complex scripts** (subcommands, validation, required args):

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="+", help="files to process")
parser.add_argument("--format", choices=["json", "yaml"], default="json")
parser.add_argument("--verbose", "-v", action="store_true")
args = parser.parse_args()
```

### Error Handling

```python
from sys import stderr

# Error messages to stderr
print("error: surplus is not installed", file=stderr)

# Specific exit codes
def main() -> int:
    # 0. parse arguments
    # 1. validate inputs
    # 2. load data
    # 3. process
    # 4. output
    return 0  # success

if __name__ == "__main__":
    exit(main())
```

## Advanced Patterns

For detailed examples of advanced patterns, see:
- [references/ADVANCED_PATTERNS.md](references/ADVANCED_PATTERNS.md) — Walrus operator, match/case, generators, nested functions, progress bars, pathlib operations, and more

## Testing Skills

**Test implicit invocation** (without naming the skill):

| Prompt | Should Trigger? |
|--------|-----------------|
| "Help me write a Python script" | ✅ Yes |
| "I need to add type hints to this code" | ✅ Yes |
| "Set up a new Python project" | ✅ Yes |
| "Run the tests for this codebase" | ❌ No (use testing-specific skill) |
| "Explain what Python is" | ❌ No (exploratory, not actionable) |

**Constraints test:**
- Does the code use UV commands instead of pip?
- Are type annotations in Python 3.10+ syntax?
- Does the file header include SPDX identifier?
- Are both basedpyright and mypy satisfied?

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- British English spellings
- Universal code principles

Works alongside:
- `mdf-majo` - meadow Docstring Format (MDF) specification
- `mdf-md-api-docs-majo` — Writing API refs or docs from code using the MDF
- `git-majo` — For committing Python code changes
- `writing-docs-majo` — For writing Python API documentation
- `shell-majo` — For shell scripting within Python projects
- `task-planning-majo` — For planning complex Python projects
