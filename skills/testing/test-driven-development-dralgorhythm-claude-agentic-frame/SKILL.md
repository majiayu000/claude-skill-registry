---
name: test-driven-development
description: Write tests before implementation code. Use when starting new features or fixing bugs. Covers Red-Green-Refactor cycle and TDD best practices.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Test-Driven Development

## The TDD Cycle

1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

## Workflows

- [ ] **Write Test**: Write a test that describes desired behavior
- [ ] **Run Test**: Verify it fails (Red)
- [ ] **Implement**: Write minimal code to pass
- [ ] **Run Test**: Verify it passes (Green)
- [ ] **Refactor**: Clean up while tests stay green
- [ ] **Repeat**: Next test case

## TDD Example

### Step 1: Red - Write Failing Test

```typescript
describe("Calculator", () => {
  test("adds two numbers", () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5);
  });
});

// Run: FAIL - Calculator is not defined
```

### Step 2: Green - Minimal Implementation

```typescript
class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
}

// Run: PASS
```

### Step 3: Refactor (if needed)

Code is already clean, move to next test.

### Step 4: Next Test

```typescript
test("subtracts two numbers", () => {
  const calc = new Calculator();
  expect(calc.subtract(5, 3)).toBe(2);
});

// Run: FAIL - subtract is not defined
```

## TDD Benefits

- **Design Feedback**: Tests reveal design issues early
- **Documentation**: Tests document expected behavior
- **Confidence**: Refactor fearlessly with test safety net
- **Focus**: One behavior at a time

## TDD Tips

1. **Start Simple**: Begin with the simplest test case
2. **One Assert**: Each test should verify one behavior
3. **Descriptive Names**: Test names are documentation
4. **No Logic in Tests**: Tests should be obvious
5. **Fast Feedback**: Tests should run in milliseconds

## When to Use TDD

- New features with clear requirements
- Bug fixes (write failing test first)
- Complex business logic
- API contract development

## When TDD is Less Useful

- Exploratory/prototype code
- UI layout changes
- Simple CRUD operations
