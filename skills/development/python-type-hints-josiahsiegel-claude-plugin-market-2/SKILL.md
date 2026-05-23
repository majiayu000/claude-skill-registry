---
name: python-type-hints
description: Complete Python type hints system. PROACTIVELY activate for: (1) Built-in generics (list[str], dict[str, int]), (2) Union types (str | None), (3) Type parameter syntax 3.12+, (4) Protocol for structural typing, (5) TypedDict for dict schemas, (6) Literal and Final types, (7) TypeGuard and TypeIs, (8) ParamSpec for decorators, (9) Mypy/Pyright configuration. Provides: Type syntax, Protocol patterns, TypedDict, mypy config. Ensures static type safety with gradual typing strategy.
---

## Quick Reference

| Type | Syntax (3.9+) | Example |
|------|---------------|---------|
| List | `list[str]` | `names: list[str] = []` |
| Dict | `dict[str, int]` | `ages: dict[str, int] = {}` |
| Optional | `str \| None` | `name: str \| None = None` |
| Union | `int \| str` | `value: int \| str` |
| Callable | `Callable[[int], str]` | `func: Callable[[int], str]` |

| Feature | Version | Syntax |
|---------|---------|--------|
| Type params | 3.12+ | `def first[T](items: list[T]) -> T:` |
| type alias | 3.12+ | `type Point = tuple[float, float]` |
| Self | 3.11+ | `def copy(self) -> Self:` |
| TypeIs | 3.13+ | `def is_str(x) -> TypeIs[str]:` |

| Construct | Use Case |
|-----------|----------|
| `Protocol` | Structural subtyping (duck typing) |
| `TypedDict` | Dict with specific keys |
| `Literal["a", "b"]` | Specific values only |
| `Final[str]` | Cannot be reassigned |

## When to Use This Skill

Use for **static type checking**:
- Adding type hints to functions and classes
- Creating typed dictionaries with TypedDict
- Defining protocols for duck typing
- Configuring mypy or pyright
- Writing generic functions and classes

**Related skills:**
- For Python fundamentals: see `python-fundamentals-313`
- For testing: see `python-testing`
- For FastAPI schemas: see `python-fastapi`

---

# Python Type Hints Complete Guide

## Overview

Type hints enable static type checking, better IDE support, and self-documenting code. Python's typing system is gradual - you can add types incrementally.

## Modern Type Hints (Python 3.9+)

### Built-in Generic Types

```python
# Python 3.9+ - Use built-in types directly
# No need for typing.List, typing.Dict, etc.

def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Collections
names: list[str] = ["Alice", "Bob"]
ages: dict[str, int] = {"Alice": 30, "Bob": 25}
coordinates: tuple[float, float] = (1.0, 2.0)
unique_ids: set[int] = {1, 2, 3}
frozen_data: frozenset[str] = frozenset(["a", "b"])

# Nested generics
matrix: list[list[int]] = [[1, 2], [3, 4]]
config: dict[str, list[str]] = {"servers": ["a", "b"]}
```

### Union Types (Python 3.10+)

```python
# Old way (still works)
from typing import Union, Optional

def old_style(value: Union[int, str]) -> Optional[str]:
    return str(value) if value else None

# New way (Python 3.10+)
def new_style(value: int | str) -> str | None:
    return str(value) if value else None

# Optional is just Union with None
# Optional[str] == str | None
```

### Type Aliases

```python
# Simple type alias
UserId = int
Username = str

def get_user(user_id: UserId) -> Username:
    return "user_" + str(user_id)

# Complex type alias
from typing import TypeAlias

JsonValue: TypeAlias = str | int | float | bool | None | list["JsonValue"] | dict[str, "JsonValue"]

# Python 3.12+ type statement
type Point = tuple[float, float]
type Vector[T] = list[T]
type JsonDict = dict[str, "JsonValue"]
```

### Type Parameters (Python 3.12+)

```python
# Old way with TypeVar
from typing import TypeVar

T = TypeVar("T")

def first_old(items: list[T]) -> T:
    return items[0]

# New way (Python 3.12+)
def first[T](items: list[T]) -> T:
    return items[0]

# Generic classes
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Multiple type parameters
def merge[K, V](d1: dict[K, V], d2: dict[K, V]) -> dict[K, V]:
    return {**d1, **d2}

# Bounded type parameters
from typing import SupportsLessThan

def minimum[T: SupportsLessThan](a: T, b: T) -> T:
    return a if a < b else b

# Default type parameters (Python 3.13+)
class Container[T = int]:
    def __init__(self, value: T) -> None:
        self.value = value
```

