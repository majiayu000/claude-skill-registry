---
name: clickhouse-kafka-validation
description: |
  Implement defense-in-depth validation patterns for ClickHouse + Kafka data pipelines.
  Covers producer validation (msgspec schemas), consumer validation (anti-corruption layers),
  ClickHouse error streaming (kafka_handle_error_mode='stream'), idempotency with ReplacingMergeTree,
  schema evolution, and monitoring. Use when implementing data pipelines, handling Kafka errors,
  setting up validation layers, managing duplicates/idempotency, or monitoring Kafka consumption.
allowed-tools: Read, Bash, Grep
---

# ClickHouse + Kafka Validation

## Purpose

This skill provides production-ready patterns for implementing defense-in-depth validation in ClickHouse + Kafka data pipelines. It ensures data integrity at both producer and consumer boundaries, handles errors without blocking consumption, automatically deduplicates messages, and provides comprehensive monitoring and observability.

## Quick Start

### 1. Enable Error Streaming in ClickHouse (30 seconds)

```sql
-- Add error streaming to your Kafka table
ALTER TABLE kafka_orders
MODIFY SETTING kafka_handle_error_mode = 'stream';

-- Create error capture table
CREATE TABLE IF NOT EXISTS kafka_errors (
    topic String,
    partition Int64,
    offset Int64,
    raw_message String,
    error_message String,
    captured_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (topic, partition, offset)
PARTITION BY toYYYYMM(captured_at)
TTL captured_at + INTERVAL 30 DAY;

-- Capture errors via materialized view
CREATE MATERIALIZED VIEW IF NOT EXISTS kafka_errors_mv
TO kafka_errors AS
SELECT
    _topic AS topic,
    _partition AS partition,
    _offset AS offset,
    _raw_message AS raw_message,
    _error AS error_message
FROM kafka_orders
WHERE length(_error) > 0;
```

### 2. Set Up Idempotency with ReplacingMergeTree

```sql
-- Target table with automatic deduplication
CREATE TABLE IF NOT EXISTS orders (
    order_id String,
    created_at DateTime,
    line_items Array(Tuple(
        line_item_id String,
        product_id String,
        product_title String,
        quantity Int32
    )),
    inserted_at DateTime
)
ENGINE = ReplacingMergeTree()
ORDER BY (order_id, created_at)
PARTITION BY toYYYYMM(created_at);

-- Valid message transformation
CREATE MATERIALIZED VIEW IF NOT EXISTS orders_mv
TO orders AS
SELECT
    order_id,
    parseDateTime64BestEffort(created_at) AS created_at,
    line_items,
    parseDateTime64BestEffort(inserted_at) AS inserted_at
FROM kafka_orders
WHERE length(_error) = 0;
```

### 3. Validate at Producer (Python - msgspec)

```python
# app/extraction/adapters/kafka/schemas.py
from __future__ import annotations

import msgspec
from datetime import datetime, timezone


class LineItemMessage(msgspec.Struct, frozen=True):
    """Type-safe schema for line items."""
    line_item_id: str
    product_id: str
    product_title: str
    quantity: int


class OrderMessage(msgspec.Struct, frozen=True):
    """Type-safe schema for orders."""
    order_id: str
    created_at: str  # ISO format
    line_items: list[LineItemMessage]
    inserted_at: str  # ISO format


# Publish with automatic validation
from app.core.monitoring.otel_logger import logger, traced

logger = logger(__name__)


@traced
def publish_order(order: Order, producer: KafkaProducer) -> None:
    """Publish order with msgspec validation."""
    try:
        message = OrderMessage(
            order_id=str(order.order_id),
            created_at=order.created_at.isoformat(),
            line_items=[
                LineItemMessage(
                    line_item_id=item.line_item_id,
                    product_id=str(item.product_id),
                    product_title=str(item.product_title),
                    quantity=item.quantity
                )
                for item in order.line_items
            ],
            inserted_at=datetime.now(timezone.utc).isoformat()
        )

        payload = msgspec.json.encode(message)
        producer.produce(topic="shopify-orders", value=payload)
        logger.info("order_published", order_id=order.order_id)

    except msgspec.ValidationError as e:
        logger.error("order_validation_failed", error=str(e), order_id=order.order_id)
        raise InvalidOrderException(f"Order validation failed: {e}") from e
```

