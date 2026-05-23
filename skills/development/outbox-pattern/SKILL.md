---
name: outbox-pattern
description: Transactional outbox pattern for reliable event publishing. Use when implementing atomic writes with event delivery, ensuring exactly-once semantics, or building event-driven microservices.
context: fork
agent: event-driven-architect
version: 2.0.0
tags: [event-driven, outbox, transactions, reliability, microservices, cdc, idempotency, 2026]
allowed-tools: [Read, Write, Grep, Glob, Bash]
author: SkillForge
user-invocable: false
---

# Outbox Pattern (2026)

Ensure atomic state changes and event publishing by writing both to a database transaction, then publishing asynchronously.

## Overview

- Ensuring database writes and event publishing are atomic
- Building reliable event-driven microservices
- Implementing exactly-once message delivery semantics
- Avoiding dual-write problems (DB + message broker)
- Decoupling domain logic from message infrastructure
- High-throughput systems needing CDC-based publishing

## Quick Reference

### Outbox Table Schema

```sql
CREATE TABLE outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    idempotency_key VARCHAR(255) UNIQUE,  -- For consumer deduplication
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    published_at TIMESTAMPTZ,
    retry_count INT DEFAULT 0,
    last_error TEXT
);

-- Index for polling unpublished messages
CREATE INDEX idx_outbox_unpublished ON outbox(created_at)
    WHERE published_at IS NULL;

-- Index for aggregate ordering
CREATE INDEX idx_outbox_aggregate ON outbox(aggregate_id, created_at);

-- Index for idempotency key lookups
CREATE INDEX idx_outbox_idempotency ON outbox(idempotency_key)
    WHERE idempotency_key IS NOT NULL;
```

### SQLAlchemy Model

```python
from sqlalchemy.dialects.postgresql import UUID, JSONB
import hashlib

class OutboxMessage(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_type = Column(String(100), nullable=False)
    aggregate_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(JSONB, nullable=False)
    idempotency_key = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    published_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, default=0)
    last_error = Column(Text, nullable=True)

    @staticmethod
    def generate_idempotency_key(aggregate_id: str, event_type: str, payload: dict) -> str:
        """Generate deterministic idempotency key for deduplication."""
        content = f"{aggregate_id}:{event_type}:{json.dumps(payload, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()[:32]
```

### Write to Outbox in Transaction

```python
from sqlalchemy.ext.asyncio import AsyncSession

class OrderService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: OrderCreate) -> Order:
        """Create order AND outbox message in single transaction."""
        # Create the order
        order = Order(**order_data.model_dump())
        self.db.add(order)

        # Create outbox message in SAME transaction
        outbox_msg = OutboxMessage(
            aggregate_type="Order",
            aggregate_id=order.id,
            event_type="OrderCreated",
            payload={
                "order_id": str(order.id),
                "customer_id": str(order.customer_id),
                "total": order.total,
            },
            idempotency_key=OutboxMessage.generate_idempotency_key(
                str(order.id), "OrderCreated", {"total": order.total}
            ),
        )
        self.db.add(outbox_msg)

        await self.db.flush()  # Both written atomically
        return order
```

### Polling Publisher

```python
class OutboxPublisher:
    """Polls outbox and publishes to message broker."""

    def __init__(self, session_factory, producer):
        self.session_factory = session_factory
        self.producer = producer

    async def publish_pending(self, batch_size: int = 100) -> int:
        async with self.session_factory() as session:
            stmt = (
                select(OutboxMessage)
                .where(OutboxMessage.published_at.is_(None))
                .order_by(OutboxMessage.created_at)
                .limit(batch_size)
                .with_for_update(skip_locked=True)  # Prevent duplicate processing
            )
            result = await session.execute(stmt)
            messages = result.scalars().all()

            published = 0
            for msg in messages:
                try:
                    await self.producer.publish(
                        topic=f"{msg.aggregate_type.lower()}-events",
                        key=str(msg.aggregate_id),
                        value={
                            "type": msg.event_type,
                            "idempotency_key": msg.idempotency_key,
                            **msg.payload
                        },
                    )
                    msg.published_at = datetime.now(timezone.utc)
                    published += 1
                except Exception as e:
                    msg.retry_count += 1
                    msg.last_error = str(e)

            await session.commit()
            return published
```

### CDC with Debezium (High-Throughput)

```yaml
# docker-compose.yml - Debezium connector
version: '3.8'
services:
  debezium:
    image: debezium/connect:2.5
    environment:
      BOOTSTRAP_SERVERS: kafka:9092
      GROUP_ID: outbox-connector
      CONFIG_STORAGE_TOPIC: connect-configs
      OFFSET_STORAGE_TOPIC: connect-offsets

# Register outbox connector
# POST http://debezium:8083/connectors
```

```json
{
  "name": "outbox-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "app",
    "table.include.list": "public.outbox",
    "transforms": "outbox",
    "transforms.outbox.type": "io.debezium.transforms.outbox.EventRouter",
    "transforms.outbox.table.field.event.id": "id",
    "transforms.outbox.table.field.event.key": "aggregate_id",
    "transforms.outbox.table.field.event.payload": "payload",
    "transforms.outbox.route.topic.replacement": "${routedByValue}-events"
  }
}
```

### Idempotent Consumer

