---
name: mpp-client-fetch
description: Implement MPP client-side payment handling with mppx.fetch(). Use when building AI agents or automated clients that consume 402-protected APIs, handling the transparent challenge-response payment flow.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Client — mppx.fetch()

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.npmjs.com/package/mppx` for the current client API and wallet configuration
2. Web-search `mppx client fetch payment wallet configuration` for client-side setup patterns
3. Web-search `site:github.com stripe-samples machine-payments client` for official client sample code
4. Fetch `https://mpp.dev/overview` for the client-side protocol flow description

## Conceptual Architecture

### What mppx.fetch() Does

`mppx.fetch()` is a drop-in replacement for the standard `fetch()` API that transparently handles the full HTTP 402 payment flow:

1. **Request** — Client sends a normal HTTP request
2. **402 Detection** — If server responds with 402, the client parses the `WWW-Authenticate: Payment` challenge
3. **Payment Fulfillment** — Client automatically pays using the configured wallet/payment method
4. **Credential Submission** — Client retries the request with `Authorization: Payment` credential
5. **Receipt Capture** — Client captures the `Payment-Receipt` header from the response
6. **Transparent Return** — Returns the final 200 response as if the payment never happened

The developer's code sees only the final successful response — all payment negotiation is handled internally.

### Client Configuration

```typescript
import { mppx } from 'mppx/client';

// Configure once
const client = mppx.create({
  wallet: {
    privateKey: process.env.WALLET_PRIVATE_KEY,  // For Tempo/crypto payments
  },
  // OR for Stripe SPT payments:
  stripe: {
    sharedPaymentToken: sptToken,  // Obtained from SPT provisioning
  },
});

// Use like fetch()
const response = await client.fetch('https://api.example.com/paid-resource');
const data = await response.json();
```

### Payment Method Selection

When a server supports multiple payment methods, the client selects based on:
- Configured wallet capabilities
- Method preference order
- Available balance (for crypto methods)
- SPT availability (for Stripe methods)

### Spending Controls

Clients should implement spending controls:
- **Per-request limit** — Maximum amount for a single payment
- **Session budget** — Maximum total spend per session
- **Daily/hourly caps** — Rate-based spending limits
- **Allowlisted domains** — Only pay specific services

### Receipt Handling

After a successful payment, the `Payment-Receipt` header contains:
- Payment status
- Method used
- Timestamp
- Reference identifier

Clients should log receipts for accounting and dispute resolution.

### Error Handling

| Scenario | Behavior |
|----------|----------|
| Insufficient balance | Throw error with details |
| Unsupported payment method | Throw error listing supported methods |
| Challenge expired | Retry with fresh request |
| Network error during payment | Do not retry payment (risk of double-pay) |
| Server returns non-402 error | Pass through as normal fetch error |

### CLI Usage

The `mppx` CLI provides a quick way to test payments:

```bash
npx mppx https://api.example.com/paid-resource
```

### Multi-Method Client

A client can be configured with multiple payment methods:

```typescript
const client = mppx.create({
  methods: [
    { type: 'tempo', wallet: { privateKey: process.env.WALLET_KEY } },
    { type: 'stripe', spt: { token: sptToken } },
  ],
  preference: ['tempo', 'stripe'],  // Try Tempo first, fall back to Stripe
});
```

### Best Practices

- Never hardcode wallet private keys or SPTs — use environment variables
- Implement spending limits to prevent runaway costs
- Log all payments with amounts and service URLs for auditing
- Handle payment failures gracefully — distinguish between "can't pay" and "won't pay"
- Cache successful payment sessions where the protocol supports it
- Implement circuit breakers for services that consistently fail

Fetch the latest mppx client documentation for exact configuration options, wallet setup, and error types before implementing.
