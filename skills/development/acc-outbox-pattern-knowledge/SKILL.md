---
name: acc-outbox-pattern-knowledge
description: Outbox Pattern knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for transactional outbox, polling publisher, and reliable messaging audits.
---

# Outbox Pattern Knowledge Base

Quick reference for Transactional Outbox pattern and PHP implementation guidelines.

## Core Principles

### Transactional Outbox Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TRANSACTIONAL OUTBOX PATTERN                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                    SINGLE TRANSACTION                             │  │
│   │  ┌──────────┐      ┌───────────────┐      ┌────────────────┐     │  │
│   │  │ Business │─────▶│ Domain Table  │      │ Outbox Table   │     │  │
│   │  │  Logic   │      │  (orders)     │      │ (outbox_msgs)  │     │  │
│   │  └──────────┘      └───────────────┘      └────────────────┘     │  │
│   │       │                   ▲                       ▲              │  │
│   │       └───────────────────┴───────────────────────┘              │  │
│   │                    COMMIT/ROLLBACK                               │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│   ┌──────────────────┐                    ┌──────────────────────────┐  │
│   │ Message Relay    │───────────────────▶│ Message Broker           │  │
│   │ (Polling/CDC)    │   publish events   │ (RabbitMQ/Kafka)         │  │
│   └──────────────────┘                    └──────────────────────────┘  │
│           │                                                              │
│           ▼                                                              │
│   Marks messages as processed                                           │
│                                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Publishing Strategies:                                                 │
│   • Polling Publisher  - Periodic poll for unprocessed messages          │
│   • Transaction Log Tailing (CDC) - Debezium, Maxwell                   │
│   • Event Sourcing + Projections - Events = Outbox                      │
│                                                                          │
│   Guarantees:                                                            │
│   • At-least-once delivery                                              │
│   • No message loss on service crash                                    │
│   • Transactional consistency between data and events                   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| Outbox Table | Database table storing pending messages within same transaction |
| Message Relay | Background process that publishes messages from outbox |
| Polling Publisher | Periodically queries outbox for unpublished messages |
| CDC (Change Data Capture) | Streams database changes to message broker |
| Idempotency Key | Unique identifier for message deduplication |
| At-least-once | Messages delivered at least once (consumers must be idempotent) |

## Quick Checklists

### Outbox Table Checklist

- [ ] Messages inserted in same transaction as domain changes
- [ ] Unique message ID for deduplication
- [ ] Event type/name for routing
- [ ] Payload serialized as JSON
- [ ] Created timestamp
- [ ] Processed/Published flag or timestamp
- [ ] Aggregate ID for correlation
- [ ] Retry count for failure tracking

### Message Relay Checklist

- [ ] Runs as separate process/cron
- [ ] Polls with configurable interval
- [ ] Batch processing for efficiency
- [ ] Marks messages as processed after publish
- [ ] Handles publish failures with retry
- [ ] Dead letter handling for poison messages
- [ ] Ordering guarantees per aggregate (if needed)

### Consumer Checklist

- [ ] Idempotent processing (check message ID)
- [ ] Handles duplicate messages gracefully
- [ ] Stores processed message IDs
- [ ] Acknowledges only after successful processing

## PHP 8.5 Outbox Patterns

### OutboxMessage Entity

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Outbox;

final readonly class OutboxMessage
{
    public function __construct(
        public string $id,
        public string $aggregateType,
        public string $aggregateId,
        public string $eventType,
        public string $payload,
        public \DateTimeImmutable $createdAt,
        public ?string $correlationId = null,
        public ?\DateTimeImmutable $processedAt = null,
        public int $retryCount = 0
    ) {}

    public function isProcessed(): bool
    {
        return $this->processedAt !== null;
    }

    public function withProcessed(\DateTimeImmutable $at): self
    {
        return new self(
            $this->id,
            $this->aggregateType,
            $this->aggregateId,
            $this->eventType,
            $this->payload,
            $this->createdAt,
            $this->correlationId,
            $at,
            $this->retryCount
        );
    }

    public function withRetry(): self
    {
        return new self(
            $this->id,
            $this->aggregateType,
            $this->aggregateId,
            $this->eventType,
            $this->payload,
            $this->createdAt,
            $this->correlationId,
            $this->processedAt,
            $this->retryCount + 1
        );
    }
}
```

### OutboxRepository Interface (Domain)

```php
<?php

declare(strict_types=1);

namespace Domain\Shared\Outbox;

interface OutboxRepositoryInterface
{
    public function save(OutboxMessage $message): void;

    /** @param array<OutboxMessage> $messages */
    public function saveAll(array $messages): void;

