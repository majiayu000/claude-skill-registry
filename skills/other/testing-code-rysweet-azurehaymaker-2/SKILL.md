---
name: "Testing Code"
description: "Generates and improves tests following TDD principles. Activates when new features are implemented, test coverage is low, or user requests tests. Ensures comprehensive test coverage with unit, integration, and edge case tests."
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash"]
---

# Testing Code

You are activating test generation and improvement capabilities. Your role is to ensure code has comprehensive, maintainable test coverage.

## When to Activate

This skill activates when:

- New features or functions are implemented
- User requests tests ("add tests", "test this")
- Test coverage is low or missing
- Bugs are found (need regression tests)
- Refactoring code (need confidence tests pass)
- Before creating pull requests

## Testing Philosophy

### Why Test?

- **Confidence**: Know code works as expected
- **Regression Prevention**: Catch bugs from changes
- **Documentation**: Tests show how code should be used
- **Design Feedback**: Hard to test = bad design
- **Refactoring Safety**: Change with confidence

### Test Pyramid

```
        /\
       /  \    E2E Tests (Few)
      /    \   - Test full workflows
     /------\
    /        \ Integration Tests (Some)
   /          \- Test module interactions
  /------------\
 /              \ Unit Tests (Many)
/______________/ - Test individual functions
```

## Testing Process

### 1. Analyze Code

Understand what to test:

- What is the purpose?
- What are the inputs and outputs?
- What are the edge cases?
- What are the error conditions?
- What are the side effects?

### 2. Identify Test Cases

#### Happy Path

- Normal, expected usage
- Valid inputs producing valid outputs

#### Edge Cases

- Boundary values (0, -1, max, empty)
- Unusual but valid inputs
- Minimum and maximum values

#### Error Cases

- Invalid inputs
- Null/undefined/None
- Wrong types
- Violations of constraints

#### Integration Points

- External API calls
- Database interactions
- File system operations
- Other modules/classes

### 3. Write Tests

Follow this structure:

```python
def test_function_name_condition_expected():
    """
    Test that function_name handles condition and returns expected result.
    """
    # Arrange: Set up test data and conditions
    input_data = ...
    expected_output = ...

    # Act: Execute the code under test
    result = function_name(input_data)

    # Assert: Verify the result
    assert result == expected_output
```

### 4. Check Coverage

Ensure comprehensive coverage:

- All code paths executed
- All branches tested
- All error conditions tested
- Edge cases covered

## Test Patterns

### Unit Tests

Test individual functions in isolation.

**Python Example**:

```python
import pytest
from mymodule import calculate_total

def test_calculate_total_with_valid_items():
    """Calculate total for valid items."""
    items = [
        {"price": 10.00, "quantity": 2},
        {"price": 5.00, "quantity": 3},
    ]
    assert calculate_total(items) == 35.00

def test_calculate_total_with_empty_list():
    """Calculate total returns 0 for empty list."""
    assert calculate_total([]) == 0.00

def test_calculate_total_with_zero_quantity():
    """Calculate total handles zero quantity."""
    items = [{"price": 10.00, "quantity": 0}]
    assert calculate_total(items) == 0.00

def test_calculate_total_raises_on_negative_price():
    """Calculate total raises ValueError for negative price."""
    items = [{"price": -10.00, "quantity": 1}]
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_total(items)
```

**JavaScript Example**:

```javascript
import { describe, it, expect } from "vitest";
import { calculateTotal } from "./cart";

describe("calculateTotal", () => {
  it("calculates total for valid items", () => {
    const items = [
      { price: 10.0, quantity: 2 },
      { price: 5.0, quantity: 3 },
    ];
    expect(calculateTotal(items)).toBe(35.0);
  });

  it("returns 0 for empty list", () => {
    expect(calculateTotal([])).toBe(0);
  });

  it("handles zero quantity", () => {
    const items = [{ price: 10.0, quantity: 0 }];
    expect(calculateTotal(items)).toBe(0);
  });

  it("throws error for negative price", () => {
    const items = [{ price: -10.0, quantity: 1 }];
    expect(() => calculateTotal(items)).toThrow("Price cannot be negative");
  });
});
```

### Integration Tests

Test multiple components working together.

**Example**:

