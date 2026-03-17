---
name: python-testing-patterns
description: Implement comprehensive testing strategies with pytest, fixtures, mocking, and test-driven development. Use when writing Python tests, setting up test suites, or implementing testing best practices.
---

# Python Testing Patterns

Comprehensive guide to implementing robust testing strategies in Python using pytest, fixtures, mocking, parameterization, and test-driven development practices.

## When to Use This Skill

- Writing unit tests for Python code
- Setting up test suites and test infrastructure
- Implementing test-driven development (TDD)
- Creating integration tests for APIs and services
- Mocking external dependencies and services
- Testing async code and concurrent operations
- Setting up continuous testing in CI/CD
- Implementing property-based testing
- Testing database operations
- Debugging failing tests
- Testing FastAPI SSE endpoints
- Testing agent communication via Unix sockets
- Writing E2E tests for complete media workflow

## Core Concepts

### 1. Test Types
- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test interaction between components
- **Functional Tests**: Test complete features end-to-end
- **Performance Tests**: Measure speed and resource usage

### 2. Test Structure (AAA Pattern)
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code under test
- **Assert**: Verify the results

### 3. Test Coverage
- Measure what code is exercised by tests
- Identify untested code paths
- Aim for meaningful coverage, not just high percentages

### 4. Test Isolation
- Tests should be independent
- No shared state between tests
- Each test should clean up after itself

## Quick Start

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """Basic test example."""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """Test with negative numbers."""
    assert add(-1, 1) == 0

# Run with: pytest test_example.py
```

## Fundamental Patterns

### Pattern 1: Basic pytest Tests

```python
# test_calculator.py
import pytest

class Calculator:
    """Simple calculator for testing."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def test_addition():
    """Test addition."""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0


def test_subtraction():
    """Test subtraction."""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_multiplication():
    """Test multiplication."""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(0, 5) == 0


def test_division():
    """Test division."""
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    assert calc.divide(5, 2) == 2.5


def test_division_by_zero():
    """Test division by zero raises error."""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### Pattern 2: Fixtures for Setup and Teardown

```python
# test_database.py
import pytest
from typing import Generator

class Database:
    """Simple database class."""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """Connect to database."""
        self.connected = True

    def disconnect(self):
        """Disconnect from database."""
        self.connected = False

    def query(self, sql: str) -> list:
        """Execute query."""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """Fixture that provides connected database."""
    # Setup
    database = Database("sqlite:///:memory:")
    database.connect()

    # Provide to test
    yield database

    # Teardown
    database.disconnect()


def test_database_query(db):
    """Test database query with fixture."""
    results = db.query("SELECT * FROM users")
    assert len(results) == 1
    assert results[0]["name"] == "Test"


@pytest.fixture(scope="session")
def app_config():
    """Session-scoped fixture - created once per test session."""
    return {
        "database_url": "postgresql://localhost/test",
        "api_key": "test-key",
        "debug": True
    }


@pytest.fixture(scope="module")
def api_client(app_config):
    """Module-scoped fixture - created once per test module."""
    # Setup expensive resource
    client = {"config": app_config, "session": "active"}
    yield client
    # Cleanup
    client["session"] = "closed"


def test_api_client(api_client):
    """Test using api client fixture."""
    assert api_client["session"] == "active"
    assert api_client["config"]["debug"] is True
```

### Pattern 3: Parameterized Tests

```python
# test_validation.py
import pytest

def is_valid_email(email: str) -> bool:
    """Check if email is valid."""
    return "@" in email and "." in email.split("@")[1]


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain", False),
    ("", False),
])
def test_email_validation(email, expected):
    """Test email validation with various inputs."""
    assert is_valid_email(email) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition_parameterized(a, b, expected):
    """Test addition with multiple parameter sets."""
    from test_calculator import Calculator
    calc = Calculator()
    assert calc.add(a, b) == expected


# Using pytest.param for special cases
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    """Test with custom test IDs."""
    assert (value > 0) == expected
```

### Pattern 4: Mocking with unittest.mock

```python
# test_api_client.py
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

class APIClient:
    """Simple API client."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """Fetch user from API."""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, data: dict) -> dict:
        """Create new user."""
        response = requests.post(f"{self.base_url}/users", json=data)
        response.raise_for_status()
        return response.json()


def test_get_user_success():
    """Test successful API call with mock."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)

        assert user["id"] == 1
        assert user["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_get_user_not_found():
    """Test API call with 404 error."""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)


