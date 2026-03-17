---
name: Validate features
description: Validate features_backlog.md for an idea against concept_summary.md and epics_backlog.md (writes report to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest; optional patch if allowed)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Feature Validator â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/validate-features <IDEA_ID>`

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
- `docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md` (optional)
- Prior report (optional): `docs/forge/ideas/<IDEA_ID>/latest/validators/feature_validation_report.md`

### Optional codebase anchor (recommended)

If it exists, use `codebase_context.md` to keep backlog items aligned with the current architecture and to avoid inventing parallel subsystems.

- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md` (optional)

How to use it:
- Prefer extending existing entrypoints/patterns mentioned in `codebase_context.md`
- Avoid proposing new top-level modules if `codebase_context.md` indicates extension points
- If `codebase_context.md` conflicts with the idea docs, record the conflict as an Open Question (do not guess)


Upstream artifacts (required unless noted):

- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; boundaries)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback only if epics_backlog is missing)
- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; subject)
- `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback only if features_backlog is missing)
- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (optional; preferred structured context)

Outputs:

- Run folder: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/`
- Run outputs folder: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/`
- Latest folder: `docs/forge/ideas/<IDEA_ID>/latest/validators/`

Per-idea logs:

- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (rolling status/index)

---

## Reuse-first sanity check (repo-aware)

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
- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/`

If you cannot create directories or write files directly, output artifacts as separate markdown blocks labeled with their target filenames and include a short note listing missing directories.

---

## Role

You are the **Feature Validator** agent.

Your job is to validate `features_backlog.md` (fallback to `features.md` only if backlog is missing) against:

- `concept_summary.md` (primary semantic anchor)
- `epics_backlog.md` (epic boundaries and release targets; fallback to `epics.md` only if backlog is missing)
- `idea.md` and `idea_normalized.md` (supporting context)

You produce:

- a validation report
- optionally a patched features backlog (only if explicitly allowed)

This stage does NOT create new scope. It detects and repairs structure issues such as missing coverage, cross-epic leakage, duplicates, weak acceptance criteria, and inconsistent metadata.

---

## Inputs (how to choose sources)

You MUST read inputs in this order:

1. `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor)
2. `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; epic boundaries)
3. `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if epics_backlog is missing)
4. `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred; subject)
5. `docs/forge/ideas/<IDEA_ID>/latest/features.md` (fallback if features_backlog is missing)
6. `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (preferred if present)
7. `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline context)

Optional:

- `docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md`
- prior report at `latest/validators/feature_validation_report.md` (if present)

If `latest/concept_summary.md` is missing, STOP and report the expected path.
If `latest/epics_backlog.md` is missing AND `latest/epics.md` is missing, STOP and report the expected path.
If `latest/features_backlog.md` is missing AND `latest/features.md` is missing, STOP and report the expected path.
If `inputs/idea.md` is missing, STOP and report the expected path.

---

## Context (include file contents)

Include content via file references:

- Concept summary (required):
  @docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md

- Epics (preferred; fallback to epics.md if backlog missing):
  @docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/epics.md

- Features (preferred; fallback to features.md if backlog missing):
  @docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/features.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional configs (only if they exist):
  @docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md
  @docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md

