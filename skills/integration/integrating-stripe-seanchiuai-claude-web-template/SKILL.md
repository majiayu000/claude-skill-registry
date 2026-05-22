---
name: Integrating Stripe Payments
description: Complete guide for integrating Stripe payments (subscriptions or one-time) with Convex + Next.js. Includes user interviews, API setup, webhook configuration, testing phases, and production deployment. Use this skill when Adding payment functionality to a Convex + Next.js app
---

# Integrating Stripe Payments

## Overview

This skill guides you through integrating Stripe payments into a Convex + Next.js application. It covers both subscription and one-time payment flows, with hosted Stripe checkout for simplicity and reliability.

**Use this skill when:**
- Adding payment functionality to a Convex + Next.js app
- Setting up subscription billing
- Processing one-time payments
- Need to avoid common Stripe + Convex integration mistakes

## Phase 1: Requirements Interview

Before starting implementation, gather these requirements from the user:

### Questions to Ask:

1. **Payment Type:**
   - Subscription (recurring billing)
   - One-time payment

2. **Backend Confirmation:**
   - Is this a Convex backend? (Required for this skill)
   - If not Convex, this skill won't apply

3. **Checkout Preference:**
   - Hosted Stripe Checkout (recommended - opens in new tab, less complex, more stable)
   - Embedded Checkout (stays on your site, more complex)

4. **Pricing Details:**
   - What's the price amount?
   - What currency?
   - For subscriptions: billing interval (monthly, every 6 months, yearly)?

5. **Product Information:**
   - Product name (e.g., "Premium Membership", "Founding Member")
   - What does the user get after payment?

### Recommended Approach

**Strongly recommend:** Hosted Stripe Checkout for subscriptions
- Less code complexity
- Better mobile support
- Stripe handles all payment UI
- More stable and secure
- Easier to test

## Phase 2: Installation & Dependencies

### 2.1 Install Stripe Package

```bash
npm install stripe
```

Note: For hosted checkout, you only need the server-side `stripe` package. No need for `@stripe/stripe-js` or `@stripe/react-stripe-js`.

### 2.2 Database Schema Updates

Add Stripe-related fields to your users table in `convex/schema.ts`:

```typescript
users: defineTable({
  // ... existing fields
  membershipStatus: v.optional(v.union(
    v.literal("free"),
    v.literal("premium"), // or your membership tier name
    v.literal("past_due") // For failed payments
  )),
  membershipExpiry: v.optional(v.number()), // Timestamp when membership expires
  stripeCustomerId: v.optional(v.string()), // Stripe customer ID
  stripeSubscriptionId: v.optional(v.string()), // Stripe subscription ID (for subscriptions)
})
  .index("by_stripe_customer", ["stripeCustomerId"])
  .index("by_stripe_subscription", ["stripeSubscriptionId"])
```

## Phase 3: API Keys Setup

### 3.1 Get Stripe API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to **Developers → API keys**
3. Copy your **Test mode** keys:
   - **Publishable key** (starts with `pk_test_...`)
   - **Secret key** (starts with `sk_test_...`)

### 3.2 Create Stripe Product & Price

1. In Stripe Dashboard, go to **Products**
2. Click **+ Add Product**
3. Enter product details:
   - Name: Your product name
   - Description: What the user gets
4. Add pricing:
   - **For one-time payments:** Set "One time" pricing
   - **For subscriptions:** Set "Recurring" and select interval
   - Enter price amount
5. Click **Save product**
6. Copy the **Price ID** (starts with `price_...`)

### 3.3 Set Environment Variables

**In Convex Dashboard** (Settings → Environment Variables):

```
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_PRICE_ID=price_your_price_id_here
STRIPE_WEBHOOK_SECRET=(we'll get this in Phase 4)
```

**In `.env.local`** (for Next.js frontend):

```
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

## Phase 4: Code Implementation

### 4.1 Create Stripe Actions (`convex/stripe.ts`)

```typescript
"use node";

import Stripe from "stripe";
import { action } from "./_generated/server";
import { v } from "convex/values";
import { internal } from "./_generated/api";

/**
 * Create a Stripe Checkout Session
 */
export const createCheckoutSession = action({
  args: {
    clerkUserId: v.string(), // Or your auth user ID
    mode: v.optional(v.union(v.literal("subscription"), v.literal("payment"))),
  },
  handler: async (ctx, args): Promise<{ url: string | null; sessionId: string }> => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: "2025-08-27.basil" as any,
    });

    // Get user from database
    const user: any = await ctx.runQuery(internal.stripeDb.getUserByClerkId, {
      clerkId: args.clerkUserId,
    });

    if (!user) {
      throw new Error("User not found");
    }

    // Create or retrieve Stripe customer
    let customerId: string | undefined = user.stripeCustomerId;
    if (!customerId) {
      const customer = await stripe.customers.create({
        email: user.email,
        name: user.name,
        metadata: {
          clerkUserId: args.clerkUserId,
          convexUserId: user._id,
        },
      });
      customerId = customer.id;

      // Update user with Stripe customer ID
      await ctx.runMutation(internal.stripeDb.updateStripeCustomerId, {
        userId: user._id,
        stripeCustomerId: customerId,
      });
    }

    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";
    const mode = args.mode || "subscription";

    // Create checkout session
    const session: Stripe.Checkout.Session = await stripe.checkout.sessions.create({
      customer: customerId,
      mode: mode, // "subscription" or "payment"
      line_items: [
        {
          price: process.env.STRIPE_PRICE_ID!,
          quantity: 1,
        },
      ],
      success_url: `${siteUrl}/checkout/return?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${siteUrl}`,
      metadata: {
        clerkUserId: args.clerkUserId,
        userId: user._id,
      },
    });

    return {
      url: session.url,
      sessionId: session.id,
    };
  },
});

