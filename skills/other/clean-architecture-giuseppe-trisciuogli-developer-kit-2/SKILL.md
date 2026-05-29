---
name: clean-architecture
description: Provides implementation patterns for Clean Architecture, Hexagonal Architecture (Ports & Adapters), and Domain-Driven Design in Python applications with FastAPI or Flask. Use when designing maintainable backends with separation of concerns, implementing repository patterns, creating entities/value objects/aggregates, or structuring domain logic independent of frameworks for testability.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Clean Architecture, DDD & Hexagonal Architecture for Python

## Overview

This skill provides comprehensive guidance for implementing Clean Architecture, Hexagonal Architecture (Ports & Adapters), and Domain-Driven Design patterns in Python applications. It focuses on creating maintainable, testable, and framework-independent business logic through proper separation of concerns.

### Core Concepts

**Layered Architecture (Clean Architecture)** - Dependencies flow inward, inner layers know nothing about outer layers:

```
+-------------------------------------+
|  Infrastructure (Frameworks, DB)   |  <- Outer layer
+-------------------------------------+
|  Adapters (Controllers, Repos)     |
+-------------------------------------+
|  Use Cases (Application Logic)     |
+-------------------------------------+
|  Domain (Entities, Value Objects)  |  <- Inner layer
+-------------------------------------+
```

**Layers:**
- **Domain**: Entities, value objects, domain events, repository interfaces
- **Use Cases**: Application business rules, orchestrate domain objects
- **Adapters**: Interface implementations (controllers, repositories, gateways)
- **Infrastructure**: Framework configuration, database connections, external clients

**Hexagonal Architecture (Ports & Adapters)**
- **Ports**: Abstract interfaces defining what the application needs
- **Adapters**: Concrete implementations of ports
- **Domain Core**: Business logic with no external dependencies

**Domain-Driven Design Tactical Patterns**
- **Entities**: Objects with identity and lifecycle
- **Value Objects**: Immutable objects defined by attributes
- **Aggregates**: Consistency boundaries with aggregate roots
- **Repositories**: Persistence abstraction for aggregates
- **Domain Events**: Capture significant occurrences in the domain

## When to Use

- Designing new Python backend systems with separation of concerns
- Refactoring tightly coupled code into layered architectures
- Implementing domain-driven design with bounded contexts
- Creating testable business logic independent of frameworks
- Building applications with FastAPI or Flask using clean patterns
- Setting up repository patterns with SQLAlchemy or async databases
- Implementing use case patterns with proper dependency injection

## Instructions

### 1. Define the Project Structure

Create the layered directory structure following the dependency rule:

```
myapp/
+-- domain/                    # Inner layer - no external deps
|   +-- entities/             # Business entities
|   +-- value_objects/        # Immutable value objects
|   +-- events/               # Domain events
|   +-- repositories/         # Abstract repository interfaces (ports)
+-- use_cases/                # Application layer
+-- adapters/                 # Interface adapters
|   +-- repositories/         # Repository implementations
|   +-- controllers/          # API controllers
+-- infrastructure/           # Framework & external concerns
|   +-- database.py          # Database configuration
|   +-- container.py         # Dependency injection container
|   +-- config.py            # Application settings
+-- main.py                  # Application entry point
```

### 2. Implement the Domain Layer

Start from the innermost layer with no external dependencies:

1. Create Value Objects using frozen dataclasses with validation in `__post_init__`
2. Define Entities with identity, behavior, and factory methods (e.g., `create()`)
3. Define Repository Interfaces (Ports) as abstract base classes with abstract methods
4. Keep all domain logic in entities - avoid anemic models

### 3. Implement the Use Cases Layer

Create application-specific business rules:

1. Define Request/Response dataclasses for input/output
2. Create Use Case classes that receive repository interfaces via constructor injection
3. Implement the `execute()` method that orchestrates domain objects
4. Handle validation and business errors, returning appropriate responses

### 4. Implement the Adapter Layer

Create concrete implementations of domain interfaces:

