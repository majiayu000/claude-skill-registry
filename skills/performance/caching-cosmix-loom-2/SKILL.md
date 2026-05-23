---
name: caching
description: Comprehensive caching strategies and patterns for performance optimization. Use when implementing cache layers, cache invalidation, TTL policies, or distributed caching. Covers Redis/Memcached patterns, CDN caching, database query caching, ML model caching, and eviction policies. Triggers: cache, caching, Redis, Memcached, CDN, TTL, invalidation, eviction, LRU, LFU, FIFO, write-through, write-behind, cache-aside, read-through, cache stampede, distributed cache, local cache, memoization, query cache, result cache, edge cache, browser cache, HTTP cache.
---

# Caching

## Overview

Caching improves application performance by storing frequently accessed data closer to the consumer. This skill covers cache strategies (aside, through, behind), invalidation patterns, TTL management, Redis/Memcached usage, stampede prevention, and distributed caching.

## Instructions

### 1. Cache Strategies

#### Cache-Aside (Lazy Loading)

```python
from typing import TypeVar, Optional, Callable
import json

T = TypeVar('T')

class CacheAside:
    """Application manages cache explicitly."""

    def __init__(self, cache_client, default_ttl: int = 3600):
        self.cache = cache_client
        self.default_ttl = default_ttl

    async def get_or_load(
        self,
        key: str,
        loader: Callable[[], T],
        ttl: Optional[int] = None
    ) -> T:
        # Try cache first
        cached = await self.cache.get(key)
        if cached is not None:
            return json.loads(cached)

        # Load from source
        value = await loader()

        # Store in cache
        await self.cache.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )

        return value

    async def invalidate(self, key: str):
        await self.cache.delete(key)

# Usage
cache = CacheAside(redis_client)

async def get_user(user_id: str) -> User:
    return await cache.get_or_load(
        f"user:{user_id}",
        lambda: database.get_user(user_id),
        ttl=300
    )
```

#### Write-Through Cache

```python
class WriteThrough:
    """Writes go to cache and database simultaneously."""

    def __init__(self, cache_client, database, default_ttl: int = 3600):
        self.cache = cache_client
        self.database = database
        self.default_ttl = default_ttl

    async def write(self, key: str, value: any, ttl: Optional[int] = None):
        # Write to database first
        await self.database.save(key, value)

        # Then update cache
        await self.cache.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )

    async def read(self, key: str) -> Optional[any]:
        cached = await self.cache.get(key)
        if cached:
            return json.loads(cached)

        # Fallback to database
        value = await self.database.get(key)
        if value:
            await self.cache.setex(key, self.default_ttl, json.dumps(value))
        return value
```

#### Write-Behind (Write-Back) Cache

```python
import asyncio
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Any
import time

@dataclass
class PendingWrite:
    key: str
    value: Any
    timestamp: float

class WriteBehind:
    """Writes go to cache immediately, database asynchronously."""

    def __init__(
        self,
        cache_client,
        database,
        flush_interval: float = 5.0,
        batch_size: int = 100
    ):
        self.cache = cache_client
        self.database = database
        self.flush_interval = flush_interval
        self.batch_size = batch_size
        self.pending_writes: Dict[str, PendingWrite] = {}
        self._lock = asyncio.Lock()
        self._flush_task = None

    async def start(self):
        self._flush_task = asyncio.create_task(self._flush_loop())

    async def stop(self):
        if self._flush_task:
            self._flush_task.cancel()
            await self._flush_pending()

    async def write(self, key: str, value: Any):
        # Write to cache immediately
        await self.cache.set(key, json.dumps(value))

        # Queue for database write
        async with self._lock:
            self.pending_writes[key] = PendingWrite(
                key=key,
                value=value,
                timestamp=time.time()
            )

        if len(self.pending_writes) >= self.batch_size:
            await self._flush_pending()

    async def _flush_loop(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            await self._flush_pending()

    async def _flush_pending(self):
        async with self._lock:
            if not self.pending_writes:
                return

            writes = list(self.pending_writes.values())
            self.pending_writes.clear()

        # Batch write to database
        await self.database.batch_save(
            [(w.key, w.value) for w in writes]
        )
```

