---
name: acc-create-domain-event
description: Generates DDD Domain Events for PHP 8.5. Creates immutable event records with metadata, past-tense naming. Includes unit tests.
---

# Domain Event Generator

Generate DDD-compliant Domain Events with metadata and tests.

## Domain Event Characteristics

- **Immutable**: `final readonly class`
- **Past tense**: Describes something that happened
- **Self-contained**: All data needed to understand what happened
- **Metadata**: Event ID, timestamp, causation/correlation IDs
- **No behavior**: Pure data, no logic

## Template

```php
<?php

declare(strict_types=1);

namespace Domain\{BoundedContext}\Event;

use Domain\Shared\Event\DomainEvent;

final readonly class {Name}Event implements DomainEvent
{
    public function __construct(
        {properties}
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->{aggregateIdProperty};
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}
```

## Event Metadata

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Event;

final readonly class EventMetadata
{
    public function __construct(
        public string $eventId,
        public DateTimeImmutable $occurredAt,
        public ?string $causationId = null,
        public ?string $correlationId = null,
        public int $version = 1,
        public ?string $userId = null
    ) {}

    public static function create(): self
    {
        return new self(
            eventId: self::generateId(),
            occurredAt: new DateTimeImmutable()
        );
    }

    public static function withCausation(string $causationId, ?string $correlationId = null): self
    {
        return new self(
            eventId: self::generateId(),
            occurredAt: new DateTimeImmutable(),
            causationId: $causationId,
            correlationId: $correlationId ?? $causationId
        );
    }

    private static function generateId(): string
    {
        $data = random_bytes(16);
        $data[6] = chr(ord($data[6]) & 0x0f | 0x40);
        $data[8] = chr(ord($data[8]) & 0x3f | 0x80);
        return vsprintf('%s%s-%s-%s-%s-%s%s%s', str_split(bin2hex($data), 4));
    }
}
```

## Domain Event Interface

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Event;

interface DomainEvent
{
    public function aggregateId(): string;

    public function occurredAt(): DateTimeImmutable;
}
```

## Common Domain Events

### Order Events

```php
<?php

declare(strict_types=1);

namespace Domain\Order\Event;

use Domain\Shared\Event\DomainEvent;
use Domain\Shared\Event\EventMetadata;

final readonly class OrderCreatedEvent implements DomainEvent
{
    public function __construct(
        public string $orderId,
        public string $customerId,
        public DateTimeImmutable $createdAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class OrderLineAddedEvent implements DomainEvent
{
    public function __construct(
        public string $orderId,
        public string $productId,
        public string $productName,
        public int $quantity,
        public int $unitPriceCents,
        public string $currency,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class OrderConfirmedEvent implements DomainEvent
{
    public function __construct(
        public string $orderId,
        public int $totalCents,
        public string $currency,
        public DateTimeImmutable $confirmedAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class OrderCancelledEvent implements DomainEvent
{
    public function __construct(
        public string $orderId,
        public string $reason,
        public DateTimeImmutable $cancelledAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class OrderShippedEvent implements DomainEvent
{
    public function __construct(
        public string $orderId,
        public string $trackingNumber,
        public string $carrier,
        public DateTimeImmutable $shippedAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->orderId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}
```

### User Events

```php
<?php

declare(strict_types=1);

namespace Domain\User\Event;

final readonly class UserRegisteredEvent implements DomainEvent
{
    public function __construct(
        public string $userId,
        public string $email,
        public string $name,
        public DateTimeImmutable $registeredAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->userId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class UserEmailChangedEvent implements DomainEvent
{
    public function __construct(
        public string $userId,
        public string $previousEmail,
        public string $newEmail,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->userId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}

final readonly class UserDeactivatedEvent implements DomainEvent
{
    public function __construct(
        public string $userId,
        public string $reason,
        public DateTimeImmutable $deactivatedAt,
        public EventMetadata $metadata
    ) {}

    public function aggregateId(): string
    {
        return $this->userId;
    }

    public function occurredAt(): DateTimeImmutable
    {
        return $this->metadata->occurredAt;
    }
}
```

## Test Template

