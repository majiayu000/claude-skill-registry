---
name: standards-python
description: This skill provides Python coding standards and is automatically loaded for Python projects. It includes naming conventions, best practices, and recommended tooling.
type: context
applies_to: [python, fastapi, django, flask, pytest, pydantic, sqlalchemy, celery, poetry, asyncio, aiohttp, httpx]
file_extensions: [".py"]
---

# Python Coding Standards

## Core Principles

1. **Simplicity**: Simple, understandable code
2. **Readability**: Readability over cleverness
3. **Maintainability**: Code that's easy to maintain
4. **Testability**: Code that's easy to test
5. **DRY**: Don't Repeat Yourself - but don't overdo it

## General Rules

- **Early Returns**: Use early returns to avoid nesting
- **Descriptive Names**: Meaningful names for variables and functions
- **Minimal Changes**: Only change relevant code parts
- **No Over-Engineering**: No unnecessary complexity
- **Minimal Comments**: Code should be self-explanatory. No redundant comments!

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Variables/Functions | snake_case | `get_user_by_id`, `is_active` |
| Classes | PascalCase | `UserService`, `ApiClient` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Private | Prefix with `_` | `_internal_method` |
| Files/Modules | snake_case | `user_service.py` |

## Project Structure

```
myproject/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Settings, env vars
│   ├── models.py            # Domain models (dataclasses/Pydantic)
│   ├── schemas.py           # Request/response DTOs
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py  # Business logic
│   └── repositories/
│       ├── __init__.py
│       └── user_repo.py     # Data access
├── tests/
│   ├── __init__.py
│   ├── test_services.py
│   └── test_repositories.py
├── pyproject.toml
└── README.md
```

## Code Style (PEP 8 + PEP 484)

```python
from dataclasses import dataclass

@dataclass
class User:
    id: str
    name: str
    email: str
    age: int | None = None  # Python 3.10+ union syntax

def get_user_by_id(user_id: str) -> User | None:
    if not user_id:
        raise ValueError("user_id cannot be empty")
    # implementation...
```

## Best Practices

```python
# Type hints everywhere
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Pydantic v2 for validation
from pydantic import BaseModel, Field, field_validator, EmailStr

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int | None = Field(None, ge=0, le=150)

    @field_validator('name')
    @classmethod
    def name_must_be_alphanumeric(cls, v: str) -> str:
        if not v.replace(' ', '').isalnum():
            raise ValueError('Name must be alphanumeric')
        return v.strip()

# Context managers
with open('file.txt', 'r') as f:
    content = f.read()

# Prefer pathlib over os.path
from pathlib import Path
config_path = Path(__file__).parent / 'config.yaml'
```

## Async/Await

```python
# Async function with proper typing
async def fetch_user(user_id: str) -> User | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/users/{user_id}")
        return User(**response.json()) if response.status_code == 200 else None

# Don't block async functions
async def process_data():
    # BAD - blocks the event loop
    time.sleep(1)

    # GOOD - async sleep
    await asyncio.sleep(1)

# Gather for concurrent operations
async def fetch_all_users(user_ids: list[str]) -> list[User]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)
```

## Exception Handling

```python
# Custom exceptions for domain errors
class UserNotFoundError(Exception):
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

# Raise vs Return None
def get_user_strict(user_id: str) -> User:
    """Raises if not found - use when user MUST exist."""
    user = repository.get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user

def get_user_optional(user_id: str) -> User | None:
    """Returns None if not found - use when absence is expected."""
    return repository.get(user_id)
```

## Comments - Less is More

```python
# BAD - redundant comment
# Get the user from database
user = repository.get_user(user_id)

# GOOD - self-explanatory code, no comment needed
user = repository.get_user(user_id)

# GOOD - comment explains WHY (not obvious)
# Rate limit: Azure API allows max 1000 requests/min
await rate_limiter.acquire()
```

## Recommended Tooling

| Tool | Purpose |
|------|---------|
| `uv` | Package manager (faster than pip/poetry) |
| `ruff` | Linting (replaces flake8, isort, black) |
| `mypy` or `pyright` | Type checking |
| `pytest` | Testing with `pytest-cov`, `pytest-asyncio` |

## Production Best Practices

1. **Type hints everywhere** - Parameters, return types, variables where helpful
2. **Pydantic for validation** - Don't validate manually, use Pydantic models
3. **Async for I/O** - Use async/await for network, database, file operations
4. **No blocking in async** - Never use `time.sleep()` or sync I/O in async functions
5. **Structured logging** - Use `logging` module with JSON format, not print()
6. **Environment variables** - Use `pydantic-settings` for config, never hardcode secrets
7. **Dependency injection** - Pass dependencies explicitly, makes testing easier
8. **Custom exceptions** - Domain-specific errors, not generic Exception
9. **Connection pooling** - Reuse database/HTTP connections, don't create per request
10. **Graceful shutdown** - Handle SIGTERM, close connections properly
