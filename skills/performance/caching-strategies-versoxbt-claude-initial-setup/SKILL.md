---
name: caching-strategies
description: >
  Implement effective caching at every layer: in-memory, Redis, CDN, and browser. Activate
  whenever the user asks about caching, performance optimization for repeated data access,
  Redis patterns, CDN configuration, cache invalidation, HTTP cache headers, memoization,
  or stale-while-revalidate strategies.
---

# Caching Strategies

Cache data at the right layer to reduce latency, database load, and compute costs.
The two hardest problems in computer science are cache invalidation and naming things.
This guide focuses on getting invalidation right.

## When to Use
- API endpoints that serve the same data to many users
- Database queries that are expensive and don't change frequently
- Static assets and CDN configuration
- Computed values that are expensive to recalculate
- Reducing latency for frequently accessed data

## Core Patterns

### In-Memory Memoization

Cache computed values within a single process. Simplest form of caching.

```typescript
// Simple memoization with Map
function memoize<Args extends unknown[], Result>(
  fn: (...args: Args) => Result,
  keyFn: (...args: Args) => string = (...args) => JSON.stringify(args),
): (...args: Args) => Result {
  const cache = new Map<string, Result>();

  return (...args: Args): Result => {
    const key = keyFn(...args);
    if (cache.has(key)) {
      return cache.get(key)!;
    }
    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}

// For bounded caches, use an LRU eviction policy (e.g., lru-cache npm package)
// to prevent unbounded memory growth in long-running processes.
import { LRUCache } from 'lru-cache';
const userCache = new LRUCache<string, User>({ max: 1000 });
```

### Redis Caching Patterns

Distributed caching for multi-instance deployments.

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

// Cache-aside pattern (most common)
async function getUserById(id: string): Promise<User> {
  const cacheKey = `user:${id}`;

  // 1. Check cache
  const cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // 2. Cache miss - fetch from database
  const user = await db.users.findById(id);
  if (!user) {
    throw new Error('User not found');
  }

  // 3. Populate cache with TTL
  await redis.set(cacheKey, JSON.stringify(user), 'EX', 3600); // 1 hour

  return user;
}

// Write-through: update cache when data changes
async function updateUser(id: string, data: UpdateUserDto): Promise<User> {
  const user = await db.users.update(id, data);
  const cacheKey = `user:${id}`;
  await redis.set(cacheKey, JSON.stringify(user), 'EX', 3600);
  return user;
}

// Cache invalidation on delete
async function deleteUser(id: string): Promise<void> {
  await db.users.delete(id);
  await redis.del(`user:${id}`);
  // Also invalidate related caches
  await redis.del(`user:${id}:posts`);
  await redis.del(`user:${id}:settings`);
}

// Pattern-based invalidation
async function invalidateUserCaches(userId: string): Promise<void> {
  const keys = await redis.keys(`user:${userId}:*`);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}
```

### HTTP Cache Headers

Control browser and CDN caching with proper headers.

```typescript
// Express middleware for cache control

// Static assets: cache aggressively (use content hashing in filenames)
app.use('/assets', express.static('dist/assets', {
  maxAge: '1y',           // Cache for 1 year
  immutable: true,        // Never revalidate (filename changes on content change)
}));

// API responses: vary by use case
app.get('/api/products', (req, res) => {
  res.set({
    'Cache-Control': 'public, max-age=300, stale-while-revalidate=60',
    'Vary': 'Accept-Encoding',
  });
  res.json(products);
});

// User-specific data: private caching only
app.get('/api/profile', authenticate, (req, res) => {
  res.set({
    'Cache-Control': 'private, max-age=60, must-revalidate',
  });
  res.json(req.user);
});

// Never cache sensitive data
app.get('/api/auth/session', (req, res) => {
  res.set({
    'Cache-Control': 'no-store',
  });
  res.json(sessionData);
});
```

```
Cache-Control Directives Cheat Sheet:

public          - CDN and browser can cache
private         - Only browser can cache (user-specific data)
max-age=N       - Fresh for N seconds
s-maxage=N      - CDN-specific max-age (overrides max-age for CDN)
no-cache        - Must revalidate with server before using cached copy
no-store        - Never cache (sensitive data)
must-revalidate - After max-age expires, must revalidate (no stale serving)
immutable       - Content will never change (use with content-hashed filenames)
stale-while-revalidate=N - Serve stale for N seconds while fetching fresh copy
```

### Stale-While-Revalidate Pattern

Serve stale data immediately while refreshing in the background. The HTTP header
`Cache-Control: stale-while-revalidate=60` does this at the CDN/browser level.
For server-side SWR, use libraries like `swr` (React) or implement a cache wrapper
that returns stale data and triggers a background refresh when the TTL expires.
```

### CDN Caching (Cloudflare / Vercel / AWS CloudFront)

Configure CDN edge caching for global performance.

```typescript
// Next.js ISR (Incremental Static Regeneration)
export async function getStaticProps() {
  const posts = await fetchPosts();
  return {
    props: { posts },
    revalidate: 60, // Regenerate page every 60 seconds
  };
}

// Vercel Edge Config / Cloudflare Cache API
app.get('/api/popular-products', (req, res) => {
  res.set({
    'Cache-Control': 'public, s-maxage=300, stale-while-revalidate=600',
    'CDN-Cache-Control': 'max-age=300',     // CDN-specific
    'Surrogate-Control': 'max-age=3600',    // Varnish/Fastly
  });
  res.json(products);
});
```

## Anti-Patterns
- Caching without a TTL (data grows forever, never expires)
- Using `redis.keys('*')` in production (blocks Redis, O(N) scan)
- Caching user-specific data with `public` Cache-Control
- Invalidating cache on every write when reads vastly outnumber writes
- Not varying cache by relevant headers (Accept-Language, Authorization)
- Caching error responses (propagates failures even after recovery)
- Using unbounded in-memory caches (memory leak in long-running processes)
- Setting very long cache TTLs without a cache-busting mechanism

## Quick Reference

| Layer | Tool | Best For |
|-------|------|----------|
| In-process | Map / LRU Cache | Computed values, hot path data |
| Distributed | Redis / Memcached | Shared state across instances |
| CDN edge | Cloudflare / CloudFront | Static assets, public API responses |
| Browser | Cache-Control headers | Repeat visits, static assets |
| Database | Query result cache | Expensive queries, materialized views |

| Pattern | When to Use |
|---------|-------------|
| Cache-aside | Read-heavy, tolerance for occasional stale data |
| Write-through | Need cache always in sync with database |
| Write-behind | High write volume, eventual consistency OK |
| SWR | User-facing reads where freshness < speed |
| TTL-based | Simple expiration, no explicit invalidation needed |
