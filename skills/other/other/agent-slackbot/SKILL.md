---
name: agent-slackbot
description: Interact with Slack workspaces using bot tokens - send messages, read channels, manage reactions
version: 1.15.0
allowed-tools: Bash(agent-slackbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-slackbot
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-slackbot]
---

# Agent SlackBot

A TypeScript CLI tool that enables AI agents and humans to interact with Slack workspaces using bot tokens (xoxb-). Unlike agent-slack which extracts user tokens from the desktop app, agent-slackbot uses standard Slack Bot tokens for server-side and CI/CD integrations.

## Quick Start

```bash
# Set your bot token
agent-slackbot auth set xoxb-your-bot-token

# Or set with a custom bot identifier for multi-bot setups
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Verify authentication
agent-slackbot auth status

# Send a message
agent-slackbot message send C0ACZKTDDC0 "Hello from bot!"

# List channels
agent-slackbot channel list
```

## Authentication

### Bot Token Setup

agent-slackbot uses Slack Bot tokens (xoxb-) which you get from the Slack App configuration:

```bash
# Set bot token (validates against Slack API before saving)
agent-slackbot auth set xoxb-your-bot-token

# Set with a custom bot identifier
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Check auth status
agent-slackbot auth status

# Clear stored credentials
agent-slackbot auth clear
```

### Multi-Bot Management

Store multiple bot tokens and switch between them:

```bash
# Add multiple bots
agent-slackbot auth set xoxb-deploy-token --bot deploy --name "Deploy Bot"
agent-slackbot auth set xoxb-alert-token --bot alert --name "Alert Bot"

# List all stored bots
agent-slackbot auth list

# Switch active bot
agent-slackbot auth use deploy

# Use a specific bot for one command (without switching)
agent-slackbot message send C0ACZKTDDC0 "Alert!" --bot alert

# Remove a stored bot
agent-slackbot auth remove deploy

# Disambiguate bots with same ID across workspaces
agent-slackbot auth use T123456/deploy
```

The `--bot <id>` flag is available on all commands to override the active bot for a single invocation.

For bot token setup (Slack App creation, required scopes, app manifest) and CI/CD environment variables, see [references/authentication.md](references/authentication.md).

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered workspace IDs, channel IDs, user IDs, and preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering workspace IDs (from `auth status`)
- After discovering useful channel IDs and names (from `channel list`, etc.)
- After discovering user IDs and names (from `user list`, etc.)
- After the user gives you an alias or preference ("call this the alerts bot", "my main workspace is X")
- After setting up bot identifiers (from `auth list`)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Workspace IDs with names
- Channel IDs with names and purpose
- User IDs with display names
- Bot identifiers and their purposes
- User-given aliases ("alerts bot", "deploys channel")
- Any user preference expressed during interaction

### What NOT to Store

Never store bot tokens, credentials, or any sensitive data. Never store full message content (just IDs and channel context). Never store file upload contents.

### Handling Stale Data

If a memorized ID returns an error (channel not found, user not found), remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Slack Workspaces (Bot)

- `T0ABC1234` — Acme Corp

## Bots (Acme Corp)

- `deploy` — Deploy Bot (active)
- `alert` — Alert Bot

## Channels (Acme Corp)

- `C012ABC` — #general (company-wide announcements)
- `C034DEF` — #engineering (team discussion)
- `C056GHI` — #deploys (CI/CD notifications)

## Users (Acme Corp)

- `U0ABC123` — Alice (engineering lead)
- `U0DEF456` — Bob (backend)

## Aliases

