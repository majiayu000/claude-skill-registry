---
name: test-writer
description: Test generation expertise for Python (pytest) and TypeScript (Jest). Use when writing new tests, improving coverage, or creating test fixtures. Ensures comprehensive coverage including edge cases, error scenarios, and integration tests.
model_tier: opus
parallel_hints:
  can_parallel_with: [code-review, lint-monorepo, security-audit]
  must_serialize_with: [database-migration]
  preferred_batch_size: 3
---

# Test Writer Skill

Expert test generation skill for creating comprehensive test suites that meet project coverage requirements.

## When This Skill Activates

- New code added without tests
- Coverage below 70% threshold
- Complex logic needs test coverage
- Bug fix requires regression test
- Refactoring needs safety net
- Integration tests needed

## Testing Standards

### Coverage Requirements

| Layer | Target | Minimum |
|-------|--------|---------|
| Services | 90% | 80% |
| Controllers | 85% | 75% |
| Models | 80% | 70% |
| Utils | 90% | 85% |
| Routes | 75% | 65% |

### Test Pyramid

```
         /\
        /  \    E2E Tests (few)
       /----\
      /      \  Integration Tests (some)
     /--------\
    /          \ Unit Tests (many)
   /------------\
```

## Python Testing (pytest)

### Test File Structure

```python
"""Tests for swap executor service."""
import pytest
from datetime import date, timedelta
from unittest.mock import AsyncMock, patch

from app.services.swap_executor import SwapExecutor
from app.models.swap import SwapRequest, SwapType
from app.schemas.swap import SwapCreate


class TestSwapExecutor:
    """Test suite for SwapExecutor service."""

    # ===== Fixtures =====

    @pytest.fixture
    def executor(self):
        """Create SwapExecutor instance."""
        return SwapExecutor()

    @pytest.fixture
    def valid_swap_request(self, db_session):
        """Create a valid swap request."""
        return SwapRequest(
            id="swap-123",
            requestor_id="person-1",
            target_id="person-2",
            swap_type=SwapType.ONE_TO_ONE,
            status="pending"
        )

    # ===== Happy Path Tests =====

    async def test_execute_one_to_one_swap_success(
        self, executor, db_session, valid_swap_request
    ):
        """Test successful execution of one-to-one swap."""
        # Arrange
        # (setup is done in fixtures)

        # Act
        result = await executor.execute_swap(db_session, valid_swap_request)

        # Assert
        assert result.status == "completed"
        assert result.executed_at is not None
        assert result.error is None

    # ===== Edge Cases =====

    async def test_execute_swap_with_past_date(
        self, executor, db_session, valid_swap_request
    ):
        """Test swap execution for past date is rejected."""
        # Arrange
        valid_swap_request.target_date = date.today() - timedelta(days=1)

        # Act & Assert
        with pytest.raises(ValueError, match="Cannot swap past dates"):
            await executor.execute_swap(db_session, valid_swap_request)

    async def test_execute_swap_with_empty_request(self, executor, db_session):
        """Test swap execution with None request."""
        # Act & Assert
        with pytest.raises(TypeError):
            await executor.execute_swap(db_session, None)

    # ===== Error Cases =====

    async def test_execute_swap_database_error(
        self, executor, valid_swap_request
    ):
        """Test handling of database connection error."""
        # Arrange
        mock_db = AsyncMock()
        mock_db.commit.side_effect = ConnectionError("DB unavailable")

        # Act & Assert
        with pytest.raises(ConnectionError):
            await executor.execute_swap(mock_db, valid_swap_request)

    async def test_execute_swap_validation_failure(
        self, executor, db_session, invalid_swap_request
    ):
        """Test swap fails validation."""
        # Act & Assert
        with pytest.raises(ValueError, match="ACGME violation"):
            await executor.execute_swap(db_session, invalid_swap_request)

    # ===== Integration Tests =====

    @pytest.mark.integration
    async def test_execute_swap_persists_to_database(
        self, executor, db_session, valid_swap_request
    ):
        """Test that swap execution persists changes."""
        # Act
        result = await executor.execute_swap(db_session, valid_swap_request)
        await db_session.commit()

        # Assert - verify in database
        saved = await db_session.get(SwapRequest, result.id)
        assert saved.status == "completed"
```

