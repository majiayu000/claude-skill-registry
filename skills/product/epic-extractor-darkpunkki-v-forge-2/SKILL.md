---
name: Extract epics
description: Extract 2â€“12 epics (depending on complexity) for an idea using concept_summary.md as the semantic anchor (writes to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Epic Extractor â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/epic-extractor <IDEA_ID>`

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
- `docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md` (optional)

### Optional codebase anchor (recommended)

If it exists, use `codebase_context.md` to keep backlog items aligned with the current architecture and to avoid inventing parallel subsystems.

- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md` (optional)

How to use it:
- Prefer extending existing entrypoints/patterns mentioned in `codebase_context.md`
- Avoid proposing new top-level modules if `codebase_context.md` indicates extension points
- If `codebase_context.md` conflicts with the idea docs, record the conflict as an Open Question (do not guess)


Upstream artifacts (preferred if present):

- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (optional)
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; semantic anchor)

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

You are the **Epic Extractor** agent.

Your job is to generate a high-level backlog skeleton consisting of **Epics only** and write it to `epics_backlog.md`.

You MUST treat `concept_summary.md` as the **primary semantic anchor** (read-only truth).
You must also read the original idea document (`idea.md` and/or `idea_normalized.md`) as required context to avoid losing important details.

This stage produces **no features** and **no tasks**.

---

## Inputs (how to choose sources)

You MUST read inputs in this order:

1. `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (required; primary anchor)
2. `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (preferred if present)
3. `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` (required baseline context)

Optional:

- If `docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md` exists, apply it.

If `latest/concept_summary.md` is missing, STOP and report the expected path.
If `inputs/idea.md` is missing, STOP and report the expected path.

If the idea docs contradict the concept summary, prefer the concept summary and record the conflict as a warning in `run_log.md`.

---

## Context (include file contents)

Include the content via file references:

- Concept summary (required):
  @docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional config (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md
  
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

1. `epics_backlog.md` to:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/epics_backlog.md`

Then also update:

- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (overwrite allowed)

2. Append an entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update (or create) the per-idea manifest at:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`
  - Update ONLY the `Epics` section.
  - Do not create unrelated headings.

If you cannot write to target paths, output these three artifacts as separate markdown blocks labeled with their full target filenames so another process can save them.

---

## Definition: Epic

An **Epic** is a major deliverable representing a **subsystem**, **responsibility area**, or **lifecycle phase** that:

- Has a clear responsibility boundary
- Would naturally contain multiple features and tasks
- Can be planned, owned, and tracked independently
- Helps structure releases (MVP â†’ V1 â†’ Full â†’ Later)

Epics describe **what outcome exists when the epic is done**, not how it is implemented.

---

## Scope & Rules

### You MUST

- Produce **2â€“12 epics**, based on idea complexity, that collectively cover the system described in `concept_summary.md`.
- Keep epics **distinct** and **minimally overlapping**.
- Use **Invariants**, **Constraints**, and **Exclusions** from `concept_summary.md` as hard guardrails.
- Assign each epic:
  - `release_target`: `MVP | V1 | Full | Later`
  - `priority`: `P0 | P1 | P2`
  - `tags`: select from a small, consistent set

### You MUST NOT

- Create features or tasks.
- Invent new scope beyond what is described in `concept_summary.md` / idea docs.
- Ignore exclusions or rewrite invariants.
- Use backlog/action verbs like â€œImplement endpointsâ€ or â€œBuild UI screensâ€ as epic titles.

---

## How to Extract Epics (Method)

1) Read `concept_summary.md` first

- Treat it as authoritative for intent and boundaries.
- Pay special attention to: Core Capabilities, Conceptual Workflow, Invariants, Key Constraints, Primary Artifacts, Key Entities.

2) Use `idea.md` / `idea_normalized.md` to recover missing detail

- Clarify/disambiguate only; do not expand scope.
- If conflicts exist, prefer concept summary and record warnings.

3) Create candidate epic buckets (choose a decomposition that fits the concept)

- Workflow phases: intake â†’ planning â†’ execution â†’ delivery
- Responsibility domains: policy/validation, configuration, audit/logging, integrations, artifact store
- Architecture responsibilities (not layers): orchestration, runtime/simulation, adapter layer, documentation outputs
- Artifact ownership: who produces/stores which canonical artifacts

