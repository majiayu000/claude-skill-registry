---
name: redis-expert
version: 1.0.0
description: Expert-level Redis for caching, pub/sub, data structures, and high-performance applications
category: data
tags: [redis, cache, pubsub, inmemory, keyvalue, nosql]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(redis-cli:*, docker:*)
---

# Redis Expert

Expert guidance for Redis - the in-memory data structure store used as cache, message broker, and database with microsecond latency.

## Core Concepts

### Data Structures
- Strings (binary-safe, up to 512MB)
- Lists (linked lists)
- Sets (unordered unique strings)
- Sorted Sets (sets ordered by score)
- Hashes (field-value pairs)
- Streams (append-only log)
- Bitmaps and HyperLogLog
- Geospatial indexes

### Key Features
- In-memory storage with persistence
- Pub/Sub messaging
- Transactions
- Lua scripting
- Pipelining
- Master-Replica replication
- Redis Sentinel (high availability)
- Redis Cluster (horizontal scaling)

### Use Cases
- Caching layer
- Session storage
- Real-time analytics
- Message queues
- Rate limiting
- Leaderboards
- Geospatial queries

## Installation and Configuration

### Docker Setup
```bash
# Development
docker run --name redis -p 6379:6379 -d redis:7-alpine

# Production with persistence
docker run --name redis \
  -p 6379:6379 \
  -v redis-data:/data \
  -d redis:7-alpine \
  redis-server --appendonly yes --requirepass strongpassword

# Redis with config file
docker run --name redis \
  -p 6379:6379 \
  -v ./redis.conf:/usr/local/etc/redis/redis.conf \
  -d redis:7-alpine \
  redis-server /usr/local/etc/redis/redis.conf
```

### Configuration (redis.conf)
```conf
# Network
bind 0.0.0.0
port 6379
protected-mode yes

# Security
requirepass strongpassword

# Memory
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1      # Save after 900s if 1 key changed
save 300 10     # Save after 300s if 10 keys changed
save 60 10000   # Save after 60s if 10000 keys changed

appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec

# Replication
replica-read-only yes
repl-diskless-sync yes

# Performance
tcp-backlog 511
timeout 0
tcp-keepalive 300
```

## Node.js Client (ioredis)

### Basic Operations
```typescript
import Redis from 'ioredis';

const redis = new Redis({
  host: 'localhost',
  port: 6379,
  password: 'strongpassword',
  db: 0,
  retryStrategy: (times) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  },
});

// Strings
await redis.set('user:1000:name', 'Alice');
await redis.set('counter', 42);
await redis.get('user:1000:name'); // 'Alice'

// Expiration (TTL)
await redis.setex('session:abc123', 3600, JSON.stringify({ userId: 1000 }));
await redis.expire('user:1000:name', 300); // 5 minutes
await redis.ttl('user:1000:name'); // Returns remaining seconds

// Atomic operations
await redis.incr('page:views'); // 1
await redis.incr('page:views'); // 2
await redis.incrby('score', 10); // Increment by 10
await redis.decr('inventory:item123');

// Hashes (objects)
await redis.hset('user:1000', {
  name: 'Alice',
  email: 'alice@example.com',
  age: 30,
});

await redis.hget('user:1000', 'name'); // 'Alice'
await redis.hgetall('user:1000'); // { name: 'Alice', email: '...', age: '30' }
await redis.hincrby('user:1000', 'loginCount', 1);

// Lists (queues, stacks)
await redis.lpush('queue:jobs', 'job1', 'job2', 'job3'); // Push to left
await redis.rpush('queue:jobs', 'job4'); // Push to right
await redis.lpop('queue:jobs'); // Pop from left (FIFO)
await redis.rpop('queue:jobs'); // Pop from right (LIFO)
await redis.lrange('queue:jobs', 0, -1); // Get all items

// Sets (unique values)
await redis.sadd('tags:post:1', 'javascript', 'nodejs', 'redis');
await redis.smembers('tags:post:1'); // ['javascript', 'nodejs', 'redis']
await redis.sismember('tags:post:1', 'nodejs'); // 1 (true)
await redis.scard('tags:post:1'); // 3 (count)

// Set operations
await redis.sadd('tags:post:2', 'nodejs', 'typescript', 'docker');
await redis.sinter('tags:post:1', 'tags:post:2'); // ['nodejs'] (intersection)
await redis.sunion('tags:post:1', 'tags:post:2'); // All unique tags
await redis.sdiff('tags:post:1', 'tags:post:2'); // ['javascript', 'redis']

// Sorted Sets (leaderboards)
await redis.zadd('leaderboard', 1000, 'player1', 1500, 'player2', 800, 'player3');
await redis.zrange('leaderboard', 0, -1, 'WITHSCORES'); // Ascending
await redis.zrevrange('leaderboard', 0, 9); // Top 10 (descending)
await redis.zincrby('leaderboard', 50, 'player1'); // Add to score
await redis.zrank('leaderboard', 'player1'); // Get rank (0-indexed)
await redis.zscore('leaderboard', 'player1'); // Get score
```

