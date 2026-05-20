---
name: spring-boot-cache
description: Provides patterns for enabling and operating the Spring Cache abstraction in Spring Boot. Use when implementing application-level caching for performance-sensitive workloads.
allowed-tools: Read, Write, Bash
---

# Spring Boot Cache Abstraction

## Overview

Spring Boot ships with a cache abstraction that wraps expensive service calls
behind annotation-driven caches. This abstraction supports multiple cache
providers (ConcurrentMap, Caffeine, Redis, Ehcache, JCache) without changing
business code. The skill provides a concise workflow for enabling caching,
managing cache lifecycles, and validating behavior in Spring Boot 3.5+ services.

## When to Use

- Add `@Cacheable`, `@CachePut`, or `@CacheEvict` to Spring Boot service methods.
- Configure Caffeine, Redis, or JCache cache managers for Spring Boot.
- Diagnose cache invalidation, eviction scheduling, or cache key issues.
- Expose cache management endpoints or scheduled eviction routines.

Use trigger phrases such as **"implement service caching"**, **"configure
CaffeineCacheManager"**, **"evict caches on update"**, or **"test Spring cache
behavior"** to load this skill.

## Instructions

Follow these steps to implement caching in Spring Boot applications:

### 1. Add Cache Dependencies

Include spring-boot-starter-cache and your preferred cache provider (Caffeine, Redis, Ehcache) in the project dependencies.

### 2. Enable Caching

Add @EnableCaching to a @Configuration class and declare CacheManager bean(s) for your cache providers.

### 3. Define Cache Configuration

Configure cache names, TTL settings, and capacity limits in application.yml or via CacheManager customizer beans.

### 4. Anotate Service Methods

Apply @Cacheable for read operations, @CachePut for updates, and @CacheEvict for invalidation. Use @CacheConfig to define default cache names at class level.

### 5. Configure Cache Keys and Conditions

Use SpEL expressions to define cache keys (key = "#user.id"), conditions (condition = "#price > 0"), and unless clauses (unless = "#result == null").

### 6. Implement Cache Eviction Strategy

Create scheduled jobs or use @CacheEvict with allEntries=true to periodically clear time-sensitive caches.

### 7. Monitor Cache Performance

Enable Actuator cache endpoint to observe hit/miss ratios. Consider Micrometer metrics for production observability.

## Prerequisites

- Java 17+ project based on Spring Boot 3.5.x (records encouraged for DTOs).
- Dependency `spring-boot-starter-cache`; add provider-specific starters as
  needed (`spring-boot-starter-data-redis`, `caffeine`, `ehcache`, etc.).
- Constructor-injected services that expose deterministic method signatures.
- Observability stack (Actuator, Micrometer) when operating caches in
  production.

## Quick Start

1. **Add dependencies**

   ```xml
   <!-- Maven -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-cache</artifactId>
   </dependency>
   <dependency> <!-- Optional: Caffeine -->
       <groupId>com.github.ben-manes.caffeine</groupId>
       <artifactId>caffeine</artifactId>
   </dependency>
   ```

   ```gradle
   implementation "org.springframework.boot:spring-boot-starter-cache"
   implementation "com.github.ben-manes.caffeine:caffeine"
   ```

2. **Enable caching**

   ```java
   @Configuration
   @EnableCaching
   class CacheConfig {
       @Bean
       CacheManager cacheManager() {
           return new CaffeineCacheManager("users", "orders");
       }
   }
   ```

3. **Annotate service methods**

   ```java
   @Service
   @CacheConfig(cacheNames = "users")
   class UserService {

       @Cacheable(key = "#id", unless = "#result == null")
       User findUser(Long id) { ... }

       @CachePut(key = "#user.id")
       User refreshUser(User user) { ... }

       @CacheEvict(key = "#id", beforeInvocation = false)
       void deleteUser(Long id) { ... }
   }
   ```

4. **Verify behavior**
   - Run focused unit tests that call cached methods twice and assert repository
     invocations.
   - Inspect Actuator `cache` endpoint (if enabled) for hit/miss counters.

## Implementation Workflow

### 1. Define Cache Strategy

- Map hot-path read operations to `@Cacheable`.
- Use `@CachePut` on write paths that must refresh cache entries.
- Apply `@CacheEvict` (`allEntries = true` when invalidating derived caches).
- Combine operations with `@Caching` to keep multi-cache updates consistent.

### 2. Shape Cache Keys and Conditions

- Generate deterministic keys via SpEL (e.g. `key = "#user.id"`).
- Guard caching with `condition = "#price > 0"` for selective caching.
- Prevent null or stale values with `unless = "#result == null"`.
- Synchronize concurrent updates via `sync = true` when needed.

### 3. Manage Providers and TTLs

