---
name: imessage
description: Send and read iMessages/SMS from macOS. Use for texting contacts, scheduling services, or automating message-based workflows. Triggers on queries about texting, messaging, SMS, iMessage, or contacting someone via text.
---

# iMessage Integration

Send and read iMessages/SMS using the `imsg` CLI tool on macOS.

## Setup

### 1. Build the imsg CLI

Clone and build the tool:
```bash
git clone https://github.com/letta-ai/imsg.git ~/repos/imsg
cd ~/repos/imsg
swift build -c release
```

The binary will be at `~/repos/imsg/.build/release/imsg` (or use the pre-built binary if available at `~/repos/imsg/bin/imsg`).

### 2. Grant Permissions

Required macOS permissions (System Settings → Privacy & Security):

| Permission | Location | Required For |
|------------|----------|--------------|
| Full Disk Access | Privacy & Security → Full Disk Access | Reading message history |
| Automation | Privacy & Security → Automation | Sending messages via Messages.app |

### 3. Enable SMS Relay (Optional)

To send SMS (green bubbles) to non-iMessage users:
1. On iPhone: Settings → Messages → Text Message Forwarding
2. Enable forwarding to your Mac

## Commands

### List Recent Chats
```bash
imsg chats --limit 10
imsg chats --limit 10 --json
```

Output format: `[chat_id] (identifier) last=timestamp`

### View Chat History
```bash
# View last 20 messages in a chat
imsg history --chat-id <id> --limit 20

# With attachments metadata
imsg history --chat-id <id> --limit 20 --attachments

# Filter by date
imsg history --chat-id <id> --start 2026-01-01T00:00:00Z --json
```

### Send a Message
```bash
# Send to phone number
imsg send --to "+15555555555" --text "Hello!"

# Send with attachment
imsg send --to "+15555555555" --text "Here's the file" --file /path/to/file.jpg

# Force iMessage or SMS
imsg send --to "+15555555555" --text "Hi" --service imessage
imsg send --to "+15555555555" --text "Hi" --service sms

# Send to existing chat by ID
imsg send --chat-id 86 --text "Hello!"
```

### Watch for New Messages
```bash
imsg watch --chat-id <id> --debounce 250ms
```

## Best Practices

### Phone Number Format
- Use E.164 format: `+1XXXXXXXXXX` for US numbers
- Include country code for international

### SMS vs iMessage
- **iMessage** (blue bubble): Default for Apple device users, free
- **SMS** (green bubble): Requires iPhone relay, may have carrier charges
- Use `--service sms` when recipient doesn't have iMessage

### Message Etiquette for Agents
- **Be concise** - Keep messages short and clear
- **Be human** - Write naturally, not robotically
- **Identify context** - If following up, reference previous conversation
- **Respect timing** - Avoid early morning/late night messages

## Common Use Cases

### Scheduling Services
```bash
imsg send --to "+14155551234" --text "Hi! Do you have availability this Saturday for a cleaning?"
```

### Following Up
```bash
imsg send --to "+14155551234" --text "Just wanted to follow up on my earlier message. Let me know when you have a chance!"
```

### Confirming Appointments
```bash
imsg send --to "+14155551234" --text "Confirming our appointment for Saturday at 10am. See you then!"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "not authorized" error | Grant Automation permission to terminal |
| Can't read messages | Grant Full Disk Access to terminal |
| SMS not sending | Enable Text Message Forwarding on iPhone |
| Message stuck sending | Check Messages.app is signed in and working |

## Technical Notes

- Uses AppleScript for sending (no private APIs)
- Read operations are read-only on the Messages SQLite database
- Requires macOS 14+ with Messages.app configured
- Binary location: `~/repos/imsg/bin/imsg` (adjust path as needed)
