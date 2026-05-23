---
name: completion-verifier
description: Verifies implementation completion by running acceptance tests and triggers retry loop on failure.
context: fork
---

# Completion Verifier Skill

## When to Use

- After each implementation phase
- Before marking task as complete
- When retry loop is triggered

## Inputs

- context.md path (contains Acceptance Tests section)
- Test framework (from PROJECT.md: jest/vitest/playwright)

## Procedure

1. Parse Acceptance Tests section from context.md
2. Extract test IDs and file paths
3. Run tests: `npm test -- --testPathPattern="{test files}"`
4. Parse results (PASS/FAIL per test)
5. Update context.md status column
6. Return completion status

## Output

```yaml
completionStatus:
  total: 5
  passed: 4
  failed: 1
  allPassed: false
  failedTests:
    - id: T2
      type: Unit  # or Integration
      file: ErrorHandler.test.tsx
      error: "Expected error message not shown"
  failedPhase: "Phase 1"  # Determines where to retry
  recommendation: "Fix ErrorHandler.tsx, then re-run Phase 1"
```

## Retry Logic

When `allPassed: false`:

1. **Identify failed phase** based on test type:
   - Unit FAIL → Phase 1 (Mock implementation)
   - Integration FAIL → Phase 2 (API integration)

2. **Return to failed phase** (NOT test writing):
   - Pass `failedTests` info to implementation-agent
   - Implementation-agent fixes code only (no test rewrite)
   
3. **Retry limits**:
   - Max 2 retries per phase
   - After 2 failures → Ask user for intervention

## Skip Conditions

- No test framework configured → Skip with warning
- No Acceptance Tests in context.md → Skip
- Skip Conditions from testing.md apply (legacy, prototype, etc.)

## Tool Call Example

```bash
# Run specific tests
npm test -- --testPathPattern="batch.test|ErrorHandler.test"

# Check coverage (optional)
npm test -- --coverage --testPathPattern="..."
```
