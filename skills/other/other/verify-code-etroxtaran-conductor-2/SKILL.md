---
name: verify-code
tags:
  technology: [python, typescript, javascript]
  feature: [testing, workflow]
  priority: high
summary: Run strict verification gate after implementation with evidence from tests
version: 1
---

# Verify Code

## When to use

- After tasks are marked done
- Before marking implementation as complete
- As part of TDD workflow verification phase

## Instructions

1. Use verification commands to run the smallest strong set of checks:
   - `pytest` for Python projects
   - `npm test` for Node.js projects
   - `npm run typecheck` for TypeScript

2. Report what passed and what is missing:
   - List all passing tests
   - List any failing tests with error details
   - Note any skipped or pending tests

3. If any blocking issue exists, return to implementation:
   - Do NOT mark as complete if tests fail
   - Document what changes are needed
   - Return to implementation phase

## Verification Checklist

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Type checking passes (if applicable)
- [ ] Linting passes with no errors
- [ ] No regressions in existing functionality
- [ ] Build completes successfully
