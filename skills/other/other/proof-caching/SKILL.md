---
name: midnight-proofs:proof-caching
description: Use when caching ZK proofs for performance, implementing proof cache invalidation, storing verification results, caching intermediate proof components, or building distributed proof caches with Redis.
---

# Proof Caching

Cache proofs and proof components to improve performance and reduce redundant computation in proof generation services.

## When to Use

- Caching verification results to avoid re-verifying the same proofs
- Storing generated proofs for potential reuse
- Caching intermediate proof components
- Implementing TTL-based proof expiration
- Building distributed proof caches with Redis

## Key Concepts

### What Can Be Cached?

| Component | Cacheable? | TTL Considerations |
|-----------|------------|-------------------|
| **Verification results** | Yes | Long (proofs are immutable) |
| **Generated proofs** | Depends | Short (state may change) |
| **Circuit keys** | Yes | Until contract update |
| **Witness templates** | Sometimes | Depends on use case |

### Cache Key Design

A good proof cache key uniquely identifies the proof:

```typescript
// For verification results
function verificationCacheKey(
  circuitId: string,
  proofHash: string,
  publicInputsHash: string
): string {
  return `verify:${circuitId}:${proofHash}:${publicInputsHash}`;
}

// For generated proofs
function proofCacheKey(
  circuitId: string,
  witnessHash: string
): string {
  return `proof:${circuitId}:${witnessHash}`;
}
```

### Cache Invalidation

| Scenario | Invalidation Strategy |
|----------|----------------------|
| Contract upgrade | Clear all proofs for circuit |
| State change | Clear proofs depending on changed state |
| TTL expiration | Automatic removal |
| Manual purge | Admin-triggered clear |

## References

| Document | Description |
|----------|-------------|
| [cache-strategies.md](references/cache-strategies.md) | Caching strategies and TTL policies |

## Examples

| Example | Description |
|---------|-------------|
| [redis-cache/](examples/redis-cache/) | Distributed cache with Redis |
| [lru-cache/](examples/lru-cache/) | In-memory LRU cache |

## Quick Start

### 1. Simple In-Memory Cache

```typescript
import { LRUCache } from 'lru-cache';
import { createHash } from 'crypto';

const verificationCache = new LRUCache<string, boolean>({
  max: 10000,
  ttl: 1000 * 60 * 60, // 1 hour
});

function hashData(data: unknown): string {
  return createHash('sha256')
    .update(JSON.stringify(data))
    .digest('hex');
}

async function verifyWithCache(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>
): Promise<boolean> {
  const key = `${circuitId}:${hashData(proof)}:${hashData(publicInputs)}`;

  // Check cache
  const cached = verificationCache.get(key);
  if (cached !== undefined) {
    return cached;
  }

  // Verify
  const result = await verifier.verify(circuitId, proof, publicInputs);

  // Cache result
  verificationCache.set(key, result.valid);

  return result.valid;
}
```

### 2. Redis-Based Distributed Cache

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);

async function verifyWithRedisCache(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>
): Promise<boolean> {
  const key = `verify:${circuitId}:${hashData(proof)}:${hashData(publicInputs)}`;

  // Check cache
  const cached = await redis.get(key);
  if (cached !== null) {
    return cached === 'true';
  }

  // Verify
  const result = await verifier.verify(circuitId, proof, publicInputs);

  // Cache with 1 hour TTL
  await redis.setex(key, 3600, result.valid ? 'true' : 'false');

  return result.valid;
}
```

## Common Patterns

### Multi-Level Caching

```typescript
class MultiLevelProofCache {
  private l1: LRUCache<string, boolean>; // In-memory
  private l2: Redis;                      // Redis

  constructor(redis: Redis) {
    this.l1 = new LRUCache({ max: 1000, ttl: 60000 });
    this.l2 = redis;
  }

  async get(key: string): Promise<boolean | undefined> {
    // Check L1
    const l1Result = this.l1.get(key);
    if (l1Result !== undefined) {
      return l1Result;
    }

    // Check L2
    const l2Result = await this.l2.get(key);
    if (l2Result !== null) {
      const value = l2Result === 'true';
      this.l1.set(key, value); // Populate L1
      return value;
    }

    return undefined;
  }

