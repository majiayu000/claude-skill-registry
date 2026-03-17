---
name: pytest-application-layer-testing
description: |
  Testing use cases and application services: use case testing with mocked gateways, DTO testing, application exception testing, orchestration testing, mocking at adapter boundaries. Coverage target: 85-90%.

  Use when: Testing use cases, testing application services, testing DTOs and data transformation, testing error handling in use cases, mocking external dependencies at layer boundaries.
allowed-tools: Read, Bash, Write
---

# Pytest Application Layer Testing

## Purpose

The application layer orchestrates domain logic with external dependencies. Tests verify that use cases correctly coordinate business logic and integration boundaries.


## When to Use This Skill

Use when testing use cases and application services with "test use case", "mock gateways", "test orchestration", or "test DTOs".

Do NOT use for domain testing (use `pytest-domain-model-testing`), adapter testing (use `pytest-adapter-integration-testing`), or pytest configuration (use `pytest-configuration`).
## Quick Start

Test use cases with mocked gateways:

```python
from unittest.mock import AsyncMock
import pytest

@pytest.mark.asyncio
async def test_extract_orders_use_case(
    mock_shopify_gateway: AsyncMock,
    mock_event_publisher: AsyncMock,
) -> None:
    """Test use case orchestration."""
    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        publisher=mock_event_publisher,
    )

    # Mock external dependencies
    async def fake_orders():
        yield create_test_order(order_id="1")
        yield create_test_order(order_id="2")

    mock_shopify_gateway.fetch_orders.return_value = fake_orders()

    # Execute
    result = await use_case.execute()

    # Verify behavior
    assert result.orders_count == 2
    mock_shopify_gateway.fetch_orders.assert_awaited_once()
    assert mock_event_publisher.publish_order.call_count == 2
```

## Instructions

### Step 1: Structure Use Case Tests with Mocked Dependencies

```python
from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, create_autospec
import pytest

from app.extraction.application.use_cases import ExtractOrdersUseCase
from app.extraction.application.ports import ShopifyPort, PublisherPort
from app.extraction.application.dtos import ExtractOrdersRequest, ExtractOrdersResponse

# Fixtures for mocked dependencies
@pytest.fixture
def mock_shopify_gateway() -> AsyncMock:
    """Mock Shopify gateway."""
    mock = create_autospec(ShopifyPort, instance=True)

    async def fake_orders():
        yield create_test_order(order_id="1")
        yield create_test_order(order_id="2")

    mock.fetch_orders.return_value = fake_orders()
    return mock

@pytest.fixture
def mock_event_publisher() -> AsyncMock:
    """Mock Kafka publisher."""
    mock = create_autospec(PublisherPort, instance=True)
    mock.publish_order.return_value = None
    mock.close.return_value = None
    return mock

class TestExtractOrdersUseCase:
    """Test extraction use case."""

    @pytest.mark.asyncio
    async def test_execute_success(
        self,
        mock_shopify_gateway: AsyncMock,
        mock_event_publisher: AsyncMock,
    ) -> None:
        """Test successful extraction."""
        # Arrange
        use_case = ExtractOrdersUseCase(
            gateway=mock_shopify_gateway,
            publisher=mock_event_publisher,
        )

        # Act
        result = await use_case.execute()

        # Assert
        assert result.total_extracted == 2
        assert result.total_published == 2
        assert result.total_errors == 0
        mock_shopify_gateway.fetch_orders.assert_awaited_once()
        assert mock_event_publisher.publish_order.call_count == 2
        mock_event_publisher.close.assert_called_once()
```

### Step 2: Test Error Handling and Recovery

```python
@pytest.mark.asyncio
async def test_use_case_with_error_recovery(
    mock_shopify_gateway: AsyncMock,
    mock_event_publisher: AsyncMock,
) -> None:
    """Test use case handles and recovers from errors."""
    # Arrange
    async def fake_orders_with_errors():
        yield create_test_order(order_id="1")
        raise RuntimeError("Temporary API error")

    mock_shopify_gateway.fetch_orders.return_value = fake_orders_with_errors()

    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        publisher=mock_event_publisher,
        max_errors=5,
    )

    # Act
    result = await use_case.execute()

    # Assert: Extracted some, had 1 error
    assert result.total_extracted == 1
    assert result.total_published == 1
    assert result.total_errors == 1

@pytest.mark.asyncio
async def test_use_case_aborts_after_max_errors(
    mock_shopify_gateway: AsyncMock,
    mock_event_publisher: AsyncMock,
) -> None:
    """Test use case aborts when errors exceed threshold."""
    from app.extraction.application.exceptions import ExtractionException

    # Arrange
    mock_event_publisher.publish_order.side_effect = RuntimeError("Kafka down")

    async def fake_orders():
        for i in range(20):
            yield create_test_order(order_id=str(i))

    mock_shopify_gateway.fetch_orders.return_value = fake_orders()

    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        publisher=mock_event_publisher,
        max_errors=10,
    )

    # Act & Assert
    with pytest.raises(ExtractionException, match="Too many errors"):
        await use_case.execute()

    # Verify cleanup
    mock_event_publisher.close.assert_called()
```