@patch("requests.post")
def test_create_user(mock_post):
    """Test user creation with decorator syntax."""
    client = APIClient("https://api.example.com")

    mock_post.return_value.json.return_value = {"id": 2, "name": "Jane Doe"}
    mock_post.return_value.raise_for_status.return_value = None

    user_data = {"name": "Jane Doe", "email": "jane@example.com"}
    result = client.create_user(user_data)

    assert result["id"] == 2
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.kwargs["json"] == user_data
```

### Pattern 5: Testing Exceptions

```python
# test_exceptions.py
import pytest

def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a / b


def test_zero_division():
    """Test exception is raised for division by zero."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_zero_division_with_message():
    """Test exception message."""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)


def test_type_error():
    """Test type error exception."""
    with pytest.raises(TypeError, match="must be numbers"):
        divide("10", 5)


def test_exception_info():
    """Test accessing exception info."""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)
```

## Advanced Patterns

### Pattern 6: Testing Async Code

```python
# test_async.py
import pytest
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data asynchronously."""
    await asyncio.sleep(0.1)
    return {"url": url, "data": "result"}


@pytest.mark.asyncio
async def test_fetch_data():
    """Test async function."""
    result = await fetch_data("https://api.example.com")
    assert result["url"] == "https://api.example.com"
    assert "data" in result


@pytest.mark.asyncio
async def test_concurrent_fetches():
    """Test concurrent async operations."""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    assert len(results) == 3
    assert all("data" in r for r in results)


@pytest.fixture
async def async_client():
    """Async fixture."""
    client = {"connected": True}
    yield client
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """Test using async fixture."""
    assert async_client["connected"] is True
```

### Pattern 7: Monkeypatch for Testing

```python
# test_environment.py
import os
import pytest

def get_database_url() -> str:
    """Get database URL from environment."""
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")


def test_database_url_default():
    """Test default database URL."""
    # Will use actual environment variable if set
    url = get_database_url()
    assert url


def test_database_url_custom(monkeypatch):
    """Test custom database URL with monkeypatch."""
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"


def test_database_url_not_set(monkeypatch):
    """Test when env var is not set."""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"


class Config:
    """Configuration class."""

    def __init__(self):
        self.api_key = "production-key"

    def get_api_key(self):
        return self.api_key


def test_monkeypatch_attribute(monkeypatch):
    """Test monkeypatching object attributes."""
    config = Config()
    monkeypatch.setattr(config, "api_key", "test-key")
    assert config.get_api_key() == "test-key"
```

### Pattern 8: Temporary Files and Directories

```python
# test_file_operations.py
import pytest
from pathlib import Path

def save_data(filepath: Path, data: str):
    """Save data to file."""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """Load data from file."""
    return filepath.read_text()


def test_file_operations(tmp_path):
    """Test file operations with temporary directory."""
    # tmp_path is a pathlib.Path object
    test_file = tmp_path / "test_data.txt"

    # Save data
    save_data(test_file, "Hello, World!")

    # Verify file exists
    assert test_file.exists()

    # Load and verify data
    data = load_data(test_file)
    assert data == "Hello, World!"


def test_multiple_files(tmp_path):
    """Test with multiple temporary files."""
    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    for filename, content in files.items():
        filepath = tmp_path / filename
        save_data(filepath, content)

    # Verify all files created
    assert len(list(tmp_path.iterdir())) == 3

    # Verify contents
    for filename, expected_content in files.items():
        filepath = tmp_path / filename
        assert load_data(filepath) == expected_content
```

### Pattern 9: Custom Fixtures and Conftest

```python
# conftest.py
"""Shared fixtures for all tests."""
import pytest

@pytest.fixture(scope="session")
def database_url():
    """Provide database URL for all tests."""
    return "postgresql://localhost/test_db"


@pytest.fixture(autouse=True)
def reset_database(database_url):
    """Auto-use fixture that runs before each test."""
    # Setup: Clear database
    print(f"Clearing database: {database_url}")
    yield
    # Teardown: Clean up
    print("Test completed")


@pytest.fixture
def sample_user():
    """Provide sample user data."""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_users():
    """Provide list of sample users."""
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        {"id": 3, "name": "User 3"},
    ]


# Parametrized fixture
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_backend(request):
    """Fixture that runs tests with different database backends."""
    return request.param


def test_with_db_backend(db_backend):
    """This test will run 3 times with different backends."""
    print(f"Testing with {db_backend}")
    assert db_backend in ["sqlite", "postgresql", "mysql"]
```

### Pattern 10: Property-Based Testing

```python
# test_properties.py
from hypothesis import given, strategies as st
import pytest

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]


