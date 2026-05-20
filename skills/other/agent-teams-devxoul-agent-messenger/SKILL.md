---
name: agent-teams
description: Interact with Microsoft Teams - send messages, read channels, manage reactions
version: 1.15.0
allowed-tools: Bash(agent-teams:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-teams
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-teams]
---

# Agent Teams

A TypeScript CLI tool that enables AI agents and humans to interact with Microsoft Teams through a simple command interface. Features seamless token extraction from the Teams desktop app and multi-team support.

## Quick Start

```bash
# Get team snapshot (credentials are extracted automatically)
agent-teams snapshot

# Send a message
agent-teams message send <team-id> <channel-id> "Hello from AI agent!"

# List channels
agent-teams channel list <team-id>
```

## Authentication

Credentials are extracted automatically from the Teams desktop app on first use. No manual setup required — just run any command and authentication happens silently in the background.

Teams tokens expire in 60-90 minutes. The CLI automatically re-extracts a fresh token when the current one expires, so you don't need to manage token lifecycle manually.

**IMPORTANT**: NEVER guide the user to open a web browser, use DevTools, or manually copy tokens from a browser. Always use `agent-teams auth extract` to obtain tokens from the desktop app.

### Multi-Team Support

```bash
# List all available teams
agent-teams team list

# Switch to a different team
agent-teams team switch <team-id>

# Show current team
agent-teams team current

# Check auth status (includes token expiry info)
agent-teams auth status
```

### Multi-Account Support (Work / Personal)

```bash
# Switch between work and personal accounts
agent-teams auth switch-account work
agent-teams auth switch-account personal

# Use a specific account for one command (without switching)
agent-teams snapshot --account work
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered team IDs, channel IDs, user IDs, and preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering team IDs and names (from `team list`, `snapshot`, etc.)
- After discovering useful channel IDs and names (from `channel list`, `snapshot`, etc.)
- After discovering user IDs and names (from `user list`, `user me`, etc.)
- After the user gives you an alias or preference ("call this the standup channel", "my main team is X")
- After discovering channel structure (standard vs private channels)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Team IDs with names
- Channel IDs with names and team context
- User IDs with display names
- User-given aliases ("standup channel", "main team")
- Account preferences (work vs personal)
- Any user preference expressed during interaction

### What NOT to Store

Never store tokens, credentials, or any sensitive data. Never store full message content (just IDs and channel context). Never store file upload contents.

### Handling Stale Data

If a memorized ID returns an error (channel not found, team not found), remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Teams

- `team-id-1` — Acme Corp (default, work account)
- `team-id-2` — Side Project (personal account)

## Channels (Acme Corp)

- `channel-id-1` — General
- `channel-id-2` — Engineering
- `channel-id-3` — Standups

## Users (Acme Corp)

- `user-id-1` — Alice (engineering lead)
- `user-id-2` — Bob (backend)

## Aliases

- "standup" → `channel-id-3` (Standups in Acme Corp)
- "main team" → `team-id-1` (Acme Corp)

## Notes

- User prefers work account by default
- Main team is "Acme Corp"
```

> Memory lets you skip repeated `channel list` and `team list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Extract token from Teams desktop app (usually automatic)
agent-teams auth extract
agent-teams auth extract --debug

# Check auth status (includes token expiry info)
agent-teams auth status

# Logout from Microsoft Teams
agent-teams auth logout

# Switch between work and personal accounts
agent-teams auth switch-account <account-type>
agent-teams auth switch-account work
agent-teams auth switch-account personal
```

### Message Commands

```bash
# Send a message
agent-teams message send <team-id> <channel-id> <content>
agent-teams message send <team-id> 19:abc123@thread.tacv2 "Hello world"

# List messages
agent-teams message list <team-id> <channel-id>
agent-teams message list <team-id> 19:abc123@thread.tacv2 --limit 50

# Get a single message by ID
agent-teams message get <team-id> <channel-id> <message-id>

# Delete a message
agent-teams message delete <team-id> <channel-id> <message-id> --force
```

### Channel Commands

```bash
# List channels in a team
agent-teams channel list <team-id>

# Get channel info
agent-teams channel info <team-id> <channel-id>
agent-teams channel info <team-id> 19:abc123@thread.tacv2

# Get channel history (alias for message list)
agent-teams channel history <team-id> <channel-id> --limit 100
```

