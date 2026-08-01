---
name: concurrency
description: Comprehensive concurrency and parallelism patterns for multi-threaded
  and async programming. Use when implementing async/await, parallel processing, thread
  safety, worker pools, or debugging race cond
---

---
name: concurrency
description: Comprehensive concurrency and parallelism patterns for multi-threaded and async programming. Use when implementing async/await, parallel processing, thread safety, worker pools, or debugging race conditions and deadlocks. Triggers: async, await, concurrent, parallel, threads, race condition, deadlock, mutex, semaphore, worker pool, queue.
---

# Concurrency

## Overview

Concurrency enables programs to handle multiple tasks efficiently. This skill covers async/await patterns, parallelism vs concurrency distinctions, race condition prevention, deadlock handling, thread safety patterns, and work queue implementations.

## Instructions

### 1. Async/Await Patterns

#### Python Async Patterns

```python
import asyncio
from typing import List, TypeVar, Coroutine, Any

T = TypeVar('T')

# Basic async function
async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# Concurrent execution with gather
async def fetch_all(urls: List[str]) -> List[dict]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks, return_exceptions=True)

# Timeout handling
async def fetch_with_timeout(url: str, timeout: float = 5.0) -> dict:
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Request to {url} timed out after {timeout}s")

# Semaphore for rate limiting
async def fetch_with_rate_limit(urls: List[str], max_concurrent: int = 10) -> List[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_fetch(url: str) -> dict:
        async with semaphore:
            return await fetch_data(url)

    return await asyncio.gather(*[limited_fetch(url) for url in urls])

# Async context manager
class AsyncDatabaseConnection:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(...)
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

# Async iterator
class AsyncPaginator:
    def __init__(self, fetch_page):
        self.fetch_page = fetch_page
        self.page = 0
        self.done = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.done:
            raise StopAsyncIteration

        result = await self.fetch_page(self.page)
        if not result:
            self.done = True
            raise StopAsyncIteration

        self.page += 1
        return result
```

#### TypeScript Async Patterns

```typescript
// Promise.all for concurrent execution
async function fetchAll<T>(urls: string[]): Promise<T[]> {
  return Promise.all(urls.map((url) => fetch(url).then((r) => r.json())));
}

// Promise.allSettled for fault tolerance
async function fetchAllSafe<T>(urls: string[]): Promise<Array<T | Error>> {
  const results = await Promise.allSettled(
    urls.map((url) => fetch(url).then((r) => r.json())),
  );

  return results.map((result) =>
    result.status === "fulfilled" ? result.value : new Error(result.reason),
  );
}

// Rate-limited concurrent execution
async function fetchWithConcurrencyLimit<T>(
  items: string[],
  fn: (item: string) => Promise<T>,
  limit: number,
): Promise<T[]> {
  const results: T[] = [];
  const executing: Promise<void>[] = [];

  for (const item of items) {
    const p = fn(item).then((result) => {
      results.push(result);
    });
    executing.push(p);

    if (executing.length >= limit) {
      await Promise.race(executing);
      executing.splice(
        executing.findIndex((e) => e === p),
        1,
      );
    }
  }

  await Promise.all(executing);
  return results;
}

// Async queue
class AsyncQueue<T> {
  private queue: T[] = [];
  private resolvers: Array<(value: T) => void> = [];

  async enqueue(item: T): Promise<void> {
    if (this.resolvers.length > 0) {
      const resolve = this.resolvers.shift()!;
      resolve(item);
    } else {
      this.queue.push(item);
    }
  }

  async dequeue(): Promise<T> {
    if (this.queue.length > 0) {
      return this.queue.shift()!;
    }
    return new Promise((resolve) => this.resolvers.push(resolve));
  }
}
```

### 2. Parallelism vs Concurrency

```python
import asyncio
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Concurrency: I/O-bound tasks (use async or threads)
async def io_bound_concurrent():
    """Use for network calls, file I/O, database queries."""
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        return await asyncio.gather(*tasks)

def io_bound_threaded(urls: List[str]):
    """Threads for I/O when async isn't available."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        return list(executor.map(requests.get, urls))

# Parallelism: CPU-bound tasks (use processes)
def cpu_bound_parallel(data: List[int]) -> List[int]:
    """Use for heavy computation - bypasses GIL."""
    with ProcessPoolExecutor() as executor:
        return list(executor.map(heavy_computation, data))

# Hybrid: CPU work with I/O
async def hybrid_processing(items: List[dict]):
    """Combine async I/O with parallel CPU processing."""
    loop = asyncio.get_event_loop()

    # Fetch data concurrently
    raw_data = await asyncio.gather(*[fetch(item) for item in items])

    # Process CPU-bound work in parallel
    with ProcessPoolExecutor() as executor:
        processed = await loop.run_in_executor(
            executor,
            process_batch,
            raw_data
        )

    return processed
```

### 3. Race Conditions and Prevention

