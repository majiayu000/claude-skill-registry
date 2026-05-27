---
name: Cache Invalidation Strategies
description: Patterns and strategies for cache invalidation - one of the two hardest problems in computer science.
---

# Cache Invalidation Strategies

## Overview

> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

Cache invalidation is the process of removing or updating cached data when the underlying data changes. Done incorrectly, it leads to stale data being served to users. Done correctly, it ensures data consistency while maintaining performance benefits.

## Why Cache Invalidation is Hard

Cache invalidation is challenging because:

1. **Multiple Cache Layers**: Data may be cached at multiple levels (browser, CDN, application cache, database cache)
2. **Complex Dependencies**: Cached data may depend on multiple data sources
3. **Timing Issues**: Changes may occur while cache is being updated
4. **Distributed Systems**: Multiple servers may have inconsistent cache states
5. **Performance Trade-offs**: Aggressive invalidation hurts performance, conservative invalidation risks stale data

## Cache Invalidation Patterns

### Time-Based Expiration (TTL)

The simplest approach - cache entries expire after a fixed time.

```javascript
// Set cache with TTL
await cache.set('user:123', userData, { ttl: 3600 });  // 1 hour

// Get from cache
const cached = await cache.get('user:123');
if (cached) {
  return cached;
}

// Cache miss - fetch from database
const data = await db.users.findById(123);
await cache.set('user:123', data, { ttl: 3600 });
return data;
```

**Pros:**
- Simple to implement
- No invalidation logic needed
- Works well for slowly changing data

**Cons:**
- May serve stale data until TTL expires
- Wastes cache space on unchanged data
- Hard to choose optimal TTL

**Choosing TTL:**

```javascript
// Adaptive TTL based on data change frequency
function calculateTTL(dataType, lastModified) {
  const age = Date.now() - lastModified;
  
  switch (dataType) {
    case 'user_profile':
      return 3600;  // 1 hour - changes rarely
    case 'stock_price':
      return 5;     // 5 seconds - changes frequently
    case 'news_feed':
      return 300;    // 5 minutes - moderate changes
    default:
      return 600;    // 10 minutes default
  }
}

// Usage
const userData = await db.users.findById(123);
const ttl = calculateTTL('user_profile', userData.updatedAt);
await cache.set(`user:${userData.id}`, userData, { ttl });
```

### Event-Driven Invalidation

Invalidate cache immediately when data changes.

```javascript
// Update user and invalidate cache
async function updateUser(userId, updates) {
  // Update database
  const user = await db.users.update(userId, updates);
  
  // Invalidate cache
  await cache.del(`user:${userId}`);
  
  return user;
}

// Delete user and invalidate cache
async function deleteUser(userId) {
  await db.users.delete(userId);
  await cache.del(`user:${userId}`);
}
```

**Event Bus Pattern:**

```javascript
const EventEmitter = require('events');

class CacheInvalidator extends EventEmitter {
  constructor() {
    super();
    this.setupListeners();
  }
  
  setupListeners() {
    // Listen for data change events
    this.on('user:updated', async ({ userId }) => {
      await cache.del(`user:${userId}`);
      await cache.del(`user:${userId}:profile`);
      await cache.del(`user:${userId}:settings`);
    });
    
    this.on('post:created', async ({ userId }) => {
      // Invalidate user's posts cache
      await cache.del(`user:${userId}:posts`);
      // Invalidate feed cache
      await cache.del('feed:recent');
    });
    
    this.on('post:deleted', async ({ userId, postId }) => {
      await cache.del(`user:${userId}:posts`);
      await cache.del(`post:${postId}`);
    });
  }
}

// Usage
const invalidator = new CacheInvalidator();

async function createPost(userId, content) {
  const post = await db.posts.create({ userId, content });
  
  // Emit event
  invalidator.emit('post:created', { userId, postId: post.id });
  
  return post;
}
```

### Write-Through Cache

Write data to cache and database simultaneously.

```javascript
async function updateUser(userId, updates) {
  const user = await db.users.update(userId, updates);
  
  // Write to cache
  await cache.set(`user:${userId}`, user, { ttl: 3600 });
  
  return user;
}

// Read always hits cache
async function getUser(userId) {
  const cached = await cache.get(`user:${userId}`);
  if (cached) {
    return cached;
  }
  
  const user = await db.users.findById(userId);
  await cache.set(`user:${userId}`, user, { ttl: 3600 });
  return user;
}
```

