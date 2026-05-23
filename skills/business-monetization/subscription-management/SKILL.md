---
name: subscription-management
description: "SaaS subscription lifecycle management - billing, upgrades, downgrades, churn prevention, and revenue optimization"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: finance
tags:
  - subscription
  - billing
  - saas
  - churn
  - revenue
department: Finance

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4

mcp:
  server: billing-mcp
  tools:
    - stripe_subscription
    - chargebee_api
    - paddle_billing

capabilities:
  - subscription_lifecycle
  - billing_optimization
  - churn_prevention
  - upgrade_paths
  - revenue_recognition

languages:
  - en
  - zh

related_skills:
  - saas-metrics
  - crm-automation
  - email-marketing
---

# Subscription Management

Comprehensive SaaS subscription lifecycle management including billing operations, upgrade/downgrade flows, churn prevention strategies, and revenue optimization.

## Overview

This skill covers:
- Subscription lifecycle management
- Pricing and packaging strategies
- Upgrade/downgrade workflows
- Churn prevention automation
- Billing operations and dunning

---

## Subscription Lifecycle

### Lifecycle Stages

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUBSCRIPTION LIFECYCLE                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Trial ──▶ Conversion ──▶ Active ──▶ Expansion ──▶ Renewal     │
│    │           │            │           │            │          │
│    ▼           ▼            ▼           ▼            ▼          │
│  [Drop]    [Churn]     [Downgrade]  [Churn]     [Churn]        │
│                            │                        │           │
│                            ▼                        ▼           │
│                       [Win-back] ◀──────────── [Win-back]      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Stage Definitions

```yaml
lifecycle_stages:
  trial:
    duration: 14_days
    goal: activation + conversion
    key_metrics:
      - trial_starts
      - activation_rate
      - trial_to_paid_conversion
    automation:
      - onboarding_emails
      - in_app_guidance
      - sales_touch (if qualified)
      
  active:
    goal: value_delivery + expansion
    key_metrics:
      - feature_adoption
      - nps_score
      - expansion_revenue
    automation:
      - health_scoring
      - usage_alerts
      - upsell_triggers
      
  at_risk:
    trigger: health_score < 40 OR usage_drop > 50%
    goal: retention
    key_metrics:
      - save_rate
      - churn_reason
    automation:
      - csm_alert
      - retention_offer
      - executive_escalation
      
  churned:
    goal: win_back
    key_metrics:
      - reactivation_rate
      - time_to_reactivate
    automation:
      - exit_survey
      - win_back_campaigns
      - competitive_monitoring
```

---

## Pricing & Packaging

### Pricing Strategy Template

```yaml
pricing_tiers:
  starter:
    price: $29/month
    billing: monthly or annual (2 months free)
    target: solopreneurs, small teams
    limits:
      users: 5
      storage: 10GB
      features: core_only
    positioning: "Get started"
    
  professional:
    price: $79/month
    billing: monthly or annual
    target: growing teams
    limits:
      users: 25
      storage: 100GB
      features: core + advanced
    positioning: "Most popular"
    highlight: true
    
  business:
    price: $199/month
    billing: monthly or annual
    target: scaling companies
    limits:
      users: unlimited
      storage: 500GB
      features: all + priority_support
    positioning: "For growth"
    
  enterprise:
    price: custom
    billing: annual only
    target: large organizations
    limits:
      users: unlimited
      storage: unlimited
      features: all + sso + api + sla
    positioning: "Contact sales"
    
add_ons:
  - extra_storage: $10/50GB
  - api_access: $50/month
  - priority_support: $100/month
  - dedicated_csm: $500/month
```

### Value Metrics

```yaml
value_metric_options:
  per_seat:
    charge: per_active_user
    pros: predictable, aligns with growth
    cons: may limit adoption
    best_for: collaboration tools
    
  usage_based:
    charge: per_api_call, per_GB, per_transaction
    pros: low barrier, scales with value
    cons: unpredictable revenue
    best_for: infrastructure, APIs
    
  feature_tiered:
    charge: based_on_features_used
    pros: clear upsell path
    cons: may feel restrictive
    best_for: software with distinct use cases
    
  hybrid:
    charge: base_fee + usage_overage
    pros: predictable base + upside
    cons: complex to explain
    best_for: mature products
```

