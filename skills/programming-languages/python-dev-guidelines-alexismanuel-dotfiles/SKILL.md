---
name: python-dev-guidelines
description: Python conventions, patterns, and workflows. Use when writing code, reviewing PRs, or setting up new Python projects.
---

# Python Development Guidelines

## Philosophy

**Strong preferences, pragmatic adaptation.**

- On new projects: Apply these patterns fully
- On existing projects: Respect existing conventions, introduce patterns gradually

## When to Use

- Writing new Python code
- Writing or reviewing tests
- Setting up new Python projects
- Debugging import, exception, or testing issues

## Tooling

| Tool | Purpose |
|------|---------|
| **uv** | Package management, virtual environments |
| **ruff** | Linting + formatting (replaces flake8, isort, black) |
| **mypy** | Type checking (standard mode) |
| **alembic** | Database migrations (if existing in project) |
| **pytest** | Testing framework |
| **pytest-asyncio** | Async test support |

## Code Style

| Category | Standard |
|----------|----------|
| Line length | 119 characters |
| Import order | isort-style (project first, then third-party) |
| Type annotations | Full coverage ideal, gradual pragmatically |
| Naming | PEP8 (ClassNames, snake_case_functions) |
| Docstrings | Google-style on all public functions |
| Complexity | Max 12, extract ruthlessly into small functions |

### Import Order

```python
# Project imports first
from app.api.v1.users.repository import UserRepository
from app.api.v1.users.exceptions import UserNotFoundError
from app.database import get_session

# Third-party imports
import structlog
from fastapi import HTTPException
from pydantic import BaseModel
```

## Project Structure

Vertical slices mirroring API routes:

```
app/
├── api/
│   └── v1/
│       ├── users/
│       │   ├── __init__.py
│       │   ├── router.py        # API routes
│       │   ├── service.py       # Business logic
│       │   ├── repository.py    # Data access
│       │   ├── models.py        # SQLAlchemy/Pydantic models
│       │   └── exceptions.py    # Domain exceptions
│       └── orders/
│           └── ...              # Same structure
├── database.py                  # Cross-cutting: DB connection
├── config.py                    # Cross-cutting: Settings
├── logging.py                   # Cross-cutting: Logging setup
└── main.py
```

## Error Handling

**For new projects**: Error as Value pattern - functions return `(result, error)` tuples.
**For existing projects**: Respect existing try/except patterns.

### Why Error as Value?
- Explicit handling at every call site (Go-style discipline)
- Type system forces callers to handle errors
- No hidden control flow from exceptions

### Domain Exceptions

Flat hierarchy in dedicated `exceptions.py`:

```python
class UserNotFoundError(Exception):
    """Raised when user lookup returns no results."""
    pass

class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""
    pass
```

### Repository Layer

```python
from app.api.v1.users.exceptions import DatabaseConnectionError, DatabaseQueryError

async def get_by_id(
    session: AsyncSession,
    user_id: str,
) -> tuple[User | None, DatabaseConnectionError | DatabaseQueryError | None]:
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none(), None
    except OperationalError as e:
        return None, DatabaseConnectionError(f"Connection failed: {e}")
    except SQLAlchemyError as e:
        return None, DatabaseQueryError(f"Query failed: {e}")
```

### Service Layer

```python
async def get_user(
    session: AsyncSession,
    user_id: str,
) -> tuple[User | None, ServiceError | None]:
    user, error = await repository.get_by_id(session, user_id)
    
    match error:
        case DatabaseConnectionError() | DatabaseQueryError():
            return None, ServiceError(f"Failed to fetch user {user_id}: {error}")
        case None if user is None:
            return None, ServiceError(f"User {user_id} not found")
        case None:
            return user, None
```

### Route Layer

```python
@router.get("/users/{user_id}")
async def get_user(user_id: str, session: AsyncSession = Depends(get_session)):
    user, error = await service.get_user(session, user_id)
    
    match error:
        case ServiceError() if "not found" in str(error):
            raise HTTPException(status_code=404, detail=str(error))
        case ServiceError():
            raise HTTPException(status_code=500, detail=str(error))
        case None:
            return user
```

## Testing

**See `python-testing-guidelines` skill for full details.**

Key principles:
- **New code ships with tests** - When implementing new functionality (validators, methods, classes), always add corresponding tests in the same task. Don't wait to be asked.
- **Never use mocks** - No `Mock`, `MagicMock`, `AsyncMock`, or `patch()`
- **Dummy classes only** - Inherit from real classes, track state for assertions
- **Test structure mirrors source** - `app/api/v1/users/` → `tests/api/v1/users/`

## Configuration

**New projects**: Pydantic Settings

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    api_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

**Existing projects**: Adapt to existing pattern.

## Logging

| Context | Approach |
|---------|----------|
| Services, APIs | Structured logging (`structlog`) |
| Scripts, tools | `print()` or basic `logging` |

## Async

| Context | Approach |
|---------|----------|
| Services, APIs | `async`/`await` |
| Scripts, CLI tools | Sync |

## Dependency Injection

Prefer explicit injection:

```python
# Good - explicit
async def get_user(user_id: str, repository: UserRepository):
    return await repository.get_by_id(user_id)

# Acceptable - module singleton for breaking circular deps
_session_factory = None

def get_session_factory():
    global _session_factory
    if _session_factory is None:
        _session_factory = create_session_factory()
    return _session_factory
```
