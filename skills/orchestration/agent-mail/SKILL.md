---
name: agent-mail
description: "MCP Agent Mail - mail-like coordination layer for coding agents with memorable identities, inbox/outbox, searchable threads, advisory file reservations, pre-commit guards, and human-auditable Git artifacts. The backbone of multi-agent workflows."
---

# MCP Agent Mail

A mail-like coordination layer for coding agents, exposed as an HTTP-only FastMCP server. Gives agents memorable identities, an inbox/outbox, searchable message history, and voluntary file reservation "leases" to avoid stepping on each other.

Think of it as **asynchronous email + directory + change-intent signaling** for your agents, backed by Git (for human-auditable artifacts) and SQLite (for indexing and queries).

## Why Agent Mail Exists

Modern projects often run multiple coding agents at once. Without coordination, agents:
- Overwrite each other's edits or panic on unexpected diffs
- Miss critical context from parallel workstreams
- Require humans to "liaison" messages across tools

Agent Mail provides:
- **Identities**: Memorable adjective+noun names (e.g., "GreenCastle", "BlueLake")
- **Messaging**: GitHub-Flavored Markdown with threading, importance levels, and acknowledgments
- **File Reservations**: Advisory leases on files/globs to signal editing intent
- **Search**: FTS5 full-text search across message history
- **Audit Trail**: Every message and reservation is committed to Git

---

## Starting the Server

```bash
# Quick start (alias added during installation)
am

# Or manually
cd ~/projects/mcp_agent_mail && ./scripts/run_server_with_token.sh

# Check server health
curl http://127.0.0.1:8765/health/liveness
```

Default: `http://127.0.0.1:8765`. Change port with `uv run python -m mcp_agent_mail.cli config set-port 9000`.

---

## Critical Concept: project_key

**The `project_key` is the absolute path to your working directory.** This is the canonical identifier for a project.

```bash
# Two agents in the SAME directory = SAME project
Agent A in /data/projects/backend → project_key="/data/projects/backend"
Agent B in /data/projects/backend → project_key="/data/projects/backend"
# They share the same mailbox, file reservations, and coordination

# Two agents in DIFFERENT directories = DIFFERENT projects
Agent A in /data/projects/backend  → project_key="/data/projects/backend"
Agent B in /data/projects/frontend → project_key="/data/projects/frontend"
# They need explicit contact requests to message each other
```

---

## Macros vs Granular Tools

**Prefer macros** when you want speed or are on a smaller model:

| Macro | What It Does |
|-------|--------------|
| `macro_start_session` | Ensures project → registers agent → optional file reservations → fetches inbox |
| `macro_prepare_thread` | Registers agent → summarizes thread → fetches inbox context |
| `macro_file_reservation_cycle` | Reserves paths → optional auto-release after work |
| `macro_contact_handshake` | Requests contact → auto-accepts → sends welcome message |

**Use granular tools** when you need explicit control over each step.

---

## MCP Tools Reference

### Health & Discovery

| Tool | Signature | Returns |
|------|-----------|---------|
| `health_check` | `()` | `{status, environment, http_host, http_port, database_url}` |

### Project & Agent Management

| Tool | Signature | Returns |
|------|-----------|---------|
| `ensure_project` | `(human_key: str)` | `{id, slug, human_key, created_at}` |
| `register_agent` | `(project_key, program, model, name?, task_description?, attachments_policy?)` | Agent profile |
| `create_agent_identity` | `(project_key, program, model, name_hint?, task_description?, attachments_policy?)` | Agent profile (always creates new) |
| `whois` | `(project_key, agent_name, include_recent_commits?, commit_limit?)` | Enriched agent profile |

**Agent naming**: Names must be adjective+noun (e.g., "GreenCastle", "BlueLake"). If invalid, the server auto-generates one (mode: `coerce`).

### Messaging