---

## Upgrade/Downgrade Flows

### Upgrade Automation

```yaml
upgrade_triggers:
  usage_based:
    - trigger: approaching_user_limit (80%)
      action:
        - in_app_notification: "You're almost at your limit"
        - email: upgrade_suggestion
        - if_ignored: soft_limit_warning
        
    - trigger: feature_blocked (tried advanced feature)
      action:
        - in_app_modal: feature_preview + upgrade_cta
        - track: feature_interest
        
    - trigger: consistent_overage (3+ months)
      action:
        - csm_outreach: proactive_upgrade_discussion
        
  behavior_based:
    - trigger: power_user_behavior
      condition: >5h/week usage AND >10 team members invited
      action:
        - flag_as: expansion_opportunity
        - assign: csm_for_outreach
        
  time_based:
    - trigger: 90_days_on_same_plan
      action:
        - email: "Are you getting the most out of {Product}?"
        - include: feature_comparison

upgrade_flow:
  steps:
    1. show_comparison: current_vs_recommended
    2. highlight_value: features_they've_tried_to_use
    3. offer_discount: if_annual (optional)
    4. prorate_billing: charge_difference_immediately
    5. unlock_features: immediately
    6. send_confirmation: email + in_app
    7. trigger_onboarding: for_new_features
```

### Downgrade Prevention

```yaml
downgrade_flow:
  steps:
    1. intercept_request:
        show: "Before you go..."
        offer: 
          - pause_subscription: 1-3_months
          - discount: 20%_for_3_months
          - free_month: if_annual
          
    2. collect_reason:
        options:
          - too_expensive
          - not_using_features
          - switching_to_competitor
          - company_downsizing
          - temporary_pause
          
    3. tailored_response:
        too_expensive:
          - offer: lower_tier_suggestion
          - show: cost_per_user_value
          
        not_using_features:
          - offer: training_session
          - show: quick_wins_tutorial
          
        switching_to_competitor:
          - ask: which_competitor
          - offer: competitive_discount
          - flag: for_win_back_later
          
    4. if_proceeds:
        - schedule_downgrade: end_of_billing_cycle
        - preserve_data: for_potential_return
        - send_survey: detailed_feedback
        
    5. track:
        - reason
        - offers_presented
        - offers_accepted/declined
        - revenue_impact
```

---

## Churn Prevention

### Health Scoring

```yaml
customer_health_score:
  components:
    product_usage: 40%
      signals:
        - daily_active_users: vs_licensed_seats
        - feature_adoption: core_features_used
        - login_frequency: weekly_active
        - depth_of_use: actions_per_session
        
    engagement: 30%
      signals:
        - email_opens: last_30_days
        - support_sentiment: positive_vs_negative
        - nps_score: latest
        - community_participation: if_applicable
        
    relationship: 20%
      signals:
        - csm_touchpoints: recent_calls
        - executive_sponsor: identified
        - contract_length: multi_year_bonus
        
    financial: 10%
      signals:
        - payment_history: on_time_payments
        - expansion_history: upgrades_vs_downgrades
        - invoice_disputes: count
        
  scoring:
    90-100: healthy (green)
    70-89: stable (yellow)
    40-69: at_risk (orange)
    0-39: critical (red)
    
  automation:
    critical:
      - immediate: csm_alert + call_scheduled
      - if_no_response: manager_escalation
      
    at_risk:
      - same_day: csm_notification
      - action: health_check_call
      
    stable:
      - weekly: review_in_team_meeting
      
    healthy:
      - monthly: expansion_opportunity_review
```

### Dunning Management

```yaml
dunning_sequence:
  payment_failed:
    day_0:
      - retry_payment: automatic
      - email: "Payment failed - please update"
      - in_app: banner_notification
      
    day_3:
      - retry_payment: automatic
      - email: "Action needed: Update payment"
      - include: direct_update_link
      
    day_7:
      - retry_payment: automatic
      - email: "Your account is at risk"
      - sms: if_enabled
      - downgrade_warning: true
      
    day_14:
      - final_retry: automatic
      - email: "Final notice before suspension"
      - csm_call: for_high_value_accounts
      
    day_21:
      - suspend_account: read_only_access
      - email: "Account suspended"
      - preserve_data: 90_days
      
    day_90:
      - delete_data: after_warning
      - final_email: account_closure
      
  recovery_metrics:
    track:
      - involuntary_churn_rate
      - recovery_rate_by_day
      - avg_days_to_recovery
      - revenue_recovered
```

