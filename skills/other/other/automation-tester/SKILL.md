---
name: automation-tester
description: Core QA engineering mindset for test planning and prioritization. Use when analyzing what to test, designing test cases, prioritizing by risk, or determining coverage strategy. Triggers on "what should I test", "test strategy", "coverage", "prioritize tests", "design test cases", "P0 P1 P2".
---

# Automation Tester Mindset

Think like a senior QA engineer: focus on risk, user impact, and business value.

## Test Case Design Process

```
1. Identify page/feature type
2. Apply type-specific test patterns (see references/test-patterns.md)
3. Assign priority based on risk (see references/priority-matrix.md)
4. Generate test specifications
```

## Priority Assignment

| Priority | Criteria | Examples |
|----------|----------|----------|
| **P0** | App broken if fails | Login, checkout, core navigation |
| **P1** | Major feature broken | Search, filters, form validation |
| **P2** | Minor/edge cases | Tooltips, animations, rare flows |

## Test Case Format for Qase

```yaml
title: "Valid login should redirect to dashboard"
suite: "Authentication"
severity: critical | major | normal | minor
priority: high | medium | low
preconditions:
  - User exists in system
steps:
  - action: Navigate to /login
    expected: Login form visible
  - action: Enter valid email
    expected: Email accepted
  - action: Enter valid password
    expected: Password masked
  - action: Click Sign In
    expected: Redirects to dashboard
```

## Coverage Strategy

**Smoke Tests (10-15 cases):**
- One happy path per critical feature
- App loads, core nav works, primary action succeeds

**Regression (comprehensive):**
- All P0 + P1 cases
- Validation testing
- Error handling
- Cross-browser

## Decision Rules

```
Is it part of core functionality?
├── Yes → P0
└── No → Continue

Does it handle money/data?
├── Yes → P0 or P1
└── No → Continue

Is it user-facing validation?
├── Yes → P1
└── No → P2
```

## References

- **Test patterns by page type**: See [references/test-patterns.md](references/test-patterns.md)
- **Priority matrix details**: See [references/priority-matrix.md](references/priority-matrix.md)
