---
name: audit-performance
description: Run a single-session performance audit on the codebase
supports_parallel: true
fallback_available: true
estimated_time_parallel: 20 min
estimated_time_sequential: 50 min
---

# Single-Session Performance Audit

## Execution Mode Selection

| Condition                                 | Mode       | Time    |
| ----------------------------------------- | ---------- | ------- |
| Task tool available + no context pressure | Parallel   | ~20 min |
| Task tool unavailable                     | Sequential | ~50 min |
| Context running low (<20% remaining)      | Sequential | ~50 min |
| User requests sequential                  | Sequential | ~50 min |

---

## Section A: Parallel Architecture (2 Agents)

**When to use:** Task tool available, sufficient context budget

### Agent 1: bundle-and-rendering

**Focus Areas:**

- Bundle Size & Loading (large deps, code splitting, dynamic imports)
- Rendering Performance (re-renders, memoization, virtualization)
- Core Web Vitals (LCP, INP, CLS optimization)

**Files:**

- `app/**/*.tsx` (pages, layouts)
- `components/**/*.tsx`
- `package.json` (dependencies)
- `next.config.mjs`

### Agent 2: data-and-memory

**Focus Areas:**

- Data Fetching & Caching (query optimization, caching strategy)
- Memory Management (effect cleanup, subscription leaks)
- Offline Support (offline state, sync strategy)

**Files:**

- `lib/**/*.ts` (services, utilities)
- `hooks/**/*.ts` (custom hooks)
- Components with `useEffect`, `onSnapshot`
- Service worker, cache configurations

### Parallel Execution Command

```markdown
Invoke both agents in a SINGLE Task message:

Task 1: bundle-and-rendering agent - audit bundle size, rendering, Core Web
Vitals Task 2: data-and-memory agent - audit data fetching, memory, offline
support
```

### Coordination Rules

1. Each agent writes findings to separate JSONL section
2. Bundle findings include estimated KB savings
3. Memory findings include leak detection results
4. Both agents note cross-cutting concerns

---

## Pre-Audit: Episodic Memory Search (Session #128)

Before running performance audit, search for context from past sessions:

```javascript
// Search for past performance audit findings
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["performance audit", "bundle size", "rendering"],
    limit: 5,
  });

// Search for specific optimization work done before
mcp__plugin_episodic -
  memory_episodic -
  memory__search({
    query: ["Core Web Vitals", "LCP", "memory leak"],
    limit: 5,
  });
```

**Why this matters:**

- Compare against previous performance baselines
- Identify recurring bottlenecks (may need architectural fixes)
- Track optimization progress over time
- Prevent re-flagging already-addressed issues

---

## Section B: Sequential Fallback (Single Agent)

**When to use:** Task tool unavailable, context limits, or user preference

**Execution Order:**

1. AI Performance Patterns (high-impact AI-generated issues) - 10 min
2. Bundle & Loading - 15 min
3. Data Fetching - 10 min
4. Remaining categories - 15 min

**Total:** ~50 min (vs ~20 min parallel)

### Checkpoint Format

```json
{
  "started_at": "ISO timestamp",
  "categories_completed": ["Bundle", "Rendering"],
  "current_category": "DataFetch",
  "findings_count": 12,
  "last_file_written": "stage-2-findings.jsonl"
}
```

---

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

Read `docs/multi-ai-audit/templates/PERFORMANCE_AUDIT_PLAN.md` and verify:

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

7. AI Performance Patterns (AI-Codebase Specific - NEW 2026-02-02):
   - Naive Data Fetching: AI defaults to fetch-all then filter client-side (S1)
   - Missing Pagination: AI often forgets pagination for lists (S2)
   - Redundant Re-Renders: AI-generated components without memo/useMemo (S2)
   - Duplicate API Calls: Same data fetched in multiple places (S2)
   - Sync Where Async Needed: AI sometimes uses sync file ops in Node.js (S2)
   - Over-Fetching: Fetching entire documents when only fields needed (S2)
   - Missing Loading States: No suspense boundaries or loading indicators (S2)
   - Unbounded Queries: Firestore queries without limit() (S1)

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

**CRITICAL - Use JSONL_SCHEMA_STANDARD.md format:**

```json
{
  "category": "performance",
  "title": "Short specific title",
  "fingerprint": "performance::path/to/file.ts::identifier",
  "severity": "S0|S1|S2|S3",
  "effort": "E0|E1|E2|E3",
  "confidence": 90,
  "files": ["path/to/file.ts:123"],
  "why_it_matters": "1-3 sentences explaining performance impact",
  "suggested_fix": "Concrete optimization direction",
  "acceptance_tests": ["Array of verification steps"],
  "evidence": ["code snippet", "build output", "profiling data"],
  "performance_details": {
    "affected_metric": "LCP|INP|CLS|bundle|render|memory",
    "current_metric": "current value",
    "expected_improvement": "estimated improvement"
  }
}
```

**For S0/S1 findings, ALSO include verification_steps:**

```json
{
  "verification_steps": {
    "first_pass": {
      "method": "grep|tool_output|file_read|code_search",
      "evidence_collected": ["initial evidence"]
    },
    "second_pass": {
      "method": "contextual_review|exploitation_test|manual_verification",
      "confirmed": true,
      "notes": "Confirmation notes"
    },
    "tool_confirmation": {
      "tool": "lighthouse|typescript|webpack|NONE",
      "reference": "Tool output or NONE justification"
    }
  }
}
```

**⚠️ REQUIRED FIELDS (per JSONL_SCHEMA_STANDARD.md):**

- `category` - MUST be `performance` (normalized)
- `fingerprint` - Format: `<category>::<primary_file>::<identifier>`
- `files` - Array with file paths (include line as `file.ts:123`)
- `confidence` - Number 0-100 (not string)
- `acceptance_tests` - Non-empty array of verification steps

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
   - Run:
     `node scripts/reset-audit-triggers.js --type=single --category=performance --apply`
6. **TDMS Integration (MANDATORY)** - Ingest findings to canonical debt store:
   ```bash
   node scripts/debt/intake-audit.js docs/audits/single-session/performance/audit-[YYYY-MM-DD].jsonl --source "audit-performance-[DATE]"
   ```
   This assigns DEBT-XXXX IDs and adds to
   `docs/technical-debt/MASTER_DEBT.jsonl`. See
   `docs/technical-debt/PROCEDURE.md` for the full TDMS workflow.
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

Multi-AI audits are triggered by total commits or time elapsed (not single audit
counts). Check `npm run review:check` for current multi-AI trigger status.

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

---

## Documentation References

Before running this audit, review:

### TDMS Integration (Required)

- [PROCEDURE.md](docs/technical-debt/PROCEDURE.md) - Full TDMS workflow
- [MASTER_DEBT.jsonl](docs/technical-debt/MASTER_DEBT.jsonl) - Canonical debt
  store
- Intake command:
  `node scripts/debt/intake-audit.js <output.jsonl> --source "audit-performance-<date>"`

### Documentation Standards (Required)

- [JSONL_SCHEMA_STANDARD.md](docs/templates/JSONL_SCHEMA_STANDARD.md) - Output
  format requirements and TDMS field mapping
- [DOCUMENTATION_STANDARDS.md](docs/DOCUMENTATION_STANDARDS.md) - 5-tier doc
  hierarchy
