---
name: python-testing-guidelines
description: This skill should be used when writing or reviewing Python tests. It enforces a dummy-class pattern over unittest.mock, requiring all test dependencies to use explicit dummy classes instead of Mock, MagicMock, AsyncMock, or patch().
---

# Python Testing Guidelines

## Core Principles

1. **Never use `unittest.mock`** - No `Mock`, `MagicMock`, `AsyncMock`, or `patch()`
2. **Use dummy classes** that inherit from real implementations
3. **Wrap infrastructure** in injectable dependencies (hexagonal architecture, kept pragmatic)
4. **Minimal test dependencies** - Only `pytest` and `pytest-asyncio`
5. **Tests as living documentation** - Emphasize failure cases and edge cases to document what the code does and does not do

## Discouraged Libraries

Do not use: `factory_boy`, `faker`, `respx`, `pytest-mock`, `responses`, `hypothesis`, or similar testing utilities.

**On `hypothesis` and property-based testing:** When asked to implement property-based testing, use `@pytest.mark.parametrize` with explicit example values instead of `hypothesis`. This keeps test dependencies minimal and ensures test cases serve as readable documentation.

## File Organization

### Test Directory Structure

The `tests/` folder mirrors the `src/` (or `app/`) file tree exactly:

```
project/
├── src/
│   ├── payments/
│   │   ├── gateways.py        # StripeGateway, PaypalGateway
│   │   └── validation.py      # validate_card()
│   └── users/
│       └── auth.py            # Authenticator.login(), Authenticator.logout()
└── tests/
    ├── fixtures.py            # All dummies and @pytest.fixture declarations
    ├── payments/
    │   ├── test_gateways.py
    │   └── test_validation.py
    └── users/
        └── test_auth.py
```

### Test File Naming

Always use `test_<module>.py` format.

### Test Class Organization

Each tested method gets its own test class. No inheritance in test classes.

**Single-class modules:** Use `TestMethodName`

```python
# tests/payments/test_validation.py
class TestValidateCard:
    def test_accepts_valid_visa(self):
        ...
    
    def test_rejects_expired_card(self):
        ...
```

**Multi-class modules:** Prefix with class name `TestClassNameMethodName`

```python
# tests/payments/test_gateways.py
class TestStripeGatewayCharge:
    def test_records_amount(self, stripe_gateway):
        ...
    
    def test_returns_success_result(self, stripe_gateway):
        ...

class TestStripeGatewayRefund:
    def test_refunds_full_amount(self, stripe_gateway):
        ...

class TestPaypalGatewayCharge:
    def test_records_amount(self, paypal_gateway):
        ...
```

### Test Methods

Each test method is either:
- A single test case
- A parametrized method for table-driven tests

### Test Naming Convention

- **Failure/rejection tests**: Use action verbs - `test_rejects_X`, `test_fails_when_X`, `test_handles_missing_X`
- **Invariant/property tests**: Use declarative style - `test_amount_must_be_positive`, `test_output_is_always_sorted`
- **Happy path tests**: Use action-oriented names - `test_charges_correct_amount`, `test_returns_user_profile`

```python
class TestValidateAmount:
    # Happy path
    def test_accepts_positive_amount(self):
        ...
    
    # Failure cases (document what the code rejects)
    def test_rejects_negative_amount(self):
        ...
    
    def test_rejects_zero_amount(self):
        ...
    
    def test_rejects_none(self):
        ...
```

## Parametrized Tests

Use `@pytest.mark.parametrize` with explicit example values for table-driven tests.

```python
class TestValidateAmount:
    @pytest.mark.parametrize("amount,expected", [
        (Decimal("10.00"), True),
        (Decimal("0"), False),
        (Decimal("-5.00"), False),
    ])
    def test_validates_amount(self, amount, expected):
        assert validate_amount(amount) == expected
```

Use `pytest.param(..., id="...")` when it improves readability:

```python
class TestParseDate:
    @pytest.mark.parametrize("input,expected", [
        pytest.param("2024-01-01", date(2024, 1, 1), id="iso_format"),
        pytest.param("01/01/2024", date(2024, 1, 1), id="us_format"),
        pytest.param("invalid", None, id="invalid_returns_none"),
    ])
    def test_parses_date(self, input, expected):
        assert parse_date(input) == expected
```

Skip IDs when the values are self-explanatory.

### Use Cases for Parametrized Tests

- **Invariants**: Output always satisfies a property
- **Round-trips**: Encode then decode returns original
- **Boundary conditions**: Edge cases around limits
- **Reference comparisons**: Compare against known-good values

