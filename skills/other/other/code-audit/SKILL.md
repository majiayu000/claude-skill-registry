---
name: code-audit
description: "Security audit, code quality review, and tech debt assessment for full-stack codebases. Run after major phases, at build completion, or cold on new codebases to surface issues before external review."
version: 1.0.0
triggers:
  - phase_complete
  - build_complete
  - manual
---

# Code Audit Skill

## Purpose

Surface security vulnerabilities, code quality issues, and tech debt before external eyes see them. Functions as:

- Post-phase validation during builds
- Final QA before shipping
- Cold assessment of acquired/inherited codebases
- Pre-DD preparation

## Execution Modes

### Quick Scan (5-10 min)

Run after phases. Catches obvious issues fast.

```
Phases: 1, 2, 3 (partial)
Output: PASS / FAIL with blockers only
```

### Full Audit (30-60 min)

Run at build completion or on new codebases.

```
Phases: All
Output: Full report with severity ratings
```

### Cold Assessment (60-90 min)

First look at unknown codebase. Includes architecture understanding.

```
Phases: All + architecture mapping
Output: Full report + codebase overview + risk assessment
```

---

## Phase 1: Codebase Reconnaissance

**Time: 5 min | Run: Always**

### Commands

```bash
# Structure overview
tree -L 3 -d --dirsfirst -I 'node_modules|.next|dist|.git|coverage|vendor'

# Size and composition
cloc . --exclude-dir=node_modules,dist,.next,vendor,coverage --quiet

# Git health
echo "=== Commit Activity (6 months) ==="
git log --oneline --since="6 months ago" 2>/dev/null | wc -l

echo "=== Contributors ==="
git shortlog -sn --no-merges 2>/dev/null | head -10

echo "=== Last 10 commits ==="
git log --oneline -10 2>/dev/null

# Package manager detection
ls -la package*.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null
```

### Flags

| Signal                      | Severity  | Meaning                 |
| --------------------------- | --------- | ----------------------- |
| < 10 commits in 6 months    | ⚠️ Medium | Stale or abandoned      |
| 1 contributor > 90% commits | ⚠️ Medium | Bus factor = 1          |
| No lock file                | 🔴 High   | Non-reproducible builds |
| Multiple lock files         | ⚠️ Medium | Tooling confusion       |

### Output

```
## Recon Summary
- Stack: [detected]
- Size: [X] files, [Y] LOC
- Contributors: [N] ([top contributor] owns [X]%)
- Velocity: [N] commits/month
- Bus Factor: [1-5 rating]
```

---

## Phase 2: Dependency Audit

**Time: 5-10 min | Run: Always**

### Commands

```bash
# Vulnerability scan
npm audit --json 2>/dev/null | jq '{critical: .metadata.vulnerabilities.critical, high: .metadata.vulnerabilities.high, moderate: .metadata.vulnerabilities.moderate}'

# Alternative: more thorough
npx better-npm-audit audit --level moderate

# Outdated packages
npm outdated --json 2>/dev/null | jq 'to_entries | map(select(.value.current != .value.latest)) | length'

# Unused dependencies
npx depcheck --json 2>/dev/null | jq '{unused: .dependencies, missing: .missing}'

# Check for known problematic packages
echo "=== Problematic Package Check ==="
grep -E "moment|request|node-uuid|crypto-js@[123]\." package.json 2>/dev/null && echo "Found legacy packages"
```

### For Python Projects

```bash
pip-audit --format=json 2>/dev/null
pip list --outdated --format=json 2>/dev/null
```

### Flags

| Signal                                | Severity    | Meaning                |
| ------------------------------------- | ----------- | ---------------------- |
| Critical vulns > 0                    | 🔴 Critical | Immediate fix required |
| High vulns > 5                        | 🔴 High     | Fix before shipping    |
| Dependencies 2+ major versions behind | ⚠️ Medium   | Update debt            |
| Unused deps > 10                      | ⚡ Low      | Bloat, cleanup needed  |
| `moment.js` present                   | ⚡ Low      | Use date-fns or dayjs  |

### Output

