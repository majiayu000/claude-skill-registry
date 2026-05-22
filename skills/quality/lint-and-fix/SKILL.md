---
name: lint-and-fix
description: Run linters and fix violations, formatting errors, or style mismatches using Trunk. Use when code quality checks fail, before submitting PRs, or to repair "broken" linting states.
---

# Lint and Fix Loop: Trunk

## Purpose

An autonomous loop for the agent to identify, fix, and verify linting and formatting violations using [Trunk](https://trunk.io).

## Loop Logic

1. **Format**: Run `pnpm format` (which executes `trunk fmt`) to automatically fix trivial formatting issues.
2. **Identify**: Run `pnpm lint` (which executes `trunk check`) to list any remaining violations.
3. **Analyze**: Examine the output from Trunk, focusing on the file path, line number, and error message. Refer to [../common-references/troubleshooting.md](../common-references/troubleshooting.md) for environment or runtime issues.
4. **Fix**: Apply the minimum necessary change to the source code to resolve the reported linting violations.
5. **Verify**: Re-run the loop (starting from **Format**) until all issues are resolved.
   - If `pnpm lint` passes: Finish.
   - If it fails: Analyze the new failure and repeat the loop.

## Termination Criteria

- No more errors reported by `pnpm lint`.
- Reached max iteration limit (default: 5).

## Examples

### Scenario: Fixing violations in a modified file

1. Agent runs `pnpm format` to ensure consistent style.
2. Agent runs `pnpm lint` and finds a linting violation in `src/index.ts`.
3. Agent analyzes the error and applies a manual fix.
4. Agent runs `pnpm format` again (part of the loop).
5. Agent runs `pnpm lint` and it now passes.

## Resources

- [Trunk CLI Reference](../common-references/trunk-commands.md): Common commands for linting and formatting.
- [Trunk Documentation](https://docs.trunk.io/): Official documentation for the Trunk CLI.