**Pros:**
- Cache is always up-to-date
- Simple read logic

**Cons:**
- Writes are slower (cache + database)
- May write data that's never read

### Write-Behind (Write-Back) Cache

Write to cache first, asynchronously persist to database.

```javascript
class WriteBehindCache {
  constructor() {
    this.writeQueue = [];
    this.processing = false;
    this.startProcessing();
  }
  
  async set(key, value, options) {
    // Write to cache immediately
    await cache.set(key, value, options);
    
    // Queue for database write
    this.writeQueue.push({ key, value, timestamp: Date.now() });
  }
  
  startProcessing() {
    setInterval(async () => {
      if (this.writeQueue.length === 0 || this.processing) return;
      
      this.processing = true;
      
      try {
        const batch = this.writeQueue.splice(0, 100);  // Process in batches
        await this.writeBatchToDatabase(batch);
      } catch (error) {
        console.error('Write-behind error:', error);
        // Re-queue failed writes
        this.writeQueue.unshift(...batch);
      } finally {
        this.processing = false;
      }
    }, 100);  // Process every 100ms
  }
  
  async writeBatchToDatabase(batch) {
    // Batch write to database
    const operations = batch.map(({ key, value }) => {
      const [type, id] = key.split(':');
      return db[type].update(id, value);
    });
    
    await Promise.all(operations);
  }
}
```

**Pros:**
- Fast writes (cache only)
- Can batch database writes

**Cons:**
- Risk of data loss if cache fails
- Complex to implement
- Eventual consistency

### Cache-Aside (Lazy Loading)

Check cache first, load from database on miss.

```javascript
async function getUser(userId) {
  // Check cache
  const cached = await cache.get(`user:${userId}`);
  if (cached) {
    return cached;
  }
  
  // Cache miss - load from database
  const user = await db.users.findById(userId);
  
  // Populate cache
  await cache.set(`user:${userId}`, user, { ttl: 3600 });
  
  return user;
}
```

**Cache Stampede Prevention:**

```javascript
async function getUserWithStampedeProtection(userId) {
  const cacheKey = `user:${userId}`;
  const lockKey = `lock:${cacheKey}`;
  
  // Check cache
  const cached = await cache.get(cacheKey);
  if (cached) {
    return cached;
  }
  
  // Try to acquire lock
  const lock = await cache.set(lockKey, '1', { 
    ttl: 10,  // Lock expires after 10s
    nx: true  // Only set if not exists
  });
  
  if (lock) {
    // We have the lock - load from database
    try {
      const user = await db.users.findById(userId);
      await cache.set(cacheKey, user, { ttl: 3600 });
      await cache.del(lockKey);
      return user;
    } catch (error) {
      await cache.del(lockKey);
      throw error;
    }
  } else {
    // Another request is loading - wait and retry
    await sleep(100);
    return getUserWithStampedeProtection(userId);
  }
}
```

### Read-Through Cache

Cache abstraction handles loading from database.

```javascript
class ReadThroughCache {
  constructor(loader) {
    this.loader = loader;
  }
  
  async get(key) {
    // Check cache
    const cached = await cache.get(key);
    if (cached) {
      return cached;
    }
    
    // Cache miss - use loader
    const value = await this.loader(key);
    
    // Populate cache
    await cache.set(key, value, { ttl: 3600 });
    
    return value;
  }
}

// Usage
const userCache = new ReadThroughCache(async (key) => {
  const userId = key.split(':')[1];
  return await db.users.findById(userId);
});

const user = await userCache.get('user:123');
```

## Invalidation Strategies

### Purge (Delete Specific Key)

Remove a specific cache entry.

```javascript
// Simple purge
await cache.del('user:123');

// Multiple keys
await cache.del('user:123', 'user:123:profile', 'user:123:settings');

// Pattern-based purge (Redis)
await cache.del('user:123:*');
```

**When to use:**
- Single data source changed
- Simple key structure
- Precise invalidation needed

### Ban (Pattern-Based Invalidation)

Remove all cache entries matching a pattern.

