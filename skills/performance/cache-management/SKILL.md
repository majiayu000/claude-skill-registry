---
name: cache-management
description: Implement production-grade caching with cache keys/TTLs/consistency classes per query, SWR (stale-while-revalidate), explicit invalidation, HTTP cache headers, and comprehensive testing for stale reads and cache warmup. Use when adding caching to queries, implementing cache invalidation, configuring HTTP caching, or ensuring cache consistency and performance.
---

# Cache Management Skill

## Context (Input)

Use this skill when:

- Adding caching to repositories or expensive queries
- Implementing cache invalidation via domain events
- Defining cache keys, TTLs, and consistency requirements
- Implementing stale-while-revalidate (SWR) pattern
- Configuring HTTP cache headers (Cache-Control, ETag, Vary)
- Testing cache behavior (stale reads, cold start, invalidation)
- Reducing database load with caching
- Setting up async event-driven cache invalidation

## Task (Function)

Implement production-ready caching with proper key design, TTL management, event-driven invalidation, HTTP cache headers, and comprehensive testing.

**Success Criteria**:

- Cache policy declared for each query (key, TTL, consistency class)
- Decorator pattern with `CachedXxxRepository` wrapping `MongoXxxRepository`
- Event-driven invalidation via domain event subscribers
- Marker interface pattern for auto-binding cache pools
- Best-effort invalidation (try/catch, never fail business operations)
- HTTP cache headers configured (Cache-Control, ETag for API responses)
- Async event processing via message queue (AP from CAP theorem)
- Comprehensive unit tests for all cache paths
- Cache observability (hit/miss/error logging)
- `make ci` outputs "✅ CI checks successfully passed!"

---

## ⚠️ CRITICAL CACHE POLICY

```text
╔═══════════════════════════════════════════════════════════════╗
║  ALWAYS use Decorator Pattern for caching (wrap repositories) ║
║  ALWAYS use CacheKeyBuilder service (prevent key drift)       ║
║  ALWAYS invalidate via Domain Events (decouple from business) ║
║  ALWAYS use TagAwareCacheInterface for cache tags             ║
║  ALWAYS wrap cache ops in try/catch (best-effort, no failures)║
║  ALWAYS use Marker Interface for auto-binding cache pools     ║
║  ALWAYS process invalidation async (AP from CAP theorem)      ║
║                                                               ║
║  ❌ FORBIDDEN: Caching in repository, implicit invalidation   ║
║  ✅ REQUIRED:  Decorator pattern, event-driven invalidation   ║
╚═══════════════════════════════════════════════════════════════╝
```

## CAP Theorem: Why We Choose AP (Availability + Partition Tolerance)

Cache invalidation follows **AP from CAP theorem** - we prioritize:

- **Availability**: Business operations never fail due to cache issues
- **Partition Tolerance**: System works even when cache is unavailable

**Trade-off**: Brief staleness is acceptable over blocking writes.

**Implementation**:

- Cache errors fallback to database (try/catch everywhere)
- Invalidation processed asynchronously via message queue
- Exceptions in subscribers are logged + emit metrics (self-healing)
- Business operations complete even if cache invalidation fails

**Non-negotiable requirements**:

- Use Decorator Pattern: `CachedXxxRepository` wraps `MongoXxxRepository`
- Use centralized `CacheKeyBuilder` service (in `Shared/Infrastructure/Cache`)
- Invalidate via Domain Event Subscribers (one subscriber per event)
- Use Marker Interface for auto-binding cache pools via `_instanceof`
- Process cache invalidation asynchronously via message queue
- Wrap ALL cache operations in try/catch (never fail business operations)
- Use `TagAwareCacheInterface` (not `CacheInterface`) for tag support
- Configure test cache pools with `tags: true` in `config/packages/test/cache.yaml`
- Log cache operations for observability

## File Locations (This Codebase)

> These are **example** locations based on the Codely/Hexagonal structure used in VilnaCRM services.
> Adapt the bounded context (`User`, `OAuth`, etc.) to your feature.

