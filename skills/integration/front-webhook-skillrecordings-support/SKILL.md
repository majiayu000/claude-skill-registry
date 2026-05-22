---
name: front-webhook
description: Handle Front webhook events for the support platform. Use when implementing conversation ingestion, message handlers, Front API integrations, or webhook signature verification.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Front Webhook Handler

Front is the **source of truth for all conversations**. Every support interaction starts with a Front webhook.

## ⚠️ CRITICAL: Webhooks Send PREVIEWS, Not Full Data

**This is the #1 gotcha with Front integration.** Webhooks do NOT contain the full message body or sender email. You MUST fetch via API.

## Key Insight: Webhooks Send PREVIEWS

Front webhooks send **event previews**, NOT full data. You get:
- IDs and `_links` for resources
- Basic metadata

You do NOT get:
- Full message body
- Author email address
- Conversation history

**Must fetch full data via Front API** using the `_links` in the preview.

## Front Signature Verification

Front uses a **different format** than Stripe-style:

```typescript
// Headers from Front:
// x-front-signature: base64-encoded HMAC
// x-front-request-timestamp: milliseconds
// x-front-challenge: present during setup only

function verifyFrontSignature(timestamp: string, body: string, secret: string): string {
  // Format: HMAC-SHA256(timestamp:body), base64 encoded
  const baseString = Buffer.concat([
    Buffer.from(`${timestamp}:`, 'utf8'),
    Buffer.from(body, 'utf8'),
  ]).toString()
  return crypto.createHmac('sha256', secret).update(baseString).digest('base64')
}
```

## Challenge-Response for Setup

When creating/updating a webhook, Front sends a validation request:
- Header: `x-front-challenge: <random-string>`
- Must respond with: `{"challenge": "<value>"}`

```typescript
if (result.challenge) {
  return NextResponse.json({ challenge: result.challenge })
}
```

## Webhook Handler Pattern

```typescript
export async function POST(request: NextRequest) {
  const payload = await request.text()
  const secret = process.env.FRONT_WEBHOOK_SECRET

  // Build headers object
  const headers: Record<string, string> = {}
  request.headers.forEach((value, key) => { headers[key] = value })

  // Verify signature
  const result = verifyFrontWebhook(payload, headers, { secret })
  if (!result.valid) {
    return NextResponse.json({ error: result.error }, { status: 401 })
  }

  // Handle challenge during setup
  if (result.challenge) {
    return NextResponse.json({ challenge: result.challenge })
  }

  // Parse and dispatch to Inngest
  const event = JSON.parse(payload)
  if (event.type === 'inbound_received') {
    await inngest.send({
      name: SUPPORT_INBOUND_RECEIVED,
      data: {
        conversationId: event.payload.conversation.id,
        messageId: event.payload.target.data.id,
        _links: {
          message: event.payload.target.data._links?.self,
          conversation: event.payload.conversation._links?.self,
        },
      },
    })
  }

  return NextResponse.json({ received: true })
}
```

## Local Dev (ngrok)

For local testing, use a tunnel (ngrok) and point the Front webhook to the **exact** tunnel URL:

```bash
ngrok http 3000
# Use the https URL printed by ngrok as the webhook target
```

Do not use wildcard domains for webhook URLs.

## Front Event Types (Application Webhooks)

| Webhook Event | API Event | Description |
|--------------|-----------|-------------|
| `inbound_received` | `inbound` | Incoming message |
| `outbound_sent` | `outbound` | Outbound message sent |
| `conversation_archived` | `archive` | Conversation archived |
| `conversation_reopened` | `reopen` | Conversation reopened |
| `assignee_changed` | `assign`/`unassign` | Assignee changed |
| `tag_added` | `tag` | Tag added |
| `tag_removed` | `untag` | Tag removed |

## Fetching Full Data

```typescript
const front = createFrontClient(process.env.FRONT_API_TOKEN)

// Fetch full message
const message = await front.getMessage(messageId)
// message.body, message.author.email now available

// Fetch conversation history
const history = await front.getConversationMessages(conversationId)
```

## File Locations

- Webhook handler: `apps/front/app/api/webhooks/front/route.ts`
- Front API client: `packages/core/src/front/client.ts`
- Signature verification: `packages/core/src/webhooks/verify.ts`
- Event types reference: `docs/FRONT-EVENTS.md`

## Inbox ID Conversion

Front UI URLs use decimal IDs, but the API uses base-36 with a prefix.

**Formula:** `inb_` + base36(decimal_id)

**Example:**
- UI URL: `https://app.frontapp.com/settings/tim:571743/inboxes/edit/6380615/settings`
- Decimal ID: `6380615`
- Base-36: `3srbb`
- API ID: `inb_3srbb`

**JavaScript conversion:**
```typescript
function frontInboxId(decimalId: number): string {
  return `inb_${decimalId.toString(36)}`
}
// frontInboxId(6380615) → "inb_3srbb"
```

**List all inboxes via API:**
```bash
curl -H "Authorization: Bearer $FRONT_API_TOKEN" "https://api2.frontapp.com/inboxes" | jq '._results[] | {id, name}'
```

**Known Skill Recordings inboxes:**
| Product | Inbox ID | Email |
|---------|----------|-------|
| Total TypeScript | `inb_3srbb` | team@totaltypescript.com |
| Pro Tailwind | `inb_3pqh3` | team@protailwind.com |
| Epic Web | `inb_jqs2t` | team@epicweb.dev |
| Testing Accessibility | `inb_3bkef` | team@testingaccessibility.com |
| Just JavaScript | `inb_2odqf` | team@overreacted.io |
| Pro NextJS | `inb_43olj` | team@pronextjs.dev |
| AI Hero | `inb_4bj7r` | team@aihero.dev |
| ScriptKit | `inb_41c3r` | team@scriptkit.com |
| Badass Courses | `inb_3mn7r` | team@badass.dev |

## Environment Variables

```bash
FRONT_WEBHOOK_SECRET=  # App signing key (32-char hex)
FRONT_API_TOKEN=       # API token for fetching data
```

## Reference Docs

- `docs/FRONT-EVENTS.md` - Event types and payload structure
- `docs/support-app-prd/76-front-integration.md` - Full integration spec
