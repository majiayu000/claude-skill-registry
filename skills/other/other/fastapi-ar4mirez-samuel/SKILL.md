---
name: fastapi
description: |
  FastAPI framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with FastAPI projects, or when the user mentions FastAPI.
  Provides async patterns, Pydantic models, dependency injection, and OpenAPI guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: python
  extensions: ".py"
---

# FastAPI Framework Guide

> Applies to: FastAPI 0.100+, Pydantic v2, SQLAlchemy 2.0
> Language: Python 3.10+
> Type: Async API Framework

## Overview

FastAPI is a modern, high-performance web framework for building APIs with Python based on standard type hints. Built on Starlette (web) and Pydantic (validation).

**Use FastAPI when:**
- Building REST APIs or GraphQL backends
- Need native async/await support
- Want automatic OpenAPI documentation
- Need high performance (comparable to Node.js/Go)
- Want strong type validation with Pydantic

**Consider alternatives when:**
- Need full-stack with templates (consider Django)
- Building simple scripts (consider Flask)
- Need extensive admin interface (consider Django)

## Core Principles

1. **Type-First**: Use type hints everywhere; they drive validation and docs
2. **Async by Default**: Use `async def` for I/O-bound endpoints
3. **Dependency Injection**: Use `Depends()` for shared logic and resources
4. **Thin Endpoints**: Keep route handlers thin, business logic in services
5. **Schema Validation**: Use Pydantic models for all request/response data

## Guardrails

### Code Style

- Use `async def` for endpoints with I/O operations
- Use `def` (sync) only for CPU-bound operations without I/O
- Never use sync database calls in async context
- Always use type hints on function signatures
- Run `ruff check` and `mypy` before committing

### API Design

- Version your API: `/api/v1/...`
- Use plural nouns for resources: `/users`, `/products`
- Use HTTP methods correctly: GET (read), POST (create), PUT/PATCH (update), DELETE
- Return appropriate status codes (201 for creation, 204 for deletion)
- Always set `response_model` on endpoints

### Security

- Validate all inputs with Pydantic (automatic with FastAPI)
- Use `OAuth2PasswordBearer` for token auth
- Hash passwords with bcrypt (never store plaintext)
- Set CORS origins explicitly (never use `*` in production)
- Use `Depends()` for auth checks on every protected endpoint

### Error Handling

- Use custom exception classes inheriting from `HTTPException`
- Register global exception handlers for consistent responses
- Never expose internal errors to clients
- Always wrap database errors with context

## Project Structure

```
myproject/
├── pyproject.toml
├── alembic.ini
├── alembic/
│   ├── versions/
│   └── env.py
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config.py               # Settings (pydantic-settings)
│   ├── database.py             # Async SQLAlchemy engine/session
│   ├── dependencies.py         # Shared dependencies
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── base.py             # DeclarativeBase, mixins
│   │   └── user.py
│   ├── schemas/                # Pydantic v2 schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── deps.py             # API-level dependencies (auth)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Aggregates all v1 routers
│   │       └── endpoints/
│   │           ├── users.py
│   │           └── products.py
│   ├── services/               # Business logic layer
│   │   ├── __init__.py
│   │   └── user.py
│   ├── repositories/           # Data access layer
│   │   ├── __init__.py
│   │   └── user.py
│   └── core/                   # Cross-cutting utilities
│       ├── __init__.py
│       ├── security.py         # JWT, password hashing
│       └── exceptions.py       # Custom exception classes
├── tests/
│   ├── conftest.py             # Fixtures (async client, db session)
│   ├── test_users.py
│   └── factories.py
└── docker-compose.yml
```

- `models/` = SQLAlchemy ORM (database shape)
- `schemas/` = Pydantic (API shape, validation)
- `services/` = Business logic (orchestration, rules)
- `repositories/` = Data access (queries, CRUD)

## Application Setup

### Main Application

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.database import engine
from app.models.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### Configuration

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/db"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

## Pydantic Schemas (v2)

```python
# app/schemas/user.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """Partial update: all fields optional."""
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    is_active: bool
    created_at: datetime

class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
```

**Key Pydantic v2 patterns:**
- Use `ConfigDict(from_attributes=True)` instead of `class Config: orm_mode = True`
- Use `model_dump()` / `model_validate()` instead of `.dict()` / `.from_orm()`
- Use `Field(...)` for required fields with constraints
- Use `model_dump(exclude_unset=True)` for partial updates

## Route Definitions

### Router Setup

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, products

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
```

### Endpoint Pattern

```python
# app/api/v1/endpoints/users.py
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, PaginatedResponse
from app.services.user import UserService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[UserResponse])
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get paginated list of users."""
    service = UserService(db)
    skip = (page - 1) * size
    users, total = await service.get_multi(skip=skip, limit=size)

    return PaginatedResponse(
        items=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user by ID."""
    service = UserService(db)
    user = await service.get(user_id)
    return UserResponse.model_validate(user)
```

## Dependency Injection

```python
# app/database.py — Session dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# app/api/deps.py — Auth dependencies
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_token(token)
    user = await UserRepository(db).get(payload.sub)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive or missing user")
    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user
```

**DI best practices:**
- Use `Depends()` for database sessions, auth, services
- Dependencies can depend on other dependencies (chain)
- Use `yield` dependencies for setup/teardown (e.g., DB sessions)
- Keep dependency functions small and focused

## Async Patterns

### Database (Async SQLAlchemy)

```python
# app/database.py
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False,
)
```

### Key async rules

- Use `asyncpg` driver (not `psycopg2`) for PostgreSQL
- Use `selectinload()` for eager loading relationships (avoids N+1)
- Use `await session.flush()` to get IDs without committing
- Use `await session.refresh(obj)` after flush to load defaults

## Error Handling

```python
# app/core/exceptions.py
from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(detail=detail, status_code=status.HTTP_409_CONFLICT)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)
```

Register a global handler in `main.py`:
```python
from fastapi.responses import JSONResponse

@app.exception_handler(AppException)
async def app_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
```

## Commands Reference

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Database migrations
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
alembic downgrade -1

# Testing
pytest
pytest -v --cov=app --cov-report=html
pytest tests/test_users.py -k "test_register"

# Linting & type checking
ruff check app/
ruff check app/ --fix
mypy app/
```

## Best Practices Summary

### Do
- Use Pydantic for all request/response validation
- Use dependency injection for services and sessions
- Keep endpoints thin, logic in services
- Use `async def` for I/O operations
- Handle errors with custom exceptions
- Use type hints everywhere
- Write comprehensive async tests with `httpx.AsyncClient`

### Don't
- Put business logic in endpoints
- Use sync database calls in async context
- Expose internal ORM models directly as responses
- Skip input validation
- Ignore error handling
- Use global mutable state

## Advanced Topics

For detailed patterns, full code examples, and advanced usage, see:

- [references/patterns.md](references/patterns.md) -- Repository pattern, services, testing, security, middleware, background tasks, WebSocket

## External References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Starlette Documentation](https://www.starlette.io/)
