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

## Purpose

Write production-grade integration tests for Kafka producers and consumers using testcontainers. Covers setting up temporary test brokers, testing producer/consumer workflows, verifying message ordering guarantees, testing error scenarios, and validating delivery semantics without mocking external services.


## When to Use This Skill

Use when testing Kafka producer/consumer workflows end-to-end with "test Kafka integration", "verify message ordering", "test Kafka roundtrip", or "validate exactly-once semantics".

Do NOT use for unit testing with mocked Kafka (use `pytest-adapter-integration-testing`), implementing producers/consumers (use respective `kafka-*-implementation` skills), or schema validation (use `kafka-schema-management`).
## Quick Start

Create a producer/consumer round-trip test in 3 steps:

1. **Add dependency**:
```bash
pip install testcontainers[kafka]>=4.0.0
```

2. **Write test**:
```python
import pytest
from testcontainers.kafka import KafkaContainer
from app.extraction.adapters.kafka.producer import OrderEventPublisher
from app.storage.adapters.kafka.consumer import OrderEventConsumer

@pytest.fixture
def kafka_container():
    with KafkaContainer() as kafka:
        yield kafka

def test_producer_consumer_roundtrip(kafka_container):
    brokers = [kafka_container.get_bootstrap_server()]

    # Produce
    publisher = OrderEventPublisher(brokers, "test-orders")
    event = OrderEventMessage(order_id="test_123", ...)
    publisher.publish_order(event)
    publisher.flush()

    # Consume
    consumer = OrderEventConsumer(brokers, "test-orders", "test-group")
    message = consumer.consume(timeout=5.0)

    assert message is not None
    assert message.order_id == "test_123"
```

3. **Run**:
```bash
pytest tests/integration/test_kafka_roundtrip.py -v
```

## Implementation Steps

### 1. Set Up Test Environment

Configure pytest fixtures for Kafka container management:

```python
# tests/integration/conftest.py
import pytest
from testcontainers.kafka import KafkaContainer

@pytest.fixture(scope="function")
def kafka_container() -> KafkaContainer:
    """Start isolated Kafka container for each test."""
    container = KafkaContainer()
    container.start()

    try:
        import time
        time.sleep(2)  # Give broker time to become ready
        yield container
    finally:
        container.stop()

@pytest.fixture
def kafka_brokers(kafka_container: KafkaContainer) -> list[str]:
    """Get broker addresses."""
    return [kafka_container.get_bootstrap_server()]
```

### 2. Test Producer Functionality

```python
def test_publisher_publishes_message_to_kafka(kafka_brokers: list[str]) -> None:
    """Test publisher successfully publishes message."""
    publisher = OrderEventPublisher(brokers=kafka_brokers, topic="orders")

    event = OrderEventMessage(order_id="order_123", ...)
    publisher.publish_order(event)
    publisher.flush()
```

### 3. Test Consumer Functionality

```python
def test_consumer_receives_published_message(kafka_brokers: list[str]) -> None:
    """Test consumer receives published message."""
    topic = "test-orders"

    # Publish
    publisher = OrderEventPublisher(brokers=kafka_brokers, topic=topic)
    publisher.publish_order(event)
    publisher.flush()

    # Consume
    consumer = OrderEventConsumer(brokers=kafka_brokers, topic=topic, group_id="test-group")
    message = consumer.consume(timeout=5.0)

    assert message is not None
    assert message.order_id == "order_123"
    consumer.close()
```

### 4. Test Error Scenarios

```python
def test_consumer_handles_malformed_message(kafka_brokers: list[str]) -> None:
    """Test consumer raises error on malformed JSON."""
    from confluent_kafka import Producer

    producer = Producer({"bootstrap.servers": ",".join(kafka_brokers)})
    producer.produce("test-orders", key=b"bad", value=b"not valid json")
    producer.flush()

    consumer = OrderEventConsumer(brokers=kafka_brokers, topic="test-orders", group_id="test-group")
    with pytest.raises(KafkaConsumerException):
        consumer.consume(timeout=5.0)
```

### 5. Test Message Ordering

```python
def test_messages_ordered_within_partition(kafka_brokers: list[str]) -> None:
    """Test messages with same key maintain order."""
    publisher = OrderEventPublisher(brokers=kafka_brokers, topic="ordered-orders")
    order_id = "order_123"

    # Publish 5 messages with same order_id (same partition key)
    for i in range(5):
        event = OrderEventMessage(order_id=order_id, created_at=f"2024-01-01T12:00:{i:02d}Z", ...)
        publisher.publish_order(event)
    publisher.flush()

    # Consume and verify order
    consumer = OrderEventConsumer(brokers=kafka_brokers, topic="ordered-orders", group_id="test-group")
    for i in range(5):
        message = consumer.consume(timeout=5.0)
        assert message is not None
        assert message.created_at == f"2024-01-01T12:00:{i:02d}Z"
```

## Requirements

- `testcontainers>=4.0.0` - Container management
- `testcontainers[kafka]>=4.0.0` - Kafka container support
- `confluent-kafka>=2.3.0` - Kafka client
- `msgspec>=0.18.6` - Message serialization
- `pytest>=7.4.3` - Test framework
- `pytest-asyncio>=0.21.1` - Async test support
- Docker - Required for testcontainers
- Python 3.11+ with type checking

## Running Tests

```bash
# All integration tests
pytest tests/integration/ -v

# Specific test class
pytest tests/integration/test_kafka_producer_integration.py::TestOrderEventPublisherIntegration -v

# With coverage
pytest tests/integration/ --cov=app.extraction.adapters.kafka --cov=app.storage.adapters.kafka
```

## Debugging Failed Tests

**Container logs**:
```bash
docker logs <container_id>
```

**Verbose output**:
```bash
pytest tests/integration/test_kafka.py::test_name -vv -s
```

## Common Issues

**Container fails to start**: Check Docker is running and has available resources.

**Test hangs on consume()**: Verify publisher called `flush()` before consuming.

**Malformed message exceptions**: Check message schema matches expected structure.

**Port already in use**: Testcontainers uses random ports, conflicts are rare.

**Intermittent failures**: Add 2s sleep after container start for broker readiness.

## Best Practices

- Use unique consumer groups per test for isolation
- Always flush producers before consuming
- Clean up resources with try/finally or fixtures
- Use timeouts on consume() to avoid hanging tests
- Test with real Kafka (don't mock) for confidence

## Example Test Patterns

See `examples/examples.md` for comprehensive examples:
- Basic producer/consumer tests
- Round-trip workflow testing
- Message ordering verification
- Exactly-once semantics validation
- Error handling scenarios
- Async testing patterns
- Custom fixtures for pre-populated topics

## Troubleshooting Guide

See `references/reference.md` for detailed troubleshooting:
- Container startup issues
- Network configuration
- Performance optimization
- Docker Compose integration
- CI/CD pipeline setup

## See Also

- `kafka-producer-implementation` skill - Producer implementation
- `kafka-consumer-implementation` skill - Consumer implementation
- `kafka-schema-management` skill - Schema design
- `examples/examples.md` - Complete test examples
- `references/reference.md` - Troubleshooting guide
