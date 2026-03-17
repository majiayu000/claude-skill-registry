---
name: python-dev-guidelines
description: Python development guidelines for modern Python projects. Use when creating Python modules, classes, functions, scripts, or working with type hints, pytest, packaging (pip/poetry), virtual environments, async/await, data classes, or Python best practices. Covers project structure, typing, testing patterns, error handling, logging, and Pythonic idioms.
---

# Python Development Guidelines

## Purpose

Establish consistency and best practices for Python development, covering modern Python 3.12+ patterns, type safety, testing, and project organization.

---

## Standards Overview

| Category | Standard |
|----------|----------|
| **Python** | 3.12+, FastAPI, async/await preferred |
| **Formatting** | ruff (96-char lines, double quotes, sorted imports) |
| **Typing** | Strict (Pydantic v2 models preferred); `from __future__ import annotations` |
| **Naming** | `snake_case` (functions/variables), `PascalCase` (classes), `SCREAMING_SNAKE` (constants) |
| **Error Handling** | Typed exceptions; context managers for resources |
| **Documentation** | Google-style docstrings for public functions/classes |
| **Testing** | Separate test files matching source file patterns |

## When to Use This Skill

Automatically activates when working on:
- Creating or modifying Python files (`.py`)
- Writing classes, functions, or modules
- Setting up Python projects (pyproject.toml, setup.py)
- Writing tests with pytest
- Working with type hints and mypy
- Async/await patterns with FastAPI
- Package management (pip, poetry, conda)

---

## Quick Start

### New Python Project Checklist

- [ ] **Python version**: 3.12+ specified in `.python-version`
- [ ] **Project structure**: src layout or flat layout
- [ ] **pyproject.toml**: Modern packaging config with ruff
- [ ] **Type hints**: Strict typing with `from __future__ import annotations`
- [ ] **Tests**: pytest with fixtures, matching source patterns
- [ ] **Linting**: ruff (96-char lines, double quotes, sorted imports)
- [ ] **Virtual env**: venv, poetry, or conda
- [ ] **Documentation**: Google-style docstrings
- [ ] **Exceptions**: Hierarchical exceptions in `exceptions.py`

### New Module Checklist

- [ ] `from __future__ import annotations` at top
- [ ] Module docstring (Google-style)
- [ ] Type hints on all public functions
- [ ] `__all__` export list (if applicable)
- [ ] Unit tests in `tests/` mirror structure
- [ ] Error handling with typed exceptions from `exceptions.py`

---

## Project Structure

### Recommended Layout (src-layout)

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── exceptions.py     # Hierarchical typed exceptions
│       ├── core/
│       │   ├── __init__.py
│       │   └── module.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── py.typed          # PEP 561 marker
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── test_core/
│   │   └── test_module.py    # Mirrors src/mypackage/core/module.py
│   └── test_utils/
│       └── test_helpers.py   # Mirrors src/mypackage/utils/helpers.py
├── pyproject.toml
├── ruff.toml                 # ruff config (96-char, double quotes)
├── README.md
└── .python-version           # 3.12+
```

### Alternative: Flat Layout (smaller projects)

```
project/
├── mypackage/
│   ├── __init__.py
│   └── module.py
├── tests/
│   └── test_module.py
├── pyproject.toml
└── README.md
```

---

## Core Principles (7 Key Rules)

### 1. Type Everything Public (Strict Typing)

```python
from __future__ import annotations  # Always at top of file

# ❌ NEVER: Untyped public functions
def process_data(data):
    return data.upper()

# ✅ ALWAYS: Full type annotations
def process_data(data: str) -> str:
    """Process input data.

    Args:
        data: The input string to process.

    Returns:
        The processed uppercase string.
    """
    return data.upper()
```

### 2. Use Pydantic v2 for Data Models (Preferred)

```python
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field

# ✅ Pydantic v2 for validation (preferred)
class UserCreate(BaseModel):
    """User creation model with validation."""

    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserResponse(BaseModel):
    """User response model."""

    id: int
    name: str
    email: str

# For simple internal data without validation, dataclasses are acceptable
from dataclasses import dataclass

@dataclass
class InternalConfig:
    timeout: int = 30
    retries: int = 3
```

### 3. Handle Errors with Typed Hierarchical Exceptions

```python
# exceptions.py - Define hierarchical typed exceptions
from __future__ import annotations


