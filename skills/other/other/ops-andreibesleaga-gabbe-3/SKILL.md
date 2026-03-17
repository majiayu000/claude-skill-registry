---
name: caching-strategy
description: Implement Redis/Memcached patterns and invalidation strategies.
role: eng-backend
triggers:
  - cache
  - redis
  - memcached
  - speed up
  - ttl
  - invalidation
---

# caching-strategy Skill

This skill defines how to implement caching to improve performance without serving stale data.

## 1. Caching Patterns

### Read Patterns
1.  **Cache-Aside (Lazy Loading)** - *Most Common*
    - App checks Cache.
    - If hit: return.
    - If miss: fetch DB -> write to Cache -> return.
    - *Pros*: Resilient to cache failure. *Cons*: First request is slow.

2.  **Read-Through**
    - App asks Cache. Cache itself fetches from DB if missing.
    - *Pros*: App logic simple. *Cons*: Requires specific library/provider support.

### Write Patterns
1.  **Write-Through**
    - App writes to Cache and DB synchronously.
    - *Pros*: Consistency. *Cons*: Write latency.

2.  **Write-Behind (Write-Back)**
    - App writes to Cache. Cache writes to DB asynchronously.
    - *Pros*: Fast writes. *Cons*: Data loss risk if cache crashes.

3.  **Write-Around**
    - App writes to DB directly. Cache is only populated on Read miss.
    - *Pros*: Reduces cache churn for write-heavy data.

## 2. Invalidation Strategy (The Hard Part)

- **Time To Live (TTL)**: Always set a TTL. No key lives forever.
- **Event-Based Invalidation**: On `UserUpdated` event, delete `user:{id}` key.
- **Versioned Keys**: `user:{id}:v2`. Increment version to bust cache.

## 3. Keys & Values

- **Naming**: `namespace:entity:id:attribute` (e.g., `app:users:123:profile`).
- **Serialization**: Compress large JSON payloads (zlib/snappy) before caching.
- **Hot Keys**: If one key gets 100k req/s, replicate it or use local in-memory caching (L1) + Redis (L2).

## 4. Implementation Checklist

- [ ] **Fallbacks**: Wrap cache calls in try/catch. If Redis is down, fetch from DB.
- [ ] **Metrics**: Track `cache_hit_rate` (Target: >96%).
- [ ] **Consistency**: Is eventual consistency acceptable? If no, do not cache.
- [ ] **Eviction Policy**: Configure Redis `maxmemory-policy` (usually `allkeys-lru` or `volatile-lru`).

## 5. Anti-Patterns
- **Caching Lists**: Hard to update. Better to cache individual items and IDs.
- **Long TTLs for Dynamic Data**: Users will see old profiles.
- **Thundering Herd**: 1000 processes ensuring the same cache key at once. (Use locking or "probabilistic early expiration").
