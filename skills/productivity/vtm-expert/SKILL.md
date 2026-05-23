---
name: vtm-expert
description: |
  Virtual Task Manager domain expert.

  Knows about:
  - Next, Context, Task, Start, Complete, Stats, List operations

  Use when:
  - User asks about task management operations
  - Context needed before starting work
  - Reviewing task status
  - Managing task workflow

trigger_phrases:
  - "what should i work on"
  - "next task"
  - "show my tasks"
  - "task status"
  - "vtm status"
  - "get context for task"
  - "start task"
  - "complete task"
  - "mark task done"
  - "task stats"
  - "list tasks"
---

# VTM Expert Skill

## What This Skill Does

Helps you manage your Virtual Task Manager workflow with smart command suggestions.

Auto-discovers when you mention task-related work and suggests the appropriate VTM command.

## Available Commands

- `/vtm:next` - Get next ready task to work on
- `/vtm:context` - Generate minimal context for a specific task
- `/vtm:task` - View details of a specific task
- `/vtm:start` - Mark a task as in-progress
- `/vtm:complete` - Mark a task as completed
- `/vtm:stats` - Show VTM statistics and progress
- `/vtm:list` - List all tasks with their status

## When Claude Uses This

When you mention things like:

- "What should I work on?" → Suggests `/vtm:next`
- "I need context for TASK-003" → Suggests `/vtm:context TASK-003`
- "Show me task status" → Suggests `/vtm:stats` or `/vtm:list`
- "Start working on TASK-005" → Suggests `/vtm:start TASK-005`
- "Mark TASK-003 as done" → Suggests `/vtm:complete TASK-003`
- "How many tasks are left?" → Suggests `/vtm:stats`

## VTM Workflow

The typical VTM workflow:

1. **Find work**: `/vtm:next` - Shows ready tasks (dependencies met)
2. **Get context**: `/vtm:context TASK-XXX` - Token-efficient task context
3. **Start task**: `/vtm:start TASK-XXX` - Mark as in-progress
4. **Implement**: Use PROMPT 2 with TDD based on test_strategy
5. **Complete**: `/vtm:complete TASK-XXX` - Mark as done, unblocks dependents
6. **Repeat**: Back to step 1

## Token Efficiency

VTM achieves 99% token reduction by:

- Surgical access to specific tasks (not loading entire manifest)
- Dependency resolution built-in
- Two context modes: minimal (~2000 tokens) and compact (~500 tokens)
- No need to load related specs unless specifically needed

## Best Practices

1. **Before starting**: Run `/vtm:next` to see what's ready
2. **Get context first**: Always use `/vtm:context` before implementing
3. **Follow TDD**: Respect the task's `test_strategy` field
4. **Track progress**: Use `/vtm:stats` to monitor overall progress
5. **Update status**: Mark tasks in-progress and completed for accurate tracking

## Integration

Works seamlessly with other Claude Code domains:

- Can be invoked manually: `/vtm:operation`
- Auto-triggered by Claude based on conversation
- Integrates with git hooks for validation
- Supports team workflows via shared vtm.json

## Customization

Edit trigger phrases in the frontmatter above to match your vocabulary.

**Examples:**

- Add project-specific terms: "backlog item", "sprint task"
- Add abbreviations: "ctx" for context, "nxt" for next
- Add workflow terms: "pick up task", "finish task"

## Technical Details

**Architecture:**

- Commands wrap the vtm CLI (npm package)
- Requires vtm.json in project root
- Atomic writes with automatic stats recalculation
- Dependency validation built-in

**Data Flow:**

```
User phrase → Skill triggers → Command suggested →
User approves → vtm CLI executes → Stats auto-update
```

## See Also

- Design spec: `.claude/designs/vtm.json`
- Commands: `.claude/commands/vtm/`
- Prompts: `prompts/1-generate-vtm.md`, `prompts/2-execute-task.md`, `prompts/3-add-feature.md`