```javascript
// Redis pattern-based deletion
async function banPattern(pattern) {
  const keys = await cache.keys(pattern);
  if (keys.length > 0) {
    await cache.del(...keys);
  }
}

// Usage
await banPattern('user:123:*');  // Delete all user 123's cache
await banPattern('feed:*');       // Delete all feed caches
```

**Tag-Based Invalidation:**

```javascript
class TaggedCache {
  constructor() {
    this.keyTags = new Map();  // key -> Set of tags
    this.tagKeys = new Map();  // tag -> Set of keys
  }
  
  async set(key, value, options = {}) {
    const tags = options.tags || [];
    
    // Store value
    await cache.set(key, value, options);
    
    // Update tag mappings
    this.keyTags.set(key, new Set(tags));
    
    for (const tag of tags) {
      if (!this.tagKeys.has(tag)) {
        this.tagKeys.set(tag, new Set());
      }
      this.tagKeys.get(tag).add(key);
    }
  }
  
  async invalidateByTag(tag) {
    const keys = this.tagKeys.get(tag);
    if (!keys) return;
    
    // Delete all keys with this tag
    const keyArray = Array.from(keys);
    await cache.del(...keyArray);
    
    // Clean up mappings
    for (const key of keyArray) {
      const tags = this.keyTags.get(key);
      tags.delete(tag);
      if (tags.size === 0) {
        this.keyTags.delete(key);
      }
    }
    
    this.tagKeys.delete(tag);
  }
}

// Usage
const taggedCache = new TaggedCache();

// Cache with tags
await taggedCache.set('user:123', userData, {
  tags: ['user', 'profile', 'premium']
});

await taggedCache.set('user:456', userData, {
  tags: ['user', 'profile']
});

// Invalidate all user caches
await taggedCache.invalidateByTag('user');

// Invalidate only premium user caches
await taggedCache.invalidateByTag('premium');
```

### Refresh (Update in Place)

Update cache with fresh data without removing it.

```javascript
async function refreshUser(userId) {
  // Fetch fresh data
  const user = await db.users.findById(userId);
  
  // Update cache in place
  await cache.set(`user:${userId}`, user, { ttl: 3600 });
  
  return user;
}

// Background refresh
async function backgroundRefresh(key, loader) {
  try {
    const freshData = await loader(key);
    await cache.set(key, freshData, { ttl: 3600 });
  } catch (error) {
    console.error('Background refresh failed:', error);
  }
}

// Proactive refresh before expiration
async function getWithProactiveRefresh(key, loader) {
  const cached = await cache.get(key);
  
  if (cached) {
    const ttl = await cache.ttl(key);
    
    // Refresh if TTL is below threshold (e.g., 10% remaining)
    if (ttl < 360) {  // 3600 * 0.1
      backgroundRefresh(key, loader);
    }
    
    return cached;
  }
  
  // Cache miss
  const data = await loader(key);
  await cache.set(key, data, { ttl: 3600 });
  return data;
}
```

### Soft Purge (Serve Stale While Revalidating)

Mark cache as stale but continue serving it while refreshing.

```javascript
class SoftPurgeCache {
  async get(key) {
    const cached = await cache.get(key);
    
    if (!cached) {
      return null;
    }
    
    // Check if marked for soft purge
    if (cached._stale) {
      // Trigger background refresh
      this.backgroundRefresh(key);
      
      // Return stale data
      return cached._data;
    }
    
    return cached;
  }
  
  async softPurge(key) {
    const cached = await cache.get(key);
    
    if (cached) {
      // Mark as stale but keep data
      await cache.set(key, {
        _stale: true,
        _data: cached,
        _purgedAt: Date.now(),
      });
    }
  }
  
  async backgroundRefresh(key) {
    const cached = await cache.get(key);
    
    // Check if already refreshing
    if (cached && cached._refreshing) {
      return;
    }
    
    // Mark as refreshing
    await cache.set(key, {
      ...cached,
      _refreshing: true,
    });
    
    try {
      const freshData = await this.loader(key);
      await cache.set(key, freshData, { ttl: 3600 });
    } catch (error) {
      console.error('Refresh failed:', error);
      // Remove refreshing flag
      await cache.set(key, { ...cached, _refreshing: false });
    }
  }
}
```