```
## Dependency Health
- Vulnerabilities: [X] critical, [Y] high, [Z] moderate
- Outdated: [N] packages behind latest
- Unused: [list if < 10, count if > 10]
- Action Required: [Yes/No]
```

---

## Phase 3: Security Scan

**Time: 10-15 min | Run: Always**

### 3.1 Secrets Detection

```bash
# Git history secrets (CRITICAL)
echo "=== Secrets in Git History ==="
git log -p --all 2>/dev/null | grep -E "(sk_live|pk_live|ghp_|gho_|AKIA[A-Z0-9]{16}|password\s*=\s*['\"][^'\"]+['\"]|api[_-]?key\s*=\s*['\"][^'\"]+['\"])" | head -20

# Current codebase secrets
echo "=== Hardcoded Secrets ==="
grep -rn --include="*.ts" --include="*.tsx" --include="*.js" --include="*.env*" \
  -E "(sk_live|pk_live|ghp_|gho_|AKIA|secret.*=.*['\"][A-Za-z0-9+/]{20,})" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null

# Environment variable patterns (check for proper handling)
echo "=== Env Var Usage ==="
grep -rn "process.env\." --include="*.ts" --include="*.tsx" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | \
  grep -v "process.env.NODE_ENV" | head -20
```

### 3.2 Authentication Review

```bash
echo "=== Auth Implementation ==="
# Find auth-related files
find . -type f \( -name "*.ts" -o -name "*.tsx" \) \
  -path "*/auth/*" -o -name "*auth*" -o -name "*session*" \
  2>/dev/null | grep -v node_modules | head -20

# Session/JWT handling
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(jwt\.|jsonwebtoken|getSession|getServerSession|useSession|signIn|signOut)" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | head -20

# Password handling
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(bcrypt|argon2|pbkdf2|password.*hash|hashPassword)" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null
```

### 3.3 Injection Vulnerabilities

```bash
echo "=== SQL Injection Risk ==="
# Raw queries with interpolation (CRITICAL)
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(\\\$queryRaw|\\\$executeRaw|\.raw\(|\.query\().*\\\$\{" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null

# String concatenation in queries
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(SELECT|INSERT|UPDATE|DELETE|WHERE).*\+" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null

echo "=== XSS Risk ==="
# Dangerous React patterns
grep -rn --include="*.tsx" --include="*.jsx" \
  "dangerouslySetInnerHTML" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null

# innerHTML usage
grep -rn --include="*.ts" --include="*.tsx" \
  "\.innerHTML\s*=" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null
```

### 3.4 API Security

```bash
echo "=== API Route Auth Coverage ==="
# List all API routes
find . -path "*/api/*" -name "*.ts" -not -path "*/node_modules/*" 2>/dev/null | head -30

# Check for auth middleware usage
echo "Routes with auth:"
grep -rln --include="*.ts" \
  -E "(getServerSession|withAuth|requireAuth|authenticate)" \
  --exclude-dir={node_modules,.next,dist} ./app/api ./pages/api 2>/dev/null | wc -l

echo "Total API routes:"
find . \( -path "*/app/api/*" -o -path "*/pages/api/*" \) -name "*.ts" \
  -not -path "*/node_modules/*" 2>/dev/null | wc -l

echo "=== CORS Configuration ==="
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(cors|Access-Control-Allow-Origin)" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null
```

### 3.5 Input Validation

```bash
echo "=== Validation Library Usage ==="
grep -rn --include="*.ts" --include="*.tsx" \
  -E "(zod|yup|joi|class-validator|\.safeParse|\.parse\()" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | head -10

# Unvalidated request body access
echo "=== Unvalidated Request Access ==="
grep -rn --include="*.ts" \
  "request\.body\|req\.body" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | \
  grep -v -E "(parse|valid|schema|zod)" | head -10
```

### Flags

| Signal                          | Severity    | Action                                     |
| ------------------------------- | ----------- | ------------------------------------------ |
| Secrets in git history          | 🔴 Critical | Rotate ALL exposed credentials immediately |
| Hardcoded secrets in code       | 🔴 Critical | Move to env vars, add to .gitignore        |
| Raw SQL with interpolation      | 🔴 Critical | Parameterize all queries                   |
| dangerouslySetInnerHTML         | 🔴 High     | Audit each usage, sanitize input           |
| API routes without auth check   | 🔴 High     | Add auth middleware                        |
| CORS set to `*`                 | ⚠️ Medium   | Restrict to known origins                  |
| No input validation library     | ⚠️ Medium   | Add zod/yup validation                     |
| Password stored without hashing | 🔴 Critical | Never store plaintext passwords            |

