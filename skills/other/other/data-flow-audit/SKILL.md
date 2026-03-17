---
name: data-flow-audit
description: Detect split data source anti-patterns and scattered business rule duplication where the same logic is reimplemented across multiple files and languages. Catches semantic duplication that syntactic tools like jscpd miss. Use at phase checkpoints or when investigating data consistency issues.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Data Flow Audit Skill

Detect cases where the same business concept is served through multiple API endpoints with independently maintained logic — the "split data source" anti-pattern — and where the same business rule (filter predicates, conditions, thresholds) is scattered across multiple files and languages.

## Why This Matters

When the same data reaches the UI through two different code paths, subtle inconsistencies emerge:
- Different filtering, defaults, or error handling per endpoint
- Duplicated helper functions that drift independently
- Hardcoded constants (rates, thresholds) updated in one place but not the other
- Frontend components showing conflicting values for the same metric

When the same business rule is reimplemented across SQL, API routes, shared libs, and Trigger.dev jobs:
- Adding a new filter condition requires updating N locations manually
- Some locations get missed, causing silent data inconsistencies
- No tool catches it because the code is *reimplemented* in each language, not *copy-pasted*

## Workflow Overview

Copy this checklist and track progress:

```
Data Flow Audit Progress:
- [ ] Step 0: Validate known rules from MEMORY.md
- [ ] Step 1: Map all API routes, jobs, and data sources
- [ ] Step 2: Detect overlapping SQL/table references
- [ ] Step 2.5: Detect scattered filter predicates (fingerprint matching)
- [ ] Step 3: Detect duplicated types and helpers across routes
- [ ] Step 4: Detect cross-layer formula and constant divergence
- [ ] Step 5: Map frontend consumers to endpoints
- [ ] Step 6: Detect test mock divergence
- [ ] Step 7: Score and report findings
```

## Step 0: Validate Known Rules from MEMORY.md

Before running the full audit, check for documented business rules that already have tracked locations.

### 0.1 Parse MEMORY.md for documented rules

Search the project's MEMORY.md for patterns that indicate tracked business rules:
- Phrases like "N live locations", "canonical", "single source of truth", "conditions"
- Lists of files/modules that implement the same rule

For each documented rule, extract: rule name, conditions/fingerprint, canonical location, documented locations, documented exceptions.

### 0.2 Validate each documented location

For each documented rule:
1. Read each documented file and verify the rule's conditions are still present
2. Compare conditions against the canonical definition — flag any differences
3. Check that the canonical location itself still exists and is current

### 0.3 Discover undocumented locations

Use fingerprint-grep (see Step 2.5 methodology in [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md)) to search for the rule's column names across the full scan scope. Compare discovered set against documented set to find new, removed, or drifted locations.

### 0.4 Report known rule status

```
KNOWN RULE VALIDATION
---------------------
Rule: {rule name} ({N} conditions)
Canonical: {canonical location}
Documented locations: {N}  |  Actual: {N}  |  Status: {ALIGNED | DRIFTED | LOCATIONS_CHANGED}
  ✓ {file1} — conditions match ({implementation style})
  ✗ {file3} — MISSING condition: {condition name}
  + {new_file} — UNDOCUMENTED location ({N}/{total} conditions found)
  - {removed_file} — REMOVED (no longer contains rule conditions)
  ⊘ {exception_file} — documented skip ({reason})
```

**Severity:** CRITICAL if canonical drifted, HIGH if documented locations missing conditions, MEDIUM if location count changed but conditions consistent.

## Step 1: Map API Routes, Jobs, and Data Sources

Build an inventory of every API route, Trigger.dev job, and shared module that touches data.

### 1.1 Discover API routes and jobs

```bash
# Next.js API routes (pages router)
find src/pages/api -name "*.ts" -not -name "*.test.*"

# Next.js API routes (app router)
find src/app/api -name "route.ts"

# Trigger.dev jobs
find trigger/jobs -name "*.ts" -not -name "*.test.*" 2>/dev/null

# Shared lib modules with data fetching
grep -rl "\.from(\|\.rpc(" src/lib/ --include="*.ts" | grep -v test
```

### 1.2 For each route/job, extract data sources

Record: SQL tables queried (`.from()`), RPC functions called (`.rpc()`), shared service imports, response shape.

### 1.3 Identify route groups

Group routes serving the same business domain. Heuristics: same URL prefix, same tables/RPCs, >50% response field overlap.

### 1.4 Identify implicit BFF pairs

Check if list/detail endpoints, dashboard/overview endpoints, or Trigger.dev jobs compute overlapping data independently. BFF pairs are prime candidates for split data sources.

## Step 2: Detect Overlapping SQL/Table References

### 2.1 Shared table access

```bash
grep -rn "\.from(" src/pages/api/ src/lib/ trigger/jobs/ --include="*.ts" | grep -v test
```

Flag when two different route files query the same table with different filters, columns, or joins.

### 2.2 Shared RPC calls

```bash
grep -rn "\.rpc(" src/pages/api/ src/lib/ trigger/jobs/ --include="*.ts" | grep -v test
```

Flag when two routes call the same RPC, or two RPCs compute overlapping metrics.

### 2.3 SQL function overlap

Read SQL definitions in `supabase/migrations/` for any RPCs found. Flag when two SQL functions compute the same metric independently (HIGH) vs. one delegating to another (MEDIUM).

### 2.4 Detect aggregation cascades

An aggregation cascade occurs when an overview endpoint computes `SUM(metric)` using its own formula while per-item endpoints compute that metric individually with a different formula. If the per-item formula changes, the aggregate won't match the sum of its parts.

