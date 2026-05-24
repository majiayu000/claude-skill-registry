---
name: amq-cli
version: 1.0.5
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

## Quick Reference

```bash
# One-time project setup (run once per project)
amq coop start claude    # Initializes if needed, then tells you to run: claude
amq coop start codex     # Same for Codex

# Or initialize manually
amq coop init            # Creates .amqrc, mailboxes, updates .gitignore
```

**As Claude** (talking to Codex):
```bash
amq send --me claude --to codex --body "Message"
amq drain --me claude --include-body
amq reply --me claude --id <msg_id> --body "Response"
amq watch --me claude --timeout 60s
```

**As Codex** (talking to Claude):
```bash
amq send --me codex --to claude --body "Message"
amq drain --me codex --include-body
amq reply --me codex --id <msg_id> --body "Response"
amq watch --me codex --timeout 60s
```

**Note**: Root is auto-detected from `.amqrc`. Commands work from any subdirectory.

## Co-op Mode: Phased Parallel Work

Both agents work in parallel where safe, coordinate where risky. Different models = different training = different blind spots. Cross-model work catches errors that same-model review misses.

### Roles

- **Initiator** = whoever starts the task (agent or human). Owns decisions and receives updates.
- **Leader/Coordinator** = coordinates phases, merges, and final decisions (often the initiator).
- **Worker** = executes assigned phases and reports back to the initiator.

**Default pairing note**: Claude is often faster and more decisive, while Codex tends to be deeper but slower. That commonly makes Claude a natural coordinator and Codex a strong worker. This is a default, not a rule — roles are set per task by the initiator.

### Phased Flow

| Phase | Mode | Description |
|-------|------|-------------|
| **Research** | Parallel | Both explore codebase, read docs, search. No conflicts. |
| **Design** | Parallel → Merge | Both propose approaches. Leader merges/decides. |
| **Code** | Split | Divide by file/module. Never edit same file. |
| **Review** | Parallel | Both review each other's code. Leader decides disputes. |
| **Test** | Parallel | Both run tests, report results to leader. |

```
Research (parallel) → sync findings
    ↓
Design (parallel) → leader merges approach
    ↓
Code (split: e.g., Claude=files A,B; Codex=files C,D)
    ↓
Review (parallel: each reviews other's code)
    ↓
Test (parallel: both run tests)
    ↓
Leader prepares commit → user approves → push
```

### Key Rules

- **Initiator rule** — reply to the initiator and ask the initiator for clarifications
- **Never branch** — always work on same branch (joined work)
- **Code phase = split** — divide files/modules to avoid conflicts
- **File overlap** — if same file unavoidable, assign one owner; other reviews/proposes via message
- **Coordinate between phases** — sync before moving to next phase
- **Leader decides** — initiator or designated leader makes final calls at merge points

### Stay in Sync

- After completing a phase, report to the initiator and await next assignment
- While waiting, safe to do: review partner's work, run tests, read docs
- If no assignment comes, ask the initiator (not a third party) for next task

### Progress Protocol (Start / Heartbeat / Done)

- **Start**: send `kind=status` with an ETA to the initiator as soon as you begin.
- **Heartbeat**: update on phase boundaries or every 10-15 minutes.
- **Done**: send Summary / Changes / Tests / Notes to the initiator.
- **Blocked**: send `kind=question` to the initiator with options and a recommendation.

### Modes of Collaboration (Modus Operandi)

Pick one mode per task; the initiator decides or delegates.

- **Leader + Worker**: leader decides, worker executes; best default.
- **Co-workers**: peers decide together; if no consensus, ask the initiator.
- **Duplicate**: independent solutions or reviews; initiator merges results.
- **Driver + Navigator**: driver codes, navigator reviews/tests and can interrupt.
- **Spec + Implementer**: one writes spec/tests, the other implements.
- **Reviewer + Implementer**: one codes, the other focuses on review and risk detection.

### Shared Workspace

**Both agents work in the same project folder.** Files are shared automatically:
- If partner says "done with X" → check the files directly, don't ask for code
- Don't send code snippets in messages → just reference file paths

### When to Act

| Role | Action |
|------|--------|
| Worker | Complete phase → report to initiator → await next assignment |
| Leader/Initiator | Merge results → decide next phase work |
| Either | Ask the initiator for clarifications (ask the user only if the user initiated) |

### Setup

Run once per project:
```bash
amq coop start claude   # Initializes + tells you to run: claude
```

In a second terminal:
```bash
amq coop start codex    # Tells you to run: codex
```

### Multiple Pairs (Isolated Sessions)

Run multiple agent pairs on different features using `--root`:

