---
name: notifications
description: Webhook payload schemas, provider configurations, event types, and retry logic for notification delivery
---

# Notifications Skill
# Project Autopilot - Webhook notification system
# Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

Reference this skill for webhook configuration, payload formatting, and notification delivery.

---

## Provider Configurations

### Slack

```json
{
  "provider": "slack",
  "type": "incoming_webhook",
  "setup_url": "https://api.slack.com/messaging/webhooks",
  "url_format": "https://hooks.slack.com/services/T00/B00/xxx",
  "features": ["attachments", "blocks", "buttons", "mentions"],
  "rate_limit": "1 msg/sec"
}
```

### Discord

```json
{
  "provider": "discord",
  "type": "webhook",
  "setup_url": "https://discord.com/developers/docs/resources/webhook",
  "url_format": "https://discord.com/api/webhooks/{id}/{token}",
  "features": ["embeds", "mentions", "files"],
  "rate_limit": "5 msg/sec per channel"
}
```

### Microsoft Teams

```json
{
  "provider": "teams",
  "type": "connector",
  "setup_url": "https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/",
  "url_format": "https://outlook.office.com/webhook/{guid}",
  "features": ["adaptive_cards", "actions", "mentions"],
  "rate_limit": "4 msg/sec per connector"
}
```

### Generic Webhook

```json
{
  "provider": "webhook",
  "type": "http_post",
  "url_format": "any valid URL",
  "features": ["custom_payload", "custom_headers"],
  "rate_limit": "none (user configured)"
}
```

---

## Payload Schemas

### Slack Attachment Format

```json
{
  "text": "Notification text (shown in notifications)",
  "attachments": [
    {
      "fallback": "Plain text fallback",
      "color": "#36a64f",
      "pretext": "Optional text above attachment",
      "author_name": "Autopilot",
      "author_icon": "https://example.com/icon.png",
      "title": "Attachment title",
      "title_link": "https://example.com",
      "text": "Attachment body text",
      "fields": [
        {
          "title": "Field Title",
          "value": "Field value",
          "short": true
        }
      ],
      "footer": "Footer text",
      "footer_icon": "https://example.com/footer.png",
      "ts": 1706540400
    }
  ]
}
```

### Slack Block Format

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "Phase Complete"
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Phase:*\n003: Auth"
        },
        {
          "type": "mrkdwn",
          "text": "*Cost:*\n$0.85"
        }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "View Details" },
          "url": "https://example.com/details"
        }
      ]
    }
  ]
}
```

### Discord Embed Format

```json
{
  "content": "Optional text outside embed",
  "embeds": [
    {
      "title": "Embed Title",
      "description": "Embed description",
      "url": "https://example.com",
      "color": 3066993,
      "fields": [
        {
          "name": "Field Name",
          "value": "Field Value",
          "inline": true
        }
      ],
      "author": {
        "name": "Autopilot",
        "icon_url": "https://example.com/icon.png"
      },
      "footer": {
        "text": "Footer text",
        "icon_url": "https://example.com/footer.png"
      },
      "timestamp": "2026-01-29T12:00:00.000Z"
    }
  ]
}
```

### Teams MessageCard Format

```json
{
  "@type": "MessageCard",
  "@context": "http://schema.org/extensions",
  "themeColor": "36a64f",
  "summary": "Summary text",
  "sections": [
    {
      "activityTitle": "Activity Title",
      "activitySubtitle": "Subtitle",
      "activityImage": "https://example.com/image.png",
      "facts": [
        {
          "name": "Fact Name",
          "value": "Fact Value"
        }
      ],
      "markdown": true
    }
  ],
  "potentialAction": [
    {
      "@type": "OpenUri",
      "name": "View Details",
      "targets": [
        {
          "os": "default",
          "uri": "https://example.com"
        }
      ]
    }
  ]
}
```

### Generic Webhook Format

```json
{
  "event": "phase_complete",
  "timestamp": "2026-01-29T12:00:00.000Z",
  "project": {
    "name": "my-project",
    "path": "/path/to/project"
  },
  "phase": {
    "id": "003",
    "name": "Authentication",
    "status": "complete"
  },
  "cost": {
    "estimated": 0.85,
    "actual": 0.92,
    "variance": 8.2
  },
  "tasks": {
    "total": 8,
    "completed": 8
  }
}
```

---

## Event Types

### Lifecycle Events

| Event | When Triggered | Data |
|-------|----------------|------|
| `phase_start` | Phase begins | Phase info, estimate |
| `phase_complete` | Phase passes gate | Phase info, cost, tasks |
| `build_complete` | All phases done | Summary stats |
| `build_failed` | Error occurs | Error details |

### Budget Events

| Event | When Triggered | Data |
|-------|----------------|------|
| `budget_warning` | Warn threshold hit | Current cost, threshold |
| `budget_alert` | Alert threshold hit | Current cost, threshold |
| `budget_exceeded` | Max budget hit | Current cost, max |

### State Events

| Event | When Triggered | Data |
|-------|----------------|------|
| `checkpoint_created` | Save point made | Checkpoint info |
| `rollback` | Rollback executed | From/to phases |
| `project_paused` | Execution paused | Current state |
| `project_resumed` | Execution resumed | Resume state |

---

## Color Codes

### Status Colors

| Status | Hex | Slack | Discord |
|--------|-----|-------|---------|
| Success | `#36a64f` | `good` | 3586615 |
| Warning | `#ff9900` | `warning` | 16750848 |
| Danger | `#ff0000` | `danger` | 16711680 |
| Info | `#3498db` | N/A | 3447003 |

