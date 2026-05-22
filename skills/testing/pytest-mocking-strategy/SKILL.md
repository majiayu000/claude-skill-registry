---
name: pytest-mocking-strategy
description: |
  Master mocking strategy for pytest: when to use autospec=True vs manual mocks, AsyncMock patterns for async code, mock builders and factories, and what should NEVER be mocked. Includes type-safe mock creation patterns and decision matrix for mocking vs real objects.

  Use when: Creating unit tests with mocked dependencies, deciding whether to mock or use real objects, setting up test isolation, testing use cases with external service boundaries, or building reusable mock factories.
allowed-tools: Read, Bash, Write
---

# Pytest Mocking Strategy

## Purpose

Mocking is essential for unit testing, but over-mocking creates brittle tests that fail on refactoring. This skill provides a comprehensive framework for deciding what to mock, how to mock it safely, and when to use real objects instead.


## When to Use This Skill

Use when deciding what to mock in tests with "create mock", "mock external service", "AsyncMock pattern", or "what should I mock".

Do NOT use for domain testing (never mock domain objects), pytest configuration (use `pytest-configuration`), or test factories (use `pytest-test-data-factories`).
## Quick Start

The golden rule: **Mock external boundaries, test the unit in isolation.**

```python
from unittest.mock import AsyncMock, create_autospec
import pytest

# ✅ GOOD: Mock external dependency
@pytest.fixture
def mock_shopify_gateway() -> AsyncMock:
    mock = create_autospec(ShopifyGateway, instance=True)
    mock.fetch_orders.return_value = [create_test_order()]
    return mock

# Test uses mocked dependency
async def test_use_case(mock_shopify_gateway: AsyncMock) -> None:
    use_case = ExtractOrdersUseCase(gateway=mock_shopify_gateway)
    result = await use_case.execute()
    assert result.orders_count == 1
```

## Instructions

### Step 1: Decide What "The Unit" Is

For **function-based code**: A single function
For **class-based code**: A single method or the entire class
For **use cases**: The use case orchestration logic (not its dependencies)

**Key principle**: The unit is what you're testing, everything else should be mocked.

### Step 2: Always Use `autospec=True` (or `create_autospec()`)

`autospec` prevents typos and ensures you're only mocking real methods:

```python
# ❌ BAD: Without autospec, allows invalid calls
def test_bad():
    mock = Mock()
    mock.typo_method_name()  # No error! Dangerous!

# ✅ GOOD: With autospec, enforces interface
def test_good():
    mock = create_autospec(ShopifyGateway, instance=True)
    # mock.typo_method_name() raises AttributeError
    mock.fetch_orders.return_value = []  # Only real methods work
```

### Step 3: Use `AsyncMock` for Async Methods

```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_async_gateway() -> AsyncMock:
    mock = AsyncMock()
    mock.fetch_orders.return_value = [order1, order2]
    return mock

# For async generators:
@pytest.fixture
def mock_async_generator() -> AsyncMock:
    mock = AsyncMock()

    async def fake_generator():
        yield order1
        yield order2

    mock.fetch_orders.return_value = fake_generator()
    return mock
```

### Step 4: Apply the Mocking Decision Matrix

| What? | Mock? | Reasoning |
|-------|-------|-----------|
| **Shopify API calls** | ✅ YES | External HTTP service |
| **Kafka producers/consumers** | ✅ YES | Message queue boundary |
| **ClickHouse queries** | ✅ YES | Database boundary |
| **Order domain entity** | ❌ NO | Pure business logic, no deps |
| **ProductTitle value object** | ❌ NO | Simple immutable value |
| **Use case orchestration** | ❌ NO | The unit under test |
| **DTOs** | ❌ NO | Simple data containers |
| **Third-party library functions** | ❌ NO | Test your code, not Kafka |

### Step 5: Create Reusable Mock Factories

Store mock factories in `conftest.py` for reuse across tests:

```python
# tests/unit/conftest.py

from unittest.mock import AsyncMock, create_autospec

@pytest.fixture
def mock_shopify_gateway() -> AsyncMock:
    """Reusable mock for ShopifyGateway."""
    mock = create_autospec(ShopifyGateway, instance=True)

    async def fake_orders():
        yield create_test_order(order_id="1")
        yield create_test_order(order_id="2")

    mock.fetch_orders.return_value = fake_orders()
    return mock

@pytest.fixture
def mock_kafka_publisher() -> AsyncMock:
    """Reusable mock for Kafka publisher."""
    mock = create_autospec(PublisherPort, instance=True)
    mock.publish_order.return_value = None
    mock.close.return_value = None
    return mock
```

### Step 6: Mock Complex Side Effects Carefully

Use `side_effect` for error scenarios, but keep it simple:

```python
# ✅ GOOD: Simple side effect for retry testing
mock_gateway.fetch_orders.side_effect = [
    ShopifyApiException("Temporary error"),
    [order1, order2],  # Succeeds on second call
]

# ❌ BAD: Over-complex side effect (use parametrization instead)
def complex_side_effect(*args, **kwargs):
    if args[0] == "123":
        return order1
    elif args[0] == "456":
        return order2
    else:
        raise ValueError()

mock_gateway.get_order.side_effect = complex_side_effect
```

### Step 7: Know What NOT to Mock

