---
name: acc-create-outbox-pattern
description: Generates Transactional Outbox pattern components for PHP 8.5. Creates OutboxMessage entity, repository, publisher, and processor with unit tests.
---

# Outbox Pattern Generator

Creates Transactional Outbox pattern infrastructure for reliable event publishing.

## When to Use

- Need reliable event publishing across transaction boundaries
- Prevent message loss if broker is down
- Ensure exactly-once or at-least-once delivery
- Maintain consistency between database and message broker

## Component Characteristics

### OutboxMessage Entity
- Immutable value object in Domain layer
- Contains: id, aggregateType, aggregateId, eventType, payload, timestamps
- Supports reconstitution for persistence
- Methods: withProcessed(), withRetryIncremented()

### OutboxRepository
- Interface in Domain layer
- Implementation in Infrastructure layer
- Methods: save, findUnprocessed, markAsProcessed, incrementRetry, delete

### OutboxProcessor
- Application layer service
- Polls for unprocessed messages
- Publishes to message broker
- Handles failures with retry and dead letter

### Console Command
- Infrastructure layer
- Runs as daemon or one-shot
- Configurable batch size and interval

---

## Generation Process

### Step 1: Generate Domain Layer

**Path:** `src/Domain/Shared/Outbox/`

1. `OutboxMessage.php` — Immutable message entity
2. `OutboxRepositoryInterface.php` — Repository contract

### Step 2: Generate Application Layer

**Path:** `src/Application/Shared/`

1. `Port/Output/MessagePublisherInterface.php` — Publisher port
2. `Port/Output/DeadLetterRepositoryInterface.php` — Dead letter port
3. `Outbox/ProcessingResult.php` — Result value object
4. `Outbox/MessageResult.php` — Result enum
5. `Outbox/OutboxProcessor.php` — Processing service

### Step 3: Generate Infrastructure Layer

**Path:** `src/Infrastructure/`

1. `Persistence/Doctrine/Repository/DoctrineOutboxRepository.php`
2. `Console/OutboxProcessCommand.php`
3. Database migration

### Step 4: Generate Tests

1. `tests/Unit/Domain/Shared/Outbox/OutboxMessageTest.php`
2. `tests/Unit/Application/Shared/Outbox/OutboxProcessorTest.php`

---

## Key Principles

### Transactional Consistency
```php
// In UseCase - save outbox message in SAME transaction
$this->connection->transactional(function () use ($order, $event) {
    $this->orderRepository->save($order);
    $this->outboxRepository->save(
        OutboxMessage::create(
            id: Uuid::uuid4()->toString(),
            aggregateType: 'Order',
            aggregateId: $order->id()->toString(),
            eventType: 'order.placed',
            payload: $event->toArray()
        )
    );
});
```

### Retry with Dead Letter
1. Retry up to MAX_RETRIES times
2. Exponential backoff between retries
3. Move to dead letter queue after max retries
4. Log all failures with context

### Message Headers
Include metadata for tracing:
- message_id, correlation_id, causation_id
- aggregate_type, aggregate_id
- created_at

---

## File Placement

| Layer | Path |
|-------|------|
| Domain Entity | `src/Domain/Shared/Outbox/` |
| Domain Interface | `src/Domain/Shared/Outbox/` |
| Application Service | `src/Application/Shared/Outbox/` |
| Application Port | `src/Application/Shared/Port/Output/` |
| Infrastructure Repo | `src/Infrastructure/Persistence/Doctrine/Repository/` |
| Infrastructure Console | `src/Infrastructure/Console/` |
| Unit Tests | `tests/Unit/{Layer}/{Path}/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Entity | `{Name}` | `OutboxMessage` |
| Repository Interface | `{Name}RepositoryInterface` | `OutboxRepositoryInterface` |
| Repository Impl | `Doctrine{Name}Repository` | `DoctrineOutboxRepository` |
| Service | `{Name}Processor` | `OutboxProcessor` |
| Command | `{Name}Command` | `OutboxProcessCommand` |
| Test | `{ClassName}Test` | `OutboxMessageTest` |

---

## Quick Template Reference

### OutboxMessage

```php
final readonly class OutboxMessage
{
    public static function create(
        string $id,
        string $aggregateType,
        string $aggregateId,
        string $eventType,
        array $payload,
        ?string $correlationId = null,
        ?string $causationId = null
    ): self;

    public function isProcessed(): bool;
    public function isPoisoned(int $maxRetries): bool;
    public function payloadAsArray(): array;
    public function withProcessed(): self;
    public function withRetryIncremented(): self;
}
```

### OutboxRepositoryInterface

```php
interface OutboxRepositoryInterface
{
    public function save(OutboxMessage $message): void;
    public function findUnprocessed(int $limit = 100): array;
    public function markAsProcessed(string $id): void;
    public function incrementRetry(string $id): void;
    public function delete(string $id): void;
}
```

### OutboxProcessor

```php
final readonly class OutboxProcessor
{
    public function process(int $batchSize = 100): ProcessingResult;
}
```

---

## Usage Example

### Saving to Outbox

```php
// In UseCase
$message = OutboxMessage::create(
    id: Uuid::uuid4()->toString(),
    aggregateType: 'Order',
    aggregateId: $order->id()->toString(),
    eventType: 'order.placed',
    payload: [
        'order_id' => $order->id()->toString(),
        'customer_id' => $order->customerId()->toString(),
        'total' => $order->total()->amount(),
    ],
    correlationId: $command->correlationId
);

$this->outboxRepository->save($message);
```

### Console Command

```bash
# One-shot processing
php bin/console outbox:process --batch-size=100

# Daemon mode
php bin/console outbox:process --daemon --interval=1000
```

---

## DI Configuration

```yaml
# Symfony services.yaml
Domain\Shared\Outbox\OutboxRepositoryInterface:
    alias: Infrastructure\Persistence\Doctrine\Repository\DoctrineOutboxRepository

Application\Shared\Port\Output\MessagePublisherInterface:
    alias: Infrastructure\Messaging\RabbitMq\RabbitMqPublisher

Application\Shared\Outbox\OutboxProcessor:
    arguments:
        $maxRetries: 5
```

---

## Database Schema

```sql
CREATE TABLE outbox_messages (
    id VARCHAR(36) PRIMARY KEY,
    aggregate_type VARCHAR(255) NOT NULL,
    aggregate_id VARCHAR(255) NOT NULL,
    event_type VARCHAR(255) NOT NULL,
    payload JSONB NOT NULL,
    correlation_id VARCHAR(255),
    causation_id VARCHAR(255),
    created_at TIMESTAMP(6) NOT NULL,
    processed_at TIMESTAMP(6),
    retry_count INT NOT NULL DEFAULT 0
);

CREATE INDEX idx_outbox_unprocessed
ON outbox_messages (processed_at, created_at)
WHERE processed_at IS NULL;
```

---

## References

For complete PHP templates and test examples, see:
- `references/templates.md` — All component templates
- `references/tests.md` — Unit test examples