#### Read-Through Cache

```python
class ReadThrough:
    """Cache automatically loads from database on miss."""

    def __init__(self, cache_client, loader, default_ttl: int = 3600):
        self.cache = cache_client
        self.loader = loader
        self.default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        # Check cache
        cached = await self.cache.get(key)
        if cached:
            return json.loads(cached)

        # Auto-load on miss
        value = await self.loader(key)
        if value is not None:
            await self.cache.setex(key, self.default_ttl, json.dumps(value))

        return value
```

### 2. Invalidation Strategies

```python
from enum import Enum
from typing import Set, List
import fnmatch

class InvalidationStrategy(Enum):
    TIME_BASED = "time_based"
    EVENT_BASED = "event_based"
    VERSION_BASED = "version_based"

class CacheInvalidator:
    def __init__(self, cache_client):
        self.cache = cache_client
        self._tag_index: Dict[str, Set[str]] = defaultdict(set)

    # Tag-based invalidation
    async def set_with_tags(
        self,
        key: str,
        value: Any,
        tags: List[str],
        ttl: int = 3600
    ):
        await self.cache.setex(key, ttl, json.dumps(value))

        for tag in tags:
            self._tag_index[tag].add(key)
            await self.cache.sadd(f"tag:{tag}", key)

    async def invalidate_by_tag(self, tag: str):
        keys = await self.cache.smembers(f"tag:{tag}")
        if keys:
            await self.cache.delete(*keys)
            await self.cache.delete(f"tag:{tag}")

    # Pattern-based invalidation
    async def invalidate_by_pattern(self, pattern: str):
        cursor = 0
        while True:
            cursor, keys = await self.cache.scan(
                cursor,
                match=pattern,
                count=100
            )
            if keys:
                await self.cache.delete(*keys)
            if cursor == 0:
                break

    # Version-based invalidation
    async def get_versioned(self, key: str, version: int) -> Optional[Any]:
        versioned_key = f"{key}:v{version}"
        return await self.cache.get(versioned_key)

    async def set_versioned(
        self,
        key: str,
        value: Any,
        version: int,
        ttl: int = 3600
    ):
        versioned_key = f"{key}:v{version}"
        await self.cache.setex(versioned_key, ttl, json.dumps(value))

# Event-based invalidation with pub/sub
class EventBasedInvalidator:
    def __init__(self, cache_client, pubsub_client):
        self.cache = cache_client
        self.pubsub = pubsub_client

    async def start_listener(self):
        await self.pubsub.subscribe("cache:invalidate")

        async for message in self.pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                await self._handle_invalidation(data)

    async def _handle_invalidation(self, data: dict):
        if "key" in data:
            await self.cache.delete(data["key"])
        elif "pattern" in data:
            await self.invalidate_by_pattern(data["pattern"])
        elif "tag" in data:
            await self.invalidate_by_tag(data["tag"])

    async def publish_invalidation(self, **kwargs):
        await self.pubsub.publish(
            "cache:invalidate",
            json.dumps(kwargs)
        )
```

### 3. TTL and Expiration

```python
import random
from datetime import datetime, timedelta

class TTLManager:
    def __init__(self, base_ttl: int = 3600):
        self.base_ttl = base_ttl

    def get_ttl_with_jitter(self, ttl: Optional[int] = None) -> int:
        """Add randomness to prevent synchronized expiration."""
        base = ttl or self.base_ttl
        jitter = random.uniform(-0.1, 0.1) * base
        return int(base + jitter)

    def get_sliding_ttl(
        self,
        last_access: datetime,
        min_ttl: int = 60,
        max_ttl: int = 3600
    ) -> int:
        """TTL based on access frequency."""
        age = (datetime.utcnow() - last_access).total_seconds()

        if age < 60:
            return max_ttl  # Frequently accessed
        elif age < 300:
            return max_ttl // 2
        else:
            return min_ttl

    def get_tiered_ttl(self, data_type: str) -> int:
        """Different TTL for different data types."""
        ttl_tiers = {
            "user_session": 86400,      # 1 day
            "user_profile": 3600,       # 1 hour
            "product_catalog": 300,     # 5 minutes
            "search_results": 60,       # 1 minute
            "real_time_data": 10,       # 10 seconds
        }
        return ttl_tiers.get(data_type, self.base_ttl)

# Sliding window expiration
class SlidingCache:
    def __init__(self, cache_client, default_ttl: int = 3600):
        self.cache = cache_client
        self.default_ttl = default_ttl

    async def get(self, key: str) -> Optional[Any]:
        value = await self.cache.get(key)
        if value:
            # Refresh TTL on access
            await self.cache.expire(key, self.default_ttl)
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        await self.cache.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(value)
        )
```

