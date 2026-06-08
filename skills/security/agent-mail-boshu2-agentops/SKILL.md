---
name: agent-mail
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when coordinating agents with Agent Mail locks, inboxes, threads, and conflict-prevention handoffs."
practices:
- pragmatic-programmer
---
<!-- TOC: Boundary | Bootstrap | Core Ops | File Reservations | Beads | Troubleshooting | Identity | Human Overseer | Pre-Commit Guard | References -->

# Using MCP Agent Mail

> **Core Insight:** Agent Mail is the side channel for leases, notifications, acknowledgements, and handoffs. BR/beads is the durable coordination bus and source of truth for work state, evidence, and decisions.

## Coordination Boundary

| Need | Source of truth |
|------|-----------------|
| Work queue, status, dependencies, priority, closure evidence | BR/beads (`br`/`bv`) |
| File ownership, active edit leases, lane notifications, acks | Agent Mail |
| Final proof that work is done | Bead notes/closure plus git/CI evidence |
| "Who may write this hot path right now?" | Agent Mail file reservation |

Use Agent Mail to prevent collisions and notify active agents. Do not use it as the durable task queue, audit log, or final evidence store. If a mail thread and BR disagree, reconcile the bead first and link the mail thread from the bead note if the conversation matters.

One-writer-per-hot-dir rule: reserve the path before editing it. If the reservation conflicts, do not write into that path; coordinate with the holder, narrow scope, or wait for the lease to clear.

## When to Use What

| Situation | Action |
|-----------|--------|
| Starting any agent session | `macro_start_session` |
| About to edit files | `file_reservation_paths` → edit → `release_file_reservations` |
| Need to tell another agent something | `send_message` with `thread_id` |
| Picking up someone else's work | `macro_prepare_thread` |
| Need durable work state or evidence | Update BR/beads, then link the mail thread if useful |
| Can't message an agent | `request_contact` → wait for approval |
| Server seems broken | Use `health_check()` first; CLI-only: `doctor check --verbose` → `doctor repair --yes` |

---

## THE EXACT PROMPT — Session Bootstrap

**Call this at the start of every agent session:**

```
macro_start_session(
  human_key="/abs/path/to/project",
  program="codex-cli",
  model="YOUR_MODEL",
  task_description="Working on auth module"
)
```

Returns: `{project, agent, file_reservations, inbox}`

This single call: ensures project exists → registers your identity → fetches inbox.

---

## Core Operations

| Task | Tool |
|------|------|
| Bootstrap session | `macro_start_session(human_key, program, model, task_description)` |
| Send message | `send_message(project_key, sender_name, to, subject, body_md)` |
| Reply in thread | `reply_message(project_key, message_id, sender_name, body_md)` |
| Check inbox | `fetch_inbox(project_key, agent_name, limit=20)` |
| Reserve files | `file_reservation_paths(project_key, agent_name, paths, ttl_seconds)` |
| Release files | `release_file_reservations(project_key, agent_name)` |
| Search messages | `search_messages(project_key, "query")` |

### The Four Macros

| Macro | When to Use |
|-------|-------------|
| `macro_start_session` | Bootstrap: project → agent → inbox |
| `macro_prepare_thread` | Join existing thread with summary |
| `macro_file_reservation_cycle` | Reserve → work → auto-release |
| `macro_contact_handshake` | Cross-agent contact setup |

### Fast Resource Reads (No Tool Call Required)

| Need | Resource |
|------|----------|
| List agents | `resource://agents/{project_key}` |
| Inbox | `resource://inbox/{agent}?project=/abs/path&limit=20` |
| Thread | `resource://thread/{thread_id}?project=/abs/path&include_bodies=true` |
| Ack-required | `resource://views/ack-required/{agent}?project=/abs/path` |

---

## File Reservations

### Reserve Before Editing

```
file_reservation_paths(
  project_key="/abs/path/project",
  agent_name="GreenCastle",
  paths=["src/auth/**/*.ts"],
  ttl_seconds=3600,
  exclusive=true,
  reason="bd-123"
)
```

Returns: `{granted: [...], conflicts: [...]}`

### Conflict Resolution

If conflicts exist:
1. **Wait** — TTL will expire
2. **Coordinate** — Message the holder
3. **Share** — Use `exclusive=false`

