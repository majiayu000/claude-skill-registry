---
name: unit-test-writer
description: Generate comprehensive unit tests with proper structure, mocking, and
  coverage. Use for general unit testing guidance across languages.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Unit Test Writer Skill

## Purpose

This skill provides systematic guidance for writing comprehensive, maintainable unit tests that achieve high coverage and follow best practices across multiple programming languages.

## When to Use

- Need to create unit tests for new code
- Want to improve existing test coverage
- Need guidance on test structure and organization
- Writing tests following TDD methodology
- Ensuring proper mocking and fixtures

## Unit Testing Principles

### Test Structure: Arrange-Act-Assert (AAA)

Every test should follow this clear pattern:

```python
def test_feature_condition_expected():
    """Clear test description."""
    # Arrange: Setup test data and dependencies
    input_data = create_test_data()
    mock_dependency = setup_mock()

    # Act: Execute the code under test
    result = function_under_test(input_data, mock_dependency)

    # Assert: Verify expected outcomes
    assert result.status == "success"
    mock_dependency.method.assert_called_once()
```

### Test Naming Conventions

**Python (pytest):**
- Pattern: `test_<function>_<condition>_<expected_result>`
- File: `test_<source_file_name>.py`
- Examples:
  - `test_create_user_valid_data_returns_user`
  - `test_validate_email_invalid_format_raises_error`
  - `test_process_data_empty_input_returns_empty_list`

**JavaScript/TypeScript (Jest):**
- Pattern: `should <expected behavior> when <condition>`
- File: `<source_file_name>.test.ts` or `<source_file_name>.test.js`
- Examples:
  - `should return user when valid data provided`
  - `should throw error when email format is invalid`
  - `should return empty list when input is empty`

### Coverage Goals

- **Overall coverage:** ≥ 80%
- **Critical business logic:** ≥ 90%
- **Error handling paths:** 100%
- **Utility functions:** ≥ 85%

---

## Unit Testing Workflow

### 1. Analyze Code to Test

**Read and understand the source:**
```bash
# Read the source file
cat src/module/feature.py

# Identify:
# - Functions and classes to test
# - Dependencies and external calls
# - Error conditions and edge cases
# - Input validation requirements
```

**Checklist:**
- [ ] Identify all public functions/methods
- [ ] Note external dependencies (APIs, databases, file system)
- [ ] Identify edge cases and boundary conditions
- [ ] List error conditions to test
- [ ] Understand expected behavior

**Deliverable:** Analysis of test requirements

---

### 2. Create Test File Structure

**File naming:**
- Python: `tests/test_<module_name>.py`
- JavaScript/TypeScript: `tests/<ModuleName>.test.ts`

**Test file template:**

```python
"""
Unit tests for [module description].

Tests cover:
- [Functionality area 1]
- [Functionality area 2]
- Error handling and edge cases
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from typing import Any

from src.module.feature import (
    FunctionToTest,
    ClassToTest,
    ExceptionToRaise
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_input() -> dict[str, Any]:
    """Sample input data for tests."""
    return {
        "field1": "value1",
        "field2": 123
    }


@pytest.fixture
def mock_dependency() -> Mock:
    """Mock external dependency."""
    mock = Mock()
    mock.method.return_value = {"status": "success"}
    return mock


# ============================================================================
# Test Classes
# ============================================================================

class TestClassName:
    """Tests for ClassName functionality."""

    def test_init_valid_params_creates_instance(self):
        """Test initialization with valid parameters."""
        pass

    def test_method_valid_input_returns_expected(self):
        """Test method with valid input."""
        pass


# ============================================================================
# Test Functions
# ============================================================================

def test_function_valid_input_returns_expected():
    """Test function with valid input."""
    pass


def test_function_invalid_input_raises_error():
    """Test function with invalid input raises error."""
    pass
```

**Deliverable:** Structured test file

---

### 3. Write Test Cases

**Test coverage checklist:**

