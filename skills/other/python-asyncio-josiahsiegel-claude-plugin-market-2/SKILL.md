---
name: python-asyncio
description: Complete Python asyncio system. PROACTIVELY activate for: (1) async/await syntax, (2) asyncio.gather for concurrent execution, (3) TaskGroup (3.11+), (4) Semaphores for rate limiting, (5) Timeouts with asyncio.timeout, (6) Producer-consumer with Queue, (7) Async generators and context managers, (8) uvloop performance, (9) Common async gotchas. Provides: Concurrent patterns, I/O optimization, async libraries (aiohttp, httpx, asyncpg). Ensures correct async patterns without blocking.
---

## Quick Reference

| Function | Purpose | Code |
|----------|---------|------|
| `asyncio.run()` | Entry point | `asyncio.run(main())` |
| `asyncio.gather()` | Concurrent tasks | `await asyncio.gather(*tasks)` |
| `asyncio.create_task()` | Fire-and-await | `task = asyncio.create_task(coro)` |
| `asyncio.TaskGroup()` | Structured concurrency | `async with asyncio.TaskGroup() as tg:` |
| `asyncio.Semaphore()` | Rate limiting | `async with semaphore:` |
| `asyncio.timeout()` | Timeout (3.11+) | `async with asyncio.timeout(5.0):` |

| Pattern | Sequential | Concurrent |
|---------|------------|------------|
| Execution | `await a(); await b()` | `await gather(a(), b())` |
| Time | Sum of durations | Max of durations |

| Library | Use Case |
|---------|----------|
| `aiohttp` | HTTP client (most popular) |
| `httpx` | HTTP (sync + async) |
| `asyncpg` | PostgreSQL |
| `uvloop` | 2-4x faster event loop |

## When to Use This Skill

Use for **async/concurrent programming**:
- Network requests (HTTP, WebSockets)
- Database queries
- File I/O operations
- Multiple concurrent I/O operations
- FastAPI/Starlette async endpoints

**Related skills:**
- For FastAPI: see `python-fastapi`
- For type hints: see `python-type-hints`
- For gotchas: see `python-gotchas`

---

# Python Asyncio Complete Guide

## Overview

Asyncio is Python's built-in framework for writing concurrent code using async/await syntax. It's ideal for I/O-bound operations like network requests, file I/O, and database queries.

## When to Use Asyncio

### Good Use Cases
- Network requests (HTTP clients, WebSockets)
- Database queries
- File I/O operations
- Web servers (FastAPI, Starlette)
- Message queues
- Multiple concurrent I/O operations

### When NOT to Use
- CPU-bound tasks (use multiprocessing instead)
- Simple sequential scripts
- Legacy codebases without async support

## Core Concepts

### Basic Async/Await

```python
import asyncio

# Async function (coroutine)
async def fetch_data(url: str) -> dict:
    # Simulated async I/O
    await asyncio.sleep(1)
    return {"url": url, "data": "..."}

# Running a coroutine
async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

# Entry point
asyncio.run(main())
```

### Concurrent Execution with gather()

```python
import asyncio
import aiohttp

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    async with session.get(url) as response:
        return {"url": url, "status": response.status}

async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        # Run all requests concurrently
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Usage
urls = [
    "https://api.example.com/1",
    "https://api.example.com/2",
    "https://api.example.com/3",
]
results = asyncio.run(fetch_all(urls))
```

### TaskGroup (Python 3.11+)

```python
import asyncio

async def process_item(item: str) -> str:
    await asyncio.sleep(1)
    return f"Processed: {item}"

async def process_all(items: list[str]) -> list[str]:
    results = []

    # TaskGroup provides structured concurrency
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(process_item(item)) for item in items]

    # All tasks complete when exiting the context
    return [task.result() for task in tasks]

# Exception handling with TaskGroup
async def process_with_errors(items: list[str]):
    try:
        async with asyncio.TaskGroup() as tg:
            for item in items:
                tg.create_task(process_item(item))
    except* ValueError as eg:
        # Handle ValueError exceptions
        for exc in eg.exceptions:
            print(f"ValueError: {exc}")
    except* TypeError as eg:
        # Handle TypeError exceptions
        for exc in eg.exceptions:
            print(f"TypeError: {exc}")
```