```python
import threading
import asyncio
from contextlib import contextmanager

# Thread-safe counter with lock
class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1
            return self._value

    @property
    def value(self):
        with self._lock:
            return self._value

# Read-write lock for optimized concurrent access
class ReadWriteLock:
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    @contextmanager
    def read_lock(self):
        with self._read_ready:
            self._readers += 1
        try:
            yield
        finally:
            with self._read_ready:
                self._readers -= 1
                if self._readers == 0:
                    self._read_ready.notify_all()

    @contextmanager
    def write_lock(self):
        with self._read_ready:
            while self._readers > 0:
                self._read_ready.wait()
            yield

# Async lock for async code
class AsyncSafeCache:
    def __init__(self):
        self._cache = {}
        self._lock = asyncio.Lock()

    async def get_or_set(self, key: str, factory):
        async with self._lock:
            if key not in self._cache:
                self._cache[key] = await factory()
            return self._cache[key]

# Compare-and-swap for lock-free operations
import atomics  # or use threading primitives

class LockFreeCounter:
    def __init__(self):
        self._value = atomics.atomic(width=8, atype=atomics.INT)

    def increment(self):
        while True:
            current = self._value.load()
            if self._value.cmpxchg_weak(current, current + 1):
                return current + 1
```

### 4. Deadlock Detection and Prevention

```python
import threading
from collections import defaultdict
from typing import Dict, Set
import time

# Deadlock prevention with lock ordering
class OrderedLockManager:
    """Prevents deadlocks by enforcing lock acquisition order."""

    def __init__(self):
        self._lock_order: Dict[str, int] = {}
        self._next_order = 0
        self._thread_locks: Dict[int, Set[str]] = defaultdict(set)
        self._meta_lock = threading.Lock()

    def register_lock(self, name: str) -> threading.Lock:
        with self._meta_lock:
            if name not in self._lock_order:
                self._lock_order[name] = self._next_order
                self._next_order += 1
        return threading.Lock()

    @contextmanager
    def acquire(self, lock: threading.Lock, name: str):
        thread_id = threading.current_thread().ident

        # Check lock ordering
        held_locks = self._thread_locks[thread_id]
        for held_name in held_locks:
            if self._lock_order[name] < self._lock_order[held_name]:
                raise RuntimeError(
                    f"Lock ordering violation: {name} < {held_name}"
                )

        lock.acquire()
        self._thread_locks[thread_id].add(name)
        try:
            yield
        finally:
            self._thread_locks[thread_id].discard(name)
            lock.release()

# Timeout-based deadlock detection
class TimeoutLock:
    def __init__(self, timeout: float = 5.0):
        self._lock = threading.Lock()
        self._timeout = timeout

    def acquire(self):
        acquired = self._lock.acquire(timeout=self._timeout)
        if not acquired:
            raise DeadlockError(
                f"Failed to acquire lock within {self._timeout}s - possible deadlock"
            )
        return True

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        self.release()

# Deadlock detection with wait-for graph
class DeadlockDetector:
    def __init__(self):
        self._wait_for: Dict[int, int] = {}  # thread -> thread it's waiting for
        self._lock = threading.Lock()

    def register_wait(self, waiting_thread: int, holding_thread: int):
        with self._lock:
            self._wait_for[waiting_thread] = holding_thread
            if self._has_cycle():
                raise DeadlockError("Deadlock detected in wait-for graph")

    def unregister_wait(self, thread: int):
        with self._lock:
            self._wait_for.pop(thread, None)

    def _has_cycle(self) -> bool:
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            next_node = self._wait_for.get(node)
            if next_node:
                if next_node not in visited:
                    if dfs(next_node):
                        return True
                elif next_node in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self._wait_for:
            if node not in visited:
                if dfs(node):
                    return True
        return False
```

### 5. Thread Safety Patterns

```python
import threading
from functools import wraps
from typing import TypeVar, Generic

T = TypeVar('T')

# Thread-local storage
class RequestContext:
    _local = threading.local()

    @classmethod
    def set_user(cls, user_id: str):
        cls._local.user_id = user_id

    @classmethod
    def get_user(cls) -> str:
        return getattr(cls._local, 'user_id', None)

# Immutable data for thread safety
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class ImmutableConfig:
    host: str
    port: int
    options: Tuple[str, ...]  # Use tuple instead of list

# Copy-on-write pattern
class CopyOnWriteList(Generic[T]):
    def __init__(self):
        self._data: Tuple[T, ...] = ()
        self._lock = threading.Lock()

    def append(self, item: T):
        with self._lock:
            self._data = (*self._data, item)

    def __iter__(self):
        # Snapshot iteration - safe without lock
        return iter(self._data)

# Thread-safe singleton
class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Synchronized decorator
def synchronized(lock: threading.Lock = None):
    def decorator(func):
        nonlocal lock
        if lock is None:
            lock = threading.Lock()

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 6. Work Queues and Worker Pools

```python
import asyncio
import queue
import threading
from typing import Callable, Any, List
from dataclasses import dataclass
from concurrent.futures import Future

