---
name: slack-notifications
description: Slack messaging, channels, and notifications - send messages, manage channels, interact with users, upload files, and add reactions. Use for team communication, incident notifications, and workflow alerts.
allowed-tools: bash, read, webfetch
---

# Slack Notifications Skill

## Overview

This skill provides Slack API operations with progressive disclosure for optimal context usage.

**Context Savings**: ~90% reduction

- **MCP Mode**: ~15,000 tokens always loaded (30+ tools)
- **Skill Mode**: ~500 tokens metadata + on-demand loading

## Requirements

- **SLACK_BOT_TOKEN** environment variable (required)
- **SLACK_SIGNING_SECRET** environment variable (optional, for event verification)
- **SLACK_APP_TOKEN** environment variable (optional, for Socket Mode)

### Setting up Slack Bot Token

1. Create a Slack App at https://api.slack.com/apps
2. Navigate to "OAuth & Permissions"
3. Add required bot token scopes:
   - `chat:write` - Send messages
   - `channels:read` - List channels
   - `channels:history` - Read channel history
   - `users:read` - List users
   - `files:write` - Upload files
   - `reactions:write` - Add reactions
4. Install app to workspace
5. Copy "Bot User OAuth Token" to `SLACK_BOT_TOKEN` environment variable

## Tools

The skill provides 14 tools across 5 categories:

| Category      | Tools                                                     | Confirmation Required |
| ------------- | --------------------------------------------------------- | --------------------- |
| **Messaging** | post-message, post-thread, update-message, delete-message | Yes (all)             |
| **Channels**  | list-channels, get-channel, channel-history               | No                    |
| **Users**     | list-users, get-user, user-presence                       | No                    |
| **Files**     | upload-file, list-files                                   | Yes (upload only)     |
| **Reactions** | add-reaction, get-reactions                               | No                    |

## Quick Reference

```bash
# Post message to channel
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C1234567890", "text": "Hello from Claude!"}'

# List channels
curl -X GET "https://slack.com/api/conversations.list" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"

# Upload file
curl -X POST https://slack.com/api/files.upload \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -F "channels=C1234567890" \
  -F "file=@report.pdf" \
  -F "title=Weekly Report"
```

## Tool Details

### Messaging Tools (Confirmation Required)

#### post-message

Send a message to a Slack channel.

**Parameters**:

- `channel` (required): Channel ID or name (e.g., "C1234567890" or "#general")
- `text` (required): Message text (supports Slack markdown)
- `thread_ts` (optional): Parent message timestamp for threading
- `blocks` (optional): Rich message blocks (JSON array)

**Example**:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "text": "Deployment successful!",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Deployment Status*\n:white_check_mark: Production deployed successfully"
        }
      }
    ]
  }'
```

#### post-thread

Reply to a message in a thread.

**Parameters**:

- `channel` (required): Channel ID
- `thread_ts` (required): Parent message timestamp
- `text` (required): Reply text

**Example**:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "thread_ts": "1234567890.123456",
    "text": "Thread reply here"
  }'
```

#### update-message

Update an existing message.

**Parameters**:

- `channel` (required): Channel ID
- `ts` (required): Message timestamp
- `text` (required): New message text

**Example**:

```bash
curl -X POST https://slack.com/api/chat.update \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "ts": "1234567890.123456",
    "text": "Updated message"
  }'
```

#### delete-message

Delete a message.

**Parameters**:

- `channel` (required): Channel ID
- `ts` (required): Message timestamp

**Example**:

```bash
curl -X POST https://slack.com/api/chat.delete \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "ts": "1234567890.123456"
  }'
```

### Channel Tools

#### list-channels

List all channels in workspace.

**Parameters**:

- `types` (optional): Comma-separated channel types (default: "public_channel")
  - Options: "public_channel", "private_channel", "mpim", "im"
- `limit` (optional): Max channels to return (default: 100)

**Example**:

```bash
curl -X GET "https://slack.com/api/conversations.list?types=public_channel,private_channel" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

#### get-channel

Get channel information.

**Parameters**:

- `channel` (required): Channel ID

**Example**:

```bash
curl -X GET "https://slack.com/api/conversations.info?channel=C1234567890" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

#### channel-history

Get channel message history.

**Parameters**:

- `channel` (required): Channel ID
- `limit` (optional): Max messages to return (default: 100)
- `oldest` (optional): Start of time range (Unix timestamp)
- `latest` (optional): End of time range (Unix timestamp)

**Example**:

```bash
curl -X GET "https://slack.com/api/conversations.history?channel=C1234567890&limit=50" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

**Security Note**: Channel history may contain sensitive information. Use with caution.

### User Tools

#### list-users

List all users in workspace.

**Parameters**:

- `limit` (optional): Max users to return (default: 100)

**Example**:

```bash
curl -X GET "https://slack.com/api/users.list" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

#### get-user

Get user profile information.

**Parameters**:

- `user` (required): User ID

**Example**:

```bash
curl -X GET "https://slack.com/api/users.info?user=U1234567890" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

#### user-presence

Get user online status.

**Parameters**:

- `user` (required): User ID

**Example**:

```bash
curl -X GET "https://slack.com/api/users.getPresence?user=U1234567890" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

### File Tools

#### upload-file (Confirmation Required)

Upload a file to Slack channel.

**Parameters**:

- `channels` (required): Comma-separated channel IDs
- `file` (required): File path to upload
- `title` (optional): File title
- `initial_comment` (optional): Message text

**Example**:

```bash
curl -X POST https://slack.com/api/files.upload \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -F "channels=C1234567890" \
  -F "file=@C:\reports\weekly.pdf" \
  -F "title=Weekly Report" \
  -F "initial_comment=Here is this week's report"
```

#### list-files

List files in channel.

**Parameters**:

- `channel` (optional): Channel ID to filter by
- `user` (optional): User ID to filter by
- `count` (optional): Max files to return (default: 100)

**Example**:

```bash
curl -X GET "https://slack.com/api/files.list?channel=C1234567890" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

### Reaction Tools

#### add-reaction

Add emoji reaction to a message.

**Parameters**:

- `channel` (required): Channel ID
- `timestamp` (required): Message timestamp
- `name` (required): Emoji name (without colons, e.g., "thumbsup")

**Example**:

```bash
curl -X POST https://slack.com/api/reactions.add \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C1234567890",
    "timestamp": "1234567890.123456",
    "name": "thumbsup"
  }'
```

#### get-reactions

Get reactions on a message.

**Parameters**:

- `channel` (required): Channel ID
- `timestamp` (required): Message timestamp

**Example**:

```bash
curl -X GET "https://slack.com/api/reactions.get?channel=C1234567890&timestamp=1234567890.123456" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

## Agent Integration

### Primary Agents

- **devops**: Infrastructure alerts, deployment notifications, monitoring
- **incident-responder**: Incident alerts, status updates, escalations

### Secondary Agents

- **pm**: Sprint notifications, milestone updates, team announcements
- **developer**: Build notifications, PR alerts, test results
- **qa**: Test failure alerts, quality reports
- **security-architect**: Security alerts, vulnerability notifications

## Common Use Cases

### Deployment Notifications

```bash
# Notify channel of successful deployment
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#deployments",
    "text": ":rocket: Production deployment completed",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Production Deployment*\n:white_check_mark: v1.2.3 deployed successfully\n*Duration:* 5m 23s"
        }
      }
    ]
  }'
```

### Incident Alerts

```bash
# Alert on-call team of incident
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#incidents",
    "text": "<!channel> :rotating_light: High severity incident detected",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Incident INC-1234*\n:rotating_light: *Severity:* P1\n*Service:* API Gateway\n*Status:* 503 errors increasing"
        }
      }
    ]
  }'
```

### Test Results

```bash
# Post test results
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#qa",
    "text": "Test suite completed",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "*Test Results*\n:white_check_mark: 245 passed\n:x: 3 failed\n:warning: 2 skipped"
        }
      }
    ]
  }'
```

## Security Considerations

### Token Security

- **NEVER** expose bot token in logs or error messages
- Store token in environment variable, not in code
- Use least-privilege scopes for bot token
- Rotate tokens periodically

### Message Security

- All message operations require confirmation
- Channel history may contain sensitive information (PII, credentials, etc.)
- Validate channel permissions before posting
- Use private channels for sensitive communications

### Data Privacy

- Comply with workspace data retention policies
- Avoid posting PII or credentials in messages
- Use Slack's data export features for compliance
- Respect user privacy and online status

## Error Handling

### Common Errors

| Error               | Cause                         | Solution                                 |
| ------------------- | ----------------------------- | ---------------------------------------- |
| `not_authed`        | Missing or invalid token      | Check `SLACK_BOT_TOKEN` is set correctly |
| `channel_not_found` | Invalid channel ID            | Verify channel ID with `list-channels`   |
| `missing_scope`     | Bot lacks required permission | Add scope in Slack App settings          |
| `rate_limited`      | Too many requests             | Implement exponential backoff            |
| `message_not_found` | Invalid timestamp             | Check message timestamp is correct       |

### Retry Strategy

For rate limiting errors, implement exponential backoff:

1. Wait 1 second, retry
2. Wait 2 seconds, retry
3. Wait 4 seconds, retry
4. Wait 8 seconds, retry
5. Give up after 5 attempts

## Rate Limits

Slack API rate limits:

- **Tier 1**: 1 request per second
- **Tier 2**: 20 requests per minute
- **Tier 3**: 50 requests per minute
- **Tier 4**: 100 requests per minute

Methods by tier:

- `chat.postMessage`: Tier 3 (50/min)
- `conversations.list`: Tier 2 (20/min)
- `users.list`: Tier 2 (20/min)
- `files.upload`: Tier 4 (100/min)

## Related

- Slack API Documentation: https://api.slack.com/docs
- Block Kit Builder: https://app.slack.com/block-kit-builder
- Slack App Management: https://api.slack.com/apps
