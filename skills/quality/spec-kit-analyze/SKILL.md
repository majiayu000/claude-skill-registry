---
name: spec-kit-analyze
description: Use when `spec.md`, `plan.md`, and `tasks.md` exist and you need a read-only Spec Kit audit for consistency, requirement-to-task coverage, ambiguity, duplication, or constitution conflicts before implementation.
---

# Spec Kit Analyze

Run a non-destructive cross-artifact quality audit before implementation.

## When to Use

- `tasks.md` exists and you want a pre-implementation consistency check across spec/plan/tasks.
- You suspect coverage gaps, requirement drift, ambiguous language, or contradictory artifacts.
- You need a constitution-alignment gate without editing artifacts yet.

## When Not to Use

- Any prerequisite artifact is missing (`spec-kit-specify`, `spec-kit-plan`, or `spec-kit-tasks` first).
- You need targeted remediation edits now (`spec-kit-reconcile`).
- You are executing implementation work (`spec-kit-implement`).

## Router Fit

- Primary route from `spec-kit` after `spec-kit-tasks`.
- Read-only quality gate before `spec-kit-implement`.
- Default handoff to `spec-kit-reconcile` when findings require coordinated artifact updates.

## Critical Constraints

- Strictly read-only: do not modify files.
- Treat `memory/constitution.md` as authoritative; any MUST-level conflict is `CRITICAL`.

## Preconditions

- Run from repository root (or a subdirectory inside it).
- Active feature context resolves to one feature directory with `spec.md`, `plan.md`, and `tasks.md`.

## Workflow

1. Resolve artifact paths and enforce prerequisite gate:

   - Run `scripts/check-prerequisites.sh --json --require-tasks --include-tasks` exactly once.
   - Parse:
     - `FEATURE_DIR`
     - `AVAILABLE_DOCS`
   - Derive:
     - `SPEC = FEATURE_DIR/spec.md`
     - `PLAN = FEATURE_DIR/plan.md`
     - `TASKS = FEATURE_DIR/tasks.md`
   - If any required artifact is missing, stop and route to the owning sibling skill.

2. Load focused sections from:

   - `spec.md`: requirements, stories, acceptance criteria, edge cases.
   - `plan.md`: architecture/stack decisions, phases, constraints.
   - `tasks.md`: task IDs, phase grouping, `[P]` markers, referenced paths.
   - `memory/constitution.md`: principle names and normative MUST/SHOULD statements.

3. Build internal maps:

   - Requirement inventory (functional + non-functional) with stable keys.
   - Story/action inventory with acceptance-test intent.
   - Task-to-requirement/story coverage mapping.
   - Constitution obligations relevant to spec/plan/tasks scope.

4. Detect and classify issues:

   - Duplication: overlapping or near-duplicate requirements.
   - Ambiguity/placeholders: vague quality terms, TODO/TKTK/placeholder tokens.
   - Underspecification: requirements lacking measurable outcomes or clear objects.
   - Constitution conflicts: violations against MUST principles (`CRITICAL`).
   - Coverage gaps: requirements without tasks and tasks without mapped requirement/story.
   - Cross-artifact inconsistency: terminology drift, entity mismatch, ordering contradictions.
   - Cap findings at 50 rows; summarize overflow counts by category.

5. Assign severity and output a compact report with stable IDs, coverage table, and metrics.

   - `CRITICAL`: constitution MUST violations, missing core coverage that blocks baseline behavior.
   - `HIGH`: conflicting/duplicate requirements, untestable or high-risk ambiguity.
   - `MEDIUM`: terminology drift, non-functional coverage gaps, underspecified edge cases.
   - `LOW`: wording/style cleanup without execution impact.

6. Recommend next actions:

   - If `CRITICAL`/`HIGH` findings require cross-artifact edits, block `spec-kit-implement` and route to `spec-kit-reconcile` with a concise gap summary.
   - If only one artifact needs focused updates, route to its owner skill (`spec-kit-specify`, `spec-kit-plan`, or `spec-kit-tasks`).
   - Otherwise provide prioritized improvements and whether implementation can proceed.

7. Offer follow-up only:

   - Ask whether to run `spec-kit-reconcile` using top findings as the gap report.
   - Do not apply any edits in this skill.

## Output

- Markdown report only (no file writes) containing:
  - Findings table: `ID | Category | Severity | Location(s) | Summary | Recommendation`
  - Requirement coverage table: `Requirement Key | Has Task? | Task IDs | Notes`
  - Constitution alignment issues (if any)
  - Unmapped tasks (if any)
  - Metrics:
    - Total requirements
    - Total tasks
    - Coverage percentage
    - Ambiguity count
    - Duplication count
    - Critical issues count
  - Next-step routing recommendation

## References

- `references/command-analyze.md`
- `scripts/check-prerequisites.sh`
- `https://github.com/github/spec-kit/blob/9111699cd27879e3e6301651a03e502ecb6dd65d/templates/commands/analyze.md`
