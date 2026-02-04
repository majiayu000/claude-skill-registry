---
name: python-testing
description: Complete Python testing system. PROACTIVELY activate for: (1) pytest fundamentals, (2) Fixtures and scopes, (3) Parameterized tests, (4) Mocking with pytest-mock, (5) Async testing with pytest-asyncio, (6) Coverage configuration, (7) FastAPI testing with httpx, (8) Property-based testing with hypothesis, (9) Snapshot testing. Provides: pytest patterns, fixture examples, mock setup, coverage config. Ensures comprehensive test coverage with best practices.
---

## Quick Reference

| pytest Command | Purpose |
|----------------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -k "name"` | Run tests matching pattern |
| `pytest -x` | Stop on first failure |
| `pytest --lf` | Run last failed |
| `pytest -n auto` | Parallel execution |

| Fixture Scope | Duration |
|---------------|----------|
| `function` | Per test (default) |
| `class` | Per test class |
| `module` | Per test file |
| `session` | Entire test run |

| Mock Pattern | Code |
|--------------|------|
| Patch function | `mocker.patch("module.func")` |
| Return value | `mock.return_value = {...}` |
| Side effect | `mock.side_effect = [a, b, exc]` |
| Assert called | `mock.assert_called_once()` |

| Marker | Use Case |
|--------|----------|
| `@pytest.mark.asyncio` | Async tests |
| `@pytest.mark.parametrize` | Multiple inputs |
| `@pytest.mark.skip` | Skip test |
| `@pytest.mark.xfail` | Expected failure |

## When to Use This Skill

Use for **testing Python code**:
- Writing pytest tests with fixtures
- Mocking external dependencies
- Testing async code
- Setting up code coverage
- Testing FastAPI applications

**Related skills:**
- For FastAPI: see `python-fastapi`
- For async patterns: see `python-asyncio`
- For CI/CD: see `python-github-actions`

---

# Python Testing Best Practices (2025)

## Overview

Modern Python testing centers around pytest as the de facto standard, with additional tools for coverage, mocking, and async testing.

## Pytest Fundamentals

### Installation

```bash
# With uv
uv add --dev pytest pytest-cov pytest-asyncio pytest-xdist

# With pip
pip install pytest pytest-cov pytest-asyncio pytest-xdist
```

### Basic Test Structure

```python
# tests/test_calculator.py
import pytest
from mypackage.calculator import add, divide

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_mixed_numbers():
    assert add(-2, 3) == 1

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_result():
    result = divide(10, 2)
    assert result == pytest.approx(5.0)
```

### Running Tests

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific file
pytest tests/test_calculator.py

# Run specific test
pytest tests/test_calculator.py::test_add_positive_numbers

# Run tests matching pattern
pytest -k "add"

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Parallel execution
pytest -n auto
```

## Fixtures

### Basic Fixtures

```python
# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def sample_user():
    """Provides a sample user dictionary."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
    }

@pytest.fixture
def db_session():
    """Provides a database session that rolls back after test."""
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.rollback()
    session.close()
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new for each test
def per_test_fixture():
    return create_resource()

@pytest.fixture(scope="class")  # Shared within test class
def per_class_fixture():
    return create_expensive_resource()

@pytest.fixture(scope="module")  # Shared within test module
def per_module_fixture():
    return create_very_expensive_resource()

@pytest.fixture(scope="session")  # Shared across entire test session
def per_session_fixture():
    resource = create_global_resource()
    yield resource
    cleanup_global_resource(resource)
```

### Parameterized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    return request.param

def test_with_multiple_databases(database_type):
    # This test runs 3 times, once for each database type
    db = create_connection(database_type)
    assert db.is_connected()
```

## Parameterized Tests

### Basic Parametrize

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize("input,expected", [
    pytest.param(1, 1, id="one"),
    pytest.param(2, 4, id="two"),
    pytest.param(3, 9, id="three"),
])
def test_square_with_ids(input, expected):
    assert input ** 2 == expected

# Run with: pytest -v
# Shows: test_square_with_ids[one] PASSED
```

### Combining Parametrize

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_combinations(x, y):
    # Runs 4 times: (1,3), (1,4), (2,3), (2,4)
    assert x + y in [4, 5, 6]
```

## Mocking

### Using pytest-mock

```python
from unittest.mock import MagicMock, patch

def test_with_mock(mocker):
    # Mock a method
    mock_api = mocker.patch("mypackage.api.fetch_data")
    mock_api.return_value = {"status": "success"}

    result = process_data()
    assert result["status"] == "success"
    mock_api.assert_called_once()

def test_mock_return_values(mocker):
    # Different return values for successive calls
    mock_func = mocker.patch("mypackage.service.get_item")
    mock_func.side_effect = [
        {"id": 1},
        {"id": 2},
        ValueError("Not found"),
    ]

    assert get_item(1) == {"id": 1}
    assert get_item(2) == {"id": 2}

    with pytest.raises(ValueError):
        get_item(3)
```

### Context Manager Mocking

```python
def test_mock_context_manager(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="file content"))

    with open("test.txt") as f:
        content = f.read()

    assert content == "file content"
    mock_open.assert_called_once_with("test.txt")
