---
name: shared
description: Shared reference documents for distributed mode skills (not directly invocable)
user-invocable: false
metadata:
  tier: library
  internal: true
---

# Shared References

This directory contains shared reference documents used by multiple skills:

- `agent-mail-protocol.md` - Message protocol for distributed mode coordination
- `validation-contract.md` - Verification requirements for accepting spawned work
- `references/claude-code-latest-features.md` - Claude Code feature contract (slash commands, agent isolation, hooks, settings)
- `references/backend-claude-teams.md` - Concrete examples for Claude native teams (`TeamCreate` + `SendMessage`)
- `references/backend-codex-subagents.md` - Concrete examples for Codex CLI and Codex sub-agents
- `references/backend-background-tasks.md` - Fallback: `Task(run_in_background=true)`
- `references/backend-inline.md` - Degraded single-agent mode (no spawn)

These are **not directly invocable skills**. They are loaded by other skills (council, crank, swarm, research, implement) when needed.

---

## CLI Availability Pattern

All skills that reference external CLIs MUST degrade gracefully when those CLIs are absent.

### Check Pattern

```bash
# Before using any external CLI, check availability
if command -v bd &>/dev/null; then
  # Full behavior with bd
else
  echo "Note: bd CLI not installed. Using plain text tracking."
  # Fallback: use TaskList, plain markdown, or skip
fi
```

### Fallback Table

| Capability | When Missing | Fallback Behavior |
|------------|-------------|-------------------|
| `bd` | Issue tracking unavailable | Use TaskList for tracking. Note "install bd for persistent issue tracking" |
| `ao` | Knowledge flywheel unavailable | Write learnings to `.agents/knowledge/` directly. Skip flywheel metrics |
| `gt` | Workspace management unavailable | Work in current directory. Skip convoy/sling operations |
| `codex` | CLI missing or model unavailable | Fall back to runtime-native agents. Council pre-flight checks CLI presence (`which codex`) and model availability for `--mixed` mode. |
| `cass` | Session search unavailable | Skip transcript search. Note "install cass for session history" |

### Required Multi-Agent Capabilities

Council, swarm, and crank require a runtime that provides these capabilities. If a capability is missing, the corresponding feature degrades.

| Capability | What it does | If missing |
|------------|-------------|------------|
| **Spawn subagent** | Create a parallel agent with a prompt | Cannot run multi-agent. Fall back to `--quick` (inline single-agent). |
| **Agent-to-agent messaging** | Send a message to a specific agent | No debate R2. Workers run fire-and-forget. |
| **Broadcast** | Message all agents at once | Per-agent messaging fallback. |
| **Graceful shutdown** | Request an agent to terminate | Agents terminate on their own when done. |
| **Shared task list** | Agents see shared work state | Lead tracks manually. |

Every runtime maps these capabilities to its own API. Skills describe WHAT to do, not WHICH tool to call.

**After detecting your backend (see Backend Detection below), load the matching reference for concrete tool call examples:**

| Backend | Reference |
|---------|-----------|
| Claude feature contract | `skills/shared/references/claude-code-latest-features.md` |
| Claude Native Teams | `skills/shared/references/backend-claude-teams.md` |
| Codex Sub-Agents / CLI | `skills/shared/references/backend-codex-subagents.md` |
| Background Tasks (fallback) | `skills/shared/references/backend-background-tasks.md` |
| Inline (no spawn) | `skills/shared/references/backend-inline.md` |

### Backend Detection

Use capability detection at runtime, not hardcoded tool names. The same skill must work across any agent harness that provides multi-agent primitives. If no multi-agent capability is detected, degrade to single-agent inline mode (`--quick`).

**Selection policy (runtime-native first):**
1. If running in a Claude session and `TeamCreate`/`SendMessage` are available, use **Claude Native Teams** as the primary backend.
2. If running in a Codex session and `spawn_agent` is available, use **Codex sub-agents** as the primary backend.
3. If both are technically available, pick the backend native to the current runtime unless the user explicitly requests mixed/cross-vendor execution.
4. Only use background tasks when neither native backend is available.

