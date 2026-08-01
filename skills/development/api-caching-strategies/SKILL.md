---
name: api-caching-strategies
description: Application-level caching strategies, HTTP caching, cache invalidation, and stampede prevention
---

# Caching Strategies

> **Quick Guide:** Choose the right caching strategy for your use case: cache-aside for read-heavy data, write-through for consistency, write-behind for write-heavy workloads. Always set TTL to prevent stale data and memory exhaustion. Use HTTP caching headers (Cache-Control, ETag, Last-Modified) for API responses. Prevent cache stampedes with locking or request coalescing. Measure cache hit rates before and after -- caching without metrics is guessing.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set TTL on ALL cached data -- cache without TTL leads to memory exhaustion and infinitely stale data)**

**(You MUST use namespaced cache keys with a consistent prefix -- generic keys cause collisions across data types)**

**(You MUST invalidate or update cache entries on writes -- serving stale data after mutation breaks user trust)**

**(You MUST implement stampede prevention (locking or coalescing) for high-traffic cache keys -- concurrent misses can overwhelm your data source)**

</critical_requirements>

---

**Auto-detection:** caching, cache-aside, write-through, write-behind, cache invalidation, TTL, Cache-Control, ETag, Last-Modified, stale-while-revalidate, s-maxage, cache stampede, thundering herd, in-memory cache, LRU cache, distributed cache, cache key, cache miss, cache hit, CDN caching, HTTP caching, conditional request, 304 Not Modified

**When to use:**

- Read-heavy endpoints fetching the same data repeatedly (cache-aside)
- Data that must stay consistent between cache and database after writes (write-through)
- API responses that benefit from HTTP caching headers (Cache-Control, ETag)
- High-traffic cache keys that risk stampede on expiration
- Reducing database load by caching expensive query results

**When NOT to use:**

- Data that must always be real-time fresh (caching adds staleness by definition)
- Simple CRUD with low traffic (caching complexity outweighs benefit)
- Development/debugging (caching obscures issues -- disable in dev)
- Premature optimization without measuring actual bottlenecks first

**Key patterns covered:**

- Cache-aside (lazy loading) with TTL
- Write-through for read-after-write consistency
- Write-behind (write-back) for write-heavy workloads
- HTTP caching: Cache-Control, ETag, Last-Modified, conditional requests
- CDN caching with s-maxage and stale-while-revalidate
- In-memory LRU caching for single-process hot data
- Cache key strategies and namespacing
- Stampede prevention (locking, request coalescing, early recomputation)
- Tag-based and pattern-based invalidation

---

<philosophy>

## Philosophy

Caching trades freshness for speed. Every caching decision is a **consistency vs performance** trade-off -- understand where your use case falls on that spectrum before choosing a strategy.

**The three questions before adding caching:**

1. **Is this actually slow?** Measure first. If the uncached response is fast enough, caching adds complexity without benefit.
2. **Can I tolerate staleness?** If data must always be real-time, caching is the wrong tool. Use read replicas or materialized views instead.
3. **What is the read-to-write ratio?** Caching shines when reads vastly outnumber writes. For write-heavy workloads, consider write-behind or skip caching entirely.

**Caching is a layered system.** HTTP caching (browser and CDN) reduces requests to your server. Application-level caching (in-memory or distributed) reduces requests to your database. Apply caching at the right layer for the problem.

**When to use caching:**

- Response times exceed acceptable thresholds and the data source is the bottleneck
- The same data is fetched repeatedly across requests
- Data freshness requirements allow some staleness (even 60 seconds)
- Traffic is high enough that database load is a concern

**When NOT to use caching:**

- Data changes frequently and must always be current
- Every request returns unique data (no cache reuse)
- You have not measured the actual bottleneck yet (premature optimization)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Cache-Aside (Lazy Loading)

The most common application-level caching pattern. The application checks the cache first, fetches from the data source on miss, and stores the result with a TTL.

