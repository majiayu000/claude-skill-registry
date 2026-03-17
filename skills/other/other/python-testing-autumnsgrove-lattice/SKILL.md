---
name: python-testing
description: Write and run Python tests using pytest with fixtures, mocking, coverage, and the AAA pattern. Use when writing Python tests, creating test files, or setting up pytest configuration.
---

# Python Testing Skill

## When to Activate

Activate this skill when:
- Writing Python unit tests
- Creating test files or test directories
- Setting up pytest configuration
- Working with test fixtures or mocking
- Running tests or checking coverage

## Quick Commands

```bash
# Run all tests
uv run pytest

# Run specific file
uv run pytest tests/test_auth.py

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run verbose with output
uv run pytest -v -s

# Run tests matching pattern
uv run pytest -k "test_user"

# Run last failed
uv run pytest --lf
```

## Test Structure: AAA Pattern

Follow **Arrange-Act-Assert** for clear, maintainable tests:

```python
def test_user_registration():
    # Arrange - set up test data
    email = "test@example.com"
    password = "secure_pass123"
    user_service = UserService()

    # Act - execute the function
    result = user_service.register(email, password)

    # Assert - verify the outcome
    assert result.success is True
    assert result.user.email == email
```

## Directory Structure

```
project/
├── src/
│   └── myapp/
├── tests/
│   ├── conftest.py      # Shared fixtures
│   ├── unit/
│   │   └── test_utils.py
│   ├── integration/
│   │   └── test_api.py
│   └── e2e/
│       └── test_workflows.py
└── pyproject.toml
```

## Fixtures (conftest.py)

```python
import pytest
from myapp import create_app

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    yield app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(email="test@example.com", username="testuser")
```

## Parametrized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("valid@example.com", True),
    ("invalid.email", False),
    ("special+chars@test.co.uk", True),
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected
```

## Mocking

```python
from unittest.mock import Mock, patch

def test_api_call():
    mock_response = Mock()
    mock_response.json.return_value = {"data": "success"}

    with patch("requests.get", return_value=mock_response):
        result = fetch_data("https://api.example.com")
        assert result == {"data": "success"}
```

## Common Patterns

### Testing Exceptions
```python
def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

### Testing with Temp Files
```python
def test_file_processing(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World")
    result = process_file(str(test_file))
    assert result.word_count == 2
```

### Testing Environment Variables
```python
def test_config_from_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_key_123")
    assert load_config().api_key == "test_key_123"
```

## Coverage Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["tests/*"]
```

## Naming Conventions

- Test files: `test_*.py`
- Test functions: `test_*`
- Test classes: `Test*`

## Related Resources

See `AgentUsage/testing_python.md` for complete documentation including:
- Async testing patterns
- Integration test examples
- CI/CD integration
- Test priority guidelines
