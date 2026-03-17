---
name: product-analytics-integrator
description: Expert guidance for designing event tracking systems, implementing analytics SDKs (PostHog, Mixpanel, GA4, Amplitude), creating semantic event taxonomies, validating instrumentation, building dashboards, and interpreting user behavior metrics. Use when setting up product analytics, designing event tracking, analyzing retention/engagement data, or improving analytics infrastructure.
---

# Product Analytics Integrator

## Overview

This skill provides comprehensive guidance for implementing and optimizing product analytics infrastructure. It covers event tracking design, SDK integration, data governance, dashboard creation, and behavioral analysis using industry-leading tools like PostHog, Mixpanel, Google Analytics 4, and Amplitude.

---

## Core Responsibilities

### 1. Event Tracking Design
- Design semantic event models using Object-Action framework
- Establish naming conventions and taxonomy standards
- Define event properties and user attributes
- Create tracking plans with clear documentation
- Validate event instrumentation completeness

### 2. Analytics SDK Integration
- Integrate PostHog, Mixpanel, GA4, or Amplitude SDKs
- Configure autocapture vs custom event strategies
- Implement privacy-compliant tracking
- Set up cross-platform tracking (web, mobile, backend)
- Validate data flow and event delivery

### 3. Dashboard & Reporting
- Design KPI dashboards for product metrics
- Create funnel analyses for conversion optimization
- Build cohort retention analyses
- Set up automated Slack/email reports
- Implement real-time monitoring for critical events

### 4. Data Interpretation
- Analyze user behavior patterns and trends
- Identify drop-off points in user journeys
- Measure feature adoption and engagement
- Calculate retention curves and churn rates
- Generate actionable insights from metrics

---

## Event Naming Convention Standards

### Object-Action Framework

**Format**: `Object Action` or `Category: Object Action`

**Best Practice**: Use **Title Case** for event names, **snake_case** for properties

**Examples**:
- ✅ `Button Clicked`
- ✅ `Form Submitted`
- ✅ `Product Added`
- ✅ `app: Onboarding Completed`
- ✅ `checkout: Payment Failed`
- ❌ `button_clicked` (wrong casing)
- ❌ `ClickedButton` (wrong order)
- ❌ `User clicked the submit button` (too verbose)

### Category Prefixes

Add context for where events originate:

- `app:` - Main application events
- `site:` - Marketing website events
- `checkout:` - Checkout flow events
- `onboarding:` - User onboarding events
- `settings:` - Account settings events

**Examples**:
```
app: Dashboard Viewed
site: Newsletter Subscribed
checkout: Payment Completed
onboarding: Step Completed
settings: Password Changed
```
### Verb Tense Guidelines

**Recommended**: Past tense (event already happened)

**Examples**:
- ✅ `Product Added` (clear: action completed)
- ✅ `User Signed Up`
- ✅ `Page Viewed`
- ❌ `Product Add` (confusing: incomplete action?)
- ❌ `User Sign Up`

### Property Naming

**Format**: `snake_case` for all event properties

**Best Practices**:
- Descriptive and clear names
- Include units where relevant
- Use consistent data types
- Document expected values

**Examples**:
```javascript
analytics.track('Product Added', {
  product_id: 'prod_123',
  product_name: 'Premium Subscription',
  product_category: 'subscriptions',
  price_usd: 29.99,
  currency: 'USD',
  quantity: 1,
  discount_applied: true,
  discount_code: 'SAVE20'
});
```
### Standard Property Types

**Common Property Patterns**:

```javascript
// Identifiers (suffix with _id)
user_id, session_id, product_id, order_id

// Names (suffix with _name)
product_name, feature_name, campaign_name

// Status/State (suffix with _status or _state)
payment_status, order_status, subscription_state

// Timestamps (suffix with _at)
created_at, completed_at, canceled_at

// Durations (suffix with _seconds or _ms)
session_duration_seconds, load_time_ms

// Counts (suffix with _count)
item_count, retry_count, view_count

// Booleans (prefix with is_ or has_)
is_premium, has_discount, is_mobile

// Categories/Types (suffix with _type or _category)
product_type, event_type, user_category
```

---
## Platform-Specific Implementation

### PostHog Integration

**Best For**: Product-focused teams needing session replay, feature flags, and A/B testing

**Key Features**:
- Autocapture with minimal setup
- Built-in session replay
- Feature flags and experiments
- Self-hosted option for data privacy
- SQL access for custom queries

