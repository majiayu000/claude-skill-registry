---
name: acc-create-unit-test
description: Generates PHPUnit unit tests for PHP 8.5. Creates isolated tests with AAA pattern, proper naming, attributes, and one behavior per test. Supports Value Objects, Entities, Services.
---

# Unit Test Generator

Generates PHPUnit 11+ unit tests for PHP 8.5 classes.

## Characteristics

- **Isolated** — no external dependencies (DB, HTTP, filesystem)
- **Fast** — executes in <100ms
- **Focused** — one behavior per test
- **AAA Pattern** — Arrange-Act-Assert structure
- **Self-documenting** — descriptive test names

## Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\{Namespace};

use {FullyQualifiedClassName};
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass({ClassName}::class)]
final class {ClassName}Test extends TestCase
{
    private {ClassName} $sut;

    protected function setUp(): void
    {
        $this->sut = new {ClassName}(/* dependencies */);
    }

    public function test_{method}_{scenario}_{expected}(): void
    {
        // Arrange
        {arrange_code}

        // Act
        {act_code}

        // Assert
        {assert_code}
    }
}
```

## Naming Convention

```
test_{method}_{scenario}_{expected}
```

| Part | Description | Example |
|------|-------------|---------|
| `{method}` | Method under test | `calculate_total` |
| `{scenario}` | Input condition | `with_discount` |
| `{expected}` | Expected outcome | `returns_reduced_price` |

**Examples:**
```php
test_confirm_when_pending_changes_status_to_confirmed
test_create_with_invalid_email_throws_exception
test_equals_with_same_value_returns_true
test_add_item_increases_total
```

## Test Patterns by Component

### Value Object Tests

```php
#[Group('unit')]
#[CoversClass(Email::class)]
final class EmailTest extends TestCase
{
    // Creation - valid
    public function test_creates_with_valid_email(): void
    {
        $email = new Email('user@example.com');

        self::assertSame('user@example.com', $email->value);
    }

    // Validation - invalid
    public function test_throws_for_empty_value(): void
    {
        $this->expectException(InvalidArgumentException::class);

        new Email('');
    }

    public function test_throws_for_invalid_format(): void
    {
        $this->expectException(InvalidArgumentException::class);

        new Email('not-an-email');
    }

    // Equality
    public function test_equals_returns_true_for_same_value(): void
    {
        $email1 = new Email('user@example.com');
        $email2 = new Email('user@example.com');

        self::assertTrue($email1->equals($email2));
    }

    public function test_equals_returns_false_for_different_value(): void
    {
        $email1 = new Email('user@example.com');
        $email2 = new Email('other@example.com');

        self::assertFalse($email1->equals($email2));
    }
}
```

### Entity Tests

```php
#[Group('unit')]
#[CoversClass(Order::class)]
final class OrderTest extends TestCase
{
    private Order $order;

    protected function setUp(): void
    {
        $this->order = new Order(
            OrderId::fromString('order-123'),
            CustomerId::fromString('customer-456')
        );
    }

    // Identity
    public function test_has_unique_identity(): void
    {
        self::assertSame('order-123', $this->order->id()->toString());
    }

    // Initial state
    public function test_is_pending_when_created(): void
    {
        self::assertTrue($this->order->isPending());
    }

    // State transitions - valid
    public function test_confirm_changes_status_to_confirmed(): void
    {
        $this->order->addItem(ProductMother::book(), 1);

        $this->order->confirm();

        self::assertTrue($this->order->isConfirmed());
    }

    // State transitions - invalid
    public function test_confirm_throws_when_already_confirmed(): void
    {
        $this->order->addItem(ProductMother::book(), 1);
        $this->order->confirm();

        $this->expectException(DomainException::class);

        $this->order->confirm();
    }

    // Business rules
    public function test_add_item_increases_total(): void
    {
        $this->order->addItem(ProductMother::withPrice(Money::EUR(100)), 2);

        self::assertEquals(Money::EUR(200), $this->order->total());
    }

    // Domain events
    public function test_records_order_confirmed_event(): void
    {
        $this->order->addItem(ProductMother::book(), 1);

        $this->order->confirm();

        $events = $this->order->releaseEvents();
        self::assertCount(1, $events);
        self::assertInstanceOf(OrderConfirmedEvent::class, $events[0]);
    }
}
```

### Domain Service Tests

```php
#[Group('unit')]
#[CoversClass(TransferMoneyService::class)]
final class TransferMoneyServiceTest extends TestCase
{
    private TransferMoneyService $service;
    private InMemoryAccountRepository $repository;
    private CollectingEventDispatcher $dispatcher;

