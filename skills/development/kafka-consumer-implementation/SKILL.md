---
name: kafka-consumer-implementation
description: |
  Implement type-safe Kafka consumers for event consumption with msgspec deserialization.
  Use when building async consumers that process domain events (order messages, transactions)
  with offset management, error recovery, graceful shutdown, and distributed tracing.
  Handles consumer configuration, manual commits, and rebalancing strategies.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Kafka Consumer Implementation

## Purpose

Implement production-grade Kafka consumers that reliably consume and process domain events with high performance, type safety, and comprehensive error recovery. Covers msgspec deserialization, confluent-kafka configuration, offset management, OpenTelemetry tracing, and anti-corruption layer patterns for translating message schemas to domain models.

## When to Use This Skill

Use when building event-driven systems that consume domain events from Kafka topics with "implement Kafka consumer", "consume events from Kafka", "process order messages", or "set up event consumer".

Do NOT use when mocking Kafka consumers in unit tests (use `pytest-adapter-integration-testing`), implementing producers (use `kafka-producer-implementation`), or testing with testcontainers (use `kafka-integration-testing`).

## Quick Start

Create a high-performance Kafka consumer in 3 steps:

1. **Define message schema**:
```python
import msgspec

class OrderEventMessage(msgspec.Struct, frozen=True):
    order_id: str
    created_at: str
    customer_name: str
    total_price: float
```

2. **Implement consumer**:
```python
from confluent_kafka import Consumer
import msgspec

class OrderEventConsumer:
    def __init__(self, brokers: list[str], topic: str, group_id: str) -> None:
        config = {
            "bootstrap.servers": ",".join(brokers),
            "group.id": group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False,
        }
        self.consumer = Consumer(config)
        self.consumer.subscribe([topic])
        self.decoder = msgspec.json.Decoder(OrderEventMessage)

    def consume(self, timeout: float = 1.0) -> OrderEventMessage | None:
        msg = self.consumer.poll(timeout)
        if msg is None or msg.error():
            return None
        return self.decoder.decode(msg.value())

    def commit(self) -> None:
        self.consumer.commit(asynchronous=False)
```

3. **Use in application**:
```python
consumer = OrderEventConsumer(["localhost:9092"], "orders", "loader")
message = consumer.consume()
if message:
    process(message)
    consumer.commit()
```

## Implementation Steps

### 1. Consumer Configuration

Key configuration for exactly-once processing:
```python
config = {
    "bootstrap.servers": ",".join(brokers),
    "group.id": group_id,
    "auto.offset.reset": "earliest",  # Start from beginning
    "enable.auto.commit": False,  # Manual offset management
    "session.timeout.ms": 300000,  # 5 minute timeout
    "max.poll.interval.ms": 300000,  # 5 minutes for processing
}
```

### 2. Consumer Adapter

Implement consumer with error handling:
- msgspec deserialization (10-20x faster than Pydantic)
- OpenTelemetry distributed tracing
- Manual offset management for exactly-once semantics
- Comprehensive error logging

See `references/detailed-implementation.md` for complete consumer adapter code.

### 3. Anti-Corruption Layer

Translate Kafka messages to domain entities:
```python
class OrderEventTranslator:
    @staticmethod
    def to_domain_order(message: OrderEventMessage) -> Order:
        # Validate
        if not message.order_id:
            raise ValueError("order_id is required")

        # Convert types (str -> OrderId, float -> Money)
        created_at = datetime.fromisoformat(message.created_at)
        order_id = OrderId(message.order_id)
        total_price = Money(Decimal(str(message.total_price)))

        return Order(order_id, created_at, message.customer_name, total_price, [])
```

### 4. Processing Loop

Main consumer loop pattern:
1. Poll for messages (5s timeout)
2. Translate to domain objects
3. Process (load into storage)
4. Commit offset (only after success)
5. Handle errors without stopping loop

See `references/detailed-implementation.md` for complete processing loop code.

### 5. Lifecycle Management

Use context managers for clean shutdown:
```python
@asynccontextmanager
async def managed_consumer(brokers, topic, group_id):
    consumer = OrderEventConsumer(brokers, topic, group_id)
    try:
        yield consumer
    finally:
        consumer.close()
```

## Requirements

- `confluent-kafka>=2.3.0` - Production-grade Kafka client
- `msgspec>=0.18.6` - Ultra-fast deserialization
- `structlog>=23.2.0` - Structured logging
- `opentelemetry-api>=1.22.0` - Distributed tracing
- Kafka/Redpanda broker running (3.x or later)
- Python 3.11+ with type checking enabled

## Consumer Groups and Offset Management

**Consumer Groups**: Consumers in the same group share responsibility for topic partitions. Kafka automatically rebalances when members join/leave.

**Manual Offset Management** (exactly-once-per-restart):
1. Disable auto-commit: `"enable.auto.commit": False`
2. Commit only after successful processing: `consumer.commit()`
3. Offset reset behavior: `"auto.offset.reset": "earliest"` starts from beginning

See `references/detailed-implementation.md` for complete offset management patterns, consumer lag monitoring, and rebalancing behavior.

## Error Handling

Key error handling strategies:
- **Deserialization failures**: Log error, commit offset to skip poison pill
- **Processing failures**: Don't commit, message will be retried on restart
- **Commit failures**: Log error, continue (will retry on next message)

See `references/error-handling.md` for comprehensive error handling strategies and dead letter queue patterns.

## Testing

Use testcontainers for integration tests:
```python
from testcontainers.kafka import KafkaContainer

@pytest.fixture
def kafka_container():
    with KafkaContainer() as kafka:
        yield kafka

def test_consumer_roundtrip(kafka_container):
    brokers = [kafka_container.get_bootstrap_server()]
    # Test consumer/producer workflow
```

See `examples/integration-examples.md` for complete integration test patterns.

## See Also

- `references/detailed-implementation.md` - Complete consumer adapter and processing loop code
- `references/error-handling.md` - Comprehensive error handling strategies
- `examples/integration-examples.md` - Real-world integration patterns
- `kafka-producer-implementation` skill - For producing events
- `kafka-schema-management` skill - For schema design
