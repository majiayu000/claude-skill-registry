---
name: type-hints
description: Python type hint conventions for this codebase. Apply when writing or reviewing Python code that needs type annotations on functions, classes, or variables.
user-invocable: false
---

# Type Hints

**Type annotations are REQUIRED on all functions and classes.**

## Quick Reference

| Element | Convention | Example |
|---------|------------|---------|
| Optional values | `X \| None` | `user: User \| None` |
| Input collections | `Sequence`, `Mapping`, `Iterable` | `items: Sequence[str]` |
| Return collections | `list`, `dict` | `-> list[str]` |
| Generic containers | Lowercase builtins | `list[str]`, `dict[str, int]` |
| Type variables | Single uppercase letters | `T`, `K`, `V` |
| Type aliases | `TypeAlias` annotation | `UserId: TypeAlias = int` |
| Constrained strings | `Literal` | `Status = Literal["active", "pending"]` |
| Dict structures | `TypedDict` | For API responses and configs |
| Fluent methods | `Self` | For builder patterns |
| Interfaces | `Protocol` | For duck typing with type safety |

## Modern Syntax (Python 3.10+)

### Union Types

```python
# CORRECT - modern union syntax
def get_user(user_id: int) -> User | None:
    ...

def process(value: str | int | float) -> str:
    ...

# INCORRECT - deprecated Optional
from typing import Optional, Union
def get_user(user_id: int) -> Optional[User]:  # Don't use
    ...
def process(value: Union[str, int, float]) -> str:  # Don't use
    ...
```

### Generic Containers

```python
# CORRECT - lowercase builtins
def process(items: list[str]) -> dict[str, int]:
    ...

# INCORRECT - typing module generics
from typing import List, Dict
def process(items: List[str]) -> Dict[str, int]:  # Don't use
    ...
```

### Abstract Container Types

Use `collections.abc` for parameters when you only need iteration or read access:

```python
from collections.abc import Sequence, Mapping, Callable, Iterator, Iterable

# CORRECT - accept abstract, return concrete
def transform(items: Sequence[str]) -> list[str]:
    return [item.upper() for item in items]

def lookup(data: Mapping[str, int], key: str) -> int | None:
    return data.get(key)

def apply(fn: Callable[[int], str], values: Iterable[int]) -> Iterator[str]:
    return (fn(v) for v in values)

# INCORRECT - overly restrictive parameter types
def transform(items: list[str]) -> list[str]:  # Rejects tuples, other sequences
    ...
```

## Generic Types

```python
from typing import TypeVar
from collections.abc import Sequence

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def first(items: Sequence[T]) -> T | None:
    """Return the first item or None if empty."""
    return items[0] if items else None

def merge_dicts(a: dict[K, V], b: dict[K, V]) -> dict[K, V]:
    """Merge two dictionaries, with b taking precedence."""
    return {**a, **b}
```

## Self Type (Python 3.11+)

Use `Self` for methods that return the instance (fluent/builder patterns):

```python
from typing import Self

class Builder:
    """Fluent builder pattern with proper typing."""

    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def with_value(self, value: int) -> Self:
        self.value = value
        return self
```

## Protocol for Structural Subtyping

Use `Protocol` to define interfaces based on behavior (duck typing with type safety):

```python
from typing import Protocol

class Readable(Protocol):
    """Any object that can be read."""
    def read(self) -> str: ...

class Closeable(Protocol):
    """Any object that can be closed."""
    def close(self) -> None: ...

# Intersection of protocols
def process_stream(stream: Readable & Closeable) -> str:
    """Process any readable, closeable stream."""
    try:
        return stream.read()
    finally:
        stream.close()
```

## Type Aliases

```python
from typing import TypeAlias

# Simple aliases
UserId: TypeAlias = int
Embedding: TypeAlias = list[float]
BatchEmbeddings: TypeAlias = list[Embedding]

# Recursive aliases (use forward references)
JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

def encode(texts: list[str]) -> BatchEmbeddings:
    ...
```

## TypedDict for JSON-like Structures

```python
from typing import TypedDict, Required, NotRequired, Any

class UserResponse(TypedDict):
    id: Required[int]
    name: Required[str]
    email: NotRequired[str]

def parse_user(data: dict[str, Any]) -> UserResponse:
    ...
```

## Literal Types for Constrained Strings

```python
from typing import Literal

Status = Literal["pending", "active", "completed", "failed"]
LogLevel = Literal["debug", "info", "warning", "error"]

def update_status(task_id: int, status: Status) -> None:
    ...
```

## Validation Commands

| Check | Command |
|-------|---------|
| Type checking | `uv run ty check <path>` |