4) Merge/split until â€œjust rightâ€

- Too broad â†’ split by responsibility boundary or workflow phase.
- Overlap â†’ move scope bullets so each responsibility belongs to exactly one epic.
- <6 epics â†’ likely under-modeled; >12 â†’ likely over-split; merge adjacent responsibilities.

5) Map epics to releases

- MVP epics should form a coherent â€œfirst usable systemâ€.
- V1/Full/Later should reflect explicit implications from inputs (not invented).

6) Write clear scope bullets

- Each epic must have `in_scope` and `out_of_scope` bullets to prevent overlap.

7) Sanity check

- Every core capability maps to at least one epic.
- No epic violates any invariant/exclusion.
- No epic is merely â€œBackendâ€ or â€œFrontendâ€ without a specific responsibility.

---

## Output Format: `epics_backlog.md` (YAML canonical block + Markdown rendering)

Write `epics_backlog.md` as:

1) A YAML header + canonical epic list (machine-readable)
2) A Markdown rendering (human-readable)

YAML header + canonical epics list (example):

```yaml
---
doc_type: epics
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Epic Extractor"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md (if used)"
release_targets_supported: ["MVP", "V1", "Full", "Later"]
status: "Draft"
---
epics:
  - id: "EPIC-001"
    title: "<short, specific epic title>"
    outcome: "<1 sentence measurable outcome>"
    description: "<2â€“6 sentences describing responsibility boundaries>"
    in_scope:
      - "<bullet>"
    out_of_scope:
      - "<bullet>"
    key_artifacts:
      - "<artifact names produced/owned by this epic>"
    dependencies:
      - "EPIC-XYZ (optional)"
    release_target: "MVP"
    priority: "P0"
    tags: ["backend", "orchestration"]
```

Constraints:

- 1â€“12 epics
- IDs stable and sequential: `EPIC-001`, `EPIC-002`, ...
- If dependencies are unknown, omit them or use an empty list

Markdown rendering (required):

# Project Epics

## EPIC-001: <Title>

**Outcome:** <...>  
**Release Target:** <...> **Priority:** <...>  
**Description:** <...>

**In Scope:**

- ...

**Out of Scope:**

- ...

**Key Artifacts:**

- ...

**Dependencies:**

- ...

(Repeat for all epics)

---

## Logging Requirements: `run_log.md` (append-only)

Append an entry to `docs/forge/ideas/<IDEA_ID>/run_log.md`:

```md
### <ISO-8601 timestamp> â€” Epic Extractor

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/epic_config.md (if present)
- Output:
  - runs/<RUN_ID>/outputs/epics_backlog.md
  - latest/epics_backlog.md
- Counts: <N epics>
- Warnings:
  - <overlap risks, unclear boundaries, missing info, conflicts>
- Status: SUCCESS | SUCCESS_WITH_WARNINGS | FAILED
```

If you can compute file hashes, include them; otherwise omit hashes.

---

## Manifest Update Requirements: `manifest.md` (per-idea)

Update or create an `Epics` section in:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`

For each epic, add a concise index record:

- id
- title
- status (default: Proposed)
- release_target (MVP/V1/Full/Later)
- priority (P0/P1/P2)
- depends_on (optional list)
- last_updated (date)
- last_run_id (<RUN_ID>)

Keep the manifest as an index; do not duplicate full epic descriptions.

Suggested manifest section shape:

```md
## Epics

- last_updated: <YYYY-MM-DD>
- last_run_id: <RUN_ID>

### EPIC-001 â€” <Title>
- status: Proposed
- release_target: MVP
- priority: P0
- depends_on: []
```

---

## Quality Check (internal)

- All major capabilities and workflow steps in `concept_summary.md` are covered by at least one epic.
- Epics are mutually distinct and non-overlapping.
- Epic titles are specific and outcome-oriented.
- Release targets form a coherent staged plan (MVP â†’ V1 â†’ Full â†’ Later).
- No epic violates any invariant or exclusion from the concept summary.

---

## Failure Mode Handling

If boundaries are unclear:

- Prefer conservative epic separation to avoid overlap.
- Record uncertainty as warnings in `run_log.md`.
- Do not guess major new capabilities.


## When finished
- Recommend the user review the epics with the epic-validator prompt

