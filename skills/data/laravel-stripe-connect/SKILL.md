---
name: laravel-stripe-connect
description: Build marketplaces and platforms with Stripe Connect. Use when implementing multi-vendor payments, seller onboarding, commissions, payouts, or split payments.
versions:
  laravel: "12.x"
  stripe-php: "16.x"
  php: "8.4"
user-invocable: true
references: references/overview.md, references/account-types.md, references/payment-flows.md, references/onboarding.md, references/fees-commissions.md, references/payouts.md, references/refunds-disputes.md, references/compliance.md, references/templates/Seller.php.md, references/templates/SellerOnboardingController.php.md, references/templates/MarketplacePaymentController.php.md, references/templates/PayoutController.php.md, references/templates/ConnectWebhookHandler.php.md, references/templates/ConnectRoutes.php.md
related-skills: laravel-billing, laravel-api, laravel-auth
---

# Laravel Stripe Connect

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Check existing payment setup, Seller model
2. **fuse-ai-pilot:research-expert** - Verify latest Stripe Connect docs via Context7
3. **mcp__context7__query-docs** - Query specific patterns (account types, payment flows)

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

Stripe Connect enables platforms and marketplaces to accept payments and pay out sellers/service providers.

| Use Case | Example | This Skill |
|----------|---------|------------|
| **Marketplace** | Etsy, eBay | ✅ Yes |
| **On-demand services** | Uber, DoorDash | ✅ Yes |
| **Crowdfunding** | Kickstarter | ✅ Yes |
| **SaaS with payouts** | Substack, Teachable | ✅ Yes |
| **Simple SaaS** | Netflix, Notion | ❌ Use billing |

### Key Difference: Billing vs Connect

| Aspect | **Laravel Cashier** | **Stripe Connect** |
|--------|--------------------|--------------------|
| **Money flow** | Customer → You | Customer → Seller (via you) |
| **Accounts** | 1 Stripe account | Platform + N seller accounts |
| **Use case** | Subscriptions | Multi-party payments |
| **Complexity** | Simple | Complex |

---

## Critical Rules

1. **Verify seller identity** - KYC required before payouts
2. **Handle negative balances** - Platform liable if seller can't cover refunds
3. **Webhook-driven** - Never trust client-side for payment confirmation
4. **Store account IDs** - Always persist `stripe_account_id` on sellers
5. **Test with test mode** - Use test account IDs before production
6. **Understand liability** - Know who pays for disputes per account type

---

## Architecture

```
app/
├── Http/
│   ├── Controllers/
│   │   └── Connect/
│   │       ├── SellerOnboardingController.php
│   │       ├── MarketplacePaymentController.php
│   │       └── PayoutController.php
│   └── Middleware/
│       └── EnsureSellerOnboarded.php
├── Models/
│   ├── Seller.php              ← Connected account holder
│   └── Transaction.php         ← Payment records
├── Listeners/
│   └── ConnectWebhookHandler.php
└── Services/
    └── StripeConnectService.php

config/
└── services.php                ← Stripe keys

routes/
└── web.php                     ← Webhook routes (no CSRF)
```

---

## Decision Guide

### Which Account Type?

```
Who handles customer support?
├── Seller handles everything → Standard
├── Platform handles support → Express or Custom
│   ├── Need full UI control? → Custom
│   └── Want Stripe's dashboard? → Express (recommended)
```

### Which Payment Flow?

```
Who appears on customer's bank statement?
├── Seller's name → Direct charges
├── Platform's name → Destination charges (recommended)
└── Complex split? → Separate charges + transfers
```

---

## Key Concepts

| Concept | Description | Reference |
|---------|-------------|-----------|
| **Connected Account** | Seller's Stripe account linked to platform | [account-types.md](references/account-types.md) |
| **Onboarding** | KYC process for sellers | [onboarding.md](references/onboarding.md) |
| **Application Fee** | Platform's commission on payments | [fees-commissions.md](references/fees-commissions.md) |
| **Destination Charge** | Payment with automatic transfer to seller | [payment-flows.md](references/payment-flows.md) |
| **Payout** | Transfer from Stripe balance to bank | [payouts.md](references/payouts.md) |

---

## Reference Guide

### Concepts (WHY & Architecture)

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Overview** | [overview.md](references/overview.md) | Understanding Connect fundamentals |
| **Account Types** | [account-types.md](references/account-types.md) | Choosing Standard/Express/Custom |
| **Payment Flows** | [payment-flows.md](references/payment-flows.md) | Direct vs Destination vs Transfers |
| **Onboarding** | [onboarding.md](references/onboarding.md) | Seller verification process |
| **Fees & Commissions** | [fees-commissions.md](references/fees-commissions.md) | Platform revenue model |
| **Payouts** | [payouts.md](references/payouts.md) | Paying sellers |
| **Refunds & Disputes** | [refunds-disputes.md](references/refunds-disputes.md) | Handling chargebacks |
| **Compliance** | [compliance.md](references/compliance.md) | Legal and tax requirements |

### Templates (Complete Code)

| Template | When to Use |
|----------|-------------|
| [Seller.php.md](references/templates/Seller.php.md) | Seller model with Connect integration |
| [SellerOnboardingController.php.md](references/templates/SellerOnboardingController.php.md) | OAuth and onboarding flow |
| [MarketplacePaymentController.php.md](references/templates/MarketplacePaymentController.php.md) | Creating charges with fees |
| [PayoutController.php.md](references/templates/PayoutController.php.md) | Managing seller payouts |
| [ConnectWebhookHandler.php.md](references/templates/ConnectWebhookHandler.php.md) | Webhook event handling |
| [ConnectRoutes.php.md](references/templates/ConnectRoutes.php.md) | Route definitions |

---

## Quick Reference

### Create Connected Account

```php
$account = \Stripe\Account::create([
    'type' => 'express',
    'country' => 'FR',
    'email' => $seller->email,
    'capabilities' => [
        'card_payments' => ['requested' => true],
        'transfers' => ['requested' => true],
    ],
]);

$seller->update(['stripe_account_id' => $account->id]);
```

### Create Onboarding Link

```php
$link = \Stripe\AccountLink::create([
    'account' => $seller->stripe_account_id,
    'refresh_url' => route('connect.onboarding.refresh'),
    'return_url' => route('connect.onboarding.complete'),
    'type' => 'account_onboarding',
]);

return redirect($link->url);
```

### Destination Charge with Fee

```php
$payment = \Stripe\PaymentIntent::create([
    'amount' => 10000, // €100.00
    'currency' => 'eur',
    'payment_method' => $paymentMethodId,
    'confirm' => true,
    'application_fee_amount' => 1500, // €15.00 platform fee
    'transfer_data' => [
        'destination' => $seller->stripe_account_id,
    ],
]);
```

### Check Account Status

```php
$account = \Stripe\Account::retrieve($seller->stripe_account_id);

$isOnboarded = $account->charges_enabled && $account->payouts_enabled;
$needsInfo = !empty($account->requirements->currently_due);
```

---

## Best Practices

### DO
- Use Express accounts for most marketplaces
- Implement webhook handlers for all Connect events
- Store transaction records locally
- Handle `account.updated` to track onboarding status
- Use idempotency keys for payment creation
- Test with Stripe CLI and test clocks

### DON'T
- Enable payouts before KYC completion
- Ignore negative balance scenarios
- Skip webhook signature verification
- Hardcode Stripe account IDs
- Forget to handle dispute notifications
- Process refunds without checking seller balance