class AppError(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ValidationError(AppError):
    """Raised when validation fails."""

    pass


class NotFoundError(AppError):
    """Raised when resource not found."""

    pass


class DatabaseError(AppError):
    """Raised when database operation fails."""

    pass


# Usage - catch specific exceptions, not general Exception
from mypackage.exceptions import ValidationError, NotFoundError

async def get_user(user_id: int) -> User:
    """Get user by ID.

    Args:
        user_id: The user's unique identifier.

    Returns:
        The user object.

    Raises:
        NotFoundError: If user does not exist.
    """
    user = await db.find(user_id)
    if not user:
        raise NotFoundError(f"User {user_id} not found")
    return user
```

### 4. Use Context Managers for Resources

```python
from __future__ import annotations
from contextlib import asynccontextmanager, contextmanager

# ❌ NEVER: Manual resource management
f = open("file.txt")
data = f.read()
f.close()

# ✅ ALWAYS: Context managers
with open("file.txt") as f:
    data = f.read()

# ✅ Sync context manager
@contextmanager
def database_transaction():
    """Manage database transaction with automatic cleanup."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# ✅ Async - use try/finally to ensure cleanup
@asynccontextmanager
async def async_db_session():
    """Manage async database session with cleanup."""
    session = await create_session()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

### 5. Prefer Composition Over Inheritance

```python
# ❌ Avoid deep inheritance
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...

# ✅ Prefer composition and protocols
from typing import Protocol

class Walker(Protocol):
    def walk(self) -> None: ...

class Dog:
    def __init__(self, legs: int = 4):
        self.legs = legs

    def walk(self) -> None:
        print(f"Walking on {self.legs} legs")
```

### 6. Use Logging, Not Print

```python
import logging

logger = logging.getLogger(__name__)

# ❌ NEVER
print(f"Processing {item}")

# ✅ ALWAYS
logger.info("Processing %s", item)
logger.error("Failed to process", exc_info=True)
```

### 7. Write Testable Code

```python
# ❌ Hard to test: hidden dependencies
def send_email(user_id: int) -> None:
    user = database.get_user(user_id)  # Hidden dependency
    smtp.send(user.email, "Hello")      # Hidden dependency

# ✅ Easy to test: explicit dependencies
def send_email(
    user: User,
    email_sender: EmailSender
) -> None:
    email_sender.send(user.email, "Hello")
```

---

## Type Hints Quick Reference

```python
from __future__ import annotations
from typing import TypeVar, Generic
from collections.abc import Callable

# Basic types (Python 3.12+)
values: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1}
value: str | None = None  # Union syntax

# Callable and Generics
handler: Callable[[int, str], bool]
T = TypeVar("T")

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
```

---

## Testing Patterns

```python
# tests/test_user_service.py - mirrors src/mypackage/services/user_service.py
from __future__ import annotations
import pytest
from mypackage.services import UserService
from mypackage.exceptions import ValidationError

class TestUserService:
    """Tests for UserService."""

    def test_create_user_success(self, mock_database):
        """Should create user with valid data."""
        service = UserService(mock_database)
        user = service.create(name="Test", email="test@example.com")
        assert user.name == "Test"

    def test_create_user_invalid_email_raises(self, mock_database):
        """Should raise ValidationError for invalid email."""
        service = UserService(mock_database)
        with pytest.raises(ValidationError, match="invalid email"):
            service.create(name="Test", email="not-an-email")
```

---

## Anti-Patterns to Avoid

❌ Mutable default arguments (`def foo(items=[])`)
❌ Bare `except:` clauses - catch specific exceptions
❌ Catching general `Exception` - use typed exceptions
❌ `from module import *`
❌ Global mutable state
❌ Ignoring type checker errors
❌ print() instead of logging
❌ String concatenation in loops (use join)
❌ Not using `if __name__ == "__main__":`
❌ Missing `from __future__ import annotations`

---

## Async Patterns (FastAPI Preferred)

```python
from __future__ import annotations
from fastapi import FastAPI, HTTPException, status
from mypackage.exceptions import ValidationError

app = FastAPI()

# ✅ FastAPI endpoint with proper error handling
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
    """Create a new user."""
    try:
        return await user_service.create(user)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

# ✅ Async error handling with exception chaining (from e)
async def process_data(data: dict) -> Result:
    """Process data with proper exception handling."""
    try:
        return await do_processing(data)
    except KeyError as e:
        raise ValidationError(f"Missing required field: {e}") from e

# ✅ Concurrent operations
async def process_items(items: list[str]) -> list[dict]:
    return await asyncio.gather(*[fetch_data(item) for item in items])
```

---

## Resource Files

### [style-guide.md](resources/style-guide.md)
Google Python Style Guide + PEP 8 practices, naming, docstrings, imports

<!-- ### [project-setup.md](resources/project-setup.md)
pyproject.toml, poetry, pip, virtual environments

### [typing-guide.md](resources/typing-guide.md)
Advanced type hints, generics, protocols, mypy configuration

### [testing-patterns.md](resources/testing-patterns.md)
pytest fixtures, mocking, parameterization, coverage

### [async-patterns.md](resources/async-patterns.md)
asyncio, aiohttp, async context managers

### [packaging.md](resources/packaging.md)
Building packages, publishing to PyPI, versioning -->

---

## Related Skills

- **cpp-dev-guidelines** - C++ development patterns
- **error-tracking** - Sentry integration for Python
- **skill-developer** - Creating and managing skills

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 450 ✅
**Progressive Disclosure**: Resource files for details ✅
