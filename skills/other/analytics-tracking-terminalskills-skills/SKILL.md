---
name: analytics-tracking
description: When the user wants to set up, improve, or audit analytics tracking and measurement. Also use when the user mentions "set up tracking," "GA4," "Google Analytics," "conversion tracking," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics implementation," or "tracking plan." For A/B test measurement, see ab-test-setup.
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: business
  tags:
    - analytics
    - tracking
    - measurement
---

# Analytics Tracking

## Overview

You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions. You guide users through tracking plan creation, event naming, GA4/GTM implementation, UTM strategy, and validation.

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

## Instructions

### Initial Assessment

Before implementing tracking, understand:

1. **Business Context** - What decisions will this data inform? What are key conversions?
2. **Current State** - What tracking exists? What tools are in use?
3. **Technical Context** - What's the tech stack? Any privacy/compliance requirements?

### Core Principles

1. **Track for Decisions, Not Data** - Every event should inform a decision. Avoid vanity metrics. Quality > quantity.
2. **Start with the Questions** - What do you need to know? What actions will you take? Work backwards to what you need to track.
3. **Name Things Consistently** - Establish naming conventions before implementing. Document everything.
4. **Maintain Data Quality** - Validate implementation. Monitor for issues. Clean data > more data.

### Tracking Plan Framework

```
Event Name | Category | Properties | Trigger | Notes
---------- | -------- | ---------- | ------- | -----
```

**Event Types:**

| Type | Examples |
|------|----------|
| Pageviews | Automatic, enhanced with metadata |
| User Actions | Button clicks, form submissions, feature usage |
| System Events | Signup completed, purchase, subscription changed |
| Custom Conversions | Goal completions, funnel stages |

**For comprehensive event lists**: See [references/event-library.md](references/event-library.md)

### Event Naming Conventions

Use Object-Action format, lowercase with underscores:

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

Be specific: `cta_hero_clicked` not `button_clicked`. Include context in properties, not event name.

### Essential Events

**Marketing Site:**

| Event | Properties |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

**Product/App:**

| Event | Properties |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**For full event library by business type**: See [references/event-library.md](references/event-library.md)

### Standard Event Properties

| Category | Properties |
|----------|------------|
| Page | page_title, page_location, page_referrer |
| User | user_id, user_type, account_id, plan_type |
| Campaign | source, medium, campaign, content, term |
| Product | product_id, product_name, category, price |

### GA4 Implementation

1. Create GA4 property and data stream
2. Install gtag.js or GTM
3. Enable enhanced measurement
4. Configure custom events
5. Mark conversions in Admin

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**For detailed GA4 implementation**: See [references/ga4-implementation.md](references/ga4-implementation.md)

### Google Tag Manager

| Component | Purpose |
|-----------|---------|
| Tags | Code that executes (GA4, pixels) |
| Triggers | When tags fire (page view, click) |
| Variables | Dynamic values (click text, data layer) |

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**For detailed GTM implementation**: See [references/gtm-implementation.md](references/gtm-implementation.md)

### UTM Parameter Strategy

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Traffic source | google, newsletter |
| utm_medium | Marketing medium | cpc, email, social |
| utm_campaign | Campaign name | spring_sale |
| utm_content | Differentiate versions | hero_cta |
| utm_term | Paid search keywords | running+shoes |

Lowercase everything. Use underscores or hyphens consistently. Document all UTMs in a spreadsheet.

### Debugging and Validation

| Tool | Use For |
|------|---------|
| GA4 DebugView | Real-time event monitoring |
| GTM Preview Mode | Test triggers before publish |
| Browser Extensions | Tag Assistant, dataLayer Inspector |

**Validation Checklist:**
- [ ] Events firing on correct triggers
- [ ] Property values populating correctly
- [ ] No duplicate events
- [ ] Works across browsers and mobile
- [ ] Conversions recorded correctly
- [ ] No PII leaking

### Privacy and Compliance

- Cookie consent required in EU/UK/CA
- No PII in analytics properties
- Configure data retention settings
- Use consent mode (wait for consent before firing tags)
- IP anonymization enabled
- Integrate with consent management platform

## Examples

### Example 1: SaaS Marketing Site Tracking Plan

**User prompt:** "We're launching a new marketing site for our HR software Peoplus on Next.js. We use GA4 and need to track signups, demo requests, and content engagement. Help me create a tracking plan."

The agent will:
- Create a structured tracking plan with events: `cta_clicked`, `demo_form_submitted`, `signup_completed`, `pricing_toggled`, `blog_article_read`, `resource_downloaded`.
- Define properties for each event (e.g., `demo_form_submitted` with `company_size`, `source_page`).
- Provide GTM data layer implementation code for each event.
- Recommend custom dimensions for `user_type` and `plan_interest`.
- Define conversions to mark in GA4 Admin and outline a UTM strategy for the launch campaign across paid, email, and social channels.

### Example 2: E-commerce Conversion Funnel Audit

**User prompt:** "Our Shopify store DailyBrew sells specialty coffee. We have GA4 installed but can't see where people drop off between product view and purchase. Our conversion rate is 1.2% and we need better funnel tracking."

The agent will:
- Audit the current GA4 setup and identify missing events in the purchase funnel.
- Create a funnel tracking plan: `product_viewed` (with `product_name`, `price`, `category`), `add_to_cart`, `cart_viewed`, `checkout_started`, `shipping_selected`, `payment_submitted`, `purchase_completed`.
- Provide Shopify-specific GTM implementation using Shopify's data layer.
- Set up enhanced e-commerce tracking in GA4 with proper product properties.
- Recommend a validation process using GA4 DebugView to confirm each funnel step fires correctly.

## Guidelines

- **Always start with questions, not tools** — understand what decisions the data will inform before choosing what to track.
- **Avoid PII in event properties** — never pass emails, full names, or other personally identifiable information as event parameters.
- **Test tracking before going live** — use GA4 DebugView and GTM Preview Mode to verify every event fires correctly with the right properties.
- **Don't duplicate automatic properties** — GA4 already captures page_location, page_referrer, and other standard parameters. Only add custom properties that provide additional context.
- **Document naming conventions upfront** — inconsistent event names (mixing `signupCompleted` with `signup_completed`) create data headaches that are painful to fix later.
- **Keep UTM parameters lowercase and consistent** — `utm_source=Google` and `utm_source=google` create separate entries in reports. Standardize before launching campaigns.
- **Plan for consent** — implement consent mode from day one. Retrofitting cookie consent is much harder than building it in.
