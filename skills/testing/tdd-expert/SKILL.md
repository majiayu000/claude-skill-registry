---
name: tdd-expert
description: Test-Driven Development expert. Use when implementing TDD workflow, red-green-refactor, or writing tests first.
---

# Test-Driven Development (TDD) Expert

**Self-contained TDD expertise for ANY user project.**

---

## The TDD Cycle: Red-Green-Refactor

### 1. RED Phase: Write Failing Test

**Goal**: Define expected behavior through a failing test

```typescript
import { describe, it, expect } from 'vitest';
import { Calculator } from './Calculator';

describe('Calculator', () => {
  it('should add two numbers', () => {
    const calculator = new Calculator();
    expect(calculator.add(2, 3)).toBe(5); // WILL FAIL - Calculator doesn't exist
  });
});
```

**RED Checklist**:
- [ ] Test describes ONE specific behavior
- [ ] Test fails for RIGHT reason (not syntax error)
- [ ] Test name is clear
- [ ] Expected behavior obvious

### 2. GREEN Phase: Minimal Implementation

**Goal**: Simplest code that makes test pass

```typescript
// Calculator.ts
export class Calculator {
  add(a: number, b: number): number {
    return a + b; // Minimal implementation
  }
}
```

**GREEN Checklist**:
- [ ] Test passes
- [ ] Code is simplest possible
- [ ] No premature optimization
- [ ] No extra features

### 3. REFACTOR Phase: Improve Design

**Goal**: Improve code quality without changing behavior

```typescript
// Refactor: Support variable arguments
export class Calculator {
  add(...numbers: number[]): number {
    return numbers.reduce((sum, n) => sum + n, 0);
  }
}

// Tests still pass!
```

**REFACTOR Checklist**:
- [ ] All tests still pass
- [ ] Code is more readable
- [ ] Removed duplication
- [ ] Better design patterns

---

## TDD Benefits

**Design Benefits**:
- Forces modular, testable code
- Reveals design problems early
- Encourages SOLID principles
- Promotes simple solutions

**Quality Benefits**:
- 100% test coverage (by definition)
- Tests document behavior
- Regression safety net
- Faster debugging

**Productivity Benefits**:
- Less time debugging
- Confidence to refactor
- Faster iterations
- Clearer requirements

---

## BDD: Behavior-Driven Development

**Extension of TDD with natural language tests**

### Given-When-Then Pattern

```typescript
describe('Shopping Cart', () => {
  it('should apply 10% discount when total exceeds $100', () => {
    // Given: A cart with $120 worth of items
    const cart = new ShoppingCart();
    cart.addItem({ price: 120, quantity: 1 });

    // When: Getting the total
    const total = cart.getTotal();

    // Then: 10% discount applied
    expect(total).toBe(108); // $120 - $12 (10%)
  });
});
```

**BDD Benefits**:
- Tests readable by non-developers
- Clear business requirements
- Better stakeholder communication
- Executable specifications

---

## TDD Patterns

### Pattern 1: Test List

Before coding, list all tests needed:

```markdown
Calculator Tests:
- [ ] add two positive numbers
- [ ] add negative numbers
- [ ] add zero
- [ ] add multiple numbers
- [ ] multiply two numbers
- [ ] divide two numbers
- [ ] divide by zero (error)
```

Work through list one by one.

### Pattern 2: Fake It Till You Make It

Start with hardcoded returns, generalize later:

```typescript
// Test 1: add(2, 3) = 5
add(a, b) { return 5; } // Hardcoded!

// Test 2: add(5, 7) = 12
add(a, b) { return a + b; } // Generalized
```

### Pattern 3: Triangulation

Use multiple tests to force generalization:

```typescript
// Test 1
expect(fizzbuzz(3)).toBe('Fizz');

// Test 2
expect(fizzbuzz(5)).toBe('Buzz');

// Test 3
expect(fizzbuzz(15)).toBe('FizzBuzz');

// Forces complete implementation
```

### Pattern 4: Test Data Builders

Create test helpers for complex objects:

```typescript
class UserBuilder {
  private user = { name: 'Test', email: 'test@example.com', role: 'user' };

  withName(name: string) {
    this.user.name = name;
    return this;
  }

  withRole(role: string) {
    this.user.role = role;
    return this;
  }

  build() {
    return this.user;
  }
}

// Usage
const admin = new UserBuilder().withRole('admin').build();
```

---

## Refactoring with Confidence

**The TDD Safety Net**

### Refactoring Types

**1. Extract Method**:
```typescript
// Before
function processOrder(order) {
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  const tax = total * 0.1;
  return total + tax;
}

// After (refactored with test safety)
function calculateTotal(items) {
  return items.reduce((sum, item) => sum + item.price, 0);
}

function calculateTax(total) {
  return total * 0.1;
}

function processOrder(order) {
  const total = calculateTotal(order.items);
  const tax = calculateTax(total);
  return total + tax;
}
```

