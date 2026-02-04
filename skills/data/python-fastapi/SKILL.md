---
name: python-fastapi
description: Complete FastAPI production system. PROACTIVELY activate for: (1) Project structure (scalable layout), (2) Pydantic schemas (input/output separation), (3) Dependency injection, (4) Async database with SQLAlchemy, (5) JWT authentication, (6) Error handling patterns, (7) Docker deployment, (8) Gunicorn + Uvicorn production, (9) Rate limiting, (10) Testing with httpx. Provides: Project templates, schema patterns, auth setup, Docker config. Ensures production-ready FastAPI applications.
---

## Quick Reference

| Layer | File | Purpose |
|-------|------|---------|
| Entrypoint | `main.py` | App factory, lifespan |
| Config | `config.py` | pydantic-settings |
| Routes | `api/v1/endpoints/` | Endpoint handlers |
| Schemas | `schemas/` | Pydantic models |
| Models | `models/` | SQLAlchemy models |
| Services | `services/` | Business logic |
| Deps | `api/deps.py` | Dependency injection |

| Pydantic Pattern | Use Case |
|------------------|----------|
| `UserCreate` | Input for creation |
| `UserUpdate` | Input for updates |
| `UserResponse` | API output |
| `UserInDB` | Internal with hash |

| Dependency | Code |
|------------|------|
| DB session | `db: Annotated[AsyncSession, Depends(get_db)]` |
| Current user | `user: Annotated[User, Depends(get_current_user)]` |
| Type alias | `CurrentUser = Annotated[User, Depends(...)]` |

| Production | Config |
|------------|--------|
| Server | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker` |
| Workers | `CPU cores` for async |

## When to Use This Skill

Use for **FastAPI development**:
- Setting up FastAPI project structure
- Creating Pydantic schemas with validation
- Implementing dependency injection
- JWT authentication setup
- Docker deployment configuration

**Related skills:**
- For async patterns: see `python-asyncio`
- For testing: see `python-testing`
- For type hints: see `python-type-hints`

---

# FastAPI Production Best Practices (2025)

## Overview

FastAPI is a modern, high-performance web framework for building APIs. Built on Starlette and Pydantic, it provides automatic validation, serialization, and OpenAPI documentation.

## Project Structure

### Scalable Structure (Recommended)

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application factory
│   ├── config.py            # Settings management
│   ├── database.py          # Database setup
│   ├── dependencies.py      # Shared dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py    # API router
│   │   │   └── endpoints/
│   │   │       ├── users.py
│   │   │       ├── items.py
│   │   │       └── auth.py
│   │   └── deps.py          # API dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # Auth/JWT
│   │   └── exceptions.py    # Custom exceptions
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   └── services/            # Business logic
│       ├── __init__.py
│       ├── user.py
│       └── item.py
├── tests/
├── pyproject.toml
└── Dockerfile
```

## Configuration

### Settings with pydantic-settings

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "My API"
    debug: bool = False
    environment: str = "production"

    # Database
    database_url: str
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # External services
    redis_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Application Factory

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.v1.router import api_router
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        openapi_url="/api/v1/openapi.json" if settings.debug else None,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url="/api/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.debug else ["https://myapp.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
```

## Pydantic Schemas

### Input/Output Separation

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Base schema with shared fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

# Input schema for creation
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Input schema for updates
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)

# Output schema (what API returns)
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# Internal schema with password hash
class UserInDB(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
```

### Validation Examples

```python
from typing import Annotated
from pydantic import BaseModel, Field, field_validator, model_validator

class ItemCreate(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=100)]
    price: Annotated[float, Field(gt=0, description="Price must be positive")]
    quantity: Annotated[int, Field(ge=0, le=10000)]
    tags: list[str] = Field(default_factory=list, max_length=10)

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def tags_must_be_unique(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")
        return v

    @model_validator(mode="after")
    def validate_price_quantity(self) -> "ItemCreate":
        if self.quantity > 0 and self.price < 0.01:
            raise ValueError("Price too low for available items")
        return self
```

## Async Best Practices

### Correct Async Usage

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

app = FastAPI()

# GOOD: Async database operations
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# GOOD: Async HTTP calls
async def fetch_external_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# BAD: Blocking call in async route
@app.get("/bad")
async def bad_endpoint():
    import time
    time.sleep(5)  # Blocks entire event loop!
    return {"status": "done"}

# GOOD: Use asyncio.sleep or run in executor
@app.get("/good")
async def good_endpoint():
    import asyncio
    await asyncio.sleep(5)  # Non-blocking
    return {"status": "done"}

# GOOD: Run blocking code in executor
@app.get("/cpu-bound")
async def cpu_bound():
    import asyncio
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, heavy_computation)
    return {"result": result}
```

### Sync vs Async Routes

```python
# Async route - for I/O-bound operations
@app.get("/async-users")
async def get_users(db: AsyncSession = Depends(get_db)):
    # Uses async database session
    users = await db.execute(select(User))
    return users.scalars().all()

# Sync route - FastAPI runs in thread pool
@app.get("/sync-compute")
def compute_heavy():
    # OK for CPU-bound operations
    # FastAPI automatically runs this in thread pool
    return {"result": heavy_cpu_computation()}
```

## Dependencies

### Dependency Injection

```python
# app/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.database import get_db
from app.config import settings
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Type aliases for cleaner signatures
CurrentUser = Annotated[User, Depends(get_current_active_user)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
```

### Using Dependencies

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, HTTPException
from app.api.deps import CurrentUser, DbSession
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: CurrentUser):
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    update_data: UserUpdate,
    current_user: CurrentUser,
    db: DbSession,
):
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
```

## Error Handling

### Custom Exception Handlers

```python
# app/core/exceptions.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

class AppException(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code

class NotFoundError(AppException):
    def __init__(self, resource: str, id: int):
        super().__init__(
            status_code=404,
            detail=f"{resource} with id {id} not found",
            error_code="NOT_FOUND",
        )

class ValidationError(AppException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR",
        )

# app/main.py
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    # Log the error
    logger.exception(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)
```

## Production Deployment

### Docker

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY src/ ./src/

# Run with uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Gunicorn with Uvicorn Workers

```python
# gunicorn.conf.py
import multiprocessing

# Workers = CPU cores (for async)
workers = multiprocessing.cpu_count()
worker_class = "uvicorn.workers.UvicornWorker"

# Timeouts
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Binding
bind = "0.0.0.0:8000"
```

```bash
# Run in production
gunicorn app.main:app -c gunicorn.conf.py
```

### Health Checks

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/ready")
async def readiness_check(db: DbSession):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")
```

## Security

### JWT Authentication

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: int | str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
```

### Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited")
@limiter.limit("10/minute")
async def limited_endpoint(request: Request):
    return {"message": "This endpoint is rate limited"}
```

## Testing

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.main import app
from app.database import get_db

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture
async def authenticated_client(client: AsyncClient, test_user_token: str):
    client.headers["Authorization"] = f"Bearer {test_user_token}"
    yield client

# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users", json={
        "email": "test@example.com",
        "password": "testpassword123",
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Additional References

For advanced patterns beyond this guide, see:

- **[Dependency Injection Patterns](references/dependency-injection-patterns.md)** - Type aliases (DbSession, CurrentUser, AdminUser), pagination dependencies, sorting/filtering, service layer patterns, request context, feature flags, rate limiting, caching dependencies