@given(st.text())
def test_reverse_twice_is_original(s):
    """Property: reversing twice returns original."""
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_length(s):
    """Property: reversed string has same length."""
    assert len(reverse_string(s)) == len(s)


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """Property: addition is commutative."""
    assert a + b == b + a


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst):
    """Property: sorted list is ordered."""
    sorted_lst = sorted(lst)

    # Same length
    assert len(sorted_lst) == len(lst)

    # All elements present
    assert set(sorted_lst) == set(lst)

    # Is ordered
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## Testing Best Practices

### Test Organization

```python
# tests/
#   __init__.py
#   conftest.py           # Shared fixtures
#   test_unit/            # Unit tests
#     test_models.py
#     test_utils.py
#   test_integration/     # Integration tests
#     test_api.py
#     test_database.py
#   test_e2e/            # End-to-end tests
#     test_workflows.py
```

### Test Naming

```python
# Good test names
def test_user_creation_with_valid_data():
    """Clear name describes what is being tested."""
    pass


def test_login_fails_with_invalid_password():
    """Name describes expected behavior."""
    pass


def test_api_returns_404_for_missing_resource():
    """Specific about inputs and expected outcomes."""
    pass


# Bad test names
def test_1():  # Not descriptive
    pass


def test_user():  # Too vague
    pass


def test_function():  # Doesn't explain what's tested
    pass
```

### Test Markers

```python
# test_markers.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Mark slow tests."""
    import time
    time.sleep(2)


@pytest.mark.integration
def test_database_integration():
    """Mark integration tests."""
    pass


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """Skip tests temporarily."""
    pass


@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    """Conditional skip."""
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """Mark expected failures."""
    assert False


# Run with:
# pytest -m slow          # Run only slow tests
# pytest -m "not slow"    # Skip slow tests
# pytest -m integration   # Run integration tests
```

### Coverage Reporting

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=myapp tests/

# Generate HTML report
pytest --cov=myapp --cov-report=html tests/

# Fail if coverage below threshold
pytest --cov=myapp --cov-fail-under=80 tests/

# Show missing lines
pytest --cov=myapp --cov-report=term-missing tests/
```

## Testing FastAPI SSE Endpoints

```python
# test_sse_streaming.py
import pytest
import json
from fastapi.testclient import TestClient
from sse_starlette import EventSourceResponse

def test_agent_sse_streaming(client: TestClient):
    """Test SSE streaming for agent updates."""
    response = client.get("/api/agent/stream")
    
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    # Parse SSE events
    events = []
    for line in response.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            events.append(data)
    
    assert len(events) > 0
    assert events[0]["event"] == "update"


def test_sse_connection_error(client: TestClient):
    """Test SSE connection error handling."""
    with patch('python.main.agent_queue') as mock_queue:
        mock_queue.get.side_effect = ConnectionError("Agent not available")
        
        response = client.get("/api/agent/stream")
        
        # Should return error or close connection gracefully
        assert response.status_code in [500, 503]


@pytest.mark.asyncio
async def test_sse_event_format():
    """Test SSE event format validation."""
    from python.main import format_sse_event
    
    event = format_sse_event("update", {"status": "working", "progress": 50})
    
    assert "event: update" in event
    assert "data: " in event
    assert '"status": "working"' in event
```

## Testing Agent Communication via Unix Sockets

```python
# test_unix_socket_ipc.py
import pytest
import socket
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_socket_path(tmp_path: Path):
    """Create temporary Unix socket for testing."""
    socket_path = tmp_path / "test.sock"
    return str(socket_path)


def test_osxphotos_sandbox_extraction(mock_socket_path: str):
    """Test osxphotos sandbox extraction via Unix socket."""
    # Mock osxphotos server
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(mock_socket_path)
    server_socket.listen(1)
    
    # Test client
    client = OsxphotosSandboxClient(mock_socket_path)
    
    # Start server in thread
    def handle_request():
        conn, _ = server_socket.accept()
        request = json.loads(conn.recv(4096).decode())
        
        # Validate request
        assert request["method"] == "extract"
        assert request["params"]["album"] == "Test Album"
        
        # Send response
        response = {"status": "success", "photos": []}
        conn.sendall(json.dumps(response).encode())
        conn.close()
    
    import threading
    server_thread = threading.Thread(target=handle_request)
    server_thread.start()
    
    # Execute extraction
    result = client.extract_photos("Test Album", "/tmp/exports")
    
    assert result["status"] == "success"
    server_thread.join()