### Advanced Patterns

#### Caching with JSON
```typescript
// Cache helper
class CacheService {
  constructor(private redis: Redis) {}

  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async delete(key: string): Promise<void> {
    await this.redis.del(key);
  }

  async getOrSet<T>(
    key: string,
    factory: () => Promise<T>,
    ttl: number = 3600
  ): Promise<T> {
    const cached = await this.get<T>(key);
    if (cached) return cached;

    const fresh = await factory();
    await this.set(key, fresh, ttl);
    return fresh;
  }
}

// Usage
const cache = new CacheService(redis);

const user = await cache.getOrSet(
  'user:1000',
  async () => await db.user.findById(1000),
  3600
);
```

#### Rate Limiting
```typescript
class RateLimiter {
  constructor(private redis: Redis) {}

  async checkRateLimit(
    key: string,
    limit: number,
    window: number
  ): Promise<{ allowed: boolean; remaining: number }> {
    const current = await this.redis.incr(key);

    if (current === 1) {
      await this.redis.expire(key, window);
    }

    return {
      allowed: current <= limit,
      remaining: Math.max(0, limit - current),
    };
  }
}

// Usage: 100 requests per hour per IP
const limiter = new RateLimiter(redis);
const result = await limiter.checkRateLimit(`ratelimit:${ip}`, 100, 3600);

if (!result.allowed) {
  return res.status(429).json({ error: 'Too many requests' });
}
```

#### Sliding Window Rate Limiting
```typescript
async function slidingWindowRateLimit(
  redis: Redis,
  key: string,
  limit: number,
  window: number
): Promise<boolean> {
  const now = Date.now();
  const windowStart = now - window * 1000;

  // Remove old entries
  await redis.zremrangebyscore(key, 0, windowStart);

  // Count requests in window
  const count = await redis.zcard(key);

  if (count < limit) {
    // Add current request
    await redis.zadd(key, now, `${now}-${Math.random()}`);
    await redis.expire(key, window);
    return true;
  }

  return false;
}
```

#### Distributed Locking
```typescript
class RedisLock {
  constructor(private redis: Redis) {}

  async acquire(
    resource: string,
    ttl: number = 10000,
    retryDelay: number = 50,
    retryCount: number = 100
  ): Promise<string | null> {
    const lockKey = `lock:${resource}`;
    const lockValue = crypto.randomUUID();

    for (let i = 0; i < retryCount; i++) {
      const acquired = await this.redis.set(
        lockKey,
        lockValue,
        'PX',
        ttl,
        'NX'
      );

      if (acquired === 'OK') {
        return lockValue;
      }

      await new Promise((resolve) => setTimeout(resolve, retryDelay));
    }

    return null;
  }

  async release(resource: string, lockValue: string): Promise<boolean> {
    const lockKey = `lock:${resource}`;

    // Use Lua script to ensure atomicity
    const script = `
      if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
      else
        return 0
      end
    `;

    const result = await this.redis.eval(script, 1, lockKey, lockValue);
    return result === 1;
  }

  async withLock<T>(
    resource: string,
    fn: () => Promise<T>,
    ttl: number = 10000
  ): Promise<T> {
    const lockValue = await this.acquire(resource, ttl);
    if (!lockValue) {
      throw new Error('Failed to acquire lock');
    }

    try {
      return await fn();
    } finally {
      await this.release(resource, lockValue);
    }
  }
}

// Usage
const lock = new RedisLock(redis);

await lock.withLock('resource:123', async () => {
  // Critical section - only one process can execute this
  const data = await fetchData();
  await processData(data);
});
```

