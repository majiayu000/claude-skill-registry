---
name: advanced-caching-strategies
version: "1.0"
description: >
  Multi-layer caching strategies across CDN, browser, server, and database.
  PROACTIVELY activate for: (1) HTTP caching headers, (2) CDN configuration,
  (3) Server-side caching with Redis, (4) Cache invalidation strategies, (5) ETag implementation.
  Triggers: "caching", "cache strategy", "CDN", "browser cache", "server cache", "redis", "cache invalidation", "ETag", "Cache-Control"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Advanced Caching Strategies

This skill provides guidance on designing and implementing multi-layered caching strategies across the full application stack (CDN, browser, server, database) to minimize latency, reduce server load, and improve overall application resilience and user experience.

## The Cache Hierarchy

Caching can be implemented at multiple layers, from closest to the user to closest to the data source:

1. **Browser Cache**: Client-side caching (HTTP caching, LocalStorage, IndexedDB)
2. **CDN Edge Cache**: Geographically distributed caching (Vercel Edge, CloudFront, Cloudflare)
3. **Server-Side Cache**: Application-level caching (Redis, in-memory)
4. **Database Cache**: Query result caching, connection pooling

**Goal**: Serve content from the closest, fastest cache layer possible.

## Browser Caching

Browser caching reduces network requests by storing resources locally.

### HTTP Cache-Control Headers

The `Cache-Control` header controls how and for how long browsers cache responses.

#### Immutable Static Assets

```http
# For assets with content-addressed filenames (e.g., app.abc123.js)
Cache-Control: public, max-age=31536000, immutable
```

- **public**: Can be cached by browsers and CDNs
- **max-age=31536000**: Cache for 1 year (in seconds)
- **immutable**: Never revalidate (file name changes when content changes)

**Next.js**: Automatically sets this for `/_next/static/` files

#### Dynamic HTML Pages

```http
# For HTML pages that change periodically
Cache-Control: public, max-age=0, must-revalidate
```

- **max-age=0**: Revalidate on every request
- **must-revalidate**: Must check server before using stale cache

Or with stale-while-revalidate:
```http
Cache-Control: public, max-age=60, stale-while-revalidate=86400
```

- Serve from cache for 60s
- If 60s-24h old, serve stale content while revalidating in background

#### API Responses

```http
# User-specific data (don't cache)
Cache-Control: private, no-store

# Public data that changes occasionally
Cache-Control: public, max-age=300, stale-while-revalidate=600
```

- **private**: Only browser cache (not CDN)
- **no-store**: Don't cache at all
- **stale-while-revalidate**: Serve stale data while fetching fresh data

### ETag and Conditional Requests

ETags enable efficient revalidation without re-downloading unchanged content.

#### Server Implementation (Next.js API Route)

```ts
// app/api/data/route.ts
import { NextResponse } from 'next/server'
import crypto from 'crypto'

export async function GET(request: Request) {
  const data = await fetchData()
  const content = JSON.stringify(data)

  // Generate ETag from content hash
  const etag = crypto.createHash('md5').update(content).digest('hex')

  // Check If-None-Match header
  const clientEtag = request.headers.get('if-none-match')

  if (clientEtag === etag) {
    // Content hasn't changed
    return new NextResponse(null, { status: 304 })
  }

  // Content changed, send full response
  return NextResponse.json(data, {
    headers: {
      'ETag': etag,
      'Cache-Control': 'public, max-age=300',
    },
  })
}
```

#### Python FastAPI Implementation

```python
from fastapi import FastAPI, Request, Response
import hashlib
import json

app = FastAPI()

@app.get("/api/data")
async def get_data(request: Request):
    data = await fetch_data()
    content = json.dumps(data)

    # Generate ETag
    etag = hashlib.md5(content.encode()).hexdigest()

    # Check If-None-Match
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    # Return with ETag
    return Response(
        content=content,
        headers={
            "ETag": etag,
            "Cache-Control": "public, max-age=300"
        }
    )
```

### LocalStorage and IndexedDB

For application state and data that doesn't need to be in HTTP cache.

```ts
// Simple cache wrapper for localStorage
class BrowserCache {
  static set(key: string, value: any, ttlMs: number) {
    const item = {
      value,
      expiry: Date.now() + ttlMs,
    }
    localStorage.setItem(key, JSON.stringify(item))
  }

  static get(key: string) {
    const itemStr = localStorage.getItem(key)
    if (!itemStr) return null

    const item = JSON.parse(itemStr)
    if (Date.now() > item.expiry) {
      localStorage.removeItem(key)
      return null
    }

    return item.value
  }
}

// Usage
BrowserCache.set('user-prefs', preferences, 7 * 24 * 60 * 60 * 1000) // 7 days
const prefs = BrowserCache.get('user-prefs')
```