def test_osxphotos_path_validation():
    """Test osxphotos path whitelist validation."""
    client = OsxphotosSandboxClient("/tmp/test.sock")
    
    # Valid paths
    assert client._is_path_allowed("~/Exports/test.jpg")
    assert client._is_path_allowed("~/Documents/TraeExports/photo.jpg")
    
    # Invalid paths
    assert not client._is_path_allowed("~/Photos/export.jpg")
    assert not client._is_path_allowed("/etc/passwd")


@patch('subprocess.run')
def test_osxphotos_no_network_access(mock_run):
    """Test osxphotos sandbox has no network access."""
    mock_run.return_value = MagicMock(returncode=0)
    
    client = OsxphotosSandboxClient("/tmp/test.sock")
    client.extract_photos("Test", "~/Exports/")
    
    # Verify no network calls
    for call in mock_run.call_args_list:
        args = call[0][0]
        assert "curl" not in str(args)
        assert "wget" not in str(args)


def test_unix_socket_timeout():
    """Test Unix socket timeout handling."""
    client = OsxphotosSandboxClient("/nonexistent.sock")
    
    with pytest.raises((ConnectionRefusedError, TimeoutError)):
        client.extract_photos("Test", "~/Exports/")
```

## Testing Cagent YAML Generation

```python
# test_cagent_yaml.py
import pytest
from pydantic import ValidationError

def test_cagent_config_validation():
    """Test Cagent configuration validation."""
    config = {
        "agents": {
            "captioning_agent": {
                "provider": "anthropic",
                "model": "claude-3-haiku",
                "toolsets": [{"type": "mcp", "ref": "cloudinary"}]
            }
        }
    }
    
    # Validate with Pydantic
    try:
        validated = CagentConfig(**config)
        assert validated.agents["captioning_agent"].provider == "anthropic"
    except ValidationError as e:
        pytest.fail(f"Config validation failed: {e}")


def test_cagent_yaml_serialization():
    """Test Cagent config serialization to YAML."""
    config = CagentConfig(
        agents={
            "captioning_agent": AgentConfig(
                name="captioning_agent",
                provider="anthropic",
                model="claude-3-haiku"
            )
        }
    )
    
    yaml_str = config.to_yaml()
    assert "captioning_agent" in yaml_str
    assert "anthropic" in yaml_str


def test_cagent_toolset_validation():
    """Test Cagent toolset configuration validation."""
    toolset = {
        "type": "mcp",
        "ref": "cloudinary",
        "config": {"api_key": "test-key"}
    }
    
    validated = ToolsetConfig(**toolset)
    assert validated.type == "mcp"
    assert validated.ref == "cloudinary"
```

## E2E Testing for Complete Workflows

```python
# test_e2e_workflow.py
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.e2e
async def test_complete_media_workflow():
    """Test complete workflow: extract → edit → caption → schedule."""
    
    # Step 1: Extract photos
    with patch('electron.ipc-handlers.osxphotos.extract') as mock_extract:
        mock_extract.return_value = [
            {"filename": "photo1.jpg", "path": "/tmp/photo1.jpg"}
        ]
        
        extracted = await window.electronAPI.extractPhotos("Test Album")
        assert len(extracted) == 1
    
    # Step 2: Edit with Cloudinary
    with patch('python.tools.cloudinary.edit') as mock_edit:
        mock_edit.return_value = {
            "url": "https://res.cloudinary.com/edited.jpg",
            "public_id": "edited_photo"
        }
        
        edited = await edit_photo(extracted[0])
        assert edited["url"].startswith("https://")
    
    # Step 3: Generate caption
    with patch('python.agents.captioning.generate') as mock_caption:
        mock_caption.return_value = CaptionSchema(
            text="Beautiful sunset photo",
            hashtags=["#sunset", "#photography"]
        )
        
        caption = await generate_caption(edited)
        assert len(caption.text) > 0
    
    # Step 4: Schedule post
    with patch('python.tools.postiz.schedule') as mock_schedule:
        mock_schedule.return_value = {"post_id": "12345"}
        
        scheduled = await schedule_post({
            "media_id": edited["public_id"],
            "caption": caption.text,
            "platforms": ["instagram"]
        })
        
        assert scheduled["post_id"] == "12345"


