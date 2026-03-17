---
name: telegram-assistant
description: |
  Telegram automation assistant using telegram-mcp. Use when users want to:
  (1) Get a digest of unread Telegram messages
  (2) Analyze their writing style from channel posts
  (3) Draft and publish posts to Telegram channels
  (4) Search and reply to messages across chats
  Triggers: "telegram digest", "unread messages", "morning summary",
  "post to channel", "draft telegram post", "analyze writing style",
  "extract style from channel", "telegram workflow"
license: MIT
compatibility: |
  Requires telegram-mcp server configured in Claude Code.
  See references/setup.md for installation instructions.
metadata:
  author: Bayram Annakov (onsa.ai)
  version: "1.0.0"
  category: productivity
  telegram-mcp-repo: https://github.com/chigwell/telegram-mcp
allowed-tools: mcp__telegram-mcp__* Read Write Edit Glob
---

# Telegram Assistant

Automate Telegram workflows with AI: digests, channel posting, and style-matched drafts.

## Quick Start

```
Need morning digest?     → Use Digest Workflow
Want to post to channel? → Use Style + Post Workflow
Replying to messages?    → Use Reply Workflow
```

---

## Workflow 1: Digest

**Goal**: Summarize unread messages across all chats.

### Step 1: Get Unread Chats
```
Use list_chats to find chats with unread messages.
Look for "Unread:" in the output (both count and "marked" flag).
```

### Step 2: Read Recent Messages
For each chat with unread:
1. Use `get_messages` or `list_messages` to fetch recent messages
2. Focus on messages since last read

### Step 3: Summarize
Create a digest with:
- **Priority items**: Direct mentions, questions needing response
- **Updates**: News, announcements from channels
- **Low priority**: General chatter, FYI items

### Step 4: Draft Replies (Optional)
For messages needing response:
1. Draft a reply
2. Use `save_draft` to save it for user review
3. User can review and send manually in Telegram app

**Safety**: Never send messages directly. Always save as draft first.

---

## Workflow 2: Style Extraction

**Goal**: Analyze channel posts to capture user's writing style.

### Step 1: Fetch Posts
```
Use list_messages with the channel name/ID.
Fetch last 15-20 posts (skip media-only posts).
```

### Step 2: Analyze Patterns
Extract these characteristics:
- **Language mix**: Ratio of Russian to English terms
- **Structure**: Use of hooks, tldr, bullets, numbered lists, sections
- **Tone**: Formal (вы) vs casual (ты), first-person usage (я/мы)
- **Length**: Average post length in words
- **Emoji**: Frequency and types used
- **Call-to-action**: How posts typically end

### Step 3: Generate Style Guide
Create `references/style-guide.md` with:
```markdown
# [Channel Name] Style Guide

## Language
- Primary: Russian with English tech terms
- Formality: [formal/casual]
- Person: [я/мы usage]

## Structure
- Hook: [question/statement/story]
- Sections: [yes/no, with headers?]
- Lists: [bullets/numbered]
- tldr: [yes/no]

## Formatting
- Average length: ~[X] words
- Emoji: [frequent/occasional/rare]
- Common emojis: [list]

## Endings
- Call-to-action style: [question/invitation/resource link]

## Example Patterns
[Include 2-3 anonymized structure examples]
```

### Step 4: Save for Future Use
The style guide is now available for the Post workflow.

---

## Workflow 3: Post to Channel

**Goal**: Draft a post matching user's writing style.

### Pre-requisite
Run Style Extraction workflow first if `references/style-guide.md` doesn't exist.

### Step 1: Read Style Guide
```
Read references/style-guide.md to understand the target style.
```

### Step 2: Understand Topic
Ask user for:
- Topic/subject matter
- Key points to cover
- Target audience (if different from usual)
- Any specific call-to-action

### Step 3: Draft Post
Write the post following the style guide:
- Match language mix ratio
- Use the same structural patterns
- Maintain consistent tone
- Include appropriate emoji (if style uses them)
- End with typical call-to-action pattern

### Step 4: User Review
Present the draft to user for feedback. Iterate if needed.

### Step 5: Save as Draft
```
Use save_draft(chat_id="ChannelName", message="draft content")
```

User can then:
1. Open Telegram app
2. Go to the channel
3. See the draft in the input field
4. Review and send when ready

**Safety**: Always use `save_draft`, never `send_message` for channel posts.

---

## Workflow 4: Search & Reply

**Goal**: Find specific messages and draft contextual replies.

### Step 1: Search
```
Use search_messages(chat_id, query) to find relevant messages.
Or list recent messages and filter manually.
```

### Step 2: Get Context
```
Use get_message_context(chat_id, message_id) to see surrounding messages.
```

### Step 3: Draft Reply
Write a contextual reply based on the conversation flow.

### Step 4: Save as Draft Reply
```
Use save_draft(chat_id, message, reply_to_msg_id=message_id)
```

User reviews and sends from Telegram app.

---

## Safety Guidelines

1. **Draft First**: Never use `send_message` for important communications. Always `save_draft`.

2. **Verify Chat ID**: Double-check you're targeting the right chat before any action.

3. **Rate Limits**: Avoid rapid-fire API calls. Space out requests if processing many chats.

4. **Privacy**: The AI sees all accessible chats. Be mindful of sensitive conversations.

5. **Session Security**: The session string provides full account access. Treat it like a password.
   - On macOS: Store in Keychain (see setup.md) rather than .env files
   - Never commit credentials to git

---

## Troubleshooting

### "Could not find the input entity"
- Use channel username (without @) or numeric ID
- For supergroups, try prepending -100 to the ID

### "Chat not found"
- Ensure the account has access to the chat
- Try using the exact chat title from `list_chats`

### Draft not appearing
- Open the specific chat in Telegram app
- Drafts are saved per-chat

---

## Resources

- **telegram-mcp repo**: https://github.com/chigwell/telegram-mcp
- **Setup guide**: [references/setup.md](references/setup.md)
- **Style guide template**: [references/style-guide.md](references/style-guide.md)
