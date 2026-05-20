---
name: agent-channeltalk
description: Interact with Channel Talk using extracted desktop app credentials - read chats, send messages, search messages, manage groups
version: 1.15.0
allowed-tools: Bash(agent-channeltalk:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-channeltalk
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-channeltalk]
---

# Agent Channel

A TypeScript CLI tool that enables AI agents and humans to interact with Channel Talk workspaces through a simple command interface. Features zero-config credential extraction from the Channel Talk desktop app and multi-workspace support.

## Key Concepts

Before diving in, a few things about Channel Talk's terminology:

- **Channel** = workspace (not a chat channel like Slack). The API calls it a "channel," but it means your entire workspace.
- **UserChats** = 1:1 conversations with end users (customers).
- **Groups** = team inbox channels (similar to Slack channels). Referenced by ID.
- **DirectChats** = direct messages between managers.
- **Managers** = human agents on your team.
- **Bots** = automated agents in the workspace.
- **Messages** use a `blocks` format: `[{ type: "text", value: "..." }]`. The CLI handles this automatically when you pass plain text.

## Quick Start

```bash
# Get workspace snapshot (credentials are extracted automatically)
agent-channeltalk snapshot --pretty

# Send a message to a group
agent-channeltalk message send group grp_abc123 "Hello from the CLI!"

# Send a message to a user chat
agent-channeltalk message send user-chat uc_abc123 "Thanks for reaching out!"

# List user chats
agent-channeltalk chat list
```

## Authentication

Credentials are extracted automatically from the Channel Talk desktop app on first use. No manual setup required, no API keys needed. Just run any command and authentication happens silently in the background.

The Channel Talk desktop app stores auth cookies in a SQLite database. On macOS, cookies are plaintext and no Keychain prompt is needed. On Windows, cookies are DPAPI-encrypted and decrypted automatically. The CLI reads two cookies:

- `x-account` (JWT) - your account identity
- `ch-session-1` (JWT) - your session token

These cookies expire after roughly 30 days. When they expire, the CLI automatically re-extracts fresh cookies from the desktop app on the next command.

**IMPORTANT**: NEVER guide the user to open a web browser, use DevTools, or manually copy tokens. Always use `agent-channeltalk auth extract` to obtain credentials from the desktop app.

### Multi-Workspace Support

If you're logged into multiple Channel Talk workspaces, all are discovered automatically. The first workspace is selected by default.

```bash
# List all available workspaces
agent-channeltalk auth list

# Switch to a different workspace
agent-channeltalk auth use <workspace-id>

# Check auth status
agent-channeltalk auth status

# Remove a stored workspace
agent-channeltalk auth remove <workspace-id>
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed, the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered workspace IDs, group IDs, chat IDs, manager IDs, and preferences.

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

When writing, include the **complete file content**. The `Write` tool overwrites the entire file.

### What to Store

- Workspace IDs with names
- Group IDs with names
- UserChat IDs with context
- Manager IDs with names
- Bot IDs with names
- User-given aliases ("support workspace", "billing group")
- Any user preference expressed during interaction

### What NOT to Store

Never store cookies, tokens, credentials, or any sensitive data. Never store full message content (just IDs and context). Never store personal user data.

### Handling Stale Data

If a memorized ID returns an error (chat not found, group not found), remove it from `MEMORY.md`. Don't blindly trust memorized data. Verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## Channel Talk Workspaces

- `abc123` - Acme Support

## Groups (Acme Support)

- `grp_111` - Support Inbox
- `grp_222` - Billing Inbox
- `grp_333` - Engineering

## Recent UserChats (Acme Support)

- `uc_aaa` - John Doe inquiry (opened)
- `uc_bbb` - Refund request (closed)

## Managers (Acme Support)

- `mgr_001` - Alice (Team Lead)
- `mgr_002` - Bob (Support Agent)

## Bots (Acme Support)

- `bot_001` - Support Bot
- `bot_002` - Notification Bot

## Aliases

- "support" -> `grp_111` (Support Inbox in Acme Support)

## Notes

- User prefers --pretty output for snapshots
- Main workspace is "Acme Support"
```

> Memory lets you skip repeated `group list` and `chat list` calls. When you already know an ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Extract cookies from Channel Talk desktop app (usually automatic)
agent-channeltalk auth extract

# Check auth status
agent-channeltalk auth status
agent-channeltalk auth status --workspace <id>

# Clear all stored credentials
agent-channeltalk auth clear

# List all stored workspaces
agent-channeltalk auth list

# Switch active workspace
agent-channeltalk auth use <workspace-id>

# Remove a stored workspace
agent-channeltalk auth remove <workspace-id>
```

### Message Commands

```bash
# Send a message (chat-type: group, user-chat, or direct-chat)
agent-channeltalk message send <chat-type> <chat-id> <text>
agent-channeltalk message send group grp_abc123 "Hello team!"
agent-channeltalk message send user-chat uc_abc123 "Thanks for reaching out!"
agent-channeltalk message send direct-chat dc_abc123 "Quick question..."

# List messages from a group, user chat, or direct chat
agent-channeltalk message list <chat-type> <chat-id>
agent-channeltalk message list group grp_abc123 --limit 50
agent-channeltalk message list user-chat uc_abc123 --sort asc

# Get a specific message by ID
agent-channeltalk message get <chat-type> <chat-id> <message-id>