### Release When Done

```
release_file_reservations(project_key="/abs/path/project", agent_name="GreenCastle")
```

---

## Beads Integration

Use bead IDs as your threading anchor. BR remains authoritative; mail carries the lease, notification, and discussion side channel.

```
1. Pick work:        br ready --json → choose bd-123
2. Reserve files:    file_reservation_paths(..., reason="bd-123")
3. Announce:         send_message(..., thread_id="bd-123", subject="[bd-123] Starting...")
4. Work:             Reply in thread with progress
5. Record evidence:  br update bd-123 --notes "Validation: tests, commit, CI, or handoff proof"
6. Complete:         br close bd-123, release_file_reservations(...), final message
```

**Bead ID (often bd-###) goes in:** thread_id, subject prefix, reservation reason, commit message

**Do not infer durable state from mail silence.** A missing reply is not proof that a bead is abandoned, blocked, or complete. Check `br show <id> --json`, `bv --robot-insights`, git state, and CI evidence before changing work state.

---

## Quick Troubleshooting

| Error | Fix |
|-------|-----|
| "sender_name not registered" | Call `macro_start_session` first |
| "FILE_RESERVATION_CONFLICT" | Wait, coordinate, or use `exclusive=false` |
| "CONTACT_BLOCKED" | Use `request_contact`, wait for approval |
| Empty inbox | Check `since_ts`, `urgent_only`, agent name spelling |
| Server unreachable | Use `health_check()` or `resource://config/environment` to confirm MCP server is up; if CLI-only, check `curl http://127.0.0.1:8765/health` |
| Guard blocks commit | Set `AGENT_NAME` env var; bypass: `AGENT_MAIL_BYPASS=1 git commit` |

### Doctor Diagnostics (CLI-only, optional)

```bash
# Quick health check (CLI daemon)
curl http://127.0.0.1:8765/health

# Full diagnostics (CLI)
uv run python -m mcp_agent_mail.cli doctor check --verbose

# Preview repairs (dry run, CLI)
uv run python -m mcp_agent_mail.cli doctor repair --dry-run

# Apply repairs (CLI)
uv run python -m mcp_agent_mail.cli doctor repair --yes
```

---

## Agent Identity

Agents get adjective+noun names: GreenCastle, BlueLake, RedBear.

**Best practice:** Omit `name` parameter to auto-generate valid names.

```
register_agent(
  project_key="/abs/path/project",
  program="codex-cli",
  model="YOUR_MODEL",
  task_description="Auth refactor"
)  # name auto-generated
```

---

## Human Overseer

Send urgent messages to agents from the web UI at `http://127.0.0.1:8765/mail`:

1. Click "Human Overseer" mode
2. Compose with `importance: urgent`
3. Select target agents

Agents see urgent messages via `fetch_inbox(..., urgent_only=true)`.

---

## Pre-Commit Guard

```
install_precommit_guard(project_key="/abs/path", code_repo_path="/abs/path")
```

- Set `AGENT_NAME` env var so guard knows who you are
- Bypass emergency: `AGENT_MAIL_BYPASS=1 git commit -m "fix"`
- Warning mode: `AGENT_MAIL_GUARD_MODE=warn`

---

## Search Syntax (FTS5)

```
"exact phrase"
prefix*
term1 AND term2
term1 OR term2
(auth OR login) AND NOT admin
```

---

## References

| Topic | Reference |
|-------|-----------|
| All MCP tools | [TOOLS.md](references/TOOLS.md) |
| Workflow patterns | [WORKFLOWS.md](references/WORKFLOWS.md) |
| MCP resources | [RESOURCES.md](references/RESOURCES.md) |
| Cross-project setup | [CROSS-PROJECT.md](references/CROSS-PROJECT.md) |
| Doctor & recovery | [RECOVERY.md](references/RECOVERY.md) |
| Installation | [INSTALL.md](references/INSTALL.md) |
| Fix MCP config | [FIX-MCP-CONFIG.md](references/FIX-MCP-CONFIG.md) |
| Product bus, build slots, internals | [ADVANCED.md](references/ADVANCED.md) |

---

## Validation

```bash
# Server health
curl http://127.0.0.1:8765/health
# → {"status": "healthy"}

# Start server if needed
am
```