### Step 3: Test DTO Creation and Validation

```python
from __future__ import annotations

from pydantic import ValidationError
import pytest

from app.extraction.application.dtos import ExtractOrdersRequest
from app.reporting.adapters.api.dtos import ProductRankingDTO

class TestExtractOrdersRequestDTO:
    """Test DTO for use case input."""

    def test_valid_creation(self) -> None:
        """Test DTO creation with valid data."""
        from datetime import datetime

        request = ExtractOrdersRequest(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
        )

        assert request.start_date.year == 2024
        assert request.end_date.month == 12

    def test_validation_end_before_start_fails(self) -> None:
        """Test DTO validation fails when dates are invalid."""
        from datetime import datetime

        with pytest.raises(ValidationError, match="end_date must be after start_date"):
            ExtractOrdersRequest(
                start_date=datetime(2024, 12, 31),
                end_date=datetime(2024, 1, 1),  # Before start!
            )

    def test_serialization_to_dict(self) -> None:
        """Test DTO serializes to dict correctly."""
        from datetime import datetime

        request = ExtractOrdersRequest(
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 12, 31),
        )

        data = request.model_dump()

        assert "start_date" in data
        assert "end_date" in data

class TestProductRankingDTO:
    """Test DTO for API response."""

    def test_valid_creation(self) -> None:
        """Test DTO with valid data."""
        dto = ProductRankingDTO(
            title="Laptop",
            cnt_bought=100,
        )

        assert dto.title == "Laptop"
        assert dto.cnt_bought == 100

    def test_validation_negative_count_fails(self) -> None:
        """Test DTO validates cnt_bought is non-negative."""
        with pytest.raises(ValidationError):
            ProductRankingDTO(
                title="Laptop",
                cnt_bought=-5,  # Invalid!
            )

    def test_serialization_to_json(self) -> None:
        """Test DTO serializes to JSON."""
        dto = ProductRankingDTO(title="Laptop", cnt_bought=100)
        json_data = dto.model_dump_json()

        assert "Laptop" in json_data
        assert "100" in json_data
```

### Step 4: Test Use Case Interactions with Multiple Dependencies

```python
@pytest.mark.asyncio
async def test_use_case_coordinates_multiple_services(
    mock_gateway: AsyncMock,
    mock_publisher: AsyncMock,
    mock_logger: AsyncMock,
) -> None:
    """Test use case coordinates multiple dependencies correctly."""
    use_case = ExtractOrdersUseCase(
        gateway=mock_gateway,
        publisher=mock_publisher,
        logger=mock_logger,
    )

    result = await use_case.execute()

    # Verify correct orchestration order:
    # 1. Fetch from gateway
    assert mock_gateway.fetch_orders.await_count >= 1
    # 2. Publish to publisher
    assert mock_publisher.publish_order.call_count >= 1
    # 3. Log operation
    assert mock_logger.info.call_count >= 1
```

### Step 5: Test Exception Handling at Application Layer

```python
@pytest.mark.asyncio
async def test_application_exception_on_gateway_failure(
    mock_shopify_gateway: AsyncMock,
    mock_event_publisher: AsyncMock,
) -> None:
    """Test application wraps infrastructure errors."""
    from app.extraction.adapters.shopify import ShopifyApiException
    from app.extraction.application.exceptions import ExtractionApplicationException

    # Arrange: Gateway raises infrastructure error
    mock_shopify_gateway.fetch_orders.side_effect = ShopifyApiException("API down")

    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        publisher=mock_event_publisher,
    )

    # Act & Assert: Use case wraps in application exception
    with pytest.raises(ExtractionApplicationException, match="Failed to fetch"):
        await use_case.execute()

@pytest.mark.asyncio
async def test_domain_exception_propagates(
    mock_shopify_gateway: AsyncMock,
    mock_event_publisher: AsyncMock,
) -> None:
    """Test domain exceptions bubble up unchanged."""
    from app.extraction.domain.exceptions import InvalidOrderException

    # Arrange: Mocked gateway returns invalid order
    async def fake_invalid_order():
        # This would raise InvalidOrderException during processing
        raise InvalidOrderException("Order missing line items")

    mock_shopify_gateway.fetch_orders.return_value = fake_invalid_order()

    use_case = ExtractOrdersUseCase(
        gateway=mock_shopify_gateway,
        publisher=mock_event_publisher,
    )

    # Act & Assert: Domain exception propagates
    with pytest.raises(InvalidOrderException):
        await use_case.execute()
```

