---
name: async-python-patterns
description: Python asyncio and concurrent programming patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.
---

# Async Python Patterns

Expert guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## When to Use This Skill

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Optimizing I/O-bound workloads requiring parallelism
- Implementing async background tasks and task queues

## Core Patterns

### 1. Basic Async/Await

**Foundation for all async operations:**
```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

**Key concepts:**
- `async def` defines coroutines (pausable functions)
- `await` yields control back to event loop
- `asyncio.run()` is the entry point (Python 3.7+)
- Single-threaded cooperative multitasking

### 2. Concurrent Execution with gather()

**Execute multiple operations simultaneously:**
```python
import asyncio
from typing import List

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results

# Speed: Sequential = 5s, Concurrent = 0.5s for 10 users
```

**When to use:**
- Independent operations that can run in parallel
- I/O-bound tasks (API calls, database queries)
- Need all results before proceeding
- Use `return_exceptions=True` to handle partial failures

### 3. Task Creation and Management

**Background tasks that run independently:**
```python
import asyncio

async def background_task(name: str, delay: int):
    print(f"{name} started")
    await asyncio.sleep(delay)
    return f"Result from {name}"

async def main():
    # Create tasks (starts execution immediately)
    task1 = asyncio.create_task(background_task("Task 1", 2))
    task2 = asyncio.create_task(background_task("Task 2", 1))

    # Do other work while tasks run
    print("Doing other work")
    await asyncio.sleep(0.5)

    # Wait for results when needed
    result1, result2 = await task1, await task2
```

**Differences:**
- `await coroutine()` - Waits immediately
- `asyncio.create_task()` - Starts background execution
- Tasks can be cancelled with `task.cancel()`

### 4. Error Handling

**Robust error handling for concurrent operations:**
```python
import asyncio
from typing import List, Optional

async def safe_operation(item_id: int) -> Optional[dict]:
    try:
        await asyncio.sleep(0.1)
        if item_id % 3 == 0:
            raise ValueError(f"Item {item_id} failed")
        return {"id": item_id, "status": "success"}
    except ValueError as e:
        print(f"Error: {e}")
        return None

async def process_items(item_ids: List[int]):
    # gather with return_exceptions=True continues on errors
    results = await asyncio.gather(
        *[safe_operation(iid) for iid in item_ids],
        return_exceptions=True
    )

    successful = [r for r in results if r and not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"Success: {len(successful)}, Failed: {len(failed)}")
    return successful
```

### 5. Timeout Handling

**Prevent operations from hanging indefinitely:**
```python
import asyncio

async def with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_operation(5),
            timeout=2.0
        )
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")
        # Handle timeout (retry, fallback, etc.)
```

## Advanced Patterns

### 6. Async Context Managers

**Proper resource management with async operations:**
```python
import asyncio

