---
name: faion-execute-task
description: "Execute specific SDD task via faion-task-executor-agent agent. Loads context, runs agent, moves task through lifecycle."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, TodoWrite
---

# SDD Execute Task Skill

**Communication with user: User's language. Code/commits: English.**

## Purpose

Execute a single SDD task using the `faion-task-executor-agent` agent.

## Input

- `project`: Project name (e.g., "qcdoc")
- `feature`: Feature name (e.g., "01-auth")
- `task_name`: Task identifier (e.g., "TASK_001" or partial match)

## Workflow

```
1. Parse project, feature, task_name
   ↓
2. Find task file in todo/ or in-progress/
   ↓
3. Load SDD context (constitution, spec, design, impl-plan)
   ↓
4. Call faion-task-executor-agent agent
   ↓
5. Report results
```

## Task Resolution

Search order:
1. `tasks/in-progress/TASK_*{name}*.md`
2. `tasks/todo/TASK_*{name}*.md`

Partial match supported: "TASK_001", "001", "models"

## Context Loading

Load these files for agent context:
```
aidocs/sdd/{project}/constitution.md
aidocs/sdd/{project}/features/{status}/{feature}/spec.md
aidocs/sdd/{project}/features/{status}/{feature}/design.md
aidocs/sdd/{project}/features/{status}/{feature}/implementation-plan.md
{task_file}
```

## Agent Invocation

```python
Task(
    subagent_type="faion-task-executor-agent",
    description=f"Execute {task_name}",
    prompt=f"""
PROJECT: {project}
FEATURE: {feature}
TASK_FILE: {task_path}

SDD CONTEXT:
- Constitution: {constitution_content}
- Spec: {spec_content}
- Design: {design_content}
- Implementation Plan: {impl_plan_content}

TASK CONTENT:
{task_content}

EXECUTION STEPS:
1. Move task to in-progress/ (if in todo/)
2. Deep research - understand codebase context
3. Plan subtasks using TodoWrite
4. Execute implementation
5. Quality checks (tests, linting)
6. Commit with message: "TASK_XXX: {description}"
7. Move task to done/
"""
)
```

## Output Format

```markdown
## Task Execution: {TASK_NAME}

**Status:** ✅ SUCCESS | ❌ FAILED | ⚠️ BLOCKED

### Summary
{what was done}

### Files Changed
- {file1}: {change description}
- {file2}: {change description}

### Commit
{commit_hash}: {commit_message}

### Notes
{any issues or blockers}
```

## Error Handling

| Error | Action |
|-------|--------|
| Task not found | List available tasks, ask user |
| Context missing | Warn, continue with available context |
| Execution failed | Report error, keep task in in-progress |
| Tests failed | Document failures, don't move to done |
