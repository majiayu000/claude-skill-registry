---
name: python-type-system
description: Use when Python's type system including type hints, mypy, Protocol, TypedDict, and Generics. Use when working with Python type annotations.
allowed-tools:
  - Bash
  - Read
---

# Python Type System

Master Python's type system to write type-safe, maintainable code. This
skill covers type hints, static type checking with mypy, and advanced
typing features.

## Type Checking Tools

```bash
# Install mypy for static type checking
pip install mypy

# Run mypy on a file or directory
mypy my_module.py
mypy src/

# Run with specific configuration
mypy --config-file mypy.ini src/

# Run with strict mode
mypy --strict src/

# Show type coverage report
mypy --html-report mypy-report src/
```

## mypy Configuration

**mypy.ini configuration file:**

```ini
[mypy]
# Global options
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_unimported = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
check_untyped_defs = True
strict_equality = True

# Per-module options
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-third_party.*]
ignore_missing_imports = True
```

**pyproject.toml configuration:**

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
check_untyped_defs = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

## Basic Type Hints

**Primitive types and collections:**

```python
from typing import List, Dict, Set, Tuple, Optional, Union, Any

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}"

# Collections
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

# Optional (can be None)
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# Union types (multiple possible types)
def process_value(value: Union[int, str]) -> str:
    return str(value)

# Tuple with fixed types
def get_coordinates() -> Tuple[float, float]:
    return (37.7749, -122.4194)

# Any type (avoid when possible)
def process_data(data: Any) -> None:
    print(data)
```

## Modern Type Syntax (Python 3.10+)

**Using PEP 604 union syntax:**

```python
# Python 3.10+ union syntax with |
def process_value(value: int | str) -> str:
    return str(value)

# Optional with | None
def find_user(user_id: int) -> str | None:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

# Multiple unions
def handle_response(
    response: dict | list | str | None
) -> str:
    if response is None:
        return "No response"
    return str(response)
```

**Built-in generic types (Python 3.9+):**

```python
# Use built-in types instead of typing module
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def get_mapping() -> dict[str, list[int]]:
    return {"numbers": [1, 2, 3]}

def get_unique(items: list[str]) -> set[str]:
    return set(items)

# Nested generics
def group_items(
    items: list[tuple[str, int]]
) -> dict[str, list[int]]:
    result: dict[str, list[int]] = {}
    for key, value in items:
        result.setdefault(key, []).append(value)
    return result
```

## Generic Types

**Creating generic functions and classes:**

```python
from typing import TypeVar, Generic, Sequence

# Type variable
T = TypeVar("T")

def first(items: Sequence[T]) -> T | None:
    return items[0] if items else None

def last(items: list[T]) -> T | None:
    return items[-1] if items else None

# Constrained type variable
Number = TypeVar("Number", int, float)

def add(a: Number, b: Number) -> Number:
    return a + b  # type: ignore

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T | None:
        return self._items[-1] if self._items else None

# Usage
stack: Stack[int] = Stack()
stack.push(1)
stack.push(2)
value: int = stack.pop()
```

**Bound type variables:**

```python
from typing import TypeVar
from collections.abc import Sized

# Type variable with upper bound
TSized = TypeVar("TSized", bound=Sized)

def get_length(obj: TSized) -> int:
    return len(obj)

# Works with any Sized type
get_length("hello")
get_length([1, 2, 3])
get_length({"a": 1})
```

## Protocol (Structural Subtyping)

**Define interfaces using Protocol:**

```python
from typing import Protocol

# Define a protocol
class Drawable(Protocol):
    def draw(self) -> str:
        ...

# Classes that match the protocol don't need inheritance
class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

# Function accepts any type matching the protocol
def render(shape: Drawable) -> None:
    print(shape.draw())

# Works with any matching class
render(Circle())
render(Square())
```

**Protocol with properties and methods:**

```python
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other: "Comparable") -> bool:
        ...

    def __gt__(self, other: "Comparable") -> bool:
        ...

def find_max(items: list[Comparable]) -> Comparable:
    return max(items)

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __lt__(self, other: "Person") -> bool:
        return self.age < other.age

    def __gt__(self, other: "Person") -> bool:
        return self.age > other.age

# Works because Person implements Comparable protocol
people = [Person("Alice", 30), Person("Bob", 25)]
oldest = find_max(people)
```

**Runtime checkable protocols:**

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]:
        ...

class User:
    def __init__(self, name: str) -> None:
        self.name = name

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name}

user = User("Alice")
assert isinstance(user, Serializable)
```

## TypedDict

**Define dictionary shapes with TypedDict:**

```python
from typing import TypedDict, NotRequired

# Basic TypedDict
class UserDict(TypedDict):
    id: int
    name: str
    email: str

def create_user(user: UserDict) -> UserDict:
    return user

user: UserDict = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}

# Optional fields (Python 3.11+)
class PersonDict(TypedDict):
    name: str
    age: int
    email: NotRequired[str]  # Optional field

person: PersonDict = {"name": "Bob", "age": 30}

# Total=False makes all fields optional
class ConfigDict(TypedDict, total=False):
    host: str
    port: int
    debug: bool

config: ConfigDict = {"host": "localhost"}
```

**Inheritance with TypedDict:**

```python
from typing import TypedDict

class BaseUserDict(TypedDict):
    id: int
    name: str

class ExtendedUserDict(BaseUserDict):
    email: str
    is_active: bool

