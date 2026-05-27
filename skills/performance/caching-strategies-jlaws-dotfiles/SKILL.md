---
name: caching-strategies
description: Implement multi-layer caching with Redis, application caches, and CDN for optimal performance
---

# Caching Strategies

## Caching Layer Selection

| Layer | Latency | Capacity | Best For | Invalidation |
|-------|---------|----------|----------|--------------|
| **L1: In-process** | <1ms | MBs | Hot config, computed values | TTL, app restart |
| **L2: Redis/Memcached** | 1-5ms | GBs | Session, API responses, shared state | Explicit + TTL |
| **L3: CDN** | 10-50ms | TBs | Static assets, public API responses | Cache-Control headers, purge API |
| **L4: Browser** | 0ms | MBs | Static assets, prefetch | Cache-Control, ETag |

**Default strategy:** L1 for hot paths (<100 items), L2 for shared mutable state, L3 for static/semi-static content.

## Write Pattern Selection

| Pattern | Consistency | Write Latency | Read Latency | Use Case |
|---------|------------|---------------|--------------|----------|
| **Cache-aside** | Eventual | Normal | Miss penalty | General purpose, default choice |
| **Write-through** | Strong | Higher (cache+DB) | Always fast | Read-heavy, consistency matters |
| **Write-behind** | Eventual | Low (async DB) | Always fast | Write-heavy, DB bottleneck |
| **Read-through** | Eventual | Normal | Miss penalty | Uniform cache access layer |

## Redis Patterns

```python
import redis, json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Cache-aside: check cache, fetch on miss, populate
def cache_aside(key: str, ttl: int, fetch_fn):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    value = fetch_fn()                    # DB call on miss
    r.setex(key, ttl, json.dumps(value))
    return value

# Hashes: partial reads/updates without deserializing entire object
def cache_user_hash(user_id: str, user: dict):
    r.hset(f"user:{user_id}", mapping=user)
    r.expire(f"user:{user_id}", 3600)

def increment_login_count(user_id: str):
    r.hincrby(f"user:{user_id}", "login_count", 1)  # Atomic, no race

# Sorted sets: leaderboards
def update_score(board: str, user_id: str, score: float):
    r.zadd(board, {user_id: score})       # O(log N) insert

def get_top_n(board: str, n: int = 10) -> list[tuple[str, float]]:
    return r.zrevrange(board, 0, n - 1, withscores=True)

def get_rank(board: str, user_id: str) -> int | None:
    rank = r.zrevrank(board, user_id)
    return rank + 1 if rank is not None else None
```

### Pub/Sub: Cache Invalidation Broadcast

```python
import threading

def publish_invalidation(channel: str, key: str):
    """Notify all app instances to evict local cache."""
    r.publish(channel, json.dumps({"action": "invalidate", "key": key}))

def subscribe_invalidations(channel: str, local_cache: dict):
    """Background listener for cache invalidation events."""
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    def listener():
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                local_cache.pop(data["key"], None)
    threading.Thread(target=listener, daemon=True).start()
```

## Application-Level Caching

```python
from functools import lru_cache
from cachetools import TTLCache, cached
import threading

# lru_cache: in-process, no TTL, cleared on deploy
@lru_cache(maxsize=256)
def get_config(key: str) -> str:
    return db.query(Config).filter_by(key=key).scalar()

get_config.cache_clear()                  # Manual invalidation
get_config.cache_info()                   # CacheInfo(hits=47, misses=3, ...)

# cachetools: TTL + size-bounded, thread-safe
_cache = TTLCache(maxsize=1000, ttl=300)
_lock = threading.Lock()

@cached(cache=_cache, lock=_lock)
def get_product(product_id: str) -> dict:
    return db.query(Product).get(product_id).to_dict()

def update_product(product_id: str, data: dict):
    db.query(Product).filter_by(id=product_id).update(data)
    db.commit()
    _cache.pop(product_id, None)          # Invalidate immediately
```

## Cache Stampede Prevention

### Probabilistic Early Expiry (XFetch)

```python
import random, time

def xfetch(key: str, ttl: int, beta: float, fetch_fn):
    """Probabilistic early recomputation to prevent stampede.
    beta=1.0 is standard; higher = earlier refresh."""
    cached = r.get(key)
    if cached:
        data = json.loads(cached)
        remaining_ttl = r.ttl(key)
        if remaining_ttl > 0:
            delta = ttl - remaining_ttl
            if delta * beta * random.random() < remaining_ttl:
                return data["value"]      # Still fresh enough
    value = fetch_fn()
    r.setex(key, ttl, json.dumps({"value": value}))
    return value
```

