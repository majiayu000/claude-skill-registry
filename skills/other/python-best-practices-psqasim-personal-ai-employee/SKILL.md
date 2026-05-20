---
name: python-best-practices
description: Expert guidance on Python 3.12+ best practices for clean, maintainable code. Use when writing or reviewing Python code requiring: (1) Type hints and generic types, (2) Async/await patterns, (3) Pydantic v2 models, (4) Clean code principles (DRY, SOLID), (5) Dependency injection, (6) Error handling patterns, (7) Code organization. Invoke when user asks about Python patterns, code quality, or when writing production Python code.
---

# Python Best Practices

Expert guidance for writing clean, maintainable Python 3.12+ code.

## Type Hints

Always use type hints. Python 3.12+ supports clean generic syntax:

```python
# Collections (no typing import needed)
def process(items: list[str]) -> dict[str, int]: ...

# Optional values
def find(id: int) -> User | None: ...

# Callables
def retry(fn: Callable[[int], str], attempts: int) -> str: ...

# TypeVar for generics
type T = TypeVar('T')
def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

**Avoid `Any`** - use `object` for truly unknown types, or create proper protocols.

## Async Patterns

See [references/async-patterns.md](references/async-patterns.md) for:
- async/await fundamentals
- Concurrent execution with gather/TaskGroup
- Async context managers
- Common pitfalls

## Pydantic Models

See [references/pydantic-patterns.md](references/pydantic-patterns.md) for:
- Model definition patterns
- Validators and field constraints
- Serialization/deserialization
- Settings and configuration

## Clean Code Principles

### DRY (Don't Repeat Yourself)

Extract repeated logic into functions. If code appears 3+ times, refactor:

```python
# Bad: repeated validation
if not title or len(title) > 200:
    raise ValueError("Invalid title")
# ... same check elsewhere

# Good: single function
def validate_title(title: str) -> str:
    if not title or len(title) > 200:
        raise ValueError("Title must be 1-200 characters")
    return title
```

### SOLID Principles

See [references/solid-patterns.md](references/solid-patterns.md) for:
- Single Responsibility
- Open/Closed
- Liskov Substitution
- Interface Segregation
- Dependency Inversion

## Dependency Injection

Prefer constructor injection for testability:

```python
# Protocol for interface
class StorageBackend(Protocol):
    def save(self, key: str, data: dict) -> None: ...
    def get(self, key: str) -> dict | None: ...

# Class accepts dependency via constructor
class TaskManager:
    def __init__(self, storage: StorageBackend) -> None:
        self._storage = storage

    def create_task(self, title: str) -> Task:
        task = Task(title=title)
        self._storage.save(str(task.id), task.model_dump())
        return task
```

Benefits:
- Easy to test with mocks
- Explicit dependencies
- Swappable implementations

## Error Handling

See [references/error-handling.md](references/error-handling.md) for:
- Exception hierarchy design
- When to catch vs propagate
- Result pattern alternative
- Logging best practices

### Quick Reference

```python
# Custom exception with context
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")

# Specific catches, log errors
try:
    result = process(data)
except ValidationError as e:
    logger.warning("validation_failed", error=str(e))
    return ErrorResponse(message=str(e))
except Exception as e:
    logger.exception("unexpected_error")
    raise
```

## Code Organization

### Module Structure

```
src/
├── __init__.py          # Package version
├── models/              # Data classes, Pydantic models
├── services/            # Business logic
├── repositories/        # Data access
└── exceptions.py        # Custom exceptions
```

### Function Guidelines

- Max 25 lines (50 absolute max)
- Max 3-4 parameters
- Single responsibility
- Descriptive names (no abbreviations)
- Docstrings for public functions

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions/variables | snake_case | `get_user`, `task_id` |
| Classes | PascalCase | `TaskManager`, `User` |
| Constants | UPPER_SNAKE | `MAX_RETRIES`, `API_KEY` |
| Private | _prefix | `_validate`, `_cache` |
