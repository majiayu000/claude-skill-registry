---
name: agent-channeltalkbot
description: Interact with Channel Talk workspaces using API credentials - send messages, read chats, manage groups and bots
version: 1.15.0
allowed-tools: Bash(agent-channeltalkbot:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-channeltalkbot
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-channeltalkbot]
---

# Agent ChannelBot

A TypeScript CLI tool that enables AI agents and humans to interact with Channel Talk workspaces using API credentials (Access Key + Access Secret). Designed for customer support automation, team inbox management, and CI/CD integrations.

## Key Concepts

Before diving in, a few things about Channel Talk's terminology:

- **Channel** = workspace (not a chat channel like Slack). The API calls it a "channel," but it means your entire workspace.
- **UserChats** = 1:1 conversations with end users (customers).
- **Groups** = team inbox channels (similar to Slack channels). Referenced by ID or `@name`.
- **Managers** = human agents on your team.
- **Bots** = automated agents that can send messages and close chats.
- **Messages** use a `blocks` format: `[{ type: "text", value: "..." }]`. The CLI handles this automatically when you pass plain text.

## Quick Start

```bash
# Set your API credentials
agent-channeltalkbot auth set your-access-key your-access-secret

# Verify authentication
agent-channeltalkbot auth status

# Get a workspace overview
agent-channeltalkbot snapshot --pretty

# Send a message to a UserChat
agent-channeltalkbot message send abc123-chat-id "Hello from the CLI!"

# Send a message to a Group
agent-channeltalkbot message send @support "Team update: deployment complete"
```

## Authentication

### API Credential Setup

agent-channeltalkbot uses Access Key + Access Secret pairs from Channel Talk's developer settings:

```bash
# Set credentials (validates against Channel Talk API before saving)
agent-channeltalkbot auth set your-access-key your-access-secret

# Check auth status
agent-channeltalkbot auth status

# Clear stored credentials
agent-channeltalkbot auth clear
```

For credential setup, multi-workspace management, and security details, see [references/authentication.md](references/authentication.md).

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed, the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered workspace IDs, group IDs, chat IDs, manager IDs, bot names, and preferences.

- If the file doesn't exist yet, that's fine. Proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory. Don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering workspace IDs and names (from `auth list`, `snapshot`, etc.)
- After discovering group IDs and names (from `group list`, `snapshot`, etc.)
- After discovering chat IDs (from `chat list`, etc.)
- After discovering manager IDs and names (from `manager list`, etc.)
- After discovering bot names (from `bot list`, etc.)
- After the user gives you an alias or preference ("call this the support workspace", "my main group is X")
- After setting a default bot name (from `auth bot`)

When writing, include the **complete file content**. The `Write` tool overwrites the entire file.

### What to Store

- Workspace IDs with names
- Group IDs with names (and `@name` aliases)
- UserChat IDs with context
- Manager IDs with names
- Bot names and their purposes
- Default bot name per workspace
- User-given aliases ("support workspace", "billing group")
- Any user preference expressed during interaction

### What NOT to Store

Never store access keys, access secrets, or any credentials. Never store full message content (just IDs and context). Never store personal user data.

### Handling Stale Data

If a memorized ID returns an error (chat not found, group not found), remove it from `MEMORY.md`. Don't blindly trust memorized data. Verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Channel Talk Workspaces

- `abc123` - Acme Support

## Default Bot (Acme Support)

- Support Bot

## Groups (Acme Support)

- `grp_111` - @support (Support Inbox)
- `grp_222` - @billing (Billing Inbox)
- `grp_333` - @engineering (Engineering)

## Recent UserChats (Acme Support)

- `uc_aaa` - John Doe inquiry (opened)
- `uc_bbb` - Refund request (closed)

## Managers (Acme Support)

- `mgr_001` - Alice (Team Lead)
- `mgr_002` - Bob (Support Agent)

## Bots (Acme Support)

- Support Bot (default, used for auto-replies)
- Notification Bot (used for alerts)

## Aliases

- "support" -> `grp_111` (@support in Acme Support)

## Notes

- Support Bot is used for closing chats and auto-replies
- Notification Bot is used for CI/CD alerts to @engineering
```

> Memory lets you skip repeated `group list` and `chat list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Set workspace credentials (validates against API)
agent-channeltalkbot auth set <access-key> <access-secret>

# Check auth status
agent-channeltalkbot auth status

# Clear all credentials
agent-channeltalkbot auth clear

# List stored workspaces
agent-channeltalkbot auth list

# Switch active workspace
agent-channeltalkbot auth use <workspace-id>

# Remove a stored workspace
agent-channeltalkbot auth remove <workspace-id>

# Set default bot name for sending messages
agent-channeltalkbot auth bot <name>
```

### Message Commands

```bash
# Send a message to a UserChat or Group
agent-channeltalkbot message send <target> <text>
agent-channeltalkbot message send abc123-chat-id "Hello!"
agent-channeltalkbot message send @support "Team update"

# List messages from a UserChat or Group
agent-channeltalkbot message list <target>
agent-channeltalkbot message list abc123-chat-id --limit 50

# Get a specific message by ID
# Note: Searches the latest 100 messages. Older messages may not be found.
agent-channeltalkbot message get <target> <message-id>

