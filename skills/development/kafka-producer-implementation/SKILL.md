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

## Table of Contents

- [Purpose](#purpose)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Design Message Schema with msgspec](#step-1-design-message-schema-with-msgspec)
  - [Step 2: Create Producer Adapter with Error Handling](#step-2-create-producer-adapter-with-error-handling)
  - [Step 3: Implement Anti-Corruption Layer](#step-3-implement-anti-corruption-layer)
  - [Step 4: Configure in Bounded Context](#step-4-configure-in-bounded-context)
  - [Step 5: Handle Graceful Shutdown](#step-5-handle-graceful-shutdown)
- [Requirements](#requirements)
- [Error Handling Patterns](#error-handling-patterns)
- [Integration Examples](#integration-examples)
- [Supporting Resources](#supporting-resources)

## Purpose

This skill guides implementing production-grade Kafka producers that reliably publish domain events with high performance, type safety, and comprehensive error handling. It covers msgspec serialization, confluent-kafka configuration, OpenTelemetry tracing, and anti-corruption layer patterns for translating domain models to message schemas.

## Quick Start

Create a high-performance Kafka producer in 5 minutes:

1. **Define message schema** using msgspec immutable Struct:
```python
import msgspec

class OrderEventMessage(msgspec.Struct, frozen=True):
    """Order event message schema."""
    order_id: str
    created_at: str  # ISO 8601
    customer_name: str
    total_price: float
```

2. **Implement producer adapter**:
```python
from confluent_kafka import Producer
import msgspec
from structlog import get_logger

class OrderEventPublisher:
    """Publishes order events with msgspec serialization."""

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
        self.logger = get_logger(__name__)

    def publish(self, event: OrderEventMessage) -> None:
        """Publish event with order_id as partition key."""
        payload = self.encoder.encode(event)
        self.producer.produce(
            topic=self.topic,
            key=event.order_id.encode("utf-8"),
            value=payload,
        )
        self.producer.poll(0)

    def close(self) -> None:
        """Flush pending messages and close."""
        self.producer.flush(10.0)
```

3. **Use in extraction context**:
```python
publisher = OrderEventPublisher(["localhost:9092"], "orders")
publisher.publish(order_event)
publisher.close()
```

## Instructions

### Step 1: Design Message Schema with msgspec

Define immutable message schemas using `msgspec.Struct` for 10-20x faster serialization vs Pydantic:

```python
from __future__ import annotations
import msgspec

class LineItemEventMessage(msgspec.Struct, frozen=True):
    """Line item event schema for Kafka.

    Immutable struct with zero-copy deserialization.
    Uses msgspec for high-performance serialization.
    """
    line_item_id: str
    product_id: str
    product_title: str
    quantity: int
    price: float  # Use float, not Decimal


class OrderEventMessage(msgspec.Struct, frozen=True):
    """Order event message schema.

    Represents a complete order event for streaming.
    Includes all line items and pricing information.
    """
    order_id: str
    created_at: str  # ISO 8601 format string
    customer_name: str
    line_items: list[LineItemEventMessage]
    total_price: float
```

**Key Points:**
- Use `frozen=True` to create immutable structures
- Use primitive types (str, float, int) - not custom objects
- Store timestamps as ISO 8601 strings
- Arrays must have concrete element types
- msgspec produces/consumes JSON bytes automatically

### Step 2: Create Producer Adapter with Error Handling

Implement the producer adapter in your bounded context's adapters layer:

```python
from __future__ import annotations

from typing import Any

import msgspec
from confluent_kafka import KafkaError, KafkaException, Producer
from opentelemetry import trace
from structlog import get_logger

from app.extraction.adapters.kafka.schemas import OrderEventMessage


class KafkaProducerError(Exception):
    """Kafka producer operational error."""


class OrderEventPublisher:
    """Publishes order events to Kafka with high performance and reliability.

    Features:
    - msgspec serialization (10-20x faster than Pydantic)
    - confluent-kafka with production-grade configuration
    - OpenTelemetry distributed tracing
    - Comprehensive error handling and logging
    - Idempotent exactly-once semantics
    - Message ordering guarantees

    Configuration (from Kafka 3.x best practices):
    - acks=all: Wait for all in-sync replicas before returning
    - enable.idempotence=True: Exactly-once-per-send semantics
    - max.in.flight.requests.per.connection=1: Preserve message order
    - compression.type=snappy: Balance CPU/network
    - retries=5: Automatic retry on transient failures
    - enable.auto.commit=False: Manual offset management for consumers

    Args:
        brokers: List of Kafka broker addresses (e.g. ["localhost:9092"])
        topic: Kafka topic name for order events
        batch_size: Max bytes per batch (default: 16KB for low latency)
        linger_ms: Max time to wait for batch (default: 10ms)

    Example:
        >>> publisher = OrderEventPublisher(
        ...     brokers=["kafka:9092"],
        ...     topic="orders"
        ... )
        >>> publisher.publish_order(order_event)
        >>> publisher.flush()
        >>> publisher.close()
    """

    def __init__(
        self,
        brokers: list[str],
        topic: str,
        batch_size: int = 16384,
        linger_ms: int = 10,
    ) -> None:
        """Initialize Kafka producer with production configuration.

        Args:
            brokers: List of broker addresses
            topic: Topic name
            batch_size: Batch size in bytes
            linger_ms: Linger time in milliseconds

        Raises:
            KafkaProducerError: Initialization failed
        """
        self.topic = topic
        self.logger = get_logger(__name__)
        self.tracer = trace.get_tracer(__name__)
        self.encoder = msgspec.json.Encoder()

        config = {
            "bootstrap.servers": ",".join(brokers),
            "acks": "all",  # Wait for all in-sync replicas
            "retries": 5,  # Retry on transient failures
            "max.in.flight.requests.per.connection": 1,  # Preserve order
            "compression.type": "snappy",  # Good CPU/network balance
            "batch.size": batch_size,
            "linger.ms": linger_ms,
            "enable.idempotence": True,  # Exactly-once-per-send
        }

        try:
            self.producer = Producer(config)
            self.logger.info("kafka_producer_initialized", topic=topic, brokers=brokers)
        except KafkaException as e:
            self.logger.error("kafka_producer_init_failed", error=str(e))
            raise KafkaProducerError(f"Failed to initialize Kafka producer: {e}") from e

    def publish_order(self, event: OrderEventMessage) -> None:
        """Publish order event to Kafka topic.

        Transforms domain event to message schema and publishes with:
        - order_id as partition key (ensures ordering per order)
        - msgspec serialization (10-20x faster)
        - Distributed tracing span
        - Error handling and logging

        Args:
            event: Order event message to publish

        Raises:
            KafkaProducerError: Publication failed
        """
        with self.tracer.start_as_current_span("publish_order") as span:
            span.set_attribute("order_id", event.order_id)
            span.set_attribute("topic", self.topic)

            try:
                # Serialize with msgspec (10-20x faster than Pydantic JSON)
                payload = self.encoder.encode(event)

                # Use order_id as key to maintain order within partition
                self.producer.produce(
                    topic=self.topic,
                    key=event.order_id.encode("utf-8"),
                    value=payload,
                    on_delivery=self._delivery_callback,
                )

                # Poll to trigger delivery callbacks
                self.producer.poll(0)

                self.logger.info(
                    "order_event_published",
                    order_id=event.order_id,
                    topic=self.topic,
                )

            except (KafkaException, msgspec.EncodeError) as e:
                self.logger.error(
                    "order_event_publish_failed",
                    order_id=event.order_id,
                    error=str(e),
                )
                raise KafkaProducerError(f"Failed to publish order event: {e}") from e

    def _delivery_callback(self, err: KafkaError | None, msg: Any) -> None:
        """Handle delivery callback from Kafka.

        Called asynchronously after broker processes message.
        Logs success or failure for observability.

        Args:
            err: Error if delivery failed, None if successful
            msg: Message metadata (topic, partition, offset)
        """
        if err:
            self.logger.error(
                "message_delivery_failed",
                error=str(err),
                topic=msg.topic() if msg else None,
            )
        else:
            self.logger.debug(
                "message_delivered",
                topic=msg.topic(),
                partition=msg.partition(),
                offset=msg.offset(),
            )

    def flush(self, timeout: float = 10.0) -> None:
        """Flush all pending messages.

        Blocks until all outstanding messages are published or timeout.
        Call before graceful shutdown to ensure no message loss.

        Args:
            timeout: Flush timeout in seconds (default: 10s)

        Raises:
            KafkaProducerError: Flush timed out with messages remaining
        """
        self.logger.info("flushing_producer", timeout=timeout)
        remaining = self.producer.flush(timeout)
        if remaining > 0:
            raise KafkaProducerError(
                f"Failed to flush {remaining} messages within {timeout}s"
            )

    def close(self) -> None:
        """Close producer and release resources.

        Flushes pending messages with graceful timeout.
        Logs warnings but doesn't raise if flush times out.
        """
        try:
            self.flush()
            self.logger.info("kafka_producer_closed")
        except KafkaProducerError:
            self.logger.warning("flush_timeout_on_close")
```

### Step 3: Implement Anti-Corruption Layer

Create adapter to translate domain models to message schemas:

```python
from app.extraction.domain.entities import Order
from app.extraction.adapters.kafka.schemas import (
    LineItemEventMessage,
    OrderEventMessage,
)


class OrderEventTranslator:
    """Translates domain Order to message schema.

    Anti-corruption layer that:
    - Converts domain entities to message DTOs
    - Handles type conversions (OrderId -> str, Money -> float)
    - Preserves timestamp information
    - Validates translation completeness
    """

    @staticmethod
    def to_event_message(order: Order) -> OrderEventMessage:
        """Convert domain Order to publishable event message.

        Args:
            order: Domain order aggregate root

        Returns:
            OrderEventMessage ready for Kafka publication
        """
        line_items = [
            LineItemEventMessage(
                line_item_id=item.line_item_id,
                product_id=str(item.product_id),
                product_title=str(item.product_title),
                quantity=item.quantity,
                price=float(item.price.amount),  # Convert Decimal to float
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

### Step 4: Configure in Bounded Context

Set up producer in your extraction context's use case:

```python
from app.extraction.adapters.kafka.producer import OrderEventPublisher
from app.extraction.application.use_cases import ExtractOrdersUseCase


class ExtractOrdersUseCase:
    """Use case for extracting and publishing orders.

    Coordinates:
    1. Fetching orders from Shopify (via ShopifyGateway)
    2. Translating to event messages (via OrderEventTranslator)
    3. Publishing to Kafka (via OrderEventPublisher)
    """

    def __init__(
        self,
        shopify_gateway: ShopifyGateway,
        publisher: OrderEventPublisher,
    ) -> None:
        self.shopify_gateway = shopify_gateway
        self.publisher = publisher
        self.translator = OrderEventTranslator()

    async def execute(self) -> int:
        """Extract orders and publish to Kafka.

        Returns:
            Number of orders published
        """
        # Fetch all orders (domain layer)
        orders = await self.shopify_gateway.fetch_all_orders()

        # Publish each order
        published_count = 0
        for order in orders:
            event = self.translator.to_event_message(order)
            self.publisher.publish_order(event)
            published_count += 1

        # Ensure all messages sent before returning
        self.publisher.flush()
        return published_count
```

### Step 5: Handle Graceful Shutdown

Implement signal handlers for clean shutdown:

```python
import asyncio
import signal
from contextlib import asynccontextmanager

from app.extraction.adapters.kafka.producer import OrderEventPublisher


@asynccontextmanager
async def managed_publisher(brokers: list[str], topic: str):
    """Context manager for producer lifecycle.

    Ensures proper cleanup on shutdown.
    """
    publisher = OrderEventPublisher(brokers, topic)

    def handle_shutdown(signum: int, frame: Any) -> None:
        print(f"Received signal {signum}, shutting down...")
        publisher.close()

    # Register signal handlers
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    try:
        yield publisher
    finally:
        publisher.close()


# In extractor_main.py:
async def main() -> None:
    async with managed_publisher(
        brokers=["kafka:9092"],
        topic="orders"
    ) as publisher:
        use_case = ExtractOrdersUseCase(
            shopify_gateway=ShopifyGateway(...),
            publisher=publisher,
        )
        count = await use_case.execute()
        print(f"Published {count} orders")
```

## Requirements

- `confluent-kafka>=2.3.0` - Production-grade Kafka client (C-based, 10-20x faster than kafka-python)
- `msgspec>=0.18.6` - Ultra-fast serialization (10-20x faster than Pydantic)
- `structlog>=23.2.0` - Structured logging with context
- `opentelemetry-api>=1.22.0` - Distributed tracing
- Kafka/Redpanda broker running (3.x or later for exactly-once semantics)
- Python 3.11+ with type checking enabled

## Error Handling Patterns

See [`references/error-handling.md`](./references/error-handling.md) for comprehensive error handling strategies including:

- **Error Classification**: Distinguish transient failures (retry) from permanent failures (fail fast)
- **Retry with Exponential Backoff**: Automatic retry on transient failures with configurable backoff
- **Dead Letter Queue (DLQ)**: Send unrecoverable messages to DLQ for manual inspection
- **Circuit Breaker Pattern**: Prevent cascading failures when broker is persistently unavailable
- **Idempotent Publishing**: Ensure exactly-once delivery despite retries
- **Monitoring & Alerting**: Key metrics and health checks for producer health

## Integration Examples

See [`examples/examples.md`](./examples/examples.md) for 10 complete, production-ready examples:

1. **Basic Order Publisher** - Simple single-topic producer with error handling
2. **Multi-Topic Publisher** - Route different event types to different topics
3. **Async Batch Publisher** - Buffer and batch messages for efficiency
4. **Monitored Publisher** - Collect comprehensive performance metrics
5. **Context Manager** - Ensure proper cleanup with context managers
6. **Testing with Mocks** - Unit test producer without Kafka
7. **Integration with Use Case** - Use producer in extraction use case
8. **Performance Tuning** - Optimize for throughput vs latency
9. **Low-Latency Configuration** - Minimize publish latency
10. **Graceful Shutdown** - Handle SIGTERM and SIGINT signals

## Supporting Resources

| Resource | Purpose |
|----------|---------|
| [`references/error-handling.md`](./references/error-handling.md) | Comprehensive error handling patterns and monitoring strategies |
| [`examples/examples.md`](./examples/examples.md) | 10 production-ready code examples demonstrating common scenarios |