- [ ] **Happy path:** Normal successful execution
- [ ] **Edge cases:** Boundary conditions (empty, null, max values)
- [ ] **Error cases:** Invalid input, exceptions
- [ ] **State changes:** Verify object state after operations
- [ ] **Side effects:** Verify external calls (mocked)
- [ ] **Return values:** Verify correct outputs
- [ ] **Data validation:** Input validation tests

**Example test cases:**

```python
def test_create_user_valid_data_returns_user(sample_input, mock_db):
    """Test user creation with valid data."""
    # Arrange
    service = UserService(database=mock_db)

    # Act
    user = service.create_user(sample_input)

    # Assert
    assert user.name == sample_input["name"]
    assert user.email == sample_input["email"]
    mock_db.save.assert_called_once()


def test_create_user_duplicate_email_raises_error(mock_db):
    """Test user creation with duplicate email raises error."""
    # Arrange
    service = UserService(database=mock_db)
    mock_db.exists.return_value = True

    # Act & Assert
    with pytest.raises(DuplicateEmailError):
        service.create_user({"email": "test@example.com"})


def test_create_user_invalid_email_raises_error():
    """Test user creation with invalid email format."""
    # Arrange
    service = UserService()
    invalid_data = {"email": "not-an-email"}

    # Act & Assert
    with pytest.raises(ValidationError, match="Invalid email"):
        service.create_user(invalid_data)


@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid.email", False),
    ("", False),
    (None, False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(email, valid):
    """Test email validation with various inputs."""
    # Act
    result = validate_email(email)

    # Assert
    assert result == valid
```

**Deliverable:** Comprehensive test cases

---

### 4. Implement Mocking

**When to mock:**
- External API calls
- Database operations
- File system operations
- Time-dependent operations
- Random number generation
- External services

**Mocking patterns:**

```python
# Mock with unittest.mock
from unittest.mock import Mock, MagicMock, patch

# Method 1: Mock passed as argument
def test_with_mock_argument(mock_dependency):
    service = Service(dependency=mock_dependency)
    result = service.process()
    mock_dependency.method.assert_called_once()


# Method 2: Patch decorator
@patch('module.external_function')
def test_with_patch(mock_external):
    mock_external.return_value = "expected"
    result = function_using_external()
    assert result == "expected"


# Method 3: Context manager
def test_with_context_manager():
    with patch('module.external_function') as mock_func:
        mock_func.return_value = "expected"
        result = function_using_external()
        assert result == "expected"


# Mock side effects
def test_with_side_effect():
    mock = Mock()
    mock.method.side_effect = [1, 2, 3]  # Returns different values

    assert mock.method() == 1
    assert mock.method() == 2
    assert mock.method() == 3


# Mock exceptions
def test_with_exception():
    mock = Mock()
    mock.method.side_effect = ValueError("Error message")

    with pytest.raises(ValueError):
        mock.method()
```

**Deliverable:** Properly mocked tests

---

### 5. Write Fixtures

**Fixture patterns:**

```python
# conftest.py - Shared fixtures

import pytest
from pathlib import Path


@pytest.fixture
def sample_data() -> dict:
    """Sample data for tests."""
    return {
        "id": 1,
        "name": "test",
        "value": 123
    }


@pytest.fixture
def temp_directory(tmp_path: Path) -> Path:
    """Temporary directory for test files."""
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    return test_dir


@pytest.fixture
def mock_database() -> Mock:
    """Mock database connection."""
    mock_db = Mock()
    mock_db.connect.return_value = True
    mock_db.execute.return_value = []
    return mock_db


@pytest.fixture
def user_service(mock_database) -> UserService:
    """UserService with mocked database."""
    return UserService(database=mock_database)


# Fixture with setup and teardown
@pytest.fixture
def setup_environment():
    """Setup test environment."""
    # Setup
    original_value = os.environ.get("TEST_VAR")
    os.environ["TEST_VAR"] = "test_value"

    yield  # Test runs here

    # Teardown
    if original_value:
        os.environ["TEST_VAR"] = original_value
    else:
        del os.environ["TEST_VAR"]


# Parametrized fixture
@pytest.fixture(params=["value1", "value2", "value3"])
def test_values(request):
    """Parametrized fixture for multiple test values."""
    return request.param
```

