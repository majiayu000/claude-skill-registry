---
name: kafka-producer-implementation
description: |
  Implement type-safe Kafka producers for event streaming with msgspec serialization.
  Use when building async/await producers that publish domain events (orders, transactions, etc.)
  with schema validation, error handling, retry logic, and distributed tracing.
  Handles producer configuration, idempotent writes, and graceful shutdown.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Kafka Producer Implementation

## Purpose

Implement production-grade Kafka producers that reliably publish domain events with high performance, type safety, and comprehensive error handling. Covers msgspec serialization, confluent-kafka configuration, OpenTelemetry tracing, and anti-corruption layer patterns for translating domain models to message schemas.


## When to Use This Skill

Use when building event publishers that send domain events to Kafka topics with "implement Kafka producer", "publish events to Kafka", "send order events", or "create event publisher".

Do NOT use for consuming events (use `kafka-consumer-implementation`), testing with testcontainers (use `kafka-integration-testing`), or designing schemas (use `kafka-schema-management`).
## Quick Start

Create a high-performance Kafka producer in 3 steps:

1. **Define message schema**:
```python
import msgspec

class OrderEventMessage(msgspec.Struct, frozen=True):
    order_id: str
    created_at: str  # ISO 8601
    customer_name: str
    total_price: float
```

2. **Implement producer**:
```python
from confluent_kafka import Producer
import msgspec

class OrderEventPublisher:
    def __init__(self, brokers: list[str], topic: str) -> None:
        config = {
            "bootstrap.servers": ",".join(brokers),
            "acks": "all",
            "enable.idempotence": True,
            "compression.type": "snappy",
        }
        self.producer = Producer(config)
        self.topic = topic
        self.encoder = msgspec.json.Encoder()

    def publish(self, event: OrderEventMessage) -> None:
        payload = self.encoder.encode(event)
        self.producer.produce(
            topic=self.topic,
            key=event.order_id.encode("utf-8"),
            value=payload,
        )
        self.producer.poll(0)

    def close(self) -> None:
        self.producer.flush(10.0)
```

3. **Use in application**:
```python
publisher = OrderEventPublisher(["localhost:9092"], "orders")
publisher.publish(order_event)
publisher.close()
```

## Implementation Steps

### 1. Message Schema with msgspec

Define immutable schemas using `msgspec.Struct` for 10-20x faster serialization:

```python
import msgspec

class LineItemEventMessage(msgspec.Struct, frozen=True):
    line_item_id: str
    product_id: str
    product_title: str
    quantity: int
    price: float

class OrderEventMessage(msgspec.Struct, frozen=True):
    order_id: str
    created_at: str  # ISO 8601 format string
    customer_name: str
    line_items: list[LineItemEventMessage]
    total_price: float
```

**Key Points:**
- Use `frozen=True` for immutability
- Use primitive types (str, float, int) not custom objects
- Store timestamps as ISO 8601 strings
- msgspec produces JSON bytes automatically

### 2. Producer Adapter

Implement producer with error handling and tracing:

```python
import msgspec
from confluent_kafka import Producer, KafkaException
from opentelemetry import trace
from structlog import get_logger

class OrderEventPublisher:
    """Publishes order events with high performance and reliability.

    Features:
    - msgspec serialization (10-20x faster than Pydantic)
    - OpenTelemetry distributed tracing
    - Idempotent exactly-once semantics
    - Message ordering guarantees (by order_id key)

    Configuration:
    - acks=all: Wait for all in-sync replicas
    - enable.idempotence=True: Exactly-once-per-send
    - max.in.flight.requests.per.connection=1: Preserve order
    - compression.type=snappy: Balance CPU/network
    """

    def __init__(self, brokers: list[str], topic: str) -> None:
        self.topic = topic
        self.logger = get_logger(__name__)
        self.tracer = trace.get_tracer(__name__)
        self.encoder = msgspec.json.Encoder()

        config = {
            "bootstrap.servers": ",".join(brokers),
            "acks": "all",
            "retries": 5,
            "max.in.flight.requests.per.connection": 1,
            "compression.type": "snappy",
            "enable.idempotence": True,
        }

        self.producer = Producer(config)

    def publish_order(self, event: OrderEventMessage) -> None:
        """Publish order event with order_id as partition key."""
        with self.tracer.start_as_current_span("publish_order") as span:
            span.set_attribute("order_id", event.order_id)

            payload = self.encoder.encode(event)
            self.producer.produce(
                topic=self.topic,
                key=event.order_id.encode("utf-8"),
                value=payload,
                on_delivery=self._delivery_callback,
            )
            self.producer.poll(0)

    def _delivery_callback(self, err, msg):
        """Handle delivery callback."""
        if err:
            self.logger.error("delivery_failed", error=str(err))
        else:
            self.logger.debug("message_delivered", partition=msg.partition(), offset=msg.offset())

    def flush(self, timeout: float = 10.0) -> None:
        """Flush all pending messages."""
        remaining = self.producer.flush(timeout)
        if remaining > 0:
            raise KafkaProducerError(f"Failed to flush {remaining} messages")

    def close(self) -> None:
        """Close producer and release resources."""
        self.flush()
```

