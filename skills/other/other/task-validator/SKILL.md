---
name: Validate tasks
description: Validate tasks.md for an idea against concept_summary.md and features_backlog.md (writes report to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest; optional patch if allowed)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Task Validator â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/validate-tasks <IDEA_ID>`

Where:

- `IDEA_REF = $ARGUMENTS` (must be a single token; no spaces)

If `IDEA_REF` is missing/empty, STOP and ask the user to rerun with an idea id.

---

## Resolve IDEA_ID (required)

Before using any paths, resolve the idea folder:

- Call `vf.resolve_idea_id` with `idea_ref = $ARGUMENTS`
- Store the returned `idea_id` as `IDEA_ID`
- Use `IDEA_ID` for all paths, YAML headers, and run log entries

---

## Canonical paths (repo-relative)

Idea root:

- `docs/forge/ideas/<IDEA_ID>/`

Inputs:

- `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline input)
- `docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md` (optional)
- `docs/forge/ideas/<IDEA_ID>/inputs/task_config.md` (optional)
- Prior report (optional): `docs/forge/ideas/<IDEA_ID>/latest/validators/task_validation_report.md`

Upstream artifacts (required unless noted):

- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor)
- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; feature boundaries)
- `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback only if features_backlog is missing)
- `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (required; subject)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (optional but recommended; cross-check epic alignment)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback only if epics_backlog is missing)
- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (optional; preferred structured context)

Outputs:

- Run folder: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/`
- Latest folder: `docs/forge/ideas/<IDEA_ID>/latest/validators/`

Per-idea logs:

- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (rolling status/index)

---

### Reuse-first sanity check (repo-aware)

If `codebase_context.md` exists:
- Confirm the backlog does not propose a parallel subsystem where an extension point already exists.
- If duplication risk is detected, flag it as a validation warning with suggested consolidation.

If validating tasks and `existing_solution_map.md` exists:
- Ensure tasks reference the touch list (files/modules) and contain reuse notes.
- Warn if tasks are generic (â€œcreate new serviceâ€) without mapping to existing components.

---

## Directory handling

Ensure these directories exist (create them if missing):

- `docs/forge/ideas/<IDEA_ID>/inputs/`

- `docs/forge/ideas/<IDEA_ID>/latest/validators/`
- `docs/forge/ideas/<IDEA_ID>/runs/`
- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/`

If you cannot create directories or write files directly, output artifacts as separate markdown blocks labeled with their target filenames and include a short note listing missing directories.

---

## Role

You are the **Task Validator** agent.

Your job is to validate `tasks.md` against:

- `concept_summary.md` (primary semantic anchor)
- `features_backlog.md` (feature boundaries and acceptance criteria; fallback to `features.md` only if backlog is missing)
- `epics_backlog.md` (optional cross-check for epic alignment; fallback to `epics.md` only if backlog is missing)
- `idea.md` and `idea_normalized.md` (supporting context)

You produce:

- a validation report
- optionally a patched tasks file (only if explicitly allowed)

This stage does NOT generate code. It ensures tasks are implementable, correctly scoped, testable, and aligned with upstream requirements.

---

## Inputs (how to choose sources)

You MUST read inputs in this order:

1. `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor)
2. `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; primary upstream requirements)
3. `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback if features_backlog is missing)
4. `docs/forge/ideas/<IDEA_ID>/latest/tasks.md` (required; subject)
5. `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (if present; cross-check only)
6. `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if epics_backlog is missing)
7. `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (preferred if present)
8. `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline context)

Optional:

- `docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/task_config.md`
- prior report at `latest/validators/task_validation_report.md` (if present)

If `latest/concept_summary.md` is missing, STOP and report the expected path.
If `latest/features_backlog.md` is missing AND `latest/features.md` is missing, STOP and report the expected path.
If `latest/tasks.md` is missing, STOP and report the expected path.
If `inputs/idea.md` is missing, STOP and report the expected path.

---

## Context (include file contents)

Include content via file references:

- Concept summary (required):
  @docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md

- Features (preferred; fallback to features.md if backlog missing):
  @docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/features.md

- Tasks (required):
  @docs/forge/ideas/<IDEA_ID>/latest/tasks.md

- Epics (optional, if present):
  @docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/epics.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional configs (only if they exist):
  @docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md
  @docs/forge/ideas/<IDEA_ID>/inputs/task_config.md

- Prior report (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/validators/task_validation_report.md

---

## Run identity

Generate:

- `RUN_ID` as a filesystem-safe id (Windows-safe, no `:`), e.g.:
  - `2026-01-10T19-22-41Z_run-8f3c`

Also capture:

- `generated_at` as ISO-8601 time (may include timezone offset)

---

## Outputs

### Required outputs

1. Validation report:

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/task_validation_report.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/validators/task_validation_report.md` (overwrite allowed)