## Tests as Living Documentation

Tests should document what the code does and does not do. Emphasize failure cases and edge cases.

### Testing Expected Errors

Use `pytest.raises` to assert exception types:

```python
class TestWithdraw:
    def test_withdraws_available_balance(self, account):
        account.deposit(Decimal("100.00"))
        account.withdraw(Decimal("50.00"))
        assert account.balance == Decimal("50.00")
    
    def test_rejects_overdraft(self, account):
        account.deposit(Decimal("100.00"))
        with pytest.raises(InsufficientFundsError):
            account.withdraw(Decimal("150.00"))
    
    def test_rejects_negative_amount(self, account):
        with pytest.raises(ValueError):
            account.withdraw(Decimal("-10.00"))
```

### Edge Cases to Consider

For every function, consider testing:

- **Boundary values**: Zero, negative, maximum, minimum
- **Empty inputs**: Empty string, empty list, None
- **Invalid types**: Wrong type passed (if not caught by type hints)
- **Missing data**: Required fields absent
- **Malformed data**: Invalid format, encoding issues

```python
class TestParseEmail:
    # Happy path
    def test_parses_valid_email(self):
        assert parse_email("user@example.com") == ("user", "example.com")
    
    # Edge cases - document what is rejected
    def test_rejects_empty_string(self):
        with pytest.raises(ValueError):
            parse_email("")
    
    def test_rejects_missing_at_symbol(self):
        with pytest.raises(ValueError):
            parse_email("userexample.com")
    
    def test_rejects_multiple_at_symbols(self):
        with pytest.raises(ValueError):
            parse_email("user@@example.com")
    
    def test_rejects_none(self):
        with pytest.raises(TypeError):
            parse_email(None)
```

### Coverage Philosophy

- Every public function should have at least one failure test
- Complex logic warrants more edge case coverage
- Tests document the contract: "this input produces this output" and "this input is rejected"

## Rule 1: Dummies Inherit from Real Classes

Dummy classes inherit from the real class and override methods. Typically skip `super().__init__()`, but call it when rational and needed (e.g., when the parent initializes state the dummy relies on).

```python
# infra/stripe_gateway.py
class StripeGateway:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client
    
    async def charge(self, amount: Decimal) -> PaymentResult:
        response = await self.client.post(...)
        return PaymentResult(...)

# tests/fixtures.py
class DummyStripeGateway(StripeGateway):
    def __init__(self):
        # Skip super().__init__() - no real client needed
        self.charges = []
    
    async def charge(self, amount: Decimal) -> PaymentResult:
        self.charges.append(amount)
        return PaymentResult(success=True)
```

Do not define `Protocol` or ABC interfaces. Keep it simple: real class + dummy that inherits from it.

## Rule 2: Wrap Stdlib in Injectable Classes

Never call stdlib directly for time, sleep, or similar. Wrap in injectable dependencies.

```python
# infra/clock.py
class Clock:
    def now(self) -> datetime:
        return datetime.now()
    
    async def sleep(self, seconds: float):
        await asyncio.sleep(seconds)

# tests/fixtures.py
class DummyClock(Clock):
    def __init__(self, fixed_time: datetime = None):
        self.fixed_time = fixed_time or datetime(2024, 1, 1)
        self.sleep_calls = []
    
    def now(self) -> datetime:
        return self.fixed_time
    
    async def sleep(self, seconds: float):
        self.sleep_calls.append(seconds)
```

## Rule 3: Injectable Config Classes

Wrap environment variables and configuration in injectable classes.

```python
# infra/config.py
class Config:
    def __init__(self):
        self.db_host = os.environ["DB_HOST"]
        self.db_port = int(os.environ.get("DB_PORT", 5432))
        self.api_key = os.environ["API_KEY"]

# tests/fixtures.py
class DummyConfig(Config):
    def __init__(self):
        self.db_host = "localhost"
        self.db_port = 5432
        self.api_key = "test-key"
```

Do not use `monkeypatch.setenv()`. Inject the config class instead.

## Rule 4: Handle Async with Real Async Methods

```python
# BAD
async def test_db():
    mock_session = AsyncMock()
    await mock_session.execute()

# GOOD
class DummySession(Session):
    async def execute(self, query):
        return []
```

## Rule 5: All Fixtures in tests/fixtures.py

Centralize all dummy classes and `@pytest.fixture` declarations in `tests/fixtures.py`.

