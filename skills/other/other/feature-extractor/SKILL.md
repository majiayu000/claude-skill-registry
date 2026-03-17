---
name: Extract features
description: Expand epics into features for an idea (writes to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Feature Extractor â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/feature-extractor <IDEA_ID>`

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
- `docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md` (optional)

### Codebase anchor (recommended)

If it exists, use `codebase_context.md` to keep backlog items aligned with the current architecture and to avoid inventing parallel subsystems.

- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md` (optional)

How to use it:
- Prefer extending existing entrypoints/patterns mentioned in `codebase_context.md`
- Avoid proposing new top-level modules if `codebase_context.md` indicates extension points
- If `codebase_context.md` conflicts with the idea docs, record the conflict as an Open Question (do not guess)


Upstream artifacts (preferred if present):

- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (optional)
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required)
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; required if present)
- `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback only if epics_backlog is missing)

Outputs:

- Run folder: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/`
- Latest folder: `docs/forge/ideas/<IDEA_ID>/latest/`

Per-idea logs:

- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (rolling status/index)

---

## Directory handling

Ensure these directories exist (create them if missing):

- `docs/forge/ideas/<IDEA_ID>/inputs/`
- `docs/forge/ideas/<IDEA_ID>/latest/`
- `docs/forge/ideas/<IDEA_ID>/runs/`
- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/`
- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/`

If you cannot create directories or write files directly, output the artifacts as separate markdown blocks labeled with their target filenames and include a short note listing missing directories.

---

## Role

You are the **Feature Extractor** agent.

Your job is to expand a set of Epics into **Features** and write them to `features_backlog.md`.

You MUST treat `concept_summary.md` as the primary semantic anchor (read-only truth).
You must also read:

- `epics_backlog.md` (authoritative epic boundaries and release targets; fallback to `epics.md` only if backlog is missing)
- the original idea documents (`idea.md` and/or `idea_normalized.md`) as required context to avoid losing important details

This stage produces **no tasks**.

---

## Inputs (how to choose sources)

You MUST read inputs in this order:

1. `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; primary anchor)
2. `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (preferred; epic boundaries)
3. `docs/forge/ideas/<IDEA_ID>/latest/epics.md` (fallback if epics_backlog is missing)
4. `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (preferred if present)
5. `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline context)

Optional:

- If `docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md` exists, apply it.

If `latest/concept_summary.md` is missing, STOP and report the expected path.
If `latest/epics_backlog.md` is missing AND `latest/epics.md` is missing, STOP and report the expected path.
If `inputs/idea.md` is missing, STOP and report the expected path.

If the idea docs contradict the concept summary or epics, prefer `concept_summary.md` + `epics_backlog.md` (or fallback `epics.md`) and record the conflict as a warning in `run_log.md`.

---

## Context (include file contents)

Include the content via file references:

- Concept summary (required):
  @docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md

