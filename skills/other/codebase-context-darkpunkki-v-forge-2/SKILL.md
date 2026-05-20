---
name: Codebase context
description: Create a lightweight codebase_context.md that anchors the idea in the existing repo (modules, constraints, extension points). Generic framework prompt.
argument-hint: "<IDEA_ID>   (example: IDEA-0003_my-idea)"
disable-model-invocation: true
---

# Codebase Context â€” Agent Instructions

## Invocation
- `/codebase-context <IDEA_ID>`
Where:
- `IDEA_REF = $ARGUMENTS` (single token; no spaces)

If missing, STOP.

---

## Resolve IDEA_ID (required)
Before using any paths:
- Call `vf.resolve_idea_id` with `idea_ref = $ARGUMENTS`
- Store returned `idea_id` as `IDEA_ID`
- Use `IDEA_ID` for all paths and YAML headers

---

## Goal
Produce a lightweight, durable â€œmapâ€ of the existing codebase relevant to this idea, focusing on:
- where to extend vs create
- major boundaries (API layer, core logic, models/state, UI, tests)
- any constraints/invariants implied by the current architecture

This is NOT a full survey and NOT a task list. It is an early anchor to prevent greenfield assumptions.

---

## Canonical paths (repo-relative)
Idea root:
- `docs/forge/ideas/<IDEA_ID>/`

Inputs (required):
- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/concept_summary_config.md`
Fallback/optional:
- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/idea.md`

Outputs:
- `docs/forge/ideas/<IDEA_ID>/latest/codebase_context.md`
- Run snapshot:
  - `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/outputs/codebase_context.md`

Logs:
- `docs/forge/ideas/<IDEA_ID>/run_log.md`

---

## Method (generic, repo-aware)
1) Read the concept summary (primary semantic anchor).
2) Identify which kinds of components are likely involved:
   - API endpoints / controllers / routers
   - core domain logic / services
   - data models / schemas / state
   - UI components
   - orchestration / simulation engine (if applicable)
   - tests and fixtures
3) Do a targeted scan of the repo to find:
   - existing entry points matching the feature area (e.g., control/admin/simulation/session/etc.)
   - existing patterns for request/response models and state persistence
   - existing â€œconfigâ€ or â€œpolicyâ€ mechanisms that constrain behavior
4) Capture only the minimum necessary file/module references (10â€“25 max):
   - keep it stable, not exhaustive
5) Write the output artifact.

If you are unsure where something lives, state it as a hypothesis + provide search cues (keywords to grep), rather than inventing file paths.

---

## Output format: codebase_context.md
Write with YAML header + sections.

YAML header shape:

---
doc_type: codebase_context
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Codebase Context"
generated_at: "<ISO-8601>"
sources:
  - "docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if used)"
status: "Draft"
---

# Codebase Context

## Purpose of this map
(1 short paragraph)

## High-level architecture boundaries (as observed)
- Boundary: ... â€” responsibility â€” notes

## Likely extension points
- Area: ... â€” existing component(s) â€” recommended extension approach

## Key existing concepts to reuse
- Concept/Model: ... â€” where it exists â€” why it matters

## Constraints implied by current architecture
- Constraint: ... â€” evidence â€” impact

## Candidate file/module touch list (max ~25)
List as bullets with a short reason:
- <path-or-module> â€” why itâ€™s relevant

## Unknowns / where to look next
- Unknown: ... â€” suggested keywords or search locations

---

## Required tool calls
1) vf.start_run with idea_id=<IDEA_ID> (label: codebase-context)
2) Write run snapshot to runs/<RUN_ID>/outputs/codebase_context.md
3) Write latest to latest/codebase_context.md
4) Append a run_log entry with stage codebase.context and outputs.

