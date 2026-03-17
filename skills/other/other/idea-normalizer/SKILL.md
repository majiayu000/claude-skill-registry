---
name: Normalize idea
description: Normalize an idea into a consistent structure (writes to ideas/<IDEA_ID>/runs and updates ideas/<IDEA_ID>/latest). If Open Questions exist, ask the user and finalize with captured answers.
argument-hint: "<IDEA_ID>   (example: IDEA-0002_controller-tool)"
disable-model-invocation: true
---

# Idea Normalizer â€” Agent Instructions

## Invocation

Run this command with an idea folder id:

- `/idea-normalizer <IDEA_ID>`

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

- `docs/forge/ideas/<IDEA_ID>/inputs/idea.md`
- `docs/forge/ideas/<IDEA_ID>/inputs/normalizer_config.md` (optional)
- `docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md` (optional; created in interactive mode)

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

## Inputs

### Required

- `idea.md` at `docs/forge/ideas/<IDEA_ID>/inputs/idea.md`

### Optional

- `normalizer_config.md` at `docs/forge/ideas/<IDEA_ID>/inputs/normalizer_config.md`
- `normalizer_answers.md` at `docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md` (if it exists)

If `idea.md` is missing, STOP and report the expected path.

---

## Context (include file contents)

Use file references to pull content into context:

- Raw idea:
  @docs/forge/ideas/<IDEA_ID>/inputs/idea.md

- Optional config (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/inputs/normalizer_config.md

- Optional prior answers (only if it exists):
  @docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md

---

## Run identity

Generate:

- `RUN_ID` as a filesystem-safe id (Windows-safe, no `:`), e.g.:
  - `2026-01-10T19-22-41Z_run-8f3c`

Also capture:

- `generated_at` as ISO-8601 time (may include timezone offset)

---

## Outputs (required)

### Always write a draft first

1) Write a draft to the run folder:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/idea_normalized_draft.md`

2) Write the Open Questions list for the run:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/open_questions.md`

### Final outputs (only after questions are resolved OR if no questions exist)

3) Write final `idea_normalized.md` to:

- `docs/forge/ideas/<IDEA_ID>/runs/<RUN_ID>/idea_normalized.md`

Then also update:

- `docs/forge/ideas/<IDEA_ID>/latest/idea_normalized.md` (overwrite allowed)

4) Append an entry to:

- `docs/forge/ideas/<IDEA_ID>/run_log.md`

5) Update (or create) the per-idea manifest at:

- `docs/forge/ideas/<IDEA_ID>/manifest.md`

---

## Interactive Open Questions Resolution (IMPORTANT)

Goal: avoid leaving key decisions as â€œOpen Questionsâ€ when the user can answer them now.

### Default behavior
- If Open Questions exist, you MUST ask the user those questions and capture their answers.
- Exception: if `normalizer_config.md` explicitly sets `interactive: false`, then proceed without asking and keep Open Questions as-is.

### Phase 1 â€” Draft + ask
After producing `idea_normalized_draft.md` and `open_questions.md`:

1) Present the questions to the user as a numbered list.
2) Ask the user to answer in the same numbered format.
3) STOP and wait for the userâ€™s reply.

Also append a run_log entry with:
- Status: `NEEDS_USER_INPUT`
- Run-ID: `<RUN_ID>`
- Output draft paths

### Phase 2 â€” Capture answers + finalize
When the user replies:

1) Save the userâ€™s answers to:
- `docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md`
  - Append a new section with header: `### <ISO-8601> â€” Answers for <RUN_ID>`

2) Produce final `idea_normalized.md`:
- Move answered items into the correct sections (Constraints, Preferences, Outputs, etc.)
- Remove or reword answered questions from â€œOpen Questionsâ€
- Keep any truly unresolved items in â€œOpen Questionsâ€

3) Write final outputs to `runs/<RUN_ID>/idea_normalized.md` and `latest/idea_normalized.md`

4) Append a new run_log entry with:
- Status: `SUCCESS` (or `SUCCESS_WITH_WARNINGS` if some questions remain unanswered)
- Notes: include a bullet like `Resolved N open questions; remaining M`