- "deploys" → `C056GHI` (#deploys in Acme Corp)

## Notes

- Deploy Bot is used for CI/CD notifications
- Alert Bot is used for error monitoring
```

> Memory lets you skip repeated `channel list` and `auth list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Message Commands

```bash
# Send a message
agent-slackbot message send <channel> <text>
agent-slackbot message send C0ACZKTDDC0 "Hello world"

# Send a threaded reply
agent-slackbot message send C0ACZKTDDC0 "Reply" --thread <ts>

# List messages
agent-slackbot message list <channel>
agent-slackbot message list C0ACZKTDDC0 --limit 50

# Get a single message by timestamp
agent-slackbot message get <channel> <ts>

# Get thread replies (includes parent message)
agent-slackbot message replies <channel> <thread_ts>
agent-slackbot message replies C0ACZKTDDC0 1234567890.123456 --limit 50

# Update a message (bot's own messages only)
agent-slackbot message update <channel> <ts> <new-text>

# Delete a message (bot's own messages only)
agent-slackbot message delete <channel> <ts> --force
```

### Channel Commands

```bash
# List channels the bot can see
agent-slackbot channel list
agent-slackbot channel list --limit 50

# Get channel info
agent-slackbot channel info <channel>
agent-slackbot channel info C0ACZKTDDC0
```

### User Commands

```bash
# List users
agent-slackbot user list
agent-slackbot user list --limit 50

# Get user info
agent-slackbot user info <user-id>
```

### Reaction Commands

```bash
# Add reaction
agent-slackbot reaction add <channel> <ts> <emoji>
agent-slackbot reaction add C0ACZKTDDC0 1234567890.123456 thumbsup

# Remove reaction
agent-slackbot reaction remove <channel> <ts> <emoji>
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "ts": "1234567890.123456",
  "channel": "C0ACZKTDDC0",
  "text": "Hello world"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-slackbot channel list --pretty
```

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:

- `post-message.sh` - Send messages with error handling
- `monitor-channel.sh` - Monitor channel for new messages
- `workspace-summary.sh` - Generate workspace summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No credentials. Run \"auth set\" first."
}
```

Common errors:

- `missing_token`: No credentials configured
- `invalid_token_type`: Token is not a bot token (must start with xoxb-)
- `not_in_channel`: Bot needs to join the channel first
- `slack_webapi_rate_limited_error`: Hit rate limit (auto-retries with backoff)

## Configuration

Credentials stored in `~/.config/agent-messenger/slackbot-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

## Key Differences from agent-slack

| Feature              | agent-slack                     | agent-slackbot               |
| -------------------- | ------------------------------- | ---------------------------- |
| Token type           | User token (xoxc-)              | Bot token (xoxb-)            |
| Token source         | Auto-extracted from desktop app | Manual from Slack App config |
| Message search       | Yes                             | No (requires user token)     |
| File operations      | Yes                             | No                           |
| Snapshot             | Yes                             | No                           |
| Edit/delete messages | Any message                     | Bot's own messages only      |
| Workspace management | Multi-workspace                 | Multi-bot, multi-workspace   |
| CI/CD friendly       | Requires desktop app            | Yes (just set token)         |

## Limitations

- No real-time events / Socket Mode
- No message search (requires user token scope)
- No file upload/download
- No workspace snapshot
- Bot can only edit/delete its own messages
- Bot must be invited to private channels
- No scheduled messages
- Plain text messages only (no blocks/formatting)

## Troubleshooting

### `agent-slackbot: command not found`

**`agent-slackbot` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-slackbot` directly:

```bash
agent-slackbot message send general "Hello"
```

If the package is NOT installed, use `npx -y` by default. **Do NOT ask the user which package runner to use** — just run it:

```bash
npx -y agent-messenger slackbot message send general "Hello"
bunx agent-messenger slackbot message send general "Hello"
pnpm dlx agent-messenger slackbot message send general "Hello"
```

> If you already know the user's preferred package runner (e.g., `bunx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-slackbot`, `bunx agent-slackbot`, or `pnpm dlx agent-slackbot`** — it will fail or install a wrong package since `agent-slackbot` is not the npm package name.

For other troubleshooting (token issues, scopes, permissions), see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
