---
name: ralph-status
description: Monitor all active Ralph Wiggum agents and their progress. Shows iteration counts, gate status, and blocked tasks.
triggers:
  - /ralph.status
  - agent status
  - check agents
---

# /ralph.status

Display status of all active agents and their progress.

## Process

1. **Read manifest.json**
   ```bash
   cat .ralph/manifest.json
   ```

2. **Check each worktree status**
   - Read `.agent/plan.json` for iteration and gate results
   - Read `.agent/activity.md` for recent activity
   - Check git status for uncommitted changes

3. **Query Linear for current state**
   - Verify task statuses match manifest

4. **Compile and display status**

## Output Format

```
RALPH WIGGUM STATUS - floe

Active Agents: 4/5
Completed Today: 12 tasks
Average Duration: 42 minutes

+----------+--------+-------+--------+-------------+
| Task     | Agent  | Iter  | Status | Last Update |
+----------+--------+-------+--------+-------------+
| T001     | WK-001 | 5/15  | lint   | 2 min ago   |
| T003     | WK-002 | 3/15  | test   | 1 min ago   |
| T005     | WK-003 | 8/15  | sec    | 30s ago     |
| T007     | WK-004 | 1/15  | impl   | 5s ago      |
+----------+--------+-------+--------+-------------+

Blocked: 1 (T002 - waiting for human input)
Queued: 8 tasks ready after current wave

Wave Progress:
  Wave 1: [T001, T003, T005] - 2/3 complete
  Wave 2: [T002, T004, T007] - 0/3 complete (waiting)
  Wave 3: [T008] - blocked on Wave 1+2

Recent Activity:
- 14:32 T006 COMPLETE (7 iterations, 38 min)
- 14:15 T004 COMPLETE (4 iterations, 22 min)
- 13:58 T002 BLOCKED (security finding needs review)
```

## Status Codes

| Status | Meaning |
|--------|---------|
| `impl` | Implementing current subtask |
| `lint` | Running ruff check |
| `type` | Running mypy --strict |
| `test` | Running pytest |
| `sec` | Running /security-review |
| `const` | Validating constitution |
| `commit` | Creating git commit |
| `COMPLETE` | All subtasks passed |
| `BLOCKED` | Needs human intervention |

## Detailed Agent View

To see details for a specific agent:

```bash
# Read plan.json
cat ../floe-agent-ep001-auth/.agent/plan.json

# Read recent activity
tail -50 ../floe-agent-ep001-auth/.agent/activity.md

# Check git status
cd ../floe-agent-ep001-auth && git log --oneline -5
```

## Statistics

The manifest tracks:
- `total_tasks_completed` - Lifetime count
- `average_duration_minutes` - Rolling average
- `completed_today` - Today's completions with details

## Notifications

| Event | Action |
|-------|--------|
| Task complete | Update manifest, Linear comment |
| Task blocked | Alert in status, Linear comment |
| All complete | Signal READY_FOR_REVIEW |
| Stale agent | Warn (no commits in 24h) |

## Related Commands

- `/ralph.spawn` - Start agents for an epic
- `/ralph.integrate` - Prepare for PR
- `/ralph.cleanup` - Remove worktrees
- `/ralph.preflight` - Check service health
- `/ralph.resume` - Resume from saved session
- `/ralph.memory-status` - Check memory buffer status
