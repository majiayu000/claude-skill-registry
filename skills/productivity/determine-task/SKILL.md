---
name: determine-task
description: Determine current task from state files and git context
allowed-tools: Bash, Read
---

# Task Determination

Analyze session state to determine what task to work on.

## Execution

Run the task determiner agent:

```bash
./agents/task-determiner.sh
```

## Analysis Performed

1. **Git History** - Recent commits, uncommitted changes
2. **Progress File** - `claude-progress.txt` if present (harness pattern)
3. **Branch Name** - Extract hints from feature/*, fix/*, claude/* branches
4. **Tasks File** - `.contextium/tasks.json` for explicit task list

## Task Selection Logic

1. Find first task with status != "completed"
2. Consider task dependencies
3. Update `.contextium/tasks.json` with current task

## Output

```
=== RECOMMENDED TASK ===
Task: <task-id>
Reason: <selection rationale>
Prerequisites: <any setup needed>
Scope: <files/modules in scope>
========================
```

## Creating Tasks

If no tasks exist, create them:

```bash
# Edit tasks.json directly or use the task management skill
cat > .contextium/tasks.json << 'EOF'
{
  "version": "1.0.0",
  "tasks": [
    {
      "id": "implement-feature-x",
      "description": "Implement feature X",
      "status": "pending",
      "priority": "high",
      "scope": ["src/features/x/*"]
    }
  ],
  "current": null,
  "history": []
}
EOF
```
