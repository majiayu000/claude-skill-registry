---
name: intelligent-cache
description: Multi-layer caching with type-specific TTLs, get-or-generate pattern, memory and database layers, and graceful invalidation without cache stampede.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: performance
  time: 5h
  source: drift-masterguide
---

# Intelligent Caching

Multi-layer caching with type-specific TTLs and get-or-generate pattern.

## When to Use This Skill

- Different content types need different freshness
- Expensive generation (AI, aggregations)
- Need persistence across restarts
- Want to track generation time for optimization

## Core Concepts

Production caching needs:
1. **Type-specific TTLs** - Different content, different freshness
2. **Two-layer cache** - Memory for speed, DB for persistence
3. **Get-or-generate** - Single function handles everything
4. **Generation timing** - Track for optimization

## Implementation

### TypeScript

```typescript
// Cache durations by content type
const CACHE_DURATIONS: Record<string, number> = {
  daily_briefing: 4 * 60 * 60 * 1000,    // 4 hours
  weekly_summary: 24 * 60 * 60 * 1000,   // 24 hours
  country_analysis: 2 * 60 * 60 * 1000,  // 2 hours
  alert_digest: 30 * 60 * 1000,          // 30 minutes
  pattern_report: 6 * 60 * 60 * 1000,    // 6 hours
};

type CacheType = keyof typeof CACHE_DURATIONS;

interface CachedItem<T = unknown> {
  id: string;
  cacheType: CacheType;
  cacheKey: string;
  contentMarkdown: string;
  contentStructured: T;
  generatedAt: string;
  expiresAt: string;
  generationTimeMs?: number;
}

// In-memory cache layer
const memoryCache = new Map<string, CachedItem>();

function getCacheKey(type: CacheType, key: string): string {
  return `${type}:${key}`;
}

/**
 * Cache content with type-specific TTL
 */
async function cacheContent<T>(
  type: CacheType,
  key: string,
  markdown: string,
  structured: T,
  generationTimeMs?: number
): Promise<void> {
  const cacheKey = getCacheKey(type, key);
  const now = new Date();
  const expiresAt = new Date(now.getTime() + CACHE_DURATIONS[type]);
  
  const cache: CachedItem<T> = {
    id: crypto.randomUUID(),
    cacheType: type,
    cacheKey: key,
    contentMarkdown: markdown,
    contentStructured: structured,
    generatedAt: now.toISOString(),
    expiresAt: expiresAt.toISOString(),
    generationTimeMs,
  };
  
  // Layer 1: Memory cache
  memoryCache.set(cacheKey, cache as CachedItem);
  
  // Layer 2: Database cache (if enabled)
  if (isPersistenceEnabled()) {
    await db.cache.upsert({
      where: { cacheType_cacheKey: { cacheType: type, cacheKey: key } },
      create: cache,
      update: cache,
    });
  }
}

/**
 * Get cached content with memory -> DB fallback
 */
async function getCached<T>(type: CacheType, key: string): Promise<CachedItem<T> | null> {
  const cacheKey = getCacheKey(type, key);
  const now = new Date();
  
  // Layer 1: Check memory cache
  const memoryCached = memoryCache.get(cacheKey);
  if (memoryCached) {
    if (new Date(memoryCached.expiresAt) > now) {
      return memoryCached as CachedItem<T>;
    }
    memoryCache.delete(cacheKey);
  }
  
  // Layer 2: Check database
  if (!isPersistenceEnabled()) return null;
  
  const dbCached = await db.cache.findFirst({
    where: {
      cacheType: type,
      cacheKey: key,
      expiresAt: { gt: now },
    },
  });
  
  if (dbCached) {
    // Promote to memory cache
    memoryCache.set(cacheKey, dbCached as CachedItem);
    return dbCached as CachedItem<T>;
  }
  
  return null;
}

/**
 * Get from cache or generate and cache
 */
async function getOrGenerate<T extends Record<string, unknown>>(
  type: CacheType,
  key: string,
  generator: () => Promise<{ markdown: string; structured: T }>
): Promise<{
  markdown: string;
  structured: T;
  fromCache: boolean;
  generationTimeMs?: number;
}> {
  // Try cache first
  const cached = await getCached<T>(type, key);
  if (cached) {
    return {
      markdown: cached.contentMarkdown,
      structured: cached.contentStructured,
      fromCache: true,
      generationTimeMs: cached.generationTimeMs,
    };
  }
  
  // Generate with timing
  const startTime = Date.now();
  const { markdown, structured } = await generator();
  const generationTimeMs = Date.now() - startTime;
  
  // Cache the result
  await cacheContent(type, key, markdown, structured, generationTimeMs);
  
  return {
    markdown,
    structured,
    fromCache: false,
    generationTimeMs,
  };
}

/**
 * Invalidate specific cache entry
 */
async function invalidateCache(type: CacheType, key: string): Promise<void> {
  const cacheKey = getCacheKey(type, key);
  memoryCache.delete(cacheKey);
  
  if (isPersistenceEnabled()) {
    await db.cache.deleteMany({
      where: { cacheType: type, cacheKey: key },
    });
  }
}

/**
 * Invalidate all entries of a type
 */
async function invalidateCacheType(type: CacheType): Promise<void> {
  for (const key of memoryCache.keys()) {
    if (key.startsWith(`${type}:`)) {
      memoryCache.delete(key);
    }
  }
  
  if (isPersistenceEnabled()) {
    await db.cache.deleteMany({ where: { cacheType: type } });
  }
}

/**
 * Clear expired entries
 */
async function clearExpiredCache(): Promise<number> {
  const now = new Date();
  let cleared = 0;
  
  for (const [key, cache] of memoryCache) {
    if (new Date(cache.expiresAt) <= now) {
      memoryCache.delete(key);
      cleared++;
    }
  }
  
  if (isPersistenceEnabled()) {
    const result = await db.cache.deleteMany({
      where: { expiresAt: { lte: now } },
    });
    cleared = Math.max(cleared, result.count);
  }
  
  return cleared;
}
```