### Test Categories

#### 1. Unit Tests

```python
"""Unit tests - test single function/method in isolation."""

def test_calculate_weekly_hours():
    """Test hour calculation logic."""
    assignments = [
        Assignment(hours=8),
        Assignment(hours=8),
        Assignment(hours=4),
    ]
    result = calculate_weekly_hours(assignments)
    assert result == 20

def test_calculate_weekly_hours_empty():
    """Test with empty input."""
    assert calculate_weekly_hours([]) == 0

def test_calculate_weekly_hours_negative():
    """Test negative hours are handled."""
    with pytest.raises(ValueError):
        calculate_weekly_hours([Assignment(hours=-1)])
```

#### 2. Service Tests

```python
"""Service layer tests - test business logic."""

class TestScheduleService:

    async def test_create_schedule_validates_acgme(self, db, service):
        """Test ACGME validation during schedule creation."""
        data = ScheduleCreate(...)

        result = await service.create_schedule(db, data)

        assert result.acgme_compliant is True

    async def test_create_schedule_rejects_violation(self, db, service):
        """Test schedule creation rejects ACGME violation."""
        data = ScheduleCreate(weekly_hours=90)  # Over 80 limit

        with pytest.raises(ACGMEViolationError):
            await service.create_schedule(db, data)
```

#### 3. API Tests

```python
"""API route tests - test HTTP endpoints."""
from fastapi.testclient import TestClient

class TestScheduleAPI:

    def test_get_schedule_returns_200(self, client: TestClient, auth_headers):
        """Test successful schedule retrieval."""
        response = client.get("/api/schedules/123", headers=auth_headers)

        assert response.status_code == 200
        assert "id" in response.json()

    def test_get_schedule_unauthorized(self, client: TestClient):
        """Test schedule access without auth."""
        response = client.get("/api/schedules/123")

        assert response.status_code == 401

    def test_create_schedule_returns_201(self, client, auth_headers):
        """Test schedule creation."""
        response = client.post(
            "/api/schedules",
            json={"name": "Test Schedule"},
            headers=auth_headers
        )

        assert response.status_code == 201
```

### Pytest Fixtures

```python
# conftest.py

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.db.base import Base
from app.models import *  # Import all models

@pytest.fixture(scope="function")
async def db_session():
    """Create test database session."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()

@pytest.fixture
def client(db_session):
    """Create test client with overridden dependencies."""
    from app.main import app
    from app.api.deps import get_db

    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(test_user):
    """Create authentication headers."""
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}
```

### Mocking Patterns

```python
from unittest.mock import AsyncMock, patch, MagicMock

# Mock async function
@patch("app.services.email.send_email", new_callable=AsyncMock)
async def test_notification_sends_email(mock_send):
    mock_send.return_value = True
    await notify_user("user-123", "Test message")
    mock_send.assert_called_once()

# Mock database query
async def test_with_mocked_db():
    mock_db = AsyncMock()
    mock_db.execute.return_value.scalar_one_or_none.return_value = User(id="123")

    result = await get_user(mock_db, "123")
    assert result.id == "123"

# Mock external API
@patch("httpx.AsyncClient.get")
async def test_external_api(mock_get):
    mock_get.return_value = MagicMock(
        status_code=200,
        json=lambda: {"data": "value"}
    )
    result = await fetch_external_data()
    assert result == {"data": "value"}
```

## TypeScript Testing (Jest)

### Test File Structure

