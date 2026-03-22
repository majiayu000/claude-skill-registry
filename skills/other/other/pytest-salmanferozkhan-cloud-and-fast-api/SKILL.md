---
name: pytest
description: Expert guidance for Python testing with pytest framework. Use when (1) writing unit tests or integration tests, (2) setting up test fixtures for setup/teardown, (3) parametrizing tests with multiple inputs, (4) using markers (skip, xfail, custom), (5) mocking/patching with monkeypatch or pytest-mock, (6) configuring pytest (pytest.ini, pyproject.toml, conftest.py), (7) running tests with coverage, (8) debugging test failures, or (9) testing async code, FastAPI, Django, or Flask apps.
---

# Pytest Testing Guide

Write Python tests efficiently with pytest.

## Quick Start

```bash
pip install pytest
```

```python
# test_example.py
def test_addition():
    assert 1 + 1 == 2
```

Run: `pytest` or `pytest -v`

## Core Concepts

| Concept | Example |
|---------|---------|
| Test function | `def test_something():` |
| Assertion | `assert result == expected` |
| Fixture | `@pytest.fixture` - dependency injection |
| Marker | `@pytest.mark.skip` - test metadata |
| Parametrize | `@pytest.mark.parametrize` - multiple inputs |

## Essential Patterns

### Basic Test
```python
def test_function():
    result = my_function(1, 2)
    assert result == 3
```

### Exception Testing
```python
import pytest

def test_raises():
    with pytest.raises(ValueError, match="invalid"):
        raise ValueError("invalid input")
```

### Fixture (Setup/Teardown)
```python
@pytest.fixture
def database():
    db = create_db()
    yield db          # provide to test
    db.cleanup()      # teardown

def test_query(database):
    assert database.query("SELECT 1")
```

### Parametrize
```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Mocking
```python
def test_mock(monkeypatch):
    monkeypatch.setattr("module.func", lambda: "mocked")
    monkeypatch.setenv("API_KEY", "test-key")
```

## Reference Files

| Topic | File | When to Use |
|-------|------|-------------|
| **Basics** | [basics.md](references/basics.md) | Test discovery, assertions, running tests, config |
| **Fixtures** | [fixtures.md](references/fixtures.md) | Setup/teardown, scopes, factories, conftest.py |
| **Markers** | [markers.md](references/markers.md) | skip, xfail, parametrize, custom markers |
| **Mocking** | [mocking.md](references/mocking.md) | monkeypatch, pytest-mock, spies, async mocks |
| **Plugins** | [plugins.md](references/plugins.md) | Coverage, parallel, async, Django, Flask, FastAPI |

## Common Commands

```bash
pytest                    # Run all tests
pytest -v                 # Verbose
pytest -s                 # Show prints
pytest -x                 # Stop on first failure
pytest -k "pattern"       # Run matching tests
pytest -m slow            # Run by marker
pytest --cov=mypackage    # With coverage
pytest -n auto            # Parallel (xdist)
pytest --lf               # Run last failed
pytest --pdb              # Debug on failure
```

## Project Structure

```
project/
├── src/
│   └── mypackage/
│       └── module.py
├── tests/
│   ├── conftest.py      # Shared fixtures
│   ├── test_unit.py
│   └── test_integration.py
├── pytest.ini           # Or pyproject.toml
└── requirements-test.txt
```

## Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
markers = [
    "slow: slow tests",
    "integration: integration tests",
]
```

## Built-in Fixtures

| Fixture | Purpose |
|---------|---------|
| `tmp_path` | Temp directory (pathlib.Path) |
| `tmpdir` | Temp directory (legacy) |
| `capsys` | Capture stdout/stderr |
| `caplog` | Capture logging |
| `monkeypatch` | Patch attributes/env vars |
| `request` | Test/fixture metadata |

## Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - per test
@pytest.fixture(scope="class")     # Per test class
@pytest.fixture(scope="module")    # Per file
@pytest.fixture(scope="session")   # Per test run
```

## Best Practices

- Name tests descriptively: `test_user_login_with_invalid_password_fails`
- One assertion concept per test
- Use fixtures for reusable setup
- Use `conftest.py` for shared fixtures
- Use markers to categorize tests (unit, integration, slow)
- Run with coverage: `pytest --cov --cov-report=html`
- Use parametrize to reduce duplicate tests
