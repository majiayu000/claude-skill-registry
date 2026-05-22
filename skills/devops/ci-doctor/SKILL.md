---
name: ci-doctor
description: |
  Diagnose and fix CI/CD pipeline failures, test errors, GitHub Actions issues, and code scanning alerts.

  Use when:
  - CI pipeline fails (red build)
  - GitHub Actions workflow errors
  - Test failures in CI (Vitest, Playwright)
  - TypeScript/lint errors blocking builds
  - GitHub notifications about failed checks
  - "CI is red" or "build failed" or "tests failing"
  - Supabase/OpenAPI type generation failures
  - Pre-commit hook failures
  - GitHub Code Scanning alerts (CodeQL)
  - Security vulnerabilities in code
  - /security/code-scanning alerts

  Triggers: "fix ci", "ci failed", "build broken", "tests failing in ci", "github actions error", "pipeline red", "check failed", "code scanning", "codeql", "security alert", "vulnerability"
---

# CI Doctor

Diagnose and fix CI failures fast. Read logs, identify root cause, fix or delegate.

## Context Files (Read First)

For project structure, read from `Docs/context/`:
- `Docs/context/repo-structure.md` - File locations
- `Docs/context/conventions.md` - CI/build patterns

## Workflow

```
1. FETCH    → Get failure details (gh cli or logs)
2. DIAGNOSE → Identify error category
3. FIX      → Apply fix or delegate to specialist skill
4. VERIFY   → Run locally to confirm
5. PUSH     → Commit and push fix
```

## Step 1: Fetch Failure Details

```bash
# Get recent workflow runs
gh run list --limit 5

# Get failed run details
gh run view <run-id>

# Get job logs
gh run view <run-id> --log-failed

# Get PR checks
gh pr checks
```

If user provides a GitHub URL, extract info with `gh`:
```bash
gh pr view <url> --json statusCheckRollup
gh run view <url>
```

## Step 2: Diagnose Error Category

| Error Pattern | Category | Action |
|---------------|----------|--------|
| `tsc` errors, "TS2xxx" | TypeScript | Fix type errors |
| `biome lint`, "lint error" | Lint | Delegate to `lint-fixer` |
| `FAIL src/...test.ts` | Test failure | Delegate to `test-writer` or fix |
| `npm ci` failed | Dependency | Check package-lock.json |
| `types.ts changed` | Generated types | Regenerate and commit |
| `timeout`, `ETIMEDOUT` | Flaky/infra | Retry or increase timeout |
| `permission denied` | Secrets/auth | Check workflow permissions |
| CodeQL alert, code scanning | Security vulnerability | See "Code Scanning Alerts" section |

## Step 3: Fix by Category

### TypeScript Errors

```bash
# Run locally to see all errors
npm run typecheck:ci
# or
npx tsc -p tsconfig.ci.json --noEmit
```

Fix each error. Common patterns:
- Missing imports
- Type mismatches
- Unused variables (remove or prefix with `_`)

### Lint Errors

Delegate: `Use the lint-fixer skill`

Or quick fix:
```bash
npx @biomejs/biome check --write .
```

### Test Failures

1. Run failing test locally:
```bash
npm run test --workspace=apps/raamattu-nyt -- --run <test-file>
```

2. If complex, delegate: `Use the systematic-debugging skill`

3. If test needs update, delegate: `Use the test-writer skill`

### Generated Types Out of Sync

**Supabase types:**
```bash
# Regenerate (requires SUPABASE_PROJECT_ID and SUPABASE_ACCESS_TOKEN)
npx supabase gen types typescript --project-id "$SUPABASE_PROJECT_ID" > apps/raamattu-nyt/src/integrations/supabase/types.ts
git add apps/raamattu-nyt/src/integrations/supabase/types.ts
git commit -m "Regenerate Supabase types"
```

**OpenAPI types:**
```bash
npx openapi-typescript ./openapi.yaml -o apps/raamattu-nyt/src/lib/openapi.types.ts
git add apps/raamattu-nyt/src/lib/openapi.types.ts
git commit -m "Regenerate OpenAPI types"
```

### Dependency Issues

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
git add package-lock.json
git commit -m "Refresh package-lock.json"
```

### Code Scanning Alerts (CodeQL)

GitHub Code Scanning uses CodeQL to find security vulnerabilities. Access alerts via:

```bash
# List all code scanning alerts
gh api repos/{owner}/{repo}/code-scanning/alerts --jq '.[] | {number, state, rule: .rule.id, severity: .rule.security_severity_level, file: .most_recent_instance.location.path, line: .most_recent_instance.location.start_line}'

# Get specific alert details
gh api repos/{owner}/{repo}/code-scanning/alerts/<alert-number>

# List open alerts only
gh api repos/{owner}/{repo}/code-scanning/alerts?state=open
```

**Common CodeQL Alerts and Fixes:**

| Alert Type | Fix |
|------------|-----|
| `js/xss` | Sanitize user input before rendering, use `textContent` not `innerHTML` |
| `js/sql-injection` | Use parameterized queries, never concatenate user input |
| `js/path-injection` | Validate/sanitize file paths, use `path.join` with basename |
| `js/prototype-pollution` | Use `Object.create(null)` or validate object keys |
| `js/insecure-randomness` | Use `crypto.randomUUID()` instead of `Math.random()` |
| `js/hardcoded-credentials` | Move secrets to environment variables |
| `js/log-injection` | Sanitize user input before logging |
| `js/regex-injection` | Escape regex special characters in user input |

**Workflow:**
1. Fetch alert details with `gh api`
2. Read the affected file and understand the vulnerability
3. Apply the appropriate fix
4. Test locally
5. Commit and push - CodeQL will re-analyze

**Dismissing False Positives:**
```bash
# Dismiss alert as false positive
gh api -X PATCH repos/{owner}/{repo}/code-scanning/alerts/<number> -f state=dismissed -f dismissed_reason=false_positive -f dismissed_comment="Reason here"
```

## Step 4: Verify Locally

Before pushing, run the same checks CI runs:

```bash
# TypeScript
npm run typecheck:ci || npx tsc -p tsconfig.ci.json

# Lint
npx @biomejs/biome lint .

# Build
npm run build

# Tests
npm run test --workspace=apps/raamattu-nyt
```

## Step 5: Push Fix

```bash
git add -A
git commit -m "Fix CI: <brief description>"
git push
```

Then monitor: `gh run watch`

## Project CI Structure

This project has these workflows:

| Workflow | File | Triggers | Checks |
|----------|------|----------|--------|
| CI | `.github/workflows/ci.yml` | PR, push to main | TypeScript, Lint, Build |
| Tests | `.github/workflows/tests.yml` | PR, push (code changes) | Vitest, Playwright smoke |
| Supabase Sync | `.github/workflows/supabase-sync.yml` | Various | Type generation |

## Delegation Guide

| Situation | Delegate To |
|-----------|-------------|
| Lint/format errors | `lint-fixer` skill |
| Test needs rewriting | `test-writer` skill |
| Complex bug in test | `systematic-debugging` skill |
| Supabase migration issue | `supabase-migration-writer` skill |
| Type refactoring needed | `code-refactoring` skill |

## Quick Commands Reference

```bash
# See what's failing
gh pr checks
gh run list --limit 3

# Get logs for failed run
gh run view <id> --log-failed

# Re-run failed jobs
gh run rerun <id> --failed

# Watch current run
gh run watch
```
