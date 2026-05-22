---
name: spring-boot-cache
description: Instruction set for enabling and operating the Spring Cache abstraction in Spring Boot when implementing application-level caching for performance-sensitive workloads.
allowed-tools: Read, Write, Bash
category: backend
tags: [spring-boot, caching, performance, cacheable, cache-managers]
version: 1.1.0
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

- [`skills/spring-boot/spring-boot-rest-api-standards`](../spring-boot-rest-api-standards/SKILL.md)
- [`skills/spring-boot/spring-boot-test-patterns`](../spring-boot-test-patterns/SKILL.md)
- [`skills/junit-test/unit-test-caching`](../../junit-test/unit-test-caching/SKILL.md)