**Never mock:**
- Domain entities (`Order`, `ProductRanking`)
- Value objects (`ProductTitle`, `Money`, `OrderId`)
- Domain validation logic and business rules
- Simple data structures and DTOs
- The unit under test itself

**Instead:**
- Create real instances
- Test their behavior directly
- Use factories for sensible defaults

```python
# ❌ DON'T mock domain objects
def test_bad(mocker):
    mock_order = mocker.Mock()  # Wrong!
    assert mock_order.is_valid()  # Testing the mock, not domain logic

# ✅ DO create real domain objects
def test_good():
    order = Order(
        order_id=OrderId("123"),
        customer_name="John",
        line_items=[create_test_line_item()],
        total_price=Money.from_float(99.99),
    )
    order.validate()  # Testing real business logic
    assert order.is_valid()
```

### Step 8: Verify Mock Interactions Properly

Use mock assertion methods to verify the unit called its dependencies correctly:

```python
async def test_use_case_interactions(mock_gateway: AsyncMock) -> None:
    """Verify use case calls dependencies as expected."""
    use_case = ExtractOrdersUseCase(gateway=mock_gateway)

    await use_case.execute()

    # Verify the gateway was called
    mock_gateway.fetch_orders.assert_awaited_once()  # For async

    # Verify it was called with specific arguments
    mock_gateway.fetch_orders.assert_called_once_with(
        start_date=expected_date,
        end_date=expected_date
    )

    # Verify call count for loops
    assert mock_gateway.publish.call_count == 3
```

## Examples

### Example 1: Mock External HTTP API

```python
from unittest.mock import AsyncMock, create_autospec
import pytest
from app.extraction.application.use_cases import ExtractOrdersUseCase
from app.extraction.adapters.shopify import ShopifyGateway

@pytest.fixture
def mock_shopify_gateway() -> AsyncMock:
    """Mock Shopify API calls."""
    mock = create_autospec(ShopifyGateway, instance=True)

    async def fake_orders():
        yield {"id": "1", "total": 100.0}
        yield {"id": "2", "total": 200.0}

    mock.fetch_orders.return_value = fake_orders()
    return mock

@pytest.mark.asyncio
async def test_extract_orders_success(mock_shopify_gateway: AsyncMock) -> None:
    """Test order extraction with mocked API."""
    use_case = ExtractOrdersUseCase(gateway=mock_shopify_gateway)

    result = await use_case.execute()

    assert result.orders_count == 2
    mock_shopify_gateway.fetch_orders.assert_awaited_once()
```

### Example 2: Mock with Error Scenarios

```python
from unittest.mock import AsyncMock
import pytest

@pytest.mark.asyncio
async def test_extract_orders_with_retry(
    mock_shopify_gateway: AsyncMock
) -> None:
    """Test retry logic on temporary failure."""
    # First call fails, second succeeds
    mock_shopify_gateway.fetch_orders.side_effect = [
        RuntimeError("Temporary error"),
        [{"id": "1", "total": 100.0}],
    ]

    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        max_retries=3
    )

    result = await use_case.execute()

    assert result.orders_count == 1
    assert mock_shopify_gateway.fetch_orders.call_count == 2
```

### Example 3: Builder Pattern for Complex Mocks

```python
from unittest.mock import AsyncMock, create_autospec

class MockGatewayBuilder:
    """Builder for creating configured mocks with sensible defaults."""

    def __init__(self):
        self.mock = create_autospec(ShopifyGateway, instance=True)
        self.orders = []

    def with_orders(self, orders: list) -> "MockGatewayBuilder":
        """Configure mock to return specific orders."""
        async def fake_fetch():
            for order in orders:
                yield order

        self.mock.fetch_orders.return_value = fake_fetch()
        return self

    def with_error(self, error: Exception) -> "MockGatewayBuilder":
        """Configure mock to raise error."""
        self.mock.fetch_orders.side_effect = error
        return self

    def build(self) -> AsyncMock:
        """Return configured mock."""
        return self.mock

# Usage
@pytest.mark.asyncio
async def test_with_builder():
    mock = MockGatewayBuilder()\
        .with_orders([order1, order2])\
        .build()

    use_case = ExtractOrdersUseCase(gateway=mock)
    result = await use_case.execute()
    assert result.orders_count == 2
```

### Example 4: Type-Safe Mocking with Protocols

```python
from typing import Protocol
from unittest.mock import AsyncMock, create_autospec

class OrderRepository(Protocol):
    """Protocol defining repository interface."""

    async def create(self, order_data: dict) -> Order:
        """Create order in storage."""
        ...

@pytest.fixture
def mock_repository() -> AsyncMock:
    """Create type-safe mock repository."""
    mock = create_autospec(OrderRepository, instance=True)
    mock.create = AsyncMock(return_value=Order(id="123"))
    return mock
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- unittest.mock (standard library)
- Optional: pytest-mock for `mocker` fixture
- pytest-asyncio for async test support

## See Also

- [pytest-async-testing](../pytest-async-testing/SKILL.md) - Async testing patterns
- [pytest-test-data-factories](../pytest-test-data-factories/SKILL.md) - Create test data safely
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Section: "Mocking Strategy & Test Isolation"
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Mocking Requirements by Context"
