---
name: tzurot-caching
description: Caching patterns for Tzurot v3. Use when implementing cache layers, TTL strategies, or debugging cache issues. Covers Redis patterns, cache-aside, and invalidation.
lastUpdated: '2026-01-21'
---

# Tzurot Caching & Horizontal Scaling Patterns

## Overview

This skill covers caching patterns for Tzurot v3, with a focus on horizontal scaling readiness. Use this skill when:

- Adding a new cache
- Evaluating if a cache needs cross-instance invalidation
- Debugging cache-related issues
- Planning for horizontal scaling

## Cache Decision Tree

When adding or modifying a cache, follow this decision tree:

```
Does staleness cause incorrect behavior?
├── YES → Redis + pub/sub invalidation
│         (e.g., channel activations - stale = missed messages)
│
└── NO → Is it expensive external API data?
         ├── YES → Must survive Redis restarts?
         │         ├── YES → Two-tier (L1 Redis + L2 PostgreSQL)
         │         │         (e.g., vision descriptions - expensive API, immutable)
         │         │
         │         └── NO → Redis with TTL
         │                  (e.g., OpenRouter model list - shared across instances)
         │
         └── NO → Is it read-heavy optimization?
                  ├── YES → In-memory TTL only
                  │         (e.g., autocomplete - 60s staleness acceptable)
                  │
                  └── NO → Is it rate limiting?
                           ├── YES → In-memory Map (local is correct)
                           │         (e.g., notification cooldowns)
                           │
                           └── NO → Probably don't need caching
```

## Cache Types & When to Use Each

### 1. Redis + Pub/Sub Invalidation

**Use when**: Staleness causes **correctness issues** (wrong behavior, not just stale UX).

**Pattern**: Redis pub/sub broadcasts invalidation events to all instances.

**Example**: Channel activation cache

```typescript
// Service definition (common-types)
export class ChannelActivationCacheInvalidationService extends BaseCacheInvalidationService<Event> {
  constructor(redis: Redis) {
    super(
      redis,
      REDIS_CHANNELS.CHANNEL_ACTIVATION_CACHE_INVALIDATION,
      'ChannelActivationCacheInvalidation',
      validator
    );
  }

  async invalidateChannel(channelId: string): Promise<void> {
    await this.publish({ type: 'channel', channelId });
  }
}

// Subscriber (bot-client startup)
await invalidationService.subscribe(event => {
  if (event.type === 'channel') {
    invalidateChannelActivationCache(event.channelId);
  }
});

// Publisher (after successful operation)
await invalidationService.invalidateChannel(channelId);
```

**Current implementations**:

- `CacheInvalidationService` - Personality cache
- `ChannelActivationCacheInvalidationService` - Channel activation cache

### 2. Redis with TTL (No Invalidation)

**Use when**: Data is expensive to fetch, shared across instances, and TTL-based staleness is acceptable.

**Pattern**: Store in Redis with TTL, optionally layer in-memory cache on top.

**Example**: OpenRouter model list

```typescript
// Redis as source of truth (24 hour TTL)
const cached = await redis.get('openrouter:models');
if (cached) return JSON.parse(cached);

const models = await fetchFromOpenRouter();
await redis.setex('openrouter:models', 86400, JSON.stringify(models));
return models;
```

**Current implementations**:

- `OpenRouterModelCache.ts` - Model list (24h Redis TTL + 5min memory TTL)
- `VisionDescriptionCache.ts` - Image descriptions (1h Redis TTL)
- `VoiceTranscriptCache.ts` - Voice transcripts (5min Redis TTL)
- `RedisDeduplicationCache.ts` - Request dedup (5sec Redis TTL)

### 3. Two-Tier Cache (L1 Redis + L2 PostgreSQL)

**Use when**: Data is expensive to compute, shared across instances, and must survive Redis restarts.

**Pattern**: L1 (Redis with TTL) → L2 (PostgreSQL persistent) → API fallback → write to both tiers.

**Example**: Vision description cache (image → text descriptions)

```
Lookup Flow:
1. Check L1 (Redis) → cache HIT → return
2. Check L2 (PostgreSQL) → cache HIT → populate L1 → return
3. Call vision API → store in both L1 and L2 → return
```

```typescript
// L1: VisionDescriptionCache (Redis, 1h TTL)
const l1Cache = new VisionDescriptionCache(redis);

// L2: PersistentVisionCache (PostgreSQL, no TTL)
const l2Cache = new PersistentVisionCache(prisma);

// Lookup pattern
async function getImageDescription(attachmentId: string): Promise<string> {
  // L1 check
  const l1Result = await l1Cache.get(attachmentId);
  if (l1Result) return l1Result;

  // L2 check
  const l2Result = await l2Cache.get(attachmentId);
  if (l2Result) {
    // Populate L1 from L2
    await l1Cache.set(attachmentId, l2Result.description, l2Result.model);
    return l2Result.description;
  }

  // API fallback
  const description = await callVisionAPI(imageUrl);

  // Write to both tiers
  await Promise.all([
    l1Cache.set(attachmentId, description, model),
    l2Cache.set({ attachmentId, description, model }),
  ]);

  return description;
}
```

**Key strategy**: Uses Discord attachment snowflake IDs (stable) instead of ephemeral CDN URLs (expire after ~24h). This ensures cache hits even when the URL changes.

**Current implementations**:

| Tier | Service                     | Storage    | TTL     | Purpose                     |
| ---- | --------------------------- | ---------- | ------- | --------------------------- |
| L1   | `VisionDescriptionCache.ts` | Redis      | 1 hour  | Fast lookup, network-shared |
| L2   | `PersistentVisionCache.ts`  | PostgreSQL | Forever | Survives Redis restarts     |

