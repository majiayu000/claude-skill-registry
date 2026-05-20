---
name: auth-builder
description: Build and maintain Stripe → Clerk authentication flows for pricing CTA buttons. Use when implementing new subscription tiers, fixing auto-enrollment issues, or adding payment-to-access flows.
allowed-tools: Read, Write, Edit, Glob, Grep, Shell
---

# Auth Builder for NGM Platform

## Overview
This skill manages the authentication and enrollment flow for the NGM platform, specifically the integration between Stripe payments and Clerk user management. It handles the complete flow from CTA button click to auto-login.

## Complete Flow

```
1. User clicks CTA button
   ↓
2. Frontend calls /api/lip/create-checkout with tier + billingPeriod
   ↓
3. User is redirected to Stripe Checkout
   ↓
4. User completes payment
   ↓
5. Stripe redirects to /subscription-success?session_id={id}
   ↓
6. Frontend calls /api/verify-and-enroll with session_id
   ↓
7. Backend verifies payment, creates/updates Clerk user
   ↓
8. Backend generates sign-in token
   ↓
9. Frontend redirects to /auth/callback?ticket={token}
   ↓
10. User is auto-logged in and redirected to dashboard
```

## Key Files

| File | Purpose |
|------|---------|
| `src/views/LongevityIntelligenceCore.tsx` | Pricing cards and `handleSubscribe` function |
| `server/routes.ts` | Express route for `/api/lip/create-checkout` |
| `src/app/api/lip/create-checkout/route.ts` | Next.js App Router checkout (backup) |
| `src/app/api/verify-and-enroll/route.ts` | Creates Clerk user, sets metadata, generates sign-in token |
| `src/views/SubscriptionSuccess.tsx` | Post-payment page, calls verify-and-enroll |
| `src/app/auth/callback/page.tsx` | Handles sign-in token authentication |
| `src/views/AuthCallback.tsx` | Clerk sign-in with ticket |

## Tier Metadata Configuration

All LIP tiers use this metadata structure:

### Core ($99/month or $79/month annual)
```json
{
  "lipTier": "core",
  "mentorshipAccess": false
}
```

### Professional ($249/month or $199/month annual)
```json
{
  "lipTier": "professional",
  "mentorshipTier": "legacy",
  "mentorshipAccess": true
}
```

### Elite ($625/month or $499/month annual)
```json
{
  "lipTier": "elite",
  "mentorshipTier": "legacy",
  "mentorshipAccess": true
}
```

## Environment Variables

### Required Stripe Price IDs
```bash
# Annual pricing (effective monthly rate)
STRIPE_PRICE_ID_CORE=price_xxx           # $79/mo billed annually
STRIPE_PRICE_ID_PROFESSIONAL=price_xxx    # $199/mo billed annually
STRIPE_PRICE_ID_ELITE=price_xxx           # $499/mo billed annually

# Monthly pricing
STRIPE_PRICE_ID_CORE_MONTHLY=price_xxx         # $99/mo
STRIPE_PRICE_ID_PROFESSIONAL_MONTHLY=price_xxx  # $249/mo
STRIPE_PRICE_ID_ELITE_MONTHLY=price_xxx         # $625/mo
```

## Frontend Implementation

### handleSubscribe Function
Located in `src/views/LongevityIntelligenceCore.tsx`:

```typescript
const handleSubscribe = async (
  tier: "core" | "professional" | "elite",
  period: "annual" | "monthly" = billingPeriod
) => {
  try {
    const response = await fetch("/api/lip/create-checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        tier,
        billingPeriod: period,
        clerkUserId: user?.id || null,
        userEmail: user?.email || null,
      }),
    });

    const data = await response.json();
    if (data.checkoutUrl) {
      window.location.href = data.checkoutUrl;
    }
  } catch (error) {
    console.error("Error creating checkout session:", error);
  }
};
```

### Billing Period Toggle
```typescript
const [billingPeriod, setBillingPeriod] = useState<'annual' | 'monthly'>('annual');
```

## Backend Implementation

### Create Checkout Session
The checkout session must include `session_id` in the success URL:

```typescript
success_url: `${origin}/subscription-success?session_id={CHECKOUT_SESSION_ID}`,
```

### Verify and Enroll (Key Logic)
Located in `src/app/api/verify-and-enroll/route.ts`:

1. **Verify Stripe Session**: Check `session.status === 'complete'`
2. **Extract Customer Info**:
   - Email: `session.customer_details.email`
   - Name: `session.customer_details.name` (split into first/last)
3. **Check Clerk for Existing User**: `clerk.users.getUserList({ emailAddress: [email] })`
4. **Create or Update User**:
   - If exists: `clerk.users.updateUserMetadata()`
   - If new: `clerk.users.createUser()` with firstName, lastName, email
5. **Generate Sign-In Token**: `clerk.signInTokens.createSignInToken()`
6. **Return Token**: Frontend uses it for auto-login

### Required Clerk User Fields
Your Clerk instance requires these fields:
```typescript
await clerk.users.createUser({
  emailAddress: [customerEmail],
  firstName: firstName,
  lastName: lastName,
  publicMetadata: { lipTier, mentorshipTier, mentorshipAccess },
  privateMetadata: { stripeCustomerId, lipSubscriptionStatus: 'active' },
  skipPasswordRequirement: true
});
```

## Error Handling

### Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| 422 "form_data_missing" | Clerk requires first_name/last_name | Extract name from Stripe session |
| 422 "Unprocessable Entity" | User already exists | Retry lookup and update instead |
| 400 "Bad Request" on invitation | Email has pending invitation | Skip invitation, return success with manual sign-in instructions |
| No session_id | success_url missing template var | Add `?session_id={CHECKOUT_SESSION_ID}` |

### Fallback Chain
1. Try to find existing user → update metadata
2. Try to create new user → with name and metadata
3. If 422, retry user lookup → update if found
4. If still fails, create invitation
5. If invitation fails, return success with manual sign-in instructions

## Testing Checklist

- [ ] Annual Core subscription creates user with `lipTier: "core"`, `mentorshipAccess: false` (no `mentorshipTier`)
- [ ] Monthly Professional subscription creates user with `lipTier: "professional"`, `mentorshipTier: "legacy"`, `mentorshipAccess: true`
- [ ] Elite subscription creates user with `lipTier: "elite"`, `mentorshipTier: "legacy"`, `mentorshipAccess: true`
- [ ] User is auto-logged in after payment
- [ ] User is redirected to `/longevity-intelligence-core`
- [ ] Existing user's metadata is updated (not duplicated)
- [ ] User name is extracted from Stripe checkout

## Debugging

Check terminal logs for these patterns:
```
[Verify-Enroll] Looking up user by email: xxx
[Verify-Enroll] Found X existing user(s)
[Verify-Enroll] ✅ Created new user xxx with tier: xxx
[Verify-Enroll] ✅ Generated sign-in token for user xxx
```

Errors will show:
```
[Verify-Enroll] Error creating user: xxx
[Verify-Enroll] Error details: [...]
```
