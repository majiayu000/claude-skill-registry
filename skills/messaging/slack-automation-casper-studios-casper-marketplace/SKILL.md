---
name: slack-automation
description: Slack channel management, message fetching, searching, and AI categorization. Use this skill when searching Slack channels, reading messages, creating channels, or categorizing message content. Triggers on Slack-related operations, channel search, message history, or internal communications analysis.
---

# Slack Automation

## Overview

Interact with Slack workspaces for channel management, message reading, and content analysis. All operations are read-only unless creating channels.

## Quick Decision Tree

```
What do you need?
│
├── Search for channels by name
│   └── references/search.md
│   └── Script: scripts/slack_search.py search
│
├── Read messages from a channel
│   └── references/fetch-news.md
│   └── Script: scripts/fetch_slack_news.py
│
├── Create a new channel
│   └── references/create-channel.md
│   └── Script: scripts/create_slack_channel.py
│
└── Categorize/analyze messages
    └── references/categorize.md
    └── Script: scripts/categorize_slack_messages.py
```

## Environment Setup

```bash
# Required in .env
SLACK_BOT_TOKEN=xoxb-your-bot-token
```

## Required Bot Scopes

| Scope | Purpose |
|-------|---------|
| `channels:read` | List public channels |
| `channels:history` | Read public channel messages |
| `groups:read` | List private channels |
| `groups:history` | Read private channel messages |
| `channels:manage` | Create channels |

## Common Usage

### Search Channels
```bash
python scripts/slack_search.py search "internal" --limit 10
```

### Read Channel Messages
```bash
python scripts/slack_search.py read "internal-client" --days 7
```

### Create Channel
```bash
python scripts/create_slack_channel.py "project-alpha" --private
```

## Channel Naming Pattern

For client channels: `internal-{client-name}`
- e.g., `internal-microsoft`, `internal-acme-corp`

## Cost
Free - Slack API has no per-request cost. Rate limited to ~50 requests/minute.

## Security Notes

### Credential Handling
- Store `SLACK_BOT_TOKEN` in `.env` file (never commit to git)
- Bot tokens start with `xoxb-` - never expose in logs or output
- Rotate tokens via Slack App settings if compromised
- Use environment variables, not hardcoded values

### Data Privacy
- Messages may contain sensitive internal communications
- Avoid storing message content in persistent logs
- Use message links/IDs for references instead of copying content
- Consider data retention policies for exported messages
- User profiles include PII (names, emails, profile photos)

### Access Scopes
- Request minimum required scopes for your use case:
  - `channels:read` - List public channels (read-only)
  - `channels:history` - Read public channel messages (read-only)
  - `groups:read` - List private channels bot is in (read-only)
  - `groups:history` - Read private channel messages (read-only)
  - `channels:manage` - Create channels (write access)
- Bot can only access channels it has been invited to
- Review scopes at: Slack App Settings > OAuth & Permissions

### Compliance Considerations
- **Audit Logging**: Slack Enterprise Grid provides audit logs for compliance
- **Message Retention**: Follow your organization's data retention policies
- **GDPR**: Message content may contain EU user PII
- **eDiscovery**: Exported messages may be subject to legal holds
- **Internal Communications**: Treat Slack data as confidential
- **Channel Privacy**: Private channel access requires explicit invitation

## Troubleshooting

### Common Issues

#### Issue: Channel not found
**Symptoms:** "channel_not_found" error when reading or posting
**Cause:** Invalid channel ID, bot not in channel, or private channel
**Solution:**
- Verify channel ID is correct (use `slack_search.py search`)
- Invite the bot to the channel (`/invite @botname`)
- Check if channel is private - bot needs explicit invitation
- Ensure channel hasn't been archived or deleted

#### Issue: Missing permissions / scope errors
**Symptoms:** "missing_scope" or "not_allowed_token_type" error
**Cause:** Bot token missing required OAuth scopes
**Solution:**
- Go to Slack App Settings > OAuth & Permissions
- Add required scopes: `channels:read`, `channels:history`, etc.
- Reinstall the app to workspace after adding scopes
- Verify using the correct bot token (starts with `xoxb-`)

#### Issue: Token expired or invalid
**Symptoms:** "invalid_auth" or "token_revoked" error
**Cause:** OAuth token expired, revoked, or incorrectly configured
**Solution:**
- Reauthorize the bot in Slack App settings
- Regenerate the bot token if revoked
- Check `.env` for correct `SLACK_BOT_TOKEN` value
- Verify no whitespace or special characters in token

#### Issue: Rate limited
**Symptoms:** "ratelimited" error or 429 status code
**Cause:** Too many API requests in short period
**Solution:**
- Add delays between requests (1-2 seconds)
- Reduce batch size for bulk operations
- Implement exponential backoff on retries
- Slack allows ~50 requests/minute for most endpoints

#### Issue: Private channel access denied
**Symptoms:** Can't read private channel despite having scopes
**Cause:** Bot not added to the private channel
**Solution:**
- Have a channel member invite the bot: `/invite @botname`
- Ensure `groups:read` and `groups:history` scopes are added
- Verify bot has been reinstalled after adding scopes

## Resources

- **references/search.md** - Channel search and message reading
- **references/fetch-news.md** - Fetch news from channels
- **references/create-channel.md** - Create new channels
- **references/categorize.md** - AI message categorization

## Integration Patterns

### Slack to Newsletter
**Skills:** slack-automation → content-generation
**Use case:** Summarize internal news for weekly newsletter
**Flow:**
1. Fetch messages from news/announcements channels
2. Categorize and filter relevant content
3. Generate formatted newsletter section via content-generation

### Slack and Meeting Context
**Skills:** slack-automation → transcript-search
**Use case:** Find related meetings when researching Slack discussions
**Flow:**
1. Search Slack for client name or topic
2. Extract date ranges and participant names
3. Search transcript-search for related meeting recordings

### Slack Reports to Drive
**Skills:** slack-automation → google-workspace
**Use case:** Archive categorized Slack summaries to Google Drive
**Flow:**
1. Fetch and categorize messages from internal channels
2. Generate formatted report document
3. Upload to Google Drive via google-workspace