| Component                    | Typical Location                                                                                |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| CacheKeyBuilder              | `src/Shared/Infrastructure/Cache/CacheKeyBuilder.php`                                           |
| CachedXxxRepository          | `src/{Context}/{Bounded}/Infrastructure/Repository/CachedXxxRepository.php`                     |
| Base repository (inner)      | `src/{Context}/{Bounded}/Infrastructure/Repository/*Repository.php`                             |
| Marker interface             | `src/{Context}/{Bounded}/Application/EventSubscriber/*CacheInvalidationSubscriberInterface.php` |
| Invalidation subscriber      | `src/{Context}/{Bounded}/Application/EventSubscriber/*CacheInvalidationSubscriber.php`          |
| Cache pool config            | `config/packages/cache.yaml`                                                                    |
| Test cache config            | `config/packages/test/cache.yaml`                                                               |
| Service wiring / aliases     | `config/services.yaml`                                                                          |
| HTTP cache tests             | `tests/Integration/*HttpCacheTest.php`                                                          |
| Unit tests                   | `tests/Unit/**`                                                                                 |
| Integration tests (optional) | `tests/Integration/**`                                                                          |

---

## TL;DR - Cache Management Checklist

**Before Implementing Cache:**

- [ ] Identified slow query worth caching
- [ ] Cache policy declared (key pattern, TTL, consistency class)
- [ ] Cache tags defined for invalidation strategy
- [ ] Domain events defined for cache invalidation triggers
- [ ] HTTP cache headers strategy defined (if API endpoint)

**Architecture Setup:**

- [ ] Created `CachedXxxRepository` decorator class
- [ ] Created `CacheKeyBuilder` service (or extended existing one)
- [ ] Created marker interface for cache invalidation subscribers
- [ ] Created cache invalidation event subscribers (one per event)
- [ ] Configured `services.yaml` with `_instanceof` for auto-binding cache pools
- [ ] Configured async event processing via message bus

**During Implementation:**

- [ ] Decorator wraps inner repository (not extends)
- [ ] CacheKeyBuilder used for all cache keys (prevents drift)
- [ ] Cache operations wrapped in try/catch (best-effort)
- [ ] Event subscribers use same CacheKeyBuilder for tags
- [ ] Logging added for cache hits/misses/errors
- [ ] Repository uses `TagAwareCacheInterface` (required for tags)

**Testing:**

- [ ] Test cache pool configured with `tags: true`
- [ ] Unit tests for cache invalidation subscribers
- [ ] Integration tests for stale reads after writes (if valuable)
- [ ] Test: Cache error fallback to database works
- [ ] HTTP cache tests for Cache-Control headers and ETag validation

**Before Merge:**

- [ ] All cache tests pass
- [ ] Cache observability verified (logs present)
- [ ] HTTP cache headers verified (if API endpoint)
- [ ] CI checks pass (`make ci`)
- [ ] No cache-related stale data issues

---

## Quick Start: Cache in 9 Steps

### Step 1: Declare Cache Policy

**Before writing code, declare the complete policy:**

```php
/**
 * Cache Policy for Customer By ID Query
 *
 * Key Pattern: customer.{id}
 * TTL: 600s (10 minutes)
 * Consistency: Stale-While-Revalidate
 * Invalidation: Via domain events (CustomerCreated/Updated/Deleted)
 * Tags: [customer, customer.{id}]
 * HTTP Cache: Cache-Control: max-age=600, public, s-maxage=600
 * Notes: Read-heavy operation, tolerates brief staleness
 */
```

### Step 2: Create CacheKeyBuilder Service

**Location**: `src/Shared/Infrastructure/Cache/CacheKeyBuilder.php`

```php
final readonly class CacheKeyBuilder
{
    public function build(string $namespace, string ...$parts): string
    {
        return $namespace . '.' . implode('.', $parts);
    }

    public function buildCustomerKey(string $customerId): string
    {
        return $this->build('customer', $customerId);
    }

    public function buildCustomerEmailKey(string $email): string
    {
        return $this->build('customer', 'email', $this->hashEmail($email));
    }

    /**
     * Build cache key for collections (filters normalized + hashed)
     * @param array<string, string|int|float|bool|array|null> $filters
     */
    public function buildCustomerCollectionKey(array $filters): string
    {
        ksort($filters);  // Normalize key order
        return $this->build(
            'customer',
            'collection',
            hash('sha256', json_encode($filters, \JSON_THROW_ON_ERROR))
        );
    }

    /**
     * Hash email consistently (lowercase + SHA256)
     * - Lowercase normalization (email case-insensitive)
     * - SHA256 hashing (fixed length, prevents key length issues)
     */
    public function hashEmail(string $email): string
    {
        return hash('sha256', strtolower($email));
    }
}
```

