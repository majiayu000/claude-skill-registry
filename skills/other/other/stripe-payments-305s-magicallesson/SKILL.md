---
name: Stripe Payments
description: Automate Stripe payment processing, subscription management, invoicing, and financial reporting
version: 1.0.0
author: Claude Office Skills
category: payments
tags:
  - stripe
  - payments
  - subscriptions
  - billing
  - fintech
department: finance
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: payments-mcp
  tools:
    - stripe_charges
    - stripe_customers
    - stripe_subscriptions
    - stripe_invoices
capabilities:
  - Payment processing
  - Subscription lifecycle
  - Invoice management
  - Revenue analytics
input:
  - Payment details
  - Customer data
  - Subscription plans
  - Invoice configurations
output:
  - Payment confirmations
  - Subscription status
  - Financial reports
  - Webhook events
languages:
  - en
related_skills:
  - subscription-management
  - invoice-automation
  - saas-metrics
---

# Stripe Payments

Comprehensive skill for automating Stripe payment processing and subscription management.

## Core Workflows

### 1. Payment Flow

```
STRIPE PAYMENT FLOW:
┌─────────────────┐
│    Customer     │
│  Payment Intent │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Checkout     │
│  - Card Input   │
│  - Validation   │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Processing    │
│  - Auth         │
│  - Capture      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Confirmation  │
│  - Receipt      │
│  - Webhook      │
└─────────────────┘
```

### 2. Webhook Events

```yaml
webhook_handlers:
  payment_intent.succeeded:
    actions:
      - fulfill_order
      - send_receipt
      - update_crm
      
  payment_intent.payment_failed:
    actions:
      - notify_customer
      - retry_payment
      - log_failure
      
  customer.subscription.created:
    actions:
      - provision_access
      - send_welcome_email
      - update_metrics
      
  customer.subscription.deleted:
    actions:
      - revoke_access
      - send_offboarding_email
      - trigger_retention_flow
      
  invoice.payment_failed:
    actions:
      - send_dunning_email
      - update_subscription_status
      - create_support_ticket
```

## Subscription Management

### Plan Configuration

```yaml
subscription_plans:
  - name: Starter
    id: plan_starter
    price: 29
    currency: usd
    interval: month
    features:
      - "5 users"
      - "10GB storage"
      - "Email support"
    metadata:
      tier: 1
      
  - name: Growth
    id: plan_growth
    price: 79
    currency: usd
    interval: month
    features:
      - "25 users"
      - "100GB storage"
      - "Priority support"
    metadata:
      tier: 2
      
  - name: Enterprise
    id: plan_enterprise
    price: custom
    interval: month
    features:
      - "Unlimited users"
      - "Unlimited storage"
      - "24/7 support"
      - "Custom integrations"
    metadata:
      tier: 3
```

### Subscription Lifecycle

```yaml
subscription_automation:
  on_create:
    - provision_service
    - send_welcome_email
    - create_customer_record
    - schedule_onboarding_call
    
  on_upgrade:
    - adjust_limits
    - prorate_billing
    - send_upgrade_confirmation
    - unlock_features
    
  on_downgrade:
    - schedule_limit_reduction
    - send_downgrade_notice
    - offer_retention_discount
    
  on_cancel:
    - schedule_access_revocation
    - send_exit_survey
    - trigger_win_back_campaign
    
  on_renewal:
    - send_renewal_receipt
    - update_usage_quotas
    - check_plan_eligibility
```

## Invoice Management

### Invoice Automation

```yaml
invoice_settings:
  defaults:
    auto_advance: true
    collection_method: charge_automatically
    days_until_due: 30
    
  templates:
    header:
      company_name: "{{company}}"
      logo: "{{logo_url}}"
      
    footer:
      payment_terms: "Net 30"
      thank_you: "Thank you for your business!"
      
  automation:
    - event: invoice.created
      actions:
        - add_line_items
        - apply_discounts
        - calculate_tax
        
    - event: invoice.finalized
      actions:
        - send_to_customer
        - log_to_accounting
        
    - event: invoice.paid
      actions:
        - send_receipt
        - update_revenue
```

### Dunning Management

```yaml
dunning_sequence:
  - day: 0
    event: payment_failed
    actions:
      - retry_payment
      - email_template: payment_failed_1
      
  - day: 3
    actions:
      - retry_payment
      - email_template: payment_failed_2
      - sms_reminder
      
  - day: 7
    actions:
      - retry_payment
      - email_template: payment_failed_3
      - mark_at_risk
      
  - day: 14
    actions:
      - final_retry
      - email_template: final_notice
      - pause_subscription
      
  - day: 30
    actions:
      - cancel_subscription
      - email_template: cancellation
      - revoke_access
```

## Checkout Integration

### Checkout Session

```javascript
// Create Checkout Session
const session = await stripe.checkout.sessions.create({
  mode: 'subscription',
  payment_method_types: ['card'],
  line_items: [{
    price: 'price_xxx',
    quantity: 1,
  }],
  success_url: 'https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url: 'https://example.com/cancel',
  customer_email: 'customer@example.com',
  subscription_data: {
    trial_period_days: 14,
    metadata: {
      plan_tier: 'growth'
    }
  },
  allow_promotion_codes: true,
});
```

