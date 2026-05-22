---
name: pytest-generator
description: Generate pytest-based unit tests for Python code. Creates test files
  following pytest conventions with proper fixtures, mocking, and parametrization.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Pytest Generator Skill

## Purpose

This skill generates pytest-based unit tests for Python code, following pytest conventions, best practices, and project standards. It creates comprehensive test suites with proper fixtures, mocking, parametrization, and coverage.

## When to Use

- Generate pytest tests for Python modules
- Create test files for new Python features
- Add missing test coverage to existing Python code
- Need pytest-specific patterns (fixtures, markers, parametrize)

## Test File Naming Convention

**Source to Test Mapping:**
- Source: `src/tools/feature/core.py`
- Test: `tests/test_core.py`
- Pattern: `test_<source_filename>.py`

**Examples:**
- `src/utils/validator.py` → `tests/test_validator.py`
- `src/models/user.py` → `tests/test_user.py`
- `src/services/auth.py` → `tests/test_auth.py`

---

## Pytest Test Generation Workflow

### 1. Analyze Python Source Code

**Read the source file:**
```bash
# Read the source to understand structure
cat src/tools/feature/core.py
```

**Identify test targets:**
- Public functions to test
- Classes and methods
- Error conditions
- Edge cases
- Dependencies (imports, external calls)

**Output:** List of functions/classes requiring tests

---

### 2. Generate Test File Structure

**Create test file with proper naming:**

