---
name: acc-ddd-knowledge
description: DDD architecture knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Domain-Driven Design audits.
---

# DDD Knowledge Base

Quick reference for DDD architecture patterns and PHP implementation guidelines.

## Core Principles

### Layer Dependencies (Clean Architecture)

```
Presentation → Application → Domain ← Infrastructure
                    ↓
              Domain (center)
```

**Rule:** Dependencies point INWARD. Domain has ZERO external dependencies.

### Layer Responsibilities

| Layer | Contains | Depends On |
|-------|----------|------------|
| **Domain** | Entities, Value Objects, Aggregates, Domain Services, Repository Interfaces, Domain Events | Nothing |
| **Application** | Use Cases, DTOs, Application Services | Domain |
| **Infrastructure** | Repository Implementations, External APIs, DB, Cache, Queue | Domain, Application |
| **Presentation** | Controllers, Actions, Request/Response, CLI | Application |

## Quick Checklists

### Domain Layer Checklist

- [ ] No framework imports (Doctrine, Eloquent, Symfony)
- [ ] Entities have behavior, not just data
- [ ] Value Objects for domain concepts (Email, Money, Id)
- [ ] Repository INTERFACES defined here
- [ ] Enums for fixed value sets
- [ ] Domain Events for side effects
- [ ] No `public function set*()` methods

### Application Layer Checklist

- [ ] UseCases orchestrate, don't decide
- [ ] DTOs for input/output
- [ ] No business logic (if/switch on domain state)
- [ ] Transaction boundaries here
- [ ] No HTTP/CLI concerns

### Infrastructure Layer Checklist

- [ ] Implements Domain interfaces
- [ ] No business logic in repositories
- [ ] External service adapters
- [ ] Caching, queuing implementations

### Presentation Layer Checklist

- [ ] Validates input
- [ ] Maps to DTOs
- [ ] Calls UseCase
- [ ] Formats response
- [ ] No business logic

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| `use Doctrine\\` in Domain | Domain/*.php | Critical |
| `use Illuminate\\` in Domain | Domain/*.php | Critical |
| `use Infrastructure\\` in Domain | Domain/*.php | Critical |
| Only getters/setters in Entity | Domain/Entity/*.php | Warning |
| `=== 'pending'` magic strings | Any PHP file | Warning |
| `public function set*()` | Domain/Entity/*.php | Warning |
| Business logic in Controller | Presentation/*.php | Warning |
| Business logic in Repository | Infrastructure/*.php | Warning |

## PHP 8.5 DDD Patterns

### Value Object

```php
final readonly class Email
{
    public function __construct(
        public string $value
    ) {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Invalid email');
        }
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }
}
```

### Entity with Behavior

```php
final class Order
{
    private OrderStatus $status;

    public function __construct(
        private readonly OrderId $id,
        private readonly CustomerId $customerId
    ) {
        $this->status = OrderStatus::Pending;
    }

    public function confirm(): void
    {
        if (!$this->status->canTransitionTo(OrderStatus::Confirmed)) {
            throw new DomainException('Cannot confirm order');
        }
        $this->status = OrderStatus::Confirmed;
    }
}
```

### Repository Interface

```php
// Domain/Repository/OrderRepositoryInterface.php
interface OrderRepositoryInterface
{
    public function findById(OrderId $id): ?Order;
    public function save(Order $order): void;
}
```

## References

For detailed information, load these reference files:

- `references/layer-architecture.md` — Detailed layer rules and boundaries
- `references/domain-patterns.md` — Entity, VO, Aggregate, Repository patterns
- `references/application-patterns.md` — UseCase, DTO, Command/Query patterns
- `references/antipatterns.md` — Common violations with detection patterns
- `references/php-specific.md` — PHP 8.5 specific implementations

## Assets

- `assets/report-template.md` — Structured audit report template