1. Implement Repository classes that extend domain interfaces
2. Use SQLAlchemy async sessions or other ORM tools
3. Map between domain entities and database models
4. Create Controllers (FastAPI routers) that invoke use cases

### 5. Implement the Infrastructure Layer

Configure frameworks and external dependencies:

1. Set up database connections and session management
2. Configure the dependency injection container
3. Wire all components together
4. Define application settings and configuration

### 6. Create the Application Entry Point

Build the FastAPI or Flask application:

1. Initialize the DI container and wire modules
2. Configure application lifespan (startup/shutdown)
3. Register routers and middleware
4. Export the application factory function

### 7. Write Tests

Test each layer in isolation:

1. Unit test use cases with mocked repositories
2. Unit test domain entities and value objects
3. Integration test adapters with test databases
4. End-to-end test the full application stack

## Examples

### Example 1: Domain Layer - Value Object & Entity

```python
# domain/value_objects/email.py
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.value):
            raise ValueError(f"Invalid email: {self.value}")
    def __str__(self) -> str:
        return self.value


# domain/entities/user.py
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from domain.value_objects.email import Email

@dataclass
class User:
    email: Email
    name: str
    id: UUID = field(default_factory=uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    def deactivate(self) -> None:
        self.is_active = False

    def can_login(self) -> bool:
        return self.is_active

    @classmethod
    def create(cls, email: Email, name: str) -> "User":
        return cls(email=email, name=name)
```

### Example 2: Repository Port (Interface)

```python
# domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.entities.user import User
from domain.value_objects.email import Email

class IUserRepository(ABC):
    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]: ...
    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]: ...
    @abstractmethod
    async def save(self, user: User) -> User: ...
    @abstractmethod
    async def delete(self, user_id: UUID) -> bool: ...
```

### Example 3: Use Case Layer

```python
# use_cases/create_user.py
from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import IUserRepository

@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user_id: Optional[UUID]
    success: bool
    error_message: Optional[str] = None

class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        try:
            email = Email(request.email)
        except ValueError as e:
            return CreateUserResponse(None, False, str(e))
        if await self._user_repository.find_by_email(email):
            return CreateUserResponse(None, False, "Email already registered")
        user = User.create(email=email, name=request.name)
        saved = await self._user_repository.save(user)
        return CreateUserResponse(saved.id, True)
```

### Example 4: Adapter Layer - Repository Implementation

```python
# adapters/repositories/sqlalchemy_user_repository.py
from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from domain.entities.user import User
from domain.value_objects.email import Email
from domain.repositories.user_repository import IUserRepository

class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None

    async def find_by_email(self, email: Email) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == str(email))
        )
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        model = UserModel(
            id=user.id, email=str(user.email), name=user.name,
            is_active=user.is_active, created_at=user.created_at
        )
        self._session.add(model)
        await self._session.commit()
        return user

    def _to_entity(self, model) -> User:
        return User(
            id=model.id, email=Email(model.email), name=model.name,
            is_active=model.is_active, created_at=model.created_at
        )
```

### Example 5: Dependency Injection Container

```python
# infrastructure/container.py
from dependency_injector import containers, providers
from adapters.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from use_cases.create_user import CreateUserUseCase
from infrastructure.database import get_session

class Container(containers.DeclarativeContainer):
    db_session = providers.Factory(get_session)
    user_repository = providers.Factory(SQLAlchemyUserRepository, session=db_session)
    create_user_use_case = providers.Factory(
        CreateUserUseCase, user_repository=user_repository
    )
```

### Example 6: FastAPI Controller

```python
# adapters/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from use_cases.create_user import CreateUserUseCase, CreateUserRequest
from infrastructure.container import Container
from dependency_injector.wiring import inject, Provide

router = APIRouter(prefix="/users", tags=["users"])

class CreateUserInput(BaseModel):
    email: EmailStr
    name: str

@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
    data: CreateUserInput,
    use_case: CreateUserUseCase = Depends(Provide[Container.create_user_use_case])
):
    request = CreateUserRequest(email=data.email, name=data.name)
    response = await use_case.execute(request)
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error_message)
    return {"id": str(response.user_id)}
```

