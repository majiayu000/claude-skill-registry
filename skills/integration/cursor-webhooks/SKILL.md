---
name: cursor-webhooks
description: >
  Receive and verify Cursor Cloud Agent webhooks. Use when setting up Cursor
  webhook handlers, debugging signature verification, or handling Cloud Agent
  status change events (ERROR, FINISHED).
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Cursor Webhooks

## When to Use This Skill

- Setting up Cursor Cloud Agent webhook handlers
- Debugging signature verification failures
- Understanding Cursor webhook event types and payloads
- Handling Cloud Agent status change events (ERROR, FINISHED)

## Essential Code (USE THIS)

### Cursor Signature Verification (JavaScript)

```javascript
const crypto = require('crypto');

function verifyCursorWebhook(rawBody, signatureHeader, secret) {
  if (!signatureHeader || !secret) return false;

  // Cursor sends: sha256=xxxx
  const [algorithm, signature] = signatureHeader.split('=');
  if (algorithm !== 'sha256') return false;

  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');

  try {
    return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected));
  } catch {
    return false;
  }
}
```

### Express Webhook Handler

```javascript
const express = require('express');
const app = express();

// CRITICAL: Use express.raw() - Cursor requires raw body for signature verification
app.post('/webhooks/cursor',
  express.raw({ type: 'application/json' }),
  (req, res) => {
    const signature = req.headers['x-webhook-signature'];
    const webhookId = req.headers['x-webhook-id'];
    const event = req.headers['x-webhook-event'];

    // Verify signature
    if (!verifyCursorWebhook(req.body, signature, process.env.CURSOR_WEBHOOK_SECRET)) {
      console.error('Cursor signature verification failed');
      return res.status(401).send('Invalid signature');
    }

    // Parse payload after verification
    const payload = JSON.parse(req.body.toString());

    console.log(`Received ${event} (id: ${webhookId})`);

    // Handle status changes
    if (event === 'statusChange') {
      console.log(`Agent ${payload.id} status: ${payload.status}`);

      if (payload.status === 'FINISHED') {
        console.log(`Summary: ${payload.summary}`);
      } else if (payload.status === 'ERROR') {
        console.error(`Agent error for ${payload.id}`);
      }
    }

    res.json({ received: true });
  }
);
```

### Python Signature Verification (FastAPI)

```python
import hmac
import hashlib
from fastapi import Request, HTTPException

def verify_cursor_webhook(body: bytes, signature_header: str, secret: str) -> bool:
    if not signature_header or not secret:
        return False

    # Cursor sends: sha256=xxxx
    parts = signature_header.split('=')
    if len(parts) != 2 or parts[0] != 'sha256':
        return False

    signature = parts[1]
    expected = hmac.new(
        secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    # Timing-safe comparison
    return hmac.compare_digest(signature, expected)
```

## Common Event Types

| Event Type | Description | Common Use Cases |
|------------|-------------|------------------|
| `statusChange` | Agent status changed | Monitor agent completion, handle errors |

### Event Payload Structure

```json
{
  "event": "statusChange",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "id": "agent_123456",
  "status": "FINISHED",  // or "ERROR"
  "source": {
    "repository": "https://github.com/user/repo",
    "ref": "main"
  },
  "target": {
    "url": "https://github.com/user/repo/pull/123",
    "branchName": "feature-branch",
    "prUrl": "https://github.com/user/repo/pull/123"
  },
  "summary": "Updated 3 files and fixed linting errors"
}
```

## Environment Variables

```bash
# Your Cursor webhook signing secret
CURSOR_WEBHOOK_SECRET=your_webhook_secret_here
```

## Local Development

For local webhook testing, install Hookdeck CLI:

```bash
# Install via npm
npm install -g hookdeck-cli

# Or via Homebrew
brew install hookdeck/hookdeck/hookdeck
```

Then start the tunnel:

```bash
hookdeck listen 3000 --path /webhooks/cursor
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Resources

- `overview.md` - What Cursor webhooks are, event types
- `setup.md` - Configure webhooks in Cursor dashboard
- `verification.md` - Signature verification details and gotchas
- `examples/` - Runnable examples per framework

## Recommended: webhook-handler-patterns

For production-ready webhook handling, also use the webhook-handler-patterns skill:

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md)
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md)
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md)
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md)

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe webhook handling
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub webhook handling
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify webhook handling
- [openai-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/openai-webhooks) - OpenAI webhook handling
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Webhook infrastructure that replaces your queue — guaranteed delivery, automatic retries, replay, rate limiting, and observability for your webhook handlers