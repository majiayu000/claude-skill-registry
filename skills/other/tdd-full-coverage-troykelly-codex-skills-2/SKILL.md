---
name: tdd-full-coverage
description: Use when implementing features or fixes - test-driven development with RED-GREEN-REFACTOR cycle and full code coverage requirement
---

# TDD Full Coverage

## Overview

Test-Driven Development with full code coverage.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Announce at start:** "I'm using TDD to implement this feature."

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before a test? Delete it. Start over.

## Red-Green-Refactor Cycle

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    ▼                                             │
┌───────┐     ┌───────┐     ┌──────────┐         │
│  RED  │────►│ GREEN │────►│ REFACTOR │─────────┘
└───────┘     └───────┘     └──────────┘
  Write         Write          Clean
  failing       minimal        up code
  test          code           (stay green)
```

### RED: Write Failing Test

Write ONE test for ONE behavior.

```typescript
// Test one specific thing
test('rejects empty email', async () => {
  const result = await validateEmail('');
  expect(result.valid).toBe(false);
  expect(result.error).toBe('Email is required');
});
```

### Verify RED: Watch It Fail

**MANDATORY. Never skip.**

```bash
pnpm test --grep "rejects empty email"
```

Confirm:
- Test FAILS (not errors)
- Fails for EXPECTED reason (feature missing, not typo)
- Error message is what you expect

If test passes → You're testing existing behavior. Fix the test.

### GREEN: Minimal Code

Write the SIMPLEST code to pass the test.

```typescript
function validateEmail(email: string): ValidationResult {
  if (!email) {
    return { valid: false, error: 'Email is required' };
  }
  return { valid: true };
}
```

Don't add:
- Error handling for cases you haven't tested
- Configuration options you don't need yet
- Optimizations

### Verify GREEN: Watch It Pass

**MANDATORY.**

```bash
pnpm test --grep "rejects empty email"
```

Confirm:
- Test PASSES
- All other tests still pass
- No errors or warnings

### REFACTOR: Clean Up

After green, improve code quality:
- Remove duplication
- Improve names
- Extract helpers

**Keep tests green during refactoring.**

### Repeat

Write next failing test for next behavior.

## Coverage Requirements

### Target: 100% for New Code

```bash
# Check coverage
pnpm test --coverage

