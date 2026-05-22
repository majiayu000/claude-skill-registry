---
name: pytest-patterns
version: "1.0"
description: >
  Modern pytest test structure with fixtures, parametrization, and the AAA pattern.
  PROACTIVELY activate for: (1) Writing new pytest test suites, (2) Creating test fixtures,
  (3) Implementing parametrized tests, (4) Testing async code, (5) Organizing tests with conftest.py.
  Triggers: "pytest", "test", "fixture", "parametrize", "mock", "assert", "conftest", "test coverage"
core-integration:
  techniques:
    primary: ["exhaustive_edge_case_enumeration"]
    secondary: ["completeness_verification"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Pytest Modern Test Structure

## Core Principles

All Python code in Vibekit **MUST achieve 80%+ test coverage**. This skill provides authoritative patterns for writing clean, maintainable, and effective tests using pytest.

## The AAA Pattern (Arrange-Act-Assert)

Every test should follow the AAA structure:

```python
import pytest

# ✅ REQUIRED: Use AAA pattern for all tests
def test_user_creation():
    # ARRANGE: Set up test data and dependencies
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "age": 25
    }

    # ACT: Execute the code under test
    user = User.create(user_data)

    # ASSERT: Verify the outcome
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.age == 25
    assert user.id is not None

# ❌ FORBIDDEN: Tests without clear structure
def bad_test():
    user = User.create({"email": "test@example.com", "username": "testuser"})
    assert user.email == "test@example.com"
    user.update({"age": 30})
    assert user.age == 30
    # Mixing arrange/act/assert makes tests hard to understand
```

## Fixtures for Test Dependencies

Fixtures provide reusable test setup and teardown:

```python
import pytest
from typing import Generator

# ✅ REQUIRED: Use fixtures for shared setup
@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(
        id=1,
        email="test@example.com",
        username="testuser"
    )

@pytest.fixture
def database_connection() -> Generator:
    """Provide database connection with cleanup."""
    # Setup
    conn = connect_to_test_db()

    yield conn  # Provide to test

    # Teardown (always runs, even if test fails)
    conn.close()

# Using fixtures in tests
def test_user_retrieval(database_connection, sample_user):
    # ARRANGE: Dependencies injected via fixtures
    db = database_connection

    # ACT
    retrieved = db.get_user(sample_user.id)

    # ASSERT
    assert retrieved.id == sample_user.id
    assert retrieved.email == sample_user.email
```

## Fixture Scopes

Control fixture lifecycle with scopes:

```python
import pytest

# ✅ REQUIRED: Use narrowest scope possible
@pytest.fixture(scope="function")  # Default: runs for each test
def user():
    return User(id=1, email="test@example.com")

@pytest.fixture(scope="module")  # Runs once per test module
def expensive_setup():
    # Expensive operation
    return initialize_test_environment()

@pytest.fixture(scope="session")  # Runs once per test session
def database_connection():
    """Shared database for all tests."""
    conn = connect_to_test_db()
    yield conn
    conn.close()

# ❌ FORBIDDEN: Using broad scope for mutable fixtures
@pytest.fixture(scope="session")  # BAD! Can cause test interdependency
def user_list():
    return []  # Mutable state shared across tests - dangerous!

# ✅ GOOD: Use function scope for mutable data
@pytest.fixture(scope="function")
def user_list():
    return []  # Fresh list for each test
```

## Parametrized Tests

Test multiple inputs without code duplication:

```python
import pytest

# ✅ REQUIRED: Use parametrize for testing multiple cases
@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("user@subdomain.example.com", True),
    ("invalid-email", False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(email: str, expected_valid: bool):
    # ARRANGE
    validator = EmailValidator()

    # ACT
    result = validator.is_valid(email)

    # ASSERT
    assert result == expected_valid

# Multiple parameters
@pytest.mark.parametrize("age,income,expected_eligible", [
    (18, 30000, True),
    (17, 30000, False),
    (18, 20000, False),
    (25, 50000, True),
])
def test_loan_eligibility(age: int, income: int, expected_eligible: bool):
    assert check_loan_eligibility(age, income) == expected_eligible
```

## Mocking with pytest

Isolate code under test using mocks:

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

# ✅ REQUIRED: Use patch for external dependencies
def test_api_client_with_mock():
    # ARRANGE
    mock_response = Mock()
    mock_response.json.return_value = {"user_id": 123, "name": "Test User"}
    mock_response.status_code = 200

    with patch('requests.get', return_value=mock_response) as mock_get:
        client = APIClient()

        # ACT
        user = client.get_user(123)

        # ASSERT
        assert user["user_id"] == 123
        assert user["name"] == "Test User"
        mock_get.assert_called_once_with("https://api.example.com/users/123")

# Using patch as decorator
@patch('module.expensive_function')
def test_with_decorated_mock(mock_expensive):
    # ARRANGE
    mock_expensive.return_value = 42

    # ACT
    result = function_that_calls_expensive()

    # ASSERT
    assert result == 42
    mock_expensive.assert_called_once()

# Mock side effects
def test_retry_logic():
    # ARRANGE
    mock_api = Mock()
    # First call raises, second succeeds
    mock_api.fetch.side_effect = [ConnectionError("Network issue"), {"data": "success"}]

    # ACT
    result = retry_fetch(mock_api)

    # ASSERT
    assert result == {"data": "success"}
    assert mock_api.fetch.call_count == 2
```

## Testing Exceptions

Verify error handling:

```python
import pytest

# ✅ REQUIRED: Use pytest.raises for exception testing
def test_invalid_age_raises_error():
    # ARRANGE
    invalid_data = {"age": -5}

    # ACT & ASSERT
    with pytest.raises(ValueError, match="Age must be positive"):
        User.create(invalid_data)

# Verifying exception attributes
def test_custom_exception_details():
    with pytest.raises(ValidationError) as exc_info:
        validate_input({"bad": "data"})

    # Assert on exception details
    assert exc_info.value.code == "INVALID_INPUT"
    assert "bad" in str(exc_info.value)

# ❌ FORBIDDEN: Try/except for expected exceptions
def bad_exception_test():
    try:
        User.create({"age": -5})
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Don't do this - use pytest.raises
```

## Async Tests

Test asynchronous code with pytest-asyncio:

```python
import pytest
import asyncio

# ✅ REQUIRED: Use @pytest.mark.asyncio for async tests
@pytest.mark.asyncio
async def test_async_api_call():
    # ARRANGE
    client = AsyncAPIClient()

    # ACT
    result = await client.fetch_data("https://api.example.com")

    # ASSERT
    assert result["status"] == "success"

# Async fixtures
@pytest.fixture
async def async_database():
    """Async fixture with cleanup."""
    conn = await connect_async_db()
    yield conn
    await conn.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_database):
    result = await async_database.query("SELECT * FROM users")
    assert len(result) > 0
