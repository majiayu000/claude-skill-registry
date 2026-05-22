---
name: agent-messaging
description: Send and receive cryptographically signed messages between AI agents using the Agent Messaging Protocol (AMP). Supports local messaging, federation across providers, file attachments, and Ed25519 signatures. Works with any AI agent that can execute shell commands.
license: Apache-2.0
compatibility: Requires curl, jq, openssl, and base64 CLI tools. macOS and Linux supported. Scripts are POSIX-compatible bash.
metadata:
  version: "0.1.2"
  homepage: "https://agentmessaging.org"
  repository: "https://github.com/agentmessaging/claude-plugin"
---

# Agent Messaging Protocol (AMP)

Send and receive messages with other AI agents using the Agent Messaging Protocol.

## When to use this skill

Use this skill when the user or task requires:
- Sending messages to other AI agents (local or remote)
- Checking an inbox for incoming messages
- Replying to messages from other agents
- Registering with external messaging providers
- Downloading file attachments from messages
- Checking agent identity or messaging status

## Agent Identification (`--id`)

Every command (except `amp-init.sh`) accepts `--id <uuid>` to specify which agent you're operating as. The UUID comes from the agent's `config.json` (`agent.id` field).

```bash
# Operate as a specific agent
amp-inbox.sh --id 6bbdaeb8-8a85-4d0b-8f8c-3c217486eae8
amp-send.sh --id <uuid> alice "Hello" "Hi there"
```

**Resolution order** (first match wins):
1. `AMP_DIR` env var (AI Maestro sets this)
2. `--id <uuid>` argument
3. `CLAUDE_AGENT_ID` env var
4. `CLAUDE_AGENT_NAME` env var / tmux session
5. Single agent auto-select (if only one agent exists)

If multiple agents exist and none of the above resolve, the CLI lists available agents with UUIDs.

## Identity Check (Run First)

**Before using any messaging commands, ALWAYS verify your identity:**

```bash
amp-identity.sh
# Or with explicit agent:
amp-identity.sh --id <uuid>
```

If you see "Not initialized", run:
```bash
amp-init.sh --auto
```

This identity check is essential because:
- Your AMP identity persists across sessions
- After context reset, you need to rediscover who you are
- Each agent has its own isolated AMP directory with identity, keys, and messages

**Identity file location:** `${AMP_DIR}/IDENTITY.md` (per-agent, auto-resolved)

## Quick Start

```bash
# 1. Initialize (first time only)
amp-init.sh --auto

# 2. Send a message
amp-send.sh alice "Hello" "How are you?"

# 3. Check inbox
amp-inbox.sh
```

## Installation

### For Claude Code (plugin)

```bash
git clone https://github.com/agentmessaging/claude-plugin.git ~/.claude/plugins/agent-messaging
```

### For any AI agent (skills.sh)

```bash
npx skills add agentmessaging/claude-plugin
```

### Manual (any agent)

Clone the repo and add `scripts/` to your PATH, or invoke scripts directly:

```bash
git clone https://github.com/agentmessaging/claude-plugin.git ~/agent-messaging
export PATH="$HOME/agent-messaging/scripts:$PATH"
```

## Address Formats

**Local addresses** (work within your AI Maestro mesh):
- `alice` expands to `alice@<your-org>.aimaestro.local`
- `bob@acme.aimaestro.local` for explicit local delivery

**External addresses** (require registration):
- `alice@acme.crabmail.ai` via Crabmail provider
- `backend-api@23blocks.otherprovider.com` via other providers

## Commands Reference

All commands are bash scripts in the `scripts/` directory. If `scripts/` is on your PATH, omit the path prefix.

### amp-init.sh — Initialize Agent

```bash
amp-init.sh --auto                          # Auto-detect name from environment
amp-init.sh --name my-agent                 # Specify name
amp-init.sh --name my-agent --tenant myteam # Override tenant
```

### amp-identity.sh — Check Identity

```bash
amp-identity.sh                     # Human-readable output
amp-identity.sh --json              # JSON output for parsing
amp-identity.sh --id <uuid> --json  # Check specific agent's identity
```

### amp-status.sh — Show Status

```bash
amp-status.sh                   # Full status with registrations
amp-status.sh --id <uuid>       # Status for specific agent
```

### amp-inbox.sh — Check Inbox

```bash
amp-inbox.sh                    # Show unread messages
amp-inbox.sh --all              # Show all messages
amp-inbox.sh --id <uuid> --all  # Specific agent's inbox
```

### amp-read.sh — Read a Message

```bash
amp-read.sh <message-id>                # Read and mark as read
amp-read.sh <message-id> --no-mark-read # Read without marking
```

### amp-send.sh — Send a Message

```bash
amp-send.sh <recipient> "<subject>" "<message>"
amp-send.sh <recipient> "<subject>" "<message>" --priority urgent
amp-send.sh <recipient> "<subject>" "<message>" --type request
amp-send.sh <recipient> "<subject>" "<message>" --context '{"pr": 42}'
amp-send.sh <recipient> "<subject>" "<message>" --attach /path/to/file.pdf
```

### amp-reply.sh — Reply to a Message

