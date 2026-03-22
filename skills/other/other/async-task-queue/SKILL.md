---
name: vibe-async-task-queue
description: Provides a persistent cross-session task queue for work that should be done but isn't blocking current tasks. Enables background and future-session work tracking.
user-invocable: true
---

# vibe-async-task-queue

Not everything needs to be done right now. But "I'll do it later" only works if "later" actually happens.

## When to Use This Skill

- You identify work that should be done but isn't blocking the current task
- During code review, you find issues that aren't urgent
- Tests reveal non-critical flakiness
- Documentation needs updating but not right now
- "TODO" comments that should become tracked tasks

## When NOT to Use This Skill

- Blocking work that must be done now
- Tasks already tracked in an issue tracker (GitHub Issues, Jira, etc.)
- One-off tasks in the current session (just do them)

## Queue Format

Tasks are stored in a JSON file at a project-specific location (e.g., `.claude/task-queue.json`):

```json
{
  "tasks": [
    {
      "id": "vibe-001",
      "created": "2026-02-28",
      "priority": "medium",
      "status": "pending",
      "description": "Add error handling to parseConfig edge cases",
      "target_files": ["internal/config/parser.go"],
      "acceptance": "go test ./internal/config/... -run TestParseConfigEdge -v passes",
      "context": "Discovered during fuzz testing session"
    }
  ]
}
```

## Steps

### Adding a Task
1. Identify the work
2. Write a clear description with:
   - What needs to be done
   - Which files are affected
   - How to verify it's done (acceptance command)
   - Why it was deferred (context)
3. Append to queue file

### Processing the Queue
1. Read queue file
2. Pick highest-priority pending task
3. Set status to `in_progress`
4. Do the work
5. Run acceptance test
6. If pass: set status to `completed`, commit
7. If fail: set status to `pending`, add notes about what went wrong

### Reviewing the Queue
List all tasks with status counts. Identify stale tasks (>7 days pending).

## Output Format

### Task Queue Status

**Pending**: X | **In Progress**: Y | **Completed**: Z | **Failed**: W

| ID | Priority | Description | Age | Status |
|----|----------|------------|-----|--------|
| vibe-001 | high | Add auth token refresh | 2d | pending |
| vibe-002 | medium | Fix flaky test in utils | 5d | pending |

### Stale Tasks (>7 days)
- [task IDs that need attention or should be closed]
