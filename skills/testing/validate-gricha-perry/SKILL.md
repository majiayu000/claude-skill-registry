---
name: validate
description: Run validation checks - determines whether to use fast (validate) or full (validate:full) based on changed files
---

# Validate Skill

Run the appropriate validation for your changes.

## Commands

| Command | What it does | When to use |
|---------|--------------|-------------|
| `bun run check` | lint + format + typecheck | Quick syntax check |
| `bun run validate` | check + build TS/worker + unit tests | Default for most changes |
| `bun run validate:core` | validate + integration tests | Core behavior changes |

## Decision Logic

1. **Check what files changed** using `git status` or `git diff --name-only`

2. **Use `bun run validate:core`** if changes touch:
   - `src/agent/` (core agent behavior)
   - `src/workspace/` (workspace lifecycle)
   - `src/terminal/` (terminal/WebSocket)

3. **Use `bun run validate`** for everything else

4. **Run specific tests** relevant to your changes instead of full suites:
   ```bash
   bun test test/unit/relevant.test.ts
   bun test test/integration/relevant.test.ts
   bun test web/e2e/relevant.spec.ts
   ```

## Steps

1. Check changed files:
   ```bash
   git diff --name-only HEAD
   ```

2. Run validation + relevant tests:
   ```bash
   bun run validate
   # Then run specific tests for your changes
   bun test test/unit/relevant.test.ts
   ```

3. If validation fails, fix issues and re-run

4. Run warden to get code review feedback locally (security, react best practices, code simplification):
   ```bash
   warden -v
   ```
   The `-v` flag streams findings in real-time. Fix any issues warden finds before creating a PR.

## Notes

- `validate` is fast (~30s), `validate:core` adds integration tests (~1-2min)
- CI runs full validation on PRs, so targeted tests are usually sufficient locally
