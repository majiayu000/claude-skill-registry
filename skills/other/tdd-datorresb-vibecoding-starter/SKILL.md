---
name: tdd
description: Test-Driven Development methodology for writing tests before code. Use when developing new features, fixing bugs with test cases, or ensuring high code quality through test-first approach.
---

# Test-Driven Development (TDD) Skill

## Core Principle

**Write the test first, then make it pass, then refactor.**

TDD is a discipline where you:
1. Write a failing test
2. Write minimal code to make it pass
3. Refactor while keeping tests green

This creates well-tested, well-designed code by default.

---

## The TDD Cycle (Red-Green-Refactor)

```
┌─────────────────────────────────────────────────────────┐
│                    TDD CYCLE                            │
└─────────────────────────────────────────────────────────┘

    ┌───────────────┐
    │   1. RED      │   Write a failing test
    │   ❌ Test     │   (Test what you want to build)
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  2. GREEN     │   Write minimal code to pass
    │   ✅ Test     │   (Make it work)
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │  3. REFACTOR  │   Improve code quality
    │   🔄 Clean    │   (Make it right)
    └───────┬───────┘
            │
            └─────────► Repeat for next behavior
```

---

## Step 1: RED — Write a Failing Test

### What to Test First

Start with the simplest, most basic behavior:

❌ **Don't start with:** Edge cases, error handling, complex scenarios
✅ **Do start with:** The happy path, core functionality, simplest use case

### Example: Building a Calculator

```python
# test_calculator.py

def test_add_two_positive_numbers():
    """Test the simplest addition case"""
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

### Run the Test (Watch it Fail)

```bash
pytest test_calculator.py

# Output:
# NameError: name 'Calculator' is not defined
# ✅ GOOD! This is expected (RED phase)
```

**Why this is important:** Watching the test fail proves:
- The test actually runs
- The test can detect problems
- You're not testing code that already exists

---

## Step 2: GREEN — Write Minimal Code

### Goal: Make the Test Pass (Nothing More)

Write the **simplest possible code** to make the test pass:

```python
# calculator.py

class Calculator:
    def add(self, a, b):
        return a + b
```

### Run the Test Again

```bash
pytest test_calculator.py

# Output:
# test_calculator.py::test_add_two_positive_numbers PASSED
# ✅ GREEN! Test passes
```

**Resist the urge to:**
- Add features that aren't tested
- Handle edge cases you haven't tested for
- Optimize prematurely
- Write "clever" code

**At this stage:** Working code > Perfect code

---

## Step 3: REFACTOR — Improve the Code

### Now Make It Better

With tests passing, you can safely improve code:

```python
# No refactoring needed yet (code is already simple)
# Wait until you have duplication or complexity
```

### Rules for Refactoring

- Tests must stay GREEN
- No behavior changes
- Improve structure, readability, performance
- Commit after successful refactoring

---

## Expanding Functionality

### Add More Tests, One at a Time

```python
# test_calculator.py

def test_add_two_positive_numbers():
    calc = Calculator()
    assert calc.add(2, 3) == 5

def test_add_negative_numbers():  # ← New test
    calc = Calculator()
    assert calc.add(-1, -1) == -2

def test_add_zero():  # ← New test
    calc = Calculator()
    assert calc.add(5, 0) == 5
```

**Pattern:**
1. Write one new test (RED)
2. Make it pass (GREEN)
3. Refactor if needed
4. Repeat

---

## TDD for Bug Fixes

### When You Find a Bug

**Traditional approach:**
1. Fix the bug
2. Hope it doesn't come back

**TDD approach:**
1. Write a test that demonstrates the bug (RED)
2. Fix the code to make test pass (GREEN)
3. Refactor if needed
4. Bug can't return (test prevents regression)

### Example: Bug Fix with TDD

```python
# Bug report: Calculator.divide() crashes when dividing by zero

def test_divide_by_zero_raises_error():  # ← RED (test the bug)
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

# Now fix the code to handle this case
# GREEN: Test passes after fix
# REFACTOR: Clean up if needed
```

---

## Test Organization Patterns

### Arrange-Act-Assert (AAA)

Structure tests in three phases:

```python
def test_user_registration():
    # ARRANGE — Set up test data
    email = "user@example.com"
    password = "secure123"
    user_service = UserService()

    # ACT — Execute the behavior
    user = user_service.register(email, password)

    # ASSERT — Verify the outcome
    assert user.email == email
    assert user.password != password  # Should be hashed
    assert user.id is not None
```

### Given-When-Then (BDD Style)

Alternative pattern (same concept):

```python
def test_shopping_cart_calculates_total():
    # GIVEN a cart with items
    cart = ShoppingCart()
    cart.add_item(Item("Widget", price=10.00))
    cart.add_item(Item("Gadget", price=15.00))

    # WHEN calculating the total
    total = cart.calculate_total()

    # THEN the total should be correct
    assert total == 25.00
```

---

## What Makes a Good Test

### Characteristics of Good Tests

✅ **Fast** — Run in milliseconds
✅ **Independent** — No dependencies on other tests
✅ **Repeatable** — Same result every time
✅ **Self-validating** — Clear pass/fail (no manual verification)
✅ **Timely** — Written before the code (TDD)

### Test Naming Conventions

**Good test names explain:**
- What is being tested
- Under what conditions
- What the expected result is

```python
# ✅ GOOD
def test_add_returns_sum_of_two_positive_numbers()
def test_divide_raises_error_when_divisor_is_zero()
def test_user_registration_sends_confirmation_email()