### Pub/Sub

```typescript
// Publisher
const publisher = new Redis();

await publisher.publish('notifications', JSON.stringify({
  type: 'new_message',
  userId: 1000,
  message: 'Hello!',
}));

// Subscriber
const subscriber = new Redis();

subscriber.subscribe('notifications', (err, count) => {
  console.log(`Subscribed to ${count} channels`);
});

subscriber.on('message', (channel, message) => {
  const data = JSON.parse(message);
  console.log(`Received from ${channel}:`, data);
});

// Pattern subscription
subscriber.psubscribe('user:*:notifications', (err, count) => {
  console.log(`Subscribed to ${count} patterns`);
});

subscriber.on('pmessage', (pattern, channel, message) => {
  console.log(`Pattern ${pattern} matched ${channel}:`, message);
});

// Unsubscribe
await subscriber.unsubscribe('notifications');
await subscriber.punsubscribe('user:*:notifications');
```

### Redis Streams

```typescript
// Add to stream
await redis.xadd(
  'events',
  '*', // Auto-generate ID
  'type', 'user_registered',
  'userId', '1000',
  'email', 'alice@example.com'
);

// Read from stream
const messages = await redis.xread('COUNT', 10, 'STREAMS', 'events', '0');
/*
[
  ['events', [
    ['1609459200000-0', ['type', 'user_registered', 'userId', '1000']],
    ['1609459201000-0', ['type', 'order_placed', 'orderId', '500']]
  ]]
]
*/

// Consumer Groups
await redis.xgroup('CREATE', 'events', 'worker-group', '0', 'MKSTREAM');

// Read as consumer
const messages = await redis.xreadgroup(
  'GROUP', 'worker-group', 'consumer-1',
  'COUNT', 10,
  'STREAMS', 'events', '>'
);

// Acknowledge message
await redis.xack('events', 'worker-group', '1609459200000-0');

// Pending messages
const pending = await redis.xpending('events', 'worker-group');
```

### Transactions

```typescript
// Multi/Exec (transaction)
const pipeline = redis.multi();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.incr('counter');
const results = await pipeline.exec();

// Watch (optimistic locking)
await redis.watch('balance:1000');
const balance = parseInt(await redis.get('balance:1000') || '0');

if (balance >= amount) {
  const multi = redis.multi();
  multi.decrby('balance:1000', amount);
  multi.incrby('balance:2000', amount);
  await multi.exec(); // Executes only if balance:1000 wasn't modified
} else {
  await redis.unwatch();
}
```

### Pipelining

```typescript
// Pipeline multiple commands
const pipeline = redis.pipeline();
pipeline.set('key1', 'value1');
pipeline.set('key2', 'value2');
pipeline.get('key1');
pipeline.get('key2');
const results = await pipeline.exec();
// [[null, 'OK'], [null, 'OK'], [null, 'value1'], [null, 'value2']]

// Batch operations
async function batchSet(items: Record<string, string>) {
  const pipeline = redis.pipeline();
  for (const [key, value] of Object.entries(items)) {
    pipeline.set(key, value);
  }
  await pipeline.exec();
}
```

### Lua Scripts

```typescript
// Atomic increment with max
const script = `
  local current = redis.call('GET', KEYS[1])
  local max = tonumber(ARGV[1])

  if current and tonumber(current) >= max then
    return tonumber(current)
  else
    return redis.call('INCR', KEYS[1])
  end
`;

const result = await redis.eval(script, 1, 'counter', 100);

// Load script once, execute many times
const sha = await redis.script('LOAD', script);
const result = await redis.evalsha(sha, 1, 'counter', 100);
```

## Redis Cluster

### Setup
```bash
# Create 6 nodes (3 masters, 3 replicas)
for port in {7000..7005}; do
  mkdir -p cluster/${port}
  cat > cluster/${port}/redis.conf <<EOF
port ${port}
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
EOF
  redis-server cluster/${port}/redis.conf &
done

# Create cluster
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

### Cluster Client
```typescript
import Redis from 'ioredis';

