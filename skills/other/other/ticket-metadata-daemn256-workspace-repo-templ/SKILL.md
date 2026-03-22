---
name: ticket-metadata
description: Set or update ticket labels, milestone, and assignee
---

# Ticket Metadata

Uses **Orchestrator** for ticket lifecycle. Set or update the metadata fields on an existing ticket: labels, milestone, and assignee.

**Prerequisites:** Ticket number, desired field values

---

## Steps

1. Read the current issue metadata via the forge's read operation
2. Determine which fields need updating
3. Present the proposed changes for approval — show current vs. proposed for each field

### Label Taxonomy

| Category | Purpose       | Examples                                     |
| -------- | ------------- | -------------------------------------------- |
| `type:`  | Work type     | `type:feature`, `type:bug`, `type:docs`      |
| `area:`  | Codebase area | `area:api`, `area:ui`, `area:core`           |
| `topic:` | Cross-cutting | `topic:auth`, `topic:perf`, `topic:security` |

### ⛔ CHECKPOINT

**STOP.** Await approval of metadata changes.

4. Execute the forge's issue edit operation for each changed field

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>

## Updated

- **Fields changed:** <list of fields modified>

## Next Step

Ticket metadata updated.

**Approval Required:** No
```

---

## Error Handling

| Error             | Recovery                                           |
| ----------------- | -------------------------------------------------- |
| Issue not found   | Verify the issue number                            |
| Label not found   | List available labels on the repo, suggest closest |
| Milestone unknown | List open milestones, ask user to select           |