**Setup Example (JavaScript)**:
```javascript
// Install: npm install posthog-js

import posthog from 'posthog-js'

posthog.init('<project_api_key>', {
  api_host: 'https://us.i.posthog.com',
  defaults: '2025-05-24', // Use latest defaults
  capture_pageview: 'history_change', // For SPAs
  autocapture: true, // Enable autocapture
  session_recording: {
    maskAllInputs: true, // Privacy-first
    maskTextSelector: '.sensitive'
  }
})
```
// Custom event tracking
posthog.capture('Product Added', {
  product_id: 'prod_123',
  product_name: 'Premium Plan',
  price_usd: 29.99
})

// Identify users
posthog.identify('user_123', {
  email: 'user@example.com',
  plan: 'premium',
  signup_date: '2025-01-15'
})
```

**Best Practices**:
- Use autocapture initially, then add custom events for critical actions
- Enable session replay for debugging user issues
- Set up feature flags for gradual rollouts
- Use reverse proxy to avoid ad blockers

### Mixpanel Integration

**Best For**: Deep behavioral analysis with advanced segmentation

**Key Features**:
- Event-driven architecture
- Powerful cohort analysis
- Real-time data updates
- Advanced funnel analysis
- A/B test result analysis
**Setup Example (JavaScript)**:
```javascript
// Install: npm install mixpanel-browser

import mixpanel from 'mixpanel-browser'

mixpanel.init('<project_token>', {
  track_pageview: true,
  persistence: 'localStorage'
})

// Track events
mixpanel.track('Product Added', {
  product_id: 'prod_123',
  product_name: 'Premium Plan',
  product_category: 'subscriptions',
  price_usd: 29.99
})

// Identify users
mixpanel.identify('user_123')
mixpanel.people.set({
  '$email': 'user@example.com',
  '$name': 'John Doe',
  'plan': 'premium',
  'signup_date': '2025-01-15'
})

// Track revenue
mixpanel.people.track_charge(29.99, {
  '$time': new Date().toISOString(),
  'product_id': 'prod_123'
})
```
**Best Practices**:
- Track user properties for detailed segmentation
- Use Mixpanel's people profiles for user-centric analysis
- Set up custom dashboards for key metrics
- Track revenue events for monetization analysis

### Google Analytics 4 Integration

**Best For**: Marketing-focused teams tracking acquisition and content

**Key Features**:
- Free tier with generous limits
- Deep Google Ads integration
- Predictive metrics (churn, purchase probability)
- Cross-platform tracking (web + app)
- BigQuery export

**Setup Example (JavaScript)**:
```javascript
// Add to <head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>

// Custom event tracking
gtag('event', 'product_added', {
  product_id: 'prod_123',
  product_name: 'Premium Plan',
  product_category: 'subscriptions',
  price: 29.99,
  currency: 'USD'
});
```
**Best Practices**:
- Use Google Tag Manager for flexible tracking
- Set up enhanced ecommerce for online stores
- Configure custom dimensions/metrics for product-specific data
- Enable BigQuery export for advanced analysis

### Amplitude Integration

**Best For**: Enterprise teams needing advanced behavioral analytics

**Key Features**:
- Industry-leading cohort analysis
- Behavioral insights and predictions
- Multi-step funnel analysis
- User journey mapping
- Robust data governance tools

**Setup Example (JavaScript)**:
```javascript
// Install: npm install @amplitude/analytics-browser
import * as amplitude from '@amplitude/analytics-browser'

amplitude.init('<api_key>', {
  defaultTracking: {
    sessions: true,
    pageViews: true,
    formInteractions: true
  }
})

// Track events
amplitude.track('Product Added', {
  product_id: 'prod_123',
  product_name: 'Premium Plan',
  product_category: 'subscriptions',
  price_usd: 29.99
})

