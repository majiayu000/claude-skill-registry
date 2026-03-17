---
name: caching
model: standard
description: Caching strategies, invalidation, eviction policies, HTTP caching, distributed caching, and anti-patterns. Use when designing cache layers, choosing eviction policies, debugging stale data, or optimizing read-heavy workloads.
---

# Caching Patterns

> A well-placed cache is the cheapest way to buy speed. A misplaced cache is the most expensive way to buy bugs.

## Cache Strategies

| Strategy | How It Works | When to Use |
|----------|-------------|-------------|
| **Cache-Aside (Lazy)** | App checks cache → miss → reads DB → writes to cache | **Default choice** — general purpose |
| **Read-Through** | Cache fetches from DB on miss automatically | ORM-integrated caching, CDN origin fetch |
| **Write-Through** | Writes go to cache AND DB synchronously | Read-heavy with strong consistency |
| **Write-Behind** | Writes go to cache, async flush to DB | High write throughput, eventual consistency OK |
| **Refresh-Ahead** | Cache proactively refreshes before expiry | Predictable access patterns, low-latency critical |

```
Cache-Aside Flow:

  App ──► Cache ──► HIT? ──► Return data
              │
              ▼ MISS
          Read DB ──► Store in Cache ──► Return data
```


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install caching
```


---

## Cache Invalidation

| Method | Consistency | When to Use |
|--------|-------------|-------------|
| **TTL-based** | Eventual (up to TTL) | Simple data, acceptable staleness |
| **Event-based** | Strong (near real-time) | Inventory, profile updates |
| **Version-based** | Strong | Static assets, API responses, config |
| **Tag-based** | Strong | CMS content, category-based purging |

### TTL Guidelines

| Data Type | TTL | Rationale |
|-----------|-----|-----------|
| Static assets (CSS/JS/images) | 1 year + cache-busting hash | Immutable by filename |
| API config / feature flags | 30–60 seconds | Fast propagation needed |
| User profile data | 5–15 minutes | Tolerable staleness |
| Product catalog | 1–5 minutes | Balance freshness vs load |
| Session data | Match session timeout | Security requirement |

---

## HTTP Caching

### Cache-Control Directives

| Directive | Meaning |
|-----------|---------|
| `max-age=N` | Cache for N seconds |
| `s-maxage=N` | CDN/shared cache max age (overrides max-age) |
| `no-cache` | Must revalidate before using cached copy |
| `no-store` | Never cache anywhere |
| `must-revalidate` | Once stale, must revalidate |
| `private` | Only browser can cache, not CDN |
| `public` | Any cache can store |
| `immutable` | Content will never change (within max-age) |
| `stale-while-revalidate=N` | Serve stale for N seconds while fetching fresh |

### Common Recipes

```
# Immutable static assets (hashed filenames)
Cache-Control: public, max-age=31536000, immutable

# API response, CDN-cached, background refresh
Cache-Control: public, s-maxage=60, stale-while-revalidate=300

# Personalized data, browser-only
Cache-Control: private, max-age=0, must-revalidate
ETag: "abc123"

