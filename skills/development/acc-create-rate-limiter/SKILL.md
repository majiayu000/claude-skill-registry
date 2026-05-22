---
name: acc-create-rate-limiter
description: Generates Rate Limiter pattern for PHP 8.5. Creates request throttling with token bucket, sliding window, and fixed window algorithms. Includes unit tests.
---

# Rate Limiter Generator

Creates Rate Limiter pattern infrastructure for request throttling and API protection.

## When to Use

| Scenario | Example |
|----------|---------|
| API protection | Prevent abuse |
| Resource throttling | Database connection limits |
| Fair usage | Per-user request limits |
| Burst protection | Spike handling |

## Component Characteristics

### RateLimiterInterface
- Common interface for all algorithms
- Check and consume methods
- Remaining capacity queries

### Algorithms
- **Token Bucket**: Smooth rate limiting with burst capacity
- **Sliding Window**: Time-based with sliding window log
- **Fixed Window**: Simple time-based counter

### RateLimitResult
- Contains allowed/denied status
- Provides retry-after information
- Generates HTTP headers

---

## Generation Process

### Step 1: Generate Core Components

**Path:** `src/Infrastructure/Resilience/RateLimiter/`

1. `RateLimiterInterface.php` — Common interface
2. `RateLimitResult.php` — Result value object with headers
3. `RateLimitExceededException.php` — Exception with retry info
4. `StorageInterface.php` — Storage abstraction

### Step 2: Choose and Generate Algorithm

Choose based on use case:

1. `TokenBucketRateLimiter.php` — For APIs with burst allowance
2. `SlidingWindowRateLimiter.php` — For strict per-time limits
3. `FixedWindowRateLimiter.php` — For simple rate limiting

### Step 3: Generate Storage

1. `RedisStorage.php` — Production storage with TTL

### Step 4: Generate Tests

1. `{Algorithm}RateLimiterTest.php` — Algorithm tests
2. `RateLimitResultTest.php` — Result value object tests

---

## File Placement

| Component | Path |
|-----------|------|
| All Classes | `src/Infrastructure/Resilience/RateLimiter/` |
| Unit Tests | `tests/Unit/Infrastructure/Resilience/RateLimiter/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `RateLimiterInterface` | `RateLimiterInterface` |
| Token Bucket | `TokenBucketRateLimiter` | `TokenBucketRateLimiter` |
| Sliding Window | `SlidingWindowRateLimiter` | `SlidingWindowRateLimiter` |
| Fixed Window | `FixedWindowRateLimiter` | `FixedWindowRateLimiter` |
| Result | `RateLimitResult` | `RateLimitResult` |
| Exception | `RateLimitExceededException` | `RateLimitExceededException` |
| Test | `{ClassName}Test` | `TokenBucketRateLimiterTest` |

---

## Quick Template Reference

### RateLimiterInterface

```php
interface RateLimiterInterface
{
    public function attempt(string $key, int $tokens = 1): RateLimitResult;
    public function getRemainingTokens(string $key): int;
    public function getRetryAfter(string $key): ?int;
    public function reset(string $key): void;
}
```

### RateLimitResult

```php
final readonly class RateLimitResult
{
    public static function allowed(int $remaining, int $limit, \DateTimeImmutable $resetsAt): self;
    public static function denied(int $limit, int $retryAfter, \DateTimeImmutable $resetsAt): self;
    public function isAllowed(): bool;
    public function isDenied(): bool;
    public function toHeaders(): array; // X-RateLimit-* headers
}
```

---

## Usage Example

```php
// Create limiter
$limiter = new TokenBucketRateLimiter(
    capacity: 100,
    refillRate: 10.0, // 10 tokens per second
    clock: $clock,
    storage: new RedisStorage($redis)
);

// Check limit
$result = $limiter->attempt('user:123');

if ($result->isDenied()) {
    throw new RateLimitExceededException(
        key: 'user:123',
        limit: $result->limit,
        retryAfterSeconds: $result->retryAfterSeconds
    );
}

// Add headers to response
foreach ($result->toHeaders() as $name => $value) {
    $response = $response->withHeader($name, (string) $value);
}
```

---

## Algorithm Comparison

| Algorithm | Burst Handling | Memory | Precision | Use Case |
|-----------|----------------|--------|-----------|----------|
| Token Bucket | Good (configurable) | Low | Medium | APIs with burst allowance |
| Sliding Window | Limited | High | High | Strict per-time limits |
| Fixed Window | Poor (boundary issues) | Low | Low | Simple rate limiting |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No Redis/Shared Storage | Per-instance limits | Use shared storage |
| Missing Headers | Client can't adapt | Return X-RateLimit-* headers |
| Single Algorithm | Doesn't fit all cases | Choose per use case |
| No Retry-After | Client spams | Always return retry timing |
| Synchronous Blocking | Thread blocking | Use non-blocking check |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — All algorithm implementations
- `references/examples.md` — Middleware example and tests
