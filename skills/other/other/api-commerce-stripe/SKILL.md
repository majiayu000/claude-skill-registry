---
name: api-commerce-stripe
description: Stripe payment processing — Checkout Sessions, Payment Intents, subscriptions, webhooks, Connect, customer management, error handling
---

# Stripe Patterns

> **Quick Guide:** Use the `stripe` npm package for all server-side Stripe operations. Always verify webhook signatures with `constructEvent()` using the raw request body, never the parsed body. Use idempotency keys on all mutating requests. Keep the secret key server-side only. Handle errors with `instanceof Stripe.errors.StripeError`. Amounts are always in the smallest currency unit (e.g., cents for USD).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST NEVER expose `STRIPE_SECRET_KEY` in client-side code — it stays on the server only)**

**(You MUST verify webhook signatures with `stripe.webhooks.constructEvent()` using the RAW request body — never parsed JSON)**

**(You MUST use idempotency keys on all mutating (POST) requests to prevent duplicate charges)**

**(You MUST handle all Stripe errors with `instanceof Stripe.errors.StripeError` — never swallow payment errors)**

**(You MUST express monetary amounts in the smallest currency unit — cents for USD, not dollars)**

</critical_requirements>

---

**Auto-detection:** Stripe, stripe, stripe.checkout.sessions, stripe.paymentIntents, stripe.customers, stripe.subscriptions, stripe.webhooks, constructEvent, PaymentIntent, CheckoutSession, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, stripe.prices, stripe.products, stripe.refunds, stripe.transfers, stripe.accounts, Stripe.errors, idempotencyKey, payment_intent.succeeded, checkout.session.completed

**When to use:**

- Creating Checkout Sessions for one-time or subscription payments
- Building custom payment flows with Payment Intents
- Handling webhook events for asynchronous payment lifecycle
- Managing customers, payment methods, and subscriptions
- Building marketplace platforms with Stripe Connect
- Processing refunds and handling disputes
- Setting up products and prices for a catalog

**Key patterns covered:**

- Stripe client initialization with TypeScript types
- Checkout Sessions (one-time payments, subscriptions, setup mode)
- Payment Intents (custom flows, confirmation, capture)
- Webhook signature verification and event handling
- Customer creation, update, and payment method attachment
- Subscription lifecycle (create, update, cancel, trials, proration)
- Products and Prices (catalog management)
- Stripe Connect (account creation, transfers, destination charges)
- Error handling with typed Stripe errors
- Idempotency keys for safe retries

**When NOT to use:**

- Client-side Stripe.js or Stripe Elements (use your frontend framework skill)
- Stripe CLI commands or dashboard configuration
- Non-Stripe payment processors (use their dedicated skill)

**Detailed Resources:**

- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Core Setup & Payments:**

- [examples/core.md](examples/core.md) — Client setup, Checkout Sessions, Payment Intents, error handling

**Webhooks & Events:**

- [examples/webhooks.md](examples/webhooks.md) — Signature verification, event handling, idempotent processing

**Subscriptions & Billing:**

- [examples/subscriptions.md](examples/subscriptions.md) — Subscription lifecycle, trials, proration, metered billing

**Connect & Platforms:**

- [examples/connect.md](examples/connect.md) — Connected accounts, transfers, destination charges, platform fees

---

<philosophy>

## Philosophy

Stripe is a payment infrastructure platform. The `stripe` npm package is the server-side SDK for interacting with the Stripe API. All payment processing happens server-side for security.

**Core principles:**

1. **Server-side only** — The secret key and all payment-creating operations must never run in the browser. Client-side uses Stripe.js (a separate concern) only for collecting payment details.
2. **Amounts in smallest unit** — All monetary values are integers in the smallest currency unit (cents for USD, pence for GBP). `1000` means $10.00, not $1000.
3. **Idempotency for safety** — Every mutating request should include an idempotency key to prevent duplicate charges on network retries. Stripe's SDK auto-generates keys for retries, but you should provide explicit keys for application-level retries.
4. **Webhooks are the source of truth** — Payment status should be confirmed via webhooks, not by polling. Webhook events are the only reliable indicator that a payment succeeded, failed, or requires action.
5. **Error as typed exceptions** — Stripe errors are thrown (not returned as values). Catch with `instanceof Stripe.errors.StripeError` and handle by type for appropriate user responses.
6. **API versioning matters** — Pin your API version. Types reflect the latest API version. Use `apiVersion` in the constructor to lock behavior.

**When to use Stripe:**

- Accepting payments (one-time, recurring, marketplace splits)
- Building subscription billing systems
- Platform/marketplace payment splitting with Connect
- Saving payment methods for future charges

**When NOT to use:**

- Client-side payment form rendering (Stripe.js / Elements is a separate domain)
- Payment processing without a server (Stripe requires server-side secret key)
- Simple donation buttons (Stripe Payment Links may suffice without code)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Stripe Client Initialization

Create a singleton Stripe client. Secret key from env, API version pinned. See [examples/core.md](examples/core.md) for full setup.

```typescript
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2026-02-25.clover",
});
```

Never hardcode the secret key or omit `apiVersion` (behavior changes silently on Stripe API upgrades).

---

### Pattern 2: Checkout Sessions

Use `mode: "payment"` for one-time, `mode: "subscription"` for recurring. Stripe hosts the payment page. Always include `{CHECKOUT_SESSION_ID}` in the success URL (Stripe replaces this template automatically). See [examples/core.md](examples/core.md) for full examples.

