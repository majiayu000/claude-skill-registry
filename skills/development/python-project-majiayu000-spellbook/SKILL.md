---
name: python-project
description: Modern Python project architecture guide for 2025. Use when creating Python projects (APIs, CLI, data pipelines). Covers uv, Ruff, Pydantic, FastAPI, and async patterns.
---
# Python Project Architecture

## Core Principles

- **Type hints everywhere** — Pydantic for runtime, mypy for static
- **uv for everything** — Package management, virtualenv, Python version
- **Ruff only** — Replace Flake8 + Black + isort with single tool
- **src layout** — All code under `src/` directory
- **pyproject.toml only** — No setup.py, no requirements.txt
- **Async all the way** — Once async, stay async through call chain
- **No backwards compatibility** — Delete, don't deprecate. Change directly
- **LiteLLM for LLM APIs** — Use LiteLLM proxy for all LLM integrations

---

## No Backwards Compatibility

> **Delete unused code. Change directly. No compatibility layers.**

```python
# ❌ BAD: Deprecated decorator kept around
import warnings

def old_function():
    warnings.warn("Use new_function instead", DeprecationWarning)
    return new_function()

# ❌ BAD: Alias for renamed functions
new_name = old_name  # "for backwards compatibility"

# ❌ BAD: Unused parameters with underscore
def process(_legacy_param, data):
    ...

# ❌ BAD: Version checking for old behavior
if version < "2.0":
    # old behavior
    ...

# ✅ GOOD: Just delete and update all usages
def new_function():
    ...
# Then: Find & replace all old_function → new_function

# ✅ GOOD: Remove unused parameters entirely
def process(data):
    ...
```

---

## LiteLLM for LLM APIs

> **Use LiteLLM proxy. Don't call provider APIs directly.**

```python
# src/myapp/llm.py
from openai import AsyncOpenAI

from myapp.config import settings

# Connect to LiteLLM proxy using OpenAI SDK
client = AsyncOpenAI(
    base_url=settings.litellm_url,  # "http://localhost:4000"
    api_key=settings.litellm_api_key,
)


async def complete(prompt: str, model: str = "gpt-4o") -> str:
    """Call any LLM through LiteLLM proxy."""
    response = await client.chat.completions.create(
        model=model,  # "gpt-4o", "claude-3-opus", "gemini-pro", etc.
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""
```

---

## Quick Start

### 1. Initialize Project

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init myapp
cd myapp

# Set Python version
echo "3.12" > .python-version

# Add dependencies
uv add fastapi uvicorn pydantic sqlalchemy httpx
uv add --dev pytest pytest-asyncio ruff mypy
```

### 2. Apply Tech Stack

| Layer | Recommendation |
|-------|----------------|
| Package Manager | uv |
| Linting + Format | Ruff |
| Type Checking | mypy |
| Validation | Pydantic v2 |
| Web Framework | FastAPI |
| Database | SQLAlchemy 2.0 + asyncpg |
| HTTP Client | httpx |
| Testing | pytest + pytest-asyncio |
| Logging | structlog |

### Version Strategy

> **Always use latest. Never pin in templates.**

```toml
[project]
dependencies = [
    "fastapi",      # uv resolves to latest
    "pydantic",
    "sqlalchemy",
]
```

- `uv add` fetches latest compatible versions
- `uv.lock` ensures reproducible builds
- `uv sync` installs exact locked versions

### 3. Use Standard Structure (src layout)

```
myapp/
├── pyproject.toml         # Single config file
├── uv.lock                # Lock file (commit this)
├── .python-version        # Python version for uv
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── __main__.py    # Entry point
│       ├── main.py        # FastAPI app
│       ├── config.py      # Pydantic Settings
│       ├── models/        # Pydantic models
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/      # Business logic
│       │   ├── __init__.py
│       │   └── user.py
│       ├── repositories/  # Data access
│       │   ├── __init__.py
│       │   └── user.py
│       ├── api/           # HTTP layer
│       │   ├── __init__.py
│       │   ├── deps.py    # Dependencies
│       │   └── routes/
│       │       ├── __init__.py
│       │       └── user.py
│       └── core/          # Shared utilities
│           ├── __init__.py
│           ├── exceptions.py
│           └── logging.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # Fixtures
│   └── test_user.py
└── Makefile
```

---

## Architecture Layers

### main.py — FastAPI Application

```python
# src/myapp/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from myapp.api.routes import router
from myapp.config import settings
from myapp.core.logging import setup_logging
from myapp.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
```

### config.py — Pydantic Settings

```python
# src/myapp/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "myapp"
    debug: bool = False

    # Database
    database_url: str = "postgresql+asyncpg://localhost/myapp"

    # LiteLLM
    litellm_url: str = "http://localhost:4000"
    litellm_api_key: str = ""


settings = Settings()
```

### models/ — Pydantic Models

```python
# src/myapp/models/user.py
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = Field(default=None, min_length=2, max_length=100)


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### services/ — Business Logic

```python
# src/myapp/services/user.py
from uuid import UUID

from myapp.core.exceptions import NotFoundError, ConflictError
from myapp.models.user import User, UserCreate, UserUpdate
from myapp.repositories.user import UserRepository


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get(self, id: UUID) -> User:
        user = await self.repo.get(id)
        if not user:
            raise NotFoundError("user", str(id))
        return user

    async def create(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictError("email already exists")
        return await self.repo.create(data)

    async def update(self, id: UUID, data: UserUpdate) -> User:
        user = await self.get(id)
        return await self.repo.update(user, data)

    async def delete(self, id: UUID) -> None:
        user = await self.get(id)
        await self.repo.delete(user)
```

### api/routes/ — HTTP Handlers

```python
# src/myapp/api/routes/user.py
from uuid import UUID

from fastapi import APIRouter, Depends, status

from myapp.api.deps import get_user_service
from myapp.models.user import User, UserCreate, UserUpdate
from myapp.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=User)
async def get_user(
    id: UUID,
    service: UserService = Depends(get_user_service),
):
    return await service.get(id)


@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.create(data)


@router.patch("/{id}", response_model=User)
async def update_user(
    id: UUID,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID,
    service: UserService = Depends(get_user_service),
):
    await service.delete(id)
```

### core/exceptions.py — Custom Exceptions

```python
# src/myapp/core/exceptions.py
from fastapi import HTTPException, status


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, resource: str, id: str):
        super().__init__(f"{resource} not found: {id}", "NOT_FOUND")


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "CONFLICT")


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


# FastAPI exception handler
def app_error_to_http(error: AppError) -> HTTPException:
    status_map = {
        "NOT_FOUND": status.HTTP_404_NOT_FOUND,
        "CONFLICT": status.HTTP_409_CONFLICT,
        "VALIDATION_ERROR": status.HTTP_400_BAD_REQUEST,
    }
    return HTTPException(
        status_code=status_map.get(error.code, status.HTTP_500_INTERNAL_SERVER_ERROR),
        detail={"message": error.message, "code": error.code},
    )
```

---

## pyproject.toml

```toml
[project]
name = "myapp"
version = "0.1.0"
description = "My application"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn[standard]",
    "pydantic",
    "pydantic-settings",
    "sqlalchemy[asyncio]",
    "asyncpg",
    "httpx",
    "structlog",
]

[tool.uv]
dev-dependencies = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "mypy",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "SIM", # flake8-simplify
]

[tool.ruff.lint.isort]
known-first-party = ["myapp"]

[tool.mypy]
strict = true
python_version = "3.12"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

---


## Extended Reference

Detailed material starting at `## Testing` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
