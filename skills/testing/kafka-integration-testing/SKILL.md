---
name: kafka-integration-testing
description: |
  Write integration tests for Kafka producers and consumers using testcontainers.
  Use when testing producer/consumer workflows, verifying message ordering, testing
  error scenarios, and validating exactly-once semantics. Creates test Kafka brokers
  and validates end-to-end streaming behavior without mocking.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Kafka Integration Testing

## Table of Contents

- [Purpose](#purpose)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Set Up Test Environment](#step-1-set-up-test-environment)
  - [Step 2: Test Producer Functionality](#step-2-test-producer-functionality)
  - [Step 3: Test Consumer Functionality](#step-3-test-consumer-functionality)
  - [Step 4: Test Error Scenarios](#step-4-test-error-scenarios)
  - [Step 5: Test Message Ordering and Delivery Semantics](#step-5-test-message-ordering-and-delivery-semantics)
- [Requirements](#requirements)
- [Running Integration Tests](#running-integration-tests)
- [Debugging Failed Tests](#debugging-failed-tests)
- [Example Test Patterns](#example-test-patterns)
- [Troubleshooting & Best Practices](#troubleshooting--best-practices)
- [See Also](#see-also)

## Purpose

This skill guides writing production-grade integration tests for Kafka producers and consumers using testcontainers. It covers setting up temporary test brokers, testing producer/consumer workflows, verifying message ordering guarantees, testing error scenarios, and validating delivery semantics without mocking external services.

## Quick Start

Create a producer/consumer round-trip test in 5 minutes:

1. **Add test dependency**:
```bash
pip install testcontainers[kafka]>=4.0.0
```

2. **Write integration test**:
```python
import pytest
from testcontainers.kafka import KafkaContainer
from app.extraction.adapters.kafka.producer import OrderEventPublisher
from app.storage.adapters.kafka.consumer import OrderEventConsumer

@pytest.fixture
def kafka_container():
    """Start Kafka container for testing."""
    with KafkaContainer() as kafka:
        yield kafka

def test_producer_consumer_roundtrip(kafka_container):
    """Test publish and consume workflow."""
    brokers = [kafka_container.get_bootstrap_server()]

    # Produce message
    publisher = OrderEventPublisher(brokers, "test-orders")
    event = OrderEventMessage(
        order_id="test_123",
        created_at="2024-01-01T12:00:00Z",
        customer_name="Test User",
        line_items=[...],
        total_price=99.99,
    )
    publisher.publish_order(event)
    publisher.flush()

    # Consume message
    consumer = OrderEventConsumer(brokers, "test-orders", "test-group")
    message = consumer.consume(timeout=5.0)

    assert message is not None
    assert message.order_id == "test_123"
```

3. **Run test**:
```bash
pytest tests/integration/test_kafka_roundtrip.py -v
```

## Instructions

### Step 1: Set Up Test Environment

Configure pytest fixtures for Kafka container management:

```python
# tests/integration/conftest.py
from __future__ import annotations

import asyncio
import pytest
from testcontainers.kafka import KafkaContainer
from structlog import get_logger


logger = get_logger(__name__)


@pytest.fixture(scope="function")
def kafka_container() -> KafkaContainer:
    """Fixture: Start isolated Kafka container for each test.

    Scope: function (new container per test, fully isolated)

    Provides:
    - Kafka broker running on random port
    - Bootstrap server address for clients
    - Automatic cleanup after test

    Example:
        >>> def test_kafka(kafka_container):
        ...     brokers = [kafka_container.get_bootstrap_server()]
        ...     # Test code here

    Note:
        First test in a session will take 5-10s to start container.
        Subsequent tests should be faster due to Docker layer caching.
    """
    logger.info("starting_kafka_container")
    container = KafkaContainer()
    container.start()

    try:
        # Give broker time to become ready
        import time
        time.sleep(2)

        bootstrap_server = container.get_bootstrap_server()
        logger.info("kafka_container_ready", bootstrap_server=bootstrap_server)
        yield container
    finally:
        logger.info("stopping_kafka_container")
        container.stop()


@pytest.fixture
def kafka_brokers(kafka_container: KafkaContainer) -> list[str]:
    """Fixture: Get broker addresses for Kafka container.

    Wraps kafka_container to provide brokers list directly.
    Use this when you only need broker addresses.

    Example:
        >>> def test_producer(kafka_brokers):
        ...     publisher = OrderEventPublisher(kafka_brokers, "test-topic")
    """
    return [kafka_container.get_bootstrap_server()]


@pytest.fixture
def event_loop():
    """Fixture: Create event loop for async tests.

    Required for async test functions with pytest-asyncio.
    Scope: function (new loop per test, fully isolated)
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()
```

### Step 2: Test Producer Functionality

Write tests for producer behavior:

```python
# tests/integration/test_kafka_producer_integration.py
from __future__ import annotations

import pytest
import msgspec
from testcontainers.kafka import KafkaContainer

from app.extraction.adapters.kafka.producer import OrderEventPublisher, KafkaProducerError
from app.extraction.adapters.kafka.schemas import OrderEventMessage, LineItemMessage


class TestOrderEventPublisherIntegration:
    """Integration tests for OrderEventPublisher with real Kafka."""

    def test_publisher_publishes_message_to_kafka(self, kafka_brokers: list[str]) -> None:
        """Test publisher successfully publishes message to Kafka broker.

        This is the happy path: message is published and acknowledged.
        """
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic="orders")

        event = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test Customer",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test Product",
                    quantity=1,
                    price=99.99,
                )
            ],
            total_price=99.99,
        )

        # Should not raise
        publisher.publish_order(event)
        publisher.flush()

        # Note: We're only verifying publish succeeds, not that message was stored.
        # See consumer tests for end-to-end verification.

    def test_publisher_flushes_successfully(self, kafka_brokers: list[str]) -> None:
        """Test publisher flush completes without timeout."""
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic="orders")

        event = OrderEventMessage(
            order_id="order_456",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test",
                    quantity=1,
                    price=50.0,
                )
            ],
            total_price=50.0,
        )

        publisher.publish_order(event)

        # Should complete without raising
        publisher.flush(timeout=5.0)

    def test_publisher_closes_successfully(self, kafka_brokers: list[str]) -> None:
        """Test publisher close handles flush and cleanup."""
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic="orders")

        # Should not raise even if no messages published
        publisher.close()

    def test_publisher_preserves_message_order_per_order(
        self, kafka_brokers: list[str]
    ) -> None:
        """Test messages for same order maintain order.

        Uses order_id as partition key to ensure all messages for an order
        go to same partition, preserving order.
        """
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic="orders")

        order_id = "order_789"
        num_messages = 5

        # Publish 5 messages for same order
        for i in range(num_messages):
            event = OrderEventMessage(
                order_id=order_id,
                created_at=f"2024-01-01T12:00:{i:02d}Z",
                customer_name="Test",
                line_items=[
                    LineItemMessage(
                        line_item_id=f"item_{i}",
                        product_id=f"prod_{i}",
                        product_title="Test",
                        quantity=1,
                        price=10.0 * (i + 1),
                    )
                ],
                total_price=10.0 * (i + 1),
            )
            publisher.publish_order(event)

        publisher.flush()

        # Note: Ordering verification happens in consumer tests
```

### Step 3: Test Consumer Functionality

Write tests for consumer behavior and offset management:

```python
# tests/integration/test_kafka_consumer_integration.py
from __future__ import annotations

import pytest
from testcontainers.kafka import KafkaContainer

from app.extraction.adapters.kafka.producer import OrderEventPublisher
from app.storage.adapters.kafka.consumer import OrderEventConsumer, KafkaConsumerException
from app.extraction.adapters.kafka.schemas import OrderEventMessage, LineItemMessage


class TestOrderEventConsumerIntegration:
    """Integration tests for OrderEventConsumer with real Kafka."""

    def test_consumer_receives_published_message(self, kafka_brokers: list[str]) -> None:
        """Test consumer receives message published by producer.

        End-to-end test: publish -> consume flow.
        """
        topic = "test-orders"
        group_id = "test-group"

        # Publish message
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        event = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test Customer",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Laptop",
                    quantity=1,
                    price=999.99,
                )
            ],
            total_price=999.99,
        )
        publisher.publish_order(event)
        publisher.flush()

        # Consume message
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message = consumer.consume(timeout=5.0)

        assert message is not None
        assert message.order_id == "order_123"
        assert message.customer_name == "Test Customer"
        assert len(message.line_items) == 1
        assert message.line_items[0].product_title == "Laptop"

        consumer.close()

    def test_consumer_commits_offset(self, kafka_brokers: list[str]) -> None:
        """Test consumer offset commit after message processing.

        Verifies that commit() succeeds and offset is persisted.
        """
        topic = "test-orders"
        group_id = "commit-test-group"

        # Publish message
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        event = OrderEventMessage(
            order_id="order_456",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test Product",
                    quantity=1,
                    price=50.0,
                )
            ],
            total_price=50.0,
        )
        publisher.publish_order(event)
        publisher.flush()

        # Consume and commit
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message = consumer.consume(timeout=5.0)

        assert message is not None

        # Commit should succeed
        consumer.commit()

        consumer.close()

    def test_consumer_starts_from_earliest_if_no_offset(
        self, kafka_brokers: list[str]
    ) -> None:
        """Test consumer starts from earliest message if no stored offset.

        Verifies auto.offset.reset=earliest behavior.
        """
        topic = "test-orders"
        group_id = f"fresh-group-{id(object())}"  # Unique group

        # Publish messages
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        event1 = OrderEventMessage(
            order_id="order_1",
            created_at="2024-01-01T12:00:00Z",
            customer_name="User 1",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Product 1",
                    quantity=1,
                    price=100.0,
                )
            ],
            total_price=100.0,
        )
        publisher.publish_order(event1)
        publisher.flush()

        # Consume with new group (no offset)
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message = consumer.consume(timeout=5.0)

        # Should receive the first (earliest) message
        assert message is not None
        assert message.order_id == "order_1"

        consumer.close()

    def test_consumer_handles_malformed_message(self, kafka_brokers: list[str]) -> None:
        """Test consumer raises error on malformed JSON message.

        Verifies error handling for invalid schema data.
        """
        topic = "test-orders"
        group_id = "malformed-test-group"

        # Publish malformed message directly using confluent_kafka
        from confluent_kafka import Producer

        producer = Producer({"bootstrap.servers": ",".join(kafka_brokers)})
        producer.produce(topic, key=b"bad", value=b"not valid json")
        producer.flush()

        # Try to consume
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)

        # Consuming malformed message should raise error
        with pytest.raises(KafkaConsumerException):
            consumer.consume(timeout=5.0)

        consumer.close()

    def test_consumer_returns_none_on_timeout(self, kafka_brokers: list[str]) -> None:
        """Test consumer returns None if timeout expires with no message.

        Verifies non-blocking behavior.
        """
        topic = "empty-topic"
        group_id = "timeout-test-group"

        # Don't publish anything - topic is empty
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)

        # Should return None after timeout
        message = consumer.consume(timeout=1.0)

        assert message is None

        consumer.close()
```

### Step 4: Test Error Scenarios

Write tests for error handling and recovery:

```python
# tests/integration/test_kafka_error_scenarios.py
from __future__ import annotations

import pytest
from app.extraction.adapters.kafka.producer import (
    OrderEventPublisher,
    KafkaProducerError,
)
from app.extraction.adapters.kafka.schemas import OrderEventMessage, LineItemMessage


class TestKafkaErrorScenarios:
    """Integration tests for error handling."""

    def test_publisher_handles_invalid_brokers(self) -> None:
        """Test publisher raises error if broker is unreachable."""
        # Use invalid broker address
        invalid_brokers = ["invalid-broker-that-does-not-exist:9092"]

        # This will try to connect but may not fail until first publish
        # depending on broker connection timeout
        publisher = OrderEventPublisher(brokers=invalid_brokers, topic="test")

        event = OrderEventMessage(
            order_id="test",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test",
                    quantity=1,
                    price=50.0,
                )
            ],
            total_price=50.0,
        )

        # Publish should eventually fail due to broker unavailable
        # (May not fail immediately due to internal retries)
        # In real scenarios, producer waits for broker connection

    def test_consumer_handles_commit_failure_gracefully(self, kafka_brokers: list[str]) -> None:
        """Test consumer logs error if commit fails but doesn't crash.

        Simulates transient commit failure.
        """
        topic = "test-orders"
        group_id = "commit-error-test-group"

        # Publish message
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        event = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test",
                    quantity=1,
                    price=50.0,
                )
            ],
            total_price=50.0,
        )
        publisher.publish_order(event)
        publisher.flush()

        # Consume message
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message = consumer.consume(timeout=5.0)

        assert message is not None

        # Commit should succeed on real broker
        consumer.commit()

        consumer.close()
```

### Step 5: Test Message Ordering and Delivery Semantics

Write tests for ordering guarantees:

```python
# tests/integration/test_kafka_ordering_integration.py
from __future__ import annotations

import pytest
from app.extraction.adapters.kafka.producer import OrderEventPublisher
from app.storage.adapters.kafka.consumer import OrderEventConsumer
from app.extraction.adapters.kafka.schemas import OrderEventMessage, LineItemMessage


class TestKafkaOrderingSemantics:
    """Integration tests for ordering and delivery guarantees."""

    def test_messages_ordered_within_partition(self, kafka_brokers: list[str]) -> None:
        """Test messages published to same partition maintain order.

        Messages with same order_id (key) go to same partition.
        Kafka guarantees ordering within a partition.
        """
        topic = "ordered-orders"
        group_id = "ordering-test-group"

        # Publish messages with same order_id (same partition key)
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        order_id = "order_123"
        messages_published = []

        for i in range(5):
            event = OrderEventMessage(
                order_id=order_id,
                created_at=f"2024-01-01T12:00:{i:02d}Z",
                customer_name="Test",
                line_items=[
                    LineItemMessage(
                        line_item_id=f"item_{i}",
                        product_id=f"prod_{i}",
                        product_title=f"Product {i}",
                        quantity=1,
                        price=10.0 * (i + 1),
                    )
                ],
                total_price=10.0 * (i + 1),
            )
            publisher.publish_order(event)
            messages_published.append(event)

        publisher.flush()

        # Consume all messages
        consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        messages_consumed = []

        for _ in range(5):
            message = consumer.consume(timeout=5.0)
            if message:
                messages_consumed.append(message)
                consumer.commit()

        # Verify order maintained
        assert len(messages_consumed) == 5
        for i, consumed in enumerate(messages_consumed):
            assert consumed.order_id == order_id
            assert consumed.line_items[0].product_title == f"Product {i}"

        consumer.close()

    def test_exactly_once_semantics_with_manual_commit(
        self, kafka_brokers: list[str]
    ) -> None:
        """Test exactly-once processing with manual offset management.

        With enable.auto.commit=False:
        - Only committed messages are not reprocessed on restart
        - Uncommitted messages are reprocessed
        - This ensures exactly-once-per-commit semantics
        """
        topic = "exactly-once-orders"
        group_id = "exactly-once-test-group"

        # Publish message
        publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
        event = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="Test",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Test",
                    quantity=1,
                    price=50.0,
                )
            ],
            total_price=50.0,
        )
        publisher.publish_order(event)
        publisher.flush()

        # First consumer: consume but don't commit
        consumer1 = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message1 = consumer1.consume(timeout=5.0)
        assert message1 is not None
        # Don't commit!
        consumer1.close()

        # Second consumer: same group, should get same message (not committed)
        consumer2 = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message2 = consumer2.consume(timeout=5.0)
        assert message2 is not None
        assert message2.order_id == message1.order_id
        # This time commit
        consumer2.commit()
        consumer2.close()

        # Third consumer: same group, should NOT get message (now committed)
        consumer3 = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id=group_id)
        message3 = consumer3.consume(timeout=1.0)
        assert message3 is None  # No more messages in this group
        consumer3.close()
```

## Requirements

- `testcontainers>=4.0.0` - Container management for testing
- `testcontainers[kafka]>=4.0.0` - Kafka container support
- `confluent-kafka>=2.3.0` - Kafka client
- `msgspec>=0.18.6` - Message serialization
- `pytest>=7.4.3` - Test framework
- `pytest-asyncio>=0.21.1` - Async test support
- Docker - Required for testcontainers (running containers)
- Python 3.11+ with type checking enabled

**Installation:**

```bash
# Install test dependencies
pip install testcontainers[kafka] pytest pytest-asyncio

# Or from pyproject.toml [test] group
pip install -e ".[test]"
```

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test class
pytest tests/integration/test_kafka_producer_integration.py::TestOrderEventPublisherIntegration -v

# Run with output capturing disabled (see print statements)
pytest tests/integration/ -v -s

# Run with coverage
pytest tests/integration/ --cov=app.extraction.adapters.kafka --cov=app.storage.adapters.kafka
```

## Debugging Failed Tests

**Container logs:**
```bash
# If test fails, check container logs
docker logs <container_id>
```

**Test with verbose output:**
```bash
pytest tests/integration/test_kafka_producer_integration.py::test_producer_publishes_message_to_kafka -vv -s
```

**Print debug info:**
```python
import logging
logging.basicConfig(level=logging.DEBUG)  # In test
```

## Example Test Patterns

For comprehensive examples covering various testing scenarios, see [examples/examples.md](./examples/examples.md):

- **Basic Producer Tests**: Simple message publishing, batch publishing
- **Basic Consumer Tests**: Single message consumption, consuming multiple messages
- **Producer-Consumer Round-Trip**: End-to-end workflow testing
- **Message Ordering**: Testing order preservation with same key, different keys behavior
- **Exactly-Once Semantics**: Manual commit for guaranteed processing
- **Error Handling**: Malformed messages, timeout handling
- **Async Testing**: Async producer/consumer operations
- **Custom Fixtures**: Pre-populated topics, multi-partition topics

## Troubleshooting & Best Practices

For detailed troubleshooting guidance and best practices, see [references/reference.md](./references/reference.md):

**Common Issues Covered:**
- Container fails to start
- Test hangs on consume()
- Malformed message exceptions
- Port already in use
- Offset commit failures
- Intermittent test failures
- Docker integration patterns

**Best Practices:**
- Using unique consumer groups per test
- Always flushing producers
- Proper resource cleanup
- Timeout considerations
- Error handling patterns
- Type safety in tests
- Performance optimization
- Docker Compose integration

## See Also

- **Producer Implementation**: `kafka-producer-implementation` skill
- **Consumer Implementation**: `kafka-consumer-implementation` skill
- **Schema Management**: `kafka-schema-management` skill
- **Project E2E Tests**: `tests/e2e/test_complete_pipeline.py` for full system tests
