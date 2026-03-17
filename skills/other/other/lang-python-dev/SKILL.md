---
name: lang-python-dev
description: Foundational Python patterns covering core syntax, idioms, type hints, testing, and modern tooling. Use when writing Python code, understanding Pythonic patterns, working with type hints, or needing guidance on which specialized Python skill to use. This is the entry point for Python development.
---

# Python Fundamentals

Foundational Python patterns and core language features. This skill serves as both a reference for common patterns and an index to specialized Python skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Python Skill Hierarchy                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                  ┌─────────────────────┐                        │
│                  │  lang-python-dev    │ ◄── You are here       │
│                  │   (foundation)      │                        │
│                  └──────────┬──────────┘                        │
│                             │                                   │
│     ┌───────────┬───────────┼───────────┬───────────┐          │
│     │           │           │           │           │          │
│     ▼           ▼           ▼           ▼           ▼          │
│ ┌────────┐ ┌────────┐ ┌─────────┐ ┌─────────┐ ┌────────┐      │
│ │packaging│ │testing │ │ async   │ │  data   │ │ web    │      │
│ │  -dev  │ │  -dev  │ │  -dev   │ │ science │ │ api    │      │
│ └────────┘ └────────┘ └─────────┘ └─────────┘ └────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**This skill covers:**
- Core syntax (functions, classes, decorators)
- Pythonic idioms and conventions
- Type hints and type checking
- Iteration and comprehensions
- Context managers and protocols
- Modern tooling (uv, ruff, mypy)
- Testing fundamentals

**This skill does NOT cover (see specialized skills):**
- Package publishing → `python-packaging-dev`
- Advanced testing strategies → `python-testing-dev`
- Async/await patterns → `python-async-dev`
- Data science libraries → `data-analysis-polars-dev`
- Web framework specifics → Framework-specific skills

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Define function | `def name(param: type) -> return_type:` |
| Define class | `class Name:` |
| List comprehension | `[expr for item in iterable if condition]` |
| Dict comprehension | `{k: v for k, v in items if condition}` |
| Context manager | `with resource as r:` |
| Decorator | `@decorator` above function |
| Type hint | `variable: Type = value` |
| Match statement | `match value: case pattern: ...` |
| Walrus operator | `if (x := func()) is not None:` |

---

## Skill Routing

Use this table to find the right specialized skill:

| When you need to... | Use this skill |
|---------------------|----------------|
| Package and publish to PyPI | `python-packaging-dev` |
| Set up pytest, fixtures, mocking | `python-testing-dev` |
| Work with async/await, asyncio | `python-async-dev` |
| Data analysis with Polars/Pandas | `data-analysis-polars-dev` |
| Build REST APIs | Framework-specific skills |

---

## Core Syntax

### Functions

```python
# Basic function
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Default arguments
def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"

# *args and **kwargs
def log_message(*args, **kwargs):
    print(f"Args: {args}")
    print(f"Kwargs: {kwargs}")

# Type hints with Optional, Union
from typing import Optional, Union

def find_user(user_id: int) -> Optional[dict]:
    # Returns dict or None
    return None

def process(value: Union[int, str]) -> str:
    return str(value)

# Modern union syntax (Python 3.10+)
def process(value: int | str) -> str:
    return str(value)
```

### Classes

```python
# Basic class
class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# Dataclass (preferred for data containers)
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: str
    age: int = 0  # Default value

    def greet(self) -> str:
        return f"Hello, {self.name}!"

# Inheritance
class AdminUser(User):
    def __init__(self, name: str, email: str, permissions: list[str]):
        super().__init__(name, email)
        self.permissions = permissions

# Property decorator
class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def area(self) -> float:
        return 3.14159 * self._radius ** 2

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float) -> None:
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

# Usage
circle = Circle(5)
print(circle.area)  # 78.53975
circle.radius = 10  # Uses setter
```

### Decorators

```python
# Function decorator
from functools import wraps
from typing import Callable, Any

def log_calls(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
def process_data(data: list) -> int:
    return len(data)

# Decorator with arguments
def repeat(times: int):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say_hello():
    print("Hello!")

# Class decorator
def singleton(cls):
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connection = "Connected"
```

---

## Type Hints

### Basic Types

```python
from typing import Any, Optional, Union

# Built-in types
name: str = "Alice"
age: int = 30
height: float = 5.8
is_active: bool = True

# Collections
numbers: list[int] = [1, 2, 3]
coords: tuple[float, float] = (10.5, 20.3)
user_ids: set[int] = {1, 2, 3}
config: dict[str, Any] = {"key": "value"}

# Optional (value or None)
middle_name: Optional[str] = None
# Equivalent to:
middle_name: str | None = None

# Union (multiple types)
user_id: Union[int, str] = 123
# Modern syntax:
user_id: int | str = 123
```

