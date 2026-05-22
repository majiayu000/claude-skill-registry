---
name: python-clean-architecture
description: Clean architecture patterns for Python services — service layer, repository pattern, domain models, dependency injection, error hierarchy, and testing strategy
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Bash
argument-hint: "[file path or architecture question]"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: python, architecture, patterns
---

# Python Clean Architecture

## Overview

Reference guide for structuring Python services with clean architecture. Apply these patterns to separate business logic from framework concerns, making code testable, maintainable, and framework-independent.

## Project Structure

```
src/
├── domain/              # Core business logic — NO framework imports
│   ├── models/          # Domain entities and value objects
│   │   ├── user.py
│   │   └── order.py
│   ├── errors.py        # Domain-specific exceptions
│   └── services/        # Business logic / use cases
│       ├── user_service.py
│       └── order_service.py
├── infrastructure/      # External concerns
│   ├── repositories/    # Data access implementations
│   │   ├── user_repo.py
│   │   └── order_repo.py
│   ├── external/        # Third-party API clients
│   │   └── payment_client.py
│   └── db.py            # Database connection setup
├── api/                 # Framework layer (FastAPI, Flask, etc.)
│   ├── routers/
│   │   ├── users.py
│   │   └── orders.py
│   ├── dependencies.py  # DI wiring
│   └── error_handlers.py
└── main.py
```

**Key rule**: Dependencies point inward. `domain/` imports nothing from `infrastructure/` or `api/`. `infrastructure/` imports from `domain/`. `api/` imports from both.

## Domain Models (vs ORM Models)

Domain models represent business concepts with behavior. ORM models represent database tables. Keep them separate.

```python
# domain/models/user.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

class UserRole(StrEnum):
    MEMBER = "member"
    ADMIN = "admin"

@dataclass
class User:
    id: str
    email: str
    name: str
    role: UserRole
    created_at: datetime
    is_active: bool = True

    def promote_to_admin(self) -> None:
        if not self.is_active:
            raise InactiveUserError(self.id)
        self.role = UserRole.ADMIN

    def deactivate(self) -> None:
        self.is_active = False

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN


# domain/models/order.py
@dataclass
class OrderItem:
    product_id: str
    quantity: int
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price

@dataclass
class Order:
    id: str
    user_id: str
    items: list[OrderItem] = field(default_factory=list)
    status: str = "draft"

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)

    def add_item(self, product_id: str, quantity: int, unit_price: float) -> None:
        if self.status != "draft":
            raise OrderNotEditableError(self.id, self.status)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self.items.append(OrderItem(product_id, quantity, unit_price))

    def submit(self) -> None:
        if not self.items:
            raise EmptyOrderError(self.id)
        self.status = "submitted"
```

### ORM Model — Separate Concern

ORM models mirror the database schema and may include fields not in the domain model (e.g., `password_hash`). Map between ORM and domain models in the repository layer.

```python
# infrastructure/db_models/user_model.py
class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="member")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    password_hash = Column(String, nullable=False)  # Not in domain model
```

## Repository Pattern

Define abstract interfaces in the domain layer. Implement in infrastructure.

```python
# domain/repositories.py
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...
    @abstractmethod
    async def save(self, user: User) -> None: ...
    @abstractmethod
    async def delete(self, user_id: str) -> None: ...

class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, order_id: str) -> Order | None: ...
    @abstractmethod
    async def save(self, order: Order) -> None: ...
```

### Repository Implementation

```python
# infrastructure/repositories/user_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.repositories import UserRepository
from domain.models.user import User, UserRole

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: str) -> User | None:
        model = await self._session.get(UserModel, user_id)
        return self._to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None

    async def save(self, user: User) -> None:
        model = await self._session.get(UserModel, user.id)
        if model is None:
            model = UserModel(id=user.id)
            self._session.add(model)
        model.email = user.email
        model.name = user.name
        model.role = user.role.value
        model.is_active = user.is_active
        model.created_at = user.created_at

    async def delete(self, user_id: str) -> None:
        model = await self._session.get(UserModel, user_id)
        if model:
            await self._session.delete(model)

    @staticmethod
    def _to_domain(model: UserModel) -> User:
        return User(
            id=model.id, email=model.email, name=model.name,
            role=UserRole(model.role), is_active=model.is_active,
            created_at=model.created_at,
        )
```

## Service Layer

Services contain business logic. They depend on repository abstractions, never on concrete implementations or frameworks.

```python
# domain/services/user_service.py
from domain.models.user import User, UserRole
from domain.repositories import UserRepository
from domain.errors import NotFoundError, ConflictError

class UserService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def get_user(self, user_id: str) -> User:
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user

    async def create_user(self, email: str, name: str) -> User:
        existing = await self._user_repo.get_by_email(email)
        if existing is not None:
            raise ConflictError(f"User with email {email} already exists")

        user = User(
            id=generate_id(),
            email=email,
            name=name,
            role=UserRole.MEMBER,
            created_at=utcnow(),
        )
        await self._user_repo.save(user)
        return user

    async def promote_to_admin(self, user_id: str) -> User:
        user = await self.get_user(user_id)
        user.promote_to_admin()  # Domain logic on the model
        await self._user_repo.save(user)
        return user

    async def deactivate_user(self, user_id: str) -> User:
        user = await self.get_user(user_id)
        user.deactivate()
        await self._user_repo.save(user)
        return user
```

## Dependency Injection (Without Framework)

Wire dependencies manually using constructor injection. No DI container needed for most Python services.

