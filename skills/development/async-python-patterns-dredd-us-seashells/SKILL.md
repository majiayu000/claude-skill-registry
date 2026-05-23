---
name: async-python-patterns
description: Implement AsyncIO patterns for I/O-bound tasks with asyncio.gather, semaphores, and FastAPI async endpoints. Use for concurrent operations, parallel HTTP fetches, rate-limited operations, or async API development. Achieves near-linear scaling with concurrent tasks and minimal overhead. Triggers on "async", "asyncio", "concurrent", "parallel requests", "FastAPI async", "aiohttp", "async Python".
---

# Async Python Patterns

## Purpose

Implement AsyncIO patterns for concurrent I/O-bound operations with proper semaphores, gather, and FastAPI integration.

## When to Use

- Concurrent I/O operations (HTTP requests, file I/O, database queries)
- Parallel API calls or web scraping
- Rate-limited concurrent operations
- FastAPI async endpoint development
- Performance optimization for I/O-bound code

## Core Instructions

### Basic Async Function

```python
import asyncio

async def fetch_url(url):
    """Async function for I/O operation"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Run async function
result = asyncio.run(fetch_url('https://example.com'))
```

### Parallel Execution with gather()

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    """Fetch single URL"""
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    """Fetch multiple URLs in parallel"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

# Usage
urls = ['https://example.com', 'https://example.org']
results = asyncio.run(fetch_all(urls))
```

### Rate Limiting with Semaphore

```python
import asyncio

async def limited_fetch(semaphore, session, url):
    """Fetch with concurrency limit"""
    async with semaphore:
        return await fetch_url(session, url)

async def fetch_all_limited(urls, max_concurrent=10):
    """Fetch URLs with max 10 concurrent requests"""
    semaphore = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:
        tasks = [
            limited_fetch(semaphore, session, url)
            for url in urls
        ]
        return await asyncio.gather(*tasks)
```

### Error Handling

```python
async def safe_fetch(url):
    """Fetch with error handling"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
    except asyncio.TimeoutError:
        return f"Timeout: {url}"
    except aiohttp.ClientError as e:
        return f"Error: {url}: {str(e)}"

# Gather with return_exceptions to continue on failures
results = await asyncio.gather(*tasks, return_exceptions=True)
```

### FastAPI Async Endpoints

```python
from fastapi import FastAPI
import aiohttp

app = FastAPI()

@app.get("/data")
async def get_data():
    """Async endpoint"""
    # I/O operations run concurrently
    async with aiohttp.ClientSession() as session:
        result = await fetch_from_api(session)
    return {"data": result}

@app.post("/process")
async def process_data(items: list):
    """Process multiple items concurrently"""
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return {"results": results}
```

### Async Database Operations

```python
import asyncpg

async def fetch_users():
    """Async database query"""
    conn = await asyncpg.connect(
        host='localhost',
        user='user',
        password='pass',
        database='db'
    )

    users = await conn.fetch('SELECT * FROM users')
    await conn.close()
    return users

async def bulk_insert(records):
    """Batch insert with connection pool"""
    pool = await asyncpg.create_pool(
        host='localhost',
        database='db'
    )

    async with pool.acquire() as conn:
        await conn.executemany(
            'INSERT INTO users VALUES ($1, $2)',
            records
        )

    await pool.close()
```

## Performance Patterns

### Sequential vs Parallel Comparison

```python
import time

# Sequential (slow)
async def sequential_fetch(urls):
    results = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            result = await fetch_url(session, url)
            results.append(result)
    return results
# Time: N * avg_response_time

# Parallel (fast)
async def parallel_fetch(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
# Time: max(response_times) ≈ single request time
```

### Chunk Processing for Large Lists

```python
async def process_in_chunks(items, chunk_size=100):
    """Process large list in chunks to avoid memory issues"""
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        tasks = [process_item(item) for item in chunk]
        results = await asyncio.gather(*tasks)
        yield results
```

## Best Practices

### Do:
- Use `async/await` for I/O-bound operations
- Use `asyncio.gather()` for parallel execution
- Implement semaphores for rate limiting
- Handle errors gracefully with `return_exceptions=True`
- Use connection pools for databases
- Set timeouts on all I/O operations

### Don't:
- Use async for CPU-bound tasks (use multiprocessing instead)
- Create too many concurrent tasks (use semaphores)
- Forget to close connections/sessions
- Mix blocking and async code (use `run_in_executor` if needed)
- Ignore error handling

### Wrapping Sync Code

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

def blocking_function():
    """Sync function that blocks"""
    time.sleep(1)
    return "result"

async def async_wrapper():
    """Run sync function in executor"""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,  # Use default executor
        blocking_function
    )
    return result
```

## Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    result = await fetch_url('https://example.com')
    assert result is not None

@pytest.mark.asyncio
async def test_parallel_fetch():
    """Test parallel execution"""
    urls = ['https://example.com'] * 5
    results = await fetch_all(urls)
    assert len(results) == 5
```

## Common Patterns

### Retry with Exponential Backoff

```python
async def retry_fetch(url, max_retries=3):
    """Fetch with retries"""
    for attempt in range(max_retries):
        try:
            return await fetch_url(url)
        except aiohttp.ClientError:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Task Queue Pattern

```python
import asyncio
from asyncio import Queue

async def worker(queue):
    """Process items from queue"""
    while True:
        item = await queue.get()
        try:
            await process_item(item)
        finally:
            queue.task_done()

async def main():
    queue = Queue()

    # Start workers
    workers = [
        asyncio.create_task(worker(queue))
        for _ in range(10)
    ]

    # Add items to queue
    for item in items:
        await queue.put(item)

    # Wait for completion
    await queue.join()

    # Cancel workers
    for w in workers:
        w.cancel()
```

## Performance Characteristics

- **Near-linear scaling** with concurrent I/O tasks
- **Minimal overhead** compared to sequential
- **Efficient** for I/O-bound operations (10-100x speedup)
- **NOT suitable** for CPU-bound tasks (use multiprocessing)

## Dependencies

- Python 3.7+
- `asyncio` (built-in)
- `aiohttp` - Async HTTP client
- `asyncpg` - Async PostgreSQL (optional)
- `fastapi` - Async web framework (optional)
- `pytest-asyncio` - Testing support

## Version

v1.0.0 (2025-10-23)