## CDN Caching

CDNs cache content at edge locations close to users, reducing latency and server load.

### Vercel Edge Network (Next.js)

Vercel automatically caches static assets and certain dynamic routes.

```ts
// app/products/page.tsx
export const revalidate = 3600 // Cache for 1 hour

export default async function ProductsPage() {
  const products = await fetch('https://api.example.com/products', {
    next: { revalidate: 3600 }
  }).then(r => r.json())

  return <ProductGrid products={products} />
}
```

### Custom CDN Headers

```ts
// app/api/public-data/route.ts
export async function GET() {
  const data = await fetchPublicData()

  return NextResponse.json(data, {
    headers: {
      'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=86400',
      'CDN-Cache-Control': 'max-age=7200',
    },
  })
}
```

- **s-maxage**: CDN cache duration (overrides max-age for shared caches)
- **CDN-Cache-Control**: Cloudflare-specific directive

### Cache Key Configuration

Ensure cache keys include relevant parameters:

```ts
// BAD: Same cache for all users
fetch(`https://api.example.com/dashboard`)

// GOOD: User-specific cache key
fetch(`https://api.example.com/dashboard`, {
  headers: {
    'x-user-id': userId,
  },
  cache: 'no-store', // Don't cache user-specific data in CDN
})
```

### CDN Purging

```ts
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache'

export async function POST(request: Request) {
  const { path, tag } = await request.json()

  if (path) {
    revalidatePath(path) // Purge specific path
  }

  if (tag) {
    revalidateTag(tag) // Purge all fetches with this tag
  }

  return Response.json({ revalidated: true })
}
```

## Server-Side Caching

Application-level caching reduces database load and improves response times.

### Next.js React cache()

```ts
// lib/data.ts
import { cache } from 'react'

export const getUser = cache(async (id: string) => {
  // This function is memoized during a single request
  const user = await db.query('SELECT * FROM users WHERE id = ?', [id])
  return user
})

// Can be called multiple times in components without re-fetching
const user1 = await getUser('123')
const user2 = await getUser('123') // Returns memoized result
```

### Next.js unstable_cache

```ts
import { unstable_cache } from 'next/cache'

export const getCachedProducts = unstable_cache(
  async () => {
    return await db.query('SELECT * FROM products')
  },
  ['products-list'], // Cache key
  {
    revalidate: 3600, // Cache for 1 hour
    tags: ['products'], // For on-demand revalidation
  }
)
```

### Redis Caching (Python)

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(ttl: int = 300):
    """Decorator for caching function results in Redis"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = f"{func.__name__}:{args}:{kwargs}"

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Cache miss - execute function
            result = await func(*args, **kwargs)

            # Store in cache
            redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result)
            )

            return result

        return wrapper
    return decorator

# Usage
@cache_result(ttl=600)
async def get_user_profile(user_id: str):
    return await db.fetch_one(
        "SELECT * FROM users WHERE id = ?",
        user_id
    )
```

### LRU Cache (Python)

