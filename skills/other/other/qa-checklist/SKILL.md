---
name: qa-checklist
description: Formal Quality Assurance Checklist before every Merge/Deploy. 6-phase validation with Build Verification, Test Suite, No-Touch Zones, Region Check, Security Review, and QA Report generation. Activate on "merge", "deploy", "release", "production", or /qa command.
---

# QA Checklist

> Formal Quality Assurance Checklist before every Merge/Deploy

## Trigger

This skill activates automatically on:

- `git commit` (after production code changes)
- Deploy commands (`vercel --prod`, `npm run deploy`, etc.)
- `/qa` command
- Trigger words: "merge", "deploy", "release", "production"

---

## Configuration

Customize these values for your project:

```yaml
# Add to your project's CLAUDE.md or settings
no_touch_zones:
  - "src/auth/**"           # Authentication logic
  - "src/core/**"           # Core business logic
  - "config/production.*"   # Production config

required_region: "your-region"  # e.g., fra1, us-east-1
deploy_timeout: 60              # seconds
```

---

## PHASE 1: Build Verification (BLOCKING)

### 1.1 TypeScript Compilation

```bash
npx tsc --noEmit
```

**Expected:** No errors

| Status | Action |
|--------|--------|
| PASS | Continue to 1.2 |
| FAIL | STOP - Fix type errors |

### 1.2 Production Build

```bash
npm run build
```

**Expected:** Build successful, no warnings

| Status | Action |
|--------|--------|
| PASS | Continue to Phase 2 |
| FAIL | STOP - Fix build errors |

---

## PHASE 2: Test Suite (BLOCKING)

### 2.1 Unit Tests

```bash
npm run test
```

**Expected:** All tests green

### 2.2 E2E Tests (optional but recommended)

```bash
npm run test:e2e
```

**Expected:** Critical flows working

---

## PHASE 3: No-Touch Zones Check (BLOCKING)

Check if protected files were modified:

```bash
# Replace with your no-touch zones
git diff --name-only HEAD~1 | grep -E "(auth|core|production)"
```

**Expected:** No matches (or explicit approval present)

| File Pattern | Modification Allowed? |
|--------------|----------------------|
| `**/auth/**` | ONLY with explicit request |
| `**/core/**` | ONLY with explicit request |
| `config/production.*` | ONLY with explicit request |

---

## PHASE 4: Region/Environment Check (BLOCKING on Deploy)

### 4.1 Before Production Deploy

Verify deployment target matches requirements:

```bash
# Vercel example
npx vercel inspect <preview-url> --wait

# AWS example
aws configure get region

# Check environment
echo $NODE_ENV
```

**Expected:** Correct region/environment

### 4.2 After Production Deploy

```bash
# Verify production deployment
curl -s -o /dev/null -w "%{http_code}" https://your-domain.com/health
```

**Expected:** 200 OK

---

## PHASE 5: Security Review (WARNING)

### 5.1 No Secrets in Code

```bash
git diff HEAD~1 | grep -iE "(password|secret|api_key|token|private_key)" | grep -v "process\.env\|\.env\|example"
```

**Expected:** No matches

### 5.2 No Unsafe Types

```bash
# TypeScript: Check for untyped any
git diff HEAD~1 --name-only -- "*.ts" "*.tsx" | xargs grep -l ": any" 2>/dev/null
```

**Expected:** No new `any` types (or documented reason)

### 5.3 Dependency Check

```bash
npm audit --production
```

**Expected:** No high/critical vulnerabilities

---

## PHASE 6: QA Report

After completing all checks, generate a report:

```markdown
## QA Validation Report

**Date:** [ISO Timestamp]
**Branch:** [Branch Name]
**Commit:** [Commit Hash]

### Results

| Check | Status | Details |
|-------|--------|---------|
| TypeScript | PASS/FAIL | [Error count] |
| Build | PASS/FAIL | [Build time] |
| Unit Tests | PASS/FAIL | [X/Y passed] |
| E2E Tests | PASS/FAIL/SKIP | [X/Y passed] |
| No-Touch Zones | PASS/FAIL | [Affected files] |
| Region | PASS/FAIL/N/A | [Current region] |
| Security | PASS/WARN | [Issues found] |

### Verdict

**Status:** APPROVED / REJECTED

**Next Steps:**
- [If APPROVED: Merge/Deploy allowed]
- [If REJECTED: List of issues to fix]
```

---

## Workflow Integration

### Before Every Commit

1. Run Phase 1-3
2. On PASS: Commit allowed
3. On FAIL: Fix issues, re-run

### Before Production Deploy

1. Run Phase 1-5
2. On PASS: Deploy allowed
3. On FAIL: Fix issues, re-run
4. After Deploy: Phase 4.2 (Verification)

### QA Loop (max 3 iterations)

```
1. Run checks
2. On failure: Implement fix
3. Return to step 1
4. After 3 iterations: Escalate to user
```

---

## Integration with Other Skills

- **code-quality-gate**: Can be used together for comprehensive checks
- **strict-typescript-mode**: Enforces Phase 5.2 automatically
- **security-scan hook**: Automates Phase 5.1

---

## Origin

Originally developed for [fabrikIQ](https://fabrikiq.com) - AI-powered manufacturing data analysis.

## License

MIT - Free to use and modify