@pytest.mark.e2e
async def test_workflow_with_failure_recovery():
    """Test workflow with agent failure and recovery."""
    
    # Step 1: Extract succeeds
    with patch('electron.ipc-handlers.osxphotos.extract') as mock_extract:
        mock_extract.return_value = [{"filename": "photo1.jpg"}]
        extracted = await window.electronAPI.extractPhotos("Test Album")
    
    # Step 2: Captioning fails, then succeeds with fallback
    with patch('python.agents.captioning.generate') as mock_caption:
        mock_caption.side_effect = [
            Exception("Primary LLM failed"),
            CaptionSchema(text="Fallback caption", hashtags=[])
        ]
        
        # First attempt fails
        with pytest.raises(Exception):
            caption = await generate_caption(extracted[0])
        
        # Second attempt succeeds
        caption = await generate_caption(extracted[0])
        assert caption.text == "Fallback caption"


@pytest.mark.e2e
async def test_workflow_parallel_processing():
    """Test workflow with parallel agent processing."""
    
    photos = [{"filename": f"photo{i}.jpg"} for i in range(5)]
    
    # Process all photos in parallel
    with patch('python.agents.captioning.generate') as mock_caption:
        mock_caption.return_value = CaptionSchema(
            text="Caption",
            hashtags=[]
        )
        
        captions = await asyncio.gather(*[
            generate_caption(photo) for photo in photos
        ])
        
        assert len(captions) == 5
        assert all(c.text == "Caption" for c in captions)
```

## Property-Based Testing for Agent Logic

```python
# test_agent_property.py
from hypothesis import given, strategies as st
from pydantic import BaseModel, Field

class AgentDecision(BaseModel):
    action: str
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


@given(st.text(min_size=10, max_size=100), st.floats(min_value=0.0, max_value=1.0))
def test_agent_decision_properties(action: str, confidence: float):
    """Test agent decision properties."""
    decision = AgentDecision(
        action=action,
        confidence=confidence,
        reasoning="Test reasoning"
    )
    
    # Property: confidence is always valid
    assert 0.0 <= decision.confidence <= 1.0
    
    # Property: action is never empty
    assert len(decision.action) > 0


@given(st.lists(st.text()))
def test_rag_retrieval_properties(queries: list[str]):
    """Test RAG retrieval properties."""
    # Property: retrieval returns same number of results as queries
    results = [retrieve_from_rag(q) for q in queries]
    assert len(results) == len(queries)
    
    # Property: all results have scores
    for result in results:
        assert "score" in result
        assert 0.0 <= result["score"] <= 1.0


@given(st.lists(st.text(min_size=1), min_size=1, max_size=10))
def test_hashtag_generation_properties(captions: list[str]):
    """Test hashtag generation properties."""
    for caption in captions:
        hashtags = generate_hashtags(caption)
        
        # Property: hashtags start with #
        assert all(tag.startswith("#") for tag in hashtags)
        
        # Property: hashtags are lowercase
        assert all(tag.islower() or tag[1:].islower() for tag in hashtags)
        
        # Property: no duplicate hashtags
        assert len(hashtags) == len(set(hashtags))


@given(st.text(min_size=10, max_size=2200))
def test_caption_length_properties(caption: str):
    """Test caption length validation."""
    # Property: caption length is within limits
    assert 10 <= len(caption) <= 2200
    
    # Property: caption doesn't contain null bytes
    assert "\x00" not in caption
```

## Testing Database Code

```python
# test_database_models.py
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """Create in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


def test_create_user(db_session):
    """Test creating a user."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == "Test User"


def test_query_user(db_session):
    """Test querying users."""
    user1 = User(name="User 1", email="user1@example.com")
    user2 = User(name="User 2", email="user2@example.com")

    db_session.add_all([user1, user2])
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 2


def test_unique_email_constraint(db_session):
    """Test unique email constraint."""
    from sqlalchemy.exc import IntegrityError

    user1 = User(name="User 1", email="same@example.com")
    user2 = User(name="User 2", email="same@example.com")

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Configuration Files

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
    e2e: marks end-to-end tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--cov=myapp",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## Resources

- **pytest documentation**: https://docs.pytest.org/
- **unittest.mock**: https://docs.python.org/3/library/unittest.mock.html
- **hypothesis**: Property-based testing
- **pytest-asyncio**: Testing async code
- **pytest-cov**: Coverage reporting
- **pytest-mock**: pytest wrapper for mock

## Best Practices Summary

1. **Write tests first** (TDD) or alongside code
2. **One assertion per test** when possible
3. **Use descriptive test names** that explain behavior
4. **Keep tests independent** and isolated
5. **Use fixtures** for setup and teardown
6. **Mock external dependencies** appropriately
7. **Parametrize tests** to reduce duplication
8. **Test edge cases** and error conditions
9. **Measure coverage** but focus on quality
10. **Run tests in CI/CD** on every commit