---

## Definition: Normalization

Normalization means:

- Preserve meaning and scope of the source idea
- Re-express in consistent sections/terminology
- Make implicit structure explicit (inputs, workflow, outputs, constraints, exclusions)
- Record uncertainties instead of guessing

Normalization does NOT mean:

- Adding new requirements
- Choosing tech stacks not stated in the source
- Writing implementation plans, epics, features, or tasks

---

## Scope & Rules

### You MUST

- Preserve original intent and scope from `idea.md`
- Use the required section template below
- Convert free-form text into concise bullets where appropriate
- Mark assumptions explicitly as assumptions
- Capture constraints and exclusions explicitly
- Include â€œOpen Questionsâ€ for missing decisions (only those that remain after interactive resolution)

### You MUST NOT

- Introduce new scope or features not present in `idea.md`
- Redesign the system
- Produce backlog items
- Remove meaningful nuance; if unsure, keep detail and place it in the correct section

---

## How to Normalize (Method)

1. Read entire `idea.md` once
2. Extract key statements into scratch (do not output scratch)
3. Map statements into the standard sections
4. Rewrite in consistent modality:
   - Must / Should / May
5. Handle contradictions conservatively (record in Open Questions)
6. Keep it brief but complete (prefer bullets)

---

## Output Format: `idea_normalized.md` (Markdown + YAML header)

Write `idea_normalized.md` with a YAML header followed by required sections.

### YAML header (example)

```yaml
---
doc_type: idea_normalized
idea_id: "<IDEA_ID>"
run_id: "<RUN_ID>"
generated_by: "Idea Normalizer"
generated_at: "<ISO-8601>"
source_inputs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/idea.md"
configs:
  - "docs/forge/ideas/<IDEA_ID>/inputs/normalizer_config.md (if used)"
  - "docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md (if used)"
status: "Draft"
---
```

### Required sections

# Idea (Normalized)

## Summary

(1 short paragraph)

## Goals

- ...

## Target Users

- ...

## Primary Use Cases

- ...

## Inputs

- ...

## Outputs

- ...

## Conceptual Workflow

1. ...
2. ...

## Core Capabilities

- The system can ...

## Constraints

- ...

## Preferences

- ...

## Out-of-Scope / Exclusions

- ...

## Terminology

- Term: meaning

## Open Questions / Ambiguities

- ...

---

## Logging Requirements: `run_log.md` (append-only)

Append an entry with this shape:

```md
### <ISO-8601 timestamp> â€” Idea Normalizer

- Idea-ID: <IDEA_ID>
- Run-ID: <RUN_ID>
- Inputs:
  - docs/forge/ideas/<IDEA_ID>/inputs/idea.md
  - docs/forge/ideas/<IDEA_ID>/inputs/normalizer_config.md (if present)
  - docs/forge/ideas/<IDEA_ID>/inputs/normalizer_answers.md (if present)
- Outputs:
  - runs/<RUN_ID>/idea_normalized_draft.md
  - runs/<RUN_ID>/open_questions.md
  - runs/<RUN_ID>/idea_normalized.md (final, if produced)
  - latest/idea_normalized.md (final, if produced)
- Notes:
  - <1â€“5 bullets on key clarifications or ambiguities>
- Status: NEEDS_USER_INPUT | SUCCESS | SUCCESS_WITH_WARNINGS | FAILED
```

---

## Manifest updates: `manifest.md` (per-idea)

If `manifest.md` does not exist, create it using the template below.
If it exists, update ONLY the keys under the `Idea` section.

### Manifest template (if creating new)

```md
# Manifest â€” <IDEA_ID>

## Idea

- idea_normalized_status: Draft
- last_updated: <YYYY-MM-DD>
- last_run_id: <RUN_ID>
- latest_outputs:
  - latest/idea_normalized.md
- notes:
  - <optional bullets>
```

Do not add epics/features/tasks here.

---

## Failure handling

If `idea.md` is extremely short/vague:

- Produce the normalized template anyway
- Put missing items into Open Questions
- Do not invent details