### Advanced Type Hints

```python
from typing import Protocol, TypeVar, Generic, Callable

# TypeVar for generics
T = TypeVar('T')

def first(items: list[T]) -> T:
    return items[0]

# Generic class
class Stack(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Protocol (structural typing)
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(obj: Drawable) -> None:
    obj.draw()

# Callable type hints
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

# TypedDict for dict with known keys
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    email: str
    age: int

user: UserDict = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}
```

### Type Checking

```python
# Runtime type checking with isinstance
def process(value: int | str) -> str:
    if isinstance(value, int):
        return f"Number: {value}"
    else:
        return f"String: {value}"

# Static type checking with mypy
# Run: mypy your_file.py

# Type narrowing
def get_length(value: str | list) -> int:
    if isinstance(value, str):
        # Type narrowed to str
        return len(value)
    else:
        # Type narrowed to list
        return len(value)

# Assert for type narrowing
def process_user(user: dict | None) -> str:
    assert user is not None
    # Type narrowed to dict
    return user["name"]
```

---

## Pythonic Idioms

### List Comprehensions

```python
# Basic list comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested
matrix = [[i+j for j in range(3)] for i in range(3)]

# Dict comprehension
word_lengths = {word: len(word) for word in ["hello", "world"]}

# Set comprehension
unique_lengths = {len(word) for word in ["hello", "world", "hi"]}

# Generator expression (lazy evaluation)
squares_gen = (x**2 for x in range(1000000))  # Memory efficient
```

### Iteration Patterns

```python
# Enumerate for index + value
for i, value in enumerate(["a", "b", "c"]):
    print(f"{i}: {value}")

# Zip for parallel iteration
names = ["Alice", "Bob"]
ages = [30, 25]
for name, age in zip(names, ages):
    print(f"{name} is {age}")

# Reversed iteration
for item in reversed([1, 2, 3]):
    print(item)

# Sorted iteration
for name in sorted(["Charlie", "Alice", "Bob"]):
    print(name)

# Dict iteration
user = {"name": "Alice", "age": 30}
for key, value in user.items():
    print(f"{key}: {value}")
```

### Context Managers

```python
# File handling
with open("file.txt", "r") as f:
    content = f.read()
# File automatically closed

# Multiple context managers
with open("input.txt") as infile, open("output.txt", "w") as outfile:
    outfile.write(infile.read())

# Custom context manager (class)
class Timer:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        print(f"Elapsed: {self.end - self.start:.2f}s")

with Timer():
    # Code to time
    time.sleep(1)

# Custom context manager (generator)
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"Elapsed: {end - start:.2f}s")

with timer():
    time.sleep(1)
```

### Match Statements (Python 3.10+)

```python
# Basic match
def http_status(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return "Unknown"

# Pattern matching with structures
def process_command(command):
    match command:
        case {"action": "create", "type": type_}:
            return f"Creating {type_}"
        case {"action": "delete", "id": id_}:
            return f"Deleting {id_}"
        case {"action": action}:
            return f"Unknown action: {action}"
        case _:
            return "Invalid command"

# Sequence patterns
def describe_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (0, y):
            return f"Y-axis at {y}"
        case (x, 0):
            return f"X-axis at {x}"
        case (x, y):
            return f"Point at ({x}, {y})"
```

### Walrus Operator (Python 3.8+)

```python
# Assignment expression
if (n := len(data)) > 10:
    print(f"Large dataset: {n} items")

# In while loops
while (line := file.readline()):
    process(line)

# In comprehensions
filtered = [y for x in data if (y := transform(x)) is not None]

# Multiple uses
if (match := pattern.search(text)) and match.group(1):
    return match.group(1)
```

---

## Error Handling

### Exception Basics

```python
# Try-except
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# Multiple exceptions
try:
    data = load_data()
except (FileNotFoundError, PermissionError) as e:
    print(f"Error loading data: {e}")

# Try-except-else-finally
try:
    result = risky_operation()
except ValueError as e:
    print(f"Invalid value: {e}")
else:
    # Runs if no exception
    print("Success!")
finally:
    # Always runs
    cleanup()
```

### Custom Exceptions