### create_task() vs await

```python
import asyncio

async def task_a():
    await asyncio.sleep(2)
    return "A done"

async def task_b():
    await asyncio.sleep(1)
    return "B done"

# Sequential (slower - 3 seconds total)
async def sequential():
    result_a = await task_a()  # Wait 2 seconds
    result_b = await task_b()  # Wait 1 second
    return result_a, result_b

# Concurrent (faster - 2 seconds total)
async def concurrent():
    task1 = asyncio.create_task(task_a())  # Start immediately
    task2 = asyncio.create_task(task_b())  # Start immediately
    result_a = await task1
    result_b = await task2
    return result_a, result_b

# Using gather (recommended for multiple tasks)
async def concurrent_gather():
    result_a, result_b = await asyncio.gather(task_a(), task_b())
    return result_a, result_b
```

## Advanced Patterns

### Semaphores for Rate Limiting

```python
import asyncio
import aiohttp

async def fetch_with_limit(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore
) -> dict:
    async with semaphore:  # Limits concurrent requests
        async with session.get(url) as response:
            return await response.json()

async def fetch_many(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)
```

### Timeouts

```python
import asyncio

async def slow_operation():
    await asyncio.sleep(10)
    return "done"

async def with_timeout():
    try:
        # Wait at most 5 seconds
        result = await asyncio.wait_for(slow_operation(), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        print("Operation timed out")
        return None

# Using timeout context manager (Python 3.11+)
async def with_timeout_context():
    async with asyncio.timeout(5.0):
        result = await slow_operation()
        return result
```

### Queues for Producer-Consumer

```python
import asyncio
from typing import Any

async def producer(queue: asyncio.Queue, items: list[Any]):
    for item in items:
        await queue.put(item)
        print(f"Produced: {item}")
    # Signal completion
    await queue.put(None)

async def consumer(queue: asyncio.Queue, consumer_id: int):
    while True:
        item = await queue.get()
        if item is None:
            # Put sentinel back for other consumers
            await queue.put(None)
            break
        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.5)  # Simulate work
        queue.task_done()

async def main():
    queue: asyncio.Queue = asyncio.Queue(maxsize=10)

    items = list(range(20))

    # Start producer and consumers
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producer(queue, items))
        for i in range(3):
            tg.create_task(consumer(queue, i))

asyncio.run(main())
```

### Async Generators

```python
import asyncio
from typing import AsyncIterator

async def fetch_pages(url: str, max_pages: int = 10) -> AsyncIterator[dict]:
    """Async generator for paginated API."""
    page = 1
    while page <= max_pages:
        # Simulate API call
        await asyncio.sleep(0.1)
        data = {"page": page, "items": [f"item_{i}" for i in range(10)]}

        if not data["items"]:
            break

        yield data
        page += 1

async def process_pages():
    async for page_data in fetch_pages("https://api.example.com"):
        print(f"Processing page {page_data['page']}")
        for item in page_data["items"]:
            process(item)
```

### Async Context Managers

```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

class AsyncDatabaseConnection:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
        return False

    async def connect(self):
        print("Connecting...")
        await asyncio.sleep(0.1)

    async def disconnect(self):
        print("Disconnecting...")
        await asyncio.sleep(0.1)

# Using decorator
@asynccontextmanager
async def async_session() -> AsyncIterator[dict]:
    session = {"connected": True}
    try:
        yield session
    finally:
        session["connected"] = False
        await asyncio.sleep(0.1)  # Cleanup

# Usage
async def main():
    async with AsyncDatabaseConnection() as db:
        await db.query("SELECT * FROM users")

    async with async_session() as session:
        print(session)
```

## Performance Optimization

### Eager Task Factory (Python 3.12+)

