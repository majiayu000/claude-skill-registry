---
name: audit-performance
description: Run a single-session performance audit on the codebase
---

# Single-Session Performance Audit

## Pre-Audit Validation

**Step 1: Check Thresholds**

Run `npm run review:check` and report results.

- If no thresholds triggered: "⚠️ No review thresholds triggered. Proceed
  anyway?"
- Continue with audit regardless (user invoked intentionally)

**Step 2: Gather Current Baselines**

Collect these metrics by running commands:

```bash
# Build output (bundle sizes)
npm run build 2>&1 | tail -30

# Count client vs server components
grep -rn "use client" app/ components/ --include="*.tsx" 2>/dev/null | wc -l
grep -rn "use server" app/ components/ --include="*.tsx" 2>/dev/null | wc -l

# Count useEffect hooks (potential performance issues)
grep -rn "useEffect" --include="*.tsx" --include="*.ts" 2>/dev/null | wc -l

# Count real-time listeners
grep -rn "onSnapshot" --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l

# Image optimization check
grep -rn "<img" --include="*.tsx" 2>/dev/null | wc -l
grep -rn "next/image" --include="*.tsx" 2>/dev/null | wc -l
```

**Step 3: Load False Positives Database**

Read `docs/audits/FALSE_POSITIVES.jsonl` and filter findings matching:

- Category: `performance`
- Expired entries (skip if `expires` date passed)

Note patterns to exclude from final findings. If file doesn't exist, proceed
with no exclusions.

**Step 4: Check Template Currency**

Read `docs/templates/MULTI_AI_PERFORMANCE_AUDIT_PLAN_TEMPLATE.md` and verify:

- [ ] Stack versions match package.json
- [ ] Bundle size baseline is recent
- [ ] Performance-critical paths are accurate

If outdated, note discrepancies but proceed with current values.

---

## Audit Execution

**Focus Areas (6 Categories):**

1. Bundle Size & Loading (large deps, code splitting, dynamic imports)
2. Rendering Performance (re-renders, memoization, virtualization)
3. Data Fetching & Caching (query optimization, caching strategy)
4. Memory Management (effect cleanup, subscription leaks)
5. Core Web Vitals (LCP, INP, CLS optimization)
6. Offline Support (NEW - 2026-01-17):
   - Offline state storage (localStorage, IndexedDB, cache API)
   - Sync strategy (optimistic updates, conflict resolution)
   - Failure mode handling (network errors, retry logic)
   - Offline-first data patterns (queue writes, batch sync)
   - Service worker caching strategy
   - Offline testability (can app function without network?)

**For each category:**

1. Search relevant files using Grep/Glob
2. Identify specific issues with file:line references
3. Classify severity: S0 (>50% impact) | S1 (20-50%) | S2 (5-20%) | S3 (<5%)
4. Estimate effort: E0 (trivial) | E1 (hours) | E2 (day) | E3 (major)
5. Note affected metric (LCP, bundle, render, memory)
6. **Assign confidence level** (see Evidence Requirements below)

**Performance Patterns to Find:**

- Inline arrow functions in JSX props
- Object literals in JSX props
- Missing React.memo on frequently re-rendered components
- useEffect without cleanup
- Large components without code splitting
- Queries without limits
- onSnapshot where one-time fetch would suffice

**Scope:**

- Include: `app/`, `components/`, `lib/`, `hooks/`
- Exclude: `node_modules/`, `.next/`, `docs/`, `tests/`

---

## Evidence Requirements (MANDATORY)

**All findings MUST include:**

1. **File:Line Reference** - Exact location (e.g., `components/List.tsx:45`)
2. **Code Snippet** - The actual problematic code (3-5 lines of context)
3. **Verification Method** - How you confirmed this is an issue (build output,
   grep, profiling)
4. **Impact Estimate** - Quantified performance impact (% improvement, KB saved,
   ms saved)

**Confidence Levels:**

- **HIGH (90%+)**: Confirmed by build output, Lighthouse, or profiling data;
  verified file exists, code snippet matches
- **MEDIUM (70-89%)**: Found via pattern search, file verified, performance
  impact estimated
- **LOW (<70%)**: Pattern match only, impact uncertain, needs profiling to
  confirm

**S0/S1 findings require:**

- HIGH or MEDIUM confidence (LOW confidence S0/S1 must be escalated)
- Dual-pass verification (re-read the code after initial finding)
- Quantified impact estimate with methodology

---

## Cross-Reference Validation

Before finalizing findings, cross-reference with:

1. **Build output** - Mark bundle findings as "TOOL_VALIDATED" if build shows
   large chunks
2. **Lighthouse data** - Mark Web Vitals findings as "TOOL_VALIDATED" if
   Lighthouse flagged
3. **React DevTools** - Mark rendering findings as "TOOL_VALIDATED" if profiler
   confirms re-renders
4. **Prior audits** - Check `docs/audits/single-session/performance/` for
   duplicate findings

Findings without tool validation should note: `"cross_ref": "MANUAL_ONLY"`

---

## Dual-Pass Verification (S0/S1 Only)

For all S0 (>50% impact) and S1 (20-50% impact) findings:

