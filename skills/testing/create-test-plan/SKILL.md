---
name: create-test-plan
description: Create a test plan when the user asks to plan testing, define test cases, create a QA strategy, write a test plan, or prepare for testing a feature
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Write, Grep
argument-hint: "[feature or component to test]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: testing, quality, planning
---

# Create Test Plan

## Overview

Create a structured test plan using the test pyramid (Mike Cohn), boundary value analysis, and risk-based testing. Every test case traces back to an acceptance criterion, covers the right level of the pyramid, and explicitly addresses edge cases and error states.

## Workflow

1. **Read project context** -- Read `.chalk/docs/` for PRDs, user stories, acceptance criteria, and architecture docs. Read existing test plans to understand conventions and coverage gaps.

2. **Determine the next test plan number** -- List files in `.chalk/docs/engineering/` matching the pattern `*_test_plan_*.md`. Find the highest number and increment by 1. If none exist, start at `1`.

3. **Identify acceptance criteria** -- From `$ARGUMENTS`, conversation context, and project docs, extract every acceptance criterion or expected behavior. If no formal acceptance criteria exist, derive them from the feature description and confirm with the user.

4. **Map criteria to test pyramid levels** -- For each acceptance criterion, determine the appropriate test level:
   - **Unit**: Pure logic, calculations, data transformations, validation rules
   - **Integration**: Component interactions, API contracts, database queries, external service calls
   - **E2E**: Critical user journeys, cross-feature workflows, deployment verification

5. **Generate test cases per criterion** -- For each acceptance criterion, write specific test cases at the appropriate pyramid level. Include:
   - Happy path (expected inputs produce expected outputs)
   - Boundary values (edges of valid input ranges)
   - Error states (invalid inputs, missing data, system failures)
   - Concurrent/race conditions (if applicable)

6. **Identify edge cases** -- Systematically generate edge case tests using boundary value analysis:
   - Null/empty/missing inputs
   - Minimum and maximum valid values
   - Values just inside and outside boundaries
   - Special characters, unicode, extremely long strings
   - Concurrent access and race conditions
   - Network failures, timeouts, partial responses

7. **Classify manual vs. automated** -- Mark each test case as automated or manual. Default to automated. Manual testing is reserved for:
   - Visual/UX verification that cannot be reliably automated
   - Exploratory testing for complex user flows
   - Accessibility testing requiring human judgment
   - Third-party integration testing in sandbox environments

8. **Assign priority tags** -- Tag each test case:
   - **Smoke**: Must pass for any deploy -- critical path, data integrity, authentication
   - **Regression**: Run on every PR -- core functionality, important edge cases
   - **Full**: Run before releases -- comprehensive coverage including rare edge cases

9. **Write the file** -- Save to `.chalk/docs/engineering/<n>_test_plan_<feature_slug>.md`.

10. **Confirm** -- Tell the user the test plan was created with its path, total test case count, pyramid distribution, and any gaps or risks identified.

## Filename Convention

```
<number>_test_plan_<snake_case_feature>.md
```

Examples:
- `4_test_plan_user_registration.md`
- `6_test_plan_checkout_flow.md`
- `11_test_plan_api_rate_limiting.md`

## Test Plan Format

```markdown
# Test Plan: <Feature or Component>

Last updated: <YYYY-MM-DD>

## Scope

<What is being tested. Link to PRD, user story, or acceptance criteria document.
State what is in scope and out of scope for this test plan.>

## Acceptance Criteria Reference

| ID | Acceptance Criterion | Source |
|----|---------------------|--------|
| AC-1 | <Criterion text> | <PRD/Story link or "derived"> |
| AC-2 | <Criterion text> | <PRD/Story link or "derived"> |
| AC-3 | <Criterion text> | <PRD/Story link or "derived"> |

## Test Pyramid Distribution

| Level | Count | Percentage |
|-------|-------|------------|
| Unit | <n> | <x%> |
| Integration | <n> | <x%> |
| E2E | <n> | <x%> |
| Manual | <n> | <x%> |
| **Total** | **<n>** | **100%** |

Target distribution: ~70% unit, ~20% integration, ~10% e2e. Deviations noted below.

## Unit Tests

### AC-1: <Criterion summary>

| ID | Test Case | Input | Expected Output | Priority | Type |
|----|-----------|-------|-----------------|----------|------|
| U-1.1 | <Happy path description> | <input> | <output> | Smoke | Auto |
| U-1.2 | <Boundary value> | <input> | <output> | Regression | Auto |
| U-1.3 | <Error case> | <input> | <error/behavior> | Regression | Auto |

### AC-2: <Criterion summary>

| ID | Test Case | Input | Expected Output | Priority | Type |
|----|-----------|-------|-----------------|----------|------|
| U-2.1 | ... | ... | ... | ... | ... |

## Integration Tests

### AC-1: <Criterion summary>

| ID | Test Case | Setup | Action | Expected Result | Priority | Type |
|----|-----------|-------|--------|-----------------|----------|------|
| I-1.1 | <Description> | <preconditions> | <action> | <result> | Smoke | Auto |
| I-1.2 | <Description> | <preconditions> | <action> | <result> | Regression | Auto |

## E2E Tests

| ID | User Journey | Steps | Expected Result | Priority | Type |
|----|-------------|-------|-----------------|----------|------|
| E-1 | <Journey name> | 1. <step> 2. <step> 3. <step> | <result> | Smoke | Auto |
| E-2 | <Journey name> | 1. <step> 2. <step> | <result> | Regression | Auto |

## Edge Case Tests

| ID | Category | Test Case | Input | Expected Behavior | Level | Priority |
|----|----------|-----------|-------|--------------------|-------|----------|
| EC-1 | Null/Empty | <description> | `null` | <behavior> | Unit | Regression |
| EC-2 | Boundary | <description> | <boundary value> | <behavior> | Unit | Regression |
| EC-3 | Concurrency | <description> | <scenario> | <behavior> | Integration | Full |
| EC-4 | Error State | <description> | <failure scenario> | <behavior> | Integration | Regression |

## Manual Tests

| ID | Test Case | Steps | Expected Result | Priority | Why Manual |
|----|-----------|-------|-----------------|----------|------------|
| M-1 | <Description> | 1. <step> 2. <step> | <result> | Full | <reason automation is insufficient> |

## Test Data Requirements

<Describe any test fixtures, seed data, mock services, or environment setup needed.>

## Risks and Gaps

| Risk | Impact | Mitigation |
|------|--------|------------|
| <Testing gap or risk> | <What could go wrong> | <How to address it> |
```

