---
name: writing-tests
description: TypeScript testing conventions and TDD practices. Use when writing tests, fixing bugs, or organizing test files.
---

# Writing Tests

## File Organization

* 1:1 test file mapping: `foo.ts` → `foo.test.ts`
* `describe` blocks for each export (unless single export)
* No top-level describes repeating module name
* __Avoid redundant top-level describe blocks__ that repeat information already in the file path
  * Example: In `src/arr/traits/eq.test.ts`, don't use `describe('Arr.Eq implementation')` - the file path already indicates this
  * Focus describe blocks on behavior groupings, not restating what's being tested

## Test Quality

* Prefer property-based testing with fast-check
* Few high-impact tests over exhaustive coverage
* __Minimalist test fixtures__ - absolute minimum test cases needed. Quality over quantity.

## Grouping

__CRITICAL__: Use `Test.describe()` NOT comments for grouping:

```typescript
// ❌ BAD - inline comments for grouping
// Long flags
test('--verbose works', ...)
test('--quiet works', ...)

// ✅ GOOD - Test.describe for grouping
Test.describe('long flags', () => {
  test('--verbose works', ...)
  test('--quiet works', ...)
})
```

## TDD for Bug Fixes

__CRITICAL__: Before implementing ANY bug fix:

1. Create a failing unit test that reproduces the problem
2. Confirm it fails
3. Implement the fix
4. Confirm test passes

No exceptions - TDD is mandatory for bug fixes. Only skip for complex integration scenarios (e.g., massive deep state in Playwright browser tests).

## Before Using Test APIs

__READ THE JSDOC__ - Before using ANY test API, read the actual JSDoc documentation in the source code. Never guess the API signature. Find usage examples in the codebase if needed.
