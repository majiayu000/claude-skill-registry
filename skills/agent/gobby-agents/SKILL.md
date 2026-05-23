---
name: gobby-agents
description: This skill should be used when the user asks to "/gobby-agents", "spawn agent", "start agent", "list agents". Manage subagent spawning - start, cancel, list, and check results of autonomous agents.
---

# /gobby-agents - Agent Management Skill

This skill manages subagent spawning via the gobby-agents MCP server. Parse the user's input to determine which subcommand to execute.

## Session Context

**IMPORTANT**: Use the `session_id` from your SessionStart hook context for agent calls. Look for it in your system context:
```
session_id: fd59c8fc-...
```

## Subcommands

### `/gobby-agents start <prompt>` - Start a new agent
Call `gobby-agents.start_agent` with:
- `prompt`: (required) Task description for the agent
- `mode`: Execution mode - "terminal" (default), "headless", or "embedded"
- `workflow`: Optional workflow to activate (plan-execute, test-driven, etc.)
- `agent`: Named agent definition to use (e.g., "validation-runner")
- `session_context`: Context injection sources
- `task`: Task ID to associate with the agent
- `terminal`: Terminal type for terminal mode
- `provider`: LLM provider override
- `model`: Model override
- `worktree_id`: Run in specific worktree
- `timeout`: Max runtime
- `max_turns`: Max conversation turns
- `parent_session_id`: Parent session for tracking

Modes:
- `terminal` - Opens in new terminal window (default)
- `headless` - Runs in background, no UI
- `embedded` - Runs in current process

Example: `/gobby-agents start Implement the login feature`
→ `start_agent(prompt="Implement the login feature")`

Example: `/gobby-agents start --headless Fix all type errors`
→ `start_agent(prompt="Fix all type errors", mode="headless")`

### `/gobby-agents result <run-id>` - Get agent result
Call `gobby-agents.get_agent_result` with:
- `run_id`: (required) The agent run ID

Returns the result of a completed agent run.

Example: `/gobby-agents result run-abc123` → `get_agent_result(run_id="run-abc123")`

### `/gobby-agents cancel <run-id>` - Cancel a running agent
Call `gobby-agents.cancel_agent` with:
- `run_id`: (required) The agent run ID to cancel

Example: `/gobby-agents cancel run-abc123` → `cancel_agent(run_id="run-abc123")`

### `/gobby-agents list` - List agent runs for a session
Call `gobby-agents.list_agents` with:
- `parent_session_id`: (required) Session ID to list agents for
- `status`: Optional filter (running, completed, cancelled)
- `limit`: Max results

Returns agents with run ID, status, prompt summary, and runtime.

Example: `/gobby-agents list` → `list_agents(parent_session_id="<session_id>")`
Example: `/gobby-agents list running` → `list_agents(parent_session_id="<session_id>", status="running")`

### `/gobby-agents running` - List currently running agents
Call `gobby-agents.list_running_agents` with:
- `parent_session_id`: Optional filter by parent session
- `mode`: Optional filter by mode

Returns in-memory process state for running agents.

Example: `/gobby-agents running` → `list_running_agents()`

### `/gobby-agents can-spawn` - Check if agent can be spawned
Call `gobby-agents.can_spawn_agent` with:
- `parent_session_id`: (required) Session ID to check

Checks agent depth limit to prevent infinite spawning.

Example: `/gobby-agents can-spawn` → `can_spawn_agent(parent_session_id="<session_id>")`

### `/gobby-agents stats` - Get running agent statistics
Call `gobby-agents.running_agent_stats` to get statistics about running agents.

Example: `/gobby-agents stats` → `running_agent_stats()`

## Response Format

After executing the appropriate MCP tool, present the results clearly:
- For start: Show run ID, mode, and initial status
- For result: Show agent output and completion status
- For cancel: Confirm agent cancelled
- For list: Table with run ID, status, prompt, duration
- For running: Show active processes
- For can-spawn: Show yes/no with depth info
- For stats: Show running agent statistics

## Agent Safety

- Agent depth is limited (default 3) to prevent infinite spawning
- Each workflow step restricts available tools
- Parent session context is injected automatically
- Use `can_spawn_agent` to check before spawning

## Error Handling

If the subcommand is not recognized, show available subcommands:
- start, result, cancel, list, running, can-spawn, stats