# ❌ BAD
def test_add()
def test_divide()
def test_registration()
```

---

## TDD Anti-Patterns to Avoid

### 1. Writing Tests After Code

❌ **Don't:**
```python
# Write all the code first
class Calculator:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b
    # ... then write tests
```

✅ **Do:**
```python
# Write test first
def test_add(): ...
# Then write code to pass
class Calculator:
    def add(self, a, b): return a + b
# Repeat for next function
```

---

### 2. Testing Implementation Details

❌ **Don't test HOW:**
```python
def test_sort_uses_quicksort_algorithm():
    # Testing internal implementation
    sorter = Sorter()
    assert sorter.algorithm == 'quicksort'
```

✅ **Do test WHAT:**
```python
def test_sort_returns_items_in_ascending_order():
    # Testing behavior
    sorter = Sorter()
    result = sorter.sort([3, 1, 2])
    assert result == [1, 2, 3]
```

---

### 3. Over-Mocking

❌ **Don't mock everything:**
```python
def test_process_order():
    mock_db = Mock()
    mock_email = Mock()
    mock_payment = Mock()
    mock_inventory = Mock()
    # Test becomes testing mocks, not real behavior
```

✅ **Do mock external dependencies only:**
```python
def test_process_order():
    mock_payment_gateway = Mock()  # External service
    # Use real objects for your own code
    order_processor = OrderProcessor(mock_payment_gateway)
```

---

### 4. One Giant Test

❌ **Don't test everything in one test:**
```python
def test_user_system():
    # Test registration
    # Test login
    # Test logout
    # Test password reset
    # 200 lines of assertions
```

✅ **Do write focused tests:**
```python
def test_user_registration_creates_account(): ...
def test_user_login_with_valid_credentials(): ...
def test_user_logout_clears_session(): ...
def test_password_reset_sends_email(): ...
```

---

## TDD Workflow Example

### Building a User Authentication System

**Iteration 1: Basic registration**

```python
# RED
def test_register_user_with_valid_email():
    auth = AuthService()
    user = auth.register("user@example.com", "password123")
    assert user is not None

# GREEN
class AuthService:
    def register(self, email, password):
        return User(email=email)

# REFACTOR
# (Code is simple, no refactoring needed yet)
```

**Iteration 2: Password hashing**

```python
# RED
def test_register_user_hashes_password():
    auth = AuthService()
    user = auth.register("user@example.com", "password123")
    assert user.password_hash != "password123"
    assert len(user.password_hash) > 20  # Hashed value

# GREEN
class AuthService:
    def register(self, email, password):
        password_hash = bcrypt.hash(password)
        return User(email=email, password_hash=password_hash)

# REFACTOR
# Extract password hashing to separate class
class PasswordHasher:
    @staticmethod
    def hash(password):
        return bcrypt.hash(password)
```

**Iteration 3: Email validation**

```python
# RED
def test_register_user_with_invalid_email_raises_error():
    auth = AuthService()
    with pytest.raises(ValueError):
        auth.register("not-an-email", "password123")

# GREEN
class AuthService:
    def register(self, email, password):
        if '@' not in email:  # Simple validation
            raise ValueError("Invalid email")
        password_hash = PasswordHasher.hash(password)
        return User(email=email, password_hash=password_hash)

# REFACTOR
# Extract email validation
class EmailValidator:
    @staticmethod
    def validate(email):
        if '@' not in email or '.' not in email:
            raise ValueError("Invalid email format")
```

---

## TDD Benefits

### Design Benefits

- **Better API design** — Writing tests first forces you to think about usage
- **Modular code** — Testable code is naturally decoupled
- **YAGNI** — You only build what's tested (what's needed)

### Quality Benefits

- **High test coverage** — Code is tested by default
- **Regression prevention** — Tests catch breaking changes
- **Living documentation** — Tests show how code should be used

### Workflow Benefits

- **Confidence to refactor** — Tests prove behavior unchanged
- **Faster debugging** — Test pinpoints exact failure
- **Clear progress** — Each passing test is visible progress

---

## Integration with Other Skills

### With Refactoring Skill

- TDD makes refactoring safe (tests prove behavior unchanged)
- Refactor step is built into TDD cycle
- Always refactor with GREEN tests

### With Code Review Skill

- TDD code comes with tests (review checklist item)
- Tests document intended behavior
- Easier to review (test shows expected behavior)

### With Git Hygiene

- Commit after each RED-GREEN-REFACTOR cycle
- Atomic commits for each new behavior
- Commit message: "test: add validation for X"

---

## Quick Reference

### TDD Cycle

1. **RED** — Write failing test
2. **GREEN** — Write minimal code to pass
3. **REFACTOR** — Improve code quality
4. Repeat

### Test Structure (AAA)

```python
def test_behavior():
    # ARRANGE — Set up
    # ACT — Execute
    # ASSERT — Verify
```

### When to TDD

✅ New features
✅ Bug fixes (test the bug first)
✅ Refactoring (tests enable safe refactoring)
✅ Learning new APIs (tests are documentation)

### When NOT to TDD

❌ Prototyping/experimenting (TDD after design is clear)
❌ UI layout (use visual testing instead)
❌ Performance tuning (benchmark, don't TDD)

---

**Remember:** TDD is a discipline. It feels slow at first, but leads to faster development over time. Red-Green-Refactor. Test first, code second, refactor third. Small steps, frequent commits, always keep tests passing.