For single-process applications:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Cache recent exchange rate lookups"""
    response = requests.get(
        f"https://api.example.com/rate/{from_currency}/{to_currency}"
    )
    return response.json()['rate']

# Clear cache when needed
get_exchange_rate.cache_clear()
```

## Database Caching

Optimize database performance through caching and connection pooling.

### Query Result Caching

```python
# Using Redis for query result caching
async def get_popular_products():
    cache_key = "popular_products"

    # Check cache
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - query database
    products = await db.fetch_all(
        """
        SELECT * FROM products
        WHERE views > 1000
        ORDER BY views DESC
        LIMIT 20
        """
    )

    # Cache for 10 minutes
    await redis_client.setex(
        cache_key,
        600,
        json.dumps(products)
    )

    return products
```

### Connection Pooling

```python
# PostgreSQL connection pool
import asyncpg

pool = await asyncpg.create_pool(
    host='localhost',
    database='mydb',
    user='user',
    password='password',
    min_size=10,    # Minimum connections
    max_size=20,    # Maximum connections
)

# Use pooled connection
async with pool.acquire() as connection:
    result = await connection.fetch('SELECT * FROM users')
```

### Prepared Statements

```python
# Reuse parsed queries
async with pool.acquire() as conn:
    stmt = await conn.prepare('SELECT * FROM users WHERE id = $1')

    # Execute multiple times without re-parsing
    user1 = await stmt.fetchrow(123)
    user2 = await stmt.fetchrow(456)
```

## Cache Invalidation Strategies

"There are only two hard things in Computer Science: cache invalidation and naming things."

### Time-Based (TTL)

Simplest strategy: data expires after a set time.

```ts
// Cache for 5 minutes
fetch('https://api.example.com/data', {
  next: { revalidate: 300 }
})
```

**Pros**: Simple, predictable
**Cons**: Data can be stale for up to TTL duration

### On-Demand Invalidation

Invalidate cache when data changes.

```ts
// When product is updated
await fetch('/api/revalidate', {
  method: 'POST',
  body: JSON.stringify({ tag: 'products' }),
})
```

**Pros**: Always fresh data
**Cons**: Requires webhook/trigger on every update

### Stale-While-Revalidate

Serve stale content while fetching fresh data in the background.

```http
Cache-Control: max-age=60, stale-while-revalidate=86400
```

**Pros**: Fast response (always from cache), eventually consistent
**Cons**: Users may see stale data briefly

### Write-Through Cache

Update cache atomically with database write.

```python
async def update_user(user_id: str, data: dict):
    # Update database
    await db.execute(
        "UPDATE users SET name = $1 WHERE id = $2",
        data['name'],
        user_id
    )

    # Update cache
    cache_key = f"user:{user_id}"
    await redis_client.setex(
        cache_key,
        3600,
        json.dumps(data)
    )
```

**Pros**: Cache always consistent with database
**Cons**: Slower writes (two operations)

### Cache-Aside Pattern

Application checks cache, fetches from DB on miss, then populates cache.

```python
async def get_user(user_id: str):
    cache_key = f"user:{user_id}"

    # Check cache
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss - fetch from DB
    user = await db.fetch_one(
        "SELECT * FROM users WHERE id = $1",
        user_id
    )

    # Populate cache
    await redis_client.setex(cache_key, 3600, json.dumps(user))

    return user
```

**Pros**: Only caches accessed data
**Cons**: Cache can become stale if DB updated elsewhere

## Anti-Patterns

### Caching User-Specific Data in Public Cache

```http
# BAD: User data cached in CDN
Cache-Control: public, max-age=3600
```

**Result**: User A sees User B's data

**Fix**: Use `private` or `no-store` for user-specific data

### No Cache-Busting for Static Assets

```html
<!-- BAD: Users stuck with old version -->
<script src="/app.js"></script>

<!-- GOOD: Content-addressed filename -->
<script src="/app.abc123.js"></script>
```

**Next.js handles this automatically** for `/_next/static/` files.

### Long TTL Without Invalidation Strategy

```ts
// BAD: Data could be stale for a month
fetch(url, { next: { revalidate: 2592000 } })
```

**Fix**: Use shorter TTL or implement on-demand invalidation.

### Not Varying Cache by Request Headers

```ts
// BAD: Same cache for all languages
fetch('/api/content')

// GOOD: Cache varies by Accept-Language
fetch('/api/content', {
  headers: {
    'Accept-Language': locale,
  },
})
```

### Ignoring Cache Stampede

Multiple requests fetch same data simultaneously when cache expires (thundering herd).

**Fix**: Use request coalescing or stale-while-revalidate.

## Caching Strategy Decision Tree

```
Is the data user-specific?
├─ YES → Use private cache or no-store
│   └─ High traffic? → Server-side cache (Redis) with user-specific keys
└─ NO → Is the data static?
    ├─ YES → Cache-Control: public, max-age=31536000, immutable
    └─ NO → How often does it change?
        ├─ Frequently (< 1 min) → Cache-Control: max-age=60, stale-while-revalidate
        ├─ Periodically (< 1 hour) → Cache-Control: max-age=300 + on-demand invalidation
        └─ Rarely (> 1 hour) → Cache-Control: max-age=3600
```

## Caching Checklist

- [ ] Static assets cached with long TTL and immutable flag
- [ ] HTML pages use stale-while-revalidate pattern
- [ ] User-specific data NOT cached in CDN (use private/no-store)
- [ ] ETags implemented for efficient revalidation
- [ ] CDN configured for public cacheable routes
- [ ] Redis/in-memory cache for hot database queries
- [ ] Database connection pooling configured
- [ ] Cache invalidation strategy defined and implemented
- [ ] Cache keys include relevant parameters (avoid cache poisoning)
- [ ] Monitoring for cache hit rates and effectiveness

## Performance Impact

Effective caching can:
- **Reduce server load**: 70-90% reduction for cacheable content
- **Improve response time**: 10-100x faster (edge cache vs origin)
- **Reduce database load**: 80-95% reduction for popular queries
- **Improve reliability**: Serve stale content during outages
