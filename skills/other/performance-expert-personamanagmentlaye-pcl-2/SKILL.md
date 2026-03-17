---
name: performance-expert
version: 1.0.0
description: Expert-level performance optimization, profiling, benchmarking, and tuning
category: devops
tags: [performance, optimization, profiling, benchmarking, scalability]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# Performance Expert

Expert guidance for performance optimization, profiling, benchmarking, and system tuning.

## Core Concepts

### Performance Fundamentals
- Response time vs throughput
- Latency vs bandwidth
- CPU, memory, I/O bottlenecks
- Concurrency vs parallelism
- Caching strategies
- Load balancing

### Optimization Areas
- Algorithm optimization
- Database optimization
- Network optimization
- Frontend performance
- Backend performance
- Infrastructure tuning

### Profiling Tools
- CPU profilers
- Memory profilers
- Network profilers
- Application Performance Monitoring (APM)
- Load testing tools

## Python Performance

```python
import cProfile
import pstats
import timeit
import memory_profiler
from functools import lru_cache
from typing import List
import numpy as np

# Performance Profiling
def profile_function(func):
    """Decorator for profiling function execution"""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        result = func(*args, **kwargs)

        profiler.disable()
        stats = pstats.Stats(profiler)
        stats.sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions

        return result
    return wrapper

@profile_function
def slow_function():
    total = 0
    for i in range(1000000):
        total += i
    return total

# Memoization for expensive computations
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Cached Fibonacci calculation"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Vectorization with NumPy
def slow_loop(data: List[float]) -> List[float]:
    """Slow: Using Python loops"""
    return [x ** 2 + 2 * x + 1 for x in data]

def fast_vectorized(data: np.ndarray) -> np.ndarray:
    """Fast: Using NumPy vectorization"""
    return data ** 2 + 2 * data + 1

# Benchmarking
def benchmark_function(func, *args, iterations=1000):
    """Benchmark function execution time"""
    total_time = timeit.timeit(
        lambda: func(*args),
        number=iterations
    )
    avg_time = total_time / iterations

    return {
        'total_time': total_time,
        'avg_time': avg_time,
        'iterations': iterations
    }

# Memory profiling
@memory_profiler.profile
def memory_intensive_function():
    """Function that uses significant memory"""
    data = [i for i in range(1000000)]
    return sum(data)

# Efficient string concatenation
def slow_string_concat(items: List[str]) -> str:
    """Slow: String concatenation in loop"""
    result = ""
    for item in items:
        result += item  # Creates new string each time
    return result

def fast_string_concat(items: List[str]) -> str:
    """Fast: Using join"""
    return "".join(items)

# Generator for memory efficiency
def slow_list_comprehension(n: int) -> List[int]:
    """Returns all squares at once"""
    return [i ** 2 for i in range(n)]

def fast_generator(n: int):
    """Yields squares one at a time"""
    for i in range(n):
        yield i ** 2
```

## Database Optimization

```python
from sqlalchemy import create_engine, Index, text
from sqlalchemy.orm import sessionmaker
import redis

# Connection pooling
engine = create_engine(
    'postgresql://user:pass@localhost/db',
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Query optimization
class DatabaseOptimizer:
    def __init__(self, session):
        self.session = session

    def bad_n_plus_one(self):
        """N+1 query problem"""
        users = self.session.query(User).all()
        for user in users:
            posts = user.posts  # Triggers additional query per user
            print(f"{user.name}: {len(posts)} posts")

    def good_eager_loading(self):
        """Eager loading to avoid N+1"""
        from sqlalchemy.orm import joinedload

        users = self.session.query(User)\
            .options(joinedload(User.posts))\
            .all()

        for user in users:
            posts = user.posts  # No additional query
            print(f"{user.name}: {len(posts)} posts")

    def use_indexes(self):
        """Create indexes for frequent queries"""
        # Index on frequently queried columns
        Index('idx_user_email', User.email)
        Index('idx_post_created_at', Post.created_at)

        # Composite index
        Index('idx_post_user_status', Post.user_id, Post.status)

    def batch_operations(self, items: List[dict]):
        """Batch insert instead of individual inserts"""
        # Bad: Individual inserts
        # for item in items:
        #     self.session.add(User(**item))
        #     self.session.commit()

        # Good: Batch insert
        self.session.bulk_insert_mappings(User, items)
        self.session.commit()

    def use_pagination(self, page: int = 1, page_size: int = 20):
        """Paginate large result sets"""
        offset = (page - 1) * page_size

        return self.session.query(User)\
            .order_by(User.created_at.desc())\
            .limit(page_size)\
            .offset(offset)\
            .all()

# Redis caching
class CacheOptimizer:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def cache_query_result(self, key: str, query_func, ttl: int = 3600):
        """Cache database query results"""
        # Check cache first
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)

        # Execute query
        result = query_func()

        # Cache result
        self.redis.setex(key, ttl, json.dumps(result))

        return result

    def cache_aside_pattern(self, key: str, fetch_func, ttl: int = 3600):
        """Implement cache-aside pattern"""
        data = self.redis.get(key)

        if data is None:
            data = fetch_func()
            self.redis.setex(key, ttl, json.dumps(data))
        else:
            data = json.loads(data)

        return data
```

