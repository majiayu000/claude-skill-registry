---
name: pytest-configuration
description: |
  Provides Complete pytest configuration: pyproject.toml setup, custom markers registration, test discovery patterns, plugin configuration, environment-specific settings. Includes conftest.py hierarchy, fixture scoping, and coverage configuration.

  Use when: Setting up pytest in a project, configuring test discovery, creating shared fixtures, setting up coverage reporting, managing test environments, organizing conftest.py files.
allowed-tools: Read, Bash, Write
---

# Pytest Configuration

## Purpose

Proper pytest configuration ensures fast test discovery, correct isolation, and consistent behavior across environments. This skill provides production-ready configuration patterns.


## When to Use This Skill

Use when setting up pytest in a project with "configure pytest", "setup test discovery", "create conftest", or "configure coverage".

Do NOT use for writing tests themselves (use layer-specific testing skills), debugging failures (use `test-debug-failures`), or mocking strategies (use `pytest-mocking-strategy`).
## Quick Start

Minimal `pyproject.toml` configuration:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

asyncio_mode = "auto"  # For async tests
asyncio_default_fixture_loop_scope = "function"  # Max isolation

addopts = [
    "--strict-markers",
    "--cov=app",
    "--cov-report=html",
    "--cov-fail-under=80",
]

markers = [
    "unit: Unit tests (fast, mocked)",
    "integration: Integration tests (external services)",
]
```

## Instructions

### Step 1: Configure Test Discovery

```toml
# pyproject.toml

[tool.pytest.ini_options]
# Where pytest looks for tests
testpaths = ["tests"]

# Test file naming pattern
python_files = ["test_*.py", "*_test.py"]

# Test class naming pattern
python_classes = ["Test*"]

# Test function naming pattern
python_functions = ["test_*"]

# Minimum Python version
minversion = "7.0"
```

### Step 2: Configure Async Support

```toml
[tool.pytest.ini_options]
# Auto-detect async tests (no decorator needed)
asyncio_mode = "auto"

# Event loop scope for async tests
# "function": New loop per test (max isolation)
# "module": Shared loop per module (faster)
# "session": Single loop for all tests (fastest)
asyncio_default_fixture_loop_scope = "function"
```

### Step 3: Set Up Custom Markers

```toml
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests (fast, fully mocked)",
    "integration: Integration tests (external services)",
    "e2e: End-to-end tests (full pipeline)",
    "slow: Tests that take significant time",
    "smoke: Critical path smoke tests",
    "skip_ci: Skip in CI environment",
]

# Usage:
# pytest -m unit          # Run only unit tests
# pytest -m "not slow"    # Exclude slow tests
# pytest -m "unit or integration"  # Multiple markers
```

### Step 4: Configure Coverage Reporting

```toml
[tool.pytest.ini_options]
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",                              # All outcomes summary
    "--showlocals",                     # Show local vars in traceback
    "--tb=short",                       # Short traceback format
    "--cov=app",                        # Coverage source
    "--cov-report=html",                # HTML report
    "--cov-report=term-missing",        # Terminal with missing lines
    "--cov-fail-under=80",              # Fail if < 80%
]

# Coverage configuration
[tool.coverage.run]
source = ["app"]
branch = true  # Branch coverage

omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/.venv/*",
]

[tool.coverage.report]
precision = 2
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@(abc\\.)?abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"
```

### Step 5: Set Up Logging in Pytest

```toml
[tool.pytest.ini_options]
log_cli = true
log_cli_level = "INFO"
log_cli_format = "%(asctime)s [%(levelname)8s] %(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"

# Or log to file
log_file = "pytest.log"
log_file_level = "DEBUG"
log_file_format = "%(asctime)s [%(levelname)8s] %(name)s: %(message)s"
```

### Step 6: Create Root conftest.py

```python
# tests/conftest.py - Root-level shared fixtures

from __future__ import annotations

import os
from typing import Generator
import pytest


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest environment before running tests."""
    # Set test environment variables
    os.environ["ENVIRONMENT"] = "test"
    os.environ["LOG_LEVEL"] = "DEBUG"


@pytest.fixture(scope="session", autouse=True)
def test_environment() -> Generator[None, None, None]:
    """Set up test environment for entire session."""
    # Save original environment
    original_env = os.environ.copy()

    # Configure test environment
    os.environ.update({
        "SHOPIFY_SHOP_URL": "https://test.myshopify.com",
        "SHOPIFY_ACCESS_TOKEN": "test_token_123",
        "KAFKA_BOOTSTRAP_SERVERS": "localhost:9092",
        "CLICKHOUSE_HOST": "localhost",
        "CLICKHOUSE_PORT": "8123",
    })

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
```

### Step 7: Create Unit Test Conftest with Fixtures

```python
# tests/unit/conftest.py - Unit test shared fixtures

from __future__ import annotations

from datetime import datetime
from typing import Optional
import pytest

from app.extraction.domain.entities import Order, LineItem
from app.extraction.domain.value_objects import OrderId, ProductId, ProductTitle, Money


# Test data factories
@pytest.fixture
def create_test_line_item():
    """Factory for LineItem with defaults."""
    def _create(
        product_id: str = "prod_1",
        title: str = "Test Product",
        quantity: int = 1,
        price: float = 99.99,
    ) -> LineItem:
        return LineItem(
            product_id=ProductId(product_id),
            product_title=ProductTitle(title),
            quantity=quantity,
            price=Money.from_float(price),
        )

    return _create


@pytest.fixture
def create_test_order(create_test_line_item):
    """Factory for Order with defaults."""
    def _create(
        order_id: str = "order_123",
        customer_name: str = "Test User",
        items: Optional[list[LineItem]] = None,
    ) -> Order:
        if items is None:
            items = [create_test_line_item()]

        total = sum(
            float(item.price.amount) * item.quantity for item in items
        )

        return Order(
            order_id=OrderId(order_id),
            created_at=datetime.now(),
            customer_name=customer_name,
            line_items=items,
            total_price=Money.from_float(total),
        )

    return _create
```

### Step 8: Create Domain-Specific Conftest Files

```python
# tests/unit/extraction/conftest.py - Extraction context fixtures

from __future__ import annotations

from unittest.mock import AsyncMock, create_autospec
import pytest

from app.extraction.application.ports import ShopifyPort, PublisherPort


@pytest.fixture
def mock_shopify_gateway() -> AsyncMock:
    """Mock Shopify gateway for extraction tests."""
    mock = create_autospec(ShopifyPort, instance=True)

    async def fake_orders():
        yield create_test_order(order_id="1")
        yield create_test_order(order_id="2")

    mock.fetch_orders.return_value = fake_orders()
    return mock


@pytest.fixture
def mock_event_publisher() -> AsyncMock:
    """Mock Kafka publisher for extraction tests."""
    mock = create_autospec(PublisherPort, instance=True)
    mock.publish_order.return_value = None
    mock.close.return_value = None
    return mock


# tests/unit/reporting/conftest.py - Reporting context fixtures

from __future__ import annotations

from unittest.mock import AsyncMock, create_autospec
import pytest

from app.reporting.application.ports import QueryPort
from app.reporting.domain.entities import ProductRanking
from app.reporting.domain.value_objects import Rank


@pytest.fixture
def mock_query_gateway() -> AsyncMock:
    """Mock ClickHouse query gateway for reporting tests."""
    mock = create_autospec(QueryPort, instance=True)
    mock.query_top_products.return_value = [
        ProductRanking(title="Laptop", rank=Rank(1), cnt_bought=100),
        ProductRanking(title="Mouse", rank=Rank(2), cnt_bought=50),
    ]
    return mock
```

### Step 9: Environment-Specific Configuration

```python
# tests/conftest.py - Handle different environments

import os
import pytest


@pytest.fixture(scope="session")
def ci_environment():
    """Detect if running in CI environment."""
    return os.getenv("CI") == "true"


@pytest.fixture(scope="session")
def database_url():
    """Get database URL based on environment."""
    if os.getenv("CI"):
        return "sqlite:///:memory:"  # In-memory for CI
    else:
        return "sqlite:///test.db"  # File-based for local


# Skip tests in CI if marked with skip_ci
def pytest_runtest_setup(item):
    """Skip tests marked with skip_ci when in CI."""
    if item.get_closest_marker("skip_ci"):
        if os.getenv("CI"):
            pytest.skip("Skipping in CI environment")
```

### Step 10: Configure Pytest Plugins

```toml
[tool.pytest.ini_options]
# Install plugins: uv add --dev pytest-asyncio pytest-cov pytest-mock pytest-xdist

plugins = [
    "pytest_asyncio",  # Async test support
    "pytest_cov",      # Coverage reporting
]
```

## Examples

### Example 1: Complete pyproject.toml

```toml
[tool.pytest.ini_options]
# Test discovery
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

# Async support
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"

# Strict mode
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
    "--showlocals",
    "--tb=short",
    "--cov=app",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]

# Custom markers
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "e2e: End-to-end tests",
    "slow: Slow tests",
]

# Logging
log_cli = true
log_cli_level = "INFO"

# Coverage
[tool.coverage.run]
source = ["app"]
branch = true
omit = ["*/tests/*"]

[tool.coverage.report]
precision = 2
show_missing = true

[tool.coverage.html]
directory = "htmlcov"
```

### Example 2: Complete Conftest Hierarchy

```
tests/
├── conftest.py                    # Root: environment setup
├── unit/
│   ├── conftest.py                # Unit test factories
│   ├── extraction/
│   │   ├── conftest.py            # Extraction mocks
│   │   └── domain/
│   │       └── test_entities.py
│   └── reporting/
│       ├── conftest.py            # Reporting mocks
│       └── domain/
│           └── test_entities.py
└── integration/
    ├── conftest.py                # Container fixtures
    └── test_kafka.py
```

### Example 3: Running Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run everything except slow tests
pytest -m "not slow"

# Run integration tests
pytest -m integration

# Run unit and integration (skip e2e)
pytest -m "unit or integration"

# Run specific context
pytest tests/unit/extraction/

# Run with parallel execution
pytest -n auto

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Requirements

- Python 3.11+
- pytest >= 7.0
- pytest-asyncio >= 0.20.0
- pytest-cov >= 4.0
- pytest-mock >= 3.10

## See Also

- [pytest-async-testing](../pytest-async-testing/SKILL.md) - Async configuration details
- [pytest-test-data-factories](../pytest-test-data-factories/SKILL.md) - conftest fixture examples
- [PYTHON_UNIT_TESTING_BEST_PRACTICES.md](../../artifacts/2025-11-09/testing-research/PYTHON_UNIT_TESTING_BEST_PRACTICES.md) - Section: "Pytest Configuration"
- [PROJECT_UNIT_TESTING_STRATEGY.md](../../artifacts/2025-11-09/testing-research/PROJECT_UNIT_TESTING_STRATEGY.md) - Section: "Pytest Configuration for This Project"
