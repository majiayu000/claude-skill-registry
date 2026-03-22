---
name: type-hints-guide
description: >
  Guide Python type annotations using the typing module: Protocol, TypeVar, ParamSpec,
  Generic, Literal, TypeAlias, overload, and dataclass field typing. Use when the user
  writes Python type hints, asks about typing, creates generic classes, defines protocols,
  or works with mypy/pyright. Trigger when you see untyped Python code that should be typed.
---

# Python Type Hints Guide

Write precise, expressive type annotations that catch bugs at static analysis time.
Modern Python typing (3.10+) is powerful enough to express complex relationships
without runtime overhead.

## When to Use
- User writes or refactors Python functions without type hints
- User asks about typing, generics, or protocols
- User encounters mypy or pyright errors
- User builds libraries or APIs that need clear contracts
- User works with complex data structures or callbacks

## Core Patterns

### Modern Built-in Types (Python 3.10+)

Prefer built-in generics and union syntax over `typing` imports.

```python
# Python 3.10+ -- use built-in types and | union
def process_items(
    items: list[str],
    config: dict[str, int | float],
    callback: Callable[[str], None] | None = None,
) -> tuple[int, list[str]]:
    ...

# For older Python, import from typing
from typing import List, Dict, Optional, Union, Tuple
```

### TypeVar and Generic Classes

Use TypeVar for functions/classes that work with any type while preserving
type relationships.

```python
from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class Result(Generic[T]):
    """A container that holds either a value or an error."""

    def __init__(self, value: T | None = None, error: str | None = None):
        self._value = value
        self._error = error

    def unwrap(self) -> T:
        if self._error is not None:
            raise ValueError(self._error)
        assert self._value is not None
        return self._value

    def map(self, func: Callable[[T], V]) -> "Result[V]":
        if self._error:
            return Result(error=self._error)
        return Result(value=func(self.unwrap()))

# Bounded TypeVar -- restrict to specific types
Numeric = TypeVar("Numeric", int, float)

def add(a: Numeric, b: Numeric) -> Numeric:
    return a + b

# Upper bound -- must be subclass of
from datetime import datetime
DateLike = TypeVar("DateLike", bound=datetime)
```

### Protocol (Structural Subtyping)

Use Protocol instead of ABCs when you want duck typing with static checking.
This is Python's answer to Go-style interfaces.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Renderable(Protocol):
    def render(self) -> str: ...

class SupportsComparison(Protocol):
    def __lt__(self, other: "SupportsComparison") -> bool: ...
    def __eq__(self, other: object) -> bool: ...

# Any class with a render() -> str method satisfies Renderable
# No inheritance needed
class HtmlWidget:
    def render(self) -> str:
        return "<div>widget</div>"

def display(item: Renderable) -> None:
    print(item.render())

display(HtmlWidget())  # Works -- structural match
```

### ParamSpec (Preserving Function Signatures)

Use ParamSpec for decorators that preserve the wrapped function's signature.

```python
from typing import ParamSpec, TypeVar, Callable
import functools

P = ParamSpec("P")
R = TypeVar("R")

def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs function calls while preserving type info."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# Type checker knows: greet(name: str, greeting: str = "Hello") -> str
```

### Literal, TypeAlias, and Overload

```python
from typing import Literal, TypeAlias, overload

# Literal -- restrict to exact values
Direction: TypeAlias = Literal["north", "south", "east", "west"]
LogLevel: TypeAlias = Literal["debug", "info", "warning", "error"]

def set_log_level(level: LogLevel) -> None:
    ...

# TypeAlias -- name complex types
JsonPrimitive: TypeAlias = str | int | float | bool | None
JsonValue: TypeAlias = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]
UserHandler: TypeAlias = Callable[[str, dict[str, str]], "Response"]

# Overload -- different return types based on input
@overload
def parse(raw: str, as_list: Literal[True]) -> list[str]: ...
@overload
def parse(raw: str, as_list: Literal[False] = ...) -> str: ...

def parse(raw: str, as_list: bool = False) -> str | list[str]:
    if as_list:
        return raw.split(",")
    return raw.strip()
```

### Dataclass Field Typing

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Config:
    # Required fields
    host: str
    port: int

    # Optional with defaults
    debug: bool = False
    tags: list[str] = field(default_factory=list)

    # ClassVar -- not included in __init__ or __repr__
    MAX_RETRIES: ClassVar[int] = 3

    # InitVar -- passed to __init__ but not stored as field
    from dataclasses import InitVar
    password: InitVar[str] = ""

    def __post_init__(self, password: str) -> None:
        self._hashed = hash(password) if password else 0
```

### TypeGuard and TypeIs (Narrowing)

```python
from typing import TypeGuard, TypeIs

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """Narrow list[object] to list[str]."""
    return all(isinstance(item, str) for item in val)

# Python 3.13+ TypeIs -- narrower and more precise than TypeGuard
def is_int(val: int | str) -> TypeIs[int]:
    return isinstance(val, int)

def process(val: int | str) -> None:
    if is_int(val):
        # val is narrowed to int
        print(val + 1)
    else:
        # val is narrowed to str (TypeIs does this, TypeGuard does not)
        print(val.upper())
```

## Anti-Patterns

- **Using `Any` to silence type errors**: Fix the actual type issue. `Any` disables
  all checking and defeats the purpose.
- **`Optional[X]` confusion**: `Optional[X]` means `X | None`, not "this parameter
  is optional." Use `X | None` for clarity (Python 3.10+).
- **Forgetting `@runtime_checkable` on Protocols**: Without it, `isinstance()` checks
  against the Protocol will fail at runtime.
- **Over-generic TypeVars**: If a TypeVar is only used once in a signature, it adds
  no value. Use the concrete type or `object` instead.
- **Ignoring `# type: ignore` comments**: Each suppression should have a specific
  error code: `# type: ignore[assignment]`. Never use bare `# type: ignore`.

## Quick Reference

| Construct | Purpose |
|---|---|
| `T = TypeVar("T")` | Generic type parameter |
| `TypeVar("T", bound=Base)` | Upper-bounded generic |
| `Protocol` | Structural subtyping (duck typing) |
| `ParamSpec("P")` | Preserve callable signatures |
| `Literal["a", "b"]` | Exact value types |
| `TypeAlias` | Name complex type expressions |
| `@overload` | Multiple return types by input |
| `TypeGuard[X]` | Custom type narrowing |
| `ClassVar[int]` | Class-level (not instance) field |
| `Final[str]` | Immutable binding |
