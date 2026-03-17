---
name: pytest-advanced
description: Advanced Python testing with pytest including fixtures, parametrization, mocking, markers, and plugins. Test async code, APIs, and databases. Use for Python testing, test automation, or CI/CD pipelines.
---

# Advanced pytest Testing

## Quick Reference

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -k "pattern"` | Run matching tests |
| `pytest -m marker` | Run marked tests |
| `pytest --cov=src` | Coverage report |
| `pytest -x` | Stop on first failure |
| `pytest --pdb` | Debug on failure |

## 1. Setup

### Installation

```bash
pip install pytest pytest-cov pytest-asyncio pytest-mock pytest-xdist
```

### Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --strict-markers"
testpaths = ["tests"]
pythonpath = ["src"]
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "unit: marks unit tests"
]
filterwarnings = [
    "error",
    "ignore::DeprecationWarning"
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["tests/*", "*/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError"
]
fail_under = 80
```

## 2. Fixtures

### Basic Fixtures

```python
import pytest

@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return {"id": 1, "name": "John", "email": "john@example.com"}

@pytest.fixture
def sample_users():
    """Create multiple users."""
    return [
        {"id": 1, "name": "John"},
        {"id": 2, "name": "Jane"},
        {"id": 3, "name": "Bob"}
    ]

def test_user_name(sample_user):
    assert sample_user["name"] == "John"

def test_users_count(sample_users):
    assert len(sample_users) == 3
```

### Fixture Scopes

```python
@pytest.fixture(scope="function")  # Default - runs for each test
def function_fixture():
    return create_resource()

@pytest.fixture(scope="class")  # Once per test class
def class_fixture():
    return create_resource()

@pytest.fixture(scope="module")  # Once per module
def module_fixture():
    return create_resource()

@pytest.fixture(scope="session")  # Once per test session
def session_fixture():
    return create_expensive_resource()
```

### Fixture with Setup/Teardown

```python
@pytest.fixture
def database_connection():
    # Setup
    conn = create_database_connection()

    yield conn  # Provide the fixture value

    # Teardown
    conn.close()

@pytest.fixture
def temp_directory(tmp_path):
    # tmp_path is a built-in fixture
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()

    yield test_dir

    # Cleanup is automatic with tmp_path
```

### Fixture Factory

```python
@pytest.fixture
def make_user():
    """Factory fixture to create users with custom attributes."""
    created_users = []

    def _make_user(name="John", email=None):
        user = User(
            name=name,
            email=email or f"{name.lower()}@example.com"
        )
        created_users.append(user)
        return user

    yield _make_user

    # Cleanup
    for user in created_users:
        user.delete()

def test_multiple_users(make_user):
    user1 = make_user("Alice")
    user2 = make_user("Bob", "bob@test.com")

    assert user1.name == "Alice"
    assert user2.email == "bob@test.com"
```

### Conftest.py (Shared Fixtures)

```python
# tests/conftest.py
import pytest
from myapp import create_app, db

@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app("testing")
    return app

@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture(scope="function")
def database(app):
    """Create fresh database for each test."""
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()
```

## 3. Parametrization

### Basic Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (0, 0),
    (-1, -2)
])
def test_double(input, expected):
    assert double(input) == expected

@pytest.mark.parametrize("x,y,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300)
], ids=["positive", "zeros", "mixed", "large"])
def test_add(x, y, expected):
    assert add(x, y) == expected
```

### Multiple Parametrize (Cartesian Product)

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    # Runs 4 tests: (1,10), (1,20), (2,10), (2,20)
    result = x * y
    assert result > 0
```

### Parametrize with Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database_type(request):
    return request.param

def test_database_connection(database_type):
    # Runs 3 times, once for each database
    conn = connect(database_type)
    assert conn.is_connected()
```

## 4. Markers

### Built-in Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.version_info < (3, 10), reason="Requires Python 3.10+")
def test_new_syntax():
    pass

@pytest.mark.xfail(reason="Known bug #123")
def test_known_issue():
    assert buggy_function() == expected

@pytest.mark.xfail(strict=True)  # Must fail, or test fails
def test_must_fail():
    assert False
```

### Custom Markers

```python
# pytest.ini or pyproject.toml - register markers
# [pytest]
# markers =
#     slow: marks tests as slow
#     integration: integration tests

@pytest.mark.slow
def test_slow_operation():
    time.sleep(10)
    assert True

@pytest.mark.integration
def test_database_integration(database):
    result = database.query("SELECT 1")
    assert result == 1

# Run specific markers
# pytest -m slow
# pytest -m "not slow"
# pytest -m "integration and not slow"
```

