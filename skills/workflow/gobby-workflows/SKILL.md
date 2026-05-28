---
name: gobby-workflows
description: This skill should be used when the user asks to "/gobby-workflows", "activate workflow", "workflow status". Manage step-based workflows - activate, deactivate, check status, and list available workflows.
---

# /gobby-workflows - Workflow Management Skill

This skill manages step-based workflows via the gobby-workflows MCP server. Parse the user's input to determine which subcommand to execute.

## Session Context

**IMPORTANT**: Use the `session_id` from your SessionStart hook context (injected at session start) for all workflow calls. Look for it in your system context - it looks like:
```
session_id: fd59c8fc-...
```

Do NOT call `list_sessions` to look it up - you already have it.

## Subcommands

### `/gobby-workflows activate <workflow-name>` - Activate a workflow
Call `gobby-workflows.activate_workflow` with:
- `session_id`: **Required** - from your SessionStart context
- `name`: The workflow name to activate
- `variables`: Optional initial variables (e.g., `session_task` for auto-task)
- `initial_step`: Optional starting step (defaults to first step)

Available workflows:
- `auto-task` - Task execution with session_task variable
- `plan-execute` - Planning then execution phases
- `test-driven` - TDD: Red → Green → Refactor
- `plan-act-reflect` - Structured development cycle
- `react` - Reason-Act continuous loop

Example: `/gobby-workflows activate plan-execute`
→ `activate_workflow(session_id="<from context>", name="plan-execute")`

Example: `/gobby-workflows activate auto-task session_task=gt-abc123`
→ `activate_workflow(session_id="<from context>", name="auto-task", variables={"session_task": "gt-abc123"})`

### `/gobby-workflows deactivate` - Deactivate current workflow
Call `gobby-workflows.end_workflow` with:
- `session_id`: **Required** - from your SessionStart context

Example: `/gobby-workflows deactivate`
→ `end_workflow(session_id="<from context>")`

### `/gobby-workflows status` - Show current workflow status
Call `gobby-workflows.get_workflow_status` with:
- `session_id`: **Required** - from your SessionStart context

Returns:
- Active workflow name (if any)
- Current step
- Available transitions
- Session variables

Example: `/gobby-workflows status`
→ `get_workflow_status(session_id="<from context>")`

### `/gobby-workflows list` - List available workflows
Call `gobby-workflows.list_workflows` to see all available workflows:
- Built-in workflows (global)
- Project-specific workflows (.gobby/workflows/)
- Workflow descriptions and step counts

Example: `/gobby-workflows list` → `list_workflows()`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For activate: Confirm activation with workflow name and starting step
- For deactivate: Confirm deactivation
- For status: Show current state, step, and available actions
- For list: Display workflows with name, description, and type (step/stepped)

## Workflow Concepts

- **Steps**: Named states with allowed tools and transitions
- **Variables**: Session-scoped key-value storage (e.g., `session_task`)
- **Transitions**: Move between steps based on conditions
- **Tool filtering**: Each step restricts which tools are available

## Error Handling

If the subcommand is not recognized, show available subcommands:
- activate, deactivate, status, list
