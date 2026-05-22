---
name: asyncio-advanced
description: Python asyncio patterns with TaskGroup, structured concurrency, and modern 3.11+ features. Use when implementing concurrent operations, async context managers, or high-performance async services.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [asyncio, python, concurrency, taskgroup, structured-concurrency, 2026]
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
author: SkillForge
user-invocable: false
---

# Asyncio Advanced Patterns (2026)

Modern Python asyncio patterns using structured concurrency, TaskGroup, and Python 3.11+ features.

## Overview

- Implementing concurrent HTTP requests or database queries
- Building async services with proper cancellation handling
- Managing multiple concurrent tasks with error propagation
- Rate limiting async operations with semaphores
- Bridging sync code to async contexts

## Quick Reference

### TaskGroup (Replaces gather)

```python
import asyncio

async def fetch_user_data(user_id: str) -> dict:
    """Fetch user data concurrently - all tasks complete or all cancelled."""
    async with asyncio.TaskGroup() as tg:
        user_task = tg.create_task(fetch_user(user_id))
        orders_task = tg.create_task(fetch_orders(user_id))
        preferences_task = tg.create_task(fetch_preferences(user_id))

    # All tasks guaranteed complete here
    return {
        "user": user_task.result(),
        "orders": orders_task.result(),
        "preferences": preferences_task.result(),
    }
```

### TaskGroup with Timeout

```python
async def fetch_with_timeout(urls: list[str], timeout_sec: float = 30) -> list[dict]:
    """Fetch all URLs with overall timeout - structured concurrency."""
    results = []

    async with asyncio.timeout(timeout_sec):
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(fetch_url(url)) for url in urls]

    return [t.result() for t in tasks]
```

### Semaphore for Concurrency Limiting

```python
class RateLimitedClient:
    """HTTP client with concurrency limiting."""

    def __init__(self, max_concurrent: int = 10):
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._session: aiohttp.ClientSession | None = None

    async def fetch(self, url: str) -> dict:
        async with self._semaphore:  # Limit concurrent requests
            async with self._session.get(url) as response:
                return await response.json()

    async def fetch_many(self, urls: list[str]) -> list[dict]:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self.fetch(url)) for url in urls]
        return [t.result() for t in tasks]
```

### Exception Group Handling

```python
async def process_batch(items: list[dict]) -> tuple[list[dict], list[Exception]]:
    """Process batch, collecting both successes and failures."""
    results = []
    errors = []

    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(process_item(item)) for item in items]
    except* ValueError as eg:
        # Handle specific exception types from ExceptionGroup
        errors.extend(eg.exceptions)
    except* Exception as eg:
        errors.extend(eg.exceptions)
    else:
        results = [t.result() for t in tasks]

    return results, errors
```

### Sync-to-Async Bridge

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

# For CPU-bound or blocking sync code
async def run_blocking_operation(data: bytes) -> dict:
    """Run blocking sync code in thread pool."""
    return await asyncio.to_thread(cpu_intensive_parse, data)

# For sync code that needs async context
def sync_caller():
    """Call async code from sync context (not in existing loop)."""
    return asyncio.run(async_main())

# For sync code within existing async context
async def wrapper_for_sync_lib():
    """Bridge sync library to async - use with care."""
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, sync_blocking_call)
    return result
```

### Cancellation Handling

```python
async def cancellable_operation(resource_id: str) -> dict:
    """Properly handle cancellation - NEVER swallow CancelledError."""
    resource = await acquire_resource(resource_id)
    try:
        return await process_resource(resource)
    except asyncio.CancelledError:
        # Clean up but RE-RAISE - this is critical!
        await cleanup_resource(resource)
        raise  # ALWAYS re-raise CancelledError
    finally:
        await release_resource(resource)
```

## Key Decisions

| Decision | 2026 Recommendation | Rationale |
|----------|---------------------|-----------|
| Task spawning | `TaskGroup` not `gather()` | Structured concurrency, auto-cancellation |
| Timeouts | `asyncio.timeout()` context manager | Composable, cancels on exit |
| Concurrency limit | `asyncio.Semaphore` | Prevents resource exhaustion |
| Sync bridge | `asyncio.to_thread()` | Clean API, manages thread pool |
| Exception handling | `except*` with ExceptionGroup | Handle multiple failures properly |
| Cancellation | Always re-raise `CancelledError` | Breaking this breaks TaskGroup/timeout |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER use gather() for new code - no structured concurrency
results = await asyncio.gather(task1(), task2())  # LEGACY

# NEVER swallow CancelledError - breaks structured concurrency
except asyncio.CancelledError:
    return None  # BREAKS TaskGroup and timeout!

# NEVER use create_task() without TaskGroup - tasks leak
asyncio.create_task(background_work())  # Fire and forget = leaked task

# NEVER yield inside async context managers (PEP 789)
async with asyncio.timeout(10):
    yield item  # DANGEROUS - cancellation bugs!

# NEVER use asyncio.run() inside existing event loop
async def handler():
    asyncio.run(other_async())  # CRASHES - loop already running

# NEVER block the event loop with sync calls
async def bad_handler():
    time.sleep(1)  # BLOCKS ALL TASKS
    requests.get(url)  # BLOCKS ALL TASKS
```

## Related Skills

- `sqlalchemy-2-async` - Async database sessions with SQLAlchemy 2.0
- `fastapi-advanced` - Async FastAPI patterns
- `background-jobs` - Celery/ARQ for heavy async work
- `streaming-api-patterns` - SSE/WebSocket async patterns

## Capability Details

### taskgroup-patterns
**Keywords:** taskgroup, structured concurrency, concurrent tasks, parallel execution
**Solves:**
- How do I run multiple async tasks concurrently?
- Replace asyncio.gather with TaskGroup
- Handle exceptions from multiple tasks

### timeout-patterns
**Keywords:** timeout, asyncio.timeout, cancel, deadline
**Solves:**
- How do I add timeouts to async operations?
- Timeout multiple concurrent operations
- Cancel tasks after deadline

### semaphore-limiting
**Keywords:** semaphore, rate limit, concurrency limit, throttle
**Solves:**
- How do I limit concurrent async operations?
- Rate limit HTTP requests
- Prevent connection pool exhaustion

### exception-groups
**Keywords:** ExceptionGroup, except*, multiple exceptions, error handling
**Solves:**
- How do I handle multiple task failures?
- Collect errors from concurrent operations
- Python 3.11+ exception group patterns

### sync-async-bridge
**Keywords:** to_thread, run_in_executor, sync to async, blocking code
**Solves:**
- How do I call sync code from async?
- Run CPU-bound code without blocking
- Bridge sync libraries to async context
