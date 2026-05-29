---
name: gobby-worktrees
description: This skill should be used when the user asks to "/gobby-worktrees", "create worktree", "spawn in worktree". Manage git worktrees for parallel development - create, list, spawn agents, sync, and cleanup.
---

# /gobby-worktrees - Worktree Management Skill

This skill manages git worktrees via the gobby-worktrees MCP server. Parse the user's input to determine which subcommand to execute.

## Subcommands

### `/gobby-worktrees create <branch-name>` - Create a new worktree
Call `gobby-worktrees.create_worktree` with:
- `branch_name`: (required) Name for the new branch
- `base_branch`: Base branch (default: current)
- `task_id`: Optional task ID to associate
- `worktree_path`: Custom worktree path
- `create_branch`: Create new branch (default true)
- `project_path`: Project path
- `provider`: LLM provider

Creates an isolated git worktree for parallel development.

Example: `/gobby-worktrees create feature/auth`
→ `create_worktree(branch_name="feature/auth")`

Example: `/gobby-worktrees create feature/auth --task #1`
→ `create_worktree(branch_name="feature/auth", task_id="#1")`

### `/gobby-worktrees show <worktree-id>` - Show worktree details
Call `gobby-worktrees.get_worktree` with:
- `worktree_id`: (required) Worktree ID

Returns worktree details including path, branch, status, and linked task.

Example: `/gobby-worktrees show wt-abc123` → `get_worktree(worktree_id="wt-abc123")`

### `/gobby-worktrees list` - List all worktrees
Call `gobby-worktrees.list_worktrees` with:
- `status`: Filter by status (active, stale, merged, abandoned)
- `agent_session_id`: Filter by agent session
- `limit`: Max results

Returns worktrees with path, branch, status, and associated task.

Example: `/gobby-worktrees list` → `list_worktrees()`
Example: `/gobby-worktrees list active` → `list_worktrees(status="active")`

### `/gobby-worktrees spawn <branch-name> <prompt>` - Spawn agent in new worktree
Call `gobby-worktrees.spawn_agent_in_worktree` with:
- `prompt`: (required) Task description for the agent
- `branch_name`: (required) Name for the new branch
- `base_branch`: Base branch
- `task_id`: Optional task ID
- `parent_session_id`: Parent session for tracking
- `mode`: Agent mode (terminal, headless)
- `terminal`: Terminal type
- `provider`: LLM provider
- `model`: Model override
- `workflow`: Workflow to activate
- `timeout`: Max runtime
- `max_turns`: Max conversation turns
- `project_path`: Project path

Creates worktree + spawns agent in one call.

Example: `/gobby-worktrees spawn feature/auth Implement OAuth login`
→ `spawn_agent_in_worktree(branch_name="feature/auth", prompt="Implement OAuth login")`

### `/gobby-worktrees delete <worktree-id>` - Delete a worktree
Call `gobby-worktrees.delete_worktree` with:
- `worktree_id`: (required) Worktree ID
- `force`: Force deletion

Deletes both git worktree and database record.

Example: `/gobby-worktrees delete wt-abc123` → `delete_worktree(worktree_id="wt-abc123")`

### `/gobby-worktrees sync <worktree-id>` - Sync with main branch
Call `gobby-worktrees.sync_worktree` with:
- `worktree_id`: (required) Worktree ID
- `strategy`: Sync strategy (merge, rebase)

Syncs the worktree with the main branch.

Example: `/gobby-worktrees sync wt-abc123` → `sync_worktree(worktree_id="wt-abc123")`

### `/gobby-worktrees claim <worktree-id>` - Claim worktree ownership
Call `gobby-worktrees.claim_worktree` to claim a worktree for an agent session.

### `/gobby-worktrees release <worktree-id>` - Release worktree ownership
Call `gobby-worktrees.release_worktree` to release ownership.

### `/gobby-worktrees mark-merged <worktree-id>` - Mark as merged
Call `gobby-worktrees.mark_worktree_merged` to mark a worktree as merged (ready for cleanup).

### `/gobby-worktrees detect-stale` - Find stale worktrees
Call `gobby-worktrees.detect_stale_worktrees` to find worktrees with no recent activity.

### `/gobby-worktrees cleanup` - Clean up stale worktrees
Call `gobby-worktrees.cleanup_stale_worktrees` with:
- `hours`: Hours of inactivity (default varies)
- `dry_run`: Preview without deleting
- `delete_git`: Also delete git worktree
- `project_path`: Project path

Marks and optionally deletes stale worktrees.

Example: `/gobby-worktrees cleanup` → `cleanup_stale_worktrees()`
Example: `/gobby-worktrees cleanup --dry-run` → `cleanup_stale_worktrees(dry_run="true")`

### `/gobby-worktrees stats` - Get worktree statistics
Call `gobby-worktrees.get_worktree_stats` for project worktree statistics.

Example: `/gobby-worktrees stats` → `get_worktree_stats()`

### `/gobby-worktrees by-task <task-id>` - Get worktree for task
Call `gobby-worktrees.get_worktree_by_task` with:
- Task ID

Finds the worktree linked to a specific task.

Example: `/gobby-worktrees by-task #1` → `get_worktree_by_task(...)`

### `/gobby-worktrees link <worktree-id> <task-id>` - Link task to worktree
Call `gobby-worktrees.link_task_to_worktree` to link a task to an existing worktree.

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For create: Show worktree path, branch name, and status
- For show: Full worktree details
- For list: Table with branch, path, status, task ID
- For spawn: Show worktree + agent creation confirmation
- For delete: Confirm deletion
- For sync: Show sync result
- For cleanup: Summary of affected worktrees
- For stats: Worktree statistics

## Worktree Lifecycle

1. `active` - Currently in use
2. `stale` - No recent activity
3. `merged` - Branch merged to main
4. `abandoned` - Manually marked for cleanup

## Error Handling

If the subcommand is not recognized, show available subcommands:
- create, show, list, spawn, delete, sync
- claim, release, mark-merged
- detect-stale, cleanup, stats
- by-task, link
