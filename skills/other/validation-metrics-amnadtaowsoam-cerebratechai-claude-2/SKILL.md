---
name: Validation Metrics
description: Comprehensive guide to choosing and tracking validation metrics that prove product-market fit and drive actionable insights
---

# Validation Metrics

## What are Validation Metrics?

**Definition:** Quantifiable proof that your hypothesis is correct and your product is working.

### Characteristics

1. **Tied to Hypothesis**
   - Directly measures what you're testing
   - Example: Hypothesis says "increase signups by 30%" → Metric is signup rate

2. **Actionable**
   - Can optimize based on metric
   - Shows what to improve
   - Example: "30% activation rate" → Focus on onboarding

3. **Leading Indicators**
   - Predict future success
   - Faster feedback than lagging indicators
   - Example: Activation rate → Predicts retention

4. **Measurable**
   - Can track with current tools
   - Quantifiable (not subjective)
   - Example: "% of users who complete first project" (measurable) vs "users are happy" (not measurable)

---

## Validation vs Vanity Metrics

### Vanity Metrics (Look Good, Not Actionable)

**Examples:**
- **Total signups:** 1 million signups
  - Problem: Doesn't show engagement or retention
  - Could be 1M inactive users

- **Page views:** 10 million page views
  - Problem: Doesn't show value delivered
  - Could be bots or bounces

- **Social media followers:** 100k followers
  - Problem: Doesn't show business impact
  - Could be fake/inactive followers

**Why They're Vanity:**
- Impressive numbers
- Don't drive decisions
- Don't correlate with business success

### Validation Metrics (Actionable, Meaningful)

**Examples:**
- **Active users:** 30% of signups are active weekly
  - Actionable: Focus on activation
  - Shows: Real engagement

- **Retention:** 60% of users return after 7 days
  - Actionable: Improve onboarding
  - Shows: Product stickiness

- **Revenue per user:** $50 average revenue per user
  - Actionable: Optimize pricing/upsells
  - Shows: Monetization effectiveness

**Why They're Validation:**
- Show real user behavior
- Drive product decisions
- Correlate with business success

### Comparison Table

| Vanity Metric | Validation Metric |
|---------------|-------------------|
| Total signups | % of signups who activate |
| Page views | Time spent per session |
| Email subscribers | Email open/click rate |
| App downloads | DAU / MAU ratio |
| Social followers | Engagement rate |

---

## Choosing Validation Metrics

### 1. Tied Directly to Hypothesis

**Hypothesis:**
> "If we add social login, signup completion will increase by 30%."

**Validation Metric:**
- Signup completion rate
- % using social login vs email/password

**Why:** Directly measures hypothesis outcome.

### 2. Measurable with Current Tools

**Good (Measurable):**
- Signup completion rate (track with analytics)
- Time to first action (track with events)
- Retention rate (track with cohorts)

**Bad (Hard to Measure):**
- User happiness (subjective, requires surveys)
- Brand awareness (requires expensive studies)
- "Quality" of users (vague, undefined)

### 3. Leading (Predict Future Success)

**Leading Indicators:**
- Activation rate → Predicts retention
- Engagement (DAU/MAU) → Predicts churn
- NPS score → Predicts growth

**Lagging Indicators:**
- Revenue (delayed, many factors)
- Churn (happens after problem)
- LTV (takes months to measure)

**Why Leading is Better:**
- Faster feedback
- Can fix issues before they become problems
- Iterate faster

### 4. Actionable (Can Optimize)

**Actionable:**
- "30% of users complete onboarding" → Improve onboarding
- "50% drop off at step 3" → Fix step 3
- "Users spend 2 min/session" → Increase engagement

**Not Actionable:**
- "Users are happy" → What to do?
- "Product is good" → What to improve?
- "Traffic is up" → Why? What next?

---

## Metric Types by Stage

### Problem Validation

**Goal:** Confirm the problem exists