| Tool | Signature | Returns |
|------|-----------|---------|
| `send_message` | `(project_key, sender_name, to[], subject, body_md, cc?, bcc?, attachment_paths?, convert_images?, importance?, ack_required?, thread_id?, auto_contact_if_blocked?)` | `{deliveries, count, attachments?}` |
| `reply_message` | `(project_key, message_id, sender_name, body_md, to?, cc?, bcc?, subject_prefix?)` | `{thread_id, reply_to, deliveries, count}` |
| `fetch_inbox` | `(project_key, agent_name, limit?, urgent_only?, include_bodies?, since_ts?)` | `list[message]` |
| `mark_message_read` | `(project_key, agent_name, message_id)` | `{message_id, read, read_at}` |
| `acknowledge_message` | `(project_key, agent_name, message_id)` | `{message_id, acknowledged, acknowledged_at, read_at}` |
| `search_messages` | `(project_key, query, limit?)` | `list[message]` |
| `summarize_thread` | `(project_key, thread_id, include_examples?, llm_mode?, llm_model?, per_thread_limit?)` | `{thread_id, summary, examples}` |

**Importance levels**: `low`, `normal`, `high`, `urgent`

### Contact Policies

| Tool | Signature | Returns |
|------|-----------|---------|
| `request_contact` | `(project_key, from_agent, to_agent, to_project?, reason?, ttl_seconds?)` | Contact link |
| `respond_contact` | `(project_key, to_agent, from_agent, accept, from_project?, ttl_seconds?)` | Contact link |
| `list_contacts` | `(project_key, agent_name)` | `list[contact]` |
| `set_contact_policy` | `(project_key, agent_name, policy)` | Agent profile |

**Policies**: `open`, `auto` (default), `contacts_only`, `block_all`

### File Reservations

| Tool | Signature | Returns |
|------|-----------|---------|
| `file_reservation_paths` | `(project_key, agent_name, paths[], ttl_seconds?, exclusive?, reason?)` | `{granted[], conflicts[]}` |
| `release_file_reservations` | `(project_key, agent_name, paths?, file_reservation_ids?)` | `{released, released_at}` |
| `renew_file_reservations` | `(project_key, agent_name, extend_seconds?, paths?, file_reservation_ids?)` | `{renewed, file_reservations[]}` |
| `force_release_file_reservation` | `(project_key, agent_name, file_reservation_id, notify_previous?, note?)` | `{released, released_at, reservation}` |

**File reservations are advisory** but auditable. The optional pre-commit guard blocks commits that conflict with others' active exclusive reservations.

### Pre-Commit Guard

| Tool | Signature | Returns |
|------|-----------|---------|
| `install_precommit_guard` | `(project_key, code_repo_path)` | `{hook}` |
| `uninstall_precommit_guard` | `(code_repo_path)` | `{removed}` |

### Session Macros

| Tool | Signature | Returns |
|------|-----------|---------|
| `macro_start_session` | `(human_key, program, model, task_description?, agent_name?, file_reservation_paths?, file_reservation_reason?, file_reservation_ttl_seconds?, inbox_limit?)` | `{project, agent, file_reservations, inbox}` |
| `macro_prepare_thread` | `(project_key, thread_id, program, model, agent_name?, task_description?, register_if_missing?, include_examples?, inbox_limit?, include_inbox_bodies?, llm_mode?, llm_model?)` | `{project, agent, thread, inbox}` |
| `macro_file_reservation_cycle` | `(project_key, agent_name, paths[], ttl_seconds?, exclusive?, reason?, auto_release?)` | `{file_reservations, released}` |
| `macro_contact_handshake` | `(project_key, requester, target, to_project?, reason?, ttl_seconds?, auto_accept?, welcome_subject?, welcome_body?)` | `{request, response, welcome_message}` |

---

## MCP Resources Reference

