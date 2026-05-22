---
name: agent-whatsapp
description: Interact with WhatsApp - send messages, read chats, manage conversations
version: 1.15.0
allowed-tools: Bash(agent-whatsapp:*)
metadata:
  openclaw:
    requires:
      bins:
        - agent-whatsapp
    install:
      - kind: node
        package: agent-messenger
        bins: [agent-whatsapp]
---

# Agent WhatsApp

A Baileys-backed WhatsApp CLI for AI agents. Links as a companion device via pairing code, so your phone stays connected. Each command connects on demand and disconnects when done.

Use one of these entrypoints:
- Global install: `agent-whatsapp ...`
- One-off execution: `bunx --package agent-messenger agent-whatsapp ...`

## Key Concepts

Before diving in, a few things about WhatsApp's architecture:

- **JID** (Jabber ID) = WhatsApp's address format. Individual: `1234567890@s.whatsapp.net`. Group: `123456789-123345@g.us`. You can pass plain phone numbers and the CLI resolves them to JIDs automatically.
- **Pairing code auth** = links the CLI as a companion device using a numeric code displayed in your terminal. Enter it in WhatsApp on your phone under Linked Devices.
- **Connect-on-demand** = the CLI opens a WebSocket connection for each command and disconnects afterward. There's no persistent background process.
- **Multi-account** = multiple WhatsApp accounts can be linked. Use `auth list` and `auth use` to switch between them.

## Quick Start

```bash
# Link as companion device (enter the pairing code on your phone)
agent-whatsapp auth login --phone +1234567890

# List chats
agent-whatsapp chat list

# Send a message
agent-whatsapp message send +1234567890 "Hello from agent-whatsapp"
```

## Authentication Flow

WhatsApp uses pairing code authentication. The CLI registers as a companion (linked) device, so your phone session is never affected.

### Agent Behavior (MANDATORY)

When a command fails because no account is configured, the agent MUST drive the auth flow itself. Never tell the user to run commands. The agent runs everything.

**Step 1: Check for existing accounts**

```bash
agent-whatsapp auth list
```

If accounts exist, use `agent-whatsapp auth use <account-id>` and retry the original command.

**Step 2: If no accounts, ask for phone number**

Ask the user for their WhatsApp phone number (international format, e.g. `+1234567890`). This is the ONLY thing the user needs to provide.

**Step 3: Start login**

```bash
agent-whatsapp auth login --phone +1234567890
# -> {"next_action":"enter_pairing_code","pairing_code":"A1B2-C3D4","message":"Enter this code in WhatsApp on your phone: Linked Devices > Link a Device."}
```

Tell the user the pairing code and ask them to enter it on their phone: open WhatsApp > Settings > Linked Devices > Link a Device > enter the code.

**Step 4: Wait for confirmation**

The CLI polls until the user confirms on their phone. Once confirmed:

```bash
# -> {"authenticated":true,...}
```

**Step 5: Retry the original command**

After successful auth, immediately execute whatever the user originally asked for.

### Common Auth Commands

```bash
agent-whatsapp auth status              # Check current auth state
agent-whatsapp auth status --account <id>  # Check specific account
agent-whatsapp auth list                # List all linked accounts
agent-whatsapp auth use <id>            # Switch active account
agent-whatsapp auth logout              # Unlink current account
agent-whatsapp auth logout --account <id>  # Unlink specific account
```

## Memory

The agent maintains a `~/.config/agent-messenger/MEMORY.md` file as persistent memory across sessions. This is agent-managed. The CLI does not read or write this file. Use the `Read` and `Write` tools to manage your memory file.

### Reading Memory

At the **start of every task**, read `~/.config/agent-messenger/MEMORY.md` using the `Read` tool to load any previously discovered chat IDs, contact names, and preferences.

- If the file doesn't exist yet, that's fine. Proceed without it and create it when you first have useful information to store.
- If the file can't be read (permissions, missing directory), proceed without memory.

