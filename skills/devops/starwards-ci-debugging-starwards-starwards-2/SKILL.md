---
name: starwards-ci-debugging
description: Debug Starwards GitHub Actions CI failures - analyze logs for ESLint/TypeScript/E2E/Docker errors, identify root causes, and apply fixes locally before pushing
version: 2025-11-05
related_skills:
  - github-api (GitHub CLI setup and API access)
  - starwards-debugging (systematic debugging framework)
  - starwards-verification (verify fixes with test commands)
  - starwards-monorepo (understand build dependencies)
  - using-superpowers (announce skill usage)
---

# CI Debugging for Starwards

## Overview

Debug GitHub Actions CI failures independently by downloading logs and analyzing them locally.

**Core principle:** ALWAYS download CI logs before attempting to debug failures.

**Prerequisites:** Use the **github-api** skill to set up GitHub CLI access first.

## The Iron Law

```
NO CI DEBUGGING WITHOUT LOG ACCESS FIRST
```

If you haven't downloaded logs, you cannot diagnose CI failures.

## When to Use

**Any Starwards GitHub Actions failure:**
- Test-Static (TypeScript, ESLint, Prettier)
- Test-Units (Jest test failures)
- Test-E2e (Playwright test failures)
- Build failures
- Workflow configuration errors

## Quick Start

**Prerequisites:**
1. Use **github-api** skill to install GitHub CLI
2. Verify authentication: `gh auth status`
3. Set alias: `GH="/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh"`

**Quick Workflow:**
```bash
# 1. Get PR checks
$GH pr checks <PR_NUMBER> --repo starwards/starwards

# 2. Extract run ID from URL
RUN_ID=$($GH pr checks <PR_NUMBER> --repo starwards/starwards | grep -oP 'runs/\K[0-9]+' | head -1)

# 3. Download logs
$GH api repos/starwards/starwards/actions/runs/$RUN_ID/logs --paginate > /tmp/run-logs.zip
cd /tmp && unzip -o -q run-logs.zip

# 4. Analyze failures (see sections below)
```

## CI Log Analysis

### Identify Failed Jobs

```bash
# Get failed jobs and steps
$GH api repos/starwards/starwards/actions/runs/<RUN_ID>/jobs \
  --jq '.jobs[] | select(.conclusion=="failure") | {name, steps: [.steps[] | select(.conclusion=="failure") | .name]}'
```

**Example output:**
```json
{
  "name": "Test-Static",
  "steps": ["Run npm run test:format"]
}
{
  "name": "Test-E2e",
  "steps": ["Run npm run test:e2e"]
}
```

### Log File Organization

Downloaded logs are named by job:
```
/tmp/0_Test-Units.txt
/tmp/1_Build.txt
/tmp/2_Test-E2e.txt
/tmp/3_Test-Static.txt
```

### Test-Static Analysis

```bash
# Find ESLint errors
grep "##\[error\]" /tmp/3_Test-Static.txt

# Find TypeScript errors
grep "error TS" /tmp/3_Test-Static.txt

# Find Prettier failures
grep -A 5 "Code style issues" /tmp/3_Test-Static.txt

# Group TypeScript errors by code
grep "error TS" /tmp/3_Test-Static.txt | grep -oP 'error TS\d+' | sort | uniq -c
```

### Test-E2e Analysis

```bash
# Find Playwright errors
grep -E "FAIL|Error:" /tmp/2_Test-E2e.txt | head -50

# Find browser launch errors
grep "Executable doesn't exist" /tmp/2_Test-E2e.txt

# Find test assertion failures
grep -A 10 "Expected.*Received" /tmp/2_Test-E2e.txt

# Find timeout issues
grep -i "timeout" /tmp/2_Test-E2e.txt
```

### Test-Units Analysis

```bash
# Find test failures
grep -A 20 "FAIL " /tmp/0_Test-Units.txt

# Find timeout errors
grep "Timeout" /tmp/0_Test-Units.txt

# Find assertion errors
grep -B 5 -A 10 "expect.*toEqual\|toBe\|toBeCloseTo" /tmp/0_Test-Units.txt

# Find connection errors (common in Colyseus tests)
grep -i "connection.*error\|ECONNREFUSED" /tmp/0_Test-Units.txt
```

## Common Starwards CI Failures

### 1. ESLint: Unsafe `any` Type Usage

**Symptoms:**
```
##[error]  192:23  error  Unsafe assignment of an `any` value  @typescript-eslint/no-unsafe-assignment
##[error]  192:61  error  Unexpected any. Specify a different type  @typescript-eslint/no-explicit-any
```

**Root cause:** Using `(e as any).code` violates strict TypeScript rules.

**Fix pattern:**
```typescript
// BEFORE (fails lint):
const hasCode = typeof (e as any).code === 'string' && (e as any).code;
const code = String((e as any).code);

// AFTER (passes lint):
function hasStringCode(e: unknown): e is { code: string } {
    return typeof (e as { code?: unknown })?.code === 'string'
        && !!(e as { code?: string }).code;
}

if (hasStringCode(e)) {
    const code = e.code; // Type-safe!
}
```