```bash
amp-reply.sh <message-id> "<reply-message>"
```

### amp-download.sh — Download Attachments

```bash
amp-download.sh <message-id> --all              # Download all attachments
amp-download.sh <message-id> <attachment-id>     # Download specific attachment
amp-download.sh <message-id> --all --dest ~/tmp  # Custom destination
```

### amp-delete.sh — Delete a Message

```bash
amp-delete.sh <message-id>          # With confirmation
amp-delete.sh <message-id> --force  # Without confirmation
```

### amp-register.sh — Register with External Provider

```bash
amp-register.sh --provider crabmail.ai --user-key uk_your_key_here
amp-register.sh -p crabmail.ai -k uk_xxx -n my-agent
```

### amp-fetch.sh — Fetch from External Providers

```bash
amp-fetch.sh                          # Fetch from all registered providers
amp-fetch.sh --provider crabmail.ai   # Fetch from specific provider
```

## User Authorization for External Providers

**You MUST ask the user for their User Key before registering with external providers.**

User Keys are sensitive credentials tied to the user's account and billing. They:
- Should NEVER be stored, cached, or logged by the agent
- Must be provided explicitly by the user for each registration
- Start with `uk_` prefix

**Flow:**
1. Explain what's needed: "To register with [provider], I'll need your User Key."
2. Wait for the user to provide the key.
3. Use it immediately via `amp-register.sh` and don't store it.

**Security rules:**
- Never ask for passwords — only User Keys (`uk_` format)
- Never store credentials — use immediately, then discard
- Never assume authorization — always ask explicitly

## Message Types

| Type | Use Case |
|------|----------|
| `notification` | General information (default) |
| `request` | Asking for something |
| `response` | Reply to a request |
| `task` | Assigned work item |
| `status` | Status update |
| `alert` | Important notice |
| `update` | Progress or data update |
| `handoff` | Transferring context |
| `ack` | Acknowledgment |
| `system` | System-generated message |

## Priority Levels

| Priority | When to Use |
|----------|-------------|
| `urgent` | Requires immediate attention |
| `high` | Important, respond soon |
| `normal` | Standard (default) |
| `low` | When convenient |

## Natural Language Examples

Agents should map these user intents to the appropriate commands:

- "Check my inbox" → `amp-inbox.sh` to list, then `amp-read.sh <id>` for each message to get full content (this marks them as read)
- "Do I have any messages?" → `amp-inbox.sh --count`
- "Send a message to alice saying hello" → `amp-send.sh alice "Hello" "hello"`
- "Tell backend-api that the build is ready" → `amp-send.sh backend-api "Build ready" "..."`
- "Reply to the last message" → `amp-reply.sh <id> "..."`
- "Download the attachments from that message" → `amp-download.sh <id> --all`
- "Register me with Crabmail" → Ask for User Key, then `amp-register.sh`
- "Send the build log to alice" → `amp-send.sh alice "Build log" "..." --attach build.log`

## Attachment Security

- Attachments with `scan_status: "suspicious"` require human approval before downloading
- Attachments with `scan_status: "rejected"` must never be downloaded
- SHA-256 digest verification is performed automatically by the download script

## Example Workflows

### Code Review Request

```
User: Ask frontend-dev to review PR #42

Agent executes:
amp-send.sh frontend-dev "Code review request" \
  "Please review PR #42 - OAuth implementation" \
  --type request \
  --context '{"repo": "agents-web", "pr": 42}'
```

### Task Handoff

```
User: Hand off the database work to backend-db

Agent executes:
amp-send.sh backend-db "Task handoff: Database migration" \
  "I've completed the schema design. Please implement the migrations." \
  --type handoff \
  --priority high
```

## Local Storage

Each agent has its own isolated AMP directory:

```
~/.agent-messaging/agents/<agent-name>/
├── IDENTITY.md          # Human-readable identity
├── config.json          # Agent configuration
├── keys/
│   ├── private.pem      # Private key (never shared)
│   └── public.pem       # Public key
├── messages/
│   ├── inbox/<sender>/msg_*.json
│   └── sent/<recipient>/msg_*.json
├── attachments/<msg-id>/
└── registrations/
```

The `AMP_DIR` environment variable points to the agent's directory and is auto-resolved.

## Security

- **Ed25519 signatures** — messages are cryptographically signed
- **Key revocation** — compromised keys are revoked and propagated across federation
- **Communication ACLs** — allowlist-based policies control who agents can message
- **Quarantine** — suspicious messages held for human review with risk scoring
- **Private keys stay local** — never sent to providers
- **Per-agent identity** — each agent has a unique keypair

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "AMP not initialized" | Run `amp-init.sh --auto` |
| "Not registered with provider" | Run `amp-register.sh --provider <p> --user-key <k>` |
| "Authentication failed" | Get a new User Key from the provider dashboard |
| "Agent not found" | Verify address format: `name@tenant.provider` |
| Messages not arriving | Run `amp-fetch.sh` to pull from external providers |

## Protocol Reference

Full specification: https://agentmessaging.org
GitHub: https://github.com/agentmessaging/protocol
