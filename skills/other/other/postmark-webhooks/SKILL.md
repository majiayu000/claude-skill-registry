---
name: postmark-webhooks
description: >
  Receive and process Postmark webhooks. Use when setting up Postmark webhook
  handlers, handling email delivery events, processing bounces, opens, clicks,
  spam complaints, or subscription changes.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Postmark Webhooks

## When to Use This Skill

- Setting up Postmark webhook handlers for email event tracking
- Processing email delivery events (bounce, delivered, open, click)
- Handling spam complaints and subscription changes
- Implementing email engagement analytics
- Troubleshooting webhook authentication issues

## Essential Code

### Authentication

Postmark does NOT use signature verification. Instead, webhooks are authenticated by including credentials in the webhook URL itself.

```javascript
// Express - Basic Auth in URL
// Configure webhook URL in Postmark as:
// https://username:password@yourdomain.com/webhooks/postmark

app.post('/webhooks/postmark', express.json(), (req, res) => {
  // Basic auth is handled by your web server or proxy
  // Additional validation can check expected payload structure

  const event = req.body;

  // Validate expected fields exist
  if (!event.RecordType || !event.MessageID) {
    return res.status(400).send('Invalid payload structure');
  }

  // Process event
  console.log(`Received ${event.RecordType} event for ${event.Email}`);

  res.sendStatus(200);
});

// Alternative: Token in URL
// Configure webhook URL as:
// https://yourdomain.com/webhooks/postmark?token=your-secret-token

app.post('/webhooks/postmark', express.json(), (req, res) => {
  const token = req.query.token;

  if (token !== process.env.POSTMARK_WEBHOOK_TOKEN) {
    return res.status(401).send('Unauthorized');
  }

  const event = req.body;
  console.log(`Received ${event.RecordType} event`);

  res.sendStatus(200);
});
```

### Handling Multiple Events

```javascript
// Postmark sends one event per request (not batched)
app.post('/webhooks/postmark', express.json(), (req, res) => {
  const event = req.body;

  switch (event.RecordType) {
    case 'Bounce':
      console.log(`Bounce: ${event.Email} - ${event.Type} - ${event.Description}`);
      // Update contact as undeliverable
      break;

    case 'SpamComplaint':
      console.log(`Spam complaint: ${event.Email}`);
      // Remove from mailing list
      break;

    case 'Open':
      console.log(`Email opened: ${event.Email} at ${event.ReceivedAt}`);
      // Track engagement
      break;

    case 'Click':
      console.log(`Link clicked: ${event.Email} - ${event.OriginalLink}`);
      // Track click-through rate
      break;

    case 'Delivery':
      console.log(`Delivered: ${event.Email} at ${event.DeliveredAt}`);
      // Confirm delivery
      break;

    case 'SubscriptionChange':
      console.log(`Subscription change: ${event.Email} - ${event.ChangedAt}`);
      // Update subscription preferences
      break;

    case 'Inbound':
      console.log(`Inbound email from: ${event.Email} - Subject: ${event.Subject}`);
      // Process incoming email
      break;

    case 'SMTP API Error':
      console.log(`SMTP API error: ${event.Email} - ${event.Error}`);
      // Handle API error, maybe retry
      break;

    default:
      console.log(`Unknown event type: ${event.RecordType}`);
  }

  res.sendStatus(200);
});
```

## Common Event Types

| Event | RecordType | Description | Key Fields |
|-------|------------|-------------|------------|
| Bounce | `Bounce` | Hard/soft bounce or blocked email | Email, Type, TypeCode, Description |
| Spam Complaint | `SpamComplaint` | Recipient marked as spam | Email, BouncedAt |
| Open | `Open` | Email opened (requires open tracking) | Email, ReceivedAt, Platform, UserAgent |
| Click | `Click` | Link clicked (requires click tracking) | Email, ClickedAt, OriginalLink |
| Delivery | `Delivery` | Successfully delivered | Email, DeliveredAt, Details |
| Subscription Change | `SubscriptionChange` | Unsubscribe/resubscribe | Email, ChangedAt, SuppressionReason |
| Inbound | `Inbound` | Incoming email received | Email, FromFull, Subject, TextBody, HtmlBody |
| SMTP API Error | `SMTP API Error` | SMTP API call failed | Email, Error, ErrorCode, MessageID |

## Environment Variables

```bash
# For token-based authentication
POSTMARK_WEBHOOK_TOKEN="your-secret-token-here"

# For basic auth (if not using URL-embedded credentials)
WEBHOOK_USERNAME="your-username"
WEBHOOK_PASSWORD="your-password"
```

## Security Best Practices

1. **Always use HTTPS** - Never configure webhooks with HTTP URLs
2. **Use strong credentials** - Generate long, random tokens or passwords
3. **Validate payload structure** - Check for expected fields before processing
4. **Implement IP allowlisting** - Postmark publishes their IP ranges
5. **Consider using a webhook gateway** - Like Hookdeck for additional security layers

## Local Development

For local webhook testing, use Hookdeck CLI:

```bash
brew install hookdeck/hookdeck/hookdeck
hookdeck listen 3000 --path /webhooks/postmark
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Resources

- [overview.md](references/overview.md) - What Postmark webhooks are, common event types
- [setup.md](references/setup.md) - Configure webhooks in Postmark dashboard
- [verification.md](references/verification.md) - Authentication methods and security best practices
- [examples/](examples/) - Complete implementations for Express, Next.js, and FastAPI

## Recommended: webhook-handler-patterns

For production-ready webhook handling, also install the webhook-handler-patterns skill:

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md) - Webhook processing flow
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md) - Prevent duplicate processing
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md) - Graceful error recovery
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md) - Handle transient failures

## Related Skills

- [sendgrid-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/sendgrid-webhooks) - SendGrid webhook handling with ECDSA verification
- [resend-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/resend-webhooks) - Resend webhook handling with Svix signatures
- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe webhook handling with HMAC-SHA256
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Production webhook infrastructure