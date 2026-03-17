---
name: test-driven-development
description: Red-green-refactor development methodology requiring verified test coverage. Use for feature implementation, bugfixes, refactoring, or any behavior changes where tests must prove correctness.
---

# Test-Driven Development

Write test first. Watch it fail. Write minimal code to pass. Refactor.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO BEHAVIOR-CHANGING PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before test? Delete it completely. Implement fresh from tests.

**Refactoring is exempt:** The refactor step changes structure, not behavior. Tests stay green throughout. No new failing test required.

## Red-Green-Refactor Cycle

```
RED ──► Verify Fail ──► GREEN ──► Verify Pass ──► REFACTOR ──► Verify Pass ──► Next RED
         │                         │                            │
         ▼                         ▼                            ▼
      Wrong failure?           Still failing?              Broke tests?
      Fix test, retry          Fix code, retry             Fix, retry
```

### RED - Write Failing Test

Write one minimal test for one behavior.

**Good example:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = async () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
*Clear name, tests real behavior, asserts observable outcome*

**Bad example:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
*Vague name, asserts only call count without verifying outcome, tests mock mechanics not behavior*

**Requirements:** One behavior. Clear name. Real code (mocks only if unavoidable).

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

Test must go red for the right reason. Acceptable RED states:
- Assertion failure (expected behavior missing)
- Compile/type error (function doesn't exist yet)

Not acceptable: Runtime setup errors, import failures, environment issues.

Test passes immediately? You're testing existing behavior—fix test.
Test errors for wrong reason? Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**Good example:**
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
*Just enough to pass*

**Bad example:**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: { maxRetries?: number; backoff?: 'linear' | 'exponential'; }
): Promise<T> { /* YAGNI */ }
```
*Over-engineered beyond test requirements*

Write only what the test demands. No extra features, no "improvements."

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm: Test passes. All other tests still pass. Output pristine (no errors, warnings).

Test fails? Fix code, not test.
Other tests fail? Fix now before continuing.

### REFACTOR - Clean Up

After green only: Remove duplication. Improve names. Extract helpers.

Keep tests green throughout. Add no new behavior.

### Repeat

Next failing test for next behavior.

## Good Tests

**Minimal:** One thing per test. "and" in name? Split it. ❌ `test('validates email and domain and whitespace')`

**Clear:** Name describes behavior. ❌ `test('test1')`

**Shows intent:** Demonstrates desired API usage, not implementation details.

## Example: Bug Fix

**Bug:** Empty email accepted

**RED:**
```typescript
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});
```

**Verify RED:**
```bash
$ npm test
FAIL: expected 'Email required', got undefined
```

**GREEN:**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}
```

**Verify GREEN:**
```bash
$ npm test
PASS
```

**REFACTOR:** Extract validation helper if pattern repeats.

## Red Flags - STOP and Start Over

Any of these means delete code and restart with TDD:

- Code written before test
- Test passes immediately (testing existing behavior)
- Can't explain why test failed
- Rationalizing "just this once" or "this is different"
- Keeping code "as reference" while writing tests
- Claiming "tests after achieve the same purpose"

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the API you wish existed. Write assertion first. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Introduce dependency injection. |
| Test setup huge | Extract helpers. Still complex? Simplify design. |

## Legacy Code (No Existing Tests)

The Iron Law ("delete and restart") applies to **new code you wrote without tests**. For inherited code with no tests, use characterization tests:

1. Write tests that capture current behavior (even if "wrong")
2. Run tests, observe actual outputs
3. Update assertions to match reality (these are "golden masters")
4. Now you have a safety net for refactoring
5. Apply TDD for new behavior changes

Characterization tests lock down existing behavior so you can refactor safely. They're the on-ramp, not a permanent state.

## Flakiness Rules

Tests must be deterministic. Ban these in unit tests:

- **Real sleeps / delays** → Use fake timers (`vi.useFakeTimers()`, `jest.useFakeTimers()`)
- **Wall clock time** → Inject clock, assert against injected time
- **Math.random()** → Seed or inject RNG
- **Network calls** → Mock at boundary or use MSW
- **Filesystem race conditions** → Use temp dirs with unique names

Flaky test? Fix or delete. Flaky tests erode trust in the entire suite.

## Debugging Integration

Bug found? Write failing test reproducing it first. Then follow TDD cycle. Test proves fix and prevents regression.

## Planning: Test List

Before diving into the cycle, spend 2 minutes listing the next 3-10 tests you expect to write. This prevents local-optimum design where early tests paint you into a corner.

Example test list for a retry function:
- retries N times on failure
- returns result on success
- throws after max retries exhausted  
- calls onRetry callback between attempts
- respects backoff delay

Work through the list in order. Add/remove tests as you learn.

## Testing Anti-Patterns

When writing tests involving mocks, dependencies, or test utilities: See [references/testing-anti-patterns.md](references/testing-anti-patterns.md) for common pitfalls including testing mock behavior and adding test-only methods to production classes.

## Philosophy and Rationalizations

For detailed rebuttals to common objections ("I'll test after", "deleting work is wasteful", "TDD is dogmatic"): See [references/tdd-philosophy.md](references/tdd-philosophy.md)

## Final Rule

```
Production code exists → test existed first and failed first
Otherwise → not TDD
```
