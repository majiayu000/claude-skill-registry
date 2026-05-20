---
name: work-status
description: Shows WORK progress and TASK status. Use when the user asks about WORK list, WORK progress, TASK status, or pipeline status (e.g., "WORK list", "WORK-01 progress", "show status").
---

# WORK Status

Check and report the current status of WORKs and TASKs.

## How to Check

1. Read `works/WORK-LIST.md` for the master index of all WORKs
2. For a specific WORK, read `works/WORK-NN/PROGRESS.md` for TASK-level progress
3. For a specific TASK, read `works/WORK-NN/TASK-NN_result.md` for completion details

## Status Values

| Status | Meaning |
|--------|---------|
| `IN_PROGRESS` | WORK created, TASKs being executed |
| `DONE` | All TASKs committed — committer auto-sets on last TASK |
| `COMPLETED` | Archived to `_COMPLETED/` — set during push |

## Display Format

```
WORK Status
  WORK-01: User Authentication    ✅ 5/5 completed
  WORK-02: Payment Integration    🔄 2/4 in progress
  WORK-03: Admin Dashboard        ⬜ 0/6 pending
```

## Arguments

Query: $ARGUMENTS
