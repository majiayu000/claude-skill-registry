---
name: fix-ci
description: Investigate and fix the latest failing CI workflow
user-invocable: true
argument-hint: "[run-id]"
---

# Fix CI Workflow

Investigate the latest CI failure, reproduce locally, and fix it.

## Steps

### 1. Identify the Failure

```bash
# Get latest (or specific) workflow run
gh run list --limit 5
gh run view <run-id>
```

If `$ARGUMENTS.run-id` is provided, use that. Otherwise pick the latest failed run.

- Show which jobs failed and which passed
- Download the failed job logs: `gh run view <run-id> --log-failed`

### 2. Analyze the Error

Read the logs and classify the failure:

| Type | Indicators |
|------|-----------|
| **typecheck** | `error TS`, `tsc --noEmit` |
| **lint** | `eslint`, `warning`/`error` with rule names |
| **unit test** | `vitest`, `FAIL`, `expect(` |
| **e2e test** | `playwright`, `spec.ts`, `timeout`, `locator` |
| **build** | `npm run build`, `vite build`, `rollup` |
| **dependency** | `npm ci`, `ERESOLVE`, `peer dep` |

Extract the exact error message, file path, and line number.

Use superpowers:systematic-debugging to find root cause before attempting any fix.

### 3. Reproduce Locally

Run the failing CI step locally from `apps/web/`:

| CI Step | Local Command |
|---------|--------------|
| typecheck | `npm run typecheck` |
| lint | `npm run lint` |
| unit test | `npm run test` |
| e2e test | `npm run test:e2e` |
| build | `npm run build` |
| install | `npm ci` |

If reproducing a specific test:
- Unit: `npx vitest run <test-file>`
- E2E: `npx playwright test <spec-file>`

### 4. Investigate with Playwright (if E2E failure)

If the failure is an E2E test or a visual/runtime bug:

1. Start the dev server if not running: check `lsof -i :3000`
2. Navigate to the failing page: `mcp__playwright__browser_navigate`
3. Take a screenshot: `mcp__playwright__browser_take_screenshot`
4. Check console errors: `mcp__playwright__browser_console_messages`
5. Check network failures: `mcp__playwright__browser_network_requests`
6. Get the accessibility tree: `mcp__playwright__browser_snapshot`
7. Interact as the test would — click, fill forms, etc.
8. Compare actual behavior with what the test expects

### 5. Fix the Issue

- Read the failing source code
- Apply the minimal fix
- If the test expectation is wrong (not the code), fix the test

### 6. Verify the Fix

Run the exact failing step again locally:
```bash
cd apps/web
# Run the specific failing command
```

Then run the full quality suite to ensure no regressions:
```bash
cd apps/web
npm run typecheck
npm run lint
npm run test
npm run build
```

### 7. Report

Output a summary:

```
## CI Fix Summary
- Run: #<run-id> (<branch>)
- Failed job: <job-name>
- Root cause: <description>
- Fix: <what was changed>
- Local verification: PASS / FAIL
```

## Rules
- Always reproduce locally before fixing — don't guess at fixes
- If the failure is flaky (passes locally, fails in CI), check for:
  - Race conditions / timing issues
  - Missing env vars in CI
  - Different Node.js versions
  - CI-specific caching issues
- Don't disable or skip tests to "fix" CI — fix the underlying issue
- Close the Playwright browser when done: `mcp__playwright__browser_close`
