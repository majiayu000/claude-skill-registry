---
name: Integrating Stripe Payments
description: Complete workflow for integrating Stripe payments (subscriptions or one-time) with Convex + Next.js. Includes hosted checkout, webhooks, UI components, and testing. Use when adding payment functionality to a Convex + Next.js app.
version: "1.0.0"
dependencies: ["stripe", "convex", "next.js"]
allowed-tools: ["stripe-mcp", "convex-mcp", "file_write", "bash"]
---

# Integrating Stripe Payments

## Core Workflow

When user requests Stripe payment integration for Convex + Next.js:

### 1. Requirements Gathering
Ask these questions first:
- **Payment type**: Subscription or one-time payment?
- **Backend**: Confirm this is Convex (required for this skill)
- **Checkout preference**: Hosted Stripe Checkout (recommended) or embedded?
- **Pricing**: Amount, currency, billing interval for subscriptions?
- **Product**: What does user get after payment?

### 2. API Keys & Environment Setup
**CRITICAL**: Gather these FIRST before proceeding - MCP tools require credentials.

1. **Get Stripe API keys from user**:
   - Ask for Stripe Secret Key (starts with `sk_test_` or `sk_live_`)
   - Add to `.env.local`: `STRIPE_SECRET_KEY=sk_test_...`

2. **Install dependencies**: `npm install stripe`

3. **Set initial environment variables**:
   - `STRIPE_SECRET_KEY` (from step 1)
   - `NEXT_PUBLIC_SITE_URL=http://localhost:3000` (default local development)

4. **Use Stripe MCP tool** to create product/price and get price ID
5. **Use Convex MCP tool** to set remaining environment variables
6. **Manual fallback**: Follow `resources/environment-setup.md`

Complete required env vars:
- `STRIPE_SECRET_KEY` ✓ (set in step 1)
- `STRIPE_PRICE_ID` (from Stripe MCP tool)
- `STRIPE_WEBHOOK_SECRET` (set during webhook configuration)
- `NEXT_PUBLIC_SITE_URL` ✓ (set in step 1)

### 3. Database Schema
Update `convex/schema.ts` with Stripe fields. See `resources/database-schema.ts` for complete schema.

### 4. Backend Implementation
Copy and customize these files:
- `convex/stripe.ts` ← Use `resources/convex-stripe-actions.ts`
- `convex/stripeDb.ts` ← Use `resources/convex-stripe-db.ts`
- `convex/http.ts` ← Use `resources/convex-webhook-handler.ts`

**Key customizations**:
- Update membership tier names (`"pro"` vs `"premium"`)
- Adjust auth field names (`clerkId` vs your auth system)
- Set correct API version: `2025-08-27.basil`
- Enable coupon codes by setting `allow_promotion_codes: true` in checkout session creation

### 5. Frontend Components
Create UI components from `resources/ui-components.tsx`:
- `UpgradeButton` - Shows different states based on membership
- `ManageBillingButton` - Opens customer portal

**UI Design Guidelines**:
- Match existing app design system
- Use gradients and proper state management
- Show loading states and error handling
- Keep prices in sync with Stripe Dashboard

### 6. Webhook Configuration
1. Get Convex deployment URL (use `.convex.site` domain)
2. Create webhook in Stripe Dashboard: `https://your-deployment.convex.site/stripe/webhook`
3. Select events: `checkout.session.completed`, `customer.subscription.*`, `invoice.*`
4. Copy webhook secret to environment variables

### 7. Testing
Follow `resources/testing-checklist.md`:
- Test successful payment flow
- Test failed payments
- Test customer portal
- Verify webhook delivery
- Use Stripe CLI for local testing

### 8. Production Deployment
- Switch to live Stripe keys
- Create production webhook endpoint
- Configure Customer Portal and Smart Retries
- Test with real payment (then refund)

## Best Practices

**Always:**
- Use hosted checkout for simplicity and security
- Use `constructEventAsync` in webhooks (not `constructEvent`)
- Include user metadata in checkout sessions
- Handle missing `current_period_end` with fallbacks
- Keep UI prices synchronized with Stripe prices
- Use consistent Stripe API version across all files
- Set `allow_promotion_codes: true` to enable coupon code input during checkout

**Never:**
- Use `.convex.cloud` for webhooks (use `.convex.site`)
- Skip webhook idempotency in production
- Forget to configure Customer Portal
- Deploy without testing webhook delivery

## Common Issues

**Webhook not working**: Check domain (`.convex.site`) and webhook secret
**Membership not updating**: Verify webhook events and metadata
**API errors**: Ensure consistent API version usage

## Documentation References

Use **Stripe MCP tool** for latest documentation when:
- Checking API changes or new features
- Troubleshooting integration issues
- Verifying best practices

See `resources/` folder for complete code examples and detailed setup instructions.