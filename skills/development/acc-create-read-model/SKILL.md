---
name: acc-create-read-model
description: Generates Read Model/Projection for PHP 8.5. Creates optimized query models for CQRS read side with projections and denormalization. Includes unit tests.
---

# Read Model / Projection Generator

Creates Read Model infrastructure for CQRS read side with optimized query models.

## When to Use

| Scenario | Example |
|----------|---------|
| CQRS read side | Separate query models |
| Denormalized views | Dashboard aggregates |
| Complex queries | Multi-entity joins |
| Event-driven updates | Event projections |

## Component Characteristics

### Read Model
- Optimized for queries
- Denormalized data
- Eventually consistent
- No business logic

### Projection
- Builds read models from events
- Handles event streams
- Maintains synchronization
- Idempotent processing

### Repository
- Query-focused methods
- Returns read models
- No write operations

---

## Generation Process

### Step 1: Generate Domain Read Model

**Path:** `src/Domain/{BoundedContext}/ReadModel/`

1. `{Name}ReadModel.php` — Immutable read model with fromArray/toArray
2. `{Name}ReadModelRepositoryInterface.php` — Query-focused repository interface

### Step 2: Generate Application Projection

**Path:** `src/Application/{BoundedContext}/Projection/`

1. `{Name}ProjectionInterface.php` — Projection contract
2. `{Name}Projection.php` — Event handlers building read model

### Step 3: Generate Infrastructure

**Path:** `src/Infrastructure/{BoundedContext}/`

1. `Projection/{Name}Store.php` — Store for insert/update/upsert
2. `ReadModel/Doctrine{Name}Repository.php` — Repository implementation

### Step 4: Generate Tests

1. `{Name}ReadModelTest.php` — Read model serialization tests
2. `{Name}ProjectionTest.php` — Projection event handling tests

---

## File Placement

| Component | Path |
|-----------|------|
| Read Model | `src/Domain/{BoundedContext}/ReadModel/` |
| Repository Interface | `src/Domain/{BoundedContext}/ReadModel/` |
| Projection Interface | `src/Application/{BoundedContext}/Projection/` |
| Projection | `src/Application/{BoundedContext}/Projection/` |
| Store | `src/Infrastructure/{BoundedContext}/Projection/` |
| Repository Impl | `src/Infrastructure/{BoundedContext}/ReadModel/` |
| Unit Tests | `tests/Unit/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Read Model | `{Name}ReadModel` | `OrderSummaryReadModel` |
| Repository Interface | `{Name}ReadModelRepositoryInterface` | `OrderSummaryReadModelRepositoryInterface` |
| Projection Interface | `{Name}ProjectionInterface` | `OrderSummaryProjectionInterface` |
| Projection | `{Name}Projection` | `OrderSummaryProjection` |
| Store | `{Name}Store` | `OrderSummaryStore` |
| Test | `{ClassName}Test` | `OrderSummaryProjectionTest` |

---

## Quick Template Reference

### Read Model

```php
final readonly class {Name}ReadModel
{
    public function __construct(
        public string $id,
        // ... denormalized properties
        public \DateTimeImmutable $createdAt,
        public \DateTimeImmutable $updatedAt
    ) {}

    public static function fromArray(array $data): self;
    public function toArray(): array;
}
```

### Projection

```php
final class {Name}Projection implements {Name}ProjectionInterface
{
    public function project(DomainEventInterface $event): void
    {
        match ($event::class) {
            OrderCreated::class => $this->whenOrderCreated($event),
            OrderShipped::class => $this->whenOrderShipped($event),
            default => null,
        };
    }

    public function reset(): void;
    public function subscribedEvents(): array;
}
```

---

## Usage Example

```php
// Query read model
$orders = $orderSummaryRepository->findByCustomerId($customerId);

// Project event
$projection->project($orderCreatedEvent);

// Reset projection for rebuild
$projection->reset();
```

---

## Database Schema

```sql
CREATE TABLE order_summaries (
    id VARCHAR(36) PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id VARCHAR(36) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    total_cents BIGINT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    INDEX idx_customer (customer_id),
    INDEX idx_status (status)
);
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Business Logic | Read model has behavior | Keep data-only |
| Write Operations | Modifying read models | Use projections only |
| Non-idempotent | Re-projection breaks data | Idempotent event handling |
| Missing Reset | Can't rebuild | Add reset() method |
| Tight Coupling | Projection depends on domain | Use events only |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Read model, projection, store templates
- `references/examples.md` — OrderSummary example and tests