## Frontend Performance

```javascript
// Debouncing for expensive operations
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Example: Debounce search input
const searchInput = document.getElementById('search');
const debouncedSearch = debounce((query) => {
    // Expensive search operation
    fetchSearchResults(query);
}, 300);

searchInput.addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
});

// Lazy loading images
const lazyLoadImages = () => {
    const images = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
};

// Virtual scrolling for large lists
class VirtualScroller {
    constructor(container, items, itemHeight) {
        this.container = container;
        this.items = items;
        this.itemHeight = itemHeight;
        this.visibleItems = Math.ceil(container.clientHeight / itemHeight);
        this.render();
    }

    render() {
        const scrollTop = this.container.scrollTop;
        const startIndex = Math.floor(scrollTop / this.itemHeight);
        const endIndex = startIndex + this.visibleItems;

        // Only render visible items
        const visibleData = this.items.slice(startIndex, endIndex);

        this.container.innerHTML = visibleData
            .map(item => `<div style="height: ${this.itemHeight}px">${item}</div>`)
            .join('');
    }
}

// Code splitting with dynamic imports
async function loadModule() {
    const module = await import('./heavy-module.js');
    module.init();
}
```

## API Performance

```python
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
import asyncio
from typing import AsyncGenerator

app = FastAPI()

# Async endpoints for I/O bound operations
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Async endpoint for database queries"""
    user = await db.fetch_user(user_id)
    return user

# Streaming responses for large data
async def generate_large_file() -> AsyncGenerator[bytes, None]:
    """Stream large file in chunks"""
    chunk_size = 8192
    with open("large_file.csv", "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk
            await asyncio.sleep(0)  # Allow other tasks to run

@app.get("/download")
async def download_large_file():
    return StreamingResponse(
        generate_large_file(),
        media_type="text/csv"
    )

# Background tasks for long-running operations
@app.post("/process")
async def process_data(background_tasks: BackgroundTasks):
    """Offload heavy processing to background"""
    background_tasks.add_task(heavy_processing_task)
    return {"status": "processing started"}

# Connection pooling
import aiohttp

class APIClient:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=100)
        )
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    async def fetch(self, url: str):
        async with self.session.get(url) as response:
            return await response.json()
```

## Load Testing

```python
from locust import HttpUser, task, between

class PerformanceTest(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_users(self):
        """High frequency endpoint"""
        self.client.get("/api/users")

    @task(1)
    def create_user(self):
        """Lower frequency endpoint"""
        self.client.post("/api/users", json={
            "email": "test@example.com",
            "name": "Test User"
        })

    def on_start(self):
        """Login once per user"""
        response = self.client.post("/api/login", json={
            "username": "test",
            "password": "password"
        })
        self.token = response.json()["token"]
```

## Best Practices

### General
- Measure before optimizing
- Focus on bottlenecks
- Use appropriate data structures
- Cache expensive computations
- Minimize I/O operations
- Use connection pooling
- Implement pagination

### Database
- Create proper indexes
- Avoid N+1 queries
- Use eager loading
- Batch operations
- Optimize queries
- Use read replicas
- Implement caching

### Frontend
- Minimize bundle size
- Code splitting
- Lazy loading
- Compress assets
- Use CDN
- Optimize images
- Debounce/throttle events

### Backend
- Use async for I/O
- Implement caching
- Connection pooling
- Background processing
- Horizontal scaling
- Load balancing

## Anti-Patterns

❌ Premature optimization
❌ No profiling/measurement
❌ Optimizing wrong bottlenecks
❌ Ignoring caching
❌ Synchronous I/O operations
❌ No database indexes
❌ Loading all data at once

## Resources

- Python Performance Tips: https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- Web Performance: https://web.dev/performance/
- Locust Load Testing: https://locust.io/
- py-spy Profiler: https://github.com/benfred/py-spy
- Chrome DevTools: https://developer.chrome.com/docs/devtools/
