---
name: type-safety
description: Automatically applies when writing Python code to enforce comprehensive type hints. Ensures mypy compatibility, proper generic types, and type safety best practices.
---

# Type Safety Pattern Enforcer

All Python code should include comprehensive type hints for better IDE support, documentation, and error catching. This skill enforces type safety best practices and mypy compatibility.

## ✅ Correct Pattern

```python
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic
from collections.abc import Callable, Iterable


def process_transaction(
    amount: Decimal,
    user_id: str,
    metadata: Optional[Dict[str, Any]] = None
) -> TransactionResult:
    """Process a transaction with validation."""
    if metadata is None:
        metadata = {}

    # Process transaction
    return TransactionResult(
        transaction_id="txn_123",
        amount=amount,
        status="completed"
    )


class PaymentService:
    """Service for handling payments."""

    api_key: str
    base_url: str
    timeout: int = 30

    def __init__(self, api_key: str, base_url: str, timeout: int = 30) -> None:
        """Initialize payment service."""
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout


async def fetch_user_data(user_id: str) -> UserData:
    """Fetch user data asynchronously."""
    # Fetch and return user data
    pass
```

## Function Type Hints

```python
# Basic function
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


# Multiple return types
def get_user(user_id: str) -> Optional[User]:
    """Get user by ID, None if not found."""
    pass


# No return value
def log_event(event: str) -> None:
    """Log an event."""
    print(event)


# Variable arguments
def concatenate(*args: str) -> str:
    """Concatenate strings."""
    return "".join(args)


# Keyword arguments
def create_user(**kwargs: Any) -> User:
    """Create user from keyword arguments."""
    pass


# Callable type
def apply_operation(
    value: int,
    operation: Callable[[int], int]
) -> int:
    """Apply operation to value."""
    return operation(value)


# Union types (Python 3.10+)
def process(value: int | str) -> str:
    """Process int or string."""
    return str(value)


# Union types (pre-3.10)
def process_legacy(value: Union[int, str]) -> str:
    """Process int or string."""
    return str(value)
```

## Class Type Hints

```python
from typing import ClassVar


class User:
    """User with type-hinted attributes."""

    # Instance attributes
    id: str
    name: str
    email: str
    age: Optional[int] = None

    # Class variable
    default_role: ClassVar[str] = "user"

    def __init__(self, id: str, name: str, email: str) -> None:
        """Initialize user."""
        self.id = id
        self.name = name
        self.email = email

    def get_display_name(self) -> str:
        """Get display name."""
        return self.name

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create user from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"]
        )

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        return "@" in email
```

## Generic Types

```python
from typing import TypeVar, Generic, List, Dict

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


class Container(Generic[T]):
    """Generic container for any type."""

    def __init__(self, item: T) -> None:
        """Initialize with item."""
        self.item = item

    def get(self) -> T:
        """Get the item."""
        return self.item

    def set(self, item: T) -> None:
        """Set the item."""
        self.item = item


class Cache(Generic[K, V]):
    """Generic key-value cache."""

    def __init__(self) -> None:
        """Initialize cache."""
        self._data: Dict[K, V] = {}

    def get(self, key: K) -> Optional[V]:
        """Get value by key."""
        return self._data.get(key)

    def set(self, key: K, value: V) -> None:
        """Set key-value pair."""
        self._data[key] = value


# Usage
int_container: Container[int] = Container(42)
str_cache: Cache[str, User] = Cache()
```

## Collection Type Hints

```python
# Modern syntax (Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    """Process list of strings."""
    return {item: len(item) for item in items}


def aggregate(data: set[int]) -> tuple[int, int]:
    """Get min and max from set."""
    return (min(data), max(data))


# Legacy syntax (pre-3.9)
from typing import List, Dict, Set, Tuple


def process_items_legacy(items: List[str]) -> Dict[str, int]:
    """Process list of strings."""
    return {item: len(item) for item in items}


# Nested collections
def group_users(users: List[User]) -> Dict[str, List[User]]:
    """Group users by role."""
    pass


# Complex types
from typing import Mapping, Sequence, Iterable


def process_mapping(data: Mapping[str, Any]) -> Sequence[str]:
    """Process read-only mapping."""
    pass


def process_iterable(items: Iterable[int]) -> list[int]:
    """Process any iterable."""
    return list(items)
```

## Optional and None

```python
# Optional (can be None)
def get_user(user_id: str) -> Optional[User]:
    """Get user, None if not found."""
    pass


# Explicit None checking
def process_user(user: Optional[User]) -> str:
    """Process user with None check."""
    if user is None:
        return "No user"
    return user.name


# Default None parameter
def create_report(
    title: str,
    author: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Report:
    """Create report with optional fields."""
    if tags is None:
        tags = []
    return Report(title=title, author=author, tags=tags)
```

## Async Type Hints

```python
import asyncio
from typing import AsyncIterator


async def fetch_data(url: str) -> Dict[str, Any]:
    """Fetch data asynchronously."""
    pass


async def fetch_all(urls: List[str]) -> List[Dict[str, Any]]:
    """Fetch multiple URLs."""
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)


async def stream_data() -> AsyncIterator[str]:
    """Stream data asynchronously."""
    for i in range(10):
        await asyncio.sleep(0.1)
        yield f"item-{i}"


# Usage
async def main() -> None:
    """Main async function."""
    data = await fetch_data("https://example.com")
    async for item in stream_data():
        print(item)
```

