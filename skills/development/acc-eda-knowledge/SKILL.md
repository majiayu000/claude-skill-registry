---
name: acc-eda-knowledge
description: Event-Driven Architecture knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for EDA audits including messaging, pub/sub, and saga patterns.
---

# Event-Driven Architecture Knowledge Base

Quick reference for Event-Driven Architecture (EDA) patterns and PHP implementation guidelines.

## Core Principles

### Event-Driven Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     EVENT-DRIVEN ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────┐     ┌──────────────────┐     ┌──────────────────┐        │
│   │ Producer │────▶│  Message Broker  │────▶│    Consumer      │        │
│   │          │     │  (RabbitMQ/Kafka)│     │                  │        │
│   └──────────┘     └──────────────────┘     └──────────────────┘        │
│        │                    │                       │                    │
│        │                    │                       │                    │
│   Publishes            Routes/Stores            Subscribes               │
│   Events               Messages                 to Events                │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Event Types:                                                           │
│   • Domain Events    - Business facts (OrderPlaced, PaymentReceived)     │
│   • Integration Events - Cross-boundary communication                    │
│   • System Events    - Infrastructure notifications                      │
│                                                                          │
│   Patterns:                                                              │
│   • Pub/Sub          - Many subscribers per event                        │
│   • Message Queue    - One consumer per message                          │
│   • Event Sourcing   - Store all events as source of truth              │
│   • Saga/Process Manager - Coordinate distributed transactions          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| Event | Immutable fact that something happened |
| Producer | Publishes events to broker |
| Consumer | Subscribes to and processes events |
| Message Broker | Routes events between producers and consumers |
| Topic/Exchange | Event routing mechanism |
| Queue | Stores messages for consumers |
| Eventual Consistency | System state converges over time |

## Quick Checklists

### Event Design Checklist

- [ ] Events are immutable
- [ ] Events use past tense (OrderPlaced, not PlaceOrder)
- [ ] Events contain necessary data (no fetching needed)
- [ ] Events have unique IDs and timestamps
- [ ] Events include correlation/causation IDs
- [ ] Events are versioned for schema evolution

### Producer Checklist

- [ ] Publishes events after state change
- [ ] Uses transactional outbox for reliability
- [ ] Events are serializable (JSON/Protobuf)
- [ ] Handles publish failures gracefully
- [ ] No business logic dependent on consumers

### Consumer Checklist

- [ ] Idempotent processing
- [ ] Handles out-of-order events
- [ ] Implements retry with backoff
- [ ] Dead letter queue for failures
- [ ] No side effects until processing complete

## PHP 8.5 Event-Driven Patterns

### Domain Event

```php
<?php

declare(strict_types=1);

namespace Domain\Order\Event;

use Domain\Shared\Event\DomainEvent;

final readonly class OrderPlaced implements DomainEvent
{
    public function __construct(
        public string $eventId,
        public string $orderId,
        public string $customerId,
        public int $totalCents,
        public \DateTimeImmutable $occurredAt,
        public ?string $correlationId = null,
        public ?string $causationId = null
    ) {}

    public function eventName(): string
    {
        return 'order.placed';
    }

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function toArray(): array
    {
        return [
            'event_id' => $this->eventId,
            'order_id' => $this->orderId,
            'customer_id' => $this->customerId,
            'total_cents' => $this->totalCents,
            'occurred_at' => $this->occurredAt->format('c'),
            'correlation_id' => $this->correlationId,
            'causation_id' => $this->causationId,
        ];
    }
}
```

### Event Publisher Interface

```php
<?php

declare(strict_types=1);

namespace Application\Shared\Port\Output;

use Domain\Shared\Event\DomainEvent;

interface EventPublisherInterface
{
    public function publish(DomainEvent $event): void;

    /** @param array<DomainEvent> $events */
    public function publishAll(array $events): void;
}
```

### Event Consumer/Handler

```php
<?php

declare(strict_types=1);

namespace Application\Order\EventHandler;

use Application\Shared\Port\Output\EventHandlerInterface;
use Domain\Order\Event\OrderPlaced;

final readonly class SendOrderConfirmationEmail implements EventHandlerInterface
{
    public function __construct(
        private EmailServiceInterface $emailService,
        private CustomerRepositoryInterface $customers
    ) {}

    public function __invoke(OrderPlaced $event): void
    {
        $customer = $this->customers->findById($event->customerId);

        $this->emailService->send(
            to: $customer->email(),
            template: 'order-confirmation',
            data: [
                'order_id' => $event->orderId,
                'total' => $event->totalCents / 100,
            ]
        );
    }

    public static function subscribedTo(): string
    {
        return OrderPlaced::class;
    }
}
```

### RabbitMQ Publisher (Infrastructure)

```php
<?php

declare(strict_types=1);

namespace Infrastructure\Messaging\RabbitMQ;

use Application\Shared\Port\Output\EventPublisherInterface;
use Domain\Shared\Event\DomainEvent;
use PhpAmqpLib\Channel\AMQPChannel;
use PhpAmqpLib\Message\AMQPMessage;

final readonly class RabbitMQEventPublisher implements EventPublisherInterface
{
    public function __construct(
        private AMQPChannel $channel,
        private string $exchangeName
    ) {}

    public function publish(DomainEvent $event): void
    {
        $message = new AMQPMessage(
            json_encode($event->toArray()),
            [
                'content_type' => 'application/json',
                'delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT,
                'message_id' => $event->eventId,
                'timestamp' => $event->occurredAt->getTimestamp(),
            ]
        );

        $this->channel->basic_publish(
            $message,
            $this->exchangeName,
            $event->eventName()
        );
    }

    public function publishAll(array $events): void
    {
        foreach ($events as $event) {
            $this->publish($event);
        }
    }
}
```

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Synchronous calls disguised as events | Consumer calls HTTP API | Critical |
| Missing idempotency | No deduplication check | Critical |
| Tight coupling via events | Event contains entity references | Warning |
| Fire and forget | No error handling on publish | Warning |
| Blocking consumer | Slow processing without async | Warning |

## Detection Patterns

```bash
# Find event classes
Glob: **/Event/**/*Event.php
Glob: **/Events/**/*.php

# Check for event publishers
Grep: "EventPublisher|EventDispatcher|publish\(" --glob "**/*.php"

# Find event handlers/consumers
Grep: "implements.*EventHandler|implements.*Consumer" --glob "**/*.php"

# Check for message broker usage
Grep: "AMQPChannel|RabbitMQ|Kafka" --glob "**/Infrastructure/**/*.php"

# Find potential issues
Grep: "new.*Event\(" --glob "**/Controller/**/*.php"  # Events in controllers
Grep: "->findById|->save" --glob "**/EventHandler/**/*.php"  # Sync calls in handlers
```

## References

For detailed information, load these reference files:

- `references/event-patterns.md` — Event types, structure, publishing patterns
- `references/messaging-patterns.md` — Message broker patterns, queues, topics
- `references/saga-patterns.md` — Distributed transactions, choreography, orchestration
- `references/antipatterns.md` — Common violations with detection patterns