- Configure provider-specific options:
  - Caffeine spec: `spring.cache.caffeine.spec=maximumSize=500,expireAfterWrite=10m`
  - Redis TTL: `spring.cache.redis.time-to-live=600000`
  - Ehcache XML: define `ttl` and heap/off-heap resources.
- Expose cache names via `spring.cache.cache-names=users,orders,catalog`.
- Avoid on-demand cache name creation in production unless metrics cover usage.

### 4. Operate and Observe Caches

- Surface cache maintenance via a dedicated `CacheManagementService` with
  programmatic `cacheManager.getCache(name)` access.
- Schedule periodic eviction for time-bound caches using `@Scheduled`.
- Wire Actuator `cache` endpoint and Micrometer meters to track hit ratio,
  eviction count, and size.

### 5. Test and Validate

- Prefer slice or unit tests with Mockito/SpyBean to ensure method invocation
  counts.
- Add integration tests with Testcontainers for Redis/Ehcache when using
  external providers.
- Validate concurrency behavior under load (e.g. `sync = true` scenarios).

## Advanced Options

- Integrate JCache annotations when interoperating with providers that favor
  JSR-107 (`@CacheResult`, `@CacheRemove`). Avoid mixing with Spring annotations
  on the same method.
- Cache reactive return types (`Mono`, `Flux`) or `CompletableFuture` values.
  Spring stores resolved values and resubscribes on hits; consider TTL alignment
  with publisher semantics.
- Apply HTTP caching headers using `CacheControl` when exposing cached responses
  via REST.

## Examples

### Example 1: Basic @Cacheable Usage

**Input:**
```java
// First call - cache miss, method executes
User user1 = userService.findUser(1L);

// Second call - cache hit, method skipped
User user2 = userService.findUser(1L);
```

**Output:**
```
// First call logs:
Hibernate: select u1_0.id,u1_0.name from users u1_0 where u1_0.id=?

// Second call: No SQL executed (served from cache)
```

### Example 2: Conditional Caching with SpEL

**Input:**
```java
@Cacheable(value = "products", key = "#id", condition = "#price > 100")
public Product getProduct(Long id, BigDecimal price) {
    return productRepository.findById(id);
}

// Only expensive products are cached
getProduct(1L, new BigDecimal("50.00"));   // Not cached
getProduct(2L, new BigDecimal("150.00"));  // Cached
```

**Output:**
```
Cache 'products' contents after operations:
{2=Product(id=2, price=150.00)}
```

### Example 3: Cache Eviction

**Input:**
```java
@CacheEvict(value = "users", key = "#id")
public void deleteUser(Long id) {
    userRepository.deleteById(id);
}

deleteUser(1L);
```

**Output:**
```
Cache 'users' entry for key '1' removed
```

---

- Load [`references/cache-examples.md`](references/cache-examples.md) for
  progressive scenarios (basic product cache, conditional caching, multilevel
  eviction, Redis integration).
- Load [`references/cache-core-reference.md`](references/cache-core-reference.md)
  for annotation matrices, configuration tables, and property samples.

## References

- [`references/spring-framework-cache-docs.md`](references/spring-framework-cache-docs.md):
  curated excerpts from the Spring Framework Reference Guide (official).
- [`references/spring-cache-doc-snippet.md`](references/spring-cache-doc-snippet.md):
  narrative overview extracted from Spring documentation.
- [`references/cache-core-reference.md`](references/cache-core-reference.md):
  annotation parameters, dependency matrices, property catalogs.
- [`references/cache-examples.md`](references/cache-examples.md):
  end-to-end examples with tests.

## Best Practices

- Prefer constructor injection and immutable DTOs for cache entries.
- Separate cache names per aggregate (`users`, `orders`) to simplify eviction.
- Log cache hits/misses only at debug to avoid noise; push metrics via Micrometer.
- Tune TTLs based on data staleness tolerance; document rationale in code.
- Guard caches that store PII or credentials with encryption or avoid caching.
- Align cache eviction with transactional boundaries to prevent dirty reads.

## Constraints and Warnings

- Avoid caching mutable entities that depend on open persistence contexts.
- Do not mix Spring cache annotations with JCache annotations on the same
  method.
- Ensure multi-level caches (e.g. Caffeine + Redis) maintain consistency; prefer
  publish/subscribe invalidation channels.
- Validate serialization compatibility when caching across service instances.
- Monitor memory footprint to prevent OOM when using in-memory stores.

## Related Skills

- [`../spring-boot-rest-api-standards`](../spring-boot-rest-api-standards/SKILL.md)
- [`../spring-boot-test-patterns`](../spring-boot-test-patterns/SKILL.md)
- [`../unit-test-caching`](../unit-test-caching/SKILL.md)
