---
name: woocommerce-webhooks
description: >
  Receive and verify WooCommerce webhooks. Use when setting up WooCommerce webhook
  handlers, debugging signature verification, or handling e-commerce events like
  order.created, order.updated, product.created, or customer.created.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# WooCommerce Webhooks

## When to Use This Skill

- Setting up WooCommerce webhook handlers
- Debugging signature verification failures
- Understanding WooCommerce event types and payloads
- Handling order, product, or customer events
- Integrating with WooCommerce stores

## Essential Code (USE THIS)

### WooCommerce Signature Verification (JavaScript)

```javascript
const crypto = require('crypto');

function verifyWooCommerceWebhook(rawBody, signature, secret) {
  if (!signature || !secret) return false;
  
  const hash = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('base64');
  
  try {
    return crypto.timingSafeEqual(
      Buffer.from(signature), 
      Buffer.from(hash)
    );
  } catch {
    return false;
  }
}
```

### Express Webhook Handler

```javascript
const express = require('express');
const app = express();

// CRITICAL: Use raw body for signature verification
app.use('/webhooks/woocommerce', express.raw({ type: 'application/json' }));

app.post('/webhooks/woocommerce', (req, res) => {
  const signature = req.headers['x-wc-webhook-signature'];
  const secret = process.env.WOOCOMMERCE_WEBHOOK_SECRET;
  
  if (!verifyWooCommerceWebhook(req.body, signature, secret)) {
    return res.status(400).send('Invalid signature');
  }
  
  const payload = JSON.parse(req.body);
  const topic = req.headers['x-wc-webhook-topic'];
  
  console.log(`Received ${topic} event:`, payload.id);
  res.status(200).send('OK');
});
```

### Next.js API Route (App Router)

```typescript
import crypto from 'crypto';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const signature = request.headers.get('x-wc-webhook-signature');
  const secret = process.env.WOOCOMMERCE_WEBHOOK_SECRET;
  
  const rawBody = await request.text();
  
  if (!verifyWooCommerceWebhook(rawBody, signature, secret)) {
    return new Response('Invalid signature', { status: 400 });
  }
  
  const payload = JSON.parse(rawBody);
  const topic = request.headers.get('x-wc-webhook-topic');
  
  console.log(`Received ${topic} event:`, payload.id);
  return new Response('OK', { status: 200 });
}
```

### FastAPI Handler

```python
import hmac
import hashlib
import base64
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

def verify_woocommerce_webhook(raw_body: bytes, signature: str, secret: str) -> bool:
    if not signature or not secret:
        return False
    
    hash_digest = hmac.new(
        secret.encode(),
        raw_body,
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(hash_digest).decode()
    
    return hmac.compare_digest(signature, expected_signature)

@app.post('/webhooks/woocommerce')
async def handle_webhook(request: Request):
    raw_body = await request.body()
    signature = request.headers.get('x-wc-webhook-signature')
    secret = os.getenv('WOOCOMMERCE_WEBHOOK_SECRET')
    
    if not verify_woocommerce_webhook(raw_body, signature, secret):
        raise HTTPException(status_code=400, detail='Invalid signature')
    
    payload = await request.json()
    topic = request.headers.get('x-wc-webhook-topic')
    
    print(f"Received {topic} event: {payload.get('id')}")
    return {'status': 'success'}
```

## Common Event Types

| Event | Triggered When | Common Use Cases |
|-------|----------------|------------------|
| `order.created` | New order placed | Send confirmation emails, update inventory |
| `order.updated` | Order status changed | Track fulfillment, send notifications |
| `order.deleted` | Order deleted | Clean up external systems |
| `product.created` | Product added | Sync to external catalogs |
| `product.updated` | Product modified | Update pricing, inventory |
| `customer.created` | New customer registered | Welcome emails, CRM sync |
| `customer.updated` | Customer info changed | Update profiles, preferences |

## Environment Variables

```bash
WOOCOMMERCE_WEBHOOK_SECRET=your_webhook_secret_key
```

## Headers Reference

WooCommerce webhooks include these headers:

- `X-WC-Webhook-Signature` - HMAC SHA256 signature (base64)
- `X-WC-Webhook-Topic` - Event type (e.g., "order.created")
- `X-WC-Webhook-Resource` - Resource type (e.g., "order")
- `X-WC-Webhook-Event` - Action (e.g., "created")
- `X-WC-Webhook-Source` - Store URL
- `X-WC-Webhook-ID` - Webhook ID
- `X-WC-Webhook-Delivery-ID` - Unique delivery ID

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
hookdeck listen 3000 --path /webhooks/woocommerce
```

No account required. Provides local tunnel + web UI for inspecting requests.

## Reference Materials

- `overview.md` - What WooCommerce webhooks are, common event types
- `setup.md` - Configure webhooks in WooCommerce admin, get signing secret
- `verification.md` - Signature verification details and gotchas
- `examples/` - Complete runnable examples per framework

## Recommended: webhook-handler-patterns

For production-ready webhook handlers, also install the webhook-handler-patterns skill for:

- <a href="https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md">Handler sequence</a>
- <a href="https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md">Idempotency</a>  
- <a href="https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md">Error handling</a>
- <a href="https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md">Retry logic</a>

## Related Skills

- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe payment webhooks with HMAC verification
- [shopify-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/shopify-webhooks) - Shopify store webhooks with HMAC verification
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub repository webhooks
- [paddle-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/paddle-webhooks) - Paddle billing webhooks
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Production webhook infrastructure