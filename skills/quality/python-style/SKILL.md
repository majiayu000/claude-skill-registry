---
name: python-style
description: Python coding style enforcement (PEP standards, type hints, docstrings, modern patterns). Auto-loads when writing or reviewing Python code.
user-invocable: false
---

# Python Style Best Practices Skill

This skill automatically activates when writing Python code to ensure consistency with PEP standards, type hints, and modern Python idioms.

## Core Standards

- **PEP 8**: Naming conventions, imports, line length
- **Type Hints**: Modern syntax (`list[str]` not `List[str]`, `X | None` not `Optional[X]`)
- **Docstrings**: Google style with Args, Returns, Raises sections
- **Imports**: stdlib → third-party → local, alphabetically sorted

## Naming Conventions

```python
# Classes: PascalCase
class UserAccount:
    pass

# Functions/variables: snake_case
def calculate_total():
    user_name = "john"

# Constants: SCREAMING_SNAKE_CASE
MAX_RETRY_COUNT = 3

# Private: single underscore prefix
def _internal_helper():
    pass
```

## Type Hints (Python 3.10+)

```python
# Use built-in generics
def process(items: list[str]) -> dict[str, int]:
    pass

# Use | for Optional/Union
def find_user(id: str) -> User | None:
    pass

# TypedDict for structured dicts
class UserData(TypedDict):
    id: str
    name: str
```

## Function Length Guidelines

- **< 30 lines**: Ideal
- **30-50 lines**: Review for refactoring
- **> 50 lines**: Must be broken down

## Anti-Patterns to Avoid

- Missing type hints
- Bare `except:` clauses
- Magic numbers/strings without constants
- Non-expressive variable names (`d`, `temp`, `x`)
- Vague function names (`process`, `handle`, `do_stuff`)

## Merge-Friendly Patterns (for Parallel Development)

When multiple agents modify the same module, follow these patterns to enable automatic merge resolution by semantic merge tools (mergiraf).

### Always Run Ruff Before Commit

```bash
uv run ruff format .
uv run ruff check --fix .
```

This ensures imports are consistently ordered, enabling clean merges.

### `__all__` Must Be Alphabetical

Enable **RUF022** in ruff to enforce this automatically:

```toml
[tool.ruff.lint]
select = [
    # ... other rules
    "RUF022", # unsorted-dunder-all (enforces alphabetical __all__)
]
```

```python
# CORRECT - alphabetical, one per line, no comments
__all__ = [
    "ACLFilterSpec",
    "Chunk",
    "ChunkerInterface",
    "Document",
    "QueryACLContext",
    "Visibility",
]

# WRONG - grouped by category (causes merge conflicts)
__all__ = [
    # Types
    "Chunk",
    "Document",
    # Interfaces
    "ChunkerInterface",
]
```

### No Comments Inside Lists

Comments inside `__all__`, import groups, or other lists break deterministic ordering and cause merge conflicts. Keep comments outside:

```python
# ACL and schema types exported for public API
__all__ = [
    "ACLFilterSpec",
    "Chunk",
    "Document",
]
```

### When Adding to Shared Files (`__init__.py`, etc.)

1. Add new exports in **alphabetical position**
2. Never reorder existing exports
3. Run `ruff format` immediately after changes
4. Avoid adding section comments

### Why This Matters

Semantic merge tools like mergiraf can automatically resolve conflicts when:
- Both branches add items to the same list in alphabetical order
- No comments or groupings change the structure
- Formatting is consistent (via ruff)

Without these patterns, parallel agents adding exports to the same `__init__.py` will create conflicts requiring manual resolution.