### 4. Validate at Consumer (Python - Anti-Corruption Layer)

```python
# app/storage/adapters/anti_corruption.py
from __future__ import annotations

import msgspec
from datetime import datetime
from app.core.monitoring.otel_logger import logger, traced
from app.storage.adapters.kafka.schemas import OrderMessage
from app.storage.domain.entities import Order, OrderItem

logger = logger(__name__)


class KafkaMessageTranslator:
    """Anti-corruption layer with defense-in-depth validation."""


    @staticmethod
    @traced
    def translate_order(message: OrderMessage) -> Order:
        """Translate and validate Kafka message.

        Raises:
            DataIntegrityException: If message is invalid
        """
        try:
            # Validation 1: Timestamp format validation
            created_at = _parse_iso_timestamp(message.created_at)
            inserted_at = _parse_iso_timestamp(message.inserted_at)

            # Validation 2: Business rule validation
            if not message.line_items:
                raise ValueError("Order must have at least one line item")

            if len(message.order_id) == 0:
                raise ValueError("Order ID cannot be empty")

            # Validation 3: Line item constraint validation
            line_items: list[OrderItem] = []
            for item in message.line_items:
                if item.quantity <= 0:
                    raise ValueError(f"Invalid quantity: {item.quantity}")
                if not item.product_title.strip():
                    raise ValueError("Product title cannot be empty")

                line_items.append(OrderItem(
                    line_item_id=item.line_item_id,
                    product_id=item.product_id,
                    product_title=item.product_title,
                    quantity=item.quantity
                ))

            # All validations passed - translate to domain entity
            order = Order(
                order_id=message.order_id,
                created_at=created_at,
                line_items=line_items,
                inserted_at=inserted_at
            )

            logger.info("order_translated", order_id=message.order_id)
            return order

        except ValueError as e:
            logger.error("order_translation_failed", error=str(e))
            raise DataIntegrityException(f"Invalid order data: {e}") from e


def _parse_iso_timestamp(timestamp_str: str) -> datetime:
    """Parse ISO 8601 timestamp with validation."""
    try:
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except ValueError as e:
        raise ValueError(f"Invalid ISO timestamp: {timestamp_str}") from e
```

## Instructions

### Step 1: Understand the Defense-in-Depth Pattern

The skill is built on **validating at both producer and consumer layers**:

- **Producer Validation (Extraction Context):** Validate business rules and schema compliance before publishing to Kafka using msgspec schemas and domain value objects
- **Consumer Validation (Storage Context):** Validate data integrity and transformation when consuming from Kafka using anti-corruption layers
- **ClickHouse Error Streaming:** Capture malformed messages in a separate error table instead of blocking consumption with `kafka_handle_error_mode='stream'`
- **Idempotency:** Handle at-least-once delivery semantics using ReplacingMergeTree for automatic deduplication

### Step 2: Set Up ClickHouse Error Handling

Create the error capture infrastructure in ClickHouse:

1. **Add error streaming to Kafka table:** Set `kafka_handle_error_mode='stream'` and `input_format_skip_unknown_fields=1`
2. **Create error table:** Dedicated table to store malformed messages with Kafka metadata (topic, partition, offset)
3. **Create error materialized view:** Automatically captures errors where `_error` virtual column is non-empty
4. **Create target table:** ReplacingMergeTree for idempotent data storage
5. **Create data transformation view:** Filters valid messages (`_error` is empty) and transforms timestamps

See `references/clickhouse-schema.sql` for complete SQL templates.

### Step 3: Implement Producer Validation with msgspec

Producer-side validation prevents invalid data from entering Kafka:

1. **Define msgspec schemas:** Frozen, type-safe message structures in `adapters/kafka/schemas.py`
2. **Add domain validation:** Use value objects with `__post_init__` for business rule enforcement
3. **Handle validation errors:** Catch `msgspec.ValidationError` and translate to domain exceptions
4. **Log validation failures:** Use OTEL logging to track producer-side rejections

See `references/producer-patterns.py` for detailed implementations.

### Step 4: Implement Consumer Validation with Anti-Corruption Layer

Consumer-side validation provides defense-in-depth and context isolation:

1. **Define msgspec schemas locally:** Each context owns its own message schema definition
2. **Create KafkaMessageTranslator class:** Implement `translate_*` methods for each message type
3. **Validate timestamp formats:** Use `_parse_iso_timestamp` helper for ISO 8601 parsing
4. **Validate business rules:** Enforce constraints like non-empty fields, positive quantities
5. **Handle translation failures:** Catch exceptions and translate to application-layer exceptions

See `references/consumer-patterns.py` for detailed implementations.

### Step 5: Set Up Error Monitoring

Implement observability for Kafka error detection:

1. **Create monitoring queries:** Query `kafka_errors` table to detect error spikes
2. **Track error metrics:** Count errors by type, partition, and time window
3. **Configure alerts:** Alert when error rate exceeds threshold (e.g., >20 errors/sec)
4. **Create dashboards:** Visualize error trends, most common errors, consumer lag
5. **Document runbooks:** Create investigation procedures for common error patterns

See `references/monitoring-queries.sql` and `examples/examples.md` for detailed queries.

### Step 6: Test Validation and Error Handling

Implement integration and unit tests to verify the pattern:

1. **Unit tests:** Test validation logic in isolation (value objects, anti-corruption layer)
2. **Integration tests:** Test end-to-end with Kafka and ClickHouse using testcontainers
3. **Error capture tests:** Verify malformed messages are captured in error table
4. **Deduplication tests:** Verify duplicates are eliminated by ReplacingMergeTree
5. **Schema evolution tests:** Test adding optional fields without breaking consumption

See `examples/examples.md` for test patterns.

## Examples

### Example 1: Setting Up Complete Error Handling Pipeline

**Goal:** Enable error capture in existing ClickHouse Kafka pipeline

**Steps:**

```sql
-- 1. Modify existing Kafka table to enable error streaming
ALTER TABLE shopify.kafka_orders
MODIFY SETTING kafka_handle_error_mode = 'stream';

-- 2. Create error capture table
CREATE TABLE shopify.kafka_errors (
    topic String,
    partition Int64,
    offset Int64,
    raw_message String,
    error_message String,
    captured_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY (topic, partition, offset)
PARTITION BY toYYYYMM(captured_at)
TTL captured_at + INTERVAL 30 DAY;

-- 3. Create error capture materialized view
CREATE MATERIALIZED VIEW shopify.kafka_errors_mv
TO shopify.kafka_errors AS
SELECT
    _topic AS topic,
    _partition AS partition,
    _offset AS offset,
    _raw_message AS raw_message,
    _error AS error_message
FROM shopify.kafka_orders
WHERE length(_error) > 0;

-- 4. Verify it's working
SELECT count(*) as error_count FROM shopify.kafka_errors
WHERE captured_at > now() - INTERVAL 1 HOUR;
```

**Result:** Any malformed JSON is now captured in `shopify.kafka_errors` instead of blocking consumption.

### Example 2: Detecting High Error Rate

**Goal:** Monitor error rate and alert if spike detected

```sql
-- Query current error rate (5-minute window)
SELECT
    count(*) as error_count,
    uniq(error_message) as unique_error_types,
    max(captured_at) as latest_error_time
FROM shopify.kafka_errors
WHERE captured_at > now() - INTERVAL 5 MINUTE;

-- If error_count > 100, investigate error types:
SELECT
    error_message,
    count(*) as occurrences,
    substring(raw_message, 1, 200) as sample
FROM shopify.kafka_errors
WHERE captured_at > now() - INTERVAL 1 HOUR
GROUP BY error_message
ORDER BY occurrences DESC
LIMIT 10;
```

**Result:** Identifies root cause of error spike (e.g., schema mismatch, encoding issue).

### Example 3: Implementing Anti-Corruption Layer

**Goal:** Add consumer-side validation before loading data

