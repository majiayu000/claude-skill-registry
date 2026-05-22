---
name: beck-test-driven-development
description: Develop software in the style of Kent Beck, creator of Test-Driven Development and Extreme Programming. Emphasizes red-green-refactor, tests-first design, small steps, and emergent architecture. Use when writing new features, refactoring legacy code, or establishing development discipline.
---

# Kent Beck Test-Driven Development Style Guide

## Overview

Kent Beck is the creator of Test-Driven Development (TDD) and Extreme Programming (XP), two of the most influential software development practices of the past 30 years. TDD inverts the traditional code-then-test approach: write a failing test first, make it pass with the simplest code, then refactor. This discipline produces clean, tested, well-designed code as a natural byproduct of the development process.

## Core Philosophy

> "Test-Driven Development is a way of managing fear during programming."

> "Make it work, make it right, make it fast—in that order."

> "I'm not a great programmer; I'm just a good programmer with great habits."

TDD is not primarily about testing—it's about design. Writing tests first forces you to think about interfaces before implementations, dependencies before details, and behavior before structure. The tests are a beneficial side effect of a disciplined design process.

## Design Principles

1. **Red-Green-Refactor**: Write failing test → make it pass → improve the code.

2. **Baby Steps**: Take the smallest step that could possibly work.

3. **YAGNI**: You Aren't Gonna Need It—don't build what you don't need yet.

4. **Simple Design**: Code that passes tests, reveals intent, has no duplication, and has fewest elements.

5. **Courage**: Tests give you the courage to refactor aggressively.

## The TDD Cycle

```
    ┌─────────────────────────────────────────┐
    │                                         │
    │    1. RED: Write a failing test         │
    │       - Test doesn't compile? That's    │
    │         failing. Write minimal code     │
    │         to make it compile (still fail) │
    │                                         │
    │                    │                    │
    │                    ▼                    │
    │                                         │
    │    2. GREEN: Make it pass               │
    │       - Write the simplest code that    │
    │         could possibly work             │
    │       - Sins allowed: duplication,      │
    │         hardcoding, ugly code           │
    │                                         │
    │                    │                    │
    │                    ▼                    │
    │                                         │
    │    3. REFACTOR: Clean up                │
    │       - Remove duplication              │
    │       - Improve names                   │
    │       - Extract methods/classes         │
    │       - Tests must stay green           │
    │                                         │
    │                    │                    │
    │                    ▼                    │
    │              (repeat)                   │
    └─────────────────────────────────────────┘
```

## When Practicing TDD

### Always

- Write the test before the code
- Run the test and watch it fail (red)
- Write only enough code to pass the test
- Refactor only when tests are green
- Commit after each green-refactor cycle
- Keep tests fast (milliseconds, not seconds)
- Test behavior, not implementation

### Never

- Write code without a failing test
- Write more than one failing test at a time
- Refactor while tests are red
- Skip the refactoring step
- Test private methods directly
- Let tests become slow
- Mock what you don't own

### Prefer

- Small, focused tests over large integration tests
- One assertion per test (logical assertion)
- Descriptive test names that document behavior
- Testing through public interfaces
- Fake it till you make it
- Triangulation to drive generalization
- Obvious implementation when it's obvious

## Code Patterns

### The TDD Rhythm

```python
# Example: Building a Money class with TDD

# ═══════════════════════════════════════════════════════════════
# Cycle 1: First test - establish the basics
# ═══════════════════════════════════════════════════════════════

# RED: Write failing test
def test_multiplication():
    five = Dollar(5)
    assert five.times(2) == Dollar(10)

# This fails: Dollar doesn't exist

# GREEN: Simplest code to pass
class Dollar:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        return Dollar(self.amount * multiplier)
    
    def __eq__(self, other):
        return self.amount == other.amount

# REFACTOR: Nothing to refactor yet

# ═══════════════════════════════════════════════════════════════
# Cycle 2: Add another test - triangulate
# ═══════════════════════════════════════════════════════════════

# RED: New failing test
def test_multiplication_by_three():
    five = Dollar(5)
    assert five.times(3) == Dollar(15)

# GREEN: Already passes! Our implementation was general enough

# REFACTOR: Still clean

# ═══════════════════════════════════════════════════════════════
# Cycle 3: Handle a new requirement - different currencies
# ═══════════════════════════════════════════════════════════════

# RED: Failing test for Franc
def test_franc_multiplication():
    five = Franc(5)
    assert five.times(2) == Franc(10)

# GREEN: Quick and dirty - copy Dollar (sin: duplication)
class Franc:
    def __init__(self, amount):
        self.amount = amount
    
    def times(self, multiplier):
        return Franc(self.amount * multiplier)
    
    def __eq__(self, other):
        return self.amount == other.amount

# REFACTOR: Extract common parent class
class Money:
    def __init__(self, amount):
        self.amount = amount
    
    def __eq__(self, other):
        return (self.amount == other.amount and 
                type(self) == type(other))

class Dollar(Money):
    def times(self, multiplier):
        return Dollar(self.amount * multiplier)

class Franc(Money):
    def times(self, multiplier):
        return Franc(self.amount * multiplier)
```

