---
name: mercadopago
description: |
  Mercado Pago payment integration for Node.js/TypeScript applications. Covers the official MCP Server, Node.js SDK (mercadopago npm), Checkout Pro, Checkout Bricks, Checkout API, OAuth marketplace model, webhooks, multi-tenant architecture, and payment link generation.
  Use this skill whenever working with Mercado Pago payments, MercadoPago API, checkout preferences, payment links, MP webhooks, MP OAuth, marketplace fees, or the mercadopago npm package. Also triggers on: "link de pago", "cobro", "preferencia", "init_point", "sandbox_init_point", "mercadopago SDK", "MP integration", payment processing for Latin American markets (AR, BR, MX, CO, CL, PE, UY), or any code importing from 'mercadopago'. Even if the user just mentions "payment link" or "checkout" in the context of a Latin American market, use this skill.
---

# Mercado Pago Integration Guide

This skill provides everything needed to integrate Mercado Pago into Node.js/TypeScript applications, especially for chat-commerce (WhatsApp/Instagram) and multi-tenant SaaS platforms.

## Quick Decision: Which Checkout?

| Checkout | Best For | Effort | Chat-compatible? |
|----------|----------|--------|-----------------|
| **Checkout Pro** | Payment links, chat commerce, quick setup | Low | Yes - send `init_point` URL |
| **Checkout Bricks** | Embedded UI components on your site | Medium | No - requires webpage |
| **Checkout API** | Full custom checkout, max control | High | No - requires frontend |

For chat-based selling (WhatsApp/Instagram bots), always use **Checkout Pro** — create a preference server-side, extract the `init_point` URL, and send it to the customer.

## Node.js SDK Setup

```bash
npm install mercadopago
# v2.12.0 — TypeScript-native, class-based API
```

```typescript
import { MercadoPagoConfig, Preference, Payment } from 'mercadopago';

const client = new MercadoPagoConfig({
  accessToken: '<ACCESS_TOKEN>',
  options: { timeout: 5000 }
});
```

Available SDK classes: `MercadoPagoConfig` (client), `Preference`, `Payment`, `Order`, `Customer`, `CustomerCard`, `CardToken`, `OAuth`, `MerchantOrder`, `PaymentRefund`, `PaymentMethod`, `PreApproval`, `PreApprovalPlan`, `Invoice`, `IdentificationType`, `Point`, `User`.

## Creating a Payment Link (Checkout Pro)

```typescript
const preference = new Preference(client);
const result = await preference.create({
  body: {
    items: [{
      id: 'product-123',
      title: 'Blue T-Shirt',
      quantity: 1,
      unit_price: 2500.00,
      currency_id: 'UYU' // or ARS, BRL, MXN, COP, CLP, PEN
    }],
    external_reference: 'your-order-id',
    notification_url: 'https://yoursite.com/webhooks/mp?source_news=webhooks',
    back_urls: {
      success: 'https://yoursite.com/payment/success',
      failure: 'https://yoursite.com/payment/failure',
      pending: 'https://yoursite.com/payment/pending'
    },
    auto_return: 'approved',
    expires: true,
    date_of_expiration: '2026-03-18T23:59:59.000-03:00',
    marketplace_fee: 250.00, // platform commission (marketplace model)
    binary_mode: false,      // false allows pending (cash payments)
  }
});

const paymentLink = result.init_point;          // production
const sandboxLink = result.sandbox_init_point;  // testing
```

Critical fields in the response: `id`, `init_point`, `sandbox_init_point`, `collector_id`, `external_reference`.

## Webhook Handling

Webhooks notify you of payment status changes. The payload only contains `data.id` (payment ID) — always fetch full payment details after receiving a webhook.

### HMAC-SHA256 Signature Verification

```typescript
import crypto from 'crypto';

function verifyWebhookSignature(
  xSignature: string,   // from x-signature header
  xRequestId: string,   // from x-request-id header
  dataId: string,       // from query param data.id
  secret: string        // webhook secret from MP dashboard
): boolean {
  const parts = xSignature.split(',');
  let ts = '', hash = '';
  for (const part of parts) {
    const [key, value] = part.split('=').map(s => s.trim());
    if (key === 'ts') ts = value;
    if (key === 'v1') hash = value;
  }
  const manifest = `id:${dataId};request-id:${xRequestId};ts:${ts};`;
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(manifest);
  const calculated = hmac.digest('hex');
  return crypto.timingSafeEqual(Buffer.from(calculated), Buffer.from(hash));
}
```

### Webhook Best Practices
- Return HTTP 200 immediately, process asynchronously
- Implement idempotency — MP may send duplicate notifications
- The `id` in payload is the notification ID; the payment ID is `data.id`
- Always fetch full payment via `Payment.get({ id })` after webhook
- Append `?source_news=webhooks` to `notification_url` to get only webhook format (not legacy IPN)
- Webhook URL must be HTTPS and publicly accessible

### Payment Status Lifecycle

```
created -> pending/in_process -> approved (done)
                              -> rejected (done)
                              -> cancelled (done)
         -> authorized -> captured -> approved (auth+capture flow)
```

Key statuses: `pending`, `approved`, `in_process`, `rejected`, `cancelled`, `refunded`, `charged_back`.

