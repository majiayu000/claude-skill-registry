---
name: kapso-ops
description: Operate and troubleshoot Kapso projects. Manage webhooks, debug message delivery, inspect API errors, and run health checks. Use when diagnosing issues, setting up webhooks, or investigating message failures.
---

# Kapso Ops

## When to use

Use this skill for operational diagnostics: webhook setup, message delivery investigation, error triage, and WhatsApp health checks.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`

## How to

### Set up a webhook

1. Create: `node scripts/create.js --phone-number-id <id> --url <https://...> --events <csv>`
2. Verify signature handling (see `references/webhooks-overview.md`)
3. Test: `node scripts/test.js --webhook-id <id>`

### Investigate message delivery

1. List messages: `node scripts/messages.js --phone-number-id <id>`
2. Inspect message: `node scripts/message-details.js --message-id <id>`
3. Find conversation: `node scripts/lookup-conversation.js --phone-number <e164>`

### Triage errors

1. Message errors: `node scripts/errors.js`
2. API logs: `node scripts/api-logs.js`
3. Webhook deliveries: `node scripts/webhook-deliveries.js`

### Run health checks

1. Project overview: `node scripts/overview.js`
2. Phone number health: `node scripts/whatsapp-health.js --phone-number-id <id>`

## Scripts

### Webhooks

| Script | Purpose |
|--------|---------|
| `list.js` | List webhooks for a phone number |
| `get.js` | Get webhook details |
| `create.js` | Create a webhook |
| `update.js` | Update a webhook |
| `delete.js` | Delete a webhook |
| `test.js` | Send a test event to a webhook |

Common flags for create/update:
- `--url <https://...>` - Webhook URL
- `--events <csv>` - Event types (comma-separated)
- `--kind <kapso|meta>` - Webhook type
- `--payload-version <v1|v2>` - Payload format (v2 recommended)
- `--buffer-enabled <true|false>` - Enable buffering
- `--active <true|false>` - Enable/disable

### Messages

| Script | Purpose |
|--------|---------|
| `messages.js` | List messages |
| `message-details.js` | Get message details |
| `lookup-conversation.js` | Find conversation by phone or ID |

### Errors and logs

| Script | Purpose |
|--------|---------|
| `errors.js` | List message errors |
| `api-logs.js` | List external API logs |
| `webhook-deliveries.js` | List webhook delivery attempts |

### Health

| Script | Purpose |
|--------|---------|
| `overview.js` | Project overview |
| `whatsapp-health.js` | Phone number health check |

## Notes

- Use config-level webhooks for `whatsapp.message.*` events
- Payload version `v2` is recommended for new integrations
- Meta webhooks provide raw payloads; Kapso webhooks support buffering

## References

- [references/webhooks-reference.md](references/webhooks-reference.md) - Webhook API reference
- [references/webhooks-overview.md](references/webhooks-overview.md) - Webhook concepts and setup
- [references/webhooks-event-types.md](references/webhooks-event-types.md) - Available event types
- [references/message-debugging-reference.md](references/message-debugging-reference.md) - Message debugging guide
- [references/triage-reference.md](references/triage-reference.md) - Error triage guide
- [references/health-reference.md](references/health-reference.md) - Health check guide

## Related skills

- `kapso-automation` - Automation and functions
- `whatsapp-messaging` - WhatsApp messaging
- `kapso-api` - Platform API and customers
