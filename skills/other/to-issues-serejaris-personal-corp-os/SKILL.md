---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable task files using tracer-bullet vertical slices.
disable-model-invocation: true
---

# To Issues

Break a plan into independently-grabbable task files using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If `PRD.md` exists in the project folder root, read it in full. If the user points at another spec file, read that instead.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Task titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the plan into **tracer bullet** tasks. Each task is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

<vertical-slice-rules>

- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Any prefactoring should be done first

</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Depends on**: which other tasks (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?

Iterate until the user approves the breakdown.

### 5. Write task files

For each approved slice, create one markdown file under `tasks/` in the project folder.

- **Filename**: `NN-slug.md` where `NN` is `01`, `02`, … assigned in dependency order (blockers first, then dependents).
- **Slug**: lowercase words separated by hyphens, derived from the task title.

Use the task file template below.

<task-template>

# Title

Short descriptive title (same as the slice name).

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

Avoid specific file paths or code snippets — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it here and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Depends on

`tasks/NN-slug.md` references for prerequisite tasks, one per line, or `none` if the task can start immediately.

</task-template>

When listing dependencies in **Depends on**, use paths relative to the project folder (e.g. `tasks/01-roster-ingest.md`). Do not modify `PRD.md` when writing tasks.