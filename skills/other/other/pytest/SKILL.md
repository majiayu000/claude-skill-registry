---
name: pytest
description: Python testing framework for writing simple, scalable, and powerful tests
when_to_use: When you need to write, run, or organize Python tests with fixtures, parametrization, or async testing
---

# Pytest Testing Framework

Pytest is a mature Python testing framework that makes it easy to write small tests while scaling to support complex functional testing.

## Quick Start

### Basic Test Structure

```python
# test_example.py
def test_addition():
    assert 2 + 2 == 4

def test_string_operations():
    assert "hello".upper() == "HELLO"
    assert "world" in "hello world"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest test_example.py

# Run specific test function
uv run pytest test_example.py::test_addition
```

## Common Patterns

### Fixtures

**Basic fixture definition:**

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

def test_user_data(sample_data):
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
```

**Fixture with setup and teardown:**

```python
@pytest.fixture
def database_connection():
    # Setup
    conn = create_database_connection()
    yield conn
    # Teardown
    conn.close()

def test_database_query(database_connection):
    result = database_connection.query("SELECT * FROM users")
    assert len(result) > 0
```

**Fixture scopes:**

```python
@pytest.fixture(scope="function")  # Default - created per test
def temp_file():
    pass

@pytest.fixture(scope="module")    # Created once per module
def module_resource():
    pass

@pytest.fixture(scope="session")   # Created once per test session
def session_resource():
    pass
```

### Parametrization

**Basic parametrization:**

```python
@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 54),
])
def test_eval(input, expected):
    assert eval(input) == expected
```

**Parametrized fixtures:**

```python
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def database(request):
    if request.param == "mysql":
        return MySQLConnection()
    elif request.param == "postgresql":
        return PostgreSQLConnection()
    else:
        return SQLiteConnection()

def test_database_operations(database):
    # Test runs 3 times, once for each database type
    result = database.execute("SELECT 1")
    assert result == 1
```

**Stacking parametrization for combinatorial testing:**

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    # Runs 4 times: (0,2), (0,3), (1,2), (1,3)
    assert x + y > 1
```

### Async Testing

**Basic async test:**

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

**Async fixtures:**

```python
@pytest.fixture
async def async_client():
    client = AsyncClient()
    await client.connect()
    yield client
    await client.disconnect()

@pytest.mark.asyncio
async def test_async_api(async_client):
    response = await async_client.get("/api/data")
    assert response.status_code == 200
```

### Test Organization

**Using conftest.py for shared fixtures:**

```python
# conftest.py
@pytest.fixture
def authenticated_client():
    client = create_test_client()
    client.login("testuser", "password")
    return client

@pytest.fixture(scope="session")
def test_database():
    db = create_test_database()
    yield db
    db.cleanup()
```

**Test classes:**

```python
class TestUserAPI:
    def test_create_user(self, authenticated_client):
        response = authenticated_client.post("/users", json={"name": "John"})
        assert response.status_code == 201

    def test_get_user(self, authenticated_client):
        user_id = create_test_user()
        response = authenticated_client.get(f"/users/{user_id}")
        assert response.status_code == 200
```

### Mocking and Patching

**Using monkeypatch fixture:**

```python
def test_environment_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key")
    assert get_api_key() == "test-key"

def test_file_operations(monkeypatch, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    monkeypatch.setattr("module.FILE_PATH", str(test_file))
    assert read_file_content() == "test content"
```

### Markers and Selection

**Custom markers:**

```python
# pytest.ini
[tool:pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

# test_file.py
@pytest.mark.slow
def test_expensive_operation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass
```

**Running tests by marker:**

```bash
# Run only unit tests
uv run pytest -m unit

# Skip slow tests
uv run pytest -m "not slow"

# Run integration or unit tests
uv run pytest -m "integration or unit"
```

## Practical Code Snippets

### API Testing

```python
import pytest
from fastapi.testclient import TestClient
from myapp import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {"username": "testuser", "email": "test@example.com"}

def test_create_user(client, test_user):
    response = client.post("/users/", json=test_user)
    assert response.status_code == 201
    assert response.json()["username"] == test_user["username"]

def test_get_user(client, test_user):
    # Create user first
    create_response = client.post("/users/", json=test_user)
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]
```

### Database Testing

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()

def test_user_creation(test_db):
    user = User(name="John", email="john@example.com")
    test_db.add(user)
    test_db.commit()

    retrieved_user = test_db.query(User).filter_by(name="John").first()
    assert retrieved_user.email == "john@example.com"
```

### Error Handling Testing

```python
def test_invalid_input_raises_error():
    with pytest.raises(ValueError, match="Invalid input"):
        process_input("invalid")

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_nonexistent_file()

def test_custom_exception():
    with pytest.raises(CustomAPIError) as exc_info:
        call_api_endpoint()
    assert exc_info.value.status_code == 404
    assert "not found" in str(exc_info.value)
```

## Requirements

- Python 3.7+
- pytest (`uv add --dev pytest`)
- For async testing: pytest-asyncio (`uv add --dev pytest-asyncio`)
- For API testing: web framework test client (e.g., `uv add --dev httpx` for async HTTP tests)
