---
name: acc-create-test-double
description: Generates test doubles (Mocks, Stubs, Fakes, Spies) for PHP 8.5. Creates appropriate double type based on testing needs with PHPUnit MockBuilder patterns.
---

# Test Double Generator

Generates appropriate test doubles based on testing needs.

## Test Double Types

| Type | Purpose | Behavior | Verification |
|------|---------|----------|--------------|
| **Stub** | Provide canned answers | Returns predefined values | No |
| **Mock** | Verify interactions | Configurable | Yes (expectations) |
| **Fake** | Working implementation | Real logic, simplified | No |
| **Spy** | Record interactions | Passes through | Yes (inspection) |

## Decision Matrix

```
Need to verify method was called?
├── Yes → Need to record actual calls?
│   ├── Yes → Spy
│   └── No → Mock
└── No → Need real behavior?
    ├── Yes → Fake
    └── No → Stub
```

## When to Use Each

| Scenario | Double Type | Example |
|----------|-------------|---------|
| External API response | Stub | HTTP client returns fixed JSON |
| Verify email sent | Mock | Assert `send()` was called |
| Repository for domain tests | Fake | InMemory implementation |
| Audit logging | Spy | Record all log calls |
| Time-dependent code | Fake | FrozenClock |

## Stub Examples

### PHPUnit Stub

```php
use PHPUnit\Framework\TestCase;

final class OrderServiceTest extends TestCase
{
    public function test_calculates_order_total(): void
    {
        // Create stub
        $taxCalculator = $this->createStub(TaxCalculatorInterface::class);
        $taxCalculator->method('calculate')
            ->willReturn(Money::EUR(100));

        $service = new OrderService($taxCalculator);

        $total = $service->calculateTotal($order);

        self::assertEquals(Money::EUR(1100), $total);
    }
}
```

### Stub with Different Returns

```php
public function test_handles_multiple_calls(): void
{
    $repository = $this->createStub(UserRepositoryInterface::class);

    // Return different values based on argument
    $repository->method('findById')
        ->willReturnCallback(function (UserId $id) {
            return match ($id->toString()) {
                'user-1' => UserMother::john(),
                'user-2' => UserMother::jane(),
                default => null,
            };
        });

    // Or return sequence
    $repository->method('findById')
        ->willReturnOnConsecutiveCalls(
            UserMother::john(),
            UserMother::jane(),
            null
        );
}
```

### Manual Stub Class

```php
<?php

declare(strict_types=1);

namespace Tests\Stub;

use App\Infrastructure\Http\HttpClientInterface;
use App\Infrastructure\Http\HttpResponse;

final class FixedHttpClientStub implements HttpClientInterface
{
    public function __construct(
        private readonly HttpResponse $response
    ) {}

    public function get(string $url, array $headers = []): HttpResponse
    {
        return $this->response;
    }

    public function post(string $url, array $data, array $headers = []): HttpResponse
    {
        return $this->response;
    }

    public static function returning(int $status, array $body): self
    {
        return new self(new HttpResponse($status, json_encode($body)));
    }

    public static function ok(array $body): self
    {
        return self::returning(200, $body);
    }

    public static function error(int $status = 500): self
    {
        return self::returning($status, ['error' => 'Server error']);
    }
}
```

## Mock Examples

### PHPUnit Mock

```php
public function test_sends_notification_on_order_placed(): void
{
    // Create mock with expectations
    $notifier = $this->createMock(NotifierInterface::class);
    $notifier->expects($this->once())
        ->method('notify')
        ->with(
            $this->isInstanceOf(OrderPlacedNotification::class)
        );

    $service = new OrderService($this->repository, $notifier);

    $service->placeOrder($command);

    // Expectations verified automatically
}
```

### Mock with Argument Matching

```php
public function test_logs_with_correct_context(): void
{
    $logger = $this->createMock(LoggerInterface::class);
    $logger->expects($this->once())
        ->method('info')
        ->with(
            'Order placed',
            $this->callback(function (array $context) {
                return isset($context['orderId'])
                    && isset($context['customerId'])
                    && $context['amount'] > 0;
            })
        );

    $service = new OrderService($this->repository, $logger);

    $service->placeOrder($command);
}
```

### Mock Method Call Count

```php
public function test_retries_on_failure(): void
{
    $client = $this->createMock(HttpClientInterface::class);
    $client->expects($this->exactly(3))  // Called exactly 3 times
        ->method('post')
        ->willThrowException(new ConnectionException());

    $service = new PaymentService($client, maxRetries: 3);

    $this->expectException(PaymentFailedException::class);

    $service->charge($payment);
}
```

