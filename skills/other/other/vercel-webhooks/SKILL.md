---
name: vercel-webhooks
description: >
  Receive and verify Vercel webhooks. Use when setting up Vercel webhook
  handlers, debugging signature verification, or handling deployment events
  like deployment.created, deployment.succeeded, or project.created.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Vercel Webhooks

## When to Use This Skill

- Setting up Vercel webhook handlers
- Debugging signature verification failures
- Understanding Vercel event types and payloads
- Handling deployment, project, domain, or integration events
- Monitoring deployment status changes

## Essential Code (USE THIS)

### Express Webhook Handler with Manual Verification

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();

// CRITICAL: Use express.raw() for webhook endpoint - Vercel needs raw body
app.post('/webhooks/vercel',
  express.raw({ type: 'application/json' }),
  async (req, res) => {
    const signature = req.headers['x-vercel-signature'];

    if (!signature) {
      return res.status(400).send('Missing x-vercel-signature header');
    }

    // Verify signature using SHA1 HMAC
    const expectedSignature = crypto
      .createHmac('sha1', process.env.VERCEL_WEBHOOK_SECRET)
      .update(req.body)
      .digest('hex');

    // Use timing-safe comparison
    let signaturesMatch;
    try {
      signaturesMatch = crypto.timingSafeEqual(
        Buffer.from(signature),
        Buffer.from(expectedSignature)
      );
    } catch (err) {
      // Buffer length mismatch = invalid signature
      signaturesMatch = false;
    }

    if (!signaturesMatch) {
      console.error('Invalid Vercel webhook signature');
      return res.status(400).send('Invalid signature');
    }

    // Parse the verified payload
    const event = JSON.parse(req.body.toString());

    // Handle the event
    switch (event.type) {
      case 'deployment.created':
        console.log('Deployment created:', event.payload.deployment.id);
        break;
      case 'deployment.succeeded':
        console.log('Deployment succeeded:', event.payload.deployment.id);
        break;
      case 'deployment.error':
        console.log('Deployment failed:', event.payload.deployment.id);
        break;
      case 'project.created':
        console.log('Project created:', event.payload.project.name);
        break;
      default:
        console.log('Unhandled event:', event.type);
    }

    res.json({ received: true });
  }
);
```

### Python (FastAPI) Webhook Handler

```python
import os
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI()
webhook_secret = os.environ.get("VERCEL_WEBHOOK_SECRET")

@app.post("/webhooks/vercel")
async def vercel_webhook(
    request: Request,
    x_vercel_signature: str = Header(None)
):
    if not x_vercel_signature:
        raise HTTPException(status_code=400, detail="Missing x-vercel-signature header")

    # Get raw body
    body = await request.body()

    # Compute expected signature
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha1
    ).hexdigest()

    # Timing-safe comparison
    if not hmac.compare_digest(x_vercel_signature, expected_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Parse verified payload
    event = await request.json()

    # Handle event
    if event["type"] == "deployment.created":
        print(f"Deployment created: {event['payload']['deployment']['id']}")
    elif event["type"] == "deployment.succeeded":
        print(f"Deployment succeeded: {event['payload']['deployment']['id']}")
    # ... handle other events

    return {"received": True}
```

> **For complete working examples with tests**, see:
> - [examples/express/](examples/express/) - Full Express implementation
> - [examples/nextjs/](examples/nextjs/) - Next.js App Router implementation
> - [examples/fastapi/](examples/fastapi/) - Python FastAPI implementation

## Common Event Types

| Event | Triggered When | Common Use Cases |
|-------|----------------|------------------|
| `deployment.created` | A new deployment starts | Start deployment monitoring, notify team |
| `deployment.succeeded` | Deployment completes successfully | Update status, trigger post-deploy tasks |
| `deployment.error` | Deployment fails | Alert team, rollback actions |
| `deployment.canceled` | Deployment is canceled | Clean up resources |
| `project.created` | New project is created | Set up monitoring, configure resources |
| `project.removed` | Project is deleted | Clean up external resources |
| `domain.created` | Domain is added | Update DNS, SSL configuration |

See [references/overview.md](references/overview.md) for the complete event list.

## Environment Variables

```bash
# Required
VERCEL_WEBHOOK_SECRET=your_webhook_secret_from_dashboard

# Optional (for API calls)
VERCEL_TOKEN=your_vercel_api_token
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
hookdeck listen 3000 --path /webhooks/vercel
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Reference Materials

- [Webhook Overview](references/overview.md) - What Vercel webhooks are, all event types
- [Setup Guide](references/setup.md) - Configure webhooks in Vercel dashboard
- [Signature Verification](references/verification.md) - SHA1 HMAC verification details

## Recommended: webhook-handler-patterns

For production-ready webhook handling, also install the `webhook-handler-patterns` skill to learn:

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md) - Correct order of operations
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md) - Handle duplicate webhooks
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md) - Proper status codes and retries
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md) - Handle transient failures

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe payment webhooks
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub repository webhooks
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify store webhooks
- [sendgrid-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/sendgrid-webhooks) - SendGrid email webhooks
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Webhook infrastructure that replaces your queue — guaranteed delivery, automatic retries, replay, rate limiting, and observability for your webhook handlers