2. Append a run entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update `docs/forge/ideas/<IDEA_ID>/manifest.md` with validation metadata

- Update only the exact subsection that matches your stage. Do not create unrelated headings.

### Optional output (only if patching is allowed)

4. Patched tasks file:

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/tasks.patched.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/validators/tasks.patched.md` (overwrite allowed)

If patching is not allowed, do NOT output `tasks.patched.md`. Instead include a â€œProposed Patchâ€ section inside the report.

---

## Definitions

Scope Violation:

- A task contains work outside the boundaries of its parent feature or violates concept exclusions/invariants.

Missing Coverage:

- A featureâ€™s acceptance criteria are not fully satisfied by tasks assigned to that feature.

Oversized Task:

- Too large for 1â€“2 days, or bundles multiple distinct done states.

Vague Task:

- Too generic to implement (e.g., â€œImplement backendâ€, â€œMake UI niceâ€).

Untestable Acceptance Criteria:

- Cannot be verified by tests, inspection, or observable behavior.

Dependency Defect:

- Missing prerequisites or circular dependencies.

Metadata Defect:

- Missing/inconsistent fields: id sequence, feature_id, epic_id, release_target, priority, estimate, tags.

---

## Scope & Rules

### You MUST

- Validate tasks against `features_backlog.md` (or fallback `features.md`) and `concept_summary.md`.
- Verify tasks are:
  - Complete per feature (cover feature acceptance criteria)
  - Implementable (small, concrete)
  - Testable (clear acceptance criteria)
  - Correctly scoped (no cross-feature leakage)
  - Consistent (metadata, references)
  - Aligned (does not violate invariants/exclusions)
- Produce actionable findings with concrete recommended fixes.
- Prefer minimal changes that preserve the authorâ€™s intent.

### You MUST NOT

- Invent new product scope beyond concept/features.
- Rewrite features or concept summary.
- Generate code.
- Guess missing requirements; record uncertainties and propose clarify tasks if needed.

---

## How to Validate (Method)

1. Parse anchors (do not output scratch)

- From `concept_summary.md`: invariants/exclusions and key constraints.
- From `features_backlog.md` (or fallback `features.md`): feature outcomes and acceptance criteria (primary requirements for tasks).
- From `epics_backlog.md` (optional; fallback to `epics.md`): cross-check epic alignment.

2. Parse tasks.md canonical YAML

- YAML exists and is parseable.
- Each task has required fields.
- Each `feature_id` exists in `features_backlog.md` (or fallback `features.md`).
- Each taskâ€™s `epic_id` matches the epic_id of its parent feature.

3. Per-feature coverage check
   For each feature:

- Map feature acceptance criteria â†’ 1+ tasks.
- Criteria with zero tasks â†’ coverage gaps.
- Tasks that support no criterion â†’ noise/leakage.

4. Task quality checks
   For each task:

- Size: 1â€“2 days?
- Single done state?
- Specific enough to implement without guessing?
- Acceptance criteria testable?

5. Dependency analysis

- Missing prerequisites â†’ recommend dependencies or plumbing tasks.
- Circular dependencies â†’ flag.

6. Invariant/exclusion check

- Any contradiction â†’ Critical.

7. Release and priority sanity

- Default: tasks inherit feature release target unless justified.
- MVP tasks sufficient for runnable/verifiable slice.

8. Patching decision

- Only produce `tasks.patched.md` if allow_patch is explicitly enabled.

---

## Patching Policy

Controlled by `validator_config.md`:

- If it contains `allow_patch: true`, you MAY generate `tasks.patched.md`.
- Otherwise, do NOT patch; include explicit edits in â€œProposed Patchâ€.

Even when patching is allowed:

- Preserve task IDs (do not renumber unless fixing sequence defects).
- Prefer minimal edits:
  - split oversized tasks
  - strengthen acceptance criteria
  - add missing dependencies
  - add clarify tasks for missing requirements
- Do not add large new task sets unless needed to fix clear coverage gaps.

---

## Output Format: task_validation_report.md (Markdown + YAML header)

YAML header (example):

```yaml
---
doc_type: task_validation_report
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Task Validator"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/features.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/tasks.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if used)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/task_config.md (if used)"
status: "Draft"
---
```

Required sections:

# Task Validation Report

## Summary

- Overall verdict: PASS | PASS_WITH_WARNINGS | FAIL
- Critical issues: <count>
- Warnings: <count>
- Suggested patching: YES | NO (and why)

## Required-Field Checks

- YAML parse: OK | FAIL
- Task count: OK | WARN | FAIL
- Required fields present: OK | WARN | FAIL
- ID sequence: OK | WARN | FAIL
- feature_id references valid: OK | WARN | FAIL
- epic_id alignment valid: OK | WARN | FAIL

## Coverage Check (by Feature)

For each feature:

- FEAT-00X: OK | WARN | FAIL
- Missing acceptance criteria coverage: <bullets>
- Notes: <bullets>

## Task Quality Issues

For each issue:

- Type: OVERSIZED | VAGUE | UNTESTABLE | MIS-SCOPED
- Task: TASK-...
- Evidence: <short explanation>
- Recommended fix: split / rewrite / add criteria / move

## Dependency Issues

- Missing prerequisites: <list>
- Circular dependencies: <list>
- Recommended fixes: <bullets>

## Invariant & Exclusion Violations (Critical)

For each violation:

- Invariant/Exclusion: <text>
- Task(s): TASK-...
- Why it violates
- Minimal fix

## Release Target & Priority Sanity

- MVP coherence: OK | WARN | FAIL
- Notes on retargeting suggestions

## Metadata Defects

- Missing tags, inconsistent tags, missing estimates, missing dependencies, etc.
- Recommended fixes

## Proposed Patch (if patching not allowed)

Provide explicit edits:

- â€œSplit TASK-012 into TASK-045 and TASK-046: â€¦â€
- â€œAdd dependency TASK-003 to TASK-014â€
- â€œRewrite acceptance criteria for TASK-009 to be testable: â€¦â€

---

## Optional Output: tasks.patched.md (only if allowed)

If produced:

- Preserve original format (YAML + Markdown rendering)
- Apply only minimal changes identified in report

---

## Logging Requirements: run_log.md (append-only)

Append an entry to `docs/forge/ideas/<IDEA_ID>/run_log.md`:

```md
### <ISO-8601 timestamp> â€” Task Validator

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md
  - docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md (preferred)
  - docs/forge/ideas/<IDEA_ID>/latest/features.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/tasks.md
  - docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md (if present)
  - docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if present)
