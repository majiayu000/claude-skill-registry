---
name: faion-do-all-tasks
description: "Execute all SDD tasks for a feature sequentially. Handles task ordering, continues on minor failures, stops on critical issues."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite, AskUserQuestion
---

# SDD Do All Tasks Skill

**Communication with user: User's language. Code/commits: English.**

## Purpose

Execute all tasks for a feature in sequence, with intelligent failure handling.

## Input

- `project`: Project name
- `feature`: Feature name

## Workflow

```
1. Parse project, feature
   ↓
2. Find all tasks (in-progress first, then todo, sorted)
   ↓
3. Load SDD context
   ↓
4. Clarify ambiguities BEFORE execution
   ↓
5. Create feature branch (optional)
   ↓
6. Execute each task via faion-execute-task skill
   ↓
7. Run post-execution review (faion-tasks-reviewer-agent)
   ↓
8. Quality checks (tests, lint)
   ↓
9. Report summary
```

## Task Discovery

```bash
# Priority order
1. tasks/in-progress/TASK_*.md  # Resume first
2. tasks/todo/TASK_*.md         # Then new tasks

# Sort by task number
TASK_001, TASK_002, TASK_003...
```

## Pre-Execution Clarification

Before starting, review all tasks for:
- Ambiguous requirements
- Missing dependencies
- Unclear acceptance criteria

Use AskUserQuestion if clarification needed.

## Execution Loop

```python
for task in sorted_tasks:
    result = Skill(
        skill="faion-execute-task",
        args=f"{project}/{feature} {task.name}"
    )

    if result.status == "BLOCKED":
        if is_critical(result.error):
            STOP  # Git conflict, build broken, security
        else:
            CONTINUE  # Test failures, minor issues

    log_result(result)
```

## Continue vs Stop Rules

**Continue if:**
- Single task fails (document and continue)
- Test failures (log for later fix)
- Minor code style issues
- Non-blocking warnings

**Stop if:**
- Git merge conflict
- Build completely broken
- Security vulnerability detected
- User requests stop

## Post-Execution Review

```python
Task(
    subagent_type="faion-tasks-reviewer-agent",
    prompt=f"Review completed tasks for {project}/{feature}"
)
```

## Output Format

```markdown
## Feature Execution: {project}/{feature}

### Summary
- **Tasks:** {completed}/{total}
- **Status:** ✅ Complete | ⚠️ Partial | ❌ Failed
- **Duration:** {time}

### Task Results
| Task | Status | Commit | Notes |
|------|--------|--------|-------|
| TASK_001 | ✅ | abc123 | |
| TASK_002 | ✅ | def456 | |
| TASK_003 | ⚠️ | - | Tests failing |

### Quality Report
- Tests: {pass}/{total}
- Lint: {status}

### Next Steps
{recommendations}
```

## Agents Used

| Agent | Purpose |
|-------|---------|
| faion-task-executor-agent | Individual task execution |
| faion-tasks-reviewer-agent | Post-execution review |
