---
name: acc-testing-knowledge
description: Testing knowledge base for PHP 8.5 projects. Provides testing pyramid, AAA pattern, naming conventions, isolation principles, DDD testing guidelines, and PHPUnit patterns.
---

# Testing Knowledge Base

Quick reference for PHP testing patterns, principles, and best practices.

## Testing Pyramid

```
        /\
       /  \     Functional (10%)
      /────\    - E2E, browser tests
     /      \   - Slow, fragile
    /────────\  Integration (20%)
   /          \ - DB, HTTP, queues
  /────────────\Unit (70%)
 /              \- Fast, isolated
/________________\- Business logic
```

**Rule:** 70% unit, 20% integration, 10% functional. Invert the pyramid = slow, brittle test suite.

## AAA Pattern (Arrange-Act-Assert)

```php
public function test_order_calculates_total_with_discount(): void
{
    // Arrange — set up test data
    $order = new Order(OrderId::generate());
    $order->addItem(new Product('Book', Money::EUR(100)));
    $discount = new PercentageDiscount(10);

    // Act — execute the behavior
    $total = $order->calculateTotal($discount);

    // Assert — verify the outcome
    self::assertEquals(Money::EUR(90), $total);
}
```

**Rules:**
- One blank line between sections
- Single Act per test
- Assert behavior, not implementation

## Naming Conventions

### PHPUnit Style

```
test_{method}_{scenario}_{expected}
```

| Example | Method | Scenario | Expected |
|---------|--------|----------|----------|
| `test_calculate_total_with_discount_returns_reduced_amount` | calculateTotal | with discount | returns reduced amount |
| `test_confirm_when_already_shipped_throws_exception` | confirm | when already shipped | throws exception |
| `test_email_with_invalid_format_fails_validation` | Email (VO) | with invalid format | fails validation |

### Pest Style

```php
it('calculates total with discount applied')
it('throws exception when confirming shipped order')
it('fails validation for invalid email format')
```

## Test Isolation Principles

### DO

- [ ] Fresh fixtures per test
- [ ] Independent test execution (any order)
- [ ] Teardown cleans all state
- [ ] Use in-memory implementations

### DON'T

- [ ] Shared mutable state between tests
- [ ] Tests depending on execution order
- [ ] Global variables or singletons
- [ ] Real external services in unit tests

## Quick Quality Checklist

| Rule | Check |
|------|-------|
| One test = one behavior | Single assertion group |
| Test is documentation | Name reads as specification |
| No logic in tests | No if/for/while |
| Fast execution | <100ms per unit test |
| Mock interfaces only | Never mock VO, Entity, final |
| ≤3 mocks per test | More = design smell |
| Behavior over implementation | Test WHAT, not HOW |

## DDD Component Testing

| Component | Test Focus | Mocks Allowed |
|-----------|------------|---------------|
| **Value Object** | Validation, equality, immutability | None |
| **Entity** | State transitions, business rules | None |
| **Aggregate** | Invariants, consistency, events | None |
| **Domain Service** | Business logic spanning aggregates | Repository (Fake) |
| **Application Service** | Orchestration, transactions | Repository, EventDispatcher |
| **Repository** | CRUD operations | Database (SQLite) |

## PHP 8.5 Test Patterns

### Unit Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Domain;

use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass(Email::class)]
final class EmailTest extends TestCase
{
    public function test_creates_valid_email(): void
    {
        $email = new Email('user@example.com');

        self::assertSame('user@example.com', $email->value);
    }

    public function test_throws_for_invalid_format(): void
    {
        $this->expectException(InvalidArgumentException::class);

        new Email('invalid');
    }
}
```

### Integration Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Integration\Infrastructure;

use PHPUnit\Framework\Attributes\Group;
use Tests\DatabaseTestCase;

#[Group('integration')]
final class DoctrineOrderRepositoryTest extends DatabaseTestCase
{
    private OrderRepositoryInterface $repository;

    protected function setUp(): void
    {
        parent::setUp();
        $this->repository = $this->getContainer()->get(OrderRepositoryInterface::class);
    }

    public function test_saves_and_retrieves_order(): void
    {
        // Arrange
        $order = OrderMother::pending();

        // Act
        $this->repository->save($order);
        $found = $this->repository->findById($order->id());

        // Assert
        self::assertNotNull($found);
        self::assertTrue($order->id()->equals($found->id()));
    }
}
```

## Test Doubles Quick Reference

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Stub** | Returns canned answers | External API responses |
| **Mock** | Verifies interactions | Event publishing |
| **Fake** | Working implementation | InMemory repository |
| **Spy** | Records calls | Logging, notifications |

### Decision Matrix

```
Need to verify a call was made?
├── Yes → Mock or Spy
└── No → Need real behavior?
    ├── Yes → Fake
    └── No → Stub
```

## Common Test Smells

| Smell | Detection | Fix |
|-------|-----------|-----|
| Logic in Test | `if`, `for`, `while` in test | Extract to helper or parameterize |
| Mock Overuse | >3 mocks | Refactor design, use Fakes |
| Mystery Guest | External files, hidden data | Inline test data or use Builder |
| Eager Test | Tests multiple behaviors | Split into separate tests |
| Fragile Test | Breaks on refactor | Test behavior, not implementation |

## References

For detailed information, load these reference files:

- `references/unit-testing.md` — Unit test patterns and examples
- `references/integration-testing.md` — Integration test setup and patterns
- `references/ddd-testing.md` — Testing DDD components (VO, Entity, Aggregate, Service)
