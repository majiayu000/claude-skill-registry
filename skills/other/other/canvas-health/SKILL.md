---
name: canvas-health
description: "Lint canvas files for staleness, missing fields, inconsistent evidence types, and orphaned references. Run periodically or before major transitions."
---

# Canvas Health Check

Audit the canvas knowledge base for quality, consistency, and completeness. The canvas is Mycelium's source of truth -- its quality directly determines agent output quality (Raschka: "context quality = model quality").

## When to Use

- Before any diamond phase transition (called automatically by `/diamond-assess`)
- After a period of inactivity (>7 days since last canvas update)
- When agent output quality seems to degrade
- After onboarding a new team member (ensures canvas is self-explanatory)
- Proactively: run periodically to catch silent drift

## Workflow

1. **Load project configuration**:
   - Read `diamonds/active.yml` for `product_type` and `project_type`
   - Read `.claude/engine/canvas-guidance.yml` for required/recommended/optional files per project type

2. **Check file presence**:
   - For each **required** canvas file: does it exist? Is it non-empty (>50 bytes)?
   - For each **recommended** canvas file: does it exist? Flag as gap if missing.
   - Report: `N/M required files present, K recommended files missing`

3. **Check `_meta` blocks**:
   - For each existing canvas file, check for `_meta:` block
   - Flag missing `_meta` blocks
   - Flag `last_validated` older than 30 days (staleness warning)
   - Flag `version` field missing or at 0

4. **Check confidence consistency**:
   - Gather all `confidence:` values across canvas files
   - Flag confidence > 0.5 with `evidence_type: speculation` or `evidence_type: assumption`
   - Flag confidence > 0.7 with fewer than 2 evidence sources
   - Flag confidence values that haven't changed across git history (anchored confidence anti-pattern)
   - Cross-check against `diamonds/active.yml` confidence

5. **Check evidence type consistency**:
   - Every canvas file with `evidence_type:` should have it set to one of: `interview`, `survey`, `analytics`, `experiment`, `speculation`, `assumption`, `mocked_persona`
   - Flag unknown evidence types
   - Flag `evidence_type: interview` when only mocked personas were used (honesty check)

6. **Check for orphaned references**:
   - Canvas files that reference other canvas files (e.g., jobs-to-be-done.yml referencing opportunities.yml) -- verify the referenced file exists
   - Diamond references to canvas files -- verify they exist

7. **Check evidence freshness** (evidence decay):
   - Scan all `provenance` blocks across canvas files for `validated_at` or `captured_at` timestamps
   - Compare against staleness thresholds from `engine/evidence-decay.md`:
     - User needs/interviews: 90 days
     - Competitive intelligence: 90 days
     - Strategic assumptions: 180 days
     - Technical feasibility: 120 days
     - DORA/delivery metrics: 30 days
   - Flag evidence past threshold as warning; past 3x threshold as critical
   - Suggest refresh actions: "Evidence in [file] is [N] days old. Run `/user-interview` or `/log-evidence` to refresh."
   - Note: corrections and patterns do NOT decay — process learnings are timeless

7b. **Check metric snapshot freshness** (v0.14):
   - If `.claude/jit-tooling/active-metrics.yml` exists, for each `status: active` source:
     - Find the newest snapshot in `.claude/evals/metrics/<source>/`.
     - If >7 days old: warning ("[source] snapshot is [N] days old — run `/metrics-pull` to refresh").
     - If >30 days old: critical (evidence this stale is worse than no metric reference — anchors old state).
     - If missing entirely: info-level ("No snapshots yet for [source]. Run `/metrics-pull`.").
   - Also check per-adapter freshness: for each adapter file in `.claude/jit-tooling/metrics-adapters/`, if `last_known_working` is >180 days old, flag as warning suggesting regeneration via `metrics-adapters/GENERATING.md`.
   - Source: v0.14 metrics harvesting. Metric evidence has a faster staleness curve than interview evidence because the underlying data changes continuously.

8. **Check cross-reference integrity** (leaf lifecycle):
   - Every GIST idea with `source_leaf_id` → verify that leaf exists in `opportunities.yml` (and not in `archived-solutions.yml` without the GIST being shelved)
   - Every service entry with `gist_id` → verify that GIST idea exists
   - Every threat model entry with `solution_id` → verify that solution exists
   - Every go-to-market `feedback_loop` entry with `source_leaf_id` → verify leaf exists
   - Flag broken references as warnings ("Zombie Solution" anti-pattern)

8b. **Check scenario health** (Hoskins):
   - If `canvas/scenarios.yml` exists:
     - Every scenario must have all four Hoskins elements populated (persona, means, motive, simulation) — flag incomplete scenarios
     - Every scenario must have `lifecycle.born_at` set — flag if missing (orphan scenario with no origin)
     - Every scenario with `confidence > 0.5` must have evidence sources — flag unsupported confidence
     - Every scenario referenced in `lifecycle.designed_against[]` → verify the solution exists in `opportunities.yml` or `gist.yml`
     - Every scenario referenced in `lifecycle.tested_against[]` → verify test date is not in the future
     - Flag scenarios with `status: draft` older than 30 days (stale draft — either promote or discard)
   - If `canvas/scenarios.yml` does NOT exist but project_type requires it (per canvas-guidance.yml): flag as warning

9. **Check for boilerplate content**:
   - Flag canvas files where >50% of content matches the template defaults from canvas-guidance.yml
   - Flag files with placeholder text ("TBD", "TODO", "fill in later", "placeholder")

10. **Log findings to decision-log.md** (MANDATORY):
   - APPEND a `### Canvas Health Report` entry to `harness/decision-log.md`
   - Include: overall status (HEALTHY/WARNINGS/CRITICAL), stale evidence found, refresh recommendations
   - Use these words explicitly when applicable: "stale", "evidence", "refresh", "interview", "validate"
   - Example: "Evidence in opportunities.yml is stale (183 days old, threshold 90). Refresh needed: run fresh interviews to validate opportunity assumptions."
   - This log entry is essential for auditability and for downstream skills (e.g., `/diamond-progress`) to detect health issues

11. **Generate health report**:
   - Summarize findings by severity: critical (required file missing), warning (stale, inconsistent), info (recommended file missing, meta block absent)

## Output Format

```
## Canvas Health Report

Overall: [HEALTHY | WARNINGS | CRITICAL]
Files checked: N canvas files, M diamonds files

### Critical Issues
- [required file missing or empty]

### Warnings
- [stale confidence, inconsistent evidence, anchored values]

### Suggestions
- [missing recommended files, absent _meta blocks]

### Coverage Summary
| Category | Required | Present | Gap |
|----------|----------|---------|-----|
| Discovery (L0-L2) | N | M | ... |
| Solution (L3) | N | M | ... |
| Delivery (L4) | N | M | ... |
| Market (L5) | N | M | ... |

Recommended actions:
  - /canvas-update [file] -- [reason]
  - /interview -- [if evidence gaps found]
  - /log-evidence -- [if confidence unsupported]
```

## Theory Citations
- Karpathy: Knowledge base health checks and auto-maintained indexes
- aiops3000: Anti-drift through externalized knowledge, versioned reference artifacts
- Raschka: "Context quality = model quality" -- canvas quality determines agent output quality
- Gilad: Confidence must be evidence-backed (confidence consistency checks)
- Torres: Evidence triangulation (evidence type consistency)