```python
# api/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db import get_session
from infrastructure.repositories.user_repo import SqlAlchemyUserRepository
from domain.services.user_service import UserService

async def get_user_repo(
    session: AsyncSession = Depends(get_session),
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)

async def get_user_service(
    user_repo: SqlAlchemyUserRepository = Depends(get_user_repo),
) -> UserService:
    return UserService(user_repo)
```

```python
# api/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from domain.services.user_service import UserService
from domain.errors import NotFoundError, ConflictError
from api.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    try:
        return await service.get_user(user_id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
```

## Error Hierarchy

Define domain errors that are framework-agnostic. Map them to HTTP errors in the API layer.

```python
# domain/errors.py
class DomainError(Exception):
    """Base class for all domain errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(DomainError):
    def __init__(self, resource: str, resource_id: str | int):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} {resource_id} not found")

class ConflictError(DomainError):
    pass

class ValidationError(DomainError):
    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error on {field}: {message}")

class InactiveUserError(DomainError):
    def __init__(self, user_id: str):
        super().__init__(f"User {user_id} is inactive")

class OrderNotEditableError(DomainError):
    def __init__(self, order_id: str, status: str):
        super().__init__(f"Order {order_id} cannot be edited in status '{status}'")

class EmptyOrderError(DomainError):
    def __init__(self, order_id: str):
        super().__init__(f"Order {order_id} cannot be submitted with no items")
```

### Mapping Domain Errors to HTTP

```python
# api/error_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from domain.errors import DomainError, NotFoundError, ConflictError, ValidationError

def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"error": exc.message})

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"error": exc.message})

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": exc.message, "field": exc.field},
        )

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        return JSONResponse(status_code=400, content={"error": exc.message})
```

## Testing Strategy

### Unit Test Services with Mock Repos

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock
from domain.services.user_service import UserService
from domain.models.user import User, UserRole
from domain.errors import NotFoundError, ConflictError

@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def service(mock_repo):
    return UserService(user_repo=mock_repo)

@pytest.mark.asyncio
async def test_create_user_success(service, mock_repo):
    mock_repo.get_by_email.return_value = None  # No existing user

    user = await service.create_user(email="new@test.com", name="New User")

    assert user.email == "new@test.com"
    assert user.role == UserRole.MEMBER
    mock_repo.save.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_duplicate_email(service, mock_repo):
    mock_repo.get_by_email.return_value = User(
        id="existing", email="dupe@test.com", name="Existing",
        role=UserRole.MEMBER, created_at=utcnow(),
    )

    with pytest.raises(ConflictError, match="already exists"):
        await service.create_user(email="dupe@test.com", name="New")

@pytest.mark.asyncio
async def test_promote_inactive_user_fails(service, mock_repo):
    inactive_user = User(
        id="u1", email="x@test.com", name="X",
        role=UserRole.MEMBER, created_at=utcnow(), is_active=False,
    )
    mock_repo.get_by_id.return_value = inactive_user

    with pytest.raises(InactiveUserError):
        await service.promote_to_admin("u1")
```

### Integration Test Repos with Test DB

Use an in-memory SQLite database. Create tables in a fixture, inject the session into the repo, and test round-trip persistence.

```python
# tests/integration/test_user_repo.py
@pytest.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_sessionmaker(engine)() as session:
        yield session

@pytest.mark.asyncio
async def test_save_and_retrieve(session):
    repo = SqlAlchemyUserRepository(session)
    user = User(id="u1", email="test@test.com", name="Test",
                role=UserRole.MEMBER, created_at=utcnow())
    await repo.save(user)
    await session.commit()

    retrieved = await repo.get_by_id("u1")
    assert retrieved is not None
    assert retrieved.email == "test@test.com"
```

## Anti-patterns

### Business Logic in Route Handlers

```python
# BAD: Business logic mixed with HTTP handling
@router.post("/orders")
async def create_order(body: CreateOrderRequest, db = Depends(get_db)):
    user = await db.get(User, body.user_id)
    if not user.is_active:
        raise HTTPException(400, "Inactive user")  # Business rule in handler
    if len(body.items) == 0:
        raise HTTPException(400, "Empty order")    # Business rule in handler
    order = Order(...)
    db.add(order)
    # This is untestable without spinning up FastAPI

# GOOD: Handler delegates to service
@router.post("/orders")
async def create_order(body: CreateOrderRequest, service = Depends(get_order_service)):
    return await service.create_order(body.user_id, body.items)
```

### ORM Models as Domain Models

Using SQLAlchemy models directly in business logic couples your domain to the database schema. Change a column name and your business logic breaks.

### Importing Framework in Service Layer

```python
# BAD: Service imports FastAPI
from fastapi import HTTPException

class UserService:
    async def get_user(self, id):
        user = await self.repo.get(id)
        if not user:
            raise HTTPException(404)  # Framework leak!

# GOOD: Service raises domain error
from domain.errors import NotFoundError

class UserService:
    async def get_user(self, id):
        user = await self.repo.get(id)
        if not user:
            raise NotFoundError("User", id)  # Framework-agnostic
```

### No Error Hierarchy

Using bare `Exception` or `ValueError` everywhere makes it impossible to map domain errors to HTTP status codes consistently. Define a clear hierarchy rooted in `DomainError`.

### Untestable Code

If you cannot test a service without starting a web server or connecting to a database, your architecture is wrong. Services should accept repository interfaces, and tests should inject mocks.
