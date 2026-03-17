---
name: doc-writer
description: Create or update numbered task docs using repo context, DOC_TEMPLATE.md, and naming conventions.
---

# Doc Writer Skill

## Purpose
Generate or refresh `docs/planned/XX-*.md` and `docs/completed/XX-*.md` files using the mandated template (`docs/DOC_TEMPLATE.md`) and existing repository content.

## Instructions
1. Inspect relevant source material:
   - Read `docs/DOC_TEMPLATE.md` for structure expectations.
   - Gather context from `PLAN.md`, `AGENTS.md`, and any existing task doc being updated.
   - When creating a new task, identify prior numbering and ensure a unique two-digit prefix.
2. Draft the document following exact sections: metadata block, Objective, Prerequisites / Dependencies, Implementation Steps, Validation, Completion Criteria, Notes / Follow-ups.
3. Reference existing code or documentation by linking relative paths rather than duplicating large excerpts.
4. Confirm acceptance criteria reflect the latest repository state (tests, tooling, env requirements).
5. Save the file under the correct directory (`docs/planned/` or `docs/completed/`) with the naming convention `NN-task-name.md`.
6. Run required validators (lint/tests) if file changes mandate repository updates; record commands executed.
7. Summarize the edits in the PR/task notes.

## Verification
- Ensure the new/updated doc passes markdown lint (if configured) and adheres to `docs/DOC_TEMPLATE.md` structure.
- Confirm numbering sequence remains unique.
