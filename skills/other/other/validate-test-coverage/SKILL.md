---
name: validate-test-coverage
description: Validate test coverage against acceptance criteria when the user asks to check test coverage, verify tests match requirements, audit test completeness, or cross-reference user stories with test cases
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[feature, user story doc, or test plan to validate]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: validation, testing, coverage
---

# Validate Test Coverage

## Overview

Cross-reference acceptance criteria from user stories against existing test cases to identify coverage gaps. This is not about code coverage percentages — it is about whether every requirement has a corresponding test at the appropriate level of the test pyramid, including edge cases and error states.

## Workflow

1. **Read project context** — Read `.chalk/docs/` for:
   - User stories with acceptance criteria (`*user_stories*`, `*prd*`, `*requirements*`)
   - Test plans (`*test_plan*`)
   - Any existing coverage reports (`*test_coverage*`)
   - Architecture docs for understanding component boundaries

2. **Identify the scope** — From `$ARGUMENTS` and conversation context:
   - If a specific feature or user story is named, scope the validation to those criteria
   - If no scope is given, validate all acceptance criteria found in `.chalk/docs/`
   - List every acceptance criterion with its source document and ID

3. **Inventory existing test cases** — Scan test plans in `.chalk/docs/engineering/` and test files in the codebase:
   - Map each test case to the acceptance criterion it covers
   - Note the test pyramid level (unit, integration, E2E, manual)
   - Note whether the test covers happy path only, or also includes edge cases and error states

4. **Cross-reference criteria to tests** — For each acceptance criterion, determine:
   - **Covered**: A test exists for the happy path AND at least one edge case or error state, at the appropriate pyramid level
   - **Partially Covered**: A test exists but only covers the happy path, or exists at the wrong pyramid level (e.g., E2E test for pure logic that should be a unit test)
   - **Uncovered**: No test case maps to this criterion

5. **Identify missing edge cases** — For each acceptance criterion, check whether tests exist for:
   - Boundary values (min, max, off-by-one)
   - Null/empty/missing inputs
   - Error states and failure modes
   - Concurrent access (if applicable)
   - Permission/authorization variations
   - If the user story mentions specific edge cases, verify those have explicit tests

6. **Assess pyramid health** — Check whether the test distribution follows the pyramid:
   - ~70% unit, ~20% integration, ~10% E2E
   - Flag inversions where business logic is only tested via E2E
   - Flag gaps where integration points have no integration tests

7. **Generate the coverage report** — Write the report using the format below. Save to `.chalk/docs/engineering/<n>_test_coverage_report.md` if requested, or present in conversation.

8. **Confirm** — Summarize findings: total criteria count, covered/partially covered/uncovered counts, and the most critical gaps.

## Filename Convention

```
<number>_test_coverage_report.md
```

Examples:
- `7_test_coverage_report.md`
- `12_test_coverage_report.md`

## Coverage Report Format

```markdown
# Test Coverage Report

Last updated: <YYYY-MM-DD>

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Acceptance Criteria | <n> | 100% |
| Fully Covered | <n> | <x%> |
| Partially Covered | <n> | <x%> |
| Uncovered | <n> | <x%> |

## Test Pyramid Distribution

| Level | Count | Percentage | Target |
|-------|-------|------------|--------|
| Unit | <n> | <x%> | ~70% |
| Integration | <n> | <x%> | ~20% |
| E2E | <n> | <x%> | ~10% |

## Coverage Detail

### Fully Covered

| AC ID | Criterion | Test IDs | Levels | Edge Cases |
|-------|-----------|----------|--------|------------|
| AC-1 | <criterion text> | U-1.1, U-1.2, I-1.1 | Unit, Integration | Null input, boundary |

### Partially Covered

| AC ID | Criterion | Test IDs | What is Covered | What is Missing |
|-------|-----------|----------|-----------------|-----------------|
| AC-3 | <criterion text> | U-3.1 | Happy path only | Error states, boundary values |

### Uncovered

| AC ID | Criterion | Source | Recommended Level | Priority |
|-------|-----------|--------|-------------------|----------|
| AC-5 | <criterion text> | <PRD/story ref> | Unit | High — data validation |

## Missing Edge Cases

| AC ID | Edge Case Category | Description | Recommended Test |
|-------|-------------------|-------------|------------------|
| AC-1 | Boundary | Max length input not tested | Unit test with 255-char input |
| AC-2 | Error State | Network timeout not tested | Integration test with mock timeout |
| AC-4 | Concurrency | Simultaneous updates not tested | Integration test with concurrent writes |

## Pyramid Health Issues

<List any pyramid inversions or gaps. For example:>
- **Inversion**: AC-2 (input validation) is only tested via E2E. This logic should have unit tests.
- **Gap**: No integration tests exist for the payment service boundary. API contract changes could break silently.

## Recommendations

1. **Critical** — <uncovered criterion with high user impact>
2. **High** — <partially covered criterion missing error states>
3. **Medium** — <pyramid inversion that should be restructured>
```

## Coverage Classification Rules

### Fully Covered
All of the following must be true:
- At least one test exists for the happy path
- At least one test exists for an error or edge case
- Tests are at the appropriate pyramid level (logic = unit, boundaries = integration, journeys = E2E)
- Test assertions verify the correct behavior (not just "no error thrown")

### Partially Covered
Any of the following:
- Happy path tested but no edge cases or error states
- Tests exist but at the wrong pyramid level
- Tests exist but assertions are weak (e.g., only checking status code, not response body)
- Only one path through a conditional is tested

### Uncovered
- No test maps to this acceptance criterion at any level
- A test exists with a similar name but does not actually verify the criterion's behavior

## Content Guidelines

### What Counts as an Acceptance Criterion
- Explicit "Given/When/Then" statements in user stories
- "The system shall..." requirements
- Validation rules (e.g., "email must be valid format")
- Business rules (e.g., "discount applies only to orders over $50")
- Non-functional requirements (e.g., "page loads in under 2 seconds")
- Error handling requirements (e.g., "invalid input shows error message")

### What Does NOT Count as Coverage
- A test file existing for a module (the tests must actually verify the criterion)
- Code coverage percentage (100% line coverage can still miss acceptance criteria)
- Tests that only exercise code without meaningful assertions
- Tests that verify implementation details rather than behavior

## Anti-patterns

- **Counting tests instead of checking coverage** — 200 unit tests means nothing if 5 acceptance criteria have zero tests. Coverage is about requirements traceability, not test count.
- **Ignoring edge case coverage** — A criterion marked "covered" because the happy path works, while boundary values, null inputs, and error states are untested. Partial coverage must be flagged honestly.
- **Only checking unit test presence** — Integration boundaries and E2E user journeys need their own tests. A feature with 50 unit tests but no integration test for the API contract is not fully covered.
- **Treating code coverage as test coverage** — Code coverage measures which lines were executed, not whether the behavior is correct. A test that calls a function without asserting the result gives you line coverage but zero behavioral coverage.
- **Not reading the actual test assertions** — A test named `test_user_registration` might only check that no exception is thrown, not that the user is actually created with the correct data. Read the assertions, not just the test names.
- **Marking derived criteria as uncovered without context** — If acceptance criteria were derived (not from a formal document), note that they are derived and flag for product confirmation rather than marking as a gap.