### Usage

```javascript
// Slack
{ "color": "good" }  // or "#36a64f"

// Discord
{ "color": 3586615 }  // Integer representation
```

---

## Configuration Schema

### Global Config Structure

```json
{
  "notifications": {
    "enabled": true,
    "webhooks": {
      "slack": {
        "url": "https://hooks.slack.com/services/...",
        "enabled": true,
        "addedAt": "2026-01-29T00:00:00Z",
        "lastTest": "2026-01-29T12:00:00Z",
        "lastTestSuccess": true
      },
      "discord": {
        "url": "https://discord.com/api/webhooks/...",
        "enabled": true,
        "addedAt": "2026-01-29T00:00:00Z"
      }
    },
    "events": {
      "phase_complete": ["slack", "discord"],
      "build_complete": ["slack", "discord"],
      "budget_alert": ["slack"],
      "build_failed": ["slack", "discord"],
      "checkpoint_created": []
    },
    "defaults": {
      "retryOnFailure": true,
      "maxRetries": 3,
      "retryDelayMs": [1000, 5000, 30000]
    }
  }
}
```

---

## Retry Logic

### Exponential Backoff

```
Attempt 1: Immediate
Attempt 2: Wait 1 second
Attempt 3: Wait 5 seconds
Attempt 4: Wait 30 seconds
(Give up after attempt 4)
```

### Retry Conditions

| HTTP Status | Retry? | Reason |
|-------------|--------|--------|
| 200-299 | No | Success |
| 400 | No | Bad request (fix payload) |
| 401, 403 | No | Auth error (fix config) |
| 404 | No | Endpoint not found |
| 429 | Yes | Rate limited |
| 500-599 | Yes | Server error |
| Timeout | Yes | Network issue |

---

## Security Considerations

### URL Storage

- Store webhook URLs in global config only
- Never log full URLs (mask tokens)
- Validate URL format before storing

### Payload Sanitization

- Never include sensitive data in notifications
- Mask API keys, tokens, passwords
- Limit error messages to safe excerpts

### Verification

- Verify webhook URL on add
- Re-verify periodically
- Track delivery success rate

---

## Testing

### Test Payload

```json
{
  "text": "🧪 Autopilot Test Notification",
  "attachments": [{
    "color": "#3498db",
    "title": "Test Notification",
    "text": "This is a test from Autopilot notification system.",
    "fields": [
      { "title": "Project", "value": "my-project", "short": true },
      { "title": "Time", "value": "2026-01-29 12:00:00", "short": true }
    ],
    "footer": "Autopilot • Test Mode"
  }]
}
```

### Verification Response

```json
{
  "success": true,
  "provider": "slack",
  "latency_ms": 245,
  "response": {
    "ok": true
  }
}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `429 Too Many Requests` | Rate limited | Wait and retry |
| `400 Bad Request` | Invalid payload | Check format |
| `404 Not Found` | Webhook deleted | Reconfigure |
| `Timeout` | Network issue | Check connectivity |
| `SSL Error` | Cert issue | Update CA certs |
