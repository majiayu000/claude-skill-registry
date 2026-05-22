---
name: testing-ai-agents
description: Use when testing AI agent code with pytest. Covers TDD for agent APIs, mocking LLM calls (NOT evaluating LLM outputs), pytest-asyncio patterns, FastAPI testing with httpx, SQLModel testing, and agent tool testing. NOT for evaluating LLM reasoning quality (use evals skill).
---

# Testing AI Agents: TDD for Agent Code

Test-Driven Development for agent applications. This skill covers testing **code correctness** (deterministic, passes/fails), NOT measuring **LLM reasoning quality** (probabilistic, scores - use evals for that).

## Critical Distinction: TDD vs Evals

| Aspect | TDD (This Skill) | Evals (Chapter 47) |
|--------|------------------|-------------------|
| Question | Does the code work correctly? | Does the LLM reason well? |
| Nature | Deterministic | Probabilistic |
| Output | Pass/Fail | Scores (0-1) |
| Tests | Functions, APIs, DB operations | Response quality, faithfulness |
| Speed | Fast (mocked LLM) | Slow (real LLM calls) |
| Cost | Zero (no API calls) | High (API calls required) |

## Quick Start: Project Setup

```bash
# Install testing dependencies
uv add --dev pytest pytest-asyncio httpx respx pytest-cov

# Configure pytest
cat > pyproject.toml << 'EOF'
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
EOF
```

## Core Testing Patterns

### Pattern 1: Async Test Setup

```python
# tests/conftest.py
import os
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

# Set environment FIRST
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("OPENAI_API_KEY", "test-key-not-used")

from app.main import app
from app.database import get_session
from app.auth import get_current_user

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)

TestAsyncSession = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Mock user
TEST_USER = {"sub": "test-user-123", "email": "test@example.com"}

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session-scoped fixtures."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
async def setup_database():
    """Create tables before each test, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

async def get_test_session():
    async with TestAsyncSession() as session:
        yield session

def get_test_user():
    return TEST_USER

@pytest.fixture
async def client():
    """Async test client with mocked dependencies."""
    app.dependency_overrides[get_session] = get_test_session
    app.dependency_overrides[get_current_user] = get_test_user

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
```

### Pattern 2: Testing FastAPI Endpoints

```python
# tests/test_tasks.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    """Test creating a task via API."""
    response = await client.post(
        "/api/tasks",
        json={"title": "Test Task", "priority": "high"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_get_task_not_found(client: AsyncClient):
    """Test 404 for non-existent task."""
    response = await client.get("/api/tasks/99999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_list_tasks_with_filter(client: AsyncClient):
    """Test filtering tasks by status."""
    # Create test data
    await client.post("/api/tasks", json={"title": "Task 1"})
    await client.post("/api/tasks", json={"title": "Task 2"})

    # Filter by status
    response = await client.get("/api/tasks", params={"status": "pending"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
```

### Pattern 3: Testing SQLModel Operations

```python
# tests/test_models.py
import pytest
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Task, Project

@pytest.fixture
async def session():
    """Direct database session for model testing."""
    async with TestAsyncSession() as session:
        yield session

@pytest.mark.asyncio
async def test_create_task(session: AsyncSession):
    """Test Task model creation."""
    task = Task(title="Test", priority="high")
    session.add(task)
    await session.commit()
    await session.refresh(task)

    assert task.id is not None
    assert task.created_at is not None

@pytest.mark.asyncio
async def test_cascade_delete(session: AsyncSession):
    """Test parent-child cascade deletion."""
    project = Project(name="Test Project")
    session.add(project)
    await session.commit()

    task = Task(title="Test", project_id=project.id)
    session.add(task)
    await session.commit()

    # Delete parent
    await session.delete(project)
    await session.commit()

    # Verify child deleted
    result = await session.get(Task, task.id)
    assert result is None
```

### Pattern 4: Mocking LLM Calls with respx

```python
# tests/test_agent_tools.py
import pytest
import respx
import httpx
from app.agent import call_openai

@pytest.mark.asyncio
@respx.mock
async def test_openai_completion():
    """Mock OpenAI API response."""
    # Mock the API endpoint
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "Hello, I can help with that!"
                    }
                }],
                "usage": {"total_tokens": 50}
            }
        )
    )

    # Call your function
    result = await call_openai("Say hello")

    assert "Hello" in result
    assert respx.calls.call_count == 1

@pytest.mark.asyncio
@respx.mock
async def test_openai_rate_limit():
    """Test rate limit handling."""
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(429, json={"error": "Rate limited"})
    )

    with pytest.raises(RateLimitError):
        await call_openai("Test")

@pytest.mark.asyncio
@respx.mock
async def test_tool_call_parsing():
    """Test agent parses tool calls correctly."""
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "tool_calls": [{
                            "id": "call_123",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"city": "London"}'
                            }
                        }]
                    }
                }]
            }
        )
    )

    result = await agent.process("What's the weather in London?")

    assert result.tool_calls[0].function.name == "get_weather"
    assert result.tool_calls[0].function.arguments["city"] == "London"
```

### Pattern 5: Using pytest-mockllm

