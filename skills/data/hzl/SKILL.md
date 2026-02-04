---
name: hzl
description: OpenClaw's persistent task database. Coordinate sub-agents, checkpoint progress, survive session boundaries.
homepage: https://github.com/tmchow/hzl
metadata:
  { "openclaw": { "emoji": "🧾", "homepage": "https://github.com/tmchow/hzl", "requires": { "bins": ["hzl"] }, "install": [ { "id": "brew", "kind": "brew", "package": "hzl", "bins": ["hzl"], "label": "Install HZL (Homebrew)" }, { "id": "node", "kind": "node", "package": "hzl-cli", "bins": ["hzl"], "label": "Install HZL (npm)" } ] } }
---

# HZL: Persistent task tracking for agents

HZL (https://github.com/tmchow/hzl) is a local-first task ledger (database-backed, optionally cloud-synced for backup) that an agent can use to:

- plan multi-step work into projects + tasks
- checkpoint progress (so work survives session boundaries)
- coordinate sub-agents or multiple coding tools with leases
- generate reliable status reports ("what's done vs what's left")

This skill teaches an agent how to use the `hzl` CLI.

## When to use HZL

**OpenClaw has NO native task tracking tools.** Unlike Claude Code (which has TodoWrite) or Codex (which has update_plan), OpenClaw relies on memory and markdown files for tracking work. This makes HZL especially valuable for OpenClaw.

**Use HZL by default for any non-trivial task tracking:**

- Multi-step projects with real sequencing (dependencies) and handoffs
- Work that spans multiple sessions, days, or tools/agents
- Orchestration: delegating work to sub-agents and needing recovery if they crash
- Anything where "resume exactly where we left off" matters
- **Any work you want to persist beyond this session**
- **Any work that needs structure (nesting, dependencies, progress tracking)**

**Why HZL is the right choice for OpenClaw:**

Without HZL, OpenClaw tracks tasks in-context (burns space, fragments during compaction) or in markdown files (requires manual management, no nesting/dependencies, no dashboard). HZL provides:

- Persistent storage that survives session boundaries
- Nesting (parent tasks + subtasks) and dependencies
- Web dashboard for human visibility (`hzl serve`)
- Leases for multi-agent coordination
- Checkpoints for progress recovery

**Only skip HZL for:**

- Truly trivial, one-step tasks you will complete immediately in this session
- Time-based reminders/alerts (use OpenClaw Cron instead)
- Longform notes or knowledge capture (use a notes or memory system)

Personal tasks: HZL is not a polished human to-do app, but it is usable for personal task tracking, and it can also serve as a backend for a lightweight UI.

## Core concepts

- **Project**: stable container. For OpenClaw, use a single `openclaw` project—this keeps `hzl task next` simple. Check `hzl project list` before creating.
- **Task**: top-level work item. For multi-step requests, this becomes a parent task.
- **Subtask**: breakdown of a task into parts (`--parent <id>`). Max 1 level of nesting. Parent tasks are organizational containers—never returned by `hzl task next`.
- **Checkpoint**: short progress snapshot to support recovery
- **Lease**: time-limited claim (prevents orphaned work in multi-agent flows)

## Anti-pattern: Project Sprawl

Use a single `openclaw` project. Requests and initiatives become **parent tasks**, not new projects.

**Wrong (creates sprawl):**
```bash
hzl project create "garage-sensors"
hzl project create "query-perf"
# Now you have to track which project to query
```

**Correct (single project, parent tasks):**
```bash
# Check for existing project first
hzl project list

# Use single openclaw project
hzl task add "Install garage sensors" -P openclaw
# → Created task abc123

hzl task add "Wire sensor to hub" --parent abc123
hzl task add "Configure alerts" --parent abc123

# hzl task next --project openclaw always works
```

Why this matters:
- Projects accumulate forever; you'll have dozens of abandoned one-off projects
- `hzl task next --project X` requires knowing which project to query
- With a single project, `hzl task next --project openclaw` always works

## Sizing Parent Tasks

HZL supports one level of nesting (parent → subtasks). Scope parent tasks to completable outcomes.

**The completability test:** "I finished [parent task]" should describe a real outcome.
- ✓ "Finished installing garage motion sensors"
- ✓ "Finished fixing query performance"
- ✗ "Finished home automation" (open-ended domain, never done)
- ✗ "Finished backend work" (if frontend still pending for feature to ship)

**Scope by problem, not technical layer.** A full-stack feature (frontend + backend + tests) is usually one parent if it ships together.

**Split into multiple parents when:**
- Parts deliver independent value (can ship separately)
- You're solving distinct problems that happen to be related

**Adding context:** Use `--links` to attach specs or reference docs when the description isn't enough:
```bash
hzl task add "Install garage sensors" -P openclaw \
  --links docs/sensor-spec.md \
  --links "https://example.com/wiring-guide"
```

## ⚠️ DESTRUCTIVE COMMANDS - READ CAREFULLY

The following commands **PERMANENTLY DELETE HZL DATA** and cannot be undone:

| Command | Effect |
|---------|--------|
| `hzl init --force` | **DELETES ALL DATA.** Prompts for confirmation. |
| `hzl init --force --yes` | **DELETES ALL DATA WITHOUT CONFIRMATION.** Extremely dangerous. |
| `hzl task prune ... --yes` | **PERMANENTLY DELETES** old done/archived tasks and their event history. |

**AI agents: NEVER run these commands unless the user EXPLICITLY asks you to delete data.**

- `hzl init --force` deletes the entire event database: all projects, tasks, checkpoints, and history
- `hzl task prune` deletes only tasks in terminal states (done/archived) older than the specified age
- There is NO undo. There is NO recovery without a backup.

## Quick reference

```bash
# Setup
hzl init                                      # Initialize (safe, won't overwrite)
hzl init --reset-config                       # Reset config to default location (non-destructive)
hzl project create <project>
hzl project list

# Create tasks
hzl task add "<title>" -P <project>
hzl task add "<title>" -P <project> --priority 2 --tags backend,auth
hzl task add "<title>" -P <project> --depends-on <other-id>

# Subtasks (organize related work)
hzl task add "<title>" --parent <parent-id>   # Create subtask
hzl task list --parent <parent-id>            # List subtasks
hzl task list --root                          # Top-level tasks only
hzl task next --parent <parent-id>            # Next subtask of parent

# Find work
hzl task list --project <project> --available
hzl task next --project <project>

# Work + persist progress
hzl task claim <id> --author <agent-id>
hzl task checkpoint <id> "<what changed / what's next>" [--progress 50]
hzl task progress <id> 50                     # Set progress without checkpoint
hzl task show <id> --json
hzl task complete <id>

# Blocked tasks (stuck on external issues)
hzl task block <id> --reason "Waiting for API key"
hzl task unblock <id>                         # Returns to in_progress

# Dependencies + validation
hzl task add-dep <task-id> <depends-on-id>
hzl validate

# Diagnostics
hzl status   # database mode, paths, sync state
hzl doctor   # health check for debugging

# Web Dashboard (human visibility into task state)
hzl serve                    # Start on port 3456 (network accessible)
hzl serve --host 127.0.0.1   # Restrict to localhost only
hzl serve --background       # Fork to background
hzl serve --status           # Check if running
hzl serve --stop             # Stop background server

# Multi-agent recovery
hzl task claim <id> --author <agent-id> --lease 30
hzl task stuck
hzl task steal <id> --if-expired --author <agent-id>
```

Tip: When a tool needs to parse output, prefer `--json`.

## Authorship tracking

HZL tracks authorship at two levels:

| Concept | What it tracks | Set by |
|---------|----------------|--------|
| **Assignee** | Who owns the task | `--author` on `claim` |
| **Event author** | Who performed an action | `--author` on any command |

The `--author` flag appears on many commands (checkpoint, comment, block, etc.) to record who performed each action. This is separate from task ownership:

```bash
# Alice owns the task
hzl task claim 1 --author alice

# Bob adds a checkpoint (doesn't change ownership)
hzl task checkpoint 1 "Reviewed the code" --author bob

# Task is still assigned to Alice, but checkpoint was recorded by Bob
```

For AI agents that need session tracking, use `--agent-id` on claim:
```bash
hzl task claim 1 --author "Claude Code" --agent-id "session-abc123"
```

## Recommended patterns

### Start a multi-step project

1) Create (or reuse) a stable project name.  
2) Decompose into tasks.  
3) Use dependencies to encode sequencing, not just priority.  
4) Validate.

