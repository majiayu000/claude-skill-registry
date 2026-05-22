---
name: tdd
description: >
  Use when implementing any feature or fix outside code-forge workflow — enforces
  Red-Green-Refactor cycle with mandatory test-first discipline. For ad-hoc development,
  quick fixes, or any code change that is not tracked by code-forge:impl.
---

# Code Forge — TDD

Standalone Test-Driven Development enforcement for any code change.

## When to Use

- Writing code outside of code-forge:impl workflow (ad-hoc changes, quick fixes)
- Any new feature, bug fix, or behavior change that needs test discipline
- When you catch yourself about to write production code without a test

**Note:** code-forge:impl already enforces TDD internally. This skill is for work outside that workflow.

## Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

No exceptions. Not for "simple" changes. Not for "obvious" fixes. Not when under time pressure.

## Workflow

```
RED (write failing test) → VERIFY RED → GREEN (minimal code) → VERIFY GREEN → REFACTOR → REPEAT
```

## The Cycle

Complete each phase fully before moving to the next.

### 1. RED — Write a Failing Test

- One minimal test showing the desired behavior
- Clear, descriptive test name
- Use real code, not mocks (unless unavoidable: external APIs, time-dependent behavior)
- One behavior per test

### 2. VERIFY RED — Watch It Fail (MANDATORY)

Run the test. Confirm:
- It **fails** (not errors)
- The failure message describes the missing behavior
- It fails because the feature is missing, not because of typos or setup issues

If the test **passes**: you're testing existing behavior. Rewrite the test.
If the test **errors**: fix the error, re-run until it fails correctly.

### 3. GREEN — Write Minimal Code

- Simplest code that makes the test pass
- No extra features, no "while I'm here" improvements
- No premature abstractions — three similar lines beats a premature helper

### 4. VERIFY GREEN — Watch It Pass (MANDATORY)

Run the test. Confirm:
- The new test **passes**
- All other tests **still pass**
- Output is clean (no warnings, no errors)

If the new test **fails**: fix the code, not the test.
If other tests **fail**: fix them now, before proceeding.

### 5. REFACTOR — Clean Up (After Green Only)

- Remove duplication, improve names, extract helpers
- Keep all tests green throughout
- Do NOT add new behavior during refactor

### 6. REPEAT

Go back to Step 1 for the next behavior.

## Decision Rules

| If you're about to... | Instead... | Why |
|----------------------|-----------|-----|
| Write production code without a test | STOP — write the failing test first | Tests written after implementation pass immediately and prove nothing |
| Skip testing because the change is "simple" | Write the test — it will be quick if it's truly simple | Simple code has the sneakiest bugs (off-by-one, null edge cases) |
| Apply a quick fix without a regression test | Write the test, then fix | Untested fixes become permanent regressions |
| Continue with code that wasn't test-driven | Consider rewriting test-first | Sunk cost — untested code is a liability regardless of time spent |

## Example

```
Task: Add isPalindrome(str) function

1. RED — Write test:
   test("isPalindrome returns true for 'racecar'", () => {
     expect(isPalindrome("racecar")).toBe(true);
   });

2. VERIFY RED — Run: npm test
   ✗ ReferenceError: isPalindrome is not defined    ← fails correctly

3. GREEN — Minimal code:
   function isPalindrome(str) {
     return str === str.split("").reverse().join("");
   }

4. VERIFY GREEN — Run: npm test
   ✓ isPalindrome returns true for 'racecar'        ← passes
   42 passed, 0 failed

5. REFACTOR — (no changes needed)

6. REPEAT — next test: edge case with empty string
```

**Test runner detection:** Check `package.json` scripts, `pytest.ini`, `Cargo.toml`, `go.mod`, or `Makefile` for the project's test command before starting the cycle. Use the same runner consistently.

## Verification Checklist

Before claiming work is complete:

- [ ] Every new function/method has at least one test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason (not errors)
- [ ] Wrote minimal code per test (no gold-plating)
- [ ] All tests pass with clean output
- [ ] Edge cases and error paths covered
- [ ] Mocks used only when unavoidable

## When Stuck

- Test too complicated to write → design is too complicated, simplify first
- Must mock everything → code is too coupled, extract interfaces
- Test setup is huge → extract test helpers or fixtures
