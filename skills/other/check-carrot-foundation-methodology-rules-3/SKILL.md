---
name: 'Quality Check'
description: 'Run lint, typecheck, and test checks on affected projects to verify code quality.'
---

Run the three quality gates in order on affected projects:

1. **Lint**: `pnpm lint:affected`
2. **Typecheck**: `pnpm ts:affected`
3. **Test**: `pnpm test:affected`

If any step fails, diagnose and fix the issue, then re-run that step before proceeding.

To target a single project instead of all affected projects:

```bash
pnpm nx lint <project-name>
pnpm nx ts <project-name>
pnpm nx test <project-name>
```

All three checks must pass before the work is considered complete.
