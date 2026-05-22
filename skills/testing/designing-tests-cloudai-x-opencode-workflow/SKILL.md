---
name: designing-tests
description: Guides test strategy, TDD/BDD approaches, test coverage planning, and testing best practices. Use when designing test suites, improving coverage, or choosing testing approaches.
license: MIT
compatibility: opencode
metadata:
  category: quality
  audience: developers
---

# Designing Tests

Strategies and patterns for designing effective, maintainable test suites.

## When to Use This Skill

- Planning test coverage for new features
- Choosing between testing approaches (TDD, BDD)
- Designing integration or E2E tests
- Improving existing test suites
- Setting up testing infrastructure
- Debugging flaky tests

---

## The Testing Pyramid

```
                 ┌─────────┐
                 │   E2E   │  ← Few, slow, expensive
                 │  Tests  │     (Selenium, Playwright)
                 ├─────────┤
                 │         │
              ┌──┤ Integr- │  ← Some, medium speed
              │  │  ation  │     (API tests, DB tests)
              │  │  Tests  │
              │  ├─────────┤
              │  │         │
              │  │  Unit   │  ← Many, fast, cheap
              │  │  Tests  │     (Pure functions, isolated)
              └──┴─────────┘
```

| Level | Speed | Scope | Quantity | Purpose |
|-------|-------|-------|----------|---------|
| Unit | ~ms | Single function/class | Many (70-80%) | Logic correctness |
| Integration | ~s | Multiple components | Some (15-20%) | Component interaction |
| E2E | ~10s+ | Full system | Few (5-10%) | User flows work |

---

## Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

```
     ┌─────────────────────────────────┐
     │                                 │
     ▼                                 │
┌─────────┐    ┌─────────┐    ┌────────┴──┐
│   RED   │───▶│  GREEN  │───▶│ REFACTOR  │
│  Write  │    │  Make   │    │  Clean    │
│ failing │    │   it    │    │   up      │
│  test   │    │  pass   │    │  code     │
└─────────┘    └─────────┘    └───────────┘
```

### TDD Best Practices

1. **Write the test first** - Don't write production code without a failing test
2. **Write the minimal test** - One behavior per test
3. **Write the minimal code** - Just enough to pass
4. **Refactor ruthlessly** - Clean up after green
5. **Run tests frequently** - After every small change

### TDD Example Flow

```python
# Step 1: RED - Write failing test
def test_calculate_total_with_discount():
    order = Order(items=[Item(price=100)])
    order.apply_discount(10)  # 10%
    assert order.total() == 90

# Step 2: GREEN - Minimal implementation
class Order:
    def __init__(self, items):
        self.items = items
        self.discount = 0

    def apply_discount(self, percent):
        self.discount = percent

    def total(self):
        subtotal = sum(i.price for i in self.items)
        return subtotal * (100 - self.discount) / 100

# Step 3: REFACTOR - Clean up (if needed)
```

---

## Behavior-Driven Development (BDD)

### Gherkin Syntax

```gherkin
Feature: Shopping Cart
  As a customer
  I want to add items to my cart
  So that I can purchase them later

  Scenario: Add item to empty cart
    Given I have an empty cart
    When I add a product "Widget" priced at $10
    Then my cart should contain 1 item
    And my cart total should be $10

  Scenario: Apply discount code
    Given I have a cart with total $100
    When I apply discount code "SAVE10"
    Then my cart total should be $90
```

### BDD Benefits

- Tests as documentation
- Shared language with stakeholders
- Focus on behavior, not implementation
- Easy to understand test intent

---

## Test Design Patterns

### Arrange-Act-Assert (AAA)

```python
def test_user_registration():
    # Arrange - Set up preconditions
    user_data = {"email": "test@example.com", "password": "secure123"}
    user_service = UserService(mock_repository)

    # Act - Perform the action
    result = user_service.register(user_data)

    # Assert - Verify the outcome
    assert result.success is True
    assert result.user.email == "test@example.com"
```

### Given-When-Then (BDD style)

```python
def test_order_cancellation():
    # Given - a confirmed order
    order = create_confirmed_order()

    # When - the customer cancels it
    order.cancel()

    # Then - the order is cancelled and refund initiated
    assert order.status == "cancelled"
    assert order.refund_initiated is True
```

### Test Data Builders

```python
class UserBuilder:
    def __init__(self):
        self.email = "default@test.com"
        self.name = "Test User"
        self.role = "user"

    def with_email(self, email):
        self.email = email
        return self

    def with_role(self, role):
        self.role = role
        return self

    def build(self):
        return User(email=self.email, name=self.name, role=self.role)

# Usage
admin = UserBuilder().with_role("admin").build()
```

### Object Mother Pattern

```python
class TestUsers:
    @staticmethod
    def admin():
        return User(email="admin@test.com", role="admin")

    @staticmethod
    def customer():
        return User(email="customer@test.com", role="customer")

    @staticmethod
    def guest():
        return User(email=None, role="guest")
```

---

## Mocking Strategies

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Pure business logic |
| Database (for unit tests) | Simple value objects |
| File system | Deterministic functions |
| Time/random | Core domain entities |
| Third-party services | Internal collaborators (usually) |

### Mock Types

