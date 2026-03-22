---
name: pytest-patterns
description: pytest best practices for writing comprehensive test suites. Use when writing or running Python tests, setting up test fixtures, mocking, or achieving good test coverage.
---

# pytest Patterns

## Structure
```
tests/
  conftest.py        # Shared fixtures
  unit/              # Pure unit tests (no I/O)
  integration/       # DB, Redis, API tests
  e2e/               # Full flow tests
  test_models.py     # Test naming: test_<module>.py
```

## conftest.py (Fixtures)
```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost/test_db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db(engine):
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db):
    app.dependency_overrides[get_db] = lambda: db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
async def user(db):
    u = User(email="test@example.com", name="Test")
    db.add(u)
    await db.flush()
    return u
```

## Test Patterns
```python
# Parametrize for edge cases
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid", False),
    ("", False),
    ("a" * 300 + "@x.com", False),
])
async def test_email_validation(email, valid):
    ...

# Mock external services
from unittest.mock import AsyncMock, patch

async def test_sends_email(client, user):
    with patch("app.services.email.send") as mock_send:
        mock_send.return_value = None
        resp = await client.post("/users/verify", json={"email": user.email})
        assert resp.status_code == 200
        mock_send.assert_called_once_with(user.email, subject="Verify your account")

# Test error cases
async def test_get_user_not_found(client):
    resp = await client.get("/users/99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
```

## Running Tests
```bash
# Full suite with coverage
pytest tests/ -v --tb=short --cov=app --cov-report=term-missing

# Fast: only unit tests
pytest tests/unit/ -v

# Specific test
pytest tests/test_auth.py::test_login_success -v

# Stop on first failure
pytest -x
```

## Rules
- Every fixture that creates DB data must rollback after test
- Mock ALL external APIs (email, Stripe, S3) — never call real ones in tests
- Test both success AND failure paths for every endpoint
- Use parametrize for boundary conditions
- Keep unit tests pure (no I/O, no DB) — they must run in < 1ms each
- Coverage goal: 80%+ for services, 60%+ overall
- Test names must describe WHAT they test: test_login_with_wrong_password_returns_401
