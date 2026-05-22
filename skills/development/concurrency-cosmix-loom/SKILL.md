---
name: concurrency
description: Comprehensive concurrency and parallelism patterns for multi-threaded and async programming. Use when implementing async/await, parallel processing, thread safety, worker pools, or debugging race conditions and deadlocks. Triggers: async, await, thread, mutex, lock, semaphore, channel, actor, parallel, concurrent, race condition, deadlock, livelock, atomic, futures, promises, tokio, asyncio, goroutine, spawn, Arc, Mutex, RwLock, mpsc, select, join, worker pool, queue, synchronization, critical section, context switch.
---

# Concurrency

## Overview

Concurrency enables programs to handle multiple tasks efficiently. This skill covers async/await patterns across Rust (tokio), Python (asyncio), TypeScript (Promises), and Go (goroutines). Includes parallelism strategies, race condition prevention, deadlock handling, thread safety patterns, channel-based communication, and work queue implementations.

## Agent Specializations

When implementing concurrency, delegate to the appropriate specialist:

1. **senior-software-engineer** (Opus) - Architectural decisions for concurrent systems, choosing between threading models, designing message-passing vs shared-state architectures
2. **software-engineer** (Sonnet) - Implementing concurrent code following established patterns, writing async functions, worker pools, rate limiters
3. **security-engineer** (Opus) - Identifying race conditions, time-of-check-time-of-use vulnerabilities, reviewing lock ordering for deadlocks
4. **senior-infrastructure-engineer** (Opus) - Distributed systems concurrency, consistency models, distributed locks, saga patterns

## Instructions

### 1. Rust Async/Await with Tokio

```rust
use tokio::sync::{Mutex, RwLock, Semaphore, mpsc};
use tokio::time::{sleep, Duration, timeout};
use std::sync::Arc;
use futures::future::join_all;

// Basic async function
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    response.text().await
}

// Concurrent execution with join_all
async fn fetch_all(urls: Vec<String>) -> Vec<Result<String, reqwest::Error>> {
    let tasks: Vec<_> = urls.into_iter()
        .map(|url| tokio::spawn(async move { fetch_data(&url).await }))
        .collect();

    join_all(tasks).await
        .into_iter()
        .map(|r| r.unwrap())
        .collect()
}

// Timeout handling
async fn fetch_with_timeout(url: &str) -> Result<String, Box<dyn std::error::Error>> {
    match timeout(Duration::from_secs(5), fetch_data(url)).await {
        Ok(result) => Ok(result?),
        Err(_) => Err(format!("Request to {} timed out", url).into()),
    }
}

// Semaphore for rate limiting
async fn fetch_with_rate_limit(
    urls: Vec<String>,
    max_concurrent: usize,
) -> Vec<Result<String, reqwest::Error>> {
    let semaphore = Arc::new(Semaphore::new(max_concurrent));

    let tasks: Vec<_> = urls.into_iter()
        .map(|url| {
            let sem = semaphore.clone();
            tokio::spawn(async move {
                let _permit = sem.acquire().await.unwrap();
                fetch_data(&url).await
            })
        })
        .collect();

    join_all(tasks).await
        .into_iter()
        .map(|r| r.unwrap())
        .collect()
}

// Channel-based worker pattern
async fn worker_pool_example() {
    let (tx, mut rx) = mpsc::channel::<String>(100);

    // Spawn workers
    for i in 0..4 {
        let mut worker_rx = rx.clone();
        tokio::spawn(async move {
            while let Some(url) = worker_rx.recv().await {
                println!("Worker {} processing {}", i, url);
                let _ = fetch_data(&url).await;
            }
        });
    }

    // Send work
    for url in vec!["https://example.com"; 20] {
        tx.send(url.to_string()).await.unwrap();
    }
}

// Shared state with Arc<Mutex<T>>
#[derive(Clone)]
struct SharedCache {
    data: Arc<Mutex<std::collections::HashMap<String, String>>>,
}

impl SharedCache {
    async fn get_or_insert(&self, key: String, value: String) -> String {
        let mut cache = self.data.lock().await;
        cache.entry(key).or_insert(value).clone()
    }
}

// Arc<RwLock<T>> for read-heavy workloads
struct ReadHeavyCache {
    data: Arc<RwLock<std::collections::HashMap<String, String>>>,
}

impl ReadHeavyCache {
    async fn get(&self, key: &str) -> Option<String> {
        let cache = self.data.read().await;
        cache.get(key).cloned()
    }

    async fn insert(&self, key: String, value: String) {
        let mut cache = self.data.write().await;
        cache.insert(key, value);
    }
}

// Select for racing multiple futures
use tokio::select;

async fn fetch_from_fastest(urls: Vec<String>) -> Option<String> {
    let mut tasks = urls.into_iter()
        .map(|url| Box::pin(fetch_data(&url)))
        .collect::<Vec<_>>();

    if tasks.is_empty() {
        return None;
    }

    loop {
        select! {
            result = tasks[0], if !tasks.is_empty() => {
                if result.is_ok() {
                    return result.ok();
                }
                tasks.remove(0);
            }
            else => break,
        }
    }
    None
}
```