### Output

```
## Security Assessment
- Secrets Exposure: [None/Found in code/Found in git history]
- Auth Coverage: [X]% of API routes protected
- Injection Risk: [None/Low/Medium/High]
- XSS Risk: [None/Low/Medium/High]
- Input Validation: [Comprehensive/Partial/Missing]
- Critical Issues: [count]
- High Issues: [count]
```

---

## Phase 4: Code Quality Analysis

**Time: 10-15 min | Run: Full/Cold audits**

### 4.1 Type Safety

```bash
echo "=== TypeScript Health ==="
# any usage
echo "any count:"
grep -rn ": any" --include="*.ts" --include="*.tsx" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l

# Type assertions
echo "Type assertions (as any/unknown):"
grep -rn "as any\|as unknown" --include="*.ts" --include="*.tsx" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l

# Suppression comments
echo "Type suppressions:"
grep -rn "@ts-ignore\|@ts-nocheck\|@ts-expect-error" --include="*.ts" --include="*.tsx" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l

# Strict mode check
echo "Strict mode:"
grep -E "\"strict\":\s*true" tsconfig.json 2>/dev/null && echo "Enabled" || echo "DISABLED"
```

### 4.2 Error Handling

```bash
echo "=== Error Handling ==="
# Empty catch blocks
echo "Empty catches:"
grep -rn --include="*.ts" --include="*.tsx" \
  -E "catch\s*\([^)]*\)\s*\{\s*\}" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l

# Console statements (should be proper logging)
echo "Console statements:"
grep -rn --include="*.ts" --include="*.tsx" \
  "console\.(log|error|warn|info)" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l

# Unhandled promise rejections
echo "Unhandled async (missing await/catch):"
grep -rn --include="*.ts" --include="*.tsx" \
  -E "^\s*[a-zA-Z]+\.(create|update|delete|save|remove)\(" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | \
  grep -v "await\|\.then\|\.catch" | head -10
```

### 4.3 Architecture Smells

```bash
echo "=== Architecture Health ==="
# God files (>500 lines)
echo "Large files (>500 lines):"
find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | \
  grep -v node_modules | \
  xargs wc -l 2>/dev/null | \
  awk '$1 > 500 {print}' | sort -rn | head -10

# Circular dependencies (if madge available)
npx madge --circular --extensions ts,tsx src/ 2>/dev/null || echo "Install madge for circular dep detection"

# Import depth (deeply nested = coupled)
echo "Deep imports:"
grep -rn --include="*.ts" --include="*.tsx" \
  "from ['\"].*\/.*\/.*\/.*\/.*['\"]" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | wc -l
```

### 4.4 Test Coverage

```bash
echo "=== Test Health ==="
# Test file count
echo "Test files:"
TEST_COUNT=$(find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*.test.tsx" -o -name "*.spec.tsx" 2>/dev/null | \
  grep -v node_modules | wc -l)
echo "$TEST_COUNT"

# Source files (excluding tests)
echo "Source files:"
SOURCE_COUNT=$(find . -name "*.ts" -o -name "*.tsx" 2>/dev/null | \
  grep -v node_modules | grep -v ".test\|.spec" | wc -l)
echo "$SOURCE_COUNT"

# Test to source ratio
if [ "$SOURCE_COUNT" -gt 0 ]; then
  RATIO=$(echo "scale=2; $TEST_COUNT / $SOURCE_COUNT" | bc 2>/dev/null || echo "N/A")
  echo "Test:Source ratio: $RATIO"
fi

# Check for Vitest config
echo "=== Test Infrastructure ==="
ls vitest.config.ts vitest.config.js 2>/dev/null || echo "⚠️ No vitest config found"

# Check for test setup file
ls tests/setup.ts test/setup.ts 2>/dev/null || echo "⚠️ No test setup file found"

# Check for test scripts in package.json
echo "Test scripts in package.json:"
grep -E '"test":|"test:' package.json 2>/dev/null | head -5 || echo "⚠️ No test scripts found"

# Run coverage if available
npm run test:coverage --if-present 2>/dev/null || npm run coverage --if-present 2>/dev/null
```

