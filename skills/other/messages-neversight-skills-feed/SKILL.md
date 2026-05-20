---
name: messages
description: Retrieve chat message history, send messages, and manage reactions in Lark - get messages from group chats, private chats, threads, send messages to users or chats, and add/list/remove reactions. Use when user asks about chat messages, conversation history, what was discussed in a group, or wants to send a message or react.
---

# Messages Skill

Retrieve chat message history, send messages, manage reactions, and search for chats/groups via the `lark` CLI.

## 🤖 Capabilities and Use Cases

- Send markdown-lite messages with links and mentions
- Send images with `--image` and `{{image}}` placement
- Message recall/delete for cleanup
- Add/list/remove emoji reactions
- Browse emoji catalog reference
- Read chat history (chat or thread)
- Download message resources (images/files/audio/video)
- Find chats by name or member
- Use clear, flag-based CLI with consistent JSON output

## 🚀 Quick Reference

**Send message:**
```bash
lark msg send --to user@example.com --text "Hello!"
```

**Read messages:**
```bash
lark msg history --chat-id oc_12345 --limit 10
```

**Find chats:**
```bash
lark chat search "project team"
```

**React / list / remove reaction:**
```bash
lark msg react --message-id om_123456789abcdef --reaction SMILE
lark msg react list --message-id om_123456789abcdef
lark msg react remove --message-id om_123456789abcdef --reaction-id ZCaCIjUBVVWSrm5L-3ZTw...
```

**Download resource:**
```bash
lark msg resource --message-id om_xxx --file-key img_v3_xxx --type image --output ./image.png
```

## Running Commands

Ensure `lark` is in your PATH, or use the full path to the binary. Set the config directory if not using the default:

```bash
lark msg <command>
lark chat <command>
# Or with explicit config:
LARK_CONFIG_DIR=/path/to/.lark lark msg <command>
```

## Commands Reference

### Search for Chats/Groups

```bash
lark chat search "project" --limit 10
```

Available flags:
- `--limit`: Maximum number of chats to retrieve (0 = no limit)

Output fields include:
- `chats[]` with `chat_id`, `name`, `description`, `owner_id`, `external`, `chat_status`
- `count`, `query`

### Send Messages

Send messages to users or group chats as the bot.

```bash
lark msg send --to ou_xxxx --text "Hello!"
```

Available flags:
- `--to` (required): Recipient identifier (user ID, open_id, email, or chat_id)
- `--to-type`: Explicitly specify ID type (`open_id`, `user_id`, `email`, `chat_id`) - auto-detected if omitted
- `--text`: Message text content (markdown-lite). Use `{{image}}` to place images.
- `--image`: Image file path (repeatable)

Output:
```json
{
  "success": true,
  "message_id": "om_dc13264520392913993dd051dba21dcf",
  "chat_id": "oc_xxxxx",
  "create_time": "2026-01-14T10:30:00+08:00"
}
```

### Get Chat History

```bash
lark msg history --chat-id oc_xxxxx --limit 50 --sort desc
```

Available flags:
- `--chat-id` (required): Chat ID or thread ID
- `--type`: Container type - `chat` (default) or `thread`
- `--start`: Start time (Unix timestamp or ISO 8601)
- `--end`: End time (Unix timestamp or ISO 8601)
- `--sort`: Sort order - `asc` (default) or `desc`
- `--limit`: Maximum number of messages (0 = no limit)

Output fields include:
- `messages[]` with `message_id`, `msg_type`, `content`, `sender`, `create_time`, `mentions`, `is_reply`, `thread_id`, `deleted`
- `count`, `chat_id`

### React to Message

Add a reaction to a message as the bot.

```bash
lark msg react --message-id om_dc13264520392913993dd051dba21dcf --reaction SMILE
```

Available flags:
- `--message-id` (required): Message ID to react to
- `--reaction` (required): Reaction ID or emoji name
- `--type`: Reaction type (default: `emoji`)

Output:
```json
{
  "success": true,
  "message_id": "om_dc13264520392913993dd051dba21dcf",
  "reaction_type": "emoji",
  "reaction_id": "ZCaCIjUBVVWSrm5L-3ZTw...",
  "emoji_type": "SMILE"
}
```

Notes:
- Reactions are added as the bot/app. The bot must be in the chat to react.
- Emoji types must match the Lark emoji catalog (e.g., `SMILE`, `LAUGH`).

### Emoji Catalog Reference

```bash
lark msg react emojis
```

Use this command to list the supported emoji types for reactions.

