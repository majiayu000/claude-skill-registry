---
name: kafka-schema-management
description: |
  Design and manage Kafka message schemas with type safety and schema evolution.
  Use when defining event schemas, creating schema validators, managing versions,
  and generating type-safe Pydantic/msgspec models from schema definitions.
  Supports schema registry patterns and backward/forward compatibility.
allowed-tools: Read, Write, Edit, Bash, Grep
---

## Table of Contents

- [Purpose](#purpose)
- [Quick Start](#quick-start)
- [Instructions](#instructions)
  - [Step 1: Design Schema with msgspec.Struct](#step-1-design-schema-with-msgspecstruct)
  - [Step 2: Create Schema Validator](#step-2-create-schema-validator)
  - [Step 3: Implement Schema Builder (DTO Factory)](#step-3-implement-schema-builder-dto-factory)
  - [Step 4: Handle Schema Evolution](#step-4-handle-schema-evolution)
  - [Step 5: Testing Schemas](#step-5-testing-schemas)
- [Schema Design Principles](#schema-design-principles)
- [Schema Evolution Strategies](#schema-evolution-strategies)
- [Implementation Examples](#implementation-examples)
- [Best Practices and Patterns](#best-practices-and-patterns)
- [Requirements](#requirements)
- [See Also](#see-also)

# Kafka Schema Management

## Purpose

This skill guides designing production-grade Kafka message schemas with type safety, validation, and evolution support. It covers msgspec immutable struct definitions, schema validation patterns, version management, and strategies for handling schema changes without breaking consumers or producers.

## Quick Start

Define schemas in 3 steps:

1. **Create schema file** with msgspec structs:
```python
import msgspec

class LineItemMessage(msgspec.Struct, frozen=True):
    line_item_id: str
    product_id: str
    product_title: str
    quantity: int
    price: float

class OrderEventMessage(msgspec.Struct, frozen=True):
    order_id: str
    created_at: str
    customer_name: str
    line_items: list[LineItemMessage]
    total_price: float
```

2. **Create validator class**:
```python
import msgspec

class OrderMessageValidator:
    def __init__(self):
        self.decoder = msgspec.json.Decoder(OrderEventMessage)
        self.encoder = msgspec.json.Encoder()

    def validate(self, data: bytes) -> OrderEventMessage:
        return self.decoder.decode(data)

    def serialize(self, msg: OrderEventMessage) -> bytes:
        return self.encoder.encode(msg)
```

3. **Use in producer/consumer**:
```python
validator = OrderMessageValidator()
# Serialization
bytes_payload = validator.serialize(order_msg)
# Deserialization
order_msg = validator.validate(bytes_payload)
```

## Instructions

### Step 1: Design Schema with msgspec.Struct

Use msgspec Structs for high-performance immutable schemas:

```python
from __future__ import annotations

import msgspec
from typing import Optional


# Value object schemas - represent domain concepts
class MoneyMessage(msgspec.Struct, frozen=True):
    """Money value object schema.

    Immutable representation of monetary value.
    Uses float for serialization (Kafka JSON doesn't support Decimal).
    """

    amount: float
    currency: str = "USD"  # Default currency


# Line item aggregates
class LineItemMessage(msgspec.Struct, frozen=True):
    """Line item in an order.

    Represents a single product purchase with quantity and price.

    Attributes:
        line_item_id: Unique line item identifier
        product_id: Product catalog ID
        product_title: Human-readable product name
        quantity: Number of units purchased
        price: Unit price in currency
    """

    line_item_id: str
    product_id: str
    product_title: str
    quantity: int  # Positive integer
    price: float  # Unit price


# Root aggregate messages
class OrderEventMessage(msgspec.Struct, frozen=True):
    """Order event - root aggregate for Kafka.

    Immutable event representing a complete order.
    Published when order is placed or updated.

    Attributes:
        order_id: Unique order identifier (primary key)
        created_at: ISO 8601 timestamp when order was created
        customer_name: Customer name for delivery
        line_items: List of products in order
        total_price: Total order value (sum validation in consumer)

    Event Schema Versioning:
    - Version 1.0: Initial schema (current)
    - Fields: order_id, created_at, customer_name, line_items, total_price
    - Type Guarantees: All fields required (no Optional)
    """

    order_id: str
    created_at: str  # ISO 8601 format: "2024-01-01T12:00:00Z"
    customer_name: str
    line_items: list[LineItemMessage]
    total_price: float


# Event envelope for metadata
class EventEnvelopeMessage(msgspec.Struct, frozen=True):
    """Event envelope with metadata.

    Wrapper that adds metadata to domain events:
    - Source: Which bounded context published this
    - Version: Schema version (for evolution)
    - Timestamp: When event was created
    - Correlation ID: For distributed tracing

    Use this pattern for complex systems with multiple event types.
    """

    event_type: str  # "order.created", "order.updated", etc.
    event_version: str  # "1.0", "2.0" for schema versioning
    correlation_id: str  # For distributed tracing
    timestamp: str  # ISO 8601 when event created
    source: str  # "extraction", "reporting", etc.
    payload: dict[str, object]  # Actual event data (JSON)
```

**Design Principles:**

- **Immutable**: Use `frozen=True` - prevents accidental mutation
- **Primitive Types**: Use str, int, float, list, dict - not custom objects
- **Timestamps as ISO 8601 Strings**: Easier serialization and compatibility
- **Required Fields Only**: Avoid Optional at schema level (validation layer handles defaults)
- **Specific Types**: Not `list[Any]` or `dict[str, Any]`

### Step 2: Create Schema Validator

Implement validator class for serialization/deserialization:

```python
from __future__ import annotations

import msgspec
from structlog import get_logger


class SchemaValidationError(Exception):
    """Schema validation failed."""


class OrderMessageValidator:
    """Validates and serializes order event messages.

    Responsibilities:
    - Deserialize bytes to typed messages (validation)
    - Serialize messages to bytes (serialization)
    - Handle version detection
    - Log validation errors with context

    Design Pattern:
    - Single responsibility: only validation
    - Stateless: can be shared across threads
    - No side effects: pure functions

    Performance:
    - msgspec: 10-20x faster than json.loads + Pydantic
    - Pre-compiled decoder/encoder: no runtime overhead
    """

    def __init__(self) -> None:
        """Initialize validator with pre-compiled codecs."""
        self.decoder = msgspec.json.Decoder(OrderEventMessage)
        self.encoder = msgspec.json.Encoder()
        self.logger = get_logger(__name__)

    def validate(self, data: bytes) -> OrderEventMessage:
        """Validate and deserialize bytes to OrderEventMessage.

        Args:
            data: Raw bytes from Kafka message

        Returns:
            Validated OrderEventMessage

        Raises:
            SchemaValidationError: Deserialization failed (malformed JSON, missing fields)

        Example:
            >>> validator = OrderMessageValidator()
            >>> message = validator.validate(b'{"order_id":"123",...}')
            >>> print(message.order_id)
            123
        """
        try:
            message: OrderEventMessage = self.decoder.decode(data)

            # Additional validation (msgspec doesn't check these)
            self._validate_business_rules(message)

            return message

        except msgspec.DecodeError as e:
            self.logger.error(
                "message_validation_failed",
                error=str(e),
                data_sample=data[:100] if len(data) > 100 else data,
            )
            raise SchemaValidationError(f"Failed to decode message: {e}") from e

    def _validate_business_rules(self, message: OrderEventMessage) -> None:
        """Validate business rules that msgspec can't check.

        Args:
            message: Validated message structure

        Raises:
            SchemaValidationError: Business rules violated
        """
        # Validate order_id format
        if not message.order_id or len(message.order_id) == 0:
            raise SchemaValidationError("order_id cannot be empty")

        # Validate line items
        if len(message.line_items) == 0:
            raise SchemaValidationError("Order must have at least one line item")

        # Validate quantities
        for item in message.line_items:
            if item.quantity <= 0:
                raise SchemaValidationError(f"Invalid quantity: {item.quantity}")
            if item.price < 0:
                raise SchemaValidationError(f"Invalid price: {item.price}")

        # Validate total price approximately matches sum
        calculated_total = sum(item.price * item.quantity for item in message.line_items)
        if abs(calculated_total - message.total_price) > 0.01:  # 1 cent tolerance for rounding
            self.logger.warning(
                "total_price_mismatch",
                expected=calculated_total,
                actual=message.total_price,
            )

    def serialize(self, message: OrderEventMessage) -> bytes:
        """Serialize OrderEventMessage to bytes.

        Args:
            message: Message to serialize

        Returns:
            JSON bytes ready for Kafka

        Raises:
            SchemaValidationError: Serialization failed (shouldn't happen with valid message)

        Example:
            >>> msg = OrderEventMessage(...)
            >>> bytes_payload = validator.serialize(msg)
            >>> len(bytes_payload)  # Actual size
            256
        """
        try:
            return self.encoder.encode(message)
        except msgspec.EncodeError as e:
            self.logger.error("message_serialization_failed", error=str(e))
            raise SchemaValidationError(f"Failed to encode message: {e}") from e
```

### Step 3: Implement Schema Builder (DTO Factory)

Create builders for constructing messages from domain objects:

```python
from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from app.extraction.domain.entities import Order
from app.extraction.domain.value_objects import Money


class OrderMessageBuilder:
    """Builder pattern for constructing OrderEventMessage from domain Order.

    Separates concerns:
    - OrderMessage: Low-level schema for serialization
    - OrderMessageBuilder: Converts domain to schema
    - Order: High-level domain logic

    This is a simpler alternative to separate translator class.
    Use when domain-to-schema conversion is straightforward.

    Example:
        >>> order = Order(...)
        >>> message = OrderMessageBuilder.from_domain(order)
        >>> validator.serialize(message)
    """

    @staticmethod
    def from_domain(order: Order) -> OrderEventMessage:
        """Convert domain Order to message schema.

        Args:
            order: Domain order aggregate root

        Returns:
            OrderEventMessage ready for serialization

        Raises:
            ValueError: Domain order is invalid for serialization
        """
        # Build line items
        line_items = [
            LineItemMessage(
                line_item_id=item.line_item_id,
                product_id=str(item.product_id),
                product_title=str(item.product_title),
                quantity=item.quantity,
                price=float(item.price.amount),
            )
            for item in order.line_items
        ]

        # Build root message
        return OrderEventMessage(
            order_id=str(order.order_id),
            created_at=order.created_at.isoformat(),
            customer_name=order.customer_name,
            line_items=line_items,
            total_price=float(order.total_price.amount),
        )

    @staticmethod
    def from_dict(data: dict[str, object]) -> OrderEventMessage:
        """Construct message from dictionary (useful for testing).

        Args:
            data: Dictionary with order fields

        Returns:
            OrderEventMessage

        Raises:
            ValueError: Missing required fields
        """
        order_id = data.get("order_id", "")
        created_at = data.get("created_at", "")
        customer_name = data.get("customer_name", "")
        line_items_data = data.get("line_items", [])
        total_price = data.get("total_price", 0.0)

        line_items = [
            LineItemMessage(
                line_item_id=str(item.get("line_item_id", "")),
                product_id=str(item.get("product_id", "")),
                product_title=str(item.get("product_title", "")),
                quantity=int(item.get("quantity", 0)),
                price=float(item.get("price", 0.0)),
            )
            for item in line_items_data
        ]

        return OrderEventMessage(
            order_id=str(order_id),
            created_at=str(created_at),
            customer_name=str(customer_name),
            line_items=line_items,
            total_price=float(total_price),
        )
```

### Step 4: Handle Schema Evolution

Manage schema versions with backward compatibility:

```python
from __future__ import annotations

from typing import Union
import msgspec


class OrderEventMessageV1(msgspec.Struct, frozen=True):
    """Order event schema version 1.0 (deprecated).

    Original schema without customer_name.
    """

    order_id: str
    created_at: str
    line_items: list[LineItemMessage]
    total_price: float


class OrderEventMessageV2(msgspec.Struct, frozen=True):
    """Order event schema version 2.0 (current).

    Added customer_name field (backward compatible).
    Old consumers ignore new field, new consumers provide default.
    """

    order_id: str
    created_at: str
    customer_name: str
    line_items: list[LineItemMessage]
    total_price: float


# Alias current version
OrderEventMessage = OrderEventMessageV2


class SchemaUpgrader:
    """Handle schema evolution when reading old messages.

    Strategy:
    1. Try to decode as current schema (V2)
    2. If fails, try to decode as V1
    3. Upgrade V1 to V2 by adding default values
    4. Log warning when upgrading

    This allows gradual rollout:
    - Old producers send V1, new consumers upgrade on read
    - New producers send V2, old consumers ignore new field
    """

    @staticmethod
    def upgrade_v1_to_v2(msg_v1: OrderEventMessageV1) -> OrderEventMessageV2:
        """Upgrade V1 message to V2 schema.

        Args:
            msg_v1: Message in V1 schema

        Returns:
            Message in V2 schema with default customer_name
        """
        return OrderEventMessageV2(
            order_id=msg_v1.order_id,
            created_at=msg_v1.created_at,
            customer_name="Unknown Customer",  # Default for old messages
            line_items=msg_v1.line_items,
            total_price=msg_v1.total_price,
        )

    @staticmethod
    def smart_decode(data: bytes) -> OrderEventMessageV2:
        """Decode message, upgrading schema version if needed.

        Args:
            data: Raw bytes from Kafka

        Returns:
            Message in current (V2) schema

        Raises:
            SchemaValidationError: Neither V1 nor V2 schema matched
        """
        # Try current version first (faster path)
        try:
            decoder_v2 = msgspec.json.Decoder(OrderEventMessageV2)
            return decoder_v2.decode(data)
        except msgspec.DecodeError:
            pass

        # Fall back to V1 and upgrade
        try:
            decoder_v1 = msgspec.json.Decoder(OrderEventMessageV1)
            msg_v1 = decoder_v1.decode(data)
            return SchemaUpgrader.upgrade_v1_to_v2(msg_v1)
        except msgspec.DecodeError as e:
            raise SchemaValidationError(f"Message matches neither V1 nor V2: {e}") from e
```

### Step 5: Testing Schemas

Write tests to validate schema correctness:

```python
import pytest
import msgspec
from app.extraction.adapters.kafka.schemas import OrderEventMessage, OrderMessageValidator


class TestOrderMessageSchema:
    """Test OrderEventMessage schema validation."""

    def test_valid_order_message(self) -> None:
        """Test valid order message serialization."""
        msg = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="John Doe",
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

        validator = OrderMessageValidator()
        bytes_payload = validator.serialize(msg)
        decoded = validator.validate(bytes_payload)

        assert decoded.order_id == "order_123"
        assert decoded.customer_name == "John Doe"
        assert len(decoded.line_items) == 1

    def test_invalid_message_missing_order_id(self) -> None:
        """Test validation fails for invalid message."""
        from app.extraction.adapters.kafka.schemas import SchemaValidationError

        invalid_json = b'{"created_at":"2024-01-01","customer_name":"John"}'

        validator = OrderMessageValidator()
        with pytest.raises(SchemaValidationError):
            validator.validate(invalid_json)

    def test_zero_quantity_fails_validation(self) -> None:
        """Test business rule: quantity must be positive."""
        invalid_msg = OrderEventMessage(
            order_id="order_123",
            created_at="2024-01-01T12:00:00Z",
            customer_name="John Doe",
            line_items=[
                LineItemMessage(
                    line_item_id="item_1",
                    product_id="prod_1",
                    product_title="Laptop",
                    quantity=0,  # Invalid!
                    price=999.99,
                )
            ],
            total_price=999.99,
        )

        validator = OrderMessageValidator()
        with pytest.raises(SchemaValidationError, match="Invalid quantity"):
            validator._validate_business_rules(invalid_msg)
```

## Schema Design Principles

### Immutability
Use `frozen=True` in msgspec.Struct definitions to prevent accidental mutation of messages during processing. Immutable messages are safer for distributed systems.

```python
class OrderEventMessage(msgspec.Struct, frozen=True):  # frozen=True required
    order_id: str
    customer_name: str
```

### Primitive Types Only
Stick to primitive JSON-compatible types: `str`, `int`, `float`, `bool`, `list`, `dict`. Avoid custom Python objects, Decimal, or datetime objects. Kafka messages must serialize cleanly to JSON.

### ISO 8601 Timestamps
Use ISO 8601 string format for dates: `"2024-01-01T12:00:00Z"`. This avoids timezone issues and works across all systems.

### Required Fields Only (at Schema Level)
Define all fields as required in the msgspec.Struct. Use a validation layer (application layer) to handle defaults and optional values. This ensures consumers always receive complete messages.

### Specific Types Over Any
Never use `list[Any]` or `dict[str, Any]`. Be explicit about nested structures to enable static type checking:

```python
# Good
line_items: list[LineItemMessage]
metadata: dict[str, str]

# Avoid
data: Any
items: list[Any]
```

### Document Schema Versions
Include version history in docstrings:

```python
class OrderEventMessage(msgspec.Struct, frozen=True):
    """Order event schema.

    Version History:
    - 1.0: Initial (order_id, created_at, line_items, total_price)
    - 2.0: Added customer_name field (backward compatible)
    """
```

## Schema Evolution Strategies

### Strategy 1: Adding Optional Fields (Backward Compatible)

When adding a new field to a schema:

1. **Producers Start First**: Deploy new producers that include the new field
2. **Consumers Prepare**: Deploy updated consumers that can handle the new field
3. **Old Messages**: Consumers add default values when reading old messages

Example - adding `discount_amount` field:

```python
# Old Schema (V1)
class OrderEventMessageV1(msgspec.Struct, frozen=True):
    order_id: str
    total_price: float

# New Schema (V2)
class OrderEventMessageV2(msgspec.Struct, frozen=True):
    order_id: str
    total_price: float
    discount_amount: float  # New field

# Consumer handles both versions
def decode_order(data: bytes) -> OrderEventMessageV2:
    try:
        return decoder_v2.decode(data)
    except msgspec.DecodeError:
        msg_v1 = decoder_v1.decode(data)
        return OrderEventMessageV2(
            order_id=msg_v1.order_id,
            total_price=msg_v1.total_price,
            discount_amount=0.0  # Default for old messages
        )
```

### Strategy 2: Removing Fields (Forward Compatible)

When removing a field:

1. **Producers Stop First**: Old producers stop sending deprecated field
2. **Consumers Updated Second**: Consumers ignore the removed field (msgspec automatically ignores unknown fields in flexible mode)
3. **Messages in Queue**: Old messages with deprecated field still work

### Strategy 3: Changing Field Types (Breaking)

Avoid if possible. If necessary:

1. Create new event type (e.g., `OrderEventV3`)
2. Keep both types in the schema module
3. Migrate step by step with dual-write/dual-read phases

```python
class OrderEventMessageV2(msgspec.Struct, frozen=True):
    price: float  # Old type

class OrderEventMessageV3(msgspec.Struct, frozen=True):
    price: str  # New type (breaking change - avoid!)
```

### Best Practice: Schema Registry Pattern

Encode schema version in the message envelope:

```python
class EventEnvelopeMessage(msgspec.Struct, frozen=True):
    event_type: str  # "order.created"
    event_version: str  # "2.0" - explicitly track version
    timestamp: str
    payload: dict[str, object]  # Flexible payload for evolution
```

This allows:
- Explicit versioning without guessing
- Gradual migration between versions
- Support for multiple schema versions in flight

## Implementation Examples

See [`examples/examples.md`](./examples/examples.md) for:
- Complete order event schema example
- Event envelope pattern with multiple event types
- Schema registry integration
- Testing multiple schema versions
- Schema validation edge cases

## Best Practices and Patterns

See [`references/reference.md`](./references/reference.md) for:
- Performance optimization techniques
- Integration with Pydantic models
- Schema documentation standards
- Monitoring schema usage and versioning
- ClickHouse table schema alignment
- Distributed tracing with correlation IDs

## Requirements

- `msgspec>=0.18.6` - Immutable struct definitions and serialization
- `pydantic>=2.5.0` - Alternative for schema definition (if using Pydantic instead of msgspec)
- Python 3.11+ with type checking enabled

## See Also

- **Producer Implementation**: `kafka-producer-implementation` skill for using schemas in producers
- **Consumer Implementation**: `kafka-consumer-implementation` skill for consuming and validating messages
- **Integration Testing**: `kafka-integration-testing` skill for end-to-end schema validation tests
- **Examples**: [`examples/examples.md`](./examples/examples.md) for comprehensive schema patterns
- **References**: [`references/reference.md`](./references/reference.md) for advanced topics and integrations