## Type Narrowing

```python
from typing import Union


def process_value(value: Union[int, str, None]) -> str:
    """Process value with type narrowing."""
    if value is None:
        return "none"
    elif isinstance(value, int):
        # Type narrowed to int
        return f"int: {value * 2}"
    elif isinstance(value, str):
        # Type narrowed to str
        return f"str: {value.upper()}"
    else:
        # This should never happen with proper types
        raise TypeError(f"Unexpected type: {type(value)}")


def process_user(user: Optional[User]) -> str:
    """Process user with None check."""
    if user is None:
        return "No user"
    # Type narrowed to User (not None)
    return user.name
```

## Type Aliases

```python
from typing import TypeAlias, NewType

# Type alias (simple)
UserId: TypeAlias = str
Email: TypeAlias = str
Metadata: TypeAlias = Dict[str, Any]


def get_user(user_id: UserId) -> User:
    """Get user by ID."""
    pass


def send_email(email: Email, subject: str) -> None:
    """Send email."""
    pass


# NewType (distinct type)
UserId = NewType('UserId', str)
ProductId = NewType('ProductId', str)


def get_user(user_id: UserId) -> User:
    """Get user by ID."""
    pass


# These are type-safe
user_id: UserId = UserId("usr_123")
product_id: ProductId = ProductId("prd_456")

# This would be a mypy error:
# get_user(product_id)  # Error: Expected UserId, got ProductId
```

## Protocol Types

```python
from typing import Protocol


class Drawable(Protocol):
    """Protocol for drawable objects."""

    def draw(self) -> None:
        """Draw the object."""
        ...


class Circle:
    """Circle class."""

    def draw(self) -> None:
        """Draw circle."""
        print("Drawing circle")


class Square:
    """Square class."""

    def draw(self) -> None:
        """Draw square."""
        print("Drawing square")


def render(shape: Drawable) -> None:
    """Render any drawable shape."""
    shape.draw()


# Both work with structural typing
render(Circle())
render(Square())
```

## Literal Types

```python
from typing import Literal


def set_status(status: Literal["active", "inactive", "suspended"]) -> None:
    """Set status to specific values only."""
    pass


# Valid
set_status("active")

# Invalid (mypy error)
# set_status("unknown")


def process_mode(mode: Literal["read", "write", "append"]) -> None:
    """Process with specific mode."""
    if mode == "read":
        pass
    elif mode == "write":
        pass
    elif mode == "append":
        pass
```

## Type Guards

```python
from typing import TypeGuard


def is_string_list(val: List[Any]) -> TypeGuard[List[str]]:
    """Check if list contains only strings."""
    return all(isinstance(item, str) for item in val)


def process_strings(items: List[Any]) -> None:
    """Process list if all items are strings."""
    if is_string_list(items):
        # Type narrowed to List[str]
        for item in items:
            print(item.upper())  # Safe, item is str
```

## ❌ Anti-Patterns

```python
# ❌ No type hints
def process_data(data):  # Missing all type hints
    return data


# ✅ Better
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return data


# ❌ Using Any everywhere
def process(data: Any) -> Any:  # Too generic
    pass


# ✅ Better: specific types
def process(data: Dict[str, str]) -> List[str]:
    pass


# ❌ Mutable default arguments
def add_item(item: str, items: List[str] = []) -> List[str]:
    items.append(item)
    return items


# ✅ Better: use None and create new list
def add_item(item: str, items: Optional[List[str]] = None) -> List[str]:
    if items is None:
        items = []
    items.append(item)
    return items


# ❌ Not using Optional
def get_user(user_id: str) -> User:  # Can return None!
    return None  # Type error


# ✅ Better
def get_user(user_id: str) -> Optional[User]:
    return None  # Correct


# ❌ Wrong collection types (pre-3.9)
def process(items: list) -> dict:  # Should use List, Dict
    pass


# ✅ Better
from typing import List, Dict


def process(items: List[str]) -> Dict[str, int]:
    pass
```

## Best Practices Checklist

- ✅ All public functions have type hints
- ✅ All class attributes have type hints
- ✅ Use `Optional[T]` for values that can be None
- ✅ Use specific types instead of `Any` when possible
- ✅ Use modern syntax (`list[T]`) on Python 3.9+
- ✅ Use `Protocol` for structural typing
- ✅ Use `TypeAlias` for complex type expressions
- ✅ Use `Literal` for fixed string/int values
- ✅ Run mypy in strict mode
- ✅ Handle None cases explicitly
- ✅ Use type narrowing with isinstance checks
- ✅ Avoid mutable default arguments

## Mypy Configuration

Add to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
disallow_subclassing_any = true
disallow_untyped_calls = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
```

## Auto-Apply

When writing Python code:
1. Add type hints to all function parameters
2. Add return type hints to all functions
3. Use `Optional[T]` for nullable values
4. Use specific collection types
5. Run mypy to verify type safety
6. Fix any type errors

## References

For comprehensive examples, see:
- [Python Patterns Guide](../../../docs/python-patterns.md#type-safety)
- [Best Practices Guide](../../../docs/best-practices.md#type-safety)

## Related Skills

- pydantic-models - For runtime type validation
- docstring-format - For documenting types
- async-await-checker - For async type hints