```python
"""
Unit tests for [module name].

This module tests:
- [Functionality 1]
- [Functionality 2]
- Error handling and edge cases
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from typing import Any, Dict, List, Optional
from pathlib import Path

# Import functions/classes to test
from src.tools.feature.core import (
    function_to_test,
    ClassToTest,
    CustomException,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Sample data for testing.

    Returns:
        Dictionary with test data
    """
    return {
        "id": 1,
        "name": "test",
        "value": 123,
    }


@pytest.fixture
def mock_dependency() -> Mock:
    """
    Mock external dependency.

    Returns:
        Configured mock object
    """
    mock = Mock()
    mock.method.return_value = {"status": "success"}
    mock.validate.return_value = True
    return mock


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """
    Temporary directory for test files.

    Args:
        tmp_path: pytest temporary directory fixture

    Returns:
        Path to test directory
    """
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    return test_dir


# ============================================================================
# Test Classes (for testing classes)
# ============================================================================

class TestClassName:
    """Tests for ClassName."""

    def test_init_valid_params_creates_instance(self):
        """Test initialization with valid parameters."""
        # Arrange & Act
        instance = ClassToTest(param="value")

        # Assert
        assert instance.param == "value"
        assert instance.initialized is True

    def test_method_valid_input_returns_expected(self, sample_data):
        """Test method with valid input."""
        # Arrange
        instance = ClassToTest()

        # Act
        result = instance.method(sample_data)

        # Assert
        assert result["processed"] is True
        assert result["id"] == sample_data["id"]

    def test_method_invalid_input_raises_error(self):
        """Test method with invalid input raises error."""
        # Arrange
        instance = ClassToTest()
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid input"):
            instance.method(invalid_data)


# ============================================================================
# Test Functions
# ============================================================================

def test_function_valid_input_returns_expected(sample_data):
    """Test function with valid input returns expected result."""
    # Arrange
    expected = "processed"

    # Act
    result = function_to_test(sample_data)

    # Assert
    assert result == expected


def test_function_empty_input_returns_empty():
    """Test function with empty input returns empty result."""
    # Arrange
    empty_input = {}

    # Act
    result = function_to_test(empty_input)

    # Assert
    assert result == {}


def test_function_none_input_raises_error():
    """Test function with None input raises ValueError."""
    # Arrange
    invalid_input = None

    # Act & Assert
    with pytest.raises(ValueError, match="Input cannot be None"):
        function_to_test(invalid_input)


def test_function_with_mock_dependency(mock_dependency):
    """Test function with mocked external dependency."""
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = function_using_dependency(input_data, mock_dependency)

    # Assert
    assert result["status"] == "success"
    mock_dependency.method.assert_called_once_with(input_data)


@patch('src.tools.feature.core.external_api_call')
def test_function_with_patched_external(mock_api):
    """Test function with patched external API call."""
    # Arrange
    mock_api.return_value = {"data": "test"}
    input_data = {"key": "value"}

    # Act
    result = function_with_api(input_data)

    # Assert
    assert result["data"] == "test"
    mock_api.assert_called_once()


# ============================================================================
# Parametrized Tests
# ============================================================================

@pytest.mark.parametrize("input_value,expected", [
    ("valid@email.com", True),
    ("invalid.email", False),
    ("", False),
    (None, False),
    ("no@domain", False),
    ("@no-user.com", False),
])
def test_validation_multiple_inputs(input_value, expected):
    """Test validation with multiple input scenarios."""
    # Act
    result = validate_input(input_value)

    # Assert
    assert result == expected


@pytest.mark.parametrize("user_type,permission", [
    ("admin", "all"),
    ("moderator", "edit"),
    ("user", "read"),
    ("guest", "none"),
])
def test_permissions_by_user_type(user_type, permission):
    """Test permissions based on user type."""
    # Arrange
    user = {"type": user_type}

    # Act
    result = get_permissions(user)

    # Assert
    assert result == permission


# ============================================================================
# Async Tests
# ============================================================================

@pytest.mark.asyncio
async def test_async_function_success():
    """Test async function with successful execution."""
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = await async_function(input_data)

    # Assert
    assert result.success is True
    assert result.data == input_data


@pytest.mark.asyncio
async def test_async_function_with_mock():
    """Test async function with mocked dependency."""
    # Arrange
    mock_service = Mock()
    mock_service.fetch = AsyncMock(return_value={"data": "test"})
    input_data = {"key": "value"}

    # Act
    result = await async_function_with_service(input_data, mock_service)

    # Assert
    assert result["data"] == "test"
    mock_service.fetch.assert_awaited_once()


# ============================================================================
# Exception Tests
# ============================================================================

def test_custom_exception_raised():
    """Test that custom exception is raised."""
    # Arrange
    invalid_input = "invalid"

    # Act & Assert
    with pytest.raises(CustomException):
        function_that_raises(invalid_input)


def test_exception_message_content():
    """Test exception message contains expected content."""
    # Arrange
    invalid_input = "invalid"

    # Act & Assert
    with pytest.raises(CustomException, match="Expected error message"):
        function_that_raises(invalid_input)


def test_exception_attributes():
    """Test exception has expected attributes."""
    # Arrange
    invalid_input = "invalid"

    # Act & Assert
    with pytest.raises(CustomException) as exc_info:
        function_that_raises(invalid_input)

    assert exc_info.value.code == 400
    assert "field" in exc_info.value.details


# ============================================================================
# File Operation Tests
# ============================================================================

def test_save_file(temp_directory):
    """Test file saving functionality."""
    # Arrange
    file_path = temp_directory / "test_file.txt"
    content = "test content"

    # Act
    save_file(file_path, content)

    # Assert
    assert file_path.exists()
    assert file_path.read_text() == content


def test_read_file(temp_directory):
    """Test file reading functionality."""
    # Arrange
    file_path = temp_directory / "test_file.txt"
    expected_content = "test content"
    file_path.write_text(expected_content)

    # Act
    content = read_file(file_path)

    # Assert
    assert content == expected_content


def test_file_not_found_raises_error(temp_directory):
    """Test reading non-existent file raises error."""
    # Arrange
    missing_file = temp_directory / "missing.txt"

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        read_file(missing_file)


# ============================================================================
# Marker Examples
# ============================================================================

@pytest.mark.slow
def test_slow_operation():
    """Test slow operation (marked as slow)."""
    # This test can be skipped with: pytest -m "not slow"
    pass


@pytest.mark.integration
def test_integration_scenario():
    """Test integration scenario (marked as integration)."""
    # Run only integration tests: pytest -m integration
    pass


@pytest.mark.skipif(sys.version_info < (3, 9), reason="Requires Python 3.9+")
def test_python39_feature():
    """Test feature that requires Python 3.9+."""
    pass


# ============================================================================
# Fixture Scope Examples
# ============================================================================

@pytest.fixture(scope="module")
def expensive_setup():
    """
    Expensive setup that runs once per module.

    Returns:
        Setup result
    """
    # Setup runs once for entire test module
    result = perform_expensive_setup()
    yield result
    # Teardown runs once after all tests
    cleanup(result)


@pytest.fixture(scope="function")
def per_test_setup():
    """
    Setup that runs before each test function.

    Returns:
        Setup result
    """
    # Setup runs before each test
    result = setup()
    yield result
    # Teardown runs after each test
    teardown(result)
```

**Deliverable:** Complete pytest test file

---

## Pytest-Specific Patterns

### 1. Fixtures

**Basic fixture:**
```python
@pytest.fixture
def sample_user():
    """Create sample user for testing."""
    return User(name="Test User", email="test@example.com")
```

**Fixture with setup and teardown:**
```python
@pytest.fixture
def database_connection():
    """Database connection with cleanup."""
    # Setup
    conn = connect_to_database()

    yield conn  # Test uses connection here

    # Teardown
    conn.close()
```

**Fixture with parameters:**
```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database_type(request):
    """Parametrized database fixture."""
    return request.param


def test_with_all_databases(database_type):
    """Test runs 3 times, once per database."""
    db = connect(database_type)
    assert db.connected
```