## Cache Stampede Prevention

### Lock-Based Prevention

```javascript
async function getWithLock(key, loader, ttl = 3600) {
  const cached = await cache.get(key);
  if (cached) {
    return cached;
  }
  
  const lockKey = `lock:${key}`;
  const lockValue = Date.now().toString();
  
  // Try to acquire lock
  const acquired = await cache.set(lockKey, lockValue, {
    ttl: 10,  // Lock expires after 10s
    nx: true,
  });
  
  if (acquired) {
    // We have the lock
    try {
      const value = await loader(key);
      await cache.set(key, value, { ttl });
      await cache.del(lockKey);
      return value;
    } catch (error) {
      await cache.del(lockKey);
      throw error;
    }
  } else {
    // Wait for lock holder
    await sleep(50);
    
    // Check cache again
    const cached = await cache.get(key);
    if (cached) {
      return cached;
    }
    
    // Still no cache, try again
    return getWithLock(key, loader, ttl);
  }
}
```

### Request Coalescing

```javascript
class RequestCoalescer {
  constructor() {
    this.pendingRequests = new Map();
  }
  
  async get(key, loader) {
    // Check if request is already pending
    if (this.pendingRequests.has(key)) {
      return await this.pendingRequests.get(key);
    }
    
    // Create new promise
    const promise = this.loadAndCache(key, loader);
    this.pendingRequests.set(key, promise);
    
    try {
      return await promise;
    } finally {
      this.pendingRequests.delete(key);
    }
  }
  
  async loadAndCache(key, loader) {
    const cached = await cache.get(key);
    if (cached) {
      return cached;
    }
    
    const value = await loader(key);
    await cache.set(key, value, { ttl: 3600 });
    return value;
  }
}

// Usage
const coalescer = new RequestCoalescer();

async function getUser(userId) {
  return await coalescer.get(`user:${userId}`, async (key) => {
    const id = key.split(':')[1];
    return await db.users.findById(id);
  });
}
```

## Distributed Cache Invalidation

### Pub/Sub Pattern

```javascript
const Redis = require('ioredis');

class DistributedCacheInvalidator {
  constructor() {
    this.publisher = new Redis();
    this.subscriber = new Redis();
    this.setupSubscriber();
  }
  
  setupSubscriber() {
    this.subscriber.psubscribe('cache:*');
    
    this.subscriber.on('pmessage', (pattern, channel, message) => {
      const [action, key] = channel.split(':').slice(1);
      
      switch (action) {
        case 'invalidate':
          cache.del(key);
          break;
        case 'invalidate_pattern':
          this.invalidatePattern(message);
          break;
      }
    });
  }
  
  async invalidate(key) {
    // Invalidate local cache
    await cache.del(key);
    
    // Notify other instances
    await this.publisher.publish(`cache:invalidate:${key}`, '');
  }
  
  async invalidatePattern(pattern) {
    const keys = await cache.keys(pattern);
    if (keys.length > 0) {
      await cache.del(...keys);
    }
  }
  
  async invalidatePatternDistributed(pattern) {
    // Invalidate local cache
    await this.invalidatePattern(pattern);
    
    // Notify other instances
    await this.publisher.publish(`cache:invalidate_pattern:${pattern}`, '');
  }
}
```

### Database Change Data Capture (CDC)

```javascript
const { DebeziumConnector } = require('debezium-connector');

class CDCInvalidator {
  constructor() {
    this.connector = new DebeziumConnector({
      bootstrapServers: 'localhost:9092',
      topic: 'dbserver1.inventory.users',
    });
    
    this.setupListener();
  }
  
  setupListener() {
    this.connector.on('change', async (event) => {
      const { op, before, after } = event;
      
      switch (op) {
        case 'u':  // Update
        case 'd':  // Delete
          const userId = before.id;
          await cache.del(`user:${userId}`);
          await cache.del(`user:${userId}:profile`);
          break;
          
        case 'c':  // Create
          const newUserId = after.id;
          // Optionally pre-warm cache
          await cache.set(`user:${newUserId}`, after, { ttl: 3600 });
          break;
      }
    });
  }
}
```

## Cache Tags and Grouping

### Hierarchical Tags