### Fake It Till You Make It

```python
# Start with the most degenerate implementation
# Then generalize as tests force you

# RED: First test
def test_sum():
    assert sum([1, 2, 3]) == 6

# GREEN: Fake it!
def sum(numbers):
    return 6  # Obviously wrong, but test passes

# RED: Add a test that forces generalization
def test_sum_different_numbers():
    assert sum([2, 3, 4]) == 9

# GREEN: Now we must implement for real
def sum(numbers):
    result = 0
    for n in numbers:
        result += n
    return result

# REFACTOR: Use built-in (if appropriate)
def sum(numbers):
    return builtins.sum(numbers)
```

### Triangulation

```python
# Use multiple examples to drive toward generalization

# RED: First example
def test_equality_same_amount():
    assert Dollar(5) == Dollar(5)

# GREEN: Simplest implementation
def __eq__(self, other):
    return True  # Fake it!

# RED: Second example forces real implementation
def test_equality_different_amount():
    assert Dollar(5) != Dollar(6)

# GREEN: Now we need real logic
def __eq__(self, other):
    return self.amount == other.amount

# RED: Third example - different types
def test_equality_different_types():
    assert Dollar(5) != Franc(5)

# GREEN: Check type too
def __eq__(self, other):
    return (self.amount == other.amount and 
            type(self) == type(other))
```

### Test Structure: Arrange-Act-Assert

```python
def test_withdraw_reduces_balance():
    # Arrange: Set up the test context
    account = Account(balance=100)
    
    # Act: Perform the action being tested
    account.withdraw(30)
    
    # Assert: Verify the expected outcome
    assert account.balance == 70


# Or Given-When-Then for BDD style
def test_given_account_with_balance_when_withdraw_then_balance_reduced():
    # Given
    account = Account(balance=100)
    
    # When
    account.withdraw(30)
    
    # Then
    assert account.balance == 70
```

### Test Doubles

```python
# Beck's approach: Use the simplest double that works

# 1. Fake: Working implementation with shortcuts
class FakeRepository:
    def __init__(self):
        self.data = {}
    
    def save(self, entity):
        self.data[entity.id] = entity
    
    def find(self, id):
        return self.data.get(id)


# 2. Stub: Returns canned answers
class StubPriceService:
    def get_price(self, symbol):
        return 100.00  # Always returns same price


# 3. Spy: Records what happened
class SpyEmailService:
    def __init__(self):
        self.sent_emails = []
    
    def send(self, to, subject, body):
        self.sent_emails.append({
            'to': to,
            'subject': subject,
            'body': body
        })


# 4. Mock: Verifies expected interactions
# (Use sparingly - prefer state verification over behavior verification)


# Test using a fake
def test_user_registration_saves_user():
    # Arrange
    repository = FakeRepository()
    service = UserService(repository)
    
    # Act
    service.register("alice@example.com", "password123")
    
    # Assert: Check state, not behavior
    saved_user = repository.find_by_email("alice@example.com")
    assert saved_user is not None
    assert saved_user.email == "alice@example.com"
```

### The Testing Pyramid