/**
 * Get checkout session status (for return page)
 */
export const getCheckoutSessionStatus = action({
  args: {
    sessionId: v.string(),
  },
  handler: async (ctx, args) => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: "2025-08-27.basil" as any,
    });

    const session = await stripe.checkout.sessions.retrieve(args.sessionId);

    return {
      status: session.status,
      customerEmail: session.customer_details?.email,
      paymentStatus: session.payment_status,
    };
  },
});

/**
 * Create Customer Portal Session
 * Essential for letting users manage their subscriptions, payment methods, and invoices
 */
export const createCustomerPortalSession = action({
  args: {
    clerkUserId: v.string(),
  },
  handler: async (ctx, args): Promise<{ url: string }> => {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: "2025-08-27.basil" as any,
    });

    // Get user from database
    const user: any = await ctx.runQuery(internal.stripeDb.getUserByClerkId, {
      clerkId: args.clerkUserId,
    });

    if (!user || !user.stripeCustomerId) {
      throw new Error("User not found or has no Stripe customer ID");
    }

    const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";

    // Create portal session
    const session = await stripe.billingPortal.sessions.create({
      customer: user.stripeCustomerId,
      return_url: `${siteUrl}/dashboard`,
    });

    return {
      url: session.url,
    };
  },
});
```

### 4.2 Create Database Helpers (`convex/stripeDb.ts`)

```typescript
import { internalMutation, internalQuery } from "./_generated/server";
import { v } from "convex/values";

/**
 * Internal query to get user by Clerk ID
 */
export const getUserByClerkId = internalQuery({
  args: {
    clerkId: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkId))
      .unique();

    return user;
  },
});

/**
 * Internal mutation to update user's Stripe customer ID
 */
export const updateStripeCustomerId = internalMutation({
  args: {
    userId: v.id("users"),
    stripeCustomerId: v.string(),
  },
  handler: async (ctx, args) => {
    await ctx.db.patch(args.userId, {
      stripeCustomerId: args.stripeCustomerId,
    });
  },
});

/**
 * Internal mutation to update user's membership status after successful payment
 */
export const updateMembershipStatus = internalMutation({
  args: {
    clerkUserId: v.string(),
    stripeSubscriptionId: v.string(), // For subscriptions
    currentPeriodEnd: v.number(), // Timestamp when current period ends
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkUserId))
      .unique();

    if (!user) {
      throw new Error("User not found");
    }

    await ctx.db.patch(user._id, {
      membershipStatus: "premium",
      membershipExpiry: args.currentPeriodEnd * 1000, // Convert to milliseconds
      stripeSubscriptionId: args.stripeSubscriptionId,
    });

    return user._id;
  },
});

/**
 * Internal mutation to cancel user's membership
 */
export const cancelMembership = internalMutation({
  args: {
    stripeSubscriptionId: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_stripe_subscription", (q) =>
        q.eq("stripeSubscriptionId", args.stripeSubscriptionId)
      )
      .unique();

    if (!user) {
      console.error("User not found for subscription:", args.stripeSubscriptionId);
      return null;
    }

    await ctx.db.patch(user._id, {
      membershipStatus: "free",
      membershipExpiry: undefined,
      stripeSubscriptionId: undefined,
    });

    return user._id;
  },
});

/**
 * Internal mutation to handle payment failure
 */
export const handlePaymentFailure = internalMutation({
  args: {
    stripeSubscriptionId: v.string(),
    attemptCount: v.number(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_stripe_subscription", (q) =>
        q.eq("stripeSubscriptionId", args.stripeSubscriptionId)
      )
      .unique();

    if (!user) {
      console.error("User not found for subscription:", args.stripeSubscriptionId);
      return null;
    }

    // You can implement grace period logic here
    // For example, keep access for 3 failed attempts
    if (args.attemptCount >= 3) {
      await ctx.db.patch(user._id, {
        membershipStatus: "past_due",
      });
    }

    return user._id;
  },
});
```

### 4.3 Create Webhook Handler (`convex/http.ts`)

⚠️ **CRITICAL: Use `.convex.site` domain for webhooks, NOT `.convex.cloud`**

```typescript
import { httpRouter } from "convex/server";
import { httpAction } from "./_generated/server";

const http = httpRouter();

