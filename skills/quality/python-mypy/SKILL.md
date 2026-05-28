---
name: python-mypy
description: Static type checking with Mypy for Python code quality. Use when writing or reviewing Python code to ensure type safety, catch bugs early, and maintain code quality through proper type annotations and Mypy configuration.
user-invocable: false
---

# Python Mypy Type Checking Skill

This skill automatically activates when writing Python code to ensure proper type annotations and compatibility with Mypy static type checking.

## Core Principles

- **Type Safety**: Catch type errors before runtime
- **Gradual Typing**: Start with critical paths, expand coverage over time
- **Strict Mode**: Enable strict checks for new code
- **CI Integration**: Run Mypy in continuous integration

## Type Annotation Patterns

### Function Signatures

```python
from typing import Optional
from collections.abc import Sequence

# Good: Complete type hints
def process_items(
    items: list[str],
    max_count: int | None = None,
    debug: bool = False,
) -> dict[str, int]:
    """Process items and return counts."""
    result: dict[str, int] = {}
    # Implementation
    return result

# Good: Generic types with TypeVar
from typing import TypeVar

T = TypeVar('T')

def first(items: Sequence[T]) -> T | None:
    """Get first item from sequence."""
    return items[0] if items else None
```

### Class Type Hints

```python
from typing import ClassVar
from dataclasses import dataclass

@dataclass
class User:
    """User model with type hints."""

    id: int
    name: str
    email: str | None = None
    active: bool = True

    # Class variable
    _registry: ClassVar[dict[int, 'User']] = {}

    def __post_init__(self) -> None:
        """Register user after initialization."""
        self._registry[self.id] = self
```

### Protocol for Structural Typing

```python
from typing import Protocol

class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> str:
        """Draw the object."""
        ...

def render(obj: Drawable) -> None:
    """Render any drawable object."""
    print(obj.draw())

# Any class with draw() method satisfies this
class Circle:
    def draw(self) -> str:
        return "○"

render(Circle())  # OK with Mypy
```

### TypedDict for Structured Dictionaries

```python
from typing import TypedDict, NotRequired

class UserDict(TypedDict):
    """Structured user dictionary."""
    id: int
    name: str
    email: NotRequired[str]  # Optional key (Python 3.11+)

def create_user(data: UserDict) -> None:
    """Create user from typed dictionary."""
    user_id: int = data["id"]  # Type-safe access
    # Mypy knows 'email' might not exist
```

## Mypy Configuration Best Practices

### Recommended mypy.ini

```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_any_generics = True
disallow_subclassing_any = True
disallow_untyped_calls = True
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True
show_error_codes = True
show_column_numbers = True

# Start strict, relax per-module if needed
[mypy-tests.*]
disallow_untyped_defs = False

[mypy-migrations.*]
ignore_errors = True

# Third-party without stubs
[mypy-some_library.*]
ignore_missing_imports = True
```

### pyproject.toml Configuration

```toml
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
show_error_codes = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[[tool.mypy.overrides]]
module = "migrations.*"
ignore_errors = true
```

## Common Mypy Checks

### Strict Optional Checking

```python
# Bad: Implicit Optional
def find_user(id: int) -> User:  # Mypy error if can return None
    return users.get(id)  # dict.get returns User | None

# Good: Explicit Optional
def find_user(id: int) -> User | None:
    return users.get(id)

# Good: Narrow type with assertion
def get_user(id: int) -> User:
    user = users.get(id)
    assert user is not None, f"User {id} not found"
    return user  # Mypy knows this is User, not None
```

### Type Narrowing

```python
def process(value: str | int) -> str:
    """Process value based on type."""
    if isinstance(value, str):
        # Mypy knows value is str here
        return value.upper()
    else:
        # Mypy knows value is int here
        return str(value * 2)
```