user: ExtendedUserDict = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "is_active": True
}
```

## Literal Types

**Restrict values to specific literals:**

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    print(f"Mode set to {mode}")

# Valid
set_mode("read")

# Type error: not a valid literal
# set_mode("invalid")

# Literal unions
Status = Literal["pending", "active", "completed"]

def update_status(status: Status) -> None:
    print(f"Status: {status}")

# Literal with multiple types
MixedLiteral = Literal[True, 1, "one"]
```

## Type Aliases

**Create type aliases for complex types:**

```python
from typing import TypeAlias

# Type alias
UserId: TypeAlias = int
UserName: TypeAlias = str

def get_user(user_id: UserId) -> UserName:
    return f"User {user_id}"

# Complex type alias
JsonValue: TypeAlias = (
    dict[str, "JsonValue"]
    | list["JsonValue"]
    | str
    | int
    | float
    | bool
    | None
)

def process_json(data: JsonValue) -> None:
    print(data)

# Generic type alias
Vector: TypeAlias = list[float]
Matrix: TypeAlias = list[Vector]

def multiply_matrix(a: Matrix, b: Matrix) -> Matrix:
    # Implementation
    return [[0.0]]
```

## Callable Types

**Type hints for functions and callables:**

```python
from typing import Callable

# Function that takes a callback
def apply_operation(
    x: int,
    y: int,
    operation: Callable[[int, int], int]
) -> int:
    return operation(x, y)

def add(a: int, b: int) -> int:
    return a + b

result = apply_operation(5, 3, add)

# Callable with no arguments
def execute(task: Callable[[], None]) -> None:
    task()

# Callback with multiple argument types
Callback: TypeAlias = Callable[[str, int], bool]

def register_handler(callback: Callback) -> None:
    callback("test", 42)
```

## ParamSpec and Concatenate

**Advanced callable typing:**

```python
from typing import Callable, ParamSpec, TypeVar, Concatenate
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

# Decorator that preserves function signature
def log_calls(
    func: Callable[P, R]
) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a: int, b: int) -> int:
    return a + b

# Concatenate adds parameters
def with_context(
    func: Callable[Concatenate[str, P], R]
) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func("context", *args, **kwargs)
    return wrapper
```

## Type Guards

**Create type guards for runtime type narrowing:**

```python
from typing import TypeGuard

def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process_strings(values: list[object]) -> None:
    if is_str_list(values):
        # Type narrowed to list[str]
        for value in values:
            print(value.upper())

# More complex type guard
def is_non_empty_str(val: str | None) -> TypeGuard[str]:
    return val is not None and len(val) > 0

def process_name(name: str | None) -> None:
    if is_non_empty_str(name):
        # Type narrowed to str (non-None)
        print(name.upper())
```

## Overload

**Multiple function signatures with overload:**

```python
from typing import overload, Literal

@overload
def get_value(key: str, as_int: Literal[True]) -> int:
    ...

@overload
def get_value(key: str, as_int: Literal[False]) -> str:
    ...

def get_value(key: str, as_int: bool) -> int | str:
    value = "42"
    return int(value) if as_int else value

# Type checker knows return type based on literal
int_value: int = get_value("key", True)
str_value: str = get_value("key", False)
```

## Common Patterns

**Avoiding common type checking issues:**

```python
from typing import TYPE_CHECKING, cast

# Avoid circular imports
if TYPE_CHECKING:
    from my_module import MyClass

def process(obj: "MyClass") -> None:
    pass

# Type casting when you know better than the type checker
def get_data() -> object:
    return {"key": "value"}

data = cast(dict[str, str], get_data())

# Assert type with reveal_type (mypy only)
x = [1, 2, 3]
# reveal_type(x)  # Reveals: list[int]

# Ignore type checking for specific line
result = some_untyped_function()  # type: ignore[no-untyped-call]

# Ignore specific error code
value: Any = get_dynamic_value()
processed = process_value(value)  # type: ignore[arg-type]
```

## When to Use This Skill

Use python-type-system when you need to:

- Add type hints to Python code for better IDE support and documentation
- Configure mypy for static type checking in your project
- Create reusable generic functions and classes
- Define structural interfaces using Protocol
- Specify exact dictionary shapes with TypedDict
- Create type-safe decorators with ParamSpec
- Implement runtime type narrowing with TypeGuard
- Handle complex union types and literal types
- Build type-safe APIs and library interfaces

## Best Practices

- Enable strict mode in mypy for maximum type safety
- Use Protocol for structural typing instead of ABC when possible
- Prefer built-in generic types (list, dict) over typing module (3.9+)
- Use TypedDict for dictionary shapes instead of Dict[str, Any]
- Create type aliases for complex types to improve readability
- Use TYPE_CHECKING to avoid circular import issues
- Add type hints incrementally, starting with public APIs
- Run mypy in CI/CD to catch type errors early
- Use reveal_type during development to debug type inference
- Avoid Any type except when interfacing with untyped code

## Common Pitfalls

- Forgetting to handle None in Optional types
- Using mutable default arguments (use None and create in function)
- Not using Protocol for duck-typed interfaces
- Overusing Any type, reducing type safety benefits
- Not enabling strict mode in mypy configuration
- Ignoring type errors instead of fixing them properly
- Using old typing syntax (List, Dict) in Python 3.9+
- Circular import issues with forward references
- Not understanding variance in generic types
- Mixing runtime behavior with type hints (use TypeGuard)

## Resources

- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 544 - Protocols](https://peps.python.org/pep-0544/)
- [PEP 589 - TypedDict](https://peps.python.org/pep-0589/)
- [PEP 604 - Union Syntax](https://peps.python.org/pep-0604/)