### Writing Memory

After discovering useful information, update `~/.config/agent-messenger/MEMORY.md` using the `Write` tool. Write triggers include:

- After discovering chat JIDs and contact names (from `chat list`)
- After discovering group names and participants
- After the user gives you an alias or preference ("call this the family group", "my work chat is X")

When writing, include the **complete file content**. The `Write` tool overwrites the entire file.

### What to Store

- Chat JIDs with contact/group names
- Your own phone number and JID
- User-given aliases ("family group", "work chat")
- Commonly referenced chat JIDs
- Any user preference expressed during interaction

### What NOT to Store

Never store auth credentials, session keys, or any sensitive data. Never store full message content (just IDs and chat context).

### Handling Stale Data

If a memorized JID returns an error, remove it from `MEMORY.md`. Don't blindly trust memorized data. Prefer re-listing over using a memorized JID that might be stale.

### Format / Example

```markdown
# Agent Messenger Memory

## WhatsApp Account

- Phone: +1234567890
- JID: 1234567890@s.whatsapp.net

## Chats

- `1234567890@s.whatsapp.net` - Alice (1:1)
- `5678901234@s.whatsapp.net` - Bob (1:1)
- `123456789-123345@g.us` - Project Team (group, 8 members)
- `987654321-654321@g.us` - Family (group, 5 members)

## Aliases

- "alice" -> `1234567890@s.whatsapp.net`
- "project" -> `123456789-123345@g.us` (Project Team)
- "family" -> `987654321-654321@g.us` (Family group)

## Notes

- User prefers --pretty output
- Project Team is the most frequently used chat
```

> Memory lets you skip repeated `chat list` calls. When you already know a JID from a previous session, use it directly.

## Commands

### Auth Commands

```bash
# Link as companion device via pairing code
agent-whatsapp auth login --phone +1234567890

# Check auth status
agent-whatsapp auth status
agent-whatsapp auth status --account <id>

# List linked accounts
agent-whatsapp auth list

# Switch active account
agent-whatsapp auth use <id>

# Unlink account
agent-whatsapp auth logout
agent-whatsapp auth logout --account <id>
```

### Chat Commands

```bash
# List chats (sorted by most recent activity)
agent-whatsapp chat list
agent-whatsapp chat list --limit 50
agent-whatsapp chat list --account <id>

# Search chats by name
agent-whatsapp chat search "project"
agent-whatsapp chat search "project" --limit 10
agent-whatsapp chat search "project" --account <id>
```

Output includes:
- `jid` - chat JID (individual or group)
- `name` - contact or group name
- `unread_count` - unread message count
- `last_message` - most recent message preview

### Message Commands

```bash
# List messages in a chat
agent-whatsapp message list <chat> --limit 20
agent-whatsapp message list +1234567890 --limit 50
agent-whatsapp message list 123456789-123345@g.us --limit 10
agent-whatsapp message list +1234567890 --limit 20 --account <id>

# Send a text message
agent-whatsapp message send <chat> <text>
agent-whatsapp message send +1234567890 "Hello!"
agent-whatsapp message send 123456789-123345@g.us "Hello team!"
agent-whatsapp message send +1234567890 "Hello!" --account <id>

# React to a message
agent-whatsapp message react <chat> <message-id> <emoji>
agent-whatsapp message react +1234567890 ABC123DEF456 "👍"
agent-whatsapp message react +1234567890 ABC123DEF456 "👍" --from-me
agent-whatsapp message react +1234567890 ABC123DEF456 "👍" --account <id>
```

The `<chat>` argument accepts:
- Phone number: `+1234567890` (auto-resolved to JID)
- Individual JID: `1234567890@s.whatsapp.net`
- Group JID: `123456789-123345@g.us`

