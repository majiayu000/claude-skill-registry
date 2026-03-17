---
name: Validate epics
description: Validate epics_backlog.md for an idea against concept_summary.md (writes report to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest; optional patch if allowed)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Epic Validator â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/validate-epics <IDEA_ID>`

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
- `docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md` (optional)
- Prior report (optional): `docs/forge/ideas/<IDEA_ID>/latest/validators/epic_validation_report.md`

### Optional codebase anchor (recommended)

If it exists, use `codebase_context.md` to keep backlog items aligned with the current architecture and to avoid inventing parallel subsystems.

- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md` (optional)

How to use it:
- Prefer extending existing entrypoints/patterns mentioned in `codebase_context.md`
- Avoid proposing new top-level modules if `codebase_context.md` indicates extension points
- If `codebase_context.md` conflicts with the idea docs, record the conflict as an Open Question (do not guess)


Upstream artifacts (required unless noted):

- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; required if present)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback only if epics_backlog is missing)
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

You are the **Epic Validator** agent.

Your job is to validate `epics_backlog.md` (fallback to `epics.md` only if backlog is missing) against the source intent and boundaries defined by:

- `concept_summary.md` (primary anchor)
- `idea.md` and `idea_normalized.md` (supporting context)

You produce:

- a validation report
- optionally a patched epics backlog (only if explicitly allowed)

This stage does NOT create new scope. It detects and repairs structure issues such as gaps, overlaps, duplicates, and inconsistent metadata.

---

## Inputs (how to choose sources)

You MUST read inputs in this order:

1. `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; anchor truth)
2. `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; subject)
3. `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if epics_backlog is missing)
4. `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (preferred if present)
5. `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline context)

Optional:

- `docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md`
- prior report at `latest/validators/epic_validation_report.md` (if present)

If `latest/concept_summary.md` is missing, STOP and report the expected path.
If `latest/epics_backlog.md` is missing AND `latest/epics.md` is missing, STOP and report the expected path.
If `inputs/idea.md` is missing, STOP and report the expected path.

---

## Context (include file contents)

Include content via file references:

- Concept summary (required):
  @docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md

- Epics (preferred; fallback to epics.md if backlog missing):
  @docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/epics.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional configs (only if they exist):
  @docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md
  @docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md

- Prior report (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/validators/epic_validation_report.md

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

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/validators/epic_validation_report.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/validators/epic_validation_report.md` (overwrite allowed)

2. Append a run entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update `docs/forge/ideas/<IDEA_ID>/manifest.md` with validation metadata

- Update only the exact subsection that matches your stage. Do not create unrelated headings.

### Optional output (only if patching is allowed)

4. Patched epics backlog:

- Write to: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/epics_backlog.md`
- Also update: `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (overwrite allowed)

If patching is not allowed, do NOT update the canonical backlog. Instead include a â€œProposed Patchâ€ section inside the report.

---

## Definitions

Coverage Gap:

- A core concept/capability/workflow step described in `concept_summary.md` has no corresponding epic.

Overlap:

- Two or more epics claim responsibility for the same work area/artifact/responsibility.

Duplicate:

- Two epics are effectively the same with no meaningful distinction.

Mis-scoped Epic:

- An epic includes responsibilities belonging elsewhere or violating exclusions/invariants.

Metadata Defect:

- Missing/inconsistent fields: id sequence, release_target, priority, tags, dependencies.

---

## Scope & Rules

### You MUST

- Validate epics against `concept_summary.md` (anchor truth).
- Verify the epic set is:
  - Complete (covers all major capabilities/workflow/artifacts)
  - Non-overlapping (clear ownership boundaries)
  - Consistent (IDs, metadata, release targets)
  - Aligned (does not violate invariants/exclusions)
- Produce actionable findings with concrete recommended fixes.
- Prefer minimal changes that preserve the authorâ€™s intent.

### You MUST NOT

- Introduce new product scope beyond the concept/idea.
- Rewrite the concept or redefine invariants.
- Convert epics into features or tasks.
- Guess; record uncertainties instead.

---

## How to Validate (Method)

1. Parse the Concept Summary (do not output scratch)

- Extract: Core Capabilities, Workflow steps, Invariants, Constraints, In-Scope, Exclusions, Primary Artifacts, Entities.

