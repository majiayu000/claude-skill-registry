---
name: pytests
description: Create comprehensive Python test suites with pytest. Supports unit, integration,
  e2e, and user flow tests. Dual-mode testing for FastAPI (direct code + live API).
  Uses functional style (no test classe
---

---
name: pytests
description: Create comprehensive Python test suites with pytest. Supports unit, integration, e2e, and user flow tests. Dual-mode testing for FastAPI (direct code + live API). Uses functional style (no test classes). File naming: <name>_test.py.
---

# Python Testing Skill

Create well-structured, comprehensive Python test suites following best practices.

## When to Use

Use this skill when:
- Setting up a test suite for a Python project
- Adding tests to an existing codebase
- Creating tests for FastAPI/web applications
- Need unit, integration, e2e, or user flow tests

## Core Principles

1. **Functional style** - No test classes, use plain functions
2. **Naming convention** - Files: `<name>_test.py`, functions: `test_<behavior>`
3. **Tests in root** - All tests live in `tests/` at project root
4. **Dual-mode for APIs** - Test directly against code OR via live server
5. **Arrange-Act-Assert** - Clear test structure
6. **One assertion per concept** - Keep tests focused

## Test Categories

| Type | Purpose | Location | Speed |
|------|---------|----------|-------|
| Unit | Test isolated functions/classes | `tests/unit/` | Fast |
| Integration | Test component interactions | `tests/integration/` | Medium |
| E2E | Test full request/response cycles | `tests/e2e/` | Slow |
| User Flow | Test real user scenarios | `tests/flows/` | Slow |

## Directory Structure

```
project/
├── src/
│   └── myapp/
│       ├── main.py
│       ├── services/
│       └── models/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── fixtures/             # Reusable test data
│   │   ├── __init__.py
│   │   └── factories.py      # Data factories
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── conftest.py       # Unit-specific fixtures
│   │   ├── services_test.py
│   │   └── models_test.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── api_test.py
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── endpoints_test.py
│   └── flows/
│       ├── __init__.py
│       ├── conftest.py
│       └── user_journey_test.py
├── pytest.ini
└── pyproject.toml
```

## Setup Steps

### 1. Install Test Dependencies

Add to `pyproject.toml`:

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=6.0.0",
    "pytest-xdist>=3.5.0",      # Parallel execution
    "pytest-sugar>=1.0.0",       # Better output
    "pytest-randomly>=3.15.0",   # Randomize test order
    "httpx>=0.28.0",             # Async HTTP client
    "respx>=0.21.0",             # Mock HTTP requests
    "factory-boy>=3.3.0",        # Test data factories
    "faker>=30.0.0",             # Fake data generation
    "freezegun>=1.4.0",          # Time mocking
    "aiosqlite>=0.20.0",         # Async SQLite for tests
]
```

Install:
```bash
uv sync --extra dev
```

### 2. Create pytest.ini

Use template: [templates/pytest.ini](templates/pytest.ini)

### 3. Create Root conftest.py

Use template: [templates/conftest.py](templates/conftest.py)

Key features:
- Dual-mode client fixture (direct vs live API)
- Database fixtures with automatic cleanup
- Environment variable fixtures
- Common async fixtures

### 4. Create Test Files

Follow naming: `<descriptive_name>_test.py`

Examples:
- `auth_test.py` (not `test_auth.py`)
- `user_service_test.py`
- `checkout_flow_test.py`

## Dual-Mode API Testing

The skill supports two testing modes for FastAPI applications:

### Mode 1: Direct Testing (Default)
Tests against the application directly using ASGI transport. Fast, no server needed.

```python
@pytest.fixture
def client(app):
    """Direct ASGI client - tests code directly."""
    transport = ASGITransport(app=app)
    with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
```

### Mode 2: Live Server Testing
Tests against a running server. Set `TEST_SERVER_URL` environment variable.

```bash
# Start your server
uvicorn myapp.main:app --port 8000

# Run tests against it
TEST_SERVER_URL=http://localhost:8000 pytest tests/e2e/
```

```python
@pytest.fixture
def client():
    """Live server client - tests running API."""
    base_url = os.environ.get("TEST_SERVER_URL", "http://localhost:8000")
    with AsyncClient(base_url=base_url) as c:
        yield c
```

The conftest.py template automatically switches between modes based on `TEST_SERVER_URL`.

## Test Templates

### Unit Test Pattern

```python
"""Unit tests for user service."""
import pytest
from myapp.services.user import create_user, validate_email


def test_validate_email_accepts_valid_format():
    """Valid email format should return True."""
    assert validate_email("user@example.com") is True


def test_validate_email_rejects_missing_at():
    """Email without @ should return False."""
    assert validate_email("userexample.com") is False


@pytest.mark.asyncio
async def test_create_user_returns_user_with_id(db_session, user_factory):
    """Creating a user should return user with generated ID."""
    # Arrange
    user_data = user_factory.build()

    # Act
    result = await create_user(db_session, user_data)

    # Assert
    assert result.id is not None
    assert result.email == user_data.email
