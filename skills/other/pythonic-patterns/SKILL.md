---
name: pythonic-patterns
description: >
  Apply idiomatic Python patterns: list comprehensions, generators, context managers,
  decorators, dataclasses, walrus operator, and unpacking. Use when the user writes
  Python code, asks for Pythonic idioms, refactors Python, or mentions any of these
  patterns. Trigger proactively when you see non-idiomatic Python.
---

# Pythonic Patterns

Write idiomatic Python that leverages the language's expressive power. Pythonic code
is concise, readable, and uses built-in constructs instead of reinventing them.

## When to Use
- User writes Python loops that could be comprehensions
- User asks for "Pythonic" or "idiomatic" Python
- Refactoring Python code for readability
- User works with iterables, files, or resource management
- User defines simple data containers or wrapper functions

## Core Patterns

### List Comprehensions and Generator Expressions

Use comprehensions for transforming and filtering sequences. Use generator expressions
for large datasets to avoid materializing the entire list in memory.

```python
# Comprehension with filtering
active_emails = [user.email for user in users if user.is_active]

# Dict comprehension
scores_by_name = {s.name: s.score for s in students}

# Set comprehension for deduplication
unique_domains = {email.split("@")[1] for email in emails}

# Generator expression for large data -- lazy evaluation
total = sum(order.amount for order in orders if order.status == "paid")

# Nested comprehension (keep it readable -- max 2 levels)
flat = [cell for row in matrix for cell in row]
```

### Generators and Iterators

Use generators when you need lazy evaluation, infinite sequences, or pipeline processing.

```python
def read_chunks(file_path: str, chunk_size: int = 8192):
    """Yield file chunks without loading entire file into memory."""
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

def fibonacci():
    """Infinite Fibonacci generator."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Pipeline processing with generators
def process_pipeline(records):
    cleaned = (clean(r) for r in records)
    validated = (r for r in cleaned if is_valid(r))
    transformed = (transform(r) for r in validated)
    yield from transformed
```

### Context Managers

Use context managers for any resource that needs setup/teardown. Prefer `contextlib`
for simple cases.

```python
from contextlib import contextmanager

@contextmanager
def temporary_directory(prefix: str = "tmp"):
    """Create and clean up a temporary directory."""
    import tempfile
    import shutil
    path = tempfile.mkdtemp(prefix=prefix)
    try:
        yield path
    finally:
        shutil.rmtree(path)

# Class-based for complex state
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False  # Do not suppress exceptions
```

### Decorators

Use decorators to separate cross-cutting concerns from business logic.

```python
import functools
import time
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on exception with exponential backoff."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            raise RuntimeError("Unreachable")
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    ...
```

### Dataclasses

Use dataclasses for data containers instead of plain dicts or manual `__init__`.

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)  # frozen=True for immutability
class Event:
    name: str
    timestamp: datetime
    tags: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def is_recent(self) -> bool:
        return (datetime.now() - self.timestamp).days < 7
```

### Walrus Operator (:=)

Use the walrus operator to assign and test in one expression. Keep usage simple
and readable.

```python
# Filter and capture in comprehension
results = [
    matched
    for line in lines
    if (matched := pattern.search(line)) is not None
]

# Avoid repeated expensive calls
while (chunk := file.read(8192)):
    process(chunk)

# Guard clause with assignment
if (user := find_user(user_id)) is None:
    raise UserNotFoundError(user_id)
```

### Unpacking and Starred Expressions

```python
# Swap without temp variable
a, b = b, a

# Extended unpacking
first, *middle, last = scores

# Ignore values
_, _, status_code = parse_response(raw)

# Dict merging (Python 3.9+)
merged = {**defaults, **overrides}

# Function argument unpacking
def create_user(name: str, email: str, role: str = "user"):
    ...

config = {"name": "Alice", "email": "alice@example.com"}
user = create_user(**config)
```

## Anti-Patterns

- **Overcomplex comprehensions**: If a comprehension exceeds one line or has 3+ levels
  of nesting, use a regular loop instead. Readability beats cleverness.
- **Ignoring generators for large data**: Using `[x for x in huge_list]` when you only
  iterate once wastes memory. Use a generator expression.
- **Bare `except`**: Always catch specific exceptions. `except Exception` at minimum.
- **Mutable default arguments**: Never use `def f(items=[])`. Use `None` and assign
  inside the function body, or use `field(default_factory=list)` for dataclasses.
- **Using `dict` as a data container**: If you access the same keys repeatedly, use a
  dataclass or NamedTuple instead.

## Quick Reference

| Pattern | Use When |
|---|---|
| List comprehension | Transform/filter sequences |
| Generator expression | Large data, single iteration |
| `yield from` | Delegate to sub-generator |
| `@contextmanager` | Simple setup/teardown |
| `@dataclass(frozen=True)` | Immutable data containers |
| `:=` walrus | Assign + test in one expression |
| `*args` unpacking | Variable positional args |
| `**kwargs` unpacking | Variable keyword args |