### Flags

| Signal                  | Severity    | Meaning                             |
| ----------------------- | ----------- | ----------------------------------- |
| `any` count > 50        | ⚠️ Medium   | Types are lying, bugs hiding        |
| `any` count > 200       | 🔴 High     | Type system effectively disabled    |
| strict mode off         | ⚠️ Medium   | Missing type safety guarantees      |
| Empty catches > 10      | ⚠️ Medium   | Silent failures, hard to debug      |
| Files > 500 lines > 5   | ⚠️ Medium   | God objects, needs refactoring      |
| Circular dependencies   | 🔴 High     | Architecture rot                    |
| Test:source ratio < 0.3 | ⚠️ Medium   | Under-tested                        |
| Test:source ratio < 0.1 | 🔴 High     | Severely under-tested               |
| Zero tests              | 🔴 Critical | No safety net — **blocks shipping** |
| No vitest config        | 🔴 High     | Test infrastructure missing         |
| No test scripts         | 🔴 High     | Tests cannot be run                 |

### Output

```
## Code Quality
- Type Safety: [Strong/Moderate/Weak]
  - any usage: [N]
  - Strict mode: [Yes/No]
- Error Handling: [Good/Inconsistent/Poor]
- Architecture: [Clean/Some coupling/Tangled]
- Test Coverage: [X]% ([N] test files)
- Tech Debt Score: [1-10]
```

---

## Phase 5: Database Review

**Time: 5-10 min | Run: Full/Cold audits**

### Commands

```bash
echo "=== Schema Analysis ==="
# Get schema (Prisma)
cat prisma/schema.prisma 2>/dev/null | head -100

# Check for indexing
echo "Indexes defined:"
grep -c "@@index\|@unique\|@@unique" prisma/schema.prisma 2>/dev/null || echo "0"

# Check for relations
echo "Relations:"
grep -c "@relation" prisma/schema.prisma 2>/dev/null || echo "0"

# Soft delete pattern
echo "Soft delete fields:"
grep -c "deletedAt\|isDeleted\|deleted" prisma/schema.prisma 2>/dev/null || echo "0"

echo "=== Query Patterns ==="
# N+1 potential (findMany followed by access to relations)
grep -rn --include="*.ts" \
  -A5 "findMany\|findFirst" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | \
  grep -E "include:|\.map\(" | head -10

# Missing where clauses on updates/deletes (dangerous!)
grep -rn --include="*.ts" \
  -E "\.(update|delete)\(\s*\{[^}]*\}" \
  --exclude-dir={node_modules,.next,dist} . 2>/dev/null | \
  grep -v "where" | head -5
```

### Flags

| Signal                      | Severity    | Meaning                     |
| --------------------------- | ----------- | --------------------------- |
| No indexes on foreign keys  | ⚠️ Medium   | Performance issues at scale |
| Update/delete without where | 🔴 Critical | Data loss risk              |
| No timestamps on tables     | ⚡ Low      | Audit trail missing         |
| Inconsistent soft delete    | ⚠️ Medium   | Data integrity issues       |

---

## Phase 6: Infrastructure & DevOps

**Time: 5 min | Run: Full/Cold audits**

### Commands

```bash
echo "=== CI/CD Check ==="
ls -la .github/workflows/ 2>/dev/null
cat .github/workflows/*.yml 2>/dev/null | grep -E "test|lint|security|audit" | head -10

echo "=== Environment Config ==="
# .env example exists?
ls -la .env.example .env.sample .env.template 2>/dev/null

# What envs are expected?
grep -h "process.env\." --include="*.ts" --include="*.tsx" -r . 2>/dev/null | \
  grep -oE "process\.env\.[A-Z_]+" | sort -u

echo "=== Docker ==="
ls -la Dockerfile docker-compose*.yml 2>/dev/null
cat Dockerfile 2>/dev/null | head -20
```

### Flags