The `--from-me` flag on `message react` indicates the target message was sent by you (outgoing). Without it, the reaction targets an incoming message.

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "jid": "1234567890@s.whatsapp.net",
  "name": "Alice",
  "unread_count": 3,
  "last_message": {
    "id": "ABC123DEF456",
    "text": "See you tomorrow!",
    "from": "1234567890@s.whatsapp.net",
    "timestamp": 1705312200
  }
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-whatsapp chat list --pretty
```

## Global Options

| Option          | Description                                |
| --------------- | ------------------------------------------ |
| `--pretty`      | Human-readable output instead of JSON      |
| `--account <id>`| Use a specific account for this command     |

## Common Patterns

### Check unread messages

```bash
# List chats to see unread counts
agent-whatsapp chat list --limit 20

# Read messages from a specific chat
agent-whatsapp message list +1234567890 --limit 10
```

### Send a message to a contact

```bash
# By phone number (simplest)
agent-whatsapp message send +1234567890 "Hey, are we still on for tomorrow?"

# By JID
agent-whatsapp message send 1234567890@s.whatsapp.net "Hey, are we still on for tomorrow?"
```

### Send a message to a group

```bash
# Find the group first
agent-whatsapp chat search "Project Team"

# Send to the group JID
agent-whatsapp message send 123456789-123345@g.us "Status update: deployment complete."
```

### React to the latest message

```bash
# Get the latest message ID
agent-whatsapp message list +1234567890 --limit 1

# React to it
agent-whatsapp message react +1234567890 <message-id> "👍"
```

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No WhatsApp account linked. Run: agent-whatsapp auth login --phone <number>"
}
```

Common errors:

- `No WhatsApp account linked` - not authenticated. Run `auth login --phone <number>`.
- `Connection timeout` - WebSocket connection to WhatsApp failed. Retry the command.
- `Invalid JID` - malformed phone number or JID. Use international format with `+` prefix.
- `Not a group participant` - can't send to a group you're not a member of.

## Notes

- **JID format**: Individual chats use `1234567890@s.whatsapp.net`, groups use `123456789-123345@g.us`. Phone numbers can be passed directly and are auto-resolved.
- **Connect-on-demand**: Each command opens a WebSocket connection and closes it when done. There's no persistent daemon or background process.
- **Ban risk**: WhatsApp monitors for automated behavior. Avoid high-volume messaging, rapid-fire sends, or bulk operations. Space out commands when sending multiple messages.
- **Multi-account**: Multiple WhatsApp numbers can be linked simultaneously. Use `auth list` to see all accounts and `auth use <id>` to switch.
- **Phone numbers**: Always use international format with country code (e.g. `+1234567890`, `+821012345678`).
- `agent-whatsapp` returns JSON by default and `--pretty` for indented output.

## Troubleshooting

### `agent-whatsapp: command not found`

**`agent-whatsapp` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-whatsapp` directly:

```bash
agent-whatsapp chat list --pretty
```

If the package is NOT installed, use `--package` to install and run:

```bash
npx -y --package agent-messenger agent-whatsapp chat list --pretty
bunx --package agent-messenger agent-whatsapp chat list --pretty
pnpm dlx --package agent-messenger agent-whatsapp chat list --pretty
```

**NEVER run `npx agent-whatsapp`, `bunx agent-whatsapp`, or `pnpm dlx agent-whatsapp`** without `--package agent-messenger`. It will fail or install a wrong package since `agent-whatsapp` is not the npm package name.

### Pairing code not working

1. Make sure WhatsApp is open on your phone
2. Go to Settings > Linked Devices > Link a Device
3. Choose "Link with phone number instead" if you see a QR code
4. Enter the pairing code shown in the terminal
5. If the code expires, run `auth login --phone <number>` again for a fresh code

### Connection drops

WhatsApp may disconnect linked devices that are inactive for extended periods. If commands start failing:

```bash
# Check if still linked
agent-whatsapp auth status

# Re-link if needed
agent-whatsapp auth login --phone +1234567890
```
