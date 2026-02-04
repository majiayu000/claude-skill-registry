---
name: audit-engineering-productivity
description: Run a single-session engineering productivity audit on the codebase
supports_parallel: true
fallback_available: true
estimated_time_parallel: 15 min
estimated_time_sequential: 45 min
---

# Single-Session Engineering Productivity Audit

## Purpose

Evaluates developer experience (DX), debugging capabilities, and offline support
infrastructure. Identifies friction points in development workflows and provides
actionable recommendations for improvement.

## Execution Mode Selection

| Condition                                 | Mode       | Time    |
| ----------------------------------------- | ---------- | ------- |
| Task tool available + no context pressure | Parallel   | ~15 min |
| Task tool unavailable                     | Sequential | ~45 min |
| Context running low (<20% remaining)      | Sequential | ~45 min |
| User requests sequential                  | Sequential | ~45 min |

---

## Section A: Parallel Architecture (3 Agents)

**When to use:** Task tool available, sufficient context budget

### Agent 1: dx-golden-path-auditor

**Focus Areas:**

- Developer onboarding friction
- npm scripts completeness
- Setup automation (doctor scripts, env validation)
- Development workflow ergonomics

**Files:**

- `package.json` (scripts section)
- `scripts/` directory
- `.env.example`, `.env.local`
- `README.md`, `DEVELOPMENT.md`

**Checks:**

```bash
# Count npm scripts
grep -c '"[^"]*":' package.json

# Check for setup/doctor scripts
ls scripts/*.js 2>/dev/null | grep -E 'setup|doctor|verify'

# Check for dev:offline script
grep -c "dev:offline" package.json
```

### Agent 2: debugging-ergonomics-auditor

**Focus Areas:**

- Structured logging vs console.log ratio
- Correlation ID support for request tracing
- Error message quality and user guidance
- Sentry integration completeness

**Files:**

- `lib/logger.ts`
- `*.ts` `*.tsx` files (console.log patterns)
- `functions/src/**/*.ts` (Cloud Functions logging)
- `app/**/error.tsx` (error boundaries)

**Checks:**

```bash
# Console.log to logger ratio
echo "Console.log calls:"
grep -r "console.log" --include="*.ts" --include="*.tsx" app/ lib/ components/ | wc -l
echo "Logger calls:"
grep -r "logger\." --include="*.ts" --include="*.tsx" app/ lib/ components/ | wc -l

# Correlation ID patterns
grep -r "correlationId\|correlation-id\|x-request-id" --include="*.ts" .
```

### Agent 3: offline-support-auditor

**Focus Areas:**

- Firebase IndexedDB persistence configuration
- Service worker presence and functionality
- Offline write queue implementation
- Network status indicators and user feedback

**Files:**

- `lib/firebase.ts`
- `public/sw.js` (if exists)
- `components/status/offline-indicator.tsx`
- `lib/offline-queue.ts` (if exists)

**Checks:**

```bash
# Firebase persistence
grep -r "enableIndexedDbPersistence\|enablePersistence" lib/ app/

# Service worker
ls -la public/sw.js 2>/dev/null || echo "No service worker"

# LocalStorage vs IndexedDB usage
grep -r "localStorage" --include="*.ts" --include="*.tsx" | wc -l
grep -r "indexedDB\|IDB\|Dexie" --include="*.ts" --include="*.tsx" | wc -l
```

### Parallel Execution Command

```markdown
Invoke all 3 agents in a SINGLE Task message:

Task 1: dx-golden-path-auditor agent - audit setup, scripts, onboarding Task 2:
debugging-ergonomics-auditor agent - audit logging, error handling Task 3:
offline-support-auditor agent - audit persistence, service workers
```

---

## Section B: Sequential Fallback

**When to use:** Task tool unavailable, context pressure, or user request

### Step 1: Golden Path & DX (10 min)

1. Review `package.json` scripts section
2. Check for setup/doctor automation scripts
3. Verify `.env.example` completeness
4. Assess README setup instructions
5. Identify missing "golden path" scripts