class AsyncDatabaseConnection:
    """Async database connection with automatic cleanup."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection = None

    async def __aenter__(self):
        print("Opening connection")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connection = {"dsn": self.dsn, "connected": True}
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connection = None

async def query_database():
    async with AsyncDatabaseConnection("postgresql://localhost") as conn:
        # Connection automatically closed on exit
        return await perform_query(conn)
```

**Use cases:**
- Database connections (asyncpg, motor)
- HTTP sessions (aiohttp.ClientSession)
- File I/O (aiofiles)
- Locks and semaphores

### 7. Async Iterators and Generators

**Stream data asynchronously:**
```python
import asyncio
from typing import AsyncIterator

async def fetch_pages(url: str, max_pages: int) -> AsyncIterator[dict]:
    """Fetch paginated data lazily."""
    for page in range(1, max_pages + 1):
        await asyncio.sleep(0.2)  # API call
        yield {
            "page": page,
            "url": f"{url}?page={page}",
            "data": [f"item_{page}_{i}" for i in range(5)]
        }

async def process_stream():
    async for page_data in fetch_pages("https://api.example.com", 10):
        # Process each page as it arrives (memory efficient)
        print(f"Processing page {page_data['page']}")
```

**Benefits:**
- Memory efficient for large datasets
- Start processing before all data arrives
- Natural backpressure handling

### 8. Producer-Consumer with Queues

**Coordinate work between producers and consumers:**
```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, producer_id: int, num_items: int):
    for i in range(num_items):
        item = f"Item-{producer_id}-{i}"
        await queue.put(item)
        await asyncio.sleep(0.1)
    await queue.put(None)  # Signal completion

async def consumer(queue: Queue, consumer_id: int):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.2)
        queue.task_done()

async def run_pipeline():
    queue = Queue(maxsize=10)

    # 2 producers, 3 consumers
    producers = [asyncio.create_task(producer(queue, i, 5)) for i in range(2)]
    consumers = [asyncio.create_task(consumer(queue, i)) for i in range(3)]

    await asyncio.gather(*producers)
    await queue.join()  # Wait for all items processed

    for c in consumers:
        c.cancel()
```

### 9. Rate Limiting with Semaphores

**Control concurrent operations:**
```python
import asyncio
from typing import List

async def api_call(url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:  # Only N operations at once
        print(f"Calling {url}")
        await asyncio.sleep(0.5)
        return {"url": url, "status": 200}

async def rate_limited_requests(urls: List[str], max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [api_call(url, semaphore) for url in urls]
    return await asyncio.gather(*tasks)

# Limits to 5 concurrent requests regardless of total URLs
```

**Use cases:**
- API rate limiting (respect API quotas)
- Database connection limits
- File descriptor limits
- Memory-constrained operations

### 10. Async Locks for Shared State

**Thread-safe operations in async context:**
```python
import asyncio

class AsyncCounter:
    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate work
            self.value = current + 1

    async def get_value(self) -> int:
        async with self.lock:
            return self.value
```

**Synchronization primitives:**
- `Lock`: Mutual exclusion
- `Event`: Signal between tasks
- `Condition`: Wait for condition
- `Semaphore`: Limit concurrent access

## Performance Best Practices

### 1. Use Connection Pools

**Reuse connections for efficiency:**
```python
import aiohttp

async def with_connection_pool():
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [session.get(f"https://api.example.com/item/{i}")
                 for i in range(50)]
        return await asyncio.gather(*tasks)
```

### 2. Avoid Blocking the Event Loop

**Run CPU-intensive work in executor:**
```python
import asyncio
import concurrent.futures

def blocking_operation(data):
    """CPU-intensive blocking operation."""
    import time
    time.sleep(1)
    return data * 2

async def run_in_executor(data):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_operation, data)
        return result
```

**Common blockers to avoid:**
- `time.sleep()` - Use `asyncio.sleep()`
- Synchronous file I/O - Use `aiofiles`
- Synchronous HTTP - Use `aiohttp` or `httpx`
- Heavy computation - Use `loop.run_in_executor()`

### 3. Batch Operations

**Process in chunks to control memory:**
```python
async def batch_process(items: List[str], batch_size: int = 10):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        results = await asyncio.gather(*[process_item(item) for item in batch])
        print(f"Processed batch {i // batch_size + 1}")
```

## Common Pitfalls

### 1. Forgetting await
```python
# Wrong - returns coroutine, doesn't execute
result = async_function()

# Correct
result = await async_function()
```

### 2. Blocking the Event Loop
```python
# Wrong - blocks entire event loop
import time
async def bad():
    time.sleep(1)

# Correct
async def good():
    await asyncio.sleep(1)
```

### 3. Not Handling Cancellation
```python
async def cancelable_task():
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # Cleanup resources
        raise  # Re-raise to propagate
```

### 4. Mixing Sync and Async
```python
# Wrong
def sync_function():
    result = await async_function()  # SyntaxError

# Correct
def sync_function():
    result = asyncio.run(async_function())
```

## Testing Async Code

**Use pytest-asyncio for testing:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data("https://api.example.com")
    assert result is not None

@pytest.mark.asyncio
async def test_with_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(5), timeout=1.0)
```

## Resources

- **Python asyncio docs**: https://docs.python.org/3/library/asyncio.html
- **aiohttp**: Async HTTP client/server framework
- **FastAPI**: Modern async web framework with automatic OpenAPI
- **asyncpg**: High-performance async PostgreSQL driver
- **motor**: Async MongoDB driver for Python
- **pytest-asyncio**: Testing framework for async code

## Best Practices Summary

1. Use `asyncio.run()` for entry point (Python 3.7+)
2. Always `await` coroutines to execute them
3. Use `gather()` for concurrent execution of independent tasks
4. Implement proper error handling with try/except and `return_exceptions=True`
5. Use timeouts to prevent hanging operations
6. Pool connections for better performance and resource management
7. Avoid blocking operations in async code (use executors if needed)
8. Use semaphores for rate limiting and resource control
9. Handle task cancellation properly with CancelledError
10. Test async code thoroughly with pytest-asyncio
