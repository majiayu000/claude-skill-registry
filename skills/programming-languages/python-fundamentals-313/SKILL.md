---
name: python-fundamentals-313
description: Complete Python 3.13+ fundamentals system. PROACTIVELY activate for: (1) Python 3.13 free-threading (no-GIL), (2) JIT compiler usage, (3) Pattern matching syntax, (4) Walrus operator, (5) F-string features 3.12+, (6) Type parameter syntax 3.12+, (7) Exception groups, (8) Dataclasses and enums, (9) Context managers. Provides: Modern syntax, performance features, best practices, naming conventions. Ensures correct Python 3.13+ patterns with optimal performance.
---

## Quick Reference

| Feature | Version | Syntax |
|---------|---------|--------|
| Free-threading | 3.13t | `python3.13t script.py` |
| JIT compiler | 3.13 | `PYTHON_JIT=1 python3.13 script.py` |
| Pattern matching | 3.10+ | `match x: case {...}:` |
| Walrus operator | 3.8+ | `if (n := len(x)) > 10:` |
| Type params | 3.12+ | `def first[T](items: list[T]) -> T:` |
| Type alias | 3.12+ | `type Point = tuple[float, float]` |

| Construct | Code | Use Case |
|-----------|------|----------|
| Exception Group | `ExceptionGroup("msg", [e1, e2])` | Multiple errors |
| except* | `except* ValueError as eg:` | Handle groups |
| @dataclass(slots=True) | Memory efficient | High-volume objects |
| StrEnum | `class Status(StrEnum):` | String enums 3.11+ |

## When to Use This Skill

Use for **Python 3.13+ fundamentals**:
- Learning Python 3.13 new features (free-threading, JIT)
- Using modern pattern matching syntax
- Writing type-annotated generic functions
- Creating dataclasses and enums
- Understanding Python naming conventions

**Related skills:**
- For type hints: see `python-type-hints`
- For async: see `python-asyncio`
- For common mistakes: see `python-gotchas`

---

# Python 3.13+ Fundamentals

## Overview

Python 3.13 (released October 2024) introduces significant performance improvements including experimental free-threading (no-GIL) mode, a JIT compiler, enhanced error messages, and improved REPL.

## Python 3.13 New Features

### Free-Threaded Mode (Experimental)

```python
# Python 3.13t - Free-threaded build (GIL disabled)
# Use python3.13t or python3.13t.exe

import threading
import time

def cpu_bound_task(n):
    """CPU-intensive calculation that benefits from true parallelism"""
    total = 0
    for i in range(n):
        total += i * i
    return total

# With free-threading, these actually run in parallel
threads = []
for _ in range(4):
    t = threading.Thread(target=cpu_bound_task, args=(10_000_000,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

**Key Points:**
- Requires separate executable: `python3.13t`
- Build with `--disable-gil` option
- Best for CPU-bound multi-threaded workloads
- Scientific computing and data analysis benefit most

### JIT Compiler (Experimental)

```python
# Enable JIT with environment variable or flag
# PYTHON_JIT=1 python3.13 script.py

# JIT provides 5-15% speedups, up to 30% for computation-heavy tasks
def fibonacci(n: int) -> int:
    """JIT-optimized computation"""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b

# Hot loops benefit most from JIT compilation
result = fibonacci(10000)
```

### Improved Interactive REPL

```python
# New REPL features (automatic in Python 3.13):
# - Multiline editing with history preservation
# - Colored prompts and tracebacks (default)
# - F1: Interactive help browsing
# - F2: History browsing (skips output)
# - F3: Paste mode for larger code blocks
# - Direct commands: help, exit, quit (no parentheses needed)
```

### Better Error Messages

```python
# Python 3.13 provides:
# - Colored tracebacks by default
# - Suggests correct keyword if incorrect one passed
# - Warns when script name shadows stdlib module

# Example: If you name a file "random.py"
# Python now shows: "Note: File '/path/random.py' shadows the 'random' module"
```

## Modern Python Syntax

### Pattern Matching (3.10+)

```python
def process_command(command: dict) -> str:
    match command:
        case {"action": "create", "name": str(name)}:
            return f"Creating {name}"
        case {"action": "delete", "id": int(id_)}:
            return f"Deleting item {id_}"
        case {"action": "update", "id": int(id_), "data": dict(data)}:
            return f"Updating {id_} with {data}"
        case {"action": action}:
            return f"Unknown action: {action}"
        case _:
            return "Invalid command format"

# With guards
def categorize_value(value):
    match value:
        case int(n) if n < 0:
            return "negative"
        case int(n) if n == 0:
            return "zero"
        case int(n) if n > 0:
            return "positive"
        case float(f) if f.is_integer():
            return "float-integer"
        case str(s) if len(s) > 10:
            return "long-string"
        case _:
            return "other"
```

### Walrus Operator (:=)

```python
# Assignment expressions
if (n := len(data)) > 10:
    print(f"Processing {n} items")

# In comprehensions
filtered = [y for x in data if (y := transform(x)) is not None]

# In while loops
while (line := file.readline()):
    process(line)

# Avoid in simple cases - prefer explicit assignment
# Bad: if (x := get_value()) > 0: use(x)
# Good: x = get_value(); if x > 0: use(x)
```

### F-Strings (Enhanced in 3.12+)

```python
# Basic f-strings
name = "World"
print(f"Hello, {name}!")