// Stripe webhook handler
http.route({
  path: "/stripe/webhook",
  method: "POST",
  handler: httpAction(async (ctx, request: Request) => {
    const Stripe = (await import("stripe")).default;
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
      apiVersion: "2025-08-27.basil" as any,
    });

    const body = await request.text();
    const sig = request.headers.get("stripe-signature");

    if (!sig) {
      return new Response(JSON.stringify({ error: "No signature" }), {
        status: 400,
      });
    }

    try {
      // ⚠️ CRITICAL: Use constructEventAsync (NOT constructEvent)
      const event = await stripe.webhooks.constructEventAsync(
        body,
        sig,
        process.env.STRIPE_WEBHOOK_SECRET!
      );

      // Handle the event
      switch (event.type) {
        case "checkout.session.completed": {
          const session = event.data.object as any;

          const clerkUserId = session.metadata?.clerkUserId;

          // Handle subscription checkout
          if (session.mode === "subscription") {
            const subscriptionId = session.subscription as string;

            if (!clerkUserId || !subscriptionId) {
              console.error("Missing clerkUserId or subscriptionId");
              break;
            }

            // ⚠️ CRITICAL: current_period_end is in subscription.items.data[0]
            const subscription: any = await stripe.subscriptions.retrieve(subscriptionId);
            const currentPeriodEnd = subscription.items?.data?.[0]?.current_period_end;

            if (!currentPeriodEnd) {
              console.error("No current_period_end found");
              break;
            }

            // Update user membership
            const { internal } = await import("./_generated/api.js");
            await ctx.runMutation(internal.stripeDb.updateMembershipStatus, {
              clerkUserId,
              stripeSubscriptionId: subscriptionId,
              currentPeriodEnd,
            });

            console.log(`✅ Membership activated for user: ${clerkUserId}`);
          }

          // Handle one-time payment checkout
          if (session.mode === "payment") {
            // For one-time payments, you might want different logic
            console.log(`✅ One-time payment completed for user: ${clerkUserId}`);
          }

          break;
        }

        case "customer.subscription.updated": {
          // Handle subscription renewal/update
          const subscription = event.data.object as any;
          const clerkUserId = subscription.metadata?.clerkUserId;

          if (!clerkUserId) {
            console.error("Missing clerkUserId in subscription metadata");
            break;
          }

          const currentPeriodEnd = subscription.items?.data?.[0]?.current_period_end;

          if (!currentPeriodEnd) {
            console.error("No current_period_end found");
            break;
          }

          // Update membership expiry (handles renewals)
          const { internal } = await import("./_generated/api.js");
          await ctx.runMutation(internal.stripeDb.updateMembershipStatus, {
            clerkUserId,
            stripeSubscriptionId: subscription.id,
            currentPeriodEnd,
          });

          console.log(`✅ Subscription updated for user: ${clerkUserId}`);
          break;
        }

        case "customer.subscription.deleted": {
          // Handle subscription cancellation
          const subscription = event.data.object as any;

          const { internal } = await import("./_generated/api.js");
          await ctx.runMutation(internal.stripeDb.cancelMembership, {
            stripeSubscriptionId: subscription.id,
          });

          console.log(`✅ Subscription canceled: ${subscription.id}`);
          break;
        }

        case "invoice.payment_failed": {
          // Handle failed payment
          const invoice = event.data.object as any;
          const subscriptionId = invoice.subscription;

          if (!subscriptionId) {
            console.error("No subscription ID in failed invoice");
            break;
          }

          const attemptCount = invoice.attempt_count || 0;

          const { internal } = await import("./_generated/api.js");
          await ctx.runMutation(internal.stripeDb.handlePaymentFailure, {
            stripeSubscriptionId: subscriptionId,
            attemptCount,
          });

          console.log(`⚠️ Payment failed for subscription: ${subscriptionId}, attempt: ${attemptCount}`);
          break;
        }

        case "invoice.paid": {
          // Confirm successful payment (handles renewals)
          const invoice = event.data.object as any;
          const subscriptionId = invoice.subscription;

          if (!subscriptionId) {
            break; // One-time invoice, not subscription
          }

          const subscription: any = await stripe.subscriptions.retrieve(subscriptionId);
          const clerkUserId = subscription.metadata?.clerkUserId;
          const currentPeriodEnd = subscription.items?.data?.[0]?.current_period_end;

          if (!clerkUserId || !currentPeriodEnd) {
            console.error("Missing data for invoice.paid event");
            break;
          }

          const { internal } = await import("./_generated/api.js");
          await ctx.runMutation(internal.stripeDb.updateMembershipStatus, {
            clerkUserId,
            stripeSubscriptionId: subscriptionId,
            currentPeriodEnd,
          });

          console.log(`✅ Invoice paid for user: ${clerkUserId}`);
          break;
        }
      }

      return new Response(JSON.stringify({ received: true }), {
        status: 200,
      });
    } catch (err) {
      console.error("Webhook error:", err);
      return new Response(
        JSON.stringify({ error: err instanceof Error ? err.message : "Webhook error" }),
        { status: 400 }
      );
    }
  }),
});

export default http;
```

### 4.4 Frontend Integration

#### Checkout Button

On your frontend, create a button that calls the `createCheckoutSession` action:

```tsx
"use client";

import { useAction } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useUser } from "@clerk/nextjs";
import { useState } from "react";

export function UpgradeButton() {
  const { user } = useUser();
  const createCheckoutSession = useAction(api.stripe.createCheckoutSession);
  const [loading, setLoading] = useState(false);

  const handleUpgrade = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const result = await createCheckoutSession({
        clerkUserId: user.id,
        mode: "subscription", // or "payment" for one-time
      });

      if (result.url) {
        window.open(result.url, "_blank");
      }
    } catch (error) {
      console.error("Error creating checkout session:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleUpgrade} disabled={loading}>
      {loading ? "Loading..." : "Upgrade to Premium"}
    </button>
  );
}
```

#### Customer Portal Button

Allow users to manage their subscription, payment methods, and billing:

```tsx
"use client";

import { useAction } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useUser } from "@clerk/nextjs";
import { useState } from "react";

export function ManageBillingButton() {
  const { user } = useUser();
  const createPortalSession = useAction(api.stripe.createCustomerPortalSession);
  const [loading, setLoading] = useState(false);

  const handleManageBilling = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const result = await createPortalSession({
        clerkUserId: user.id,
      });

      if (result.url) {
        window.open(result.url, "_blank");
      }
    } catch (error) {
      console.error("Error creating portal session:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleManageBilling} disabled={loading}>
      {loading ? "Loading..." : "Manage Billing"}
    </button>
  );
}
```

### 4.5 Return Page (`app/checkout/return/page.tsx`)

See `resources/return-page-example.tsx` for full implementation with success/error states.

## Phase 5: Webhook Setup & Testing

### 5.1 Get Your Convex HTTP Actions URL

⚠️ **CRITICAL: Use the `.convex.site` domain**

1. Go to Convex Dashboard → **Settings**
2. Find your deployment URL
3. Your webhook URL will be: `https://your-deployment.convex.site/stripe/webhook`
   - ❌ NOT `.convex.cloud`
   - ✅ USE `.convex.site`

