---
name: python-code-patterns
description: Python code style and type hinting patterns. Use when writing or reviewing Python code to ensure consistent, modern type annotations, clean code structure, and proper separation of concerns. Covers modern type hints, import organization, router-service separation, comment practices, and docstring conventions.
metadata:
  author: eder
  version: "1.2"
---

# Python Code Patterns

## Exception: Tests Directory

All these rules can be relaxed in the `tests/` directory. Go wild there - write whatever helps you test effectively.

## Type Hints

Use modern Python type hints (PEP 585):

**DO:**

```python
def process(items: list[str]) -> dict[str, int]:
    ...

data: list[dict[str, Any]] = []
```text

**DON'T:**

```python
from typing import List, Union, Optional

def process(items: List[str]) -> Dict[str, int]:
    ...

data: List[Dict[str, Any]] = []
```

Use lowercase built-in types: `list`, `dict`, `tuple`, `set`, `frozenset`, `type`, `bytes`

## Import Organization

**DO:**

```python
from typing import Any

def my_function(data: Any) -> None:
    ...
```text

**DON'T:**

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any

def my_function(data: Any) -> None:
    ...
```

- Never use TYPE_CHECKING guards
- Never use imports not at the top level (inside functions, classes, etc.)
- If you have circular imports, your code structure needs refactoring
- TYPE_CHECKING guards and late imports are code smells indicating poor architecture

## Type Checking

Avoid `# type: ignore` as much as possible:

- Only use as a last resort when there's a genuine limitation in type checking
- If you find yourself needing `# type: ignore` frequently, reconsider your type annotations
- Comment why it's needed when you must use it:

```python
result: int = some_complex_function()  # type: ignore  # external library has incorrect type stub
```text

## Comments

Don't add obvious/redundant comments:

**DON'T:**

```python
id: str  # id
name: str  # the name
count: int  # number of items

# loop through items
for item in items:
    # process the item
    process(item)
```

Comments should explain **why**, not **what**.

## Router-Service Separation

Keep routers free of business logic:

**DO:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    return await service.get_item(item_id)
```

**DON'T:**

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item
```

- Routers should only call service functions and return results
- Validation, checks, business logic belong in the service layer
- Services raise HTTPExceptions directly - let them bubble up through routers
- Services contain domain logic and return domain objects or primitives

**Service layer handles:**

- Input validation and sanitization
- Business rules and constraints
- Database operations and queries
- Error conditions and exceptions raising

**Router layer handles:**

- HTTP method routing
- Delegating to service functions
- Returning service results directly
- No business logic or validation

## Docstrings

Keep docstrings concise and focused:

**DON'T:**

```python
def process_data(data: list[str]) -> dict[str, int]:
    """
    Process data.
    
    Args:
        data: The data to process
        
    Returns:
        dict[str, int]: The processed data
    """
    ...
```text

**DO:**

```python
def process_data(data: list[str]) -> dict[str, int]:
    """
    Converts string data to word frequency counts, ignoring case and punctuation.
    """
    ...
```

- Type information already in signature - don't repeat it
- Only include non-obvious information
- Explain edge cases, constraints, algorithm choices, or complex behavior

## When to Apply

Apply these patterns whenever:

- Writing new Python code (outside tests/)
- Reviewing or refactoring existing Python code (outside tests/)
- Updating type annotations (outside tests/)
- Adding or modifying imports (outside tests/)
- Implementing API routers or service layer functions