```typescript
const CACHE_TTL_SECONDS = 300;
const CACHE_PREFIX = "app:user";

async function getUserById(userId: string): Promise<User | null> {
  const cacheKey = `${CACHE_PREFIX}:${userId}`;
  const cached = await cacheStore.get(cacheKey);
  if (cached) return JSON.parse(cached) as User;

  const user = await db.query.users.findFirst({ where: eq(users.id, userId) });
  if (!user) return null;

  await cacheStore.set(cacheKey, JSON.stringify(user), {
    ttl: CACHE_TTL_SECONDS,
  });
  return user;
}
```

**Why good:** TTL prevents stale data, namespaced keys prevent collisions, early return on cache hit, cache is populated lazily (only data that is actually requested gets cached)

```typescript
// BAD: No TTL, generic key
async function getUser(id: string) {
  const cached = await cacheStore.get(id); // No prefix -- collides with other data types
  if (cached) return JSON.parse(cached);
  const user = await db.query.users.findFirst({ where: eq(users.id, id) });
  await cacheStore.set(id, JSON.stringify(user)); // No TTL -- never expires
  return user;
}
```

**Why bad:** No TTL means infinite staleness and eventual memory exhaustion, generic key collides with other entity types using the same ID format

**When to use:** Read-heavy endpoints where data changes infrequently relative to reads.

See [examples/core.md](examples/core.md) for generic cache wrapper and error handling patterns.

---

### Pattern 2: Write-Through

Update both cache and data source on every write. Guarantees read-after-write consistency without waiting for TTL expiration.

```typescript
const CACHE_TTL_SECONDS = 300;

async function updateUser(
  userId: string,
  updates: Partial<User>,
): Promise<User> {
  const updatedUser = await db
    .update(users)
    .set({ ...updates, updatedAt: new Date() })
    .where(eq(users.id, userId))
    .returning();

  const cacheKey = `${CACHE_PREFIX}:${userId}`;
  await cacheStore.set(cacheKey, JSON.stringify(updatedUser[0]), {
    ttl: CACHE_TTL_SECONDS,
  });

  return updatedUser[0];
}
```

**Why good:** Cache always reflects latest database state, no stale reads after updates

**When to use:** Data that is read frequently after writes and must be consistent. **When not to use:** Write-heavy workloads where the overhead of updating cache on every write is too expensive.

See [examples/core.md](examples/core.md) for write-through with delete invalidation.

---

### Pattern 3: HTTP Caching Headers

Set appropriate Cache-Control, ETag, and Last-Modified headers on API responses to leverage browser and CDN caching. This reduces requests to your server entirely.

```typescript
// API endpoint setting caching headers
function setCacheHeaders(
  res: Response,
  body: unknown,
  options: { maxAge: number; isPublic: boolean },
) {
  const etag = generateETag(body);
  const scope = options.isPublic ? "public" : "private";

  res.setHeader(
    "Cache-Control",
    `${scope}, max-age=${options.maxAge}, must-revalidate`,
  );
  res.setHeader("ETag", etag);
  res.setHeader("Last-Modified", new Date().toUTCString());
}
```

**Key header combinations for APIs:**

| Use Case           | Cache-Control                         | Why                                |
| ------------------ | ------------------------------------- | ---------------------------------- |
| Public list data   | `public, max-age=60, s-maxage=300`    | CDN caches longer than browser     |
| User-specific data | `private, max-age=0, must-revalidate` | No shared cache, always revalidate |
| Sensitive data     | `no-store, private`                   | Never cache anywhere               |
| Immutable assets   | `public, max-age=31536000, immutable` | Version in URL, cache forever      |

See [examples/core.md](examples/core.md) for conditional request handling (If-None-Match / 304) and CDN patterns.

---

### Pattern 4: In-Memory LRU Cache

For single-process hot data that does not need to be shared across instances. Faster than a distributed cache (no network hop) but lost on process restart and not shared between workers.

