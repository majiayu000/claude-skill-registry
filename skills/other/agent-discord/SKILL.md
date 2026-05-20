---
name: agent-discord
description: Interact with Discord servers - send messages, read channels, manage reactions
version: 1.15.0
allowed-tools: Bash(agent-discord:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-discord
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-discord]
---

# Agent Discord

A TypeScript CLI tool that enables AI agents and humans to interact with Discord servers through a simple command interface. Features seamless token extraction from the Discord desktop app and multi-server support.

## Quick Start

```bash
# Get server snapshot (credentials are extracted automatically)
agent-discord snapshot

# Send a message
agent-discord message send <channel-id> "Hello from AI agent!"

# List channels
agent-discord channel list
```

## Authentication

Credentials are extracted automatically from the Discord desktop app on first use. No manual setup required — just run any command and authentication happens silently in the background.

On macOS, the system may prompt for your Keychain password the first time (required to decrypt Discord's stored token). This is a one-time prompt.

**IMPORTANT**: NEVER guide the user to open a web browser, use DevTools, or manually copy tokens from a browser. Always use `agent-discord auth extract` to obtain tokens from the desktop app.

### Multi-Server Support

```bash
# List all available servers
agent-discord server list

# Switch to a different server
agent-discord server switch <server-id>

# Show current server
agent-discord server current

# Check auth status
agent-discord auth status
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered server IDs, channel IDs, user IDs, and preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering server IDs and names (from `server list`, `snapshot`, etc.)
- After discovering useful channel IDs and names (from `channel list`, `snapshot`, etc.)
- After discovering user IDs and names (from `user list`, `user me`, etc.)
- After the user gives you an alias or preference ("call this the dev server", "my main channel is X")
- After discovering channel structure (categories, voice channels)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Server IDs with names
- Channel IDs with names and categories
- User IDs with display names
- User-given aliases ("dev server", "announcements channel")
- Commonly used thread IDs
- Any user preference expressed during interaction

### What NOT to Store

Never store tokens, credentials, or any sensitive data. Never store full message content (just IDs and channel context). Never store file upload contents.

### Handling Stale Data

If a memorized ID returns an error (channel not found, server not found), remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Discord Servers

- `1234567890123456` — Acme Dev (default)
- `9876543210987654` — Open Source Community

## Channels (Acme Dev)

- `1111111111111111` — #general (General category)
- `2222222222222222` — #engineering (Engineering category)
- `3333333333333333` — #deploys (Engineering category)

## Users (Acme Dev)

- `4444444444444444` — Alice (server owner)
- `5555555555555555` — Bob

## Aliases

- "dev server" → `1234567890123456` (Acme Dev)
- "deploys" → `3333333333333333` (#deploys in Acme Dev)

## Notes

- User prefers --pretty output for snapshots
- Main server is "Acme Dev"
```

> Memory lets you skip repeated `channel list` and `server list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Extract token from Discord desktop app (usually automatic)
agent-discord auth extract
agent-discord auth extract --debug

# Check auth status
agent-discord auth status

# Logout from Discord
agent-discord auth logout
```

### Message Commands

```bash
# Send a message
agent-discord message send <channel-id> <content>
agent-discord message send 1234567890123456789 "Hello world"

# List messages
agent-discord message list <channel-id>
agent-discord message list 1234567890123456789 --limit 50

# Get a single message by ID
agent-discord message get <channel-id> <message-id>
agent-discord message get 1234567890123456789 9876543210987654321

# Delete a message
agent-discord message delete <channel-id> <message-id> --force

# Acknowledge/mark a message as read
agent-discord message ack <channel-id> <message-id>

# Search messages in current server
agent-discord message search <query>
agent-discord message search "project update" --limit 10
agent-discord message search "hello" --channel <channel-id> --author <user-id>
```

### Channel Commands

```bash
# List channels in current server (text channels only)
agent-discord channel list

# Get channel info
agent-discord channel info <channel-id>
agent-discord channel info 1234567890123456789

# Get channel history (alias for message list)
agent-discord channel history <channel-id> --limit 100
```

### Server Commands

```bash
# List all servers
agent-discord server list

# Get server info
agent-discord server info <server-id>

# Switch active server
agent-discord server switch <server-id>

# Show current server
agent-discord server current
```

### User Commands

```bash
# List server members
agent-discord user list

# Get user info
agent-discord user info <user-id>

# Get current user
agent-discord user me
```

### DM Commands

```bash
# List DM channels
agent-discord dm list

# Create a DM channel with a user
agent-discord dm create <user-id>
```

### Mention Commands

```bash
# List recent mentions
agent-discord mention list
agent-discord mention list --limit 50
agent-discord mention list --guild <server-id>
```

### Friend Commands

```bash
# List all relationships (friends, blocked, pending requests)
agent-discord friend list
agent-discord friend list --pretty
```

### Note Commands

```bash
# Get note for a user
agent-discord note get <user-id>

# Set note for a user
agent-discord note set <user-id> "Note content"
```

### Profile Commands

```bash
# Get detailed user profile
agent-discord profile get <user-id>
```

### Member Commands

```bash
# Search guild members
agent-discord member search <guild-id> <query>
agent-discord member search 1234567890123456789 "john" --limit 20
```

### Thread Commands

```bash
# Create a thread in a channel
agent-discord thread create <channel-id> <name>
agent-discord thread create 1234567890123456789 "Discussion" --auto-archive-duration 1440

# Archive a thread
agent-discord thread archive <thread-id>
```

### Reaction Commands

```bash
# Add reaction (use emoji name without colons)
agent-discord reaction add <channel-id> <message-id> <emoji>
agent-discord reaction add 1234567890123456789 9876543210987654321 thumbsup

# Remove reaction
agent-discord reaction remove <channel-id> <message-id> <emoji>

# List reactions on a message
agent-discord reaction list <channel-id> <message-id>
```

### File Commands

```bash
# Upload file
agent-discord file upload <channel-id> <path>
agent-discord file upload 1234567890123456789 ./report.pdf

# List files in channel
agent-discord file list <channel-id>

# Get file info
agent-discord file info <channel-id> <file-id>
```

### Snapshot Command

Get comprehensive server state for AI agents:

```bash
# Full snapshot
agent-discord snapshot

# Filtered snapshots
agent-discord snapshot --channels-only
agent-discord snapshot --users-only

# Limit messages per channel
agent-discord snapshot --limit 10
```

Returns JSON with:

- Server metadata (id, name)
- Channels (id, name, type, topic)
- Recent messages (id, content, author, timestamp)
- Members (id, username, global_name)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "1234567890123456789",
  "content": "Hello world",
  "author": "username",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-discord channel list --pretty
```

## Key Differences from Slack

| Feature             | Discord         | Slack              |
| ------------------- | --------------- | ------------------ |
| Server terminology  | Server          | Workspace          |
| Channel identifiers | Snowflake IDs   | Channel name or ID |
| Message identifiers | Snowflake IDs   | Timestamps (ts)    |
| Threads             | Thread ID field | Thread timestamp   |
| Mentions            | `<@user_id>`    | `<@USER_ID>`       |

**Important**: Discord uses Snowflake IDs (large numbers like `1234567890123456789`) for all identifiers. You cannot use channel names directly - use `channel list` to find IDs first.

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:

- `post-message.sh` - Send messages with error handling
- `monitor-channel.sh` - Monitor channel for new messages
- `server-summary.sh` - Generate server summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "Not authenticated. Run \"auth extract\" first."
}
```

Common errors:

- `Not authenticated`: No valid token (auto-extraction failed — see Troubleshooting)
- `No current server set`: Run `server switch <id>` first
- `Message not found`: Invalid message ID
- `Unknown Channel`: Invalid channel ID

## Configuration

Credentials stored in `~/.config/agent-messenger/discord-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

## Limitations

- No real-time events / Gateway connection
- No voice channel support
- No server management (create/delete channels, roles)
- No slash commands
- No webhook support
- Plain text messages only (no embeds in v1)
- User tokens only (no bot tokens)

## Troubleshooting

### `agent-discord: command not found`

**`agent-discord` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-discord` directly:

```bash
agent-discord server list
```

If the package is NOT installed, use `npx -y` by default. **Do NOT ask the user which package runner to use** — just run it:

```bash
npx -y agent-messenger discord server list
bunx agent-messenger discord server list
pnpm dlx agent-messenger discord server list
```

> If you already know the user's preferred package runner (e.g., `bunx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-discord`, `bunx agent-discord`, or `pnpm dlx agent-discord`** — it will fail or install a wrong package since `agent-discord` is not the npm package name.

For other troubleshooting (auth extraction, token issues, permissions), see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