### 4. Redis/Memcached Patterns

```python
import redis.asyncio as redis
from typing import List, Tuple

class RedisCache:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    # Hash operations for structured data
    async def set_hash(self, key: str, data: dict, ttl: int = 3600):
        await self.redis.hset(key, mapping=data)
        await self.redis.expire(key, ttl)

    async def get_hash(self, key: str) -> Optional[dict]:
        data = await self.redis.hgetall(key)
        return {k.decode(): v.decode() for k, v in data.items()} if data else None

    async def update_hash_field(self, key: str, field: str, value: str):
        await self.redis.hset(key, field, value)

    # Sorted sets for leaderboards/rankings
    async def add_to_ranking(self, key: str, member: str, score: float):
        await self.redis.zadd(key, {member: score})

    async def get_top_n(self, key: str, n: int) -> List[Tuple[str, float]]:
        return await self.redis.zrevrange(key, 0, n - 1, withscores=True)

    # Lists for queues
    async def push_to_queue(self, key: str, *values):
        await self.redis.lpush(key, *values)

    async def pop_from_queue(self, key: str, timeout: int = 0):
        return await self.redis.brpop(key, timeout=timeout)

    # Pub/Sub for cache invalidation
    async def publish(self, channel: str, message: str):
        await self.redis.publish(channel, message)

    # Lua scripts for atomic operations
    async def increment_with_cap(self, key: str, cap: int) -> int:
        script = """
        local current = redis.call('GET', KEYS[1])
        if current and tonumber(current) >= tonumber(ARGV[1]) then
            return -1
        end
        return redis.call('INCR', KEYS[1])
        """
        return await self.redis.eval(script, 1, key, cap)

    # Pipeline for batch operations
    async def batch_get(self, keys: List[str]) -> List[Optional[str]]:
        async with self.redis.pipeline() as pipe:
            for key in keys:
                pipe.get(key)
            return await pipe.execute()

    async def batch_set(
        self,
        items: List[Tuple[str, str]],
        ttl: int = 3600
    ):
        async with self.redis.pipeline() as pipe:
            for key, value in items:
                pipe.setex(key, ttl, value)
            await pipe.execute()
```

### 5. Cache Stampede Prevention

