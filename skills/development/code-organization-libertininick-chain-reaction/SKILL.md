---
name: code-organization
description: Python code organization conventions for this codebase. Apply when structuring modules, organizing imports, and designing file layouts.
user-invocable: false
---

# Code Organization Conventions

Apply these organization patterns when writing Python code in this repository.

## Quick Reference

| Aspect | Pattern |
|--------|---------|
| File layout | Imports → Public interface → Private helpers |
| Module size | Split at ~800 lines or multiple responsibilities |
| Import order | stdlib → third-party → local |
| Import style | Absolute imports, no wildcards |
| Private members | Single `_` prefix |
| Cohesion | Group by feature/responsibility |
| Coupling | Depend on abstractions, not concretions |
| Dependencies | No circular imports |
| Responsibility | One purpose per function/class |

## Module Structure

**Pattern**: Public interface at top, private helpers below. Within each section,
group related classes and functions together and order them by logical flow. 

```python
# src/package/module/file.py

# Imports (organized by section)
...

# Public interface
class PublicClass:
    """Public API class."""
    ...

def public_function() -> ReturnType:
    """Public API function."""
    ...

# Private helpers
def _private_helper() -> ReturnType:
    """Internal implementation detail."""
    ...
```

### Module Size Rules

| Condition | Action |
|-----------|--------|
| File exceeds ~800 lines | Split into multiple modules |
| File has multiple unrelated responsibilities | Split by responsibility |
| Functions are tightly related | Keep in same module |

## Import Organization

**Pattern**: Three sections in order, separated by blank lines (enforced by ruff)

```python
# 1. Standard library
import json
from collections.abc import Sequence
from pathlib import Path

# 2. Third-party packages
import numpy as np
from pydantic import BaseModel

# 3. Local application imports
from chain_reaction.core import Config
from chain_reaction.utils import validate_input
```

### Import Rules

| Rule | Correct | Incorrect |
|------|---------|-----------|
| Use absolute imports | `from chain_reaction.core import X` | `from .core import X` |
| No wildcard imports | `from module import func1, func2` | `from module import *` |
| Group related imports | `from typing import Final, TypeVar` | Separate lines for same module |

## Private Members

**Pattern**: Single underscore `_` prefix for internal implementation

| Element | Public | Private |
|---------|--------|---------|
| Functions | `validate_input()` | `_normalize_data()` |
| Methods | `process()` | `_internal_step()` |
| Attributes | `self.config` | `self._cache` |
| Module-level | `DEFAULT_CONFIG` | `_INTERNAL_STATE` |

```python
# CORRECT - clear public/private distinction
class DataProcessor:
    def __init__(self, config: Config) -> None:
        self.config = config           # Public attribute
        self._cache: dict[str, Any] = {}  # Private attribute

    def process(self, data: Data) -> Result:  # Public method
        normalized = self._normalize(data)
        return self._transform(normalized)

    def _normalize(self, data: Data) -> Data:  # Private method
        """Normalize input data."""
        ...

    def _transform(self, data: Data) -> Result:  # Private method
        """Transform normalized data to result."""
        ...
```

## Module Design Principles

### High Cohesion

Group code by feature or responsibility:

```python
# CORRECT - user module contains all user-related code
# src/chain_reaction/users/repository.py
def fetch_user_by_id(user_id: int) -> User: ...
def create_user(data: UserCreate) -> User: ...
def update_user(user_id: int, data: UserUpdate) -> User: ...

# INCORRECT - mixed responsibilities
# src/chain_reaction/database.py
def fetch_user_by_id(user_id: int) -> User: ...
def fetch_order_by_id(order_id: int) -> Order: ...
def create_user(data: UserCreate) -> User: ...
def create_order(data: OrderCreate) -> Order: ...
```

### Low Coupling

Changes to one module should not require changes to others:

```python
# CORRECT - module depends on abstraction
from chain_reaction.interfaces import Storage

def save_data(storage: Storage, data: Data) -> None:
    storage.write(data)

# INCORRECT - module depends on concrete implementation
from chain_reaction.s3 import S3Client

def save_data(data: Data) -> None:
    client = S3Client()
    client.upload(data)
```

### No Circular Dependencies

```python
# INCORRECT - circular import
# module_a.py
from module_b import func_b
def func_a(): return func_b()

# module_b.py
from module_a import func_a  # Circular!
def func_b(): return func_a()

# CORRECT - extract shared code to third module
# shared.py
def shared_func(): ...

# module_a.py
from shared import shared_func

# module_b.py
from shared import shared_func
```

### Single Responsibility

Each function/class should have one clear purpose:

```python
# CORRECT - single responsibility
def validate_email(email: str) -> bool:
    """Check if email format is valid."""
    ...

def send_email(to: str, subject: str, body: str) -> None:
    """Send an email to recipient."""
    ...

# INCORRECT - multiple responsibilities
def validate_and_send_email(email: str, subject: str, body: str) -> bool:
    """Validate email and send if valid."""
    ...
```

## DRY Without Tight Coupling

Follow DRY, but never create tight coupling just to avoid repetition:

```python
# CORRECT - acceptable duplication to avoid coupling
# orders/validation.py
def validate_order_amount(amount: Decimal) -> bool:
    return amount > 0 and amount < MAX_ORDER_AMOUNT

# payments/validation.py
def validate_payment_amount(amount: Decimal) -> bool:
    return amount > 0 and amount < MAX_PAYMENT_AMOUNT

# INCORRECT - forced coupling to avoid duplication
# shared/validation.py
def validate_amount(amount: Decimal, max_amount: Decimal) -> bool:
    return amount > 0 and amount < max_amount

# Now orders and payments both depend on shared module
```


