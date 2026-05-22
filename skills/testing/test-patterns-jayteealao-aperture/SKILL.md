---
name: test-patterns
description: This skill provides patterns and best practices for generating and organizing tests. It covers unit testing, integration testing, test data factories, and coverage strategies across multiple languages and frameworks.
context: fork
user-invocable: false
---

# Test Patterns Skill

Generate and organize tests following project conventions and industry best practices.

## When to Use

- Generating unit tests for new or existing code
- Creating integration/API tests
- Setting up test data factories
- Analyzing and improving test coverage
- Establishing testing conventions in a project

## Reference Documents

- [Unit Test Patterns](./references/unit-test-patterns.md) - Patterns for unit tests including mocking, fixtures, and assertions
- [Integration Test Patterns](./references/integration-test-patterns.md) - API and integration testing patterns
- [Test Data Factories](./references/test-data-factories.md) - Factory patterns for generating test data
- [Coverage Strategies](./references/coverage-strategies.md) - Approaches to meaningful test coverage

## Core Principles

### 1. Test Behavior, Not Implementation

```
WRONG: Testing internal method calls
RIGHT: Testing observable behavior and outputs
```

Tests should verify what code does, not how it does it. This makes tests resilient to refactoring.

### 2. Arrange-Act-Assert (AAA) Pattern

Every test should have three distinct sections:

```python
# Arrange - Set up test data and conditions
user = create_user(name="Alice")
order = create_order(user=user, items=[item1, item2])

# Act - Execute the behavior being tested
result = order.calculate_total()

# Assert - Verify the expected outcome
assert result == 150.00
```

### 3. One Assertion Per Test (Logical)

Each test should verify one logical concept, though it may have multiple assertions for that concept:

```python
def test_user_creation_sets_defaults():
    user = User.create(email="test@example.com")

    # Multiple assertions for one concept: default values
    assert user.status == "pending"
    assert user.role == "member"
    assert user.created_at is not None
```

### 4. Descriptive Test Names

Test names should describe the scenario and expected outcome:

```python
# WRONG
def test_order():
def test_calculate():

# RIGHT
def test_order_with_discount_applies_percentage_reduction():
def test_calculate_total_includes_tax_for_taxable_items():
```

### 5. Test Independence

Tests must not depend on each other or on execution order:

- Each test sets up its own data
- Each test cleans up after itself (or uses transactions)
- No shared mutable state between tests

## Workflow: Generating Tests

### Step 1: Analyze the Code Under Test

1. Read the file/function to be tested
2. Identify public interfaces and behaviors
3. List edge cases and error conditions
4. Note dependencies that need mocking

### Step 2: Determine Test Type

| Code Type | Test Type | Focus |
|-----------|-----------|-------|
| Pure function | Unit test | Input/output |
| Class with dependencies | Unit test with mocks | Behavior |
| API endpoint | Integration test | Request/response |
| Database operation | Integration test | Data persistence |
| External service call | Unit test with mocks | Contract |

### Step 3: Create Test Structure

```
tests/
├── unit/
│   └── [module]/
│       └── test_[file].py
├── integration/
│   └── test_[feature].py
└── fixtures/
    └── [shared fixtures]
```

### Step 4: Write Tests

Follow the patterns in reference documents for specific test types.

### Step 5: Verify Coverage

Run coverage analysis and add tests for uncovered critical paths.

## Language-Specific Patterns

### Python (pytest)

```python
import pytest
from unittest.mock import Mock, patch

class TestOrderCalculation:
    @pytest.fixture
    def order(self):
        return Order(items=[Item(price=100), Item(price=50)])

    def test_calculates_subtotal(self, order):
        assert order.subtotal == 150

    @pytest.mark.parametrize("discount,expected", [
        (0, 150),
        (10, 135),
        (50, 75),
    ])
    def test_applies_discount(self, order, discount, expected):
        order.apply_discount(discount)
        assert order.total == expected
```

### TypeScript (Jest/Vitest)

```typescript
import { describe, it, expect, vi } from 'vitest';

describe('OrderService', () => {
  it('calculates total with tax', () => {
    const order = new Order([
      { price: 100 },
      { price: 50 }
    ]);

    expect(order.totalWithTax(0.1)).toBe(165);
  });

  it('sends confirmation email on completion', async () => {
    const emailService = { send: vi.fn() };
    const order = new Order([], { emailService });

    await order.complete();

    expect(emailService.send).toHaveBeenCalledWith(
      expect.objectContaining({ type: 'confirmation' })
    );
  });
});
```

### Ruby (RSpec)

```ruby
RSpec.describe Order do
  subject(:order) { described_class.new(items: items) }
  let(:items) { [Item.new(price: 100), Item.new(price: 50)] }

  describe '#total' do
    it 'sums item prices' do
      expect(order.total).to eq(150)
    end

    context 'with discount applied' do
      before { order.apply_discount(10) }

      it 'reduces total by percentage' do
        expect(order.total).to eq(135)
      end
    end
  end
end
```

## Quick Reference

| Pattern | When to Use |
|---------|-------------|
| Factory | Creating test objects with defaults |
| Builder | Creating complex test objects step-by-step |
| Mock | Replacing dependencies |
| Stub | Providing canned responses |
| Spy | Verifying method calls |
| Fake | Lightweight implementation for testing |
| Fixture | Shared test data setup |
| Parametrize | Testing multiple inputs |