| Operation | Codex Sub-Agents | Claude Native Teams | OpenCode Subagents | Inline Fallback |
|-----------|------------------|---------------------|--------------------|-----------------|
| Spawn | `spawn_agent(message=...)` | `TeamCreate` + `Task(team_name=...)` | `task(subagent_type="general", prompt=...)` | Execute inline |
| Spawn (read-only) | `spawn_agent(message=...)` | `Task(subagent_type="Explore")` | `task(subagent_type="explore", prompt=...)` | Execute inline |
| Wait | `wait(ids=[...])` | Completion via `SendMessage` | Task returns result directly | N/A |
| Retry/follow-up | `send_input(id=..., message=...)` | `SendMessage(type="message", ...)` | `task(task_id="<prior>", prompt=...)` | N/A |
| Cleanup | `close_agent(id=...)` | `shutdown_request` + `TeamDelete()` | None (sub-sessions auto-terminate) | N/A |
| Inter-agent messaging | `send_input` | `SendMessage` | Not available | N/A |
| Debate (R2) | Supported | Supported | **Not supported** (no messaging) | N/A |

**OpenCode limitations:**
- No inter-agent messaging — workers run as independent sub-sessions
- No debate mode (`--debate`) — requires messaging between judges
- `--quick` (inline) mode works identically across all backends

### Backend Capabilities Matrix

> **Prefer native teams over background tasks.** Native teams provide messaging, redirect, and graceful shutdown. Background tasks are fire-and-forget with no steering — only a speedometer and emergency brake.

| Capability | Codex Sub-Agents | Claude Native Teams | Background Tasks | Distributed (tmux) |
|------------|------------------|---------------------|------------------|---------------------|
| Observe output | `wait()` result | `SendMessage` delivery | `TaskOutput` (tail) | Agent Mail inbox |
| Send message mid-flight | `send_input` | `SendMessage` | **NO** | Agent Mail |
| Pause / resume | NO | Idle → wake via `SendMessage` | **NO** | `tmux` detach/attach |
| Graceful stop | `close_agent` | `shutdown_request` | **TaskStop (lossy)** | `tmux kill-session` |
| Redirect to different task | `send_input` | `SendMessage` | **NO** | Agent Mail |
| Adjust scope mid-flight | `send_input` | `SendMessage` | **NO** | Agent Mail |
| File conflict prevention | Manual `git worktree` routing | Native `isolation: worktree` + lead-only commits | None | File reservations |
| Crash recovery | NO | NO | NO | **YES** (tmux persists) |
| Process isolation | YES (sub-process) | Shared worktree | Shared worktree | **YES** (separate process) |

**When to use each:**

| Scenario | Backend |
|----------|---------|
| Quick parallel tasks, coordination needed | Claude Native Teams |
| Codex-specific execution | Codex Sub-Agents |
| Long-running work, need debug/recovery | Distributed (tmux + Agent Mail) |
| No team APIs available (last resort) | Background Tasks |

### Skill Invocation Across Runtimes

Skills that chain to other skills (e.g., `/rpi` calls `/research`, `/vibe` calls `/council`) MUST handle runtime differences:

| Runtime | Tool | Behavior | Pattern |
|---------|------|----------|---------|
| Claude Code | `Skill(skill="X", args="...")` | **Executable** — skill runs as a sub-invocation | `Skill(skill="council", args="--quick validate recent")` |
| Codex | N/A | Skills not available — inline the logic or skip | Check if `Skill` tool exists before calling |
| OpenCode | `skill` tool (read-only) | **Load-only** — returns `<skill_content>` blocks into context | Call `skill(skill="council")`, then follow the loaded instructions inline |

**OpenCode skill chaining rules:**
1. Call the `skill` tool to load the target skill's content into context
2. Read and follow the loaded instructions directly — do NOT expect automatic execution
3. **NEVER use slashcommand syntax** (e.g., `/council`) in OpenCode — it triggers a command lookup, not skill loading
4. If the loaded skill references tools by Claude Code names, use OpenCode equivalents (see tool mapping below)

**Cross-runtime tool mapping:**

| Claude Code | OpenCode | Notes |
|-------------|----------|-------|
| `Task(subagent_type="...")` | `task(subagent_type="...")` | Same semantics, different casing |
| `Skill(skill="X")` | `skill` tool (read-only) | Load content, then follow inline |
| `AskUserQuestion` | `question` | Same purpose, different name |
| `TodoWrite` | `todo` | Same purpose, different name |
| `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep` | Same names | Identical across runtimes |

### Rules

1. **Never crash** — missing CLI = skip or fallback, not error
2. **Always inform** — tell the user what was skipped and how to enable it
3. **Preserve core function** — the skill's primary purpose must still work without optional CLIs
4. **Progressive enhancement** — CLIs add capabilities, their absence removes them cleanly
