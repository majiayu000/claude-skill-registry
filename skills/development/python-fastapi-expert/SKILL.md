---
name: python-fastapi-expert
description: Use when building FastAPI backends, creating API endpoints, implementing Pydantic models, using SQLAlchemy ORM, or working with async Python patterns for web applications.
---

# Python/FastAPI Backend Expert

## Overview
Senior-level expertise in modern Python backend development with FastAPI framework, Pydantic validation, SQLAlchemy ORM, and asynchronous programming patterns.

## When to Use
- Creating new FastAPI endpoints or routers
- Implementing request/response models with Pydantic
- Setting up database models with SQLAlchemy
- Implementing dependency injection patterns
- Working with async/await patterns
- Configuring middleware or CORS
- Implementing authentication/authorization flows

## Core Patterns

### FastAPI Endpoint Structure
```python
# Good: Clean endpoint with dependency injection
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> User:
    """Create a new user with validated input."""
    user = User(**user_data.model_dump())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

```python
# Bad: No validation, no dependency injection, mixed concerns
@app.post("/users")
async def create_user(request: Request):
    data = await request.json()
    # Direct database access, no validation
    user = User(email=data['email'], name=data['name'])
    # Synchronous DB call in async endpoint
    db.add(user)
    db.commit()
    return user
```

### Pydantic Models (V2)
```python
# Good: Comprehensive validation with field constraints
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime
```

### Dependency Injection
```python
# Good: Reusable dependencies
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine("postgresql+asyncpg://...")
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### SQLAlchemy 2.0 Models
```python
# Good: Modern SQLAlchemy with type hints
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
```

## Quick Reference: FastAPI Best Practices

| Pattern | Recommendation |
|---------|---------------|
| Route organization | Use APIRouter for modular endpoints |
| Validation | Always use Pydantic models for request/response |
| Database access | Async sessions with dependency injection |
| Error handling | HTTPException with appropriate status codes |
| Response models | Specify `response_model` for type safety |
| Async patterns | Use `async def` for I/O operations |
| Dependencies | Leverage `Depends()` for reusable components |

## Common Mistakes

**Mixing sync and async:**
```python
# Bad: Blocking call in async endpoint
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()  # Blocking!

# Good: Proper async query
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()
```

**Missing response models:**
```python
# Bad: No type safety, can leak sensitive data
@router.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, id)
    return user  # Returns model with password hash!

# Good: Explicit response model filters fields
@router.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # UserResponse excludes password_hash
```

**Poor error handling:**
```python
# Bad: Generic errors
if not user:
    raise Exception("Not found")  # 500 error

# Good: Specific HTTP exceptions
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
```

## Testing Patterns

```python
# Good: Async test with dependency override
import pytest
from httpx import AsyncClient
from app.main import app
from app.dependencies import get_db

@pytest.mark.asyncio
async def test_create_user():
    async def override_get_db():
        # Test database session
        pass

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users/",
            json={"email": "test@example.com", "name": "Test"}
        )

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Key Principles

1. **Always async for I/O**: Database, HTTP, file operations
2. **Validate everything**: Use Pydantic models for all inputs
3. **Type hints everywhere**: Leverage mypy and IDE support
4. **Dependency injection**: Reusable, testable dependencies
5. **SQLAlchemy 2.0 patterns**: Use modern mapped_column syntax
6. **Proper error handling**: HTTPException with appropriate codes
7. **Response models**: Explicit `response_model` for security and docs
