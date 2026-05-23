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

---

## Self-Audit Pattern

> After implementation, compare results against context.md requirements to verify fulfillment.

### Purpose

According to the "How to write a good spec for AI agents" guide, having AI verify its own work against the spec is a powerful pattern. This helps catch missing items before running tests.

### Trigger

- After each implementation phase
- Before test execution

### Prompt Example

At completion, verify the following:

> "After implementation, compare your results against the requirements in context.md 
> and verify each item is fulfilled. 
> If any requirements are not met, list them."

### Self-Audit Output Format

```yaml
selfAuditResult:
  # Requirements fulfillment
  requirementsMet:
    - "[REQ-1] User query API ✅"
    - "[REQ-2] Error handling ✅"
  requirementsNotMet:
    - "[REQ-3] Pagination ❌ (not implemented)"
  
  # 3-tier boundary check
  boundaryCheck:
    neverDoViolations: []          # Critical violations (halt if any)
    askFirstItems: []              # Items needing approval
    alwaysDoCompleted:             # Required actions
      - "lint executed"
      - "tests passed"
  
  # Overall judgment
  readyForTest: true | false
  blockers:                        # Blocking reasons if false
    - "REQ-3 not implemented"
```

### Workflow Integration

```
Implementation Phase Complete
        ↓
[Self-Audit] Compare against context.md requirements
        ↓
    readyForTest?
     ↓         ↓
   true      false
     ↓         ↓
Run tests   Fix implementation and retry
```

### Notes

- Self-Audit is a **supplementary check**, not a replacement for actual tests
- Requirement fulfillment involves subjective judgment; tests provide final verification
- If `neverDoViolations` exist, halt immediately and report to user