See `references/detailed-implementation.md` for complete producer adapter code with full error handling.

### 3. Anti-Corruption Layer

Translate domain models to message schemas:

```python
class OrderEventTranslator:
    """Translates domain Order to message schema.

    Anti-corruption layer that:
    - Converts domain entities to message DTOs
    - Handles type conversions (OrderId -> str, Money -> float)
    - Preserves timestamp information
    """

    @staticmethod
    def to_event_message(order: Order) -> OrderEventMessage:
        line_items = [
            LineItemEventMessage(
                line_item_id=item.line_item_id,
                product_id=str(item.product_id),
                product_title=str(item.product_title),
                quantity=item.quantity,
                price=float(item.price.amount),
            )
            for item in order.line_items
        ]

        return OrderEventMessage(
            order_id=str(order.order_id),
            created_at=order.created_at.isoformat(),
            customer_name=order.customer_name,
            line_items=line_items,
            total_price=float(order.total_price.amount),
        )
```

### 4. Use Case Integration

Integrate producer in extraction use case:

```python
class ExtractOrdersUseCase:
    def __init__(self, shopify_gateway, publisher):
        self.shopify_gateway = shopify_gateway
        self.publisher = publisher
        self.translator = OrderEventTranslator()

    async def execute(self) -> int:
        orders = await self.shopify_gateway.fetch_all_orders()

        for order in orders:
            event = self.translator.to_event_message(order)
            self.publisher.publish_order(event)

        self.publisher.flush()
        return len(orders)
```

### 5. Graceful Shutdown

Handle signals for clean shutdown:

```python
from contextlib import asynccontextmanager
import signal

@asynccontextmanager
async def managed_publisher(brokers, topic):
    """Context manager for producer lifecycle."""
    publisher = OrderEventPublisher(brokers, topic)

    def handle_shutdown(signum, frame):
        print(f"Received signal {signum}, shutting down...")
        publisher.close()

    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    try:
        yield publisher
    finally:
        publisher.close()
```

## Requirements

- `confluent-kafka>=2.3.0` - Production-grade Kafka client (10-20x faster than kafka-python)
- `msgspec>=0.18.6` - Ultra-fast serialization (10-20x faster than Pydantic)
- `structlog>=23.2.0` - Structured logging
- `opentelemetry-api>=1.22.0` - Distributed tracing
- Kafka/Redpanda broker (3.x or later for exactly-once semantics)
- Python 3.11+ with type checking

## Configuration Guidelines

**For Low Latency** (real-time):
```python
config = {
    "acks": "all",
    "linger.ms": 0,  # Send immediately
    "batch.size": 16384,  # Small batches
}
```

**For High Throughput** (batch processing):
```python
config = {
    "acks": "all",
    "linger.ms": 100,  # Wait 100ms for batching
    "batch.size": 131072,  # 128KB batches
    "compression.type": "lz4",  # Better compression
}
```

## Error Handling

**Transient Errors** (auto-retry by confluent-kafka):
- Network timeouts
- Broker temporarily unavailable
- Leader election

**Permanent Errors** (fail fast):
- Invalid topic
- Permission denied
- Schema validation failed

See `references/error-handling.md` for comprehensive error handling strategies including retry with exponential backoff, dead letter queues, circuit breaker patterns, and monitoring metrics.

## Integration Examples

See `examples/examples.md` for 10 production-ready examples:
1. Basic Order Publisher
2. Multi-Topic Publisher
3. Async Batch Publisher
4. Monitored Publisher
5. Context Manager Pattern
6. Testing with Mocks
7. Integration with Use Case
8. Performance Tuning
9. Low-Latency Configuration
10. Graceful Shutdown

## See Also

- `kafka-consumer-implementation` skill - For consuming events
- `kafka-schema-management` skill - For schema design
- `kafka-integration-testing` skill - For testing
- `references/detailed-implementation.md` - Complete implementation code
- `references/error-handling.md` - Error handling strategies
- `examples/examples.md` - Production-ready examples
