---
name: complexity-refactoring
description: Refactoring complex functions into smaller, pure helper functions. Apply when McCabe complexity is exceeded or when extracting helper functions during refactoring.
user-invocable: false
---

# Refactoring Complex Functions

When a function exceeds McCabe complexity limits (C901), extract helper functions that are **pure** and **return values**.

## Quick Reference

| Principle | Pattern |
|-----------|---------|
| Pure helpers | Extract functions that return values, never mutate inputs |
| No void mutators | NEVER create helpers that modify a collection and return `None` |
| Transform, don't mutate | `result = transform(data)` not `mutate(data)` |
| Comprehensions first | Prefer comprehensions over loops when building collections |
| Single return value | Each helper computes and returns one thing |

---

## The Anti-Pattern: Void Mutator Functions

**NEVER** create helper functions that mutate a collection passed as an argument.

```python
# INCORRECT - void mutator anti-pattern
def _add_user_fields(result: dict[str, Any], user: User) -> None:
    """Mutates result dict - THIS IS WRONG."""
    result["name"] = user.name
    result["email"] = user.email
    result["role"] = user.role

def _add_metadata(result: dict[str, Any], metadata: Metadata) -> None:
    """Mutates result dict - THIS IS WRONG."""
    result["created_at"] = metadata.created_at
    result["version"] = metadata.version

def build_response(user: User, metadata: Metadata) -> dict[str, Any]:
    result: dict[str, Any] = {}
    _add_user_fields(result, user)  # Side effect
    _add_metadata(result, metadata)  # Side effect
    return result
```

**Why this is wrong:**
- Hidden side effects make code harder to reason about
- Can't compose or test helpers in isolation
- Violates command-query separation
- Makes the data flow invisible

---

## The Correct Pattern: Pure Helpers That Return Values

```python
# CORRECT - pure functions that return values
def _build_user_fields(user: User) -> dict[str, Any]:
    """Return user fields as a dict."""
    return {
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }

def _build_metadata_fields(metadata: Metadata) -> dict[str, Any]:
    """Return metadata fields as a dict."""
    return {
        "created_at": metadata.created_at,
        "version": metadata.version,
    }

def build_response(user: User, metadata: Metadata) -> dict[str, Any]:
    return {
        **_build_user_fields(user),
        **_build_metadata_fields(metadata),
    }
```

---

## Refactoring Patterns

### Pattern 1: Extract Computation

When a function has complex logic that computes a value, extract it.

```python
# BEFORE - complex inline computation
def process_order(order: Order) -> Summary:
    # ... lots of code ...
    total = 0
    for item in order.items:
        price = item.unit_price * item.quantity
        if item.discount:
            price *= (1 - item.discount)
        if order.member:
            price *= 0.9
        total += price
    # ... more code ...

# AFTER - extracted pure helper
def _calculate_item_price(item: OrderItem, is_member: bool) -> Decimal:
    """Calculate final price for a single item."""
    price = item.unit_price * item.quantity
    if item.discount:
        price *= (1 - item.discount)
    if is_member:
        price *= Decimal("0.9")
    return price

def _calculate_order_total(order: Order) -> Decimal:
    """Calculate total price for all items."""
    return sum(
        _calculate_item_price(item, order.member)
        for item in order.items
    )

def process_order(order: Order) -> Summary:
    # ... lots of code ...
    total = _calculate_order_total(order)
    # ... more code ...
```

### Pattern 2: Extract Collection Building

When building a list or dict, extract the transformation logic.

```python
# INCORRECT - void mutator for list building
def _add_valid_items(results: list[Item], items: list[Item]) -> None:
    for item in items:
        if item.is_valid and item.score > 0.5:
            results.append(item)

# CORRECT - return the filtered list
def _filter_valid_items(items: list[Item]) -> list[Item]:
    """Return items that are valid with score > 0.5."""
    return [item for item in items if item.is_valid and item.score > 0.5]

# Even better - use comprehension inline if simple enough
valid_items = [item for item in items if item.is_valid and item.score > 0.5]
```

### Pattern 3: Extract Conditional Logic

When a function has complex branching, extract the decision or transformation.

```python
# BEFORE - complex conditional
def format_value(value: Any, config: Config) -> str:
    if isinstance(value, datetime):
        if config.use_iso:
            return value.isoformat()
        else:
            return value.strftime(config.date_format)
    elif isinstance(value, Decimal):
        if config.currency:
            return f"${value:.2f}"
        else:
            return str(value)
    # ... more cases ...

# AFTER - extracted formatters
def _format_datetime(value: datetime, config: Config) -> str:
    """Format datetime according to config."""
    if config.use_iso:
        return value.isoformat()
    return value.strftime(config.date_format)

def _format_decimal(value: Decimal, config: Config) -> str:
    """Format decimal according to config."""
    if config.currency:
        return f"${value:.2f}"
    return str(value)

def format_value(value: Any, config: Config) -> str:
    if isinstance(value, datetime):
        return _format_datetime(value, config)
    if isinstance(value, Decimal):
        return _format_decimal(value, config)
    # ... more cases ...
```

### Pattern 4: Extract Validation

When validation logic is complex, extract validators that return results.

```python
# INCORRECT - validation that mutates error list
def _validate_email(user: User, errors: list[str]) -> None:
    if not user.email:
        errors.append("Email is required")
    elif "@" not in user.email:
        errors.append("Invalid email format")

# CORRECT - validation that returns errors
def _validate_email(email: str | None) -> list[str]:
    """Return list of validation errors for email (empty if valid)."""
    if not email:
        return ["Email is required"]
    if "@" not in email:
        return ["Invalid email format"]
    return []

def validate_user(user: User) -> list[str]:
    """Return all validation errors for user."""
    return [
        *_validate_email(user.email),
        *_validate_name(user.name),
        *_validate_role(user.role),
    ]
```

---

## Checklist When Extracting Helpers

Before creating a helper function during refactoring, verify:

- [ ] Does it **return a value**? (Not `None` with side effects)
- [ ] Does it **avoid mutating** any input parameters?
- [ ] Can it be **tested in isolation** without setup?
- [ ] Does it have a **single responsibility**?
- [ ] Is the **data flow visible** at the call site?

If any answer is "no", redesign the helper.

---

## Validation

Check complexity after refactoring:

```bash
ruff check --select C901 <file>
```

The refactored code should have no functions exceeding McCabe complexity of 5.