// Identify users
amplitude.setUserId('user_123')
amplitude.identify(
  new amplitude.Identify()
    .set('email', 'user@example.com')
    .set('plan', 'premium')
    .set('signup_date', '2025-01-15')
)
```

**Best Practices**:
- Use Amplitude's taxonomy feature for data governance
- Set up retention cohorts to measure feature stickiness
- Create user journey maps for complex flows
- Use Amplitude Data for tracking plan management

---

## Event Tracking Strategy

### Autocapture vs Custom Events

**Autocapture (PostHog, Heap)**:
- ✅ Fast setup with zero code
- ✅ Retroactive event definition
- ✅ No missing interactions
- ❌ High data volume
- ❌ Noisy/unclear event names
- ❌ Difficult to filter signal from noise

**Custom Events (Mixpanel, Amplitude)**:
- ✅ Clean, intentional data
- ✅ Clear event semantics
- ✅ Lower data volume
- ✅ Business-focused tracking
- ❌ Requires developer implementation
- ❌ Can miss unexpected behaviors
- ❌ Not retroactive

**Recommended Hybrid Approach**:
1. Start with autocapture for quick insights
2. Identify critical user actions
3. Implement custom events for these actions
4. Keep autocapture for exploratory analysis
5. Gradually refine based on insights

### Critical Events to Track

**User Lifecycle**:
- User Signed Up
- Onboarding Completed
- First Action Completed
- Feature Discovered
- Subscription Started
- Subscription Canceled
- Account Deleted

**Product Engagement**:
- Page Viewed
- Feature Used
- Search Performed
- Filter Applied
- Content Created
- Content Shared
- Help Accessed

**Conversion Funnel**:
- Product Viewed
- Product Added to Cart
- Checkout Started
- Payment Information Entered
- Order Completed
- Order Failed

**Feature Adoption**:
- Feature Viewed
- Feature Interaction Started
- Feature Action Completed
- Feature Shared
- Feedback Provided

---

## Dashboard Design Patterns

### 1. Product Health Dashboard

**Metrics**:
- Daily/Weekly/Monthly Active Users (DAU/WAU/MAU)
- User retention curves (D1, D7, D30)
- Feature adoption rates
- Session duration averages
- Crash/error rates

**Recommended Visualizations**:
- Line charts for DAU/WAU/MAU trends
- Retention curves (cohort retention)
- Feature usage heatmap
- Top features by engagement

### 2. Conversion Funnel Dashboard

**Metrics**:
- Funnel conversion rates by stage
- Drop-off points identification
- Time between funnel steps
- Conversion by user segment
- Revenue per conversion

**Recommended Visualizations**:
- Funnel chart with drop-off rates
- Cohort conversion over time
- Segment comparison (A/B testing)

### 3. Engagement Dashboard

**Metrics**:
- Feature engagement frequency
- Power user identification
- Engagement distribution
- Content interaction rates
- Session depth metrics

**Recommended Visualizations**:
- Feature usage matrix
- User engagement distribution
- Session flow diagrams

### 4. Retention Dashboard

**Metrics**:
- N-day retention rates
- Churn prediction
- Feature stickiness
- Activation correlation
- Resurrection rates

**Recommended Visualizations**:
- Retention curves by cohort
- Churn risk segments
- Feature impact on retention

---

## Cohort Analysis Patterns

### Cohort Types

**1. Time-Based Cohorts**:
- Sign-up week/month cohorts
- Feature launch cohorts
- Campaign cohorts
- Seasonal cohorts

**2. Behavioral Cohorts**:
- Power users (>X actions/week)
- Trial users
- Paying customers
- Churned users
- At-risk users

**3. Demographic Cohorts**:
- Geographic segments
- Plan type segments
- Company size segments
- Industry segments

### Cohort Analysis Examples

**Example 1: Feature Adoption by Cohort**
```
Question: Do users who sign up in Q1 2025 adopt Feature X faster than Q4 2024 users?

Setup:
1. Create cohorts by signup quarter
2. Track "Feature X Used" event
3. Measure time-to-feature-adoption
4. Compare adoption curves
```

**Example 2: Retention by Acquisition Channel**
```
Question: Which marketing channel brings the most retained users?

Setup:
1. Create cohorts by utm_source
2. Measure D7, D30, D90 retention
3. Calculate retention curves
4. Identify highest-quality channels
```

**Example 3: Feature Impact on Retention**
```
Question: Does using Feature Y improve 30-day retention?

