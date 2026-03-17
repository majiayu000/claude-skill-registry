---
name: learning-agents
description: Dispatch entry point for the LearningAgents plugin. Routes to sub-commands for creating agents, running learning cycles, and reporting issues.
---

# LearningAgents

Manage auto-improving AI sub-agents that learn from their mistakes across sessions.

## Arguments

`$ARGUMENTS` is the text after `/learning-agents` (e.g., for `/learning-agents create foo`, `$ARGUMENTS` is `create foo`).

## Setup Check

Before routing, check if `.claude/session_log_folder_info.md` exists. If it does **not** exist, run `Skill learning-agents:setup` first, then continue with routing below.

Only perform this check once per session — after the setup skill completes (or if the file already exists), proceed directly to routing for all subsequent invocations.

## Routing

Split `$ARGUMENTS` on the first whitespace. The first token is the sub-command (case-insensitive); the remainder is passed to the sub-skill. Accept both underscores and dashes in sub-command names (e.g., `report_issue` and `report-issue` are equivalent).

### `create <name>`

Create a new LearningAgent scaffold.

Invoke: `Skill learning-agents:create-agent <name>`

Example: `$ARGUMENTS = "create rails-activejob"` → `Skill learning-agents:create-agent rails-activejob`

### `learn`

Run the learning cycle on all pending session transcripts. Any arguments after `learn` are ignored.

Invoke: `Skill learning-agents:learn`

### `report_issue <agentId> <details>`

Report an issue with a LearningAgent from the current session.

Invoke: `Skill learning-agents:report-issue <session_log_folder> <details>`

To construct the session log folder path: search `.deepwork/tmp/agent_sessions/` for a subdirectory whose name contains the provided `agentId`. The path structure is `.deepwork/tmp/agent_sessions/<session_id>/<agentId>/`. If no match is found, inform the user. If multiple matches exist, use the most recently modified one.

Example: `$ARGUMENTS = "report_issue abc123 Used wrong retry strategy"` → find folder matching `abc123` under `.deepwork/tmp/agent_sessions/`, then `Skill learning-agents:report-issue .deepwork/tmp/agent_sessions/sess-xyz/abc123/ Used wrong retry strategy`

### No arguments or ambiguous input

Display available sub-commands:

```
LearningAgents - Auto-improving AI sub-agents

Available commands:
  /learning-agents create <name>                    Create a new LearningAgent
  /learning-agents learn                            Run learning cycle on pending sessions
  /learning-agents report_issue <agentId> <details>      Report an issue with an agent

Examples:
  /learning-agents create rails-activejob
  /learning-agents learn
  /learning-agents report_issue abc123 "Used wrong retry strategy for background jobs"
```

## Guardrails

- Always route to the appropriate skill — do NOT implement sub-command logic inline
- If `$ARGUMENTS` doesn't match any known sub-command, show the help text above
- Pass arguments through to sub-skills exactly as provided
