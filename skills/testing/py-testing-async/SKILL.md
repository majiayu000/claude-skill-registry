---
name: py-testing-async
description: Async testing patterns with pytest-asyncio. Use when writing tests, mocking async code, testing database operations, or debugging test failures.
---

# Python Async Testing

## Problem Statement

Async testing requires specific patterns. pytest-asyncio has modes that affect behavior. Database tests need isolation. Mocking async functions differs from sync. Get these wrong and tests are flaky or don't catch bugs.

---

## Pattern: pytest-asyncio Configuration

**Problem:** Pytest needs configuration for async tests.

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "strict"  # Requires explicit @pytest.mark.asyncio
# OR
asyncio_mode = "auto"    # All async tests run automatically
```

```python
import pytest

# With asyncio_mode = "strict" (this codebase)
@pytest.mark.asyncio
async def test_something():
    result = await some_async_function()
    assert result == expected

# Without the marker = test won't run as async!
```

---

## Pattern: Async Fixtures

**Problem:** Fixtures that provide async resources need specific handling.

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

# ✅ CORRECT: Async fixture for session
@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        await session.rollback()  # Clean up after test

# ✅ CORRECT: Async fixture for test data
@pytest.fixture
async def test_user(session: AsyncSession) -> User:
    user = User(email="test@example.com", hashed_password="...")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

# ✅ CORRECT: Using async fixtures
@pytest.mark.asyncio
async def test_get_user(session: AsyncSession, test_user: User):
    result = await session.execute(
        select(User).where(User.id == test_user.id)
    )
    user = result.scalar_one()
    assert user.email == "test@example.com"
```

---

## Pattern: Database Test Isolation

**Problem:** Tests polluting each other's database state.

```python
# ✅ CORRECT: Transaction rollback per test
@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        # Start a transaction
        async with session.begin():
            yield session
            # Rollback happens automatically when we exit

# ✅ CORRECT: Nested transactions for complex tests
@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        await session.begin()
        yield session
        await session.rollback()

# Alternative: Use separate test database
# conftest.py
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    # Use SQLite for tests, PostgreSQL for prod
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield engine
    await engine.dispose()
```

---

## Pattern: Mocking Async Functions

**Problem:** Regular `Mock` doesn't work with async functions.

```python
from unittest.mock import AsyncMock, patch

# ✅ CORRECT: AsyncMock for async functions
@pytest.mark.asyncio
async def test_with_mocked_service():
    mock_service = AsyncMock()
    mock_service.get_user.return_value = User(id=uuid4(), email="test@example.com")
    
    result = await mock_service.get_user(user_id)
    
    assert result.email == "test@example.com"
    mock_service.get_user.assert_called_once_with(user_id)

# ✅ CORRECT: Patching async functions
@pytest.mark.asyncio
@patch("app.services.user_service.send_email", new_callable=AsyncMock)
async def test_user_creation_sends_email(mock_send_email: AsyncMock, session: AsyncSession):
    mock_send_email.return_value = True
    
    user = await create_user(email="new@example.com", session=session)
    
    mock_send_email.assert_called_once_with(user.email, "Welcome!")

# ✅ CORRECT: AsyncMock with side_effect
mock_service = AsyncMock()
mock_service.get_user.side_effect = [
    User(id=uuid4(), email="first@example.com"),
    User(id=uuid4(), email="second@example.com"),
]

# First call returns first user, second call returns second user
```

---

## Pattern: HTTP Client Testing