```bash
hzl project create myapp-auth

hzl task add "Clarify requirements + acceptance criteria" -P myapp-auth --priority 5
hzl task add "Design API + data model" -P myapp-auth --priority 4 --depends-on <reqs-id>
hzl task add "Implement endpoints" -P myapp-auth --priority 3 --depends-on <design-id>
hzl task add "Write tests" -P myapp-auth --priority 2 --depends-on <impl-id>
hzl task add "Docs + rollout plan" -P myapp-auth --priority 1 --depends-on <tests-id>

hzl validate
```

### Work a task with checkpoints and progress

Checkpoint early and often. A checkpoint should be short and operational:
- what you verified
- what you changed
- what's next
- what's blocking you (if anything)

```bash
hzl task claim <id> --author orchestrator
# ...do work...
hzl task checkpoint <id> "Implemented login flow. Next: add token refresh." --progress 50
# ...more work...
hzl task checkpoint <id> "Added token refresh. Testing complete." --progress 100
hzl task complete <id>
```

You can also set progress without a checkpoint:
```bash
hzl task progress <id> 75
```

### Handle blocked tasks

When stuck on external dependencies, mark the task as blocked:

```bash
hzl task claim <id> --author orchestrator
hzl task checkpoint <id> "Implemented login flow. Blocked: need API key for staging."
hzl task block <id> --reason "Waiting for staging API key from DevOps"

# Later, when unblocked:
hzl task unblock <id>
hzl task checkpoint <id> "Got API key, resuming work"
hzl task complete <id>
```

