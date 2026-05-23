---
name: caching-strategy
description: Implement efficient caching strategies using Redis, Memcached, CDN, and cache invalidation patterns. Use when optimizing application performance, reducing database load, or improving response times.
---

# Caching Strategy

## Overview

Implement effective caching strategies to improve application performance, reduce latency, and decrease load on backend systems.

## When to Use

- Reducing database query load
- Improving API response times
- Handling high traffic loads
- Caching expensive computations
- Storing session data
- CDN integration for static assets
- Implementing distributed caching
- Rate limiting and throttling

## Caching Layers

```
┌─────────────────────────────────────────┐
│         Client Browser Cache            │
├─────────────────────────────────────────┤
│              CDN Cache                  │
├─────────────────────────────────────────┤
│      Application Memory Cache           │
├─────────────────────────────────────────┤
│      Distributed Cache (Redis)          │
├─────────────────────────────────────────┤
│            Database                     │
└─────────────────────────────────────────┘
```

## Implementation Examples

### 1. **Redis Cache Implementation (Node.js)**

```typescript
import Redis from 'ioredis';

interface CacheOptions {
  ttl?: number; // Time to live in seconds
  prefix?: string;
}

class CacheService {
  private redis: Redis;
  private defaultTTL = 3600; // 1 hour

  constructor(redisUrl: string) {
    this.redis = new Redis(redisUrl, {
      retryStrategy: (times) => {
        const delay = Math.min(times * 50, 2000);
        return delay;
      },
      maxRetriesPerRequest: 3
    });

    this.redis.on('connect', () => {
      console.log('Redis connected');
    });

    this.redis.on('error', (error) => {
      console.error('Redis error:', error);
    });
  }

  /**
   * Get cached value
   */
  async get<T>(key: string): Promise<T | null> {
    try {
      const value = await this.redis.get(key);
      if (!value) return null;

      return JSON.parse(value) as T;
    } catch (error) {
      console.error(`Cache get error for key ${key}:`, error);
      return null;
    }
  }

  /**
   * Set cached value
   */
  async set(
    key: string,
    value: any,
    options: CacheOptions = {}
  ): Promise<boolean> {
    try {
      const ttl = options.ttl || this.defaultTTL;
      const serialized = JSON.stringify(value);

      if (ttl > 0) {
        await this.redis.setex(key, ttl, serialized);
      } else {
        await this.redis.set(key, serialized);
      }

      return true;
    } catch (error) {
      console.error(`Cache set error for key ${key}:`, error);
      return false;
    }
  }

  /**
   * Delete cached value
   */
  async delete(key: string): Promise<boolean> {
    try {
      await this.redis.del(key);
      return true;
    } catch (error) {
      console.error(`Cache delete error for key ${key}:`, error);
      return false;
    }
  }

  /**
   * Delete multiple keys by pattern
   */
  async deletePattern(pattern: string): Promise<number> {
    try {
      const keys = await this.redis.keys(pattern);
      if (keys.length === 0) return 0;

      await this.redis.del(...keys);
      return keys.length;
    } catch (error) {
      console.error(`Cache delete pattern error for ${pattern}:`, error);
      return 0;
    }
  }

  /**
   * Get or set pattern - fetch from cache or compute and cache
   */
  async getOrSet<T>(
    key: string,
    fetchFn: () => Promise<T>,
    options: CacheOptions = {}
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.get<T>(key);
    if (cached !== null) {
      return cached;
    }

    // Fetch and cache
    const value = await fetchFn();
    await this.set(key, value, options);

    return value;
  }

  /**
   * Implement cache-aside pattern with stale-while-revalidate
   */
  async getStaleWhileRevalidate<T>(
    key: string,
    fetchFn: () => Promise<T>,
    options: {
      ttl: number;
      staleTime: number;
    }
  ): Promise<T> {
    const cacheKey = `cache:${key}`;
    const timestampKey = `cache:${key}:timestamp`;

    const [cached, timestamp] = await Promise.all([
      this.get<T>(cacheKey),
      this.redis.get(timestampKey)
    ]);

    const now = Date.now();
    const age = timestamp ? now - parseInt(timestamp) : Infinity;

    // Return cached if fresh
    if (cached !== null && age < options.ttl * 1000) {
      return cached;
    }

    // Return stale while revalidating in background
    if (cached !== null && age < options.staleTime * 1000) {
      // Background revalidation
      fetchFn()
        .then(async (fresh) => {
          await this.set(cacheKey, fresh, { ttl: options.ttl });
          await this.redis.set(timestampKey, now.toString());
        })
        .catch(console.error);

      return cached;
    }

    // Fetch fresh data
    const fresh = await fetchFn();
    await Promise.all([
      this.set(cacheKey, fresh, { ttl: options.ttl }),
      this.redis.set(timestampKey, now.toString())
    ]);

    return fresh;
  }

  /**
   * Increment counter with TTL
   */
  async increment(key: string, ttl?: number): Promise<number> {
    const count = await this.redis.incr(key);

    if (count === 1 && ttl) {
      await this.redis.expire(key, ttl);
    }

    return count;
  }

  /**
   * Check if key exists
   */
  async exists(key: string): Promise<boolean> {
    const result = await this.redis.exists(key);
    return result === 1;
  }

  /**
   * Get remaining TTL
   */
  async ttl(key: string): Promise<number> {
    return await this.redis.ttl(key);
  }

  /**
   * Close connection
   */
  async disconnect(): Promise<void> {
    await this.redis.quit();
  }
}

// Usage
const cache = new CacheService('redis://localhost:6379');

// Simple get/set
await cache.set('user:123', { name: 'John', age: 30 }, { ttl: 3600 });
const user = await cache.get('user:123');

// Get or set pattern
const posts = await cache.getOrSet(
  'posts:recent',
  async () => {
    return await database.query('SELECT * FROM posts ORDER BY created_at DESC LIMIT 10');
  },
  { ttl: 300 }
);

// Stale-while-revalidate
const data = await cache.getStaleWhileRevalidate(
  'expensive-query',
  async () => await runExpensiveQuery(),
  { ttl: 300, staleTime: 600 }
);
```