### Generics

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    """Type-safe stack."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)  # OK
int_stack.push("x")  # Mypy error!
```

## Type Checking Strategies

### Gradual Adoption

1. **Start with New Code**: Use strict mode for new modules
2. **Core Paths First**: Type-check critical business logic
3. **Expand Coverage**: Gradually increase `disallow_untyped_defs`
4. **Per-Module Configuration**: Use mypy overrides for legacy code

```ini
[mypy]
# Strict by default
disallow_untyped_defs = True

# Relax for legacy
[mypy-legacy.*]
disallow_untyped_defs = False
check_untyped_defs = True  # Still check what we can
```

### Type Ignores (Use Sparingly)

```python
# When third-party library lacks types
import untyped_library  # type: ignore[import-untyped]

# When dealing with dynamic code (rare)
def dynamic_call() -> Any:
    result = getattr(obj, method_name)()  # type: ignore[misc]
    return result
```

## Common Patterns

### Context Managers

```python
from typing import Generator
from contextlib import contextmanager

@contextmanager
def database_transaction() -> Generator[Connection, None, None]:
    """Type-safe context manager."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### Callable Types

```python
from collections.abc import Callable

def retry(
    func: Callable[[int], str],
    times: int = 3,
) -> str:
    """Retry a function that takes int and returns str."""
    for _ in range(times):
        try:
            return func(42)
        except Exception:
            continue
    raise RuntimeError("All retries failed")
```

### Overloads for Multiple Signatures

```python
from typing import overload

@overload
def parse(data: str) -> dict[str, str]: ...

@overload
def parse(data: bytes) -> dict[str, bytes]: ...

def parse(data: str | bytes) -> dict[str, str] | dict[str, bytes]:
    """Parse data with type-specific return."""
    if isinstance(data, str):
        return {"parsed": data}
    return {"parsed": data}
```

## Django Integration

### Model Type Hints

```python
from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

class Author(models.Model):
    name = models.CharField(max_length=100)

    if TYPE_CHECKING:
        books: RelatedManager['Book']

class Book(models.Model):
    title = models.CharField(max_length=200)
    author: models.ForeignKey[Author] = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
    )
```

### Django Mypy Plugin

```ini
[mypy]
plugins = mypy_django_plugin.main

[mypy.plugins.django-stubs]
django_settings_module = "myproject.settings"
```

## Running Mypy

### Basic Check

```bash
# Check all files
mypy .

# Check specific files/directories
mypy src/

# Show error codes
mypy --show-error-codes .

# Generate HTML report
mypy --html-report ./mypy-report .
```

### In CI/CD

```yaml
# .github/workflows/type-check.yml
- name: Type check with Mypy
  run: |
    pip install mypy
    mypy --strict src/
```

## Anti-Patterns to Avoid

### Don't Use `Any` Unnecessarily

```python
# Bad: Any hides all type errors
def process(data: Any) -> Any:
    return data.unknown_method()  # No error!

# Good: Use specific types
def process(data: dict[str, int]) -> list[int]:
    return list(data.values())
```

### Don't Ignore All Errors

```python
# Bad: Blanket ignore
x = dangerous_call()  # type: ignore

# Good: Specific ignore with reason
x = legacy_api_call()  # type: ignore[misc]  # TODO: Add types to legacy API
```

### Don't Mix str and bytes

```python
# Bad: Mypy will catch this
def process(data: str) -> None:
    encoded: bytes = data  # Error!

# Good: Explicit conversion
def process(data: str) -> None:
    encoded: bytes = data.encode('utf-8')
```

## Coverage Reporting

```bash
# Check type coverage
mypy --html-report ./coverage .

# Show coverage stats
mypy --any-exprs-report ./coverage .
```

## Integration with Other Tools

- **Pre-commit**: Run Mypy before commits
- **VS Code**: Use Pylance with type checking mode
- **Ruff**: Complement Mypy with Ruff for runtime checks

## Related Skills

| Skill | Purpose |
|-------|---------|
| `python-experts:python-style` | Python coding standards |
| `python-experts:python-code-review` | Code review guidelines |
| `python-experts:python-testing-expert` | Testing patterns |

## References

- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Python Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [TypedDict (PEP 589)](https://peps.python.org/pep-0589/)
- [Protocol (PEP 544)](https://peps.python.org/pep-0544/)
