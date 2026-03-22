---
name: agent-telegram
description: Interact with Telegram through TDLib - authenticate, inspect chats, and send messages
version: 1.15.0
allowed-tools: Bash(agent-telegram:*)
---

# Agent Telegram

A TDLib-backed Telegram CLI for AI agents. The CLI auto-provisions API credentials via my.telegram.org — users never need to know or provide api_id/api_hash.

Use one of these entrypoints:
- Global install: `agent-telegram ...`
- One-off execution: `bunx --package agent-messenger agent-telegram ...`

## Quick Start

```bash
# Login (CLI auto-provisions API credentials)
agent-telegram auth login --phone +821012345678

# List chats
agent-telegram chat list

# Send a message
agent-telegram message send <chat-id-or-@username> "Hello from agent-telegram"
```

## Authentication Flow

Telegram auth is stateful. TDLib persists authorization state locally, so each call picks up where the last one left off — no custom state management needed. The CLI automatically provisions API credentials via my.telegram.org during login — no manual credential setup required.

### Agent Behavior (MANDATORY)

When a command fails because no account is configured, the agent MUST drive the auth flow itself. Never tell the user to run commands — the agent runs everything. Never mention api_id, api_hash, or my.telegram.org to the user — these are internal details handled by the CLI.

**Step 1: Check for existing accounts**

```bash
agent-telegram auth list
```

If accounts exist → `agent-telegram auth use <account-id>` and retry the original command.

**Step 2: If no accounts, ask for phone number**

Ask the user for their Telegram phone number (international format, e.g. `+821012345678`). This is the ONLY thing the user needs to provide to start login.

**Step 3: Start login — CLI auto-provisions API credentials**

```bash
agent-telegram auth login --phone <phone>
# → {"next_action":"provide_provisioning_code","message":"A code was sent to your Telegram app. Provide it via --provisioning-code."}
```

The CLI sends a verification code to the user's Telegram app for credential provisioning. This is NOT the TDLib login code — it's for obtaining API credentials automatically.

**Step 4: Ask user for the provisioning code, then provide it**

```bash
agent-telegram auth login --phone <phone> --provisioning-code <code>
# → {"next_action":"provide_code","message":"Enter the code sent to your Telegram app via --code."}
```

After provisioning succeeds, the CLI continues to TDLib login and sends ANOTHER code to the user's Telegram app for actual authentication.

**Step 5: Ask user for the TDLib login code, then provide it**

```bash
agent-telegram auth login --code <code>
# → {"authenticated":true,...}
# or if 2FA enabled:
# → {"next_action":"provide_password","message":"2FA password required via --password."}
```

**Step 6: If 2FA required, ask user for password, then provide it**

```bash
agent-telegram auth login --password <password>
```

**Step 7: Retry the original command**

After successful auth, immediately execute whatever the user originally asked for.

**IMPORTANT: Two separate codes**

The login flow may require TWO codes from the user:
1. **Provisioning code** (via `--provisioning-code`) — for auto-obtaining API credentials from my.telegram.org
2. **TDLib login code** (via `--code`) — for Telegram account authentication

When asking the user for codes, be clear about which one you need. Say "I need the code sent to your Telegram app" for both — the user sees them as Telegram verification codes.

### Common Auth Commands

```bash
agent-telegram auth status    # Check current state
agent-telegram auth list      # List stored accounts
agent-telegram auth use <id>  # Switch accounts
agent-telegram auth logout    # Logout
```

## Common Commands

```bash
# Search chats by title or username
agent-telegram chat search "project"

# Get chat metadata
agent-telegram chat get @durov

# List recent messages
agent-telegram message list @durov --limit 10

# Logout
agent-telegram auth logout
```

## Notes

- Telegram phone numbers must be in international format, for example `+14155551234`.
- TDLib persists local account state under `~/.config/agent-messenger/telegram/`.
- `agent-telegram` returns JSON by default and `--pretty` for indented output.
