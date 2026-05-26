---
name: canvas-health
description: "Lint canvas files for staleness, missing fields, inconsistent evidence types, and orphaned references. Run periodically or before major transitions."
metadata:
  instruction_budget: "87"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Canvas Health Check

Audit the canvas knowledge base for quality, consistency, and completeness. The canvas is Mycelium's source of truth -- its quality directly determines agent output quality (Raschka: "context quality = model quality").

## When to Use

- Before any diamond phase transition (called automatically by `/mycelium:diamond-assess`)
- After a period of inactivity (>7 days since last canvas update)
- When agent output quality seems to degrade
- After onboarding a new team member (ensures canvas is self-explanatory)
- Proactively: run periodically to catch silent drift

## Workflow

1. **Load project configuration**:
   - Read `.claude/diamonds/active.yml` for `product_type` and `project_type`
   - Read `${CLAUDE_PLUGIN_ROOT}/engine/canvas-guidance.yml` for required/recommended/optional files per project type

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
   - Cross-check against `.claude/diamonds/active.yml` confidence

5. **Check evidence type consistency**:
   - Every canvas file with `evidence_type:` should have it set to one of: `interview`, `survey`, `analytics`, `experiment`, `speculation`, `assumption`, `mocked_persona`
   - Flag unknown evidence types
   - Flag `evidence_type: interview` when only mocked personas were used (honesty check)
   - Every `source_class:` value should be one of: `external_human`, `external_data`, `internal_stakeholder`, `internal_desk`, `internal_simulated` — flag unknown values
   - Flag `internal_stakeholder` evidence with confidence > 0.5 that has `validated: false` or no `validated` field — stakeholder beliefs should not carry high confidence without external validation (Brown: organizational mythology)
   - Flag L2 opportunity canvas entries where ALL evidence is `internal_stakeholder` or `internal_desk` — no external human voice heard (Spool: secondhand research insufficient)

6. **Check for orphaned references**:
   - Canvas files that reference other canvas files (e.g., jobs-to-be-done.yml referencing opportunities.yml) -- verify the referenced file exists
   - Diamond references to canvas files -- verify they exist

7. **Check evidence freshness** (evidence decay):
   - Scan all `provenance` blocks across canvas files for `validated_at` or `captured_at` timestamps
   - Compare against staleness thresholds from `${CLAUDE_PLUGIN_ROOT}/engine/evidence-decay.md`:
     - User needs/interviews: 90 days
     - Competitive intelligence: 90 days
     - Strategic assumptions: 180 days
     - Technical feasibility: 120 days
     - DORA/delivery metrics: 30 days
   - Flag evidence past threshold as warning; past 3x threshold as critical
   - Suggest refresh actions: "Evidence in [file] is [N] days old. Run `/mycelium:user-interview` or `/mycelium:log-evidence` to refresh."
   - Note: corrections and patterns do NOT decay — process learnings are timeless

7b. **Check metric snapshot freshness** (v0.14):
   - If `.claude/jit-tooling/active-metrics.yml` exists, for each `status: active` source:
     - Find the newest snapshot in `.claude/evals/metrics/<source>/`.
     - If >7 days old: warning ("[source] snapshot is [N] days old — run `/mycelium:metrics-pull` to refresh").
     - If >30 days old: critical (evidence this stale is worse than no metric reference — anchors old state).
     - If missing entirely: info-level ("No snapshots yet for [source]. Run `/mycelium:metrics-pull`.").
   - Also check per-adapter freshness: for each adapter file in `${CLAUDE_PLUGIN_ROOT}/jit-tooling/metrics-adapters/`, if `last_known_working` is >180 days old, flag as warning suggesting regeneration via `metrics-adapters/GENERATING.md`.
   - Source: v0.14 metrics harvesting. Metric evidence has a faster staleness curve than interview evidence because the underlying data changes continuously.

8. **Check cross-reference integrity** (leaf lifecycle):
   - Every GIST idea with `source_leaf_id` → verify that leaf exists in `opportunities.yml` (and not in `archived-solutions.yml` without the GIST being shelved)
   - Every service entry with `gist_id` → verify that GIST idea exists
   - Every threat model entry with `solution_id` → verify that solution exists
   - Every go-to-market `feedback_loop` entry with `source_leaf_id` → verify leaf exists
   - Flag broken references as warnings ("Zombie Solution" anti-pattern)

8b. **Check scenario health** (Hoskins):
   - If `.claude/canvas/scenarios.yml` exists:
     - Every scenario must have all four Hoskins elements populated (persona, means, motive, simulation) — flag incomplete scenarios
     - Every scenario must have `lifecycle.born_at` set — flag if missing (orphan scenario with no origin)
     - Every scenario with `confidence > 0.5` must have evidence sources — flag unsupported confidence
     - Every scenario referenced in `lifecycle.designed_against[]` → verify the solution exists in `opportunities.yml` or `gist.yml`
     - Every scenario referenced in `lifecycle.tested_against[]` → verify test date is not in the future
     - Flag scenarios with `status: draft` older than 30 days (stale draft — either promote or discard)
   - If `.claude/canvas/scenarios.yml` does NOT exist but project_type requires it (per ${CLAUDE_PLUGIN_ROOT}/engine/canvas-guidance.yml): flag as warning

9. **Check for boilerplate content**:
   - Flag canvas files where >50% of content matches the template defaults from ${CLAUDE_PLUGIN_ROOT}/engine/canvas-guidance.yml
   - Flag files with placeholder text ("TBD", "TODO", "fill in later", "placeholder")