**2. Remove Duplication**:
```typescript
// Tests force you to see duplication
it('should validate email', () => {
  expect(validateEmail('test@example.com')).toBe(true);
  expect(validateEmail('invalid')).toBe(false);
});

it('should validate phone', () => {
  expect(validatePhone('+1-555-0100')).toBe(true);
  expect(validatePhone('invalid')).toBe(false);
});

// Extract common validation pattern
```

### Refactoring Workflow

```
1. All tests GREEN? → Continue
2. Identify code smell
3. Make small refactoring
4. Run tests → GREEN? → Continue
5. Repeat until satisfied
6. Commit
```

---

## TDD Anti-Patterns

### ❌ Testing Implementation Details

```typescript
// BAD: Testing private method
it('should call _validateEmail internally', () => {
  spyOn(service, '_validateEmail');
  service.createUser({ email: 'test@example.com' });
  expect(service._validateEmail).toHaveBeenCalled();
});

// GOOD: Testing behavior
it('should reject invalid email', () => {
  expect(() => service.createUser({ email: 'invalid' }))
    .toThrow('Invalid email');
});
```

### ❌ Writing Tests After Code

```typescript
// Wrong order!
1. Write implementation
2. Write tests

// Correct TDD:
1. Write test (RED)
2. Write implementation (GREEN)
3. Refactor
```

### ❌ Large Tests

```typescript
// BAD: Testing multiple behaviors
it('should handle user lifecycle', () => {
  const user = createUser();
  updateUser(user, { name: 'New Name' });
  deleteUser(user);
  // Too much in one test!
});

// GOOD: One behavior per test
it('should create user', () => {
  const user = createUser();
  expect(user).toBeDefined();
});

it('should update user name', () => {
  const user = createUser();
  updateUser(user, { name: 'New Name' });
  expect(user.name).toBe('New Name');
});
```

### ❌ Skipping Refactor Phase

```typescript
// Don't skip refactoring!
RED → GREEN → REFACTOR → RED → GREEN → REFACTOR
     ↑________________↑
     Always refactor!
```

---

## Mock-Driven TDD

**When testing with external dependencies**

### Strategy 1: Dependency Injection

```typescript
class UserService {
  constructor(private db: Database) {} // Inject dependency

  async getUser(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// Test with mock
const mockDb = { query: vi.fn().mockResolvedValue({ id: '123' }) };
const service = new UserService(mockDb);
```

### Strategy 2: Interface-Based Mocking

```typescript
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class MockEmailService implements EmailService {
  sent: any[] = [];

  async send(to: string, subject: string, body: string) {
    this.sent.push({ to, subject, body });
  }
}

// Test with mock
const mockEmail = new MockEmailService();
const service = new UserService(mockEmail);
await service.registerUser({ email: 'test@example.com' });
expect(mockEmail.sent).toHaveLength(1);
```

---

## SOLID Principles Through TDD

**TDD naturally leads to SOLID design**

### Single Responsibility (SRP)
Tests reveal when class does too much:
```typescript
// Many tests for one class? Split it!
describe('UserManager', () => {
  // 20+ tests here → Too many responsibilities
});

// Refactor to multiple classes
describe('UserCreator', () => { /* 5 tests */ });
describe('UserValidator', () => { /* 5 tests */ });
describe('UserNotifier', () => { /* 5 tests */ });
```

### Open/Closed (OCP)
Tests enable extension without modification:
```typescript
// Testable, extensible design
interface PaymentProcessor {
  process(amount: number): Promise<void>;
}

class StripeProcessor implements PaymentProcessor { }
class PayPalProcessor implements PaymentProcessor { }
```

### Dependency Inversion (DIP)
TDD requires dependency injection:
```typescript
// Testable: Depends on abstraction
class OrderService {
  constructor(private payment: PaymentProcessor) {}
}

// Easy to test with mocks
const mockPayment = new MockPaymentProcessor();
const service = new OrderService(mockPayment);
```

---

## Quick Reference

### TDD Workflow
```
1. Write test (RED) → Fails ✅
2. Minimal code (GREEN) → Passes ✅
3. Refactor → Still passes ✅
4. Repeat
```

### Test Smells
- Test too long (>20 lines)
- Multiple assertions (>3)
- Testing implementation
- Unclear test name
- Slow tests (>100ms)
- Flaky tests

### When to Use TDD
✅ New features
✅ Bug fixes (add test first)
✅ Refactoring
✅ Complex logic
✅ Public APIs

❌ Throwaway prototypes
❌ UI layout (use E2E instead)
❌ Highly experimental code

---

**This skill is self-contained and works in ANY user project.**