**Deliverable:** Reusable test fixtures

---

### 6. Test Async Code

**Python async tests:**

```python
import pytest
import asyncio


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    # Arrange
    input_data = {"key": "value"}

    # Act
    result = await async_function(input_data)

    # Assert
    assert result.success is True


@pytest.mark.asyncio
async def test_async_with_mock():
    """Test async function with mock."""
    # Arrange
    mock_api = Mock()
    mock_api.fetch = AsyncMock(return_value={"data": "test"})

    # Act
    result = await process_with_api(mock_api)

    # Assert
    assert result["data"] == "test"
    mock_api.fetch.assert_called_once()
```

**JavaScript/TypeScript async tests:**

```typescript
describe('async operations', () => {
  it('should resolve with expected result', async () => {
    // Arrange
    const input = { key: 'value' };

    // Act
    const result = await asyncFunction(input);

    // Assert
    expect(result.success).toBe(true);
  });

  it('should reject with error', async () => {
    // Arrange
    const invalidInput = null;

    // Act & Assert
    await expect(asyncFunction(invalidInput)).rejects.toThrow('Invalid input');
  });
});
```

**Deliverable:** Tested async operations

---

### 7. Run Tests and Check Coverage

**Run tests:**

```bash
# Python (pytest)
pytest tests/ -v
pytest tests/test_feature.py -v
pytest tests/test_feature.py::test_specific_test -v

# With coverage
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# JavaScript/TypeScript (Jest)
npm test
jest tests/Feature.test.ts
jest --coverage
```

**Check coverage report:**

```bash
# Python - View HTML coverage report
open htmlcov/index.html

# Identify uncovered lines
pytest --cov=src --cov-report=term-missing

# JavaScript - View coverage
open coverage/lcov-report/index.html
```

**Coverage checklist:**
- [ ] Overall coverage ≥ 80%
- [ ] All critical paths covered
- [ ] All error conditions tested
- [ ] All public APIs tested
- [ ] No untested branches in critical code

**Deliverable:** Coverage report with ≥ 80% coverage

---

## Testing Best Practices

### 1. Test Independence

**Each test should be independent:**
```python
# Good: Independent tests
def test_create_user():
    user = create_user({"name": "Alice"})
    assert user.name == "Alice"

def test_delete_user():
    user = create_user({"name": "Bob"})
    delete_user(user.id)
    assert get_user(user.id) is None


# Bad: Tests depend on each other
def test_create_user():
    global created_user
    created_user = create_user({"name": "Alice"})

def test_delete_user():
    # Depends on test_create_user running first
    delete_user(created_user.id)
```

### 2. Clear Test Names

**Descriptive test names:**
```python
# Good: Clear and descriptive
def test_create_user_with_valid_email_returns_user():
    pass

def test_create_user_with_duplicate_email_raises_duplicate_error():
    pass


# Bad: Unclear names
def test_user1():
    pass

def test_error():
    pass
```

### 3. One Assertion Per Test (Generally)

```python
# Good: Tests one thing
def test_user_creation_sets_name():
    user = create_user({"name": "Alice"})
    assert user.name == "Alice"

def test_user_creation_generates_id():
    user = create_user({"name": "Alice"})
    assert user.id is not None


# Acceptable: Related assertions
def test_user_creation_returns_user_with_attributes():
    user = create_user({"name": "Alice", "email": "alice@example.com"})
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.id is not None
```

### 4. Test Behavior, Not Implementation