```python
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class ConfigError(Exception):
    """Configuration-related errors."""
    def __init__(self, key: str, message: str):
        self.key = key
        super().__init__(f"Config error for '{key}': {message}")

# Raising exceptions
def validate_age(age: int) -> None:
    if age < 0:
        raise ValidationError("Age cannot be negative")
    if age > 150:
        raise ValidationError("Age unrealistic")

# Exception chaining
try:
    process_data()
except ValueError as e:
    raise ConfigError("database_url", "Invalid format") from e
```

---

## Modern Tooling

### uv (Fast Python Package Manager)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create new project
uv init my-project
cd my-project

# Add dependencies
uv add requests pytest

# Run script
uv run python script.py

# Sync dependencies
uv sync
```

### ruff (Fast Linter & Formatter)

```bash
# Install
uv add --dev ruff

# Lint
ruff check .

# Format
ruff format .

# Auto-fix issues
ruff check --fix .
```

**pyproject.toml configuration:**
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### mypy (Static Type Checker)

```bash
# Install
uv add --dev mypy

# Run type checking
mypy src/

# With strict mode
mypy --strict src/
```

**pyproject.toml configuration:**
```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
strict_equality = true
```

---

## Testing Fundamentals

### pytest Basics

```python
# test_example.py

def test_addition():
    assert 1 + 1 == 2

def test_string_operations():
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert "world" in text

# Parametrize tests
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (10, 11),
])
def test_increment(input, expected):
    assert input + 1 == expected

# Fixtures
@pytest.fixture
def sample_user():
    return {"name": "Alice", "age": 30}

def test_user_data(sample_user):
    assert sample_user["name"] == "Alice"
    assert sample_user["age"] == 30

# Exception testing
def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        1 / 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py

# Run tests matching pattern
pytest -k "test_user"

# Show print output
pytest -s

# Coverage report
pytest --cov=src tests/
```

**pyproject.toml configuration:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]
```

---

## Common Patterns

### Singleton Pattern

```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Or use decorator (shown earlier)
```

### Factory Pattern

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self) -> str:
        pass

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"

def animal_factory(animal_type: str) -> Animal:
    if animal_type == "dog":
        return Dog()
    elif animal_type == "cat":
        return Cat()
    else:
        raise ValueError(f"Unknown animal type: {animal_type}")

# Usage
animal = animal_factory("dog")
print(animal.speak())  # "Woof!"
```

### Builder Pattern

```python
class RequestBuilder:
    def __init__(self):
        self._url = ""
        self._method = "GET"
        self._headers: dict[str, str] = {}
        self._body: dict | None = None

    def url(self, url: str) -> "RequestBuilder":
        self._url = url
        return self

    def method(self, method: str) -> "RequestBuilder":
        self._method = method
        return self

    def header(self, key: str, value: str) -> "RequestBuilder":
        self._headers[key] = value
        return self

    def body(self, body: dict) -> "RequestBuilder":
        self._body = body
        return self

    def build(self) -> dict:
        return {
            "url": self._url,
            "method": self._method,
            "headers": self._headers,
            "body": self._body,
        }

# Usage
request = (RequestBuilder()
    .url("https://api.example.com/users")
    .method("POST")
    .header("Content-Type", "application/json")
    .body({"name": "Alice"})
    .build())
```

---

## Troubleshooting

### ImportError / ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'xyz'`

**Fixes:**
1. Install the package: `uv add xyz`
2. Check virtual environment is activated
3. Verify package name (e.g., `beautifulsoup4` not `bs4`)

### Type Errors with mypy

**Problem:** `error: Incompatible types in assignment`

**Fixes:**
1. Add explicit type hints
2. Use type narrowing with `isinstance()`
3. Use `# type: ignore` comment if necessary (last resort)

### Circular Imports

**Problem:** `ImportError: cannot import name 'X' from partially initialized module`

**Fixes:**
1. Move import inside function (lazy import)
2. Restructure code to remove circular dependency
3. Use `TYPE_CHECKING` for type-only imports:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from other_module import SomeClass

def my_function(obj: "SomeClass") -> None:
    # String annotation avoids runtime import
    pass
```

### Mutable Default Arguments

**Problem:** Default list/dict shared across calls

```python
# Bad
def add_item(item, items=[]):
    items.append(item)
    return items

# Each call shares the same list!
```

**Fix:**
```python
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## Module System

Python uses a straightforward module and package system for code organization.

### Import and Export

```python
# Importing modules
import math
import json
from pathlib import Path

# Named imports
from typing import Optional, List, Dict
from dataclasses import dataclass

# Import with alias
import numpy as np
import pandas as pd
from collections import defaultdict as dd

# Import everything (avoid in production)
from math import *  # Pollutes namespace

# Relative imports (within package)
from . import sibling_module
from .. import parent_module
from ..utils import helper_function
```