### Step 3: Create Cached Repository Decorator

**Location**: `src/{Context}/{Entity}/Infrastructure/Repository/Cached{Entity}Repository.php`

```php
final class CachedCustomerRepository implements CustomerRepositoryInterface
{
    public function __construct(
        private CustomerRepositoryInterface $inner,  // Wraps base repository
        private TagAwareCacheInterface $cache,
        private CacheKeyBuilder $cacheKeyBuilder,
        private LoggerInterface $logger
    ) {}

    /**
     * Proxy all other method calls to inner repository
     * Required for API Platform's collection provider compatibility
     * @param array<int, mixed> $arguments
     */
    public function __call(string $method, array $arguments): mixed
    {
        return $this->inner->{$method}(...$arguments);
    }

    public function find(mixed $id, int $lockMode = 0, ?int $lockVersion = null): ?Customer
    {
        $cacheKey = $this->cacheKeyBuilder->buildCustomerKey((string) $id);

        try {
            return $this->cache->get(
                $cacheKey,
                fn (ItemInterface $item) => $this->loadCustomerFromDb($id, $lockMode, $lockVersion, $cacheKey, $item),
                beta: 1.0
            );
        } catch (\Throwable $e) {
            $this->logCacheError($cacheKey, $e);
            return $this->inner->find($id, $lockMode, $lockVersion);
        }
    }

    public function save(Customer $customer): void
    {
        $this->inner->save($customer);
        // NO cache invalidation here - handled by domain event subscribers
    }

    private function loadCustomerFromDb(mixed $id, int $lockMode, ?int $lockVersion, string $cacheKey, ItemInterface $item): ?Customer
    {
        $item->expiresAfter(600);
        $item->tag(['customer', "customer.{$id}"]);

        $this->logger->info('Cache miss - loading customer from database', [
            'cache_key' => $cacheKey,
            'customer_id' => $id,
            'operation' => 'cache.miss',
        ]);

        return $this->inner->find($id, $lockMode, $lockVersion);
    }

    private function logCacheError(string $cacheKey, \Throwable $e): void
    {
        $this->logger->error('Cache error - falling back to database', [
            'cache_key' => $cacheKey,
            'error' => $e->getMessage(),
            'operation' => 'cache.error',
        ]);
    }
}
```

### Step 4: Create Marker Interface for Auto-Binding

**Location**: `src/{Context}/{Entity}/Application/EventSubscriber/{Entity}CacheInvalidationSubscriberInterface.php`

**Purpose**: Enables automatic cache pool injection via `_instanceof` in services.yaml.

```php
<?php

declare(strict_types=1);

namespace App\Core\Customer\Application\EventSubscriber;

use App\Shared\Domain\Bus\Event\DomainEventSubscriberInterface;

/**
 * Marker interface for customer cache invalidation subscribers.
 *
 * Used to auto-bind the customer cache pool via Symfony _instanceof configuration.
 */
interface CustomerCacheInvalidationSubscriberInterface extends DomainEventSubscriberInterface
{
}
```

### Step 5: Create Event Subscribers for Invalidation

**Location**: `src/{Context}/{Entity}/Application/EventSubscriber/{Event}CacheInvalidationSubscriber.php`

**IMPORTANT**: Create ONE subscriber per event. Implement the marker interface.

