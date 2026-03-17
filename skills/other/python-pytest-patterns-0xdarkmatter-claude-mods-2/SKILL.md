---
name: python-pytest-patterns
description: "pytest testing patterns for Python. Triggers on: pytest, fixture, mark, parametrize, mock, conftest, test coverage, unit test, integration test, pytest.raises."
compatibility: "pytest 7.0+, Python 3.9+. Some features require pytest-asyncio, pytest-mock, pytest-cov."
allowed-tools: "Read Write Bash"
depends-on: []
related-skills: [python-typing-patterns, python-async-patterns]
---

# Python pytest Patterns

Modern pytest patterns for effective testing.

## Basic Test Structure

```python
import pytest

def test_basic():
    """Simple assertion test."""
    assert 1 + 1 == 2

def test_with_description():
    """Descriptive name and docstring."""
    result = calculate_total([1, 2, 3])
    assert result == 6, "Sum should equal 6"
```

## Fixtures

```python
import pytest

@pytest.fixture
def sample_user():
    """Create test user."""
    return {"id": 1, "name": "Test User"}

@pytest.fixture
def db_connection():
    """Fixture with setup and teardown."""
    conn = create_connection()
    yield conn
    conn.close()

def test_user(sample_user):
    """Fixtures injected by name."""
    assert sample_user["name"] == "Test User"
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - per test
@pytest.fixture(scope="class")     # Per test class
@pytest.fixture(scope="module")    # Per test file
@pytest.fixture(scope="session")   # Entire test run
```

## Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected

# Multiple parameters
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):  # 4 test combinations
    assert x * y > 0
```

## Exception Testing

```python
def test_raises():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("Invalid input")
    assert "Invalid" in str(exc_info.value)

def test_raises_match():
    with pytest.raises(ValueError, match=r".*[Ii]nvalid.*"):
        raise ValueError("Invalid input")
```

## Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_buggy():
    assert broken_function() == expected

@pytest.mark.slow
def test_performance():
    """Custom marker - register in pytest.ini."""
    pass
```

## Mocking

```python
from unittest.mock import Mock, patch, MagicMock

def test_with_mock():
    mock_api = Mock()
    mock_api.get.return_value = {"status": "ok"}
    result = mock_api.get("/endpoint")
    assert result["status"] == "ok"

@patch("module.external_api")
def test_with_patch(mock_api):
    mock_api.return_value = {"data": []}
    result = function_using_api()
    mock_api.assert_called_once()
```

### pytest-mock (Recommended)

```python
def test_with_mocker(mocker):
    mock_api = mocker.patch("module.api_call")
    mock_api.return_value = {"success": True}
    result = process_data()
    assert result["success"]
```

## conftest.py

```python
# tests/conftest.py - Shared fixtures

import pytest

@pytest.fixture(scope="session")
def app():
    """Application fixture available to all tests."""
    return create_app(testing=True)

@pytest.fixture
def client(app):
    """Test client fixture."""
    return app.test_client()
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest -k "test_name"` | Run matching tests |
| `pytest -m slow` | Run marked tests |
| `pytest --lf` | Rerun last failed |
| `pytest --cov=src` | Coverage report |
| `pytest -n auto` | Parallel (pytest-xdist) |

## Additional Resources

- `./references/fixtures-advanced.md` - Factory fixtures, autouse, conftest patterns
- `./references/mocking-patterns.md` - Mock, patch, MagicMock, side_effect
- `./references/async-testing.md` - pytest-asyncio patterns
- `./references/coverage-strategies.md` - pytest-cov, branch coverage, reports
- `./references/integration-testing.md` - Database fixtures, API testing, testcontainers
- `./references/property-testing.md` - Hypothesis framework, strategies, shrinking
- `./references/test-architecture.md` - Test pyramid, organization, isolation strategies

## Scripts

- `./scripts/run-tests.sh` - Run tests with recommended options
- `./scripts/generate-conftest.sh` - Generate conftest.py boilerplate

## Assets

- `./assets/pytest.ini.template` - Recommended pytest configuration
- `./assets/conftest.py.template` - Common fixture patterns

---

## See Also

**Related Skills:**
- `python-typing-patterns` - Type-safe test code
- `python-async-patterns` - Async test patterns (pytest-asyncio)

**Testing specific frameworks:**
- `python-fastapi-patterns` - TestClient, API testing
- `python-database-patterns` - Database fixtures, transactions