### 5.2 Create Webhook in Stripe Dashboard

1. Go to **Developers → Webhooks** in Stripe Dashboard
2. Click **+ Add endpoint**
3. Enter webhook URL: `https://your-deployment.convex.site/stripe/webhook`
4. Select events to listen for:
   - `checkout.session.completed` (required - initial payment)
   - `customer.subscription.updated` (required - renewals & updates)
   - `customer.subscription.deleted` (required - cancellations)
   - `invoice.payment_failed` (required - failed payments)
   - `invoice.paid` (recommended - successful renewals)
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_...`)
7. Add to Convex environment: `STRIPE_WEBHOOK_SECRET=whsec_...`

### 5.3 Test with Stripe CLI (Optional but Recommended)

```bash
# Install Stripe CLI
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward webhooks to your Convex endpoint
stripe listen --forward-to https://your-deployment.convex.site/stripe/webhook
```

## Phase 6: Dev Mode Testing

### 6.1 Test Checklist

- [ ] Start your app: `npm run dev`
- [ ] Click upgrade/checkout button
- [ ] Verify Stripe checkout page opens in new tab
- [ ] Use Stripe test card:
  - Card: `4242 4242 4242 4242`
  - Expiry: Any future date
  - CVC: Any 3 digits
  - ZIP: Any 5 digits
- [ ] Complete payment
- [ ] Verify redirect to success page
- [ ] Check Convex Dashboard → Data → users table
- [ ] Confirm user has updated membership fields
- [ ] Check Stripe Dashboard → Webhooks → Events
- [ ] Verify webhook was received successfully

### 6.2 Common Issues & Solutions

**Issue:** Webhook not receiving events
- **Fix:** Confirm you're using `.convex.site` not `.convex.cloud`
- **Fix:** Verify webhook secret is set correctly in Convex env vars

**Issue:** `SubtleCryptoProvider cannot be used in a synchronous context`
- **Fix:** Use `constructEventAsync` not `constructEvent`

**Issue:** Membership status not updating
- **Fix:** Check `current_period_end` is accessed from `subscription.items.data[0]`
- **Fix:** Verify `clerkUserId` is in checkout session metadata

## Phase 7: Customer Portal Configuration

The Customer Portal is **essential** for any SaaS product. It allows users to self-manage their subscriptions without contacting support.

### 7.1 Configure Customer Portal in Dashboard

1. Go to [Customer Portal Settings](https://dashboard.stripe.com/settings/billing/portal) in Stripe Dashboard
2. **Business information**
   - Add your logo, icon, and brand colors
   - Add support email and phone number
   - Add Terms of Service and Privacy Policy URLs
3. **Features to enable:**
   - ✅ **Update payment method** - Let customers add/remove cards
   - ✅ **Cancel subscriptions** - Choose immediate or end-of-period cancellation
   - ✅ **Update subscription** - Allow upgrades/downgrades (if you have multiple tiers)
   - ✅ **Invoice history** - Let customers download past invoices
   - ✅ **Customer information** - Allow email/address updates
4. Click **Save**

### 7.2 What Customers Can Do in the Portal

With the Customer Portal, your customers can:
- View current subscription and billing cycle
- Update payment methods (add/remove cards)
- Cancel or resume subscriptions
- View and download all invoices
- Update billing information
- See payment history

**This means less support work for you!** Most billing questions can be self-served.

### 7.3 Portal Best Practices

**Where to place the Portal button:**
- In account/settings page (always visible)
- In subscription status displays
- In email receipts (Stripe adds this automatically)

**When to show the Portal button:**
- Only show to users with `stripeCustomerId` (i.e., users who have subscribed)

Example conditional rendering:
```tsx
{user.stripeCustomerId && <ManageBillingButton />}
```

## Phase 8: Payment Failure Handling & Revenue Recovery

~9-15% of subscription payments fail initially, but most are recoverable. Proper handling is **critical** for revenue.

### 8.1 Enable Smart Retries

Smart Retries use AI to determine the best time to retry failed payments.

**In Stripe Dashboard:**
1. Go to [Revenue Recovery → Retries](https://dashboard.stripe.com/revenue_recovery/retries)
2. Toggle on **Smart Retries**
3. Configure retry settings:
   - **Number of retries:** 4-8 retries recommended
   - **Duration:** 2-4 weeks recommended
4. Configure what happens after final retry:
   - **Recommended:** Mark subscription as unpaid (keeps subscription, stops invoicing)
   - Alternative: Cancel subscription
   - Alternative: Leave past_due (keeps invoicing, may annoy customers)
5. Click **Save**

### 8.2 Why Smart Retries Matter

- **Success rate:** 15-25% of failed payments succeed on retry
- **Revenue recovery:** Can recover thousands per month for mid-size SaaS
- **AI-powered:** Retries at optimal times (e.g., after payday for debit cards)
- **No work required:** Fully automated once enabled

### 8.3 Handle Failed Payments in Your App

Your app should respond to payment failures:

```typescript
// Already implemented in convex/stripeDb.ts!
export const handlePaymentFailure = internalMutation({
  args: {
    stripeSubscriptionId: v.string(),
    attemptCount: v.number(),
  },
  handler: async (ctx, args) => {
    // Grace period logic: keep access for 3 attempts
    if (args.attemptCount >= 3) {
      await ctx.db.patch(user._id, {
        membershipStatus: "past_due",
      });
    }
  },
});
```

**User Experience Recommendations:**
- Attempts 1-2: Don't revoke access, send gentle reminder email
- Attempts 3-4: Revoke access, show "Payment Failed" banner in app
- Final retry: Send "Subscription at risk of cancellation" email

### 8.4 Enable Automated Emails (Recommended)

1. Go to [Billing → Revenue recovery → Emails](https://dashboard.stripe.com/revenue_recovery/customer_emails)
2. Enable these emails:
   - ✅ **Payment failed** - Sent immediately when payment fails
   - ✅ **Card expiring soon** - Sent 7-15 days before expiry
   - ✅ **Update payment method** - Sent when card needs updating
3. Customize email templates with your branding
4. Click **Save**

**Why this matters:** Automated emails recover 5-10% of failed payments without any manual work.

### 8.5 Monitor Failed Payments

**In your Dashboard:**
- Go to [Billing → Revenue Recovery](https://dashboard.stripe.com/revenue_recovery)
- View recovery rate and revenue recovered
- See which customers have failing payments

**Set up alerts:**
- For high-value subscriptions (>$100/month), notify your sales team of failures
- Use webhooks to send Slack notifications for VIP customer failures

## Phase 9: Comprehensive Testing Guide

Thorough testing prevents production issues and lost revenue.

### 9.1 Local Webhook Testing with Stripe CLI

**Install Stripe CLI:**
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows (with Scoop)
scoop install stripe

# Or download from https://stripe.com/docs/stripe-cli
```