**Local verification:**
```bash
npm run lint
# Expected: No errors
```

### 2. Playwright: Browser Executable Not Found

**Symptoms:**
```
Error: browserType.launch: Executable doesn't exist at /ms-playwright/chromium_headless_shell-1194/chrome-linux/headless_shell
```

**Root cause:** Docker image version doesn't match installed Playwright version.

**Diagnosis:**
```bash
# Check package version
grep '"@playwright/test"' package.json
# Example: "@playwright/test": "^1.56.1"

# Check exact installed version
grep -A 15 'node_modules/@playwright/test"' package-lock.json | grep '"version"' | head -1
# Example: "version": "1.56.1"

# Check CI workflow Docker image
grep "mcr.microsoft.com/playwright" .github/workflows/ci-cd.yml
# Example: image: mcr.microsoft.com/playwright:v1.42.1-jammy
#                                                 ^^^^^^^ MISMATCH!
```

**Fix:**
```yaml
# .github/workflows/ci-cd.yml
Test-E2e:
    runs-on: ubuntu-latest
    container:
        image: mcr.microsoft.com/playwright:v1.56.1-jammy  # Match package version exactly
        options: --user 1001
```

**Find available versions:**
```bash
curl -s https://mcr.microsoft.com/v2/playwright/tags/list | jq -r '.tags[] | select(startswith("v1.5"))' | sort -V | tail -10
```

**Local verification:**
```bash
# Cannot test Docker image locally, must verify on CI
git add .github/workflows/ci-cd.yml
git commit -m "Update Playwright Docker image to v1.56.1"
git push
```

### 3. TypeScript: Type Errors

**Symptoms:**
```
modules/core/src/file.ts(42,15): error TS2322: Type 'string | undefined' is not assignable to type 'string'
```

**Common error codes:**
- `TS2322`: Type mismatch - add type assertion or fix types
- `TS2532`: Possibly undefined - add null check or `!` assertion
- `TS2345`: Argument type mismatch - check function signature
- `TS2339`: Property doesn't exist - check interface/type definition

**Local verification:**
```bash
npm run test:types
# Expected: No errors
```

### 4. Jest: Flaky Colyseus Tests

**Symptoms:**
```
connection error: AggregateError
expect(received).toEqual(expected)
  "text": "err: "  // Expected "err: ECONNREFUSED"
```

**Common causes:**
- Dependency update changed error message format
- Race condition in async test
- Port conflict (rare)
- Timing issue in Colyseus state sync

**Diagnosis:**
```bash
# Check recent changes
git log --oneline -5
git diff HEAD~1 package.json

# Search for error in logs
grep -B 10 -A 10 "expect.*toEqual" /tmp/0_Test-Units.txt

# Look for timing issues
grep -i "timeout\|race\|async" /tmp/0_Test-Units.txt
```

**Fix pattern:**
- Update expected error format to match new behavior
- Add longer timeouts for flaky tests
- Use `waitFor` helpers from `@testing-library/react`
- Check Colyseus state sync timing

### 5. Build Failures

**Symptoms:**
```
error TS6059: File '...' is not under 'rootDir'
error TS5055: Cannot write file '...' because it would overwrite input file
```

**Common causes:**
- Circular dependencies
- Module import issues
- Monorepo build order violation
- Missing `npm run build:core` before dependent modules

**Diagnosis:**
```bash
# Check build order
grep "npm run build" .github/workflows/ci-cd.yml

# Check for circular deps
npm ls | grep "deduped"

# Verify module dependencies
cat modules/browser/package.json | jq '.dependencies'
```

**Fix:**
- Use **starwards-monorepo** skill for build order issues
- Check imports in affected files
- Ensure `core` builds before `browser`/`server`

## Complete CI Debug Workflow

### Full Script

```bash
#!/bin/bash
set -e

# Setup (use github-api skill for this part)
GH="/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh"
REPO="starwards/starwards"
PR_NUMBER=$1

if [ -z "$PR_NUMBER" ]; then
  echo "Usage: $0 <PR_NUMBER>"
  exit 1
fi

echo "=== Step 1: Check PR Status ==="
$GH pr view $PR_NUMBER --repo $REPO

echo -e "\n=== Step 2: Get Check Results ==="
$GH pr checks $PR_NUMBER --repo $REPO

echo -e "\n=== Step 3: Identify Failed Jobs ==="
RUN_ID=$($GH pr checks $PR_NUMBER --repo $REPO | grep -oP 'runs/\K[0-9]+' | head -1)
echo "Run ID: $RUN_ID"

$GH api repos/$REPO/actions/runs/$RUN_ID/jobs \
  --jq '.jobs[] | select(.conclusion=="failure") | {
    name: .name,
    failed_steps: [.steps[] | select(.conclusion=="failure") | .name]
  }'

echo -e "\n=== Step 4: Download Logs ==="
$GH api repos/$REPO/actions/runs/$RUN_ID/logs --paginate > /tmp/run-logs.zip
cd /tmp && unzip -o -q run-logs.zip
echo "Logs extracted to /tmp/*.txt"

echo -e "\n=== Step 5: Analyze Failures ==="
echo "TypeScript errors:"
grep -h "error TS" /tmp/*.txt | head -10 || echo "None found"

echo -e "\nESLint errors:"
grep -h "##\[error\]" /tmp/*.txt | head -10 || echo "None found"

echo -e "\nTest failures:"
grep -h "FAIL.*spec\." /tmp/*.txt | head -10 || echo "None found"

echo -e "\nBrowser errors:"
grep -h "Executable doesn't exist" /tmp/*.txt || echo "None found"

echo -e "\n=== Step 6: Next Steps ==="
echo "1. Review errors above"
echo "2. Fix issues locally"
echo "3. Run: npm run lint && npm test && npm run build"
echo "4. Commit and push"
echo "5. Monitor new CI run with: $GH pr checks $PR_NUMBER --repo $REPO"
```

