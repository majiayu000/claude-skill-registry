---
name: amq-cli
version: 1.2.0
description: Coordinate agents via the AMQ CLI for file-based inter-agent messaging. Use when you need to send messages to another agent (Claude/Codex), receive messages from partner agents, set up co-op mode between Claude Code and Codex CLI, or manage agent-to-agent communication in any multi-agent workflow. Triggers include "message codex", "talk to claude", "collaborate with partner agent", "AMQ", "inter-agent messaging", or "agent coordination".
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

Verify: `amq --version`

## Quick Start

```bash
# One-time project setup
amq coop init

# Per-session (one command per terminal — defaults to --session collab)
amq coop exec claude -- --dangerously-skip-permissions  # Terminal 1
amq coop exec codex -- --dangerously-bypass-approvals-and-sandbox  # Terminal 2
```

Without `--session` or `--root`, `coop exec` defaults to `--session collab`.

That's it. `coop exec` auto-initializes if needed, sets `AM_ROOT`/`AM_ME`, starts wake notifications, and execs into the agent.

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

## Environment Rules (IMPORTANT)

When running inside `coop exec`, the environment is already configured. Follow these rules:

- **Always use `amq` from PATH** — never `./amq`, `../amq`, or absolute paths to local binaries
- **Never override `AM_ROOT` or `AM_ME`** — they are set by `coop exec` and point to the correct session. Do not prefix commands with `AM_ROOT=... amq ...`
- **Never pass `--root` or `--me` flags** — the env vars handle routing automatically
- **Just run commands as-is**: `amq send --to codex --body "hello"`

Wrong:
```bash
AM_ROOT=.agent-mail AM_ME=claude ./amq send --to codex --body "hello"
```

Right:
```bash
amq send --to codex --body "hello"
```

## Messaging

```bash
amq send --to codex --body "Message"              # Send (uses AM_ROOT/AM_ME from env)
amq drain --include-body                          # Receive (one-shot, silent when empty)
amq reply --id <msg_id> --body "Response"          # Reply in thread
amq watch --timeout 60s                           # Block until message arrives
amq list --new                                    # Peek without side effects
```

Root and agent handle come from `AM_ROOT` and `AM_ME` environment variables. Commands work from any subdirectory.

## Isolated Sessions (Multiple Pairs)

```bash
amq coop exec --session auth claude               # Pair A
amq coop exec --session auth codex
amq coop exec --session api claude                # Pair B
amq coop exec --session api codex
```

Or with shell aliases (via `eval "$(amq shell-setup)"`):
```bash
amc auth    # Claude in auth session
amx auth    # Codex in auth session
amc api     # Claude in api session
amx api     # Codex in api session
```

Each session has isolated inboxes. Messages stay within their root.

## For Scripts/CI

When you can't use `exec` (non-interactive environments):
```bash
amq coop init
eval "$(amq env --me claude)"    # Set env vars manually
```

## Co-op Protocol

### Core Rules

1. **Initiator rule** — reply to the initiator; ask the initiator for clarifications
2. **Never branch** — always work on same branch
3. **Code phase = split** — divide files/modules to avoid conflicts
4. **Shared workspace** — reference file paths, don't paste code in messages

### Priority Handling

| Priority | Action |
|----------|--------|
| `urgent` | Interrupt current work, respond now |
| `normal` | Add to TODOs, respond after current task |
| `low` | Batch for session end |

### Progress Updates

```bash
amq reply --id <msg_id> --kind status --body "Started, eta ~20m"
amq reply --id <msg_id> --kind answer --body "Summary: ..."
```

## Commands Reference

### Send
```bash
amq send --to codex --body "Quick message"
amq send --to codex --subject "Review" --kind review_request --body @file.md
amq send --to codex --priority urgent --kind question --body "Blocked on API"
amq send --to codex --labels "bug,parser" --body "Found issue"
amq send --to codex --context '{"paths": ["internal/cli/"]}' --body "Review these"
```

### Filter
```bash
amq list --new --priority urgent
amq list --new --from codex --kind review_request
amq list --new --label bug --label critical
```

### Reply
```bash
amq reply --id <msg_id> --body "LGTM"
amq reply --id <msg_id> --kind review_response --body "See comments..."
```

### Dead Letter Queue
```bash
amq dlq list                                      # List failed messages
amq dlq retry --id <dlq_id>                       # Retry one
amq dlq retry --all                               # Retry all
amq dlq purge --older-than 24h --yes              # Clean old entries
```

### Other
```bash
amq thread --id p2p/claude__codex --include-body  # View thread
amq presence set --status busy --note "reviewing" # Set presence
amq cleanup --tmp-older-than 36h --yes            # Clean stale tmp
amq upgrade                                       # Self-update
```

## Message Kinds

| Kind | Reply Kind | Default Priority |
|------|------------|------------------|
| `review_request` | `review_response` | normal |
| `question` | `answer` | normal |
| `decision` | — | normal |
| `todo` | — | normal |
| `status` | — | low |
| `brainstorm` | — | low |

## Swarm Mode: Agent Teams

Enable external agents to participate in Claude Code Agent Teams.

```bash
amq swarm list                                    # Discover teams
amq swarm join --team my-team --me codex          # Join team
amq swarm tasks --team my-team                    # View tasks
amq swarm claim --team my-team --task t1 --me codex  # Claim work
amq swarm complete --team my-team --task t1 --me codex  # Mark done
amq swarm bridge --team my-team --me codex        # Run task notification bridge
```

Communication is asymmetric: bridge delivers task notifications only. Claude Code teammates can `amq send` to external agents. External agents relay messages to the team leader's inbox.

## References

- `references/coop-mode.md` — Phased workflow, collaboration modes, detailed coordination patterns
- `references/message-format.md` — Frontmatter schema cheat sheet (fields, types, defaults)