### Module Structure

```python
# my_module.py - A simple module
"""Module docstring describing purpose."""

# Module-level constants
VERSION = "1.0.0"
DEFAULT_TIMEOUT = 30

# Module-level variables
_private_var = "internal use only"
public_var = "accessible from outside"

# Functions
def public_function():
    """Public API function."""
    return _private_helper()

def _private_helper():
    """Private helper (by convention)."""
    return "helper result"

# Classes
class MyClass:
    """Public class."""
    pass
```

### Packages and __init__.py

```python
# Project structure
mypackage/
├── __init__.py       # Makes directory a package
├── module_a.py
├── module_b.py
└── subpackage/
    ├── __init__.py
    └── module_c.py

# mypackage/__init__.py - Package initialization
"""MyPackage - A sample package."""

__version__ = "1.0.0"
__all__ = ["ClassA", "ClassB", "function_a"]  # Controls `from package import *`

# Import and expose public API
from .module_a import ClassA, function_a
from .module_b import ClassB
from .subpackage import module_c

# Package-level initialization
def init():
    """Initialize package resources."""
    pass

# mypackage/module_a.py
class ClassA:
    pass

def function_a():
    pass

# Usage
from mypackage import ClassA, function_a
from mypackage.subpackage import module_c
```

### Namespace Packages (PEP 420)

```python
# No __init__.py needed for namespace packages (Python 3.3+)
# Allows multiple directories to contribute to same package

# Directory structure
site-packages/
├── mynamespace/
│   └── plugin_a/
│       └── core.py
└── another-location/
    └── mynamespace/
        └── plugin_b/
            └── core.py

# Both are part of 'mynamespace' package
from mynamespace.plugin_a import core as core_a
from mynamespace.plugin_b import core as core_b
```

### Lazy Imports

```python
# Import at module level (loaded on import)
import heavy_module  # Loaded immediately

# Lazy import inside function (loaded on use)
def process_data():
    import heavy_module  # Only loaded when function is called
    return heavy_module.process()

# TYPE_CHECKING for type-only imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from expensive_module import ExpensiveClass

def my_function(obj: "ExpensiveClass") -> None:
    # String annotation avoids runtime import
    pass
```

### Dynamic Imports

```python
# importlib for dynamic imports
import importlib

# Import module by name
module_name = "json"
json_module = importlib.import_module(module_name)
data = json_module.loads('{"key": "value"}')

# Import from package
module = importlib.import_module(".module_a", package="mypackage")

# Reload module (useful for development)
importlib.reload(module)

# Check if module exists
import importlib.util
spec = importlib.util.find_spec("optional_module")
if spec is not None:
    import optional_module
```

### sys.path and Module Resolution

```python
import sys
from pathlib import Path

# View module search paths
print(sys.path)

# Add directory to search path
sys.path.insert(0, str(Path(__file__).parent / "lib"))

# Module resolution order:
# 1. Built-in modules
# 2. Current directory
# 3. PYTHONPATH environment variable
# 4. Installation-dependent defaults (site-packages)

# Check where module was loaded from
import json
print(json.__file__)  # /usr/lib/python3.11/json/__init__.py
```

### __all__ and Public API

```python
# module.py
"""Sample module with explicit public API."""

__all__ = ["public_function", "PublicClass"]  # Explicit exports

def public_function():
    """Part of public API."""
    pass

class PublicClass:
    """Part of public API."""
    pass

def _private_function():
    """Not exported (by convention)."""
    pass

class _PrivateClass:
    """Not exported (by convention)."""
    pass

# Usage
from module import *  # Only imports public_function and PublicClass
```

---

## Concurrency

Python supports multiple concurrency models: threading, multiprocessing, and async/await.

### Threading (I/O-bound tasks)

```python
import threading
import time
from queue import Queue

# Basic thread
def worker(name: str, delay: float) -> None:
    time.sleep(delay)
    print(f"Worker {name} done")

thread = threading.Thread(target=worker, args=("A", 1.0))
thread.start()
thread.join()  # Wait for completion

# Thread with return value (using Queue)
def worker_with_result(queue: Queue, n: int) -> None:
    result = n * 2
    queue.put(result)

q: Queue = Queue()
t = threading.Thread(target=worker_with_result, args=(q, 5))
t.start()
t.join()
result = q.get()  # 10

# ThreadPoolExecutor (easier)
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_url(url: str) -> str:
    # I/O-bound operation
    return f"Content from {url}"

urls = ["http://example.com", "http://example.org"]

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_url, url) for url in urls]
    for future in as_completed(futures):
        print(future.result())
```

