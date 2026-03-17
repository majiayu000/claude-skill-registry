---
name: arcanea-tdd
description: Test-Driven Development with Arcanean philosophy - write tests first, fail intentionally, implement minimally, refactor with confidence. Embodies the Arcanean principle that constraint liberates creativity.
version: 2.0.0
author: Arcanea
tags: [testing, tdd, development, quality, methodology]
triggers:
  - test
  - tdd
  - test driven
  - write tests
  - test first
  - feature implementation
---

# Test-Driven Development: The Arcanean Way

> *"The test is not a check. The test is a specification. Write the specification before the implementation, and the implementation reveals itself."*

---

## The TDD Philosophy

In Arcanea, we recognize that **constraints liberate creativity**. TDD embodies this principle perfectly:

```
CONSTRAINT: Write the test first
LIBERATION: The implementation becomes clear
CONSTRAINT: Make it fail first
LIBERATION: You know what success looks like
CONSTRAINT: Implement minimally
LIBERATION: No over-engineering
CONSTRAINT: Refactor with green tests
LIBERATION: Confidence to improve
```

---

## The Sacred Cycle

```
         ╭──────────────────╮
         │    RED           │
         │  Write a test    │
         │  that fails      │
         ╰────────┬─────────╯
                  │
                  ▼
         ╭──────────────────╮
         │    GREEN         │
         │  Write minimum   │
         │  code to pass    │
         ╰────────┬─────────╯
                  │
                  ▼
         ╭──────────────────╮
         │   REFACTOR       │
         │  Improve code    │
         │  tests stay green│
         ╰────────┬─────────╯
                  │
                  ╰──────────────╮
                                 │
         ╭───────────────────────╯
         │
         ▼
    (Next test)
```

### RED: The Failing Test

```typescript
// Write a test for behavior that doesn't exist yet
describe('UserService', () => {
  it('should create a user with valid email', async () => {
    const service = new UserService();
    const user = await service.create({ email: 'test@example.com' });

    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
    expect(user.createdAt).toBeInstanceOf(Date);
  });
});

// Run the test - IT MUST FAIL
// This proves the test is testing something real
```

### GREEN: The Minimal Implementation

```typescript
// Write the MINIMUM code to make the test pass
// No more, no less
class UserService {
  async create(data: { email: string }) {
    return {
      id: crypto.randomUUID(),
      email: data.email,
      createdAt: new Date(),
    };
  }
}

// Run the test - IT MUST PASS
```

### REFACTOR: Improve With Confidence

```typescript
// Now improve the code
// The test protects you from breaking things
class UserService {
  private readonly users: Map<string, User> = new Map();

  async create(data: CreateUserInput): Promise<User> {
    const user = User.create(data);
    this.users.set(user.id, user);
    return user;
  }
}

// Run the test - IT MUST STILL PASS
```

---

## The TDD Workflow

### Step 1: Understand the Requirement
```
Before writing any code:
1. What is the feature/behavior?
2. What are the inputs?
3. What are the expected outputs?
4. What are the edge cases?
```

### Step 2: Write the Test
```
The test describes the behavior you want:
- Given [initial state]
- When [action occurs]
- Then [expected result]
```

### Step 3: Watch It Fail
```
Run the test and confirm:
- It fails for the RIGHT reason
- The error message makes sense
- You understand what's missing
```

### Step 4: Write Minimal Code
```
Implement only what's needed to pass:
- No additional features
- No optimization
- No "while I'm here" improvements
```

### Step 5: Watch It Pass
```
Run the test and confirm:
- It passes
- Other tests still pass
- You didn't break anything
```

### Step 6: Refactor
```
Now improve the code:
- Extract functions
- Rename for clarity
- Optimize if needed
- Remove duplication

The tests protect you.
```

### Step 7: Repeat
```
Next behavior → Next test → Next cycle
```

---

## Test Categories

### Unit Tests
```
Test individual units in isolation.

SCOPE: Single function, class, or module
SPEED: Milliseconds
DEPENDENCIES: Mocked/stubbed
WHEN: Every code change

Example:
it('should validate email format', () => {
  expect(isValidEmail('test@example.com')).toBe(true);
  expect(isValidEmail('not-an-email')).toBe(false);
});
```

### Integration Tests
```
Test how units work together.

SCOPE: Multiple components interacting
SPEED: Seconds
DEPENDENCIES: Some real, some mocked
WHEN: Before commits

Example:
it('should save user to database', async () => {
  const user = await userService.create({ email: 'test@example.com' });
  const found = await userRepository.findById(user.id);
  expect(found).toEqual(user);
});
```

