---
name: writing-test-plans
description: Creates risk-based test plans and strategies. Use when planning testing, defining test scope, or documenting QA approach.
---

# Test Plan Writing

Create practical, risk-based test plans.

## Right-Size the Plan

Small feature: One-page plan (scope, risks, approach). Large feature: Full plan with all sections. Ask "Does the reader need this?" for every section.

## Risk-Based Prioritization

| Risk/Impact | High Impact | Low Impact |
|-------------|-------------|------------|
| High Risk | Test thoroughly | Test defensively |
| Low Risk | Test key paths | Minimal testing |

## Test Pyramid

```
        /  E2E  \        Few, slow, expensive
       /  Integ. \       Some, moderate
      /   Unit    \      Many, fast, cheap
```

## Required Sections

1. **Overview** - Feature under test, objectives, link to spec

2. **Scope** - In scope (what tested), Out of scope (what not, and why)

3. **Test Strategy** - Test types, approach per component, automation decisions

4. **Risk Assessment** - Identified risks, severity, mitigation, attention areas

5. **Test Cases** - Organized by feature, priority (P0/P1/P2), happy path and edge cases

6. **Environment & Data** - Test environments, data requirements, dependencies

7. **Entry/Exit Criteria** - When testing starts, when testing is complete

## Test Case Format

```markdown
### TC-001: [Description]

**Priority**: P0 | P1 | P2
**Type**: Unit | Integration | E2E | Manual

**Preconditions**:
- [Required state]

**Steps**:
1. [Action]

**Expected Result**:
- [Outcome]

**Edge Cases**:
- [Variations]
```

## Priority Definitions

| Priority | Description | Coverage |
|----------|-------------|----------|
| P0 | Critical path, must work | 100% automated |
| P1 | Important functionality | Mostly automated |
| P2 | Edge cases | Manual or deferred |

## Test Types

| Type | Purpose | When |
|------|---------|------|
| Unit | Isolated functions | Business logic, utilities |
| Integration | Component interactions | APIs, database, services |
| E2E | Complete user flows | Critical journeys |
| Manual | Exploratory, UX | Complex UI, accessibility |

## Guidelines

Link tests to requirements. Prefer automation. Test behavior, not implementation. Keep tests simple.

## Anti-Patterns

Do not test implementation details. Do not target 100% coverage as a goal. Do not create flaky tests. Do not rely on specific timing or order. Do not mock everything.

## Template

Use `templates/test-plan.md` for new plans.