### Multiprocessing (CPU-bound tasks)

```python
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

# Basic process
def cpu_bound_task(n: int) -> int:
    # Heavy computation
    return sum(i * i for i in range(n))

process = mp.Process(target=cpu_bound_task, args=(1000000,))
process.start()
process.join()

# ProcessPoolExecutor (recommended)
def process_item(item: int) -> int:
    return item * item

with ProcessPoolExecutor(max_workers=4) as executor:
    items = range(10)
    results = list(executor.map(process_item, items))
    print(results)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Shared memory (for communication)
from multiprocessing import Value, Array, Manager

# Shared value
counter = Value('i', 0)  # 'i' = integer

def increment(counter):
    with counter.get_lock():
        counter.value += 1

# Shared array
arr = Array('d', [1.0, 2.0, 3.0])  # 'd' = double

# Manager (for complex types)
with mp.Manager() as manager:
    shared_dict = manager.dict()
    shared_list = manager.list()
```

### Async/Await (Asyncio)

```python
import asyncio
import httpx

# Basic async function
async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.1)  # Simulate I/O
    return {"id": user_id, "name": f"User {user_id}"}

# Run async function
result = asyncio.run(fetch_user(1))

# Concurrent execution
async def main():
    # Sequential (slow)
    user1 = await fetch_user(1)
    user2 = await fetch_user(2)

    # Concurrent (fast)
    users = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3)
    )
    print(users)

asyncio.run(main())

# Real HTTP example
async def fetch_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# Error handling
async def fetch_with_timeout(url: str) -> str:
    try:
        return await asyncio.wait_for(fetch_url(url), timeout=5.0)
    except asyncio.TimeoutError:
        return "Request timed out"

# Creating tasks
async def background_task():
    while True:
        print("Working...")
        await asyncio.sleep(1)

async def main():
    task = asyncio.create_task(background_task())
    await asyncio.sleep(3)
    task.cancel()  # Stop background task
    try:
        await task
    except asyncio.CancelledError:
        print("Task cancelled")

asyncio.run(main())
```

### GIL Considerations

```python
# Global Interpreter Lock (GIL) implications:

# ❌ Threading does NOT help CPU-bound tasks
# (GIL prevents parallel CPU execution)
import threading
import time

def cpu_intensive():
    sum(i**2 for i in range(10_000_000))

# This is NOT faster (GIL prevents parallel execution)
threads = [threading.Thread(target=cpu_intensive) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# ✓ Threading DOES help I/O-bound tasks
# (GIL released during I/O operations)
def io_intensive():
    time.sleep(1)  # GIL released during sleep

threads = [threading.Thread(target=io_intensive) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# ✓ Multiprocessing bypasses GIL
# (Each process has its own Python interpreter)
from multiprocessing import Pool

with Pool(4) as pool:
    pool.map(cpu_intensive, range(4))  # True parallelism

# ✓ Asyncio for many concurrent I/O operations
# (Single-threaded but non-blocking)
async def many_io_operations():
    await asyncio.gather(*[io_task() for _ in range(1000)])
```

### Choosing the Right Model

```python
# Decision matrix:

# I/O-bound + simple → Threading
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor() as executor:
    results = executor.map(fetch_url, urls)

# I/O-bound + many connections → Asyncio
async def fetch_all():
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        return await asyncio.gather(*tasks)

# CPU-bound → Multiprocessing
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as executor:
    results = executor.map(compute_heavy, data)

# Mixed workload → Combination
async def mixed():
    # Async for I/O
    data = await fetch_data()

    # Process pool for CPU work
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(executor, process_cpu_bound, data)

    return result
```

### See Also

- `patterns-concurrency-dev` - Cross-language concurrency patterns and translation

---

## Build and Dependencies

Python uses package managers and pyproject.toml for dependency management and build configuration.

### Package Managers

```bash
# pip (standard package manager)
pip install requests
pip install pytest==7.4.0
pip install "flask>=2.0,<3.0"

# Requirements file
pip install -r requirements.txt
pip freeze > requirements.txt

# uv (fast, modern package manager - recommended)
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init my-project
cd my-project

# Add dependencies
uv add requests pytest

# Development dependencies
uv add --dev ruff mypy

# Run commands in virtual environment
uv run python script.py
uv run pytest

# Sync dependencies
uv sync
```

### Virtual Environments

```bash
# Standard venv
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
deactivate

# With uv (automatic)
uv venv           # Creates .venv
source .venv/bin/activate
uv pip install requests  # Faster than pip

# poetry (alternative)
poetry new my-project
poetry add requests
poetry install
poetry shell
```