## Function Signatures

### Basic Functions

```python
from typing import Callable, Iterable, Iterator

# Simple function
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Multiple parameters
def create_user(name: str, age: int, email: str | None = None) -> dict:
    return {"name": name, "age": age, "email": email}

# *args and **kwargs
def log(*args: str, **kwargs: int) -> None:
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}={value}")

# Callable type
def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# Higher-order functions
def make_multiplier(n: int) -> Callable[[int], int]:
    def multiplier(x: int) -> int:
        return x * n
    return multiplier
```

### Overloads

```python
from typing import overload, Literal

@overload
def process(data: str) -> str: ...
@overload
def process(data: bytes) -> bytes: ...
@overload
def process(data: int) -> int: ...

def process(data: str | bytes | int) -> str | bytes | int:
    if isinstance(data, str):
        return data.upper()
    elif isinstance(data, bytes):
        return data.upper()
    else:
        return data * 2

# Overload with Literal
@overload
def fetch(url: str, format: Literal["json"]) -> dict: ...
@overload
def fetch(url: str, format: Literal["text"]) -> str: ...
@overload
def fetch(url: str, format: Literal["bytes"]) -> bytes: ...

def fetch(url: str, format: str) -> dict | str | bytes:
    # Implementation
    ...
```

### ParamSpec for Decorators

```python
from typing import ParamSpec, TypeVar, Callable
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

# Python 3.12+ syntax
def log_calls_new[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## Classes and Protocols

### Class Typing

```python
from typing import ClassVar, Self

class User:
    # Class variable
    count: ClassVar[int] = 0

    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        User.count += 1

    # Self type for method chaining
    def with_name(self, name: str) -> Self:
        self.name = name
        return self

    def with_age(self, age: int) -> Self:
        self.age = age
        return self

# Usage
user = User("Alice", 30).with_name("Bob").with_age(25)
```

### Protocols (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable

# Define a protocol (interface)
class Drawable(Protocol):
    def draw(self) -> None: ...

class Resizable(Protocol):
    def resize(self, width: int, height: int) -> None: ...

# Combining protocols
class DrawableAndResizable(Drawable, Resizable, Protocol):
    pass

# Implementation (no explicit inheritance needed!)
class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Rectangle:
    def draw(self) -> None:
        print("Drawing rectangle")

    def resize(self, width: int, height: int) -> None:
        print(f"Resizing to {width}x{height}")

# Works because Circle has draw() method
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK - Circle satisfies Drawable protocol

# Runtime checkable protocol
@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None: ...

# Can use isinstance
if isinstance(file, Closeable):
    file.close()
```

### TypedDict

```python
from typing import TypedDict, Required, NotRequired

# Basic TypedDict
class Movie(TypedDict):
    title: str
    year: int
    director: str

movie: Movie = {"title": "Inception", "year": 2010, "director": "Nolan"}

# With optional keys
class UserProfile(TypedDict, total=False):
    name: str  # Optional
    email: str  # Optional
    age: int   # Optional

# Mixed required and optional (Python 3.11+)
class Article(TypedDict):
    title: Required[str]
    content: Required[str]
    author: NotRequired[str]
    tags: NotRequired[list[str]]

# Inheritance
class DetailedMovie(Movie):
    rating: float
    genres: list[str]
```

### Abstract Base Classes

```python
from abc import ABC, abstractmethod

class Repository[T](ABC):
    @abstractmethod
    def get(self, id: int) -> T | None:
        ...

    @abstractmethod
    def save(self, entity: T) -> T:
        ...

    @abstractmethod
    def delete(self, id: int) -> bool:
        ...

class UserRepository(Repository["User"]):
    def get(self, id: int) -> "User | None":
        return self._db.get(id)

    def save(self, entity: "User") -> "User":
        return self._db.save(entity)

    def delete(self, id: int) -> bool:
        return self._db.delete(id)
```

## Advanced Types

### Literal Types

```python
from typing import Literal

# Restrict to specific values
Mode = Literal["r", "w", "a", "rb", "wb"]

def open_file(path: str, mode: Mode) -> None:
    ...

open_file("test.txt", "r")   # OK
open_file("test.txt", "x")   # Type error!

# Combining literals
HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
StatusCode = Literal[200, 201, 400, 401, 403, 404, 500]
```

### Final and Const