```python
def test_user_registration_flow():
    """Test complete user registration workflow."""
    # Arrange: Set up test database
    db = setup_test_database()
    api = UserAPI(db)

    # Act: Register user
    response = api.register({
        "email": "test@example.com",
        "password": "SecurePass123!",
    })

    # Assert: User created and email sent
    assert response.status == 201
    assert db.users.find_by_email("test@example.com") is not None
    assert email_was_sent("test@example.com", "Welcome")
```

### Mocking & Stubbing

Isolate code from external dependencies.

**Python Example**:

```python
from unittest.mock import Mock, patch

def test_send_notification_calls_email_service():
    """Test that send_notification calls email service correctly."""
    # Arrange: Mock email service
    mock_email = Mock()

    # Act: Send notification
    with patch('mymodule.email_service', mock_email):
        send_notification("user@example.com", "Hello")

    # Assert: Email service called with correct args
    mock_email.send.assert_called_once_with(
        to="user@example.com",
        subject="Notification",
        body="Hello"
    )
```

### Parameterized Tests

Test multiple inputs efficiently.

**Python Example**:

```python
@pytest.mark.parametrize("input,expected", [
    (0, "zero"),
    (1, "one"),
    (2, "two"),
    (10, "many"),
    (-5, "negative"),
])
def test_number_to_word(input, expected):
    """Test number_to_word for various inputs."""
    assert number_to_word(input) == expected
```

### Property-Based Tests

Generate test cases automatically.

**Python Example**:

```python
from hypothesis import given
from hypothesis.strategies import integers

@given(integers())
def test_double_is_reversible(x):
    """Test that doubling and halving returns original value."""
    assert half(double(x)) == x
```

## Test Organization

### Directory Structure

```
project/
├── src/
│   └── mymodule/
│       ├── __init__.py
│       ├── calculator.py
│       └── user.py
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── test_calculator.py
    │   └── test_user.py
    ├── integration/
    │   └── test_user_flow.py
    └── conftest.py  # Shared fixtures
```

### Naming Conventions

- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_<function>_<condition>_<expected>`
- Test classes: `Test<ClassName>`

**Good Names**:

- `test_calculate_total_with_empty_list_returns_zero`
- `test_user_login_with_invalid_password_raises_error`
- `test_api_returns_404_for_nonexistent_resource`

**Bad Names**:

- `test_calc` (too vague)
- `test_1` (no meaning)
- `test_it_works` (what works?)

## Testing Checklist

For each function/class, ensure tests for:

### Functionality

- [ ] Happy path (normal usage)
- [ ] Return values correct
- [ ] Side effects occur as expected

### Edge Cases

- [ ] Empty inputs ([], "", 0, None)
- [ ] Boundary values (min, max, -1)
- [ ] Large inputs
- [ ] Special characters/values

### Error Handling

- [ ] Invalid inputs
- [ ] Null/undefined/None
- [ ] Wrong types
- [ ] Constraint violations
- [ ] External failures (API down, etc.)

### Integration

- [ ] Calls to other functions/modules
- [ ] Database interactions
- [ ] File operations
- [ ] Network requests

## Test Quality Standards

### Good Tests Are:

**Fast**:

- Run in milliseconds
- No unnecessary I/O
- Use mocks for external dependencies

**Independent**:

- No shared state between tests
- Can run in any order
- Don't depend on other tests

**Repeatable**:

- Same result every time
- No flaky tests
- No dependency on external state

**Self-Validating**:

- Pass or fail clearly
- No manual inspection
- Descriptive failure messages

**Timely**:

- Written before or with code (TDD)
- Not as an afterthought
- Updated when code changes

### Anti-Patterns to Avoid

**Testing Implementation Details**:

```python
# Bad: Tests internal state
def test_cache_uses_dict():
    cache = Cache()
    assert isinstance(cache._storage, dict)

# Good: Tests behavior
def test_cache_stores_and_retrieves_value():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

**Overly Complex Tests**:

```python
# Bad: Test is hard to understand
def test_complex():
    data = [process(x) for x in range(100) if x % 2]
    result = calculate(data)
    assert result == sum(data) / len(data)

# Good: Clear and simple
def test_calculate_returns_average():
    data = [2, 4, 6]
    assert calculate(data) == 4.0
```

**Not Testing Edge Cases**:

```python
# Incomplete: Only tests happy path
def test_divide():
    assert divide(10, 2) == 5

# Complete: Tests edge cases too
def test_divide_with_valid_numbers():
    assert divide(10, 2) == 5

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_with_negative_numbers():
    assert divide(-10, 2) == -5
```

## Coverage Targets

### Minimum Coverage