**Metrics:**
- Interview requests (% of outreach that accepts)
- Survey responses (% who respond)
- Problem severity rating (1-10 scale)
- Frequency of problem (daily, weekly, monthly)

**Example:**
- Sent 100 interview requests → 40 accepted (40% response rate)
- 8 out of 10 rated problem as 8+ severity
- **Validation:** Problem is real and severe

### Solution Validation

**Goal:** Confirm solution solves the problem

**Metrics:**
- Prototype interactions (% who engage)
- Waitlist signups (% interested)
- Willingness to pay (% who say yes)
- Task completion rate (usability tests)

**Example:**
- Showed prototype to 20 users → 18 engaged (90%)
- 15 out of 20 joined waitlist (75%)
- 10 out of 20 said they'd pay $49/month (50%)
- **Validation:** Solution is valuable

### MVP Validation

**Goal:** Confirm product delivers value

**Metrics:**
- Activation rate (% who complete key action)
- Retention rate (% who return)
- Revenue (% who pay)
- NPS (net promoter score)

**Example:**
- 100 signups → 40 activated (40% activation)
- 40 activated → 28 retained after 7 days (70% retention)
- 28 retained → 12 paid (43% conversion)
- **Validation:** Product has product-market fit

### Growth

**Goal:** Scale the product

**Metrics:**
- DAU, WAU, MAU (daily/weekly/monthly active users)
- Churn rate (% who leave)
- Virality (K-factor, viral coefficient)
- CAC (customer acquisition cost)
- LTV (lifetime value)

**Example:**
- 10,000 MAU, growing 10% MoM
- 5% monthly churn
- K-factor: 1.2 (viral growth)
- CAC: $50, LTV: $500 (10x LTV/CAC)
- **Validation:** Product is scaling

---

## AARRR Metrics (Pirate Metrics)

### 1. Acquisition: Where Users Come From

**Metrics:**
- Traffic sources (organic, paid, referral)
- Signup rate (% of visitors who sign up)
- Cost per acquisition (CPA)

**Example:**
- 10,000 visitors → 500 signups (5% signup rate)
- Sources: 40% organic, 30% paid, 30% referral
- CPA: $20 (paid), $0 (organic)

**Optimization:**
- Improve signup rate (test landing page)
- Increase organic traffic (SEO, content)
- Reduce CPA (optimize ads)

### 2. Activation: First Experience, Aha Moment

**Metrics:**
- Activation rate (% who complete key action)
- Time to first value
- Onboarding completion rate

**Example:**
- 500 signups → 200 activated (40% activation)
- Activation = Complete first project
- Time to activation: 15 minutes (median)

**Optimization:**
- Improve onboarding (reduce time to activation)
- Increase activation rate (test different flows)
- Identify "aha moment" (what makes users stick)

### 3. Retention: Come Back and Use Regularly

**Metrics:**
- Day 1, 7, 30 retention
- DAU / MAU ratio (stickiness)
- Churn rate

**Example:**
- Day 1 retention: 60%
- Day 7 retention: 40%
- Day 30 retention: 25%
- DAU/MAU: 0.3 (30% of monthly users are daily active)

**Optimization:**
- Improve Day 7 retention (email reminders, push notifications)
- Increase stickiness (make product more valuable)
- Reduce churn (identify why users leave)

### 4. Referral: Tell Others

**Metrics:**
- Viral coefficient (K-factor)
- Referral rate (% who refer)
- Invites sent per user

**Example:**
- 100 users → 30 sent invites (30% referral rate)
- 30 invites → 15 signups (50% conversion)
- K-factor: 0.3 × 0.5 = 0.15 (not viral, need >1)

**Optimization:**
- Increase referral rate (add referral program)
- Increase invite conversion (improve invite messaging)
- Achieve K > 1 (viral growth)

### 5. Revenue: Pay for Product

**Metrics:**
- Conversion rate (% who pay)
- ARPU (average revenue per user)
- MRR (monthly recurring revenue)
- Churn rate (revenue churn)

