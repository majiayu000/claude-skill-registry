---
name: plan-from-spec
description: 'Generate an executable plan + test plan from a spec/decision log, including impact analysis for brownfield changes. Suitable for TDD implementation and PR review.'
license: MIT
---

# Plan From Spec

## When to Use
After a spec exists (either `changes/<...>/03-spec.md` or `specs/<...>/proposal.md`).

## Inputs
- Spec path(s)
- Decision log path (optional but recommended)
- Constraints (time, scope, dependencies)
- Brownfield indicator (is this modifying existing system?)

## Outputs
- `changes/<...>/04-plan.md` — includes:
  - Implementation steps with verification
  - Test strategy
  - **Impact analysis** (for brownfield/high-risk)
  - Rollback strategy

## Impact Analysis (Brownfield/High-Risk)
For any brownfield change or Medium/High risk change, include:
- **Current behavior**: What exists today
- **Impacted modules/flows**: What will be affected
- **Compatibility/migration**: Breaking changes and migration path
- **Regression mitigations**: Critical paths to test
- **Observability additions**: Logging, monitoring, alerts
- **Rollback strategy**: How to revert if needed

## Rules
- Every step must include how to verify
- Prefer small, reviewable steps (split PRs if needed)
- Call out risky areas: auth/authz, secrets, data flow, CI/CD
- Separate refactor from behavior change when possible

## Output Format
Provide file-ready markdown for `04-plan.md`:

```markdown
# Implementation Plan: {Feature Name}

## Risk Assessment
- **Risk Level**: Low / Med / High
- **Brownfield**: Yes / No
- **Affected Systems**: {list}

## Impact Analysis (if brownfield/high-risk)
### Current Behavior
{description}

### Impacted Modules
- {module 1}: {impact}
- {module 2}: {impact}

### Rollback Strategy
{how to revert}

## Implementation Steps

### Step 1: {Title}
- **Files**: {paths}
- **Changes**: {description}
- **Verify**: {how to verify}

### Step 2: {Title}
...

## Test Strategy
- **Unit Tests**: {list}
- **Integration Tests**: {list}
- **Regression Tests**: {critical paths}

## Dependencies
- {dependency 1}
- {dependency 2}
```
