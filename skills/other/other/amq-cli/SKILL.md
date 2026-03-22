---
name: amq-cli
version: 1.7.0
description: >-
  Coordinate agents via the AMQ CLI for file-based inter-agent messaging.
  Use when you need to send messages to another agent (Claude/Codex),
  receive messages from partner agents, set up co-op mode between Claude
  Code and Codex CLI, or manage agent-to-agent communication in any
  multi-agent workflow. Triggers include "message codex", "talk to claude",
  "collaborate with partner agent", "AMQ", "inter-agent messaging",
  "agent coordination". For spec/design tasks use the /spec command
  instead.
metadata:
  short-description: Inter-agent messaging via AMQ CLI
  compatibility: claude-code, codex-cli
---

# AMQ CLI Skill

File-based message queue for agent-to-agent coordination.

## Prerequisites

Requires `amq` binary in PATH. Install:
```bash
curl -fsSL https://raw.githubusercontent.com/avivsinai/agent-message-queue/main/scripts/install.sh | bash
```

## Environment Rules (IMPORTANT)

When running inside `coop exec`, the environment is already configured:

- **Always use `amq` from PATH** — never `./amq`, `../amq`, or absolute paths
- **Never override `AM_ROOT` or `AM_ME`** — they are set by `coop exec`
- **Never pass `--root` or `--me` flags** — env vars handle routing
- **Just run commands as-is**: `amq send --to codex --body "hello"`

When running **outside** `coop exec` (e.g. new conversation, manual terminal):

- **Use `amq env` to resolve the root** — it reads `.amqrc` and returns the base root:
  ```bash
  eval "$(amq env --me claude)"          # sets AM_ME + AM_ROOT from .amqrc
  ```
- Or resolve and pin explicitly per command (never hardcode the root — read it from `.amqrc`):
  ```bash
  AM_ME=claude AM_ROOT=$(amq env --json | jq -r .root) amq send --to codex --body "hello"
  ```
- **Do NOT append a session name** (e.g. `/collab`) unless you intentionally want an isolated session. Outside `coop exec`, the base root from `.amqrc` is where agents live.
- **Pitfall**: `coop exec` defaults to `--session collab` (i.e. `.agent-mail/collab`). If you manually use `.agent-mail/collab` outside `coop exec`, messages go to a different mailbox tree than `.agent-mail`. Only use a session path if the target agent is also in that session.

### Root Resolution Truth-Table

| Context | Command | AM_ROOT resolves to |
|---------|---------|---------------------|
| Outside `coop exec` | `amq env --me claude` | base root from `.amqrc` (e.g. `.agent-mail`) |
| Outside `coop exec`, isolated session | `amq env --session auth --me claude` | `.agent-mail/auth` |
| Inside `coop exec` (no flags) | automatic | `.agent-mail/collab` (default session) |
| Inside `coop exec --session X` | automatic | `.agent-mail/X` |

## Task Routing — READ THIS FIRST

**Before doing anything**, match your task to the right workflow:

| Your task | What to do | DO NOT |
|-----------|-----------|--------|
| **"spec", "design with", "collaborative spec"** | Use the `/spec` command instead. It provides structured phase-by-phase guidance. | Do NOT handle spec tasks from this skill. |
| **Send a message, review request, question** | Use `amq send` (see Messaging below) | — |
| **Swarm / agent teams** | Read [references/swarm-mode.md](references/swarm-mode.md), then use `amq swarm` | — |
| **Received message with labels `workflow:spec`** | Follow the spec skill protocol: do independent research first, then engage on the `spec/<topic>` thread. | Do NOT skip straight to implementation. |

## Quick Start

```bash
# One-time project setup
amq coop init

# Per-session (one command per terminal — defaults to --session collab)
amq coop exec claude -- --dangerously-skip-permissions  # Terminal 1
amq coop exec codex -- --dangerously-bypass-approvals-and-sandbox  # Terminal 2
```

Without `--session` or `--root`, `coop exec` defaults to `--session collab`.

## Session Layout

By default, `.amqrc` points to a literal root (e.g., `.agent-mail`). Use `--session` to create isolated subdirectories:

```
.agent-mail/              ← default root (configured in .amqrc)
.agent-mail/auth/         ← isolated session (via --session auth)
.agent-mail/api/          ← isolated session (via --session api)
```

