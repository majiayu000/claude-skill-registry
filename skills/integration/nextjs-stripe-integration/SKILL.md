---
name: nextjs-stripe-integration
description: Add Stripe payment processing to Next.js projects. Implement checkout sessions, payment handling, subscriptions, webhooks, and customer management. Use when adding Stripe to a Next.js project, building payment flows, implementing subscriptions, or integrating payment processing.
---

# Next.js + Stripe Integration

This Skill teaches Claude how to implement Stripe payment processing in Next.js projects, including one-time payments, subscriptions, webhooks, and customer management. Based on real-world implementation experience with modern Stripe APIs and authentication frameworks.

## ⚠️ CRITICAL: Breaking Changes in Modern Stripe.js

**`stripe.redirectToCheckout()` is DEPRECATED and no longer works!**

Modern Stripe implementations use the checkout session URL directly:

```typescript
// ❌ OLD (BROKEN)
const { error } = await stripe.redirectToCheckout({ sessionId });

// ✅ NEW (CORRECT)
const session = await stripe.checkout.sessions.create({...});
window.location.href = session.url; // Use the URL directly!
```

## Quick Start Checklist

When implementing Stripe in a Next.js project:

1. **Install dependencies**: `stripe` and `@stripe/stripe-js`
2. **Configure environment**: Add `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` to `.env.local`
3. **Access env vars correctly**: Load inside functions, NOT at module level (critical for runtime)
4. **Create API routes**: Build endpoints for checkout sessions, webhooks, and customer portal
5. **Build UI**: Create checkout forms and payment pages
6. **Handle webhooks**: Set up secure webhook handlers for payment events
7. **Update middleware**: Add payment routes to `unauthenticatedPaths` if using auth middleware
8. **Test locally**: Use Stripe CLI for webhook testing

## Core Implementation Patterns

### 1. Environment Setup & Runtime Loading

```env
# .env.local
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

**CRITICAL**: Access environment variables **inside API route functions**, NOT at module initialization:

```typescript
// ❌ WRONG - Fails at build/startup
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
export async function POST() { ... }