### 2. Python Async Patterns

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
    urls.map((url) => fetch(url).then((r) => r.json()))
  );

  return results.map((result) =>
    result.status === "fulfilled" ? result.value : new Error(result.reason)
  );
}

// Rate-limited concurrent execution
async function fetchWithConcurrencyLimit<T>(
  items: string[],
  fn: (item: string) => Promise<T>,
  limit: number
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
        1
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

#### Go Concurrency Patterns

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Basic goroutine with channel
func fetchData(url string, ch chan<- string) {
    // Simulate fetch
    time.Sleep(100 * time.Millisecond)
    ch <- fmt.Sprintf("Data from %s", url)
}

// Fan-out pattern (concurrent workers)
func fetchAll(urls []string) []string {
    ch := make(chan string, len(urls))

    for _, url := range urls {
        go fetchData(url, ch)
    }

    results := make([]string, 0, len(urls))
    for i := 0; i < len(urls); i++ {
        results = append(results, <-ch)
    }

    return results
}

// WaitGroup for synchronization
func fetchAllWithWaitGroup(urls []string) []string {
    var wg sync.WaitGroup
    results := make([]string, len(urls))

    for i, url := range urls {
        wg.Add(1)
        go func(idx int, u string) {
            defer wg.Done()
            results[idx] = fmt.Sprintf("Data from %s", u)
        }(i, url)
    }

    wg.Wait()
    return results
}

// Context for cancellation
func fetchWithTimeout(ctx context.Context, url string) (string, error) {
    ch := make(chan string, 1)

    go func() {
        time.Sleep(100 * time.Millisecond)
        ch <- fmt.Sprintf("Data from %s", url)
    }()

    select {
    case result := <-ch:
        return result, nil
    case <-ctx.Done():
        return "", ctx.Err()
    }
}

// Worker pool with buffered channel
func workerPool(jobs <-chan string, results chan<- string, numWorkers int) {
    var wg sync.WaitGroup

    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            for job := range jobs {
                results <- fmt.Sprintf("Worker %d processed %s", id, job)
            }
        }(i)
    }

    wg.Wait()
    close(results)
}

// Rate limiting with ticker
func rateLimit(urls []string, requestsPerSecond int) {
    ticker := time.NewTicker(time.Second / time.Duration(requestsPerSecond))
    defer ticker.Stop()

    for _, url := range urls {
        <-ticker.C
        go fetchData(url, nil)
    }
}

// Select for multiplexing channels
func fanIn(ch1, ch2 <-chan string) <-chan string {
    out := make(chan string)

    go func() {
        defer close(out)
        for {
            select {
            case val, ok := <-ch1:
                if !ok {
                    ch1 = nil
                } else {
                    out <- val
                }
            case val, ok := <-ch2:
                if !ok {
                    ch2 = nil
                } else {
                    out <- val
                }
            }

            if ch1 == nil && ch2 == nil {
                return
            }
        }
    }()

    return out
}

// Mutex for shared state
type SafeCounter struct {
    mu    sync.Mutex
    count int
}

func (c *SafeCounter) Inc() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *SafeCounter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}

// RWMutex for read-heavy workloads
type Cache struct {
    mu   sync.RWMutex
    data map[string]string
}

func (c *Cache) Get(key string) (string, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    val, ok := c.data[key]
    return val, ok
}

func (c *Cache) Set(key, value string) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.data[key] = value
}

// Once for one-time initialization
var (
    instance *Singleton
    once     sync.Once
)

type Singleton struct {
    value string
}

