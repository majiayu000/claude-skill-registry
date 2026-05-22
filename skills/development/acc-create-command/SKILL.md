---
name: acc-create-command
description: Generates CQRS Commands and Handlers for PHP 8.5. Creates immutable command DTOs with handlers that modify state. Includes unit tests.
---

# Command Generator

Generate CQRS-compliant Commands and Command Handlers with tests.

## Command Characteristics

- **Immutable**: `final readonly class`
- **Imperative naming**: Verb + noun (CreateOrder, ConfirmPayment)
- **Self-validating**: Validates invariants in constructor
- **Intent-revealing**: Name describes what should happen
- **Returns void or ID**: Never returns data

---

## Generation Process

### Step 1: Generate Command

**Path:** `src/Application/{BoundedContext}/Command/`

1. `{Name}Command.php` — Immutable command DTO

### Step 2: Generate Handler

**Path:** `src/Application/{BoundedContext}/Handler/`

1. `{Name}Handler.php` — Command processor

### Step 3: Generate Tests

**Path:** `tests/Unit/Application/{BoundedContext}/`

---

## File Placement

| Component | Path |
|-----------|------|
| Command | `src/Application/{BoundedContext}/Command/` |
| Handler | `src/Application/{BoundedContext}/Handler/` |
| Unit Tests | `tests/Unit/Application/{BoundedContext}/` |

---

## Command Naming Conventions

| Action | Command Name | Returns |
|--------|--------------|---------|
| Create new | `CreateOrderCommand` | ID |
| Confirm/Approve | `ConfirmOrderCommand` | void |
| Cancel/Reject | `CancelOrderCommand` | void |
| Update property | `UpdateShippingAddressCommand` | void |
| Add child | `AddOrderLineCommand` | void |
| Remove child | `RemoveOrderLineCommand` | void |

---

## Quick Template Reference

### Command

```php
final readonly class {Name}Command
{
    public function __construct(
        public {ValueObject} $id,
        public string $data
    ) {
        if (empty($data)) {
            throw new \InvalidArgumentException('Data is required');
        }
    }

    public static function fromArray(array $data): self
    {
        return new self(
            id: new {ValueObject}($data['id']),
            data: $data['data']
        );
    }
}
```

### Handler (Update Flow)

```php
final readonly class {Name}Handler
{
    public function __construct(
        private {Repository}Interface $repository,
        private EventDispatcherInterface $events
    ) {}

    public function __invoke({Name}Command $command): void
    {
        $aggregate = $this->repository->findById($command->id);

        if ($aggregate === null) {
            throw new NotFoundException($command->id);
        }

        $aggregate->doSomething($command->data);

        $this->repository->save($aggregate);

        foreach ($aggregate->releaseEvents() as $event) {
            $this->events->dispatch($event);
        }
    }
}
```

### Handler (Create Flow)

```php
public function __invoke(CreateCommand $command): AggregateId
{
    $aggregate = Aggregate::create(
        id: $this->repository->nextIdentity(),
        ...
    );

    $this->repository->save($aggregate);

    foreach ($aggregate->releaseEvents() as $event) {
        $this->events->dispatch($event);
    }

    return $aggregate->id();
}
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Returning Data | Query through command | Use Query for reads |
| No Validation | Invalid commands | Validate in constructor |
| Business Logic | Handler has decisions | Delegate to aggregate |
| Missing Events | Events not dispatched | Always dispatch after save |
| Direct Persistence | Bypassing aggregate | Always use aggregate methods |

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Command, Handler, Test templates with patterns
- `references/examples.md` — CreateOrder, ConfirmOrder, CancelOrder examples and tests