// ✅ CORRECT - Variables loaded at runtime
export async function POST(request: NextRequest) {
  const stripeSecretKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeSecretKey) {
    return NextResponse.json({ error: 'API key not configured' }, { status: 500 });
  }
  const stripe = new Stripe(stripeSecretKey);
  // ... rest of function
}
```

**Important**: Only use `NEXT_PUBLIC_` prefix for publishable keys. Secret keys stay server-side only.

### 2. One-Time Payments (Checkout) - Modern Approach

**API Route** (`app/api/checkout/route.ts`):
- Load Stripe with secret key **inside the function**
- Create a Stripe checkout session with `mode: 'payment'`
- Return the full session URL (not just session ID)
- Verify webhook signatures on payment success

```typescript
// ✅ CORRECT: Load env vars inside function
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
const session = await stripe.checkout.sessions.create({...});
return NextResponse.json({ url: session.url }); // Return URL directly
```

**Client Side** (Simplified):
- NO need to load Stripe.js for basic checkout
- Call checkout API route
- Redirect to `session.url` directly from response
- Handle success/cancel redirects via query parameters

### 3. Subscriptions

**Differences from one-time payments**:
- Create products in Stripe Dashboard with recurring pricing
- Use `mode: 'subscription'` when creating checkout sessions
- Manage customer subscriptions in database
- Handle multiple lifecycle events via webhooks

**Key workflow**:
1. Fetch available subscription tiers from Stripe API
2. Display pricing page with subscription options
3. Create checkout session with subscription mode
4. Handle `customer.subscription.created` webhook
5. Sync subscription status to your database

### 4. Webhook Handling

**Critical security requirements**:
- Verify webhook signatures using Stripe's libraries
- Use raw request body for signature validation (disable body parsing)
- Handle these key events:
  - `payment_intent.succeeded` — one-time payment confirmed
  - `customer.subscription.created` — new subscription
  - `customer.subscription.updated` — subscription changes
  - `customer.subscription.deleted` — cancellation
  - `invoice.payment_succeeded` — renewal payment

**Webhook endpoint** (`app/api/webhooks/stripe/route.ts`):
- Accept POST requests from Stripe
- Verify signature: `stripe.webhooks.constructEvent(body, signature, secret)`
- Process event and update database
- Return 200 status to acknowledge

### 5. Authentication Middleware Configuration

**When using WorkOS or similar auth frameworks**, explicitly allow payment routes:

```typescript
// middleware.ts
export default authkitMiddleware({
  eagerAuth: true,
  middlewareAuth: {
    enabled: true,
    unauthenticatedPaths: [
      '/',
      '/sign-in',
      '/sign-up',
      '/api/checkout',              // Allow unauthenticated checkout
      '/api/webhooks/stripe',       // Allow webhook delivery
      '/payment-success',
      '/payment-cancel',
    ],
  },
});
```

**Why**: Without this, auth middleware intercepts payment routes, causing CORS errors when the frontend tries to call them.

### 6. Customer Portal

Enable users to manage subscriptions without custom code:
- Configure Customer Portal in Stripe Dashboard
- Create API route that generates portal sessions
- Redirect users to portal for managing subscriptions, payment methods, and invoices

## Implementation Guide

### Setup Phase

1. Create Next.js project (or use existing)
2. Install Stripe packages:
   ```bash
   npm install stripe @stripe/stripe-js
   ```
3. Get API keys from Stripe Dashboard → Developers → API Keys
4. Add keys to `.env.local`
5. Add `.env.local` to `.gitignore`

### Build Checkout Flow (One-Time Payments)

1. Create `app/api/checkout/route.ts`:
   - Load Stripe with secret key **inside the function**
   - Accept POST with amount and metadata
   - Create checkout session
   - Return session.url directly (not just session ID)
   - See [API_ROUTES.md](API_ROUTES.md) for complete code

2. Create checkout page:
   - Simple button component (no Stripe.js needed for basic flow)
   - Call checkout API route on button click
   - Redirect to `response.url` directly
   - Handle success/cancel via query parameters

3. Create success page:
   - Accepts `session_id` query parameter
   - Retrieves session details from Stripe (optional - for confirmation display)
   - Displays confirmation message
   - Can fetch order details from your database

### Build Subscription Flow

1. Create product in Stripe Dashboard (recurring pricing)
2. Create `app/api/subscriptions/list/route.ts`:
   - Fetch products and prices from Stripe API
   - Return formatted subscription tiers

3. Create `app/api/checkout-subscription/route.ts`:
   - Similar to checkout flow but use `mode: 'subscription'`
   - Link to price ID instead of amount

4. Create subscriptions page:
   - Fetch available tiers from API
   - Display subscription cards with pricing
   - Implement checkout on selection

5. Create `app/api/customer-portal/route.ts`:
   - Accept POST request
   - Create portal session with customer ID
   - Return portal URL

### Webhook Integration

1. Create `app/api/webhooks/stripe/route.ts`:
   - Disable body parsing: `export const config = { api: { bodyParser: false } }`
   - Extract raw body and signature from headers
   - Verify: `stripe.webhooks.constructEvent(body, signature, webhookSecret)`
   - Handle subscription and payment events
   - Update database based on event type

2. Test locally with Stripe CLI:
   ```bash
   stripe listen --forward-to localhost:3000/api/webhooks/stripe
   stripe trigger payment_intent.succeeded
   ```

3. Deploy webhook endpoint to production
4. Add webhook endpoint URL in Stripe Dashboard → Webhooks
5. Use production secret key for production webhooks

## Best Practices

- **PCI Compliance**: Always load Stripe.js from Stripe's CDN, never bundle it
- **Singleton Pattern**: Lazy-load Stripe.js only when needed (performance optimization)
- **Environment Variables**: Use `NEXT_PUBLIC_` only for publishable keys
- **Error Handling**: Catch and log errors from Stripe API calls
- **Webhook Security**: Always verify signatures; never trust webhook data without verification
- **Database Sync**: Store customer IDs, subscription status, and invoice data in your database
- **Testing**: Use Stripe test mode keys during development; switch to live keys only in production
- **Customer Portal**: Leverage it for subscription management instead of building custom UI

## Common Patterns

### Check if User has Active Subscription

```typescript
// Query your database for customer's subscription status
const subscription = await db.subscriptions.findFirst({
  where: { userId, status: 'active' }
});
return subscription !== null;
```

### Handle Failed Payments

Listen for `invoice.payment_failed` webhook and:
- Send customer notification email
- Update UI to show payment issue
- Offer retry option via customer portal

### Prorate Subscription Changes

Stripe handles this automatically when updating subscriptions via the API. Use `proration_behavior` to control how changes are billed.

## Architecture Recommendations

```
app/
├── api/
│   ├── checkout/route.ts           # One-time payment sessions
│   ├── checkout-subscription/route.ts
│   ├── subscriptions/
│   │   └── list/route.ts           # Get available tiers
│   ├── customer-portal/route.ts    # Manage subscriptions
│   └── webhooks/
│       └── stripe/route.ts         # Webhook handler
├── checkout/
│   └── page.tsx                    # Checkout form
├── success/
│   └── page.tsx                    # Success page
└── subscriptions/
    └── page.tsx                    # Subscription tiers
```

## Deployment Considerations

- **Vercel**: Natural fit for Next.js projects; environment variables work seamlessly
- **Environment Variables**: Ensure all keys are added to your hosting platform
- **Webhooks**: Update webhook endpoint URL in Stripe Dashboard after deployment
- **HTTPS**: Required for production (Stripe won't send webhooks to non-HTTPS URLs)
- **Testing**: Create webhook endpoints in both test and production modes

## References and Resources

- [Vercel Next.js + Stripe Guide](https://vercel.com/guides/getting-started-with-nextjs-typescript-stripe)
- [Stripe Subscriptions with Next.js](https://www.pedroalonso.net/blog/stripe-subscriptions-nextjs/)
- [Stripe Official Documentation](https://stripe.com/docs)
- [Stripe Sample Applications](https://github.com/stripe-samples)
