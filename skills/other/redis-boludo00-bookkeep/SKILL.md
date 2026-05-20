---
name: redis
description: |
  Implements caching layer with Redis or memory fallback using aiocache.
  Use when: Adding cache operations, modifying TTLs, implementing cache invalidation patterns, or debugging cache behavior.
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# Redis Skill

Bookkeep uses `aiocache` with Redis 7.x for distributed caching, automatically falling back to in-memory cache when Redis is unavailable. The cache layer is defined in `backend/app/cache.py` and provides async get/set/delete operations with pattern-based invalidation.

## Quick Start

### Basic Cache Operations

```python
from app.cache import get_cached, set_cached, delete_cached, make_cache_key, CACHE_TTL

# Get with cache
cache_key = make_cache_key("book_details", book_id=123)
cached = await get_cached(cache_key)
if cached is not None:
    return cached

# Fetch and cache
result = await fetch_book(book_id)
await set_cached(cache_key, result, ttl=CACHE_TTL["book_details"])
return result
```

### Cache Invalidation on Mutation

```python
from app.cache import delete_cached, clear_cache_pattern, make_cache_key

# Single key invalidation
await delete_cached(make_cache_key("requests_by_hardcover", hardcover_id=book.hardcover_id))

# Pattern-based invalidation (clears all batch caches)
await clear_cache_pattern("requests_by_hardcover_batch:*")
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| `make_cache_key` | Create deterministic keys from prefix + sorted kwargs | `make_cache_key("search", query="foo", limit=10)` → `search:limit:10:query:foo` |
| `CACHE_TTL` | Dict of resource → seconds | `CACHE_TTL["trending"]` → `86400` (24h) |
| `CACHE_RESOURCES` | Admin UI resource groups with patterns | `{"books": {"patterns": ["book_details:*", "search:*"]}}` |
| Pattern clear | Glob-style deletion for invalidation | `clear_cache_pattern("series:*")` |

## Common Patterns

### Cache-Aside Pattern (Standard)

**When:** Every read operation that hits external API or expensive DB query

```python
cache_key = cache.make_cache_key("trending", limit=limit, date=current_date)
cached_result = await cache.get_cached(cache_key)
if cached_result is not None:
    return cached_result

# Expensive operation
result = await hardcover_api.fetch_trending(limit)

await cache.set_cached(cache_key, result, ttl=cache.CACHE_TTL["trending"])
return result
```

### Bypass Cache (Force Refresh)

**When:** User explicitly requests fresh data

```python
cache_key = cache.make_cache_key("book_details", book_id=book_id)
cached_result = None if bypass_cache else await cache.get_cached(cache_key)
```

## TTL Reference

| Resource | TTL | Rationale |
|----------|-----|-----------|
| `trending`, `popular`, `new_releases` | 24h | Updated via background job |
| `book_details`, `author` | 24h | Metadata rarely changes |
| `series` | 7 days | Very stable data |
| `search`, `search_grouped` | 30min | Query results can change |
| `requests_by_hardcover` | 5min | Status changes frequently |

## See Also

- [patterns](references/patterns.md)
- [workflows](references/workflows.md)

## Related Skills

- See the **fastapi** skill for router integration
- See the **python** skill for async patterns