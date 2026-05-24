---
name: whatsapp-messaging
description: Send and read WhatsApp messages via Kapso Meta proxy, manage templates (CRUD/send), and upload media. Use when sending messages, creating templates, or reading inbox history.
---

# WhatsApp Messaging

## When to use

Use this skill when working with WhatsApp messaging via Kapso: sending messages, creating/managing templates, uploading media, or reading inbox history.

## Setup

Env vars:
- `KAPSO_API_BASE_URL` (host only, no `/platform/v1`)
- `KAPSO_API_KEY`
- `PROJECT_ID`
- `KAPSO_META_GRAPH_VERSION` (optional, default `v24.0`)

## Discover IDs first

Two Meta IDs are needed for different operations:

| ID | Used for | How to discover |
|----|----------|-----------------|
| `business_account_id` (WABA) | Template CRUD | `node scripts/list-platform-phone-numbers.mjs` |
| `phone_number_id` | Sending messages, media upload | `node scripts/list-platform-phone-numbers.mjs` |

## SDK setup

Install:
```bash
npm install @kapso/whatsapp-cloud-api
```

Create client:
```ts
import { WhatsAppClient } from "@kapso/whatsapp-cloud-api";

const client = new WhatsAppClient({
  baseUrl: "https://api.kapso.ai/meta/whatsapp",
  kapsoApiKey: process.env.KAPSO_API_KEY!
});
```

## How to

### Send a text message

Via SDK:
```ts
await client.messages.sendText({
  phoneNumberId: "<PHONE_NUMBER_ID>",
  to: "+15551234567",
  body: "Hello from Kapso"
});
```

### Send a template message

1. Discover IDs: `node scripts/list-platform-phone-numbers.mjs`
2. Draft template payload from `assets/template-utility-order-status-update.json`
3. Create: `node scripts/create-template.mjs --business-account-id <WABA_ID> --file <payload.json>`
4. Check status: `node scripts/template-status.mjs --business-account-id <WABA_ID> --name <name>`
5. Send: `node scripts/send-template.mjs --phone-number-id <ID> --file <send-payload.json>`

### Send an interactive message

Interactive messages require an active 24-hour session window. For outbound notifications outside the window, use templates.

1. Discover `phone_number_id`
2. Pick payload from `assets/send-interactive-*.json`
3. Send: `node scripts/send-interactive.mjs --phone-number-id <ID> --file <payload.json>`

### Read inbox data

Use Meta proxy or SDK:
- Proxy: `GET /{phone_number_id}/messages`, `GET /{phone_number_id}/conversations`
- SDK: `client.messages.query()`, `client.conversations.list()`

## Template rules

Creation:
- Use `parameter_format: "NAMED"` with `{{param_name}}` (preferred over positional)
- Include examples when using variables in HEADER/BODY
- Use `language` (not `language_code`)
- Don't interleave QUICK_REPLY with URL/PHONE_NUMBER buttons
- URL button variables must be at the end of the URL and use positional `{{1}}`

Send-time:
- For NAMED templates, include `parameter_name` in header/body params
- URL buttons need a `button` component with `sub_type: "url"` and `index`
- Media headers use either `id` or `link` (never both)

## Scripts

| Script | Purpose | Required ID |
|--------|---------|-------------|
| `list-platform-phone-numbers.mjs` | Discover business_account_id + phone_number_id | — |
| `list-connected-numbers.mjs` | List WABA phone numbers | business_account_id |
| `list-templates.mjs` | List templates (with filters) | business_account_id |
| `template-status.mjs` | Check single template status | business_account_id |
| `create-template.mjs` | Create a template | business_account_id |
| `update-template.mjs` | Update existing template | business_account_id |
| `send-template.mjs` | Send template message | phone_number_id |
| `send-interactive.mjs` | Send interactive message | phone_number_id |
| `upload-media.mjs` | Upload media for send-time headers | phone_number_id |

## Assets

| File | Description |
|------|-------------|
| `template-utility-order-status-update.json` | UTILITY template with named params + URL button |
| `send-template-order-status-update.json` | Send-time payload for order_status_update |
| `template-utility-named.json` | UTILITY template showing button ordering rules |
| `template-marketing-media-header.json` | MARKETING template with IMAGE header |
| `template-authentication-otp.json` | AUTHENTICATION OTP template (COPY_CODE) |
| `send-interactive-buttons.json` | Interactive button message |
| `send-interactive-list.json` | Interactive list message |
| `send-interactive-cta-url.json` | Interactive CTA URL message |
| `send-interactive-location-request.json` | Location request message |
| `send-interactive-catalog-message.json` | Catalog message |

## References

- [references/templates-reference.md](references/templates-reference.md) - Template creation rules, components cheat sheet, send-time components
- [references/whatsapp-api-reference.md](references/whatsapp-api-reference.md) - Meta proxy payloads for messages and conversations
- [references/whatsapp-cloud-api-js.md](references/whatsapp-cloud-api-js.md) - SDK usage for sending and reading messages

## Related skills

- `kapso-automation` - Workflow automation
- `whatsapp-flows` - WhatsApp Flows
- `kapso-api` - Platform API and customers
