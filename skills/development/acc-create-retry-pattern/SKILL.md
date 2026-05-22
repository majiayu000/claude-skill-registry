---
name: acc-create-retry-pattern
description: Generates Retry pattern for PHP 8.5. Creates resilience component with exponential backoff, jitter, and configurable retry strategies. Includes unit tests.
---

# Retry Pattern Generator

Creates Retry pattern infrastructure for handling transient failures.

## When to Use

| Scenario | Example |
|----------|---------|
| Transient failures | Network timeouts, temporary unavailability |
| External API calls | HTTP requests to third-party services |
| Database operations | Deadlock recovery, connection issues |
| Message processing | Queue message handling with retries |

## Component Characteristics

### RetryPolicy
- Configures retry behavior
- Maximum attempts
- Delay strategy (fixed, exponential, linear)
- Jitter support to prevent thundering herd

### RetryExecutor
- Executes operations with retry logic
- Tracks attempt count
- Applies delay between retries
- Logs retry attempts

### Backoff Strategies
- **Fixed**: Same delay every time
- **Linear**: Delay increases linearly
- **Exponential**: Delay doubles (with optional jitter)

---

## Generation Process

### Step 1: Generate Core Components

**Path:** `src/Infrastructure/Resilience/Retry/`

1. `BackoffStrategy.php` — Enum for delay strategies
2. `RetryPolicy.php` — Configuration with shouldRetry/calculateDelay
3. `RetryContext.php` — Attempt context value object
4. `RetryException.php` — Exception with attempt history

### Step 2: Generate Executor

**Path:** `src/Infrastructure/Resilience/Retry/`

1. `RetryExecutor.php` — Main retry logic with callbacks
2. `SleepInterface.php` — For testability

### Step 3: Generate Tests

1. `RetryPolicyTest.php` — Policy behavior tests
2. `RetryExecutorTest.php` — Executor tests

---

## File Placement

| Component | Path |
|-----------|------|
| All Classes | `src/Infrastructure/Resilience/Retry/` |
| Unit Tests | `tests/Unit/Infrastructure/Resilience/Retry/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Policy | `RetryPolicy` | `RetryPolicy` |
| Strategy Enum | `BackoffStrategy` | `BackoffStrategy` |
| Executor | `RetryExecutor` | `RetryExecutor` |
| Context | `RetryContext` | `RetryContext` |
| Exception | `RetryException` | `RetryException` |
| Test | `{ClassName}Test` | `RetryExecutorTest` |

---

## Quick Template Reference

### RetryPolicy

```php
final readonly class RetryPolicy
{
    public function __construct(
        public int $maxAttempts = 3,
        public int $baseDelayMs = 100,
        public int $maxDelayMs = 10000,
        public float $multiplier = 2.0,
        public bool $useJitter = true,
        public BackoffStrategy $strategy = BackoffStrategy::Exponential,
        public array $retryableExceptions = [],
        public array $nonRetryableExceptions = []
    ) {}

    public static function exponential(int $maxAttempts = 5, int $baseDelayMs = 100): self;
    public static function linear(int $maxAttempts = 5, int $baseDelayMs = 500): self;
    public function shouldRetry(\Throwable $e, int $attempt): bool;
    public function calculateDelay(int $attempt): int;
}
```

### RetryExecutor

```php
final readonly class RetryExecutor
{
    public function execute(
        callable $operation,
        RetryPolicy $policy,
        ?callable $onRetry = null
    ): mixed;
}
```

---

## Usage Example

```php
$policy = new RetryPolicy(
    maxAttempts: 3,
    baseDelayMs: 200,
    retryableExceptions: [
        ConnectionException::class,
        TimeoutException::class,
    ],
    nonRetryableExceptions: [
        ClientException::class,
    ]
);

try {
    $result = $retryExecutor->execute(
        operation: fn() => $httpClient->get($url),
        policy: $policy,
        onRetry: fn($e, $ctx) => $logger->warning('Retrying...', ['attempt' => $ctx->attempt])
    );
} catch (RetryException $e) {
    // All retries exhausted
    $deadLetter->send($message, $e);
}
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| No Max Attempts | Infinite retries | Always set maxAttempts |
| No Backoff | Hammering service | Use exponential backoff |
| Retrying All Exceptions | Retrying unrecoverable errors | Specify retryable exceptions |
| No Jitter | Thundering herd | Enable jitter |
| Ignoring Context | Can't track attempts | Use RetryContext |
| Blocking Forever | Thread exhaustion | Set maxDelayMs cap |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — RetryPolicy, BackoffStrategy, RetryExecutor, RetryContext templates
- `references/examples.md` — HTTP client, database, message consumer examples and tests