    protected function setUp(): void
    {
        $this->repository = new InMemoryAccountRepository();
        $this->dispatcher = new CollectingEventDispatcher();
        $this->service = new TransferMoneyService(
            $this->repository,
            $this->dispatcher
        );
    }

    public function test_transfers_money_between_accounts(): void
    {
        // Arrange
        $source = AccountMother::withBalance(Money::EUR(1000));
        $target = AccountMother::withBalance(Money::EUR(500));
        $this->repository->save($source);
        $this->repository->save($target);

        // Act
        $this->service->transfer(
            $source->id(),
            $target->id(),
            Money::EUR(300)
        );

        // Assert
        $updatedSource = $this->repository->findById($source->id());
        $updatedTarget = $this->repository->findById($target->id());
        self::assertEquals(Money::EUR(700), $updatedSource->balance());
        self::assertEquals(Money::EUR(800), $updatedTarget->balance());
    }

    public function test_throws_for_insufficient_funds(): void
    {
        // Arrange
        $source = AccountMother::withBalance(Money::EUR(100));
        $target = AccountMother::withBalance(Money::EUR(500));
        $this->repository->save($source);
        $this->repository->save($target);

        // Assert
        $this->expectException(InsufficientFundsException::class);

        // Act
        $this->service->transfer(
            $source->id(),
            $target->id(),
            Money::EUR(300)
        );
    }
}
```

## Data Providers

```php
use PHPUnit\Framework\Attributes\DataProvider;

#[DataProvider('validEmailsProvider')]
public function test_accepts_valid_formats(string $email): void
{
    $vo = new Email($email);

    self::assertSame($email, $vo->value);
}

public static function validEmailsProvider(): array
{
    return [
        'simple' => ['user@example.com'],
        'with subdomain' => ['user@mail.example.com'],
        'with plus' => ['user+tag@example.com'],
        'with dots' => ['first.last@example.com'],
    ];
}

#[DataProvider('invalidEmailsProvider')]
public function test_rejects_invalid_formats(string $email): void
{
    $this->expectException(InvalidArgumentException::class);

    new Email($email);
}

public static function invalidEmailsProvider(): array
{
    return [
        'empty' => [''],
        'no at' => ['userexample.com'],
        'no domain' => ['user@'],
        'spaces' => ['user @example.com'],
    ];
}
```

## Generation Instructions

1. **Analyze the class:**
   - Identify public methods
   - Identify dependencies (constructor parameters)
   - Identify value objects (final readonly)
   - Identify entities (has id, state changes)
   - Identify services (orchestrates, uses repositories)

2. **Determine test cases:**
   - Happy path for each method
   - Edge cases (null, empty, boundary)
   - Exception paths (validation failures)
   - State transitions (for entities)

3. **Generate test class:**
   - Match namespace: `src/Domain/Order/Order.php` → `tests/Unit/Domain/Order/OrderTest.php`
   - Add attributes: `#[Group('unit')]`, `#[CoversClass]`
   - Create setUp if shared state needed

4. **Generate test methods:**
   - Follow naming convention
   - Use AAA structure
   - One assertion group per test

5. **Add helpers if needed:**
   - Use existing Mothers/Builders
   - Create inline builders for simple cases

## Assertions Reference

```php
// Value comparisons
self::assertSame($expected, $actual);      // ===
self::assertEquals($expected, $actual);    // ==
self::assertTrue($condition);
self::assertFalse($condition);
self::assertNull($value);
self::assertNotNull($value);

// Types
self::assertInstanceOf(ClassName::class, $object);

// Strings
self::assertStringContainsString($needle, $haystack);
self::assertStringStartsWith($prefix, $string);

// Arrays
self::assertCount($expected, $array);
self::assertContains($needle, $array);
self::assertArrayHasKey($key, $array);

// Exceptions
$this->expectException(ExceptionClass::class);
$this->expectExceptionMessage('message');
$this->expectExceptionCode(404);
```

## Usage

Provide:
- Path to class to test
- Or class name and namespace
- Specific methods to focus on (optional)

The generator will:
1. Read the source class
2. Analyze methods and dependencies
3. Generate comprehensive test class
4. Include happy path + edge cases + exceptions
