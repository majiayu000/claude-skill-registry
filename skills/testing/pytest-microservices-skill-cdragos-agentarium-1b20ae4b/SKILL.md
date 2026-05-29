---
name: pytest-microservices-skill
description: Pytest test development for Python microservices. Use when writing unit tests, integration tests, fixtures, mocking external services, or setting up test infrastructure. Triggers on requests to create tests, debug failing tests, test organization, factory fixtures, parametrization, or testcontainers.
---

# Pytest Development

## Workflow

1. **Identify behavior** - Target a single function/behavior per test
2. **Write the test** - Plain function (never a class) with AAA structure
3. **Run and iterate** - Refine for readability and isolation

## Best Practices

- Write plain functions, no test classes
- Name tests `test_<function>_<behavior>` — be specific about inputs and outcomes
- One test per distinct behavior; multiple assertions are fine when verifying one operation's effects
- Use parametrization when testing the same logic with different inputs (e.g., True/False flags)
- Skip trivial tests that verify unchanged/default behavior (e.g., "False stays False")
- Use `HTTPStatus.OK` not `200` for status assertions
- Test both success and error paths
- Verify database state after operations
- Use parametrization for input/output matrices, not loops
- Keep fixtures in app-specific `conftest.py` files
- Use `pytestmark` for module-level markers
- Aim for meaningful coverage, not just high percentages
- Keep imports at the top of the file, never inside test functions
- Use blank lines to separate AAA sections, no comments needed
- Use modern type hints: `dict[str, Any]`, `list[int]`, `str | None` (not `Dict`, `List`, `Optional`)
- Consolidate assertions: Verify status code, response body, and side effects (DB state) in a single test function. Do not split these into separate tests.
- Avoid implementation details: Do not test logging calls, private methods, path construction strings, or simple wrapper delegation.
- Dataclasses for Parametrization: If a parametrized test needs more than 2 arguments, use a dataclass to structure the test cases.

## Project Structure

Always organize tests using src layout with unit/integration split:

```
my-service/
├── src/
│   └── my_service/
├── tests/
│   ├── conftest.py          # Global fixtures
│   ├── mocks/               # Shared mock objects (optional)
│   │   └── fake_s3.py
│   ├── unit/
│   │   ├── conftest.py      # Unit fixtures (mocks)
│   │   └── test_api.py
│   └── integration/
│       ├── conftest.py      # Integration fixtures (containers)
│       └── test_database.py
└── pyproject.toml
```

- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Create the directories if they don't exist

**Unit tests:** Mock everything, run in milliseconds, no external services.

**Integration tests:** Real dependencies via testcontainers.

## Anti-Patterns (Do Not Generate)

- **Test Classes**: Do not use `class TestFoo:` to group tests. Use plain functions with descriptive names like `test_foo_does_x()`. Test classes add unnecessary indentation and `self` parameters.
- **Logging Verification**: Do not test that `logger.error` was called. Exception raising is sufficient contract verification.
- **Wrapper Tests**: Do not test methods that simply call another method (delegation). Test the underlying logic or the full chain.
- **Path Construction**: Do not write tests solely to verify a URL string is built correctly; this is covered by the actual API call test.
- **Atomic Fragmentation**: Do not write separate tests for `status_code`, `response_data`, and `db_state`. Combine them into one behavioral test.

## Test Naming

Good names — specific about function and behavior:
```python
def test_user_creation_with_valid_data(): ...
def test_login_fails_with_invalid_password(): ...
def test_api_returns_404_for_missing_resource(): ...
def test_order_total_includes_tax_for_california(): ...
```

Bad names — vague or meaningless:
```python
def test_1(): ...           # Not descriptive
def test_user(): ...        # Too vague
def test_it_works(): ...    # What works?
```

## Test Structure (AAA Pattern)

Use blank lines to separate Arrange/Act/Assert — no comments needed:

