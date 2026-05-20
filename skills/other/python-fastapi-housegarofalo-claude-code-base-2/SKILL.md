---
name: python-fastapi
description: Build high-performance Python APIs with FastAPI. Covers async endpoints, dependency injection, Pydantic validation, OpenAPI auto-generation, OAuth2/JWT authentication, and database integration. Use when building REST APIs, microservices, or backend services with Python.
---

# FastAPI Skill

## Triggers

Use this skill when:
- Building REST APIs with Python and FastAPI
- Creating async endpoints with dependency injection
- Implementing Pydantic validation for request/response schemas
- Setting up OAuth2/JWT authentication in Python APIs
- Integrating SQLAlchemy async with FastAPI
- Writing pytest tests for API endpoints
- Keywords: fastapi, pydantic, uvicorn, python api, async api, dependency injection, openapi, sqlalchemy async

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── config.py            # Settings with pydantic-settings
│   ├── dependencies.py      # Shared dependencies
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py    # API v1 router
│   │   │   └── endpoints/
│   │   │       ├── users.py
│   │   │       └── items.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # JWT, OAuth2
│   │   └── exceptions.py    # Custom exceptions
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py       # Async session factory
│   │   └── base.py          # SQLAlchemy base
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   └── services/            # Business logic
│       ├── __init__.py
│       └── user_service.py
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── alembic/                 # Migrations
├── pyproject.toml
└── .env
```

## Application Setup

### Main Application

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.config import settings
from app.db.session import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize connections, load models
    yield
    # Shutdown: close connections
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)
```

### Configuration with pydantic-settings

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

    PROJECT_NAME: str = "FastAPI Project"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

---

## Async Endpoints

### Basic CRUD Endpoints

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[UserRead]:
    """List users with pagination."""
    service = UserService(db)
    return await service.get_many(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """Get user by ID."""
    service = UserService(db)
    user = await service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """Create new user."""
    service = UserService(db)
    return await service.create(user_in)

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserRead:
    """Update user by ID."""
    service = UserService(db)
    user = await service.update(user_id, user_in)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete user by ID."""
    service = UserService(db)
    deleted = await service.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
```

---

## Dependency Injection

### Creating Reusable Dependencies

```python
# app/dependencies.py
from typing import Annotated
from fastapi import Depends, HTTPException, status, Header

from app.core.security import verify_token
from app.db.session import get_db
from app.models.user import User
from app.services.user_service import UserService

async def get_current_user(
    token: Annotated[str, Depends(verify_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get current authenticated user from token."""
    service = UserService(db)
    user = await service.get_by_id(token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user

async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Ensure user is superuser."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user

# Type aliases for cleaner annotations
CurrentUser = Annotated[User, Depends(get_current_active_user)]
SuperUser = Annotated[User, Depends(get_current_superuser)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
```

---

## Pydantic Validation

### Request/Response Schemas

```python
# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
import re

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain digit")
        return v

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(None, min_length=1, max_length=100)
    password: str | None = Field(None, min_length=8, max_length=100)

class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime | None = None

class UserInDB(UserRead):
    hashed_password: str
```

---

## Authentication (OAuth2, JWT)

### Security Module

```python
# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")

class TokenPayload(BaseModel):
    sub: int  # user_id
    exp: datetime

class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"

def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: int, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def verify_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """Verify and decode JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        return TokenPayload(sub=user_id, exp=payload.get("exp"))
    except (JWTError, ValueError):
        raise credentials_exception
```

### Auth Endpoints

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, verify_password, TokenData
from app.dependencies import DbSession
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: DbSession = None,
) -> TokenData:
    """Authenticate user and return access token."""
    service = UserService(db)
    user = await service.get_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    access_token = create_access_token(user_id=user.id)
    return TokenData(access_token=access_token)
```

---

## Database Integration (SQLAlchemy Async)

### Async Session Setup

```python
# app/db/session.py
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=5,
    max_overflow=10,
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### SQLAlchemy Models

```python
# app/models/user.py
from datetime import datetime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    # Relationships
    items: Mapped[list["Item"]] = relationship(back_populates="owner")
```

### Service Layer Pattern

```python
# app/services/user_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_many(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit).order_by(User.id)
        )
        return list(result.scalars().all())

    async def create(self, user_in: UserCreate) -> User:
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hash_password(user_in.password),
        )
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user_id: int, user_in: UserUpdate) -> User | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        await self.db.delete(user)
        return True
```

---

## Testing with pytest

### Test Configuration

```python
# tests/conftest.py
import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

### Writing Tests

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

class TestUserEndpoints:
    async def test_create_user(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "newuser@example.com",
                "full_name": "New User",
                "password": "SecurePass123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "hashed_password" not in data

    async def test_create_user_invalid_password(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/users/",
            json={
                "email": "user@example.com",
                "full_name": "User",
                "password": "weak",
            },
        )
        assert response.status_code == 422
```

---

## Dependencies

```toml
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",          # PostgreSQL
    "aiosqlite>=0.19.0",        # SQLite (dev/test)
    "alembic>=1.13.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "httpx>=0.26.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]
```

## Quick Commands

```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest -v --cov=app tests/

# Type checking
mypy app/

# Linting
ruff check app/ tests/
ruff format app/ tests/

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
```