```python
import asyncio
import hashlib
import time
from typing import Optional, Callable

class StampedeProtection:
    """Prevents cache stampede using various strategies."""

    def __init__(self, cache_client):
        self.cache = cache_client
        self._locks: Dict[str, asyncio.Lock] = {}

    # Strategy 1: Locking (prevents concurrent regeneration)
    async def get_with_lock(
        self,
        key: str,
        loader: Callable,
        ttl: int = 3600
    ) -> Any:
        cached = await self.cache.get(key)
        if cached:
            return json.loads(cached)

        # Get or create lock for this key
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()

        async with self._locks[key]:
            # Double-check after acquiring lock
            cached = await self.cache.get(key)
            if cached:
                return json.loads(cached)

            value = await loader()
            await self.cache.setex(key, ttl, json.dumps(value))
            return value

    # Strategy 2: Probabilistic early expiration
    async def get_with_early_recompute(
        self,
        key: str,
        loader: Callable,
        ttl: int = 3600,
        beta: float = 1.0
    ) -> Any:
        data = await self.cache.get(key)

        if data:
            cached = json.loads(data)
            expiry = cached.get("_expiry", 0)
            delta = cached.get("_delta", 0)

            # Probabilistic early recomputation
            now = time.time()
            if now - delta * beta * random.random() < expiry:
                return cached["value"]

        # Recompute
        start = time.time()
        value = await loader()
        delta = time.time() - start

        cache_data = {
            "value": value,
            "_expiry": time.time() + ttl,
            "_delta": delta
        }
        await self.cache.setex(key, ttl, json.dumps(cache_data))
        return value

    # Strategy 3: Stale-while-revalidate
    async def get_stale_while_revalidate(
        self,
        key: str,
        loader: Callable,
        ttl: int = 3600,
        stale_ttl: int = 300
    ) -> Any:
        data = await self.cache.get(key)

        if data:
            cached = json.loads(data)

            if cached.get("_fresh", True):
                return cached["value"]

            # Return stale, revalidate in background
            asyncio.create_task(self._revalidate(key, loader, ttl, stale_ttl))
            return cached["value"]

        return await self._load_and_cache(key, loader, ttl, stale_ttl)

    async def _revalidate(
        self,
        key: str,
        loader: Callable,
        ttl: int,
        stale_ttl: int
    ):
        lock_key = f"lock:{key}"
        acquired = await self.cache.setnx(lock_key, "1")

        if acquired:
            try:
                await self.cache.expire(lock_key, 30)
                await self._load_and_cache(key, loader, ttl, stale_ttl)
            finally:
                await self.cache.delete(lock_key)

    async def _load_and_cache(
        self,
        key: str,
        loader: Callable,
        ttl: int,
        stale_ttl: int
    ):
        value = await loader()

        cache_data = {"value": value, "_fresh": True}
        await self.cache.setex(key, ttl, json.dumps(cache_data))

        # Mark as stale after TTL
        async def mark_stale():
            await asyncio.sleep(ttl - stale_ttl)
            data = await self.cache.get(key)
            if data:
                cached = json.loads(data)
                cached["_fresh"] = False
                await self.cache.setex(key, stale_ttl, json.dumps(cached))

        asyncio.create_task(mark_stale())
        return value
```

### 6. Distributed Caching

```python
import hashlib
from typing import List, Optional
import random

class ConsistentHashing:
    """Consistent hashing for distributed cache nodes."""

    def __init__(self, nodes: List[str], replicas: int = 100):
        self.replicas = replicas
        self.ring: Dict[int, str] = {}
        self.sorted_keys: List[int] = []

        for node in nodes:
            self.add_node(node)

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            self.ring[key] = node
            self.sorted_keys.append(key)
        self.sorted_keys.sort()

    def remove_node(self, node: str):
        for i in range(self.replicas):
            key = self._hash(f"{node}:{i}")
            del self.ring[key]
            self.sorted_keys.remove(key)

    def get_node(self, key: str) -> str:
        if not self.ring:
            raise ValueError("No nodes in ring")

        h = self._hash(key)

        for ring_key in self.sorted_keys:
            if h <= ring_key:
                return self.ring[ring_key]

        return self.ring[self.sorted_keys[0]]

class DistributedCache:
    """Distributed cache with consistent hashing."""

    def __init__(self, nodes: List[str]):
        self.ring = ConsistentHashing(nodes)
        self.clients: Dict[str, RedisCache] = {
            node: RedisCache(node) for node in nodes
        }

    def _get_client(self, key: str) -> RedisCache:
        node = self.ring.get_node(key)
        return self.clients[node]

    async def get(self, key: str) -> Optional[str]:
        client = self._get_client(key)
        return await client.redis.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600):
        client = self._get_client(key)
        await client.redis.setex(key, ttl, value)

    async def delete(self, key: str):
        client = self._get_client(key)
        await client.redis.delete(key)

    # Multi-get across nodes
    async def mget(self, keys: List[str]) -> Dict[str, Optional[str]]:
        # Group keys by node
        node_keys: Dict[str, List[str]] = defaultdict(list)
        for key in keys:
            node = self.ring.get_node(key)
            node_keys[node].append(key)

        # Fetch in parallel
        results = {}
        tasks = []

        for node, node_key_list in node_keys.items():
            client = self.clients[node]
            tasks.append(self._fetch_from_node(client, node_key_list, results))

        await asyncio.gather(*tasks)
        return results

    async def _fetch_from_node(
        self,
        client: RedisCache,
        keys: List[str],
        results: Dict
    ):
        values = await client.batch_get(keys)
        for key, value in zip(keys, values):
            results[key] = value
```

