---
name: pytest-patterns
description: Automatically applies when writing pytest tests. Ensures proper use of fixtures, parametrize, marks, mocking, async tests, and follows testing best practices.
---

# Pytest Testing Pattern Enforcer

When writing tests, follow these established pytest patterns and best practices.

## ✅ Basic Test Pattern

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

def test_function_name_success():
    """Test successful operation."""
    # Arrange
    input_data = "test input"

    # Act
    result = function_under_test(input_data)

    # Assert
    assert result == expected_output
    assert result.status == "success"

def test_function_name_error_case():
    """Test error handling."""
    # Arrange
    invalid_input = ""

    # Act & Assert
    with pytest.raises(ValueError, match="Input cannot be empty"):
        function_under_test(invalid_input)
```

## ✅ Async Test Pattern

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_async_function():
    """Test async function behavior."""
    # Arrange
    mock_data = {"id": "123", "name": "Test"}

    # Act
    result = await async_function()

    # Assert
    assert result == expected
    assert result["id"] == "123"

@pytest.mark.asyncio
@patch('module.async_dependency')
async def test_with_async_mock(mock_dependency):
    """Test with mocked async dependency."""
    # Arrange
    mock_dependency.return_value = AsyncMock(return_value={"status": "ok"})

    # Act
    result = await function_calling_dependency()

    # Assert
    assert result["status"] == "ok"
    mock_dependency.assert_called_once()
```

## Fixtures

```python
import pytest

# Function-scoped fixture (default)
@pytest.fixture
def user_data():
    """Provide test user data."""
    return {
        "id": "user_123",
        "email": "test@example.com",
        "name": "Test User"
    }

# Session-scoped fixture (created once per test session)
@pytest.fixture(scope="session")
def database_connection():
    """Provide database connection for all tests."""
    db = Database.connect("test_db")
    yield db
    db.close()

# Module-scoped fixture
@pytest.fixture(scope="module")
def api_client():
    """Provide API client for module tests."""
    client = APIClient(base_url="http://test.local")
    yield client
    client.close()

# Fixture with cleanup (teardown)
@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")

    yield file_path

    # Cleanup (runs after test)
    if file_path.exists():
        file_path.unlink()

# Usage in tests
def test_user_creation(user_data):
    """Test using fixture."""
    user = create_user(user_data)
    assert user.id == user_data["id"]
```

## Parametrize for Multiple Test Cases

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
    ("123", "123"),
])
def test_uppercase(input, expected):
    """Test uppercase conversion with multiple inputs."""
    assert uppercase(input) == expected

@pytest.mark.parametrize("email", [
    "user@example.com",
    "test.user@domain.co.uk",
    "user+tag@example.com",
])
def test_valid_emails(email):
    """Test valid email formats."""
    assert is_valid_email(email) is True

@pytest.mark.parametrize("email", [
    "invalid",
    "@example.com",
    "user@",
    "user@.com",
])
def test_invalid_emails(email):
    """Test invalid email formats."""
    assert is_valid_email(email) is False

# Multiple parameters
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_addition(a, b, expected):
    """Test addition with various inputs."""
    assert add(a, b) == expected

# Named test cases
@pytest.mark.parametrize("input,expected", [
    pytest.param("valid@email.com", True, id="valid_email"),
    pytest.param("invalid", False, id="invalid_email"),
    pytest.param("", False, id="empty_string"),
])
def test_email_validation(input, expected):
    """Test email validation."""
    assert is_valid_email(input) == expected
```

## Mocking with unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch, call

def test_with_mock():
    """Test with Mock object."""
    mock_service = Mock()
    mock_service.get_data.return_value = {"status": "success"}

    result = process_data(mock_service)

    assert result["status"] == "success"
    mock_service.get_data.assert_called_once()

def test_mock_multiple_calls():
    """Test multiple calls to mock."""
    mock = Mock()
    mock.side_effect = [1, 2, 3]  # Different return for each call

    assert mock() == 1
    assert mock() == 2
    assert mock() == 3

@patch('module.external_api_call')
def test_with_patch(mock_api):
    """Test with patched external call."""
    # Arrange
    mock_api.return_value = {"data": "test"}

    # Act
    result = function_that_calls_api()

    # Assert
    assert result["data"] == "test"
    mock_api.assert_called_once_with(expected_param)

def test_mock_http_request():
    """Test HTTP request with mock response."""
    with patch('httpx.get') as mock_get:
        # Create mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Test
        result = fetch_data_from_api()

        assert result["key"] == "value"
        mock_get.assert_called_once()

def test_verify_call_arguments():
    """Test that mock was called with specific arguments."""
    mock = Mock()
    function_with_mock(mock, param1="test", param2=123)

    # Verify call
    mock.method.assert_called_with("test", 123)

    # Verify any call in call history
    mock.method.assert_any_call("test", 123)

    # Verify call count
    assert mock.method.call_count == 1

    # Verify all calls
    mock.method.assert_has_calls([
        call("first"),
        call("second"),
    ])
```

## Pytest Marks