```

Target auto-detection: if the target starts with `@`, it's treated as a group. Otherwise, it's treated as a UserChat. You can override with `--type userchat` or `--type group`.

### Chat Commands (UserChats)

```bash
# List UserChats (default: opened)
agent-channeltalkbot chat list
agent-channeltalkbot chat list --state opened
agent-channeltalkbot chat list --state snoozed
agent-channeltalkbot chat list --state closed

# Get a specific UserChat
agent-channeltalkbot chat get <chat-id>

# Close a UserChat (requires --bot or default bot)
agent-channeltalkbot chat close <chat-id>
agent-channeltalkbot chat close <chat-id> --bot "Support Bot"

# Delete a UserChat (requires --force)
agent-channeltalkbot chat delete <chat-id> --force
```

### Group Commands

```bash
# List groups
agent-channeltalkbot group list

# Get a group by ID or @name
agent-channeltalkbot group get <group>
agent-channeltalkbot group get @support

# Get messages from a group
agent-channeltalkbot group messages <group>
agent-channeltalkbot group messages @support --limit 50
```

### Manager Commands

```bash
# List all managers
agent-channeltalkbot manager list

# Get a specific manager
agent-channeltalkbot manager get <manager-id>
```

### Bot Commands

```bash
# List all bots
agent-channeltalkbot bot list

# Create a new bot
agent-channeltalkbot bot create <name>
agent-channeltalkbot bot create "Deploy Bot" --color "#FF5733" --avatar-url "https://example.com/avatar.png"

# Delete a bot (requires --force)
agent-channeltalkbot bot delete <bot-id> --force
```

### Snapshot Command

Get comprehensive workspace state for AI agents:

```bash
# Full snapshot of current workspace
agent-channeltalkbot snapshot

# Filtered snapshots
agent-channeltalkbot snapshot --groups-only
agent-channeltalkbot snapshot --chats-only

# Limit messages per group/chat
agent-channeltalkbot snapshot --limit 10
```

Returns JSON with:

- Workspace metadata (id, name, homepage_url, description)
- Groups with recent messages (id, name, messages)
- UserChat summary (opened/snoozed/closed counts, recent opened with last message)
- Managers (id, name, description)
- Bots (id, name)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "msg_abc123",
  "chat_id": "uc_def456",
  "person_type": "bot",
  "plain_text": "Hello world",
  "created_at": 1705312200000
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-channeltalkbot group list --pretty
```

## Global Options

| Option             | Description                              |
| ------------------ | ---------------------------------------- |
| `--pretty`         | Human-readable output instead of JSON    |
| `--workspace <id>` | Use a specific workspace for this command |
| `--bot <name>`     | Use a specific bot name for this command |

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:

- `post-message.sh` - Send messages with error handling
- `monitor-chat.sh` - Poll for new UserChats
- `workspace-summary.sh` - Generate workspace summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No credentials. Run \"auth set <access-key> <access-secret>\" first."
}
```

Common errors: `No credentials`, `Workspace not found`, `Bot name is required`, `Use --force to confirm deletion`.

## Configuration

Credentials stored in `~/.config/agent-messenger/channelbot-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

Config format:

```json
{
  "current": { "workspace_id": "abc123" },
  "workspaces": {
    "abc123": {
      "workspace_id": "abc123",
      "workspace_name": "My Workspace",
      "access_key": "...",
      "access_secret": "..."
    }
  },
  "default_bot": "Support Bot"
}
```

## Limitations

- No real-time events / WebSocket connection
- No file upload support
- No message editing or deletion (Channel Talk API limitation)
- No user management (users are end-customers, managed by Channel Talk)
- No webhook support
- No message search (Channel Talk Open API does not provide a search endpoint)
- Plain text messages only (no rich blocks in v1)
- Bot name must exist in the workspace for sending messages
- Channel Talk has rate limits on API calls

## Troubleshooting

### `agent-channeltalkbot: command not found`

**`agent-channeltalkbot` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-channeltalkbot` directly:

```bash
agent-channeltalkbot message send abc123-chat-id "Hello"
```

If the package is NOT installed, run it directly with `npx -y`:

```bash
npx -y agent-messenger channeltalkbot message send abc123-chat-id "Hello"
```

> **Note**: If the user prefers a different package runner (e.g., `bunx`, `pnpx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-channeltalkbot`, `bunx agent-channeltalkbot`, or `pnpm dlx agent-channeltalkbot`**. It will fail or install a wrong package since `agent-channeltalkbot` is not the npm package name.

### How to get API credentials

1. Log in to [Channel Talk](https://app.channel.io/)
2. Go to **Settings > Developers > Open API**
3. Create or copy your **Access Key** and **Access Secret**
4. Run `agent-channeltalkbot auth set <access-key> <access-secret>`

### Rate limiting

Channel Talk enforces rate limits on API calls. The CLI automatically retries on rate limit (429) responses using the `Retry-After` header. For bulk operations, add delays between requests to avoid hitting limits.

### Bot name errors

Some operations (closing chats, sending messages) require a bot name. Set a default with `auth bot <name>` or pass `--bot <name>` per command. The bot must exist in your workspace. Use `bot list` to see available bots.

For other troubleshooting, see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
