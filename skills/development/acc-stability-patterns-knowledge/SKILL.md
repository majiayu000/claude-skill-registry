---
name: acc-stability-patterns-knowledge
description: Stability Patterns knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Circuit Breaker, Retry, Rate Limiter, Bulkhead, and resilience audits.
---

# Stability Patterns Knowledge Base

Quick reference for resilience and fault tolerance patterns in PHP applications.

## Core Patterns Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STABILITY PATTERNS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                      REQUEST FLOW                                   │    │
│   │                                                                     │    │
│   │   Client  ──▶  Rate Limiter  ──▶  Circuit Breaker  ──▶  Service   │    │
│   │      │              │                   │                  │        │    │
│   │      │         Throttle            Monitor State       Actual      │    │
│   │      │         requests            Open/Closed         work        │    │
│   │      │              │                   │                  │        │    │
│   │      │              ▼                   ▼                  ▼        │    │
│   │      │         ┌────────┐          ┌────────┐         ┌────────┐   │    │
│   │      │         │Bulkhead│          │ Retry  │         │Timeout │   │    │
│   │      │         │Isolate │          │Pattern │         │Control │   │    │
│   │      │         └────────┘          └────────┘         └────────┘   │    │
│   └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│   Pattern          │ Purpose                    │ Protects Against           │
│   ─────────────────┼────────────────────────────┼─────────────────────────── │
│   Rate Limiter     │ Throttle request rate      │ DDoS, overload, abuse     │
│   Circuit Breaker  │ Fail fast on failures      │ Cascading failures        │
│   Retry            │ Retry transient failures   │ Temporary outages         │
│   Bulkhead         │ Isolate resources          │ Resource exhaustion       │
│   Timeout          │ Limit wait time            │ Slow dependencies         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Pattern Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PATTERN INTERACTION                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                         ┌────────────────────┐                               │
│                         │   Rate Limiter     │                               │
│                         │  (Entry Point)     │                               │
│                         └─────────┬──────────┘                               │
│                                   │                                          │
│                                   ▼                                          │
│                         ┌────────────────────┐                               │
│                         │     Bulkhead       │                               │
│                         │ (Resource Limits)  │                               │
│                         └─────────┬──────────┘                               │
│                                   │                                          │
│           ┌───────────────────────┼───────────────────────┐                  │
│           │                       │                       │                  │
│           ▼                       ▼                       ▼                  │
│   ┌──────────────┐       ┌──────────────┐        ┌──────────────┐           │
│   │   Service A  │       │   Service B  │        │   Service C  │           │
│   │  ┌────────┐  │       │  ┌────────┐  │        │  ┌────────┐  │           │
│   │  │Circuit │  │       │  │Circuit │  │        │  │Circuit │  │           │
│   │  │Breaker │  │       │  │Breaker │  │        │  │Breaker │  │           │
│   │  └───┬────┘  │       │  └───┬────┘  │        │  └───┬────┘  │           │
│   │      │       │       │      │       │        │      │       │           │
│   │  ┌───▼────┐  │       │  ┌───▼────┐  │        │  ┌───▼────┐  │           │
│   │  │ Retry  │  │       │  │ Retry  │  │        │  │ Retry  │  │           │
│   │  │Pattern │  │       │  │Pattern │  │        │  │Pattern │  │           │
│   │  └────────┘  │       │  └────────┘  │        │  └────────┘  │           │
│   └──────────────┘       └──────────────┘        └──────────────┘           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Quick Reference

### Circuit Breaker States

| State | Behavior | Transitions To |
|-------|----------|----------------|
| **Closed** | Requests pass through, failures counted | Open (on threshold) |
| **Open** | Requests fail fast, no calls to service | Half-Open (after timeout) |
| **Half-Open** | Limited requests allowed for testing | Closed (on success) / Open (on failure) |

### Retry Backoff Strategies

