---
name: tdd-mastery
description: Test-Driven Development Iron Law. Write the test first. Watch it fail. Write minimal code to pass. No exceptions.
---

<domain_overview>
# 🧪 TDD MASTERY: THE IRON LAW

> **Philosophy:** If you didn't watch the test fail, you don't know if it tests the right thing. TDD is not optional—it's the foundation of trustworthy code.
**TEST-FIRST INTEGRITY MANDATE (CRITICAL):** Never write production code before a test exists and has been seen failing. AI-generated code often attempts to write implementation and tests simultaneously or implementation first. You MUST strictly adhere to the Red-Green-Refactor cycle. Any code submitted without a preceding failing test or that generates tests after the implementation must be rejected as "Legacy Code on Arrival".

---

## 🚨 THE IRON LAW

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.
</domain_overview>
<core_workflow>
## 🔴 RED-GREEN-REFACTOR CYCLE

### Phase 1: RED - Write Failing Test

Write one minimal test showing what should happen.

**Good Example:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
*Clear name, tests real behavior, one thing*

**Bad Example:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(2);
});
```
*Vague name, tests mock not code*

**Requirements:**
- One behavior per test
- Clear, descriptive name
- Real code (mocks only if unavoidable)

### Phase 2: VERIFY RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
# or
pytest tests/path/test.py::test_name -v
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### Phase 3: GREEN - Minimal Code

Write **simplest code** to pass the test.

**Good:**
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

**Bad:**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> {
  // YAGNI - You Aren't Gonna Need It
}
```
*Over-engineered*

Don't add features, refactor other code, or "improve" beyond the test.

### Phase 4: VERIFY GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### Phase 5: REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Phase 6: COMMIT

```bash
git add tests/path/test.ts src/path/file.ts
git commit -m "feat: add specific feature with tests"
```

**Repeat** for next behavior.

---
</core_workflow>

<quality_standards>
## 📋 GOOD TEST QUALITIES

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |
| **Real behavior** | Tests actual code | Tests mock behavior |

---

## 🚫 COMMON RATIONALIZATIONS (ALL INVALID)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is debt. |
| "Keep as reference" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = skip test" | Hard to test = hard to use. Simplify design. |
| "TDD will slow me down" | TDD faster than debugging. Pragmatic = test-first. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

---

## 🚨 RED FLAGS - STOP AND START OVER

If you catch yourself:
- Writing code before test
- Test passes immediately
- Can't explain why test failed
- Tests added "later"
- "Just this once"
- "I already manually tested it"
- "Keep as reference"
- "TDD is dogmatic, I'm being pragmatic"

**ALL of these mean: Delete code. Start over with TDD.**

---
</quality_standards>

<bug_fix_protocol>
## 🐛 BUG FIX WORKFLOW

Bug found? Write failing test reproducing it. Follow TDD cycle.

**Example:**
```
Bug: Empty email accepted

RED:
test('rejects empty email', async () => {
  const result = await submitForm({ email: '' });
  expect(result.error).toBe('Email required');
});

VERIFY RED:
$ npm test
FAIL: expected 'Email required', got undefined

GREEN:
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ...
}

VERIFY GREEN:
$ npm test
PASS
```

**Never fix bugs without a test.**

---
</bug_fix_protocol>

<integration_and_tooling>
## 🔗 RALPH WIGGUM INTEGRATION

When Ralph Wiggum is active:

1. **Before ANY implementation:** Write failing test first
2. **Proactive Gate:** Check edge cases BEFORE coding (use TDD to cover them)
3. **Reflection Loop:** After implementation, verify RED-GREEN was followed
4. **Verification Matrix:** Track test coverage for each feature

**Ralph Wiggum will REJECT:**
- Code without corresponding tests
- Tests that were written after code
- Tests that pass without implementation

---

## ✅ VERIFICATION CHECKLIST

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

---

## 🛠️ TESTING INFRASTRUCTURE

### Stack Detection & Tool Setup

Auto-detect project type and setup appropriate tools:

| Project Type | Required Tools |
|--------------|----------------|
| **Frontend (Vite/React)** | `vitest` + `playwright` |
| **Fullstack (Next.js)** | `vitest` + `playwright` |
| **Backend (Node)** | `vitest` or `jest` |
| **Python** | `pytest` + `pytest-cov` |
| **Microservices** | `MSW` (Mock Service Worker) |

### Test Coverage Rules

For every new function/component, generate:
- **1 Happy Path** - Expected successful behavior
- **2 Edge Cases** - Boundary conditions, invalid inputs
- **1 Error Case** - Expected failure handling

### Contract-First (MSW)

**Rule:** Every frontend-backend interaction MUST have an MSW handler.

```typescript
// Example MSW handler
import { http, HttpResponse } from 'msw'

export const handlers = [
  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'Test User'
    })
  })
]
```

**Benefit:** Decouples frontend development from backend availability.

### Ghost Inspector Protocol

AI must scan for "Untested Logic Slabs" (>20 lines without coverage) and flag them:

```bash
# Check coverage gaps
npm run test -- --coverage
# Look for files with <80% coverage
```

---
</integration_and_tooling>

<reference_and_audit>
## 📖 RELATED SKILLS

- **@testing-anti-patterns.md** - Common mock/test mistakes to avoid
- **@clean-code** - Code quality standards
- **@verification-mastery** - Evidence before completion claims
- **@debug-mastery** - When tests reveal bugs

---

## 🏁 FINAL RULE

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without explicit user permission.
</reference_and_audit>
