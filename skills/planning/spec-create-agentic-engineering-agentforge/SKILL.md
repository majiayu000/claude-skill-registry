---
name: spec-create
description: Create a new numbered spec file from the template with auto-incremented SPEC-NNN numbering
argument-hint: "[spec title]"
---

You are creating a new spec file for the AgentForge project using auto-incremented numbering.

Follow these steps:

**Step 1: Find the current highest spec number**

List `specs/active/` sorted, and find files matching `SPEC-NNN-*.md`. Identify the highest NNN. If none exist, start at SPEC-001.

**Step 2: Determine the new spec number**

Increment the highest found number by 1 (e.g., if SPEC-024 is highest, the new spec is SPEC-025). Zero-pad to 3 digits.

**Step 3: Get the spec title**

If the user provided a title as an argument, use it. Otherwise ask:
> "What is the title for this new spec?"

Convert the title to kebab-case for the filename (e.g., "API Key Rotation" → `api-key-rotation`).

**Step 4: Copy the template**

Copy `specs/template.md` to:
```
specs/active/SPEC-NNN-<kebab-case-title>.md
```

**Step 5: Fill in the template header**

In the new spec file, replace:
- The spec number placeholder → `SPEC-NNN`
- The title placeholder → the actual title
- Both date fields → today's date (YYYY-MM-DD)

Leave all other sections for the user to fill in.

**Step 6: Report**

Tell the user:
- The path of the new spec file
- The spec number assigned
- Which sections to fill in next (Overview, Problem Statement, Goals, Proposed Solution)
- Reminder: per CLAUDE.md Rule 2 (SpecSafe-First), write tests before implementing
