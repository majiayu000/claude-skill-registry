---
name: python-3-13-patterns
version: "1.0"
description: >
  Modern Python 3.13 development patterns and syntax including async/await, pattern matching, and modern type annotations.
  PROACTIVELY activate for: (1) Writing new Python 3.13 modules, (2) Implementing async/concurrent operations,
  (3) Using structural pattern matching (match/case), (4) Creating decorators or context managers, (5) Working with generators.
  Triggers: "python patterns", "match case", "async await", "context manager", "decorator", "generator", "python 3.13"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: ["parallel_decomposition_strategies"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Python 3.13 Modern Patterns

## Core Principles

Python 3.13 represents the culmination of modern Python design. This skill covers essential patterns for writing clean, efficient, and maintainable Python code using the latest language features.

## Modern Type Annotations (Built-in Generics)

Python 3.9+ allows using built-in types for generic annotations. This is the **required** pattern for all new code:

```python
# ✅ REQUIRED: Use built-in types
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def merge_data(data1: dict[str, any], data2: dict[str, any]) -> dict[str, any]:
    return {**data1, **data2}

# ❌ FORBIDDEN: Legacy typing module imports
from typing import List, Dict  # Don't use these!
def process_items(items: List[str]) -> Dict[str, int]:  # Old style
    pass
```

## Union Types with | Operator

Use the pipe operator for union types. This is cleaner and more Pythonic:

```python
# ✅ REQUIRED: Use | for unions
def get_user(user_id: int) -> User | None:
    """Returns User or None if not found."""
    return db.query(User).get(user_id)

def process_value(value: str | int | float) -> str:
    """Handles multiple types."""
    return str(value)

# ✅ REQUIRED: None always comes last in unions
def find_item(query: str) -> Item | None:
    pass

# ❌ FORBIDDEN: Legacy Optional and Union
from typing import Optional, Union
def get_user(user_id: int) -> Optional[User]:  # Old style
    pass
def process_value(value: Union[str, int, float]) -> str:  # Old style
    pass
```

## Structural Pattern Matching (match/case)

Use match/case for complex conditional logic based on structure:

```python
# ✅ REQUIRED: Use match/case for complex conditionals
def handle_command(command: str) -> str:
    match command.split():
        case ["quit"]:
            return "Exiting..."
        case ["load", filename]:
            return f"Loading {filename}"
        case ["save", filename]:
            return f"Saving to {filename}"
        case ["set", key, value]:
            return f"Setting {key} = {value}"
        case _:
            return "Unknown command"

# Pattern matching with type checking
def process_message(message: dict) -> str:
    match message:
        case {"type": "user_created", "user_id": user_id, "email": email}:
            return f"Welcome user {user_id}: {email}"
        case {"type": "user_deleted", "user_id": user_id}:
            return f"User {user_id} deleted"
        case {"type": "error", "code": code, "message": msg}:
            raise ValueError(f"Error {code}: {msg}")
        case _:
            return "Unknown message type"

# Matching with guards
def categorize_number(n: int) -> str:
    match n:
        case 0:
            return "zero"
        case n if n < 0:
            return "negative"
        case n if n > 0 and n < 10:
            return "small positive"
        case n if n >= 10:
            return "large positive"
```

## Async/Await Patterns

Async functions are first-class citizens in Python 3.13:

```python
import asyncio

# ✅ REQUIRED: Comprehensive error handling in async functions
async def fetch_data(url: str) -> dict[str, any]:
    """Fetch data with proper error handling and resource cleanup."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.json()
        except asyncio.TimeoutError:
            raise TimeoutError(f"Request to {url} timed out")
        except aiohttp.ClientError as e:
            raise ConnectionError(f"Failed to fetch {url}: {e}")

# ✅ REQUIRED: Use asyncio.gather for concurrent operations
async def fetch_multiple(urls: list[str]) -> list[dict[str, any]]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

# ✅ REQUIRED: Use async context managers for resources
class AsyncDatabaseConnection:
    async def __aenter__(self):
        self.conn = await connect_to_db()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async def query_database():
    async with AsyncDatabaseConnection() as conn:
        return await conn.execute("SELECT * FROM users")
```

## Context Managers

Context managers ensure proper resource cleanup:

```python
from contextlib import contextmanager
from typing import Generator

# ✅ REQUIRED: Use context managers for resource management
@contextmanager
def open_file_safely(filename: str, mode: str = 'r') -> Generator[any, None, None]:
    """Context manager for file operations with error handling."""
    file = None
    try:
        file = open(filename, mode)
        yield file
    except IOError as e:
        print(f"Error opening {filename}: {e}")
        raise
    finally:
        if file:
            file.close()

# Class-based context manager
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.connection.begin_transaction()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        return False  # Don't suppress exceptions

# Usage
with DatabaseTransaction(conn) as db:
    db.execute("INSERT INTO users VALUES (...)")
```

## Decorators

Decorators are powerful for cross-cutting concerns:

```python
from functools import wraps
from typing import Callable, Any
import time

# ✅ REQUIRED: Preserve function metadata with @wraps
def timing_decorator(func: Callable) -> Callable:
    """Measure execution time of functions."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f}s")
        return result
    return wrapper

# Decorator with arguments (decorator factory)
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with configurable attempts and delay."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

# Usage
@retry(max_attempts=5, delay=2.0)
def fetch_api_data(url: str) -> dict:
    """Fetch data with automatic retries."""
    pass
```

## Generators

Generators enable memory-efficient data processing:

```python
from typing import Generator

# ✅ REQUIRED: Use generators for large datasets
def read_large_file(filename: str) -> Generator[str, None, None]:
    """Read file line by line without loading into memory."""
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

def process_data_stream(data: list[int]) -> Generator[int, None, None]:
    """Process data in chunks."""
    for item in data:
        if item > 0:
            yield item * 2

# Generator with send() for coroutine-like behavior
def running_average() -> Generator[float, float, None]:
    """Calculate running average of sent values."""
    total = 0.0
    count = 0
    while True:
        value = yield (total / count) if count > 0 else 0.0
        total += value
        count += 1

# Usage
avg = running_average()
next(avg)  # Prime the generator
print(avg.send(10))  # 10.0
print(avg.send(20))  # 15.0
print(avg.send(30))  # 20.0
```

## Anti-Patterns to Avoid

### Using Legacy typing Imports
```python
# BAD
from typing import List, Dict, Optional, Union
def func(items: List[str]) -> Dict[str, int]:
    pass

# GOOD
def func(items: list[str]) -> dict[str, int]:
    pass
```

### Implicit Any Return Types
```python
# BAD: Function implicitly returns Any
def process_data(data):
    return data.upper()

# GOOD: Explicit return type
def process_data(data: str) -> str:
    return data.upper()
```

### Using Any Instead of object
```python
# BAD: Any disables type checking
from typing import Any
def log_value(value: Any) -> None:
    print(str(value))

# GOOD: object is more precise
def log_value(value: object) -> None:
    print(str(value))
```

### Chained if/elif for Structured Data
```python
# BAD: Complex conditional logic
if isinstance(data, dict) and "type" in data:
    if data["type"] == "user_created":
        handle_user_created(data)
    elif data["type"] == "user_deleted":
        handle_user_deleted(data)

# GOOD: Use match/case
match data:
    case {"type": "user_created", **rest}:
        handle_user_created(data)
    case {"type": "user_deleted", **rest}:
        handle_user_deleted(data)
```

### Not Using Context Managers for Resources
```python
# BAD: Manual resource management
file = open('data.txt', 'r')
try:
    data = file.read()
finally:
    file.close()

# GOOD: Context manager
with open('data.txt', 'r') as file:
    data = file.read()
```

## When to Use This Skill

Activate this skill when:
- Writing new Python 3.13 modules
- Refactoring legacy Python code to modern patterns
- Implementing async/concurrent operations
- Using structural pattern matching (match/case)
- Creating decorators or context managers
- Working with generators for data processing
- Applying modern type annotations

## Related Resources

For additional advanced patterns, reference:
- Python 3.13 Official Documentation: https://docs.python.org/3/whatsnew/3.13.html
- Type Hints Best Practices: See `type-hints-best-practices` skill
- Async Patterns: See `async-patterns` skill
