---
name: ralph-resume
description: Resume a PAUSED Ralph session — retry failed task, skip, or abort
disable-model-invocation: true
---

# Ralph Resume

Resume a Ralph autonomous execution session that was paused by the circuit breaker.

## Pre-Flight

1. **Check for active session:**
   ```bash
   if [[ ! -d ".ralph-session" ]]; then
     echo "No Ralph session found. Nothing to resume."
     exit
   fi
   ```

2. **Read circuit breaker state:**
   ```bash
   .claude/hooks/circuit-breaker.sh status
   ```

3. **Show session summary:**
   ```bash
   python3 -c "
   import json
   cb = json.load(open('.ralph-session/circuit-breaker.json'))
   print(f\"Session state: {cb.get('state')}\")
   print(f\"Pause reason: {cb.get('pause_reason', 'none')}\")
   print(f\"Tasks completed: {cb.get('tasks_completed', 0)}\")
   print(f\"Total iterations: {cb.get('total_iterations', 0)}\")
   print(f\"Consecutive failures: {cb.get('consecutive_failures', 0)}\")
   "
   ```

4. **Identify the failed/current task:**
   Check beads for tasks still in `in_progress` status.

## Present Options

Ask the user:
1. **Retry** — Reset circuit breaker to RUNNING, re-dispatch the failed task
2. **Skip** — Mark the failed task as blocked with reason, move to next task
3. **Abort** — Clean up session, leave remaining tasks as pending

## Execute Choice

### Option 1: Retry
```bash
.claude/hooks/circuit-breaker.sh clear-degraded  # or reset if PAUSED
.claude/hooks/circuit-breaker.sh reset
```
Then re-enter the ralph-execute loop from the current task.

### Option 2: Skip
```bash
bd update <task-id> -s blocked --append-notes "Skipped during Ralph resume — failed after max attempts"
.claude/hooks/circuit-breaker.sh reset
```
Then continue ralph-execute with `bd ready --parent <epic-id>`.

### Option 3: Abort
```bash
rm -rf .ralph-session
curl -s -X POST "https://ntfy.sh/property-tracker-claude" \
  -d "Ralph session aborted by user" -H "Title: Ralph Aborted"
```

## Integration

This skill is suggested by `session-start.sh` when it detects an active Ralph session.
After choosing retry or skip, invoke `/ralph-execute <epic-id>` to continue the loop.