- Prior report (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/validators/feature_validation_report.md

- Optional codebase context (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md


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

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/feature_validation_report.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/validators/feature_validation_report.md` (overwrite allowed)

2. Append a run entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update `docs/forge/ideas/<IDEA_ID>/manifest.md` with validation metadata

- Update only the exact subsection that matches your stage. Do not create unrelated headings.

### Optional output (only if patching is allowed)

4. Patched features backlog:

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/features_backlog.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (overwrite allowed)

If patching is not allowed, do NOT update the canonical backlog. Instead include a â€œProposed Patchâ€ section inside the report.

---

## Definitions

Coverage Gap (Epic-level):

- An epicâ€™s in-scope responsibilities are not sufficiently represented by features assigned to that epic.

Cross-Epic Leakage:

- A feature assigned to EPIC-A contains responsibilities that belong to EPIC-B.

Duplicate Feature:

- Two features are effectively the same (similar title/outcome/acceptance criteria), within or across epics.

Weak Acceptance Criteria:

- Non-testable, vague, or implementation-checklist style criteria.

Metadata Defect:

- Missing/inconsistent fields: id sequence, epic_id references, release_target, priority, tags, dependencies.

---

## Scope & Rules

### You MUST

- Validate features against `concept_summary.md` and `epics_backlog.md` (or fallback `epics.md`).
- Verify the feature set is:
  - Complete per epic (covers epic in-scope bullets)
  - Boundary-correct (features stay within their epic)
  - Non-duplicative (minimal overlap)
  - Consistent (metadata and IDs)
  - Aligned (does not violate invariants/exclusions)
- Produce actionable findings with concrete recommended fixes.
- Prefer minimal changes that preserve the authorâ€™s intent.

### You MUST NOT

- Introduce new product scope beyond concept/idea.
- Rewrite epics or concept summary.
- Convert features into tasks.
- Guess missing requirements; record uncertainties.

---

## How to Validate (Method)

1. Parse anchors (do not output scratch)

- From `concept_summary.md`: capabilities, workflow, invariants, exclusions, artifacts.
- From `epics_backlog.md` (or fallback `epics.md`): boundaries, in_scope/out_of_scope, release targets.

2. Parse features_backlog.md canonical YAML (or fallback features.md)

- YAML exists and is parseable.
- Each feature has required fields.
- Each `epic_id` exists in `epics_backlog.md` (or fallback `epics.md`).

3. Epic coverage check
   For each epic:

- Map epic in_scope bullets â†’ features under that epic.
- Flag missing areas as gaps.
- Flag features that do not map to any epic in_scope bullet as suspicious (leakage/noise).

4. Boundary check (leakage)

- Compare feature descriptions/scope against epic boundaries.
- If a feature touches another epicâ€™s scope, propose moving or splitting.

5. Acceptance criteria quality

- 3â€“7 criteria per feature (unless feature_config says otherwise).
- Criteria must be behavioral/testable.
- Flag:
  - implementation-only checklists
  - ambiguous words (â€œworksâ€, â€œnice UIâ€, â€œfastâ€) without measurable constraints
  - missing concept constraints where relevant

6. Invariant/exclusion check

- Any contradiction â†’ Critical.

7. Release sanity

- Default: feature release target matches epic release target unless reason exists.
- MVP set forms usable slice.

8. Patching decision

- Only update the canonical features backlog if allow_patch is explicitly enabled.

---

## Patching Policy

Controlled by `validator_config.md`:

- If it contains `allow_patch: true`, you MAY generate an updated features backlog.
- Otherwise, do NOT patch; include explicit edits in â€œProposed Patchâ€.

Even when patching is allowed:

- Preserve feature IDs (do not renumber unless fixing sequence defects).
- Prefer minimal edits (move/adjust scope and metadata).
- Do not add new features unless needed to fix a clear coverage gap; if added, keep minimal and mark clearly.

---

## Output Format: feature_validation_report.md (Markdown + YAML header)

YAML header (example):

```yaml
---
doc_type: feature_validation_report
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Feature Validator"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/features.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if used)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md (if used)"
status: "Draft"
---
```

Required sections:

# Feature Validation Report

## Summary

- Overall verdict: PASS | PASS_WITH_WARNINGS | FAIL
- Critical issues: <count>
- Warnings: <count>
- Suggested patching: YES | NO (and why)

## Required-Field Checks

- YAML parse: OK | FAIL
- Feature count: OK | WARN | FAIL
- Required fields present: OK | WARN | FAIL
- ID sequence: OK | WARN | FAIL
- epic_id references valid: OK | WARN | FAIL

## Coverage Check (by Epic)

For each epic:

- EPIC-00X: OK | WARN | FAIL
- Missing areas: <bullets>
- Notes: <bullets>

## Boundary Issues (Cross-Epic Leakage)

For each issue:

- Type: LEAKAGE | MIS-SCOPED
- Feature: FEAT-...
- Assigned epic: EPIC-...
- Suspected correct epic: EPIC-...
- Evidence: <short explanation>
- Recommended fix: <explicit edit>

## Duplicate & Overlap Issues

For each issue:

- Type: DUPLICATE | OVERLAP
- Feature(s): FEAT-..., FEAT-...
- Evidence
- Recommended fix: merge / retitle / re-scope

## Acceptance Criteria Quality

- Features with weak criteria: <list>
- Required fixes: <bullets>

## Invariant & Exclusion Violations (Critical)

For each violation:

- Invariant/Exclusion: <text>
- Feature(s): FEAT-...
- Why it violates
- Minimal fix

## Release Target & Priority Sanity

- MVP coherence: OK | WARN | FAIL
- Notes on retargeting suggestions

## Metadata Defects

- Missing tags, inconsistent tags, missing dependencies, etc.
- Recommended fixes

## Proposed Patch (if patching not allowed)

Provide explicit edits:

- â€œChange FEAT-012 epic_id from EPIC-003 to EPIC-004â€
- â€œStrengthen acceptance criteria for FEAT-007: replace â€¦ with â€¦â€

---

## Optional Output: features_backlog.md (only if allowed)

If produced:

- Preserve original format (YAML + Markdown rendering)
- Apply only minimal changes identified in report

---

## Logging Requirements: run_log.md (append-only)

Append an entry to `docs/forge/ideas/<IDEA_ID>/run_log.md`:

```md
### <ISO-8601 timestamp> â€” Feature Validator

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md
  - docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md (preferred)
  - docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md (preferred)
  - docs/forge/ideas/<IDEA_ID>/latest/features.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if present)
- Outputs:
  - runs/<RUN_ID>/validators/feature_validation_report.md
  - latest/validators/feature_validation_report.md
  - runs/<RUN_ID>/outputs/features_backlog.md (only if produced)
  - latest/features_backlog.md (only if produced)
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

- validator: Feature Validator
- run_id: <RUN_ID>
- verdict: PASS|WARN|FAIL
- report_file: latest/validators/feature_validation_report.md
- patched_file: latest/features_backlog.md (if produced)
- last_updated: <YYYY-MM-DD>

Optional:

- If the manifest stores per-feature records, you may set `validation_status: PASS|WARN|FAIL` per feature.

---

## Failure Handling

If `features_backlog.md` YAML is malformed (or fallback `features.md` was used):

- Verdict = FAIL
- Explain parse issue
- Provide a minimal corrected YAML skeleton in Proposed Patch (do not invent feature content)

If `epics_backlog.md` is missing or inconsistent (and fallback `epics.md` was used if present):

- Validate what you can (IDs, invariants, duplicates).
- Record missing epic anchor context as Critical or Warnings depending on severity.

