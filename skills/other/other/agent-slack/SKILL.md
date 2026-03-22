---
name: agent-slack
description: Interact with Slack workspaces - send messages, read channels, manage reactions
version: 1.15.0
allowed-tools: Bash(agent-slack:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-slack
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-slack]
---

# Agent Slack

A TypeScript CLI tool that enables AI agents and humans to interact with Slack workspaces through a simple command interface. Features seamless token extraction from the Slack desktop app and multi-workspace support.

## Quick Start

```bash
# Get workspace snapshot (credentials are extracted automatically)
agent-slack snapshot

# Send a message
agent-slack message send general "Hello from AI agent!"

# List channels
agent-slack channel list
```

## Authentication

Credentials are extracted automatically from the Slack desktop app on first use. No manual setup required — just run any command and authentication happens silently in the background.

On macOS, the system may prompt for your Keychain password the first time (required to decrypt Slack's stored token). This is a one-time prompt.

**IMPORTANT**: NEVER guide the user to open a web browser, use DevTools, or manually copy tokens from a browser. Always use `agent-slack auth extract` to obtain tokens from the desktop app.

### Multi-Workspace Support

```bash
# List all authenticated workspaces
agent-slack workspace list

# Switch to a different workspace
agent-slack workspace switch <workspace-id>

# Show current workspace
agent-slack workspace current

# Remove a workspace
agent-slack workspace remove <workspace-id>

# Check auth status
agent-slack auth status
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered workspace IDs, channel IDs, user IDs, and preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering workspace IDs (from `workspace list`)
- After discovering useful channel IDs and names (from `channel list`, `snapshot`, etc.)
- After discovering user IDs and names (from `user list`, `user me`, etc.)
- After the user gives you an alias or preference ("call this the deploys channel", "my main workspace is X")
- After discovering channel structure (sidebar sections, channel categories)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Workspace IDs with names
- Channel IDs with names and purpose
- User IDs with display names
- User-given aliases ("deploys channel", "main workspace")
- Commonly used thread timestamps
- Any user preference expressed during interaction

### What NOT to Store

Never store tokens, cookies, credentials, or any sensitive data. Never store full message content (just IDs and channel context). Never store file upload contents.

### Handling Stale Data

If a memorized ID returns an error (channel not found, user not found), remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Slack Workspaces

- `T0ABC1234` — Acme Corp (default)
- `T0DEF5678` — Side Project

## Channels (Acme Corp)

- `C012ABC` — #general (company-wide announcements)
- `C034DEF` — #engineering (team discussion)
- `C056GHI` — #deploys (CI/CD notifications)

## Users (Acme Corp)

- `U0ABC123` — Alice (engineering lead)
- `U0DEF456` — Bob (backend)

## Aliases

- "deploys" → `C056GHI` (#deploys in Acme Corp)
- "main workspace" → `T0ABC1234` (Acme Corp)

## Notes

- User prefers --pretty output for snapshots
- Main workspace is "Acme Corp"
```

> Memory lets you skip repeated `channel list` and `workspace list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Extract tokens from Slack desktop app (usually automatic)
agent-slack auth extract
agent-slack auth extract --debug

# Check auth status
agent-slack auth status

# Logout from a workspace (defaults to current)
agent-slack auth logout
agent-slack auth logout <workspace-id>
```

### Message Commands

```bash
# Send a message
agent-slack message send <channel> <text>
agent-slack message send general "Hello world"

# Send a threaded reply
agent-slack message send general "Reply" --thread <ts>

# List messages
agent-slack message list <channel>
agent-slack message list general --limit 50

# Search messages across workspace
agent-slack message search <query>
agent-slack message search "project update"
agent-slack message search "from:@user deadline" --limit 50
agent-slack message search "in:#general meeting" --sort timestamp

# Get a single message by timestamp
agent-slack message get <channel> <ts>
agent-slack message get general 1234567890.123456

# Get thread replies (includes parent message)
agent-slack message replies <channel> <thread_ts>
agent-slack message replies general 1234567890.123456
agent-slack message replies general 1234567890.123456 --limit 50
agent-slack message replies general 1234567890.123456 --oldest 1234567890.000000
agent-slack message replies general 1234567890.123456 --cursor <next_cursor>

# Update a message
agent-slack message update <channel> <ts> <new-text>

# Delete a message
agent-slack message delete <channel> <ts> --force

# Schedule a message (post_at is a Unix timestamp)
agent-slack message schedule <channel> <text> <post-at>
agent-slack message schedule general "Friday update" 1700000000
agent-slack message schedule general "Thread reply" 1700000000 --thread 1234567890.123456

# List scheduled messages
agent-slack message scheduled-list
agent-slack message scheduled-list --channel general

# Delete a scheduled message
agent-slack message scheduled-delete <channel> <scheduled-message-id>

# Post ephemeral message (visible only to a specific user)
agent-slack message ephemeral <channel> <user-id> <text>

# Get a permanent link to a message
agent-slack message permalink <channel> <ts>
```

### Channel Commands

```bash
# List channels (excludes archived by default)
agent-slack channel list
agent-slack channel list --type public
agent-slack channel list --type private
agent-slack channel list --type dm
agent-slack channel list --include-archived

# Get channel info
agent-slack channel info <channel>
agent-slack channel info general

# Get channel history (alias for message list)
agent-slack channel history <channel> --limit 100

# Open a DM channel with a user (returns channel ID)
agent-slack channel open <user_id>
agent-slack channel open U0ABC123

# Open a group DM with multiple users
agent-slack channel open U0ABC123,U0DEF456

# List users in a channel
agent-slack channel users <channel>
agent-slack channel users general --include-bots

# Create a new channel
agent-slack channel create <name>
agent-slack channel create my-new-channel --private

# Archive a channel
agent-slack channel archive <channel>

# Set channel topic
agent-slack channel set-topic <channel> <topic>

# Set channel purpose
agent-slack channel set-purpose <channel> <purpose>

# Invite users to a channel (comma-separated user IDs)
agent-slack channel invite <channel> <users>
agent-slack channel invite general U0ABC123,U0DEF456

# Join a channel
agent-slack channel join <channel>

# Leave a channel
agent-slack channel leave <channel>
```

### User Commands

```bash
# List users
agent-slack user list
agent-slack user list --include-bots

# Get user info
agent-slack user info <user>

# Get current user
agent-slack user me

# Look up user by email
agent-slack user lookup <email>
agent-slack user lookup alice@example.com --pretty

# Get detailed user profile
agent-slack user profile <user-id>

# Set your status (emoji name without colons)
agent-slack user set-status <status-text>
agent-slack user set-status "In a meeting" --emoji calendar
agent-slack user set-status "On vacation" --emoji palm_tree --expiration 1700100000
```

### Reaction Commands

```bash
# Add reaction
agent-slack reaction add <channel> <ts> <emoji>
agent-slack reaction add general 1234567890.123456 thumbsup

# Remove reaction
agent-slack reaction remove <channel> <ts> <emoji>

# List reactions on a message
agent-slack reaction list <channel> <ts>
```

### File Commands

```bash
# Upload file
agent-slack file upload <channel> <path>
agent-slack file upload general ./report.pdf

# List files
agent-slack file list
agent-slack file list --channel general

# Get file info
agent-slack file info <file-id>

# Download file
agent-slack file download <file-id>
agent-slack file download <file-id> [output-path]
agent-slack file download F0ABC123 ./downloads/

# Delete a file
agent-slack file delete <file-id>
```

### Unread Commands

```bash
# Get unread counts for all channels
agent-slack unread counts

# Get thread subscription details
agent-slack unread threads <channel> <thread_ts>

# Mark channel as read up to timestamp
agent-slack unread mark <channel> <ts>
```

### Activity Commands

```bash
# List activity feed (mentions, reactions, replies)
agent-slack activity list
agent-slack activity list --limit 50
agent-slack activity list --unread
agent-slack activity list --types thread_reply,message_reaction
```

### Saved Items Commands

```bash
# List saved items
agent-slack saved list
agent-slack saved list --limit 10
agent-slack saved list --cursor <next_cursor>
```

### Drafts Commands

```bash
# List all drafts
agent-slack drafts list
agent-slack drafts list --limit 10
agent-slack drafts list --cursor <next_cursor>
```

### Channel Sections Commands

```bash
# List channel sections (sidebar organization)
agent-slack sections list
agent-slack sections list --pretty
```

### Pin Commands

```bash
# Pin a message
agent-slack pin add <channel> <ts>

# Unpin a message
agent-slack pin remove <channel> <ts>

# List pinned messages in a channel
agent-slack pin list <channel>
agent-slack pin list general --pretty
```

### Bookmark Commands

```bash
# Add a bookmark to a channel
agent-slack bookmark add <channel> <title> <link>
agent-slack bookmark add general "Our Docs" https://docs.example.com --emoji books --type link

# Edit a bookmark
agent-slack bookmark edit <channel> <bookmark-id> --title "New Title"
agent-slack bookmark edit <channel> <bookmark-id> --link https://new.example.com

# Remove a bookmark
agent-slack bookmark remove <channel> <bookmark-id>

# List bookmarks in a channel
agent-slack bookmark list <channel>
agent-slack bookmark list general --pretty
```

### Reminder Commands

```bash
# Add a reminder (time is a Unix timestamp)
agent-slack reminder add "Review PR" 1700000000
agent-slack reminder add "Team standup" 1700000000 --user U0ABC123

# List all reminders
agent-slack reminder list
agent-slack reminder list --pretty

# Complete a reminder
agent-slack reminder complete <reminder-id>

# Delete a reminder
agent-slack reminder delete <reminder-id>
```

### Emoji Commands

```bash
# List all custom emoji in the workspace
agent-slack emoji list
agent-slack emoji list --pretty
```

### Snapshot Command

Get comprehensive workspace state for AI agents:

```bash
# Full snapshot
agent-slack snapshot

# Filtered snapshots
agent-slack snapshot --channels-only
agent-slack snapshot --users-only

# Limit messages per channel
agent-slack snapshot --limit 10
```

Returns JSON with:

- Workspace metadata
- Channels (id, name, topic, purpose)
- Recent messages (ts, text, user, channel)
- Users (id, name, profile)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "ts": "1234567890.123456",
  "text": "Hello world",
  "channel": "C123456"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-slack channel list --pretty
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
  "error": "No workspace authenticated. Run: agent-slack auth extract"
}
```

Common errors:

- `NO_WORKSPACE`: No authenticated workspace (auto-extraction failed — see Troubleshooting)
- `SLACK_API_ERROR`: Slack API returned an error
- `RATE_LIMIT`: Hit Slack rate limit (auto-retries with backoff)

## Configuration

Credentials stored in `~/.config/agent-messenger/slack-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