## OAuth Marketplace Model (Multi-Tenant)

For SaaS platforms connecting multiple merchants, each with their own MP account:

### 1. Generate Authorization URL
```
https://auth.mercadopago.com/authorization
  ?client_id=APP_ID
  &response_type=code
  &platform_id=mp
  &state=RANDOM_CSRF_TOKEN
  &redirect_uri=https://yoursite.com/connect/mp/callback
```

### 2. Exchange Code for Token (code expires in 10 minutes!)
```typescript
const response = await fetch('https://api.mercadopago.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    client_id: process.env.MP_CLIENT_ID,
    client_secret: process.env.MP_CLIENT_SECRET,
    code: authorizationCode,
    grant_type: 'authorization_code',
    redirect_uri: process.env.MP_REDIRECT_URI,
    test_token: false // true for sandbox
  })
});
// Returns: access_token (180-day), refresh_token, user_id, public_key
```

### 3. Refresh Before Expiry
```typescript
const response = await fetch('https://api.mercadopago.com/oauth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    client_id: process.env.MP_CLIENT_ID,
    client_secret: process.env.MP_CLIENT_SECRET,
    grant_type: 'refresh_token',
    refresh_token: storedRefreshToken
  })
});
```

### Marketplace Fees
- Checkout Pro: `marketplace_fee` on preference — deducted from seller, sent to platform
- Checkout API: `application_fee` on payment
- Fee is in local currency, deducted from seller's receivable (not added to buyer total)

## MCP Servers

There are three MCP server options for AI-assisted development with Mercado Pago. Read `references/mcp-servers.md` for full setup details.

### Official (Remote — Recommended for Development)
```json
{
  "mcpServers": {
    "mercadopago": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://mcp.mercadopago.com/mcp",
               "--header", "Authorization:Bearer <ACCESS_TOKEN>"],
    }
  }
}
```
Tools: `search-documentation` (searches official MP docs via natural language).

### Community (Local — 27+ Payment Tools)
```json
{
  "mcpServers": {
    "mercado-pago": {
      "command": "npx",
      "args": ["mercado-pago-mcp"],
      "env": {
        "MERCADOPAGO_ACCESS_TOKEN": "YOUR_TOKEN",
        "MERCADOPAGO_ENVIRONMENT": "sandbox"
      }
    }
  }
}
```
Tools: `create_payment`, `create_payment_link`, `search_payments`, `get_payment`, `refund_payment`, `create_subscription`, `create_customer`, `batch_create_payments`, `monitor_payment`, `analyze_fraud`, `export_to_accounting`, `simulate_webhook`, and more.

## Common Gotchas

- **`external_reference`**: Always set it — only reliable way to correlate MP payments with your orders
- **Preference expiration**: Set `expires: true` + `date_of_expiration` for chat links to prevent stale payments
- **Sandbox**: Use `sandbox_init_point` (not `init_point`) with test credentials; create test buyer/seller accounts from MP dashboard
- **`binary_mode: true`**: Only `approved`/`rejected` (no `pending`) — excludes cash payment methods
- **Currency**: Always numeric (e.g., `75.76`), never strings
- **Rate limits**: ~100 req/s for preferences; HTTP 429 → exponential backoff
- **Country auth URLs**: AR: `auth.mercadopago.com.ar`, BR: `auth.mercadopago.com.br`, etc. API base is universal: `api.mercadopago.com`

## Country-Specific Payment Methods

| Country | Currency | Key Methods |
|---------|----------|-------------|
| Argentina (MLA) | ARS | Cards, Rapipago, Pago Facil, MP Wallet |
| Brazil (MLB) | BRL | Cards, Pix, Boleto, MP Wallet |
| Mexico (MLM) | MXN | Cards, OXXO, SPEI |
| Colombia (MCO) | COP | Cards, PSE, Efecty, Baloto |
| Chile (MLC) | CLP | Cards, Servipag, Webpay |
| Peru (MPE) | PEN | Cards, PagoEfectivo |
| Uruguay (MLU) | UYU | Cards, Abitab, RedPagos |

## Deep Reference

For detailed patterns including database schemas, multi-tenant preference creation, payment status details, rejection reason codes, and the full webhook topic list, read `references/api-patterns.md`.

For MCP server setup, troubleshooting, and tool lists, read `references/mcp-servers.md`.

## Official Documentation Links

- [Checkout Pro](https://www.mercadopago.com.ar/developers/en/docs/checkout-pro/overview)
- [Checkout Bricks](https://www.mercadopago.com.ar/developers/en/docs/checkout-bricks/overview)
- [Checkout API](https://www.mercadopago.com.ar/developers/en/docs/checkout-api-orders/overview)
- [Webhooks](https://www.mercadopago.com.ar/developers/en/docs/your-integrations/notifications/webhooks)
- [OAuth / Credentials](https://www.mercadopago.com.ar/developers/en/docs/your-integrations/credentials)
- [Node SDK](https://github.com/mercadopago/sdk-nodejs)
- [API Reference](https://www.mercadopago.com.ar/developers/en/reference)
- [MCP Server Docs](https://www.mercadopago.com.uy/developers/es/docs/mcp-server/overview)
