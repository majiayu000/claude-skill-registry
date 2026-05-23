---
name: agent-kakaotalk
description: Interact with KakaoTalk - send messages, read chats, manage conversations
version: 1.15.0
allowed-tools: Bash(agent-kakaotalk:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-kakaotalk
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-kakaotalk]
---

# Agent KakaoTalk

A TypeScript CLI tool that enables AI agents and humans to interact with KakaoTalk through a simple command interface. Features credential extraction from the KakaoTalk desktop app and sub-device login that keeps your desktop app running.

## Key Concepts

Before diving in, a few things about KakaoTalk's architecture:

- **LOCO protocol** = KakaoTalk's binary messaging protocol. The CLI handles this internally — you never interact with it directly.
- **Chat rooms** = conversations (1:1, group, or open chat). Referenced by numeric chat ID.
- **Device slots** = KakaoTalk allows one phone + one PC + one tablet session. The CLI registers as a **tablet** by default to avoid kicking your desktop app.
- **Sub-device** = a secondary device (PC or tablet). The CLI logs in as a sub-device, so your phone session is never affected.
- **Passcode verification** = when registering a new device, KakaoTalk displays a code on screen that you confirm on your phone.
- **Log ID** = a unique numeric identifier for each message, used for pagination.

## Quick Start

```bash
# Login (recommended — registers as sub-device, desktop app stays running)
agent-kakaotalk auth login

# Or extract credentials from desktop app (kicks desktop session)
agent-kakaotalk auth extract

# List chat rooms
agent-kakaotalk chat list

# Send a message
agent-kakaotalk message send <chat-id> "Hello from AI agent!"

# List messages in a chat
agent-kakaotalk message list <chat-id>
```

## Authentication

KakaoTalk offers two authentication methods:

### Method 1: Login (Recommended)

Registers the CLI as a sub-device (tablet slot by default). Your desktop app keeps running.

```bash
agent-kakaotalk auth login
```

In interactive mode, this prompts for email and password. The CLI first tries to extract cached credentials from the desktop app so you may not need to type anything.

For AI agents (non-interactive), provide credentials via flags:

```bash
agent-kakaotalk auth login --email user@example.com --password mypass
```

**Device registration flow**: On first login, KakaoTalk requires device verification:
1. The CLI requests a passcode from KakaoTalk's server
2. A numeric code is displayed — enter it on your phone when prompted
3. The CLI polls until you confirm on your phone
4. Login completes automatically after confirmation

**IMPORTANT**: NEVER guide the user to open a web browser, use DevTools, or manually copy tokens. Always use `agent-kakaotalk auth login` or `agent-kakaotalk auth extract`.

### Method 2: Extract from Desktop App

Extracts OAuth tokens directly from the KakaoTalk desktop app's cache. This **kicks the desktop session** because it reuses the desktop's credentials.

```bash
agent-kakaotalk auth extract
agent-kakaotalk auth extract --debug
```

On macOS, reads from `~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches/Cache.db`. On Windows, reads from the registry and `%LocalAppData%\Kakao\login_list.dat`.

### Agent Behavior (MANDATORY)

When a command fails because no account is configured, the agent MUST drive the auth flow itself:

**Step 1: Check auth status**

```bash
agent-kakaotalk auth status
```

If authenticated → retry the original command.

**Step 2: Try credential extraction first**

```bash
agent-kakaotalk auth extract
```

If extraction succeeds → retry the original command. Extraction is silent and requires no user input.

**Step 3: If extraction fails, use login flow**

Ask the user for their KakaoTalk email and password (these are the only things needed).

```bash
agent-kakaotalk auth login --email <email> --password <password>
```

Possible responses:

- `{"authenticated": true, ...}` → Success. Retry original command.
- `{"next_action": "confirm_on_phone", "passcode": "1234", ...}` → Tell the user to enter the displayed code on their phone. The CLI is polling — wait for it to complete, then the login will finish automatically.
- `{"next_action": "choose_device", ...}` → Tablet slot is occupied. Ask user which slot to use, then re-run with `--device-type pc --force` or `--device-type tablet --force`.

**Step 4: Retry the original command**

After successful auth, immediately execute whatever the user originally asked for.

### Device Slots