```javascript
class HierarchicalCache {
  constructor() {
    this.tagHierarchy = new Map();  // tag -> parent tags
  }
  
  defineTag(tag, parentTags = []) {
    this.tagHierarchy.set(tag, parentTags);
  }
  
  async set(key, value, options = {}) {
    const tags = options.tags || [];
    
    // Resolve all parent tags
    const allTags = new Set(tags);
    for (const tag of tags) {
      const parents = this.tagHierarchy.get(tag) || [];
      parents.forEach(parent => allTags.add(parent));
    }
    
    // Store with all tags
    await cache.set(key, value, { ...options, tags: Array.from(allTags) });
  }
  
  async invalidateTag(tag) {
    // Get all keys with this tag or its children
    const keys = await this.getKeysByTag(tag);
    await cache.del(...keys);
  }
  
  async getKeysByTag(tag) {
    const keys = new Set();
    
    // Direct tag matches
    const directKeys = await this.tagKeys.get(tag) || [];
    directKeys.forEach(key => keys.add(key));
    
    // Child tag matches
    for (const [childTag, parentTags] of this.tagHierarchy) {
      if (parentTags.includes(tag)) {
        const childKeys = await this.tagKeys.get(childTag) || [];
        childKeys.forEach(key => keys.add(key));
      }
    }
    
    return Array.from(keys);
  }
}

// Usage
const cache = new HierarchicalCache();

// Define tag hierarchy
cache.defineTag('user', ['data']);
cache.defineTag('post', ['data']);
cache.defineTag('feed', ['data', 'aggregated']);

// Cache with tags
await cache.set('user:123', userData, { tags: ['user'] });
await cache.set('post:456', postData, { tags: ['post'] });
await cache.set('feed:recent', feedData, { tags: ['feed'] });

// Invalidate all data
await cache.invalidateTag('data');
```

## Versioned Cache Keys

Include version in cache key to simplify invalidation.

```javascript
class VersionedCache {
  constructor() {
    this.versions = new Map();  // prefix -> version number
  }
  
  async get(prefix, key) {
    const version = this.getVersion(prefix);
    const versionedKey = `${prefix}:v${version}:${key}`;
    return await cache.get(versionedKey);
  }
  
  async set(prefix, key, value, options) {
    const version = this.getVersion(prefix);
    const versionedKey = `${prefix}:v${version}:${key}`;
    return await cache.set(versionedKey, value, options);
  }
  
  getVersion(prefix) {
    if (!this.versions.has(prefix)) {
      this.versions.set(prefix, 1);
    }
    return this.versions.get(prefix);
  }
  
  async invalidate(prefix) {
    // Increment version
    const currentVersion = this.getVersion(prefix);
    this.versions.set(prefix, currentVersion + 1);
    
    // Old keys will naturally expire
    // Optionally, delete old keys immediately
    await this.deleteOldVersionKeys(prefix, currentVersion);
  }
  
  async deleteOldVersionKeys(prefix, oldVersion) {
    const pattern = `${prefix}:v${oldVersion}:*`;
    const keys = await cache.keys(pattern);
    if (keys.length > 0) {
      await cache.del(...keys);
    }
  }
}

// Usage
const cache = new VersionedCache();

// Set cache
await cache.set('user', '123', userData, { ttl: 3600 });
await cache.get('user', '123');  // user:v1:123

// Invalidate all user caches
await cache.invalidate('user');

// New version
await cache.set('user', '123', userData, { ttl: 3600 });
await cache.get('user', '123');  // user:v2:123
```

## Cache Warming Strategies

### On-Demand Warming

Warm cache when first accessed.

```javascript
async function getWithWarmup(key, loader) {
  const cached = await cache.get(key);
  
  if (cached) {
    return cached;
  }
  
  // Cache miss - load and warm
  const value = await loader(key);
  await cache.set(key, value, { ttl: 3600 });
  
  // Warm related caches
  await warmRelatedCaches(value);
  
  return value;
}

async function warmRelatedCaches(user) {
  // Warm user's posts
  const posts = await db.posts.findByUserId(user.id);
  await cache.set(`user:${user.id}:posts`, posts, { ttl: 3600 });
  
  // Warm user's friends
  const friends = await db.friends.findByUserId(user.id);
  await cache.set(`user:${user.id}:friends`, friends, { ttl: 3600 });
}
```