### Python

```python
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional, TypeVar, Generic, Callable, Awaitable
import uuid

T = TypeVar('T')

CACHE_DURATIONS: Dict[str, timedelta] = {
    "daily_briefing": timedelta(hours=4),
    "weekly_summary": timedelta(hours=24),
    "country_analysis": timedelta(hours=2),
    "alert_digest": timedelta(minutes=30),
    "pattern_report": timedelta(hours=6),
}


@dataclass
class CachedItem(Generic[T]):
    id: str
    cache_type: str
    cache_key: str
    content_markdown: str
    content_structured: T
    generated_at: datetime
    expires_at: datetime
    generation_time_ms: Optional[int] = None


class IntelligentCache:
    def __init__(self, db=None):
        self._memory: Dict[str, CachedItem] = {}
        self._db = db
    
    def _get_cache_key(self, cache_type: str, key: str) -> str:
        return f"{cache_type}:{key}"
    
    async def cache_content(
        self,
        cache_type: str,
        key: str,
        markdown: str,
        structured: T,
        generation_time_ms: Optional[int] = None,
    ) -> None:
        cache_key = self._get_cache_key(cache_type, key)
        now = datetime.now(timezone.utc)
        expires_at = now + CACHE_DURATIONS.get(cache_type, timedelta(hours=1))
        
        item = CachedItem(
            id=str(uuid.uuid4()),
            cache_type=cache_type,
            cache_key=key,
            content_markdown=markdown,
            content_structured=structured,
            generated_at=now,
            expires_at=expires_at,
            generation_time_ms=generation_time_ms,
        )
        
        self._memory[cache_key] = item
        
        if self._db:
            await self._db.cache.upsert(item)
    
    async def get_cached(self, cache_type: str, key: str) -> Optional[CachedItem]:
        cache_key = self._get_cache_key(cache_type, key)
        now = datetime.now(timezone.utc)
        
        # Check memory
        if cache_key in self._memory:
            item = self._memory[cache_key]
            if item.expires_at > now:
                return item
            del self._memory[cache_key]
        
        # Check database
        if self._db:
            item = await self._db.cache.find_valid(cache_type, key, now)
            if item:
                self._memory[cache_key] = item
                return item
        
        return None
    
    async def get_or_generate(
        self,
        cache_type: str,
        key: str,
        generator: Callable[[], Awaitable[tuple[str, T]]],
    ) -> tuple[str, T, bool, Optional[int]]:
        cached = await self.get_cached(cache_type, key)
        if cached:
            return (
                cached.content_markdown,
                cached.content_structured,
                True,
                cached.generation_time_ms,
            )
        
        import time
        start = time.perf_counter()
        markdown, structured = await generator()
        generation_time_ms = int((time.perf_counter() - start) * 1000)
        
        await self.cache_content(cache_type, key, markdown, structured, generation_time_ms)
        
        return markdown, structured, False, generation_time_ms
    
    async def invalidate(self, cache_type: str, key: str) -> None:
        cache_key = self._get_cache_key(cache_type, key)
        self._memory.pop(cache_key, None)
        
        if self._db:
            await self._db.cache.delete(cache_type, key)
    
    async def clear_expired(self) -> int:
        now = datetime.now(timezone.utc)
        cleared = 0
        
        for key in list(self._memory.keys()):
            if self._memory[key].expires_at <= now:
                del self._memory[key]
                cleared += 1
        
        if self._db:
            db_cleared = await self._db.cache.delete_expired(now)
            cleared = max(cleared, db_cleared)
        
        return cleared
```

## Usage Examples

### API Route with Caching

```typescript
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const date = searchParams.get('date') || getTodayDate();
  
  const result = await getOrGenerate(
    'daily_briefing',
    date,
    async () => {
      // Expensive generation only on cache miss
      const events = await fetchTodayEvents();
      const analysis = await generateAIAnalysis(events);
      
      return {
        markdown: analysis.markdown,
        structured: {
          events: events.length,
          riskScore: analysis.riskScore,
        },
      };
    }
  );
  
  return Response.json({
    ...result.structured,
    markdown: result.markdown,
    cached: result.fromCache,
    generationMs: result.generationTimeMs,
  });
}
```

### Cache Statistics

```typescript
function getCacheStats(): { memoryEntries: number; byType: Record<string, number> } {
  const byType: Record<string, number> = {};
  
  for (const cache of memoryCache.values()) {
    byType[cache.cacheType] = (byType[cache.cacheType] || 0) + 1;
  }
  
  return { memoryEntries: memoryCache.size, byType };
}
```

## Best Practices

1. Set TTLs based on content freshness requirements
2. Use get-or-generate to prevent race conditions
3. Track generation time for optimization
4. Promote DB hits to memory for subsequent requests
5. Run periodic cleanup of expired entries

## Common Mistakes

- Single TTL for all content types
- Separate cache check and generation (race conditions)
- No expiry cleanup (memory leaks)
- Not tracking generation time
- Throwing errors when cache unavailable

## Related Patterns

- rate-limiting - Protect expensive generation
- circuit-breaker - Handle cache failures
- background-jobs - Async cache warming
