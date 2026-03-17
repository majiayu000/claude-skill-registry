---
name: caching
description: Enforces project caching conventions when implementing cache layers using React cache(), Next.js unstable_cache, Upstash Redis, and Cloudinary. This skill ensures consistent patterns for cache keys, tags, TTL configuration, cache invalidation, and domain-specific CacheService helpers.
---

# Caching Skill

## Purpose

This skill enforces the project caching conventions automatically during cache implementation. It ensures consistent patterns across the 4-layer caching strategy:

1. **React `cache()`** - Same-request deduplication (e.g., `getCurrentClerkUserId`, `getOptionalUserId`)
2. **Next.js `unstable_cache()`** - Cross-request caching with tag-based invalidation (primary)
3. **Upstash Redis** - High-traffic public data, distributed locks, rate limiting, view tracking
4. **Cloudinary** - Image transformation and CDN-level caching

## Activation

This skill activates when:

- Working with `CacheService` domain-specific helpers (`.bobbleheads`, `.collections`, `.users`, `.search`, `.redisSearch`, `.analytics`, `.featured`)
- Implementing cached data fetching in facades
- Setting up cache invalidation after mutations using `CacheRevalidationService`
- Working with Redis operations via `RedisOperations` class
- Using `REDIS_KEYS` for view tracking, locks, or rate limiting
- Configuring cache tags and TTL values
- Using `CACHE_KEYS`, `CACHE_CONFIG`, `REDIS_TTL`, or `CacheTagGenerators`
- Implementing request-level deduplication with React `cache()`

## Workflow

1. Detect caching work (imports from `CacheService`, `CacheRevalidationService`, `CACHE_KEYS`, or `CacheTagGenerators`)
2. Load `references/Caching-Conventions.md`
3. Generate/modify code following all conventions
4. Scan for violations of caching patterns
5. Auto-fix all violations (no permission needed)
6. Report fixes applied

## Key Patterns

### CacheService Domain Helpers

- Use `CacheService.bobbleheads.{method}()` for bobblehead caching
- Use `CacheService.collections.{method}()` for collection caching
- Use `CacheService.users.{method}()` for user caching
- Use `CacheService.search.{method}()` for search caching (Next.js unstable_cache)
- Use `CacheService.redisSearch.{method}()` for high-traffic public search (Redis)
- Use `CacheService.analytics.{method}()` for analytics caching
- Use `CacheService.featured.{method}()` for featured content caching

### Cache Invalidation

- Use `CacheRevalidationService.{domain}.on{Operation}()` for coordinated invalidation
- Use `CacheService.invalidateByTag()` for direct tag-based invalidation
- Always invalidate cache after mutations in server actions
- Check `RevalidationResult.isSuccess` and log failures to Sentry as warnings

### Constants and Utilities

- Use `CACHE_KEYS.{DOMAIN}.{METHOD}()` for cache key generation
- Use `CacheTagGenerators.{domain}.{method}()` for tag generation
- Use `CACHE_CONFIG.TTL.{LEVEL}` for TTL values:
  - `REALTIME` (30s), `SHORT` (5 min), `MEDIUM` (30 min), `LONG` (1 hr)
  - `EXTENDED` (4 hr), `PUBLIC_SEARCH` (10 min), `DAILY` (24 hr), `WEEKLY` (7 days)
- Use `REDIS_KEYS.{NAMESPACE}.{METHOD}()` for Redis-specific keys (VIEW_TRACKING, LOCKS, RATE_LIMIT)
- Use `REDIS_TTL.{CATEGORY}` for Redis-specific TTL values
- Use `createHashFromObject()` for generating option hashes in cache keys

## Usage Pattern Reference

| Use Case         | CacheService Helper                         | Invalidation Service                                |
| ---------------- | ------------------------------------------- | --------------------------------------------------- |
| Bobblehead by ID | `CacheService.bobbleheads.byId()`           | `CacheRevalidationService.bobbleheads.onUpdate()`   |
| Collection list  | `CacheService.collections.byUser()`         | `CacheRevalidationService.collections.onCreate()`   |
| User profile     | `CacheService.users.profile()`              | `CacheRevalidationService.users.onProfileUpdate()`  |
| Public search    | `CacheService.redisSearch.publicDropdown()` | `CacheService.search.invalidatePublic()`            |
| Analytics        | `CacheService.analytics.viewCounts()`       | `CacheRevalidationService.analytics.onViewRecord()` |
| Social (likes)   | Tag-based via `CacheTagGenerators`          | `CacheRevalidationService.social.onLikeChange()`    |
| View tracking    | `REDIS_KEYS.VIEW_TRACKING.*` + Redis ops    | TTL-based expiry (no explicit invalidation)         |

## Caching Layer Selection Guide

| Use Case                               | Recommended Layer | Rationale                                                            |
| -------------------------------------- | ----------------- | -------------------------------------------------------------------- |
| Same-request deduplication             | React `cache()`   | Prevents redundant calls within single render (implemented for auth) |
| Entity data (bobbleheads, collections) | `unstable_cache`  | Tag-based invalidation, automatic revalidation                       |
| High-traffic public search             | Redis             | Distributed, fast, handles scale                                     |
| View tracking deduplication            | Redis             | Distributed, TTL-based expiry                                        |
| Rate limiting                          | Redis             | Distributed counters, automatic TTL expiry                           |
| Distributed locks                      | Redis             | Prevents concurrent updates                                          |
| Image transformations                  | Cloudinary        | CDN-level caching, on-the-fly transforms                             |

## References

- `references/Caching-Conventions.md` - Complete caching conventions