```typescript
const session = await stripe.checkout.sessions.create({
  mode: "payment", // or "subscription" or "setup"
  line_items: [{ price: priceId, quantity }],
  success_url: `${process.env.APP_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${process.env.APP_URL}/cancel`,
});
```

---

### Pattern 3: Payment Intents (Custom Flows)

Use Payment Intents when you need full control over the payment UI (e.g., Stripe Elements). Always use `automatic_payment_methods` (not the legacy `payment_method_types` array) and include an idempotency key. See [examples/core.md](examples/core.md) for full examples.

```typescript
const paymentIntent = await stripe.paymentIntents.create(
  {
    amount: amountInCents,
    currency,
    automatic_payment_methods: { enabled: true },
  },
  { idempotencyKey: `pi_${orderId}` },
);
return { clientSecret: paymentIntent.client_secret };
```

Name parameters `amountInCents` to avoid dollar/cent confusion. Return `client_secret` to the frontend.

---

### Pattern 4: Customer Management

Create customers with idempotency keys (based on email to prevent duplicates). Attach payment methods in two steps: attach, then set as default via `invoice_settings.default_payment_method`. See [examples/core.md](examples/core.md) for full examples.

---

### Pattern 5: Products and Prices

Products and prices are separate resources in Stripe's data model. Add `recurring: { interval }` only for subscription prices. Name the amount parameter `amountInCents`. See [examples/core.md](examples/core.md) for full examples.

---

### Pattern 6: Refunds

Omit `amount` for a full refund. Use `payment_intent` (preferred over `charge`). Always include an idempotency key unique to the refund amount. See [examples/core.md](examples/core.md) for full examples.

---

### Pattern 7: Error Handling

Catch errors with `instanceof Stripe.errors.StripeCardError` (and other error subclasses). `StripeCardError` returns user-safe messages with `decline_code`. `StripeInvalidRequestError` is a developer bug. `StripeConnectionError` and `StripeRateLimitError` are retry-able. See [examples/core.md](examples/core.md) for the complete error handling pattern.

```typescript
if (error instanceof Stripe.errors.StripeCardError) {
  return { success: false, message: error.message, code: error.code };
}
```

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Secret key in client-side code** — `STRIPE_SECRET_KEY` must never appear in browser bundles. Use `STRIPE_PUBLISHABLE_KEY` (starts with `pk_`) for client-side Stripe.js only.
- **Webhook signature not verified** — Without `constructEvent()` verification, attackers can send fake events to fulfill orders, grant access, or modify records.
- **Raw body not used for webhooks** — Using `req.body` (parsed JSON) instead of the raw body string/buffer causes signature verification to fail silently. With Express, use `express.raw({ type: "application/json" })` on the webhook route.
- **Missing idempotency keys** — Without idempotency keys, network retries can create duplicate charges. Always pass `{ idempotencyKey }` on create/update operations.
- **Dollar amounts instead of cents** — `amount: 10` creates a $0.10 charge, not $10.00. Always multiply by 100 or name variables `amountInCents`.

**Medium Priority Issues:**

- **Not pinning API version** — Without `apiVersion` in the constructor, Stripe uses your account's default version. API changes can silently break your integration.
- **Using `payment_method_types` instead of `automatic_payment_methods`** — The legacy array approach requires manual updates as new payment methods become available. `automatic_payment_methods: { enabled: true }` is the modern approach.
- **Swallowing Stripe errors** — Empty `catch` blocks hide payment failures. Always log the error's `requestId` for debugging with Stripe support.
- **Not handling `requires_action` status** — Payment Intents may require 3D Secure authentication. Check `paymentIntent.status` after confirmation.
- **Polling instead of webhooks** — Checking payment status in a loop is unreliable and wastes API calls. Use webhooks for all asynchronous payment events.

**Common Mistakes:**

- **Processing webhooks synchronously** — Long-running operations in the webhook handler cause timeouts. Return `200` immediately, then process asynchronously.
- **Not handling duplicate webhook events** — Stripe may deliver the same event multiple times. Track processed event IDs to ensure idempotent handling.
- **Using test keys in production** — Keys starting with `sk_test_` and `pk_test_` only work with test data. Verify your environment configuration.
- **Forgetting `expand` for nested objects** — Stripe returns IDs by default for related objects. Use `expand: ["latest_invoice.payment_intent"]` to get full objects.

**Gotchas & Edge Cases:**

- **Stripe events are not ordered** — `invoice.paid` may arrive before `invoice.created`. Design handlers to be order-independent.
- **Checkout Session `{CHECKOUT_SESSION_ID}` is a literal template** — Stripe replaces this placeholder in the `success_url`. Do not URL-encode it.
- **Subscription proration is on by default** — Upgrading a plan mid-cycle prorates automatically. Pass `proration_behavior: "none"` to disable.
- **Idempotency keys expire after 24 hours** — After expiry, the same key creates a new request. For long-lived retries, generate a new key.
- **Zero-decimal currencies** — JPY, KRW, and others have no decimal subunit. `amount: 500` in JPY means 500 yen, not 5 yen. Check `Stripe.ZERO_DECIMAL_CURRENCIES`.
- **Connect transfers require `transfers` capability** — Connected accounts must have `card_payments` and `transfers` capabilities enabled before receiving transfers.
- **Webhook secrets differ per endpoint** — Each webhook endpoint has its own signing secret. Using the wrong secret causes all signature verifications to fail.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST NEVER expose `STRIPE_SECRET_KEY` in client-side code — it stays on the server only)**

**(You MUST verify webhook signatures with `stripe.webhooks.constructEvent()` using the RAW request body — never parsed JSON)**

**(You MUST use idempotency keys on all mutating (POST) requests to prevent duplicate charges)**

**(You MUST handle all Stripe errors with `instanceof Stripe.errors.StripeError` — never swallow payment errors)**

**(You MUST express monetary amounts in the smallest currency unit — cents for USD, not dollars)**

**Failure to follow these rules will create security vulnerabilities, duplicate charges, and silent payment failures.**

</critical_reminders>