**Example:**
- 200 active users → 50 paid (25% conversion)
- ARPU: $30/month
- MRR: 50 × $30 = $1,500
- Revenue churn: 5%/month

**Optimization:**
- Increase conversion rate (test pricing, features)
- Increase ARPU (upsells, higher tiers)
- Reduce churn (improve retention)

---

## North Star Metric

### What is a North Star Metric?

**Definition:** The single most important metric that aligns with value delivered to users.

**Characteristics:**
- Measures value delivered (not vanity)
- Leading indicator of growth
- Aligns team around one goal
- Actionable (can optimize)

### Examples from Successful Products

| Product | North Star Metric | Why |
|---------|-------------------|-----|
| **Airbnb** | Nights booked | Measures core value (stays) |
| **Slack** | Messages sent | Measures engagement |
| **LinkedIn** | Endorsements | Measures network value |
| **Spotify** | Time listening | Measures content consumption |
| **Uber** | Rides completed | Measures core transaction |
| **Medium** | Total time reading | Measures content engagement |

### How to Choose Your North Star

**Questions:**
1. What value do we deliver to users?
2. What action shows they're getting value?
3. What predicts long-term retention?
4. What can we optimize?

**Example: Project Management Tool**

**Options:**
- Projects created (vanity, doesn't show usage)
- Tasks completed (better, shows value)
- Active projects (even better, shows ongoing usage)

**North Star:** Active projects (projects with activity in last 7 days)

**Why:**
- Shows users are getting value (managing projects)
- Predicts retention (active users stay)
- Actionable (can optimize for more active projects)

---

## Input vs Output Metrics

### Input Metrics (What We Control)

**Examples:**
- Features shipped
- Experiments run
- Marketing campaigns launched
- Sales calls made

**Why They Matter:**
- Show team activity
- Measure effort

**Why They're Not Enough:**
- Don't show outcomes
- Can ship features that don't work
- Activity ≠ Results

### Output Metrics (What Users Do)

**Examples:**
- Signups
- Activation rate
- Retention rate
- Revenue

**Why They Matter:**
- Show real impact
- Measure results
- Drive business outcomes

**Why Focus on Outputs:**
- Outputs are what matter
- Inputs are means to outputs
- Can have high input, low output (shipping features no one uses)

### Example

**Input Metrics:**
- Shipped 10 features this quarter ✅
- Ran 5 A/B tests ✅
- Launched 3 marketing campaigns ✅

**Output Metrics:**
- Signups: Flat (0% growth) ❌
- Activation: Decreased from 40% to 35% ❌
- Retention: Flat ❌

**Learning:** High activity (inputs) but no results (outputs). Need to focus on what moves the needle.

---

## Leading vs Lagging Indicators

### Leading Indicators (Predict Future)

**Examples:**
- Activation rate → Predicts retention
- Engagement (DAU/MAU) → Predicts churn
- NPS score → Predicts growth
- Trial conversion rate → Predicts revenue

**Benefits:**
- Faster feedback
- Can fix issues early
- Iterate faster

**Example:**
- Activation rate drops from 40% to 30%
- **Action:** Fix onboarding immediately (before retention drops)

### Lagging Indicators (Measure Past)

**Examples:**
- Revenue (delayed, many factors)
- Churn (happens after problem)
- LTV (takes months to measure)
- Market share (slow to change)

**Drawbacks:**
- Slow feedback
- Problem already happened
- Hard to iterate

**Example:**
- Revenue drops 20%
- **Problem:** Issue happened weeks/months ago
- **Action:** Too late to prevent, can only fix going forward

### Use Both

**Leading:** For fast iteration
**Lagging:** For business outcomes

**Example:**
- **Leading:** Activation rate (optimize weekly)
- **Lagging:** Revenue (measure monthly)
- **Relationship:** Activation rate predicts revenue

---

## Metrics for Different Product Types

### SaaS (Software as a Service)

**Key Metrics:**
- MRR (monthly recurring revenue)
- Churn rate (% who cancel)
- NPS (net promoter score)
- Activation rate (% who complete onboarding)
- CAC (customer acquisition cost)
- LTV (lifetime value)

**Example:**
- MRR: $100k, growing 15% MoM
- Churn: 5%/month
- NPS: 50
- Activation: 40%
- CAC: $200, LTV: $2,000 (10x)

### E-Commerce

**Key Metrics:**
- Cart abandonment rate
- Conversion rate (% who buy)
- AOV (average order value)
- Repeat purchase rate
- CAC (customer acquisition cost)
- LTV (lifetime value)

**Example:**
- Cart abandonment: 70%
- Conversion: 2.5%
- AOV: $75
- Repeat purchase: 30%
- CAC: $30, LTV: $200 (6.7x)

### Marketplace (Two-Sided)

**Key Metrics:**
- Supply/demand balance
- GMV (gross merchandise value)
- Take rate (% commission)
- Liquidity (% of listings that transact)
- Repeat rate (buyers and sellers)

**Example:**
- Supply: 10,000 sellers
- Demand: 50,000 buyers (5:1 ratio)
- GMV: $1M/month
- Take rate: 15%
- Liquidity: 60% (listings sell within 30 days)

### Social / Community

**Key Metrics:**
- DAU / MAU (daily/monthly active users)
- Posts per user
- Connections per user
- Engagement rate (likes, comments, shares)
- Retention (Day 1, 7, 30)

**Example:**
- DAU: 100k, MAU: 500k (DAU/MAU: 0.2)
- Posts per user: 5/month
- Connections: 50/user
- Engagement: 10% (% of posts with engagement)
- Day 7 retention: 40%

---

## Setting Metric Targets

### 1. Baseline (Current State)

**Measure:**
- What's the current value?
- What's the trend? (improving, flat, declining)

**Example:**
- Current activation rate: 30%
- Trend: Flat (been 30% for 3 months)

### 2. Target (Desired State)

**Set:**
- What's a meaningful improvement?
- What's achievable?
- What's the industry benchmark?

**Example:**
- Target activation rate: 40%
- Improvement: +33% relative
- Benchmark: Top quartile is 45%

### 3. Time Frame (By When)

**Set:**
- How long to achieve target?
- Consider: Effort required, traffic volume, test duration

**Example:**
- Achieve 40% activation in 8 weeks
- Plan: 2 weeks per experiment, 4 experiments

### Full Example

**Metric:** Activation rate

**Baseline:** 30% (current)

**Target:** 40% (desired)

**Time Frame:** 8 weeks

**Full Statement:**
> "Increase activation rate from 30% to 40% within 8 weeks."

---

## Metric Instrumentation

### 1. Event Tracking (Segment, Amplitude, Mixpanel)

**What to Track:**
- User actions (clicks, page views, form submissions)
- Key events (signup, activation, purchase)
- User properties (plan, signup date, source)

**Example (Segment):**
```javascript
// Track signup
analytics.track('User Signed Up', {
  method: 'email', // or 'google', 'facebook'
  plan: 'free',
  source: 'organic'
});

// Track activation
analytics.track('User Activated', {
  time_to_activation: 900, // seconds
  completed_steps: 5
});

// Identify user
analytics.identify(userId, {
  email: user.email,
  plan: 'free',
  signup_date: '2024-01-15',
  source: 'organic'
});
```

### 2. Custom Events (User Actions)

**Event Naming Convention:**
```
[Object] [Action]

Examples:
- User Signed Up
- Project Created
- Task Completed
- Payment Submitted
- Feature Used
```

**Event Properties:**
```javascript
analytics.track('Project Created', {
  project_id: '123',
  project_name: 'My Project',
  template_used: true,
  team_size: 5
});
```

### 3. User Properties (Attributes)

**What to Track:**
- Demographics (age, location, role)
- Behavioral (signup date, plan, usage)
- Firmographic (company size, industry) for B2B

**Example:**
```javascript
analytics.identify(userId, {
  email: 'user@example.com',
  name: 'John Doe',
  plan: 'pro',
  signup_date: '2024-01-15',
  company_size: '50-100',
  industry: 'SaaS',
  role: 'Product Manager'
});
```

### 4. Conversion Funnels

**Define Funnel:**
```
Signup Funnel:
1. Visit landing page
2. Click "Sign Up"
3. Enter email
4. Verify email
5. Complete onboarding
6. Activate (complete first project)
```

**Track Each Step:**
```javascript
// Step 1
analytics.page('Landing Page');

// Step 2
analytics.track('Signup Button Clicked');

// Step 3
analytics.track('Email Entered');

// Step 4
analytics.track('Email Verified');

// Step 5
analytics.track('Onboarding Completed');

// Step 6
analytics.track('User Activated');
```

**Analyze:**
- Conversion rate at each step
- Drop-off points
- Time between steps

---

## Cohort Analysis

### What is Cohort Analysis?

**Definition:** Group users by time (signup week/month) and track behavior over time.

**Why:**
- See if product is improving (newer cohorts better than older)
- Identify retention patterns
- Measure long-term impact of changes

### Example: Retention Cohort

**Cohort Table:**

| Signup Week | Week 0 | Week 1 | Week 2 | Week 3 | Week 4 |
|-------------|--------|--------|--------|--------|--------|
| Jan 1-7 | 100% | 60% | 45% | 35% | 30% |
| Jan 8-14 | 100% | 65% | 50% | 40% | 35% |
| Jan 15-21 | 100% | 70% | 55% | 45% | 40% |
| Jan 22-28 | 100% | 75% | 60% | 50% | 45% |

**Analysis:**
- Retention is improving (newer cohorts have higher retention)
- Week 1 retention increased from 60% to 75%
- **Learning:** Recent product changes are working

### Example: Revenue Cohort

**Cohort Table:**

| Signup Month | Month 0 | Month 1 | Month 2 | Month 3 |
|--------------|---------|---------|---------|---------|
| Jan | $1,000 | $1,200 | $1,400 | $1,500 |
| Feb | $1,500 | $1,800 | $2,000 | - |
| Mar | $2,000 | $2,400 | - | - |

**Analysis:**
- Revenue per cohort is growing (expansion revenue)
- Newer cohorts start with higher revenue
- **Learning:** Pricing changes are working

---

## Segmentation

### Why Segment?

**Problem:**
- Averages hide insights
- Different user types behave differently
- One-size-fits-all doesn't work

**Solution:**
- Segment by user type
- Analyze each segment separately
- Optimize for each segment

### Common Segments

**1. By User Type:**
- Free vs Paid
- New vs Returning
- Power users vs Casual users

**2. By Channel:**
- Organic vs Paid
- Direct vs Referral
- Email vs Social

**3. By Feature Usage:**
- Uses Feature A vs Doesn't use Feature A
- High engagement vs Low engagement

### Example: Activation by User Type

**Overall:**
- Activation rate: 40%

**Segmented:**
- Free users: 35% activation
- Paid users: 60% activation

**Learning:** Paid users activate at higher rate. Focus on converting free to paid.

### Example: Retention by Channel

**Overall:**
- Day 7 retention: 40%

**Segmented:**
- Organic: 50% retention
- Paid: 30% retention
- Referral: 60% retention

**Learning:** Referral users have best retention. Invest in referral program.

---

## Metric Dashboards

### Key Metrics Visible at All Times

**Dashboard Structure:**
```
┌─────────────────────────────────────────────────┐
│ NORTH STAR METRIC                               │
│ Active Projects: 1,234 (+15% vs last week)      │
├─────────────────────────────────────────────────┤
│ AARRR METRICS                                   │
│ Acquisition: 500 signups (+10%)                 │
│ Activation: 40% (+5%)                           │
│ Retention: 60% Day 7 (flat)                     │
│ Referral: 0.3 K-factor (-10%)                   │
│ Revenue: $10k MRR (+20%)                        │
├─────────────────────────────────────────────────┤
│ KEY FUNNELS                                     │
│ Signup Funnel: 5% conversion (flat)             │
│ Onboarding Funnel: 40% completion (+5%)         │
│ Payment Funnel: 25% conversion (+10%)           │
└─────────────────────────────────────────────────┘
```

### Daily/Weekly/Monthly Views

**Daily:**
- DAU (daily active users)
- Signups
- Revenue

**Weekly:**
- WAU (weekly active users)
- Retention (Day 7)
- Activation rate

**Monthly:**
- MAU (monthly active users)
- MRR (monthly recurring revenue)
- Churn rate

### Trends and Anomalies

**Trend:**
- Is metric improving, flat, or declining?
- What's the rate of change?

**Anomaly:**
- Sudden spike or drop
- Investigate cause

**Example:**
- Signups spiked 300% on Tuesday
- **Investigation:** Press mention on TechCrunch
- **Action:** Prepare for increased traffic

### Segmented Views

**Example:**
- Overall activation: 40%
- By plan:
  - Free: 35%
  - Pro: 60%
  - Enterprise: 80%

**Learning:** Enterprise users activate at much higher rate.

---

## Common Metric Mistakes

### 1. Tracking Too Many Metrics

**Problem:**
- 50 metrics on dashboard
- Can't focus
- Analysis paralysis

**Solution:**
- Focus on 3-5 key metrics
- North Star + AARRR

**Example:**
- North Star: Active projects
- Acquisition: Signups
- Activation: % who complete first project
- Retention: Day 7 retention
- Revenue: MRR

### 2. Vanity Metrics

**Problem:**
- Tracking metrics that look good but don't matter
- Example: Total signups (not active users)

**Solution:**
- Track actionable metrics
- Example: % of signups who are active

### 3. Metrics Without Targets

**Problem:**
- "Activation rate is 40%"
- Is that good or bad?

**Solution:**
- Set targets
- Example: "Activation rate is 40%, target is 50%"

### 4. Not Segmenting

**Problem:**
- Averages hide insights
- Example: "Overall retention is 40%"
- Reality: Free users 30%, Paid users 60%

**Solution:**
- Segment by user type, channel, feature usage
- Analyze each segment

---

## From Metrics to Action

### Metric Drops → Investigate

**Example:**
- Activation rate dropped from 40% to 30%

**Actions:**
1. When did it drop? (identify timing)
2. What changed? (recent deployments, experiments)
3. Which segment? (all users or specific segment)
4. Funnel analysis (where are users dropping off?)

**Investigation:**
- Dropped on Jan 15
- Deployed new onboarding flow on Jan 14
- Only affects mobile users
- Users drop off at step 3 (new step added)

**Fix:**
- Revert new onboarding flow
- Redesign step 3
- Re-test

### Metric Flat → Experiment

**Example:**
- Activation rate has been 40% for 3 months

**Actions:**
1. Brainstorm hypotheses (what could improve activation?)
2. Prioritize (ICE score)
3. Run experiments
4. Measure impact

**Hypotheses:**
- Add onboarding checklist → +10% activation
- Send activation email → +5% activation
- Simplify first task → +15% activation

**Experiment:**
- Test onboarding checklist (highest expected impact)
- Run A/B test for 2 weeks
- Measure activation rate

### Metric Improves → Double Down

**Example:**
- Activation rate increased from 40% to 50% after adding onboarding checklist

**Actions:**
1. Validate (is improvement real and sustained?)
2. Understand why (what made it work?)
3. Double down (do more of what works)

**Double Down:**
- Expand checklist to more user types
- Add checklist to other flows (e.g., feature adoption)
- Share learnings with team

---

## Tools

### Amplitude

**Features:**
- Event-based analytics
- Funnel analysis
- Cohort analysis
- Retention analysis
- User segmentation

**Pricing:**
- Free tier: 10M events/month
- Paid: $995+/month

### Mixpanel

**Features:**
- Event tracking
- A/B test analysis
- Retention analysis
- Funnel analysis
- User profiles

**Pricing:**
- Free tier: 100k events/month
- Paid: $25+/month

### PostHog

**Features:**
- Open-source product analytics
- Feature flags
- Session replay
- Heatmaps
- Self-hosted option

**Pricing:**
- Free tier: 1M events/month
- Paid: $0.00031/event

### Segment

**Features:**
- Customer data platform
- Single API for all analytics tools
- Event tracking
- User identification
- Integrations (Amplitude, Mixpanel, etc.)

**Pricing:**
- Free tier: 1,000 visitors/month
- Paid: $120+/month

### Google Analytics

**Features:**
- Web analytics
- Traffic sources
- Page views
- Conversion tracking
- Free

**Limitations:**
- Not event-based (page-based)
- Limited user-level tracking
- Not ideal for SaaS products

---

## Real Metric Examples from Successful Products

### Example 1: Slack

**North Star:** Messages sent

**Why:**
- Measures core value (communication)
- Predicts retention (teams that send 2,000+ messages have 93% retention)

**Key Metrics:**
- DAU / MAU (stickiness)
- Messages per user
- Channels per team
- Integrations used

**Learning:** 2,000 messages became the "activation metric"

### Example 2: Airbnb

**North Star:** Nights booked

**Why:**
- Measures core transaction
- Aligns hosts and guests

**Key Metrics:**
- Booking rate
- Host acceptance rate
- Guest satisfaction
- Repeat booking rate

**Learning:** Photo quality was key driver of bookings

### Example 3: Superhuman

**North Star:** % of users who would be "very disappointed" without product

**Why:**
- Measures product-market fit
- Predicts retention and growth

**Key Metrics:**
- "Very disappointed" percentage (target: >40%)
- NPS score
- Response time (email speed)
- Keyboard shortcuts used

**Learning:** Focused on increasing "very disappointed" from 22% to 58%

### Example 4: Dropbox

**North Star:** Files stored

**Why:**
- Measures value delivered (storage)
- Predicts retention (more files = more locked in)

**Key Metrics:**
- Files uploaded
- Storage used
- Shared folders
- Referrals (viral growth)

**Learning:** Referral program drove massive growth (2x signups)

---

## Summary

### Quick Reference

**Validation vs Vanity:**
- Validation: Actionable, meaningful (e.g., % active users)
- Vanity: Impressive but not actionable (e.g., total signups)

**Choosing Metrics:**
- Tied to hypothesis
- Measurable with current tools
- Leading indicators (predict future)
- Actionable (can optimize)

**Metric Types by Stage:**
- Problem validation: Interview requests, survey responses
- Solution validation: Prototype interactions, waitlist signups
- MVP validation: Activation, retention, revenue
- Growth: DAU, MAU, churn, virality

**AARRR Metrics:**
- Acquisition: Where users come from
- Activation: First experience
- Retention: Come back regularly
- Referral: Tell others
- Revenue: Pay for product

**North Star Metric:**
- Single most important metric
- Aligns with value delivered
- Examples: Airbnb (nights booked), Slack (messages sent)

**Input vs Output:**
- Input: What we control (features shipped)
- Output: What users do (signups, retention)
- Focus on outputs

**Leading vs Lagging:**
- Leading: Predict future (activation → retention)
- Lagging: Measure past (revenue, churn)
- Use leading for fast iteration

**Setting Targets:**
- Baseline (current state)
- Target (desired state)
- Time frame (by when)
- Example: "Increase activation from 30% to 40% in 8 weeks"

**Common Mistakes:**
- Tracking too many metrics
- Vanity metrics
- Metrics without targets
- Not segmenting

**From Metrics to Action:**
- Metric drops → Investigate
- Metric flat → Experiment
- Metric improves → Double down

**Tools:**
- Amplitude, Mixpanel (product analytics)
- PostHog (open-source)
- Segment (customer data platform)
- Google Analytics (web analytics)
