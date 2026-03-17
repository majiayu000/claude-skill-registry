---
name: Test Engineer
description: Software testing, test strategy, and quality assurance. USE WHEN user mentions tests, testing, unit tests, integration tests, e2e, coverage, mocking, fixtures, TDD, BDD, test automation, or asks about how to test or validate code.
---

# Test Engineer Skill

AI-powered testing guidance for designing, implementing, and maintaining comprehensive test suites with focus on reliability, coverage, and test-driven development principles.

## What This Skill Does

This skill provides expert-level testing guidance including test strategy, test architecture, mock/stub design, coverage analysis, and debugging failing tests. It combines software testing best practices with practical, actionable recommendations.

**Key Capabilities:**
- **Test Strategy**: Test pyramid design, coverage goals, testing philosophies
- **Unit Testing**: Isolation patterns, mocking, assertions, fixtures
- **Integration Testing**: Component integration, API testing, database testing
- **End-to-End Testing**: User flows, browser automation, visual testing
- **Test Automation**: CI/CD integration, parallel execution, flaky test detection
- **TDD/BDD**: Test-first development, behavior specifications, acceptance criteria

## Core Principles

### The Testing Pyramid
```
          ┌───────────┐
          │   E2E     │  ← Few, slow, expensive
          ├───────────┤
          │Integration│  ← Some, medium speed
          ├───────────┤
          │   Unit    │  ← Many, fast, cheap
          └───────────┘
```

### The FIRST Principles
- **F**ast: Tests should run quickly
- **I**solated: Tests don't depend on each other
- **R**epeatable: Same result every time
- **S**elf-Validating: Pass or fail, no interpretation needed
- **T**imely: Written at the right time (ideally before code)

### Test Quality Attributes
1. **Clarity** - Easy to understand what's being tested
2. **Maintainability** - Easy to update when code changes
3. **Reliability** - No flaky tests, consistent results
4. **Speed** - Fast feedback loops
5. **Coverage** - Adequate coverage of critical paths

## Test Assessment Workflow

### 1. Test Suite Analysis
```
Analyze the current test suite:
├── Structure (test organization, naming)
├── Coverage (line, branch, path coverage)
├── Speed (execution time distribution)
├── Reliability (flaky test detection)
└── Gaps (untested critical paths)
```

### 2. Test Health Metrics
- **Coverage Score**: What percentage of code is tested?
- **Test-to-Code Ratio**: How many test lines per code line?
- **Execution Time**: How long does the full suite take?
- **Flakiness Rate**: How often do tests fail randomly?
- **Mutation Score**: How many mutants are killed?

