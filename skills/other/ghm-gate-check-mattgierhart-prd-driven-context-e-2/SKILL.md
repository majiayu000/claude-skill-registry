---
name: ghm-gate-check
description: >
  Validates gate criteria before PRD lifecycle advancement.
  Triggers before advancing from v0.X to v0.Y or explicit `/ghm-gate-check` invocation.
  Outputs pass/block summary with missing artifacts list.
---

# Gate Check

Validate all gate criteria are met before advancing the PRD lifecycle version.

## Workflow Overview

1. **Load Gate Criteria** → Read target gate requirements from PRD.md
2. **Verify Evidence** → Check required artifacts exist with valid IDs
3. **Assess Readiness** → Evaluate handoff requirements
4. **Report** → Pass/Block with specific gaps

## Core Output Template

| Element | Definition | Evidence |
|---------|------------|----------|
| **Target Gate** | Version being validated | `v0.3 → v0.4` |
| **Status** | Pass or Block | Clear determination |
| **Missing Artifacts** | What's not complete | Specific list with IDs |
| **Recommendation** | Action to take | Proceed / Address gaps |

## Gate Reference

| Gate | Focus | Key Artifacts |
|------|-------|---------------|
| v0.1 → v0.2 | Problem validated | CFD-XXX evidence |
| v0.2 → v0.3 | Market defined | Segment definitions |
| v0.3 → v0.4 | Commercial viable | BR-XXX, pricing |
| v0.4 → v0.5 | Journeys mapped | UJ-XXX complete |
| v0.5 → v0.6 | Risks addressed | Risk register |
| v0.6 → v0.7 | Architecture set | API-XXX, schemas |
| v0.7 → v0.8 | Build complete | Tests passing |
| v0.8 → v0.9 | Deployed | Live environment |
| v0.9 → v1.0 | Launched | Metrics tracking |

## Step 1: Load Gate Criteria

1. Read PRD.md gate section for target version
2. Extract all required criteria
3. Identify artifact types needed (BR, UJ, API, CFD)

### Checklist
- [ ] Target gate identified
- [ ] All criteria extracted
- [ ] Required artifact types listed

## Step 2: Verify Evidence

For each required criterion:

1. Check artifact exists in SoT/
2. Verify artifact status is not "Draft"
3. Confirm cross-references are valid
4. Check for required CFD-XXX evidence

### Evidence Matrix

| Criterion Type | Verification |
|----------------|--------------|
| Business Rule | BR-XXX exists, status Active |
| User Journey | UJ-XXX exists, all steps defined |
| API Contract | API-XXX exists, endpoints specified |
| Customer Evidence | CFD-XXX linked to BR-XXX |

### Checklist
- [ ] All required BR-XXX verified
- [ ] All required UJ-XXX verified
- [ ] All required API-XXX verified
- [ ] Evidence chain (CFD → BR) validated

## Step 3: Assess Handoff Readiness

Check downstream requirements:

1. Next agent has context needed
2. No open blockers in current EPIC
3. Documentation is current

### Checklist
- [ ] EPIC Section 0 has no blockers
- [ ] README.md is synchronized
- [ ] Handoff documentation exists

## Step 4: Generate Report

```markdown
## Gate Check Report: v0.X → v0.Y

**Status**: [PASS / BLOCK]
**Date**: YYYY-MM-DD

### Criteria Assessment

| Criterion | Status | Evidence |
|-----------|--------|----------|
| [Criterion 1] | ✅/❌ | [ID or gap] |
| [Criterion 2] | ✅/❌ | [ID or gap] |

### Missing Artifacts
- [ ] [Specific gap with required action]

### Recommendation
[Proceed to v0.Y / Address [N] gaps before advancing]
```

## Quality Gates

### Pass Checklist
- [ ] All criteria evaluated (none skipped)
- [ ] Evidence is traceable to IDs
- [ ] Recommendation is actionable

### Testability Check
- [ ] Report can be validated against PRD.md criteria
- [ ] Missing artifacts are specific and findable

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Skipping criteria | "Probably fine" | → Verify each explicitly |
| Vague gaps | "Needs more work" | → Cite specific missing ID |
| Override blocks | Advancing despite fails | → Address gaps first |

## Boundaries

**DO**:
- Validate against documented criteria
- Identify specific gaps
- Provide actionable recommendations

**DON'T**:
- Create missing artifacts (just report)
- Override gate blocks
- Make subjective quality judgments

## Handoff

After gate check:
- If PASS: Advance PRD version, trigger `ghm-status-sync`
- If BLOCK: Return to current stage, address gaps
