---
name: sendgrid-webhooks
description: >
  Receive and verify SendGrid webhooks. Use when setting up SendGrid webhook
  handlers, debugging signature verification, or handling email delivery events.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# SendGrid Webhooks

## When to Use This Skill

- Setting up SendGrid webhook handlers for email delivery tracking
- Debugging ECDSA signature verification failures
- Processing email events (bounce, delivered, open, click, spam report)
- Implementing email engagement analytics

## Essential Code

### Signature Verification (Manual)

SendGrid uses ECDSA (Elliptic Curve Digital Signature Algorithm) with public key verification.

```javascript
// Node.js manual verification
const crypto = require('crypto');

function verifySignature(publicKey, payload, signature, timestamp) {
  // Decode the base64 signature
  const decodedSignature = Buffer.from(signature, 'base64');

  // Create the signed content
  const signedContent = timestamp + payload;

  // Create verifier
  const verifier = crypto.createVerify('sha256');
  verifier.update(signedContent);

  // Add PEM headers if not present
  let pemKey = publicKey;
  if (!pemKey.includes('BEGIN PUBLIC KEY')) {
    pemKey = `-----BEGIN PUBLIC KEY-----\n${publicKey}\n-----END PUBLIC KEY-----`;
  }

  // Verify the signature
  return verifier.verify(pemKey, decodedSignature);
}

// Express middleware
app.post('/webhooks/sendgrid', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.get('X-Twilio-Email-Event-Webhook-Signature');
  const timestamp = req.get('X-Twilio-Email-Event-Webhook-Timestamp');

  if (!signature || !timestamp) {
    return res.status(400).send('Missing signature headers');
  }

  const publicKey = process.env.SENDGRID_WEBHOOK_VERIFICATION_KEY;
  const payload = req.body.toString();

  if (!verifySignature(publicKey, payload, signature, timestamp)) {
    return res.status(400).send('Invalid signature');
  }

  // Process events
  const events = JSON.parse(payload);
  console.log(`Received ${events.length} events`);

  res.sendStatus(200);
});
```

### Using SendGrid SDK

```javascript
const { EventWebhook } = require('@sendgrid/eventwebhook');

const verifyWebhook = new EventWebhook();
const publicKey = process.env.SENDGRID_WEBHOOK_VERIFICATION_KEY;

app.post('/webhooks/sendgrid', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.get('X-Twilio-Email-Event-Webhook-Signature');
  const timestamp = req.get('X-Twilio-Email-Event-Webhook-Timestamp');

  const isValid = verifyWebhook.verifySignature(
    publicKey,
    req.body,
    signature,
    timestamp
  );

  if (!isValid) {
    return res.status(400).send('Invalid signature');
  }

  // Process webhook
  res.sendStatus(200);
});
```

## Common Event Types

| Event | Description | Use Cases |
|-------|-------------|-----------|
| `processed` | Message has been received and is ready to be delivered | Track email processing |
| `delivered` | Message successfully delivered to recipient | Delivery confirmation |
| `bounce` | Message permanently rejected (includes type='blocked' for blocked messages) | Update contact lists, handle failures |
| `deferred` | Temporary delivery failure | Monitor delays |
| `open` | Recipient opened the email | Engagement tracking |
| `click` | Recipient clicked a link | Link tracking, CTR analysis |
| `spam report` | Email marked as spam | List hygiene, sender reputation |
| `unsubscribe` | Recipient unsubscribed | Update subscription status |
| `group unsubscribe` | Recipient unsubscribed from a group | Update group subscription preferences |
| `group resubscribe` | Recipient resubscribed to a group | Update group subscription preferences |

## Environment Variables

```bash
# Your SendGrid webhook verification key (public key)
SENDGRID_WEBHOOK_VERIFICATION_KEY="MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE..."
```

## Local Development

For local webhook testing, use Hookdeck CLI:

```bash
brew install hookdeck/hookdeck/hookdeck
hookdeck listen 3000 --path /webhooks/sendgrid
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Resources

- [overview.md](references/overview.md) - What SendGrid webhooks are, common event types
- [setup.md](references/setup.md) - Configure webhooks in SendGrid dashboard, get verification key
- [verification.md](references/verification.md) - ECDSA signature verification details and gotchas
- [examples/](examples/) - Complete implementations for Express, Next.js, and FastAPI

## Related Skills

- `webhook-handler-patterns` - Cross-cutting patterns (idempotency, retries, framework guides)
- `hookdeck-event-gateway` - Production infrastructure (routing, replay, monitoring)