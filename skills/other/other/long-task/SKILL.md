---
name: long-task
description: Initialize or resume a long-running task session. Use when starting a complex multi-session task, resuming work from a previous session, or when the user mentions claude-progress.json or long-running work.
execution: direct
---

# Long Task Management

Mind-powered persistence for tasks that span multiple sessions.

## Quick Commands

- `/long-task` - Show active task or start new one
- `/long-task status` - Show current task status
- `/long-task complete` - Mark task as completed

## Starting a Task

When starting a long-running task:

```
Use long_task_start with:
- task_id: unique identifier (e.g., "implement-feature-x")
- goal: clear description of what you're trying to achieve
- hard_checks: deterministic completion criteria (optional)
- soft_checks: semantic completion criteria (optional)
```

## How It Works

1. **SessionStart**: If active task exists, context auto-injects
2. **During work**: Log significant events with `long_task_event`
3. **Stop hook**: Automatically logs checkpoint and increments iteration
4. **Completion**: Mark with `[TASK_COMPLETE]` or call `long_task_complete`

## MCP Tools

| Tool | Purpose |
|------|---------|
| `long_task_start` | Start a new long-running task |
| `long_task_get` | Get task details by ID |
| `long_task_active` | Get active task for realm |
| `long_task_update` | Update progress (completed_summary, work_items, blockers) |
| `long_task_complete` | Mark task as completed |
| `long_task_event` | Log event (decision, error, checkpoint) |
| `long_task_snapshot` | Get synthesized context |
| `long_task_evaluate` | Check completion criteria |

## Process

### If no arguments (show status or start)

1. Check for active task with `long_task_active`
2. If found: show snapshot with `long_task_snapshot`
3. If not found: ask user for task goal and start new task

### If "status" argument

1. Get active task with `long_task_active`
2. Show detailed snapshot with mode="debug"

### If "complete" argument

1. Get active task
2. Ask for outcome summary
3. Call `long_task_complete`

## Example Usage

**Start a task:**
```
/long-task
> No active task. What's your goal?
> Implement the authentication system

Starting task: implement-auth
Goal: Implement the authentication system
```

**Check status:**
```
/long-task status
[LONG_TASK:implement-auth] Implement the authentication system
Iteration: 3 | Status: active
Done: Added login form, API endpoints
Pending: Add password reset; Add OAuth
```

**Complete task:**
```
/long-task complete
Outcome: Authentication system fully implemented with login, logout, and OAuth

Completed task: implement-auth
```

## Completion Markers

The Stop hook detects these markers to auto-complete:
- `[TASK_COMPLETE]`
- `[DONE]`
- `<promise>COMPLETE</promise>`

## Multi-Agent Support

Tasks support lease-based coordination:
- `task_claim`: Claim task with lease
- `task_heartbeat`: Extend lease
- Expired leases allow other agents to take over