| Signal                    | Severity  | Meaning                |
| ------------------------- | --------- | ---------------------- |
| No CI/CD                  | ⚠️ Medium | Manual deployment risk |
| CI has no tests           | ⚠️ Medium | False confidence       |
| No .env.example           | ⚡ Low    | Onboarding friction    |
| Secrets in docker-compose | 🔴 High   | Exposed credentials    |

---

## Phase 7: Report Generation

### Quick Scan Output

```markdown
# Quick Audit: [Project Name]

Date: [timestamp]
Mode: Quick Scan

## Status: [PASS / FAIL]

### Blockers (must fix)

- [list or "None"]

### Warnings (should fix)

- [list or "None"]

### Next Steps

- [specific actions]
```

### Full Audit Output

```markdown
# Full Audit Report: [Project Name]

Date: [timestamp]
Mode: Full Audit
Duration: [X] minutes

## Executive Summary

- Overall Health: [1-10 score]
- Security Posture: [Strong/Adequate/Weak/Critical]
- Code Quality: [High/Medium/Low]
- Tech Debt Level: [Low/Medium/High/Critical]
- Recommendation: [Ship/Fix then ship/Major rework needed]

## Critical Issues (Fix Immediately)

| Issue   | Location    | Severity    | Remediation |
| ------- | ----------- | ----------- | ----------- |
| [issue] | [file:line] | 🔴 Critical | [action]    |

## High Priority Issues (Fix Before Shipping)

| Issue | Location | Severity | Remediation |
| ----- | -------- | -------- | ----------- |

## Medium Priority (Plan to Fix)

| Issue | Location | Severity | Remediation |
| ----- | -------- | -------- | ----------- |

## Low Priority (Tech Debt Backlog)

| Issue | Location | Severity | Remediation |
| ----- | -------- | -------- | ----------- |

## Metrics Summary

| Metric                     | Value | Benchmark | Status  |
| -------------------------- | ----- | --------- | ------- |
| Vulnerabilities (critical) | [N]   | 0         | [✅/❌] |
| Vulnerabilities (high)     | [N]   | <3        | [✅/❌] |
| any usage                  | [N]   | <50       | [✅/❌] |
| Test coverage              | [N]%  | >60%      | [✅/❌] |
| Empty catches              | [N]   | <5        | [✅/❌] |
| Files >500 LOC             | [N]   | <5        | [✅/❌] |

## Positive Findings

- [things done well]

## Detailed Findings

[Phase-by-phase details]
```

---

## Integration with Build Harness

### As Phase Gate

```yaml
# In build spec
phases:
  - name: development
    steps: [...]
    on_complete:
      run_skill: code-audit
      mode: quick
      fail_on: critical

  - name: pre-ship
    steps: [...]
    on_complete:
      run_skill: code-audit
      mode: full
      fail_on: high
```

### As Manual Trigger

```bash
# Quick scan
harness run-skill code-audit --mode=quick

# Full audit
harness run-skill code-audit --mode=full

# Cold assessment (new codebase)
harness run-skill code-audit --mode=cold --output=report.md
```

### Decision Gates

```
Quick Scan:
- PASS: No critical issues
- FAIL: Any critical issue → block phase completion

Full Audit:
- SHIP: Score >= 7, no critical/high issues
- FIX THEN SHIP: Score >= 5, no critical issues
- MAJOR REWORK: Score < 5 or any critical issue
```

---

## Customization

### Skip Patterns

Add to `.audit-ignore` in project root:

```
# Skip specific directories
vendor/
generated/
legacy/

# Skip specific files
src/old-migration.ts

# Skip specific checks
!check:circular-deps
!check:test-coverage
```

### Severity Overrides

Add to `.audit-config.json`:

```json
{
  "severityOverrides": {
    "any-usage": "low",
    "console-statements": "ignore"
  },
  "thresholds": {
    "anyCount": 100,
    "testCoverage": 40,
    "maxFileLines": 800
  }
}
```

---

## Maintenance

Update this skill when:

- New vulnerability patterns emerge
- Framework-specific checks needed (add to relevant phase)
- New tools become available (add as alternatives)
- False positive patterns identified (add to skip defaults)
