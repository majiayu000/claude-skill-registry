---
name: function-design
description: Python function design conventions for this codebase. Apply when writing or reviewing functions including signatures, parameters, return types, and async patterns.
user-invocable: false
---

# Function Design Conventions

## Quick Reference

| Principle | Pattern |
|-----------|---------|
| Explicit dependencies | Pass as parameters, no global state |
| Single responsibility | One function = one task |
| Pure when possible | Return new values, don't mutate inputs |
| Guard clauses | Validate early, return/raise immediately |
| Stable return types | Same type regardless of input |
| Errors via exceptions | Reserve `None` for "not found" only |
| Command-query separation | Action OR data, not both |
| Keyword-only args | Use `*` for optional/multiple params |
| No mutable defaults | Use `None`, create inside function |
| Async prefix | `async_` for async functions |

---

## Core Principles

### Explicit Dependencies

```python
# INCORRECT - hidden dependency on global state
_current_user: User | None = None

def get_permissions() -> list[str]:
    return _current_user.permissions

# CORRECT - explicit dependency
def get_permissions(user: User) -> list[str]:
    return user.permissions
```

### Single Responsibility

```python
# INCORRECT - does two things
def validate_and_save_user(user: User) -> bool:
    if not user.email or "@" not in user.email:
        return False
    db.save(user)
    return True

# CORRECT - separate concerns
def is_valid_email(email: str) -> bool:
    return bool(email and "@" in email)

def save_user(user: User) -> None:
    if not is_valid_email(user.email):
        raise ValidationError("Invalid email address")
    db.save(user)
```

### Pure Functions When Possible

```python
# INCORRECT - modifies input
def normalize_scores(scores: list[float]) -> None:
    max_score = max(scores)
    for i in range(len(scores)):
        scores[i] /= max_score

# CORRECT - returns new value
def normalize_scores(scores: list[float]) -> list[float]:
    max_score = max(scores)
    return [s / max_score for s in scores]
```

### Guard Clauses (Return Early)

```python
# INCORRECT - deeply nested
def process_order(order: Order | None) -> Receipt:
    if order is not None:
        if order.items:
            if order.payment_verified:
                return generate_receipt(order)
            else:
                raise PaymentError("Payment not verified")
        else:
            raise ValidationError("Order has no items")
    else:
        raise ValidationError("Order is required")

# CORRECT - guard clauses
def process_order(order: Order | None) -> Receipt:
    if order is None:
        raise ValidationError("Order is required")
    if not order.items:
        raise ValidationError("Order has no items")
    if not order.payment_verified:
        raise PaymentError("Payment not verified")

    return generate_receipt(order)
```

### Return Type Stability

```python
# INCORRECT - inconsistent return types
def find_user(user_id: int) -> User | None | bool:
    if user_id < 0:
        return False
    user = db.get(user_id)
    return user

# CORRECT - consistent return type
def find_user(user_id: int) -> User:
    if user_id < 0:
        raise ValueError("user_id must be >=0; got {user_id}")
    return db.get(user_id)
```

### Exceptions Over None for Errors

```python
# INCORRECT - None conflates "not found" with "error"
def load_config(path: Path) -> Config | None:
    if not path.exists():
        return None
    try:
        return Config.from_file(path)
    except ParseError:
        return None

# CORRECT - exceptions for errors, None only for "not found"
def load_config(path: Path) -> Config:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    try:
        return Config.from_file(path)
    except ParseError as e:
        raise ConfigurationError(f"Invalid config format: {e}") from e
```

### Command-Query Separation

```python
# INCORRECT - does both
def get_next_id() -> int:
    global _counter
    _counter += 1      # Side effect (command)
    return _counter    # Returns value (query)

# CORRECT - separate command and query
class IdGenerator:
    def __init__(self) -> None:
        self._counter = 0

    def next(self) -> int:
        """Return the next ID (query only)."""
        return self._counter + 1

    def advance(self) -> None:
        """Increment the counter (command only)."""
        self._counter += 1

    def take(self) -> int:
        """Get next ID and advance. Clearly named to indicate both."""
        id = self.next()
        self.advance()
        return id
```

### Keep Functions Small and Focused

```python
# INCORRECT - too much happening
def process_document(doc: Document) -> ProcessedDocument:
    # Validate
    if not doc.content:
        raise ValueError("Empty document")
    if len(doc.content) > MAX_LENGTH:
        raise ValueError("Document too long")
    # Extract metadata
    title = doc.content.split("\n")[0]
    word_count = len(doc.content.split())
    # Transform content
    cleaned = doc.content.lower().strip()
    tokens = cleaned.split()
    # ... 50 more lines

# CORRECT - composed of focused functions
def process_document(doc: Document) -> ProcessedDocument:
    validate_document(doc)
    metadata = extract_metadata(doc)
    tokens = tokenize_content(doc.content)
    return ProcessedDocument(metadata=metadata, tokens=tokens)
```

---

## Parameter Guidelines

### Limit Positional Parameters

```python
# INCORRECT - too many positional parameters
def create_user(name: str, email: str, age: int, role: str, dept: str) -> User:
    ...

# CORRECT - group related parameters
@dataclass
class UserInput:
    name: str
    email: str
    age: int
    role: str
    department: str

def create_user(input: UserInput) -> User:
    ...
```

### Keyword-Only Arguments

Use `*` to force keyword arguments for optional parameters or functions with 3+ parameters.

```python
# CORRECT - keyword-only after *
def fetch_data(
    url: str,
    *,  # Everything after this must be keyword-only
    timeout: float = 30.0,
    retries: int = 3,
    headers: dict[str, str] | None = None,
) -> Response:
    ...

# Callers must be explicit
response = fetch_data("https://api.example.com", timeout=60.0, retries=5)
```

### No Mutable Default Arguments

```python
# INCORRECT - mutable default (shared across calls!)
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

add_item("a")  # Returns ["a"]
add_item("b")  # Returns ["a", "b"] - BUG!

# CORRECT - None default with internal creation
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items
```

---

## Async Functions

Prefix async functions with `async_` to make the async nature visible at call sites.

```python
# CORRECT - async prefix makes it clear
async def async_fetch_user(user_id: int) -> User:
    return await client.get(f"/users/{user_id}")

async def async_process_batch(items: list[Item]) -> list[Result]:
    return await asyncio.gather(*[async_process(item) for item in items])

# Usage is clear about async nature
user = await async_fetch_user(123)
```
