---
name: spring-boot-cache
description: "Provides patterns for implementing Spring Boot caching: configures Redis/Caffeine/EhCache providers with TTL and eviction policies, applies @Cacheable/@CacheEvict/@CachePut annotations, validates cache hit/miss behavior, and exposes metrics via Actuator. Use when adding caching to Spring Boot services, configuring cache expiration, evicting stale data, or diagnosing cache misses."
allowed-tools: Read, Write, Bash
---

# Spring Boot Cache Abstraction

## Overview

6-step workflow for enabling cache abstraction, configuring providers (Caffeine,
Redis, Ehcache), annotating service methods, and validating behavior in
Spring Boot 3.5+ applications. Apply `@Cacheable` for reads, `@CachePut` for
writes, `@CacheEvict` for deletions. Configure TTL/eviction policies and expose
metrics via Actuator.

## When to Use

- Add `@Cacheable`, `@CachePut`, or `@CacheEvict` to service methods.
- Configure Caffeine, Redis, or Ehcache with TTL and capacity policies.
- Implement eviction strategies for stale data.
- Diagnose cache misses or invalidation issues.
- Expose hit/miss metrics via Actuator or Micrometer.

## Instructions

1. **Add dependencies** — `spring-boot-starter-cache` plus a provider:
   - Caffeine: `caffeine` starter
   - Redis: `spring-boot-starter-data-redis`
   - Ehcache: `ehcache` starter

2. **Enable caching** — annotate a `@Configuration` class with `@EnableCaching`
   and define a `CacheManager` bean.

3. **Annotate methods** — `@Cacheable` for reads, `@CachePut` for writes,
   `@CacheEvict` for deletions.

4. **Configure TTL/eviction** — set `spring.cache.caffeine.spec`,
   `spring.cache.redis.time-to-live`, or `spring.cache.ehcache.config`.

5. **Shape keys** — use SpEL in `key` attributes; guard with
   `condition`/`unless` for selective caching.

6. **Validate setup** — run integration test to confirm cache hit on second
   call; check `GET /actuator/caches` to verify cache manager registration;
   query `GET /actuator/metrics/cache.gets` for hit/miss ratios.

## Examples

### Example 1: Basic `@Cacheable` Usage

```java
@Service
@CacheConfig(cacheNames = "users")
class UserService {

    @Cacheable(key = "#id", unless = "#result == null")
    User findUser(Long id) { ... }
}
```

```
First call → cache miss, repository invoked
Second call → cache hit, repository skipped
```

### Example 2: Conditional Caching with SpEL

```java
@Cacheable(value = "products", key = "#id", condition = "#price > 100")
public Product getProduct(Long id, BigDecimal price) { ... }

// Only expensive products are cached
```

### Example 3: Cache Eviction

```java
@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) { ... }
```

For progressive scenarios (basic product cache, multilevel eviction, Redis
integration), load [`references/cache-examples.md`](references/cache-examples.md).

## Advanced Options

- Use JCache annotations (`@CacheResult`, `@CacheRemove`) for providers favoring
  JSR-107 interoperability; avoid mixing with Spring annotations on the same method.
- Cache reactive return types (`Mono`, `Flux`) or `CompletableFuture` values.
- Apply HTTP `CacheControl` headers when exposing cached responses via REST.
- Schedule periodic eviction with `@Scheduled` for time-bound caches.
- Create a `CacheManagementService` for programmatic `cacheManager.getCache(name)`.

## Troubleshooting

If cache misses persist after adding `@Cacheable`:

1. Verify `@EnableCaching` is present on a `@Configuration` class.
2. Confirm the method is public and called from outside the class (Spring uses
   proxies; self-invocation bypasses the cache).
3. Validate SpEL key expressions resolve correctly.
4. Confirm the cache manager bean is registered as `cacheManager` or explicitly
   referenced via `cacheManager = "myCacheManager"`.

## References

- [`references/spring-framework-cache-docs.md`](references/spring-framework-cache-docs.md):
  curated excerpts from Spring Framework Reference Guide.
- [`references/spring-cache-doc-snippet.md`](references/spring-cache-doc-snippet.md):
  narrative overview from Spring documentation.
- [`references/cache-core-reference.md`](references/cache-core-reference.md):
  annotation parameters, dependency matrices, property catalogs.
- [`references/cache-examples.md`](references/cache-examples.md):
  end-to-end examples with tests.

## Best Practices

- Prefer constructor injection and immutable DTOs for cache entries.
- Separate cache names per aggregate (`users`, `orders`) to simplify eviction.
- Log cache hits/misses only at debug; push metrics via Micrometer.
- Tune TTLs based on data staleness tolerance; document rationale in code.
- Guard caches storing PII or credentials with encryption or avoid caching.
- Align cache eviction with transactional boundaries to prevent dirty reads.

## Constraints and Warnings

- Avoid caching mutable entities that depend on open persistence contexts.
- Do not mix Spring cache annotations with JCache annotations on the same method.
- Validate serialization compatibility when caching across service instances.
- Monitor memory footprint to prevent OOM with in-memory stores.
- Caffeine + Redis multi-level caches require publish/subscribe invalidation channels.

## Related Skills

- [`../spring-boot-rest-api-standards`](../spring-boot-rest-api-standards/SKILL.md)
- [`../spring-boot-test-patterns`](../spring-boot-test-patterns/SKILL.md)
- [`../unit-test-caching`](../unit-test-caching/SKILL.md)