```php
/**
 * Customer Updated Event Cache Invalidation Subscriber
 *
 * ARCHITECTURAL DECISION: Processed via async queue (ResilientAsyncEventBus)
 * This subscriber runs in Symfony Messenger workers. Exceptions propagate to
 * DomainEventMessageHandler which catches, logs, and emits failure metrics.
 * We follow AP from CAP theorem (Availability + Partition tolerance over Consistency).
 */
final readonly class CustomerUpdatedCacheInvalidationSubscriber implements
    CustomerCacheInvalidationSubscriberInterface
{
    public function __construct(
        private TagAwareCacheInterface $cache,
        private CacheKeyBuilder $cacheKeyBuilder,
        private LoggerInterface $logger
    ) {}

    public function __invoke(CustomerUpdatedEvent $event): void
    {
        $tagsToInvalidate = $this->buildTagsToInvalidate($event);
        $this->cache->invalidateTags($tagsToInvalidate);
        $this->logSuccess($event);
    }

    /** @return array<class-string> */
    public function subscribedTo(): array
    {
        return [CustomerUpdatedEvent::class];
    }

    /** @return array<string> */
    private function buildTagsToInvalidate(CustomerUpdatedEvent $event): array
    {
        $tags = [
            'customer.' . $event->customerId(),
            'customer.email.' . $this->cacheKeyBuilder->hashEmail($event->currentEmail()),
            'customer.collection',
        ];

        if ($event->emailChanged() && $event->previousEmail() !== null) {
            $tags[] = 'customer.email.' . $this->cacheKeyBuilder->hashEmail($event->previousEmail());
        }

        return $tags;
    }

    private function logSuccess(CustomerUpdatedEvent $event): void
    {
        $this->logger->info('Cache invalidated after customer update', [
            'event_id' => $event->eventId(),
            'email_changed' => $event->emailChanged(),
            'operation' => 'cache.invalidation',
            'reason' => 'customer_updated',
        ]);
    }
}
```

### Step 6: Configure services.yaml with Marker Interface

**CRITICAL**: Use `_instanceof` with the marker interface for auto-binding cache pools.

```yaml
services:
  # Base repository - used by API Platform for collections
  App\Core\Customer\Infrastructure\Repository\MongoCustomerRepository:
    public: true

  # Cached repository - wraps base repository with caching
  App\Core\Customer\Infrastructure\Repository\CachedCustomerRepository:
    arguments:
      $inner: '@App\Core\Customer\Infrastructure\Repository\MongoCustomerRepository'
      $cache: '@cache.customer'

  # Alias interface to cached repository for dependency injection
  App\Core\Customer\Domain\Repository\CustomerRepositoryInterface:
    alias: App\Core\Customer\Infrastructure\Repository\CachedCustomerRepository
    public: true

  # Auto-bind cache pool to all cache invalidation subscribers via marker interface
  _instanceof:
    App\Core\Customer\Application\EventSubscriber\CustomerCacheInvalidationSubscriberInterface:
      bind:
        $cache: '@cache.customer'

    App\Shared\Domain\Bus\Event\DomainEventSubscriberInterface:
      tags: ['app.event_subscriber']

  # Async event bus for cache invalidation (AP from CAP theorem)
  App\Shared\Domain\Bus\Event\EventBusInterface:
    alias: App\Shared\Infrastructure\Bus\Event\Async\ResilientAsyncEventBus
```

### Step 7: Configure Cache Pools

**Production** - `config/packages/cache.yaml`:

```yaml
framework:
  cache:
    app: cache.adapter.redis
    default_redis_provider: '%env(resolve:REDIS_URL)%'

    pools:
      cache.customer:
        adapter: cache.adapter.redis
        default_lifetime: 600
        provider: '%env(resolve:REDIS_URL)%'
        tags: true
```

**Test** - `config/packages/test/cache.yaml`:

```yaml
framework:
  cache:
    pools:
      cache.customer:
        adapter: cache.adapter.array
        provider: null
        tags: true
```

### Step 8: Configure HTTP Cache Headers (API Platform)

**For API endpoints**, configure HTTP cache headers in your API Platform resource:

```yaml
# config/api_platform/resources/customer.yaml
App\Core\Customer\Domain\Entity\Customer:
  operations:
    get:
      class: ApiPlatform\Metadata\Get
      cacheHeaders:
        max_age: 600
        shared_max_age: 600
        public: true
        vary: ['Accept', 'Accept-Language']

    get_collection:
      class: ApiPlatform\Metadata\GetCollection
      cacheHeaders:
        max_age: 300
        shared_max_age: 600
        public: true
        vary: ['Accept', 'Accept-Language']
```