```python
# Beck's view: Most tests should be unit tests

"""
                    /\
                   /  \
                  / E2E \        <- Few: Slow, brittle, but necessary
                 /──────\
                /        \
               /Integration\     <- Some: Test component boundaries
              /──────────────\
             /                \
            /    Unit Tests    \  <- Many: Fast, focused, isolated
           /────────────────────\

"""

# Unit test: Fast, isolated, focused
def test_calculate_discount_for_premium_customer():
    customer = Customer(tier='premium')
    order = Order(total=100)
    
    discount = calculate_discount(customer, order)
    
    assert discount == 20  # 20% for premium


# Integration test: Verify component interaction
def test_order_service_persists_to_database():
    db = create_test_database()
    service = OrderService(db)
    
    order = service.create_order(customer_id=1, items=[...])
    
    persisted = db.find_order(order.id)
    assert persisted == order


# E2E test: Full system, sparingly
def test_checkout_flow():
    browser = Browser()
    browser.visit('/cart')
    browser.click('Checkout')
    browser.fill('card_number', '4242424242424242')
    browser.click('Pay')
    
    assert browser.text_present('Order confirmed')
```

### Refactoring Patterns

```python
# REFACTOR phase: Common transformations

# 1. Extract Method
# Before
def print_invoice(invoice):
    print(f"Invoice #{invoice.id}")
    total = 0
    for item in invoice.items:
        total += item.price * item.quantity
    print(f"Total: ${total}")

# After
def print_invoice(invoice):
    print(f"Invoice #{invoice.id}")
    print(f"Total: ${calculate_total(invoice)}")

def calculate_total(invoice):
    return sum(item.price * item.quantity for item in invoice.items)


# 2. Extract Class
# Before: Order has too many responsibilities
class Order:
    def calculate_total(self): ...
    def calculate_tax(self): ...
    def calculate_shipping(self): ...
    def format_for_email(self): ...
    def format_for_pdf(self): ...

# After: Extract formatting
class Order:
    def calculate_total(self): ...
    def calculate_tax(self): ...
    def calculate_shipping(self): ...

class OrderFormatter:
    def __init__(self, order): ...
    def to_email(self): ...
    def to_pdf(self): ...


# 3. Replace Conditional with Polymorphism
# Before
def calculate_pay(employee):
    if employee.type == 'hourly':
        return employee.hours * employee.rate
    elif employee.type == 'salaried':
        return employee.salary / 12
    elif employee.type == 'commissioned':
        return employee.base + employee.sales * employee.commission_rate

# After
class HourlyEmployee:
    def calculate_pay(self):
        return self.hours * self.rate

class SalariedEmployee:
    def calculate_pay(self):
        return self.salary / 12

class CommissionedEmployee:
    def calculate_pay(self):
        return self.base + self.sales * self.commission_rate
```

### The TDD State Machine

```python
class TDDPractitioner:
    """
    The mental states of a TDD practitioner.
    """
    
    def __init__(self):
        self.state = 'THINKING'
        self.tests_passing = True
    
    def write_test(self):
        """Write a new failing test."""
        assert self.state == 'THINKING'
        assert self.tests_passing, "Fix failing tests before writing new ones"
        
        # Write the test...
        self.tests_passing = False  # Test should fail
        self.state = 'RED'
    
    def make_it_pass(self):
        """Write simplest code to pass the test."""
        assert self.state == 'RED'
        
        # Write minimal code...
        self.tests_passing = True
        self.state = 'GREEN'
    
    def refactor(self):
        """Improve the code while keeping tests green."""
        assert self.state == 'GREEN'
        assert self.tests_passing
        
        # Refactor...
        # Run tests after each change
        assert self.tests_passing, "Refactoring broke tests!"
        
        self.state = 'THINKING'  # Ready for next cycle
    
    def commit(self):
        """Commit after each complete cycle."""
        assert self.state in ('GREEN', 'THINKING')
        assert self.tests_passing
        
        # git commit -m "descriptive message"
```

## Mental Model

Beck approaches development by asking:

1. **What's the next test?** Start with what you want to prove
2. **What's the simplest way to pass?** Don't over-engineer
3. **What duplication can I remove?** Refactor mercilessly
4. **Am I scared?** Write more tests until you're not
5. **Is this design emerging?** Trust the process

## The TDD Checklist

```
□ Write a test that expresses what you want
□ Run it and watch it fail (RED)
□ Write the simplest code to pass
□ Run tests and see them pass (GREEN)
□ Look for duplication to remove
□ Refactor while tests stay green
□ Commit the cycle
□ Repeat
```

## Signature Beck Moves

- Red-Green-Refactor cycle
- Fake it till you make it
- Triangulation to generalize
- Obvious implementation when obvious
- Baby steps when uncertain
- Test list to track progress
- One assertion per test (conceptually)
- Test behavior, not implementation