### Step 6: Test Use Case with Dependency Injection Verification

```python
@pytest.mark.asyncio
async def test_use_case_requires_dependencies(self) -> None:
    """Test use case cannot be created without dependencies."""
    # Missing gateway
    with pytest.raises(TypeError):
        ExtractOrdersUseCase(publisher=mock_publisher)

    # Missing publisher
    with pytest.raises(TypeError):
        ExtractOrdersUseCase(gateway=mock_gateway)

    # Both provided - OK
    use_case = ExtractOrdersUseCase(
        gateway=mock_gateway,
        publisher=mock_publisher,
    )
    assert use_case is not None
```

### Step 7: Test Use Case Response Objects

```python
from __future__ import annotations

import pytest
from app.extraction.application.dtos import ExtractOrdersResponse

class TestExtractOrdersResponse:
    """Test use case response DTO."""

    def test_response_creation(self) -> None:
        """Test response DTO creation."""
        response = ExtractOrdersResponse(
            total_extracted=100,
            total_published=98,
            total_errors=2,
        )

        assert response.total_extracted == 100
        assert response.total_published == 98
        assert response.total_errors == 2

    def test_response_success_property(self) -> None:
        """Test response has success indicator."""
        success_response = ExtractOrdersResponse(
            total_extracted=100,
            total_published=100,
            total_errors=0,
        )

        assert success_response.is_success() is True

        partial_response = ExtractOrdersResponse(
            total_extracted=100,
            total_published=95,
            total_errors=5,
        )

        assert partial_response.is_success() is False

    def test_response_summary(self) -> None:
        """Test response provides summary."""
        response = ExtractOrdersResponse(
            total_extracted=100,
            total_published=98,
            total_errors=2,
        )

        summary = response.summary()
        assert "100" in summary
        assert "98" in summary
        assert "2" in summary
```

## Examples

### Example 1: Complete Use Case Test

```python
class TestQueryTopProductsUseCase:
    """Test reporting use case."""

    @pytest.fixture
    def mock_query_gateway(self) -> AsyncMock:
        """Mock ClickHouse gateway."""
        mock = create_autospec(QueryPort, instance=True)
        mock.query_top_products.return_value = [
            ProductRanking(title="Laptop", rank=Rank(1), cnt_bought=100),
            ProductRanking(title="Mouse", rank=Rank(2), cnt_bought=50),
        ]
        return mock

    @pytest.mark.asyncio
    async def test_query_success(
        self,
        mock_query_gateway: AsyncMock,
    ) -> None:
        """Test successful query."""
        use_case = QueryTopProductsUseCase(gateway=mock_query_gateway)

        result = await use_case.execute(limit=10)

        assert len(result) == 2
        assert result[0].title == "Laptop"
        assert result[0].rank.value == 1
        mock_query_gateway.query_top_products.assert_called_once_with(limit=10)

    @pytest.mark.asyncio
    async def test_query_data_not_available(
        self,
        mock_query_gateway: AsyncMock,
    ) -> None:
        """Test when ClickHouse has no data."""
        from app.reporting.application.exceptions import DataNotAvailableException

        mock_query_gateway.query_top_products.side_effect = DataNotAvailableException(
            "Table not initialized"
        )

        use_case = QueryTopProductsUseCase(gateway=mock_query_gateway)

        with pytest.raises(DataNotAvailableException):
            await use_case.execute(limit=10)
```

### Example 2: Testing Use Case with State Changes

```python
@pytest.mark.asyncio
async def test_use_case_state_transitions(
    mock_gateway: AsyncMock,
) -> None:
    """Test use case correctly transitions through states."""
    use_case = StatefulUseCase(gateway=mock_gateway)

    # Initial state
    assert use_case.state == "IDLE"

    # After calling
    await use_case.execute()

    # Final state
    assert use_case.state == "COMPLETED"
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- pytest-asyncio >= 0.20.0
- pydantic >= 2.0 (for DTOs)
- unittest.mock (standard library)

## See Also

- [pytest-mocking-strategy](../pytest-mocking-strategy/SKILL.md) - Mocking dependencies
- [pytest-async-testing](../pytest-async-testing/SKILL.md) - Async testing
- [pytest-test-data-factories](../pytest-test-data-factories/SKILL.md) - Creating test data
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Application Layer Testing"
