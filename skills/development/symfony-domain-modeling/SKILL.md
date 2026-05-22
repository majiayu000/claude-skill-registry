---
description: "Symfony domain modeling — entities, value objects, domain events, aggregates, domain exceptions. Triggers on: entity, value object, domain event, aggregate, domain exception, domain model, domain logic, business rule, invariant"
---

# Symfony Domain Modeling

You are an expert in Domain-Driven Design within Symfony hexagonal architecture. Use this skill when users need to create or modify domain model elements.

## When to Activate

- User wants to create an entity or aggregate root
- User asks about value objects
- User needs domain events
- User mentions domain exceptions or business rules
- User discusses aggregates or invariants

## Entity Patterns

### Rules
- Private constructor + static factory method(s)
- No Doctrine annotations/attributes — mapping is in Infrastructure
- Record domain events on state changes
- Protect invariants in methods, not in external validators
- Use value objects for typed properties (no primitive obsession)

### Template
```php
namespace App\Domain\{Module}\Entity;

final class {Entity}
{
    private array $domainEvents = [];

    private function __construct(
        private {EntityId} $id,
        // typed properties using value objects
    ) {
    }

    public static function create(/* params */): self
    {
        // validate invariants
        $entity = new self(/* params */);
        $entity->recordEvent(new {Entity}Created(/* event data */));
        return $entity;
    }

    // Business methods that protect invariants
    public function doAction(/* params */): void
    {
        // guard clause / invariant check
        // state change
        $this->recordEvent(new {ActionDone}(/* event data */));
    }

    public function pullDomainEvents(): array
    {
        $events = $this->domainEvents;
        $this->domainEvents = [];
        return $events;
    }

    private function recordEvent(object $event): void
    {
        $this->domainEvents[] = $event;
    }
}
```

## Value Object Patterns

### Rules
- Always `final readonly class`
- Self-validating in constructor (throw domain exception if invalid)
- Immutable — no setters
- Implement `equals()` for comparison
- Use for: IDs, email, money, dates, status enums

### Template
```php
namespace App\Domain\{Module}\ValueObject;

use App\Domain\{Module}\Exception\Invalid{ValueObject}Exception;

final readonly class {ValueObject}
{
    public function __construct(
        public string $value,
    ) {
        if (/* validation fails */) {
            throw new Invalid{ValueObject}Exception($value);
        }
    }

    public function equals(self $other): bool
    {
        return $this->value === $other->value;
    }

    public function __toString(): string
    {
        return $this->value;
    }
}
```

## Domain Event Patterns

### Rules
- Past-tense naming: `UserRegistered`, `OrderPlaced`, `PaymentFailed`
- Immutable (`final readonly class`)
- Carry only the data needed by handlers (IDs, not full entities)
- Created inside entities on state changes

### Template
```php
namespace App\Domain\{Module}\Event;

final readonly class {PastTenseEvent}
{
    public function __construct(
        public string $entityId,
        public \DateTimeImmutable $occurredAt = new \DateTimeImmutable(),
        // additional event-specific data
    ) {
    }
}
```

## Domain Exception Patterns

```php
namespace App\Domain\{Module}\Exception;

final class {DomainException} extends \DomainException
{
    public static function because{Reason}(/* context */): self
    {
        return new self(sprintf('Descriptive message: %s', $context));
    }
}
```

## References

See `references/` for detailed patterns:
- `entity-patterns.md` — Full entity examples with aggregates
- `value-object-patterns.md` — Common value object implementations
- `domain-event-patterns.md` — Event design and dispatch patterns