# Never cache (auth tokens, sensitive data)
Cache-Control: no-store
```

### Conditional Requests

| Mechanism | Request Header | Response Header | How It Works |
|-----------|---------------|-----------------|-------------|
| **ETag** | `If-None-Match: "abc"` | `ETag: "abc"` | Hash-based — 304 if match |
| **Last-Modified** | `If-Modified-Since: <date>` | `Last-Modified: <date>` | Date-based — 304 if unchanged |

Prefer ETag over Last-Modified — ETags detect content changes regardless of timestamp granularity.

---

## Application Caching

| Solution | Speed | Shared Across Processes | When to Use |
|----------|-------|------------------------|-------------|
| **In-memory LRU** | Fastest | No | Single-process, bounded memory, hot data |
| **Redis** | Sub-ms (network) | Yes | **Production default** — TTL, pub/sub, persistence |
| **Memcached** | Sub-ms (network) | Yes | Simple key-value at extreme scale |
| **SQLite** | Fast (disk) | No | Embedded apps, edge caching |

### Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data structures | Strings, hashes, lists, sets, sorted sets | Strings only |
| Persistence | AOF, RDB snapshots | None |
| Pub/Sub | Yes | No |
| Max value size | 512 MB | 1 MB |
| **Verdict** | **Default choice** | Pure cache at extreme scale |

---

## Distributed Caching

| Concern | Solution |
|---------|----------|
| **Partitioning** | Consistent hashing — minimal reshuffling on node changes |
| **Replication** | Primary-replica — writes to primary, reads from replicas |
| **Failover** | Redis Sentinel or Cluster auto-failover |

**Rule of thumb:** 3 primaries + 3 replicas minimum for production Redis Cluster.

---

## Cache Eviction Policies

| Policy | How It Works | When to Use |
|--------|-------------|-------------|
| **LRU** | Evicts least recently accessed | **Default** — general purpose |
| **LFU** | Evicts least frequently accessed | Skewed popularity distributions |
| **FIFO** | Evicts oldest entry | Simple, time-ordered data |
| **TTL** | Evicts after fixed duration | Data with known freshness window |

> Redis default is `noeviction`. Set `maxmemory-policy` to `allkeys-lru` or `volatile-lru` for production.

---

## Caching Layers

```
Browser Cache → CDN → Load Balancer → App Cache → DB Cache → Database
```

| Layer | What to Cache | Invalidation |
|-------|--------------|--------------|
| **Browser** | Static assets, API responses | Versioned URLs, Cache-Control |
| **CDN** | Static files, public API responses | Purge API, surrogate keys |
| **Application** | Computed results, DB queries, external API | Event-driven, TTL |
| **Database** | Query plans, buffer pool, materialized views | `ANALYZE`, manual refresh |

---

## Cache Stampede Prevention

When a hot key expires, hundreds of requests simultaneously hit the database.

| Technique | How It Works |
|-----------|-------------|
| **Mutex / Lock** | First request locks, fetches, populates; others wait |
| **Probabilistic early expiration** | Random chance of refreshing before TTL |
| **Request coalescing** | Deduplicate in-flight requests for same key |
| **Stale-while-revalidate** | Serve stale, refresh asynchronously |

---

## Cache Warming

| Strategy | When to Use |
|----------|-------------|
| **On-deploy warm-up** | Predictable key set, latency-sensitive |
| **Background job** | Reports, dashboards, catalog data |
| **Shadow traffic** | Cache migration, new infrastructure |
| **Priority-based** | Limited warm-up time budget |

> **Cold start impact:** A full cache flush can increase DB load 10–100x. Always warm gradually or use stale-while-revalidate.

---

## Monitoring

| Metric | Healthy Range | Action if Unhealthy |
|--------|--------------|---------------------|
| **Hit rate** | > 90% | Low → cache too small, wrong TTL, bad key design |
| **Eviction rate** | Near 0 steady state | High → increase memory or tune policy |
| **Latency (p99)** | < 1ms (Redis) | High → network issue, large values, hot key |
| **Memory usage** | < 80% of max | Approaching max → scale up or tune eviction |

---

## NEVER Do

1. **NEVER cache without a TTL or invalidation plan** — data rots; every entry needs an expiry path
2. **NEVER treat cache as durable storage** — caches evict, crash, and restart; always fall back to source of truth
3. **NEVER cache sensitive data (tokens, PII) without encryption** — cache breaches expose everything in plaintext
4. **NEVER ignore cache stampede on hot keys** — one expired popular key can take down your database
5. **NEVER use unbounded in-memory caches in production** — memory grows until OOM-killed
6. **NEVER cache mutable data with `immutable` Cache-Control** — browsers will never re-fetch
7. **NEVER skip monitoring hit/miss rates** — you won't know if your cache is helping or hurting
