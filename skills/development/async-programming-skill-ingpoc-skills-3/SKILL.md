---
name: async-programming-skill
description: This skill provides async/await patterns and best practices for concurrent programming
---

# Async Programming

## Purpose

Async/await enables non-blocking concurrent operations. This skill documents patterns for safe async code.

## When to Use

Use this skill when:
- Working with I/O operations
- Building concurrent systems
- Managing timeouts
- Implementing cancellation

## Key Patterns

### 1. All I/O is Async

Never use blocking I/O:

```python
# WRONG
with open(file) as f:
    data = json.load(f)

# CORRECT
async with aiofiles.open(file) as f:
    data = await f.read()
```

### 2. Timeout Protection

All async operations need timeouts:

```python
try:
    result = await asyncio.wait_for(operation(), timeout=30.0)
except asyncio.TimeoutError:
    # Handle timeout
```

### 3. Error Handling

Async operations need proper error handling:

```python
async def safe_operation():
    try:
        return await risky_operation()
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise TradingError(...) from e
```

## See Also

- Python asyncio: https://docs.python.org/3/library/asyncio.html
