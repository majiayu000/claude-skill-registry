---
name: testing-strategy
description: Comprehensive testing guidance covering test planning, TDD workflow, testing pyramid, and coverage targets. Ensures confidence through layered testing.
---

# Testing Strategy Skill

## Core Principle

**Confidence through layered testing.**

Tests are not just about catching bugs - they enable confident refactoring, document expected behavior, and provide fast feedback during development. A good testing strategy balances thoroughness with maintainability, using the right test type for each validation need.

**Effective testing:**
- Catches bugs before production
- Enables safe refactoring
- Documents system behavior
- Provides fast feedback loops
- Scales with codebase growth

---

## Testing Pyramid

**The testing pyramid guides test distribution across layers:**

```
        /\
       /  \      E2E (10%)
      /----\     - Full system tests
     /      \    - Slow, brittle, expensive
    /--------\   - Critical user journeys only
   /          \
  /------------\  Integration (20%)
 /              \ - Component interactions
/----------------\- Database, API, services
\----------------/- Medium speed, moderate cost
 \--------------/
  \------------/   Unit (70%)
   \----------/    - Individual functions
    \--------/     - Fast, reliable, cheap
     \------/      - Maximum coverage here
      \----/
       \__/
```

### Unit Tests (70% of tests)

**Purpose:** Validate individual functions/methods in isolation

**Characteristics:**
- Fast (milliseconds per test)
- No external dependencies (databases, APIs, file system)
- Isolated (each test independent)
- Deterministic (same input = same output)

**What to test:**
- Pure functions (input → output)
- Business logic
- Edge cases and boundary conditions
- Error handling
- Data transformations

**Example (Python):**
```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return round(price * (1 - discount_percent / 100), 2)

# Unit tests
def test_calculate_discount_normal_case():
    assert calculate_discount(100.0, 10.0) == 90.0

def test_calculate_discount_zero_discount():
    assert calculate_discount(100.0, 0.0) == 100.0

def test_calculate_discount_full_discount():
    assert calculate_discount(100.0, 100.0) == 0.0

def test_calculate_discount_rounding():
    assert calculate_discount(99.99, 10.0) == 89.99

def test_calculate_discount_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_discount(-10.0, 10.0)

def test_calculate_discount_invalid_percent():
    with pytest.raises(ValueError, match="Discount must be between"):
        calculate_discount(100.0, 150.0)
```

### Integration Tests (20% of tests)

**Purpose:** Validate interactions between components

**Characteristics:**
- Medium speed (seconds per test)
- Real dependencies (test database, external services)
- Test realistic scenarios
- More complex setup/teardown

**What to test:**
- Database queries and transactions
- API endpoint contracts
- Service-to-service communication
- Cache interactions
- File system operations

**Example (JavaScript):**
```javascript
describe('User API', () => {
  let db;

  beforeEach(async () => {
    // Setup test database
    db = await createTestDatabase();
    await db.migrate();
  });

  afterEach(async () => {
    await db.cleanup();
  });

  it('creates user and stores in database', async () => {
    const userData = {
      name: 'Jane Doe',
      email: 'jane@example.com',
      role: 'user'
    };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);

    // Verify API response
    expect(response.body).toMatchObject({
      id: expect.any(String),
      name: 'Jane Doe',
      email: 'jane@example.com',
      role: 'user'
    });

    // Verify database state
    const user = await db.users.findById(response.body.id);
    expect(user.email).toBe('jane@example.com');
  });

  it('rejects duplicate email addresses', async () => {
    await db.users.create({
      name: 'John Doe',
      email: 'jane@example.com'
    });

    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'Jane Doe',
        email: 'jane@example.com'
      })
      .expect(409);

    expect(response.body.error).toMatch(/email already exists/i);
  });
});
```

### End-to-End Tests (10% of tests)

**Purpose:** Validate complete user workflows through the system

**Characteristics:**
- Slow (minutes per test)
- Full system (UI, backend, database, external services)
- Brittle (breaks with UI changes)
- Expensive to maintain