### 7. Database Query Caching

```python
import sqlalchemy
from typing import Optional, List, Any
import hashlib

class QueryCache:
    """Database query result caching with automatic invalidation."""

    def __init__(self, cache_client, default_ttl: int = 300):
        self.cache = cache_client
        self.default_ttl = default_ttl

    def _query_key(self, sql: str, params: tuple) -> str:
        """Generate cache key from SQL and parameters."""
        query_str = f"{sql}:{params}"
        return f"query:{hashlib.md5(query_str.encode()).hexdigest()}"

    async def execute_cached(
        self,
        session,
        query,
        params: Optional[dict] = None,
        ttl: Optional[int] = None
    ) -> List[Any]:
        sql_str = str(query)
        cache_key = self._query_key(sql_str, tuple(sorted((params or {}).items())))

        # Check cache
        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)

        # Execute query
        result = session.execute(query, params).fetchall()
        serialized = [dict(row) for row in result]

        # Cache result
        await self.cache.setex(
            cache_key,
            ttl or self.default_ttl,
            json.dumps(serialized)
        )

        return serialized

    async def invalidate_table(self, table_name: str):
        """Invalidate all queries for a table."""
        pattern = f"query:*{table_name}*"
        await self.cache.delete_pattern(pattern)

# ORM-level caching with SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import Session

class ORMCache:
    def __init__(self, cache_client):
        self.cache = cache_client

    def setup_listeners(self, engine):
        """Set up automatic cache invalidation on writes."""

        @event.listens_for(Session, "after_flush")
        def receive_after_flush(session, flush_context):
            # Invalidate cache for modified tables
            for obj in session.dirty | session.new | session.deleted:
                table = obj.__tablename__
                asyncio.create_task(
                    self.cache.delete_pattern(f"query:*{table}*")
                )

    async def get_by_id(self, model, obj_id: int, session):
        key = f"{model.__tablename__}:{obj_id}"
        cached = await self.cache.get(key)

        if cached:
            return json.loads(cached)

        obj = session.query(model).get(obj_id)
        if obj:
            await self.cache.setex(key, 3600, json.dumps(obj.to_dict()))

        return obj
```

### 8. CDN and Static Asset Caching

```python
from datetime import datetime, timedelta
from typing import Dict, Optional

class CDNCache:
    """CDN caching strategies with proper headers."""

    @staticmethod
    def get_cache_headers(
        cache_type: str,
        max_age: int = 3600
    ) -> Dict[str, str]:
        """Generate appropriate HTTP cache headers."""

        strategies = {
            "immutable": {
                "Cache-Control": f"public, max-age={max_age}, immutable",
                "Expires": (datetime.utcnow() + timedelta(seconds=max_age)).strftime(
                    "%a, %d %b %Y %H:%M:%S GMT"
                ),
            },
            "versioned": {
                "Cache-Control": f"public, max-age={max_age}",
                "ETag": None,  # Set dynamically
            },
            "revalidate": {
                "Cache-Control": "public, max-age=0, must-revalidate",
                "ETag": None,  # Set dynamically
            },
            "private": {
                "Cache-Control": "private, max-age=0, must-revalidate",
                "Pragma": "no-cache",
            },
            "no-cache": {
                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        }

        return strategies.get(cache_type, strategies["revalidate"])

    @staticmethod
    def generate_etag(content: bytes) -> str:
        """Generate ETag from content hash."""
        return hashlib.md5(content).hexdigest()

# FastAPI/Flask example
from fastapi import Response
from fastapi.responses import FileResponse

class StaticAssetCache:
    def __init__(self, cdn_base_url: Optional[str] = None):
        self.cdn_base_url = cdn_base_url

    def serve_asset(
        self,
        file_path: str,
        asset_type: str = "immutable"
    ) -> FileResponse:
        """Serve static asset with caching headers."""

        with open(file_path, "rb") as f:
            content = f.read()

        headers = CDNCache.get_cache_headers(
            asset_type,
            max_age=31536000 if asset_type == "immutable" else 3600
        )

        # Add ETag for versioned assets
        if asset_type in ["versioned", "revalidate"]:
            headers["ETag"] = f'"{CDNCache.generate_etag(content)}"'

        return FileResponse(
            file_path,
            headers=headers,
            media_type=self._get_media_type(file_path)
        )

    def get_asset_url(self, path: str, version: Optional[str] = None) -> str:
        """Generate CDN URL with optional versioning."""
        base = self.cdn_base_url or ""

        if version:
            # Append version to filename for cache busting
            parts = path.rsplit(".", 1)
            path = f"{parts[0]}.{version}.{parts[1]}"

        return f"{base}/{path}"

    @staticmethod
    def _get_media_type(file_path: str) -> str:
        ext_to_mime = {
            ".js": "application/javascript",
            ".css": "text/css",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".woff2": "font/woff2",
        }
        ext = file_path[file_path.rfind("."):]
        return ext_to_mime.get(ext, "application/octet-stream")
```