**HTTP Cache Headers Explained**:

| Header     | Single Resource         | Collection              | Purpose              |
| ---------- | ----------------------- | ----------------------- | -------------------- |
| `max-age`  | 600s (10 min)           | 300s (5 min)            | Browser cache TTL    |
| `s-maxage` | 600s                    | 600s                    | CDN/proxy cache TTL  |
| `public`   | true                    | true                    | Allow shared caching |
| `Vary`     | Accept, Accept-Language | Accept, Accept-Language | Cache key variants   |
| `ETag`     | Auto-generated          | Auto-generated          | Conditional requests |

**ETag Behavior**:

- ETag is automatically generated based on resource content
- ETag changes after resource modification
- Clients can use `If-None-Match` for conditional requests
- Returns `304 Not Modified` if resource unchanged

### Step 9: Verify with CI

```bash
make ci
```

---

## HTTP Cache Testing

Test HTTP cache headers in integration tests:

```php
final class CustomerHttpCacheTest extends ApiTestCase
{
    public function testGetCustomerReturnsCacheControlHeaders(): void
    {
        $client = self::createClient();
        $customer = $this->createTestCustomer();

        $client->request('GET', "/api/customers/{$customer->getUlid()}");

        self::assertResponseIsSuccessful();
        self::assertResponseHeaderSame('Cache-Control', 'max-age=600, public, s-maxage=600');
        self::assertResponseHasHeader('ETag');
    }

    public function testGetCustomerCollectionReturnsCacheControlHeaders(): void
    {
        $client = self::createClient();
        $this->createTestCustomer();

        $client->request('GET', '/api/customers');

        self::assertResponseIsSuccessful();
        self::assertResponseHeaderSame('Cache-Control', 'max-age=300, public, s-maxage=600');
    }

    public function testETagChangesAfterModification(): void
    {
        $client = self::createClient();
        $customer = $this->createTestCustomer();

        // First request to get initial ETag
        $response1 = $client->request('GET', "/api/customers/{$customer->getUlid()}");
        $etag1 = $response1->getHeaders()['etag'][0] ?? null;
        self::assertNotNull($etag1);

        // Modify customer
        $client->request('PATCH', "/api/customers/{$customer->getUlid()}", [
            'json' => ['initials' => 'Updated Name'],
            'headers' => ['Content-Type' => 'application/merge-patch+json'],
        ]);

        // Request again to get new ETag
        $response2 = $client->request('GET', "/api/customers/{$customer->getUlid()}");
        $etag2 = $response2->getHeaders()['etag'][0] ?? null;

        // ETag should change after modification
        self::assertNotEquals($etag1, $etag2);
    }
}
```

---

## Async Event Processing Architecture

Cache invalidation is processed asynchronously for resilience:

```text
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Domain Event   │────▶│ ResilientAsyncEvent  │────▶│    SQS Queue        │
│  (Published)    │     │ Dispatcher           │     │                     │
└─────────────────┘     └──────────────────────┘     └─────────┬───────────┘
                                                               │
                        ┌──────────────────────┐               │
                        │  DomainEventMessage  │◀──────────────┘
                        │  Handler             │
                        └──────────┬───────────┘
                                   │
                        ┌──────────▼───────────┐
                        │  Cache Invalidation  │
                        │  Subscriber          │
                        └──────────────────────┘
```

**Resilience Layers**:

1. **Layer 1**: `ResilientAsyncEventDispatcher` catches SQS send failures
2. **Layer 2**: `DomainEventMessageHandler` catches subscriber failures
3. **All failures**: Logged + emit metrics (self-healing pipeline)

---

## Additional Resources

- Policy decisions: `reference/cache-policies.md`
- Invalidation patterns: `reference/invalidation-strategies.md`
- SWR details: `reference/swr-pattern.md`
- End-to-end example: `examples/cache-implementation.md`
- Tests guide: `examples/cache-testing.md`
