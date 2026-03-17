---
description: Produce existing_solution_map.md to ground task generation in the current repo.
argument-hint: "<IDEA_ID> [--epic EPIC-00X]"
---


# Existing Solution Map â€” Agent Instructions

## Invocation
- `/existing-solution-map <IDEA_ID> [--epic EPIC-00X]`
Where:
- `IDEA_REF = $ARGUMENTS` (single token; no spaces)
- Optional `--epic EPIC-00X` narrows the map to one epicâ€™s features.

If missing, STOP.

---

## Resolve IDEA_ID (required)
Before using any paths:
- Call `vf.resolve_idea_id` with `idea_ref = $ARGUMENTS`
- Store returned `idea_id` as `IDEA_ID`

---

## Goal
Create an actionable map of â€œwhat already existsâ€ in the repo for this idea (or for one epic),
so that downstream task generation can be extension-oriented and avoid duplicate subsystems.

This artifact is treated as a required input for task generation.

---

## Canonical paths (repo-relative)
Inputs (required):
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md`
- `docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md` (preferred) or `latest/features.md` (fallback)

Optional inputs:
- `docs/forge/ideas/<IDEA_ID>/latest/epics_backlog.md` (to resolve epicâ†’feature grouping)
- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md` (if present; use it)

Outputs:
- `docs/forge/ideas/<IDEA_ID>/latest/existing_solution_map.md`
- Run snapshot:
  - `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/existing_solution_map.md`

Logs:
- `docs/forge/ideas/<IDEA_ID>/run_log.md`

---

## Method (generic, reuse-first)
1) Read concept summary + features backlog.
2) If --epic is provided:
   - Restrict scope to features that belong to that epic (based on epics backlog if available).
3) Identify the main capability areas implied by the features (e.g., API, state, UI, orchestration, logging).
4) For each capability area, search the repo for existing implementations:
   - find current entrypoints, handlers/controllers/routers, state models, UI components
   - find any existing event/message/logging mechanism
   - find existing configs/policies that constrain the design
5) Produce:
   - Reuse decisions: what to extend, what not to duplicate
   - Touch list: concrete files/modules likely to change
   - Gap list: what truly does not exist yet (and where new code may be acceptable)
6) Keep it actionable but not bloated:
   - aim for 15â€“40 touch list entries for a large repo
   - attach a short reason to each

---

## Output format: existing_solution_map.md
Write with YAML header + sections.

YAML header shape:

---
doc_type: existing_solution_map
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Existing Solution Map"
generated_at: "<ISO-8601>"
scope:
  epic: "<EPIC-00X or ALL>"
inputs_used:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/features_backlog.md (or features.md)"
  - "docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md (if used)"
status: "Draft"
---

# Existing Solution Map

## Scope
- Idea: <IDEA_ID>
- Epic scope: <ALL or EPIC-00X>
- Features included: list IDs/titles processed

## Existing â€œhappy pathâ€ flow (as implemented today)
(Short description; if unknown, say so and reference where you looked)

## Reuse-first decisions (hard rules)
- Extend <component/pattern>; do NOT create a parallel <thing>
- Reuse <model/state> as the source of truth
- Keep <interface> stable unless explicitly required

## Key extension points (by capability area)

### API/endpoint layer
- Existing: ...
- Extend by: ...
- Watch-outs: ...

### Core logic / domain layer
- Existing: ...
- Extend by: ...

### Models / state / schemas
- Existing: ...
- Reuse by: ...

### UI layer
- Existing: ...
- Extend by: ...

### Orchestration / simulation (if relevant)
- Existing: ...
- Extend by: ...

### Testing
- Existing test patterns: ...
- Where to add tests: ...

## Touch list (concrete)
List in priority order:
- <path-or-module> â€” reason â€” expected change type (extend/modify/add small helper)

## Gaps / missing pieces
- Gap: ... â€” recommended minimal new module (if needed) â€” constraints

## Risks of duplication / overlap
- Risk: ... â€” mitigation

## Search breadcrumbs
Keywords/phrases that reliably find the relevant areas:
- keyword: ...

---

## Required tool calls
1) vf.start_run with idea_id=<IDEA_ID> (label: existing-solution-map)
2) Write run snapshot to runs/<RUN_ID>/outputs/existing_solution_map.md
3) Write latest to latest/existing_solution_map.md
4) Append a run_log entry with stage codebase.existing_solution_map and outputs.

