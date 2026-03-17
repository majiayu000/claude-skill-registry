---
name: pytest-mastery
description: |
  Python testing with pytest using uv package manager. Use when: (1) Running Python tests, (2) Writing test files or test functions, (3) Setting up fixtures, (4) Parametrizing tests, (5) Generating coverage reports, (6) Testing FastAPI applications, (7) Debugging test failures, (8) Configuring pytest options. Triggers: "run tests", "write tests", "test coverage", "pytest", "unit test", "integration test", "test FastAPI".
---

# pytest Testing with uv

## Quick Reference

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific file
uv run pytest tests/test_example.py

# Run specific test function
uv run pytest tests/test_example.py::test_function_name

# Run tests matching pattern
uv run pytest -k "pattern"

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

## Installation

```bash
# Add pytest as dev dependency
uv add --dev pytest

# Add coverage support
uv add --dev pytest-cov

# Add async support (for FastAPI)
uv add --dev pytest-asyncio httpx
```

## Test Discovery

pytest automatically discovers tests following these conventions:

- Files: `test_*.py` or `*_test.py`
- Functions: `test_*`
- Classes: `Test*` (no `__init__` method)
- Methods: `test_*` inside `Test*` classes

Standard project structure:
```
project/
├── src/
│   └── myapp/
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # Shared fixtures
│   ├── test_unit.py
│   └── integration/
│       └── test_api.py
└── pyproject.toml
```

## Fixtures

Fixtures provide reusable test setup/teardown:

```python
import pytest

@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Test User"}

@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn  # Test runs here
    conn.close()  # Teardown

def test_user_name(sample_user):
    assert sample_user["name"] == "Test User"
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: new instance per test
@pytest.fixture(scope="class")     # Once per test class
@pytest.fixture(scope="module")    # Once per module
@pytest.fixture(scope="session")   # Once per test session
```

### Shared Fixtures (conftest.py)

Place in `tests/conftest.py` for automatic availability:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def api_client():
    return TestClient(app)
```

## Parametrization

Run same test with multiple inputs:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected

@pytest.mark.parametrize("value", [None, "", [], {}])
def test_falsy_values(value):
    assert not value
```

## Common Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose output |
| `-vv` | More verbose |
| `-q` | Quiet mode |
| `-x` | Stop on first failure |
| `--lf` | Run last failed tests only |
| `--ff` | Run failures first |
| `-k "expr"` | Filter by name expression |
| `-m "mark"` | Run marked tests only |
| `--tb=short` | Shorter traceback |
| `--tb=no` | No traceback |
| `-s` | Show print statements |
| `--durations=10` | Show 10 slowest tests |
| `-n auto` | Parallel execution (pytest-xdist) |

## Coverage Reports

```bash
# Terminal report
uv run pytest --cov=src

# HTML report (creates htmlcov/)
uv run pytest --cov=src --cov-report=html

# With minimum threshold (fails if below)
uv run pytest --cov=src --cov-fail-under=80

# Multiple report formats
uv run pytest --cov=src --cov-report=term --cov-report=xml
```

## Markers

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    ...

@pytest.mark.skip(reason="Not implemented")
def test_future_feature():
    ...

@pytest.mark.skipif(condition, reason="...")
def test_conditional():
    ...

@pytest.mark.xfail(reason="Known bug")
def test_known_failure():
    ...
```

Run by marker:
```bash
uv run pytest -m "not slow"
uv run pytest -m "integration"
```

## pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]

[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
```

## FastAPI Testing

See [references/fastapi-testing.md](references/fastapi-testing.md) for comprehensive FastAPI testing patterns including:
- TestClient setup
- Async testing with httpx
- Database fixture patterns
- Dependency overrides
- Authentication testing

## Debugging Failed Tests

```bash
# Run with full traceback
uv run pytest --tb=long

# Drop into debugger on failure
uv run pytest --pdb

# Show local variables in traceback
uv run pytest -l

# Run only previously failed
uv run pytest --lf
```