```

## Test Organization with conftest.py

Share fixtures across multiple test files:

```python
# conftest.py in tests/ directory
import pytest

@pytest.fixture(scope="session")
def database_url():
    """Provide test database URL for all tests."""
    return "postgresql://test:test@localhost/test_db"

@pytest.fixture
def sample_user():
    """Sample user available to all test modules."""
    return User(id=1, email="test@example.com", username="testuser")

# Tests in any test_*.py file can now use these fixtures
def test_user_creation(sample_user):
    assert sample_user.id == 1
```

## Fixture Factories

Create customizable fixtures:

```python
import pytest

# ✅ REQUIRED: Use fixture factories for flexible test data
@pytest.fixture
def user_factory():
    """Factory for creating users with custom attributes."""
    def _create_user(**kwargs):
        defaults = {
            "id": 1,
            "email": "default@example.com",
            "username": "default_user",
            "is_active": True,
        }
        defaults.update(kwargs)
        return User(**defaults)

    return _create_user

# Usage
def test_active_user(user_factory):
    user = user_factory(email="active@example.com", is_active=True)
    assert user.is_active is True

def test_inactive_user(user_factory):
    user = user_factory(email="inactive@example.com", is_active=False)
    assert user.is_active is False
```

## Markers for Test Organization

Categorize and selectively run tests:

```python
import pytest

# ✅ REQUIRED: Use markers to categorize tests
@pytest.mark.unit
def test_user_validation():
    """Fast unit test."""
    assert validate_email("test@example.com") is True

@pytest.mark.integration
def test_database_integration(database_connection):
    """Slower integration test."""
    user = create_user_in_db(database_connection)
    assert user.id is not None

@pytest.mark.slow
@pytest.mark.integration
def test_full_workflow():
    """Test requiring external services."""
    pass

# Run specific markers:
# pytest -m unit          # Run only unit tests
# pytest -m "not slow"    # Skip slow tests
# pytest -m "unit or integration"  # Run unit OR integration
```

## Coverage Configuration

Ensure adequate test coverage:

```python
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
addopts = [
    "--cov=src",                    # Measure coverage of src/ directory
    "--cov-report=term-missing",    # Show missing lines in terminal
    "--cov-report=html",            # Generate HTML coverage report
    "--cov-fail-under=80",          # Fail if coverage < 80%
    "--strict-markers",             # Require all markers to be registered
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests",
]

# Run with coverage
# pytest --cov
```

## When to Use This Skill

Activate this skill when:
- Writing new pytest test suites
- Creating test fixtures or factories
- Implementing parametrized tests
- Testing async code
- Organizing tests with conftest.py
- Setting up test coverage requirements

## Integration Points

This skill is a **prerequisite** for:
- `agentient-quality-assurance/advanced-testing-strategies` - Extends these patterns
- All plugins requiring 80%+ test coverage

## Related Resources

For advanced testing strategies, see:
- pytest Documentation: https://docs.pytest.org/
- Python Async Patterns: See `async-patterns` skill for async testing
