---
name: docstring-conventions
description: Google-style docstring conventions for Python code. Apply when writing functions, classes, or modules that need documentation.
user-invocable: false
---

# Docstring Conventions

Apply Google-style docstrings when writing Python code in this repository.

## Required Docstrings

| Element | Format |
|---------|---------------------|--------|
| Public functions | Comprehensive (Args, Returns, Raises, Example) |
| Public classes | Comprehensive (Attributes, Example) |
| Public methods | Comprehensive (Args, Returns, Raises) |
| Modules | Summary + extended description |
| Private functions (`_name`) | One-liner OK |
| Private methods (`_name`) | One-liner OK |

### Private Helper Docstrings

Private functions and methods require docstrings, but one-liners are acceptable:

```python
# CORRECT - one-liner for private helper
def _normalize_vector(vec: list[float]) -> list[float]:
    """Normalize vector to unit length."""
    magnitude = sum(x**2 for x in vec) ** 0.5
    return [x / magnitude for x in vec]

# CORRECT - comprehensive if complex private function
def _parse_nested_config(raw: dict[str, Any]) -> Config:
    """Parse nested configuration with inheritance resolution.

    Args:
        raw (dict[str, Any]): Raw config dictionary with potential $ref keys.

    Returns:
        Config: Resolved configuration object.
    """
    ...

# INCORRECT - no docstring on private function
def _normalize_vector(vec: list[float]) -> list[float]:
    magnitude = sum(x**2 for x in vec) ** 0.5
    return [x / magnitude for x in vec]
```

## Function Docstring Structure

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """One-line summary of what the function does.

    Extended description explaining WHY this function exists and WHEN to use it.
    Do not explain HOW it works (the code shows that).

    Args:
        param1 (Type1): Description of first parameter.
        param2 (Type2): Description of second parameter.

    Returns:
        ReturnType: Description of return value.

    Raises:
        ExceptionType: When this exception is raised.

    Examples:
        >>> function_name(value1, value2)
        expected_output
    """
```

### Section Rules

| Section | When to include |
|---------|-----------------|
| One-line summary | **Always** - first line, ends with period |
| Extended description | When the summary isn't enough to explain purpose |
| Args | **Always** if function has parameters |
| Returns | **Always** if function returns a value (not `None`) |
| Raises | **Always** if function raises exceptions |
| Examples | When usage isn't obvious from signature |

### Complete Example

```python
def calculate_similarity(embedding_a: list[float], embedding_b: list[float]) -> float:
    """Calculate cosine similarity between two embeddings.

    Use this for comparing semantic similarity of text chunks when building
    retrieval systems. Values closer to 1.0 indicate higher similarity.

    Args:
        embedding_a (list[float]): First embedding vector.
        embedding_b (list[float]): Second embedding vector.

    Returns:
        float: Cosine similarity score between -1.0 and 1.0.

    Raises:
        ValueError: If vectors have different dimensions.

    Examples:
        >>> calculate_similarity([1.0, 0.0], [1.0, 0.0])
        1.0
    """
```

## Class Docstring Structure

```python
class ClassName:
    """One-line summary of what the class represents.

    Extended description of the class purpose and when to use it.

    Attributes:
        attr1 (Type1): Description of public attribute.
        attr2 (Type2): Description of public attribute.

    Examples:
        >>> obj = ClassName(param)
        >>> obj.method()
        expected_output
    """

    def __init__(self, param: Type) -> None:
        """Initialize the class.

        Args:
            param (Type): Description of parameter.
        """
```

## Module Docstring Structure

Every module file must start with a docstring:

```python
"""One-line summary of module purpose.

Extended description of what the module provides and when to use it.
"""

import ...
```

### Example

```python
"""Embedding utilities for vector similarity search.

This module provides functions for creating, comparing, and manipulating
embeddings used in semantic search and retrieval systems.
"""

from typing import Final
...
```

## Docstrings vs Comments

| Use | For |
|-----|-----|
| Docstrings | Public API documentation - what and why |
| Comments | Non-obvious implementation details - why this approach |

### When to Use Comments

Add comments only when the **why** isn't obvious:

```python
# CORRECT - explains why this approach was chosen
# Use binary search here because the list is sorted and can have 100k+ items
index = bisect.bisect_left(sorted_items, target)

# CORRECT - explains a non-obvious constraint
# Must check expiry before validation because expired tokens fail silently
if token.is_expired():
    raise TokenExpiredError()

# INCORRECT - explains what (the code already shows this)
# Get the index using binary search
index = bisect.bisect_left(sorted_items, target)

# INCORRECT - obvious from the code
# Increment the counter
counter += 1
```

## Forbidden Patterns

```python
# INCORRECT - no docstring on public function
def fetch_user(user_id: int) -> User:
    return db.query(User).get(user_id)

# INCORRECT - no docstring on private function
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# INCORRECT - docstring explains "how" instead of "why"
def fetch_user(user_id: int) -> User:
    """Query the database for a user by ID and return the User object."""
    return db.query(User).get(user_id)

# INCORRECT - missing Args/Returns sections
def fetch_user(user_id: int) -> User:
    """Fetch a user from the database."""
    return db.query(User).get(user_id)
```

## Doctest Examples

When including examples, make them runnable with doctest:

```python
def add_vectors(a: list[float], b: list[float]) -> list[float]:
    """Add two vectors element-wise.

    Args:
        a (list[float]): First vector.
        b (list[float]): Second vector.

    Returns:
        list[float]: Element-wise sum.

    Examples:
        >>> add_vectors([1.0, 2.0], [3.0, 4.0])
        [4.0, 6.0]
        >>> add_vectors([0.0], [0.0])
        [0.0]
    """
```

## Validation Commands

| Check | Command |
|-------|---------|
| Docstring style/completeness | `uv tool run pydoclint --style=google --allow-init-docstring=True <path>` |
| Doctest examples | `uv run pytest --doctest-modules` |
