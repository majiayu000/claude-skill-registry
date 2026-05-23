---
name: redis
description: |
  Implements Redis for session storage, caching, rate limiting, and Bull job queues.
  Use when: implementing caching layers, session management, background jobs, rate limiting, pub/sub messaging, or idempotency keys for payment flows.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Redis Skill

Redis session store, caching, and Bull job queues for Node.js/Express backends. This codebase currently uses in-memory solutions that should be replaced with Redis for production scalability and multi-instance deployments.

## WARNING: Missing Redis Implementation

**Detected:** No `ioredis`, `redis`, or `bullmq` in backend dependencies.
**Impact:** Rate limiting and caching fail across multiple server instances.

```bash
cd backend
npm install ioredis bullmq
npm install -D @types/ioredis
```

## Quick Start

### Redis Client Setup

```typescript
// src/config/redis.ts
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100,
  enableReadyCheck: true,
});

redis.on('error', (err) => console.error('Redis error:', err));
redis.on('connect', () => console.log('Redis connected'));

export { redis };
```

### Replace In-Memory Rate Limiter

```typescript
// src/middleware/redisRateLimiter.ts
import { redis } from '../config/redis';
import { Request, Response, NextFunction } from 'express';

export async function redisRateLimiter(
  key: string,
  maxRequests: number,
  windowMs: number
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const identifier = `ratelimit:${key}:${req.ip}`;
    const current = await redis.incr(identifier);
    
    if (current === 1) {
      await redis.pexpire(identifier, windowMs);
    }
    
    if (current > maxRequests) {
      const ttl = await redis.pttl(identifier);
      res.setHeader('Retry-After', Math.ceil(ttl / 1000));
      return res.status(429).json({ message: 'Too many requests' });
    }
    
    next();
  };
}
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Caching | API response caching | `redis.setex('products:list', 300, JSON.stringify(data))` |
| Rate Limiting | Request throttling | `redis.incr()` with `pexpire()` |
| Sessions | JWT token blacklist | `redis.set('blacklist:token', '1', 'EX', 86400)` |
| Job Queues | Background tasks | `new Queue('emails', { connection: redis })` |
| Pub/Sub | Real-time events | `redis.publish('order:created', orderId)` |

## Common Patterns

### Cache-Aside Pattern

**When:** Caching expensive database queries or API responses.

```typescript
async function getProducts(lang: string): Promise<Product[]> {
  const cacheKey = `products:${lang}`;
  const cached = await redis.get(cacheKey);
  
  if (cached) return JSON.parse(cached);
  
  const products = await productService.getAll(lang);
  await redis.setex(cacheKey, 300, JSON.stringify(products));
  return products;
}
```

### Cache Invalidation

**When:** Data changes and cached values become stale.

```typescript
async function updateProduct(id: number, data: ProductUpdate) {
  await productService.update(id, data);
  
  // Invalidate all product-related caches
  const keys = await redis.keys('products:*');
  if (keys.length) await redis.del(...keys);
}
```

## See Also

- [patterns](references/patterns.md) - Caching, rate limiting, sessions
- [workflows](references/workflows.md) - Setup, Bull queues, monitoring

## Related Skills

- See the **express** skill for middleware integration
- See the **postgresql** skill for cache invalidation on DB changes
- See the **docker** skill for Redis container configuration
- See the **node** skill for async patterns with Redis