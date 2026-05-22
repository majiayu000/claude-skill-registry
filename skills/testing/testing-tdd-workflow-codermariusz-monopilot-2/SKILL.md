---
name: testing-tdd-workflow
description: Apply when implementing new features, fixing bugs, or refactoring code. TDD ensures tests drive design and all code is covered.
version: 1.0.0
tokens: ~600
confidence: high
sources:
  - https://martinfowler.com/bliki/TestDrivenDevelopment.html
  - https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [testing, tdd, workflow, methodology]
---

## When to Use

Apply when implementing new features, fixing bugs, or refactoring code. TDD ensures tests drive design and all code is covered.

## Patterns

### Pattern 1: Red-Green-Refactor Cycle
```
RED:     Write failing test (test what, not how)
GREEN:   Write minimal code to pass
REFACTOR: Improve code, keep tests green
REPEAT:  Next behavior
```
Source: https://martinfowler.com/bliki/TestDrivenDevelopment.html

### Pattern 2: Test Structure (AAA)
```typescript
// Source: https://martinfowler.com/bliki/GivenWhenThen.html
it('should calculate total with discount', () => {
  // Arrange (Given)
  const cart = new Cart();
  cart.add({ price: 100, quantity: 2 });

  // Act (When)
  const total = cart.calculateTotal(0.1); // 10% discount

  // Assert (Then)
  expect(total).toBe(180);
});
```

### Pattern 3: One Assertion Per Test
```typescript
// Source: https://blog.cleancoder.com/uncle-bob/2014/12/17/TheCyclesOfTDD.html
// GOOD: Single behavior per test
it('should add item to cart', () => {
  cart.add(item);
  expect(cart.items).toContain(item);
});

it('should update cart count', () => {
  cart.add(item);
  expect(cart.count).toBe(1);
});

// BAD: Multiple behaviors
it('should add item and update count', () => { /* multiple asserts */ });
```

### Pattern 4: Test Naming Convention
```typescript
// Format: should [expected behavior] when [condition]
describe('Cart', () => {
  it('should return 0 when cart is empty', () => {});
  it('should apply discount when code is valid', () => {});
  it('should throw error when quantity is negative', () => {});
});
```

### Pattern 5: Outside-In TDD
```
1. Start with acceptance test (user story)
2. Discover collaborators through failing test
3. Write unit tests for collaborators
4. Implement from inside out
5. Acceptance test passes
```
Source: https://martinfowler.com/bliki/TestDrivenDevelopment.html

## Anti-Patterns

- **Test after code** - Loses design benefits; tests become afterthought
- **Testing implementation** - Test behavior, not internal methods
- **Large test steps** - Keep RED-GREEN cycles small (minutes, not hours)
- **Skipping refactor** - Technical debt accumulates; refactor is mandatory

## Verification Checklist

- [ ] Test written BEFORE implementation
- [ ] Test fails for the right reason (RED)
- [ ] Minimal code written to pass (GREEN)
- [ ] Code refactored, tests still pass
- [ ] Each test covers one behavior
- [ ] Test names describe expected behavior