| Strategy | Formula | Use Case |
|----------|---------|----------|
| **Fixed** | `delay` | Simple cases, known recovery time |
| **Linear** | `delay * attempt` | Gradual increase |
| **Exponential** | `delay * 2^(attempt-1)` | Unknown recovery, default choice |
| **Exponential + Jitter** | `exponential ± random` | High concurrency, prevents thundering herd |

### Rate Limiter Algorithms

| Algorithm | Precision | Memory | Burst Handling |
|-----------|-----------|--------|----------------|
| **Token Bucket** | Medium | Low | Allows bursts |
| **Sliding Window** | High | Medium | Smooth limiting |
| **Fixed Window** | Low | Low | Edge bursts |
| **Leaky Bucket** | High | Low | No bursts |

### Bulkhead Types

| Type | Isolation | Use Case |
|------|-----------|----------|
| **Semaphore** | Thread/request count | Single-process apps |
| **Thread Pool** | Dedicated threads | CPU-bound work |
| **Queue-based** | Request queue | Async processing |
| **Distributed** | Redis/shared state | Multi-instance apps |

## PHP Implementation Patterns

### Circuit Breaker with PSR Clock

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Resilience;

use Psr\Clock\ClockInterface;

final class CircuitBreaker
{
    private CircuitState $state = CircuitState::Closed;
    private int $failures = 0;
    private ?\DateTimeImmutable $openedAt = null;

    public function __construct(
        private readonly string $name,
        private readonly int $failureThreshold,
        private readonly int $openTimeoutSeconds,
        private readonly ClockInterface $clock
    ) {}

    public function execute(callable $operation, ?callable $fallback = null): mixed
    {
        if (!$this->isAvailable()) {
            return $fallback ? $fallback() : throw new CircuitOpenException($this->name);
        }

        try {
            $result = $operation();
            $this->recordSuccess();
            return $result;
        } catch (\Throwable $e) {
            $this->recordFailure();
            throw $e;
        }
    }

    private function isAvailable(): bool
    {
        if ($this->state === CircuitState::Closed) return true;
        if ($this->state === CircuitState::Open) {
            if ($this->hasTimeoutElapsed()) {
                $this->state = CircuitState::HalfOpen;
                return true;
            }
            return false;
        }
        return true;
    }
}
```

### Retry with Exponential Backoff

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Resilience;

final readonly class RetryExecutor
{
    public function execute(
        callable $operation,
        int $maxAttempts = 3,
        int $baseDelayMs = 100
    ): mixed {
        $attempt = 0;
        $lastException = null;

        while ($attempt < $maxAttempts) {
            try {
                return $operation();
            } catch (\Throwable $e) {
                $lastException = $e;
                $attempt++;

                if ($attempt < $maxAttempts) {
                    $delay = $baseDelayMs * (2 ** ($attempt - 1));
                    $jitter = random_int(0, (int)($delay * 0.3));
                    usleep(($delay + $jitter) * 1000);
                }
            }
        }

        throw $lastException;
    }
}
```

### Token Bucket Rate Limiter

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Resilience;

final class TokenBucketRateLimiter
{
    private float $tokens;
    private int $lastRefill;

    public function __construct(
        private readonly int $capacity,
        private readonly float $refillRate,
        private readonly \Redis $redis,
        private readonly string $key
    ) {
        $this->tokens = $capacity;
        $this->lastRefill = time();
    }

    public function attempt(): bool
    {
        $this->refill();

        if ($this->tokens >= 1) {
            $this->tokens--;
            return true;
        }

        return false;
    }

    private function refill(): void
    {
        $now = time();
        $elapsed = $now - $this->lastRefill;
        $this->tokens = min(
            $this->capacity,
            $this->tokens + ($elapsed * $this->refillRate)
        );
        $this->lastRefill = $now;
    }
}
```

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| No timeout on external calls | HTTP clients, DB queries | Critical |
| Retry without backoff | Retry implementations | Warning |
| No circuit breaker on external services | API clients, adapters | Critical |
| Unbounded connection pools | Database, HTTP pools | Warning |
| No fallback strategy | Circuit breaker usage | Warning |
| Retry non-idempotent operations | Command handlers | Critical |
| Rate limiting only in-memory | Multi-instance apps | Warning |
| No jitter in retry | High-concurrency systems | Warning |

## Detection Patterns

```bash
# Find resilience implementations
Glob: **/Resilience/**/*.php
Glob: **/CircuitBreaker/**/*.php
Grep: "CircuitBreaker|RateLimiter|Retry" --glob "**/*.php"