### 2. **Cache Decorator (Python)**

```python
import functools
import json
import hashlib
from typing import Any, Callable, Optional
from redis import Redis
import time

class CacheDecorator:
    def __init__(self, redis_client: Redis, ttl: int = 3600):
        self.redis = redis_client
        self.ttl = ttl

    def cache_key(self, func: Callable, *args, **kwargs) -> str:
        """Generate cache key from function name and arguments."""
        # Create deterministic key from function and arguments
        key_parts = [
            func.__module__,
            func.__name__,
            str(args),
            str(sorted(kwargs.items()))
        ]
        key_string = ':'.join(key_parts)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return f"cache:{func.__name__}:{key_hash}"

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = self.cache_key(func, *args, **kwargs)

            # Try to get from cache
            cached = self.redis.get(cache_key)
            if cached:
                print(f"Cache HIT: {cache_key}")
                return json.loads(cached)

            # Cache miss - execute function
            print(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)

            # Store in cache
            self.redis.setex(
                cache_key,
                self.ttl,
                json.dumps(result)
            )

            return result

        # Add cache invalidation method
        def invalidate(*args, **kwargs):
            cache_key = self.cache_key(func, *args, **kwargs)
            self.redis.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper


# Usage
redis = Redis(host='localhost', port=6379, db=0)
cache = CacheDecorator(redis, ttl=300)

@cache
def get_user_profile(user_id: int) -> dict:
    """Fetch user profile from database."""
    print(f"Fetching user {user_id} from database...")
    # Simulate database query
    time.sleep(1)
    return {
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    }

# First call - cache miss
profile = get_user_profile(123)  # Takes 1 second

# Second call - cache hit
profile = get_user_profile(123)  # Instant

# Invalidate cache
get_user_profile.invalidate(123)
```

### 3. **Multi-Level Cache**

```typescript
interface CacheLevel {
  get(key: string): Promise<any>;
  set(key: string, value: any, ttl?: number): Promise<void>;
  delete(key: string): Promise<void>;
}

class MemoryCache implements CacheLevel {
  private cache = new Map<string, { value: any; expiry: number }>();

  async get(key: string): Promise<any> {
    const item = this.cache.get(key);
    if (!item) return null;

    if (Date.now() > item.expiry) {
      this.cache.delete(key);
      return null;
    }

    return item.value;
  }

  async set(key: string, value: any, ttl: number = 60): Promise<void> {
    this.cache.set(key, {
      value,
      expiry: Date.now() + ttl * 1000
    });
  }

  async delete(key: string): Promise<void> {
    this.cache.delete(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

class RedisCache implements CacheLevel {
  constructor(private redis: Redis) {}

  async get(key: string): Promise<any> {
    const value = await this.redis.get(key);
    return value ? JSON.parse(value) : null;
  }

  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async delete(key: string): Promise<void> {
    await this.redis.del(key);
  }
}

class MultiLevelCache {
  private levels: CacheLevel[];

  constructor(levels: CacheLevel[]) {
    this.levels = levels; // Ordered from fastest to slowest
  }

  async get<T>(key: string): Promise<T | null> {
    for (let i = 0; i < this.levels.length; i++) {
      const value = await this.levels[i].get(key);

      if (value !== null) {
        // Backfill faster caches
        for (let j = 0; j < i; j++) {
          await this.levels[j].set(key, value);
        }

        return value as T;
      }
    }

    return null;
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    // Set in all cache levels
    await Promise.all(
      this.levels.map(level => level.set(key, value, ttl))
    );
  }

  async delete(key: string): Promise<void> {
    await Promise.all(
      this.levels.map(level => level.delete(key))
    );
  }
}

// Usage
const cache = new MultiLevelCache([
  new MemoryCache(),
  new RedisCache(redis)
]);

// Get from fastest available cache
const data = await cache.get('user:123');

// Set in all caches
await cache.set('user:123', userData, 3600);
```

### 4. **Cache Invalidation Strategies**

