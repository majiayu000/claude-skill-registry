---
name: redis-cache
description: Implement or debug Redis caching strategies using the centralized Upstash Redis client. Use when adding cache layers, debugging cache issues, or optimizing cache invalidation.
allowed-tools: Read, Edit, Grep, Glob
---

# Redis Cache Management Skill

This skill helps you implement and optimize Redis caching in `packages/utils/` and across the monorepo.

## When to Use This Skill

- Implementing caching for expensive database queries
- Adding cache layers to API endpoints
- Debugging cache hit/miss issues
- Implementing cache invalidation strategies
- Optimizing cache TTL (Time To Live)
- Setting up cache warming
- Managing cache keys and namespaces

## Redis Architecture

The project uses **Upstash Redis** with a centralized client:

```
packages/utils/
├── src/
│   └── redis.ts          # Centralized Redis client
apps/api/
├── src/
│   └── lib/
│       └── cache/
│           ├── cars.ts   # Cars data caching
│           ├── coe.ts    # COE data caching
│           └── posts.ts  # Blog posts caching
```

## Centralized Redis Client

```typescript
// packages/utils/src/redis.ts
import { Redis } from "@upstash/redis";

if (!process.env.UPSTASH_REDIS_REST_URL) {
  throw new Error("UPSTASH_REDIS_REST_URL is not defined");
}

if (!process.env.UPSTASH_REDIS_REST_TOKEN) {
  throw new Error("UPSTASH_REDIS_REST_TOKEN is not defined");
}

export const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});
```

Export from package:

```typescript
// packages/utils/src/index.ts
export { redis } from "./redis";
```

## Basic Cache Patterns

### Simple Get/Set

```typescript
import { redis } from "@sgcarstrends/utils";

// Set value
await redis.set("key", "value");

// Get value
const value = await redis.get("key");
console.log(value); // "value"

// Set with expiration (in seconds)
await redis.set("key", "value", { ex: 3600 }); // Expires in 1 hour

// Set if not exists
await redis.setnx("key", "value");
```

### JSON Data Caching

```typescript
import { redis } from "@sgcarstrends/utils";

// Cache object
const car = { make: "Toyota", model: "Camry", year: 2024 };
await redis.set("car:1", JSON.stringify(car));

// Retrieve object
const cached = await redis.get("car:1");
const parsedCar = JSON.parse(cached as string);
```

### Cache with Type Safety

```typescript
import { redis } from "@sgcarstrends/utils";

interface Car {
  make: string;
  model: string;
  year: number;
}

async function getCachedCar(id: string): Promise<Car | null> {
  const cached = await redis.get<string>(`car:${id}`);

  if (!cached) return null;

  return JSON.parse(cached) as Car;
}

async function setCachedCar(id: string, car: Car, ttl: number = 3600) {
  await redis.set(`car:${id}`, JSON.stringify(car), { ex: ttl });
}
```

## Caching Strategies

### Cache-Aside (Lazy Loading)

Most common pattern - check cache first, then database:

```typescript
// apps/api/src/lib/cache/cars.ts
import { redis } from "@sgcarstrends/utils";
import { db } from "@sgcarstrends/database";
import { cars } from "@sgcarstrends/database/schema";
import { eq } from "drizzle-orm";

export async function getCarWithCache(id: string) {
  const cacheKey = `car:${id}`;

  // 1. Try to get from cache
  const cached = await redis.get<string>(cacheKey);

  if (cached) {
    console.log("Cache hit!");
    return JSON.parse(cached);
  }

  console.log("Cache miss!");

  // 2. If not in cache, get from database
  const car = await db.query.cars.findFirst({
    where: eq(cars.id, id),
  });

  if (!car) {
    return null;
  }

  // 3. Store in cache for next time
  await redis.set(cacheKey, JSON.stringify(car), {
    ex: 3600, // 1 hour TTL
  });

  return car;
}
```

### Write-Through Cache

Update cache when writing to database:

```typescript
import { redis } from "@sgcarstrends/utils";
import { db } from "@sgcarstrends/database";
import { cars } from "@sgcarstrends/database/schema";

export async function createCarWithCache(carData: NewCar) {
  // 1. Write to database
  const [car] = await db.insert(cars).values(carData).returning();

  // 2. Write to cache
  await redis.set(`car:${car.id}`, JSON.stringify(car), { ex: 3600 });

  // 3. Invalidate list caches
  await redis.del("cars:all");

  return car;
}

export async function updateCarWithCache(id: string, updates: Partial<Car>) {
  // 1. Update database
  const [car] = await db
    .update(cars)
    .set(updates)
    .where(eq(cars.id, id))
    .returning();

  // 2. Update cache
  await redis.set(`car:${id}`, JSON.stringify(car), { ex: 3600 });

  // 3. Invalidate related caches
  await redis.del("cars:all");
  await redis.del(`cars:make:${car.make}`);

  return car;
}
```

### Cache Invalidation

```typescript
import { redis } from "@sgcarstrends/utils";

// Delete single key
export async function invalidateCarCache(id: string) {
  await redis.del(`car:${id}`);
}

// Delete multiple keys
export async function invalidateCarCaches(ids: string[]) {
  const keys = ids.map(id => `car:${id}`);
  await redis.del(...keys);
}

// Delete by pattern (use sparingly - expensive operation)
export async function invalidateCarsByPattern(pattern: string) {
  const keys = await redis.keys(pattern);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
}

// Example: Invalidate all car caches
await invalidateCarsByPattern("car:*");
```

## Cache Key Strategies

### Key Naming Conventions

```typescript
// Good key naming patterns
const keys = {
  // Entity by ID
  car: (id: string) => `car:${id}`,
  coe: (id: string) => `coe:${id}`,

  // List/Collection
  allCars: () => "cars:all",
  carsByMake: (make: string) => `cars:make:${make}`,
  carsByMonth: (month: string) => `cars:month:${month}`,

  // Computed/Aggregated
  carStats: (month: string) => `stats:cars:${month}`,
  coeStats: (biddingNo: number) => `stats:coe:${biddingNo}`,

  // User-specific
  userPreferences: (userId: string) => `user:${userId}:preferences`,

  // Session
  session: (sessionId: string) => `session:${sessionId}`,
};

// Usage
await redis.set(keys.car("123"), JSON.stringify(carData));
await redis.get(keys.carsByMake("Toyota"));
```

### Namespacing

```typescript
const CACHE_PREFIX = "sgcarstrends";

function buildKey(...parts: string[]): string {
  return [CACHE_PREFIX, ...parts].join(":");
}

// Usage
const key = buildKey("cars", "make", "Toyota"); // "sgcarstrends:cars:make:Toyota"
```

## TTL Strategies

### Time-Based Expiration

```typescript
// Different TTLs for different data types
const TTL = {
  SHORT: 60,          // 1 minute - rapidly changing data
  MEDIUM: 300,        // 5 minutes - moderately changing data
  LONG: 3600,         // 1 hour - slowly changing data
  DAY: 86400,         // 24 hours - daily data
  WEEK: 604800,       // 7 days - weekly data
  MONTH: 2592000,     // 30 days - monthly data
};

// Usage
await redis.set("realtime-data", data, { ex: TTL.SHORT });
await redis.set("daily-stats", stats, { ex: TTL.DAY });
await redis.set("monthly-report", report, { ex: TTL.MONTH });
```

### Conditional Expiration

```typescript
async function cacheWithSmartTTL(key: string, data: any) {
  const now = new Date();
  const hour = now.getHours();

  let ttl: number;

  // Short TTL during business hours (more frequent updates)
  if (hour >= 9 && hour <= 18) {
    ttl = 300; // 5 minutes
  } else {
    ttl = 3600; // 1 hour off-hours
  }

  await redis.set(key, JSON.stringify(data), { ex: ttl });
}
```

## Advanced Patterns

### Cache Stampede Prevention

Prevent multiple requests from hitting database simultaneously:

```typescript
import { redis } from "@sgcarstrends/utils";

async function getWithStampedePrevention<T>(
  key: string,
  fetchFn: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  // Try to get from cache
  const cached = await redis.get<string>(key);
  if (cached) {
    return JSON.parse(cached) as T;
  }

  // Use a lock to prevent stampede
  const lockKey = `${key}:lock`;
  const lockAcquired = await redis.setnx(lockKey, "1");

  if (lockAcquired) {
    // This request will fetch the data
    try {
      await redis.expire(lockKey, 10); // Lock expires in 10 seconds

      const data = await fetchFn();

      await redis.set(key, JSON.stringify(data), { ex: ttl });

      return data;
    } finally {
      await redis.del(lockKey);
    }
  } else {
    // Wait for the other request to finish
    await new Promise(resolve => setTimeout(resolve, 100));

    // Try again
    return getWithStampedePrevention(key, fetchFn, ttl);
  }
}

// Usage
const cars = await getWithStampedePrevention(
  "cars:all",
  () => db.query.cars.findMany(),
  3600
);
```

### Stale-While-Revalidate

Serve stale data while refreshing in background:

```typescript
async function getWithSWR<T>(
  key: string,
  fetchFn: () => Promise<T>,
  ttl: number = 3600,
  staleTime: number = 300
): Promise<T> {
  const cached = await redis.get<string>(key);

  if (cached) {
    const data = JSON.parse(cached) as T;

    // Check if data is stale
    const ttlRemaining = await redis.ttl(key);

    if (ttlRemaining < staleTime) {
      // Data is stale, refresh in background
      fetchFn().then(freshData => {
        redis.set(key, JSON.stringify(freshData), { ex: ttl });
      });
    }

    return data;
  }

  // No cache, fetch and cache
  const data = await fetchFn();
  await redis.set(key, JSON.stringify(data), { ex: ttl });

  return data;
}
```

### Layered Caching

Combine memory cache with Redis:

```typescript
import { LRUCache } from "lru-cache";
import { redis } from "@sgcarstrends/utils";

// In-memory L1 cache
const memoryCache = new LRUCache<string, any>({
  max: 500,
  ttl: 60000, // 1 minute
});

async function getWithLayeredCache<T>(
  key: string,
  fetchFn: () => Promise<T>
): Promise<T> {
  // 1. Check memory cache (L1)
  const memCached = memoryCache.get(key);
  if (memCached) {
    console.log("L1 cache hit");
    return memCached as T;
  }

  // 2. Check Redis cache (L2)
  const redisCached = await redis.get<string>(key);
  if (redisCached) {
    console.log("L2 cache hit");
    const data = JSON.parse(redisCached) as T;

    // Populate L1 cache
    memoryCache.set(key, data);

    return data;
  }

  // 3. Fetch from source
  console.log("Cache miss");
  const data = await fetchFn();

  // Populate both caches
  memoryCache.set(key, data);
  await redis.set(key, JSON.stringify(data), { ex: 3600 });

  return data;
}
```

## Rate Limiting with Redis

```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { redis } from "@sgcarstrends/utils";

// Create rate limiter
const ratelimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "10 s"), // 10 requests per 10 seconds
});

// Use in API route
export async function apiHandler(req: Request) {
  const ip = req.headers.get("x-forwarded-for") ?? "unknown";

  const { success, limit, reset, remaining } = await ratelimit.limit(ip);

  if (!success) {
    return new Response("Rate limit exceeded", {
      status: 429,
      headers: {
        "X-RateLimit-Limit": limit.toString(),
        "X-RateLimit-Remaining": remaining.toString(),
        "X-RateLimit-Reset": new Date(reset).toISOString(),
      },
    });
  }

  // Process request...
}
```

## Cache Warming

Pre-populate cache with frequently accessed data:

```typescript
import { redis } from "@sgcarstrends/utils";
import { db } from "@sgcarstrends/database";

export async function warmCarCache() {
  console.log("Warming car cache...");

  // Get frequently accessed makes
  const topMakes = ["Toyota", "Honda", "BMW", "Mercedes"];

  for (const make of topMakes) {
    const cars = await db.query.cars.findMany({
      where: eq(cars.make, make),
    });

    await redis.set(
      `cars:make:${make}`,
      JSON.stringify(cars),
      { ex: 3600 }
    );

    console.log(`Cached ${cars.length} cars for ${make}`);
  }

  console.log("Cache warming complete!");
}

// Run on application startup or scheduled job
```