### Scheduled Warming

Warm cache on a schedule.

```javascript
class CacheWarmer {
  constructor() {
    this.jobs = new Map();
  }
  
  schedule(key, loader, interval) {
    const job = setInterval(async () => {
      try {
        const value = await loader(key);
        await cache.set(key, value, { ttl: interval * 2 });
      } catch (error) {
        console.error('Cache warming failed:', error);
      }
    }, interval);
    
    this.jobs.set(key, job);
    
    // Initial warm
    loader(key).then(value => {
      cache.set(key, value, { ttl: interval * 2 });
    });
  }
  
  unschedule(key) {
    const job = this.jobs.get(key);
    if (job) {
      clearInterval(job);
      this.jobs.delete(key);
    }
  }
}

// Usage
const warmer = new CacheWarmer();

// Warm user cache every hour
warmer.schedule('user:123', async () => {
  return await db.users.findById(123);
}, 3600000);
```

### Predictive Warming

Warm cache based on access patterns.

```javascript
class PredictiveCacheWarmer {
  constructor() {
    this.accessPatterns = new Map();  // key -> access timestamps
    this.predictions = new Map();    // key -> next access prediction
  }
  
  recordAccess(key) {
    const now = Date.now();
    const timestamps = this.accessPatterns.get(key) || [];
    timestamps.push(now);
    
    // Keep only last 100 accesses
    if (timestamps.length > 100) {
      timestamps.shift();
    }
    
    this.accessPatterns.set(key, timestamps);
    this.updatePrediction(key);
  }
  
  updatePrediction(key) {
    const timestamps = this.accessPatterns.get(key);
    if (timestamps.length < 2) return;
    
    // Calculate average interval
    let totalInterval = 0;
    for (let i = 1; i < timestamps.length; i++) {
      totalInterval += timestamps[i] - timestamps[i - 1];
    }
    const avgInterval = totalInterval / (timestamps.length - 1);
    
    // Predict next access
    const lastAccess = timestamps[timestamps.length - 1];
    const predictedAccess = lastAccess + avgInterval;
    
    this.predictions.set(key, predictedAccess);
    
    // Schedule warmup before predicted access
    const warmupTime = predictedAccess - avgInterval * 0.1;  // 10% early
    const delay = warmupTime - Date.now();
    
    if (delay > 0 && delay < 3600000) {  // Within next hour
      setTimeout(async () => {
        await this.warmKey(key);
      }, delay);
    }
  }
  
  async warmKey(key) {
    const value = await this.loader(key);
    await cache.set(key, value, { ttl: 3600 });
  }
}
```

## Multi-Tier Caching (L1/L2)

### Two-Level Cache

```javascript
class TwoLevelCache {
  constructor(l1, l2) {
    this.l1 = l1;  // Fast, small cache (e.g., in-memory)
    this.l2 = l2;  // Slower, larger cache (e.g., Redis)
  }
  
  async get(key) {
    // Check L1 first
    const l1Value = await this.l1.get(key);
    if (l1Value) {
      return l1Value;
    }
    
    // Check L2
    const l2Value = await this.l2.get(key);
    if (l2Value) {
      // Promote to L1
      await this.l1.set(key, l2Value, { ttl: 300 });  // 5 minutes
      return l2Value;
    }
    
    return null;
  }
  
  async set(key, value, options = {}) {
    // Set in both levels
    await this.l1.set(key, value, { ttl: 300, ...options });
    await this.l2.set(key, value, options);
  }
  
  async invalidate(key) {
    await this.l1.del(key);
    await this.l2.del(key);
  }
}

// Usage
const l1 = new InMemoryCache({ maxSize: 1000 });
const l2 = new RedisCache();
const cache = new TwoLevelCache(l1, l2);
```

### Write-Through Multi-Tier

