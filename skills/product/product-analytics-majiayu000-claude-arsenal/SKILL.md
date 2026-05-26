---
name: product-analytics
description: Product analytics and growth expert. Use when designing event tracking, defining metrics, running A/B tests, or analyzing retention. Covers AARRR framework, funnel analysis, cohort analysis, and experimentation.
---
# Product Analytics

## Core Principles

- **Metrics over vanity** — Focus on actionable metrics tied to business outcomes
- **Data-driven decisions** — Hypothesize, measure, learn, iterate
- **User-centric measurement** — Track behavior, not just pageviews
- **Statistical rigor** — Understand significance, avoid false positives
- **Privacy-first** — Respect user data, comply with GDPR/CCPA
- **North Star focus** — Align all teams around one key metric

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### No PII in Events

**Events must NEVER contain personally identifiable information.**

```javascript
// ❌ FORBIDDEN: PII in event properties
track('user_signed_up', {
  email: 'user@example.com',     // PII!
  name: 'John Doe',              // PII!
  phone: '+1234567890',          // PII!
  ip_address: '192.168.1.1',     // PII!
  credit_card: '4111...',        // NEVER!
});

// ✅ REQUIRED: Anonymized/hashed identifiers only
track('user_signed_up', {
  user_id: hash('user@example.com'),  // Hashed
  plan: 'pro',
  source: 'organic',
  country: 'US',                       // Broad location OK
});

// Masking utilities
const maskEmail = (email) => {
  const [name, domain] = email.split('@');
  return `${name[0]}***@${domain}`;
};
```

### Object_Action Event Naming

**All event names must follow the object_action snake_case format.**

```javascript
// ❌ FORBIDDEN: Inconsistent naming
track('signup');                    // No object
track('newProject');                // camelCase
track('Upload File');               // Spaces and PascalCase
track('user-created');              // kebab-case
track('BUTTON_CLICKED');            // SCREAMING_CASE

// ✅ REQUIRED: object_action snake_case
track('user_signed_up');
track('project_created');
track('file_uploaded');
track('payment_completed');
track('checkout_started');
```

### Actionable Metrics Only

**Track metrics that drive decisions, not vanity metrics.**

```javascript
// ❌ FORBIDDEN: Vanity metrics without context
track('page_viewed');               // No insight
track('button_clicked');            // Too generic
track('app_opened');                // Doesn't indicate value

// ✅ REQUIRED: Actionable metrics tied to outcomes
track('feature_activated', {
  feature: 'dark_mode',
  time_to_activation_hours: 2.5,
  user_segment: 'power_user',
});

track('checkout_completed', {
  order_value: 99.99,
  items_count: 3,
  payment_method: 'credit_card',
  coupon_applied: true,
});
```

### Statistical Rigor for Experiments

**A/B tests must have proper sample size and significance thresholds.**

```javascript
// ❌ FORBIDDEN: Drawing conclusions too early
// "After 100 users, variant B has 5% higher conversion!"
// This is not statistically significant.

// ✅ REQUIRED: Proper experiment setup
const experimentConfig = {
  name: 'new_checkout_flow',
  hypothesis: 'New flow increases conversion by 10%',

  // Statistical requirements
  significance_level: 0.05,      // 95% confidence
  power: 0.80,                   // 80% power
  minimum_detectable_effect: 0.10, // 10% lift

  // Calculated sample size
  sample_size_per_variant: 3842,

  // Guardrails
  max_duration_days: 14,
  stop_if_degradation: -0.05,    // Stop if 5% worse
};
```

---

## Quick Reference

### When to Use What

| Scenario | Framework/Tool | Key Metric |
|----------|---------------|------------|
| Overall product health | North Star Metric | Time spent listening (Spotify), Nights booked (Airbnb) |
| Growth optimization | AARRR (Pirate Metrics) | Conversion rates per stage |
| Feature validation | A/B Testing | Statistical significance (p < 0.05) |
| User engagement | Cohort Analysis | Day 1/7/30 retention rates |
| Conversion optimization | Funnel Analysis | Drop-off rates per step |
| Feature impact | Attribution Modeling | Multi-touch attribution |
| Experiment success | Statistical Testing | Power, significance, effect size |

---

## North Star Metric

### Definition

A North Star Metric is the **one metric** that best captures the core value your product delivers to customers. When this metric grows sustainably, your business succeeds.

### Characteristics of Good NSMs

```
✓ Captures product value delivery
✓ Correlates with revenue/growth
✓ Measurable and trackable
✓ Movable by product/engineering
✓ Understandable by entire org
✓ Leading (not lagging) indicator
```

### Examples by Company

| Company | North Star Metric | Why It Works |
|---------|------------------|--------------|
| **Spotify** | Time Spent Listening | Core value = music enjoyment |
| **Airbnb** | Nights Booked | Revenue driver + value delivered |
| **Slack** | Daily Active Teams | Engagement = product stickiness |
| **Facebook** | Monthly Active Users | Network effect foundation |
| **Amplitude** | Weekly Learning Users | Value = analytics insights |
| **Dropbox** | Active Users Sharing Files | Core product behavior |

### NSM Framework

```
North Star Metric
       ↓
┌──────┴──────┬──────────┬──────────┐
│             │          │          │
Input 1    Input 2   Input 3   Input 4
(Supporting metrics that drive NSM)

Example: Spotify
NSM: Time Spent Listening
├── Daily Active Users
├── Playlists Created
├── Songs Added to Library
└── Share/Social Actions
```

### How to Define Your NSM

1. **Identify core value proposition**
   - What job does your product do for users?
   - When do users get "aha!" moment?