Blocked tasks stay visible in the dashboard (Blocked column) and keep their assignee, but don't appear in `--available` lists.

### Coordinate sub-agents with leases

Use leases when delegating, so you can detect abandoned work and recover.

```bash
hzl task add "Implement REST endpoints" -P myapp-auth --priority 3 --json
hzl task claim <id> --author subagent-claude-code --lease 30
```

Delegate with explicit instructions:
- claim the task (with their author id)
- checkpoint progress as they go
- complete when done

Monitor:
```bash
hzl task show <id> --json
hzl task stuck
hzl task steal <id> --if-expired --author orchestrator
```

### Break down work with subtasks

Use parent/subtask hierarchy to organize complex work:

```bash
# Create parent task
hzl task add "Implement vacation booking" -P portland-trip --priority 2
# → abc123

# Create subtasks (project inherited automatically)
hzl task add "Research flights" --parent abc123
hzl task add "Book hotel" --parent abc123 --depends-on <flights-id>
hzl task add "Plan activities" --parent abc123

# View breakdown
hzl task show abc123

# Work through subtasks
hzl task next --parent abc123
```

**Important:** `hzl task next` only returns leaf tasks (tasks without children). Parent tasks are organizational containers—they are never returned as "next available work."

When all subtasks are done, manually complete the parent:
```bash
hzl task complete abc123
```

## Web Dashboard

HZL includes a built-in Kanban dashboard for monitoring task state. The dashboard shows tasks in columns (Backlog → Blocked → Ready → In Progress → Done), with filtering by date and project.

### Setting up the dashboard (recommended for OpenClaw)

For always-on access on your OpenClaw box, set up as a systemd service (Linux only):

```bash
# Create the systemd user directory if needed
mkdir -p ~/.config/systemd/user

# Generate and install the service file
hzl serve --print-systemd > ~/.config/systemd/user/hzl-web.service

# Enable and start
systemctl --user daemon-reload
systemctl --user enable --now hzl-web

# IMPORTANT: Enable lingering so the service runs even when logged out
loginctl enable-linger $USER

# Verify it's running
systemctl --user status hzl-web
```

The dashboard will be available at `http://<your-box>:3456` (accessible over Tailscale).

To use a different port:
```bash
hzl serve --port 8080 --print-systemd > ~/.config/systemd/user/hzl-web.service
```

**macOS note:** systemd is Linux-only. On macOS, use `hzl serve --background` or create a launchd plist manually.

### Quick commands

```bash
hzl serve                    # Start in foreground (port 3456)
hzl serve --background       # Fork to background process
hzl serve --status           # Check if background server is running
hzl serve --stop             # Stop background server
hzl serve --host 127.0.0.1   # Restrict to localhost only
```

Use `--background` for temporary sessions. Use systemd for always-on access.

## OpenClaw-specific notes

- Run `hzl ...` via the Exec tool.
- OpenClaw skill gating checks `requires.bins` on the host at skill load time. If sandboxing is enabled, the binary must also exist inside the sandbox container too. Install it via `agents.defaults.sandbox.docker.setupCommand` (or use a custom image).
- If multiple agents share the same HZL database, use distinct `--author` ids (for example: `orchestrator`, `subagent-claude`, `subagent-gemini`) and rely on leases to avoid collisions.