## SDK: Real-Time Events

`SlackListener` connects to Slack's RTM WebSocket for instant event streaming. No polling — events arrive in real time.

### Setup

```typescript
import { SlackClient, SlackListener } from 'agent-messenger/slack'

const client = new SlackClient(token, cookie)
const listener = new SlackListener(client)
```

### Listening for Events

```typescript
listener.on('connected', (info) => {
  console.log(`Connected as ${info.self.id} on ${info.team.id}`)
})

listener.on('message', (event) => {
  // event.type, event.channel, event.user, event.text, event.ts
})

listener.on('reaction_added', (event) => {
  // event.user, event.reaction, event.item.channel, event.item.ts
})

listener.on('reaction_removed', (event) => {
  // same shape as reaction_added
})

listener.on('member_joined_channel', (event) => {
  // event.user, event.channel
})

listener.on('member_left_channel', (event) => {
  // event.user, event.channel
})

listener.on('user_typing', (event) => {
  // event.user, event.channel
})

listener.on('presence_change', (event) => {
  // event.user, event.presence ('active' | 'away')
})

// Catch-all for any RTM event type
listener.on('slack_event', (event) => {
  // event.type + all fields
})

listener.on('error', (err) => {
  console.error(err.message)
})

listener.on('disconnected', () => {
  // auto-reconnects with exponential backoff
})
```