## 5. Mocking

### Using pytest-mock

```python
def test_api_call(mocker):
    # Mock a function
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {"data": "test"}

    result = fetch_data("http://api.example.com")

    mock_get.assert_called_once_with("http://api.example.com")
    assert result == {"data": "test"}

def test_class_method(mocker):
    # Mock a class method
    mocker.patch.object(UserService, "get_user", return_value={"id": 1})

    user = UserService().get_user(1)
    assert user["id"] == 1

def test_with_side_effect(mocker):
    # Mock with side effect
    mock_db = mocker.patch("myapp.database.query")
    mock_db.side_effect = [
        {"id": 1},  # First call
        {"id": 2},  # Second call
        DatabaseError("Connection lost")  # Third call raises
    ]

    assert get_user(1) == {"id": 1}
    assert get_user(2) == {"id": 2}
    with pytest.raises(DatabaseError):
        get_user(3)
```

### Mock Context Manager

```python
def test_file_read(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="test content"))

    content = read_file("test.txt")

    mock_open.assert_called_once_with("test.txt", "r")
    assert content == "test content"
```

### Spy

```python
def test_spy(mocker):
    spy = mocker.spy(MyClass, "method")

    obj = MyClass()
    result = obj.method(1, 2)

    spy.assert_called_once_with(obj, 1, 2)
    assert result == original_result  # Spy doesn't change behavior
```

## 6. Async Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result == expected

@pytest.fixture
async def async_client():
    client = await create_async_client()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/api/data")
    assert response.status == 200

# Timeout for async tests
@pytest.mark.asyncio
@pytest.mark.timeout(5)
async def test_with_timeout():
    await long_running_task()
```

## 7. Exception Testing

```python
def test_raises_exception():
    with pytest.raises(ValueError):
        raise_value_error()

def test_exception_message():
    with pytest.raises(ValueError, match=r"invalid value: \d+"):
        raise ValueError("invalid value: 42")

def test_exception_attributes():
    with pytest.raises(CustomError) as exc_info:
        raise CustomError("error", code=500)

    assert exc_info.value.code == 500
    assert "error" in str(exc_info.value)

def test_does_not_raise():
    with pytest.raises(ValueError):
        pass  # This test will FAIL because no exception was raised
```

## 8. Database Testing

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")

@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def session(engine, tables):
    """Create a new database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_create_user(session):
    user = User(name="John")
    session.add(user)
    session.commit()

    assert session.query(User).count() == 1
```

## 9. HTTP/API Testing

```python
import pytest
import responses
import httpx

# Using responses library
@responses.activate
def test_api_call():
    responses.add(
        responses.GET,
        "https://api.example.com/users",
        json={"users": [{"id": 1}]},
        status=200
    )

    result = fetch_users()
    assert len(result["users"]) == 1

# Using pytest-httpx for async
@pytest.mark.asyncio
async def test_async_api(httpx_mock):
    httpx_mock.add_response(
        url="https://api.example.com/data",
        json={"data": "test"}
    )

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")

    assert response.json() == {"data": "test"}

# Flask/FastAPI testing
@pytest.fixture
def client(app):
    return app.test_client()

def test_endpoint(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json) > 0
```

## 10. Parallel Testing

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel
pytest -n auto  # Auto-detect CPU count
pytest -n 4     # Use 4 workers
```

```python
# Mark tests that can't run in parallel
@pytest.mark.no_parallel
def test_singleton_resource():
    pass
```

## 11. Plugins and Extensions

```python
# Custom plugin in conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "custom: custom marker")

def pytest_collection_modifyitems(config, items):
    # Modify test collection
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(pytest.mark.timeout(60))

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Custom reporting
    if call.when == "call" and call.excinfo is not None:
        # Log failed tests
        pass
```

## Best Practices

1. **Use fixtures for setup** - Avoid repetition
2. **Keep tests isolated** - No shared state between tests
3. **Name tests descriptively** - `test_<what>_<condition>_<expected>`
4. **Use parametrize** - Test multiple inputs
5. **Mock external services** - Fast, reliable tests
6. **Use markers** - Organize and filter tests
7. **Run tests in parallel** - Faster CI/CD
8. **Maintain coverage** - But focus on quality
9. **Use conftest.py** - Share fixtures across modules
10. **Test edge cases** - Empty, null, boundaries
