---
name: kafka-schema-management
description: |
  Design and manage Kafka message schemas with type safety and schema evolution.
  Use when defining event schemas, creating schema validators, managing versions,
  and generating type-safe Pydantic/msgspec models from schema definitions.
  Supports schema registry patterns and backward/forward compatibility.
allowed-tools: Read, Write, Edit, Bash, Grep
---

# Kafka Schema Management

## Purpose

Design production-grade Kafka message schemas with type safety, validation, and evolution support. Covers msgspec immutable struct definitions, schema validation patterns, version management, and strategies for handling schema changes without breaking consumers or producers.


## When to Use This Skill

Use when defining message formats for Kafka with "design Kafka schema", "create message schema", "manage schema versions", or "handle schema evolution".

Do NOT use for implementing producers/consumers (use `kafka-*-implementation` skills) or testing (use `kafka-integration-testing`).
## Quick Start

Define schemas in 3 steps:

1. **Create schema**:
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

2. **Create validator**:
```python
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

## Implementation Steps

### 1. Design Schema with msgspec.Struct

Use msgspec Structs for high-performance immutable schemas:

```python
import msgspec

# Value object schemas
class MoneyMessage(msgspec.Struct, frozen=True):
    """Money value object schema."""
    amount: float
    currency: str = "USD"

# Nested schemas
class LineItemMessage(msgspec.Struct, frozen=True):
    """Line item in an order."""
    line_item_id: str
    product_id: str
    product_title: str
    quantity: int
    price: float

# Root aggregate messages
class OrderEventMessage(msgspec.Struct, frozen=True):
    """Order event - root aggregate for Kafka.

    Version History:
    - 1.0: Initial schema
    - 2.0: Added customer_name field (backward compatible)
    """
    order_id: str
    created_at: str  # ISO 8601
    customer_name: str
    line_items: list[LineItemMessage]
    total_price: float
```

**Design Principles:**
- **Immutable**: Use `frozen=True`
- **Primitive Types**: Use str, int, float, list, dict
- **ISO 8601 Timestamps**: Use strings for dates
- **Required Fields Only**: Avoid Optional at schema level
- **Specific Types**: Not `list[Any]` or `dict[str, Any]`

### 2. Create Schema Validator

Implement validator class for serialization/deserialization:

```python
import msgspec
from structlog import get_logger

class SchemaValidationError(Exception):
    """Schema validation failed."""

class OrderMessageValidator:
    """Validates and serializes order event messages.

    Performance:
    - msgspec: 10-20x faster than json.loads + Pydantic
    - Pre-compiled decoder/encoder: no runtime overhead
    """

    def __init__(self) -> None:
        self.decoder = msgspec.json.Decoder(OrderEventMessage)
        self.encoder = msgspec.json.Encoder()
        self.logger = get_logger(__name__)

    def validate(self, data: bytes) -> OrderEventMessage:
        """Validate and deserialize bytes to OrderEventMessage."""
        try:
            message = self.decoder.decode(data)
            self._validate_business_rules(message)
            return message
        except msgspec.DecodeError as e:
            self.logger.error("validation_failed", error=str(e))
            raise SchemaValidationError(f"Failed to decode: {e}") from e

    def _validate_business_rules(self, message: OrderEventMessage) -> None:
        """Validate business rules msgspec can't check."""
        if not message.order_id:
            raise SchemaValidationError("order_id cannot be empty")
        if len(message.line_items) == 0:
            raise SchemaValidationError("Order must have at least one line item")
        for item in message.line_items:
            if item.quantity <= 0:
                raise SchemaValidationError(f"Invalid quantity: {item.quantity}")
            if item.price < 0:
                raise SchemaValidationError(f"Invalid price: {item.price}")

    def serialize(self, message: OrderEventMessage) -> bytes:
        """Serialize OrderEventMessage to bytes."""
        try:
            return self.encoder.encode(message)
        except msgspec.EncodeError as e:
            raise SchemaValidationError(f"Failed to encode: {e}") from e
```

See `references/detailed-implementation.md` for complete validator implementation with additional business rule validation.

### 3. Schema Builder (DTO Factory)

Create builders for constructing messages from domain objects:

```python
class OrderMessageBuilder:
    """Builder for constructing OrderEventMessage from domain Order."""

    @staticmethod
    def from_domain(order: Order) -> OrderEventMessage:
        """Convert domain Order to message schema."""
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

        return OrderEventMessage(
            order_id=str(order.order_id),
            created_at=order.created_at.isoformat(),
            customer_name=order.customer_name,
            line_items=line_items,
            total_price=float(order.total_price.amount),
        )
