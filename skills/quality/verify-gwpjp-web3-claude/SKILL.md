---
name: verify
description: Lightweight project verification. Runs typecheck, lint, prettier (auto-fix), and build. Reports pass/fail status and offers to auto-fix lint issues. Use for quick verification before commits or after changes.
---

# Verify Project

Run the core verification suite with live progress reporting.

## Progress Tracking

Use TodoWrite to create and update a todo list so the user can see progress:

```
- Typecheck (yarn typecheck)
- Lint (yarn lint)
- Prettier (yarn prettier)
- Build (yarn build)
```

Mark each todo as `in_progress` before running, and `completed` or note failure immediately after.

## Steps

### Phase 1 (parallel)

Run these three checks **in parallel** (they are independent). Mark all three as `in_progress`, then run the Bash commands in a single message:

- `yarn typecheck`
- `yarn lint`
- `yarn prettier` (always auto-format, NOT `prettier:check`)

After each completes, immediately mark its todo as `completed` (or note failure). Output a one-line status for each (e.g., "Typecheck: PASS", "Lint: FAIL - 3 errors").

### Phase 2 (after Phase 1)

Mark Build as `in_progress`, then run:

- `yarn build`

Mark completed and output status.

## Auto-Fix Behavior

- **Prettier:** Always auto-fixed (Phase 1 runs `yarn prettier`, not `prettier:check`).
- **Lint:** If lint fails, ask the user: "Lint found N issues. Want me to run `yarn lint --fix` to auto-fix?" If yes, run `yarn lint --fix`, then re-run `yarn lint` to check for remaining issues.
- **Typecheck/Build:** Cannot be auto-fixed. Report errors and suggest fixes.

## After Auto-Fix

If lint auto-fix was applied, re-run the full verification suite to confirm everything passes.

## Final Report

After all steps, output:

```
## Verification Report

| Check      | Status |
|------------|--------|
| Typecheck  | PASS/FAIL |
| Lint       | PASS/FAIL |
| Prettier   | PASS (auto-formatted) |
| Build      | PASS/FAIL |

### Issues
- [List any errors with file:line references]

### Summary
- [One-line: ready to commit, or what needs fixing]
```
