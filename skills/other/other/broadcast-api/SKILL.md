---
name: broadcast-api
description: Reference documentation for Broadcast API (sendbroadcast.net) integration. Use when working with the Broadcast email provider, creating/updating broadcasts, managing subscribers, or debugging API issues.
---

<objective>
Provide accurate, up-to-date documentation for integrating with the Broadcast API in the Payload Newsletter Plugin.
</objective>

<essential_principles>
- Broadcast is a self-hosted email marketing platform at sendbroadcast.net
- All API requests require Bearer token authentication
- Base URL is your Broadcast instance domain (not sendbroadcast.net)
- API responses use standard HTTP status codes
</essential_principles>

<quick_reference>

**Authentication:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Base endpoints:**
- `GET /api/v1/broadcasts` - List broadcasts
- `POST /api/v1/broadcasts` - Create broadcast
- `GET /api/v1/broadcasts/:id` - Get broadcast
- `PATCH /api/v1/broadcasts/:id` - Update broadcast
- `DELETE /api/v1/broadcasts/:id` - Delete broadcast
- `POST /api/v1/broadcasts/:id/send_broadcast` - Send broadcast

- `GET /api/v1/subscribers.json` - List subscribers
- `GET /api/v1/subscribers/find.json?email=` - Find subscriber
- `POST /api/v1/subscribers.json` - Create subscriber
- `PATCH /api/v1/subscribers.json` - Update subscriber
- `POST /api/v1/subscribers/unsubscribe.json` - Unsubscribe
- `POST /api/v1/subscribers/resubscribe.json` - Resubscribe

**Broadcast statuses:**
`draft` | `scheduled` | `queueing` | `sending` | `sent` | `failed` | `partial_failure` | `aborted` | `paused`
</quick_reference>

<routing>
| Topic | Reference File |
|-------|----------------|
| Broadcasts API (CRUD, sending, statistics) | references/broadcasts-api.md |
| Subscribers API (CRUD, tags, filtering) | references/subscribers-api.md |
| Authentication & tokens | references/authentication.md |
| Overview & general info | references/overview.md |

Read the appropriate reference file based on what you're working on.
</routing>

<common_issues>

**401 Unauthorized:**
- Token expired or revoked
- Token lacks required permissions (Read vs Write)
- Missing `Bearer ` prefix in Authorization header

**404 Not Found:**
- Broadcast/subscriber doesn't exist
- Wrong base URL (using sendbroadcast.net instead of your instance)

**422 Unprocessable Entity:**
- Missing required fields (subject, body for broadcasts)
- Invalid email format for subscribers
- Trying to update a sent broadcast

**Body format for broadcasts:**
- Must be valid HTML
- Use `<br>` for line breaks, `<p>` for paragraphs
- Don't include `<html>`, `<head>`, `<body>` tags - Broadcast wraps content automatically
</common_issues>

<integration_notes>
In this plugin, the Broadcast provider is at `src/providers/broadcast/broadcast.ts`

Key configuration:
```typescript
{
  baseUrl: 'https://your-broadcast-instance.com',
  token: 'your_access_token',
  fromEmail: 'newsletter@yourdomain.com',
  fromName: 'Your Name',
  replyTo: 'reply@yourdomain.com'
}
```

The plugin creates broadcasts in Payload first, then syncs to Broadcast on first update with content (subject + body).
</integration_notes>

<success_criteria>
- API calls use correct endpoints and methods
- Authentication header is properly formatted
- Request bodies match expected schema
- Error responses are handled appropriately
</success_criteria>
