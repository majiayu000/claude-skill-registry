---
name: vibe-scenario-matrix
description: Generates a behavioral scenario acceptance matrix for comprehensive test coverage planning. Maps user scenarios to acceptance criteria with stable IDs.
user-invocable: true
---

# vibe-scenario-matrix

Test coverage isn't about code lines -- it's about user scenarios. Map them all.

## When to Use This Skill

- Planning test coverage for a complex feature
- Preparing for a release or milestone review
- After expanding requirements significantly
- When stakeholders ask "what's tested?"
- Transitioning from ad-hoc testing to systematic testing

## When NOT to Use This Skill

- Single-function unit testing (just write the test)
- Already have comprehensive test specifications
- Prototyping/spiking (too early for formal coverage)

## Steps

1. **Gather scenarios** from:
   - PRD / Requirements document
   - User stories / acceptance criteria
   - Bug reports (past failures = scenarios to test)
   - User feedback / support tickets
   - Edge cases discovered during development

2. **Assign stable IDs** -- Use format `[Section]-[Number]`:
   - Example: `AUTH-001`, `PAYMENT-015`, `ONBOARD-003`
   - IDs never change once assigned (even if scenario text changes)

3. **Classify testing approach**:
   - **Deterministic** (61%): Can be tested with standard assertions
   - **LLM-as-Judge** (24%): Needs qualitative assessment
   - **Simulation** (11%): Needs multi-step environment
   - **Proxy Metric** (4%): Can only be measured indirectly

4. **Build the matrix**:

| ID | Scenario | Expected Behavior | Test Approach | Status |
|----|----------|-------------------|--------------|--------|
| AUTH-001 | User logs in with valid credentials | Redirect to dashboard, session created | Deterministic | PASS |
| AUTH-002 | User enters wrong password 5 times | Account locked for 30 minutes | Deterministic | NOT_IMPL |
| TONE-001 | System responds empathetically to frustration | Response acknowledges emotion without dismissing | LLM-as-Judge | PARTIAL |

5. **Track status**: PASS / PARTIAL / FAIL / NOT_IMPLEMENTED / DEFERRED

## Output Format

### Scenario Acceptance Matrix: [Feature/Product]

**Total Scenarios**: X
**Coverage**: Y% (PASS or PARTIAL)

| Status | Count | % |
|--------|-------|---|
| PASS | X | X% |
| PARTIAL | X | X% |
| NOT_IMPLEMENTED | X | X% |
| DEFERRED | X | X% |

### By Testing Approach
| Approach | Count | Tooling Needed |
|----------|-------|---------------|
| Deterministic | X | Standard test framework |
| LLM-as-Judge | X | Evaluation framework |
| Simulation | X | Environment setup |
| Proxy Metric | X | Metrics pipeline |

### Full Matrix
[Table as above]
