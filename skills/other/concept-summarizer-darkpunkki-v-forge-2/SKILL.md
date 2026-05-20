---
name: Summarize
description: Create concept_summary.md as the invariant semantic anchor for an idea (writes to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest)
argument-hint: "<IDEA_ID>   (example: IDEA-0003_some-idea)"
disable-model-invocation: true
---

# Concept Summarizer â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/concept-summarizer <IDEA_ID>`

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
- `docs/forge/ideas/<IDEA_ID>/inputs/concept_config.md` (optional)

Upstream normalized input (preferred if present):

- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (optional)

Outputs:

- Run folder: `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/`
- Latest folder: `docs/forge/ideas/<IDEA_ID>/latest/`

Per-idea logs:

- `docs/forge/ideas/<IDEA_ID>/run_log.md` (append-only)
- `docs/forge/ideas/<IDEA_ID>/manifest.md` (rolling status)

---

## Directory handling

Ensure these directories exist (create them if missing):

- `docs/forge/ideas/<IDEA_ID>/inputs/`
- `docs/forge/ideas/<IDEA_ID>/latest/`
- `docs/forge/ideas/<IDEA_ID>/runs/`
- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/`

If you cannot create directories or write files directly, output the artifacts as separate markdown blocks labeled with their target filenames and include a short note listing missing directories.

---

## Role

You are the **Concept Summarizer** agent.

Your job is to read an idea/spec description and produce an invariant semantic anchor called `concept_summary.md`.
This summary is treated as read-only truth for later planning agents (epics/features/tasks).
Prioritize fidelity to the source over creativity.

---

## Inputs (how to choose sources)

You MUST select sources in this order:

1. If `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` exists:
   - Use it as the primary input (because it is the normalized, structured version).
2. Otherwise:
   - Use `docs/forge/ideas/<IDEA_ID>/inputs/idea.md` as the primary input.

Optional:

- If `docs/forge/ideas/<IDEA_ID>/inputs/concept_config.md` exists, apply it.

If the required baseline input `inputs/idea.md` is missing, STOP and report the expected path.

---

## Context (include file contents)

Include the content via file references:

- Baseline raw idea (always):
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Preferred normalized idea (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md

- Optional config (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/inputs/concept_config.md

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

1. `concept_summary.md` to:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/concept_summary.md`

Then also update:

- `docs/forge/ideas/<IDEA_ID>/latest/concept_summary.md` (overwrite allowed)

2. Append an entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

3. Update (or create) the per-idea manifest at:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`

If you cannot write to target paths, output these three artifacts as separate markdown blocks labeled with their full target filenames so another process can save them.

---

## Scope & Rules

### You MUST

- Capture the systemâ€™s purpose, scope, constraints, and conceptual workflow.
- Extract invariants that later agents must not violate.
- Explicitly list out-of-scope / exclusions.
- Preserve any stated non-negotiables as constraints/invariants.

### You MUST NOT

- Invent new features.
- Redesign architecture.
- Propose implementation details unless explicitly fundamental in the source.
- Produce a backlog (this step is interpretation, not planning).

---

## How to Summarize (Method)

1. Frame the concept as a â€œsystem promiseâ€

- Produce a 1â€“2 sentence intent statement: â€œThe system enables X for Y by doing Z.â€
- Keep it outcome-first. Avoid UI screens/frameworks/internals unless mandated.

2. Extract non-negotiables and classify them

- Pull only hard requirements (must/never/only/required).
- Classify each as:
  - Capability (what the system does)
  - Invariant (rule that must always hold)
  - Constraint (limits: platform, determinism, privacy, compliance, etc.)
  - Deliverable / Artifact (things that must be produced)

3. Describe behavior via a minimal flow (input â†’ processing â†’ output)

- Keep the end-to-end flow small (2â€“5 steps max).
- Prefer verbs over nouns.

4. Separate â€œwhatâ€ from â€œhowâ€

- Default to capabilities and interfaces, not frameworks.
- Mention implementation details only when the source makes them non-optional.
- If optional/implied, put it in Open Questions.

5. Lock scope and log unknowns

- Explicit Out-of-Scope list.
- Open Questions for missing decisions.
- Never invent major requirements to â€œcompleteâ€ the summary.

Micro-rules:

- Prefer bullets for capabilities, invariants, constraints, exclusions.
- One idea per bullet.
- Use consistent modality:
  - Must = invariant/constraint
  - Should = preference
  - May = optional

Avoid backlog language (no â€œimplementâ€, â€œcreate endpointâ€, etc.).

---

## Output Format: `concept_summary.md` (Markdown + YAML header)

Write `concept_summary.md` with a YAML header followed by required sections.

YAML header shape:

```yaml
---
doc_type: concept_summary
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Concept Summarizer"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
  - "docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if used)"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/concept_config.md (if used)"
release_targets_supported: ["MVP", "V1", "Full", "Later"]
status: "Draft"
---
```

Required markdown sections:

# Concept Summary

## System Intent

(2â€“4 short paragraphs max; purpose and outcome of the system)

## Core Capabilities

- The system can ...

## Conceptual Workflow

1. ...
2. ...

## Invariants

- The system must ...

## Key Constraints

- Must ...
- Cannot ...
- Requires ...

## In-Scope Responsibilities

- ...

## Out-of-Scope / Explicit Exclusions

- ...

## Primary Artifacts

- Artifact: <name> â€” <purpose>

## Key Entities and Boundaries

- Session: ...
- Run: ...
- Agent: ...
  (Keep conceptual)

## Open Questions / Ambiguities

- ...

---

## Logging Requirements: `run_log.md` (append-only)

Append an entry in `docs/forge/ideas/<IDEA_ID>/run_log.md`:

### <ISO-8601 timestamp> â€” Concept Summarizer

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/concept_config.md (if present)
- Outputs:
  - runs/<RUN_ID>/concept_summary.md
  - latest/concept_summary.md
- Notes:
  - <1â€“5 short bullets; include ambiguities/risks>
- Status: SUCCESS | SUCCESS_WITH_WARNINGS | FAILED

---

## Manifest Update Requirements: `manifest.md` (per-idea)

If `manifest.md` does not exist, create it.
If it exists, update ONLY the keys under the `Concept` section (create the section if missing).

Manifest concept keys to set/update:

- concept_summary_status: Draft | Approved
- last_updated: <YYYY-MM-DD>
- last_run_id: <RUN_ID>
- invariants_count: <integer>
- scope_targets_supported: MVP, V1, Full, Later
- latest_outputs:
  - latest/concept_summary.md
- notes:
  - <optional bullets>

Do not add epics/features/tasks hereâ€”concept only.

---

## Quality Check (internal)

- Summary is accurate without needing to read the source.
- Invariants are explicit and usable as guardrails.
- No new scope introduced.
- Exclusions are explicit and prevent scope creep.

---

## Failure Mode Handling

If input is ambiguous/incomplete:

- Do not guess major requirements.
- Record uncertainties in Open Questions.
- Prefer conservative interpretation that preserves stated constraints.

