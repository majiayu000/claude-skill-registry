---
name: eywa
description: Multi-agent coordination, spatial memory, and swarm navigation. Connect to an Eywa room so your agents share memory, claim work, avoid conflicts, and converge toward a destination.
user-invocable: true
metadata:
  {
    "openclaw": {
      "emoji": "🌳",
      "requires": {
        "anyBins": ["curl", "wget"]
      },
      "homepage": "https://www.eywa-ai.dev",
      "install": [
        {
          "kind": "node",
          "package": "eywa-ai",
          "bins": ["eywa"],
          "label": "Install Eywa CLI"
        }
      ]
    }
  }
---

# Eywa: Multi-Agent Coordination Layer

You are now connected to Eywa, a coordination layer for agent swarms. Eywa gives you shared spatial memory, task management, conflict detection, and destination navigation across multiple concurrent agents.

## Setup

Your Eywa connection is configured via environment variables:

- `EYWA_ROOM` — the room slug (e.g. `demo`, `my-project`)
- `EYWA_AGENT` — your agent identity prefix (e.g. `openclaw`). The server appends a unique suffix like `/jade-dusk`.
- `EYWA_URL` — MCP endpoint (default: `https://eywa-mcp.armandsumo.workers.dev`)

The helper script at `{baseDir}/eywa-call.sh` handles all MCP communication.

## How to call Eywa tools

Use the `exec` tool to run the helper script:

```bash
bash {baseDir}/eywa-call.sh <tool_name> '<json_arguments>'
```

Examples:

```bash
# Start a session (always do this first)
bash {baseDir}/eywa-call.sh eywa_start '{"task_description":"Implementing user auth"}'

# Log an operation with semantic tags
bash {baseDir}/eywa-call.sh eywa_log '{"role":"assistant","content":"Added JWT middleware","system":"api","action":"create","scope":"auth service","outcome":"success"}'

# Check what other agents are doing
bash {baseDir}/eywa-call.sh eywa_status '{}'

# View the task queue
bash {baseDir}/eywa-call.sh eywa_tasks '{}'

# Claim a task
bash {baseDir}/eywa-call.sh eywa_pick_task '{"task_id":"<uuid>"}'

# Update task progress
bash {baseDir}/eywa-call.sh eywa_update_task '{"task_id":"<uuid>","status":"in_progress","notes":"Working on it"}'

# Store knowledge that persists across sessions
bash {baseDir}/eywa-call.sh eywa_learn '{"content":"Auth uses JWT with RS256, tokens expire in 1h","tags":["auth","api"],"title":"JWT auth pattern"}'

# Set the team destination
bash {baseDir}/eywa-call.sh eywa_destination '{"action":"set","destination":"Ship v1.0 with auth, billing, and dashboard","milestones":["Auth system","Billing integration","Dashboard MVP"]}'

# Mark session complete
bash {baseDir}/eywa-call.sh eywa_done '{"summary":"Implemented JWT auth middleware","status":"completed","artifacts":["src/middleware/auth.ts"],"tags":["auth","feature"]}'
```

## Available tools

### Session lifecycle
- **eywa_start** — Start a session. Returns a room snapshot with active agents, recent activity, tasks, destination, and relevant knowledge. Always call this first.
  - `task_description` (required): what you're working on
  - `continue_from` (optional): agent name to load context from (baton handoff)

- **eywa_done** — Mark session complete with structured summary.
  - `summary`, `status` (completed/blocked/failed/partial), `artifacts[]`, `tags[]`, `next_steps`

- **eywa_stop** — Quick session end with summary.

### Memory and logging
- **eywa_log** — Log an operation with semantic tags. Other agents and humans see what you're doing.
  - `role`, `content`, `system` (git/api/deploy/filesystem/etc.), `action` (read/write/create/deploy/test/etc.), `scope`, `outcome` (success/failure/blocked)

- **eywa_learn** — Store persistent knowledge (survives sessions).
  - `content`, `tags[]`, `title`

- **eywa_knowledge** — Retrieve the knowledge base.
  - `tag`, `search`, `limit`

- **eywa_search** — Search all messages by content.

### Tasks
- **eywa_tasks** — List tasks sorted by priority. Filter by status, assignee, milestone.
- **eywa_task** — Create a new task.
- **eywa_pick_task** — Claim an open task (sets status to claimed, creates work claim for conflict detection).
- **eywa_update_task** — Update status, add notes, reassign.
- **eywa_subtask** — Break a task into subtasks.

### Collaboration
- **eywa_status** — See all agents, their work, systems, curvature scores.
- **eywa_claim** — Declare your work scope and files. Triggers conflict detection.
- **eywa_context** — Get shared context from all agents.
- **eywa_msg** — Send a message to a specific agent or all.

### Navigation
- **eywa_destination** — Set, update, or view the team destination with milestones and progress tracking.

## Workflow

1. **Start**: Call `eywa_start` with what you're working on. Read the snapshot.
2. **Claim**: If picking up a task, call `eywa_pick_task`. Otherwise call `eywa_claim` with your scope.
3. **Work**: Do your work. Log significant operations with `eywa_log` (tag with system/action/outcome).
4. **Learn**: Store any knowledge worth keeping with `eywa_learn`.
5. **Done**: Call `eywa_done` with summary, status, artifacts, and next steps.

## When to log

| Event | system | action | outcome |
|-------|--------|--------|---------|
| Read a file | filesystem | read | success |
| Write/edit a file | filesystem | write | success |
| Create new file | filesystem | create | success |
| Run tests | ci | test | success/failure |
| Git commit | git | write | success |
| Git push | git | deploy | success/failure |
| Deploy to staging/prod | deploy | deploy | success/failure |
| API call | api | read/write | success/failure |
| Database migration | database | write | success/failure |
| Hit a blocker | (relevant) | (relevant) | blocked |

Log enough that another agent could understand what you did and continue your work.

## Key principles

- **Coordinate, don't duplicate**: Check `eywa_status` and `eywa_tasks` before starting work. If another agent is already on it, pick something else.
- **Log operations**: Every significant action should be tagged. Invisible agents have zero curvature.
- **Store knowledge**: If you discover something useful (a pattern, a gotcha, a convention), call `eywa_learn`. Future sessions benefit.
- **Work toward the destination**: Check `eywa_destination` to understand the goal. Your work should converge toward it.