**Severity: CRITICAL** if aggregate and per-item formulas produce inconsistent results.
**Severity: HIGH** if formulas are consistent but independently maintained.

## Step 2.5: Detect Scattered Filter Predicates

See [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md) for the full fingerprint matching methodology.

Read DETECTION_PATTERNS.md for the full detection procedure. The summary below is for quick reference only — always defer to the full document.

**Summary**: Extract filter predicates from all files in scope, build column-name fingerprints per file, cluster files sharing 3+ field names, validate candidates (eliminate type defs, SELECT lists, comments), and assess severity based on location count and language spread.

## Step 3: Detect Duplicated Types and Helpers

See [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md) for detailed detection commands.

**Summary**: Find type definitions with >60% field overlap across route files (HIGH). Find utility functions duplicated across routes (HIGH).
Check for routes that bypass shared `src/lib/` modules by querying tables directly (HIGH — "library drift").
Check for SQL functions that inline conditions already encapsulated by shared SQL helpers.

## Step 4: Detect Cross-Layer Formula and Constant Divergence

See [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md) for detailed detection commands.

**Summary**: Find repeated magic numbers/strings across SQL and TS layers. Verify SQL ↔ JS formula consistency (CRITICAL if different values, HIGH if independently maintained). Detect cross-layer formula duplication: SQL + API route, SQL + frontend, API route + frontend, SQL + Trigger.dev job.

## Step 5: Map Frontend Consumers

See [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md) for detailed commands.

**Summary**: Find all `fetch()` and `useSWR`/`useQuery` calls in components. Build consumer map (route → components). Flag same-page different-endpoints (CRITICAL), list-vs-detail divergence (HIGH), and missing callback patterns.

## Step 6: Detect Test Mock Divergence

See [DETECTION_PATTERNS.md](DETECTION_PATTERNS.md) for detailed methodology.

**Summary**: Collect test files for each route group. Compare mock data shapes for type divergence (field names), value representation (number vs string, snake_case vs camelCase), and endpoint divergence. **Severity: MEDIUM** — test mock divergence is a symptom, useful as an early-warning signal.

## Step 7: Score and Report

### Severity Reference

| Severity | Meaning |
|----------|---------|
| CRITICAL | Same metric, different values possible in UI; formula mismatch; 6+ scattered locations across 2+ languages |
| HIGH | Independent implementations that will drift; library bypass; 3-5 scattered locations |
| MEDIUM | Structural risk, currently consistent; test mock divergence; 2-3 same-language locations |
| LOW | Minor duplication, low divergence risk; intentional bypass with justification |

### Report Format

```
DATA FLOW AUDIT REPORT
======================
Scanned: {timestamp}
API routes analyzed: {N}  |  Jobs: {N}  |  SQL functions: {N}  |  Shared libs: {N}

KNOWN RULE VALIDATION — {per-rule status from Step 0}
SCATTERED FILTER PREDICATES — {fingerprint clusters from Step 2.5}

SPLIT DATA SOURCE FINDINGS
---------------------------
Finding 1: {Business concept} ({severity})
  Endpoints: {route1}, {route2}
  Signals: BFF pair | Aggregation cascade | Cross-layer formula | Library bypass | Mock divergence
  Risk: {what could diverge}
  Recommendation: {extract service module | designate authority | use callback pattern}

ROUTE MAP — {full table from Step 1}
CONSUMER MAP — {full table from Step 5}

SUMMARY
  Known rules: {N} aligned, {N} drifted
  Scattered predicates: {N} clusters
  Split sources: {N} critical, {N} high, {N} medium, {N} low
  Status: PASSED | PASSED WITH NOTES | FAILED
```

### Exit Criteria

| Result | Condition |
|--------|-----------|
| PASSED | No split data source patterns found and all known rules aligned |
| PASSED WITH NOTES | Only MEDIUM/LOW findings and known rules have minor location changes |
| FAILED | Any CRITICAL or HIGH finding, or known rule conditions have drifted |

## Consolidation Blueprint

When a split data source or scattered business rule is found:

1. **Extract shared service module** — Create `src/lib/{domain}Service.ts` with shared types, helpers, and computation
2. **Designate an authority endpoint** — One endpoint becomes source of truth; others delegate
3. **Use callback/prop pattern for frontend** — Parent fetches once, passes to children
4. **Centralize constants** — Move hardcoded values to named constants in shared module
5. **Create or adopt canonical helpers** — For scattered rules, create a SQL/TS helper and migrate all locations

## Error Handling

**If the project has no API routes:**
- Report: "No API route handlers found" — Mark audit as NOT APPLICABLE

**If a route file is too complex to parse (>500 lines):**
- Flag the file as tech debt, parse what you can, note: "Partial analysis"

**If no frontend consumers found for a route:**
- Note as informational, check `trigger/` or `jobs/` for server-side consumers

**If the audit finds >5 split data source patterns:**
- Present the top 3 by severity, summarize remaining, suggest `/add-todo` for tracking

**If MEMORY.md has no documented rules (Step 0):**
- Skip known rule validation, rely on Step 2.5 fingerprint matching

## Review Your Output

After generating the audit report, verify:
- All scanned files are represented in the findings
- Each finding includes actionable remediation steps
- No false positives from template or test files

## Limitations

- Cannot detect split data sources across microservices or external APIs
- SQL formula comparison is heuristic — complex SQL may need manual review
- Frontend consumer mapping relies on static analysis of `fetch()` calls
- Fingerprint matching may produce false positives — Step 2.5.4 validation mitigates this
- Known rule validation depends on MEMORY.md being kept current
