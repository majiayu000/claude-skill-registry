# Coverage Review Reference

## Review Instructions

1. Skip non-testable code (config, documentation, CI files, SKILL.md files, markdown).
2. Search for existing test files covering the target code.
3. Identify the project's test framework and conventions by reading existing test files.

## What to Review

- **No test coverage** — functions or modules with no corresponding tests
- **Missing edge cases** — tests exist but miss critical paths (error handling, boundary conditions, empty inputs, concurrent access)
- **Risk-level mismatch** — high-risk code (auth, data handling, financial logic) with only basic happy-path tests
- **Convention gaps** — tests not following the project's established testing patterns

## Determination Criteria

Flag an issue only when ALL of these hold:

1. The code performs meaningful logic worth testing (not pure configuration, boilerplate, or generated code)
2. The gap is discrete and actionable (a specific function or module, not "needs more tests generally")
3. The missing coverage creates real risk proportional to the code's criticality

## Priority Levels

- **P0** — Critical code with no tests (auth, data mutation, payment processing)
- **P1** — Important code with no tests or high-risk code with only happy-path tests
- **P2** — Code with tests but missing significant edge cases
- **P3** — Minor coverage gaps or convention mismatches

## What to Ignore

- Non-testable code (config, documentation, CI files, SKILL.md files, markdown)
- Generated code or trivial getters/setters with no logic

**Verdict label:** `Test Coverage: <adequate | gaps found>`