# Check for proper timeout usage
Grep: "CURLOPT_TIMEOUT|timeout|setTimeout" --glob "**/Http/**/*.php"

# Detect retry patterns
Grep: "retry|backoff|exponential" --glob "**/*.php"

# Find rate limiting
Grep: "RateLimiter|throttle|TokenBucket" --glob "**/*.php"

# Check for bulkhead patterns
Grep: "Semaphore|Bulkhead|maxConcurrent" --glob "**/*.php"

# Detect missing patterns
Grep: "->request\(|curl_exec|file_get_contents" --glob "**/Infrastructure/**/*.php"
```

## Configuration Guidelines

### Circuit Breaker Settings

| Service Type | Failure Threshold | Open Timeout | Success Threshold |
|--------------|-------------------|--------------|-------------------|
| Critical API | 3-5 | 30-60s | 3-5 |
| Background Job | 5-10 | 60-120s | 2-3 |
| Internal Service | 3-5 | 15-30s | 2-3 |
| Database | 2-3 | 10-20s | 1-2 |

### Retry Configuration

| Operation Type | Max Attempts | Base Delay | Max Delay |
|----------------|--------------|------------|-----------|
| HTTP API Call | 3 | 100ms | 10s |
| Database Query | 3 | 50ms | 5s |
| Message Queue | 5 | 1s | 60s |
| File Operation | 2 | 10ms | 100ms |

### Rate Limiter Settings

| Endpoint Type | Rate | Window | Burst |
|---------------|------|--------|-------|
| Public API | 100/min | 1 min | 20 |
| Authenticated API | 1000/min | 1 min | 100 |
| Admin API | 10000/min | 1 min | 1000 |
| Webhook | 60/min | 1 min | 10 |

## Integration Points

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   src/Infrastructure/                                                        │
│   ├── Resilience/                                                           │
│   │   ├── CircuitBreaker/                                                   │
│   │   │   ├── CircuitBreaker.php                                           │
│   │   │   ├── CircuitBreakerConfig.php                                     │
│   │   │   ├── CircuitBreakerRegistry.php                                   │
│   │   │   └── CircuitState.php                                             │
│   │   ├── Retry/                                                            │
│   │   │   ├── RetryExecutor.php                                            │
│   │   │   ├── RetryPolicy.php                                              │
│   │   │   └── BackoffStrategy.php                                          │
│   │   ├── RateLimiter/                                                      │
│   │   │   ├── RateLimiterInterface.php                                     │
│   │   │   ├── TokenBucketRateLimiter.php                                   │
│   │   │   └── SlidingWindowRateLimiter.php                                 │
│   │   └── Bulkhead/                                                         │
│   │       ├── BulkheadInterface.php                                        │
│   │       ├── SemaphoreBulkhead.php                                        │
│   │       └── BulkheadRegistry.php                                         │
│   │                                                                         │
│   ├── Http/                                                                  │
│   │   ├── ResilientHttpClient.php    ◀── Uses CircuitBreaker + Retry       │
│   │   └── Middleware/                                                       │
│   │       └── RateLimitMiddleware.php                                       │
│   │                                                                         │
│   └── Payment/                                                               │
│       └── PaymentGatewayAdapter.php  ◀── Uses CircuitBreaker + Bulkhead    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## References

For detailed information, load these reference files:

- `references/circuit-breaker.md` — Circuit Breaker implementation details
- `references/retry-patterns.md` — Retry strategies and backoff algorithms
- `references/rate-limiting.md` — Rate limiting algorithms and configurations
- `references/bulkhead.md` — Bulkhead isolation patterns

## Assets

- `assets/report-template.md` — Structured audit report template
