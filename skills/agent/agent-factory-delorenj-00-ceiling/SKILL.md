---
name: agent-factory
description: Bootstrap new 33GOD ecosystem agents with standardized configuration. Use when creating new agents, spawning workers, deploying Yi nodes, or when the user says "spin up an agent", "create a new agent", "deploy a new worker", or needs a new agent for a specific pipeline role. Handles workspace creation, config injection, skill installation, provider mirroring, channel binding, and 33GOD ecosystem onboarding (GOD Docs, Plane, Bloodbank, memory).
---

# Agent Factory

Standardized bootstrap for 33GOD ecosystem agents. Every agent ships ready to:
- Consume and produce Bloodbank events
- Read/write GOD Docs
- Track work on Plane boards
- Communicate with Cack (boss) and peer agents
- Use long-term vector memory
- Authenticate against all configured providers

## Quick Start

When the user requests a new agent, gather these parameters:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `id` | ✅ | Agent ID (lowercase, no spaces, e.g. `scout`) |
| `name` | ✅ | Display name (e.g. `Scout`) |
| `role` | ✅ | One of: `manager`, `exec`, `ic`, `contractor` (see Yi Node Flavors) |
| `purpose` | ✅ | One-line mission statement |
| `personality` | ❌ | Vibe/tone (defaults to "competent, concise, team-player") |
| `channel` | ❌ | `telegram` (needs bot token) or `none` (sub-agent only) |
| `telegram_bot_token` | ❌ | If channel=telegram, the BotFather token |
| `telegram_account_id` | ❌ | Account ID for multi-bot setup (defaults to agent id) |
| `model` | ❌ | Model override (defaults to ecosystem default) |
| `skills` | ❌ | Additional skills beyond the base set |

## Bootstrap Procedure

### 1. Create Workspace

```bash
bash /home/delorenj/.openclaw/skills/agent-factory/scripts/bootstrap.sh \
  --id <id> \
  --name <name> \
  --role <role> \
  --purpose "<purpose>" \
  [--personality "<personality>"] \
  [--model "<model>"]
```

This creates `~/.openclaw/workspace-<id>/` with all template files populated.

### 2. Update Gateway Config

After running the bootstrap script, update `~/.openclaw/openclaw.json`:

**Add agent to `agents.list`:**
```json
{
  "id": "<id>",
  "name": "<name>",
  "workspace": "/home/delorenj/.openclaw/workspace-<id>",
  "identity": { "name": "<name>" }
}
```

**If Telegram channel, add to `channels.telegram.accounts`:**
```json
"<account_id>": {
  "name": "<name>",
  "dmPolicy": "pairing",
  "botToken": "<token>",
  "groupPolicy": "allowlist",
  "streamMode": "partial"
}
```

**Add binding to `bindings` array:**
```json
{
  "agentId": "<id>",
  "match": {
    "channel": "telegram",
    "accountId": "<account_id>"
  }
}
```

### 3. Restart Gateway

Use the `gateway` tool with `action: "restart"` to pick up the new agent.

### 4. Send Onboarding Briefing

After gateway restart, use `sessions_send` to the new agent's session (`agent:<id>:main`) with an onboarding message that includes:
- Their specific mission and current priorities
- Any immediate tasks from the Plane board
- Context about active projects they'll touch

## Yi Node Flavors (Role Types)

| Role | Memory | Can Delegate | Description |
|------|--------|-------------|-------------|
| `manager` | ✅ Persistent | ✅ Yes | Delegators only — coordinate, don't execute |
| `exec` | ✅ Persistent | ✅ Yes | Delegator + worker hybrid |
| `ic` | ✅ Persistent | ❌ No | Individual contributor with full context |
| `contractor` | ❌ Ephemeral | ❌ No | Stateless worker, task-scoped |

**Invariant:** Delegator ⇒ persistent memory required.

## Base Skills (auto-installed via symlink)

Every agent gets these skills symlinked from Cack's install:
- `33god-creating-and-working-with-projects`
- `33god-service-development`
- `33god-workflow-generator`
- `god-docs`
- `managing-tickets-and-tasks-in-plane`
- `github`
- `ecosystem-patterns`
- `installing-apps-tools-and-services`

Contractors get a minimal set: `github`, `installing-apps-tools-and-services` only.

## Template Files

The bootstrap script generates these from templates in `references/`:
- `AGENTS.md` — Role-aware agent instructions
- `SOUL.md` — Personality + ecosystem identity
- `USER.md` — Jarad's info (static)
- `IDENTITY.md` — Agent identity card
- `TOOLS.md` — Empty, agent fills as needed
- `MEMORY.md` — Pre-seeded with ecosystem context
- `HEARTBEAT.md` — Empty (agent configures as needed)
- `memory/` directory created

## Provider Auth

Providers are configured at the gateway level in `agents.defaults`, so all agents automatically inherit:
- anthropic, github-copilot, openai-codex, opencode, kimi-coding, google, google-antigravity, openrouter

No per-agent provider config needed — it's all in defaults.

## Conventions

- Workspace: `~/.openclaw/workspace-<id>/`
- Session key: `agent:<id>:main`
- Telegram account: matches agent id unless overridden
- All agents know Cack is the coordinator/boss
- All agents use `sessions_send` for inter-agent comms
- Plane workspace: `lasertoast` (API key in `~/DevCloud/plane.lasertoast.env`)