```python
# Good: Tests behavior
def test_user_validation_rejects_invalid_email():
    with pytest.raises(ValidationError):
        validate_user({"email": "invalid"})


# Bad: Tests implementation details
def test_user_validation_calls_email_regex():
    # Don't test that specific internal method is called
    validator = UserValidator()
    validator.validate({"email": "test@example.com"})
    assert validator._email_regex_called is True
```

### 5. Use Descriptive Assertion Messages

```python
# Good: Clear failure messages
assert len(users) == 3, f"Expected 3 users, got {len(users)}"
assert user.is_active, f"User {user.id} should be active"


# Better: Use pytest assertion introspection
assert len(users) == 3  # pytest shows actual vs expected
```

---

## Common Patterns

### Testing Exceptions

```python
# Method 1: pytest.raises context manager
def test_raises_value_error():
    with pytest.raises(ValueError):
        function_that_raises()

# Method 2: With message matching
def test_raises_specific_error():
    with pytest.raises(ValueError, match="Invalid input"):
        function_that_raises()

# Method 3: Capturing exception for inspection
def test_exception_details():
    with pytest.raises(CustomError) as exc_info:
        function_that_raises()

    assert exc_info.value.code == 400
    assert "field" in exc_info.value.details
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_value,expected", [
    ("valid@email.com", True),
    ("invalid.email", False),
    ("", False),
    ("no@domain", False),
    ("@no-user.com", False),
])
def test_email_validation(input_value, expected):
    """Test email validation with multiple inputs."""
    result = validate_email(input_value)
    assert result == expected


@pytest.mark.parametrize("user_type,can_delete", [
    ("admin", True),
    ("moderator", True),
    ("user", False),
    ("guest", False),
])
def test_deletion_permissions(user_type, can_delete):
    """Test deletion permissions by user type."""
    user = User(type=user_type)
    assert user.can_delete() == can_delete
```

### Testing File Operations

```python
def test_save_file(tmp_path):
    """Test file saving."""
    # Arrange
    file_path = tmp_path / "test_file.txt"
    content = "test content"

    # Act
    save_file(file_path, content)

    # Assert
    assert file_path.exists()
    assert file_path.read_text() == content


def test_read_file(tmp_path):
    """Test file reading."""
    # Arrange
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")

    # Act
    content = read_file(file_path)

    # Assert
    assert content == "test content"
```

### Testing Time-Dependent Code

```python
from datetime import datetime, timedelta
from unittest.mock import patch

@patch('module.datetime')
def test_time_based_function(mock_datetime):
    """Test function that depends on current time."""
    # Arrange
    fixed_time = datetime(2024, 1, 1, 12, 0, 0)
    mock_datetime.now.return_value = fixed_time

    # Act
    result = get_expiration_time()

    # Assert
    expected = fixed_time + timedelta(days=30)
    assert result == expected
```

---

## Supporting Resources

Refer to these additional files for specific guidance:

- **testing-patterns.md**: Common testing patterns and examples
- **mocking-guide.md**: Comprehensive mocking strategies
- **coverage-guide.md**: Coverage analysis and improvement strategies

---

## Integration with Testing Workflow

**Input:** Source code to test
**Process:** Analyze → Structure → Write tests → Mock → Run → Verify
**Output:** Comprehensive unit test suite with ≥ 80% coverage
**Next Step:** Integration testing or validation

---

## Quality Checklist

Before completing unit testing:

- [ ] All public functions/methods have tests
- [ ] Test naming follows conventions
- [ ] Tests follow Arrange-Act-Assert pattern
- [ ] External dependencies are mocked
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] Tests are independent
- [ ] All tests pass
- [ ] Coverage ≥ 80%
- [ ] No flaky tests
- [ ] Tests run quickly (< 1 minute)
- [ ] Clear test documentation

---

## Remember

- **Write tests first** (TDD: Red → Green → Refactor)
- **Test behavior, not implementation**
- **Mock external dependencies**
- **Keep tests simple and focused**
- **Use descriptive names**
- **Aim for high coverage of critical paths**
- **Tests are documentation** - make them readable
- **Fast tests = productive development**