---
name: tdd
description: |
  Enforces Test-Driven Development (TDD) workflow with three-phase gate system.
  Use when: (1) implementing new features, (2) fixing bugs, (3) refactoring code.
  Blocks progress at each phase until conditions are met. RED → GREEN → REFACTOR.
category: testing
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Test-Driven Development (TDD) Workflow

You are not allowed to implement code until the full TDD cycle is followed.

## Three-Phase Gate System

### Phase 1: RED (Write Failing Test)

**BLOCKED: Cannot proceed until test failure is proven**

1. Write a test that captures the expected behavior
2. Run the test - it MUST fail
3. Document the failure output as proof

**Phase 1 Checklist:**
- [ ] Test file created/modified
- [ ] Test run completed
- [ ] Failure output captured
- [ ] Failure is for the RIGHT reason (not syntax error)

**Example Phase 1 output:**
```
PHASE 1 - RED ✗
Test: should return user by email
Result: FAILED
Failure: expected undefined to equal { id: 1, email: 'test@example.com' }
Proceeding to Phase 2...
```

### Phase 2: GREEN (Make It Pass)

**BLOCKED: Cannot proceed until test passes**

1. Write the MINIMUM code to make the test pass
2. No refactoring, no extra features, no "while I'm here" changes
3. Run the test - it MUST pass
4. Document the pass output as proof

**Phase 2 Checklist:**
- [ ] Implementation is minimal
- [ ] Test run completed
- [ ] Pass output captured
- [ ] No new tests added (that's a new cycle)

**Example Phase 2 output:**
```
PHASE 2 - GREEN ✓
Test: should return user by email
Result: PASSED
Implementation: Added getUserByEmail() to user.service.ts
Proceeding to Phase 3...
```

### Phase 3: REFACTOR (Clean Up)

**Only proceed after Phase 2 is complete**

1. Review code for improvements (naming, structure, duplication)
2. Make changes while keeping tests green
3. Run tests after each refactoring change
4. Document what was refactored OR why skipped

**Phase 3 Checklist:**
- [ ] Reviewed for refactoring opportunities
- [ ] Changes made (or documented "No refactoring needed")
- [ ] Tests still pass after changes

**Example Phase 3 output:**
```
PHASE 3 - REFACTOR
Changes: Extracted email validation to shared utility
Tests: Still passing (3/3)
Cycle complete.
```

## Blocking Conditions

| Phase | Condition to Proceed |
|-------|---------------------|
| RED → GREEN | Test failure output must be shown |
| GREEN → REFACTOR | Test pass output must be shown |
| REFACTOR → Done | Tests must still pass |

**If Phase 1 (failing test) is missing:**
- Respond with: **"BLOCKED: PHASE 1 - RED REQUIRED"**
- Do not write implementation code
- Do not offer alternatives

## Multiple Features

When implementing multiple features:
1. Complete full cycle (RED→GREEN→REFACTOR) for feature 1
2. Then start cycle for feature 2
3. Never batch: "I'll write all tests first, then implement"

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "It's a simple change" | Simple changes still need tests | Write the test |
| "I'll add tests after" | Tests after = not TDD | BLOCKED |
| "Tests are slow" | Speed doesn't override process | Write the test |
| "I know this works" | Confidence ≠ proof | Write the test |
| "Just this once" | That's what you said last time | Write the test |

## Skill Chaining

### After REFACTOR Phase

| Chain To | When | Action |
|----------|------|--------|
| suggest-tests | Tests written | Verify coverage gaps |
| doc-maintenance | Feature complete | Update PLAN.md |
| repo-hygiene | Session end | Clean test-skill-* artifacts |

### Chains From

| Source | Condition |
|--------|-----------|
| no-workarounds | Bug fix in tool |
| workflow-orchestrator | New feature |
| research-to-plan | Implementation phase |

### Combined With no-workarounds

**When both tdd AND no-workarounds are activated:**
1. You are BLOCKED from implementing ANY fix until Phase 1 (RED) is complete
2. You are BLOCKED from working around the tool failure
3. The ONLY valid path: RED → GREEN → REFACTOR → Verify tool works

This ensures tool fixes are both test-driven AND actually fix the tool (not worked around).

### Combined With dogfood-skills

When bug fix completes a feature:
1. Complete TDD cycle: RED → GREEN → REFACTOR
2. Run `skills scan` to check for recommendations
3. Install any HIGH confidence skills

### Testing Pipeline

TDD is the entry point to the testing pipeline:

```
tdd (RED → GREEN → REFACTOR)
  ↓
suggest-tests (identify gaps)
  ↓
unit-test-workflow (generate tests)
  ↓
property-based-testing (invariants)
  ↓
repo-hygiene (cleanup) ← TERMINAL
```