| Type | Purpose | Example |
|------|---------|---------|
| **Stub** | Return canned responses | `mock.return_value = 42` |
| **Mock** | Verify interactions | `mock.assert_called_with(...)` |
| **Spy** | Track real calls | Wraps real object, records calls |
| **Fake** | Simplified implementation | In-memory database |

### Mocking Example

```python
# Using unittest.mock
from unittest.mock import Mock, patch

def test_send_email_on_registration():
    # Arrange
    mock_email_service = Mock()
    user_service = UserService(email_service=mock_email_service)

    # Act
    user_service.register({"email": "test@example.com"})

    # Assert
    mock_email_service.send_welcome_email.assert_called_once_with("test@example.com")

# Using patch decorator
@patch("app.services.EmailService")
def test_with_patch(mock_email_class):
    mock_email_class.return_value.send.return_value = True
    # Test code...
```

---

## Integration Test Patterns

### Database Tests

```python
import pytest
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def database():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres.get_connection_url()

def test_user_persistence(database):
    repo = UserRepository(database)
    user = User(email="test@example.com")

    repo.save(user)
    retrieved = repo.find_by_email("test@example.com")

    assert retrieved.email == user.email
```

### API Tests

```python
def test_create_user_endpoint(client):
    response = client.post("/api/users", json={
        "email": "new@example.com",
        "password": "secure123"
    })

    assert response.status_code == 201
    assert response.json["email"] == "new@example.com"
    assert "id" in response.json
```

---

## E2E Test Patterns

### Page Object Model

```python
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.submit_button = page.locator("button[type=submit]")

    def login(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
        return DashboardPage(self.page)

# Usage
def test_successful_login(page):
    login_page = LoginPage(page)
    dashboard = login_page.login("user@example.com", "password")
    assert dashboard.welcome_message.is_visible()
```

### E2E Best Practices

1. **Use stable selectors** - data-testid, not CSS classes
2. **Wait for conditions** - Not arbitrary sleeps
3. **Isolate test data** - Each test gets fresh data
4. **Test critical paths** - Happy paths, key user journeys
5. **Keep them fast** - Parallelize, minimize scope

---

## Test Coverage Strategy

### What to Cover

| Priority | What | Why |
|----------|------|-----|
| High | Business logic | Core value |
| High | Edge cases | Where bugs hide |
| High | Error paths | Graceful failures |
| Medium | Integration points | Contract validation |
| Low | UI layout | Brittle, low value |
| Low | Third-party code | Not your responsibility |

### Coverage Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Line coverage | 70-80% | Basic minimum |
| Branch coverage | 60-70% | Catches conditionals |
| Mutation score | 50-70% | Measures test quality |

### Meaningful Coverage

```
HIGH VALUE:
  ✓ Core business logic
  ✓ Data transformations
  ✓ Error handling
  ✓ Security-sensitive code

LOW VALUE:
  ✗ Getters/setters
  ✗ Constructor-only classes
  ✗ Framework boilerplate
  ✗ Configuration files
```

---

## Handling Flaky Tests

### Common Causes

| Cause | Solution |
|-------|----------|
| Timing issues | Use explicit waits, not sleep |
| Shared state | Isolate test data |
| External dependencies | Mock or use containers |
| Race conditions | Add synchronization |
| Date/time | Mock time providers |
| Random data | Seed random generators |

### Flaky Test Checklist

- [ ] Is the test relying on timing?
- [ ] Is there shared state between tests?
- [ ] Is there an external dependency?
- [ ] Is the order of execution assumed?
- [ ] Is there non-deterministic data?

---

## Test Organization

### File Structure

```
tests/
├── unit/                    # Unit tests
│   ├── services/
│   │   └── test_user_service.py
│   └── models/
│       └── test_order.py
├── integration/             # Integration tests
│   ├── api/
│   │   └── test_user_endpoints.py
│   └── repositories/
│       └── test_user_repository.py
├── e2e/                     # End-to-end tests
│   └── test_checkout_flow.py
├── fixtures/                # Shared fixtures
│   └── factories.py
└── conftest.py              # Pytest configuration
```

### Naming Conventions

```python
# Pattern: test_[what]_[condition]_[expected]

def test_calculate_total_with_discount_returns_reduced_price():
    pass

def test_login_with_invalid_password_raises_auth_error():
    pass

def test_order_when_cancelled_sends_refund_notification():
    pass
```

---

## Anti-Patterns to Avoid

1. **Testing implementation, not behavior** - Tests break on refactor
2. **Large test methods** - Hard to debug, unclear intent
3. **Excessive mocking** - Tests don't reflect reality
4. **Shared mutable state** - Tests affect each other
5. **Ignoring test failures** - Broken windows effect
6. **Testing private methods** - Coupling to implementation
7. **No assertion** - Tests that can't fail
8. **Copy-paste tests** - Maintenance nightmare

---

## Quick Reference

```
PYRAMID:
  Unit (70%) → Integration (20%) → E2E (10%)

TDD CYCLE:
  Red → Green → Refactor

PATTERNS:
  AAA: Arrange-Act-Assert
  Builder: Fluent test data creation
  Page Object: E2E abstraction

MOCK WHEN:
  External APIs, Database (unit), Time, Random

COVERAGE:
  70-80% line, focus on business logic

NAMING:
  test_[what]_[condition]_[expected]
```