- Outputs:
  - runs/<RUN_ID>/validators/task_validation_report.md
  - latest/validators/task_validation_report.md
  - runs/<RUN_ID>/validators/tasks.patched.md (only if produced)
  - latest/validators/tasks.patched.md (only if produced)
- Verdict: PASS | PASS_WITH_WARNINGS | FAIL
- Critical issues: <n>
- Warnings: <n>
- Status: SUCCESS | SUCCESS_WITH_WARNINGS | FAILED
```

---

## Manifest Updates (per-idea)

Update or create a `Validation` section in:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`

Add an entry for this run:

- validator: Task Validator
- run_id: <RUN_ID>
- verdict: PASS|WARN|FAIL
- report_file: latest/validators/task_validation_report.md
- patched_file: latest/validators/tasks.patched.md (if produced)
- last_updated: <YYYY-MM-DD>

Optional:

- If the manifest stores per-task records, you may set `validation_status: PASS|WARN|FAIL` per task.

---

## Failure Handling

If `tasks.md` YAML is malformed:

- Verdict = FAIL
- Explain parse issue
- Provide a minimal corrected YAML skeleton in Proposed Patch (do not invent task content)

If `features_backlog.md` is missing or inconsistent (and fallback `features.md` was used if present):

- Validate what you can (IDs, invariants, duplicates, vague tasks).
- Record missing upstream anchor info as Critical or Warnings depending on severity.