```python
import asyncio

async def cached_operation(key: str) -> str:
    cache = {"a": "value_a", "b": "value_b"}
    if key in cache:
        return cache[key]  # Returns synchronously
    await asyncio.sleep(1)  # Only if cache miss
    return f"fetched_{key}"

async def main():
    loop = asyncio.get_event_loop()
    # Enable eager task execution
    loop.set_task_factory(asyncio.eager_task_factory)

    # Cached operations complete synchronously without event loop overhead
    result = await cached_operation("a")
```

### Using uvloop

```python
# Install: pip install uvloop

import asyncio

try:
    import uvloop
    # 2-4x performance improvement
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass  # Fall back to default event loop

async def main():
    # Your async code here
    pass

asyncio.run(main())
```

### Free-Threaded asyncio (Python 3.14+)

```python
# Python 3.14 improvements for free-threaded builds:
# - Thread-safe asyncio with lock-free data structures
# - Linear scaling with number of threads
# - 10-20% single-threaded performance improvement
# - Reduced memory usage

import asyncio
import threading

async def per_thread_loop():
    """Each thread can run its own event loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        await asyncio.sleep(1)
    finally:
        loop.close()

# Multiple event loops in parallel (free-threaded build)
threads = [
    threading.Thread(target=lambda: asyncio.run(per_thread_loop()))
    for _ in range(4)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Common Gotchas

### Blocking the Event Loop

```python
import asyncio
import time

# BAD: Blocks the event loop
async def bad_example():
    time.sleep(5)  # Blocks everything!
    return "done"

# GOOD: Use async sleep
async def good_example():
    await asyncio.sleep(5)
    return "done"

# GOOD: Run blocking code in executor
async def blocking_in_executor():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, time.sleep, 5)
    return result

# For CPU-bound work, use ProcessPoolExecutor
from concurrent.futures import ProcessPoolExecutor

async def cpu_bound_work(data: list) -> list:
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, heavy_computation, data)
    return result
```

### Creating Tasks in Wrong Context

```python
import asyncio

# BAD: Task created outside async context
# task = asyncio.create_task(some_coroutine())  # RuntimeError!

# GOOD: Create tasks inside async function
async def main():
    task = asyncio.create_task(some_coroutine())
    await task

asyncio.run(main())
```

### Forgetting to Await

```python
import asyncio

async def fetch():
    await asyncio.sleep(1)
    return "data"

# BAD: Coroutine never executed
async def bad():
    result = fetch()  # Just creates coroutine object!
    print(result)     # Prints coroutine object, not "data"

# GOOD: Always await coroutines
async def good():
    result = await fetch()
    print(result)  # Prints "data"
```

### Exception Handling in Tasks

```python
import asyncio

async def failing_task():
    await asyncio.sleep(1)
    raise ValueError("Task failed!")

async def main():
    # BAD: Exception silently lost
    task = asyncio.create_task(failing_task())
    await asyncio.sleep(2)  # Task exception ignored

    # GOOD: Always await tasks or use TaskGroup
    task = asyncio.create_task(failing_task())
    try:
        await task
    except ValueError as e:
        print(f"Caught: {e}")

    # BEST: Use TaskGroup (Python 3.11+)
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(failing_task())
    except* ValueError as eg:
        for exc in eg.exceptions:
            print(f"Caught: {exc}")
```

## Async Libraries

### HTTP Clients

```python
# aiohttp - Most popular
import aiohttp

async def fetch_aiohttp(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# httpx - Supports both sync and async
import httpx

async def fetch_httpx(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Database

```python
# asyncpg - PostgreSQL
import asyncpg

async def query_postgres():
    conn = await asyncpg.connect("postgresql://user:pass@localhost/db")
    rows = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return rows

# aiosqlite - SQLite
import aiosqlite

async def query_sqlite():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()
```

### Web Frameworks

```python
# FastAPI (built on Starlette)
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Starlette
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({"hello": "world"})

app = Starlette(routes=[Route("/", homepage)])
```

## Additional References

For production-ready patterns beyond this guide, see:

- **[Async Patterns Library](references/async-patterns-library.md)** - Token bucket rate limiter, retry with exponential backoff, connection pools, batch processors, event bus, transaction context managers, async cache with TTL, graceful shutdown handlers