### Step 2: Debugging Ergonomics (10 min)

1. Calculate console.log vs logger ratio
2. Search for correlation ID patterns
3. Review error boundary implementations
4. Check Sentry integration in logger
5. Assess error message quality

### Step 3: Offline Support (10 min)

1. Check Firebase persistence configuration
2. Look for service worker implementation
3. Review offline indicator component
4. Search for write queue patterns
5. Assess localStorage vs IndexedDB usage

---

## Output Requirements

### Report File

Create `docs/audits/comprehensive/audit-engineering-productivity-report.md`:

```markdown
# Engineering Productivity Audit - {DATE}

## Baselines

| Metric                   | Value |
| ------------------------ | ----- |
| npm scripts count        | X     |
| Console.log calls        | X     |
| Logger calls             | X     |
| Structured logging ratio | X:Y   |
| LocalStorage usages      | X     |
| IndexedDB usage          | X     |
| Service worker           | Y/N   |
| Firebase persistence     | Y/N   |

## Findings Summary

| Severity | Count | Category       |
| -------- | ----- | -------------- |
| S0       | X     | -              |
| S1       | X     | Category names |
| S2       | X     | Category names |
| S3       | X     | Category names |

## Detailed Findings

### 1. Golden Path & DX

[Findings here]

### 2. Debugging Ergonomics

[Findings here]

### 3. Offline Support

[Findings here]

## Quick Wins (E0-E1)

[Prioritized list of low-effort fixes]

## Recommendations

### Immediate (E0-E1)

[List]

### Short-term (E2)

[List]

### Long-term (E3)

[List]
```

### JSONL File

Create
`docs/audits/comprehensive/audit-engineering-productivity-findings.jsonl`:

**CRITICAL - Use this exact schema:**

```json
{
  "category": "engineering-productivity",
  "title": "Short specific title",
  "fingerprint": "engineering-productivity::primary_file::identifier",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": 75,
  "files": ["array/of/file/paths.ts"],
  "why_it_matters": "1-3 sentences explaining impact",
  "suggested_fix": "Concrete remediation direction",
  "acceptance_tests": ["Array of verification steps"]
}
```

---

## Category Definitions

| Category   | Description                                |
| ---------- | ------------------------------------------ |
| GoldenPath | Setup, scripts, onboarding, dev workflow   |
| Debugging  | Logging, tracing, error handling, messages |
| Offline    | Persistence, service workers, queues, sync |

---

## Severity Scale

| Level | Name     | Definition                               |
| ----- | -------- | ---------------------------------------- |
| S0    | Critical | Data loss risk, production breaking      |
| S1    | High     | Significant dev friction, missing core   |
| S2    | Medium   | Maintainability drag, inconsistency      |
| S3    | Low      | Polish, minor improvements, nice-to-have |

---

## Effort Scale

| Level | Name    | Definition                  |
| ----- | ------- | --------------------------- |
| E0    | Minutes | Quick fix, trivial change   |
| E1    | Hours   | Single-session work         |
| E2    | Days    | 1-3 days or staged PR       |
| E3    | Weeks   | Multi-PR, multi-week effort |

---

## Prior Audit Reference

Check `docs/audits/single-session/engineering-productivity/` for prior findings
and track carryover issues.

---

## TDMS Integration

After audit completion, findings should be ingested into MASTER_DEBT.jsonl:

```bash
node scripts/debt/intake-audit.js \
  docs/audits/comprehensive/audit-engineering-productivity-findings.jsonl \
  --source "audit-engineering-productivity-$(date +%Y-%m-%d)"
```

---

## Related Skills

- `/audit-comprehensive` - Run all 7 domain audits
- `/audit-process` - CI/CD and automation audit (overlaps with DX)
- `/audit-code` - Code quality audit

---

## Version History

| Version | Date       | Description            |
| ------- | ---------- | ---------------------- |
| 1.0     | 2026-02-03 | Initial skill creation |