```python
# app/storage/adapters/anti_corruption.py
from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from app.storage.domain.exceptions import DataIntegrityException

@dataclass
class OrderMessageValidation:
    """Validation helper for order messages."""

    @staticmethod
    def validate_timestamps(created_at_str: str, inserted_at_str: str) -> None:
        """Validate ISO 8601 timestamp format."""
        for ts_str in [created_at_str, inserted_at_str]:
            try:
                datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
            except ValueError as e:
                raise DataIntegrityException(f"Invalid timestamp: {ts_str}") from e

    @staticmethod
    def validate_line_items(line_items: list) -> None:
        """Validate line item constraints."""
        if not line_items:
            raise DataIntegrityException("Order must have at least one line item")

        for i, item in enumerate(line_items):
            if item.get('quantity', 0) <= 0:
                raise DataIntegrityException(f"Line item {i}: quantity must be positive")
            if not item.get('product_title', '').strip():
                raise DataIntegrityException(f"Line item {i}: product_title cannot be empty")

    @staticmethod
    def validate_order_id(order_id: str) -> None:
        """Validate order ID."""
        if not order_id or not order_id.strip():
            raise DataIntegrityException("Order ID cannot be empty")
```

**Result:** Systematic validation at consumer boundary prevents corrupted data from reaching storage.

### Example 4: Testing Error Capture

**Goal:** Verify malformed messages are captured

```python
# tests/integration/storage/test_kafka_error_capture.py
import pytest
import time
from testcontainers.kafka import KafkaContainer
from testcontainers.clickhouse import ClickHouseContainer

@pytest.mark.asyncio
async def test_malformed_message_captured_in_error_table(
    kafka_producer, clickhouse_client
) -> None:
    """Malformed JSON is captured in kafka_errors table."""
    # Publish invalid JSON (missing quotes)
    invalid_payload = b'{"order_id": broken_json}'
    kafka_producer.produce(
        topic="shopify-orders",
        value=invalid_payload
    )

    # Wait for ClickHouse to consume and process
    time.sleep(5)

    # Check error table
    errors = clickhouse_client.execute("""
        SELECT topic, error_message FROM shopify.kafka_errors
        WHERE captured_at > now() - INTERVAL 1 MINUTE
    """)

    assert len(errors) > 0
    assert errors[0][0] == "shopify-orders"
    assert "JSON" in errors[0][1] or "parse" in errors[0][1]
```

**Result:** Automated verification that error capture is working correctly.

## Requirements

### Python Dependencies
- `msgspec>=0.18.0` - Fast, type-safe message serialization (10-20x faster than Pydantic)
- `clickhouse-driver>=0.2.6` - ClickHouse client library
- `confluent-kafka>=2.3.0` - Kafka/Redpanda client
- `pydantic>=2.5.0` - Configuration validation (optional, for config classes)

### ClickHouse Version
- ClickHouse 21.6+ (for `kafka_handle_error_mode='stream'`)
- Earlier versions require fallback to `kafka_skip_broken_messages`

### Knowledge Requirements
- Understanding of Clean Architecture and bounded contexts (see CLAUDE.md)
- Familiarity with ClickHouse table engines (MergeTree, ReplacingMergeTree)
- Basic Kafka concepts (topics, partitions, consumer groups)
- Python dataclasses and type hints

## See Also

- **[references/clickhouse-schema.sql](./references/clickhouse-schema.sql)** - Complete ClickHouse schema templates
- **[references/producer-patterns.py](./references/producer-patterns.py)** - Producer-side validation examples
- **[references/consumer-patterns.py](./references/consumer-patterns.py)** - Consumer-side validation examples
- **[references/monitoring-queries.sql](./references/monitoring-queries.sql)** - Monitoring and alerting queries
- **[examples/examples.md](./examples/examples.md)** - Comprehensive examples and test patterns
- **[Full ADR](../../artifacts/2025-11-09/analysis/adr-clickhouse-kafka-validation-patterns.md)** - Complete architecture decision record with rationale and alternatives
- **[Quick Reference](../../artifacts/2025-11-09/analysis/quickref-validation-patterns.md)** - TL;DR quick reference guide

**Project Documentation:**
- **CLAUDE.md** - Architecture principles, DDD bounded contexts, OTEL logging patterns
- **README.md** - Project overview and deployment instructions

**External Resources:**
- [ClickHouse Kafka Engine](https://clickhouse.com/docs/integrations/kafka/kafka-table-engine)
- [ReplacingMergeTree Documentation](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/replacingmergetree)
- [Altinity KB - Kafka Error Handling](https://kb.altinity.com/altinity-kb-integrations/altinity-kb-kafka/error-handling/)
- [msgspec Documentation](https://jcristharif.com/msgspec/)