@dataclass
class Job:
    func: Callable
    args: tuple
    kwargs: dict
    future: Future

# Thread-based worker pool
class ThreadWorkerPool:
    def __init__(self, num_workers: int = 4):
        self._queue = queue.Queue()
        self._workers: List[threading.Thread] = []
        self._shutdown = False

        for _ in range(num_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self._workers.append(worker)

    def _worker_loop(self):
        while not self._shutdown:
            try:
                job = self._queue.get(timeout=1)
                try:
                    result = job.func(*job.args, **job.kwargs)
                    job.future.set_result(result)
                except Exception as e:
                    job.future.set_exception(e)
            except queue.Empty:
                continue

    def submit(self, func: Callable, *args, **kwargs) -> Future:
        future = Future()
        job = Job(func, args, kwargs, future)
        self._queue.put(job)
        return future

    def shutdown(self, wait: bool = True):
        self._shutdown = True
        if wait:
            for worker in self._workers:
                worker.join()

# Async worker pool
class AsyncWorkerPool:
    def __init__(self, num_workers: int = 10):
        self._queue: asyncio.Queue = asyncio.Queue()
        self._num_workers = num_workers
        self._workers: List[asyncio.Task] = []

    async def start(self):
        for _ in range(self._num_workers):
            task = asyncio.create_task(self._worker_loop())
            self._workers.append(task)

    async def _worker_loop(self):
        while True:
            job = await self._queue.get()
            if job is None:  # Shutdown signal
                break

            func, args, kwargs, future = job
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)
            finally:
                self._queue.task_done()

    async def submit(self, func: Callable, *args, **kwargs) -> Any:
        future = asyncio.Future()
        await self._queue.put((func, args, kwargs, future))
        return await future

    async def shutdown(self):
        for _ in self._workers:
            await self._queue.put(None)
        await asyncio.gather(*self._workers)

# Priority queue worker
class PriorityWorkerPool:
    def __init__(self, num_workers: int = 4):
        self._queue = queue.PriorityQueue()
        self._workers: List[threading.Thread] = []
        self._shutdown = False

        for _ in range(num_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            worker.start()
            self._workers.append(worker)

    def _worker_loop(self):
        while not self._shutdown:
            try:
                priority, job = self._queue.get(timeout=1)
                try:
                    result = job.func(*job.args, **job.kwargs)
                    job.future.set_result(result)
                except Exception as e:
                    job.future.set_exception(e)
            except queue.Empty:
                continue

    def submit(self, func: Callable, *args, priority: int = 0, **kwargs) -> Future:
        future = Future()
        job = Job(func, args, kwargs, future)
        self._queue.put((priority, job))
        return future
```

## Best Practices

1. **Prefer Async for I/O**: Use async/await for network and file I/O operations.

2. **Use Processes for CPU Work**: Bypass GIL with ProcessPoolExecutor for CPU-bound tasks.

3. **Minimize Shared State**: Prefer message passing over shared memory.

4. **Lock Ordering**: Always acquire locks in a consistent order to prevent deadlocks.

5. **Keep Critical Sections Small**: Hold locks for the minimum time necessary.

6. **Use Higher-Level Abstractions**: Prefer queues, futures, and async patterns over raw locks.

7. **Test for Race Conditions**: Use tools like ThreadSanitizer and stress testing.

8. **Document Thread Safety**: Clearly document which methods are thread-safe.

## Examples

### Complete Async Web Scraper with Rate Limiting

```python
import asyncio
import aiohttp
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ScrapeResult:
    url: str
    status: int
    content: Optional[str]
    error: Optional[str] = None

class AsyncScraper:
    def __init__(
        self,
        max_concurrent: int = 10,
        requests_per_second: float = 5.0
    ):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.rate_limit = 1.0 / requests_per_second
        self.last_request_time = 0
        self._lock = asyncio.Lock()

    async def _rate_limit(self):
        async with self._lock:
            now = asyncio.get_event_loop().time()
            wait_time = self.last_request_time + self.rate_limit - now
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self.last_request_time = asyncio.get_event_loop().time()

    async def scrape_url(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> ScrapeResult:
        async with self.semaphore:
            await self._rate_limit()
            try:
                async with session.get(url, timeout=10) as response:
                    content = await response.text()
                    return ScrapeResult(
                        url=url,
                        status=response.status,
                        content=content
                    )
            except Exception as e:
                return ScrapeResult(
                    url=url,
                    status=0,
                    content=None,
                    error=str(e)
                )

    async def scrape_all(self, urls: List[str]) -> List[ScrapeResult]:
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_url(session, url) for url in urls]
            return await asyncio.gather(*tasks)

# Usage
async def main():
    scraper = AsyncScraper(max_concurrent=5, requests_per_second=2.0)
    urls = ["https://example.com"] * 20
    results = await scraper.scrape_all(urls)

    for result in results:
        if result.error:
            print(f"Failed: {result.url} - {result.error}")
        else:
            print(f"Success: {result.url} - {result.status}")

asyncio.run(main())
```