```typescript
// __tests__/components/ScheduleView.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ScheduleView } from '@/components/ScheduleView';

describe('ScheduleView', () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );

  beforeEach(() => {
    queryClient.clear();
  });

  // ===== Rendering Tests =====

  it('renders loading state initially', () => {
    render(<ScheduleView scheduleId="123" />, { wrapper });

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('renders schedule data when loaded', async () => {
    render(<ScheduleView scheduleId="123" />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Schedule 123')).toBeInTheDocument();
    });
  });

  it('renders error state on failure', async () => {
    // Mock API failure
    server.use(
      rest.get('/api/schedules/123', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<ScheduleView scheduleId="123" />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  // ===== Interaction Tests =====

  it('calls onUpdate when edit button clicked', async () => {
    const onUpdate = jest.fn();
    render(<ScheduleView scheduleId="123" onUpdate={onUpdate} />, { wrapper });

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /edit/i })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /edit/i }));

    expect(onUpdate).toHaveBeenCalledTimes(1);
  });

  // ===== Accessibility Tests =====

  it('has no accessibility violations', async () => {
    const { container } = render(<ScheduleView scheduleId="123" />, { wrapper });

    await waitFor(() => {
      expect(screen.getByText('Schedule 123')).toBeInTheDocument();
    });

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

### Hook Testing

```typescript
// __tests__/hooks/useSchedule.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { useSchedule } from '@/hooks/useSchedule';

describe('useSchedule', () => {
  it('fetches schedule data', async () => {
    const { result } = renderHook(() => useSchedule('123'), { wrapper });

    await waitFor(() => {
      expect(result.current.isSuccess).toBe(true);
    });

    expect(result.current.data?.id).toBe('123');
  });

  it('handles error state', async () => {
    server.use(
      rest.get('/api/schedules/invalid', (req, res, ctx) => {
        return res(ctx.status(404));
      })
    );

    const { result } = renderHook(() => useSchedule('invalid'), { wrapper });

    await waitFor(() => {
      expect(result.current.isError).toBe(true);
    });
  });
});
```

## Test Generation Checklist

### For Every New Function

- [ ] Happy path test (normal input → expected output)
- [ ] Edge case tests (empty, null, boundary values)
- [ ] Error handling tests (invalid input, exceptions)
- [ ] Type validation tests (if applicable)

### For Every New Class

- [ ] Constructor tests
- [ ] Method tests (each public method)
- [ ] State transition tests
- [ ] Integration with dependencies

### For Every New API Endpoint

- [ ] Success response (200/201)
- [ ] Validation error (400)
- [ ] Auth required (401)
- [ ] Permission denied (403)
- [ ] Not found (404)
- [ ] Rate limiting (429)

### For Every Bug Fix

- [ ] Regression test that fails before fix
- [ ] Verify test passes after fix
- [ ] Add to edge case coverage

## Running Tests

```bash
# Python (pytest)
cd /home/user/Autonomous-Assignment-Program-Manager/backend

pytest                              # All tests
pytest -v                           # Verbose output
pytest --tb=short                   # Short traceback
pytest -x                           # Stop on first failure
pytest -k "test_swap"               # Run matching tests
pytest -m integration               # Run marked tests
pytest --cov=app                    # With coverage
pytest --cov=app --cov-fail-under=70  # Fail if under 70%

# TypeScript (Jest)
cd /home/user/Autonomous-Assignment-Program-Manager/frontend

npm test                            # All tests
npm test -- --coverage              # With coverage
npm test -- --watch                 # Watch mode
npm test -- --testPathPattern=Schedule  # Run matching
```

## Escalation Rules

**Escalate to human when:**

1. Test requires production data access
2. Unclear expected behavior
3. Complex mocking requirements
4. Flaky test identified
5. Performance test thresholds unclear

**Can generate automatically:**

1. Unit tests for pure functions
2. Basic CRUD operation tests
3. Input validation tests
4. Error handling tests
5. Simple integration tests

## Integration with Other Skills

### With code-review
When new code lacks tests:
1. code-review identifies missing coverage
2. test-writer generates test suggestions
3. Verify tests pass before merge

### With automated-code-fixer
When tests fail:
1. Analyze failure reason
2. If test bug, fix test
3. If code bug, trigger automated-code-fixer
4. Re-run tests

### With code-quality-monitor
For coverage tracking:
1. Generate coverage report
2. Identify uncovered lines
3. Generate targeted tests
4. Verify coverage improvement

## References

- `backend/tests/conftest.py` - Pytest fixtures
- `frontend/jest.config.js` - Jest configuration
- `/run-tests` slash command
- `docs/development/TESTING.md` (if exists)
