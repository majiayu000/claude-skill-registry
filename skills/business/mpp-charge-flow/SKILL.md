---
name: mpp-charge-flow
description: Implement MPP one-time charge payment flows — per-request payment gates for API monetization, data access, and file downloads. Use when building pay-per-call APIs or protecting individual resources with HTTP 402 charges.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Charge Flow (One-Time Payments)

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.npmjs.com/package/mppx` for the charge middleware API and configuration
2. Fetch `https://paymentauth.org/` for the canonical charge intent specification
3. Web-search `site:github.com stripe-samples machine-payments charge` for charge flow sample code
4. Fetch `https://docs.stripe.com/payments/machine/mpp` for Stripe charge integration details

## Conceptual Architecture

### What Charge Intent Is

The charge intent implements **immediate, per-request settlement**. Each API call triggers a single payment. The flow is:

```
Client: GET /api/data
Server: 402 Payment Required
        WWW-Authenticate: Payment <challenge with intent="charge">
Client: Fulfills payment (on-chain tx or card charge)
Client: GET /api/data
        Authorization: Payment <credential with proof>
Server: 200 OK
        Payment-Receipt: <receipt>
```

### When to Use Charge

- **API monetization** — Pay per call (e.g., $0.01 per request)
- **Data access** — Pay for each data query or download
- **File downloads** — Pay per file or per MB
- **Model inference** — Pay per inference call
- **Fixed-price resources** — Content behind a paywall

### Server-Side Implementation

```typescript
// Protect a route with a charge gate
app.get('/api/data', mppx.charge({ amount: '100' }), async (c) => {
  // Only reached after successful payment
  return c.json({ data: 'premium content' });
});
```

The `amount` is specified in the smallest unit of the payment method's currency.

### Dynamic Pricing

For routes where the price depends on the request:

```typescript
app.get('/api/data/:size', async (c, next) => {
  const size = c.req.param('size');
  const amount = calculatePrice(size);
  return mppx.charge({ amount: String(amount) })(c, next);
}, async (c) => {
  return c.json({ data: 'variable-price content' });
});
```

### Challenge Lifecycle

1. **Generation** — Server creates challenge with unique ID, HMAC-bound to secret key
2. **Delivery** — Challenge sent in `WWW-Authenticate` header with 402 status
3. **Expiration** — Challenge is time-limited (configurable, typically minutes)
4. **Fulfillment** — Client pays and constructs credential
5. **Verification** — Server verifies payment proof and HMAC binding
6. **Consumption** — Challenge is consumed (single-use)

### Amount Conventions

| Payment Method | Unit | Example: $0.01 |
|---------------|------|-----------------|
| Tempo (USDC) | Smallest token unit | Verify in SDK docs |
| Stripe | Cents (minor currency unit) | `100` (1 USD cent = `100`) |
| Lightning | Millisatoshis | Varies |

Always verify the exact unit convention in the SDK documentation for your payment method.

### Error Scenarios

| Scenario | Server Response |
|----------|----------------|
| No payment header | 402 with `payment-required` challenge |
| Payment amount too low | 402 with `verification-failed` |
| Payment to wrong address | 402 with `verification-failed` |
| Expired challenge | 402 with `payment-expired` |
| Duplicate credential (replay) | 402 with `verification-failed` |
| Successful payment | 200 with `Payment-Receipt` |

### Best Practices

- Set amounts that reflect the actual value of the resource
- Use dynamic pricing for variable-cost resources (compute, bandwidth)
- Set reasonable challenge expiration times (long enough for payment settlement)
- Monitor payment success rates and adjust pricing if needed
- Provide clear pricing documentation in your service discovery

Fetch the latest mppx SDK docs and payment method documentation for exact charge configuration options and amount unit conventions before implementing.