KakaoTalk allows these simultaneous sessions:
- **Phone** (always active, never affected by the CLI)
- **PC** — will kick KakaoTalk desktop if the CLI uses this slot
- **Tablet** (default) — safe if you don't use a tablet for KakaoTalk

```bash
# Default: tablet slot (safe for most users)
agent-kakaotalk auth login

# Use PC slot instead (kicks desktop app)
agent-kakaotalk auth login --device-type pc

# Force login even if slot is occupied
agent-kakaotalk auth login --device-type tablet --force
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed — the CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered chat IDs, friend names, and preferences.

- If the file doesn't exist yet, that's fine — proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory — don't error out.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering chat IDs and participant names (from `chat list`)
- After discovering your own user ID (from `auth status`)
- After the user gives you an alias or preference ("call this the work chat", "my group chat with Alice is X")
- After discovering chat structure (group chats, 1:1 chats)

When writing, include the **complete file content** — the `Write` tool overwrites the entire file.

### What to Store

- Chat IDs with participant names or display names
- Your own user ID
- User-given aliases ("work chat", "family group")
- Commonly referenced chat IDs
- Any user preference expressed during interaction

### What NOT to Store

Never store tokens, passwords, credentials, or any sensitive data. Never store full message content (just IDs and chat context). Never store OAuth tokens or device UUIDs.

### Handling Stale Data

If a memorized chat ID returns an error, remove it from `MEMORY.md`. Don't blindly trust memorized data — verify when something seems off. Prefer re-listing over using a memorized ID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## KakaoTalk Account

- User ID: `1234567890`
- Device type: tablet

## Chat Rooms

- `9876543210` — Work group chat (Alice, Bob, Charlie)
- `1111111111` — 1:1 with Alice
- `2222222222` — Family group

## Aliases

- "work" → `9876543210` (Work group chat)
- "alice" → `1111111111` (1:1 with Alice)

## Notes

- User prefers --pretty output
- Work chat is the most frequently used
```

> Memory lets you skip repeated `chat list` calls. When you already know a chat ID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Login as sub-device (recommended)
agent-kakaotalk auth login
agent-kakaotalk auth login --email <email> --password <password>
agent-kakaotalk auth login --device-type pc --force
agent-kakaotalk auth login --debug

# Extract credentials from KakaoTalk desktop app
agent-kakaotalk auth extract
agent-kakaotalk auth extract --debug
agent-kakaotalk auth extract --unsafely-show-secrets

# Check auth status
agent-kakaotalk auth status

# Remove stored credentials
agent-kakaotalk auth logout
agent-kakaotalk auth logout <account-id>
```

### Chat Commands

```bash
# List all chat rooms (sorted by most recent activity)
agent-kakaotalk chat list
agent-kakaotalk chat list --pretty
```

Output includes:
- `chat_id` — numeric chat room ID
- `type` — chat type (1:1, group, open chat)
- `display_name` — comma-separated member names
- `active_members` — number of active members
- `unread_count` — unread message count
- `last_message` — most recent message preview

### Message Commands

```bash
# List messages in a chat room
agent-kakaotalk message list <chat-id>
agent-kakaotalk message list <chat-id> -n 50
agent-kakaotalk message list <chat-id> --from <log-id>
agent-kakaotalk message list <chat-id> --pretty

# Send a text message
agent-kakaotalk message send <chat-id> "Hello world"
agent-kakaotalk message send <chat-id> "Hello world" --pretty
```

#### Message List Output

Each message includes:
- `log_id` — unique message identifier
- `type` — message type (1 = text, 2 = photo, etc.)
- `author_id` — sender's user ID
- `message` — message text content
- `sent_at` — Unix timestamp (milliseconds)

#### Fetching More Messages

The CLI handles internal pagination automatically. Just increase `-n` to get more messages:

```bash
# Get latest 20 messages (default)
agent-kakaotalk message list 9876543210

# Get 50 messages
agent-kakaotalk message list 9876543210 -n 50

# Get 200 messages
agent-kakaotalk message list 9876543210 -n 200

