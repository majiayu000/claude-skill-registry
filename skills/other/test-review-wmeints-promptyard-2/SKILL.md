---
name: test-review
description: Use this skill to review unit-tests, component-tests, and integration tests.
---

Use this skill for reviewing the test code written by my colleagues.
Make sure you provide actionable feedback to the developer who wrote the tests.

## File Exclusion Check

Before reviewing any test file, you MUST check the contents of `.testcriticignore` and `.gitignore` to verify
if the file should be reviewed. We use glob patterns to exclude files from test review.

**Workflow:**

1. Discover test files in the project.
2. For each test file, check if the file is excluded.
3. If the file is not excluded, review the file.

This ensures you don't waste time reviewing files that the user has explicitly excluded.

## Analysis Framework

For each test file or test suite you review, evaluate against these criteria:

### 1. Coverage Adequacy

- Identify which implementation code paths are tested
- Flag untested edge cases, error conditions, and boundary values
- Check for missing tests on public interfaces
- Verify both happy paths and failure scenarios are covered
- Note: Aim for meaningful coverage, not 100% line coverage at all costs

### 2. Test Redundancy Detection

- Identify duplicate or near-duplicate test cases
- Flag tests that verify the same behavior multiple times
- Look for tests that could be consolidated using parameterization
- Identify overly granular tests that test implementation details rather than
  behavior

### 3. Arrange-Act-Assert (AAA) Pattern Compliance

- **Arrange**: Setup code should be clearly separated and minimal
- **Act**: There should be exactly ONE action being tested
- **Assert**: Assertions should immediately follow the action
- Flag tests that mix these phases or have unclear boundaries
- Each section should be visually distinct (blank lines between sections are good)

### 4. Assertion Quality

- Assertions must be specific and meaningful
- Flag vague assertions that don't really test anything
  when more specific checks are possible
- Ensure assertion messages are helpful when provided
- Check that assertions verify the RIGHT thing (behavior, not implementation)
- Flag assertions that are too broad or too narrow

### 5. Single Responsibility Per Test

- Each test should verify ONE specific behavior or flow
- Flag tests with multiple unrelated assertions
- Flag tests named with 'and' suggesting multiple responsibilities
- Tests should fail for exactly one reason

### 6. Fixture Usage and Setup Complexity

- Complex setup code MUST be moved to fixtures
- Inline setup should be minimal (1-3 lines max)
- Check for repeated setup code that should be a fixture
- Fixtures should be appropriately scoped (function, class, module, session)
- Flag fixtures that do too much or are poorly named

## Self-Critique Mechanism

After completing your initial analysis, you MUST perform a self-critique before producing the final output:

### Validation Checklist

For each issue or recommendation you've identified, verify:

1. **Is this a real problem?**
   - Does the code actually violate the principle, or are you being overly strict?
   - Is there a valid reason for the current approach that you missed?
   - Would fixing this issue genuinely improve the test quality?

2. **Am I confusing style with substance?**
   - Is this about code style/preferences or actual testing quality?
   - Does the current approach work correctly even if it's not your preferred pattern?
   - Is there a testing framework-specific idiom being used correctly?

3. **Is my suggestion practical?**
   - Would implementing this change actually make the tests better?
   - Am I recommending changes that would make tests more complex without clear benefit?
   - Is this recommendation proportional to the severity of the issue?

4. **Am I considering context?**
   - Do I understand what's being tested well enough to critique it?
   - Are there project-specific conventions I might be missing?
   - Is the test pattern appropriate for the type of code being tested?

5. **Am I being too aggressive about coverage?**
   - Am I recommending tests for trivial scenarios?
   - Are there legitimate reasons why certain paths aren't tested?
   - Am I suggesting tests that would be brittle or test implementation details?

### Revision Process

After validation:
- **Remove** any findings that fail the validation checklist
- **Downgrade** issues from "Critical" to "Recommendations" if they're stylistic
- **Clarify** any remaining issues with specific rationale
- **Adjust** suggestions to be more practical and actionable
- **Document** why you kept each remaining critique

Only issues that pass this self-critique should appear in your final output.
## Output Format

Structure your review as follows:

```text
## Test Quality Review: [filename or module]

### Summary

- Overall Quality: [Excellent/Good/Needs Improvement/Poor]
- Coverage Assessment: [Adequate/Gaps Identified/Insufficient]
- Redundancy Level: [None/Minor/Significant]

### Coverage Analysis

[List tested and untested scenarios]

### Issues Found

#### Critical Issues

[Issues that must be fixed]

#### Recommendations

[Improvements that would enhance quality]

### Specific Test Feedback

[Per-test feedback for problematic tests]

### Suggested Actions

[Prioritized list of improvements]
```

## Guidelines

1. **Be Specific**: Don't just say 'this test is unclear' - explain exactly
   what's wrong and how to fix it
2. **Prioritize**: Critical issues first, nice-to-haves last
3. **Show Examples**: When suggesting improvements, show the improved code
4. **Consider Context**: A test for a critical security function warrants more
   thoroughness than a simple utility
5. **Balance**: Don't recommend adding tests just for coverage numbers - tests
   should add value
6. **Pytest Best Practices**: Recommend pytest idioms (fixtures, parametrize,
   markers) where appropriate

## What You Should NOT Do

- Do not suggest tests for trivial getters/setters unless they have logic
- Do not recommend 100% coverage as a goal
- Do not suggest overly complex test structures
- Do not recommend mocking everything - integration points should sometimes be tested
- Do not focus on test naming conventions unless they're genuinely confusing