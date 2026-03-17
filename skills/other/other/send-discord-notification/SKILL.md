---
name: send-discord-notification
version: "2.0.0"
description: >
  Send a notification to Discord via the Discord MCP server. Supports different
  notification types: health reports, issue alerts, investigation results,
  and escalations. Uses channel names for routing. Keywords: Discord,
  notification, alert, message, MCP.
metadata:
  domain: general
  category: notifications
  requires-approval: false
  confidence: 0.95
dependencies:
  mcp-servers:
    - discord-mcp-server
  skills: []
  tools: []
execution:
  timeout: 30s
  retries: 2
  backoff: exponential
---

# Send Discord Notification

Send notifications to Discord using the Discord MCP server.

## When to Use

- Need to notify humans about status changes or alerts
- Want to post rich formatted messages with embeds
- Sending health reports, issue alerts, or investigation results
- Keywords: discord, notify, alert, message, post

## Prerequisites

Before applying this skill, verify:

- [ ] DISCORD_MCP_URL environment variable is set (or use default)
- [ ] Target channel exists in the Discord server
- [ ] Message content or embed data is available

## Input Schema

```json
{
  "type": "string - Notification type: health | issue | investigation | success | failure | escalation",
  "title": "string - Notification title",
  "description": "string - Main message content",
  "channel_name": "string - Target channel (default: kubani-alerts)",
  "resource": "string - Optional resource identifier",
  "namespace": "string - Optional Kubernetes namespace",
  "severity": "string - Optional severity: low | medium | high | critical",
  "fields": "array - Optional additional fields [{name, value, inline}]"
}
```

## Actions

### 1. Determine Notification Type and Color

Map notification type to Discord embed color:

| Type | Color | Hex |
|------|-------|-----|
| health | Green | 0x57F287 |
| success | Green | 0x57F287 |
| issue | Orange | 0xF39C12 |
| investigation | Blue | 0x5865F2 |
| failure | Red | 0xED4245 |
| escalation | Red | 0xED4245 |

### 2. Build Discord Embed

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  embed:
    title: $title
    description: $description
    color: $type_color
    fields: $fields
    footer:
      text: "Kubani AI Agent"
    timestamp: $current_timestamp
timeout: 30s
on_error: retry
```

### 3. Send Message

Use the Discord MCP server to send the formatted message.

```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: $channel_name
  content: $plain_text_content  # Optional, if no embed
  embed: $formatted_embed       # Optional, for rich messages
```

## Output Schema

```json
{
  "status": "success | failed",
  "message_id": "string - Discord message ID if successful",
  "channel": "string - Channel where message was posted",
  "error": "string - Error message if failed"
}
```

## Success Criteria

The skill succeeds when:

- [ ] Message ID returned from Discord MCP server
- [ ] No error in response
- [ ] Message appears in target channel

## Failure Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Channel not found | Log error, check channel name |
| MCP server unavailable | Retry with exponential backoff |
| Rate limited | Wait and retry |
| Permission denied | Escalate to human |

## Examples

### Example 1: Issue Alert

**Input:**
```json
{
  "type": "issue",
  "title": "CrashLoopBackOff Detected",
  "description": "Pod has restarted 5 times in the last 10 minutes",
  "channel_name": "kubani-alerts",
  "resource": "nginx-deployment-abc123",
  "namespace": "production",
  "severity": "high"
}
```

**MCP Tool Call:**
```yaml
mcp_tool: discord-mcp-server/send_message_to_channel_name
params:
  channel_name: kubani-alerts
  embed:
    title: "⚠️ CrashLoopBackOff Detected"
    description: "Pod has restarted 5 times in the last 10 minutes"
    color: 15908140  # Orange
    fields:
      - name: "Resource"
        value: "nginx-deployment-abc123"
        inline: true
      - name: "Namespace"
        value: "production"
        inline: true
      - name: "Severity"
        value: "HIGH"
        inline: true
    footer:
      text: "Kubani K8s Monitor"
```

### Example 2: Health Report

**Input:**
```json
{
  "type": "health",
  "title": "Cluster Health Check",
  "description": "All systems operational",
  "channel_name": "kubani-alerts"
}
```

**Output:**
```json
{
  "status": "success",
  "message_id": "1234567890",
  "channel": "kubani-alerts"
}
```

## Related Skills

- [request-discord-approval](../request-discord-approval/SKILL.md) - When human approval is needed
- [publish-discord](../../../news/publishing/publish-discord/SKILL.md) - For news digests

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-11 | Migrated to Discord MCP server from webhooks |
| 1.0.0 | 2025-01-09 | Initial version with webhook support |
