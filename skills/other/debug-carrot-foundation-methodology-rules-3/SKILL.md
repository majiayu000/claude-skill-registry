---
name: Debug
description: 'Systematically diagnose and fix errors, test failures, and unexpected behavior.'
---

### 1. Capture Evidence

Gather all relevant information before making changes:

- The exact command that failed
- The full error message and stack trace
- Which package or Nx target is affected
- What changed recently (`git diff`, `git log --oneline -5`)

### 2. Isolate the Failure

Determine the error category:

- **TypeScript error**: Run `pnpm nx ts <project>` to reproduce
- **Lint error**: Run `pnpm nx lint <project>` to reproduce
- **Test failure**: Run `pnpm nx test <project>` to reproduce, then narrow to a single test file with `pnpm nx test <project> -- --testPathPattern=<file>`
- **Build error**: Run `pnpm nx build <project>` to reproduce
- **Runtime error**: Check Lambda handler wiring and environment variables

Narrow down to the smallest reproducible scope: a single `nx run <project>:<target>` command or a single test file.

### 3. Fix the Root Cause

- Fix the root cause, not just the symptom
- Preserve all existing changes that are unrelated to the bug
- Prefer using existing shared helpers over creating new utilities
- Check if the same issue exists in similar files or patterns

### 4. Re-verify

Run all quality checks to confirm the fix and ensure no regressions:

```bash
pnpm lint:affected
pnpm ts:affected
pnpm test:affected
```

All three must pass before the fix is considered complete.
