---
name: mpp-setup
description: Scaffold an MPP project — install mppx SDK, configure payment methods, set up server middleware, and create a basic paid API endpoint. Use when starting a new MPP machine payments project from scratch.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# MPP Project Setup

## Before writing code

**Fetch live docs**:
1. Fetch `https://www.npmjs.com/package/mppx` for the latest mppx SDK version, installation, and API surface
2. Web-search `site:github.com stripe-samples machine-payments` for the official sample project structure
3. Fetch `https://docs.stripe.com/payments/machine` for Stripe machine payments setup requirements
4. Web-search `site:mpp.dev overview` for the current protocol overview and getting started guide

## What This Skill Does

Scaffolds a new MPP project for monetizing HTTP services with machine payments:

1. **Detect language/framework** — TypeScript (Hono/Express/Next.js/Elysia), Python (FastAPI/Flask), or Rust
2. **Install SDK** — `npm install mppx` (TypeScript), `pip install pympp` (Python), or check mpp.dev for the Rust crate
3. **Create configuration** — Environment variables for secret key, payment method settings, Stripe keys
4. **Set up server middleware** — `Mppx.create()` with payment method configuration
5. **Create a paid endpoint** — Basic route protected by `mppx.charge()` middleware
6. **Add service discovery** — `GET /openapi.json` with `x-payment-info` extensions
7. **Set up client (optional)** — `mppx.fetch()` for consuming paid APIs

## Environment Configuration

These must be externalized (env vars or config file):
- `MPP_SECRET_KEY` — 32-byte hex key for HMAC challenge binding (generate with `openssl rand -hex 32`)
- `STRIPE_SECRET_KEY` — If using Stripe payment method
- `TEMPO_RECIPIENT_ADDRESS` — Wallet address for receiving Tempo payments
- `TEMPO_CHAIN_ID` — `4217` for Tempo mainnet
- `TEMPO_USDC_CONTRACT` — `0x20c000000000000000000000b9537d11c60e8b50` for USDC on Tempo

## Project Structure Pattern

```
my-mpp-service/
├── src/
│   ├── index.ts              # Server entry point with Mppx middleware
│   ├── routes/
│   │   ├── paid.ts           # Payment-protected endpoints
│   │   └── free.ts           # Free/health endpoints
│   ├── config.ts             # MPP and payment method configuration
│   └── openapi.ts            # Service discovery endpoint
├── .env                      # Secrets (MPP_SECRET_KEY, STRIPE_SECRET_KEY)
├── package.json
├── tsconfig.json
└── tests/
    └── payment.test.ts
```

## Key Setup Decisions

- **Payment method** — Tempo (crypto, sub-second), Stripe (cards via SPT), Lightning, or multiple
- **Payment intent** — Charge (one-time per request) or Session (streaming micropayments)
- **Framework** — Hono (recommended, lightweight), Express, Next.js, or Elysia
- **Pricing model** — Fixed per-request, dynamic based on payload, or session-based streaming

## Quick Start Pattern (Hono + Tempo)

```typescript
import { Hono } from 'hono';
import { Mppx, tempo } from 'mppx/server';

const mppx = Mppx.create({
  secretKey: process.env.MPP_SECRET_KEY,
  methods: [
    tempo.charge({
      chainId: 4217,
      currency: '0x20C000000000000000000000b9537d11c60E8b50',
      recipient: process.env.TEMPO_RECIPIENT_ADDRESS,
    }),
  ],
});

const app = new Hono();
app.get('/api/data', mppx.charge({ amount: '100' }), (c) => {
  return c.json({ data: 'premium content' });
});
```

Fetch the latest mppx README and Stripe machine payments docs for exact SDK API, current payment method configuration options, and framework-specific setup before scaffolding.