**Problem:** Testing FastAPI endpoints with async client.

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    response = await client.get("/api/users")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_create_assessment(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/assessments",
        json={"title": "Test Assessment", "skill_areas": ["fundamentals"]},
        headers=auth_headers,
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Assessment"

# ✅ CORRECT: Auth fixture
@pytest.fixture
async def auth_headers(test_user: User) -> dict:
    token = create_access_token(user_id=test_user.id)
    return {"Authorization": f"Bearer {token}"}
```

---

## Pattern: Testing Service Functions

```python
@pytest.mark.asyncio
async def test_calculate_rating(session: AsyncSession, test_user: User):
    # Arrange: Create test data
    assessment = Assessment(user_id=test_user.id, title="Test")
    session.add(assessment)
    await session.commit()
    
    answers = [
        UserAnswer(user_id=test_user.id, question_id=q_id, value=4)
        for q_id in question_ids
    ]
    session.add_all(answers)
    await session.commit()
    
    # Act: Call the service
    result = await calculate_rating(assessment.id, session)
    
    # Assert: Check the result
    assert result.rating >= 1.0
    assert result.rating <= 5.5
    assert result.confidence > 0

@pytest.mark.asyncio
async def test_calculate_rating_no_answers(session: AsyncSession, test_user: User):
    assessment = Assessment(user_id=test_user.id, title="Empty")
    session.add(assessment)
    await session.commit()
    
    # Should raise or return specific result
    with pytest.raises(ValueError, match="No answers found"):
        await calculate_rating(assessment.id, session)
```

---

## Pattern: Testing Multi-Step Flows

Same principle as frontend - test entire flows, not just units:

```python
@pytest.mark.asyncio
async def test_complete_assessment_flow(session: AsyncSession, test_user: User):
    """Test full assessment flow: create -> answer -> submit -> results."""
    
    # Step 1: Create assessment
    assessment = await create_assessment(
        user_id=test_user.id,
        data=AssessmentCreate(title="Full Flow Test", skill_areas=["fundamentals"]),
        session=session,
    )
    assert assessment.id is not None
    
    # Step 2: Answer questions
    questions = await get_assessment_questions(assessment.id, session)
    for question in questions:
        await submit_answer(
            user_id=test_user.id,
            question_id=question.id,
            value=4,
            session=session,
        )
    
    # Step 3: Submit assessment
    result = await submit_assessment(assessment.id, session)
    assert result.status == "completed"
    
    # Step 4: Verify results
    rating = await get_assessment_rating(assessment.id, session)
    assert rating is not None
    assert rating.skill_area == "fundamentals"
```

---

## Pattern: Fixture Scopes

**Problem:** Understanding when fixtures are recreated.

```python
# function (default) - recreated for each test
@pytest.fixture
async def session():
    ...  # New session per test

# class - shared within test class
@pytest.fixture(scope="class")
async def shared_data():
    ...  # Created once per test class

# module - shared within test file
@pytest.fixture(scope="module")
async def module_setup():
    ...  # Created once per file

# session - shared across entire test run
@pytest.fixture(scope="session")
async def database():
    ...  # Created once, used by all tests
```

**Best practices:**
- Database sessions: `function` scope (isolation)
- Test data: `function` scope (clean state)
- Database engine: `session` scope (expensive to create)

---

## Pattern: Testing Error Cases

```python
@pytest.mark.asyncio
async def test_get_nonexistent_user(session: AsyncSession):
    fake_id = uuid4()
    
    with pytest.raises(HTTPException) as exc_info:
        await get_user_or_404(fake_id, session)
    
    assert exc_info.value.status_code == 404
    assert str(fake_id) in exc_info.value.detail

@pytest.mark.asyncio
async def test_duplicate_email_rejected(session: AsyncSession, test_user: User):
    with pytest.raises(IntegrityError):
        duplicate = User(email=test_user.email, hashed_password="...")
        session.add(duplicate)
        await session.commit()
```

---

## Pattern: Parameterized Tests

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("skill_area,expected_min,expected_max", [
    ("fundamentals", 1.0, 5.5),
    ("advanced", 1.0, 5.5),
    ("strategy", 1.0, 5.5),
])
async def test_rating_ranges(
    skill_area: str,
    expected_min: float,
    expected_max: float,
    session: AsyncSession,
):
    rating = await calculate_rating_for_area(skill_area, session)
    assert expected_min <= rating <= expected_max

@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_input", [
    {"title": ""},  # Empty title
    {"title": "x" * 201},  # Too long
    {"skill_areas": []},  # Empty areas
])
async def test_assessment_validation(invalid_input: dict, client: AsyncClient):
    response = await client.post("/api/assessments", json=invalid_input)
    assert response.status_code == 422
```

---

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "coroutine was never awaited" | Missing `await` in test | Add `await` |
| Test not running async | Missing `@pytest.mark.asyncio` | Add marker or use `asyncio_mode = "auto"` |
| Tests polluting each other | Missing rollback | Use transaction fixture with rollback |
| "Event loop is closed" | Fixture scope mismatch | Check `scope` on async fixtures |
| Mock not working | Using `Mock` instead of `AsyncMock` | Use `AsyncMock` for async |

---

## Test Commands

```bash
# Run all tests
uv run pytest

# Verbose output
uv run pytest -v

# Specific file
uv run pytest tests/test_assessments.py

# Specific test
uv run pytest tests/test_assessments.py::test_create_assessment

# With coverage
uv run pytest --cov=app --cov-report=html

# Stop on first failure
uv run pytest -x

# Show print output
uv run pytest -s
```