```

### Mocking Classes

```python
def test_mock_class(mocker):
    MockUser = mocker.patch("mypackage.models.User")
    mock_instance = MockUser.return_value
    mock_instance.name = "Test User"
    mock_instance.save.return_value = True

    user = create_user("Test User")
    assert user.name == "Test User"
    mock_instance.save.assert_called_once()
```

## Async Testing

### pytest-asyncio

```python
import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_async_with_fixture(async_client: AsyncClient):
    response = await async_client.get("/api/users")
    assert response.status_code == 200

# Fixture for async client
@pytest.fixture
async def async_client():
    async with AsyncClient(base_url="http://test") as client:
        yield client
```

### Async Fixtures

```python
@pytest.fixture
async def async_db_session():
    engine = create_async_engine("postgresql+asyncpg://...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession)

    async with async_session() as session:
        yield session
        await session.rollback()
```

### Testing FastAPI

```python
import pytest
from httpx import AsyncClient, ASGITransport
from myapp.main import app

@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_read_main(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.0},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
```

## Coverage

### Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-ra",
    "-q",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["*/tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
]
```

### Running with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Check coverage threshold
pytest --cov=src --cov-fail-under=80

# Coverage for specific paths
pytest --cov=src/mypackage --cov-report=term-missing
```

## Test Organization

### Recommended Structure

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests
│   ├── conftest.py      # Unit test fixtures
│   ├── test_models.py
│   └── test_utils.py
├── integration/         # Integration tests
│   ├── conftest.py
│   └── test_api.py
├── e2e/                 # End-to-end tests
│   └── test_workflows.py
└── fixtures/            # Test data
    ├── users.json
    └── products.json
```

### Conftest Hierarchy

```python
# tests/conftest.py - Shared across all tests
@pytest.fixture
def app_config():
    return {"debug": True, "testing": True}

# tests/unit/conftest.py - Unit test specific
@pytest.fixture
def mock_database(mocker):
    return mocker.MagicMock()

# tests/integration/conftest.py - Integration test specific
@pytest.fixture
def real_database():
    db = create_test_database()
    yield db
    db.cleanup()
```

## Markers

### Built-in Markers

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    pass

@pytest.mark.xfail(reason="Known bug, see issue #123")
def test_known_failure():
    assert False

@pytest.mark.slow
def test_slow_operation():
    time.sleep(10)
```

### Custom Markers

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "requires_db: marks tests that need database",
]
```

```bash
# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"

# Combine markers
pytest -m "integration and not slow"
```

## Property-Based Testing

### Hypothesis

```python
from hypothesis import given, strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)

@given(st.lists(st.integers()))
def test_sort_idempotent(items):
    sorted_once = sorted(items)
    sorted_twice = sorted(sorted_once)
    assert sorted_once == sorted_twice

@given(st.text(min_size=1))
def test_string_reverse_twice(s):
    assert s[::-1][::-1] == s

# Custom strategy
@given(st.builds(
    User,
    name=st.text(min_size=1, max_size=100),
    email=st.emails(),
    age=st.integers(min_value=0, max_value=150),
))
def test_user_validation(user):
    assert user.is_valid()
```

## Snapshot Testing

### syrupy

```python
from syrupy.assertion import SnapshotAssertion

def test_api_response(snapshot: SnapshotAssertion):
    response = get_api_response()
    assert response == snapshot

def test_html_output(snapshot: SnapshotAssertion):
    html = render_template("user.html", user=sample_user)
    assert html == snapshot(extension_class=HTMLSnapshotExtension)
```

## Best Practices

### 1. Test Naming

```python
# Clear, descriptive names
def test_user_creation_with_valid_email_succeeds():
    ...

def test_user_creation_with_invalid_email_raises_validation_error():
    ...

def test_empty_cart_returns_zero_total():
    ...
```

### 2. Arrange-Act-Assert

```python
def test_order_total():
    # Arrange
    order = Order()
    order.add_item(Item(price=10.00))
    order.add_item(Item(price=20.00))

    # Act
    total = order.calculate_total()

    # Assert
    assert total == 30.00
```

### 3. One Assertion Per Test (Generally)

```python
# Prefer multiple focused tests
def test_user_has_correct_name():
    user = create_user("John")
    assert user.name == "John"

def test_user_has_default_role():
    user = create_user("John")
    assert user.role == "member"

# Over one test with many assertions
def test_user_creation():  # Less focused
    user = create_user("John")
    assert user.name == "John"
    assert user.role == "member"
    assert user.is_active
    assert user.created_at is not None
```

### 4. Use Fixtures for Setup

```python
# Good: Reusable fixture
@pytest.fixture
def authenticated_user(db_session):
    user = User(name="Test", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_can_post(authenticated_user):
    post = authenticated_user.create_post("Hello")
    assert post.author == authenticated_user

# Avoid: Repeated setup in each test
def test_user_can_post_bad():
    user = User(name="Test", email="test@example.com")
    db_session.add(user)  # Repeated in every test
    db_session.commit()
    post = user.create_post("Hello")
    assert post.author == user
```

## Additional References

For production-ready fixture patterns beyond this guide, see:

- **[Pytest Fixtures Cookbook](references/pytest-fixtures-cookbook.md)** - SQLAlchemy async sessions, PostgreSQL with Docker, user factories, generic model factories, authentication fixtures, external API mocks, time freezing, environment fixtures, file fixtures, parametrized fixtures, cleanup patterns, Redis fixtures
