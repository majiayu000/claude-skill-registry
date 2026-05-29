---
name: gobby-tasks
description: This skill should be used when the user asks to "/gobby-tasks", "task management", "create task", "list tasks", "close task". Manage gobby tasks - create, list, close, expand, validate, dependencies, and orchestration.
version: "2.0"
---

# /gobby-tasks - Task Management Skill

This skill manages tasks via the gobby-tasks MCP server. Parse the user's input to determine which subcommand to execute.

## Session Context

**IMPORTANT**: Pass your `session_id` from SessionStart context when creating or closing tasks for tracking:
```
session_id: fd59c8fc-...
```

## Task ID Formats

Tasks can be referenced by:
- `#N` - Short number (e.g., `#1`, `#47`)
- `path` - Hierarchical path (e.g., `1.2.3`)
- `UUID` - Full task ID

## Core Subcommands

### `/gobby-tasks create <title>` - Create a new task
Call `gobby-tasks.create_task` with:
- `title`: (required) The task title
- `session_id`: (required) Your session ID from SessionStart context
- `description`: Detailed description
- `task_type`: "task" (default), "bug", "feature", or "epic"
- `priority`: 1=High, 2=Medium (default), 3=Low
- `parent_task_id`: Optional parent task
- `blocks`: List of task IDs this task blocks
- `labels`: List of labels
- `test_strategy`: "manual", "automated", or "none"
- `validation_criteria`: Acceptance criteria

Example: `/gobby-tasks create Fix login button` → `create_task(title="Fix login button", session_id="<your_session_id>")`
Example: `/gobby-tasks create Add OAuth support --type=feature` → `create_task(title="Add OAuth support", task_type="feature", session_id="<your_session_id>")`

### `/gobby-tasks show <task-id>` - Show task details
Call `gobby-tasks.get_task` with:
- `task_id`: (required) Task reference

Displays full task details including description, status, validation criteria, dependencies.

Example: `/gobby-tasks show #1` → `get_task(task_id="#1")`

### `/gobby-tasks update <task-id>` - Update task fields
Call `gobby-tasks.update_task` with:
- `task_id`: (required) Task reference
- `title`, `description`, `status`, `priority`, `assignee`, `labels`, `validation_criteria`, `test_strategy`, etc.

Example: `/gobby-tasks update #1 status=in_progress` → `update_task(task_id="#1", status="in_progress")`

### `/gobby-tasks list [status]` - List tasks
Call `gobby-tasks.list_tasks` with:
- `status`: Filter (open, in_progress, review, closed, or comma-separated)
- `priority`: Filter by priority
- `task_type`: Filter by type
- `assignee`: Filter by assignee
- `label`: Filter by label
- `parent_task_id`: Filter by parent
- `title_like`: Fuzzy title match
- `limit`: Max results (default 50)
- `all_projects`: List from all projects

Example: `/gobby-tasks list` → `list_tasks(status="open")`
Example: `/gobby-tasks list in_progress` → `list_tasks(status="in_progress")`

### `/gobby-tasks close <task-id>` - Close a task
Call `gobby-tasks.close_task` with:
- `task_id`: (required) Task reference
- `reason`: "completed" (default), "duplicate", "already_implemented", "wont_fix", "obsolete"
- `changes_summary`: Summary of changes (triggers validation)
- `commit_sha`: Git commit SHA to link
- `skip_validation`: Skip LLM validation (requires justification)
- `override_justification`: Why skipping validation/commit
- `no_commit_needed`: Only for non-code tasks (requires justification)
- `session_id`: Your session ID for tracking

**IMPORTANT**: Commit changes first, then close with commit SHA.

**Review routing**: Tasks may route to `review` status instead of `closed` when:
- Task has `requires_user_review=true`, OR
- `override_justification` is provided

Returns `routed_to_review: true` if task was sent to review instead of closed.

Example: `/gobby-tasks close #1` → First commit, then `close_task(task_id="#1", commit_sha="<sha>")`

### `/gobby-tasks reopen <task-id>` - Reopen a closed or review task
Call `gobby-tasks.reopen_task` with:
- `task_id`: (required) Task reference
- `append_description`: Additional context for reopening

Works on both `closed` and `review` status tasks. Resets `accepted_by_user` to false.

Example: `/gobby-tasks reopen #1` → `reopen_task(task_id="#1")`

### `/gobby-tasks delete <task-id>` - Delete a task
Call `gobby-tasks.delete_task` with:
- `task_id`: (required) Task reference

Deletes the task and all subtasks.

Example: `/gobby-tasks delete #1` → `delete_task(task_id="#1")`

## Expansion & Planning

### `/gobby-tasks expand <task-id>` - Expand into subtasks
Call `gobby-tasks.expand_task` with:
- `task_id`: (required) Task to expand
- `context`: Additional context for expansion
- `enable_web_research`: Use web for research
- `enable_code_context`: Include code context
- `generate_validation`: Generate criteria for subtasks
- `session_id`: Your session ID

