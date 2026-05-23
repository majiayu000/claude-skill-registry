---
name: validate-spec
description: "Validate spec completeness and implementation compliance. Use before approval (--pre) or before completion (--post)."
model: claude-opus-4-5-20251101
allowed-tools: Read, Glob, Grep
---

# /validate-spec

Validate spec quality (pre-implementation) or implementation compliance (post-implementation).

## Usage

```bash
/validate-spec SPEC-001              # Auto-detect mode based on status
/validate-spec SPEC-001 --pre        # Pre-implementation validation
/validate-spec SPEC-001 --post       # Post-implementation compliance
```

## Mode Detection

| Spec Status | Default Mode | Purpose |
|-------------|--------------|---------|
| draft, review | --pre | Validate before approval |
| approved | --pre | Final check before implementation |
| in_progress, complete | --post | Verify implementation matches |

## Pre-Implementation Validation (--pre)

### 1. Structure Completeness
```
Required sections:
✓ Summary (present)
✓ Problem Statement (present)
✓ Acceptance Scenarios (3 found)
✓ Agent Context (present)
✓ Out of Scope (present)
✗ Dependencies (MISSING)
```

### 2. Acceptance Scenario Quality
```
Scenario 1: "User signs up"
✓ Has Given/When/Then clauses
✓ Specific, not vague

Scenario 2: "Invalid credentials"
⚠ Then clause is vague: "shows error"
  Suggest: "shows 'Invalid email or password' message"
```

Scenarios must be:
- **Specific**: Not "shows error" but "shows error X"
- **Testable**: Can become automated test
- **Complete**: Given/When/Then present

### 3. Agent Context Validation
```
Files referenced:
✓ src/lib/auth.ts exists
✗ src/middleware/session.ts NOT FOUND
```

### 4. Success Metrics Measurability
```
Metric 1: "Page load < 2s"
✓ Measurable, has threshold

Metric 2: "Good user experience"
✗ NOT MEASURABLE
  Suggest: "User satisfaction > 4/5"
```

### 5. Conciseness Check
```
Word count: 847 words
Guideline: < 500 words
⚠ Consider splitting into multiple specs
```

### 6. Open Questions Check
```
2 open questions found:
1. "Which OAuth providers?"
2. "Session timeout?"

⚠ Resolve before 'approved' status
```

### Pre-Validation Summary
```
Ready for approval: NO

Fix:
- Add missing Dependencies section
- Refine vague scenario
- Make metrics measurable
- Resolve open questions
```

## Post-Implementation Validation (--post)

### 1. Acceptance Scenario Coverage
```
Scenario: "User signs up"
✓ Found: auth/signup.test.ts:15

Scenario: "Session expires"
✗ NO TEST FOUND

Coverage: 2/3 scenarios (67%)
```

### 2. Success Metrics Verification
```
Metric: "Page load < 2s"
  Result: 1.4s average
  ✓ PASS

Metric: "95% coverage"
  Result: 97.2%
  ✓ PASS
```

### 3. Out-of-Scope Violations
```
Out of scope: "Social login", "2FA"

Scanning...
✓ No oauth/social code found
⚠ Found "password strength" - potential violation
```

### 4. Agent Constraints Compliance
```
Constraint: "No new dependencies"
✓ package.json unchanged

Constraint: "Files outside scope"
⚠ src/utils/helpers.ts modified
```

### 5. Definition of Done
```
- [x] Acceptance scenarios tested
- [ ] No console errors ← incomplete
```

### Post-Validation Summary
```
Implementation compliance: PARTIAL

Issues to resolve:
1. Add test for "Session expires"
2. Review password complexity code
3. Fix console warnings
```

## Interactive Fixes

When issues found:
```
AI: Let's refine Scenario 2...
    What should the error message say?

User: "Invalid email or password"

AI: Updated. Now the metrics...
    Remove "Good UX" or replace with measurable?

User: Remove it

AI: Done. Re-validating...

    ## Validation: PASS
    Ready to move to 'review' status?
```

## Integration

```
/spec → /validate-spec --pre → [approval] → /plan → /implement → /validate-spec --post → /complete
```