# Get messages newer than a known log ID (forward only)
agent-kakaotalk message list 9876543210 --from 123456789
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "chat_id": "9876543210",
  "type": 2,
  "display_name": "Alice, Bob",
  "active_members": 3,
  "unread_count": 5,
  "last_message": {
    "author_id": "1111111111",
    "message": "Hello everyone!",
    "sent_at": 1705312200000
  }
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-kakaotalk chat list --pretty
```

## Global Options

| Option     | Description                           |
| ---------- | ------------------------------------- |
| `--pretty` | Human-readable output instead of JSON |

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:

- `post-message.sh` - Send messages with error handling
- `monitor-chat.sh` - Monitor a chat for new messages
- `chat-summary.sh` - Generate chat summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No KakaoTalk credentials found. Run:\n  agent-kakaotalk auth login     (recommended — registers as sub-device, desktop app stays running)"
}
```

Common errors:

- `No KakaoTalk credentials found` — not authenticated. Run `auth login` or `auth extract`.
- `login_failed` — wrong email/password or device slot conflict.
- `passcode_request_failed` — failed to request device verification code.
- `registration_timeout` — passcode expired before user confirmed on phone.
- `login_http_error` — network issue reaching KakaoTalk servers.
- `LOCO packet timeout` — messaging protocol timed out (server may be overloaded).

## Configuration

Credentials stored in `~/.config/agent-messenger/kakaotalk-credentials.json` (0600 permissions). See [references/authentication.md](references/authentication.md) for format and security details.

Config format:

```json
{
  "current_account": "1234567890",
  "accounts": {
    "1234567890": {
      "account_id": "1234567890",
      "oauth_token": "...",
      "user_id": "1234567890",
      "refresh_token": "...",
      "device_uuid": "...",
      "device_type": "tablet",
      "created_at": "2025-01-15T10:30:00.000Z",
      "updated_at": "2025-01-15T10:30:00.000Z"
    }
  }
}
```

## Limitations

- macOS and Windows only (desktop app required for credential extraction)
- No Linux support (KakaoTalk desktop not available on Linux)
- No real-time events / push notifications
- No file upload or download
- No channel/chat room creation or management
- No friend list management
- No reactions or emoji
- No message editing or deletion
- No open chat (오픈채팅) browsing or joining
- No search across chats
- No multi-account switching (single account at a time)
- Plain text messages only (no photos, videos, or rich content)
- Chat IDs are numeric and not human-readable — use `chat list` to discover them

## Troubleshooting

### `agent-kakaotalk: command not found`

**`agent-kakaotalk` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-kakaotalk` directly:

```bash
agent-kakaotalk chat list --pretty
```

If the package is NOT installed, use `--package` to install and run:

```bash
npx -y --package agent-messenger agent-kakaotalk chat list --pretty
bunx --package agent-messenger agent-kakaotalk chat list --pretty
pnpm dlx --package agent-messenger agent-kakaotalk chat list --pretty
```

> **Note**: If the user prefers a different package runner, use the matching command above.

**NEVER run `npx agent-kakaotalk`, `bunx agent-kakaotalk`, or `pnpm dlx agent-kakaotalk`** without `--package agent-messenger`. It will fail or install a wrong package since `agent-kakaotalk` is not the npm package name.

### No credentials found

If `auth extract` fails:

1. Make sure the KakaoTalk desktop app is installed and you're logged in
2. Run `agent-kakaotalk auth extract --debug` for detailed diagnostics
3. If extraction still fails, use `agent-kakaotalk auth login` instead (recommended)

### Device slot occupied

If login fails because the tablet slot is occupied:

```bash
# Option 1: Use the PC slot instead
agent-kakaotalk auth login --device-type pc --force

# Option 2: Force the tablet slot (kicks existing tablet session)
agent-kakaotalk auth login --device-type tablet --force
```

### Passcode verification timeout

If the passcode expires before you confirm on your phone:

1. Run `agent-kakaotalk auth login` again — a new passcode will be generated
2. Confirm the code on your phone within the time limit
3. The CLI automatically completes login after confirmation

### Cache.db not found (macOS)

The CLI looks for KakaoTalk's cache at:

```
~/Library/Containers/com.kakao.KakaoTalkMac/Data/Library/Caches/Cache.db
```

If this file doesn't exist:
1. Install KakaoTalk from the Mac App Store
2. Log in and send at least one message (to populate the cache)
3. Run `agent-kakaotalk auth extract` again

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