```python
# tests/fixtures.py
import pytest
from infra.clock import Clock
from infra.stripe_gateway import StripeGateway

# --- Dummy Classes ---

class DummyClock(Clock):
    ...

class DummyStripeGateway(StripeGateway):
    ...

# --- Pytest Fixtures ---

@pytest.fixture
def clock():
    return DummyClock()

@pytest.fixture
def payment_gateway():
    return DummyStripeGateway()
```

Do not use `conftest.py`. Import fixtures explicitly in test files:

```python
# tests/test_payments.py
from tests.fixtures import payment_gateway

def test_charge_succeeds(payment_gateway):
    ...
```

## Rule 6: Track State for Verification

Add tracking attributes to dummies instead of asserting on mock calls.

```python
# tests/fixtures.py
class DummySession(Session):
    def __init__(self):
        self.commit_called = False
        self.rollback_called = False
        self.executed_queries = []

    def commit(self):
        self.commit_called = True
    
    async def execute(self, query):
        self.executed_queries.append(query)
        return []

# tests/test_db.py
def test_session_commits_on_success():
    session = DummySession()
    save_data(session)
    assert session.commit_called
```

## Rule 7: Dedicated Dummies for Error Scenarios

Create separate dummy classes for error cases.

```python
# tests/fixtures.py
class DummyCrawler(Crawler):
    async def fetch(self, url: str):
        return "<html>...</html>"

class DummyCrawlerWithConnectionError(Crawler):
    async def fetch(self, url: str):
        raise ConnectionError("Network failed")

class DummyCrawlerWithTimeout(Crawler):
    async def fetch(self, url: str):
        await asyncio.sleep(9999)
```

## Rule 8: Keep Tests Simple

One behavior per test. If setup is complex, split the test or refactor the production code.

```python
# BAD - testing too much
def test_everything():
    db = DummyDatabase()
    cache = DummyCache()
    client = DummyHttpClient()
    gateway = DummyPaymentGateway()
    # ... complex orchestration

# GOOD - one behavior
def test_charge_records_amount(payment_gateway):
    payment_gateway.charge(Decimal("10.00"))
    assert payment_gateway.charges == [Decimal("10.00")]
```

## Rule 9: Integration Tests with TestClient

Using `TestClient` from FastAPI/Starlette is acceptable for integration tests.

```python
from fastapi.testclient import TestClient
from tests.fixtures import DummyConfig, DummyStripeGateway

def test_payment_endpoint():
    app = create_app(
        config=DummyConfig(),
        payment_gateway=DummyStripeGateway(),
    )
    client = TestClient(app)
    response = client.post("/pay", json={"amount": "10.00"})
    assert response.status_code == 200
```

## Anti-Patterns

| Anti-Pattern | Fix |
|--------------|-----|
| `MagicMock()` | Dummy class inheriting from real class |
| `AsyncMock()` | Real `async def` in dummy class |
| `patch()` | Injectable dependency |
| `monkeypatch.setenv()` | Injectable config class |
| `assert mock.method.called` | `assert dummy.method_called` |
| Fixtures in `conftest.py` | Centralize in `tests/fixtures.py` |
| `Protocol` / ABC interfaces | Dummy inherits directly from real class |
| `hypothesis` / property-based libs | `@pytest.mark.parametrize` with explicit values |
| Tests not mirroring source structure | `tests/` mirrors `src/` exactly |
| Test class inheritance | Flat test classes, no inheritance |

## Quick Reference

```
Test needs a dependency?
    → Create Dummy class inheriting from real class in tests/fixtures.py

External service (HTTP, DB, etc.)?
    → Wrap in infra class, dummy inherits from it

Stdlib call (time, sleep)?
    → Wrap in injectable class (Clock, etc.)

Environment variables?
    → Injectable Config class

Need to verify calls?
    → Add tracking attributes to dummy

Error scenario?
    → Create dedicated DummyXxxWithError class

Where does the test file go?
    → Mirror source path: src/foo/bar.py → tests/foo/test_bar.py

How to name test class?
    → Single class in module: TestMethodName
    → Multiple classes in module: TestClassNameMethodName

Multiple test cases for same behavior?
    → @pytest.mark.parametrize with explicit values

How to name test methods?
    → Failures: test_rejects_X, test_fails_when_X
    → Invariants: test_X_must_be_Y
    → Happy path: test_does_X

Testing expected errors?
    → pytest.raises(ExceptionType)

Property-based testing requested?
    → Use @pytest.mark.parametrize with explicit values, NOT hypothesis
```