- **Critical paths**: 100%
- **Business logic**: 95%+
- **Utilities**: 90%+
- **UI code**: 70%+

### Focus Areas

1. Business-critical features
2. Complex algorithms
3. Error handling
4. Security-sensitive code
5. Bug-prone areas

### Don't Obsess Over 100%

- Some code is hard to test (UI rendering, etc.)
- Focus on meaningful coverage
- Quality > quantity

## Integration Points

### Invokes

- **Tester Agent**: Core testing logic from `.claude/agents/tester.md`
- **Code Analysis**: To identify untested code
- **Coverage Tools**: pytest-cov, coverage.py, jest --coverage

### Escalates To

- **Builder Agent**: To fix code that's hard to test
- **Reviewer Agent**: To review test quality

### References

- **Testing Guides**: Language-specific best practices
- **Test Patterns**: Common testing patterns
- **Fixtures**: Shared test data and setup

## Example Workflow

````
User: "I just implemented this authentication function. Can you add tests?"

Testing Code Skill:

Let me analyze the authentication function and create comprehensive tests.

## Function Analysis

The `authenticate(username, password)` function:
- Returns JWT token on success
- Raises `InvalidCredentialsError` on bad password
- Raises `UserNotFoundError` if user doesn't exist
- Hashes password before comparison
- Logs failed attempts

## Test Plan

I'll create tests for:
1. Successful authentication (happy path)
2. Invalid password (error case)
3. Non-existent user (error case)
4. Empty username/password (edge case)
5. SQL injection attempt (security)
6. Logging of failed attempts (side effect)

## Generated Tests

```python
import pytest
from unittest.mock import Mock, patch
from myapp.auth import authenticate, InvalidCredentialsError, UserNotFoundError

class TestAuthenticate:
    """Tests for authenticate function."""

    def test_successful_authentication_returns_jwt_token(self, mock_db):
        """Authenticate returns valid JWT for correct credentials."""
        # Arrange
        mock_db.get_user.return_value = User(
            username="alice",
            password_hash="$2b$12$..."
        )

        # Act
        token = authenticate("alice", "correct_password")

        # Assert
        assert token is not None
        assert jwt.decode(token)["username"] == "alice"

    def test_invalid_password_raises_error(self, mock_db):
        """Authenticate raises InvalidCredentialsError for wrong password."""
        mock_db.get_user.return_value = User(
            username="alice",
            password_hash="$2b$12$..."
        )

        with pytest.raises(InvalidCredentialsError):
            authenticate("alice", "wrong_password")

    def test_nonexistent_user_raises_error(self, mock_db):
        """Authenticate raises UserNotFoundError for unknown user."""
        mock_db.get_user.return_value = None

        with pytest.raises(UserNotFoundError):
            authenticate("nobody", "password")

    def test_empty_username_raises_error(self):
        """Authenticate raises ValueError for empty username."""
        with pytest.raises(ValueError, match="Username cannot be empty"):
            authenticate("", "password")

    def test_logs_failed_authentication_attempts(self, mock_db, mock_logger):
        """Failed authentication attempts are logged."""
        mock_db.get_user.return_value = User(username="alice", ...)

        try:
            authenticate("alice", "wrong_password")
        except InvalidCredentialsError:
            pass

        mock_logger.warning.assert_called_with(
            "Failed login attempt for user: alice"
        )

@pytest.fixture
def mock_db():
    """Mock database for tests."""
    return Mock()

@pytest.fixture
def mock_logger():
    """Mock logger for tests."""
    with patch('myapp.auth.logger') as mock:
        yield mock
````

## Coverage Report

Running tests:

```bash
pytest tests/test_auth.py --cov=myapp.auth --cov-report=term-missing
```

Current coverage: 95% (missing: edge case for special characters)

## Suggestions

Consider adding:

1. Test for rate limiting (if implemented)
2. Test for account lockout after X failures
3. Performance test for password hashing time

Ready to implement these tests?

```

## Success Criteria

Good test suite:
- All critical paths covered
- Edge cases tested
- Tests are fast (<1s per file)
- Tests are independent
- Clear test names
- Failures are descriptive
- Easy to add new tests

## Related Capabilities

- **Agent**: Tester agent (this skill invokes it)
- **Skill**: "Reviewing Code" for test quality review
- **Skill**: "Debugging Issues" when tests fail
- **Documentation**: Language-specific testing guides

---

Remember: Tests are documentation that proves your code works. Write tests you'll thank yourself for later.
```