### Payment Elements

```javascript
// Create Payment Intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,
  currency: 'usd',
  customer: 'cus_xxx',
  payment_method_types: ['card'],
  metadata: {
    order_id: '12345'
  }
});

// Confirm Payment
const result = await stripe.confirmCardPayment(
  paymentIntent.client_secret,
  {
    payment_method: {
      card: cardElement,
      billing_details: {
        name: 'John Doe'
      }
    }
  }
);
```

## Revenue Analytics

### Dashboard Metrics

```
STRIPE REVENUE DASHBOARD
═══════════════════════════════════════

MRR:          $125,450 (+8.5%)
ARR:          $1,505,400
New MRR:      $12,340
Churned MRR:  $4,120
Net MRR:      +$8,220

SUBSCRIPTION BREAKDOWN:
Active:       892
Trialing:     156
Past Due:     23
Cancelled:    45 (this month)

BY PLAN:
Starter    ████████░░░░░░░░ 45%  │ $28,500
Growth     ██████████░░░░░░ 38%  │ $47,600
Enterprise ██████░░░░░░░░░░ 17%  │ $49,350

CHURN ANALYSIS:
Monthly Churn Rate:  4.2%
MRR Churn:          $4,120
Reasons:
- Price             ████████░░░░ 35%
- Competitor        ██████░░░░░░ 25%
- No longer needed  ████░░░░░░░░ 20%
- Support issues    ███░░░░░░░░░ 12%
- Other             ██░░░░░░░░░░ 8%
```

### Cohort Analysis

```yaml
cohort_metrics:
  - cohort: "2024-01"
    customers: 150
    month_1_retention: 95%
    month_3_retention: 82%
    month_6_retention: 71%
    ltv_estimate: $890
    
  - cohort: "2024-02"
    customers: 180
    month_1_retention: 93%
    month_3_retention: 79%
    ltv_estimate: $820
```

## Fraud Prevention

### Risk Rules

```yaml
radar_rules:
  - name: block_high_risk
    condition: "risk_level = 'highest'"
    action: block
    
  - name: review_elevated_risk
    condition: "risk_level = 'elevated'"
    action: review
    
  - name: block_disposable_email
    condition: "email_domain in @disposable_domains"
    action: block
    
  - name: velocity_check
    condition: "card_country != ip_country"
    action: review
    
  - name: amount_threshold
    condition: "amount > 100000"  # $1000
    action: review
```

## Customer Portal

### Portal Configuration

```yaml
customer_portal:
  features:
    subscription_update:
      enabled: true
      products:
        - product_starter
        - product_growth
        - product_enterprise
      proration_behavior: create_prorations
      
    subscription_cancel:
      enabled: true
      mode: at_period_end
      cancellation_reason:
        enabled: true
        options:
          - "Too expensive"
          - "Missing features"
          - "Switched to competitor"
          - "No longer needed"
          - "Other"
          
    payment_method_update:
      enabled: true
      
    invoice_history:
      enabled: true
      
  branding:
    colors:
      primary: "#5469d4"
    icon: "{{company_icon}}"
```

## Reporting Automation

### Scheduled Reports

```yaml
reports:
  - name: daily_revenue
    schedule: "0 9 * * *"
    metrics:
      - gross_volume
      - net_volume
      - new_customers
      - failed_payments
    destination: slack_finance
    
  - name: weekly_mrr
    schedule: "0 9 * * 1"
    metrics:
      - mrr
      - arr
      - churn_rate
      - expansion_revenue
    destination: email_leadership
    
  - name: monthly_reconciliation
    schedule: "0 9 1 * *"
    metrics:
      - total_revenue
      - fees
      - refunds
      - payouts
    destination: accounting_system
```

## API Examples

### Common Operations

```javascript
// Create Customer
const customer = await stripe.customers.create({
  email: 'customer@example.com',
  name: 'John Doe',
  metadata: {
    user_id: '12345'
  }
});

// Create Subscription
const subscription = await stripe.subscriptions.create({
  customer: customer.id,
  items: [{ price: 'price_xxx' }],
  trial_period_days: 14,
  payment_behavior: 'default_incomplete',
  expand: ['latest_invoice.payment_intent']
});

// Update Subscription
await stripe.subscriptions.update(subscription.id, {
  items: [{
    id: subscription.items.data[0].id,
    price: 'price_new_xxx'
  }],
  proration_behavior: 'create_prorations'
});

// Issue Refund
const refund = await stripe.refunds.create({
  payment_intent: 'pi_xxx',
  amount: 1000  // Partial refund
});
```

## Best Practices

1. **Use Webhooks**: Don't rely on redirect alone
2. **Idempotency Keys**: Prevent duplicate charges
3. **Error Handling**: Graceful failure recovery
4. **PCI Compliance**: Use Stripe Elements
5. **Test Mode**: Validate before production
6. **Monitor Disputes**: Respond promptly
7. **Dunning Strategy**: Recover failed payments
8. **Revenue Recognition**: Track MRR properly