**Forward webhooks to Convex:**
```bash
# Login first
stripe login

# Forward webhooks to your Convex deployment
stripe listen --forward-to https://your-deployment.convex.site/stripe/webhook

# You'll see a webhook signing secret - add this to Convex env vars temporarily for testing
```

**Test specific events:**
```bash
# Test successful subscription creation
stripe trigger checkout.session.completed

# Test subscription renewal
stripe trigger customer.subscription.updated

# Test failed payment
stripe trigger invoice.payment_failed

# Test cancellation
stripe trigger customer.subscription.deleted
```

### 9.2 Test Cards & Scenarios

Use these test card numbers in **test mode only:**

| Card Number | Scenario | Use Case |
|------------|----------|----------|
| `4242 4242 4242 4242` | Succeeds | Normal successful payment |
| `4000 0025 0000 3155` | Requires authentication | Test 3D Secure flow |
| `4000 0000 0000 9995` | Always declines | Test payment failure handling |
| `4000 0000 0000 0341` | Attaching requires auth | Test payment method updates |
| `4000 0082 6000 0000` | Expires in current year | Test expiring card emails |

**Expiry & CVC:** Any future date and any 3-digit CVC work for test cards.

### 9.3 Test Checklist (Before Production)

Test all critical flows:

**Initial Subscription Flow:**
- [ ] User can click "Upgrade" and reach Stripe Checkout
- [ ] Test card `4242...` successfully creates subscription
- [ ] User redirects to success page after payment
- [ ] `membershipStatus` updates to "premium" in Convex
- [ ] `membershipExpiry` is set correctly (1 month from now for monthly)
- [ ] Webhook `checkout.session.completed` received and processed

**Customer Portal Flow:**
- [ ] "Manage Billing" button works for subscribed users
- [ ] User can view subscription details in portal
- [ ] User can update payment method
- [ ] User can cancel subscription
- [ ] Cancellation triggers `customer.subscription.deleted` webhook
- [ ] `membershipStatus` updates to "free" after cancellation

**Payment Failure Flow:**
- [ ] Use test card `4000 0000 0000 9995` to trigger failure
- [ ] `invoice.payment_failed` webhook received
- [ ] `handlePaymentFailure` mutation runs correctly
- [ ] User sees appropriate message in app after 3 failures
- [ ] Smart Retries are scheduled correctly

**Renewal Flow:**
- [ ] Use Test Clocks to simulate time passage (see below)
- [ ] Subscription renews automatically after 1 month
- [ ] `customer.subscription.updated` or `invoice.paid` webhook fires
- [ ] `membershipExpiry` extends by another month

### 9.4 Test Clocks (Advanced - Simulate Time)

Test Clocks let you simulate subscription renewals without waiting weeks/months.