---

## Revenue Operations

### Billing Automation

```yaml
billing_operations:
  invoice_generation:
    timing: 7_days_before_renewal
    include:
      - usage_summary
      - upcoming_charges
      - payment_method
      
  proration:
    upgrades: charge_immediately (prorated)
    downgrades: credit_at_next_billing
    mid_cycle_changes: calculate_daily
    
  discounts:
    types:
      - percentage: 10%, 20%, 30%
      - fixed: $X off
      - free_months: 1-3 months
    controls:
      - approval_required: >30%
      - expiration: always_set
      - one_per_customer: unless_approved
      
  revenue_recognition:
    method: ratable
    timing: monthly
    deferred_revenue: track_separately
```

### Reporting Dashboard

```markdown
# Subscription Metrics Dashboard

## MRR Summary
| Metric | Value | MoM Change |
|--------|-------|------------|
| Total MRR | $500K | +8% |
| New MRR | $50K | +15% |
| Expansion MRR | $30K | +12% |
| Churn MRR | $20K | -5% |
| Net New MRR | $60K | +20% |

## Subscription Health
| Tier | Customers | MRR | Avg Health |
|------|-----------|-----|------------|
| Enterprise | 50 | $200K | 85 |
| Business | 150 | $180K | 78 |
| Professional | 400 | $100K | 72 |
| Starter | 800 | $20K | 65 |

## At-Risk Accounts (Action Needed)
| Company | MRR | Health | Risk Reason |
|---------|-----|--------|-------------|
| Acme Co | $5K | 35 | Usage drop 60% |
| Tech Inc | $3K | 42 | Payment failed |
| StartupX | $2K | 38 | No login 30 days |

## Churn Analysis
- Voluntary: 1.5% (target: <2%) ✅
- Involuntary: 0.8% (target: <1%) ✅
- Top reason: Price (35%)
- Save rate: 25%
```

---

## Output Example

**Request**: "Create a churn prevention workflow for a SaaS product"

**Output**:

```markdown
# Churn Prevention Workflow

## Early Warning System

### Health Score Triggers

```yaml
triggers:
  critical_alert: # Health < 40
    - immediate: slack_alert_to_csm
    - same_day: schedule_call
    - email: "We noticed you haven't logged in..."
    - offer: free_training_session
    
  usage_drop: # >50% decrease
    - email: "Everything okay?"
    - in_app: help_resources
    - csm_task: check_in_call
    
  support_escalation: # Negative sentiment
    - flag: at_risk
    - csm_notification: with_context
    - executive_apology: if_major_issue
```

## Intervention Playbook

### Scenario: Low Usage

```
Day 1: Automated email
"Hi {name}, we noticed {Product} usage is down. 
Everything okay? Here are 3 quick wins to get value fast:"

Day 3: In-app message
"Need help? Book a free 15-min session with our team."

Day 7: CSM call
Agenda: Understand blockers, offer solutions

Day 14: Manager escalation
If no response, escalate internally
```

### Scenario: Payment Failed

```
Hour 0: Retry payment automatically
Hour 1: Email with update link
Day 3: Second email + SMS
Day 7: CSM call for high-value accounts
Day 14: Final warning
Day 21: Suspend (preserve data 90 days)
```

### Save Offer Matrix

| Churn Reason | Offer |
|--------------|-------|
| Too expensive | 20% off 3 months |
| Not using | Free training + pause option |
| Competitor | Match pricing + migration help |
| Downsizing | Downgrade to lower tier |
| Temporary | Pause 1-3 months free |

## Metrics to Track

- Save rate: Target >25%
- Time to intervention: <24h for critical
- Churn reason distribution
- Offer acceptance rate
- Recovered revenue
```

---

*Subscription Management Skill - Part of Claude Office Skills*
