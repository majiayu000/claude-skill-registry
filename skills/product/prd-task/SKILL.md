---
name: prd-task
description: Convert a Beads PRD markdown file to executable JSON tasks for autonomous execution. Use after writing `.beads/artifacts/<bead-id>/prd.md`.
references:
  - references/prd-schema.json
---

# PRD Task Skill (Beads-Native)

Convert a markdown PRD into executable JSON format for autonomous task completion.

The PRD defines the **end state** via tasks with verification steps. The agent decides HOW to get there.

## Beads-Native File Locations (Recommended)

This template uses Beads artifacts (no `.opencode/state`).

```
.beads/artifacts/<bead-id>/
├── prd.md         # PRD created by `prd` skill
├── prd.json       # Generated task list with passes field
└── progress.txt   # Cross-iteration memory (append-only)
```

## Workflow

1. Input: bead id (`bd-...`).
2. Read `.beads/artifacts/<bead-id>/prd.md`.
3. Extract tasks from `## Tasks`.
4. Write `.beads/artifacts/<bead-id>/prd.json`.
5. Ensure `.beads/artifacts/<bead-id>/progress.txt` exists (create if missing).

## Input Format

`prd-task` expects a `## Tasks` section with tasks of the form:

```markdown
## Tasks

### User Registration [functional]

User can register with email and password.

**Verification:**

- POST /api/auth/register with valid email/password
- Verify 201 response with user object
- Attempt duplicate email, verify 409
```

## Output Format

Write JSON to `.beads/artifacts/<bead-id>/prd.json`.

```json
{
  "beadId": "bd-...",
  "prdName": "<optional-slug>",
  "tasks": [
    {
      "id": "functional-1",
      "category": "functional",
      "description": "User can register with email and password",
      "steps": [
        "POST /api/auth/register with valid email/password",
        "Verify 201 response with user object",
        "Attempt duplicate email, verify 409"
      ],
      "passes": false
    }
  ]
}
```

## Task Schema

See `references/prd-schema.json`.

## Conversion Rules

### Tasks from Markdown

- Each `### Title [category]` becomes a task
- Generate `id` as `<category>-<number>` (e.g., `api-1`, `db-2`) or a descriptive slug
- Text after title becomes `description`
- Items under `**Verification:**` become `steps`
- `passes` always starts `false`

### Steps Are Verification

Steps must be written as **verification steps**, not implementation instructions.

Bad: "Add a controller and write a service"
Good: "POST /api/foo returns 201" / "bun test passes"

## Progress File

If `.beads/artifacts/<bead-id>/progress.txt` does not exist, create it with:

```markdown
# Progress Log

Bead: <bead-id>
Started: <YYYY-MM-DD>

## Codebase Patterns

<!-- Consolidate reusable patterns here -->

---

<!-- Task logs below - APPEND ONLY -->
```

## After Conversion

Tell the user:

```
PRD converted:
  - .beads/artifacts/<bead-id>/prd.md
  - .beads/artifacts/<bead-id>/prd.json
  - .beads/artifacts/<bead-id>/progress.txt

Next:
  /start <bead-id>
  /complete-next-task <bead-id>
```
