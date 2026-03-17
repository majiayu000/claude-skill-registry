---
name: agent-cicd
description: GitHub Actions expert for CI/CD pipelines, workflows, build failures, test failures, lint errors, format checks, gh run, gh pr checks, ESLint, Prettier, TypeScript errors, quality gates, automated fixes, pipeline debugging, workflow monitoring
allowed-tools: Read, Write, Edit, Bash
---

# CI/CD Monitoring Skill

Expert in GitHub Actions CI/CD pipeline monitoring and quality gates enforcement.

## When to Use This Skill

Use this skill when:

- Monitoring CI/CD pipeline status
- Analyzing build or test failures
- Fixing linting or formatting issues
- Ensuring code quality before merge
- Debugging GitHub Actions workflows

## Pre-Commit Quality Gates (MANDATORY)

**CRITICAL: ALL code MUST pass local checks BEFORE pushing to GitHub.**

### Complete Check Sequence

**Frontend (from apps/frontend):**

```bash
cd apps/frontend
npm run lint          # Code quality
npm run format:check  # Code formatting
npm run test:ci       # Unit tests
npm run build         # TypeScript compilation
```

**Backend (from apps/backend):**

```bash
cd apps/backend
npm run type-check    # Type checking
npm run format:check  # Code formatting
npm run test          # Unit tests
npm run build         # Compilation
```

### Why Local Checks Are Mandatory

- **CI feedback loop:** 3-5 minutes per iteration
- **Local checks:** <1 minute total
- **Debugging:** 10x faster locally than via CI logs
- **Cost:** Reduces CI/CD usage and costs
- **Developer experience:** Immediate feedback vs waiting for CI

**Rule: NEVER push code without running ALL local checks first.**

## CI/CD Monitoring Workflow

### 1. Monitor PR Status

```bash
# Check PR status
gh pr view <PR_NUMBER> --json statusCheckRollup,mergeable,state

# Watch checks in real-time
gh run watch <RUN_ID>

# List recent runs
gh run list --limit 5
```

### 2. Analyze Failures

When CI fails, follow this process:

```bash
# View failed run details
gh run view <RUN_ID>

# Get failed logs
gh run view <RUN_ID> --log-failed

# Analyze specific job
gh run view <RUN_ID> --job=<JOB_ID> --log
```

### 3. Common Failure Types

#### Linting Failures

```bash
# Error: ESLint found issues
# Fix: Run lint locally
cd apps/frontend && npm run lint

# Auto-fix what's possible
cd apps/frontend && npm run lint -- --fix
```

#### Formatting Failures

```bash
# Error: Prettier formatting mismatch
# Fix: Format code
cd apps/frontend && npm run format

# Verify formatting
cd apps/frontend && npm run format:check
```

#### Test Failures

```bash
# Error: Tests failing
# Fix: Run tests locally to see failures
cd apps/frontend && npm run test:ci

# Debug specific test
cd apps/frontend && npx vitest run path/to/test.spec.ts
```

#### Build Failures

```bash
# Error: TypeScript compilation errors
# Fix: Run type check
cd apps/backend && npm run type-check

# Build locally to see errors
cd apps/backend && npm run build
```

## Automated Fix Patterns

### Pattern 1: Format and Lint Issues

```bash
# Apply fixes
cd apps/frontend
npm run format
npm run lint -- --fix

# Verify fixed
npm run format:check
npm run lint

# Commit and push
git add .
git commit -m "fix: resolve linting and formatting issues"
git push
```

### Pattern 2: Schema Validation Errors

```typescript
// Error: Zod validation failing in production
// Root cause: Schema-query mismatch

// Fix:
// 1. Read database schema
cat docker/postgres/init.sql | grep -A 20 "CREATE TABLE users"

// 2. Compare with Zod schema
// 3. Make required fields optional if:
//    - Column is nullable
//    - Column doesn't exist in table
//    - SELECT query doesn't include column

// 4. Update schema
const UserSchema = z.object({
  id: z.string(),
  email: z.string(),
  role: z.string().optional(), // ← Made optional
});
```

### Pattern 3: Test Failures

```bash
# Run tests locally
cd apps/frontend && npm run test:ci

# Identify failing test
# Read error message carefully
# Fix the underlying issue
# Re-run tests

# Commit fix
git add .
git commit -m "fix: resolve failing unit tests"
git push
```

## Pull Request Status Verification

### Verify All Checks Pass

```bash
# Get PR check status
gh pr checks <PR_NUMBER>

# Should see all checks as "pass"
```

### Wait for Checks Before Merge

```bash
# Poll until checks complete
while true; do
  STATUS=$(gh pr view <PR_NUMBER> --json statusCheckRollup --jq '.statusCheckRollup[].conclusion')
  if [[ "$STATUS" != *"PENDING"* ]]; then
    break
  fi
  sleep 15
done

# Verify all passed
gh pr checks <PR_NUMBER>
```

## Remediation Decision Tree

### If Linting Fails:

1. Run `npm run lint` locally
2. Fix issues or run `npm run lint -- --fix`
3. Commit and push

### If Formatting Fails:

1. Run `npm run format` locally
2. Verify with `npm run format:check`
3. Commit and push

### If Tests Fail:

1. Run tests locally to see failure
2. Debug and fix the root cause
3. Re-run tests to verify fix
4. Commit and push

### If Build Fails:

1. Run `npm run build` or `npm run type-check` locally
2. Fix TypeScript errors
3. Re-run build to verify
4. Commit and push

### If Database Errors:

1. Check schema-query alignment
2. Verify migration exists
3. Test migration locally
4. Fix schema or query
5. Commit and push

## GitHub Actions Workflow

### Common Workflows

- **ci.yml** - Main CI pipeline (lint, test, build)
- **Format check** - Prettier formatting verification
- **Lint check** - ESLint code quality
- **Test** - Unit and integration tests
- **Build** - TypeScript compilation

### Reading Workflow Files

```bash
# View CI workflow
cat .github/workflows/ci.yml

# Understand what checks run
```

## Success Metrics

### CI Health Indicators

- ✅ All checks passing
- ✅ Green checkmarks on PR
- ✅ `mergeable: true` status
- ✅ No failed jobs

### Problem Indicators

- ❌ Red X on checks
- ❌ `mergeable: false`
- ❌ Repeated failures on same issue
- ❌ Pushing without local verification

## Workflow

1. **Monitor** PR status after push
2. **Detect** failures immediately
3. **Analyze** logs to identify root cause
4. **Fix** locally (don't rely on CI for debugging)
5. **Verify** locally with all checks
6. **Push** fix
7. **Re-monitor** until all checks pass
8. **Only then** proceed with merge

## Reference Files

For detailed patterns and examples:

- `.claude/agents/agent-cicd.md` - Complete agent specification
- `.github/workflows/ci.yml` - CI workflow configuration
- `CLAUDE.md` - Project conventions

## Critical Reminders

- **Local checks are mandatory** - Never skip
- **CI is verification, not debugging** - Debug locally
- **Fix root cause, not symptoms** - Don't just make CI pass
- **All checks must pass** - Don't merge with failing checks
- **Re-run flaky tests** - Verify consistency

## Success Criteria

Before marking work complete:

- [ ] All CI checks passing
- [ ] PR status is mergeable
- [ ] No linting errors
- [ ] No formatting issues
- [ ] All tests passing
- [ ] Build successful
- [ ] Ready for merge
