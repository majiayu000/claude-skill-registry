---
name: slack-formatting
description: Format messages correctly for Slack using mrkdwn syntax. Use this skill when sending messages to Slack channels or DMs via the AI agent. Covers the differences between standard Markdown and Slack mrkdwn, including bold (*single asterisks*), italic (_underscores_), code formatting, links, and emoji shortcodes. Use when asked to "send a Slack message", "format for Slack", or when composing any Slack communication.
---

# Slack Message Formatting

Slack uses **mrkdwn** format, NOT standard Markdown.

## Text Formatting

| Style    | Slack mrkdwn | Standard Markdown (WRONG) |
| -------- | ------------ | ------------------------- |
| **Bold** | `*text*`     | ~~`**text**`~~            |
| _Italic_ | `_text_`     | ~~`*text*`~~              |
| `Code`   | `` `text` `` | `` `text` `` ✓            |
| ~Strike~ | `~text~`     | `~text~` ✓                |

## Headers

Slack does NOT support markdown headers.

- ❌ Wrong: `## Header`
- ✅ Correct: Use `*Bold Text*` with line breaks

## Links

```
Format: <url|link text>
Example: <https://jira.example.com|View in Jira>
Auto-link: <https://example.com>
```

## Lists

- Bullet points: `• item` or `- item`
- Numbered lists: `1. item`

## Code Blocks

```
Use triple backticks (same as standard markdown)
```

## Block Quotes

```
> This is a quote
```

## Common Emoji Shortcodes

| Shortcode            | Emoji |
| -------------------- | ----- |
| `:white_check_mark:` | ✅    |
| `:warning:`          | ⚠️    |
| `:rocket:`           | 🚀    |
| `:fire:`             | 🔥    |
| `:thinking_face:`    | 🤔    |
| `:tada:`             | 🎉    |
| `:x:`                | ❌    |

## Example Comparison

### ❌ Wrong (Standard Markdown)

```markdown
## **Breakdown by Status:**

### 🔨 **In Progress (2 issues)**

- **PROJ-25519** - Create analytics events (Tom)
- **PROJ-26838** - Export Case Details (Unassigned)
```

### ✅ Correct (Slack mrkdwn)

```
*Breakdown by Status:*

*🔨 In Progress (2 issues):*
• `PROJ-25519` - Create analytics events (Tom)
• `PROJ-26838` - Export Case Details (Unassigned)

*✅ Ready for Deployment (2 issues):*
• `PROJ-25731` - HPO term fix (Daniel)
• `PROJ-25607` - Fix text highlighting (Amitai)
```

## MCP Tools

- `ai_first_slack_send_dm` - Send direct message
- `ai_first_slack_send_channel_message` - Send to channel
- `ai_first_slack_lookup_user_by_email` - Look up user

## Verification Checklist

- [ ] Bold text uses `*single asterisks*`
- [ ] No `##` header symbols visible
- [ ] Issue keys appear in monospace with backticks
- [ ] Emoji render properly
- [ ] Links use `<url|text>` format