9b. **Check `docs/` health** (added 2026-05-08 with the docs restructure):
   - **Audience markers**: every public doc under `docs/` (excluding `docs/receipts/cases/` which carry frontmatter) must have **Audience**, **Time to read**, and **Last updated** lines in the first 5 lines. Flag missing markers.
   - **Stub freshness**: docs containing `is forthcoming` are Phase 2 stubs. Flag any stub with `Last updated` older than 60 days — Phase 2 may have stalled.
   - **Length budget compliance**: per `docs/README.md` and `docs/contributing/style.md`:
     - README ≤ 250 lines (hard cap; soft cap 200)
     - `docs/<page>.md` ≤ 400 lines (hard cap; soft cap 250)
     - `docs/receipts/cases/<case>.md` ≤ 250 lines (hard cap; soft cap 150)
     - Flag any file over hard cap (FAIL); warn over soft cap (NUDGE).
   - **Last updated freshness**: any `docs/` file with `Last updated` older than 180 days gets flagged for refresh.
   - **Information scent on links**: scan for "click here", "see [filename](path)" patterns — these violate the scent rule. Flag for review.
   - **Marketing-voice scan**: scan for "powerful", "comprehensive", "robust", "seamless", "best-in-class". Flag occurrences for voice review per `docs/contributing/style.md`.
   - **Receipts case frontmatter**: every file under `docs/receipts/cases/` must have YAML frontmatter with the required fields (id, date, contributor, contributor_link, project, mechanism_or_status, commits, subclass). Flag missing fields.
   - **Highlights rotation cadence**: if README's "How Mycelium got smarter" section has not changed in >90 days (check git log for last commit touching that section), flag as a rotation candidate per `docs/contributing/style.md#highlights-rotation`. The flag is informational; rotation is a `/mycelium:framework-health` decision, not an automatic move.

9c. **Check action-flag timeout handling** (added 2026-05-23 v0.23.43, closes a documented-rule-diverges-from-enforcement instance):

Per `${CLAUDE_PLUGIN_ROOT}/engine/canvas-guidance.yml#action_flags.transitions.timeout_handling`: "ON HOLD entries with calendar conditions (e.g., 'pending May 7 evidence') that pass their named date should be flagged, not silently expired. Surface as a stale flagged item via /canvas-health (existing staleness machinery applies). Do NOT auto-transition to OPEN — the absence of the awaited evidence is itself a finding worth surfacing to the user. After 30 days past a named date with no resolution, suggest re-evaluating whether the condition is still relevant."

The convention says canvas-health surfaces this. Until v0.23.43 it didn't — the convention was written 2026-05-03 but no canvas-health check was added. This check closes that gap (cluster instance #11 of documented-rule-diverges-from-enforcement, 2026-05-23).

Concretely:
- Scan all canvas `.yml` files for ON HOLD markers via the keyword pattern: `(ON HOLD|on hold)` with a parenthetical containing a calendar date in any of: `YYYY-MM-DD`, `Month DD`, `MM/DD/YYYY`, or month-name forms (e.g., "May 7", "May 2026").
- For each match, parse the date. Resolve relative months to the most plausible recent occurrence (e.g., "May 7" → most recent 2026-05-07).
- Compare to today's date:
  - Future date → no flag (item correctly waiting).
  - Past date, <30 days → **warning**: surface the item as a flagged-pending-with-passed-date, recommend the user check whether the awaited evidence has arrived (and if so, transition per `transitions.on_hold_condition_met` audit rules). Format: "Canvas [file]: item flagged ON HOLD pending [name] [date]; date passed [N] days ago. Evidence: check if [name] arrived; if yes, transition ON HOLD → OPEN per canvas-guidance#transitions; if no, leave."
  - Past date, ≥30 days → **escalation**: same format plus "≥30 days past named date — re-evaluate whether the condition is still relevant or whether the underlying assumption has changed (per canvas-guidance#transitions.timeout_handling.escalation)."
- Do NOT auto-transition any marker. The check surfaces; the maintainer decides.
- The check is INCOMPLETE without inspection of awaited-evidence sources. Treat the output as a prompt for human judgment, not a verdict.

10. **Log findings to .claude/harness/decision-log.md** (MANDATORY):
   - APPEND a `### Canvas Health Report` entry to `.claude/harness/decision-log.md`
   - Include: overall status (HEALTHY/WARNINGS/CRITICAL), stale evidence found, refresh recommendations
   - Use these words explicitly when applicable: "stale", "evidence", "refresh", "interview", "validate"
   - Example: "Evidence in opportunities.yml is stale (183 days old, threshold 90). Refresh needed: run fresh interviews to validate opportunity assumptions."
   - This log entry is essential for auditability and for downstream skills (e.g., `/mycelium:diamond-progress`) to detect health issues

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
  - /mycelium:canvas-update [file] -- [reason]
  - /mycelium:interview -- [if evidence gaps found]
  - /mycelium:log-evidence -- [if confidence unsupported]
```

## Theory Citations
- Karpathy: Knowledge base health checks and auto-maintained indexes
- aiops3000: Anti-drift through externalized knowledge, versioned reference artifacts
- Raschka: "Context quality = model quality" -- canvas quality determines agent output quality
- Gilad: Confidence must be evidence-backed (confidence consistency checks)
- Torres: Evidence triangulation (evidence type consistency)
