---
name: tdd-workflow
description: >
  Red-green-refactor TDD cycle, test-first methodology, coverage targets (80%+),
  and test pyramid. Use when the user is implementing a new feature, fixing a bug,
  asks about TDD, or mentions writing tests before code. Always push for test-first.
---

# TDD Workflow

Test-Driven Development means writing a failing test before writing implementation code. This ensures every feature has coverage and drives cleaner design through the red-green-refactor cycle.

## When to Use
- User is implementing a new feature (push for test-first)
- User is fixing a bug (write a test that reproduces the bug first)
- User asks about TDD or test-driven development
- User asks how to structure tests
- Coverage is below 80% and needs improvement

## Core Patterns

### The Red-Green-Refactor Cycle

```
  RED: Write a failing test
   |
   v
  GREEN: Write minimal code to pass
   |
   v
  REFACTOR: Clean up without changing behavior
   |
   v
  (repeat)
```

### Step 1: RED — Write a Failing Test

Write the test first. It must fail because the implementation does not exist yet:

```typescript
// src/utils/slug.test.ts
import { describe, it, expect } from 'vitest'
import { createSlug } from './slug'

describe('createSlug', () => {
  it('converts a title to a URL-safe slug', () => {
    expect(createSlug('Hello World')).toBe('hello-world')
  })

  it('removes special characters', () => {
    expect(createSlug('Hello & World!')).toBe('hello-world')
  })

  it('collapses multiple hyphens', () => {
    expect(createSlug('Hello   World')).toBe('hello-world')
  })

  it('trims leading and trailing hyphens', () => {
    expect(createSlug(' Hello World ')).toBe('hello-world')
  })
})
```

Run the test — it must FAIL:

```bash
npx vitest run src/utils/slug.test.ts
# FAIL: Cannot find module './slug'
```

### Step 2: GREEN — Minimal Implementation

Write the minimum code to make all tests pass:

```typescript
// src/utils/slug.ts
export function createSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
}
```

Run the test — it must PASS:

```bash
npx vitest run src/utils/slug.test.ts
# PASS: All 4 tests passed
```

### Step 3: REFACTOR — Improve Without Changing Behavior

Clean up the implementation while keeping all tests green:

```typescript
// src/utils/slug.ts (refactored)
const SPECIAL_CHARS = /[^a-z0-9\s-]/g
const WHITESPACE = /\s+/g
const MULTIPLE_HYPHENS = /-+/g
const EDGE_HYPHENS = /^-|-$/g

export function createSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(SPECIAL_CHARS, '')
    .replace(WHITESPACE, '-')
    .replace(MULTIPLE_HYPHENS, '-')
    .replace(EDGE_HYPHENS, '')
}
```

Run tests again to confirm nothing broke:

```bash
npx vitest run src/utils/slug.test.ts
# PASS: All 4 tests passed
```

### Bug Fix TDD

For bug fixes, write a test that reproduces the bug first:

```typescript
// 1. Bug report: createSlug crashes on empty string

// 2. RED: Write test that demonstrates the bug
it('handles empty string', () => {
  expect(createSlug('')).toBe('')
})

// 3. Run test — confirms the bug exists (FAIL or unexpected behavior)

// 4. GREEN: Fix the implementation
export function createSlug(title: string): string {
  if (!title) return ''
  // ... rest of implementation
}

// 5. Run test — bug is fixed (PASS)
```

### Test Pyramid

Structure tests by scope and speed:

```
        /  E2E  \          Few, slow, high-value
       /----------\        (Playwright, Cypress)
      / Integration \      Moderate count, medium speed
     /----------------\    (API tests, DB tests)
    /    Unit Tests     \  Many, fast, focused
   /----------------------\ (Vitest, Jest, pytest)
```

Coverage targets by layer:

| Layer | Target | Speed | Count |
|-------|--------|-------|-------|
| Unit | 80%+ line coverage | < 1s each | Many |
| Integration | Key workflows | < 5s each | Moderate |
| E2E | Critical paths | < 30s each | Few |

### Coverage Verification

Check coverage after each TDD cycle:

```bash
# Vitest
npx vitest run --coverage

# Jest
npx jest --coverage

# pytest
python -m pytest --cov=src --cov-report=term-missing
```

Target 80% minimum overall. Focus on:
- All public functions/methods
- All error paths
- All edge cases (empty input, null, boundary values)

### TDD for API Endpoints

```typescript
// 1. RED: Write the integration test
describe('POST /api/users', () => {
  it('creates a user and returns 201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })

    expect(response.status).toBe(201)
    expect(response.body.data.email).toBe('test@example.com')
  })

  it('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'not-an-email', name: 'Test' })

    expect(response.status).toBe(400)
    expect(response.body.error).toContain('email')
  })
})

// 2. GREEN: Implement route, validation, and handler
// 3. REFACTOR: Extract validation schema, clean up handler
```

## Anti-Patterns

- **Writing tests after implementation**: This is "test-after" not TDD. Tests written after code tend to test the implementation rather than the behavior, and they always pass on first run — so you never see RED.
- **Skipping the RED step**: If your test passes on the first run, either the feature already exists or the test is wrong. A passing new test is suspicious.
- **Over-implementing in GREEN**: Write the minimum to pass, not the "best" solution. Optimization comes in REFACTOR. Minimal GREEN keeps you honest about what the tests actually require.
- **Skipping REFACTOR**: Going RED-GREEN-RED-GREEN without refactoring accumulates technical debt. Always clean up after GREEN.
- **Testing implementation details**: Test behavior (what), not implementation (how). `expect(result).toBe('hello-world')` is good. `expect(internalRegex).toHaveBeenCalled()` is brittle.
- **Fixing tests to match broken code**: If a test fails after a code change, the code is probably wrong, not the test. Fix the implementation first.

## Quick Reference

```
1. RED:      Write test -> Run -> Must FAIL
2. GREEN:    Write minimal code -> Run -> Must PASS
3. REFACTOR: Clean up -> Run -> Must still PASS
4. COVERAGE: Check -> Must be 80%+
5. REPEAT
```

**Bug fixes**: Always reproduce with a test first.
**New features**: Always write the test before the implementation.
**Coverage**: 80% minimum. Check with `--coverage` flag.
**Pyramid**: Many unit tests, moderate integration, few E2E.