**When to use this pattern**:

- API calls are expensive ($$$) or rate-limited
- Data changes rarely or never (image descriptions are immutable)
- Redis may restart (Railway deployments)
- Historical data has long-tail access patterns

### 4. In-Memory TTL Cache

**Use when**: Read-heavy optimization where staleness is acceptable UX (not correctness) issue.

**Pattern**: Use `TTLCache` from common-types.

```typescript
import { TTLCache } from '@tzurot/common-types';

const cache = new TTLCache<ResponseType>({
  ttl: 60 * 1000, // 60 seconds
  maxSize: 500, // Max entries
});

// Use
const cached = cache.get(key);
if (cached) return cached;

const fresh = await fetchData();
cache.set(key, fresh);
return fresh;
```

**Current implementations**:

- `autocompleteCache.ts` - User autocomplete data (60s TTL, 500 users)
- `channelActivationCache` in GatewayClient - Now with pub/sub invalidation
- `ModelCapabilityChecker.ts` - Vision capability flags (5min TTL)
- `PersonalityService.ts` cache - Loaded personalities (5min TTL, pub/sub invalidation)

### 5. In-Memory Map (No TTL)

**Use when**: Rate limiting or cooldowns where local-per-instance is actually **correct**.

**Pattern**: Simple Map with periodic cleanup.

```typescript
const cooldowns = new Map<string, number>();

function isOnCooldown(key: string): boolean {
  const lastTime = cooldowns.get(key);
  if (!lastTime) return false;
  return Date.now() - lastTime < COOLDOWN_MS;
}

function setCooldown(key: string): void {
  cooldowns.set(key, Date.now());
}

// Cleanup old entries periodically (see tzurot-async-flow for timer concerns)
```

**Current implementations**:

- `notificationCache.ts` - User notification timestamps (1h cooldown)

## Horizontal Scaling Concerns

### What DOES Break with Multiple Instances

1. **In-memory caches without invalidation** - Each instance has different data
2. **Timer-based cleanup (`setInterval`)** - Each instance runs its own timers
3. **In-memory state** - Sessions, connection pools, etc.

### What DOESN'T Break

1. **Redis-backed caches** - Shared state across instances
2. **Request-scoped memory** - Data lives only during request
3. **Stateless services** - No instance-specific state

### Cache Audit Summary

| Cache                  | Location                     | TTL       | Scaling Risk | Status           |
| ---------------------- | ---------------------------- | --------- | ------------ | ---------------- |
| **Channel Activation** | `GatewayClient.ts`           | 30s       | ~~CRITICAL~~ | ✅ Pub/sub added |
| Autocomplete           | `autocompleteCache.ts`       | 60s       | Minor        | Acceptable       |
| Notification           | `notificationCache.ts`       | 1 hour    | Minor        | Local is correct |
| Global Config          | `preset/autocomplete.ts`     | 60s       | None         | Single entry     |
| Personality            | `PersonalityService.ts`      | 5 min     | None         | Has pub/sub      |
| Model Capability       | `ModelCapabilityChecker.ts`  | 5 min     | None         | Reads from Redis |
| OpenRouter Models      | `OpenRouterModelCache.ts`    | 24h Redis | None         | Redis is truth   |
| Vision Description     | `VisionDescriptionCache.ts`  | 1 hour    | None         | L1/L2 two-tier   |
| Voice Transcript       | `VoiceTranscriptCache.ts`    | 5 min     | None         | Redis-backed     |
| Request Dedup          | `RedisDeduplicationCache.ts` | 5 sec     | None         | Redis-backed     |

Full audit: `docs/architecture/CACHING_AUDIT.md`

## Creating a New Cache with Pub/Sub Invalidation

For cross-instance cache invalidation, follow the 6-step guide:

1. Add Redis channel in `common-types/constants/queue.ts`
2. Create invalidation service extending `BaseCacheInvalidationService`
3. Export from common-types index
4. Register in service registry (bot-client)
5. Subscribe on startup
6. Publish on changes

**📚 See**: `docs/reference/caching/PUBSUB_INVALIDATION_GUIDE.md` for complete implementation with code examples.

**Existing implementations** to reference:

- `CacheInvalidationService` - Personality cache
- `ChannelActivationCacheInvalidationService` - Channel activation cache

## TTLCache Usage

The `TTLCache` class from common-types is the standard for in-memory caching:

```typescript
import { TTLCache } from '@tzurot/common-types';

// Create cache
const cache = new TTLCache<ValueType>({
  ttl: 60 * 1000, // TTL in milliseconds
  maxSize: 100, // Maximum entries (LRU eviction)
});

// Operations
cache.set('key', value); // Add/update entry
const value = cache.get('key'); // Get entry (undefined if expired/missing)
cache.delete('key'); // Remove specific entry
cache.clear(); // Remove all entries
const has = cache.has('key'); // Check if exists (and not expired)
```

## Related Documentation

- `docs/architecture/CACHING_AUDIT.md` - Full cache inventory and analysis
- `tzurot-async-flow` skill - Timer patterns and BullMQ alternatives
- `tzurot-architecture` skill - Service boundaries and data flow
- `tzurot-db-vector` skill - Database caching considerations

## Related Skills

- **tzurot-async-flow** - Timer patterns, BullMQ for scheduled cleanup
- **tzurot-architecture** - Where caches belong in service boundaries
- **tzurot-shared-types** - Type definitions for cache events
- **tzurot-observability** - Logging cache operations