# Search messages across team chats or user chats
agent-channeltalk message search <query>
agent-channeltalk message search "deployment" --scope team-chat
agent-channeltalk message search "refund" --scope user-chat --limit 10
```

### Chat Commands (UserChats)

```bash
# List user chats assigned to me (default: opened)
agent-channeltalk chat list
agent-channeltalk chat list --state opened
agent-channeltalk chat list --state snoozed
agent-channeltalk chat list --state closed
agent-channeltalk chat list --limit 50

# Get a specific user chat
agent-channeltalk chat get <chat-id>
```

### Group Commands

```bash
# List groups
agent-channeltalk group list
agent-channeltalk group list --limit 50

# Get a group by ID
agent-channeltalk group get <group-id>

# Get messages from a group
agent-channeltalk group messages <group-id>
agent-channeltalk group messages grp_abc123 --limit 50 --sort asc
```

### Manager Commands

```bash
# List all managers
agent-channeltalk manager list
agent-channeltalk manager list --limit 50
```

### Bot Commands

```bash
# List all bots
agent-channeltalk bot list
agent-channeltalk bot list --limit 50
```

### Snapshot Command

Get comprehensive workspace state for AI agents:

```bash
# Full snapshot of current workspace
agent-channeltalk snapshot

# Filtered snapshots
agent-channeltalk snapshot --groups-only
agent-channeltalk snapshot --chats-only

# Limit messages per group/chat
agent-channeltalk snapshot --limit 10
```

Returns JSON with:

- Workspace metadata (id, name)
- Groups with recent messages (id, name, messages)
- UserChat summary (total count, by state, recent opened)
- Managers (id, name, email)
- Bots (id, name)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "msg_abc123",
  "channel_id": "ch_def456",
  "chat_id": "uc_ghi789",
  "chat_type": "user-chat",
  "person_type": "manager",
  "plain_text": "Hello world",
  "created_at": 1705312200000
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-channeltalk group list --pretty
```

## Global Options

| Option             | Description                              |
| ------------------ | ---------------------------------------- |
| `--pretty`         | Human-readable output instead of JSON    |
| `--workspace <id>` | Use a specific workspace for this command |

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
  "error": "No credentials. Run \"agent-channeltalk auth extract\" first."
}
```

Common errors: `No credentials`, `Workspace not found`, `Invalid --limit value`.

## Configuration

Credentials stored in `~/.config/agent-messenger/channel-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

Config format:

```json
{
  "current": { "workspace_id": "abc123" },
  "workspaces": {
    "abc123": {
      "workspace_id": "abc123",
      "workspace_name": "Acme Support",
      "account_id": "acc_001",
      "account_name": "Alice",
      "account_cookie": "...",
      "session_cookie": "..."
    }
  }
}
```

## Feature Comparison: agent-channeltalk vs agent-channeltalkbot

| Feature                    | agent-channeltalk (user) | agent-channeltalkbot (bot) |
| -------------------------- | :------------------: | :--------------------: |
| Auth method                | Auto-extract cookies | API key + secret       |
| Setup required             | None (zero-config)   | Manual key setup       |
| Acts as                    | You (manager)        | Bot identity           |
| Send messages              | ✅                   | ✅                     |
| List messages              | ✅                   | ✅                     |
| Search messages            | ✅                   | -                      |
| Close/delete chats         | -                    | ✅                     |
| Create/delete bots         | -                    | ✅                     |
| Set default bot            | -                    | ✅                     |
| Group @name references     | -                    | ✅                     |
| Direct chat support        | ✅                   | -                      |
| Multi-workspace            | ✅                   | ✅                     |
| CI/CD friendly             | -                    | ✅                     |

Use **agent-channeltalk** when you want zero-config access acting as yourself. Use **agent-channeltalkbot** for server-side automation, CI/CD pipelines, or when you need bot-specific features like closing chats.

## Limitations

- macOS and Windows only (Channel Talk desktop app required)
- No real-time events / WebSocket connection
- No file upload support
- No message editing or deletion
- No chat close/delete (use agent-channeltalkbot for chat management)
- No bot creation/deletion (use agent-channeltalkbot for bot management)
- No @name group references (use group IDs from `group list`)
- Plain text messages only (no rich blocks in v1)
- Cookies expire after ~30 days (auto-re-extracted)

## Troubleshooting

### `agent-channeltalk: command not found`

**`agent-channeltalk` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-channeltalk` directly:

```bash
agent-channeltalk snapshot --pretty
```

If the package is NOT installed, run it directly with `npx -y`:

```bash
npx -y agent-messenger channeltalk snapshot --pretty
```

> **Note**: If the user prefers a different package runner (e.g., `bunx`, `pnpx`, `pnpm dlx`), use that instead.

**NEVER run `npx agent-channeltalk`, `bunx agent-channeltalk`, or `pnpm dlx agent-channeltalk`**. It will fail or install a wrong package since `agent-channeltalk` is not the npm package name.

### Channel Talk desktop app not found

The CLI looks for the Channel Talk desktop app's cookie database in these locations:

**macOS:**
1. `~/Library/Containers/com.zoyi.channel.desk.osx/Data/Library/Application Support/Channel Talk/Cookies` (Mac App Store version)
2. `~/Library/Application Support/Channel Talk/Cookies` (direct download / Electron version)

**Windows:**
1. `%APPDATA%\Channel Talk\Network\Cookies`

If none exist, install the Channel Talk desktop app and log in.

### Cookies expired

Cookies expire after roughly 30 days. The CLI automatically re-extracts on the next command. If auto-extraction fails:

1. Open the Channel Talk desktop app
2. Make sure you're logged in
3. Run `agent-channeltalk auth extract`

For other troubleshooting, see [references/authentication.md](references/authentication.md).

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
