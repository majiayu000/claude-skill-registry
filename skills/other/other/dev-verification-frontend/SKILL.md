---
version: 1.1.0
name: dev-verification-frontend
description: >
  Post-change verification for Angular/TypeScript frontend code — build, TypeScript
  type check, ESLint, unit tests with coverage, npm audit, and diff review.
  Invoked via /dev-verify (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
argument-hint: "[--quick | --full | --fix]"
---

# Verification Loop — Frontend (Angular)

Run a comprehensive quality check on Angular/TypeScript code after changes.

> **Stack:** Angular/TypeScript

## When to Use

- After completing a feature or significant frontend code change
- Before creating a PR
- After refactoring components, services, or state management
- When you want to ensure quality gates pass

## Verification Phases

### Phase 1: Build

```bash
ng build --configuration production 2>&1 | tail -20
```

If build fails, **STOP and fix** before continuing. Production build catches AOT compilation issues that dev mode misses.

### Phase 2: Type Check

```bash
npx tsc --noEmit 2>&1 | head -30
```

Report all type errors. Fix critical ones before continuing.

### Phase 3: Lint / Format Check

```bash
# ESLint
ng lint --max-warnings 0 2>&1 | head -30
# Or: npx eslint . --max-warnings 0

# Prettier (if configured)
npx prettier --check "src/**/*.{ts,html,scss}" 2>&1 | head -10

# Stylelint (if configured)
npx stylelint "src/**/*.scss" 2>&1 | head -10
```

If `--fix` flag:
```bash
ng lint --fix
npx prettier --write "src/**/*.{ts,html,scss}"
```

### Phase 4: Test Suite (Vitest)

Tests run through Angular CLI (`ng test`) which delegates to Vitest 4.x as the test runner.

```bash
ng test --watch=false --code-coverage 2>&1 | tail -50
```

Tests use `@testing-library/angular` for component testing — prefer its queries (`getByRole`, `getByText`) over direct DOM access.

Report:
```
Total tests: X
Passed: X
Failed: X
Coverage: X%
```

### Phase 5: Service Worker Verification

After a successful build, verify the service worker configuration:

```bash
# Check ngsw-config.json is valid
cat ngsw-config.json | python3 -m json.tool > /dev/null 2>&1 && echo "VALID" || echo "INVALID"

# Verify service worker is in build output
ls dist/*/ngsw-worker.js 2>/dev/null && echo "SW present" || echo "SW missing"
ls dist/*/ngsw.json 2>/dev/null && echo "SW manifest present" || echo "SW manifest missing"
```

### Phase 5b: Aspire Runtime Check (Optional)

If the frontend is served through an Aspire AppHost, verify runtime health:

**Step 1 — Resource health:**
```
mcp__aspire__list_resources
```
Verify the frontend resource (proxy or container) shows `Running`. Check the API resource is also healthy — frontend failures are often caused by backend issues.

**Step 2 — Console errors:**
```
mcp__aspire__list_console_logs  resourceName: "site"
```
Scan for Angular runtime errors: `ERROR`, `ExpressionChangedAfterItHasBeenCheckedError`, `NullInjectorError`, `NG0`, chunk load failures, or CORS errors.

**Step 3 — API errors from frontend requests:**
```
mcp__aspire__list_structured_logs  resourceName: "api"
```
Filter for `Error` severity. Check for 4xx/5xx responses triggered by frontend requests — these indicate API contract mismatches, missing endpoints, or authorization issues that the frontend is hitting at runtime.

Report any errors found as verification failures.

Skip if the frontend is not part of an Aspire deployment.

### Phase 6: Security Scan

```bash
# npm dependency vulnerabilities
npm audit --production 2>&1 | head -20

# Check for console.log left in source (should use proper logging)
grep -rn "console\.\(log\|debug\)" --include="*.ts" src/ 2>/dev/null | grep -v "\.spec\.ts" | head -10

# Check for debugger statements
grep -rn "debugger" --include="*.ts" src/ 2>/dev/null | grep -v "\.spec\.ts" | head -5

# Check for hardcoded API URLs or tokens
grep -rn "localhost:\|http://\|Bearer \|apikey" --include="*.ts" src/ 2>/dev/null | grep -v "environment" | grep -v "\.spec\.ts" | head -10
```

### Phase 7: Diff Review

```bash
git diff --stat
git diff HEAD~1 --name-only
```

Review each changed file for:
- Unintended changes
- Missing error handling (uncaught Observable errors)
- `any` types that should be properly typed
- Missing `OnPush` change detection where appropriate
- Missing `unsubscribe` / `takeUntilDestroyed` on subscriptions
- Hardcoded strings that should be in i18n files
- Missing `data-testid` attributes on interactive elements

## Output Format

```
VERIFICATION REPORT — Frontend (Angular)
==========================================

Build:     [PASS/FAIL]
TypeCheck: [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
SW:        [PASS/FAIL] (service worker check)
Aspire:    [PASS/SKIP] (proxy health)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR

Issues to Fix:
1. ...
2. ...
```

## Flags

| Flag | Behavior |
|------|----------|
| `--quick` | Build + type check only (skip tests, security) |
| `--full` | All phases (default) |
| `--fix` | Auto-fix lint and formatting (`ng lint --fix`, `prettier --write`) |

## CI Alignment

These verification phases mirror what GitHub Actions CI runs: `npm ci`, `ng build --configuration production`. Running this locally catches the same issues CI would flag, avoiding failed PR checks.