```javascript
class WriteThroughMultiTierCache {
  constructor(tiers) {
    this.tiers = tiers;  // [L1, L2, L3, ...]
  }
  
  async get(key) {
    for (const tier of this.tiers) {
      const value = await tier.get(key);
      if (value) {
        // Promote to higher tiers
        this.promote(key, value);
        return value;
      }
    }
    return null;
  }
  
  async set(key, value, options) {
    // Write to all tiers
    const promises = this.tiers.map(tier => 
      tier.set(key, value, options)
    );
    await Promise.all(promises);
  }
  
  async invalidate(key) {
    const promises = this.tiers.map(tier => tier.del(key));
    await Promise.all(promises);
  }
  
  async promote(key, value) {
    // Write to higher tiers only
    for (let i = 0; i < this.tiers.length - 1; i++) {
      await this.tiers[i].set(key, value, { ttl: 300 });
    }
  }
}
```

## CDN Cache Invalidation

### CDN Purge

```javascript
const CloudFront = require('aws-sdk/clients/cloudfront');

const cloudfront = new CloudFront({
  region: 'us-east-1',
});

async function invalidateCDN(paths) {
  const params = {
    DistributionId: process.env.CLOUDFRONT_DISTRIBUTION_ID,
    InvalidationBatch: {
      CallerReference: Date.now().toString(),
      Paths: {
        Quantity: paths.length,
        Items: paths,
      },
    },
  };

  const result = await cloudfront.createInvalidation(params).promise();
  return result.Invalidation;
}

// Usage
await invalidateCDN(['/user/123', '/user/123/profile']);
```

### CDN Cache Tags

```javascript
// Set cache headers
app.get('/user/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  
  res.set('Cache-Control', 'public, max-age=3600');
  res.set('Cache-Tag', `user-${user.id},premium-${user.isPremium}`);
  
  res.json(user);
});

// Invalidate by tag
async function invalidateByTag(tag) {
  await cloudfront.createInvalidation({
    DistributionId: process.env.CLOUDFRONT_DISTRIBUTION_ID,
    InvalidationBatch: {
      CallerReference: Date.now().toString(),
      Paths: {
        Quantity: 1,
        Items: [`*`],  // Invalidate all, filter by tag
      },
    },
  }).promise();
}
```

## Database Query Cache Invalidation

### Query-Based Invalidation

```javascript
class QueryCache {
  constructor() {
    this.queryDependencies = new Map();  // query -> affected tables
  }
  
  async query(sql, params, loader) {
    const cacheKey = this.getQueryKey(sql, params);
    
    const cached = await cache.get(cacheKey);
    if (cached) {
      return cached;
    }
    
    const result = await loader(sql, params);
    await cache.set(cacheKey, result, { ttl: 3600 });
    
    // Track dependencies
    this.trackDependencies(cacheKey, sql);
    
    return result;
  }
  
  trackDependencies(cacheKey, sql) {
    const tables = this.extractTables(sql);
    this.queryDependencies.set(cacheKey, tables);
  }
  
  extractTables(sql) {
    // Simple table extraction
    const matches = sql.match(/FROM\s+(\w+)/gi) || [];
    return matches.map(m => m.replace(/FROM\s+/i, '').toLowerCase());
  }
  
  async invalidateTable(table) {
    for (const [cacheKey, tables] of this.queryDependencies) {
      if (tables.includes(table)) {
        await cache.del(cacheKey);
      }
    }
  }
}

// Usage
const queryCache = new QueryCache();

async function getUsers() {
  return await queryCache.query(
    'SELECT * FROM users WHERE active = true',
    [],
    (sql, params) => db.query(sql, params)
  );
}

// Invalidate when users table changes
await queryCache.invalidateTable('users');
```

## Eventual Consistency Handling

### Version Vectors

```javascript
class VersionVectorCache {
  constructor() {
    this.versions = new Map();  // key -> { replicaId: version }
  }
  
  async get(key) {
    const cached = await cache.get(key);
    if (!cached) {
      return null;
    }
    
    // Check if this replica's version is up-to-date
    const myVersion = this.getVersion(key, this.replicaId);
    const cachedVersion = cached._version[this.replicaId];
    
    if (myVersion > cachedVersion) {
      // Our version is newer - cache is stale
      return null;
    }
    
    return cached._data;
  }
  
  async set(key, value) {
    // Increment our version
    this.incrementVersion(key, this.replicaId);
    
    const version = this.getVersion(key, this.replicaId);
    
    await cache.set(key, {
      _data: value,
      _version: this.getFullVersion(key),
    });
  }
  
  getVersion(key, replicaId) {
    const versions = this.versions.get(key) || {};
    return versions[replicaId] || 0;
  }
  
  incrementVersion(key, replicaId) {
    const versions = this.versions.get(key) || {};
    versions[replicaId] = (versions[replicaId] || 0) + 1;
    this.versions.set(key, versions);
  }
}
```

