---
name: slack-message-formatter
category: communication
description: |
  Format messages for Slack with pixel-perfect accuracy. Converts Markdown to
  rich HTML (for copy-paste into Slack) or Slack mrkdwn (for API/webhook).
  Use when the user asks to write a Slack message, announcement, or notification,
  format something "for Slack", preview how content looks in Slack, or send a
  message via Slack webhook. Also trigger when user mentions Slack formatting,
  mrkdwn, or wants to share Markdown content in Slack channels.
---

# Slack Message Formatter

Format messages for Slack with pixel-perfect accuracy. Converts Markdown to Slack-compatible output with two delivery paths:

1. **Copy-paste** — Rich HTML that preserves formatting when pasted into Slack's compose box
2. **API/Webhook** — Slack mrkdwn syntax for bots, automation, and CI/CD

## When to Use This Skill

- User asks to write a Slack message, announcement, or notification
- User asks to format something "for Slack"
- User wants to preview how a message will look in Slack
- User wants to send a message via Slack webhook
- User has Markdown content they want to share in Slack

## What This Skill Does

1. **Generates content in Markdown** — Claude writes the message in standard Markdown, its native format
2. **Converts to Rich HTML** — Transforms Markdown into rich HTML that preserves formatting when pasted into Slack's compose box
3. **Converts to Slack mrkdwn** — Transforms Markdown into Slack's proprietary mrkdwn syntax for API/webhook delivery
4. **Generates a Slack-themed preview** — Creates an HTML preview page styled like the Slack UI and opens it in the browser
5. **Copies to clipboard** — Automatically copies the rich HTML to the system clipboard for one-step paste into Slack

## How to Use

### Basic Usage

```
Write a Slack message announcing our Q2 product launch
```

```
Format this for Slack: We shipped 3 new features this week...
```

```
Create a Slack announcement for the engineering team about the new CI pipeline
```

### Webhook/API Delivery

```
Send a deploy notification to Slack via webhook
```

### Formatting Features

The converter handles all Markdown features and translates them correctly for Slack:

- Bold, italic, strikethrough, inline code
- Links and headings (converted to bold in Slack)
- Tables (rich HTML tables for paste, code blocks for API)
- Task lists with emoji checkboxes
- Nested lists and blockquotes
- Code blocks with syntax highlighting
- Slack mentions (`<@U012AB3CD>`, `<!here>`, `<!channel>`)
- 150+ emoji shortcodes converted to Unicode

## Example

**User**: "Write a Slack message announcing our new feature"

**Output** (opened as a Slack-themed preview in the browser + copied to clipboard):

The preview shows a pixel-perfect Slack UI rendering. The user pastes directly into Slack with Cmd+V / Ctrl+V and the formatting is preserved.

**User**: "Send a deploy notification to our #deploys channel via webhook"

**Output** (sent via mrkdwn to the configured webhook):
```
*:rocket: Deploy Successful*

*Service:* payment-api
*Version:* v2.5.1
*Environment:* production
*Duration:* 47s

:white_check_mark: All health checks passing
```

## Configuration

| Env Variable | Default | Description |
|-------------|---------|-------------|
| `SLACK_FORMATTER_CLIPBOARD` | `true` | Set to `false` to disable auto-clipboard copy |
| `SLACK_FORMATTER_PREVIEW_DIR` | `/tmp/slack-formatter` | Directory for preview HTML files |
| `CCH_SLA_WEBHOOK` | (none) | Slack webhook URL for sending messages |

## Tips

- Always let the converter handle the Markdown-to-Slack translation; never write mrkdwn or HTML by hand
- Slack mentions (`<@U...>`, `<#C...>`, `<!here>`) can be included directly in the Markdown
- Tables work beautifully via the copy-paste path; for API delivery they become code blocks (Slack has no table syntax)
- Preview files are timestamped so you can revisit them from conversation history