```typescript
class CacheInvalidation {
  constructor(private cache: CacheService) {}

  /**
   * Time-based invalidation (TTL)
   */
  async setWithTTL(key: string, value: any, seconds: number): Promise<void> {
    await this.cache.set(key, value, { ttl: seconds });
  }

  /**
   * Tag-based invalidation
   */
  async setWithTags(
    key: string,
    value: any,
    tags: string[]
  ): Promise<void> {
    // Store value
    await this.cache.set(key, value);

    // Store tag associations
    for (const tag of tags) {
      await this.cache.redis.sadd(`tag:${tag}`, key);
    }
  }

  async invalidateByTag(tag: string): Promise<number> {
    // Get all keys with this tag
    const keys = await this.cache.redis.smembers(`tag:${tag}`);

    if (keys.length === 0) return 0;

    // Delete all keys
    await Promise.all(
      keys.map(key => this.cache.delete(key))
    );

    // Delete tag set
    await this.cache.redis.del(`tag:${tag}`);

    return keys.length;
  }

  /**
   * Event-based invalidation
   */
  async invalidateOnEvent(
    entity: string,
    id: string,
    event: 'create' | 'update' | 'delete'
  ): Promise<void> {
    const patterns = [
      `${entity}:${id}`,
      `${entity}:${id}:*`,
      `${entity}:list:*`,
      `${entity}:count`
    ];

    for (const pattern of patterns) {
      await this.cache.deletePattern(pattern);
    }
  }

  /**
   * Version-based invalidation
   */
  async setVersioned(
    key: string,
    value: any,
    version: number
  ): Promise<void> {
    const versionedKey = `${key}:v${version}`;
    await this.cache.set(versionedKey, value);
    await this.cache.set(`${key}:version`, version);
  }

  async getVersioned(key: string): Promise<any> {
    const version = await this.cache.get<number>(`${key}:version`);
    if (!version) return null;

    return await this.cache.get(`${key}:v${version}`);
  }
}
```

### 5. **HTTP Caching Headers**

```typescript
import express from 'express';

const app = express();

// Cache-Control middleware
function cacheControl(maxAge: number, options: {
  private?: boolean;
  noStore?: boolean;
  noCache?: boolean;
  mustRevalidate?: boolean;
  staleWhileRevalidate?: number;
} = {}) {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const directives: string[] = [];

    if (options.noStore) {
      directives.push('no-store');
    } else if (options.noCache) {
      directives.push('no-cache');
    } else {
      directives.push(options.private ? 'private' : 'public');
      directives.push(`max-age=${maxAge}`);

      if (options.staleWhileRevalidate) {
        directives.push(`stale-while-revalidate=${options.staleWhileRevalidate}`);
      }
    }

    if (options.mustRevalidate) {
      directives.push('must-revalidate');
    }

    res.setHeader('Cache-Control', directives.join(', '));
    next();
  };
}

// Static assets - long cache
app.use('/static', cacheControl(31536000), express.static('public'));

// API - short cache with revalidation
app.get('/api/data',
  cacheControl(60, { staleWhileRevalidate: 300 }),
  (req, res) => {
    res.json({ data: 'cached for 60s' });
  }
);

// Dynamic content - no cache
app.get('/api/user/profile',
  cacheControl(0, { private: true, noCache: true }),
  (req, res) => {
    res.json({ user: 'always fresh' });
  }
);

// ETag support
app.get('/api/resource/:id', async (req, res) => {
  const resource = await getResource(req.params.id);
  const etag = generateETag(resource);

  res.setHeader('ETag', etag);

  // Check if client has current version
  if (req.headers['if-none-match'] === etag) {
    return res.status(304).end();
  }

  res.json(resource);
});

function generateETag(data: any): string {
  return require('crypto')
    .createHash('md5')
    .update(JSON.stringify(data))
    .digest('hex');
}
```

## Best Practices

### ✅ DO
- Set appropriate TTL values
- Implement cache warming for critical data
- Use cache-aside pattern for reads
- Monitor cache hit rates
- Implement graceful degradation on cache failure
- Use compression for large cached values
- Namespace cache keys properly
- Implement cache stampede prevention
- Use consistent hashing for distributed caching
- Monitor cache memory usage

### ❌ DON'T
- Cache everything indiscriminately
- Use caching as a fix for poor database design
- Store sensitive data without encryption
- Forget to handle cache misses
- Set TTL too long for frequently changing data
- Ignore cache invalidation strategies
- Cache without monitoring
- Store large objects without consideration

## Cache Strategies

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Cache-Aside** | Application checks cache, loads from DB on miss | General purpose |
| **Write-Through** | Write to cache and DB simultaneously | Strong consistency needed |
| **Write-Behind** | Write to cache, async write to DB | High write throughput |
| **Refresh-Ahead** | Proactively refresh before expiry | Predictable access patterns |
| **Read-Through** | Cache loads from DB automatically | Simplified code |

## Resources

- [Redis Documentation](https://redis.io/documentation)
- [Cache-Control Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
- [Caching Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/BestPractices.html)