## Monitoring Cache Hit/Miss Rates

### Metrics Collection

```javascript
class CacheMetrics {
  constructor() {
    this.hits = 0;
    this.misses = 0;
    this.errors = 0;
  }
  
  recordHit() {
    this.hits++;
  }
  
  recordMiss() {
    this.misses++;
  }
  
  recordError() {
    this.errors++;
  }
  
  getHitRate() {
    const total = this.hits + this.misses;
    return total > 0 ? this.hits / total : 0;
  }
  
  getStats() {
    return {
      hits: this.hits,
      misses: this.misses,
      errors: this.errors,
      hitRate: this.getHitRate(),
      total: this.hits + this.misses,
    };
  }
  
  reset() {
    this.hits = 0;
    this.misses = 0;
    this.errors = 0;
  }
}

// Usage
const metrics = new CacheMetrics();

async function get(key) {
  const cached = await cache.get(key);
  
  if (cached) {
    metrics.recordHit();
    return cached;
  }
  
  metrics.recordMiss();
  const value = await loader(key);
  await cache.set(key, value);
  return value;
}

// Report metrics periodically
setInterval(() => {
  console.log('Cache stats:', metrics.getStats());
  metrics.reset();
}, 60000);
```

## Common Anti-Patterns

### 1. Cache-Aside Without Locking

```javascript
// Bad: Multiple requests can load same data
async function getUser(userId) {
  const cached = await cache.get(`user:${userId}`);
  if (cached) return cached;
  
  const user = await db.users.findById(userId);  // Multiple requests hit DB
  await cache.set(`user:${userId}`, user);
  return user;
}

// Good: Use locking or coalescing
async function getUser(userId) {
  return await coalescer.get(`user:${userId}`, async (key) => {
    const id = key.split(':')[1];
    return await db.users.findById(id);
  });
}
```

### 2. Inconsistent Invalidation

```javascript
// Bad: Update cache but not database
async function updateUser(userId, updates) {
  await cache.set(`user:${userId}`, updates);  // Cache updated
  // Forgot to update database!
}

// Good: Update database first, then invalidate cache
async function updateUser(userId, updates) {
  const user = await db.users.update(userId, updates);
  await cache.del(`user:${userId}`);
  return user;
}
```

### 3. No TTL

```javascript
// Bad: No expiration, cache never clears
await cache.set('user:123', userData);

// Good: Always set TTL
await cache.set('user:123', userData, { ttl: 3600 });
```

### 4. Caching Everything

```javascript
// Bad: Cache everything, including rarely accessed data
async function getData(key) {
  const cached = await cache.get(key);
  if (cached) return cached;
  
  const value = await db.get(key);
  await cache.set(key, value);
  return value;
}

// Good: Cache selectively based on access patterns
async function getData(key) {
  if (!shouldCache(key)) {
    return await db.get(key);
  }
  
  const cached = await cache.get(key);
  if (cached) return cached;
  
  const value = await db.get(key);
  await cache.set(key, value, { ttl: 3600 });
  return value;
}
```

## Best Practices

1. **Choose the Right Strategy**
   - TTL for slowly changing data
   - Event-driven for critical data
   - Write-through for read-heavy workloads
   - Cache-aside for general use

2. **Prevent Cache Stampedes**
   - Use locking or request coalescing
   - Implement background refresh
   - Consider soft purge for high-traffic keys

3. **Handle Failures Gracefully**
   - Always have fallback to database
   - Log cache errors
   - Implement circuit breakers

4. **Monitor and Adjust**
   - Track hit/miss rates
   - Monitor cache size
   - Adjust TTLs based on patterns

5. **Think About Consistency**
   - Understand your consistency requirements
   - Use appropriate invalidation strategies
   - Handle distributed scenarios carefully

## Related Skills

- `04-database/redis-caching`
- `13-file-storage/cdn-setup`
- `47-performance-engineering/caching-strategies`