```python
from http import HTTPStatus

# Good — plain function
def test_create_user_returns_201_with_valid_data(client, make_user_payload):
    payload = make_user_payload(email="new@example.com")

    response = client.post("/users", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()["email"] == "new@example.com"

# Bad — test class adds unnecessary structure
class TestCreateUser:  # Don't do this
    def test_returns_201(self, client, make_user_payload):
        payload = make_user_payload(email="new@example.com")
        response = client.post("/users", json=payload)
        assert response.status_code == HTTPStatus.CREATED
```

Test both success and error paths:
```python
def test_create_user_returns_400_with_invalid_email(client, make_user_payload):
    payload = make_user_payload(email="invalid-email")

    response = client.post("/users", json=payload)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "email" in response.json()["errors"]
```

Verify database state after operations:
```python
def test_delete_user_removes_from_database(client, db_session, make_user):
    user = make_user(email="delete@example.com")
    db_session.add(user)
    db_session.commit()
    user_id = user.id

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert db_session.query(User).filter_by(id=user_id).first() is None
```

Testing exceptions:
```python
def test_withdraw_raises_on_insufficient_funds(make_account):
    account = make_account(balance=50.00)

    with pytest.raises(InsufficientFundsError) as exc_info:
        account.withdraw(100.00)

    assert exc_info.value.available == 50.00
    assert exc_info.value.requested == 100.00
```

## Test Consolidation

**Combine** when one operation affects multiple fields:
```python
# Good: One test verifies all effects of mark_completed()
def test_mark_order_completed_updates_status_and_timestamp(db_session, make_order):
    order = make_order(status="pending", completed_at=None)

    mark_completed(order.id)

    result = db_session.query(Order).filter_by(id=order.id).first()
    assert result.status == "completed"
    assert result.completed_at is not None

# Bad: Separate tests for each field
def test_mark_order_completed_sets_status(): ...
def test_mark_order_completed_sets_timestamp(): ...
```

**Parametrize** for input variations:
```python
# Good: One parametrized test
@pytest.mark.parametrize("mark_error", [
    pytest.param(False, id="without_error"),
    pytest.param(True, id="with_error"),
])
def test_create_job_status(db_session, mark_error):
    create_job_status("run-123", mark_error=mark_error)
    result = db_session.query(JobStatus).first()
    assert result.has_error is mark_error

# Bad: Separate tests for True and False
def test_create_job_status_without_error(): ...
def test_create_job_status_with_error(): ...
```

**Skip trivial tests:**
```python
# Skip: Testing that False stays False adds no value
def test_error_stays_false_when_not_marked(): ...  # Don't write this
```

**Consolidate Initialization Tests**: Instead of testing every service property separately, verify the container in one go.

```python
# Good: Comprehensive Container Test
def test_service_container_initializes_all_services(mock_client):
    container = ServiceContainer(mock_client)

    # Verify all services exist and share the client
    assert isinstance(container.users, UserService)
    assert isinstance(container.orders, OrderService)
    assert container.users.client is mock_client
    assert container.orders.client is mock_client
```

## Fixtures

### Factory Pattern

Use `make_*` naming with inner factory functions:

```python
@pytest.fixture
def make_chat_session():
    def _make(user, **kwargs):
        defaults = {"session_id": uuid4()}
        defaults.update(kwargs)
        return ChatSession.objects.create(user=user, **defaults)
    return _make

# Usage
def test_session_behavior(admin_user, make_chat_session):
    session = make_chat_session(admin_user, status="active")
    assert session.user == admin_user
```

Full example with factory fixture:
```python
@pytest.fixture
def make_order():
    def _make(user, items=None, **kwargs):
        defaults = {"status": "pending", "items": items or []}
        defaults.update(kwargs)
        return Order(user=user, **defaults)
    return _make

def test_order_total_calculates_with_tax(make_order, make_user):
    user = make_user(state="CA")
    order = make_order(user=user, items=[{"name": "Widget", "price": 100.00, "quantity": 2}])

    total = order.calculate_total()

    assert total == 214.50  # 200 + 7.25% tax
```

### Conftest Hierarchy

**tests/conftest.py** — Global fixtures:
```python
@pytest.fixture(scope="session")
def app_settings():
    return {"debug": True, "db_url": "sqlite:///:memory:"}
```

