---
name: acc-event-sourcing-knowledge
description: Event Sourcing knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Event Sourcing architecture audits.
---

# Event Sourcing Knowledge Base

Quick reference for Event Sourcing architecture patterns and PHP implementation guidelines.

## Core Principles

### Event Sourcing Fundamentals

```
Traditional Storage:          Event Sourcing:
┌─────────────────┐           ┌─────────────────┐
│  Current State  │           │  Event Stream   │
│  ─────────────  │           │  ─────────────  │
│  Order #123     │           │  1. OrderCreated│
│  Status: Paid   │           │  2. ItemAdded   │
│  Total: $150    │           │  3. ItemAdded   │
└─────────────────┘           │  4. OrderPaid   │
       ↓                      └────────┬────────┘
  Direct update                        │
                                       ▼
                              ┌─────────────────┐
                              │  Current State  │
                              │  (Rebuilt from  │
                              │   events)       │
                              └─────────────────┘
```

**Rule:** Store events, derive state. Never modify events.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Event** | Immutable record of something that happened |
| **Event Store** | Append-only storage for events |
| **Event Stream** | Ordered sequence of events for one aggregate |
| **Aggregate** | Consistency boundary, rebuilt from events |
| **Projection** | Read model built by processing events |
| **Snapshot** | Cached aggregate state for performance |

## Quick Checklists

### Event Checklist

- [ ] Named in past tense (OrderCreated, ItemAdded)
- [ ] Immutable (readonly class)
- [ ] Contains all data needed to apply change
- [ ] Has metadata (timestamp, causation, correlation IDs)
- [ ] No business logic
- [ ] Versioned for schema evolution

### Aggregate Checklist

- [ ] State rebuilt from events only
- [ ] apply*() methods modify state from events
- [ ] record*() methods create and apply events
- [ ] No direct state modification
- [ ] Returns uncommitted events for persistence

### Event Store Checklist

- [ ] Append-only (no updates, no deletes)
- [ ] Ordered within stream
- [ ] Supports optimistic concurrency
- [ ] Events never modified
- [ ] Stream position tracking

### Projection Checklist

- [ ] Idempotent event handlers
- [ ] Can be rebuilt from scratch
- [ ] Handles event ordering
- [ ] Tracks processed position

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Mutable event | Event with setters | Critical |
| Direct state mutation | Aggregate bypassing events | Critical |
| Missing event data | Event without full state info | Critical |
| Event with logic | Event doing calculations | Warning |
| Non-idempotent projection | Projection with side effects | Warning |
| Missing metadata | Event without timestamp/IDs | Warning |

## PHP 8.5 Event Sourcing Patterns

### Domain Event

```php
final readonly class OrderConfirmedEvent
{
    public function __construct(
        public string $orderId,
        public int $totalCents,
        public string $currency,
        public DateTimeImmutable $confirmedAt,
        public EventMetadata $metadata
    ) {}
}

final readonly class EventMetadata
{
    public function __construct(
        public string $eventId,
        public DateTimeImmutable $occurredAt,
        public ?string $causationId = null,
        public ?string $correlationId = null,
        public int $version = 1
    ) {}
}
```

### Event-Sourced Aggregate

```php
final class Order extends EventSourcedAggregate
{
    private OrderStatus $status;
    private Money $total;

    public static function create(OrderId $id, CustomerId $customerId): self
    {
        $order = new self($id);
        $order->recordThat(new OrderCreatedEvent(
            orderId: $id->value,
            customerId: $customerId->value,
            createdAt: new DateTimeImmutable()
        ));
        return $order;
    }

    public function confirm(): void
    {
        if ($this->status !== OrderStatus::Draft) {
            throw new InvalidStateException();
        }
        $this->recordThat(new OrderConfirmedEvent(
            orderId: $this->id->value,
            totalCents: $this->total->cents(),
            currency: $this->total->currency(),
            confirmedAt: new DateTimeImmutable()
        ));
    }

    protected function applyOrderCreatedEvent(OrderCreatedEvent $event): void
    {
        $this->status = OrderStatus::Draft;
        $this->total = Money::zero('USD');
    }

    protected function applyOrderConfirmedEvent(OrderConfirmedEvent $event): void
    {
        $this->status = OrderStatus::Confirmed;
    }
}
```

### Projection

```php
final class OrderListProjection
{
    public function __construct(
        private Connection $connection
    ) {}

    public function applyOrderCreatedEvent(OrderCreatedEvent $event): void
    {
        $this->connection->insert('order_list', [
            'id' => $event->orderId,
            'customer_id' => $event->customerId,
            'status' => 'draft',
            'created_at' => $event->createdAt->format('Y-m-d H:i:s'),
        ]);
    }

    public function applyOrderConfirmedEvent(OrderConfirmedEvent $event): void
    {
        $this->connection->update('order_list', [
            'status' => 'confirmed',
            'total_cents' => $event->totalCents,
            'confirmed_at' => $event->confirmedAt->format('Y-m-d H:i:s'),
        ], ['id' => $event->orderId]);
    }
}
```

## References

For detailed information, load these reference files:

- `references/event-store-patterns.md` — Event persistence, streams, concurrency
- `references/projection-patterns.md` — Read model projections
- `references/snapshot-patterns.md` — Performance optimization with snapshots
- `references/versioning-patterns.md` — Event schema evolution
- `references/antipatterns.md` — Common violations with detection patterns
