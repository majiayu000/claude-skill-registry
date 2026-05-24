---
name: loom-team-manager
description: Act as Team Manager for Loom team, handling ticket workflow when team commands may be unavailable
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T10:20:06.334Z"
  updated_at: "2026-01-29T10:20:06.334Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# When To Use
- User role is 'Team Manager' for a Loom team (e.g., MiyagiDo)
- Need to manage tickets, track progress, and report status
- `loom team` commands may be blocked by permissions

# Preconditions
- Loom ticket system initialized (`loom ticket init`)
- `.tickets/` directory exists
- Team charter exists (`.team/runs/<TEAM>/CHARTER.md`)

# Procedure

## 1. Initial Assessment
- Review charter: `loom ticket show <ticket-id>` or read CHARTER.md
- List all tickets: `loom ticket list`
- Check current status distribution: `loom ticket list | grep -E 'in_progress|open|done|closed'`

## 2. Verify Completed Work
- For tickets marked 'ready to merge' or 'implementation complete':
  - Use glob to find expected code files (e.g., `src/**/*connector*.py`)
  - Use read to verify implementation details
  - Check commit history if ticket references commits
  - Add note if verification fails

## 3. Close Completed Tickets
- `loom ticket close <ticket-id>` for fully verified tickets
- Add review note before closing: `loom ticket add-note <id> 'Manager review: ...'
- **Always sync**: `loom ticket sync`

## 4. Track In-Progress Work
- Check in-progress tickets: `loom ticket show <id>`
- Look for implementation notes from workers
- Verify code files exist if marked complete
- Add manager review notes

## 5. Monitor New Tickets
- List tickets by status: `loom ticket list`
- Read new ticket details: `loom ticket show <id>`
- Note dependencies and sequencing
- Document patterns in ticket creation

## 6. Handle Team Command Blocker
- If `loom team *` commands fail with permission denied:
  - Document specific permission pattern (what's allowed vs denied)
  - Use `loom ticket *` commands as alternative workflow
  - Cannot: merge, enqueue, spawn workers, retire workers, ship
  - Can: close, add-note, list, show, sync

## 7. Report Status
- Summarize closed tickets
- Summarize in-progress tickets
- Summarize pending tickets by phase/priority
- Document blockers
- Sync all updates: `loom ticket sync`

# Examples

### Verify database connector implementation:
```
glob src/vibe_piper/connectors/*.py
# Returns: postgres.py, mysql.py, snowflake.py, bigquery.py
loom ticket close vp-0862
loom ticket sync
```

### Check ticket status:
```
loom ticket show vp-e2b5
loom ticket list
```

### Add review note:
```
loom ticket add-note vp-0862 "Verified code exists. 4 connectors implemented."
```

# Gotchas
- `loom team *` commands require separate permissions from `loom ticket *`
- Ticket sync commits changes; run after modifications
- Workers may mark tickets complete before actual code exists
- Branch references in tickets (e.g., `murmur/vp-0862`) cannot be merged without team commands
- Workers create tickets automatically; watch for Phase patterns

# Notes
- This skill assumes ticket management is primary deliverable when team commands blocked
- For full team orchestration, permissions must allow `loom team *`
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