**Custom Emojis:** Organization-specific custom emojis can be configured in `.lark/config.yaml`:

```yaml
custom_emojis:
  "7405453485858095136": "ez-pepe"
```

Custom emoji IDs will appear in the `custom_emojis` field of the output.

### List Message Reactions

```bash
lark msg react list --message-id om_dc13264520392913993dd051dba21dcf --reaction SMILE --limit 50
```

Available flags:
- `--message-id` (required): Message ID to list reactions for
- `--reaction`: Emoji type filter (e.g., `SMILE`)
- `--limit`: Maximum number of reactions to retrieve (0 = no limit)

Output fields include:
- `message_id`, `reactions[]`, `count`

### Remove Message Reaction

```bash
lark msg react remove --message-id om_dc13264520392913993dd051dba21dcf --reaction-id ZCaCIjUBVVWSrm5L-3ZTw...
```

Available flags:
- `--message-id` (required): Message ID to remove reaction from
- `--reaction-id` (required): Reaction ID to remove

Output fields include:
- `success`, `message_id`, `reaction_type`, `reaction_id`, `emoji_type`

### Recall Messages

Recall/delete previously sent messages from chats.

```bash
lark msg recall om_dc13264520392913993dd051dba21dcf
```

Output fields include:
- `success`, `message_id`

### Downloading Resource Files

Download images, files, audio, and video from messages using `msg resource`:

```bash
lark msg resource --message-id om_xxx --file-key img_v3_xxx --type image --output ./image.png
lark msg resource --message-id om_xxx --file-key file_v2_xxx --type file --output ./document.pdf
```

Available flags:
- `--message-id` (required): Message ID containing the resource
- `--file-key` (required): Resource key from message content (`image_key` or `file_key`)
- `--type` (required): `image` for images, `file` for files/audio/video
- `--output` (required): Output file path

Output fields include:
- `success`, `message_id`, `file_key`, `output_path`, `content_type`, `bytes_written`

Limitations:
- Maximum file size: 100MB
- Emoji resources cannot be downloaded
- Resources from card, merged, or forwarded messages are not supported
- The `message_id` and `file_key` must match

## Tips

- Use `\n` for line breaks and `\t` for indentation in `--text`
- Use `@{ou_xxx}` to mention users in group chats
- Use `{{image}}` in text to place images in order
- Chat IDs start with `oc_`; thread IDs start with `thread_` or `omt_`
- Use `lark msg react list` to discover `reaction_id` for removal
- The CLI auto-detects recipient type; override with `--to-type` if needed

## Message Types

- `text` - Plain text message
- `post` - Rich text post
- `image` - Image
- `file` - File attachment
- `audio` - Audio message
- `media` - Video/media
- `sticker` - Sticker/emoji
- `interactive` - Interactive card
- `share_chat` - Shared chat
- `share_user` - Shared user contact

## Reading Thread Replies

If a message has a `thread_id`, it is part of a thread (or is the root). To fetch replies:

```bash
lark msg history --chat-id oc_xxxxx --limit 10 --sort desc
lark msg history --chat-id omt_1a3b99f9d2cfd982 --type thread
```

Thread messages will have `is_reply: true` for replies (root message has `is_reply: false`).

## Output Format

All commands output JSON.

## Error Handling

Errors return JSON:
```json
{
  "error": true,
  "code": "ERROR_CODE",
  "message": "Description"
}
```

Common error codes:
- `AUTH_ERROR` - Need to run `lark auth login`
- `SCOPE_ERROR` - Missing messages permissions
- `VALIDATION_ERROR` - Missing required fields (e.g., chat-id)
- `API_ERROR` - Lark API issue (e.g., bot not in group, missing permissions)

## Required Permissions

This skill requires the `messages` scope group. If you see a `SCOPE_ERROR`, add permissions:

```bash
lark auth login --add --scopes messages
```

To check current permissions:
```bash
lark auth status
```

Additional requirements:

**For reading messages:**
- The bot must be in the group chat
- Group chat reads require the "Read all messages in associated group chat" permission
- Private chat reads require `im:message:readonly`

**For sending messages:**
- Requires `im:message` or `im:message:send_as_bot`
- The bot must be added to group chats before it can send messages to them

**For reactions:**
- List reactions requires `im:message.reactions:read`
- Add/remove reactions requires `im:message.reactions:write_only`

## Notes

- Messages are sent as the bot/app
- Messages are sorted by creation time ascending by default
- Time filters do not work for thread container type
- Message IDs typically start with `om_`