    /** @return array<OutboxMessage> */
    public function findUnprocessed(int $limit = 100): array;

    public function markAsProcessed(string $id, \DateTimeImmutable $at): void;

    public function incrementRetry(string $id): void;

    public function delete(string $id): void;
}
```

### Outbox Publisher Service

```php
<?php

declare(strict_types=1);

namespace Application\Shared\Outbox;

use Domain\Shared\Outbox\OutboxMessage;
use Domain\Shared\Outbox\OutboxRepositoryInterface;

final readonly class OutboxPublisher
{
    public function __construct(
        private OutboxRepositoryInterface $outbox,
        private EventPublisherInterface $publisher,
        private int $maxRetries = 3
    ) {}

    public function processOutbox(int $batchSize = 100): int
    {
        $messages = $this->outbox->findUnprocessed($batchSize);
        $processed = 0;

        foreach ($messages as $message) {
            try {
                $this->publisher->publish(
                    $message->eventType,
                    $message->payload,
                    $message->correlationId
                );
                $this->outbox->markAsProcessed(
                    $message->id,
                    new \DateTimeImmutable()
                );
                $processed++;
            } catch (\Throwable $e) {
                $this->handleFailure($message, $e);
            }
        }

        return $processed;
    }

    private function handleFailure(OutboxMessage $message, \Throwable $e): void
    {
        if ($message->retryCount >= $this->maxRetries) {
            // Move to dead letter / log critical
            $this->outbox->delete($message->id);
            return;
        }
        $this->outbox->incrementRetry($message->id);
    }
}
```

### Transactional Event Dispatch

```php
<?php

declare(strict_types=1);

namespace Application\Order\UseCase;

use Domain\Order\OrderRepositoryInterface;
use Domain\Shared\Outbox\OutboxRepositoryInterface;
use Domain\Shared\Outbox\OutboxMessage;

final readonly class PlaceOrderUseCase
{
    public function __construct(
        private OrderRepositoryInterface $orders,
        private OutboxRepositoryInterface $outbox,
        private TransactionInterface $transaction
    ) {}

    public function execute(PlaceOrderCommand $command): OrderId
    {
        return $this->transaction->execute(function () use ($command): OrderId {
            $order = Order::place(
                OrderId::generate(),
                CustomerId::fromString($command->customerId),
                $command->items
            );

            $this->orders->save($order);

            // Store event in outbox within same transaction
            foreach ($order->releaseEvents() as $event) {
                $this->outbox->save(new OutboxMessage(
                    id: $event->eventId,
                    aggregateType: 'Order',
                    aggregateId: $order->id()->toString(),
                    eventType: $event->eventName(),
                    payload: json_encode($event->toArray()),
                    createdAt: $event->occurredAt,
                    correlationId: $command->correlationId
                ));
            }

            return $order->id();
        });
    }
}
```

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Publish before commit | Event published without outbox | Critical |
| No idempotency key | OutboxMessage without unique ID | Critical |
| Two-phase commit | Distributed transaction attempt | Critical |
| Missing retry logic | No retry count in outbox | Warning |
| No dead letter handling | Failed messages lost | Warning |
| Unbounded polling | No limit on batch size | Warning |
| Synchronous publish in transaction | HTTP call in DB transaction | Critical |

## Detection Patterns

```bash
# Find outbox implementations
Glob: **/Outbox/**/*.php
Glob: **/outbox*.php
Grep: "outbox|OutboxMessage|OutboxRepository" --glob "**/*.php"

# Check for proper transactional outbox
Grep: "->save.*->outbox|outbox.*transaction" --glob "**/UseCase/**/*.php"

# Detect anti-patterns: publishing in transaction
Grep: "transaction.*publish|->publish\(.*\)->commit" --glob "**/*.php"

# Find message relay/processor
Grep: "findUnprocessed|processOutbox|OutboxProcessor" --glob "**/*.php"

# Check for idempotency handling
Grep: "messageId|eventId|idempotencyKey" --glob "**/Consumer/**/*.php"

# Find Doctrine outbox table
Grep: "outbox_messages|OutboxMessage.*Entity" --glob "**/Infrastructure/**/*.php"
```

## Database Schema Example

```sql
CREATE TABLE outbox_messages (
    id UUID PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    correlation_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMP NULL,
    retry_count INT NOT NULL DEFAULT 0,
    INDEX idx_unprocessed (processed_at, created_at)
);
```

## References

For detailed information, load these reference files:

- `references/outbox-patterns.md` — Implementation strategies and patterns
- `references/antipatterns.md` — Common violations with detection patterns
- `references/php-specific.md` — PHP 8.5 specific implementations

## Assets

- `assets/report-template.md` — Structured audit report template
