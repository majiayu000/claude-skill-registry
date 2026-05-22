---
name: acc-cqrs-knowledge
description: CQRS architecture knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Command Query Responsibility Segregation audits.
---

# CQRS Knowledge Base

Quick reference for CQRS architecture patterns and PHP implementation guidelines.

## Core Principles

### Separation of Concerns

```
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION                            │
├─────────────────────────────────────────────────────────────┤
│   WRITE SIDE (Commands)     │     READ SIDE (Queries)       │
├─────────────────────────────┼───────────────────────────────┤
│ Command → Handler → Domain  │  Query → Handler → ReadModel  │
│ Changes state               │  Returns data, no side effects│
│ Uses Domain Model           │  Can bypass Domain Model      │
│ Single aggregate per cmd    │  Can join multiple sources    │
└─────────────────────────────┴───────────────────────────────┘
```

**Rule:** Commands WRITE, Queries READ. Never mix.

### CQRS Components

| Component | Purpose | Returns | Side Effects |
|-----------|---------|---------|--------------|
| **Command** | Request to change state | void or ID | Yes |
| **CommandHandler** | Executes command logic | void or ID | Yes |
| **Query** | Request for data | Data DTO | No |
| **QueryHandler** | Fetches and transforms data | Data DTO | No |
| **CommandBus** | Routes commands to handlers | Depends | N/A |
| **QueryBus** | Routes queries to handlers | Query result | N/A |

## Quick Checklists

### Command Checklist

- [ ] Named as imperative verb + noun (CreateOrder, ConfirmPayment)
- [ ] Immutable (readonly class)
- [ ] Contains only data needed for operation
- [ ] Returns void or created ID (never entities)
- [ ] One command = one aggregate affected
- [ ] Validated before dispatch

### Query Checklist

- [ ] Named as Get/Find/List + noun (GetOrderDetails, ListCustomers)
- [ ] Immutable (readonly class)
- [ ] Contains filtering/pagination params
- [ ] Handler has NO side effects
- [ ] Can use optimized read models
- [ ] Returns DTOs, not entities

### Handler Checklist

- [ ] Single `execute()` or `__invoke()` method
- [ ] One handler per command/query
- [ ] CommandHandler can dispatch domain events
- [ ] QueryHandler never dispatches events
- [ ] No cross-aggregate transactions in single handler

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Query with side effects | QueryHandler calling save() | Critical |
| Command returning data | CommandHandler returning entity | Critical |
| Mixed read/write in handler | Handler with both get and save | Critical |
| Business logic in handler | if/switch on domain state | Warning |
| Missing command validation | Command without invariants | Warning |
| Query using write DB | QueryHandler using EntityManager | Info |

## PHP 8.5 CQRS Patterns

### Command

```php
final readonly class CreateOrderCommand
{
    public function __construct(
        public CustomerId $customerId,
        /** @var array<OrderLineData> */
        public array $lines,
        public ?string $notes = null
    ) {
        if (empty($lines)) {
            throw new InvalidArgumentException('Order must have at least one line');
        }
    }
}
```

### Command Handler

```php
final readonly class CreateOrderHandler
{
    public function __construct(
        private OrderRepositoryInterface $orders,
        private EventDispatcherInterface $events
    ) {}

    public function __invoke(CreateOrderCommand $command): OrderId
    {
        $order = Order::create(
            id: OrderId::generate(),
            customerId: $command->customerId,
            lines: $command->lines
        );

        $this->orders->save($order);

        foreach ($order->releaseEvents() as $event) {
            $this->events->dispatch($event);
        }

        return $order->id();
    }
}
```

### Query

```php
final readonly class GetOrderDetailsQuery
{
    public function __construct(
        public OrderId $orderId
    ) {}
}
```

### Query Handler

```php
final readonly class GetOrderDetailsHandler
{
    public function __construct(
        private OrderReadModelInterface $readModel
    ) {}

    public function __invoke(GetOrderDetailsQuery $query): ?OrderDetailsDTO
    {
        return $this->readModel->findById($query->orderId);
    }
}
```

## References

For detailed information, load these reference files:

- `references/command-patterns.md` — Command structure, naming, validation
- `references/query-patterns.md` — Query structure, read models
- `references/handler-patterns.md` — Handler patterns, async/sync
- `references/bus-patterns.md` — Command/Query bus implementations
- `references/antipatterns.md` — Common violations with detection patterns