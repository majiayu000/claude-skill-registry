---
name: ticket-board
description: Add ticket to project board and set status, priority, size.
---

# Ticket Board

The Orchestrator drives this workflow. Add a ticket to the project board and set or update board-specific fields: status, priority, and size.

**Prerequisites:** Ticket number, desired field values.

---

## Board Configuration

Read `workspace.config.yaml` for all field IDs and option IDs:

- `board.project_id` — project to add the issue to
- `board.fields.status.field_id` — status field
- `board.fields.priority.field_id` — priority field
- `board.fields.size.field_id` — size field

### Status Options

| Status      | Config Key                         |
| ----------- | ---------------------------------- |
| Backlog     | `board.status_options.backlog`     |
| Ready       | `board.status_options.ready`       |
| In Progress | `board.status_options.in-progress` |
| In Review   | `board.status_options.in-review`   |
| Done        | `board.status_options.done`        |

### Priority Options

| Priority | Config Key                  |
| -------- | --------------------------- |
| P0       | `board.priority_options.p0` |
| P1       | `board.priority_options.p1` |
| P2       | `board.priority_options.p2` |

### Size Options

| Size | Config Key              |
| ---- | ----------------------- |
| XS   | `board.size_options.xs` |
| S    | `board.size_options.s`  |
| M    | `board.size_options.m`  |
| L    | `board.size_options.l`  |
| XL   | `board.size_options.xl` |

---

## Steps

1. Read `workspace.config.yaml` for board field IDs and option IDs
2. Check if the issue is already on the board
3. If not on board: add the issue to the project using `board.project_id`
4. Set or update the requested fields using the field IDs and option IDs from config
5. Report the changes

### Output

```
## Context Anchors

- **Issue:** #<number> - <title>

## Board Updated

- **On board:** <added | already present>
- **Status:** <status value set>
- **Priority:** <priority value set>
- **Size:** <size value set>

## Next Step

Board fields updated.

**Approval Required:** No
```

---

## Error Handling

| Error                  | Recovery                                            |
| ---------------------- | --------------------------------------------------- |
| Issue not found        | Verify the issue number                             |
| Issue not on board     | Add to board first, then set fields                 |
| Field ID not in config | Check workspace.config.yaml for correct field IDs   |
| Option ID not found    | List available options from config, ask user to map |
