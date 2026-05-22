---
name: autumn-best-practices
description: Skill for integrating Autumn - the billing and entitlements layer over Stripe.
---

# Autumn Integration Guide

**Always consult [docs.useautumn.com](https://docs.useautumn.com) for code examples and latest API.**

Autumn is a TypeScript-first billing SDK supporting subscriptions, usage-based pricing, credits, trials, and more via Stripe.

---

## Quick Reference

### Environment Variables
- `AUTUMN_SECRET_KEY` - API key (required). Get one at [app.useautumn.com](https://app.useautumn.com/dev?tab=api_keys)

### Installation
```bash
npm install autumn-js    # Node.js
pip install autumn-py    # Python
```

### Core Methods

| Method | Purpose |
|--------|---------|
| `customers.create` | Create or get customer (idempotent) |
| `checkout` | Get Stripe URL or payment preview |
| `attach` | Confirm purchase (card on file) |
| `cancel` | Cancel subscription |
| `check` | Verify feature access |
| `track` | Record usage |
| `products.list` | Get products with billing scenarios |

---

## Core Config Options

| Option | Notes |
|--------|-------|
| `secretKey` | Required. From env `AUTUMN_SECRET_KEY` |
| `baseURL` | Optional. Defaults to `https://api.useautumn.com` |

---

## Billing Patterns

### Check → Work → Track

Always follow this order for protected actions:

```typescript
const { data } = await autumn.check({ customer_id, feature_id: "api_calls" });
if (!data.allowed) return { error: "Limit reached" };

const result = await doWork();

await autumn.track({ customer_id, feature_id: "api_calls", value: 1 });
return result;
```

### Two-Step Checkout

```typescript
const { data } = await autumn.checkout({ customer_id, product_id: "pro" });

if (data.url) return redirect(data.url);  // New customer → Stripe

// Returning customer → show confirmation, then:
await autumn.attach({ customer_id, product_id: "pro" });
```

---

## Product Scenarios

Use `products.list` to get scenarios. Don't build custom logic.

| Scenario | Meaning |
|----------|---------|
| `new` | Not subscribed |
| `active` | Currently on plan |
| `scheduled` | Scheduled for future |
| `upgrade` | Higher tier available |
| `downgrade` | Lower tier available |
| `renew` | Cancelled, can reactivate |

---

## Feature Types

| Type | Behavior |
|------|----------|
| `boolean` | Access granted or denied |
| `metered` | Usage tracked against limit |
| `credit_system` | Pool for multiple features |

---

## React Hooks

| Hook | Purpose |
|------|---------|
| `useCustomer` | Get customer, checkout, attach, check |
| `usePricingTable` | Get products with scenarios |

```tsx
import { AutumnProvider } from "autumn-js/react";

<AutumnProvider>{children}</AutumnProvider>
```

---

## Handler Imports

| Framework | Import |
|-----------|--------|
| Next.js | `autumn-js/next` |
| React Router | `autumn-js/react-router` |
| Hono | `autumn-js/hono` |
| Express | `autumn-js/express` |
| Fastify | `autumn-js/fastify` |
| Generic | `autumn-js/backend` |

---

## Common Gotchas

1. **URL field** - Checkout URL is `data.url`, not `data.checkout_url`
2. **Frontend checks** - For UX only. Always enforce on backend
3. **Track after success** - Only track usage after work completes
4. **Credit systems** - Track metered features, not the credit system itself
5. **Cancel via free plan** - Prefer `attach({ product_id: "free" })` over `cancel()`
6. **Idempotent creation** - `customers.create` returns existing customer if ID exists

---

## Resources

- [Docs](https://docs.useautumn.com)
- [API Reference](https://docs.useautumn.com/api-reference)
- [LLMs.txt](https://docs.useautumn.com/llms.txt)
- [GitHub](https://github.com/useautumn/autumn)