1. **First Pass**: Identify the issue, note file:line and initial evidence
2. **Second Pass**: Re-read the actual code in context
   - Verify the performance issue is real
   - Check for existing optimizations (memo, useMemo, useCallback)
   - Confirm file and line still exist
3. **Decision**: Mark as CONFIRMED or DOWNGRADE (with reason)

Document dual-pass result in finding: `"verified": "DUAL_PASS_CONFIRMED"` or
`"verified": "DOWNGRADED_TO_S2"`

---

## Output Requirements

**1. Markdown Summary (display to user):**

```markdown
## Performance Audit - [DATE]

### Baselines

- Build time: Xs
- Bundle size: X KB (gzipped)
- Client components: X
- useEffect hooks: X
- Real-time listeners: X

### Findings Summary

| Severity | Count | Affected Metric | Confidence  |
| -------- | ----- | --------------- | ----------- |
| S0       | X     | ...             | HIGH/MEDIUM |
| S1       | X     | ...             | HIGH/MEDIUM |
| S2       | X     | ...             | ...         |
| S3       | X     | ...             | ...         |

### Top 5 Optimization Opportunities

1. [file:line] - Description (S1/E1) - Est. X% improvement - DUAL_PASS_CONFIRMED
2. ...

### False Positives Filtered

- X findings excluded (matched FALSE_POSITIVES.jsonl patterns)

### Quick Wins (E0-E1)

- ...

### Recommendations

- ...
```

**2. JSONL Findings (save to file):**

Create file: `docs/audits/single-session/performance/audit-[YYYY-MM-DD].jsonl`

Each line (UPDATED SCHEMA with confidence and verification):

```json
{
  "id": "PERF-001",
  "category": "Bundle|Rendering|DataFetch|Memory|WebVitals|Offline",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": "HIGH|MEDIUM|LOW",
  "verified": "DUAL_PASS_CONFIRMED|TOOL_VALIDATED|MANUAL_ONLY",
  "file": "path/to/file.ts",
  "line": 123,
  "title": "Short description",
  "description": "Detailed issue",
  "affected_metric": "LCP|INP|CLS|bundle|render|memory",
  "estimated_improvement": "X%",
  "recommendation": "How to fix",
  "evidence": ["code snippet", "build output", "profiling data"],
  "cross_ref": "build|lighthouse|profiler|MANUAL_ONLY"
}
```

**3. Markdown Report (save to file):**

Create file: `docs/audits/single-session/performance/audit-[YYYY-MM-DD].md`

Full markdown report with all findings, baselines, and optimization plan.

---

## Post-Audit Validation

**Before finalizing the audit:**

1. **Run Validation Script:**

   ```bash
   node scripts/validate-audit.js docs/audits/single-session/performance/audit-[YYYY-MM-DD].jsonl
   ```

2. **Validation Checks:**
   - All findings have required fields
   - No matches in FALSE_POSITIVES.jsonl (or documented override)
   - No duplicate findings
   - All S0/S1 have HIGH or MEDIUM confidence
   - All S0/S1 have DUAL_PASS_CONFIRMED or TOOL_VALIDATED

3. **If validation fails:**
   - Review flagged findings
   - Fix or document exceptions
   - Re-run validation

---

## Post-Audit

1. Display summary to user
2. Confirm files saved to `docs/audits/single-session/performance/`
3. Run `node scripts/validate-audit.js` on the JSONL file
4. **Validate CANON schema** (if audit updates CANON files):
   ```bash
   npm run validate:canon
   ```
   Ensure all CANON files pass validation before committing.
5. **Update AUDIT_TRACKER.md** - Add entry to "Performance Audits" table:
   - Date: Today's date
   - Session: Current session number from SESSION_CONTEXT.md
   - Commits Covered: Number of commits since last performance audit
   - Files Covered: Number of performance-critical files analyzed
   - Findings: Total count (e.g., "2 S1, 4 S2, 3 S3")
   - Reset Threshold: YES (single-session audits reset that category's
     threshold)
6. **Update Technical Debt Backlog** - Re-aggregate all findings:
   ```bash
   npm run aggregate:audit-findings
   ```
   This updates `docs/aggregation/MASTER_ISSUE_LIST.md` and the Technical Debt
   Backlog section in `ROADMAP.md`. Review the updated counts and ensure new
   findings are properly categorized.
7. Ask: "Would you like me to fix any of these issues now? (Quick wins
   recommended first)"

---

## Threshold System

### Category-Specific Thresholds

This audit **resets the performance category threshold** in
`docs/AUDIT_TRACKER.md` (single-session audits reset their own category;
multi-AI audits reset all thresholds). Reset means the commit counter for this
category starts counting from zero after this audit.

**Performance audit triggers (check AUDIT_TRACKER.md):**

- 30+ commits since last performance audit, OR
- Bundle size change detected, OR
- New heavy dependencies added

### Multi-AI Escalation

After 3 single-session performance audits, a full multi-AI Performance Audit is
recommended. Track this in AUDIT_TRACKER.md "Single audits completed" counter.

---

## Adding New False Positives

If you encounter a pattern that should be excluded from future audits:

```bash
node scripts/add-false-positive.js \
  --pattern "regex-pattern" \
  --category "performance" \
  --reason "Explanation of why this is not a performance issue" \
  --source "AI_REVIEW_LEARNINGS_LOG.md#review-XXX"
```