**tests/unit/conftest.py** — Unit-specific mocks:
```python
@pytest.fixture
def mock_db_session(mocker):
    return mocker.MagicMock()
```

**tests/integration/conftest.py** — Real resources:
```python
@pytest.fixture(scope="module")
def db_session(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    with Session(engine) as session:
        yield session
        session.rollback()
```

### Fixture Scopes

| Scope | Lifecycle | Use for |
|-------|-----------|---------|
| `function` | Each test (default) | Test-specific data |
| `module` | Per test file | Expensive setup shared by file |
| `session` | Entire test run | Containers, app config |

### Teardown

Use `yield` for cleanup:
```python
@pytest.fixture
def temp_file():
    path = Path("/tmp/test_file.txt")
    path.write_text("test")
    yield path
    path.unlink()  # Cleanup after test
```

## Mocking

### pytest-mock

Use the `mocker` fixture (not `unittest.mock` directly):

```python
def test_api_call(mocker):
    mock_client = mocker.patch("myservice.api.external_client")
    mock_client.return_value.fetch.return_value = {"data": "test"}

    result = call_external_api()

    assert result == {"data": "test"}
    mock_client.return_value.fetch.assert_called_once()
```

Mock assertions:
```python
mock_client.assert_called_once()
mock_client.assert_awaited_once_with(user=admin_user, project=project)
mock_client.assert_not_called()
assert mock_client.call_count == 1
assert mock_client.call_args.kwargs["id"] == "test_123"
```

Patching patterns:
```python
# Patch where it's used, not where it's defined
mocker.patch("myservice.handlers.requests.get")

# Patch object attribute
mocker.patch.object(MyClass, "method", return_value="mocked")

# Patch with side effect
mocker.patch("module.func", side_effect=ValueError("error"))
```

### Shared Mocks

**Inline mocks** — For simple, single-test mocks:
```python
def test_payment(mocker):
    mock_stripe = mocker.patch("myservice.payments.stripe")
    mock_stripe.charge.return_value = {"id": "ch_123"}
    # test logic
```

**Shared mocks** — For complex fakes reused across multiple tests, create `tests/mocks/` module:

```python
# tests/mocks/fake_s3.py
class FakeS3Client:
    def __init__(self):
        self.storage = {}

    def put_object(self, Bucket, Key, Body):
        self.storage[f"{Bucket}/{Key}"] = Body

    def get_object(self, Bucket, Key):
        return {"Body": self.storage[f"{Bucket}/{Key}"]}

# tests/conftest.py
from tests.mocks.fake_s3 import FakeS3Client

@pytest.fixture
def fake_s3():
    return FakeS3Client()
```

### freezegun (Time-Based Testing)

```python
from freezegun import freeze_time

def test_session_expiry(session_service, admin_user):
    with freeze_time("2023-01-01 12:00:00"):
        session = session_service.create_session(user=admin_user)

    with freeze_time("2023-01-01 13:00:00"):  # 1 hour later
        assert session_service.is_expired(session) is True
```

### testcontainers (Integration Tests)

PostgreSQL:
```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture
def db_session(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()
```

Redis:
```python
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="module")
def redis_container():
    with RedisContainer("redis:7") as redis:
        yield redis
```

Place container fixtures in `tests/integration/conftest.py` with `scope="module"` or `scope="session"`.

## Parametrization

**Rule:** Use `pytest.mark.parametrize` for inputs. If the test case requires more than 2 arguments, define a dataclass at module level.

### Dataclass Placement

Define parametrization dataclasses after imports, before tests:

```python
from dataclasses import dataclass, field
from typing import Any

import pytest

pytestmark = pytest.mark.unit


@dataclass
class ApiRequestCase:
    method: str
    path: str
    status_code: int
    response_data: dict[str, Any]
    request_kwargs: dict[str, Any] = field(default_factory=dict)
    assertion_checks: dict[str, Any] = field(default_factory=dict)


def test_api_client_request_successful_scenarios(case):
    ...
```

### Complex Parametrization (Dataclass Pattern)