```typescript
import { LRUCache } from "lru-cache";

const MAX_ITEMS = 500;
const TTL_MS = 300_000; // 5 minutes

const configCache = new LRUCache<string, AppConfig>({
  max: MAX_ITEMS,
  ttl: TTL_MS,
});

function getConfig(key: string): AppConfig | undefined {
  return configCache.get(key);
}

function setConfig(key: string, value: AppConfig): void {
  configCache.set(key, value);
}
```

**Why good:** No serialization overhead (stores objects directly), automatic eviction of least-recently-used items, TTL prevents staleness

**When to use:** Configuration, feature flags, frequently accessed reference data in single-process applications. **When not to use:** Data that must be shared across multiple server instances (use a distributed cache instead).

See [examples/core.md](examples/core.md) for LRU cache with size tracking and fetch method.

---

### Pattern 5: Cache Key Strategies

Consistent, namespaced cache keys prevent collisions and enable pattern-based invalidation.

```typescript
const CACHE_PREFIX = "myapp";

// Entity keys: prefix:type:id
const userKey = (id: string) => `${CACHE_PREFIX}:user:${id}`;
const productKey = (id: string) => `${CACHE_PREFIX}:product:${id}`;

// Query result keys: prefix:type:list:hash
const productListKey = (filters: ProductFilters) => {
  const normalized = JSON.stringify({
    category: filters.category ?? "all",
    page: filters.page ?? 1,
    sort: filters.sort ?? "created",
  });
  const hash = createHash("md5").update(normalized).digest("hex");
  return `${CACHE_PREFIX}:products:list:${hash}`;
};

// User-scoped keys
const userCartKey = (userId: string) => `${CACHE_PREFIX}:cart:${userId}`;
```

**Why good:** Hierarchical structure prevents collisions, hashing complex queries keeps keys short, pattern prefix enables bulk invalidation

See [examples/core.md](examples/core.md) for cache key generation patterns.

---

### Pattern 6: Cache Invalidation

Invalidation is the hardest part of caching. Choose the simplest strategy that meets your consistency requirements.

**Direct invalidation** -- delete the exact key on mutation:

```typescript
async function updateProduct(id: string, data: ProductUpdate) {
  await db.update(products).set(data).where(eq(products.id, id));
  await cacheStore.del(productKey(id));
}
```

**Tag-based invalidation** -- group related keys by tag for bulk invalidation:

```typescript
// Invalidate all electronics products when category changes
await invalidateByTag("category:electronics");
```

**TTL-based expiration** -- let the cache expire naturally when eventual consistency is acceptable:

```typescript
const SHORT_TTL = 60; // 1 minute for frequently changing data
const MEDIUM_TTL = 300; // 5 minutes for user data
const LONG_TTL = 3600; // 1 hour for reference data
```

See [examples/advanced.md](examples/advanced.md) for tag-based invalidation implementation and pattern-based key deletion.

---

### Pattern 7: Stampede Prevention

When a popular cache key expires, many concurrent requests may all miss the cache simultaneously and flood the data source. This is a cache stampede (thundering herd).

**Locking** -- only one request regenerates the cache; others wait or get stale data:

```typescript
async function getWithLock(
  key: string,
  fetchFn: () => Promise<string>,
): Promise<string> {
  const cached = await cacheStore.get(key);
  if (cached) return cached;

  const lockKey = `lock:${key}`;
  const acquired = await cacheStore.setNX(lockKey, "1", {
    ttl: LOCK_TTL_SECONDS,
  });

  if (!acquired) {
    await delay(RETRY_DELAY_MS);
    return getWithLock(key, fetchFn); // Retry after brief wait
  }

  try {
    const value = await fetchFn();
    await cacheStore.set(key, value, { ttl: CACHE_TTL_SECONDS });
    return value;
  } finally {
    await cacheStore.del(lockKey);
  }
}
```

**Why good:** Only one request hits the data source, others wait briefly, lock auto-expires if holder crashes

See [examples/advanced.md](examples/advanced.md) for request coalescing (singleflight) and probabilistic early recomputation.

</patterns>

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Cache-aside, write-through, HTTP caching, TTL patterns, in-memory caching
- [examples/advanced.md](examples/advanced.md) - Cache invalidation, stampede prevention, distributed caching, write-behind
- [reference.md](reference.md) - Strategy comparison, stampede comparison, cache key conventions