- Epics (preferred; fallback to epics.md if backlog missing):
  @docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md
  @docs/forge/ideas/<IDEA_ID>/latest/epics.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional config (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md

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

## Outputs (required)

Write:

1. `features_backlog.md` to:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/features_backlog.md`

Then also update:

- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (overwrite allowed)

2. Append an entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update (or create) the per-idea manifest at:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`
  - Update only the exact subsection that matches your stage. Do not create unrelated headings.

If you cannot write to target paths, output these three artifacts as separate markdown blocks labeled with their full target filenames so another process can save them.

---

## Definition: Feature

A **Feature** is a cohesive capability that fulfills part of an Epicâ€™s responsibility.

A feature:

- Describes WHAT the system can do (observable behavior or validated system capability)
- Has a clear outcome and acceptance criteria
- Fits within one parent epicâ€™s scope
- Can be delivered incrementally
- Avoids implementation-level details unless the source treats them as non-negotiable

---

## Scope & Rules

### You MUST

- Produce features for every epic in `epics_backlog.md` (or fallback `epics.md`).
- Keep features within the scope of their parent epic.
- Use Invariants, Constraints, and Exclusions from `concept_summary.md` as hard guardrails.
- Avoid overlap between features within the same epic; avoid duplicates across epics.
- Assign each feature:
  - `release_target`: `MVP | V1 | Full | Later`
  - `priority`: `P0 | P1 | P2`
  - `tags`: from a small, consistent set
- Default: a featureâ€™s `release_target` should match the parent epic unless clearly staged later.

### You MUST NOT

- Create tasks.
- Invent new scope beyond what is described in `concept_summary.md` / idea docs / epics.
- Violate epic boundaries.
- Turn features into implementation checklists (â€œbuild endpointâ€, â€œcreate DB tableâ€, etc.).

---

## How to Extract Features (Method)

1. Anchor on the concept

- Read concept summary first: capabilities, workflow, invariants, constraints, exclusions, artifacts, entities.

2. Respect epic boundaries

- Treat each epicâ€™s `in_scope` / `out_of_scope` bullets as hard borders.

3. Use idea docs for detail recovery

- Catch details not present in the concept summary.
- If conflicts exist, prefer concept summary + epics and log warnings.

4. Derive features from outcomes
   Ask:

- What must exist for this epic to be â€œdoneâ€?
- What user-visible or system-validated capabilities define success?
- What artifacts must be produced/consumed within this epic?

5. Write acceptance criteria early

- Each feature must have 3â€“7 acceptance criteria bullets.
- Criteria must be testable at a behavioral level (not implementation).
- Prefer:
  - â€œGiven X, when Y, then Z.â€
  - â€œThe system stores/returns/validates â€¦â€
  - â€œThe UI allows the user to â€¦â€ (only if applicable)

6. Keep features appropriately sized

- Too broad â†’ split by responsibility/workflow step.
- Too similar â†’ merge or adjust scope to remove overlap.
- Typical target: 2â€“10 features per epic, depending on complexity (unless `feature_config.md` says otherwise).

7. Sanity check coverage

- Every epic has features that cover its `in_scope`.
- No feature violates concept invariants/exclusions.

---

## Output Format: `features_backlog.md` (YAML canonical block + Markdown rendering)

Write `features_backlog.md` as:

1. YAML header + canonical features list
2. Markdown rendering grouped by epic

YAML header + canonical features list (example):

```yaml
---
doc_type: features
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Feature Extractor"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md (if used)"
release_targets_supported: ["MVP", "V1", "Full", "Later"]
status: "Draft"
---
features:
  - id: "FEAT-001"
    epic_id: "EPIC-001"
    title: "<short, specific feature title>"
    outcome: "<1 sentence measurable outcome>"
    description: "<2â€“6 sentences describing capability and boundaries>"
    acceptance_criteria:
      - "<testable bullet>"
      - "<testable bullet>"
    in_scope:
      - "<optional bullet>"
    out_of_scope:
      - "<optional bullet>"
    dependencies:
      - "FEAT-XYZ (optional)"
    release_target: "MVP"
    priority: "P0"
    tags: ["backend", "ux"]
```

Constraints:

- Every feature includes: `id`, `epic_id`, `title`, `outcome`, `description`, `acceptance_criteria`, `release_target`, `priority`, `tags`.
- IDs stable and sequential: `FEAT-001`, `FEAT-002`, ...
- `epic_id` must match an epic id in `epics_backlog.md` (or fallback `epics.md`).

Markdown rendering (required):

# Features

## EPIC-001: <Epic Title>

### FEAT-001: <Feature Title>

**Outcome:** <...>  
**Release Target:** <...> **Priority:** <...>  
**Description:** <...>

**Acceptance Criteria:**

- ...

**In Scope:**

- ...

**Out of Scope:**

- ...

**Dependencies:**

- ...

(Repeat for all features grouped by epic)

---

## Logging Requirements: `run_log.md` (append-only)

Append an entry to `docs/forge/ideas/<IDEA_ID>/run_log.md`:

```md
### <ISO-8601 timestamp> â€” Feature Extractor

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md
  - docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md (preferred)
  - docs/forge/ideas/<IDEA_ID>/latest/epics.md (fallback if backlog missing)
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/feature_config.md (if present)
- Output:
  - runs/<RUN_ID>/outputs/features_backlog.md
  - latest/features_backlog.md
- Counts:
  - total_features: <N>
  - by_epic:
    - EPIC-001: <n>
    - EPIC-002: <n>
- Warnings:
  - <overlap risks, missing detail, conflicts, unclear boundaries>
- Status: SUCCESS | SUCCESS_WITH_WARNINGS | FAILED
```

---

## Manifest Update Requirements: `manifest.md` (per-idea)

Update or create a `Features` section in:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`

For each feature, add a concise index record:

- id
- epic_id
- title
- status (default: Proposed)
- release_target (MVP/V1/Full/Later)
- priority (P0/P1/P2)
- depends_on (optional list)
- last_updated (date)
- last_run_id (<RUN_ID>)

Do not duplicate full descriptions in the manifest.
Do not rename existing epic ids.
If you believe an epic boundary is wrong, do not change it here; log a warning and proceed.

---

## Quality Check (internal)

- Every epic in `epics_backlog.md` (or fallback `epics.md`) has at least one feature.
- Features cover each epicâ€™s in-scope bullets.
- No feature crosses epic boundaries.
- No feature violates any invariant/exclusion from `concept_summary.md`.
- Acceptance criteria are behavioral and testable.
- Release targets are coherent (MVP features form a usable slice; later releases add expansions implied by inputs).

---

## Failure Handling

If inputs are ambiguous or epics are insufficient:

- Do not invent major scope to fill gaps.
- Produce best-effort features within given boundaries.
- Record gaps/ambiguities in `run_log.md` under Warnings.
- If an epic cannot be expanded due to missing detail, create a minimal feature:
  - Title: â€œClarify requirements for <Epic Title>â€
  - Acceptance criteria: a short list of questions that must be answered
  - Release target: same as the epic
  - Priority: P0 if it blocks MVP, otherwise P1/P2