### 9. ML Model Caching

```python
import pickle
from typing import Any, Callable
import numpy as np

class MLModelCache:
    """Caching for machine learning models and predictions."""

    def __init__(self, cache_client, model_store_path: str = "./models"):
        self.cache = cache_client
        self.model_store = model_store_path

    async def get_model(self, model_id: str, version: str):
        """Load model from cache or disk."""
        key = f"model:{model_id}:v{version}"

        cached = await self.cache.get(key)
        if cached:
            return pickle.loads(cached)

        # Load from disk
        path = f"{self.model_store}/{model_id}/{version}/model.pkl"
        with open(path, "rb") as f:
            model = pickle.load(f)

        # Cache serialized model (use compression for large models)
        await self.cache.setex(
            key,
            86400,  # 1 day
            pickle.dumps(model)
        )

        return model

    async def cache_prediction(
        self,
        model_id: str,
        input_hash: str,
        prediction: Any,
        ttl: int = 3600
    ):
        """Cache prediction results."""
        key = f"pred:{model_id}:{input_hash}"
        await self.cache.setex(key, ttl, json.dumps(prediction))

    async def get_cached_prediction(
        self,
        model_id: str,
        input_data: Any
    ) -> Optional[Any]:
        """Retrieve cached prediction if available."""
        input_hash = hashlib.md5(
            json.dumps(input_data, sort_keys=True).encode()
        ).hexdigest()

        key = f"pred:{model_id}:{input_hash}"
        cached = await self.cache.get(key)

        return json.loads(cached) if cached else None

# Feature caching for ML pipelines
class FeatureCache:
    def __init__(self, cache_client):
        self.cache = cache_client

    async def get_features(
        self,
        entity_id: str,
        feature_names: List[str],
        compute_fn: Callable
    ) -> Dict[str, Any]:
        """Get features from cache or compute."""

        # Try to get from cache
        keys = [f"feature:{entity_id}:{name}" for name in feature_names]
        cached_values = await self.cache.mget(keys)

        features = {}
        missing = []

        for name, value in zip(feature_names, cached_values):
            if value:
                features[name] = json.loads(value)
            else:
                missing.append(name)

        # Compute missing features
        if missing:
            computed = await compute_fn(entity_id, missing)

            # Cache computed features
            for name, value in computed.items():
                key = f"feature:{entity_id}:{name}"
                await self.cache.setex(key, 3600, json.dumps(value))
                features[name] = value

        return features

# Embeddings cache for vector similarity
class EmbeddingCache:
    def __init__(self, cache_client):
        self.cache = cache_client

    async def get_embedding(
        self,
        text: str,
        model: str,
        embed_fn: Callable
    ) -> np.ndarray:
        """Get or compute text embedding."""

        text_hash = hashlib.md5(text.encode()).hexdigest()
        key = f"embed:{model}:{text_hash}"

        cached = await self.cache.get(key)
        if cached:
            return np.frombuffer(cached, dtype=np.float32)

        embedding = await embed_fn(text)

        # Store as binary
        await self.cache.setex(
            key,
            86400 * 7,  # 1 week
            embedding.tobytes()
        )

        return embedding
```

