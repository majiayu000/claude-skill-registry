---
name: loom-team-lifecycle-management
description: Manage Loom team worker lifecycle from spawn to retire, including ticket assignment, progress tracking, merge operations, and workspace cleanup.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T12:18:15.163Z"
  updated_at: "2026-01-29T12:18:15.163Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Manage complete Loom team worker lifecycle: spawn, assign tickets, track progress, handle merges, retire workers.

# When To Use
- You are a team manager for a Loom team (e.g., MiyagiDo)
- Need to manage multiple workers in parallel
- Workers are implementing tickets in isolated worktrees
- Team commands are available

# Preconditions
- Loom team initialized: `loom team init <TEAM>`
- Ticket system initialized: `loom ticket init`
- Workers available to spawn

# Procedure

## 1. Spawn Workers for Tickets
- `loom team spawn <TEAM> <TICKET_ID>`
- Workers handle their own worktree creation
- Monitor team status: `loom team status <TEAM>`

## 2. Track Worker Progress
- Regularly check: `loom team inbox <TEAM> list --to manager --unacked`
- Capture worker output when needed: `loom team capture <TEAM> <WORKER_ID>`
- Acknowledge messages: `loom team inbox <TEAM> ack <MESSAGE_ID>`

## 3. Handle Ready for Review
- When worker sends READY_FOR_REVIEW:
  - Add manager review note: `loom ticket add-note <id> 'Manager review: ...'
  - Enqueue to merge queue: `loom team merge <TEAM> enqueue --ticket <id> --branch <branch> --from-worker <worker>`
  - Close ticket: `loom ticket close <id>` (if approval is straightforward)

## 4. Monitor Merge Queue
- Check merge status: `loom team merge <TEAM> list`
- When merge completes, acknowledge message from merge worker

## 5. Ship Changes
- When all tickets merged to merge-queue: `loom team ship <TEAM>`
- This merges merge-queue to main branch

## 6. Retire Workers
- `loom team retire <TEAM> <WORKER_ID>`
- If retirement fails with workspace cleanup error:
  - Check worker worktree status: `git status` in worktree
  - May need to handle cleanup manually

## 7. Worker Communication
- Send encouragement and next-step guidance via `loom team send <TEAM> <WORKER_ID> 'message'`
- Workers should be informed of successful merges and retirement

# Best Practices
- Spawn workers in priority order (P1 before P2)
- Verify ticket completion before enqueue (check code files exist)
- Keep merge queue clear after shipping
- Document blockers in ticket notes

# Gotchas
- Workers may mark tickets complete before actual code exists
- Workspace cleanup can fail with modified/untracked files
- Merge conflicts require resolution in merge worker worktree
- Ship may be NOOP if changes already in main

# Examples

### Complete Phase 3 P1 tickets:
```
# 1. Spawn workers
loom team spawn MiyagiDo vp-cf95  # Orchestration engine
loom team spawn MiyagiDo vp-6cf1  # CLI
loom team spawn MiyagiDo vp-7d49  # Scheduling

# 2. Wait for completion
loom team inbox MiyagiDo list --to manager --unacked

# 3. Approve and enqueue
loom team merge MiyagiDo enqueue --ticket vp-cf95 --branch team/vp-cf95 --from-worker w2
loom team merge MiyagiDo enqueue --ticket vp-6cf1 --branch team/vp-6cf1 --from-worker w1

# 4. Ship
loom team ship MiyagiDo

# 5. Retire
loom team retire MiyagiDo w2
loom team retire MiyagiDo w1
```

### Handle workspace cleanup failure:
```
# Error: contains modified or untracked files
# Solution:
loom team send MiyagiDo w2 'Please clean up your worktree before retirement'
# Or manually check and cleanup
git status .team/runs/MiyagiDo/worktrees/vp-cf95
```
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