# Verify new code is covered
# Lines: 100%
# Branches: 100%
# Functions: 100%
# Statements: 100%
```

### What 100% Means

| Covered | Not Covered (Fix It) |
|---------|---------------------|
| All branches tested | Some if/else paths missed |
| All functions called | Unused functions |
| All error handlers triggered | Error paths untested |
| All edge cases verified | Only happy path |

### Acceptable Exceptions

These MAY have lower coverage (discuss with team):

- Configuration files
- Type definitions only
- Auto-generated code
- Third-party integration code (mock at boundary)

Document exceptions in coverage config:

```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 100,
      functions: 100,
      lines: 100,
      statements: 100,
    },
  },
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/generated/',
    'config.ts',
  ],
};
```

## Integration Testing Against Local Services

**Core principle:** Unit tests with mocks are necessary but not sufficient. You MUST ALSO test against real services.

### The Two-Layer Testing Requirement

| Layer | Purpose | Uses Mocks? | Uses Real Services? |
|-------|---------|-------------|---------------------|
| **Unit Tests (TDD)** | Verify logic, enable RED-GREEN-REFACTOR | **YES** | No |
| **Integration Tests** | Verify real service behavior | No | **YES** |

**Both layers are REQUIRED.** Unit tests alone miss real-world failures. Integration tests alone are too slow for TDD.

### The Problem We're Solving

We've experienced **80% failure rates** with ORM migrations because:
- Unit tests with mocks pass
- Real database rejects the migration
- CI discovers the bug instead of local testing

**Mocks don't catch:** Schema mismatches, constraint violations, migration failures, connection issues, transaction behavior.

### When Integration Tests Are Required

| Code Change | Unit Tests (with mocks) | Integration Tests (with real services) |
|-------------|-------------------------|----------------------------------------|
| Database model/migration | ✅ Required | ✅ **Also required** |
| Repository/ORM layer | ✅ Required | ✅ **Also required** |
| Cache operations | ✅ Required | ✅ **Also required** |
| Pub/sub messages | ✅ Required | ✅ **Also required** |
| Queue workers | ✅ Required | ✅ **Also required** |

### Local Service Testing Protocol

After completing TDD cycle (unit tests with mocks):

1. **Ensure services are running** (`docker-compose up -d`)
2. **Run integration tests against real services**
3. **Verify migrations apply** (`pnpm migrate`)
4. **Verify in local environment before pushing**

### Example: Database Testing

```typescript
// LAYER 1: Unit tests with mocks (TDD cycle)
describe('UserRepository (unit)', () => {
  const mockDb = { query: jest.fn() };

  it('calls correct SQL for findById', async () => {
    mockDb.query.mockResolvedValue([{ id: 1, email: 'test@example.com' }]);
    const user = await userRepo.findById(1);
    expect(mockDb.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = $1', [1]);
  });
});

// LAYER 2: Integration tests with real postgres (ALSO required)
describe('UserRepository (integration)', () => {
  beforeAll(async () => {
    await db.migrate.latest();
  });

  it('actually persists and retrieves users', async () => {
    await userRepo.create({ email: 'test@example.com' });
    const user = await userRepo.findByEmail('test@example.com');
    expect(user).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  it('enforces unique email constraint', async () => {
    await userRepo.create({ email: 'unique@example.com' });
    // Real postgres will throw - mocks won't catch this
    await expect(
      userRepo.create({ email: 'unique@example.com' })
    ).rejects.toThrow(/unique constraint/);
  });
});
```

**Skill:** `local-service-testing`

## Test Quality

### Good Tests

```typescript
// GOOD: Clear name, tests one thing
test('calculates tax for positive amount', () => {
  const result = calculateTax(100, 0.08);
  expect(result).toBe(8);
});

test('returns zero tax for zero amount', () => {
  const result = calculateTax(0, 0.08);
  expect(result).toBe(0);
});

test('throws for negative amount', () => {
  expect(() => calculateTax(-100, 0.08)).toThrow('Amount must be positive');
});
```

### Bad Tests

```typescript
// BAD: Tests multiple things
test('calculateTax works', () => {
  expect(calculateTax(100, 0.08)).toBe(8);
  expect(calculateTax(0, 0.08)).toBe(0);
  expect(() => calculateTax(-100, 0.08)).toThrow();
});

// BAD: Tests mock, not real code
test('calls the tax service', () => {
  const mockTaxService = jest.fn().mockReturnValue(8);
  const result = calculateTax(100, 0.08);
  expect(mockTaxService).toHaveBeenCalled();  // Testing mock, not behavior
});
```

## Testing Patterns

### Arrange-Act-Assert

```typescript
test('description', () => {
  // Arrange - set up test data
  const user = createTestUser({ email: 'test@example.com' });
  const input = { userId: user.id, action: 'update' };

  // Act - perform the action
  const result = processAction(input);

  // Assert - verify the outcome
  expect(result.success).toBe(true);
  expect(result.timestamp).toBeDefined();
});
```

### Testing Errors

```typescript
test('throws for invalid input', () => {
  expect(() => validateInput(null)).toThrow(ValidationError);
  expect(() => validateInput(null)).toThrow('Input is required');
});

test('async throws for invalid input', async () => {
  await expect(asyncValidate(null)).rejects.toThrow(ValidationError);
});
```

### Testing Side Effects

```typescript
test('logs error on failure', async () => {
  const logSpy = jest.spyOn(logger, 'error');

  await processWithFailure();

  expect(logSpy).toHaveBeenCalledWith(
    expect.stringContaining('Failed to process')
  );
});
```

## Mocking Guidelines

### When to Mock

| Mock | Don't Mock |
|------|------------|
| External APIs | Your own code |
| Database (integration) | Simple functions |
| File system | Pure logic |
| Time/dates | Deterministic code |
| Network requests | Internal modules |

### Mock at Boundaries

```typescript
// GOOD: Mock the external boundary
const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
  new Response(JSON.stringify({ data: 'test' }))
);

// BAD: Mock internal implementation
const internalMock = jest.spyOn(utils, 'internalHelper');
```

## Debugging Test Failures

| Problem | Solution |
|---------|----------|
| Test passes when should fail | Check assertion (expect syntax) |
| Test fails unexpectedly | Check test isolation (cleanup) |
| Flaky tests | Remove timing dependencies |
| Hard to test | Improve code design |

## Checklist

Before completing a feature:

- [ ] Every function has at least one test
- [ ] Watched each test fail before implementing
- [ ] Each failure was for expected reason
- [ ] Wrote minimal code to pass
- [ ] All tests pass
- [ ] Coverage is 100% for new code
- [ ] No skipped tests
- [ ] Tests are isolated (no order dependency)
- [ ] Error cases are tested
- [ ] Integration tests ran against local services (not mocks)
- [ ] All service-dependent code verified locally

## Integration

This skill is called by:
- `issue-driven-development` - Step 7, 8, 11

This skill uses:
- `strict-typing` - Tests should be typed
- `inline-documentation` - Document test utilities

This skill ensures:
- Verified behavior
- Regression prevention
- Refactoring safety
- Documentation through tests