### Team Commands

```bash
# List all teams
agent-teams team list

# Get team info
agent-teams team info <team-id>

# Switch active team
agent-teams team switch <team-id>

# Show current team
agent-teams team current

# Remove a team from config
agent-teams team remove <team-id>
```

### User Commands

```bash
# List team members
agent-teams user list <team-id>

# Get user info
agent-teams user info <user-id>

# Get current user
agent-teams user me
```

### Reaction Commands

```bash
# Add reaction (use emoji name)
agent-teams reaction add <team-id> <channel-id> <message-id> <emoji>
agent-teams reaction add <team-id> 19:abc123@thread.tacv2 1234567890 like

# Remove reaction
agent-teams reaction remove <team-id> <channel-id> <message-id> <emoji>
```

### File Commands

```bash
# Upload file
agent-teams file upload <team-id> <channel-id> <path>
agent-teams file upload <team-id> 19:abc123@thread.tacv2 ./report.pdf

# List files in channel
agent-teams file list <team-id> <channel-id>

# Get file info
agent-teams file info <team-id> <channel-id> <file-id>
```

### Snapshot Command

Get comprehensive team state for AI agents:

```bash
# Full snapshot
agent-teams snapshot

# Filtered snapshots
agent-teams snapshot --channels-only
agent-teams snapshot --users-only

# Limit messages per channel
agent-teams snapshot --limit 10
```

Returns JSON with:

- Team metadata (id, name)
- Channels (id, name, type, description)
- Recent messages (id, content, author, timestamp)
- Members (id, displayName, email)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "19:abc123@thread.tacv2",
  "content": "Hello world",
  "author": "John Doe",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-teams channel list --pretty
```

## Key Differences from Discord/Slack

| Feature             | Teams                             | Discord        | Slack              |
| ------------------- | --------------------------------- | -------------- | ------------------ |
| Server terminology  | Team                              | Guild          | Workspace          |
| Channel identifiers | UUID format (19:xxx@thread.tacv2) | Snowflake IDs  | Channel name or ID |
| Token storage       | Cookies SQLite                    | LevelDB        | LevelDB            |
| Token expiry        | **60-90 minutes**                 | Rarely expires | Rarely expires     |
| Mentions            | `<at id="user-id">Name</at>`      | `<@user_id>`   | `<@USER_ID>`       |

**Important**: Teams uses UUID-style channel IDs (like `19:abc123@thread.tacv2`). You cannot use channel names directly - use `channel list` to find IDs first.

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:

- `post-message.sh` - Send messages with error handling
- `monitor-channel.sh` - Monitor channel for new messages (with token refresh)
- `team-summary.sh` - Generate team summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "Not authenticated. Run \"auth extract\" first."
}
```

Common errors:

- `Not authenticated`: No valid token (auto-extraction failed — see Troubleshooting)
- `Token expired`: Token has expired and auto-refresh failed — see Troubleshooting
- `No current team set`: Run `team switch <id>` first
- `Message not found`: Invalid message ID
- `Channel not found`: Invalid channel ID
- `401 Unauthorized`: Token expired and auto-refresh failed — see Troubleshooting

## Configuration

Credentials stored in `~/.config/agent-messenger/teams-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

## Limitations

- No real-time events / WebSocket connection
- No voice/video channel support
- No team management (create/delete channels, roles)
- No meeting support
- No webhook support
- Plain text messages only (no adaptive cards in v1)
- User tokens only (no app tokens)
- **Token expires in 60-90 minutes** - auto-refreshed, but requires Teams desktop app to be logged in

## Troubleshooting

### `agent-teams: command not found`

**`agent-teams` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-teams` directly:

```bash
agent-teams team list
```

If the package is NOT installed, use `npx -y` by default. **Do NOT ask the user which package runner to use** — just run it:

```bash
npx -y agent-messenger teams team list
bunx agent-messenger teams team list
pnpm dlx agent-messenger teams team list
```

> If you already know the user's preferred package runner (e.g., `bunx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-teams`, `bunx agent-teams`, or `pnpm dlx agent-teams`** — it will fail or install a wrong package since `agent-teams` is not the npm package name.

For other troubleshooting (auth extraction, token expiry, permissions), see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
