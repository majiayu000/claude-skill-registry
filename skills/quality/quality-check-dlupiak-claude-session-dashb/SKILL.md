---
name: quality-check
description: Run typecheck, lint, test, and build quality gates
user-invocable: true
---

# Quality Check

Run the full quality suite for the project.

## Steps

Run each check sequentially from `apps/web/`. Report pass/fail for each:

### 1. TypeScript
```bash
cd apps/web && npm run typecheck
```

### 2. ESLint
```bash
cd apps/web && npm run lint
```

### 3. Vitest
```bash
cd apps/web && npm run test
```

### 4. Build
```bash
cd apps/web && npm run build
```

## Report

After all checks complete, output a summary table:

| Check | Status |
|-------|--------|
| typecheck | PASS/FAIL |
| lint | PASS/FAIL |
| test | PASS/FAIL |
| build | PASS/FAIL |

If any check fails, show the first 20 lines of errors and suggest fixes.

## Notes
- The "close timed out" warning after Vitest is a known nitro issue — ignore it
- Pre-existing type errors in `src/routes/demo/` should be ignored
