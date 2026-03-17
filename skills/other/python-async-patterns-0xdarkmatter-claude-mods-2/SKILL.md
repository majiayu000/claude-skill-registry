---
name: python-async-patterns
description: "Python asyncio patterns for concurrent programming. Triggers on: asyncio, async, await, coroutine, gather, semaphore, TaskGroup, event loop, aiohttp, concurrent."
compatibility: "Python 3.10+ recommended. Some patterns require 3.11+ (TaskGroup, timeout)."
allowed-tools: "Read Write"
depends-on: [python-typing-patterns]
related-skills: [python-fastapi-patterns, python-observability-patterns]
---

# Python Async Patterns

Asyncio patterns for concurrent Python programming.

## Core Concepts

```python
import asyncio

# Coroutine (must be awaited)
async def fetch(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Entry point
async def main():
    result = await fetch("https://example.com")
    return result

asyncio.run(main())
```

## Pattern 1: Concurrent with gather

```python
async def fetch_all(urls: list[str]) -> list[str]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

## Pattern 2: Bounded Concurrency

```python
async def fetch_with_limit(urls: list[str], limit: int = 10):
    """Limit concurrent requests."""
    semaphore = asyncio.Semaphore(limit)

    async def bounded_fetch(url):
        async with semaphore:
            return await fetch_one(url)

    return await asyncio.gather(*[bounded_fetch(url) for url in urls])
```

## Pattern 3: TaskGroup (Python 3.11+)

```python
async def process_items(items):
    """Structured concurrency with automatic cleanup."""
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_one(item))
    # All tasks complete here, or exception raised
```

## Pattern 4: Timeout

```python
async def with_timeout():
    try:
        async with asyncio.timeout(5.0):  # Python 3.11+
            result = await slow_operation()
    except asyncio.TimeoutError:
        result = None
    return result
```

## Critical Warnings

```python
# WRONG - blocks event loop
async def bad():
    time.sleep(5)         # Never use time.sleep!
    requests.get(url)     # Blocking I/O!

# CORRECT
async def good():
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as s:
        await s.get(url)
```

```python
# WRONG - orphaned task
async def bad():
    asyncio.create_task(work())  # May be garbage collected!

# CORRECT - keep reference
async def good():
    task = asyncio.create_task(work())
    await task
```

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| `gather(*tasks)` | Multiple independent operations |
| `Semaphore(n)` | Rate limiting, resource constraints |
| `TaskGroup()` | Structured concurrency (3.11+) |
| `Queue()` | Producer-consumer |
| `timeout(s)` | Timeout wrapper (3.11+) |
| `Lock()` | Shared mutable state |

## Async Context Manager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_connection():
    conn = await create_connection()
    try:
        yield conn
    finally:
        await conn.close()
```

## Additional Resources

For detailed patterns, load:
- `./references/concurrency-patterns.md` - Queue, Lock, producer-consumer
- `./references/aiohttp-patterns.md` - HTTP client/server patterns
- `./references/mixing-sync-async.md` - run_in_executor, thread pools
- `./references/debugging-async.md` - Debug mode, profiling, finding issues
- `./references/production-patterns.md` - Graceful shutdown, health checks, signal handling
- `./references/error-handling.md` - Retry with backoff, circuit breakers, partial failures
- `./references/performance.md` - uvloop, connection pooling, buffer sizing

## Scripts

- `./scripts/find-blocking-calls.sh` - Scan code for blocking calls in async functions

## Assets

- `./assets/async-project-template.py` - Production-ready async app skeleton

---

## See Also

**Prerequisites:**
- `python-typing-patterns` - Type hints for async functions

**Related Skills:**
- `python-fastapi-patterns` - Async web APIs
- `python-observability-patterns` - Async logging and tracing
- `python-database-patterns` - Async database access
