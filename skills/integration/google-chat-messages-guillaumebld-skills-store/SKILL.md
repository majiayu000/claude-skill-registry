---
name: google-chat-messages
description: "Send Google Chat messages via webhook — text, rich cards (cardsV2), threaded replies. Includes TypeScript types, card builder utility, and widget reference."
---

# Google Chat Messages

Send messages to Google Chat spaces via incoming webhooks. Produces text messages, rich cards (cardsV2), and threaded replies.

## What You Produce

- Text messages with Google Chat formatting
- Rich card messages (cardsV2) with headers, sections, widgets
- Threaded conversations
- Reusable webhook sender utility

## Workflow

### Step 1: Get Webhook URL

In Google Chat:
1. Open a Space > click space name > **Manage webhooks**
2. Create webhook (name it, optionally add avatar URL)
3. Copy the webhook URL

Store the URL as a secret (environment variable or Bitwarden), never hardcode.

### Step 2: Choose Message Type

| Need | Type | Complexity |
|------|------|------------|
| Simple notification | Text message | Low |
| Structured info (status, digest) | Card message (cardsV2) | Medium |
| Ongoing updates | Threaded replies | Medium |
| Action buttons (open URL) | Card with buttonList | Medium |

### Step 3: Send the Message

Use `assets/webhook-sender.ts` for the sender utility. Use `assets/card-builder.ts` for structured card construction.

## Text Formatting

Google Chat does NOT use standard Markdown.

| Format | Syntax | Example |
|--------|--------|---------|
| Bold | `*text*` | `*important*` |
| Italic | `_text_` | `_emphasis_` |
| Strikethrough | `~text~` | `~removed~` |
| Monospace | `` `text` `` | `` `code` `` |
| Code block | ` ```text``` ` | Multi-line code |
| Link | `<url\|text>` | `<https://example.com\|Click here>` |
| Mention user | `<users/USER_ID>` | `<users/123456>` |
| Mention all | `<users/all>` | `<users/all>` |

**Not supported**: `**double asterisks**`, headings (`###`), blockquotes, tables, images inline.

### Text Message Example

```typescript
await sendText(webhookUrl, '*Build Complete*\n\nBranch: `main`\nStatus: Passed\n<https://ci.example.com/123|View Build>');
```

## cardsV2 Structure

Cards use the cardsV2 format (recommended over legacy cards).

```typescript
const message = {
  cardsV2: [{
    cardId: 'unique-id',
    card: {
      header: {
        title: 'Card Title',
        subtitle: 'Optional subtitle',
        imageUrl: 'https://example.com/icon.png',
        imageType: 'CIRCLE'  // or 'SQUARE'
      },
      sections: [{
        header: 'Section Title',  // optional
        widgets: [
          // widgets go here
        ]
      }]
    }
  }]
};
```

### Widget Types

**Text paragraph** — formatted text block:
```typescript
{ textParagraph: { text: '*Bold* and _italic_ text' } }
```

**Decorated text** — label + value with optional icon:
```typescript
{
  decoratedText: {
    topLabel: 'Status',
    text: 'Deployed',
    startIcon: { knownIcon: 'STAR' }
  }
}
```

**Button list** — action buttons:
```typescript
{
  buttonList: {
    buttons: [{
      text: 'View Dashboard',
      onClick: { openLink: { url: 'https://dashboard.example.com' } }
    }]
  }
}
```

**Image** — standalone image:
```typescript
{ image: { imageUrl: 'https://example.com/chart.png', altText: 'Usage chart' } }
```

**Divider** — horizontal separator:
```typescript
{ divider: {} }
```

See `references/widget-reference.md` for all widget types with full examples.
See `references/icon-list.md` for all available knownIcon values.

## Threading

Thread messages together using `threadKey`:

```typescript
// First message — creates thread
const response = await sendCard(webhookUrl, card, {
  threadKey: 'deploy-2026-02-16'
});

// Reply to thread — append &messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD
const threadUrl = `${webhookUrl}&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD`;
await sendCard(threadUrl, replyCard, {
  threadKey: 'deploy-2026-02-16'
});
```

The `threadKey` is a client-assigned string. Use consistent keys for related messages (e.g., `deploy-{date}`, `alert-{id}`).

## Common Patterns

### Notification Card

```typescript
import { buildCard, sendCard } from './assets/card-builder';
import { sendWebhook } from './assets/webhook-sender';

const card = buildCard({
  cardId: 'deploy-notification',
  title: 'Deployment Complete',
  subtitle: 'production - v2.1.0',
  imageUrl: 'https://www.jezweb.com.au/wp-content/uploads/2020/03/favicon-100x100.png',
  sections: [{
    widgets: [
      { decoratedText: { topLabel: 'Environment', text: 'Production' } },
      { decoratedText: { topLabel: 'Version', text: 'v2.1.0' } },
      { decoratedText: { topLabel: 'Status', text: '*Healthy*', startIcon: { knownIcon: 'STAR' } } },
      { buttonList: { buttons: [{ text: 'View Deployment', onClick: { openLink: { url: 'https://dash.example.com' } } }] } }
    ]
  }]
});
```

### Digest Card (Weekly Summary)

```typescript
const digest = buildCard({
  cardId: 'weekly-digest',
  title: 'Weekly Summary',
  subtitle: `${count} updates this week`,
  sections: [
    {
      header: 'Highlights',
      widgets: items.map(item => ({
        decoratedText: { text: item.title, bottomLabel: item.date }
      }))
    },
    {
      widgets: [{
        buttonList: {
          buttons: [{ text: 'View All', onClick: { openLink: { url: dashboardUrl } } }]
        }
      }]
    }
  ]
});
```

### Simple Text Alert

```typescript
await sendText(webhookUrl, `*Alert*: CPU usage above 90% on \`worker-prod-1\`\n<${alertUrl}|View Alert>`);
```

## Error Prevention

| Mistake | Fix |
|---------|-----|
| `**bold**` in text | Use `*bold*` (single asterisks) |
| `[text](url)` links | Use `<url\|text>` format |
| Missing `cardsV2` wrapper | Wrap card in `{ cardsV2: [{ cardId, card }] }` |
| Thread replies not threading | Append `&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD` to webhook URL |
| Webhook returns 400 | Check JSON structure — common issue is missing `text` or `cardsV2` at top level |
| Card not showing | Ensure `sections` has at least one widget |

## Asset Files

| File | Purpose |
|------|---------|
| `assets/types.ts` | TypeScript type definitions for cardsV2 |
| `assets/card-builder.ts` | Utility to build card messages |
| `assets/webhook-sender.ts` | POST to webhook with error handling |
