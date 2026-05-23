---
name: python-optimization
description: Optimizes Python performance using asyncio, profiling, and best practices. Use when implementing async/await patterns, profiling slow code, fixing bottlenecks, or improving memory usage. Triggers include "asyncio", "async def", "cProfile", "slow Python", "memory leak", "profile", or "optimize Python".
allowed-tools: Read, Edit, Bash, Grep
---

# Python Optimization

Comprehensive guide to async programming, profiling, and performance optimization for Python applications.

## When to Use This Skill

- Building async web APIs (FastAPI, aiohttp)
- Implementing concurrent I/O operations
- Profiling CPU and memory usage
- Optimizing slow functions
- Reducing memory consumption
- Parallelizing CPU-bound or I/O-bound tasks

## Async Python Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

## Core Async Patterns

### Concurrent Execution with gather()

```python
import asyncio
from typing import List

async def fetch_user(user_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

asyncio.run(fetch_all_users([1, 2, 3, 4, 5]))
```

### Rate Limiting with Semaphore

```python
import asyncio

async def api_call(url: str, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        await asyncio.sleep(0.5)  # Simulate API call
        return {"url": url, "status": 200}

async def rate_limited_requests(urls: list, max_concurrent: int = 5):
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [api_call(url, semaphore) for url in urls]
    return await asyncio.gather(*tasks)
```

### Timeout Handling

```python
import asyncio

async def slow_operation(delay: int) -> str:
    await asyncio.sleep(delay)
    return f"Completed after {delay}s"

async def with_timeout():
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2.0)
    except asyncio.TimeoutError:
        print("Operation timed out")
```

### Producer-Consumer Pattern

```python
import asyncio
from asyncio import Queue

async def producer(queue: Queue, producer_id: int, num_items: int):
    for i in range(num_items):
        await queue.put(f"Item-{producer_id}-{i}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Signal completion

async def consumer(queue: Queue, consumer_id: int):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.2)
```

## Profiling Tools

### cProfile - CPU Profiling

```python
import cProfile
import pstats
from pstats import SortKey

def main():
    # Your code here
    pass

profiler = cProfile.Profile()
profiler.enable()
main()
profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats(SortKey.CUMULATIVE)
stats.print_stats(10)
```

**Command-line:**

```bash
python -m cProfile -o output.prof script.py
python -m pstats output.prof
```

### memory_profiler - Memory Usage

```python
from memory_profiler import profile

@profile
def memory_intensive():
    big_list = [i for i in range(1000000)]
    return sum(big_list)

# Run with: python -m memory_profiler script.py
```

### py-spy - Production Profiling

```bash
# Profile running process
py-spy top --pid 12345

# Generate flamegraph
py-spy record -o profile.svg -- python script.py
```

### timeit - Benchmarking

```python
import timeit

execution_time = timeit.timeit(
    "sum(range(1000000))",
    number=100
)
print(f"Average: {execution_time/100:.6f}s")
```

## Performance Optimization Patterns

### List Comprehensions vs Loops

```python
# Slow: Traditional loop
def slow_squares(n):
    result = []
    for i in range(n):
        result.append(i**2)
    return result

# Fast: List comprehension (2-3x faster)
def fast_squares(n):
    return [i**2 for i in range(n)]
```

### Generators for Large Data

```python
# Memory-intensive list
data = [i**2 for i in range(1000000)]  # Allocates all at once

# Memory-efficient generator
data = (i**2 for i in range(1000000))  # Constant memory
```

### Dictionary Lookups vs List Search

```python
# O(n) - Slow for large lists
if target in list_of_items: pass

# O(1) - Fast regardless of size
if target in set_of_items: pass
if target in dict_of_items: pass
```

### String Concatenation

```python
# Slow: String concatenation
result = ""
for item in items:
    result += str(item)

# Fast: Join (10-100x faster)
result = "".join(str(item) for item in items)
```

### Caching with lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Using __slots__ for Memory

```python
# Regular class: ~400 bytes per instance
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Slotted class: ~80 bytes per instance (5x reduction)
class Point:
    __slots__ = ['x', 'y']
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Or with dataclass
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: int
    y: int
```

## Parallelization

### Multiprocessing for CPU-Bound

```python
import multiprocessing as mp

def cpu_intensive_task(n):
    return sum(i**2 for i in range(n))

if __name__ == "__main__":
    with mp.Pool(processes=4) as pool:
        results = pool.map(cpu_intensive_task, [1000000] * 4)
```

### Async for I/O-Bound

```python
import asyncio
import aiohttp

async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_all(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### ThreadPoolExecutor for Mixed

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

def blocking_operation(data):
    import time
    time.sleep(1)
    return data * 2

async def run_in_executor(data):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, blocking_operation, data)
```

## Database Optimization

### Batch Operations

```python
# Slow: Individual inserts
for item in items:
    cursor.execute("INSERT INTO table VALUES (?)", (item,))
    conn.commit()

# Fast: Batch insert (100x faster)
cursor.executemany("INSERT INTO table VALUES (?)", [(i,) for i in items])
conn.commit()
```

## Memory Leak Detection

```python
import tracemalloc

tracemalloc.start()
snapshot1 = tracemalloc.take_snapshot()

# Run code that might leak
problematic_function()

snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

for stat in top_stats[:10]:
    print(stat)
```

## Common Pitfalls

### Async Pitfalls

```python
# Wrong: Returns coroutine, doesn't execute
result = async_function()

# Correct
result = await async_function()

# Wrong: Blocks event loop
import time
async def bad():
    time.sleep(1)  # Blocks!

# Correct
async def good():
    await asyncio.sleep(1)
```

### Performance Pitfalls

- Using `list` for membership tests instead of `set`
- Not precompiling regex patterns
- Creating unnecessary copies of data
- Using global variables in hot loops
- Not using connection pooling for databases

## Best Practices Summary

### Async

1. Use `asyncio.run()` for entry point (Python 3.7+)
2. Always `await` coroutines
3. Use `gather()` for concurrent execution
4. Use semaphores for rate limiting
5. Handle timeouts and cancellation

### Performance

1. Profile before optimizing
2. Use appropriate data structures (dict/set for lookups)
3. Use generators for large datasets
4. Cache expensive computations with `lru_cache`
5. Use `slots=True` for memory-efficient classes
6. Batch database operations
7. Consider NumPy for numerical operations

## Performance Checklist

- [ ] Profiled code to identify bottlenecks
- [ ] Used appropriate data structures
- [ ] Implemented caching where beneficial
- [ ] Used generators for large datasets
- [ ] Multiprocessing for CPU-bound tasks
- [ ] Async I/O for I/O-bound tasks
- [ ] Checked for memory leaks
- [ ] Benchmarked before and after

## Resources

- **asyncio docs**: https://docs.python.org/3/library/asyncio.html
- **aiohttp**: Async HTTP client/server
- **FastAPI**: Modern async web framework
- **cProfile**: Built-in CPU profiler
- **memory_profiler**: Memory usage profiling
- **py-spy**: Sampling profiler for production
- **NumPy**: High-performance numerical computing