| URI | Params | Returns |
|-----|--------|---------|
| `resource://config/environment` | — | Server configuration |
| `resource://tooling/directory` | — | Tool clusters + workflow playbooks |
| `resource://tooling/schemas` | — | Argument hints for all tools |
| `resource://tooling/metrics` | — | Call/error counts per tool |
| `resource://projects` | — | All projects |
| `resource://project/{slug}` | slug | Project + agents |
| `resource://inbox/{agent}` | `?project=<abs-path>&limit=20&since_ts=...&urgent_only=...&include_bodies=...` | Inbox listing |
| `resource://outbox/{agent}` | `?project=<abs-path>&limit=20` | Sent messages |
| `resource://thread/{thread_id}` | `?project=<abs-path>&include_bodies=true` | Thread listing |
| `resource://message/{id}` | `?project=<abs-path>` | Single message |
| `resource://file_reservations/{slug}` | `?active_only=true` | File reservations + staleness metadata |
| `resource://views/urgent-unread/{agent}` | `?project=<abs-path>` | High/urgent unread messages |
| `resource://views/ack-required/{agent}` | `?project=<abs-path>` | Pending acknowledgements |
| `resource://views/ack-overdue/{agent}` | `?project=<abs-path>&ttl_minutes=30` | Overdue acknowledgements |

---

## Example Agent Workflow

```python
# 1. Start session (one call does everything)
result = macro_start_session(
    human_key="/data/projects/backend",
    program="claude-code",
    model="opus-4.5",
    task_description="Implementing auth module"
)
agent_name = result["agent"]["name"]  # e.g., "GreenCastle"
project_key = result["project"]["human_key"]

# 2. Check inbox for context
for msg in result["inbox"]:
    if msg["importance"] in ["high", "urgent"]:
        acknowledge_message(project_key, agent_name, msg["id"])

# 3. Reserve files before editing
file_reservation_paths(
    project_key, agent_name,
    paths=["src/auth/**/*.ts"],
    ttl_seconds=3600,
    exclusive=True,
    reason="bd-123"  # Link to Beads task
)

# 4. Do work, send progress updates
send_message(
    project_key, agent_name,
    to=["BlueLake"],
    subject="[bd-123] Auth module progress",
    body_md="Completed login flow. Starting session management.",
    thread_id="bd-123"
)

# 5. Release reservations when done
release_file_reservations(project_key, agent_name)
```

---

## Cross-Project Coordination

When repos are separate (e.g., frontend and backend):

**Option A: Single project bus**
- Register both agents under the same `project_key`
- Keep reservation patterns specific: `frontend/**` vs `backend/**`

**Option B: Separate projects with contact links**
```python
# Backend agent requests contact
request_contact(
    project_key="/data/projects/backend",
    from_agent="GreenCastle",
    to_agent="BlueLake",
    to_project="/data/projects/frontend",
    reason="API contract coordination"
)

# Frontend agent accepts
respond_contact(
    project_key="/data/projects/frontend",
    to_agent="BlueLake",
    from_agent="GreenCastle",
    from_project="/data/projects/backend",
    accept=True
)

# Now they can message each other
```

---

## Pre-Commit Guard

The optional pre-commit guard blocks commits that touch files reserved by other agents:

```bash
# Install guard into your code repo
mcp-agent-mail guard install /data/projects/backend /data/projects/backend

# Check guard status
mcp-agent-mail guard status /data/projects/backend

# Uninstall
mcp-agent-mail guard uninstall /data/projects/backend
```

**Requirements:**
- Set `AGENT_NAME` environment variable so the guard knows who you are
- File reservations must be active (not expired)

**Bypass (use sparingly):**
```bash
AGENT_MAIL_BYPASS=1 git commit -m "..."
# Or: AGENT_MAIL_GUARD_MODE=warn (advisory mode, doesn't block)
```

---

## Build Slots (Long-Running Tasks)

For dev servers, watchers, or builds that hold resources:

