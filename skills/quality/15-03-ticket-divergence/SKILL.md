---
name: 15-03-ticket-divergence
description: Audit open and in-progress tickets against actual codebase state, closing stale or completed tickets.
---

# 15.03 Ticket Divergence Audit

## Instructions

Use subtask agents to explore the current state of tickets (`open` and `in_progress`) and what is actually in the codebase.

- If code shows work done but ticket is open → `close ticket`
- If code is in progress → mark ticket as `in_progress` with a note why assumed to be in progress currently
- If ticket is completely indecipherable in terms of what it should mean → mark `closed`
