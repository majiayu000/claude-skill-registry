---
name: loom-ticketing
description: Use loom ticket for ticket creation, status updates, deps, and notes.
license: MIT
compatibility: opencode
metadata:
  created_at: "2026-01-27T17:03:09.731823+00:00"
  updated_at: "2026-01-27T17:03:09.731823+00:00"
  version: "1"
  tags: "tickets,workflow"
---

<!-- BEGIN:compound:skill-managed -->
## Canonical commands

Initialize (creates `.tickets/`):

- `compound_ticket(argv=["init"])`

Create:

- `compound_ticket(argv=["create", "Add foo support", "-p", "2", "-t", "task", "--tags", "foo,bar"])`

List / view:

- `compound_ticket(argv=["list"])`
- `compound_ticket(argv=["ready"])`
- `compound_ticket(argv=["show", "<id>"])`

Update:

- `compound_ticket(argv=["update", "<id>", "--status", "in_progress"])`
- `compound_ticket(argv=["update", "<id>", "--status", "closed"])`

Notes:

- `compound_ticket(argv=["add-note", "<id>", "Found X. Fixed by Y."])`

Dependencies:

- `compound_ticket(argv=["dep", "<id>"])`
- `compound_ticket(argv=["dep-add", "<id>", "<dep-id>"])`
- `compound_ticket(argv=["dep-rm", "<id>", "<dep-id>"])`

## Best practices

- One “epic” ticket per feature, with task tickets beneath.
- Record decisions and gotchas as notes, not in your head.
- Use deps to make sequencing explicit (and reviewable).
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
