---
name: publish-discord
version: "2.0.0"
description: >
  Publish formatted content to Discord channels using the Discord MCP server.
  Handles message splitting for character limits, supports embeds and threads.
license: MIT
allowed-tools:
  - discord/send_message   # Send message to Discord channel
  - discord/send_embed     # Send rich embed to Discord
  - discord/create_thread  # Create thread for digests
metadata:
  kubani:
    domain: news
    category: publishing
    requires_approval: true
    confidence: 0.98
    version: "2.0.0"
---

# Publish to Discord

Publish formatted content to Discord channels using MCP.

## When to Use

Use this skill when you need to:
- Post news digests to Discord channels
- Send breaking news alerts
- Notify teams of important updates
- Share formatted content with Discord communities

## Instructions

### Step 1: Prepare Content

Format the content for Discord:
- Split long content into chunks (max 2000 characters per message)
- Preserve markdown formatting at split points
- Add part indicators for multi-part messages

**Splitting rules:**
- Split at line boundaries when possible
- Keep headers with their content
- Add `**[Part X/Y]**` prefix for multi-part messages

### Step 2: Create Thread for Digests

For long digests, use `discord/create_thread`:
- channel_id: Target channel ID
- name: "AI News Digest - {date}"
- auto_archive_duration: 1440 (24 hours)

This keeps the main channel clean.

### Step 3: Send Messages

Use `discord/send_message` for each content chunk:
- channel_id: Thread ID (if created) or channel ID
- content: Message content (max 2000 chars)

**Rate limiting:**
- Discord allows 5 messages per 2 seconds per channel
- Add small delay between messages if needed

### Step 4: Send Breaking News as Embed

For breaking news, use `discord/send_embed` for visual impact:
- channel_id: Target channel
- title: Article title with 🚨 prefix
- description: Article summary
- url: Link to source
- color: 0xff0000 (red for breaking)
- fields: [{name: "Source", value: source}, {name: "Importance", value: "X/10"}]
- footer: Breaking reason

**Example embed call:**
```
discord/send_embed:
  channel_id: "123456789"
  title: "🚨 GPT-5 Released"
  description: "OpenAI has released GPT-5 with major advances..."
  url: "https://openai.com/blog/gpt-5"
  color: 16711680
  fields:
    - name: "Source"
      value: "OpenAI Blog"
      inline: true
    - name: "Importance"
      value: "10/10"
      inline: true
  footer: "Breaking: Major model release from leading AI company"
```

### Step 5: Include Mentions for Alerts

For critical breaking news:
- Add `@here` to notify online members
- Add `@everyone` only for truly critical alerts (use sparingly)

### Step 6: Return Results

Return success status including:
- Number of messages sent
- Thread ID (if created)
- Any errors encountered

## Tool Usage Guidance

### discord/send_message
- Basic text messages
- Max 2000 characters
- Supports Discord markdown

### discord/send_embed
- Rich formatted messages
- Better for breaking news
- Supports colors, fields, footers

### discord/create_thread
- Create threads for long content
- Keeps main channel clean
- Auto-archives after specified time

## Discord Message Limits

| Limit | Value |
|-------|-------|
| Message length | 2000 chars |
| Embeds per message | 10 |
| Fields per embed | 25 |
| Field name | 256 chars |
| Field value | 1024 chars |
| Embed description | 4096 chars |

## Breaking News Embed Colors

| Priority | Color | Hex |
|----------|-------|-----|
| Critical | Red | 0xff0000 |
| High | Orange | 0xff8000 |
| Notable | Yellow | 0xffff00 |
| Normal | Blue | 0x0099ff |

## Discord Markdown

Supported formatting:
- **Bold:** `**text**`
- *Italic:* `*text*`
- __Underline:__ `__text__`
- ~~Strikethrough:~~ `~~text~~`
- Code: `` `code` ``
- Code block: ` ```code block``` `
- Links: `[text](url)`

## Mentions

- User: `<@user_id>`
- Role: `<@&role_id>`
- Channel: `<#channel_id>`
- Everyone: `@everyone`
- Here: `@here`

## Error Handling

- If send fails, retry with exponential backoff
- If rate limited, wait specified time and retry
- Log failures but continue with remaining messages
- Return partial success if some messages sent

## Success Criteria

- Messages delivered to correct channel/thread
- Long content properly split
- Formatting preserved
- Breaking alerts visually distinct
- No message truncation or loss
- Rate limits respected
