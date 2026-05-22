---
name: pytest-python
description: |
  Comprehensive pytest testing skill for Python projects. Write efficient, maintainable tests with fixtures, parametrization, markers, mocking, and assertions. Use when: (1) Writing new tests for Python code, (2) Setting up pytest in a project, (3) Creating fixtures for test dependencies, (4) Parametrizing tests for multiple inputs, (5) Mocking/patching with monkeypatch, (6) Debugging test failures, (7) Organizing test suites with markers, (8) Any Python testing task.
---

# Pytest Testing for Python

## Quick Reference

### Test Discovery

Pytest auto-discovers tests matching:
- Files: `test_*.py` or `*_test.py`
- Functions: `test_*` prefix
- Classes: `Test*` prefix (no `__init__`)

### Running Tests

```bash
pytest                           # Run all tests
pytest test_mod.py               # Single module
pytest tests/                    # Directory
pytest -k "name"                 # By keyword
pytest -m slow                   # By marker
pytest test_mod.py::test_func    # Specific test
pytest --durations=10            # Show slowest tests
```

## Fixtures

Fixtures provide reusable test dependencies.

### Basic Fixture

```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_example(sample_data):
    assert sample_data["key"] == "value"
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default: per test
@pytest.fixture(scope="class")     # Per test class
@pytest.fixture(scope="module")    # Per module
@pytest.fixture(scope="session")   # Entire session
```

### Fixture with Teardown (yield)

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()  # Cleanup after test
```

### Factory Fixture

```python
@pytest.fixture
def make_user():
    def _make_user(name, role="user"):
        return {"name": name, "role": role}
    return _make_user

def test_users(make_user):
    admin = make_user("Alice", role="admin")
    user = make_user("Bob")
```

### Parametrized Fixture

```python
@pytest.fixture(params=["mysql", "postgres", "sqlite"])
def database(request):
    return create_db(request.param)
```

## Parametrization

Run tests with multiple inputs.

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert input * 2 == expected
```

### Multiple Parameters (Combinations)

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):  # Runs 4 combinations
    assert x * y > 0
```

### With Expected Failures

```python
@pytest.mark.parametrize("input,expected", [
    (1, 1),
    pytest.param(0, 1, marks=pytest.mark.xfail),
])
def test_factorial(input, expected):
    assert factorial(input) == expected
```

## Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented")
def test_feature(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix(): ...

@pytest.mark.xfail(reason="Known bug")
def test_buggy(): ...
```

### Custom Markers

Register in `pytest.ini` or `pyproject.toml`:

```ini
[pytest]
markers =
    slow: marks tests as slow
    integration: integration tests
```

```python
@pytest.mark.slow
def test_slow_operation(): ...
```

Run: `pytest -m slow` or `pytest -m "not slow"`

## Assertions

### Basic Assertions

```python
assert value == expected
assert value != other
assert value is None
assert value is not None
assert value in collection
assert isinstance(obj, MyClass)
```

### Floating Point

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(expected, rel=1e-3)
```

### Exception Testing

```python
def test_raises():
    with pytest.raises(ValueError):
        int("invalid")

def test_raises_with_match():
    with pytest.raises(ValueError, match=r"invalid.*"):
        raise ValueError("invalid input")

def test_raises_inspect():
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("test error")
    assert "test" in str(exc_info.value)
```

## Monkeypatch (Mocking)

### Patching Functions

```python
def test_api_call(monkeypatch):
    def mock_get(*args, **kwargs):
        return {"status": "ok"}

    monkeypatch.setattr("mymodule.api.get", mock_get)
    result = mymodule.fetch_data()
    assert result["status"] == "ok"
```

### Environment Variables

```python
def test_with_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert os.environ["API_KEY"] == "test-key"

def test_without_env(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
```

### Dictionary Values

```python
def test_config(monkeypatch):
    monkeypatch.setitem(app.config, "DEBUG", True)
```

## Built-in Fixtures

| Fixture | Purpose |
|---------|---------|
| `tmp_path` | Temporary directory (pathlib.Path) |
| `tmp_path_factory` | Session-scoped temp directories |
| `capsys` | Capture stdout/stderr |
| `caplog` | Capture log messages |
| `monkeypatch` | Dynamic patching |
| `request` | Fixture/test metadata |

### Examples

```python
def test_output(capsys):
    print("hello")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"

def test_logging(caplog):
    import logging
    logging.warning("test warning")
    assert "test warning" in caplog.text

def test_temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("content")
    assert file.read_text() == "content"
```

## Project Structure

Recommended layout:

```
project/
├── pyproject.toml
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
└── tests/
    ├── conftest.py      # Shared fixtures
    ├── test_module.py
    └── unit/
        └── test_specific.py
```

### conftest.py

Shared fixtures available to all tests in directory:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def app():
    return create_app(testing=True)

@pytest.fixture
def client(app):
    return app.test_client()
```

## Configuration

### pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]
```

## Best Practices

1. **One assertion focus per test** - Test one behavior per function
2. **Descriptive names** - `test_user_creation_with_invalid_email_raises_error`
3. **Use fixtures** - Avoid setup duplication
4. **Isolate tests** - No shared state between tests
5. **Fast unit tests** - Mark slow tests with `@pytest.mark.slow`
6. **Parametrize** - Use parametrize over copy-paste tests
7. **Test edge cases** - Empty inputs, boundaries, errors

## References

- [Fixtures Guide](references/fixtures.md) - Advanced fixture patterns
- [Patterns Guide](references/patterns.md) - Common testing patterns