Example: `/gobby-tasks expand #1` → `expand_task(task_id="#1")`

### `/gobby-tasks suggest` - Suggest next task
Call `gobby-tasks.suggest_next_task` with:
- `task_type`: Optional type filter
- `prefer_subtasks`: Prefer leaf tasks (default true)
- `parent_id`: Scope to specific epic/feature hierarchy

Returns the highest-priority ready task.

Example: `/gobby-tasks suggest` → `suggest_next_task()`

### `/gobby-tasks ready` - List ready tasks
Call `gobby-tasks.list_ready_tasks` with:
- `priority`, `task_type`, `assignee`, `parent_task_id`, `limit`

Lists tasks with no blocking dependencies.

Example: `/gobby-tasks ready` → `list_ready_tasks()`

### `/gobby-tasks blocked` - List blocked tasks
Call `gobby-tasks.list_blocked_tasks` to see tasks waiting on dependencies.

## Dependencies

### `/gobby-tasks depend <task> <blocker>` - Add dependency
Call `gobby-tasks.add_dependency` with:
- `task_id`: (required) The dependent task
- `depends_on`: (required) The blocker task
- `dep_type`: "blocks" (default), "discovered-from", or "related"

Example: `/gobby-tasks depend #2 #1` → `add_dependency(task_id="#2", depends_on="#1")`

### `/gobby-tasks undepend <task> <blocker>` - Remove dependency
Call `gobby-tasks.remove_dependency`

### `/gobby-tasks deps <task-id>` - Show dependency tree
Call `gobby-tasks.get_dependency_tree`

### `/gobby-tasks check-cycles` - Detect circular dependencies
Call `gobby-tasks.check_dependency_cycles`

## Validation

### `/gobby-tasks validate <task-id>` - Validate completion
Call `gobby-tasks.validate_task` with:
- `task_id`: (required) Task to validate
- `changes_summary`: Summary of changes
- `context_files`: Relevant files to check

Auto-gathers context from commits if not provided.

Example: `/gobby-tasks validate #1` → `validate_task(task_id="#1")`

### `/gobby-tasks validation-status <task-id>` - Get validation details
Call `gobby-tasks.get_validation_status`

### `/gobby-tasks validation-history <task-id>` - Get validation history
Call `gobby-tasks.get_validation_history`

### `/gobby-tasks generate-criteria <task-id>` - Generate validation criteria
Call `gobby-tasks.generate_validation_criteria`

### `/gobby-tasks fix <task-id>` - Run fix attempt
Call `gobby-tasks.run_fix_attempt` to spawn a fix agent for validation issues.

### `/gobby-tasks validate-fix <task-id>` - Validate with auto-fix
Call `gobby-tasks.validate_and_fix` for validation loop with automatic fixes.

## Labels

### `/gobby-tasks label <task-id> <label>` - Add label
Call `gobby-tasks.add_label`

### `/gobby-tasks unlabel <task-id> <label>` - Remove label
Call `gobby-tasks.remove_label`

## Git Integration

### `/gobby-tasks link-commit <task-id> <sha>` - Link commit
Call `gobby-tasks.link_commit`

### `/gobby-tasks unlink-commit <task-id> <sha>` - Unlink commit
Call `gobby-tasks.unlink_commit`

### `/gobby-tasks auto-link` - Auto-link commits
Call `gobby-tasks.auto_link_commits` to find commits mentioning task IDs.

### `/gobby-tasks diff <task-id>` - Get task diff
Call `gobby-tasks.get_task_diff`

## Orchestration

### `/gobby-tasks orchestrate <parent-id>` - Spawn agents for ready tasks
Call `gobby-tasks.orchestrate_ready_tasks`

### `/gobby-tasks orchestration-status <parent-id>` - Get orchestration status
Call `gobby-tasks.get_orchestration_status`

### `/gobby-tasks poll-agents` - Poll agent status
Call `gobby-tasks.poll_agent_status`

## Sync

### `/gobby-tasks sync` - Trigger sync
Call `gobby-tasks.sync_tasks`

### `/gobby-tasks sync-status` - Get sync status
Call `gobby-tasks.get_sync_status`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For create: Show the new task ID and title
- For list: Table with ID, title, status, priority
- For show: All task fields in readable format
- For close: Confirm closure with task ID
- For expand: List created subtasks
- For suggest: Show suggested task with reasoning
- For validate: Validation result (pass/fail) with feedback

## Error Handling

If the subcommand is not recognized, show available subcommands:
- create, show, update, list, close, reopen, delete
- expand, suggest, ready, blocked
- depend, undepend, deps, check-cycles
- validate, validation-status, validation-history, generate-criteria, fix, validate-fix
- label, unlabel
- link-commit, unlink-commit, auto-link, diff
- orchestrate, orchestration-status, poll-agents
- sync, sync-status