```bash
# Pair A: auth feature
amq coop start --root .agent-mail/auth claude
amq coop start --root .agent-mail/auth codex

# Pair B: api feature
amq coop start --root .agent-mail/api claude
amq coop start --root .agent-mail/api codex

# Commands use --root to stay isolated
amq send --me claude --to codex --root .agent-mail/auth --body "Auth review"
```

Each root has isolated inboxes. Messages stay within their root.

### Priority Handling

| Priority | Action |
|----------|--------|
| `urgent` | Interrupt, respond now (label `interrupt` enables wake Ctrl+C) |
| `normal` | Add to TODOs, respond after current task |
| `low` | Batch for session end |

### Progress Updates

Use Start / Heartbeat / Done with the initiator:

```bash
amq reply --me claude --id <msg_id> --kind status --body "Started, eta ~20m"
amq reply --me claude --id <msg_id> --kind status --body "Design done, coding now. ETA ~10m"
amq reply --me claude --id <msg_id> --kind answer --body "Summary:\n- ...\nChanges:\n- ...\nTests:\n- ...\nNotes:\n- ..."
```

### Optional: Wake Notifications

> Co-op works without wake. This is an optional enhancement for interactive terminals.

For human operators, wake provides background notifications:

```bash
amq wake --me claude &   # Before starting claude
```

When messages arrive:
```
AMQ: message from codex - Review complete. Drain with: amq drain --me claude --include-body
```

If notifications require manual Enter, try `--inject-mode=raw`.

**Interrupts**: urgent messages labeled `interrupt` trigger Ctrl+C injection + an interrupt notice.
Disable with `--interrupt=false`. Use `--interrupt-cmd none` for notice-only.

## Commands

All examples show Claude's perspective. Codex swaps `--me codex` and `--to claude`.

### Send
```bash
amq send --me claude --to codex --body "Quick message"
amq send --me claude --to codex --subject "Review" --kind review_request --body @file.md
amq send --me claude --to codex --priority urgent --kind question --body "Blocked on API"
amq send --me claude --to codex --labels "bug,parser" --body "Found issue in parser"
amq send --me claude --to codex --context '{"paths": ["internal/cli/"]}' --body "Review these"
```

### Receive
```bash
amq drain --me claude --include-body   # One-shot, silent when empty
amq watch --me claude --timeout 60s    # Block until message arrives
amq list --me claude --new             # Peek without side effects
```

### Filter Messages
```bash
amq list --me claude --new --priority urgent              # By priority
amq list --me claude --new --from codex                   # By sender
amq list --me claude --new --kind review_request          # By kind
amq list --me claude --new --label bug --label critical   # By labels (can repeat)
amq list --me claude --new --from codex --priority urgent # Combine filters
```

### Reply
```bash
amq reply --me claude --id <msg_id> --body "LGTM"
amq reply --me claude --id <msg_id> --kind review_response --body "See comments..."
```

### Dead Letter Queue
```bash
amq dlq list --me claude                  # List failed messages
amq dlq read --me claude --id <dlq_id>    # Inspect failure details
amq dlq retry --me claude --id <dlq_id>   # Retry (move back to inbox)
amq dlq retry --me claude --all [--force] # Retry all
amq dlq purge --me claude --older-than 24h # Clean old DLQ entries
```

### Upgrade
```bash
amq upgrade                    # Self-update to latest release
amq --no-update-check ...      # Disable update hint for this command
```

### Other
```bash
amq thread --id p2p/claude__codex --include-body        # View thread
amq presence set --me claude --status busy --note "reviewing"  # Set presence
amq cleanup --tmp-older-than 36h                        # Clean stale tmp
```

## Message Kinds

| Kind | Reply Kind | Default Priority | Use |
|------|------------|------------------|-----|
| `review_request` | `review_response` | normal | Code review |
| `review_response` | — | normal | Review feedback |
| `question` | `answer` | normal | Questions |
| `answer` | — | normal | Answers |
| `decision` | — | normal | Design decisions |
| `brainstorm` | — | low | Open discussion |
| `status` | — | low | FYI updates |
| `todo` | — | normal | Task assignments |

## Labels and Context

**Labels** tag messages for filtering:
```bash
amq send --to codex --labels "bug,urgent" --body "Critical issue"
```

**Context** provides structured metadata:
```bash
amq send --to codex --kind review_request \
  --context '{"paths": ["internal/cli/send.go"], "focus": "error handling"}' \
  --body "Please review"
```

## Conventions

- Handles: lowercase `[a-z0-9_-]+`
- Threads: `p2p/<agentA>__<agentB>` (lexicographic)
- Delivery: atomic Maildir (tmp -> new -> cur)
- Never edit message files directly

## References

Read these when you need deeper context:

- `references/coop-mode.md` — Read when setting up or debugging co-op workflows between agents
- `references/message-format.md` — Read when you need the full frontmatter schema (all fields, types, defaults)
