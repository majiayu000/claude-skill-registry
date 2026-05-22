---
name: developing-with-python
description: Python 3.11+ development with type hints, async patterns, FastAPI, and pytest. Use for backend services, CLI tools, data processing, and API development.
---

# Python Development Skill

Python 3.11+ development with modern patterns including type hints, async/await, FastAPI, and pytest.

**Progressive Disclosure**: This file provides quick reference patterns. For comprehensive guides, see [REFERENCE.md](REFERENCE.md).

## Table of Contents

1. [When to Use](#when-to-use)
2. [Quick Start](#quick-start)
3. [Project Structure](#project-structure)
4. [Type Hints](#type-hints)
5. [Dataclasses & Pydantic](#dataclasses--pydantic)
6. [FastAPI Patterns](#fastapi-patterns)
7. [Async Patterns](#async-patterns)
8. [Testing with pytest](#testing-with-pytest)
9. [Error Handling](#error-handling)
10. [Anti-Patterns](#anti-patterns)
11. [CLI Commands](#cli-commands)
12. [Configuration](#configuration)
13. [See Also](#see-also)

---

## When to Use

Loaded by `backend-developer` when:
- `pyproject.toml` or `setup.py` present
- `requirements.txt` with Python dependencies
- `.py` files in project root or `src/`
- FastAPI, Django, Flask detected

---

## Quick Start

### Basic Module

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar("T")

@dataclass
class Result(Generic[T]):
    value: T
    success: bool = True
    error: str | None = None

    @classmethod
    def ok(cls, value: T) -> Result[T]:
        return cls(value=value, success=True)

    @classmethod
    def fail(cls, error: str) -> Result[T]:
        return cls(value=None, success=False, error=error)  # type: ignore
```

### FastAPI Endpoint

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="My API", version="1.0.0")

class UserCreate(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate) -> UserResponse:
    return UserResponse(id=1, email=user.email, name=user.name)
```

---

## Project Structure

### Standard Layout (src-layout)

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py           # Entry point
│       ├── config.py         # Configuration
│       ├── models/           # Data models
│       ├── services/         # Business logic
│       ├── repositories/     # Data access
│       └── api/              # API layer
│           ├── routes/
│           └── dependencies.py
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── .python-version
```

> **More layouts**: See [REFERENCE.md#project-structure](REFERENCE.md#project-structure) for FastAPI, Django, and CLI layouts.

---

## Type Hints

### Essential Types

```python
from typing import Optional, Any
from collections.abc import Sequence, Mapping, Callable

# Basic types
name: str = "Alice"
age: int = 30
score: float = 95.5

# Optional (Python 3.10+)
middle_name: str | None = None

# Collections
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95}
coordinates: tuple[float, float] = (1.0, 2.0)

# Abstract types (prefer for function parameters)
def process_items(items: Sequence[str]) -> list[str]:
    return [item.upper() for item in items]
```

### Function Signatures

```python
from collections.abc import Callable
from typing import TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")

# Basic function
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# Async function
async def fetch_user(user_id: int) -> dict[str, Any]:
    ...

# Generic decorator (preserves signature)
def logged(func: Callable[P, T]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

> **More types**: See [REFERENCE.md#type-hints](REFERENCE.md#type-hints) for Generics, Protocols, NewType.

---

## Dataclasses & Pydantic

### Dataclasses

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)
    roles: list[str] = field(default_factory=list)

@dataclass(frozen=True)  # Immutable
class Point:
    x: float
    y: float
```

### Pydantic Models (FastAPI)

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class UserBase(BaseModel):
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Must contain uppercase")
        return v

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool = True
```

> **More patterns**: See [REFERENCE.md#classes-and-data-classes](REFERENCE.md#classes-and-data-classes) for ABCs, Protocols.

---

## FastAPI Patterns

### Application Setup

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await create_tables()  # Startup
    yield
    await engine.dispose()  # Shutdown

app = FastAPI(title="My API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
```

### Dependency Injection

```python
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db() -> AsyncIterator[AsyncSession]:
    async with get_session() as session:
        yield session

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    # Verify token and return user
    ...

# Type aliases for reuse
CurrentUser = Annotated[User, Depends(get_current_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
```

### Router Pattern

```python
from fastapi import APIRouter, HTTPException, status, Query

router = APIRouter()

@router.get("", response_model=list[UserResponse])
async def list_users(
    db: DbSession,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[UserResponse]:
    service = UserService(db)
    return await service.list(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DbSession) -> UserResponse:
    user = await UserService(db).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

> **More FastAPI**: See [REFERENCE.md#fastapi-patterns](REFERENCE.md#fastapi-patterns) for error handling, middleware.

---

## Async Patterns

### Basic Async

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def process_batch(items: list[str]) -> list[dict]:
    tasks = [fetch_data(item) for item in items]
    return await asyncio.gather(*tasks)

async def process_with_limit(items: list[str], max_concurrent: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)
    async def limited_fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)
    return await asyncio.gather(*[limited_fetch(item) for item in items])
```

### Async Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_transaction(db: AsyncSession) -> AsyncIterator[AsyncSession]:
    try:
        yield db
        await db.commit()
    except Exception:
        await db.rollback()
        raise
```

> **More async**: See [REFERENCE.md#async-await-patterns](REFERENCE.md#async-await-patterns) for generators, streaming.

---

## Testing with pytest

### Basic Tests

```python
import pytest
from unittest.mock import AsyncMock

class TestUserService:
    @pytest.fixture
    def service(self, mock_db: AsyncMock) -> UserService:
        return UserService(mock_db)

    async def test_get_user_found(self, service: UserService) -> None:
        expected = User(id=1, email="test@example.com", name="Test")
        service.repo.get.return_value = expected
        result = await service.get(1)
        assert result == expected

    async def test_get_user_not_found(self, service: UserService) -> None:
        service.repo.get.return_value = None
        result = await service.get(999)
        assert result is None
```

### Fixtures (conftest.py)

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.fixture
def override_deps(test_db: AsyncSession):
    app.dependency_overrides[get_session] = lambda: test_db
    yield
    app.dependency_overrides.clear()
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid", False),
])
def test_email_validation(email: str, valid: bool) -> None:
    if valid:
        user = User(id=1, email=email, name="Test")
        assert user.email == email
    else:
        with pytest.raises(ValueError):
            User(id=1, email=email, name="Test")
```

> **More testing**: See [REFERENCE.md#testing-with-pytest](REFERENCE.md#testing-with-pytest) for API tests, mocking.

---

## Error Handling

### Exception Hierarchy

```python
class AppError(Exception):
    def __init__(self, message: str, code: str | None = None) -> None:
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(message)

class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(f"{resource} '{identifier}' not found", code="NOT_FOUND")

class ValidationError(AppError):
    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"{field}: {message}", code="VALIDATION_ERROR")
```

> **More patterns**: See [REFERENCE.md#error-handling](REFERENCE.md#error-handling) for Result pattern.

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Mutable default `def f(items=[])` | Shared across calls | Use `items: list \| None = None` |
| Bare `except:` | Catches KeyboardInterrupt | Catch specific exceptions |
| No context managers | Resources not cleaned | Use `with`/`async with` |
| Blocking in async | Blocks event loop | Use async I/O or executor |

> **More details**: See [REFERENCE.md#anti-patterns](REFERENCE.md#anti-patterns) for examples.

---

## CLI Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"

# Run FastAPI
uvicorn myapp.main:app --reload --port 8000

# Testing
pytest                              # Run all
pytest --cov=src --cov-report=html  # With coverage

# Code quality
mypy src/ && ruff check src/ --fix && ruff format src/
```

---

## Configuration

### pyproject.toml (Essential)

```toml
[project]
name = "myapp"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.4.0", "pytest-asyncio>=0.23.0", "mypy>=1.8.0", "ruff>=0.1.0"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.mypy]
python_version = "3.11"
strict = true

[tool.ruff]
target-version = "py311"
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
```

### pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "My App"
    debug: bool = False
    database_url: str
    secret_key: str

settings = Settings()
```

> **More config**: See [REFERENCE.md#configuration](REFERENCE.md#configuration) for full examples.

---

## See Also

- **[REFERENCE.md](REFERENCE.md)** - Comprehensive guide with advanced patterns
- **[templates/](templates/)** - Code generation templates