```python
class IdempotentConsumer:
    """Consumer with deduplication using idempotency keys."""

    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.redis = redis

    async def process(self, event: dict, handler) -> bool:
        """Process event idempotently - returns False if duplicate."""
        idempotency_key = event.get("idempotency_key")
        if not idempotency_key:
            # No key = always process (but risky)
            await handler(event)
            return True

        # Check Redis cache first (fast path)
        if await self.redis.exists(f"processed:{idempotency_key}"):
            return False  # Already processed

        # Check database (slow path, but durable)
        exists = await self.db.execute(
            select(ProcessedEvent)
            .where(ProcessedEvent.idempotency_key == idempotency_key)
        )
        if exists.scalar_one_or_none():
            # Cache for future fast lookups
            await self.redis.setex(f"processed:{idempotency_key}", 86400, "1")
            return False

        # Process and record
        async with self.db.begin():
            await handler(event)
            self.db.add(ProcessedEvent(idempotency_key=idempotency_key))
            await self.db.flush()

        # Cache the processed key
        await self.redis.setex(f"processed:{idempotency_key}", 86400, "1")
        return True


class ProcessedEvent(Base):
    """Track processed events for idempotency."""
    __tablename__ = "processed_events"

    idempotency_key = Column(String(255), primary_key=True)
    processed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

### Dapr Outbox Integration

```python
# Using Dapr's built-in outbox support
from dapr.clients import DaprClient

async def create_order_with_dapr(order_data: dict):
    """Dapr handles outbox automatically."""
    async with DaprClient() as client:
        # Single call - Dapr ensures atomicity
        await client.save_state(
            store_name="statestore",
            key=f"order-{order_data['id']}",
            value=order_data,
            state_metadata={
                "outbox.publish": "true",
                "outbox.topic": "orders",
            }
        )
```

## Key Decisions

| Decision | Option A | Option B | Recommendation |
|----------|----------|----------|----------------|
| Delivery | Polling | CDC (Debezium) | Polling for simplicity, CDC for > 10K msg/s |
| Batch size | Small (10-50) | Large (100-500) | Start with 100, tune based on latency |
| Retry | Fixed delay | Exponential backoff | Exponential with max 5 retries |
| Cleanup | Delete published | Archive to cold storage | Archive for audit, delete after 30 days |
| Ordering | Per-aggregate | Global | Per-aggregate via partition key |
| Idempotency | Consumer-side | Built-in key | Always include idempotency key |
| Tool | Custom | Dapr | Dapr if K8s, custom otherwise |

## Outbox vs CDC Trade-offs

```
┌────────────────────────────────────────────────────────────────────────┐
│                     POLLING vs CDC COMPARISON                           │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  POLLING (OutboxPublisher)          CDC (Debezium)                     │
│  ──────────────────────────         ────────────────                   │
│  ✓ Simple to implement              ✓ Higher throughput (100K+ msg/s)  │
│  ✓ No extra infrastructure          ✓ Lower latency (sub-second)       │
│  ✓ Easy to debug                    ✓ No polling overhead              │
│  ✗ Polling overhead                 ✗ Complex infrastructure           │
│  ✗ Higher latency (1-5s)            ✗ Harder to debug                  │
│  ✗ Limited throughput (~10K/s)      ✗ Requires Kafka Connect           │
│                                                                         │
│  USE WHEN:                          USE WHEN:                          │
│  - Starting out                     - High throughput required         │
│  - Simple architecture              - Sub-second latency needed        │
│  - < 10K events/second              - Already using Kafka              │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER publish before commit - dual-write problem
await producer.publish(event)  # May succeed but commit may fail!
await session.commit()

# NEVER delete without publishing - events lost
await session.execute(delete(OutboxMessage).where(...))

# NEVER process without locking - causes duplicates
messages = await session.execute(select(OutboxMessage))  # No lock!

# NEVER store large payloads - use URL references instead
OutboxMessage(payload={"file": large_binary_data})

# NEVER ignore ordering - use aggregate_id as partition key
await producer.publish(event_a)  # May arrive out of order!

# NEVER skip idempotency keys
OutboxMessage(payload=event_data)  # No idempotency_key = duplicate risk

# NEVER process without idempotency check on consumer
async def handle(event):
    await process(event)  # Duplicate processing on retry!
```

## Related Skills

- `message-queues` - Kafka, RabbitMQ, Redis Streams integration
- `event-sourcing` - Full event-sourced architecture patterns
- `database-schema-designer` - Schema design and migrations
- `sqlalchemy-2-async` - Async database session patterns

## Capability Details

### outbox-schema
**Keywords:** outbox table, transactional outbox, event table, schema, idempotency
**Solves:**
- How do I design an outbox table?
- What indexes are needed for outbox?
- Outbox table best practices
- Idempotency key generation

### polling-publisher
**Keywords:** polling, publish outbox, background worker, relay
**Solves:**
- How do I publish from the outbox?
- Batch publishing patterns
- Handling publish failures
- FOR UPDATE SKIP LOCKED pattern

### cdc-debezium
**Keywords:** cdc, debezium, change data capture, kafka connect
**Solves:**
- When to use CDC vs polling?
- Debezium connector configuration
- High-throughput event publishing
- Outbox event routing

### idempotent-consumer
**Keywords:** idempotent, deduplication, exactly-once, processed events
**Solves:**
- How to handle duplicate messages?
- Idempotency key patterns
- Consumer deduplication strategies
- Redis + DB deduplication

### atomic-operations
**Keywords:** atomic, transaction, dual-write, consistency
**Solves:**
- How to avoid dual-write problems?
- Ensuring atomicity between DB and events
- Exactly-once delivery patterns