## Content Guidelines

### Test Pyramid Distribution

The test pyramid (Mike Cohn) dictates the ideal distribution:

```
      /  E2E  \        ~10% - Slow, expensive, brittle
     /----------\
    / Integration \     ~20% - Moderate speed, tests boundaries
   /----------------\
  /      Unit        \  ~70% - Fast, cheap, focused
 /--------------------\
```

If your test plan inverts this pyramid (more E2E than unit tests), stop and restructure. Common reasons for inversion and how to fix:

| Problem | Fix |
|---------|-----|
| Business logic tested through UI | Extract logic into testable functions, unit test them |
| API validation tested via E2E | Write integration tests against the API directly |
| Database logic tested via full stack | Write integration tests with a test database |

### Boundary Value Analysis

For every input that has a range, test these values:

| Input Type | Test Values |
|------------|-------------|
| Numeric (min: 1, max: 100) | 0, 1, 2, 50, 99, 100, 101 |
| String (max: 255 chars) | empty, 1 char, 254 chars, 255 chars, 256 chars |
| Array (max: 10 items) | empty, 1 item, 9 items, 10 items, 11 items |
| Date range | start-1, start, start+1, end-1, end, end+1 |
| Enum/set | each valid value, invalid value, null |

### Risk-Based Test Prioritization

Assign priority based on two dimensions:

| | High Likelihood of Failure | Low Likelihood of Failure |
|---|---|---|
| **High Impact** | **Smoke** -- test on every deploy | **Regression** -- test on every PR |
| **Low Impact** | **Regression** -- test on every PR | **Full** -- test before release |

High impact includes: data corruption, security breach, financial loss, user-facing errors.
High likelihood includes: new code, complex logic, external dependencies, recently changed areas.

### Writing Good Test Cases

Each test case must be:
- **Specific**: "User with expired session token receives 401 and redirect to login" not "Test authentication"
- **Independent**: No test should depend on another test's execution or side effects
- **Traceable**: Every test links back to an acceptance criterion (the AC-X reference)
- **Deterministic**: Same input always produces same result. No flaky tests. If testing async behavior, define explicit wait conditions.

### When to Use Manual Testing

Automated testing is the default. Use manual testing only when:
- Visual appearance must be verified by a human (layout, animations, color accuracy)
- Exploratory testing is needed to find unknown unknowns in complex workflows
- Accessibility requires human judgment (screen reader experience, cognitive load)
- Third-party sandbox environments don't support automation
- The cost of automating exceeds the cost of periodic manual execution

Always document *why* a test is manual so it can be reconsidered for automation later.

## Anti-patterns

- **Only testing the happy path**: If your test plan has no error cases, boundary tests, or null input tests, it will miss the bugs that actually ship to production. Every acceptance criterion needs at least one sad path test.
- **No edge cases**: Bugs cluster at boundaries. If you have a numeric input with a range, test the edges. If you accept strings, test empty strings, unicode, and max length. Systematic boundary value analysis catches the defects that "it works on my machine" misses.
- **Inverted test pyramid**: If most tests are E2E and few are unit tests, the test suite will be slow, flaky, and expensive to maintain. Push tests down to the lowest level that can verify the behavior. E2E tests should only cover critical user journeys, not individual validation rules.
- **Not linking tests to acceptance criteria**: Tests without traceability to requirements create two problems: you can't verify coverage (are all criteria tested?) and you can't assess impact (if this test fails, what requirement is broken?). Every test must reference an AC.
- **Testing implementation details instead of behavior**: Tests like "verify the cache map has 3 entries" break when you refactor. Test the observable behavior: "second call returns the same result in under 5ms." Tests should describe *what* the system does, not *how* it does it internally.
- **All tests marked as Smoke priority**: If everything is critical, nothing is. Smoke tests should be a small subset (10-15%) that gates deployment. Over-tagging as Smoke slows down deploys and causes alert fatigue.
- **Missing test data documentation**: Test plans that assume data exists without specifying it lead to flaky tests and environment-dependent failures. Document what fixtures, seed data, and mocks are needed.
- **No concurrency or error state coverage**: If the feature handles concurrent users, network calls, or external services, the test plan must include tests for race conditions, timeouts, and partial failures. These are the bugs that cause production incidents.
