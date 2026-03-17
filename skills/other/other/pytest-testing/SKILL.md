---
name: pytest-testing
description: Async testing with pytest, pytest-asyncio, httpx, fixtures, coverage reports, and test-first development. Use when writing tests, test fixtures, or measuring coverage.
---

# Pytest Async Testing

## Configuration (pytest.ini)
```ini
[pytest]
asyncio_mode = auto
testpaths = tests
addopts = --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=80
```

## Fixtures (conftest.py)
```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from httpx import AsyncClient

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        yield session
    await engine.dispose()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def auth_token():
    return generate_test_token("test_user")
```

## Async Tests
```python
@pytest.mark.asyncio
async def test_endpoint(client, auth_token):
    response = await client.post(
        "/api/user123/chat",
        json={"message": "Add task"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
```

## Coverage
```bash
pytest --cov=. --cov-report=html  # Generate HTML report
pytest --cov=. --cov-report=term-missing  # Show missing lines
pytest --cov-fail-under=80  # Fail if below 80%
```

## Test-First Pattern
1. Write test defining expected behavior
2. Run test (should fail)
3. Implement code to pass test
4. Refactor while keeping tests green