Setup:
1. Create cohort: Users who used Feature Y in first week
2. Create cohort: Users who did NOT use Feature Y
3. Compare 30-day retention rates
4. Calculate retention lift
```

---

## Data Validation & Quality

### Validation Checklist

**Before Launch**:
- [ ] Events fire on correct user actions
- [ ] Event properties include all required fields
- [ ] Property data types match specification
- [ ] Events fire exactly once (no duplicates)
- [ ] User identification works correctly
- [ ] Cross-platform tracking links properly
- [ ] Privacy compliance (PII masking) verified
- [ ] QA environment tracking separated from production

**Post-Launch Monitoring**:
- [ ] Event volume matches expectations
- [ ] No unexpected spikes/drops in event counts
- [ ] Property value distributions are reasonable
- [ ] No null/undefined values where unexpected
- [ ] Event timestamps are accurate
- [ ] User counts align with known metrics

### Common Data Quality Issues

**Issue 1: Duplicate Events**
```
Symptom: Same event fires multiple times for single action
Root Cause: Multiple SDK initializations, button double-clicks
Fix: Debounce event tracking, ensure single SDK init
```

**Issue 2: Missing Properties**
```
Symptom: Events missing critical properties
Root Cause: Async data loading, undefined variables
Fix: Validate properties exist before tracking, use defaults
```

**Issue 3: Inconsistent Naming**
```
Symptom: Same event with multiple names
Root Cause: No naming convention enforcement
Fix: Implement validation layer, use TypeScript types
```

**Issue 4: PII Leakage**
```
Symptom: Email, phone, or sensitive data in events
Root Cause: Autocapture capturing form inputs
Fix: Mask sensitive fields, use data governance rules
```

### Testing Strategy

**Manual Testing**:
1. Open browser developer tools
2. Trigger user actions
3. Verify events in network tab or analytics debugger
4. Check event properties match specification
5. Test across devices and browsers

**Automated Testing** (Example with Jest):
```javascript
import { render, fireEvent } from '@testing-library/react'
import { trackEvent } from './analytics'

jest.mock('./analytics')

test('tracks Product Added event on button click', () => {
  const { getByText } = render(<AddToCartButton product={mockProduct} />)
  
  fireEvent.click(getByText('Add to Cart'))
  
  expect(trackEvent).toHaveBeenCalledWith('Product Added', {
    product_id: 'prod_123',
    product_name: 'Premium Plan',
    price_usd: 29.99
  })
})
```

---

## Quick Reference: Event Examples

### Authentication Events

```javascript
// Sign Up
track('User Signed Up', {
  signup_method: 'email', // 'google', 'github'
  referral_source: 'organic',
  utm_campaign: 'spring_promo'
})

// Login
track('User Logged In', {
  login_method: 'email',
  is_new_device: true,
  session_id: 'sess_abc123'
})

// Logout
track('User Logged Out', {
  session_duration_seconds: 1847,
  pages_viewed: 12
})
```

### Ecommerce Events

```javascript
// Product View
track('Product Viewed', {
  product_id: 'prod_123',
  product_name: 'Premium Subscription',
  product_category: 'subscriptions',
  price_usd: 29.99,
  referrer: 'search_results'
})

// Add to Cart
track('Product Added', {
  product_id: 'prod_123',
  product_name: 'Premium Subscription',
  price_usd: 29.99,
  quantity: 1,
  cart_value_usd: 29.99,
  cart_item_count: 1
})

// Purchase
track('Order Completed', {
  order_id: 'order_789',
  revenue_usd: 29.99,
  tax_usd: 2.40,
  shipping_usd: 0,
  total_usd: 32.39,
  items: [
    { product_id: 'prod_123', quantity: 1, price_usd: 29.99 }
  ],
  payment_method: 'stripe',
  coupon_code: 'SAVE20'
})
```

### Feature Usage Events

```javascript
// Feature Discovery
track('Feature Discovered', {
  feature_name: 'advanced_filters',
  discovery_method: 'tooltip',
  days_since_signup: 3
})

// Feature Used
track('Feature Used', {
  feature_name: 'advanced_filters',
  usage_count: 1,
  session_id: 'sess_abc123'
})

// Feature Shared
track('Feature Shared', {
  feature_name: 'report_builder',
  share_method: 'email',
  recipient_count: 3
})
```

---

## Resources

### Analytics Platform Documentation
- PostHog: https://posthog.com/docs
- Mixpanel: https://docs.mixpanel.com
- Google Analytics 4: https://support.google.com/analytics
- Amplitude: https://amplitude.com/docs

### Best Practices Guides
- Segment Data Collection: https://segment.com/academy/collecting-data/
- Amplitude Data Taxonomy: https://amplitude.com/docs/data/data-planning-playbook
- PostHog Event Tracking: https://posthog.com/tutorials/event-tracking-guide

---

## Conclusion

Effective product analytics requires:
1. **Clear event taxonomy** with consistent naming
2. **Strategic instrumentation** focused on critical user actions
3. **Robust data validation** to ensure quality
4. **Meaningful dashboards** that drive decisions
5. **Continuous iteration** based on insights

Follow this skill's guidelines to build analytics infrastructure that scales with your product and provides reliable insights for data-driven decisions.