**What to test:**
- Critical user journeys (signup, checkout, core workflows)
- Cross-cutting features (authentication, authorization)
- Integration with third-party services
- Browser compatibility (if web app)

**Example (Playwright):**
```javascript
test('user can complete checkout flow', async ({ page }) => {
  // Login
  await page.goto('/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Add item to cart
  await page.goto('/products');
  await page.click('text=Product Name');
  await page.click('button:has-text("Add to Cart")');

  // Proceed to checkout
  await page.click('text=Cart');
  await page.click('text=Checkout');

  // Fill shipping info
  await page.fill('input[name="address"]', '123 Main St');
  await page.fill('input[name="city"]', 'San Francisco');
  await page.fill('input[name="zip"]', '94102');

  // Fill payment info (test mode)
  await page.fill('input[name="cardNumber"]', '4242424242424242');
  await page.fill('input[name="expiry"]', '12/25');
  await page.fill('input[name="cvc"]', '123');

  // Submit order
  await page.click('button:has-text("Place Order")');

  // Verify confirmation
  await expect(page.locator('text=Order Confirmed')).toBeVisible();
  await expect(page.locator('text=Order #')).toBeVisible();
});
```

---

## Test-Driven Development (TDD)

**Red-Green-Refactor workflow:**

### 1. Red (Write Failing Test)

Write the test first, before implementation. Test should fail because functionality doesn't exist yet.

```python
# test_calculator.py
def test_add_two_numbers():
    calculator = Calculator()
    result = calculator.add(2, 3)
    assert result == 5  # FAILS - Calculator doesn't exist yet
```

### 2. Green (Make Test Pass)