```

### Integration Test Pattern

```python
"""Integration tests for auth endpoints."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_returns_token_for_valid_credentials(
    client: AsyncClient,
    registered_user,
):
    """Login with valid credentials should return access token."""
    # Act
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": registered_user.email, "password": "testpass123"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_returns_401_for_wrong_password(
    client: AsyncClient,
    registered_user,
):
    """Login with wrong password should return 401."""
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": registered_user.email, "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert "detail" in response.json()
```

### E2E Test Pattern

```python
"""End-to-end tests for order processing."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.e2e
async def test_complete_order_flow(
    client: AsyncClient,
    auth_headers,
    product_in_stock,
):
    """Full order flow: add to cart -> checkout -> confirm."""
    # Add to cart
    cart_response = await client.post(
        "/api/v1/cart/items",
        json={"product_id": product_in_stock.id, "quantity": 2},
        headers=auth_headers,
    )
    assert cart_response.status_code == 201

    # Checkout
    checkout_response = await client.post(
        "/api/v1/checkout",
        json={"payment_method": "card", "shipping_address_id": 1},
        headers=auth_headers,
    )
    assert checkout_response.status_code == 200
    order_id = checkout_response.json()["order_id"]

    # Verify order
    order_response = await client.get(
        f"/api/v1/orders/{order_id}",
        headers=auth_headers,
    )
    assert order_response.status_code == 200
    assert order_response.json()["status"] == "confirmed"
```

### User Flow Test Pattern

```python
"""User flow tests for new user onboarding."""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.flow
async def test_new_user_onboarding_complete_journey(
    client: AsyncClient,
    unique_email,
):
    """New user can register, verify email, complete profile, make purchase."""
    # Step 1: Register
    register_resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "password": "SecurePass123!",
            "name": "Test User",
        },
    )
    assert register_resp.status_code == 201
    user_id = register_resp.json()["id"]

    # Step 2: Login (simulate email verified for test)
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": unique_email, "password": "SecurePass123!"},
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Complete profile
    profile_resp = await client.patch(
        "/api/v1/users/me/profile",
        json={"phone": "+1234567890", "preferences": {"newsletter": True}},
        headers=headers,
    )
    assert profile_resp.status_code == 200

    # Step 4: Browse products
    products_resp = await client.get("/api/v1/products?limit=5")
    assert products_resp.status_code == 200
    products = products_resp.json()["items"]
    assert len(products) > 0

    # Step 5: Add to cart and checkout
    await client.post(
        "/api/v1/cart/items",
        json={"product_id": products[0]["id"], "quantity": 1},
        headers=headers,
    )

    # Verify user state
    me_resp = await client.get("/api/v1/users/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["profile_completed"] is True
```

## Fixtures Reference

### Common Fixtures (in conftest.py)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `client` | function | HTTP client (dual-mode) |
| `db_session` | function | Database session with rollback |
| `async_engine` | session | Async database engine |
| `app` | session | FastAPI application instance |
| `auth_headers` | function | Authorization headers with valid token |
| `registered_user` | function | Pre-created test user |
| `unique_email` | function | Generate unique email for test |

### Factory Pattern

Use factory-boy for consistent test data:

```python
# tests/fixtures/factories.py
import factory
from faker import Faker
from myapp.models import User, Product

fake = Faker()


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyFunction(lambda: fake.email())
    name = factory.LazyFunction(lambda: fake.name())
    is_active = True


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.LazyFunction(lambda: fake.product_name())
    price = factory.LazyFunction(lambda: fake.pydecimal(min_value=1, max_value=1000))
    stock = factory.LazyFunction(lambda: fake.random_int(min=0, max=100))
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific category
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/e2e/
uv run pytest tests/flows/

# Run by marker
uv run pytest -m "not slow"
uv run pytest -m e2e
uv run pytest -m flow

# Run in parallel
uv run pytest -n auto

# Run against live server
TEST_SERVER_URL=http://localhost:8000 uv run pytest tests/e2e/

# Verbose with print output
uv run pytest -v -s

# Run single test
uv run pytest tests/unit/services_test.py::test_validate_email_accepts_valid_format

# Stop on first failure
uv run pytest -x

# Re-run failed tests
uv run pytest --lf
```

## Best Practices

### DO

- Name tests after the behavior being tested
- Use descriptive assertion messages
- Keep tests independent (no shared state)
- Use fixtures for setup, not test code
- Mock external services (APIs, email, etc.)
- Test edge cases and error conditions
- Use parametrize for similar tests with different data
- Clean up resources in fixtures (use yield)

### DON'T

- Use test classes (use functions)
- Share state between tests
- Test implementation details
- Make tests depend on execution order
- Use `time.sleep()` (use proper async waiting)
- Hardcode test data in multiple places
- Skip writing tests for "obvious" code
- Mix unit and integration concerns

### Parametrized Tests

```python
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user@sub.example.com", True),
    ("user+tag@example.com", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
])
def test_validate_email(email, expected):
    """Email validation handles various formats correctly."""
    assert validate_email(email) is expected
```

### Async Parametrized Tests

```python
@pytest.mark.asyncio
@pytest.mark.parametrize("endpoint,expected_status", [
    ("/api/v1/health", 200),
    ("/api/v1/health/ready", 200),
    ("/api/v1/nonexistent", 404),
])
async def test_endpoint_status_codes(client, endpoint, expected_status):
    """Health endpoints return expected status codes."""
    response = await client.get(endpoint)
    assert response.status_code == expected_status
```

## Markers Reference

Define in `pytest.ini`:

```ini
[pytest]
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    e2e: end-to-end tests
    flow: user flow tests
    integration: integration tests
    unit: unit tests
    wip: work in progress (skip in CI)
```

Usage:

```python
@pytest.mark.slow
def test_heavy_computation():
    ...

@pytest.mark.e2e
async def test_full_checkout():
    ...

@pytest.mark.skip(reason="Waiting for API v2")
def test_new_feature():
    ...

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific():
    ...
```