```python
# Acquire a slot
acquire_build_slot(project_key, agent_name, "frontend-build", ttl_seconds=3600, exclusive=True)

# Renew during long runs
renew_build_slot(project_key, agent_name, "frontend-build", extend_seconds=1800)

# Release when done
release_build_slot(project_key, agent_name, "frontend-build")
```

CLI helper:
```bash
mcp-agent-mail am-run frontend-build -- npm run dev
```

---

## Product Bus (Multi-Repo Coordination)

Group multiple repos under a single "product" for cross-project search and inbox:

```bash
# Create a product
mcp-agent-mail products ensure MyProduct --name "My Product"

# Link repos
mcp-agent-mail products link MyProduct /data/projects/backend
mcp-agent-mail products link MyProduct /data/projects/frontend

# Product-wide search
mcp-agent-mail products search MyProduct "urgent AND deploy" --limit 50

# Product-wide inbox
mcp-agent-mail products inbox MyProduct BlueLake --urgent-only

# Product-wide thread summary
mcp-agent-mail products summarize-thread MyProduct "bd-123"
```

---

## Web UI (Human-Facing)

Browse projects, agents, inboxes, and messages at `http://127.0.0.1:8765/mail`:

- **Unified Inbox**: Recent messages across all projects
- **Project Overview**: Search, agents, file reservations
- **Agent Inbox**: Messages for a specific agent
- **Message Detail**: Full body, attachments, thread context
- **Human Overseer**: Send high-priority messages to agents from the web

### Human Overseer

Click "Send Message" in any project view to send messages as `HumanOverseer`:
- Messages include a preamble instructing agents to pause and prioritize
- Bypasses contact policies
- Marked as `high` importance automatically

---

## Static Mailbox Export

Export mailboxes as portable, read-only HTML bundles:

```bash
# Interactive wizard (easiest)
uv run python -m mcp_agent_mail.cli share wizard

# Manual export
uv run python -m mcp_agent_mail.cli share export --output ./bundle

# Preview locally
uv run python -m mcp_agent_mail.cli share preview ./bundle --port 9000

# Verify integrity
uv run python -m mcp_agent_mail.cli share verify ./bundle
```

**Features:**
- Self-contained HTML viewer with FTS5 search
- Ed25519 signing for tamper-evident distribution
- Optional age encryption for confidential archives
- Deploy to GitHub Pages or Cloudflare Pages

---

## Integration with Beads

Beads (`bd`) owns task status/priority; Agent Mail owns conversations and audit trails.

**Conventions:**
- Use Beads issue ID as Mail `thread_id`: `send_message(..., thread_id="bd-123")`
- Prefix subjects: `[bd-123] Starting auth refactor`
- Include issue ID in file reservation `reason`: `file_reservation_paths(..., reason="bd-123")`

**Typical flow:**
```bash
# 1. Pick ready work
bd ready --json

# 2. Reserve files
file_reservation_paths(project_key, agent_name, ["src/**"], reason="bd-123")

# 3. Announce start
send_message(..., thread_id="bd-123", subject="[bd-123] Starting work")

# 4. Complete
bd close bd-123 --reason "Completed"
release_file_reservations(project_key, agent_name)
```

---

## Search Syntax (FTS5)

```
"exact phrase"           # Phrase search
prefix*                   # Prefix match
term1 AND term2           # Boolean AND
term1 OR term2            # Boolean OR
term1 NOT term2           # Exclusion
subject:login             # Field-specific
body:"build plan"         # Field-specific phrase
```

---

## CLI Commands