### Save and Use

```bash
# Save script
cat > /tmp/debug-ci.sh << 'EOF'
[paste script above]
EOF

chmod +x /tmp/debug-ci.sh

# Run
/tmp/debug-ci.sh 1826
```

## Local Verification Checklist

Before pushing CI fixes:

```bash
# ☐ Lint passes
npm run lint

# ☐ Type check passes
npm run test:types

# ☐ Unit tests pass
npm test

# ☐ Build succeeds
npm run build

# ☐ E2E tests pass (if applicable)
npm run test:e2e

# ☐ Format is correct
npm run test:format
```

## Monitoring After Push

```bash
# Wait for CI to start
sleep 30

# Check new run status
$GH pr checks <PR_NUMBER> --repo starwards/starwards

# If still failing, download new logs and repeat
RUN_ID=$($GH pr checks <PR_NUMBER> --repo starwards/starwards | grep -oP 'runs/\K[0-9]+' | head -1)
$GH api repos/starwards/starwards/actions/runs/$RUN_ID/logs --paginate > /tmp/run-logs-retry.zip
```

## Integration with Other Skills

- **github-api** - Setup GitHub CLI, download logs, query API
- **starwards-debugging** - Systematic debugging for local reproduction
- **starwards-verification** - Run verification commands before push
- **starwards-monorepo** - Understand build dependencies and order
- **starwards-workflow** - Terminal commands for local testing

## Quick Reference

### GitHub CLI Commands
See **github-api** skill for:
- Installation and setup
- Authentication
- API access patterns
- Rate limiting

### CI-Specific Commands
```bash
# Get PR checks
$GH pr checks <PR> --repo starwards/starwards

# Get run details
$GH run view <RUN_ID> --repo starwards/starwards

# Download logs
$GH api repos/starwards/starwards/actions/runs/<RUN_ID>/logs --paginate > /tmp/logs.zip

# Get failed jobs
$GH api repos/starwards/starwards/actions/runs/<RUN_ID>/jobs \
  --jq '.jobs[] | select(.conclusion=="failure")'
```

### Log Analysis Patterns
```bash
# ESLint errors
grep "##\[error\]" /tmp/*.txt

# TypeScript errors
grep "error TS" /tmp/*.txt

# Test failures
grep "FAIL " /tmp/*.txt

# Playwright errors
grep "Executable doesn't exist" /tmp/*.txt

# Assertion failures
grep -A 10 "Expected.*Received" /tmp/*.txt
```

## Tips

1. **Download logs first** - Always get complete context before debugging
2. **Check run ID** - Ensure you're analyzing the correct workflow run
3. **Group errors** - Use `sort | uniq -c` to identify patterns
4. **Verify locally** - Run all checks before pushing
5. **Monitor after push** - Watch new CI run to confirm fix
6. **Check dependencies** - Build order matters in monorepos
7. **Save scripts** - Keep debug workflow script for repeated use

## Real-World Example

**Scenario: PR #1826 failing with Test-Static and Test-E2e**

```bash
# Setup (github-api skill)
GH="/tmp/gh-install/gh_2.62.0_linux_amd64/bin/gh"

# Check status
$GH pr checks 1826 --repo starwards/starwards
# Test-Static: FAIL
# Test-E2e: FAIL

# Download logs
RUN_ID=19084760492
$GH api repos/starwards/starwards/actions/runs/$RUN_ID/logs --paginate > /tmp/run-logs.zip
cd /tmp && unzip -o -q run-logs.zip

# Analyze Test-Static
grep "##\[error\]" /tmp/3_Test-Static.txt
# Found: 7 ESLint errors about unsafe `any` usage
# File: modules/core/src/client/connection-manager.ts line 192

# Analyze Test-E2e
grep "Executable doesn't exist" /tmp/2_Test-E2e.txt
# Found: Playwright browser missing
# Cause: Docker image v1.42.1 vs package v1.56.1

# Fix: Add type guard for ESLint
# Fix: Update .github/workflows/ci-cd.yml to use playwright:v1.56.1-jammy

# Verify locally
npm run lint      # ✓ Passes
npm run test:types # ✓ Passes

# Push
git add -A
git commit -m "Fix CI failures: eslint errors and Playwright version mismatch"
git push

# Monitor
sleep 30
$GH pr checks 1826 --repo starwards/starwards
# Result: All CI checks pass ✅
```