  async set(key: string, value: boolean, ttlSeconds: number): Promise<void> {
    this.l1.set(key, value);
    await this.l2.setex(key, ttlSeconds, value ? 'true' : 'false');
  }
}
```

### Cache-Aside Pattern

```typescript
async function verifyProofCacheAside(
  circuitId: string,
  proof: Uint8Array,
  publicInputs: Record<string, unknown>
): Promise<boolean> {
  const key = buildCacheKey(circuitId, proof, publicInputs);

  // 1. Try cache
  const cached = await cache.get(key);
  if (cached !== undefined) {
    metrics.cacheHit();
    return cached;
  }

  metrics.cacheMiss();

  // 2. Compute
  const result = await verifier.verify(circuitId, proof, publicInputs);

  // 3. Store in cache
  await cache.set(key, result.valid, 3600);

  return result.valid;
}
```

### Batch Cache Lookup

```typescript
async function verifyBatchWithCache(
  proofs: ProofItem[]
): Promise<Map<string, boolean>> {
  const results = new Map<string, boolean>();
  const uncached: ProofItem[] = [];

  // Build keys
  const keys = proofs.map((p) => buildCacheKey(p.circuitId, p.proof, p.publicInputs));

  // Batch cache lookup
  const cachedValues = await redis.mget(keys);

  // Separate cached and uncached
  proofs.forEach((proof, i) => {
    if (cachedValues[i] !== null) {
      results.set(proof.id, cachedValues[i] === 'true');
    } else {
      uncached.push(proof);
    }
  });

  // Verify uncached
  if (uncached.length > 0) {
    const verifyResults = await verifyBatch(uncached);

    // Cache new results
    const pipeline = redis.pipeline();
    uncached.forEach((proof, i) => {
      const key = buildCacheKey(proof.circuitId, proof.proof, proof.publicInputs);
      pipeline.setex(key, 3600, verifyResults[i] ? 'true' : 'false');
      results.set(proof.id, verifyResults[i]);
    });
    await pipeline.exec();
  }

  return results;
}
```

### Cache Warming

```typescript
async function warmCache(circuitIds: string[]): Promise<void> {
  console.log('Warming cache for circuits:', circuitIds);

  for (const circuitId of circuitIds) {
    // Pre-generate common proofs
    const commonWitnesses = await getCommonWitnesses(circuitId);

    for (const witness of commonWitnesses) {
      try {
        const proof = await prover.prove(circuitId, witness);
        const key = buildProofCacheKey(circuitId, witness);
        await cache.set(key, proof, 3600);
      } catch (error) {
        console.warn(`Failed to warm cache for ${circuitId}:`, error);
      }
    }
  }

  console.log('Cache warming complete');
}
```

### Cache Metrics

```typescript
class CacheMetrics {
  private hits = 0;
  private misses = 0;
  private evictions = 0;

  hit(): void {
    this.hits++;
  }

  miss(): void {
    this.misses++;
  }

  evict(): void {
    this.evictions++;
  }

  getStats(): {
    hits: number;
    misses: number;
    hitRate: number;
    evictions: number;
  } {
    const total = this.hits + this.misses;
    return {
      hits: this.hits,
      misses: this.misses,
      hitRate: total > 0 ? this.hits / total : 0,
      evictions: this.evictions,
    };
  }
}
```

## Performance Considerations

| Concern | Mitigation |
|---------|------------|
| Cache stampede | Use locks or probabilistic early expiration |
| Memory pressure | Set appropriate max size, use LRU eviction |
| Stale data | Set appropriate TTL, implement invalidation |
| Network latency (Redis) | Use connection pooling, multi-level cache |

## Related Skills

- `proof-generation` - Generate proofs to cache
- `proof-verification` - Verify proofs with caching
- `prover-optimization` - Optimize proof generation

## Related Commands

None currently defined.