```php
<?php

declare(strict_types=1);

namespace Tests\Unit\Domain\Order\Event;

use Domain\Order\Event\OrderCreatedEvent;
use Domain\Shared\Event\EventMetadata;
use PHPUnit\Framework\Attributes\CoversClass;
use PHPUnit\Framework\Attributes\Group;
use PHPUnit\Framework\TestCase;

#[Group('unit')]
#[CoversClass(OrderCreatedEvent::class)]
final class OrderCreatedEventTest extends TestCase
{
    public function testCreatesEventWithAllData(): void
    {
        $metadata = EventMetadata::create();
        $createdAt = new DateTimeImmutable();

        $event = new OrderCreatedEvent(
            orderId: 'order-123',
            customerId: 'customer-456',
            createdAt: $createdAt,
            metadata: $metadata
        );

        self::assertSame('order-123', $event->orderId);
        self::assertSame('customer-456', $event->customerId);
        self::assertSame($createdAt, $event->createdAt);
        self::assertSame($metadata, $event->metadata);
    }

    public function testReturnsAggregateId(): void
    {
        $event = $this->createEvent();

        self::assertSame('order-123', $event->aggregateId());
    }

    public function testReturnsOccurredAt(): void
    {
        $metadata = EventMetadata::create();
        $event = new OrderCreatedEvent(
            orderId: 'order-123',
            customerId: 'customer-456',
            createdAt: new DateTimeImmutable(),
            metadata: $metadata
        );

        self::assertEquals($metadata->occurredAt, $event->occurredAt());
    }

    private function createEvent(): OrderCreatedEvent
    {
        return new OrderCreatedEvent(
            orderId: 'order-123',
            customerId: 'customer-456',
            createdAt: new DateTimeImmutable(),
            metadata: EventMetadata::create()
        );
    }
}
```

## Event Naming Conventions

### Past Tense Naming

| Action | Event Name |
|--------|------------|
| Create order | `OrderCreatedEvent` |
| Confirm order | `OrderConfirmedEvent` |
| Cancel order | `OrderCancelledEvent` |
| Ship order | `OrderShippedEvent` |
| Add line | `OrderLineAddedEvent` |
| Remove line | `OrderLineRemovedEvent` |
| Change email | `UserEmailChangedEvent` |
| Register user | `UserRegisteredEvent` |
| Deactivate user | `UserDeactivatedEvent` |

### Bad Names (Avoid)

| Bad Name | Why | Good Name |
|----------|-----|-----------|
| `CreateOrderEvent` | Present tense | `OrderCreatedEvent` |
| `OrderEvent` | Vague | `OrderConfirmedEvent` |
| `OrderStatusChangedEvent` | Too generic | `OrderConfirmedEvent` |
| `UpdateOrderEvent` | Doesn't say what changed | `OrderAddressChangedEvent` |

## Event Data Guidelines

### Include All Relevant Data

```php
// GOOD: All data needed to understand what happened
final readonly class OrderConfirmedEvent
{
    public function __construct(
        public string $orderId,
        public int $totalCents,       // Include computed values
        public string $currency,
        public int $lineCount,         // Summary data
        public DateTimeImmutable $confirmedAt,
        public EventMetadata $metadata
    ) {}
}

// BAD: Missing important data
final readonly class OrderConfirmedEvent
{
    public function __construct(
        public string $orderId,        // Only ID, no details
        public EventMetadata $metadata
    ) {}
}
```

### Use Primitive Types

```php
// GOOD: Primitive types for serialization
final readonly class OrderCreatedEvent
{
    public function __construct(
        public string $orderId,        // Not OrderId
        public string $customerId,     // Not CustomerId
        public int $totalCents,        // Not Money
        public string $currency,
        public EventMetadata $metadata
    ) {}
}

// BAD: Value Objects in events (serialization issues)
final readonly class OrderCreatedEvent
{
    public function __construct(
        public OrderId $orderId,       // Serialization complex
        public Money $total,           // Serialization complex
        public EventMetadata $metadata
    ) {}
}
```

## Generation Instructions

When asked to create a Domain Event:

1. **Name in past tense** (what happened)
2. **Include aggregate ID** for identification
3. **Add all relevant data** needed to understand the event
4. **Use primitive types** for easy serialization
5. **Include metadata** (event ID, timestamp)
6. **Generate tests** for structure and interface

## Usage

To generate a Domain Event, provide:
- Name (e.g., "OrderConfirmed", "UserRegistered")
- Bounded Context (e.g., "Order", "User")
- Aggregate ID field
- Data fields needed
- Any computed/summary data to include