2. **Find the metric that represents this value**
   - Transaction completed? (e.g., Nights Booked)
   - Time engaged? (e.g., Time Listening)
   - Content created? (e.g., Messages Sent)

3. **Validate it correlates with business success**
   - Does NSM increase → revenue increases?
   - Can product changes move this metric?

4. **Define supporting input metrics**
   - What user behaviors drive NSM?
   - Break into 3-5 key inputs

---

## AARRR Framework (Pirate Metrics)

### Overview

The AARRR framework tracks the customer lifecycle across five stages:

```
ACQUISITION → ACTIVATION → RETENTION → REFERRAL → REVENUE
```

### Stage Definitions

#### 1. Acquisition
**When users discover your product**

**Key Questions:**
- Where do users come from?
- Which channels have best quality users?
- What's the cost per acquisition (CPA)?

**Metrics:**
```
• Website visitors
• App installs
• Sign-ups per channel
• Cost per acquisition (CPA)
• Channel conversion rates
```

**Example Events:**
```javascript
// Landing page view
track('page_viewed', {
  page: 'landing',
  utm_source: 'google',
  utm_medium: 'cpc',
  utm_campaign: 'brand_search'
});

// Sign-up started
track('signup_started', {
  source: 'homepage_cta'
});
```

#### 2. Activation
**When users experience core product value**

**Key Questions:**
- What's the "aha!" moment?
- How long to first value?
- What % reach activation?

**Metrics:**
```
• Time to first action
• Activation rate (% completing key action)
• Setup completion rate
• Feature adoption rate
```

**Example "Aha!" Moments:**
```
Slack:     Send 2,000 messages in team
Twitter:   Follow 30 users
Dropbox:   Upload first file
LinkedIn:  Connect with 5 people
```

**Example Events:**
```javascript
// Activation milestone
track('activated', {
  user_id: 'usr_123',
  activation_action: 'first_project_created',
  time_to_activation_hours: 2.5
});
```

#### 3. Retention
**When users keep coming back**

**Key Questions:**
- What's Day 1/7/30 retention?
- Which cohorts retain best?
- What drives churn?

**Metrics:**
```
• Day 1/7/30 retention rate
• Weekly/Monthly active users (WAU/MAU)
• Churn rate
• Usage frequency
• Feature stickiness (DAU/MAU)
```

**Retention Calculation:**
```
Day X Retention = Users returning on Day X / Total users in cohort

Example:
Cohort: 1000 users signed up Jan 1
Day 7: 300 returned
Day 7 Retention = 300/1000 = 30%
```

**Example Events:**
```javascript
// Daily engagement
track('session_started', {
  user_id: 'usr_123',
  session_count: 42,
  days_since_signup: 15
});
```

#### 4. Referral
**When users recommend your product**

**Key Questions:**
- What's the viral coefficient (K-factor)?
- Which users refer most?
- What referral incentives work?

**Metrics:**
```
• Viral coefficient (K-factor)
• Referral rate (% users referring)
• Invites sent per user
• Invite conversion rate
• Net Promoter Score (NPS)
```

**Viral Coefficient:**
```
K = (% users who refer) × (avg invites per user) × (invite conversion rate)

Example:
K = 0.20 × 5 × 0.30 = 0.30

K > 1: Viral growth (each user brings >1 new user)
K < 1: Need paid acquisition
```

**Example Events:**
```javascript
// Referral actions
track('invite_sent', {
  user_id: 'usr_123',
  channel: 'email',
  recipients: 3
});

track('referral_converted', {
  referrer_id: 'usr_123',
  new_user_id: 'usr_456',
  channel: 'email'
});
```

#### 5. Revenue
**When users generate business value**

**Key Questions:**
- What's customer lifetime value (LTV)?
- What's LTV:CAC ratio?
- Which segments monetize best?

**Metrics:**
```
• Monthly Recurring Revenue (MRR)
• Average Revenue Per User (ARPU)
• Customer Lifetime Value (LTV)
• LTV:CAC ratio
• Conversion to paid
• Revenue churn
```

**LTV Calculation:**
```
LTV = ARPU × Gross Margin / Churn Rate

Example:
ARPU: $50/month
Gross Margin: 80%
Churn: 5%/month

LTV = $50 × 0.80 / 0.05 = $800

Healthy LTV:CAC ratio: 3:1 or higher
```

**Example Events:**
```javascript
// Revenue events
track('subscription_started', {
  user_id: 'usr_123',
  plan: 'pro',
  mrr: 29.99,
  billing_cycle: 'monthly'
});

track('upgrade_completed', {
  user_id: 'usr_123',
  from_plan: 'basic',
  to_plan: 'pro',
  mrr_change: 20.00
});
```

### AARRR Metrics Dashboard

```markdown
## Acquisition
- Total visitors: 50,000
- Sign-ups: 2,500 (5% conversion)
- Top channels: Organic (40%), Paid (30%), Referral (20%)

## Activation
- Activated users: 1,750 (70% of sign-ups)
- Time to activation: 3.2 hours (median)
- Activation funnel drop-off: 30% at setup step 2

## Retention
- Day 1: 60%
- Day 7: 35%
- Day 30: 20%
- Churn: 5%/month

## Referral
- K-factor: 0.4
- Users referring: 15%
- Invites per user: 4.2
- Invite conversion: 25%

## Revenue
- MRR: $125,000
- ARPU: $50
- LTV: $800
- LTV:CAC: 4:1
- Conversion to paid: 25%
```

---


## Extended Reference

Detailed material starting at `## Key Metrics & Formulas` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