---

<decision_framework>

## Decision Framework

### Which Caching Strategy?

```
Is data read much more than written?
+-- YES --> Can you tolerate staleness?
|   +-- YES --> Cache-aside with TTL
|   +-- NO  --> Write-through (consistent reads)
+-- NO  --> Is write latency critical?
    +-- YES --> Write-behind (async persist)
    +-- NO  --> Write-through or skip caching
```

### Which Cache Layer?

```
Is the response public (same for all users)?
+-- YES --> HTTP caching (Cache-Control: public, s-maxage)
|          CDN handles it, your server may never see the request
+-- NO  --> Is it shared across server instances?
    +-- YES --> Distributed cache (external store)
    +-- NO  --> Is it hot data in a single process?
        +-- YES --> In-memory LRU cache
        +-- NO  --> Cache-aside with distributed store
```

### TTL Selection Guide

| Data Type                      | Recommended TTL   | Rationale                        |
| ------------------------------ | ----------------- | -------------------------------- |
| Static config / feature flags  | 3600s+ (1h+)      | Rarely changes                   |
| Product catalog / listings     | 300-3600s (5m-1h) | Infrequent updates               |
| User profile                   | 60-300s (1-5m)    | Changes occasionally             |
| Search results                 | 30-60s (30s-1m)   | Balance freshness vs performance |
| Real-time data (prices, stock) | 5-30s             | Must be near-fresh               |
| Session data                   | 86400s (24h)      | Long-lived by design             |

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Cache without TTL -- memory grows unbounded and data is stale forever
- No cache invalidation on writes -- users see stale data after mutations, eroding trust
- Generic cache keys without namespacing -- collisions return wrong data to wrong callers
- No stampede prevention on high-traffic keys -- cache expiration triggers data source flood
- Caching errors or null results without separate short TTL -- a transient failure gets cached and served for the full TTL

**Medium Priority Issues:**

- Same TTL for all data types -- different data has different freshness requirements
- Caching user-specific data in shared caches (CDN) without `private` directive -- leaks personal data to other users
- No cache hit/miss monitoring -- impossible to know if caching is actually helping
- `no-cache` confused with `no-store` -- `no-cache` still stores but revalidates; `no-store` prevents any storage
- Over-caching low-traffic endpoints -- adds complexity without meaningful performance gain

**Gotchas & Edge Cases:**

- `Cache-Control: no-cache` does NOT prevent caching -- it forces revalidation before every use. Use `no-store` to prevent storage entirely.
- ETag takes precedence over Last-Modified during revalidation (per RFC 9110) -- always send both for best compatibility
- `s-maxage` overrides `max-age` for shared caches (CDNs) only -- browsers ignore it
- `stale-while-revalidate` lets CDNs serve expired content while refreshing in the background -- great for availability, but means users briefly see stale data
- Distributed cache SET with TTL resets the expiration timer on every write -- calling SET again extends the TTL, which may keep stale data alive longer than expected
- In-memory LRU caches are per-process -- multiple server instances have independent caches that can serve different data for the same key
- `JSON.stringify` for cache serialization drops `undefined` values and converts `Date` objects to strings -- use a structured serializer if needed
- Cache key generation must be deterministic -- object property order in `JSON.stringify` varies across engines; sort keys or use a canonical serializer

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST set TTL on ALL cached data -- cache without TTL leads to memory exhaustion and infinitely stale data)**

**(You MUST use namespaced cache keys with a consistent prefix -- generic keys cause collisions across data types)**

**(You MUST invalidate or update cache entries on writes -- serving stale data after mutation breaks user trust)**

**(You MUST implement stampede prevention (locking or coalescing) for high-traffic cache keys -- concurrent misses can overwhelm your data source)**

**Failure to follow these rules will cause stale data bugs, cache key collisions, memory exhaustion, and data source overload during traffic spikes.**

</critical_reminders>
