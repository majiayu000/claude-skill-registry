---
name: python-fastapi-ddd-skill
description: Guides FastAPI backend design using Domain-Driven Design (DDD) and Onion Architecture in Python. Use when structuring a FastAPI app (routes/handlers, Pydantic schemas, Depends-based DI), modeling domain Entities/Value Objects, defining repository interfaces, implementing SQLAlchemy infrastructure adapters, or writing use cases, based on the dddpy reference.
license: Apache-2.0
metadata:
  author: Takahiro Ikeuchi
  version: "1.0.0"
---

# FastAPI + Python DDD & Onion Architecture Design Guide

Guides FastAPI backend design using DDD principles and Onion Architecture, based on the [dddpy](https://github.com/iktakahiro/dddpy) reference implementation (FastAPI + SQLAlchemy + Python 3.13+).

## Architecture Overview

Four concentric layers with dependencies pointing inward:

```
Presentation  →  UseCase  →  Infrastructure  →  Domain (innermost)
```

**Key rule**: Inner layers never depend on outer layers. The Domain layer has zero external dependencies.

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **Domain** | Core business logic, no framework deps | Entities, Value Objects, Repository interfaces, Exceptions |
| **Infrastructure** | External integrations | DB repos, DTOs, DI config, SQLAlchemy models |
| **UseCase** | Application workflows | One class per use case with `execute()` |
| **Presentation** | HTTP API surface | FastAPI routes, Pydantic schemas, error messages |

**For detailed architecture guide**: See [ARCHITECTURE.md](references/ARCHITECTURE.md)

## Directory Structure

```
project/
├── main.py
├── app/
│   ├── domain/
│   │   └── {aggregate}/
│   │       ├── entities/
│   │       ├── value_objects/
│   │       ├── repositories/
│   │       └── exceptions/
│   ├── infrastructure/
│   │   ├── di/
│   │   │   └── injection.py
│   │   └── sqlite/
│   │       └── {aggregate}/
│   │           ├── {aggregate}_dto.py
│   │           └── {aggregate}_repository.py
│   ├── usecase/
│   │   └── {aggregate}/
│   │       └── {action}_{aggregate}_usecase.py
│   └── presentation/
│       └── api/
│           └── {aggregate}/
│               ├── handlers/
│               ├── schemas/
│               └── error_messages/
└── tests/
```

## Quick Reference

### 1. Entity

Entities have unique identifiers, mutable state, and encapsulated business logic. Equality is based on identity, not attribute values.

```python
class Todo:
    def __init__(self, id: TodoId, title: TodoTitle, status: TodoStatus = TodoStatus.NOT_STARTED):
        self._id = id
        self._title = title
        self._status = status

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Todo):
            return self.id == obj.id
        return False

    def start(self) -> None:
        self._status = TodoStatus.IN_PROGRESS

    @staticmethod
    def create(title: TodoTitle) -> "Todo":
        return Todo(TodoId.generate(), title)
```

**Detailed guide**: See [ENTITIES.md](references/ENTITIES.md)

### 2. Value Object

Immutable objects defined by their values, not identity. Use `@dataclass(frozen=True)` with validation in `__post_init__`.

```python
@dataclass(frozen=True)
class TodoTitle:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Title is required")
        if len(self.value) > 100:
            raise ValueError("Title must be 100 characters or less")
```

**Detailed guide**: See [VALUE_OBJECTS.md](references/VALUE_OBJECTS.md)

### 3. Repository Interface

Define abstract interfaces in the Domain layer. Infrastructure implements them.

```python
class TodoRepository(ABC):
    @abstractmethod
    def save(self, todo: Todo) -> None: ...

    @abstractmethod
    def find_by_id(self, todo_id: TodoId) -> Optional[Todo]: ...

    @abstractmethod
    def find_all(self) -> List[Todo]: ...

    @abstractmethod
    def delete(self, todo_id: TodoId) -> None: ...
```

**Detailed guide**: See [REPOSITORIES.md](references/REPOSITORIES.md)

### 4. UseCase

One class per use case. Abstract interface + concrete implementation + factory function.

```python
class CreateTodoUseCase(ABC):
    @abstractmethod
    def execute(self, title: TodoTitle) -> Todo: ...

class CreateTodoUseCaseImpl(CreateTodoUseCase):
    def __init__(self, todo_repository: TodoRepository):
        self.todo_repository = todo_repository

    def execute(self, title: TodoTitle) -> Todo:
        todo = Todo.create(title=title)
        self.todo_repository.save(todo)
        return todo

def new_create_todo_usecase(repo: TodoRepository) -> CreateTodoUseCase:
    return CreateTodoUseCaseImpl(repo)
```

**Detailed guide**: See [USECASES.md](references/USECASES.md)

## Best Practices

1. **Keep Domain Layer Pure**: No framework imports (no FastAPI, no SQLAlchemy) in domain code
2. **Use DTOs at Layer Boundaries**: Convert between domain entities and infrastructure models via `to_entity()` / `from_entity()` methods
3. **Dependency Injection**: Use FastAPI's `Depends()` to wire session → repository → usecase → handler
4. **One UseCase = One Responsibility**: Each UseCase has exactly one public `execute` method
5. **Validate in Value Objects**: Business rules live in `__post_init__` of frozen dataclasses
6. **Domain Exceptions**: Create specific exception classes for business rule violations (e.g., `TodoNotFoundError`, `TodoAlreadyCompletedError`)
7. **Factory Functions**: Expose `new_*` factory functions for creating implementations, keeping concrete classes as implementation details
