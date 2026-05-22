---
name: test-and-fix
description: Run unit tests and automatically fix code failures, regression bugs, or test mismatches. Use when tests are failing, after implementing new features, or to repair "broken" tests.
---

# Test and Fix Loop

## Purpose

An autonomous loop for the agent to identify, analyze, and fix failing unit tests using Vitest.

## Loop Logic

1. **Identify**: Run `pnpm test` to identify failing tests.
2. **Analyze**: Examine the test output to determine:
   - The failing test file and line number.
   - The expected vs actual values.
   - Refer to [../common-references/troubleshooting.md](../common-references/troubleshooting.md) for common test failure patterns.
3. **Fix**: Apply the minimum necessary change to either the source code (if it's a bug) or the test code (if the test is outdated).
4. **Verify**: Re-run `pnpm test`.
   - If passed: Move to the next failing test or finish if all are resolved.
   - If failed: Analyze the new failure (or the same one if the fix was insufficient) and repeat the loop.

## Termination Criteria

- All tests pass (as reported by `pnpm test`).
- Reached max iteration limit (default: 5).
- The error persists after multiple distinct fix attempts, indicating a need for human intervention or a broader architectural change.

## Examples

### Scenario: Fixing a logic error

1. `pnpm test` fails in `packages/common/src/math.test.ts` because `add(2, 2)` returned `5`.
2. Agent analyzes `packages/common/src/math.ts` and finds a typo `a + b + 1`.
3. Agent fixes the typo to `a + b`.
4. `pnpm test` passes.

### Scenario: Updating a test after a deliberate change

1. `pnpm test` fails because a UI component's text changed from "Submit" to "Confirm".
2. Agent confirms the change was intentional.
3. `pnpm test` passes.

## Resources

- [pnpm Commands for Node.js](../common-references/pnpm-commands.md): Common commands for testing and managing dependencies.
- [Testing Best Practices](../../../.cursor/rules/tech-stack.mdc): Project-specific testing guidelines.
