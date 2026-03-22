---
name: bug-investigation
description: Test-first bug investigation workflow. Use when user reports a bug, error, unexpected behavior, mentions "something is broken", "doesn't work", or "regression". Enforces writing reproducing tests BEFORE code changes.
durability: encoded-preference
---

# Bug Investigation Workflow

## Core Principle

**ALWAYS write a test that reproduces the bug BEFORE modifying any implementation code.**

This ensures:
- The bug is real and reproducible
- The fix can be verified
- Regressions are prevented

## Investigation Phases

### Phase 1: Clarify the Bug

Before writing any code, gather information:

| Question | Purpose |
|----------|---------|
| What steps reproduce the bug? | Understand the scenario |
| What is the expected behavior? | Define success criteria |
| What is the actual behavior? | Understand the failure |
| Is it environment-specific? | Determine if test reproduction is feasible |

**Environment-specific indicators** (skip to logging approach):
- "Only happens in production"
- "Works locally but fails in staging"
- "Browser-specific" or "OS-specific"

### Phase 2: Reproduce in Test (MANDATORY)

**CRITICAL: Write test BEFORE touching implementation code.**

Write a test that captures the bug scenario and run it. It MUST fail. If it passes unexpectedly, adjust the test (max 2 attempts). If still passes after 2 attempts, escalate to Phase 4 (Logging).

#### Test Selection by Bug Type

| Bug Type | Test Approach |
|----------|---------------|
| User workflow fails | E2E test with Gherkin scenario |
| API returns wrong data | Integration test |
| Calculation incorrect | Unit test |
| UI displays wrong value | Integration or E2E test |

### Phase 3: Fix Implementation

Once test fails (bug confirmed), apply a minimal fix. Run the reproducing test (must pass) and then the full test suite (no regressions).

### Phase 4: Escalation to Logging (if reproduction fails)

**Trigger**: After 2 failed attempts to reproduce in tests OR environment-specific bug identified upfront.

#### Logging Strategy

1. **Add targeted logging** to suspected code paths:
   ```typescript
   // Example: Debug intermittent calculation error
   console.log('DEBUG: Input values', { x, y, timestamp: Date.now() })
   const result = calculateTotal(x, y)
   console.log('DEBUG: Calculation result', { result, expected })
   ```

2. **Instruct user**:
   ```
   I've added logging to [file:line]. Please:
   1. Run the application in [environment]
   2. Reproduce the bug
   3. Share the console output showing the logged values
   ```

3. **When user reports logs**:
   - Analyze logged values
   - Identify the root cause
   - Write a reproducing test based on insights
   - Remove logging after fix

## Anti-Patterns (AVOID)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| "Let me check the code and fix it" | No verification, might fix wrong thing | Write reproducing test first |
| "Try changing X to Y" | Trial-and-error without proof | Reproduce bug, then fix with verification |
| Multiple code changes at once | Can't tell which change fixed it | One minimal change, verify with test |
| Skip to logging without test attempts | Premature escalation | Try test reproduction twice first |
| Ask user to manually verify fix | No automated regression prevention | Test must pass, run full suite |

## Warning Behavior

**IF user requests code modification before bug reproduction:**

```
⚠️  STOP: Test-First Bug Investigation Required

Before modifying implementation code, we need to:

1. Write a test that reproduces this bug
2. Verify the test fails (proving the bug exists)
3. Then fix the code and verify the test passes

This ensures we actually fix the bug and prevent regressions.

Shall I write a reproducing test first?
```

## Edge Cases

### Multiple Bugs Reported Simultaneously

Handle each bug in isolation:
1. Prioritize with user if needed
2. One reproducing test per bug
3. Fix bugs sequentially with test verification

### Vague Bug Description

If bug report lacks details, systematically ask:
```
To reproduce this bug, I need:
- What specific steps trigger it?
- What did you expect to happen?
- What actually happened?
- Any error messages or screenshots?
```

Do NOT proceed with guesswork - clarity enables accurate test reproduction.

## Integration with TDD Cycle

Bug investigation follows the same RED-GREEN-REFACTOR cycle:

1. **RED**: Reproducing test fails (bug confirmed)
2. **GREEN**: Minimal fix makes test pass
3. **REFACTOR**: Apply `coding-style` patterns while keeping test passing

After refactoring, run full test suite to ensure no regressions.