### End-to-End Tests
```
Test complete user flows.

SCOPE: Entire application
SPEED: Seconds to minutes
DEPENDENCIES: Real systems
WHEN: Before release

Example:
it('should complete user registration flow', async () => {
  await page.goto('/register');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'SecurePass123!');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL('/dashboard');
});
```

---

## Test Patterns

### Arrange-Act-Assert (AAA)
```typescript
it('should add items to cart', () => {
  // ARRANGE: Set up the test
  const cart = new ShoppingCart();
  const item = { id: '1', name: 'Widget', price: 9.99 };

  // ACT: Perform the action
  cart.addItem(item);

  // ASSERT: Verify the result
  expect(cart.items).toContain(item);
  expect(cart.total).toBe(9.99);
});
```

### Given-When-Then (BDD Style)
```typescript
describe('Shopping Cart', () => {
  describe('given an empty cart', () => {
    describe('when an item is added', () => {
      it('then the cart contains the item', () => {
        // ...
      });

      it('then the total reflects the item price', () => {
        // ...
      });
    });
  });
});
```

### Test Fixtures
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = createMockRepository();
    service = new UserService(mockRepository);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  // Tests use fresh fixtures each time
});
```

---

## What to Test

### The Testing Pyramid
```
           /\
          /  \
         / E2E \      (Few: Slow, expensive, broad)
        /______\
       /        \
      /Integration\   (Some: Medium speed, focused)
     /____________\
    /              \
   /   Unit Tests   \  (Many: Fast, cheap, specific)
  /__________________\
```

### Behavior, Not Implementation
```typescript
// BAD: Testing implementation details
it('should call repository.save with user object', () => {
  await service.createUser(userData);
  expect(repository.save).toHaveBeenCalledWith(expect.any(User));
});

// GOOD: Testing behavior
it('should persist user and return with id', async () => {
  const user = await service.createUser(userData);
  const found = await service.findById(user.id);
  expect(found).toEqual(user);
});
```

### Edge Cases
```typescript
describe('divide', () => {
  it('should divide two numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should throw on division by zero', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  it('should handle floating point', () => {
    expect(divide(1, 3)).toBeCloseTo(0.333, 2);
  });
});
```

---

## Common Pitfalls

### The Oracle Problem
```
PROBLEM: Tests that test themselves
EXAMPLE: expect(add(2, 2)).toBe(add(2, 2));
SOLUTION: Use concrete expected values
```

### Test Pollution
```
PROBLEM: Tests depend on each other or shared state
SOLUTION: Each test creates its own fixtures, cleanup after
```

### Over-Mocking
```
PROBLEM: Everything is mocked, testing mocks not reality
SOLUTION: Mock at boundaries, test real logic
```

### Fragile Tests
```
PROBLEM: Tests break when implementation changes
SOLUTION: Test behavior, not implementation
```

### Slow Tests
```
PROBLEM: Tests take too long, developers skip them
SOLUTION: Fast unit tests, fewer integration tests
```

---

## TDD Tips

### Start with the Simplest Test
```
Don't start with complex edge cases.
Start with the happy path.
Build complexity incrementally.
```

### One Assertion Per Test (Usually)
```
Each test should verify one behavior.
Multiple assertions are okay if testing one logical thing.
```

### Name Tests Clearly
```
WEAK: testUserCreate()
STRONG: should_create_user_with_valid_email()
         should_reject_user_with_invalid_email()
         should_assign_unique_id_to_new_user()
```

### Delete Bad Tests
```
Tests that frequently break for wrong reasons
Tests that don't catch bugs
Tests that are hard to understand
DELETE THEM. Bad tests are worse than no tests.
```

---

## Quick Reference

### TDD Checklist
```
□ Test written before code
□ Test fails first
□ Error message is clear
□ Minimum code written to pass
□ All tests pass
□ Code refactored
□ Tests still pass
□ Tests are readable
□ Tests are fast
□ Tests don't depend on each other
```

### Test Quality Criteria
```
□ Tests document behavior (can read to understand feature)
□ Tests catch bugs (when code breaks, tests fail)
□ Tests allow refactoring (can change implementation safely)
□ Tests run quickly (no excuse to skip them)
□ Tests are maintainable (easy to update when behavior changes)
```

---

*"The test is the specification made executable. Write the specification first, and the implementation reveals itself."*