### 3. Recommendations
Generate prioritized recommendations based on:
- Risk (what's most important to test)
- Coverage Gaps (what's not tested)
- Reliability (what's flaky or slow)
- Maintainability (what's hard to maintain)

## Testing Patterns by Type

### Unit Testing
```python
# Arrange-Act-Assert (AAA) Pattern
def test_calculate_discount():
    # Arrange
    cart = Cart(items=[Item(price=100)])
    discount = PercentageDiscount(10)
    
    # Act
    total = cart.apply_discount(discount)
    
    # Assert
    assert total == 90
```
**Use When:** Testing individual functions, classes, or methods in isolation

### Integration Testing
```python
# Test component interactions
def test_user_registration_flow():
    # Test that UserService correctly interacts with
    # Database, EmailService, and Validator
    user_service = UserService(db, email_svc, validator)
    
    result = user_service.register("test@example.com", "password")
    
    assert result.success
    assert db.find_user("test@example.com") is not None
    assert email_svc.sent_emails[-1].to == "test@example.com"
```
**Use When:** Testing how components work together

### End-to-End Testing
```python
# Test full user flows
def test_checkout_flow(browser):
    browser.goto("/products")
    browser.click("#add-to-cart-btn")
    browser.goto("/cart")
    browser.click("#checkout-btn")
    browser.fill("#email", "user@test.com")
    browser.click("#submit-order")
    
    assert browser.url == "/order-confirmation"
    assert "Order placed" in browser.text
```
**Use When:** Validating complete user journeys

### API Testing
```python
# Test REST/GraphQL endpoints
def test_create_user_endpoint(client):
    response = client.post("/api/users", json={
        "email": "new@test.com",
        "name": "Test User"
    })
    
    assert response.status_code == 201
    assert response.json["id"] is not None
    assert response.json["email"] == "new@test.com"
```
**Use When:** Testing HTTP APIs and web services

## Mocking Strategies

### When to Mock
| Mock | Don't Mock |
|------|------------|
| External APIs | Core business logic |
| Databases (in unit tests) | Simple value objects |
| File systems | Pure functions |
| Time/randomness | In-memory implementations |
| Email/SMS services | The system under test |

### Mocking Patterns
```python
# Spy - Track calls without changing behavior
from unittest.mock import MagicMock

def test_notification_sent():
    notifier = MagicMock()
    service = UserService(notifier=notifier)
    
    service.create_user("test@example.com")
    
    notifier.send.assert_called_once_with(
        to="test@example.com",
        subject="Welcome!"
    )
```

```python
# Stub - Provide canned responses
def test_fetch_user_data():
    api_client = MagicMock()
    api_client.get.return_value = {"name": "John", "age": 30}
    
    service = DataService(api=api_client)
    result = service.get_user_profile(123)
    
    assert result.name == "John"
```

```python
# Fake - In-memory implementation
class FakeDatabase:
    def __init__(self):
        self.data = {}
    
    def save(self, key, value):
        self.data[key] = value
    
    def find(self, key):
        return self.data.get(key)

def test_user_persistence():
    fake_db = FakeDatabase()
    repo = UserRepository(db=fake_db)
    
    repo.save(User(id=1, name="Test"))
    
    assert repo.find(1).name == "Test"
```

## Test Data Management

### Fixture Patterns
```python
# Pytest fixtures for reusable test data
import pytest

@pytest.fixture
def sample_user():
    return User(id=1, email="test@example.com", name="Test User")

@pytest.fixture
def authenticated_client(sample_user):
    client = TestClient()
    client.login(sample_user)
    return client

def test_user_profile(authenticated_client, sample_user):
    response = authenticated_client.get("/profile")
    assert response.json["email"] == sample_user.email
```

### Factory Pattern
```python
# Generate test data dynamically
class UserFactory:
    @staticmethod
    def create(**overrides):
        defaults = {
            "id": uuid4(),
            "email": f"user-{uuid4()}@test.com",
            "name": "Test User",
            "active": True
        }
        return User(**{**defaults, **overrides})

def test_inactive_users():
    inactive_user = UserFactory.create(active=False)
    assert not inactive_user.can_login()
```

### Builder Pattern
```python
# Fluent interface for complex test data
class OrderBuilder:
    def __init__(self):
        self.order = Order()
    
    def with_item(self, name, price):
        self.order.items.append(Item(name, price))
        return self
    
    def with_discount(self, percent):
        self.order.discount = percent
        return self
    
    def build(self):
        return self.order

def test_order_total():
    order = (OrderBuilder()
        .with_item("Widget", 100)
        .with_item("Gadget", 50)
        .with_discount(10)
        .build())
    
    assert order.total == 135  # (100 + 50) * 0.9
```

## Common Testing Anti-Patterns

| Anti-Pattern | Symptoms | Solution |
|--------------|----------|----------|
| **The Giant** | Test with 100+ lines | Split into focused tests |
| **The Mockery** | Mock everything | Only mock external deps |
| **The Sleeper** | Uses sleep() for timing | Use proper async waiting |
| **The Inspector** | Tests implementation details | Test behavior, not internals |
| **The Flickering** | Randomly passes/fails | Fix race conditions, isolate state |
| **The Secret Catcher** | Catches all exceptions | Assert specific exceptions |
| **The Slow Poke** | Takes minutes to run | Optimize or move to integration |
| **The Dodger** | Skipped and ignored | Fix or remove dead tests |

## Test Coverage Guidelines

### Coverage Types
```
Line Coverage:    Which lines executed?
Branch Coverage:  Which branches taken?
Path Coverage:    Which execution paths?
Mutation Testing: Are assertions meaningful?
```

### Coverage Targets
```
Critical Business Logic:  90%+
Core Services:            80%+
Utilities/Helpers:        70%+
UI Components:            60%+
Generated Code:           0% (exclude from coverage)
```

### Coverage Commands
```bash
# Python coverage
pytest --cov=src --cov-report=html
coverage run -m pytest && coverage report

# JavaScript/TypeScript
npm test -- --coverage
npx jest --collectCoverageFrom='src/**/*.ts'

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## CI/CD Integration

### Test Pipeline Structure
```yaml
# Example GitHub Actions workflow
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run unit tests
        run: npm run test:unit
      
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:15
    steps:
      - uses: actions/checkout@v4
      - name: Run integration tests
        run: npm run test:integration
        
  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4
      - name: Run E2E tests
        run: npm run test:e2e
```

### Parallel Test Execution
```bash
# Python - pytest-xdist
pytest -n auto  # Auto-detect CPU count

# JavaScript - Jest
jest --maxWorkers=4

# Go
go test -parallel 4 ./...
```

## Test-Driven Development (TDD)

### Red-Green-Refactor Cycle
```
┌─────────────────────────────────────────┐
│  1. RED: Write a failing test           │
├─────────────────────────────────────────┤
│  2. GREEN: Write minimal code to pass   │
├─────────────────────────────────────────┤
│  3. REFACTOR: Clean up without breaking │
└─────────────────────────────────────────┘
        ↑                                  │
        └──────────────────────────────────┘
```

### TDD Example
```python
# Step 1: RED - Write failing test
def test_email_validation():
    validator = EmailValidator()
    assert validator.is_valid("user@example.com") == True
    assert validator.is_valid("invalid") == False

# Step 2: GREEN - Make it pass (minimal)
class EmailValidator:
    def is_valid(self, email):
        return "@" in email

# Step 3: REFACTOR - Improve
import re
class EmailValidator:
    EMAIL_PATTERN = re.compile(r"^[^@]+@[^@]+\.[^@]+$")
    
    def is_valid(self, email):
        return bool(self.EMAIL_PATTERN.match(email))
```

## When to Use This Skill

**Trigger Phrases:**
- "How should I test..."
- "What's the best way to mock..."
- "My tests are flaky..."
- "How do I increase coverage..."
- "Write tests for..."
- "Help me set up testing..."
- "This test keeps failing..."
- "Should I use unit or integration tests for..."

**Example Requests:**
1. "How should I test this async function?"
2. "My tests are taking 10 minutes, help me speed them up"
3. "How do I mock this external API?"
4. "Help me set up pytest for this project"
5. "Write unit tests for this class"
6. "How do I test error handling?"

## Test Review Checklist

Before shipping code with tests:

- [ ] **Coverage adequate?** Critical paths covered?
- [ ] **Tests isolated?** No shared state between tests?
- [ ] **Fast enough?** Unit tests under 100ms each?
- [ ] **Clear intent?** Test name describes behavior?
- [ ] **No flakiness?** Runs reliably 100 times?
- [ ] **Proper assertions?** Testing the right things?
- [ ] **Edge cases covered?** Null, empty, boundaries?
- [ ] **Error cases tested?** Exception handling verified?

## Framework Quick Reference

### Python (pytest)
```bash
pip install pytest pytest-cov pytest-mock
pytest -v --tb=short
pytest --cov=src -x  # Stop on first failure
```

### JavaScript (Jest)
```bash
npm install --save-dev jest
npx jest --watch  # Watch mode
npx jest --coverage
```

### TypeScript (Vitest)
```bash
npm install --save-dev vitest
npx vitest run
npx vitest --coverage
```

### Go
```bash
go test ./...
go test -v -race ./...  # With race detection
go test -cover ./...
```

## Integration with Other Skills

- **Architect**: Test strategy follows architecture
- **Code Review**: Test coverage in review process
- **Performance**: Load testing and benchmarks
- **Debugging**: Test failures guide debugging

---

*Skill designed for Thanos + Antigravity integration*