Write minimal code to make the test pass. Don't worry about perfection yet.

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b  # PASSES - Simplest implementation
```

### 3. Refactor (Improve Code)

Clean up code while keeping tests passing. Tests give you confidence to refactor safely.

```python
# calculator.py (refactored)
class Calculator:
    """Simple calculator for arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Add two numbers and return the result."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Arguments must be numbers")
        return a + b
```

### TDD Benefits

- **Design first:** Writing tests forces you to think about API design
- **Documentation:** Tests document expected behavior
- **Confidence:** Tests enable safe refactoring
- **Coverage:** TDD naturally produces high test coverage
- **Bug prevention:** Catch bugs before they're written

### When to Use TDD

**Good fit:**
- Complex business logic
- Bug fixes (write failing test, then fix)
- API design (tests define the interface)
- Critical functionality (payment processing, security)

**Poor fit:**
- Spike/exploratory work (unknown requirements)
- Trivial code (getters/setters)
- UI experimentation (rapid iteration)
- Throwaway prototypes

---

## Test Structure (AAA Pattern)

**Arrange-Act-Assert pattern for clear, maintainable tests:**

### Arrange (Setup)
Prepare test data and system state

### Act (Execute)
Run the code being tested

### Assert (Verify)
Check the results match expectations

**Example:**
```python
def test_user_checkout_with_discount():
    # Arrange
    user = User(id=1, membership="premium")
    cart = ShoppingCart()
    cart.add_item(Product(id=101, price=100.0))
    cart.add_item(Product(id=102, price=50.0))
    checkout = CheckoutService(discount_calculator=PremiumDiscount())

    # Act
    total = checkout.calculate_total(user, cart)

    # Assert
    assert total == 135.0  # 150 - 10% premium discount
```

### Test Naming Convention

**Format:** `test_[unit]_[scenario]_[expected_result]`

**Good names:**
```python
test_calculate_discount_with_zero_percent_returns_original_price()
test_user_login_with_invalid_password_raises_authentication_error()
test_get_user_by_id_when_not_found_returns_none()
```

**Bad names:**
```python
test_discount()  # What about discount?
test_case_1()    # What is case 1?
test_user()      # What about user?
```

---

## Coverage Targets

**Coverage is a metric, not a goal. 100% coverage doesn't mean bug-free code.**

### Recommended Coverage by Component Type

| Component Type | Target Coverage | Rationale |
|----------------|----------------|-----------|
| **Business Logic** | 90-100% | Critical functionality, high bug cost |
| **API Endpoints** | 80-90% | Public contracts, integration points |
| **Data Models** | 70-80% | Validation and constraints |
| **Utilities** | 80-90% | Reused across codebase |
| **UI Components** | 60-70% | High churn, manual testing viable |
| **Configuration** | 50-60% | Simple, low complexity |

### Coverage Metrics

**Line coverage:** Percentage of code lines executed by tests
- Easy to measure, but can be gamed
- 80% line coverage is reasonable target

**Branch coverage:** Percentage of code paths executed
- Better than line coverage (catches untested conditions)
- 70% branch coverage is good target

**Mutation coverage:** Tests that fail when code is mutated
- Most rigorous, catches weak assertions
- Advanced metric, use for critical code

### What NOT to Test

**Avoid testing:**
- Third-party library internals (trust the library)
- Framework code (already tested)
- Trivial getters/setters (no logic to test)
- Private implementation details (test public interface)
- Generated code (already validated by generator)

---

## Mocking and Fixtures

### When to Mock

**Mock external dependencies:**
- Database connections
- API calls to external services
- File system operations
- Current time (for time-dependent logic)
- Random number generation

**Don't mock:**
- Your own domain logic (test it directly)
- Simple data structures
- Pure functions (no side effects to mock)

### Mocking Example (Python)

```python
import pytest
from unittest.mock import Mock, patch

def test_send_welcome_email_calls_email_service():
    # Arrange
    email_service = Mock()
    user_service = UserService(email_service=email_service)
    user = User(email='jane@example.com', name='Jane')

    # Act
    user_service.send_welcome_email(user)

    # Assert
    email_service.send.assert_called_once_with(
        to='jane@example.com',
        subject='Welcome!',
        body='Hi Jane, welcome to our service!'
    )

@patch('user_service.datetime')
def test_user_age_calculation(mock_datetime):
    # Arrange - Fix current time
    mock_datetime.now.return_value = datetime(2024, 1, 1)
    user = User(birth_date=datetime(2000, 1, 1))

    # Act
    age = user.calculate_age()

    # Assert
    assert age == 24
```

### Fixtures (Test Data Setup)

**Pytest fixtures:**
```python
import pytest

@pytest.fixture
def sample_user():
    """Reusable user instance for tests."""
    return User(
        id=1,
        name='Jane Doe',
        email='jane@example.com',
        role='user'
    )

@pytest.fixture
def db_session():
    """Database session with rollback."""
    session = database.create_session()
    yield session
    session.rollback()
    session.close()

def test_update_user_email(sample_user, db_session):
    # Arrange
    db_session.add(sample_user)

    # Act
    sample_user.update_email('newemail@example.com')
    db_session.commit()

    # Assert
    updated = db_session.query(User).get(1)
    assert updated.email == 'newemail@example.com'
```

**Jest setup/teardown:**
```javascript
describe('User Service', () => {
  let db;
  let userService;

  beforeAll(async () => {
    // Setup once for all tests
    db = await createTestDatabase();
  });

  afterAll(async () => {
    // Cleanup once after all tests
    await db.close();
  });

  beforeEach(() => {
    // Setup before each test
    userService = new UserService(db);
  });

  afterEach(async () => {
    // Cleanup after each test
    await db.clearAllTables();
  });

  test('creates user successfully', async () => {
    const user = await userService.create({
      name: 'Jane Doe',
      email: 'jane@example.com'
    });

    expect(user.id).toBeDefined();
  });
});
```

---

## Language/Framework Specifics

### Python (pytest)

**Installation:**
```bash
pip install pytest pytest-cov
```

**Running tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_user.py

# Run specific test
pytest tests/test_user.py::test_create_user

# Run with verbose output
pytest -v

# Run with debugging (stop on failure)
pytest -x --pdb
```

**Configuration (pytest.ini):**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --strict-markers --cov=src --cov-report=term-missing
```

**Key features:**
- Parametrized tests
- Fixtures for setup/teardown
- Markers for test categories
- Coverage reporting

**Example:**
```python
import pytest

@pytest.mark.parametrize("price,discount,expected", [
    (100.0, 10.0, 90.0),
    (100.0, 0.0, 100.0),
    (100.0, 100.0, 0.0),
    (99.99, 10.0, 89.99),
])
def test_calculate_discount(price, discount, expected):
    result = calculate_discount(price, discount)
    assert result == expected
```

### JavaScript/TypeScript (Jest)

**Installation:**
```bash
npm install --save-dev jest @types/jest
```

**Running tests:**
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test user.test.js

# Run in watch mode
npm test -- --watch

# Run with verbose output
npm test -- --verbose
```

**Configuration (jest.config.js):**
```javascript
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,ts}',
    '!src/**/*.d.ts',
  ],
  coverageThresholds: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

**Key features:**
- Snapshot testing
- Mocking built-in
- Parallel test execution
- Code coverage reporting

**Example:**
```javascript
describe('calculateDiscount', () => {
  it.each([
    [100.0, 10.0, 90.0],
    [100.0, 0.0, 100.0],
    [100.0, 100.0, 0.0],
    [99.99, 10.0, 89.99],
  ])('calculates %d with %d%% discount as %d', (price, discount, expected) => {
    expect(calculateDiscount(price, discount)).toBe(expected);
  });

  it('throws error for negative price', () => {
    expect(() => calculateDiscount(-10, 10)).toThrow('Price cannot be negative');
  });
});
```

### Rust (cargo test)

**Running tests:**
```bash
# Run all tests
cargo test

# Run with output visible
cargo test -- --nocapture

# Run specific test
cargo test test_calculate_discount

# Run with coverage (requires tarpaulin)
cargo tarpaulin --out Html
```

**Key features:**
- Tests in same file as code
- Documentation tests
- Integration tests in tests/ directory
- Built-in benchmarking

**Example:**
```rust
pub fn calculate_discount(price: f64, discount_percent: f64) -> Result<f64, String> {
    if price < 0.0 {
        return Err("Price cannot be negative".to_string());
    }
    if !(0.0..=100.0).contains(&discount_percent) {
        return Err("Discount must be between 0 and 100".to_string());
    }
    Ok((price * (1.0 - discount_percent / 100.0) * 100.0).round() / 100.0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calculate_discount_normal_case() {
        assert_eq!(calculate_discount(100.0, 10.0).unwrap(), 90.0);
    }

    #[test]
    fn test_calculate_discount_negative_price() {
        assert!(calculate_discount(-10.0, 10.0).is_err());
    }

    #[test]
    #[should_panic(expected = "Discount must be between")]
    fn test_calculate_discount_invalid_percent() {
        calculate_discount(100.0, 150.0).unwrap();
    }
}
```

---

## Integration with CI/CD

**Automated testing in continuous integration:**

### GitHub Actions Example

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml

    - name: Check coverage threshold
      run: |
        pytest --cov=src --cov-fail-under=80
```

### Pre-commit Hooks

**Run tests before allowing commits:**

```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running tests..."
npm test

if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi

echo "Tests passed. Proceeding with commit."
```

### Pull Request Requirements

**Enforce testing in PR reviews:**
- All tests must pass before merge
- Coverage must not decrease
- New code must have tests
- Integration tests for new features

---

## Quality Checklist

**Before considering testing complete:**

### Test Coverage
- [ ] Business logic has 90%+ coverage
- [ ] API endpoints have integration tests
- [ ] Edge cases are tested (zero, negative, null, empty)
- [ ] Error conditions are tested
- [ ] Happy path and sad path both covered

### Test Quality
- [ ] Tests follow AAA pattern (Arrange-Act-Assert)
- [ ] Test names describe scenario and expected result
- [ ] Tests are independent (order doesn't matter)
- [ ] Tests use appropriate assertions (specific, not generic)
- [ ] Mocks are used appropriately (external deps only)

### Test Maintainability
- [ ] No code duplication (use fixtures/helpers)
- [ ] Tests are fast (unit tests < 100ms each)
- [ ] Tests are deterministic (no flaky tests)
- [ ] Test data is realistic but minimal
- [ ] Tests don't test implementation details

### Integration with Workflow
- [ ] Tests run in CI/CD pipeline
- [ ] Coverage reported and tracked
- [ ] Tests run before commits (pre-commit hook)
- [ ] Failing tests block merge
- [ ] Coverage thresholds enforced

---

## Anti-Patterns

### What NOT to Do

**DON'T write tests that test the framework:**
```python
# Bad - testing pytest itself
def test_assert_works():
    assert 1 == 1
```

**DON'T test implementation details:**
```python
# Bad - tests internal private method
def test_internal_validation():
    user_service = UserService()
    assert user_service._validate_email('test@example.com') == True

# Good - tests public behavior
def test_create_user_with_invalid_email():
    user_service = UserService()
    with pytest.raises(ValidationError):
        user_service.create_user(email='invalid')
```

**DON'T have tests that depend on each other:**
```python
# Bad - test order matters
def test_create_user():
    global created_user
    created_user = create_user('Jane')
    assert created_user.name == 'Jane'

def test_update_user():
    created_user.name = 'John'  # Depends on previous test!
    assert created_user.name == 'John'

# Good - each test independent
def test_create_user():
    user = create_user('Jane')
    assert user.name == 'Jane'

def test_update_user():
    user = create_user('Jane')  # Setup within test
    user.name = 'John'
    assert user.name == 'John'
```

**DON'T ignore flaky tests:**
```python
# Bad - flaky test that sometimes passes
def test_async_operation():
    start_async_job()
    time.sleep(1)  # Hope it finishes in 1 second
    assert job_completed()

# Good - deterministic test
def test_async_operation():
    start_async_job()
    wait_for_condition(lambda: job_completed(), timeout=5)
    assert job_completed()
```

**DON'T have tests that are slower than necessary:**
```python
# Bad - integration test for pure function
def test_calculate_total():
    db = create_database_connection()
    result = calculate_total(100, 0.1)  # Doesn't need DB!
    assert result == 110

# Good - unit test with no dependencies
def test_calculate_total():
    result = calculate_total(100, 0.1)
    assert result == 110
```

**DON'T use generic assertions:**
```python
# Bad - generic assertion, unhelpful failure message
def test_user_creation():
    user = create_user('Jane', 'jane@example.com')
    assert user  # What exactly failed if this breaks?

# Good - specific assertions
def test_user_creation():
    user = create_user('Jane', 'jane@example.com')
    assert user.name == 'Jane'
    assert user.email == 'jane@example.com'
    assert user.id is not None
```

---

## Integration with Backlog Workflow

**Testing integrates with task execution:**

### During Task Planning
- Include test requirements in acceptance criteria
- Example: "Feature X implemented with 80%+ test coverage"

### During Task Execution
- Write tests alongside code (TDD or test-as-you-go)
- Run tests frequently during development
- Commit tests with implementation code

### During Code Review
- Review test quality (see code-review skill)
- Verify coverage for new code
- Check test names and structure
- Ensure tests actually test the right things

### Task Completion
- All tests passing is part of "done"
- Coverage meets project standards
- No skipped/disabled tests without justification

**Example acceptance criteria:**

```
Task: Implement user authentication

Acceptance Criteria:
- [ ] Login endpoint returns JWT on success
- [ ] Login endpoint returns 401 for invalid credentials
- [ ] JWT contains user ID and role
- [ ] Tests:
  - [ ] Unit tests for token generation (90%+ coverage)
  - [ ] Integration tests for login endpoint
  - [ ] E2E test for login flow
  - [ ] Test coverage overall 80%+
- [ ] All tests passing in CI
```

---

**Remember:** Tests are an investment in quality and confidence. Good tests enable rapid development by catching bugs early and enabling safe refactoring. Follow the testing pyramid, write clear tests using AAA pattern, and integrate testing into your development workflow from day one.