## Monitoring and Debugging

### Cache Hit/Miss Tracking

```typescript
let cacheHits = 0;
let cacheMisses = 0;

async function getWithMetrics<T>(
  key: string,
  fetchFn: () => Promise<T>
): Promise<T> {
  const cached = await redis.get<string>(key);

  if (cached) {
    cacheHits++;
    console.log(`Cache hit rate: ${(cacheHits / (cacheHits + cacheMisses) * 100).toFixed(2)}%`);
    return JSON.parse(cached) as T;
  }

  cacheMisses++;
  const data = await fetchFn();
  await redis.set(key, JSON.stringify(data), { ex: 3600 });

  return data;
}
```

### Cache Size Monitoring

```typescript
async function getCacheStats() {
  const info = await redis.info();
  const dbsize = await redis.dbsize();

  return {
    dbsize,
    info,
  };
}
```

## Testing Cache Logic

```typescript
// __tests__/cache/cars.test.ts
import { describe, it, expect, beforeEach, vi } from "vitest";
import { redis } from "@sgcarstrends/utils";
import { getCarWithCache } from "../cache/cars";

// Mock Redis
vi.mock("@sgcarstrends/utils", () => ({
  redis: {
    get: vi.fn(),
    set: vi.fn(),
    del: vi.fn(),
  },
}));

describe("Car Cache", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns cached data when available", async () => {
    const cachedCar = { id: "1", make: "Toyota" };

    vi.mocked(redis.get).mockResolvedValue(JSON.stringify(cachedCar));

    const result = await getCarWithCache("1");

    expect(result).toEqual(cachedCar);
    expect(redis.get).toHaveBeenCalledWith("car:1");
  });

  it("fetches from database on cache miss", async () => {
    vi.mocked(redis.get).mockResolvedValue(null);

    const result = await getCarWithCache("1");

    expect(redis.get).toHaveBeenCalled();
    expect(redis.set).toHaveBeenCalled();
  });
});
```

## Environment Variables

Required environment variables:

```env
# Upstash Redis
UPSTASH_REDIS_REST_URL=https://your-instance.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token-here
```

## Common Pitfalls

### 1. Caching Mutable Objects

```typescript
// ❌ Bad - caching object reference
const data = { count: 1 };
await redis.set("key", data); // Won't work!

// ✅ Good - serialize to JSON
await redis.set("key", JSON.stringify(data));
```

### 2. Not Setting TTL

```typescript
// ❌ Bad - data never expires
await redis.set("key", "value");

// ✅ Good - set appropriate TTL
await redis.set("key", "value", { ex: 3600 });
```

### 3. Cache Invalidation Bugs

```typescript
// ❌ Bad - forgot to invalidate related caches
await db.update(cars).set({ make: "Honda" });

// ✅ Good - invalidate all related caches
await db.update(cars).set({ make: "Honda" });
await redis.del(`car:${id}`);
await redis.del("cars:all");
await redis.del(`cars:make:Toyota`);
await redis.del(`cars:make:Honda`);
```

## References

- Upstash Redis: Use Context7 for latest docs
- Related files:
  - `packages/utils/src/redis.ts` - Redis client
  - `apps/api/src/lib/cache/` - Cache implementations
  - Root CLAUDE.md - Project documentation

## Best Practices

1. **Always Set TTL**: Prevent unbounded cache growth
2. **Serialize Data**: Use JSON.stringify/parse for objects
3. **Key Naming**: Use consistent, descriptive key patterns
4. **Invalidation**: Invalidate cache on writes
5. **Error Handling**: Gracefully handle Redis failures
6. **Monitoring**: Track cache hit/miss rates
7. **Testing**: Test cache logic thoroughly
8. **Layered Caching**: Consider L1 (memory) + L2 (Redis)