# Expressions
items = [1, 2, 3]
print(f"Sum: {sum(items)}")

# Format specifiers
value = 123.456789
print(f"{value:.2f}")      # 123.46
print(f"{value:>10.2f}")   # '    123.46'
print(f"{value:_}")        # 123.456789 (underscore separator)

# Debug format (3.8+)
x = 42
print(f"{x=}")             # x=42
print(f"{x=:>5}")          # x=   42

# Nested quotes (3.12+)
data = {"key": "value"}
print(f"Value: {data["key"]}")  # Now allowed!

# Multiline f-strings (3.12+)
result = f"""
    Name: {user.name}
    Email: {user.email}
    Status: {"Active" if user.active else "Inactive"}
"""
```

### Type Parameter Syntax (3.12+)

```python
# New generic syntax - no need for TypeVar
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

# Type aliases (3.12+)
type Point = tuple[float, float]
type Vector[T] = list[T]

# Multiple type parameters
def merge[K, V](d1: dict[K, V], d2: dict[K, V]) -> dict[K, V]:
    return {**d1, **d2}

# Bounded type parameters
from collections.abc import Comparable

def max_value[T: Comparable](items: list[T]) -> T:
    return max(items)
```

## Memory and Performance

### Memory Optimizations

```python
# __slots__ for memory efficiency
class Point:
    __slots__ = ('x', 'y')

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Generator expressions (lazy evaluation)
# Bad: sum([x * x for x in range(1000000)])  # Creates full list
# Good: sum(x * x for x in range(1000000))   # Generator

# Use itertools for memory efficiency
from itertools import islice, chain, filterfalse

def chunked(iterable, n):
    """Yield successive n-sized chunks."""
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk
```

### Python 3.13 Memory Improvements

```python
# 7% smaller memory footprint vs 3.12
# Docstrings have leading indentation stripped
# Modified mimalloc allocator (default if platform supports)

# Check memory usage
import sys

obj = {"key": "value"}
print(sys.getsizeof(obj))

# For deep size calculation
def get_size(obj, seen=None):
    """Recursively calculate object size."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum(get_size(k, seen) + get_size(v, seen) for k, v in obj.items())
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(get_size(i, seen) for i in obj)
    return size
```

## Exception Handling

### Exception Groups (3.11+)

```python
# Raise multiple exceptions
def validate_data(data: dict):
    errors = []
    if not data.get("name"):
        errors.append(ValueError("name is required"))
    if not data.get("email"):
        errors.append(ValueError("email is required"))
    if not data.get("age") or data["age"] < 0:
        errors.append(ValueError("age must be positive"))

    if errors:
        raise ExceptionGroup("Validation failed", errors)

# Handle with except*
try:
    validate_data({})
except* ValueError as eg:
    for error in eg.exceptions:
        print(f"Validation error: {error}")

# Catch specific exception types
try:
    risky_operation()
except* TypeError as eg:
    handle_type_errors(eg.exceptions)
except* ValueError as eg:
    handle_value_errors(eg.exceptions)
```

### Add Notes to Exceptions (3.11+)

```python
try:
    process_data(data)
except ValueError as e:
    e.add_note(f"Processing data: {data[:100]}...")
    e.add_note(f"Timestamp: {datetime.now()}")
    raise

# Notes appear in traceback after exception message
```

## Best Practices

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "john"
def calculate_total(items):
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: SCREAMING_SNAKE_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Private: single underscore prefix
class MyClass:
    def __init__(self):
        self._internal_value = 42  # Convention: "private"

    def __private_method(self):  # Name mangling
        pass

# Dunder methods: double underscore
def __init__(self):
    pass
```

### Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Iterator, AsyncIterator

# Class-based context manager
class DatabaseConnection:
    def __init__(self, url: str):
        self.url = url
        self.connection = None

    def __enter__(self):
        self.connection = connect(self.url)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
        return False  # Don't suppress exceptions

# Generator-based context manager
@contextmanager
def temporary_directory() -> Iterator[str]:
    import tempfile
    import shutil

    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)

# Async context manager
@asynccontextmanager
async def async_session() -> AsyncIterator[Session]:
    session = await create_session()
    try:
        yield session
    finally:
        await session.close()
```

### Dataclasses

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    age: int = 0
    tags: list[str] = field(default_factory=list)
    id: Optional[int] = field(default=None, repr=False)

# Frozen (immutable)
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# With slots (memory efficient, 3.10+)
@dataclass(slots=True)
class OptimizedData:
    value: int
    label: str

# Post-init processing
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)

    def __post_init__(self):
        self.area = self.width * self.height

# Comparison and ordering
@dataclass(order=True)
class Priority:
    priority: int
    name: str = field(compare=False)
```

### Enums

```python
from enum import Enum, auto, StrEnum, IntEnum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# With auto values
class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

# String enum (3.11+)
class HttpMethod(StrEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()

# Integer enum
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Usage
status = Status.ACTIVE
print(status.value)  # "active"
print(status.name)   # "ACTIVE"

# Pattern matching with enums
match status:
    case Status.PENDING:
        print("Waiting...")
    case Status.ACTIVE:
        print("Processing...")
    case Status.COMPLETED | Status.CANCELLED:
        print("Done")
```
