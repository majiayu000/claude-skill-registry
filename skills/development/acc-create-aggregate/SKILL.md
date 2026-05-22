---
name: acc-create-aggregate
description: Generates DDD Aggregates for PHP 8.5. Creates consistency boundaries with root entity, domain events, and invariant protection. Includes unit tests.
---

# Aggregate Generator

Generate DDD-compliant Aggregates with root, domain events, and tests.

## Aggregate Characteristics

- **Consistency boundary**: All changes atomic
- **Root entity**: Single entry point
- **Transactional consistency**: Invariants always valid
- **Domain events**: Records what happened
- **Encapsulation**: Children accessed through root
- **Identity**: Referenced by root ID

---

## Generation Process

### Step 1: Generate Base AggregateRoot

**Path:** `src/Domain/Shared/Aggregate/`

1. `AggregateRoot.php` — Base class with event recording

### Step 2: Generate Aggregate Root Entity

**Path:** `src/Domain/{BoundedContext}/Entity/`

1. `{Name}.php` — Main aggregate root

### Step 3: Generate Child Entities (if needed)

**Path:** `src/Domain/{BoundedContext}/Entity/`

1. `{ChildName}.php` — Child entity inside aggregate

### Step 4: Generate Domain Events

**Path:** `src/Domain/{BoundedContext}/Event/`

1. `{Name}CreatedEvent.php`
2. `{Name}{Action}Event.php` for each behavior

### Step 5: Generate Tests

**Path:** `tests/Unit/Domain/{BoundedContext}/Entity/`

---

## File Placement

| Component | Path |
|-----------|------|
| Base AggregateRoot | `src/Domain/Shared/Aggregate/` |
| Aggregate Entity | `src/Domain/{BoundedContext}/Entity/` |
| Child Entities | `src/Domain/{BoundedContext}/Entity/` |
| Domain Events | `src/Domain/{BoundedContext}/Event/` |
| Unit Tests | `tests/Unit/Domain/{BoundedContext}/Entity/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Aggregate Root | `{Name}` | `Order` |
| Child Entity | `{Parent}{Name}` | `OrderLine` |
| Created Event | `{Name}CreatedEvent` | `OrderCreatedEvent` |
| State Event | `{Name}{Action}Event` | `OrderConfirmedEvent` |

---

## Quick Template Reference

### Base AggregateRoot

```php
abstract class AggregateRoot
{
    private array $events = [];

    protected function recordEvent(DomainEvent $event): void
    {
        $this->events[] = $event;
    }

    public function releaseEvents(): array
    {
        $events = $this->events;
        $this->events = [];
        return $events;
    }
}
```

### Aggregate Root Entity

```php
final class {Name} extends AggregateRoot
{
    private {Name}Status $status;

    private function __construct(
        private readonly {Name}Id $id,
        {properties}
    ) {
        $this->status = {Name}Status::Draft;
    }

    public static function create({Name}Id $id, {params}): self
    {
        $aggregate = new self($id, {args});

        $aggregate->recordEvent(new {Name}CreatedEvent(...));

        return $aggregate;
    }

    public function {behavior}({params}): void
    {
        $this->ensureValidState();
        // Apply change
        $this->recordEvent(new {Name}{Behavior}Event(...));
    }
}
```

### Child Entity

```php
final readonly class {ChildName}
{
    public function __construct(
        public {PropertyType} $property1,
        public {PropertyType} $property2
    ) {}

    public function total(): Money
    {
        return $this->unitPrice->multiply($this->quantity);
    }
}
```

---

## Design Rules

| Rule | Good | Bad |
|------|------|-----|
| Transaction Boundary | One aggregate per transaction | Multiple aggregates |
| Reference | By ID only | Full entity reference |
| Size | Small, focused | Large with many collections |
| Invariants | Always valid | Can be in invalid state |
| Events | Record all state changes | No event recording |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Large Aggregate | Performance issues | Split into smaller aggregates |
| Entity References | Tight coupling | Use IDs only |
| Public Setters | No invariant protection | Use behavior methods |
| Missing Events | Can't track history | Record event for each change |
| No Root | Multiple entry points | Single root entity |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — AggregateRoot, Entity, Child Entity, Test templates
- `references/examples.md` — Order aggregate with OrderLine, events, and tests