**Fixture scopes:**
```python
@pytest.fixture(scope="function")  # Default: runs per test
def per_test():
    pass


@pytest.fixture(scope="class")  # Runs once per test class
def per_class():
    pass


@pytest.fixture(scope="module")  # Runs once per module
def per_module():
    pass


@pytest.fixture(scope="session")  # Runs once per session
def per_session():
    pass
```

### 2. Parametrize

**Basic parametrization:**
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert square(input) == expected
```

**Multiple parameters:**
```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (10, 20, 30),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

**Named parameters:**
```python
@pytest.mark.parametrize("test_input,expected", [
    pytest.param("valid", True, id="valid_input"),
    pytest.param("invalid", False, id="invalid_input"),
    pytest.param("", False, id="empty_input"),
])
def test_validation(test_input, expected):
    assert validate(test_input) == expected
```

### 3. Markers

**Built-in markers:**
```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass


@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_buggy_feature():
    pass


@pytest.mark.slow
def test_slow_operation():
    pass
```

**Custom markers (in pytest.ini):**
```ini
[pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests
```

### 4. Mocking with pytest

**Mock with pytest-mock:**
```python
def test_with_mocker(mocker):
    """Test using pytest-mock plugin."""
    mock_api = mocker.patch('module.api_call')
    mock_api.return_value = {"status": "success"}

    result = function_using_api()

    assert result["status"] == "success"
    mock_api.assert_called_once()
```

**Mock attributes:**
```python
def test_mock_attributes(mocker):
    """Test with mocked object attributes."""
    mock_obj = mocker.Mock()
    mock_obj.property = "value"
    mock_obj.method.return_value = 42

    assert mock_obj.property == "value"
    assert mock_obj.method() == 42
```

### 5. Async Testing

**Async test:**
```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result.success


@pytest.mark.asyncio
async def test_async_with_mock(mocker):
    """Test async with mocked async call."""
    mock_service = mocker.Mock()
    mock_service.fetch = AsyncMock(return_value="data")

    result = await function_with_async_call(mock_service)

    assert result == "data"
    mock_service.fetch.assert_awaited_once()
```

---

## Test Generation Strategy

### For Functions

1. **Happy path test:** Normal successful execution
2. **Edge case tests:** Empty input, max values, min values
3. **Error tests:** Invalid input, None values
4. **Dependency tests:** Mock external dependencies

### For Classes

1. **Initialization tests:** Valid params, invalid params
2. **Method tests:** Each public method
3. **State tests:** Verify state changes
4. **Property tests:** Getters and setters
5. **Error tests:** Exception handling

### For Modules

1. **Import tests:** Module can be imported
2. **Public API tests:** All public functions/classes
3. **Integration tests:** Module interactions
4. **Configuration tests:** Config loading and validation

---

## Running Pytest

**Basic commands:**
```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term-missing

# Run with markers
pytest -m "not slow"
pytest -m integration

# Run in parallel (with pytest-xdist)
pytest -n auto

# Run with output
pytest -s  # Show print statements
pytest -v -s  # Verbose + output
```

**Coverage commands:**
```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html

# Check coverage threshold
pytest --cov=src --cov-fail-under=80

# Show missing lines
pytest --cov=src --cov-report=term-missing
```

---

## Best Practices

1. **Use descriptive test names:** `test_function_condition_expected_result`
2. **Follow AAA pattern:** Arrange, Act, Assert
3. **One assertion per test** (generally)
4. **Use fixtures for setup:** Reusable test setup
5. **Mock external dependencies:** Isolate unit under test
6. **Parametrize similar tests:** Reduce code duplication
7. **Use markers for organization:** Group related tests
8. **Keep tests independent:** No test depends on another
9. **Test edge cases:** Empty, None, max values
10. **Test error conditions:** Exceptions and failures

---

## Quality Checklist

Before marking tests complete:

- [ ] Test file properly named (`test_<module>.py`)
- [ ] All public functions/classes tested
- [ ] Happy path tests included
- [ ] Edge case tests included
- [ ] Error condition tests included
- [ ] External dependencies mocked
- [ ] Fixtures used for reusable setup
- [ ] Tests follow AAA pattern
- [ ] Test names are descriptive
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] No flaky tests
- [ ] Tests run quickly

---

## Integration with Testing Workflow

**Input:** Python source file to test
**Process:** Analyze → Generate structure → Write tests → Run & verify
**Output:** pytest test file with ≥ 80% coverage
**Next Step:** Integration testing or code review

---

## Remember

- **Follow naming convention:** `test_<source_file>.py`
- **Use pytest fixtures** for reusable setup
- **Parametrize** to reduce duplication
- **Mock external calls** to isolate tests
- **Test behavior, not implementation**
- **Aim for 80%+ coverage**
- **Keep tests fast and independent**