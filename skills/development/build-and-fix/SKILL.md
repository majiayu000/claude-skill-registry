---
name: build-and-fix
description: Build the project and automatically fix any build errors, compilation failures, or type mismatches. Use when the project fails to build, shows "broken" states, or after making significant changes.
---

# Build and Fix Loop

## Purpose

An autonomous loop for the agent to identify, analyze, and fix build errors using `pnpm build`.

## Loop Logic

1. **Identify**: Run `pnpm build` to identify build failures.
2. **Analyze**: Examine the build output to determine:
   - The failing package and file.
   - The specific compiler or build error message.
   - Refer to [../common-references/troubleshooting.md](../common-references/troubleshooting.md) for common TS errors.
3. **Fix**: Apply the minimum necessary change to resolve the error (e.g., fixing TypeScript types, correcting imports, or updating configurations).
4. **Verify**: Re-run `pnpm build`.
   - If passed: Finish.
   - If failed: Analyze the new failure and repeat the loop.

## Termination Criteria

- The project builds successfully (as reported by `pnpm build`).
- Reached max iteration limit (default: 5).
- The error persists after multiple distinct fix attempts, indicating a need for human intervention.

## Examples

### Scenario: Fixing a TypeScript compilation error

1. `pnpm build` fails because of a type mismatch in `packages/common/src/index.ts`.
2. Agent analyzes the error and finds an incorrect interface implementation.

## Resources

- [pnpm Commands for Node.js](../common-references/pnpm-commands.md): Common commands for building and managing dependencies.
- [TypeScript Documentation](https://www.typescriptlang.org/docs/): Official documentation for TypeScript.
