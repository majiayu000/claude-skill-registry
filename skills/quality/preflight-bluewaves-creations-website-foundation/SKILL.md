---
name: preflight
description: Runs all pre-flight checks sequentially — TypeScript checking, tests, and production build — stopping on first failure. Use before deploying or to verify the project is healthy.
disable-model-invocation: true
---

Run pre-deploy verification checks and report results.

## Steps

### 1. Run Verification Commands

Run these sequentially using Bash, stopping if any fail:

1. `bun run check` — TypeScript type checking
2. `bun run test` — Run all Vitest tests
3. `bun run build` — Production build

### 2. Check Configuration

Read and verify these files:

- **`astro.config.mjs`** — Verify `site` is NOT `"https://example.com"` (template default)
- **`wrangler.jsonc`** — Verify `destination_address` is NOT `"you@example.com"` (template default)
- Check that `.dev.vars` file exists (for local development)

### 3. Report Results

Summarize with a clear status:

**If all checks pass:**
```
READY TO DEPLOY
- TypeScript: OK
- Tests: 42 passed
- Build: OK
- Config: Verified
```

**If any checks fail:**
```
ISSUES FOUND
- TypeScript: [pass/fail details]
- Tests: [pass/fail details]
- Build: [pass/fail details]
- Config: [any warnings]
```

List each issue with a brief explanation of how to fix it.
