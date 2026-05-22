---
name: test
description: |
  Testing workflow - write and run tests. Use when:
  - User says "test", "write tests", "add tests", "run tests"
  - User mentions "coverage", "unit test", "integration test"
  - After implementing a feature (tests should follow)
  - Before shipping or merging code
context: fork
agent: tester
---

# Testing Workflow

Delegates to the Tester agent for test coverage and verification.

## Workflow

1. **Identify** - Determine what needs testing (component, hook, utility, integration)
2. **Write** - Create test files colocated with source (e.g., `button.test.tsx`)
3. **Run** - Execute tests and verify results
4. **Report** - Summarize coverage and gaps

## Testing Priorities

1. **Critical paths** - Auth, payments, core features
2. **Edge cases** - Error states, empty states, boundaries
3. **User interactions** - Forms, buttons, navigation
4. **Integration points** - API calls, external services

## Output

Return a summary:
- **Tests written**: New test files/cases
- **Tests passing**: Status
- **Coverage**: Key areas covered
- **Gaps**: What still needs testing
