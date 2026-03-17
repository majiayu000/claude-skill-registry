---
name: move-prd
description: Move a PRD between lifecycle stages (inbox/active/completed/archived)
---

# Move PRD Skill

Move a PRD between lifecycle stages, updating all references.

## Arguments

The user provides:

- PRD number or path
- Target stage: `inbox`, `active`, `completed`, or `archived`

If not given, ask which PRD and target stage.

## Lifecycle Stages

| Stage     | Directory         | Status Value |
| --------- | ----------------- | ------------ |
| Unstarted | `wiki/inbox/`     | Draft        |
| Active    | `wiki/active/`    | In Progress  |
| Done      | `wiki/completed/` | Completed    |
| Abandoned | `wiki/archived/`  | Archived     |

## Workflow

1. **Locate PRD**: Find the current file location
2. **Validate transition**: Check the transition makes sense:
   - `inbox` → `active` (starting work)
   - `active` → `completed` (all tasks done, criteria met)
   - `active` → `archived` (abandoned/superseded)
   - `completed` → `archived` (superseded by new work)
   - `inbox` → `archived` (decided not to pursue)
3. **Move file**: Use `git mv` from repo root
   ```bash
   git mv wiki/{source}/prd-NNN-slug.md wiki/{target}/prd-NNN-slug.md
   ```
4. **Update PRD metadata**: Change the `Status` field in the PRD header
5. **Update status.md**: Update the Status and Location columns in the inventory table
6. **Add progress log entry**: Append to the Progress Log table in `wiki/status.md`

## Status.md Updates

### Inventory Table

Change the row for this PRD:

```markdown
| PRD-NNN | [Title]({new-stage}/prd-NNN-slug.md) | {New Status} | ... | `wiki/{new-stage}/` |
```

### Progress Log

Add a new row:

```markdown
| YYYY-MM-DD | PRD-NNN moved to {stage} | — |
```

## Important Notes

- `git mv` must be run from the repo root directory
- Always update BOTH the PRD file AND `wiki/status.md`
- When moving to `completed`, suggest running `/check-prd` first to verify success criteria
- When moving to `active`, check that dependencies (other PRDs) are completed