- `amq coop exec claude` → `AM_ROOT=.agent-mail/collab` (default session)
- `amq coop exec --session auth claude` → `AM_ROOT=.agent-mail/auth`

Only two env vars: `AM_ROOT` (where) + `AM_ME` (who). The CLI enforces correct routing — just run `amq` commands as-is.

## Cross-Project Routing

Send messages to agents in other projects via `--project` or inline `@project:session` syntax. Requires peer configuration in `.amqrc`.

**When to use `--session` vs `--project`**: `--session` = same project, different session. `--project` = different project. Change one dimension at a time.

### Peer setup

Add `project` and `peers` to your `.amqrc`:
```json
{
  "root": ".agent-mail",
  "project": "my-project",
  "peers": {
    "infra-lib": "/Users/me/projects/infra-lib/.agent-mail"
  }
}
```

Both projects must register each other as peers for round-trip messaging.

### Sending cross-project

```bash
# Flag syntax
amq send --to codex --project infra-lib --body "hello from here"

# Inline syntax (terser)
amq send --to codex@infra-lib:collab --body "inline syntax"

# Same session name as source (default when --session omitted)
amq send --to codex --project infra-lib --body "delivers to same session"
```

### Replies route automatically

When you receive a cross-project message, `reply_project` is set in the header. `amq reply` routes back automatically — no `--project` flag needed:
```bash
amq reply --id <msg_id> --body "got it"  # routes back via reply_project
```

### Thread naming

- **Same project P2P**: `p2p/claude__codex`
- **Cross-project P2P**: `p2p/projA:collab:claude__projB:collab:codex`
- **Topical** (cross-project): use same thread ID across projects, e.g., `decision/release-v0.24`

For full details, see [references/cross-project.md](references/cross-project.md).

## Decision Threads

Decentralized decision protocol using existing AMQ primitives (no new CLI commands).

- **Thread**: `decision/<topic>`
- **Kind**: `decision` for all messages
- **Labels**: `decision:proposal`, `decision:objection`, `decision:support`, `decision:final`; plus `project:<name>` for cross-project decisions
- **Context** on proposals: `{"proposal_id": "...", "question": "...", "options": [...], "required_projects": [...], "deadline": "..."}`

**Process**: Propose → Review/Object → Resolve objections → Close when all required projects responded and no unresolved blocking objections.

```bash
amq send --to codex --project infra-lib --kind decision \
  --labels "decision:proposal,project:my-project,project:infra-lib" \
  --thread "decision/api-v2" \
  --context '{"proposal_id":"api-v2","question":"Adopt new API?","required_projects":["my-project","infra-lib"]}' \
  --body "Proposal: migrate to API v2. All tests green."
```

## Messaging

```bash
amq send --to codex --body "Message"              # Send (uses AM_ROOT/AM_ME from env)
amq drain --include-body                          # Receive (one-shot, silent when empty)
amq reply --id <msg_id> --body "Response"          # Reply in thread
amq watch --timeout 60s                           # Block until message arrives
amq list --new                                    # Peek without side effects
```

### Send with metadata
```bash
amq send --to codex --subject "Review" --kind review_request --body @file.md
amq send --to codex --priority urgent --kind question --body "Blocked on API"
amq send --to codex --labels "bug,parser" --context '{"paths": ["src/"]}' --body "Found issue"
```

### Filter
```bash
amq list --new --priority urgent
amq list --new --from codex --kind review_request
amq list --new --label bug
```

## Priority Handling

| Priority | Action |
|----------|--------|
| `urgent` | Interrupt current work, respond now |
| `normal` | Add to TODOs, respond after current task |
| `low` | Batch for session end |

## Message Kinds

| Kind | Reply Kind | Default Priority |
|------|------------|------------------|
| `review_request` | `review_response` | normal |
| `question` | `answer` | normal |
| `decision` | — | normal |
| `todo` | — | normal |
| `status` | — | low |
| `brainstorm` | — | low |

## References

For detailed protocols, read the reference file FIRST, then follow its instructions:

- [references/coop-mode.md](references/coop-mode.md) — Co-op protocol: roles, phased flow, collaboration modes
- [references/swarm-mode.md](references/swarm-mode.md) — Swarm mode: agent teams, bridge, task workflow
- [references/message-format.md](references/message-format.md) — Message format: frontmatter schema, field reference
- [references/cross-project.md](references/cross-project.md) — Cross-project routing: peer config, addressing, decision threads