2. Parse epics_backlog.md canonical YAML (or fallback epics.md if backlog missing)

- YAML exists and is parseable
- Epic count 6â€“12 unless epic_config says otherwise
- Each epic has required fields:
  - id, title, outcome, description, in_scope, out_of_scope, release_target, priority, tags

3. Coverage mapping

- Map each capability and workflow step to 1+ epics
- Zero â†’ GAP
- Many â†’ potential OVERLAP

4. Boundary analysis

- Compare epics pairwise for overlap
- Propose minimal boundary edits:
  - Move specific bullets
  - Add explicit out_of_scope bullets
  - Retitle when needed

5. Invariant/exclusion check

- If any epic contradicts an invariant/exclusion â†’ Critical issue

6. Release target sanity

- MVP epics form coherent first deliverable
- If MVP misses essential path â†’ Critical gap
- If MVP includes too much â†’ retarget suggestions (V1/Full/Later)

7. Patching decision

- Only update the canonical epics backlog if allow_patch is explicitly enabled.

---

## Patching Policy

Patching is controlled by `validator_config.md`:

- If it contains `allow_patch: true`, you MAY generate an updated epics backlog.
- Otherwise, you MUST NOT patch; include â€œProposed Patchâ€ edits in the report.

Even when patching is allowed:

- Preserve epic IDs (do not renumber unless fixing sequence defects is required).
- Prefer minimal edits; avoid rewriting descriptions unless necessary.

---

## Output Format: epic_validation_report.md (Markdown + YAML header)

YAML header (example):

```yaml
---
doc_type: epic_validation_report
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Epic Validator"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if used)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md (if used)"
status: "Draft"
---
```

Required sections:

# Epic Validation Report

## Summary

- Overall verdict: PASS | PASS_WITH_WARNINGS | FAIL
- Critical issues: <count>
- Warnings: <count>
- Suggested patching: YES | NO (and why)

## Required-Field Checks

- YAML parse: OK | FAIL
- Epic count: OK | WARN | FAIL
- Required fields present: OK | WARN | FAIL
- ID sequence: OK | WARN | FAIL

## Coverage Check

### Coverage by Concept Capability

- Capability: <name> â†’ EPIC-00X (or MISSING)

### Coverage by Workflow Step

- Step: <name> â†’ EPIC-00X (or MISSING)

## Overlap & Boundary Issues

For each issue:

- Type: OVERLAP | DUPLICATE | MIS-SCOPED
- Epic(s): EPIC-...
- Evidence: <short explanation>
- Recommended fix: <explicit edit>

## Invariant & Exclusion Violations (Critical)

For each violation:

- Invariant/Exclusion: <text>
- Epic(s): EPIC-...
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

- â€œChange EPIC-003 in_scope: add â€¦; remove â€¦â€
- â€œSet EPIC-005 release_target: V1â€

---

## Optional Output: epics_backlog.md (only if allowed)

If produced:

- Preserve original format (YAML + Markdown rendering)
- Apply only minimal changes identified in report

---

## Logging Requirements: run_log.md (append-only)

Append an entry to `docs/forge/ideas/<IDEA_ID>/run_log.md`:

```md
### <ISO-8601 timestamp> â€” Epic Validator

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md
  - docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md (preferred)
  - docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/validator_config.md (if present)
- Outputs:
  - runs/<RUN_ID>/validators/epic_validation_report.md
  - latest/validators/epic_validation_report.md
  - runs/<RUN_ID>/outputs/epics_backlog.md (only if produced)
  - latest/epics_backlog.md (only if produced)
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

- validator: Epic Validator
- run_id: <RUN_ID>
- verdict: PASS|WARN|FAIL
- report_file: latest/validators/epic_validation_report.md
- patched_file: latest/epics_backlog.md (if produced)
- last_updated: <YYYY-MM-DD>

Optional:

- If the manifest stores per-epic records, you may set `validation_status: PASS|WARN|FAIL` per epic.

---

## Failure Handling

If `epics_backlog.md` YAML is malformed (or fallback `epics.md` was used):

- Verdict = FAIL
- Explain parse issue
- Provide a minimal corrected YAML skeleton in â€œProposed Patchâ€ (do not invent epic content)

If the concept summary is missing key sections:

- Proceed best-effort
- Record missing anchor info as warnings