## Fake Examples

### InMemory Repository (Fake)

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use App\Domain\User\User;
use App\Domain\User\UserId;
use App\Domain\User\UserRepositoryInterface;

final class InMemoryUserRepository implements UserRepositoryInterface
{
    /** @var array<string, User> */
    private array $users = [];

    public function save(User $user): void
    {
        $this->users[$user->id()->toString()] = $user;
    }

    public function findById(UserId $id): ?User
    {
        return $this->users[$id->toString()] ?? null;
    }

    public function delete(User $user): void
    {
        unset($this->users[$user->id()->toString()]);
    }

    // Test helper methods
    public function clear(): void
    {
        $this->users = [];
    }

    public function count(): int
    {
        return count($this->users);
    }
}
```

### Frozen Clock (Fake)

```php
<?php

declare(strict_types=1);

namespace Tests\Fake;

use Psr\Clock\ClockInterface;
use DateTimeImmutable;

final class FrozenClock implements ClockInterface
{
    public function __construct(
        private DateTimeImmutable $now
    ) {}

    public function now(): DateTimeImmutable
    {
        return $this->now;
    }

    public static function at(string $datetime): self
    {
        return new self(new DateTimeImmutable($datetime));
    }

    public function advance(string $interval): void
    {
        $this->now = $this->now->modify($interval);
    }
}

// Usage
$clock = FrozenClock::at('2024-01-15 10:00:00');
$service = new SubscriptionService($clock);

$subscription = $service->create($user);
self::assertEquals('2024-01-15', $subscription->startDate()->format('Y-m-d'));

$clock->advance('+30 days');
self::assertTrue($subscription->isExpired($clock->now()));
```

## Spy Examples

### Collecting Spy

```php
<?php

declare(strict_types=1);

namespace Tests\Spy;

use Psr\Log\LoggerInterface;
use Psr\Log\LogLevel;

final class SpyLogger implements LoggerInterface
{
    /** @var list<array{level: string, message: string, context: array}> */
    private array $logs = [];

    public function log($level, string|\Stringable $message, array $context = []): void
    {
        $this->logs[] = [
            'level' => $level,
            'message' => (string) $message,
            'context' => $context,
        ];
    }

    public function emergency(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::EMERGENCY, $message, $context);
    }

    public function alert(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::ALERT, $message, $context);
    }

    public function critical(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::CRITICAL, $message, $context);
    }

    public function error(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::ERROR, $message, $context);
    }

    public function warning(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::WARNING, $message, $context);
    }

    public function notice(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::NOTICE, $message, $context);
    }

    public function info(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::INFO, $message, $context);
    }

    public function debug(string|\Stringable $message, array $context = []): void
    {
        $this->log(LogLevel::DEBUG, $message, $context);
    }

    // Inspection methods
    /** @return list<array{level: string, message: string, context: array}> */
    public function getLogs(): array
    {
        return $this->logs;
    }

    public function hasLogged(string $level, string $messageContains): bool
    {
        foreach ($this->logs as $log) {
            if ($log['level'] === $level && str_contains($log['message'], $messageContains)) {
                return true;
            }
        }
        return false;
    }

    public function clear(): void
    {
        $this->logs = [];
    }
}
```

### Usage

```php
public function test_logs_order_placement(): void
{
    $logger = new SpyLogger();
    $service = new OrderService($this->repository, $logger);

    $service->placeOrder($command);

    // Inspect recorded logs
    self::assertTrue($logger->hasLogged('info', 'Order placed'));

    $logs = $logger->getLogs();
    self::assertCount(1, $logs);
    self::assertArrayHasKey('orderId', $logs[0]['context']);
}
```

## Generation Instructions

1. **Analyze the dependency:**
   - Interface or class being doubled
   - Methods that need doubling
   - Expected behavior in test

2. **Choose double type:**
   - Verification needed? → Mock or Spy
   - Real behavior needed? → Fake
   - Just return values? → Stub

3. **Generate appropriate implementation:**
   - PHPUnit built-in for simple cases
   - Custom class for complex behavior

4. **File placement:**
   - Stubs: `tests/Stub/`
   - Fakes: `tests/Fake/`
   - Spies: `tests/Spy/`
   - Or combined in `tests/Double/`

## Best Practices

1. **Mock interfaces, not classes** — avoid mocking final classes
2. **Prefer Fakes for repositories** — more realistic behavior
3. **Use Stubs for external services** — HTTP, payment gateways
4. **Limit to 3 mocks per test** — more indicates design issue
5. **Never mock Value Objects** — use real instances
6. **Don't mock what you don't own** — wrap external libraries first
