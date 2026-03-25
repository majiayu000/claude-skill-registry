---
name: caching-patterns
description: Redis caching strategies, cache invalidation, write-through/write-behind, TTL management, and cache stampede protection.
---

# Caching Patterns

Redis-based caching strategies for reducing latency and database load.

## Cache Key Design

```typescript
// Namespace:entity:id format
const CacheKeys = {
  market: (id: string) => `market:v1:${id}`,
  marketList: (filters: string) => `market:list:${filters}`,
  user: (id: string) => `user:v1:${id}`,
  userMarkets: (userId: string, page: number) => `user:${userId}:markets:${page}`,
  leaderboard: () => 'leaderboard:v1:global'
}

// Version prefix allows instant cache bust on schema change:
// bump v1 → v2 to invalidate all market keys without scanning
```

## Cache-Aside (Lazy Loading)

```typescript
import Redis from 'ioredis'

const redis = new Redis(process.env.REDIS_URL!)
const DEFAULT_TTL = 300  // 5 minutes

async function getOrSet<T>(
  key: string,
  loader: () => Promise<T>,
  ttl = DEFAULT_TTL
): Promise<T> {
  const cached = await redis.get(key)
  if (cached) return JSON.parse(cached) as T

  const value = await loader()
  await redis.setex(key, ttl, JSON.stringify(value))
  return value
}

// Usage
async function getMarket(id: string): Promise<Market> {
  return getOrSet(
    CacheKeys.market(id),
    () => db.market.findUniqueOrThrow({ where: { id } }),
    300
  )
}
```

## Write-Through Pattern

```typescript
// Write to cache AND database together - cache is always fresh
async function updateMarket(id: string, data: UpdateMarketDto): Promise<Market> {
  const updated = await db.market.update({ where: { id }, data })

  // Synchronously update cache so next read is fresh
  await redis.setex(CacheKeys.market(id), DEFAULT_TTL, JSON.stringify(updated))

  return updated
}

async function deleteMarket(id: string): Promise<void> {
  await db.market.delete({ where: { id } })
  await redis.del(CacheKeys.market(id))
}
```

## Write-Behind (Write-Back) Pattern

```typescript
// Write to cache immediately, flush to DB asynchronously (higher throughput)
// Risk: data loss on crash if queue not durable

class WriteBehindCache {
  private dirtyKeys = new Set<string>()
  private flushInterval: NodeJS.Timeout

  constructor(private flushEveryMs = 1000) {
    this.flushInterval = setInterval(() => this.flush(), flushEveryMs)
  }

  async write(key: string, value: unknown, dbWriter: () => Promise<void>): Promise<void> {
    // Instant cache update
    await redis.setex(key, DEFAULT_TTL, JSON.stringify(value))
    this.dirtyKeys.add(key)

    // Schedule DB write
    dbWriter().catch(err => {
      console.error(`Write-behind flush failed for ${key}:`, err)
      this.dirtyKeys.add(key)  // re-queue
    })
  }

  private async flush(): Promise<void> {
    // Implementation: drain dirty keys to DB in batch
    this.dirtyKeys.clear()
  }

  destroy(): void {
    clearInterval(this.flushInterval)
  }
}
```

## Cache Stampede Protection

```typescript
// Problem: 1000 concurrent requests on cache miss → 1000 DB queries
// Solution: mutex lock - only first request queries DB, rest wait

import { Mutex } from 'async-mutex'

const mutexMap = new Map<string, Mutex>()

function getMutex(key: string): Mutex {
  if (!mutexMap.has(key)) {
    mutexMap.set(key, new Mutex())
    // Cleanup after 30s to prevent memory leak
    setTimeout(() => mutexMap.delete(key), 30_000)
  }
  return mutexMap.get(key)!
}

async function getWithMutex<T>(
  key: string,
  loader: () => Promise<T>,
  ttl = DEFAULT_TTL
): Promise<T> {
  const cached = await redis.get(key)
  if (cached) return JSON.parse(cached) as T

  const mutex = getMutex(key)

  return mutex.runExclusive(async () => {
    // Double-check after acquiring lock
    const rechecked = await redis.get(key)
    if (rechecked) return JSON.parse(rechecked) as T

    const value = await loader()
    await redis.setex(key, ttl, JSON.stringify(value))
    return value
  })
}

// Probabilistic Early Expiration (alternative, no lock needed)
async function getWithEarlyExpire<T>(
  key: string,
  loader: () => Promise<T>,
  ttl = DEFAULT_TTL,
  beta = 1
): Promise<T> {
  const raw = await redis.get(key)

  if (raw) {
    const { value, expires } = JSON.parse(raw) as { value: T; expires: number }
    const ttlRemaining = (expires - Date.now()) / 1000
    // Probabilistically re-fetch before expiry
    if (ttlRemaining - beta * Math.log(Math.random()) > 0) {
      return value
    }
  }

  const value = await loader()
  const payload = { value, expires: Date.now() + ttl * 1000 }
  await redis.setex(key, ttl, JSON.stringify(payload))
  return value
}
```

