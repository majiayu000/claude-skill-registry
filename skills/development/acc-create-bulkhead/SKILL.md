---
name: acc-create-bulkhead
description: Generates Bulkhead pattern for PHP 8.5. Creates resource isolation with semaphore-based concurrency limiting and thread pool isolation. Includes unit tests.
---

# Bulkhead Pattern Generator

Creates Bulkhead pattern infrastructure for resource isolation and fault containment.

## When to Use

| Scenario | Example |
|----------|---------|
| External API calls | Limit concurrent requests to payment gateway |
| Database connections | Pool size limiting |
| CPU-intensive work | Limit by CPU cores |
| Multi-instance | Redis-based coordination |

## Component Characteristics

### BulkheadInterface
- Common interface for all isolation strategies
- Acquire and release semantics
- Capacity monitoring

### Strategies
- **Semaphore Bulkhead**: Limits concurrent executions
- **Thread Pool Bulkhead**: Isolates execution with dedicated pool
- **Queue-based Bulkhead**: Limits with waiting queue

### BulkheadFullException
- Thrown when bulkhead capacity exhausted
- Contains bulkhead name and capacity info

---

## Generation Process

### Step 1: Generate Core Components

**Path:** `src/Infrastructure/Resilience/Bulkhead/`

1. `BulkheadInterface.php` — Common interface
2. `BulkheadConfig.php` — Configuration value object
3. `BulkheadFullException.php` — Exception with capacity info

### Step 2: Generate Bulkhead Implementation

Choose based on use case:

1. `SemaphoreBulkhead.php` — Local semaphore-based limiting
2. `DistributedSemaphoreBulkhead.php` — Redis-based for multi-instance

### Step 3: Generate Registry (Optional)

1. `BulkheadRegistry.php` — Manages multiple bulkheads

### Step 4: Generate Tests

1. `SemaphoreBulkheadTest.php` — Bulkhead behavior tests
2. `BulkheadConfigTest.php` — Configuration tests

---

## File Placement

| Component | Path |
|-----------|------|
| All Classes | `src/Infrastructure/Resilience/Bulkhead/` |
| Unit Tests | `tests/Unit/Infrastructure/Resilience/Bulkhead/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `BulkheadInterface` | `BulkheadInterface` |
| Semaphore | `SemaphoreBulkhead` | `SemaphoreBulkhead` |
| Distributed | `DistributedSemaphoreBulkhead` | `DistributedSemaphoreBulkhead` |
| Config | `BulkheadConfig` | `BulkheadConfig` |
| Registry | `BulkheadRegistry` | `BulkheadRegistry` |
| Exception | `BulkheadFullException` | `BulkheadFullException` |
| Test | `{ClassName}Test` | `SemaphoreBulkheadTest` |

---

## Quick Template Reference

### BulkheadInterface

```php
interface BulkheadInterface
{
    public function execute(callable $operation): mixed;
    public function tryAcquire(): bool;
    public function release(): void;
    public function getAvailablePermits(): int;
    public function getActiveCount(): int;
    public function getName(): string;
}
```

### BulkheadConfig

```php
final readonly class BulkheadConfig
{
    public function __construct(
        public int $maxConcurrentCalls = 10,
        public int $maxWaitDuration = 0,
        public bool $fairness = true
    ) {}

    public static function default(): self;
    public static function forCpuBound(int $cpuCores): self;
    public static function forIoBound(int $cpuCores): self;
    public static function forExternalService(int $maxConnections): self;
}
```

---

## Usage Example

```php
// Create limiter
$bulkhead = new SemaphoreBulkhead(
    name: 'payment-gateway',
    config: BulkheadConfig::forExternalService(maxConnections: 20),
    logger: $logger
);

// Execute with isolation
try {
    $result = $bulkhead->execute(fn() => $client->charge($request));
} catch (BulkheadFullException $e) {
    return Result::serviceOverloaded();
}
```

---

## Use Case Selection

| Use Case | Bulkhead Type | Config |
|----------|---------------|--------|
| External API calls | Semaphore | Limited by API rate limits |
| Database connections | Semaphore | Limited by pool size |
| CPU-intensive work | Semaphore | Limited by CPU cores |
| Multi-instance | Distributed | Redis-based coordination |
| Mixed workloads | Registry | Per-service configuration |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Global Bulkhead | Single point of contention | Per-service bulkheads |
| No Release | Permit leak | Always release in finally |
| Wrong Size | Too small = rejected, too large = no protection | Right-size per service |
| No Metrics | Can't monitor usage | Track acquired/rejected |
| Infinite Wait | Thread starvation | Set maxWaitDuration |
| No Fallback | Hard failure on full | Provide degraded response |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — BulkheadInterface, Config, SemaphoreBulkhead, DistributedSemaphoreBulkhead, Registry
- `references/examples.md` — PaymentGatewayAdapter, ConnectionPool, OrderService examples and tests
