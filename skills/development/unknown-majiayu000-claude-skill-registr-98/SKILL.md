---
name: 'caching-utilities'
description: 'Guide for using caching utilities in speedy_utils, including memory, disk, and hybrid caching strategies for sync and async functions.'
---

# Caching Utilities Guide

This skill provides comprehensive guidance for using the caching utilities in `speedy_utils`.

## When to Use This Skill

Use this skill when you need to:
- Optimize performance by caching expensive function calls.
- Persist results across program runs using disk caching.
- Use memory caching for fast access within a single run.
- Handle caching for both synchronous and asynchronous functions.
- Use `imemoize` for persistent caching in interactive environments like Jupyter notebooks.

## Prerequisites

- `speedy_utils` installed in your environment.

## Core Capabilities

### Universal Memoization (`@memoize`)
- Supports `memory`, `disk`, and `both` (hybrid) caching backends.
- Works with both `sync` and `async` functions.
- Configurable LRU cache size for memory caching.
- Custom key generation strategies.

### Interactive Memoization (`@imemoize`)
- Designed for Jupyter notebooks and interactive sessions.
- Persists cache across module reloads (`%load`).
- Uses global memory cache.

### Object Identification (`identify`)
- Generates stable, content-based identifiers for arbitrary Python objects.
- Handles complex types like DataFrames, Pydantic models, and nested structures.

## Usage Examples

### Example 1: Basic Hybrid Caching
Cache results in both memory and disk.

```python
from speedy_utils import memoize
import time

@memoize(cache_type='both', size=128)
def expensive_func(x: int):
    time.sleep(1)
    return x * x
```

### Example 2: Async Disk Caching
Cache results of an async function to disk.

```python
from speedy_utils import memoize
import asyncio

@memoize(cache_type='disk', cache_dir='./my_cache')
async def fetch_data(url: str):
    # simulate network call
    await asyncio.sleep(1)
    return {"data": "content"}
```

### Example 3: Custom Key Function
Use a custom key function for complex arguments.

```python
from speedy_utils import memoize

def get_user_id(user):
    return user.id

@memoize(key=get_user_id)
def process_user(user):
    # ...
    pass
```

### Example 4: Interactive Caching (Notebooks)
Use `@imemoize` to keep cache even if you reload the cell/module.

```python
from speedy_utils import imemoize

@imemoize
def notebook_func(data):
    # ...
    return result
```

## Guidelines

1.  **Choose the Right Backend**:
    - Use `memory` for small, fast results needed frequently in one session.
    - Use `disk` for large results or to persist across runs.
    - Use `both` (default) for the best of both worlds.

2.  **Key Stability**:
    - Ensure arguments are stable (e.g., avoid using objects with changing internal state as keys unless you provide a custom `key` function).
    - `identify` handles most common types, but be careful with custom classes without `__repr__` or stable serialization.

3.  **Cache Directory**:
    - Default disk cache is `~/.cache/speedy_cache`.
    - Override `cache_dir` for project-specific caching.

4.  **Async Support**:
    - The decorators automatically detect `async` functions and handle `await` correctly.
    - Do not mix sync/async usage without proper `await`.

## Common Patterns

### Pattern: Ignoring `self`
By default, `ignore_self=True` is set. This means methods on different instances of the same class will share cache if other arguments are the same. Set `ignore_self=False` if the instance state matters.

```python
class Processor:
    def __init__(self, multiplier):
        self.multiplier = multiplier

    @memoize(ignore_self=False)
    def compute(self, x):
        return x * self.multiplier
```

## Limitations

- **Pickle Compatibility**: Disk caching relies on `pickle` (or JSON). Ensure return values are serializable.
- **Cache Invalidation**: There is no automatic TTL (Time To Live) or expiration. You must manually clear cache files if data becomes stale.