```python
from typing import Final

# Constant that shouldn't be reassigned
MAX_SIZE: Final = 100
API_URL: Final[str] = "https://api.example.com"

# Final class methods
class Base:
    from typing import final

    @final
    def critical_method(self) -> None:
        """Cannot be overridden in subclasses."""
        ...

# Final classes
from typing import final

@final
class Singleton:
    """Cannot be subclassed."""
    _instance: "Singleton | None" = None
```

### Type Guards

```python
from typing import TypeGuard, TypeIs

# TypeGuard (narrows type in if block)
def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> None:
    if is_string_list(items):
        # items is now list[str]
        for item in items:
            print(item.upper())

# TypeIs (Python 3.13+ - stricter than TypeGuard)
def is_int(val: int | str) -> TypeIs[int]:
    return isinstance(val, int)

def handle(value: int | str) -> None:
    if is_int(value):
        # value is int
        print(value + 1)
    else:
        # value is str (properly narrowed)
        print(value.upper())
```

### Annotated

```python
from typing import Annotated
from dataclasses import dataclass

# Metadata for validation/documentation
UserId = Annotated[int, "Unique user identifier"]
Email = Annotated[str, "Valid email address"]
Age = Annotated[int, "Must be >= 0"]

@dataclass
class User:
    id: UserId
    email: Email
    age: Age

# With Pydantic
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    id: Annotated[int, Field(gt=0)]
    email: Annotated[str, Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")]
    age: Annotated[int, Field(ge=0, le=150)]
```

## Type Checking Tools

### Mypy Configuration

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_configs = true

# Per-module overrides
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

### Pyright Configuration

```json
// pyrightconfig.json
{
  "include": ["src"],
  "exclude": ["**/node_modules", "**/__pycache__"],
  "typeCheckingMode": "strict",
  "pythonVersion": "3.12",
  "reportMissingImports": true,
  "reportMissingTypeStubs": false,
  "reportUnusedImport": true,
  "reportUnusedVariable": true
}
```

### Running Type Checkers

```bash
# Mypy
mypy src/ --strict
mypy src/ --ignore-missing-imports

# Pyright (faster, VS Code default)
pyright src/

# With uv
uv run mypy src/
```

## Best Practices

### 1. Use Native Generics (3.9+)

```python
# Preferred (Python 3.9+)
items: list[str] = []
mapping: dict[str, int] = {}

# Avoid (old style)
from typing import List, Dict
items: List[str] = []  # Deprecated
```

### 2. Prefer Protocols Over ABCs

```python
# Preferred - structural typing
from typing import Protocol

class Serializable(Protocol):
    def to_json(self) -> str: ...

# Less flexible - nominal typing
from abc import ABC, abstractmethod

class SerializableABC(ABC):
    @abstractmethod
    def to_json(self) -> str: ...
```

### 3. Use Abstract Collection Types

```python
from collections.abc import Iterable, Sequence, Mapping, MutableMapping

# Prefer abstract types for function parameters
def process_items(items: Iterable[str]) -> list[str]:
    return [item.upper() for item in items]

def lookup(data: Mapping[str, int], key: str) -> int | None:
    return data.get(key)

# Works with any iterable/mapping
process_items(["a", "b"])      # list
process_items({"a", "b"})      # set
process_items(("a", "b"))      # tuple
process_items(x for x in "ab") # generator
```

### 4. Gradual Typing Strategy

```python
# Start with public API
def public_function(data: dict[str, Any]) -> list[str]:
    return _internal_helper(data)

# Type internal helpers later
def _internal_helper(data):  # Untyped initially
    ...

# Aim for 80%+ coverage on new code
# Use # type: ignore sparingly
```

### 5. Document Complex Types

```python
from typing import TypeAlias

# Use type aliases for complex types
JsonPrimitive: TypeAlias = str | int | float | bool | None
JsonArray: TypeAlias = list["JsonValue"]
JsonObject: TypeAlias = dict[str, "JsonValue"]
JsonValue: TypeAlias = JsonPrimitive | JsonArray | JsonObject

def parse_json(text: str) -> JsonValue:
    """Parse JSON string into typed Python value."""
    import json
    return json.loads(text)
```

## Additional References

For advanced typing patterns beyond this guide, see:

- **[Advanced Typing Patterns](references/advanced-typing-patterns.md)** - Generic repository pattern, discriminated unions, builder pattern with Self, ParamSpec decorators, conditional types with overloads, typed decorator factories, Protocols with class methods, typed context variables, recursive types, typed event systems