```

### 4. Handle Schema Evolution

Manage schema versions with backward compatibility:

```python
# V1 schema (deprecated)
class OrderEventMessageV1(msgspec.Struct, frozen=True):
    """Original schema without customer_name."""
    order_id: str
    created_at: str
    line_items: list[LineItemMessage]
    total_price: float

# V2 schema (current)
class OrderEventMessageV2(msgspec.Struct, frozen=True):
    """Added customer_name field (backward compatible)."""
    order_id: str
    created_at: str
    customer_name: str
    line_items: list[LineItemMessage]
    total_price: float

# Alias current version
OrderEventMessage = OrderEventMessageV2

class SchemaUpgrader:
    """Handle schema evolution when reading old messages."""

    @staticmethod
    def upgrade_v1_to_v2(msg_v1: OrderEventMessageV1) -> OrderEventMessageV2:
        """Upgrade V1 message to V2 schema."""
        return OrderEventMessageV2(
            order_id=msg_v1.order_id,
            created_at=msg_v1.created_at,
            customer_name="Unknown Customer",  # Default
            line_items=msg_v1.line_items,
            total_price=msg_v1.total_price,
        )

    @staticmethod
    def smart_decode(data: bytes) -> OrderEventMessageV2:
        """Decode message, upgrading schema version if needed."""
        try:
            decoder_v2 = msgspec.json.Decoder(OrderEventMessageV2)
            return decoder_v2.decode(data)
        except msgspec.DecodeError:
            decoder_v1 = msgspec.json.Decoder(OrderEventMessageV1)
            msg_v1 = decoder_v1.decode(data)
            return SchemaUpgrader.upgrade_v1_to_v2(msg_v1)
```

### 5. Testing Schemas

Write tests to validate schema correctness:

```python
import pytest
from app.extraction.adapters.kafka.schemas import OrderEventMessage, OrderMessageValidator

def test_valid_order_message() -> None:
    """Test valid order message serialization."""
    msg = OrderEventMessage(
        order_id="order_123",
        created_at="2024-01-01T12:00:00Z",
        customer_name="John Doe",
        line_items=[...],
        total_price=999.99,
    )

    validator = OrderMessageValidator()
    bytes_payload = validator.serialize(msg)
    decoded = validator.validate(bytes_payload)

    assert decoded.order_id == "order_123"
    assert decoded.customer_name == "John Doe"

def test_invalid_message_missing_order_id() -> None:
    """Test validation fails for invalid message."""
    invalid_json = b'{"created_at":"2024-01-01","customer_name":"John"}'

    validator = OrderMessageValidator()
    with pytest.raises(SchemaValidationError):
        validator.validate(invalid_json)
```

## Schema Evolution Strategies

### Adding Optional Fields (Backward Compatible)

1. Deploy new producers with new field
2. Deploy updated consumers that handle new field
3. Old messages: Consumers add default values

```python
# New schema adds discount_amount
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
            discount_amount=0.0  # Default
        )
```

### Removing Fields (Forward Compatible)

1. Producers stop sending deprecated field
2. Consumers ignore removed field
3. Old messages with field still work (msgspec ignores unknown fields)

### Changing Field Types (Breaking)

Avoid if possible. If necessary:
1. Create new event type (OrderEventV3)
2. Keep both types in schema module
3. Migrate with dual-write/dual-read phases

### Schema Registry Pattern

Encode schema version in message envelope:

```python
class EventEnvelopeMessage(msgspec.Struct, frozen=True):
    event_type: str  # "order.created"
    event_version: str  # "2.0"
    timestamp: str
    payload: dict[str, object]
```

## Requirements

- `msgspec>=0.18.6` - Immutable struct definitions and serialization
- `pydantic>=2.5.0` - Alternative for schema definition (if using Pydantic)
- Python 3.11+ with type checking

## Best Practices

**Immutability**: Use `frozen=True` to prevent mutation.

**Primitive Types Only**: Stick to str, int, float, bool, list, dict.

**ISO 8601 Timestamps**: Use strings for dates.

**Required Fields**: Define all fields as required at schema level.

**Document Versions**: Include version history in docstrings.

## Integration Examples

See `examples/examples.md` for comprehensive examples:
- Complete order event schema
- Event envelope pattern with multiple event types
- Schema registry integration
- Testing multiple schema versions
- Schema validation edge cases

## Advanced Topics

See `references/reference.md` for:
- Performance optimization techniques
- Integration with Pydantic models
- Schema documentation standards
- Monitoring schema usage and versioning
- ClickHouse table schema alignment
- Distributed tracing with correlation IDs

## See Also

- `kafka-producer-implementation` skill - Using schemas in producers
- `kafka-consumer-implementation` skill - Consuming and validating messages
- `kafka-integration-testing` skill - End-to-end schema validation tests
- `examples/examples.md` - Comprehensive schema patterns
- `references/reference.md` - Advanced topics and integrations