**Create Test Clock:**
1. Go to [Workbench → Test Clocks](https://dashboard.stripe.com/test/test-clocks)
2. Click **Create test clock**
3. Set start time to "now"
4. Create customer and subscription using this test clock
5. Advance time by 1 month to test renewal
6. Advance by 3 months to test failed payment retries

**With Test Clocks you can test:**
- Annual subscription renewals (without waiting 1 year!)
- Trial expiration (without waiting 14 days)
- Failed payment retry schedules
- Proration calculations

### 9.5 Monitor Webhook Delivery

**In Stripe Dashboard:**
1. Go to **Developers → Webhooks**
2. Click on your webhook endpoint
3. View **Event deliveries** tab
4. Check for:
   - ✅ All events have 200 status (success)
   - ❌ Any 400/500 errors (your webhook failed)
   - ⏱️ Response times (should be <2 seconds)

**Debug failed webhooks:**
- Click on failed event to see error message
- Use Convex logs to see what went wrong
- Use "Resend" button to retry webhook

## Phase 10: Production Deployment

### 10.1 Switch to Live Mode

1. **Get Live API Keys** from Stripe Dashboard (toggle to Live mode)
2. **Create Production Product & Price** in Live mode
3. **Update Convex Production Environment Variables:**
   ```
   STRIPE_SECRET_KEY=sk_live_...
   STRIPE_PRICE_ID=price_live_...
   STRIPE_WEBHOOK_SECRET=whsec_live_...
   ```
4. **Update Next.js Environment:**
   ```
   NEXT_PUBLIC_SITE_URL=https://yourdomain.com
   ```

### 10.2 Create Production Webhook

1. In Stripe Dashboard (Live mode) → Webhooks
2. Add endpoint: `https://your-prod-deployment.convex.site/stripe/webhook`
3. Select all required events (same as test mode)
4. Copy new signing secret
5. Update `STRIPE_WEBHOOK_SECRET` in Convex production env

### 10.3 Configure Customer Portal (Live Mode)

1. Go to [Customer Portal Settings](https://dashboard.stripe.com/settings/billing/portal) (Live mode)
2. Configure same settings as test mode
3. Add your production URLs and branding
4. Enable desired features
5. Click **Save**

### 10.4 Enable Smart Retries (Live Mode)

1. Go to [Revenue Recovery → Retries](https://dashboard.stripe.com/revenue_recovery/retries) (Live mode)
2. Enable Smart Retries with same settings as test mode
3. Enable automated emails for payment failures
4. Click **Save**

### 10.5 Production Test

**Test with real payment method (refund immediately after):**
- [ ] Complete successful subscription purchase
- [ ] Verify webhook delivery in Stripe Dashboard → Webhooks → Event deliveries
- [ ] Check user membership updates in production database (Convex Dashboard)
- [ ] Test Customer Portal access (update payment method, view invoices)
- [ ] Test cancellation flow (cancel and verify webhook + database update)
- [ ] Refund the test payment in Stripe Dashboard

**Monitor for 24-48 hours:**
- [ ] Check webhook success rate (should be 100%)
- [ ] Monitor error logs in Convex
- [ ] Check first real customer payments process correctly

## Phase 11: Production Best Practices & Webhook Reliability

### 11.1 Webhook Reliability Patterns

#### Idempotency - Prevent Duplicate Processing

Webhooks may be sent multiple times. Your handler must be idempotent:

```typescript
// Add this to convex/stripeDb.ts
export const processedWebhookEvents = defineTable({
  eventId: v.string(), // Stripe event ID
  processedAt: v.number(),
}).index("by_event_id", ["eventId"]);

// Check before processing webhook
export const isEventProcessed = internalQuery({
  args: { eventId: v.string() },
  handler: async (ctx, args) => {
    const existing = await ctx.db
      .query("processedWebhookEvents")
      .withIndex("by_event_id", (q) => q.eq("eventId", args.eventId))
      .unique();
    return !!existing;
  },
});

export const markEventProcessed = internalMutation({
  args: { eventId: v.string() },
  handler: async (ctx, args) => {
    await ctx.db.insert("processedWebhookEvents", {
      eventId: args.eventId,
      processedAt: Date.now(),
    });
  },
});
```

**Update webhook handler to use idempotency:**
```typescript
// In convex/http.ts, before switch statement:
const { internal } = await import("./_generated/api.js");

// Check if already processed
const isProcessed = await ctx.runQuery(internal.stripeDb.isEventProcessed, {
  eventId: event.id,
});

if (isProcessed) {
  console.log(`Event ${event.id} already processed, skipping`);
  return new Response(JSON.stringify({ received: true }), { status: 200 });
}

// ... handle event with switch statement ...

// After successful processing, mark as processed
await ctx.runMutation(internal.stripeDb.markEventProcessed, {
  eventId: event.id,
});
```

#### Event Ordering - Don't Assume Order

Stripe doesn't guarantee event order. Handle events independently:

```typescript
// ❌ DON'T rely on event order
// Assuming subscription.updated comes before invoice.paid

// ✅ DO handle each event independently
// Each event should have enough data to process standalone
```

**Best practice:** Always fetch the latest subscription state from Stripe if you need current data:

```typescript
case "invoice.payment_failed": {
  const invoice = event.data.object;

  // Fetch current subscription state (don't assume from previous events)
  const subscription = await stripe.subscriptions.retrieve(invoice.subscription);

  // Now you have accurate current state
}
```

### 11.2 Monitoring & Alerting

#### Set Up Monitoring

**Webhook health checks:**
```typescript
// Create a simple health endpoint in convex/http.ts
http.route({
  path: "/health",
  method: "GET",
  handler: httpAction(async () => {
    return new Response(JSON.stringify({ status: "ok" }), { status: 200 });
  }),
});
```

**Monitor in Stripe Dashboard:**
- Go to **Developers → Webhooks** daily (first week of production)
- Check "Event deliveries" for any failures
- Set up email notifications for webhook failures

**Monitor in Convex:**
- Check logs for any Stripe-related errors
- Monitor subscription creation/update rates
- Track failed payment rates

#### Set Up Alerts

**Critical alerts to implement:**
1. Webhook failure rate > 1%
2. No subscriptions created in 24 hours (if you usually get signups)
3. Failed payment rate > 15%
4. Subscription cancellation spike (>2x normal rate)

### 11.3 Data Consistency

**Always sync from Stripe as source of truth:**

```typescript
// Good: Periodically sync subscription status from Stripe
export const syncSubscriptionStatus = internalMutation({
  args: {
    clerkUserId: v.string(),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_clerk_id", (q) => q.eq("clerkId", args.clerkUserId))
      .unique();

    if (!user || !user.stripeSubscriptionId) return;

    // Fetch current state from Stripe
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
    const subscription = await stripe.subscriptions.retrieve(user.stripeSubscriptionId);

    // Update database to match Stripe
    const currentPeriodEnd = subscription.items?.data?.[0]?.current_period_end;
    const status = subscription.status === "active" ? "premium" : "free";

    await ctx.db.patch(user._id, {
      membershipStatus: status,
      membershipExpiry: currentPeriodEnd ? currentPeriodEnd * 1000 : undefined,
    });
  },
});
```

Run this sync:
- When user logs in (to ensure accurate status)
- Daily via cron job (for all active subscriptions)
- When displaying billing information

### 11.4 Security Best Practices

**Protect your API keys:**
- Never commit `STRIPE_SECRET_KEY` to git
- Use different keys for dev/prod
- Rotate keys every 6 months (or immediately if compromised)

**Verify webhook signatures:**
- Always use `constructEventAsync` (already implemented)
- Never trust webhook data without signature verification
- Keep `STRIPE_WEBHOOK_SECRET` secure

**Limit webhook endpoint access:**
- Only accept POST requests (already implemented)
- Add rate limiting if you get webhook spam
- Monitor for suspicious activity

### 11.5 Common Production Issues & Solutions

**Issue: Webhooks stopped working**
- Check if Convex deployment URL changed
- Verify `STRIPE_WEBHOOK_SECRET` is correct
- Check webhook endpoint is enabled in Stripe Dashboard
- Look for errors in Stripe → Webhooks → Event deliveries

**Issue: Subscriptions not updating after renewal**
- Verify `customer.subscription.updated` or `invoice.paid` webhooks are enabled
- Check webhook handler processes these events
- Verify `current_period_end` is being updated correctly

**Issue: Users charged but no access granted**
- Check webhook was received (Stripe Dashboard)
- Check webhook processed successfully (Convex logs)
- Verify database update happened
- Check for errors in `updateMembershipStatus` mutation

**Issue: Duplicate charges**
- Usually caused by retry logic gone wrong
- Check you're not calling `stripe.checkout.sessions.create` multiple times
- Implement idempotency keys for payment creation

### 11.6 Maintenance Checklist

**Weekly:**
- [ ] Review webhook delivery success rate
- [ ] Check for any unusual failed payments
- [ ] Monitor subscription churn rate

**Monthly:**
- [ ] Review Stripe Dashboard for anomalies
- [ ] Check Smart Retries recovery rate
- [ ] Audit webhook processing logs
- [ ] Review customer support tickets related to billing

**Quarterly:**
- [ ] Update Stripe SDK version (test in staging first)
- [ ] Review and optimize retry settings based on data
- [ ] Audit security (rotate API keys)
- [ ] Test disaster recovery (webhook failures, database issues)

## Quick Reference Checklist

### Common Mistakes to Avoid

1. ❌ Using `.convex.cloud` for webhooks → ✅ Use `.convex.site`
2. ❌ Using `constructEvent()` → ✅ Use `constructEventAsync()`
3. ❌ Looking for `subscription.current_period_end` → ✅ Use `subscription.items.data[0].current_period_end`
4. ❌ Forgetting to set `STRIPE_WEBHOOK_SECRET` in Convex
5. ❌ Not including `metadata` in checkout session
6. ❌ Only listening to `checkout.session.completed` → ✅ Listen to all lifecycle events
7. ❌ Not configuring Customer Portal → ✅ Essential for production
8. ❌ Not enabling Smart Retries → ✅ Recovers 15-25% of failed payments
9. ❌ Not testing renewal flows → ✅ Use Test Clocks
10. ❌ Not implementing idempotency → ✅ Prevent duplicate processing

### Environment Variables Checklist

**Convex Dashboard:**
- [ ] `STRIPE_SECRET_KEY` (sk_test_... for dev, sk_live_... for prod)
- [ ] `STRIPE_PRICE_ID` (price_... for your product)
- [ ] `STRIPE_WEBHOOK_SECRET` (whsec_... from webhook endpoint)

**Next.js `.env.local`:**
- [ ] `NEXT_PUBLIC_SITE_URL` (http://localhost:3000 for dev, https://yourdomain.com for prod)

### Implementation Checklist

**Phase 1-3: Setup**
- [ ] Install `stripe` package
- [ ] Update database schema with Stripe fields
- [ ] Get Stripe API keys (test mode)
- [ ] Create product and price in Stripe Dashboard
- [ ] Set environment variables

**Phase 4: Code Implementation**
- [ ] Create `convex/stripe.ts` with checkout and portal actions
- [ ] Create `convex/stripeDb.ts` with database helpers
- [ ] Create `convex/http.ts` with webhook handler
- [ ] Add checkout button to frontend
- [ ] Add customer portal button to frontend
- [ ] Create return page

**Phase 5: Webhooks**
- [ ] Get Convex `.convex.site` URL
- [ ] Create webhook endpoint in Stripe Dashboard
- [ ] Add all required events (checkout, subscription, invoice events)
- [ ] Test webhooks with Stripe CLI

**Phase 6: Testing**
- [ ] Test successful subscription flow
- [ ] Test failed payment flow
- [ ] Test customer portal (cancel, update payment)
- [ ] Test renewal with Test Clocks
- [ ] Verify all webhooks process correctly

**Phase 7: Customer Portal**
- [ ] Configure portal in Stripe Dashboard
- [ ] Add branding and business information
- [ ] Enable all relevant features
- [ ] Test portal as end user

**Phase 8: Revenue Recovery**
- [ ] Enable Smart Retries
- [ ] Configure retry settings (4-8 retries, 2-4 weeks)
- [ ] Enable automated emails
- [ ] Test payment failure handling
- [ ] Monitor recovery dashboard

**Phase 9: Comprehensive Testing**
- [ ] Complete all test checklist items
- [ ] Test with different test cards
- [ ] Test subscription lifecycle with Test Clocks
- [ ] Verify webhook delivery 100% success rate

**Phase 10: Production**
- [ ] Switch to live mode API keys
- [ ] Create production webhook endpoint
- [ ] Configure Customer Portal (live mode)
- [ ] Enable Smart Retries (live mode)
- [ ] Test with real payment (then refund)
- [ ] Monitor for 24-48 hours

**Phase 11: Best Practices (Recommended)**
- [ ] Implement webhook idempotency
- [ ] Add monitoring and alerts
- [ ] Set up data consistency sync
- [ ] Review security checklist
- [ ] Create maintenance schedule

## Phase 12: Advanced Features (Optional)

### 12.1 Free Trials

Add a free trial period before charging customers:

```typescript
// In convex/stripe.ts - createCheckoutSession
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: "subscription",
  line_items: [{ price: process.env.STRIPE_PRICE_ID!, quantity: 1 }],
  subscription_data: {
    trial_period_days: 14, // 14-day free trial
  },
  success_url: `${siteUrl}/checkout/return?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${siteUrl}`,
  metadata: { clerkUserId: args.clerkUserId, userId: user._id },
});
```

**Trial best practices:**
- 7-14 days is standard for SaaS
- Collect payment method upfront (prevents trial abuse)
- Send email 3 days before trial ends
- Show trial status in your app UI

**Handling trial end:**
```typescript
case "customer.subscription.trial_will_end": {
  // Send reminder email 3 days before trial ends
  const subscription = event.data.object;
  // Email user about upcoming charge
}
```

### 12.2 Coupons & Discounts

Create and apply discount codes:

**Create coupon in Stripe Dashboard:**
1. Go to **Products → Coupons**
2. Click **+ Create coupon**
3. Set discount (% off or fixed amount)
4. Set duration (once, forever, or repeating)
5. Copy coupon ID

**Apply coupon to checkout:**
```typescript
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: "subscription",
  line_items: [{ price: process.env.STRIPE_PRICE_ID!, quantity: 1 }],
  discounts: [{
    coupon: "SUMMER2024", // Your coupon code
  }],
  // ... rest of session config
});
```

**Allow customers to enter codes:**
```typescript
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: "subscription",
  line_items: [{ price: process.env.STRIPE_PRICE_ID!, quantity: 1 }],
  allow_promotion_codes: true, // Shows coupon field in checkout
  // ... rest of session config
});
```

### 12.3 One-Time Payments

For non-subscription purchases (e.g., credits, one-time features):

```typescript
// Use mode: "payment" instead of "subscription"
const session = await stripe.checkout.sessions.create({
  customer: customerId,
  mode: "payment", // One-time payment
  line_items: [{
    price_data: {
      currency: "usd",
      product_data: {
        name: "100 Credits",
        description: "One-time credit purchase",
      },
      unit_amount: 999, // $9.99 in cents
    },
    quantity: 1,
  }],
  success_url: `${siteUrl}/checkout/return?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${siteUrl}`,
  metadata: { clerkUserId: args.clerkUserId, userId: user._id },
});
```

**Handle one-time payment webhook:**
```typescript
case "checkout.session.completed": {
  const session = event.data.object;

  if (session.mode === "payment") {
    // One-time payment completed
    const clerkUserId = session.metadata?.clerkUserId;

    // Grant one-time purchase (e.g., add credits)
    await ctx.runMutation(internal.stripeDb.addCredits, {
      clerkUserId,
      amount: 100,
    });
  }
}
```

**One-time vs Subscription - When to use which:**
- **Subscriptions:** Recurring revenue (monthly/yearly plans)
- **One-time:** Credits, lifetime access, course purchases, add-ons

### 12.4 Multiple Subscription Tiers

Support different pricing tiers (Basic, Pro, Enterprise):

**Setup in Stripe:**
1. Create separate prices for each tier
2. Add price IDs to environment variables:
   ```
   STRIPE_PRICE_ID_BASIC=price_basic...
   STRIPE_PRICE_ID_PRO=price_pro...
   STRIPE_PRICE_ID_ENTERPRISE=price_enterprise...
   ```

**Pass tier in frontend:**
```typescript
const result = await createCheckoutSession({
  clerkUserId: user.id,
  mode: "subscription",
  priceId: "price_pro...", // User selected Pro tier
});
```

**Update createCheckoutSession action:**
```typescript
export const createCheckoutSession = action({
  args: {
    clerkUserId: v.string(),
    mode: v.optional(v.union(v.literal("subscription"), v.literal("payment"))),
    priceId: v.optional(v.string()), // Allow custom price ID
  },
  handler: async (ctx, args) => {
    // ... existing code ...

    const priceId = args.priceId || process.env.STRIPE_PRICE_ID!;

    const session = await stripe.checkout.sessions.create({
      customer: customerId,
      mode: args.mode || "subscription",
      line_items: [{ price: priceId, quantity: 1 }],
      // ... rest of config
    });
  },
});
```

**Store tier in database:**
```typescript
// Update schema
membershipTier: v.optional(v.union(
  v.literal("basic"),
  v.literal("pro"),
  v.literal("enterprise")
)),

// Update in webhook
await ctx.db.patch(user._id, {
  membershipStatus: "premium",
  membershipTier: "pro", // Store which tier
  membershipExpiry: currentPeriodEnd * 1000,
  stripeSubscriptionId: subscriptionId,
});
```

**Customer Portal upgrades/downgrades:**
- Configure product catalog in Customer Portal settings
- Add all your price tiers
- Users can upgrade/downgrade themselves
- Stripe handles proration automatically

## Resources

- See `resources/common-mistakes.md` for detailed error solutions
- See `resources/return-page-example.tsx` for full return page code
- [Stripe Checkout Docs](https://docs.stripe.com/checkout)
- [Stripe Webhooks Guide](https://docs.stripe.com/webhooks)
- [Stripe Customer Portal](https://docs.stripe.com/customer-management)
- [Smart Retries](https://docs.stripe.com/billing/revenue-recovery/smart-retries)
- [Test Clocks](https://docs.stripe.com/billing/testing/test-clocks)
- [Convex HTTP Actions](https://docs.convex.dev/functions/http-actions)
