---
description: Handle Stripe payments, custom checkouts, and webhook fulfillment outside of standard plans/credits.
deps: ["plans-handler", "credits-handler", "inngest-handler"]
---

# Stripe Handler

Use this skill when you need to implement payment logic using Stripe, specifically for use cases that are **NOT** standard SaaS subscription plans or standard Credit packages (which are handled by `plans-handler` and `credits-handler` respectively).

## When to use
- Implementing "Buy One-time Product" flows (e.g., Courses, Digital Goods).
- Creating custom "Service" payments.
- Handling `checkout.session.completed` for custom metadata.
- Customizing `src/app/api/webhooks/stripe/route.ts` for non-standard events.
- Offloading heavy webhook processing to background tasks (via Inngest).

## Process

### 1. Identify Payment Type
Before writing code, determine the nature of the payment:
- **Is it a Subscription Plan?** -> Use `plans-handler`.
- **Is it a Credit Package?** -> Use `credits-handler`.
- **Is it a Custom One-time or Recurring Product?** -> **Continue with this skill.**

### 2. Create Checkout Session (API/Action)
You need a server-side endpoint to create the Stripe Checkout Session.
- **File**: Create a new route (e.g., `src/app/api/app/orders/create/route.ts`) or Server Action.
- **Import**: `import stripe from "@/lib/stripe";`
- **Metadata**: **CRITICAL**. Always attach `metadata` to the session to identify the purchase type in the webhook.
  ```typescript
  metadata: {
    type: "my_custom_feature",
    userId: user.id,
    customId: "..."
  }
  ```
- **URLs**: Use the standard success/error pages or custom ones if needed.
  - Success: `${process.env.NEXT_PUBLIC_APP_URL}/app/subscribe/success?session_id={CHECKOUT_SESSION_ID}`
  - Error: `${process.env.NEXT_PUBLIC_APP_URL}/app/subscribe/error`

### 3. Handle Webhook Fulfillment
All Stripe events go to `src/app/api/webhooks/stripe/route.ts`.
- **File**: `src/app/api/webhooks/stripe/route.ts`
- **Locate**: `onCheckoutSessionCompleted` (for one-time) or `handleOutsidePlanManagementProductInvoicePaid` (for invoices).
- **Implement**:
  1. Extract `metadata` from the event object.
  2. Check if `metadata.type` matches your custom feature.
  3. **If yes**: Run your fulfillment logic.
     - **Simple Logic**: Update DB directly.
     - **Heavy Logic**: Dispatch an Inngest event to handle it in the background.
  4. **If no**: Let the function fall through to standard plan/credit handling.

### 4. Background Processing (Inngest)
**Recommended for production**: If your fulfillment logic involves multiple DB calls, external APIs, or could timeout (Stripe expects a response in < 3s):
- Use `inngest-handler` to create a new function.
- In the webhook, just dispatch the event:
  ```typescript
  await inngest.send({ name: "app/payment.custom_succeeded", data: { sessionId: object.id, metadata } });
  ```
- Handle the actual logic in `src/inngest/functions/...`.

### 5. Database Updates
- If the purchase grants access to a resource, update the corresponding schema (e.g., `orders`, `courses`).
- Ensure the fulfillment is idempotent (handle duplicate webhook events gracefully).

### 6. Frontend Integration
- Use a simple Button or Form to call your API/Action.
- Redirect the user to the returned `url` (Stripe Checkout).

## Best Practices
- **Idempotency**: Webhooks can fire multiple times. Ensure your logic checks if the order is already fulfilled.
- **Metadata**: Rely on metadata, not just product IDs, for cleaner logic separation.
- **Timeouts**: Stripe webhooks must respond quickly. Use Inngest for anything taking > 2 seconds.
- **Testing**: Use `stripe listen` to test webhooks locally.

## Reference
See `reference.md` for code snippets on creating sessions, handling webhooks, and using Inngest.
