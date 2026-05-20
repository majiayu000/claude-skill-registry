---
name: skill-orchestrator
description: Route commands to appropriate workflows based on task language and status. Invoke when executing /task, /research, /plan, /implement commands.
allowed-tools: Read, Glob, Grep, Task
# Context loaded on-demand via @-references (see Context Loading section)
---

# Orchestrator Skill

Central routing intelligence for the task management system.

## Context Loading

Load context on-demand when needed:
- `@.claude/context/core/orchestration/orchestration-core.md` - Routing, delegation, session tracking
- `@.claude/context/core/orchestration/state-management.md` - Task lookup and status validation
- `@.claude/context/index.md` - Full context discovery index

## Trigger Conditions

This skill activates when:
- A slash command needs language-based routing
- Task context needs to be gathered before delegation
- Multi-step workflows require coordination

## Core Responsibilities

### 1. Task Lookup

Given a task number, retrieve full context:
```
1. Read specs/state.json
2. Find task by project_number
3. Extract: language, status, project_name, description, priority
4. Read TODO.md for additional context if needed
```

### 2. Language-Based Routing

Route to appropriate skill based on task language:

| Language | Research Skill | Implementation Skill |
|----------|---------------|---------------------|
| neovim | skill-neovim-research | skill-neovim-implementation |
| latex | skill-researcher | skill-latex-implementation |
| typst | skill-researcher | skill-typst-implementation |
| general | skill-researcher | skill-implementer |
| meta | skill-researcher | skill-implementer |
| markdown | skill-researcher | skill-implementer |

### 3. Status Validation

Before routing, validate task status allows the operation:

| Operation | Allowed Statuses |
|-----------|------------------|
| research | not_started, planned, partial, blocked |
| plan | not_started, researched, partial |
| implement | planned, implementing, partial, researched |
| revise | planned, implementing, partial, blocked |

### 4. Context Preparation

Prepare context package for delegated skill:
```json
{
  "task_number": 259,
  "task_name": "task_slug",
  "language": "neovim",
  "status": "planned",
  "description": "Full task description",
  "artifacts": {
    "research": ["path/to/research.md"],
    "plan": "path/to/plan.md"
  },
  "focus_prompt": "Optional user-provided focus"
}
```

## Execution Flow

```
1. Receive command context (task number, operation type)
2. Lookup task in state.json
3. Validate status for operation
4. Determine target skill by language
5. Prepare context package
6. Invoke target skill via Task tool
7. Receive and validate result
8. Return result to caller
```

## Return Format

```json
{
  "status": "completed|partial|failed",
  "routed_to": "skill-name",
  "task_number": 259,
  "result": {
    "artifacts": [],
    "summary": "..."
  }
}
```

## Error Handling

- Task not found: Return clear error with suggestions
- Invalid status: Return error with current status and allowed operations
- Skill invocation failure: Return partial result with error details
