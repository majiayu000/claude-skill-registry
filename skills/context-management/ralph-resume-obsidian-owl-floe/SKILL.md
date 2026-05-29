---
name: ralph-resume
description: Resume from saved session state after interruption or compaction. Recovers context from checkpoints and agent-memory.
triggers:
  - /ralph.resume
  - resume session
  - recover session
---

# /ralph.resume [--session SESSION_ID]

Resume a workflow session from saved state.

## When to Use

- After fixing a BLOCKED pre-flight check
- After Claude Code context compaction
- After session interruption
- To continue from a specific checkpoint

## Process

1. **Check for Active Session**

   ```bash
   cat .ralph/session/current.json 2>/dev/null
   ```

   If exists, shows session details and asks to resume.

2. **Query Agent-Memory for Context** (if Cognee available)

   ```
   Search agent-memory for:
   "session context for {work_area}"
   ```

   Retrieve:
   - Prior decisions made during session
   - Task states and progress
   - Implementation context

3. **Load Local Checkpoint** (fallback)

   ```bash
   ls -la .ralph/session/checkpoints/
   # Find most recent checkpoint
   cat .ralph/session/checkpoints/{session_id}-{checkpoint_num}.json
   ```

4. **Restore State**

   - Load active task list from checkpoint
   - Restore Linear issue states
   - Resume from last completed subtask

5. **Run Pre-Flight Check**

   ```
   /ralph.preflight
   ```

   Must PASS before resuming work.

6. **Continue Workflow**

   Resume from the interrupted step.

## Output

```
RALPH WIGGUM SESSION RESUME
===========================

Session ID: session-2026-01-16-abc123
Started: 2026-01-16T10:30:00Z
Last checkpoint: 2026-01-16T11:45:00Z (iteration 8)

Prior Context Loaded:
  - 5 decisions recovered from agent-memory
  - 3 active tasks in progress
  - 12 subtasks completed

Active Tasks:
  T001 (auth): Iteration 8/15, subtask 3 of 5
  T003 (catalog): Iteration 5/15, subtask 2 of 4
  T005 (tests): COMPLETE

Pre-flight: PASS

Resuming from iteration 8...
```

## Recovery Without Cognee

If agent-memory is unavailable, local checkpoints are used:

```
RALPH WIGGUM SESSION RESUME
===========================

Session ID: session-2026-01-16-abc123

[WARN] Agent-memory unavailable - using local checkpoint only
       Some decision context may be missing

Checkpoint loaded: .ralph/session/checkpoints/session-2026-01-16-abc123-5.json
  - Last checkpoint: 2026-01-16T11:45:00Z
  - Active tasks: 3
  - Iteration: 8

Pre-flight: PASS (with warnings)
  [??] cognee: Using local buffer

Resuming from checkpoint...
```

## Session File Format

`.ralph/session/current.json`:

```json
{
  "session_id": "session-2026-01-16-abc123",
  "started_at": "2026-01-16T10:30:00Z",
  "work_area": "feature/ep001-auth",
  "epic": "EP001",
  "active_tasks": ["T001", "T003", "T005"],
  "last_checkpoint": 5,
  "status": "interrupted"
}
```

## Checkpoint Format

`.ralph/session/checkpoints/{session_id}-{num}.json`:

```json
{
  "checkpoint_id": "session-2026-01-16-abc123-5",
  "created_at": "2026-01-16T11:45:00Z",
  "iteration": 8,
  "active_tasks": {
    "T001": {"status": "in_progress", "subtask": 3, "passes": ["T001.1", "T001.2"]},
    "T003": {"status": "in_progress", "subtask": 2, "passes": ["T003.1"]},
    "T005": {"status": "complete", "subtask": 4, "passes": ["T005.1", "T005.2", "T005.3", "T005.4"]}
  },
  "decisions": [
    {"decision": "Use polling instead of sleep", "task_id": "T001", "timestamp": "..."},
    {"decision": "Add retry logic for catalog", "task_id": "T003", "timestamp": "..."}
  ]
}
```

## Manual Session Selection

If multiple sessions exist:

```bash
/ralph.resume --session session-2026-01-15-xyz789
```

Or list available sessions:

```bash
ls .ralph/session/checkpoints/ | cut -d'-' -f1-5 | sort -u
```

## Session Cleanup

After successful workflow completion:

```bash
# Archive completed session
mv .ralph/session/current.json .ralph/session/recovery/
rm .ralph/session/checkpoints/session-2026-01-16-abc123-*.json
```

## Configuration

From `.ralph/config.yaml`:

```yaml
resilience:
  checkpoints:
    session_ttl_hours: 48      # Retain session data
    max_checkpoints: 10        # Keep last 10 per session
  recovery:
    auto_save_on_block: true   # Save on BLOCKED signal
    auto_save_on_error: true   # Save on unexpected errors
```

## Related Commands

- `/ralph.preflight` - Check services before resume
- `/ralph.memory-sync` - Sync any buffered memories
- `/ralph.status` - Check current agent status