### Lifecycle

```typescript
await listener.start()  // connects via RTM WebSocket
listener.stop()         // clean shutdown
```

### Event Types

| Event | Description |
|-------|-------------|
| `message` | New message, edit, delete, thread reply, join/leave subtypes |
| `reaction_added` | Reaction added to a message |
| `reaction_removed` | Reaction removed from a message |
| `member_joined_channel` | User joined a channel |
| `member_left_channel` | User left a channel |
| `user_typing` | User is typing |
| `presence_change` | User went active/away |
| `channel_created` | New channel created |
| `channel_deleted` | Channel deleted |
| `channel_rename` | Channel renamed |
| `channel_archive` | Channel archived |
| `channel_unarchive` | Channel unarchived |
| `slack_event` | Catch-all for every RTM event |
| `connected` | WebSocket connected |
| `disconnected` | WebSocket disconnected (auto-reconnects) |
| `error` | Connection or API error |

### Notes

- Receives all workspace events for the authenticated user — no channel subscription needed
- Auto-reconnects with exponential backoff (1s → 30s max)
- Ping/pong keepalive every 30s
- Uses Slack's RTM API with xoxc user tokens

## Limitations

- No workspace admin operations
- Plain text messages only (no blocks/formatting in v1)

## Troubleshooting

### `agent-slack: command not found`

**`agent-slack` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-slack` directly:

```bash
agent-slack message list general
```

If the package is NOT installed, use `npx -y` by default. **Do NOT ask the user which package runner to use** — just run it:

```bash
npx -y agent-messenger slack message list general
bunx agent-messenger slack message list general
pnpm dlx agent-messenger slack message list general
```

> If you already know the user's preferred package runner (e.g., `bunx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-slack`, `bunx agent-slack`, or `pnpm dlx agent-slack`** — a separate, unrelated npm package named `agent-slack` exists on npm. It will silently install the **wrong package** with different (fewer) commands.

### `Failed to read Slack cookies`

If you see:

```json
{"error":"Failed to read Slack cookies. The Slack app is currently running and locking the cookie database. Quit the Slack app completely and try again."}
```

Tell the user you need to quit the Slack app to extract credentials, and ask for confirmation. If the user agrees, quit Slack and retry the command.

For other troubleshooting (auth extraction, token issues, Keychain), see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