### Example 7: Application Entry Point

```python
# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from adapters.controllers import user_controller
from infrastructure.container import Container
from infrastructure.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

def create_app() -> FastAPI:
    container = Container()
    container.wire(modules=[user_controller])
    app = FastAPI(title="Clean Architecture API", lifespan=lifespan)
    app.container = container
    app.include_router(user_controller.router)
    return app

app = create_app()
```

### Example 8: Unit Testing Use Cases

```python
# tests/unit/test_create_user_use_case.py
import pytest
from unittest.mock import AsyncMock
from use_cases.create_user import CreateUserUseCase, CreateUserRequest
from domain.entities.user import User
from domain.value_objects.email import Email

@pytest.fixture
def mock_repository():
    return AsyncMock()

@pytest.fixture
def use_case(mock_repository):
    return CreateUserUseCase(user_repository=mock_repository)

@pytest.mark.asyncio
async def test_create_user_success(use_case, mock_repository):
    mock_repository.find_by_email.return_value = None
    mock_repository.save.return_value = User(
        email=Email("test@example.com"), name="Test User"
    )
    request = CreateUserRequest(email="test@example.com", name="Test User")
    response = await use_case.execute(request)
    assert response.success is True
    assert response.user_id is not None

@pytest.mark.asyncio
async def test_create_user_duplicate_email(use_case, mock_repository):
    mock_repository.find_by_email.return_value = AsyncMock()
    request = CreateUserRequest(email="test@example.com", name="Test User")
    response = await use_case.execute(request)
    assert response.success is False
    assert "already registered" in response.error_message
```

## Best Practices

1. **Dependency Rule**: Dependencies must always point inward toward the domain - never outward
2. **Immutable Value Objects**: Always use frozen dataclasses for value objects with validation in `__post_init__`
3. **Rich Domain Models**: Put business logic in entities, not in services or use cases
4. **Use Cases as Orchestrators**: Use cases coordinate workflows but domain objects make decisions
5. **Async by Default**: Use async/await for all I/O operations to support modern async frameworks
6. **Pydantic at Boundary**: Use Pydantic models only at the API boundary, never in domain layer
7. **Repository per Aggregate**: Create one repository per aggregate root, not per entity
8. **Factory Methods**: Use `@classmethod` factory methods like `create()` for entity construction with invariants
9. **Dependency Injection**: Inject dependencies through constructors for testability
10. **Structured Responses**: Return structured response objects from use cases, not raw entities

## Constraints and Warnings

### Architecture Constraints

- **Dependency Rule**: Dependencies must always point inward toward the domain - never outward
- **Framework Independence**: Domain layer must have no framework dependencies (no FastAPI, SQLAlchemy, Pydantic imports)
- **Interface Segregation**: Keep repository interfaces focused and small - avoid god interfaces
- **Repository per Aggregate**: Create one repository per aggregate root, not per entity

### Implementation Constraints

- **Immutable Value Objects**: Always use frozen dataclasses for value objects
- **Rich Domain Models**: Put business logic in entities, not in services or use cases
- **Use Cases as Orchestrators**: Use cases coordinate workflows but domain objects make decisions
- **Async by Default**: Use async/await for all I/O operations to support modern async frameworks
- **Pydantic at Boundary**: Use Pydantic models only at the API boundary, not in domain layer

### Common Pitfalls to Avoid

- **Anemic Domain Models**: Entities with only getters/setters and no behavior violate DDD principles
- **Leaky Abstractions**: ORM models leaking into domain layer creates tight coupling
- **Fat Controllers**: Business logic in controllers instead of use cases defeats the architecture
- **Missing Abstractions**: Direct database calls in use cases break the dependency rule
- **Circular Dependencies**: Be careful with imports between layers - use dependency injection to avoid
- **Over-Engineering**: Not every CRUD app needs full DDD - evaluate complexity before applying

## References

- `references/python-clean-architecture.md` - Python-specific patterns including Result type, Specification pattern, Event Bus, and manual DI
- `references/fastapi-implementation.md` - Complete FastAPI example with middleware, Docker setup, and integration tests