```python
import pytest

# Skip test
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    """Test to be implemented."""
    pass

# Skip conditionally
@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_python310_feature():
    """Test Python 3.10+ feature."""
    pass

# Expected failure
@pytest.mark.xfail(reason="Known bug in external library")
def test_with_known_bug():
    """Test that currently fails due to known bug."""
    assert buggy_function() == expected

# Custom marks
@pytest.mark.slow
def test_slow_operation():
    """Test that takes a long time."""
    pass

@pytest.mark.integration
def test_database_integration():
    """Integration test with database."""
    pass

# Run with: pytest -m "not slow" to skip slow tests
# Run with: pytest -m integration to run only integration tests
```

## Testing Exceptions

```python
import pytest

def test_exception_raised():
    """Test that exception is raised."""
    with pytest.raises(ValueError):
        function_that_raises()

def test_exception_message():
    """Test exception message."""
    with pytest.raises(ValueError, match="Invalid input"):
        function_that_raises("invalid")

def test_exception_with_context():
    """Test exception with context checking."""
    with pytest.raises(APIError) as exc_info:
        call_failing_api()

    # Check exception details
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value)
```

## Testing with Database (Fixtures)

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Create database session for test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()

    yield session

    session.rollback()
    session.close()

def test_create_user(db_session):
    """Test user creation in database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    # Verify
    found_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert found_user is not None
    assert found_user.name == "Test User"
```

## Testing File Operations

```python
import pytest

def test_file_read(tmp_path):
    """Test file reading with temporary file."""
    # Create temporary file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Test
    result = read_file(test_file)

    assert result == "test content"

def test_file_write(tmp_path):
    """Test file writing."""
    output_file = tmp_path / "output.txt"

    write_file(output_file, "new content")

    assert output_file.exists()
    assert output_file.read_text() == "new content"
```

## Test Organization

```python
# tests/test_user_service.py

class TestUserService:
    """Tests for UserService."""

    def test_create_user_success(self):
        """Test successful user creation."""
        service = UserService()
        user = service.create_user("test@example.com")
        assert user.email == "test@example.com"

    def test_create_user_duplicate_email(self):
        """Test error on duplicate email."""
        service = UserService()
        service.create_user("test@example.com")

        with pytest.raises(DuplicateEmailError):
            service.create_user("test@example.com")

    def test_get_user_found(self):
        """Test getting existing user."""
        service = UserService()
        created = service.create_user("test@example.com")

        found = service.get_user(created.id)

        assert found.id == created.id

    def test_get_user_not_found(self):
        """Test getting non-existent user."""
        service = UserService()

        with pytest.raises(UserNotFoundError):
            service.get_user("nonexistent_id")
```

## Coverage

```python
# Run tests with coverage
# pytest --cov=src --cov-report=html

# Add to pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=term-missing"

# Minimum coverage requirement
[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## ❌ Anti-Patterns

```python
# ❌ No test docstring
def test_something():
    assert True

# ❌ Testing multiple things in one test
def test_user():
    # Too much in one test - split into multiple tests
    user = create_user()
    update_user(user)
    delete_user(user)

# ❌ No arrange/act/assert structure
def test_messy():
    result = function()
    x = 5
    assert result > x
    y = calculate()

# ❌ Mutable fixture default
@pytest.fixture
def config():
    return {"key": "value"}  # Shared dict - mutations affect other tests!

# ✅ Better
@pytest.fixture
def config():
    return {"key": "value"}.copy()

# ❌ Not using parametrize
def test_email1():
    assert is_valid("test@example.com")

def test_email2():
    assert is_valid("user@domain.com")

# ✅ Better: Use parametrize
@pytest.mark.parametrize("email", ["test@example.com", "user@domain.com"])
def test_valid_email(email):
    assert is_valid(email)

# ❌ Not cleaning up resources
def test_file():
    file = open("test.txt", "w")
    file.write("test")
    # Missing: file.close()

# ✅ Better: Use context manager or fixture
def test_file():
    with open("test.txt", "w") as file:
        file.write("test")
```

## Best Practices Checklist

- ✅ Use descriptive test names: `test_function_scenario_expectation`
- ✅ Add docstrings to all test functions
- ✅ Follow Arrange/Act/Assert pattern
- ✅ Use fixtures for setup and teardown
- ✅ Use parametrize for multiple similar test cases
- ✅ Use marks to categorize tests (slow, integration, etc.)
- ✅ Mock external dependencies (APIs, databases)
- ✅ Test both success and failure cases
- ✅ Test edge cases (empty, null, boundary values)
- ✅ One assertion focus per test (but multiple asserts OK)
- ✅ Use `tmp_path` for file operations
- ✅ Clean up resources (use fixtures with yield)
- ✅ Aim for high coverage (80%+)
- ✅ Keep tests independent (no shared state)

## Auto-Apply

When writing tests:
1. Use `@pytest.mark.asyncio` for async functions
2. Use `@patch` decorator for mocking
3. Create fixtures for common test data
4. Follow naming conventions (`test_*`)
5. Test success + error + edge cases
6. Use parametrize for multiple inputs
7. Add descriptive docstrings

## Related Skills

- async-await-checker - For async test patterns
- pydantic-models - For testing models
- structured-errors - For testing error responses
- pii-redaction - For testing PII handling
