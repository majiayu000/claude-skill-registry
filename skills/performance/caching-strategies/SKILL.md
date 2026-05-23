---
name: caching-strategies
description: Backend caching patterns with Redis including write-through, write-behind, cache-aside, and invalidation strategies. Use when implementing Redis cache, managing TTL/expiration, preventing cache stampede, or optimizing cache hit rates.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
tags: [caching, redis, performance, fastapi, python, 2026]
author: SkillForge
user-invocable: false
---

# Backend Caching Strategies

Optimize performance with Redis caching patterns and smart invalidation.

## Pattern Selection

| Pattern | Write | Read | Consistency | Use Case |
|---------|-------|------|-------------|----------|
| Cache-Aside | DB first | Cache → DB | Eventual | General purpose |
| Write-Through | Cache + DB | Cache | Strong | Critical data |
| Write-Behind | Cache, async DB | Cache | Eventual | High write load |
| Read-Through | Cache handles | Cache → DB | Eventual | Simplified reads |

## Cache-Aside (Lazy Loading)

```python
import redis.asyncio as redis
from typing import TypeVar, Callable
import json

T = TypeVar("T")

class CacheAside:
    def __init__(self, redis_client: redis.Redis, default_ttl: int = 3600):
        self.redis = redis_client
        self.ttl = default_ttl

    async def get_or_set(
        self,
        key: str,
        fetch_fn: Callable[[], T],
        ttl: int | None = None,
        serialize: Callable[[T], str] = json.dumps,
        deserialize: Callable[[str], T] = json.loads,
    ) -> T:
        """Get from cache, or fetch and cache."""
        # Try cache first
        cached = await self.redis.get(key)
        if cached:
            return deserialize(cached)

        # Cache miss - fetch from source
        value = await fetch_fn()

        # Store in cache
        await self.redis.setex(
            key,
            ttl or self.ttl,
            serialize(value),
        )
        return value

# Usage
cache = CacheAside(redis_client)

async def get_analysis(analysis_id: str) -> Analysis:
    return await cache.get_or_set(
        key=f"analysis:{analysis_id}",
        fetch_fn=lambda: repo.get_by_id(analysis_id),
        ttl=1800,  # 30 minutes
    )
```

## Write-Through Cache

```python
class WriteThroughCache:
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl

    async def write(
        self,
        key: str,
        value: T,
        db_write_fn: Callable[[T], Awaitable[T]],
    ) -> T:
        """Write to both cache and database synchronously."""
        # Write to database first (consistency)
        result = await db_write_fn(value)

        # Then update cache
        await self.redis.setex(key, self.ttl, json.dumps(result))

        return result

    async def read(self, key: str) -> T | None:
        """Read from cache only."""
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None

# Usage
cache = WriteThroughCache(redis_client)

async def update_analysis(analysis_id: str, data: AnalysisUpdate) -> Analysis:
    return await cache.write(
        key=f"analysis:{analysis_id}",
        value=data,
        db_write_fn=lambda d: repo.update(analysis_id, d),
    )
```

## Write-Behind (Write-Back)

```python
import asyncio
from collections import deque

class WriteBehindCache:
    def __init__(
        self,
        redis_client: redis.Redis,
        flush_interval: float = 5.0,
        batch_size: int = 100,
    ):
        self.redis = redis_client
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self._pending_writes: deque = deque()
        self._flush_task: asyncio.Task | None = None

    async def start(self):
        """Start background flush task."""
        self._flush_task = asyncio.create_task(self._flush_loop())

    async def stop(self):
        """Stop and flush remaining writes."""
        if self._flush_task:
            self._flush_task.cancel()
        await self._flush_pending()

    async def write(self, key: str, value: T) -> None:
        """Write to cache immediately, queue for DB."""
        await self.redis.set(key, json.dumps(value))
        self._pending_writes.append((key, value))

        if len(self._pending_writes) >= self.batch_size:
            await self._flush_pending()

    async def _flush_loop(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            await self._flush_pending()

    async def _flush_pending(self):
        if not self._pending_writes:
            return

        batch = []
        while self._pending_writes and len(batch) < self.batch_size:
            batch.append(self._pending_writes.popleft())

        # Bulk write to database
        await repo.bulk_upsert([v for _, v in batch])
```

## Cache Invalidation Patterns

### TTL-Based (Time to Live)

```python
# Simple TTL
await redis.setex("analysis:123", 3600, data)  # 1 hour

# TTL with jitter (prevent stampede)
import random
base_ttl = 3600
jitter = random.randint(-300, 300)  # ±5 minutes
await redis.setex("analysis:123", base_ttl + jitter, data)
```