### pyproject.toml (PEP 621)

```toml
# Modern Python project configuration
[project]
name = "myproject"
version = "1.0.0"
description = "A sample Python project"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "you@example.com" }
]
keywords = ["sample", "example"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.11",
]

# Dependencies
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

# Optional dependencies (extras)
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
    "mypy>=1.6.0",
]
docs = [
    "sphinx>=7.0.0",
]

# Entry points (CLI commands)
[project.scripts]
mytool = "myproject.cli:main"

# URLs
[project.urls]
Homepage = "https://github.com/user/myproject"
Documentation = "https://myproject.readthedocs.io"
Repository = "https://github.com/user/myproject.git"
Changelog = "https://github.com/user/myproject/blob/main/CHANGELOG.md"

# Build system
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Tool configurations
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = ["-ra", "--strict-markers"]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

### requirements.txt vs pyproject.toml

```python
# requirements.txt (legacy, still common)
# requirements.txt
requests==2.31.0
pytest>=7.4.0,<8.0.0
black==23.10.0

# requirements-dev.txt
-r requirements.txt
pytest-cov==4.1.0
mypy==1.6.0

# Install
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Generate from current environment
pip freeze > requirements.txt

# pyproject.toml (modern, recommended)
[project]
dependencies = [
    "requests==2.31.0",
    "pytest>=7.4.0,<8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest-cov==4.1.0",
    "mypy==1.6.0",
]

# Install
pip install .              # Install package
pip install .[dev]         # Install with dev extras
uv sync                    # With uv
```

### Dependency Resolution

```bash
# pip-tools (for lockfiles)
pip install pip-tools

# requirements.in (high-level dependencies)
requests
pytest>=7.4.0

# Generate lockfile
pip-compile requirements.in
# Creates requirements.txt with all transitive dependencies pinned

# Sync environment
pip-sync requirements.txt

# With uv (built-in lockfile)
# uv.lock is automatically generated and maintained
uv add requests    # Updates uv.lock
uv sync           # Installs from lockfile
```

### Building Distributions

```bash
# Build source distribution and wheel
python -m build

# Creates:
# dist/myproject-1.0.0.tar.gz (source)
# dist/myproject-1.0.0-py3-none-any.whl (wheel)

# With uv
uv build

# Install locally for development
pip install -e .      # Editable install
uv pip install -e .   # With uv