### Distributed Lock (Mutex)

```python
def cache_with_lock(key: str, ttl: int, fetch_fn, lock_timeout: int = 5):
    """Only one process recomputes on miss; others wait."""
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    lock_key = f"lock:{key}"
    if r.set(lock_key, "1", nx=True, ex=lock_timeout):
        try:
            value = fetch_fn()
            r.setex(key, ttl, json.dumps(value))
            return value
        finally:
            r.delete(lock_key)
    else:
        time.sleep(0.1)                   # Another process is computing
        return cache_with_lock(key, ttl, fetch_fn, lock_timeout)
```

## CDN Cache Headers

```python
from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/api/products/{product_id}")
def get_product_api(product_id: str, response: Response):
    product = fetch_product(product_id)
    # CDN caches 60s, browser 10s, serve stale while revalidating
    response.headers["Cache-Control"] = "public, max-age=10, s-maxage=60, stale-while-revalidate=300"
    response.headers["ETag"] = f'"{product["version"]}"'
    response.headers["Vary"] = "Accept-Encoding"
    return product

@app.get("/api/user/profile")
def get_user_profile(response: Response):
    response.headers["Cache-Control"] = "private, no-store"  # No CDN
    return fetch_profile()

# Cache-Control cheat sheet:
# public, s-maxage=3600          -> CDN caches 1hr
# private, max-age=300           -> Browser only, 5min
# no-cache                       -> Must revalidate (still caches)
# no-store                       -> Never cache anywhere
# stale-while-revalidate=60      -> Serve stale 60s while refreshing
# stale-if-error=300             -> Serve stale 5min if origin down
```

## Cache Invalidation Patterns

### Event-Driven Invalidation

```python
class CacheInvalidator:
    def __init__(self, redis_client, channel: str = "cache:invalidate"):
        self.redis = redis_client
        self.channel = channel

    def on_entity_updated(self, entity_type: str, entity_id: str):
        """Delete key + broadcast to other instances."""
        key = f"{entity_type}:{entity_id}"
        self.redis.delete(key)
        self.redis.publish(self.channel, json.dumps({"key": key}))

    def on_bulk_update(self, entity_type: str, entity_ids: list[str]):
        pipe = self.redis.pipeline()
        for eid in entity_ids:
            pipe.delete(f"{entity_type}:{eid}")
        pipe.execute()
```

### Tag-Based Invalidation

```python
def set_with_tags(key: str, value, ttl: int, tags: list[str]):
    """Associate cache entry with tags for group invalidation."""
    pipe = r.pipeline()
    pipe.setex(key, ttl, json.dumps(value))
    for tag in tags:
        pipe.sadd(f"tag:{tag}", key)
        pipe.expire(f"tag:{tag}", ttl + 60)
    pipe.execute()

def invalidate_tag(tag: str):
    """Delete all cache entries with this tag."""
    keys = r.smembers(f"tag:{tag}")
    if keys:
        r.delete(*keys, f"tag:{tag}")

# Usage: product belongs to category
set_with_tags("product:123", product, 300, tags=["category:electronics", "brand:acme"])
invalidate_tag("category:electronics")    # Clears all electronics products
```

## Gotchas

- **Cache stampede on cold start**: Warm critical caches during deployment, not on first request
- **Thundering herd on expiry**: Use jittered TTLs (`ttl + random(0, 60)`) to spread recomputation
- **Stale reads after write**: Write-through or invalidate-on-write; cache-aside has a race window
- **Memory pressure**: Always set `maxmemory` + eviction policy in Redis (`allkeys-lru` for cache)
- **Serialization cost**: JSON is slow for large objects; consider msgpack or pickle (trusted data only)
- **Cache key collisions**: Namespace keys with version prefix (`v2:user:123`) for schema changes
- **Negative caching**: Cache "not found" results too (short TTL) to prevent repeated DB lookups
- **Hot key problem**: Single popular key overwhelms one Redis shard; use local L1 cache in front
- **Inconsistent invalidation**: If you cache derived data, invalidate ALL sources (joins across tables)