```bash
cd ~/projects/mcp_agent_mail

# Server
uv run python -m mcp_agent_mail.cli serve-http
uv run python -m mcp_agent_mail.cli migrate

# Configuration
uv run python -m mcp_agent_mail.cli config set-port 9000
uv run python -m mcp_agent_mail.cli config show-port

# Projects
uv run python -m mcp_agent_mail.cli list-projects --include-agents

# File Reservations
uv run python -m mcp_agent_mail.cli file_reservations list <project> --active-only
uv run python -m mcp_agent_mail.cli file_reservations soon <project> --minutes 10

# Acknowledgements
uv run python -m mcp_agent_mail.cli acks pending <project> <agent>
uv run python -m mcp_agent_mail.cli acks overdue <project> <agent> --ttl-minutes 30

# Guard
uv run python -m mcp_agent_mail.cli guard install <project_key> <code_repo_path>
uv run python -m mcp_agent_mail.cli guard uninstall <code_repo_path>
uv run python -m mcp_agent_mail.cli guard status <code_repo_path>

# Export
uv run python -m mcp_agent_mail.cli share wizard
uv run python -m mcp_agent_mail.cli share export --output ./bundle
uv run python -m mcp_agent_mail.cli share preview ./bundle

# Archive/Restore
uv run python -m mcp_agent_mail.cli archive save --label nightly
uv run python -m mcp_agent_mail.cli archive list --json
uv run python -m mcp_agent_mail.cli archive restore <file>.zip --force

# DANGER: Full reset
uv run python -m mcp_agent_mail.cli clear-and-reset-everything --force
```

---

## Configuration Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_ROOT` | `~/.mcp_agent_mail_git_mailbox_repo` | Root for project repos and SQLite |
| `HTTP_HOST` | `127.0.0.1` | Bind host |
| `HTTP_PORT` | `8765` | Bind port |
| `HTTP_BEARER_TOKEN` | — | Static bearer token for auth |
| `HTTP_ALLOW_LOCALHOST_UNAUTHENTICATED` | `true` | Allow localhost without auth |
| `LLM_ENABLED` | `true` | Enable LLM for summaries |
| `LLM_DEFAULT_MODEL` | `gpt-5-mini` | Default model for summaries |
| `CONTACT_ENFORCEMENT_ENABLED` | `true` | Enforce contact policies |
| `FILE_RESERVATIONS_ENFORCEMENT_ENABLED` | `true` | Block messages on conflicts |
| `AGENT_NAME_ENFORCEMENT_MODE` | `coerce` | `strict`, `coerce`, `always_auto` |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "sender_name not registered" | Call `register_agent` or `macro_start_session` first |
| "from_agent not registered" | Check `project_key` matches the agent's project |
| "FILE_RESERVATION_CONFLICT" | Adjust patterns, wait for expiry, or use non-exclusive |
| Pre-commit blocks commits | Set `AGENT_NAME`, or use `AGENT_MAIL_BYPASS=1` |
| Inbox empty but messages exist | Check `since_ts`, `limit`; verify recipient names match exactly |

---

## Ready-to-Paste AGENTS.md Blurb

```
## MCP Agent Mail — coordination for multi-agent workflows

**What it is:** A mail-like layer for coding agents with identities, inbox/outbox,
searchable threads, and advisory file reservations. Human-auditable artifacts in Git.

**How to use:**
1. Register identity: `ensure_project` + `register_agent` (or `macro_start_session`)
2. Reserve files: `file_reservation_paths(project_key, agent_name, ["src/**"], exclusive=true)`
3. Communicate: `send_message(..., thread_id="bd-123")`, `fetch_inbox`, `acknowledge_message`
4. Fast reads: `resource://inbox/{agent}?project=<abs-path>&limit=20`

**Macros vs granular:**
- Prefer macros for speed: `macro_start_session`, `macro_prepare_thread`
- Use granular for control: `register_agent`, `file_reservation_paths`, `send_message`

**Common pitfalls:**
- "from_agent not registered" → call `register_agent` first
- "FILE_RESERVATION_CONFLICT" → adjust patterns or wait for expiry
```

---

## Installation

```bash
curl -fsSL "https://raw.githubusercontent.com/Dicklesworthstone/mcp_agent_mail/main/scripts/install.sh?$(date +%s)" | bash -s -- --yes
```