## Multi-Level Caching (L1 Memory + L2 Redis)

```typescript
import LRU from 'lru-cache'

const l1 = new LRU<string, unknown>({
  max: 500,           // max 500 items in memory
  ttl: 30_000         // 30 seconds
})

async function getMultiLevel<T>(
  key: string,
  loader: () => Promise<T>,
  l2Ttl = DEFAULT_TTL
): Promise<T> {
  // L1: in-process memory (0ms)
  const l1Hit = l1.get(key) as T | undefined
  if (l1Hit !== undefined) return l1Hit

  // L2: Redis (~1ms)
  const l2Hit = await redis.get(key)
  if (l2Hit) {
    const value = JSON.parse(l2Hit) as T
    l1.set(key, value)  // warm L1
    return value
  }

  // L3: Database (~10ms+)
  const value = await loader()
  l1.set(key, value)
  await redis.setex(key, l2Ttl, JSON.stringify(value))
  return value
}

async function invalidateMultiLevel(key: string): Promise<void> {
  l1.delete(key)
  await redis.del(key)
}
```

## Event-Based Cache Invalidation

```typescript
// Instead of TTL-only, invalidate on data change events
import { EventEmitter } from 'events'

const cacheEvents = new EventEmitter()

// Emit on mutations
async function resolveMarket(id: string, outcome: string): Promise<void> {
  await db.market.update({ where: { id }, data: { status: 'resolved', outcome } })
  cacheEvents.emit('market:updated', id)
}

// Subscribe and invalidate
cacheEvents.on('market:updated', async (id: string) => {
  await redis.del(CacheKeys.market(id))
  // Also bust list caches containing this market
  const listKeys = await redis.keys('market:list:*')
  if (listKeys.length) await redis.del(...listKeys)
})
```

## Cache Warming

```typescript
// Pre-populate cache before traffic hits (e.g., after deploy)
async function warmCache(): Promise<void> {
  console.log('Warming cache...')

  // Top markets by volume
  const topMarkets = await db.market.findMany({
    take: 100,
    orderBy: { volume: 'desc' }
  })

  const pipeline = redis.pipeline()
  for (const market of topMarkets) {
    pipeline.setex(CacheKeys.market(market.id), 3600, JSON.stringify(market))
  }
  await pipeline.exec()

  console.log(`Cache warmed: ${topMarkets.length} markets`)
}

// Call on app startup
app.on('ready', warmCache)
```

## Monitoring Cache Health

```typescript
async function getCacheStats(): Promise<{
  hitRate: number
  memoryUsed: string
  connectedClients: number
  keyCount: number
}> {
  const info = await redis.info('stats')
  const memory = await redis.info('memory')
  const clients = await redis.info('clients')

  const hits = parseInt(info.match(/keyspace_hits:(\d+)/)?.[1] || '0')
  const misses = parseInt(info.match(/keyspace_misses:(\d+)/)?.[1] || '0')
  const total = hits + misses

  return {
    hitRate: total > 0 ? hits / total : 0,
    memoryUsed: memory.match(/used_memory_human:(.+)/)?.[1]?.trim() || 'unknown',
    connectedClients: parseInt(clients.match(/connected_clients:(\d+)/)?.[1] || '0'),
    keyCount: await redis.dbsize()
  }
}

// Alert if hit rate drops below 70%
setInterval(async () => {
  const stats = await getCacheStats()
  if (stats.hitRate < 0.7) {
    console.warn(`Low cache hit rate: ${(stats.hitRate * 100).toFixed(1)}%`)
  }
}, 60_000)
```

## Common Pitfalls

```
Cache penetration: requests for non-existent keys bypass cache every time
  → Cache null results with short TTL (30s)

Thundering herd: many requests hit DB simultaneously on cache expiry
  → Use mutex lock or probabilistic early expiration

Stale data: cache serves outdated values after DB update
  → Use write-through or event-based invalidation, not only TTL

Hot key: single cache key gets millions of requests/sec
  → Shard into multiple keys or replicate across Redis cluster

Big value: storing 10MB JSON in a single key blocks Redis
  → Compress with msgpack, split into smaller units, use streaming
```

**Remember**: Cache is eventually consistent by design. Design your system to tolerate brief staleness, and use invalidation events for correctness-critical data.