```python
# tests/test_with_mockllm.py
import pytest

def test_anthropic_mock(mock_anthropic):
    """Test with pytest-mockllm for Anthropic."""
    mock_anthropic.add_response("I can help with that task!")

    from anthropic import Anthropic
    client = Anthropic(api_key="fake")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )

    assert "help" in response.content[0].text

def test_openai_mock(mock_openai):
    """Test with pytest-mockllm for OpenAI."""
    mock_openai.add_response("Task completed successfully.")

    from openai import OpenAI
    client = OpenAI(api_key="fake")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Complete this task"}]
    )

    assert "completed" in response.choices[0].message.content
```

### Pattern 6: Testing Agent Tools in Isolation

```python
# tests/test_tools.py
import pytest
from app.tools import search_database, format_response, validate_input

@pytest.mark.asyncio
async def test_search_tool():
    """Test database search tool function."""
    # This tests the tool logic, NOT the LLM
    results = await search_database(query="python")

    assert isinstance(results, list)
    assert all("python" in r["title"].lower() for r in results)

def test_format_response():
    """Test response formatting utility."""
    raw = {"items": [1, 2, 3], "count": 3}
    formatted = format_response(raw)

    assert "3 items found" in formatted

def test_validate_input_rejects_injection():
    """Test input validation blocks SQL injection."""
    malicious = "'; DROP TABLE users; --"

    with pytest.raises(ValidationError):
        validate_input(malicious)
```

### Pattern 7: Integration Tests with Mocked LLM

```python
# tests/integration/test_agent_pipeline.py
import pytest
import respx
import httpx

@pytest.mark.asyncio
@respx.mock
async def test_complete_agent_flow(client: AsyncClient):
    """Test full agent pipeline with mocked LLM."""
    # Mock LLM to return a tool call
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        side_effect=[
            # First call: LLM decides to use tool
            httpx.Response(200, json={
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "tool_calls": [{
                            "id": "call_1",
                            "function": {
                                "name": "create_task",
                                "arguments": '{"title": "New Task"}'
                            }
                        }]
                    }
                }]
            }),
            # Second call: LLM responds with result
            httpx.Response(200, json={
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "I created the task 'New Task' for you."
                    }
                }]
            })
        ]
    )

    # Call agent endpoint
    response = await client.post(
        "/api/agent/chat",
        json={"message": "Create a task called 'New Task'"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "created" in data["response"].lower()

    # Verify task was actually created in DB
    tasks = await client.get("/api/tasks")
    assert any(t["title"] == "New Task" for t in tasks.json())
```

### Pattern 8: Testing Error Handling

```python
# tests/test_error_handling.py
import pytest
import respx
import httpx

@pytest.mark.asyncio
@respx.mock
async def test_llm_timeout_handling():
    """Test graceful handling of LLM timeout."""
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        side_effect=httpx.TimeoutException("Connection timed out")
    )

    with pytest.raises(AgentTimeoutError) as exc_info:
        await agent.process("Test query")

    assert "LLM request timed out" in str(exc_info.value)

@pytest.mark.asyncio
@respx.mock
async def test_malformed_response_handling():
    """Test handling of malformed LLM response."""
    respx.post("https://api.openai.com/v1/chat/completions").mock(
        return_value=httpx.Response(200, json={"invalid": "response"})
    )

    with pytest.raises(AgentResponseError):
        await agent.process("Test query")

@pytest.mark.asyncio
async def test_database_error_handling(client: AsyncClient):
    """Test API handles database errors gracefully."""
    # Force a constraint violation
    await client.post("/api/tasks", json={"title": "Task 1"})
    response = await client.post("/api/tasks", json={"title": "Task 1"})  # Duplicate

    assert response.status_code == 400
    assert "already exists" in response.json()["error"]
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_models.py       # SQLModel tests
│   ├── test_tools.py        # Agent tool tests
│   └── test_utils.py        # Utility function tests
├── integration/
│   ├── test_api.py          # FastAPI endpoint tests
│   └── test_agent.py        # Agent pipeline tests (mocked LLM)
└── e2e/
    └── test_flows.py        # End-to-end flows (still mocked LLM)
```

## Fixtures Reference

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `event_loop` | session | Shared async event loop |
| `setup_database` | function | Fresh DB per test |
| `session` | function | Direct DB access |
| `client` | function | Async HTTP client |
| `mock_user` | function | Test authentication |

## Best Practices

### DO
- Mock LLM calls at HTTP level (respx, httpx.MockTransport)
- Use in-memory SQLite for fast DB tests
- Test tool logic separately from LLM orchestration
- Override FastAPI dependencies for auth/DB
- Use factories for test data creation

### DON'T
- Make real LLM API calls in unit tests
- Share state between tests
- Test LLM reasoning quality (that's evals)
- Skip error path testing
- Use production databases

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_tasks.py

# Run tests matching pattern
pytest -k "test_create"

# Run async tests only
pytest -m asyncio

# Verbose output
pytest -v
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5
      - run: uv sync --all-extras
      - run: uv run pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v4
```

## References

For detailed patterns, see:
- [Pytest-Asyncio Patterns](references/pytest-asyncio.md)
- [RESPX Mocking Guide](references/respx-mocking.md)
- [FastAPI Testing Patterns](references/fastapi-testing.md)
