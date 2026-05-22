---
name: test-running
description: Run tests according to repository guidelines. Use after linting passes, before staging changes.
---

# Test Running

Run all appropriate tests according to repository guidelines.

## When to Use This Skill

Use this skill:
- After linting passes
- Before staging changes for commit
- After implementing a feature or bug fix
- When verifying existing functionality still works

## Test Discovery

Run tests according to repository guidelines. Look for test commands in:

1. Repository documentation (`README.md`, `AGENTS.md`, `CLAUDE.md`, etc.)
2. Package configuration (`package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`, etc.)
3. Standard test patterns for the project type

If no test guidelines are found or they are unclear, ask the user for
clarification.

## Common Test Commands

```bash
# JavaScript/TypeScript
npm test
yarn test
pnpm test

# Python
pytest
python -m pytest
make test

# Other
./bin/test-*
*test*
```

## Testing Process

**CRITICAL REQUIREMENT: 100% test success is MANDATORY.**

For each test command found:

1. Run it
2. If ANY test failures occur, they MUST be fixed
3. If issues can't be fixed immediately, stop and ask the user what to do next
4. Only consider the task complete when ALL tests pass with 100% success rate
   OR the user explicitly gives permission to ignore certain failures

## Important Notes

- "Issues" includes not only test failures, but also noise in test output
  such as warnings which could mask true failures
- Don't proceed until all tests pass or user explicitly allows deferral
- Document any failures clearly with file, test name, and error message

## Output

Report results organized by:

1. **Passing tests**: Summary of what passed
2. **Failing tests**: Each failure with file, test name, and error
3. **Recommendations**: What needs to be fixed

If all tests pass, simply confirm: "All tests passed."