# Publish to PyPI
pip install twine
twine upload dist/*

# With poetry
poetry build
poetry publish
```

### Project Structure Best Practices

```
myproject/
├── pyproject.toml           # Project config (modern)
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── myproject/           # Source code
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
├── tests/                   # Tests mirror src/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_cli.py
├── docs/                    # Documentation
│   └── conf.py
└── .venv/                   # Virtual environment (gitignored)

# Alternative (flat layout)
myproject/
├── pyproject.toml
├── myproject/               # Source at root
│   ├── __init__.py
│   └── core.py
└── tests/
    └── test_core.py
```

### Environment Variables and Configuration

```python
# Using python-dotenv
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")

# Using pydantic settings (recommended)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    database_url: str = "sqlite:///default.db"
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
print(settings.api_key)

# .env file
# API_KEY=secret123
# DATABASE_URL=postgresql://localhost/mydb
# DEBUG=true
```

---

## Zero and Default Values

Python's handling of None, default arguments, and empty values requires careful attention to avoid common pitfalls.

### None vs Empty Collections

```python
# None represents absence of value
value: str | None = None  # No value assigned

# Empty collections are valid values (not None)
empty_list: list[str] = []      # Empty but exists
empty_dict: dict[str, int] = {} # Empty but exists
empty_str: str = ""             # Empty but exists

# Check for None vs empty
if value is None:           # Check for None specifically
    print("No value")
elif not value:             # Falsy check (empty string, 0, etc.)
    print("Empty or falsy")

# Common pattern: treat None and empty differently
def process(items: list[str] | None) -> list[str]:
    if items is None:
        return []  # No input provided
    if not items:
        return ["default"]  # Empty list provided
    return items
```

### Default Argument Pitfalls

```python
# ❌ DANGEROUS: Mutable default argument
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)  # Shared across all calls!
    return items

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] - NOT ['b']!

# ✓ CORRECT: Use None as sentinel
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

add_item("a")  # ['a']
add_item("b")  # ['b'] - Correct!

# ✓ ALTERNATIVE: Use default_factory with dataclass
from dataclasses import dataclass, field

@dataclass
class Container:
    items: list[str] = field(default_factory=list)
    config: dict[str, str] = field(default_factory=dict)
```

### Sentinel Values

```python
# When None is a valid value, use a sentinel
_MISSING = object()

def get_config(key: str, default=_MISSING):
    value = config_store.get(key)
    if value is not None:
        return value
    if default is not _MISSING:
        return default
    raise KeyError(f"Config key '{key}' not found")

# Usage
get_config("timeout", default=30)  # Returns 30 if not found
get_config("timeout", default=None)  # Returns None if not found (None is valid)
get_config("timeout")  # Raises KeyError if not found

# Type-safe sentinel with typing
from typing import TypeVar, overload

T = TypeVar('T')
_UNSET: object = object()

@overload
def get_value(key: str) -> str: ...  # Raises if missing

@overload
def get_value(key: str, default: T) -> str | T: ...  # Returns default if missing

def get_value(key: str, default: object = _UNSET) -> str:
    if key in store:
        return store[key]
    if default is not _UNSET:
        return default
    raise KeyError(key)
```

### Optional vs Union with None

```python
from typing import Optional

# These are equivalent
name: Optional[str] = None
name: str | None = None  # Python 3.10+ preferred

# Optional does NOT mean "optional parameter"
def greet(
    name: str,                    # Required
    title: str | None = None,     # Optional with None default
    suffix: str = "",             # Optional with empty string default
) -> str:
    result = name
    if title:
        result = f"{title} {result}"
    if suffix:
        result = f"{result} {suffix}"
    return result

# Common mistake: Optional parameter without default
def bad_func(value: str | None) -> str:  # Required but can be None
    ...

bad_func(None)  # Valid - must pass explicitly
bad_func()      # Error - argument required
```

### Truthiness and Falsy Values

```python
# Python falsy values
False           # bool
None            # NoneType
0, 0.0, 0j      # numeric zeros
"", '', """"""  # empty strings
[], (), {}      # empty collections
set()           # empty set

# Explicit checks vs truthiness
data = {"count": 0}

# ❌ Bug: 0 is falsy
if not data.get("count"):
    data["count"] = 1  # Overwrites valid 0!

# ✓ Correct: Check for None explicitly
if data.get("count") is None:
    data["count"] = 1  # Only sets if missing

# ✓ Alternative: Use default
count = data.get("count", 0)  # Returns 0 if missing
```

### Default Values in Dataclasses and Pydantic

```python
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

# Dataclass defaults
@dataclass
class Config:
    # Simple defaults
    timeout: int = 30
    debug: bool = False

    # Mutable defaults require field()
    tags: list[str] = field(default_factory=list)
    settings: dict[str, str] = field(default_factory=dict)

    # Computed defaults
    created_at: datetime = field(default_factory=datetime.now)

# Pydantic defaults
class UserConfig(BaseModel):
    # Simple defaults
    timeout: int = 30
    debug: bool = False

    # Mutable defaults (Pydantic handles this correctly)
    tags: list[str] = []
    settings: dict[str, str] = {}

    # Factory defaults
    id: str = Field(default_factory=lambda: str(uuid4()))

    # Validated defaults
    port: int = Field(default=8080, ge=1, le=65535)
```

### None Coalescing Patterns

```python
# Python doesn't have ?? operator, use these patterns:

# or operator (for falsy, not just None)
name = user_name or "Anonymous"  # ⚠️ Empty string becomes "Anonymous"

# Ternary for None-specific
name = user_name if user_name is not None else "Anonymous"

# Walrus operator (Python 3.8+)
if (result := get_value()) is not None:
    process(result)

# getattr with default
value = getattr(obj, "attr", "default")

# dict.get with default
value = config.get("key", "default")

# Common helper function
def coalesce(*args):
    """Return first non-None argument."""
    for arg in args:
        if arg is not None:
            return arg
    return None

result = coalesce(primary, secondary, "fallback")
```

---

## Serialization

Python provides multiple approaches for serialization, from built-in JSON to type-safe Pydantic models.

### JSON Serialization

```python
import json
from typing import Any
from datetime import datetime, date
from dataclasses import dataclass, asdict

# Basic JSON
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data)                    # To string
json_bytes = json.dumps(data).encode('utf-8')  # To bytes
parsed = json.loads(json_str)                  # From string

# Pretty printing
formatted = json.dumps(data, indent=2, sort_keys=True)

# File I/O
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)
```

### Custom JSON Encoders

```python
from json import JSONEncoder
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from enum import Enum
from dataclasses import dataclass, asdict, is_dataclass

class CustomEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, Enum):
            return obj.value
        if is_dataclass(obj):
            return asdict(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return super().default(obj)

# Usage
data = {
    "created": datetime.now(),
    "amount": Decimal("99.99"),
    "id": UUID("12345678-1234-5678-1234-567812345678"),
}
json_str = json.dumps(data, cls=CustomEncoder)

# Function-based encoder
def json_serializer(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

json.dumps(data, default=json_serializer)
```

### Pydantic Models (Recommended)

```python
from pydantic import BaseModel, Field, field_validator, field_serializer
from datetime import datetime
from typing import Optional
from enum import Enum

class Status(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('name cannot be empty or whitespace')
        return v.strip()

    @field_serializer('created_at')
    def serialize_datetime(self, dt: datetime) -> str:
        return dt.isoformat()

# Parsing from dict/JSON
user = User(id=1, name="Alice")
user = User.model_validate({"id": 1, "name": "Alice"})
user = User.model_validate_json('{"id": 1, "name": "Alice"}')

# Serialization
user_dict = user.model_dump()                          # To dict
user_dict = user.model_dump(exclude_none=True)         # Exclude None values
user_dict = user.model_dump(exclude={"created_at"})    # Exclude fields
user_json = user.model_dump_json()                     # To JSON string
user_json = user.model_dump_json(indent=2)             # Pretty JSON

# Schema generation
schema = User.model_json_schema()  # JSON Schema dict
```

### Pydantic Settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="APP_",
        case_sensitive=False,
    )

    database_url: str
    api_key: str = Field(alias="SECRET_KEY")
    debug: bool = False
    max_connections: int = 10

# Loads from environment variables: APP_DATABASE_URL, SECRET_KEY, etc.
settings = Settings()
```

### Dataclasses with Serialization

```python
from dataclasses import dataclass, asdict, field
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        if "created_at" in data and isinstance(data["created_at"], str):
            data["created_at"] = datetime.fromisoformat(data["created_at"])
        return cls(**data)

# With dacite for complex parsing
from dacite import from_dict, Config

user = from_dict(
    User,
    data,
    config=Config(
        cast=[datetime],
        strict=True,
    )
)
```

### Binary Serialization

```python
import pickle
import struct
from typing import Any

# Pickle (Python-specific, not secure for untrusted data)
data = {"key": "value", "numbers": [1, 2, 3]}
pickled = pickle.dumps(data)
restored = pickle.loads(pickled)

# File I/O
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

with open("data.pkl", "rb") as f:
    loaded = pickle.load(f)

# ⚠️ Security warning: Never unpickle untrusted data

# MessagePack (cross-language, faster than JSON)
import msgpack

packed = msgpack.packb({"key": "value"})
unpacked = msgpack.unpackb(packed)

# Struct (for binary protocols)
# Pack: int, float, 10-char string
packed = struct.pack("if10s", 42, 3.14, b"hello")
unpacked = struct.unpack("if10s", packed)
```

### YAML and TOML

```python
# YAML
import yaml

data = {"name": "config", "settings": {"debug": True}}
yaml_str = yaml.dump(data, default_flow_style=False)
parsed = yaml.safe_load(yaml_str)

# TOML (Python 3.11+ has tomllib built-in)
import tomllib  # Read-only, built-in

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

# For writing TOML, use tomli-w
import tomli_w

with open("config.toml", "wb") as f:
    tomli_w.dump(data, f)
```

### Validation Patterns

```python
from pydantic import BaseModel, field_validator, model_validator
from typing import Self

class CreateUserRequest(BaseModel):
    username: str
    password: str
    confirm_password: str

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('must contain uppercase letter')
        return v

    @model_validator(mode='after')
    def passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('passwords do not match')
        return self

# Usage
try:
    request = CreateUserRequest(
        username="alice123",
        password="SecurePass123",
        confirm_password="SecurePass123",
    )
except ValidationError as e:
    print(e.errors())
```

### See Also

- `patterns-serialization-dev` - Cross-language serialization patterns and comparisons

---

## Cross-Cutting Patterns

For cross-language comparison and translation patterns, see:

- `patterns-concurrency-dev` - Async/await, threading, multiprocessing patterns across languages
- `patterns-serialization-dev` - JSON, validation, type-safe parsing across languages
- `patterns-metaprogramming-dev` - Decorators, metaclasses, dynamic code generation across languages

---

## References

- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints - PEP 484](https://peps.python.org/pep-0484/)
- [pyproject.toml - PEP 621](https://peps.python.org/pep-0621/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- Specialized skills: `python-packaging-dev`, `python-testing-dev`, `python-async-dev`, `data-analysis-polars-dev`