Use dataclasses for 3+ parameters with modern type hints:

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ApiCase:
    payload: dict[str, Any]
    expected_status: int
    expected_error: str | None = None
    headers: dict[str, str] = field(default_factory=dict)

@pytest.mark.parametrize("case", [
    ApiCase(
        payload={"email": "bad-format", "name": "Test"},
        expected_status=400,
        expected_error="Invalid email"
    ),
    ApiCase(
        payload={"email": "good@test.com"},
        expected_status=400,
        expected_error="Field 'name' required"
    ),
], ids=lambda c: f"status_{c.expected_status}")
def test_create_user_validation(client, case):
    response = client.post("/users", json=case.payload, headers=case.headers)

    assert response.status_code == case.expected_status
    if case.expected_error:
        assert case.expected_error in response.json()["detail"]
```

**ID Generation Tips:**
- Use lambda to generate IDs from dataclass fields
- Keep IDs concise but meaningful
- Do not add fields solely for test IDs (like `description`)
- Examples:
  - `ids=lambda c: c.method.lower()`
  - `ids=lambda c: f"{c.status}_{c.type}"`
  - `ids=lambda c: f"{c.method.lower()}_{c.status_code}"`
  - `ids=lambda c: "guaranteed_pass" if c.guaranteed_pass else "guaranteed_fail"`

**Type Hints:**
- Use lowercase: `dict[str, Any]`, `list[int]`, not `Dict`, `List`
- Use pipe syntax: `str | None`, not `Optional[str]`
- Only import `Any` from typing when needed

### Simple Parametrization (Tuple Pattern)

For 1 or 2 arguments, tuples are acceptable:

```python
@pytest.mark.parametrize("status_code, should_retry", [
    (500, True),
    (400, False),
], ids=["server_error", "client_error"])
def test_retry_logic(status_code, should_retry):
    assert should_retry_request(status_code) == should_retry
```

## Markers

```python
import pytest
pytestmark = pytest.mark.integration  # Module-level

@pytest.mark.slow
def test_heavy_computation(): ...

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_specific(): ...

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug(): ...
```

Run by marker: `pytest -m "not slow"` or `pytest -m integration`

## Running Tests

```bash
uv run pytest                                      # All tests
uv run pytest -m unit                              # Unit tests only
uv run pytest -m integration                       # Integration tests only
uv run pytest tests/unit/test_module.py::test_name # Specific test
uv run pytest -v -s                                # Verbose with print output
uv run pytest --cov=src --cov-report=term-missing  # Coverage report
uv run pytest --cov-fail-under=80                  # Enforce 80% coverage
uv run pytest -k "user"                            # Match test names
```

## Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short"
markers = [
    "unit: fast running unit tests",
    "integration: slow running integration tests",
]

[tool.pytest_env]
# Environment variables for tests (requires pytest-env)
DATABASE_URL = "postgresql://test:test@localhost:5432/test_db"
REDIS_URL = "redis://localhost:6379/0"
ENV = "test"
DEBUG = "false"
```

## Checklist

Before finishing, verify:

- [ ] Tests placed in `tests/unit/` or `tests/integration/`
- [ ] Imports at top of file, not inside functions
- [ ] Modern type hints: `dict[str, Any]`, `list[int]`, `str | None`
- [ ] Dataclasses defined at module level (after imports, before tests)
- [ ] Plain functions, no test classes
- [ ] Names follow `test_<function>_<behavior>`
- [ ] Blank lines separate AAA sections (no comments)
- [ ] One test per behavior (combine assertions for one operation's effects)
- [ ] Parametrization used for input variations (True/False, different values)
- [ ] Dataclasses used for 3+ parametrization arguments
- [ ] Lambda-based test IDs generated from dataclass fields
- [ ] No trivial tests (e.g., "False stays False")
- [ ] Using `HTTPStatus` enum, not raw status codes
- [ ] Testing both success and error paths
- [ ] Factory fixtures use `make_*` naming
- [ ] Mocks use `mocker` fixture, not `unittest.mock`
- [ ] Patching where used, not where defined
- [ ] Time tests use `freezegun`
- [ ] Integration tests use `testcontainers`
