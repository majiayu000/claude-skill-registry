---
name: create-plan
description: Create markdown plan documents with clear steps, status tracking, and progress percentage. Use when the user asks to create a plan, write a plan document, or structure implementation steps with tracking.
---

# Plan Creation Stage

Based on our full exchange, produce a markdown plan document.

## Requirements for the plan

- Include clear, minimal, concise steps.
- Track the status of each step using these emojis:
  - 🟩 Done
  - 🟨 In Progress
  - 🟥 To Do
- Include dynamic tracking of overall progress percentage (at top).
- Do NOT add extra scope or unnecessary complexity beyond explicitly clarified details.
- Steps should be modular, elegant, minimal, and integrate seamlessly within the existing codebase.

## File Location and Naming

- Save the plan in a `plans/` directory at the repository root.
- Use a numeric prefix counter in the filename to ensure plans appear in creation order.
- Format: `plans/XXX-plan-name.md` where `XXX` is a zero-padded 3-digit number (e.g., `001`, `002`, `003`).
- To determine the next number:
  1. List existing files in `plans/` directory
  2. Find the highest numbered prefix
  3. Use the next sequential number
  4. If no plans exist, start with `001`
- Example filenames:
  - `plans/001-feature-implementation.md`
  - `plans/002-api-refactor.md`
  - `plans/003-database-migration.md`

## Markdown Template

Use this template structure:

```markdown
# Feature Implementation Plan

**Overall Progress:** `0%`

## TLDR
Short summary of what we're building and why.

## Critical Decisions
Key architectural/implementation choices made during exploration:
- Decision 1: [choice] - [brief rationale]
- Decision 2: [choice] - [brief rationale]

## Tasks:

- [ ] 🟥 **Step 1: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

- [ ] 🟥 **Step 2: [Name]**
  - [ ] 🟥 Subtask 1
  - [ ] 🟥 Subtask 2

...
```

## Progress Calculation

Calculate overall progress percentage based on completed steps:
- Count total steps (including subtasks)
- Count completed steps (🟩 status)
- Percentage = (completed / total) × 100
- Round to nearest whole number
- Update the progress percentage at the top when creating or updating the plan

## Status Updates

When updating plan status:
- Change emoji from 🟥 → 🟨 → 🟩 as work progresses
- Update checkbox state: `- [ ]` for incomplete, `- [x]` for complete
- Recalculate and update overall progress percentage
- Keep status consistent across the document

## Important Notes

- This is a planning stage—do not start implementation yet
- Focus only on what was explicitly discussed
- Avoid adding extra features or complexity
- Keep steps atomic and testable
- Ensure steps can be completed independently where possible
- Maintain the existing codebase structure and patterns
