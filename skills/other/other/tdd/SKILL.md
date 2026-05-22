---
name: tdd
description: Test-Driven Development workflow - write tests first, then implementation
---

# Test-Driven Development (TDD)

Follow the Red-Green-Refactor cycle strictly. Never write production code without a failing test first.

## The TDD Cycle

```
┌─────────────────────────────────────────┐
│                                         │
│    ┌───────┐                           │
│    │  RED  │ Write a failing test      │
│    └───┬───┘                           │
│        │                               │
│        ▼                               │
│    ┌───────┐                           │
│    │ GREEN │ Write minimal code to pass│
│    └───┬───┘                           │
│        │                               │
│        ▼                               │
│    ┌──────────┐                        │
│    │ REFACTOR │ Improve without        │
│    └────┬─────┘ breaking tests         │
│         │                              │
│         └──────────────────────────────┘
```

## Rules (Non-Negotiable)

1. **No production code without a failing test**
   - Write the test first
   - Watch it fail
   - Only then write implementation

2. **Write the minimum test to fail**
   - One assertion per test
   - Test behavior, not implementation
   - Start with the simplest case

3. **Write the minimum code to pass**
   - Don't anticipate future needs
   - Hardcode if that makes it pass
   - Generalize only when forced by tests

4. **Refactor only when green**
   - All tests must pass before refactoring
   - Keep tests passing during refactoring
   - Small steps only

## Workflow

### Phase 1: RED (Write Failing Test)

```typescript
// Start with what you want the API to look like
describe('Calculator', () => {
  it('should add two numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});
```

Run test → Watch it fail → Confirm it fails for the RIGHT reason

### Phase 2: GREEN (Make It Pass)

```typescript
// Write the SIMPLEST code that passes
class Calculator {
  add(a: number, b: number): number {
    return 5; // Yes, hardcoding is fine here!
  }
}
```

Run test → Watch it pass → Celebrate (briefly)

### Phase 3: Add Another Test (Force Generalization)

```typescript
it('should add different numbers', () => {
  const calc = new Calculator();
  expect(calc.add(1, 1)).toBe(2); // Forces real implementation
});
```

### Phase 4: GREEN Again

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b; // Now we generalize
  }
}
```

### Phase 5: REFACTOR

With green tests, improve the code:
- Remove duplication
- Improve names
- Extract methods
- Keep tests green throughout

## Test Naming Convention

Use this pattern: `should [expected behavior] when [condition]`

```typescript
it('should return empty array when input is null')
it('should throw ValidationError when email is invalid')
it('should retry 3 times when connection fails')
```

## TDD Checklist

Before writing ANY code, verify:

- [ ] I have a failing test
- [ ] The test fails for the expected reason
- [ ] The test is testing behavior, not implementation
- [ ] The test name describes what it verifies

Before marking GREEN:

- [ ] Test passes
- [ ] I wrote the minimum code necessary
- [ ] I didn't add "extra" functionality

Before REFACTORING:

- [ ] All tests are green
- [ ] I have a specific improvement in mind
- [ ] Changes are small and incremental

## Common TDD Mistakes

### ❌ Writing Tests After Code
This is not TDD. Tests written after tend to test implementation, not behavior.

### ❌ Writing Too Many Tests at Once
Write ONE test, make it pass, then write the next. Stay in the cycle.

### ❌ Making Big Jumps
If your implementation is more than a few lines, you skipped steps. Add intermediate tests.

### ❌ Testing Implementation Details
```typescript
// BAD - tests implementation
expect(user._hashedPassword).toMatch(/^[a-f0-9]{64}$/);

// GOOD - tests behavior
expect(user.verifyPassword('correct')).toBe(true);
```

### ❌ Refactoring While Red
Never refactor with failing tests. Get green first.

## Starting a New Feature with TDD

1. List behaviors the feature needs (user stories → test cases)
2. Order from simplest to most complex
3. Write first test for simplest behavior
4. Cycle through Red-Green-Refactor
5. Add tests for edge cases
6. Add tests for error handling

## Example Session

**Goal:** Implement a `slugify` function

```typescript
// Test 1: Simplest case
it('should lowercase the input', () => {
  expect(slugify('Hello')).toBe('hello');
});
// Implementation: return input.toLowerCase();

// Test 2: Handle spaces
it('should replace spaces with hyphens', () => {
  expect(slugify('Hello World')).toBe('hello-world');
});
// Implementation: return input.toLowerCase().replace(/ /g, '-');

// Test 3: Handle special characters
it('should remove special characters', () => {
  expect(slugify('Hello, World!')).toBe('hello-world');
});
// Implementation: add .replace(/[^a-z0-9-]/g, '');

// Test 4: Edge case
it('should handle empty string', () => {
  expect(slugify('')).toBe('');
});
// Already passes! No change needed.
```

## Remember

> "TDD is not about testing. It's about design."

The tests drive you toward better, more modular code. Trust the process.