### 10. Local In-Memory Caching

```python
from collections import OrderedDict
from threading import RLock
from typing import Optional
import time

class LRUCache:
    """Thread-safe LRU cache with TTL support."""

    def __init__(self, capacity: int = 1000, default_ttl: Optional[int] = None):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.lock = RLock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key not in self.cache:
                return None

            value, expiry = self.cache[key]

            # Check expiration
            if expiry and time.time() > expiry:
                del self.cache[key]
                return None

            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return value

    def put(self, key: str, value: Any, ttl: Optional[int] = None):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)

            ttl = ttl or self.default_ttl
            expiry = time.time() + ttl if ttl else None
            self.cache[key] = (value, expiry)

            if len(self.cache) > self.capacity:
                # Remove oldest (least recently used)
                self.cache.popitem(last=False)

    def invalidate(self, key: str):
        with self.lock:
            self.cache.pop(key, None)

    def clear(self):
        with self.lock:
            self.cache.clear()

# Function memoization decorator
from functools import wraps

def memoize(ttl: Optional[int] = None, maxsize: int = 128):
    """Memoization decorator with TTL."""

    cache = LRUCache(capacity=maxsize, default_ttl=ttl)

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args
            key = f"{func.__name__}:{args}:{sorted(kwargs.items())}"

            result = cache.get(key)
            if result is not None:
                return result

            result = func(*args, **kwargs)
            cache.put(key, result)
            return result

        wrapper.cache_clear = cache.clear
        wrapper.cache_info = lambda: {
            "size": len(cache.cache),
            "maxsize": cache.capacity
        }

        return wrapper

    return decorator

# Usage
@memoize(ttl=300, maxsize=1000)
def expensive_computation(x: int, y: int) -> int:
    return x ** y
```

## Best Practices

1. **Cache What Matters**: Focus on frequently accessed, expensive-to-compute data.

2. **Set Appropriate TTLs**: Balance freshness vs performance. Use jitter to prevent thundering herd.

3. **Handle Cache Failures Gracefully**: Cache should enhance, not be required for operation.

4. **Monitor Cache Performance**: Track hit rates, latency, and memory usage.

5. **Use Appropriate Data Structures**: Hashes for objects, sorted sets for rankings, lists for queues.

6. **Implement Proper Invalidation**: Prefer event-driven invalidation over TTL alone for critical data.

7. **Prevent Stampedes**: Use locking, early recomputation, or stale-while-revalidate.

8. **Size Your Cache Appropriately**: Monitor eviction rates and adjust size accordingly.

9. **Layer Your Caches**: Browser cache → CDN → Redis → Database for optimal performance.

10. **Security Considerations**: Never cache sensitive data (passwords, tokens, PII) without encryption.

## Examples

### Complete Caching Layer

```python
class CacheLayer:
    """Production-ready caching layer with multiple strategies."""

    def __init__(self, redis_url: str, default_ttl: int = 3600):
        self.redis = RedisCache(redis_url)
        self.stampede = StampedeProtection(self.redis.redis)
        self.ttl_manager = TTLManager(default_ttl)
        self.invalidator = CacheInvalidator(self.redis.redis)

    async def get_user(self, user_id: str) -> User:
        return await self.stampede.get_with_lock(
            f"user:{user_id}",
            lambda: self.database.get_user(user_id),
            ttl=self.ttl_manager.get_tiered_ttl("user_profile")
        )

    async def update_user(self, user_id: str, data: dict):
        await self.database.update_user(user_id, data)
        await self.invalidator.invalidate_by_tag(f"user:{user_id}")

    async def get_product_listing(self, category: str) -> List[Product]:
        return await self.stampede.get_stale_while_revalidate(
            f"products:{category}",
            lambda: self.database.get_products(category),
            ttl=self.ttl_manager.get_tiered_ttl("product_catalog"),
            stale_ttl=60
        )
```