const cluster = new Redis.Cluster([
  { host: '127.0.0.1', port: 7000 },
  { host: '127.0.0.1', port: 7001 },
  { host: '127.0.0.1', port: 7002 },
]);

// Operations work transparently
await cluster.set('key', 'value');
await cluster.get('key');
```

## Best Practices

### Memory Management
- Set maxmemory limit
- Choose appropriate eviction policy:
  - `allkeys-lru`: Remove least recently used keys
  - `allkeys-lfu`: Remove least frequently used keys
  - `volatile-lru`: Remove LRU keys with expire set
  - `volatile-ttl`: Remove keys with shortest TTL
- Monitor memory usage: `INFO memory`
- Use memory-efficient data structures

### Key Naming
```typescript
// Good: hierarchical, descriptive
'user:1000:profile'
'session:abc123'
'cache:api:users:page:1'
'ratelimit:ip:192.168.1.1:2024-01-19'

// Use consistent separators
const key = ['user', userId, 'profile'].join(':');
```

### Expiration
- Always set TTL for cache keys
- Use appropriate TTL based on data freshness
- Monitor keys without expiration: `redis-cli --bigkeys`

### Persistence
- Use AOF for durability (appendonly yes)
- Use RDB for backups (save snapshots)
- Test restore procedures

### Monitoring
```bash
# Monitor commands in real-time
redis-cli MONITOR

# Stats
redis-cli INFO

# Slow queries
redis-cli SLOWLOG GET 10

# Memory analysis
redis-cli --bigkeys

# Latency
redis-cli --latency
```

## Performance Optimization

### Connection Pooling
```typescript
const redis = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: 3,
  enableReadyCheck: true,
  lazyConnect: true,
});
```

### Avoid KEYS Command
```typescript
// ❌ Bad: Blocks entire server
const keys = await redis.keys('user:*');

// ✅ Good: Use SCAN for large datasets
async function* scanKeys(pattern: string) {
  let cursor = '0';
  do {
    const [newCursor, keys] = await redis.scan(
      cursor,
      'MATCH',
      pattern,
      'COUNT',
      100
    );
    cursor = newCursor;
    yield* keys;
  } while (cursor !== '0');
}

for await (const key of scanKeys('user:*')) {
  console.log(key);
}
```

### Optimize Data Structures
```typescript
// Use hashes for objects instead of multiple keys
// ❌ Bad: 3 keys
await redis.set('user:1000:name', 'Alice');
await redis.set('user:1000:email', 'alice@example.com');
await redis.set('user:1000:age', '30');

// ✅ Good: 1 key
await redis.hset('user:1000', {
  name: 'Alice',
  email: 'alice@example.com',
  age: '30',
});
```

## Anti-Patterns to Avoid

❌ **Using Redis as primary database**: Use for caching/sessions
❌ **Not setting TTL on cache keys**: Causes memory bloat
❌ **Using KEYS in production**: Use SCAN instead
❌ **Large values in keys**: Keep values small (<1MB)
❌ **No monitoring**: Track memory, latency, hit rate
❌ **Synchronous blocking operations**: Use async operations
❌ **Not handling connection failures**: Implement retry logic
❌ **Storing large collections in single key**: Split into multiple keys

## Common Use Cases

### Session Store (Express)
```typescript
import session from 'express-session';
import RedisStore from 'connect-redis';

app.use(
  session({
    store: new RedisStore({ client: redis }),
    secret: 'secret',
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      maxAge: 1000 * 60 * 60 * 24, // 24 hours
    },
  })
);
```

### Job Queue (BullMQ)
```typescript
import { Queue, Worker } from 'bullmq';

const queue = new Queue('emails', { connection: redis });

// Add job
await queue.add('send-email', {
  to: 'user@example.com',
  subject: 'Welcome',
  body: 'Hello!',
});

// Process jobs
const worker = new Worker('emails', async (job) => {
  await sendEmail(job.data);
}, { connection: redis });
```

## Resources

- Redis Documentation: https://redis.io/docs/
- ioredis: https://github.com/redis/ioredis
- Redis University: https://university.redis.com/
- BullMQ: https://docs.bullmq.io/
