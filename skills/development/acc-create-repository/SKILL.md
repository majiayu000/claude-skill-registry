---
name: acc-create-repository
description: Generates DDD Repository interfaces and implementation stubs for PHP 8.5. Creates domain interfaces in Domain layer, implementation in Infrastructure.
---

# Repository Generator

Generate DDD-compliant Repository interfaces and implementation stubs.

## Repository Characteristics

- **Interface in Domain**: Contract defined in Domain layer
- **Implementation in Infrastructure**: Doctrine/Eloquent/etc. implementation
- **Works with Aggregates**: Not entities directly
- **Collection-like**: Find, save, remove operations
- **No business logic**: Only persistence operations

---

## Generation Process

### Step 1: Generate Interface

**Path:** `src/Domain/{BoundedContext}/Repository/`

1. `{AggregateRoot}RepositoryInterface.php` — Domain contract

### Step 2: Generate Implementation

**Path:** `src/Infrastructure/Persistence/Doctrine/`

1. `Doctrine{AggregateRoot}Repository.php` — Doctrine implementation

### Step 3: Generate In-Memory Repository (Optional)

**Path:** `tests/Infrastructure/Persistence/`

1. `InMemory{AggregateRoot}Repository.php` — For unit testing

### Step 4: Generate Integration Tests

**Path:** `tests/Integration/Infrastructure/Persistence/`

---

## File Placement

| Component | Path |
|-----------|------|
| Interface | `src/Domain/{BoundedContext}/Repository/` |
| Doctrine Impl | `src/Infrastructure/Persistence/Doctrine/` |
| In-Memory | `tests/Infrastructure/Persistence/` |
| Integration Tests | `tests/Integration/Infrastructure/Persistence/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Interface | `{AggregateRoot}RepositoryInterface` | `OrderRepositoryInterface` |
| Doctrine Impl | `Doctrine{AggregateRoot}Repository` | `DoctrineOrderRepository` |
| In-Memory | `InMemory{AggregateRoot}Repository` | `InMemoryOrderRepository` |

---

## Quick Template Reference

### Interface

```php
interface {AggregateRoot}RepositoryInterface
{
    public function findById({AggregateRoot}Id $id): ?{AggregateRoot};

    public function save({AggregateRoot} $aggregate): void;

    public function remove({AggregateRoot} $aggregate): void;

    public function nextIdentity(): {AggregateRoot}Id;
}
```

### Doctrine Implementation

```php
final readonly class Doctrine{AggregateRoot}Repository implements {AggregateRoot}RepositoryInterface
{
    public function __construct(
        private EntityManagerInterface $em
    ) {}

    public function findById({AggregateRoot}Id $id): ?{AggregateRoot}
    {
        return $this->em->find({AggregateRoot}::class, $id->value);
    }

    public function save({AggregateRoot} $aggregate): void
    {
        $this->em->persist($aggregate);
        $this->em->flush();
    }

    public function remove({AggregateRoot} $aggregate): void
    {
        $this->em->remove($aggregate);
        $this->em->flush();
    }

    public function nextIdentity(): {AggregateRoot}Id
    {
        return {AggregateRoot}Id::generate();
    }
}
```

### In-Memory Implementation

```php
final class InMemory{AggregateRoot}Repository implements {AggregateRoot}RepositoryInterface
{
    private array $items = [];

    public function findById({AggregateRoot}Id $id): ?{AggregateRoot}
    {
        return $this->items[$id->value] ?? null;
    }

    public function save({AggregateRoot} $aggregate): void
    {
        $this->items[$aggregate->id()->value] = $aggregate;
    }

    public function clear(): void
    {
        $this->items = [];
    }
}
```

---

## Design Rules

| Rule | Good | Bad |
|------|------|-----|
| Layer Placement | Interface in Domain | Interface in Infrastructure |
| Aggregate Scope | Repository per aggregate root | Repository per entity |
| Query Methods | Simple filters | Business logic in queries |
| Identity | `nextIdentity()` method | External ID generation |

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Entity Repository | Bypasses aggregate | Only aggregate roots |
| Business Queries | Logic in repository | Use Specification pattern |
| Infrastructure Leak | Domain depends on ORM | Interface in Domain |
| Generic Repository | Too abstract | Specific per aggregate |
| Missing nextIdentity | Can't generate IDs | Add to interface |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Interface, Doctrine, In-Memory, Test templates
- `references/examples.md` — Order, User repositories with Doctrine and In-Memory implementations
