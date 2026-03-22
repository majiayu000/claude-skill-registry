---
name: fastapi-endpoint-patterns
description: FastAPI endpoint design patterns — Pydantic models, dependency injection, async decisions, error handling, router organization, and pagination
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[endpoint file or pattern question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: python, fastapi, patterns
---

# FastAPI Endpoint Patterns

## Overview

Reference guide for idiomatic FastAPI endpoint design. Apply these patterns when building, reviewing, or refactoring API endpoints to ensure proper validation, clean dependency injection, and consistent error handling.

## Pydantic Model Design

### Request and Response Models

Always separate request models from response models. Never expose internal fields (password hashes, internal IDs) in responses.

```python
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from datetime import datetime

# Request model — what the client sends
class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v

# Response model — what the client receives
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    @computed_field
    @property
    def display_name(self) -> str:
        return self.name.title()

    model_config = {"from_attributes": True}  # Enable ORM mode

# Update model — partial updates with Optional fields
class UpdateUserRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
```

### Nested Models and Enums

```python
from enum import StrEnum

class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class AddressRequest(BaseModel):
    street: str
    city: str
    state: str = Field(min_length=2, max_length=2)
    zip_code: str = Field(pattern=r"^\d{5}(-\d{4})?$")

class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)
    notes: str | None = None

class CreateOrderRequest(BaseModel):
    items: list[OrderItemRequest] = Field(min_length=1)
    shipping_address: AddressRequest
    notes: str | None = None

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    model_config = {"from_attributes": True}

class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    items: list[OrderItemResponse]
    total: float
    created_at: datetime

    model_config = {"from_attributes": True}
```

## Dependency Injection

### The Depends Pattern

```python
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

# Database session dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Auth dependency
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await db.get(User, payload.sub)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Role-based auth dependency
def require_role(role: str):
    async def check_role(user: User = Depends(get_current_user)) -> User:
        if role not in user.roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check_role

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(require_role("admin")),
    db: AsyncSession = Depends(get_db),
):
    await db.delete(await db.get(User, user_id))
    return {"ok": True}
```

### Composing Dependencies

```python
# Service dependency that itself depends on DB and auth
class UserService:
    def __init__(self, db: AsyncSession, current_user: User):
        self.db = db
        self.current_user = current_user

    async def get_profile(self) -> UserProfile:
        return await self.db.get(UserProfile, self.current_user.id)

async def get_user_service(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UserService:
    return UserService(db=db, current_user=user)

@router.get("/profile")
async def get_profile(service: UserService = Depends(get_user_service)):
    return await service.get_profile()
```

## Async vs Sync Decision

```
Should this endpoint be async?
├── Does it call async I/O (aiohttp, asyncpg, aiofiles)?
│   └── YES → async def ✓
├── Does it call sync I/O (requests, psycopg2, open())?
│   └── YES → def (FastAPI runs it in a thread pool) ✓
├── Does it call sync CPU-bound code?
│   └── YES → def (or use run_in_executor) ✓
└── Pure computation, no I/O?
    └── def or async def — doesn't matter
```

```python
# GOOD: Async with async DB driver
@router.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# GOOD: Sync with sync library — FastAPI handles threading
@router.get("/report")
def generate_report():
    data = requests.get("https://external-api.com/data")  # sync call
    return process_report(data.json())

# BAD: async with sync I/O — blocks the event loop
@router.get("/report")
async def generate_report():
    data = requests.get("https://external-api.com/data")  # BLOCKS!
    return process_report(data.json())
```

## Error Handling

### HTTPException with Detail

```python
from fastapi import HTTPException, status

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user
```

### Custom Exception Handlers

```python
# exceptions.py
class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400):
        self.message = message
        self.code = code
        self.status_code = status_code

class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: str | int):
        super().__init__(
            message=f"{resource} {resource_id} not found",
            code="NOT_FOUND",
            status_code=404,
        )

class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT", status_code=409)

# main.py
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
```

## Router Organization

```
app/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── users.py
│   ├── posts.py
│   └── auth.py
├── models/
│   ├── user.py
│   └── post.py
├── schemas/
│   ├── user.py      # Pydantic models
│   └── post.py
├── services/
│   ├── user_service.py
│   └── post_service.py
└── dependencies.py
```

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_db)):
    ...

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(body: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    ...

# main.py
from app.routers import users, posts, auth

app = FastAPI(title="My API", version="1.0.0")
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router, prefix="/auth")
```

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_welcome_email(email: str, name: str):
    # Long-running task
    await email_client.send(to=email, subject="Welcome!", body=f"Hi {name}!")

@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    body: CreateUserRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    user = User(**body.model_dump())
    db.add(user)
    await db.flush()

    background_tasks.add_task(send_welcome_email, user.email, user.name)

    return user  # Returns immediately, email sends in background
```

## Pagination

```python
from pydantic import BaseModel, Field
from typing import Generic, TypeVar
import math
from sqlalchemy import func, select

T = TypeVar("T")

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    size: int = Field(20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    total: int
    page: int
    size: int
    pages: int

@router.get("/users", response_model=PaginatedResponse[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    total = await db.scalar(select(func.count(User.id))) or 0
    result = await db.execute(
        select(User)
        .offset(pagination.offset)
        .limit(pagination.size)
        .order_by(User.created_at.desc())
    )
    users = result.scalars().all()

    return PaginatedResponse(
        data=users,
        total=total,
        page=pagination.page,
        size=pagination.size,
        pages=math.ceil(total / pagination.size) if pagination.size > 0 else 0,
    )
```

## Anti-patterns

### No Pydantic Validation

```python
# BAD: Raw dict, no validation
@router.post("/users")
async def create_user(request: Request):
    body = await request.json()
    name = body.get("name")  # Could be None, wrong type, anything

# GOOD: Pydantic validates automatically
@router.post("/users")
async def create_user(body: CreateUserRequest):
    # body is validated, typed, and documented in OpenAPI
```

### Raw Dict Responses

Always use `response_model` to control the shape of responses. Never return raw dicts for resource endpoints.

### Sync Handlers with Async I/O Libraries

Using `async def` with `requests` blocks the event loop. Either use `httpx` (async) or `def` (sync, thread pool).

### Catching All Exceptions

```python
# BAD: Swallows all errors including programming bugs
@router.get("/users/{id}")
async def get_user(id: int):
    try:
        return await service.get(id)
    except Exception:
        return {"error": "Something went wrong"}  # No status code, no logging

# GOOD: Catch specific errors, let unexpected ones propagate
@router.get("/users/{id}")
async def get_user(id: int):
    try:
        return await service.get(id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    # Unexpected errors → 500 + FastAPI's default handler logs them
```

### No Dependency Injection

Hardcoding database sessions or auth checks in every handler creates duplication and makes testing impossible. Always use `Depends()`.