### Event-Based Invalidation

```python
class CacheInvalidator:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def invalidate(self, key: str) -> None:
        """Delete single key."""
        await self.redis.delete(key)

    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete keys matching pattern."""
        keys = []
        async for key in self.redis.scan_iter(match=pattern):
            keys.append(key)

        if keys:
            return await self.redis.delete(*keys)
        return 0

    async def invalidate_tags(self, *tags: str) -> int:
        """Invalidate all keys with given tags."""
        count = 0
        for tag in tags:
            tag_key = f"tag:{tag}"
            members = await self.redis.smembers(tag_key)
            if members:
                count += await self.redis.delete(*members)
            await self.redis.delete(tag_key)
        return count

# Usage with tags
async def cache_with_tags(key: str, value: T, tags: list[str]):
    await redis.set(key, json.dumps(value))
    for tag in tags:
        await redis.sadd(f"tag:{tag}", key)

# Invalidate by tag
await invalidator.invalidate_tags("user:123", "analyses")
```

### Version-Based Invalidation

```python
class VersionedCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get_version(self, namespace: str) -> int:
        version = await self.redis.get(f"version:{namespace}")
        return int(version) if version else 1

    async def increment_version(self, namespace: str) -> int:
        return await self.redis.incr(f"version:{namespace}")

    def make_key(self, namespace: str, key: str, version: int) -> str:
        return f"{namespace}:v{version}:{key}"

    async def get(self, namespace: str, key: str) -> T | None:
        version = await self.get_version(namespace)
        full_key = self.make_key(namespace, key, version)
        cached = await self.redis.get(full_key)
        return json.loads(cached) if cached else None

    async def invalidate_namespace(self, namespace: str) -> None:
        """Increment version to invalidate all keys."""
        await self.increment_version(namespace)
```

## Cache Stampede Prevention

```python
import asyncio
from contextlib import asynccontextmanager

class StampedeProtection:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self._local_locks: dict[str, asyncio.Lock] = {}

    @asynccontextmanager
    async def lock(self, key: str, timeout: int = 10):
        """Distributed lock to prevent stampede."""
        lock_key = f"lock:{key}"

        # Try to acquire distributed lock
        acquired = await self.redis.set(
            lock_key, "1", nx=True, ex=timeout
        )

        if not acquired:
            # Wait for existing computation
            for _ in range(timeout * 10):
                if await self.redis.exists(key):
                    return  # Data available
                await asyncio.sleep(0.1)
            raise TimeoutError(f"Lock timeout for {key}")

        try:
            yield
        finally:
            await self.redis.delete(lock_key)

# Usage
async def get_expensive_data(key: str) -> Data:
    cached = await redis.get(key)
    if cached:
        return json.loads(cached)

    async with stampede.lock(key):
        # Double-check after acquiring lock
        cached = await redis.get(key)
        if cached:
            return json.loads(cached)

        # Compute expensive data
        data = await compute_expensive_data()
        await redis.setex(key, 3600, json.dumps(data))
        return data
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER cache without TTL (memory leak)
await redis.set("key", value)  # No expiration!

# NEVER cache sensitive data without encryption
await redis.set("user:123:password", password)

# NEVER use cache as primary storage
await redis.set("order:123", order_data)
# ... database write fails, data lost!

# NEVER ignore cache failures
try:
    await redis.get(key)
except:
    pass  # Silent failure = stale data
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Default TTL | 1 hour for most data, 5 min for volatile |
| Serialization | orjson for performance |
| Key naming | `{entity}:{id}` or `{entity}:{id}:{field}` |
| Stampede | Use locks for expensive computations |
| Invalidation | Event-based for writes, TTL for reads |

## Related Skills

- `redis-patterns` - Advanced Redis usage
- `resilience-patterns` - Fallback strategies
- `observability-monitoring` - Cache hit metrics

## Capability Details

### cache-aside
**Keywords:** cache aside, lazy loading, cache miss, get or set
**Solves:**
- How to implement lazy loading cache?
- Cache on read pattern

### write-through
**Keywords:** write through, cache consistency, synchronous cache
**Solves:**
- How to keep cache consistent with database?
- Strong consistency caching

### write-behind
**Keywords:** write behind, write back, async cache, batch writes
**Solves:**
- High write throughput caching
- Async database writes

### cache-invalidation
**Keywords:** invalidation, cache bust, TTL, cache tags
**Solves:**
- How to invalidate cache?
- When to expire cached data

### stampede-prevention
**Keywords:** stampede, thundering herd, cache lock, singleflight
**Solves:**
- Prevent cache stampede
- Multiple requests hitting DB
