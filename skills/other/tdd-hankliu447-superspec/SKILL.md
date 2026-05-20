---
name: tdd
description: |
  Use when implementing any feature or bugfix, before writing implementation code.
  Each Scenario in Specs becomes a test case following RED → GREEN → REFACTOR cycle.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**SuperSpec integration:** Every Scenario in specs/*.md becomes a TDD test case.

**Announce at start:** "I'm using the TDD skill to implement this feature."

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

## Scenario-to-Test Mapping

```
Spec Scenario                        TDD Test
═══════════════════════════════════════════════════════════════════
#### Scenario: Valid login       →   test('Valid login', () => {
- WHEN valid credentials              // WHEN - setup
- THEN grants access                  const result = login(valid);
                                      // THEN - assertion
                                      expect(result.granted).toBe(true);
                                    });
═══════════════════════════════════════════════════════════════════
```

## Red-Green-Refactor Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                      TDD Cycle                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐           │
│   │   RED   │ ──────▶ │  GREEN  │ ──────▶ │REFACTOR │           │
│   │  Write  │         │ Minimal │         │ Clean   │           │
│   │  Test   │         │  Code   │         │  Up     │           │
│   └────┬────┘         └────┬────┘         └────┬────┘           │
│        │                   │                    │                │
│        ▼                   ▼                    ▼                │
│   Verify FAILS        Verify PASSES       Stay GREEN            │
│   (correctly)         (all tests)         (tests pass)          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### RED - Write Failing Test

Write one minimal test based on a Scenario.

**Good:**
```typescript
// Based on: #### Scenario: Rejects empty email
test('Rejects empty email - returns error when email is empty', async () => {
  // WHEN user submits empty email
  const result = await submitForm({ email: '' });

  // THEN returns validation error
  expect(result.error).toBe('Email required');
});
```

**Bad:**
```typescript
test('email works', async () => {
  const mock = jest.fn().mockResolvedValue('ok');
  await submitForm(mock);
  expect(mock).toHaveBeenCalled();
});
// Vague name, tests mock not real behavior
```

**Requirements:**
- One behavior per test (matches one Scenario)
- Clear name (use Scenario name)
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write simplest code to pass the test.

**Good:**
```typescript
function submitForm(data: FormData) {
  if (!data.email?.trim()) {
    return { error: 'Email required' };
  }
  // ... rest of implementation
}
```

**Bad:**
```typescript
function submitForm(
  data: FormData,
  options?: {
    validate?: boolean;
    sanitize?: boolean;
    // YAGNI - not in Scenario
  }
) { ... }
```

Don't add features not in the Scenario.

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior not in Specs.

## Integration with SuperSpec

### Reading Specs First

Before implementing, read the Spec:
```bash
cat superspec/changes/[id]/specs/[capability]/spec.md
```

Identify:
- Requirements to implement
- Scenarios to test

### Commit with Spec Reference

```bash
git commit -m "feat([capability]): implement [scenario]

Refs: superspec/changes/[id]/specs/[capability]/spec.md
Requirement: [Name]
Scenario: [Name]"
```

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keep unverified code = technical debt. |
| "TDD will slow me down" | TDD faster than debugging. |
| "I'll mock it to make testing easier" | Mocks test your mocks, not your code. Use real implementations. |
| "Need test-only method for visibility" | If you need to expose internals, your design needs work. |
| "Integration tests are for later" | Integration issues found late are 10x harder to fix. |

## Red Flags - STOP and Start Over

- Code before test
- Test after implementation
- Test passes immediately
- Can't explain why test failed
- Rationalizing "just this once"
- "Tests after achieve the same purpose"
- Implementing features not in Scenarios

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:

- [ ] Every Scenario has a corresponding test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] No features outside of Specs
- [ ] Commits reference Spec/Requirement/Scenario

Can't check all boxes? You skipped TDD. Start over.

## TDD Evidence Requirement

When implementing via `superspec:execute`, you MUST provide TDD evidence:

```markdown
## TDD Evidence

### RED Phase (Test First)
**Test written:**
[Show the test code]

**Test run output (MUST FAIL):**
```
[Paste actual test output showing FAILURE]
```

### GREEN Phase (Implementation)
**Implementation:**
[Show the implementation code]

**Test run output (MUST PASS):**
```
[Paste actual test output showing PASS]
```
```

**If you cannot show this evidence, you did NOT follow TDD.**
- Delete your code
- Start over with test first
- This is NON-NEGOTIABLE

## Related References

**Load when needed:**
- `testing-anti-patterns.md` - Common testing mistakes and how to avoid them
  - Testing mock behavior instead of real behavior
  - Test-only methods in production code
  - Mocking without understanding
  - Incomplete mocks
  - Integration tests as afterthought
  - Testing implementation details

## Integration

**Called by:**
- `superspec:execute` - TDD is the implementation method (MANDATORY)
- `superspec:plan` - Plan structure follows TDD steps

**Pairs with:**
- `superspec:verify` - Verifies Spec-Test correspondence
- `systematic-debugging` - When tests fail unexpectedly
- `verification-before-completion` - Evidence before claims

**Enforcement:**
- Spec Reviewer verifies TDD evidence before approval
- Missing evidence = implementation rejected
- Code without failing test evidence must be deleted
