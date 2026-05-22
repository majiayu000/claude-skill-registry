---
name: "Testing Strategy"
description: "Apply TDD with RED-GREEN-REFACTOR cycles, separate unit tests from integration tests, ensure comprehensive coverage. Apply when writing tests, evaluating test coverage, testing databases, or testing admin flows."
allowed-tools: Read, Write, Edit, Bash
version: 2.1.0
compatibility: Claude Opus 4.5, Claude Code v2.x
updated: 2026-01-24
---

# Testing Strategy

Systematic TDD workflow ensuring comprehensive test coverage following RED-GREEN-REFACTOR cycles.

## Overview

This Skill enforces:
- RED-GREEN-REFACTOR cycles (TDD)
- Atomic test coverage
- Separation of logic from database tests (T-3)
- E2E testing for critical admin flows (T-7)
- Edge case coverage (T-8)

Apply when writing tests, designing test suites, or evaluating coverage.

## RED-GREEN-REFACTOR Workflow

**Every feature follows this cycle**:

### RED Phase: Write Failing Test

Write test BEFORE implementation:

```ts
import { describe, test, expect } from 'vitest';
import { validateEmail } from './email';

describe('validateEmail', () => {
  test('returns true for valid email', () => {
    expect(validateEmail('user@example.com')).toBe(true);
  });

  test('returns false for missing @', () => {
    expect(validateEmail('userexample.com')).toBe(false);
  });

  test('returns false for empty string', () => {
    expect(validateEmail('')).toBe(false);
  });
});
```

Run: `pnpm test validateEmail` → **FAILS** (RED)

### GREEN Phase: Make Test Pass

Write minimal code to pass:

```ts
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

Run: `pnpm test validateEmail` → **PASSES** (GREEN)

### REFACTOR Phase: Improve Code

Improve without changing behavior:

```ts
// Extract pattern for readability
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function validateEmail(email: string): boolean {
  return EMAIL_PATTERN.test(email);
}
```

Run: `pnpm test validateEmail` → **STILL PASSES** (verify before claiming done)

## Test Organization

### T-1 (MUST): Colocate Tests with Source

```
src/utils/validators.ts
src/utils/validators.spec.ts      ← Same directory
```

### T-3 (MUST): Separate Logic from Database Tests

**Unit Tests** (pure logic, no database):

```ts
// src/utils/helpers.spec.ts
describe('calculateTotal', () => {
  test('sums array correctly', () => {
    const result = calculateTotal([10, 20, 30]);
    expect(result).toBe(60);
  });

  test('handles empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

**Integration Tests** (with database):

```ts
// server/tests/user-api.test.ts
describe('User API', () => {
  beforeEach(async () => {
    await db.clear('users');
  });

  test('creates user in database', async () => {
    const user = await createUser({
      email: 'test@example.com',
      name: 'Test User'
    });

    const retrieved = await db.users.findById(user.id);
    expect(retrieved).toEqual(user);
  });
});
```

### Anti-Pattern: Mixed Tests

```ts
// ❌ BAD: Mixes logic and database
describe('calculateTotal', () => {
  test('calculates and saves', async () => {
    const result = calculateTotal([10, 20, 30]);
    await db.totals.save(result);  // Don't mix!
    expect(result).toBe(60);
  });
});
```

## Test Coverage Requirements

**By Feature Type**:

- **Utilities** (formatting, validation): 80%+ coverage
- **Business Logic** (algorithms, rules): 90%+ coverage
- **Admin Flows** (user management): 100% coverage (T-7)
- **Public APIs** (REST endpoints): 90%+ coverage

Check coverage:

```bash
pnpm test --coverage
```

## Unit Test Patterns

### Pattern 1: Simple Function

```ts
// ✅ GOOD: Complete test
test('returns true for valid email format', () => {
  expect(validateEmail('user@example.com')).toBe(true);
});

// ❌ BAD: Unclear what's being tested
test('validates email', () => {
  expect(validateEmail('user@example.com')).toBe(true);
});
```

### Pattern 2: Edge Cases (T-8)

```ts
// ✅ GOOD: Covers boundaries
describe('calculateDiscount', () => {
  test('returns 0% for purchases under $100', () => {
    expect(calculateDiscount(99.99)).toBe(0);
  });

  test('returns 10% for purchases >= $100', () => {
    expect(calculateDiscount(100)).toBe(10);
    expect(calculateDiscount(100.01)).toBe(10.001);
  });

  test('handles edge cases', () => {
    expect(calculateDiscount(0)).toBe(0);      // Zero
    expect(calculateDiscount(-50)).toBe(0);    // Negative
    expect(calculateDiscount(999999)).toBe(99999.9);  // Large
  });
});
```

### Pattern 3: Parameterized Tests

```ts
// ✅ GOOD: No magic literals
test.each([
  ['user@example.com', true],
  ['invalid.email', false],
  ['', false],
  ['user@domain.co.uk', true]
])('validateEmail("%s") returns %p', (email, expected) => {
  expect(validateEmail(email)).toBe(expected);
});
```

### Pattern 4: Entire Structure Assertion

**T-1 (MUST)**: Compare entire result, not individual fields:

```ts
// ✅ GOOD: Complete structure
const result = createUser({ name: 'Alice', email: 'alice@example.com' });
expect(result).toEqual({
  id: expect.any(String),
  name: 'Alice',
  email: 'alice@example.com',
  createdAt: expect.any(Date)
});

// ❌ BAD: Separate assertions
expect(result).toHaveProperty('id');
expect(result.name).toBe('Alice');
expect(result.email).toBe('alice@example.com');
```

## Anti-Patterns

Avoid these:

```ts
// ❌ Testing implementation details
test('caches value internally', () => {
  const cache = getInternalCache();
  expect(cache).toContain('value');
});

// ❌ Trivial assertions
test('2 equals 2', () => {
  expect(2).toBe(2);
});

// ❌ Magic numbers
test('total calculation', () => {
  expect(calculateTotal([10, 20, 30])).toBe(60);
  // What do 10, 20, 30 represent?
});

// ❌ Testing type checker conditions
test('rejects null', () => {
  // @ts-expect-error - Testing invalid input
  expect(validateEmail(null)).toBe(false);
});

// ❌ Mixing async and sync confusingly
test('async function', () => {
  const result = fetchUser('123');
  expect(result).toBe(user);  // Wrong! result is Promise
});
```

## Integration Test Patterns

### Testing APIs

```ts
describe('POST /api/users', () => {
  test('creates user with valid input', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@example.com' })
      .expect(201);

    expect(response.body).toEqual({
      id: expect.any(String),
      name: 'Alice',
      email: 'alice@example.com'
    });
  });

  test('returns 400 for missing required fields', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Alice' })
      .expect(400);

    expect(response.body.error).toContain('Email required');
  });

  test('returns 409 for duplicate email', async () => {
    await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@example.com' });

    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Bob', email: 'alice@example.com' })
      .expect(409);

    expect(response.body.error).toContain('already exists');
  });
});
```

### Testing Database Operations

```ts
describe('User model', () => {
  beforeEach(async () => {
    await db.connect();
    await db.clear('users');
  });

  afterEach(async () => {
    await db.disconnect();
  });

  test('creates and retrieves user', async () => {
    const user = await User.create({
      name: 'Alice',
      email: 'alice@example.com'
    });

    const retrieved = await User.findById(user.id);
    expect(retrieved).toEqual(user);
  });

  test('enforces unique email constraint', async () => {
    await User.create({ name: 'Alice', email: 'alice@example.com' });

    await expect(
      User.create({ name: 'Bob', email: 'alice@example.com' })
    ).rejects.toThrow('Unique constraint');
  });
});
```

## E2E Test Patterns

### Critical Admin Flows (T-7)

E2E test all critical admin workflows:

```ts
import { test, expect } from '@playwright/test';

test.describe('Admin User Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login as admin
    await page.goto('/login');
    await page.fill('input[name="email"]', 'admin@company.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button:has-text("Login")');
    await page.waitForURL('/admin/dashboard');
  });

  test('creates new user', async ({ page }) => {
    await page.click('a:has-text("Users")');
    await page.click('button:has-text("New User")');
    await page.fill('input[name="name"]', 'John Doe');
    await page.fill('input[name="email"]', 'john@company.com');
    await page.click('button:has-text("Create")');

    await page.waitForSelector('text=User created');
    await expect(page).toContainText('john@company.com');
  });

  test('deletes user with confirmation', async ({ page }) => {
    await page.click('a:has-text("Users")');
    await page.click('[data-test="delete-btn"]');

    // Must require confirmation (U-5)
    await expect(page).toContainText('Are you sure?');
    await page.click('button:has-text("Confirm")');

    await page.waitForSelector('text=User deleted');
  });

  test('prevents accidental deletion', async ({ page }) => {
    await page.click('a:has-text("Users")');
    await page.click('[data-test="delete-btn"]');
    await page.click('button:has-text("Cancel")');

    // User should still exist
    await expect(page).not.toContainText('User deleted');
  });
});
```

## Verification Before Completion

Before marking tests complete:

- [ ] **RED phase**: Watched tests fail first
- [ ] **GREEN phase**: Tests pass with minimal code
- [ ] **REFACTOR phase**: Improved code quality
- [ ] **Verify again**: All tests still pass
- [ ] Edge cases covered (null, empty, zero, negative, large values)
- [ ] Pure logic separated from database operations
- [ ] Coverage meets minimum requirements
- [ ] No trivial assertions (avoid `expect(true).toBe(true)`)
- [ ] Tests colocated with source code
- [ ] E2E tests for critical admin flows

## Running Tests

```bash
# All tests
pnpm test

# Watch mode (rerun on change)
pnpm test --watch

# Specific file
pnpm test src/utils/helpers.spec.ts

# Coverage report
pnpm test --coverage

# Verbose output
pnpm test --reporter=verbose
```

## Integration with CLAUDE.md

Enforces CLAUDE.md Section 3:
- **T-1**: Tests colocated with source
- **T-2**: API changes have integration tests
- **T-3**: Separate logic from database tests
- **T-7**: E2E tests for admin flows
- **T-8**: Edge cases tested
- **T-9**: Redundant tests better than missing coverage
- **T-10**: RED-GREEN-REFACTOR cycle
---

**Last Updated:** January 24, 2026
**Compatibility:** Claude Opus 4.5, Claude Code v2.x
**Status:** Production Ready

> **January 2026 Update:** This skill is compatible with Claude Opus 4.5 and Claude Code v2.x. For complex tasks, use the `effort: high` parameter for thorough analysis.