func GetInstance() *Singleton {
    once.Do(func() {
        instance = &Singleton{value: "initialized"}
    })
    return instance
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

### Data Pipeline Parallelism

Patterns for ETL, stream processing, and batch data pipelines with concurrent stages.

```python
import asyncio
from typing import AsyncIterator, Callable, TypeVar, List
from dataclasses import dataclass
import queue
import threading

T = TypeVar('T')
U = TypeVar('U')

# Async pipeline with backpressure
class AsyncPipeline:
    """
    Multi-stage async pipeline with bounded queues for backpressure.
    Each stage processes items concurrently up to worker limit.
    """
    def __init__(self, max_queue_size: int = 100):
        self.max_queue_size = max_queue_size

    async def stage(
        self,
        input_iter: AsyncIterator[T],
        transform: Callable[[T], U],
        workers: int = 4
    ) -> AsyncIterator[U]:
        """Single pipeline stage with concurrent workers."""
        queue_in = asyncio.Queue(maxsize=self.max_queue_size)
        queue_out = asyncio.Queue(maxsize=self.max_queue_size)

        # Producer: feed input queue
        async def producer():
            async for item in input_iter:
                await queue_in.put(item)
            for _ in range(workers):
                await queue_in.put(None)  # Sentinel for workers

        # Workers: transform items
        async def worker():
            while True:
                item = await queue_in.get()
                if item is None:
                    break
                try:
                    if asyncio.iscoroutinefunction(transform):
                        result = await transform(item)
                    else:
                        result = transform(item)
                    await queue_out.put(result)
                except Exception as e:
                    await queue_out.put(e)

        # Consumer: yield results
        async def consumer():
            processed = 0
            while processed < workers:
                result = await queue_out.get()
                if result is None:
                    processed += 1
                    continue
                if isinstance(result, Exception):
                    raise result
                yield result

        # Start producer and workers
        asyncio.create_task(producer())
        worker_tasks = [asyncio.create_task(worker()) for _ in range(workers)]

        # Yield from consumer
        async for item in consumer():
            yield item

        # Cleanup
        await asyncio.gather(*worker_tasks)

# Thread-based pipeline for CPU-bound work
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

class ParallelPipeline:
    """Pipeline using process pools for CPU-bound stages."""

    @staticmethod
    def map_stage(
        items: List[T],
        transform: Callable[[T], U],
        workers: int = None
    ) -> List[U]:
        """Parallel map stage using processes."""
        with ProcessPoolExecutor(max_workers=workers) as executor:
            return list(executor.map(transform, items))

    @staticmethod
    def filter_stage(
        items: List[T],
        predicate: Callable[[T], bool],
        workers: int = None
    ) -> List[T]:
        """Parallel filter stage."""
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = executor.map(lambda x: (x, predicate(x)), items)
            return [item for item, keep in results if keep]

    @staticmethod
    def reduce_stage(
        items: List[T],
        reducer: Callable[[U, T], U],
        initial: U,
        chunk_size: int = 1000
    ) -> U:
        """Parallel reduce with chunking."""
        def reduce_chunk(chunk):
            result = initial
            for item in chunk:
                result = reducer(result, item)
            return result

        chunks = [items[i:i+chunk_size] for i in range(0, len(items), chunk_size)]

        with ProcessPoolExecutor() as executor:
            partial_results = list(executor.map(reduce_chunk, chunks))

        # Final reduce of partial results
        final = initial
        for partial in partial_results:
            final = reducer(final, partial)
        return final

# Streaming pipeline with batching
class StreamingPipeline:
    """Process unbounded streams with batching and timeouts."""

    @staticmethod
    async def batch_stream(
        stream: AsyncIterator[T],
        batch_size: int = 100,
        timeout: float = 1.0
    ) -> AsyncIterator[List[T]]:
        """Collect items into batches by size or timeout."""
        batch = []
        deadline = asyncio.get_event_loop().time() + timeout

        async for item in stream:
            batch.append(item)

            if len(batch) >= batch_size:
                yield batch
                batch = []
                deadline = asyncio.get_event_loop().time() + timeout
            elif asyncio.get_event_loop().time() >= deadline:
                if batch:
                    yield batch
                    batch = []
                deadline = asyncio.get_event_loop().time() + timeout

        if batch:
            yield batch

    @staticmethod
    async def parallel_batch_process(
        batched_stream: AsyncIterator[List[T]],
        process_batch: Callable[[List[T]], List[U]],
        max_concurrent: int = 4
    ) -> AsyncIterator[U]:
        """Process batches in parallel up to concurrency limit."""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_limit(batch):
            async with semaphore:
                return await asyncio.to_thread(process_batch, batch)

        pending = set()

        async for batch in batched_stream:
            task = asyncio.create_task(process_with_limit(batch))
            pending.add(task)

            if len(pending) >= max_concurrent:
                done, pending = await asyncio.wait(
                    pending,
                    return_when=asyncio.FIRST_COMPLETED
                )
                for task in done:
                    results = await task
                    for result in results:
                        yield result

        # Drain remaining
        while pending:
            done, pending = await asyncio.wait(pending)
            for task in done:
                results = await task
                for result in results:
                    yield result

# Complete ETL example
@dataclass
class Record:
    id: int
    value: str

class ETLPipeline:
    """Complete ETL pipeline with extraction, transformation, loading."""

    async def extract(self) -> AsyncIterator[Record]:
        """Simulate data extraction from source."""
        for i in range(1000):
            await asyncio.sleep(0.001)  # Simulate I/O
            yield Record(id=i, value=f"raw_{i}")

    def transform(self, record: Record) -> Record:
        """CPU-bound transformation."""
        import hashlib
        transformed = hashlib.sha256(record.value.encode()).hexdigest()
        return Record(id=record.id, value=transformed)

    async def load_batch(self, records: List[Record]):
        """Batch load to destination."""
        await asyncio.sleep(0.1)  # Simulate batch write
        print(f"Loaded batch of {len(records)} records")

    async def run(self):
        """Execute full pipeline."""
        pipeline = AsyncPipeline()

        # Stage 1: Extract
        extracted = self.extract()

        # Stage 2: Transform (concurrent)
        transformed = pipeline.stage(extracted, self.transform, workers=8)

        # Stage 3: Batch and load
        batched = StreamingPipeline.batch_stream(transformed, batch_size=50)

        async for batch in batched:
            await self.load_batch(batch)

# Usage
async def main():
    etl = ETLPipeline()
    await etl.run()

asyncio.run(main())
```

#### Rust Data Pipeline with Rayon

```rust
use rayon::prelude::*;
use std::sync::{Arc, Mutex};

// Parallel map-reduce pipeline
fn parallel_pipeline(data: Vec<i32>) -> i32 {
    data.par_iter()
        .map(|x| x * x)           // Parallel map
        .filter(|x| x % 2 == 0)   // Parallel filter
        .sum()                     // Parallel reduce
}

// Pipeline with intermediate collection
struct Pipeline<T> {
    data: Vec<T>,
}

impl<T: Send + Sync> Pipeline<T> {
    fn new(data: Vec<T>) -> Self {
        Self { data }
    }

    fn map<U, F>(self, f: F) -> Pipeline<U>
    where
        U: Send,
        F: Fn(T) -> U + Send + Sync,
    {
        let data = self.data.into_par_iter().map(f).collect();
        Pipeline { data }
    }

    fn filter<F>(self, f: F) -> Pipeline<T>
    where
        F: Fn(&T) -> bool + Send + Sync,
    {
        let data = self.data.into_par_iter().filter(f).collect();
        Pipeline { data }
    }

    fn collect(self) -> Vec<T> {
        self.data
    }
}

// Async stream processing
use tokio::sync::mpsc;
use tokio_stream::{Stream, StreamExt};

async fn process_stream<T, U, F>(
    mut stream: impl Stream<Item = T> + Unpin,
    transform: F,
    parallelism: usize,
) -> Vec<U>
where
    T: Send + 'static,
    U: Send + 'static,
    F: Fn(T) -> U + Send + Sync + Clone + 'static,
{
    let (tx, mut rx) = mpsc::channel(100);

    let processor = tokio::spawn(async move {
        let mut results = Vec::new();
        while let Some(result) = rx.recv().await {
            results.push(result);
        }
        results
    });

    stream
        .for_each_concurrent(parallelism, |item| {
            let tx = tx.clone();
            let transform = transform.clone();
            async move {
                let result = transform(item);
                let _ = tx.send(result).await;
            }
        })
        .await;

    drop(tx);
    processor.await.unwrap()
}
```
