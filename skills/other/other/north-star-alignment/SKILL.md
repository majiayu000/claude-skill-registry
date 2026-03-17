---
name: north-star-alignment
description: Use when defining success metrics for products or features - connects product metrics to company mission and business model by mapping to North Star metrics (MAU, conversion rate, transactions)
---

# North Star Alignment

## Purpose

Connect product and feature metrics to company-level success by identifying the appropriate North Star metric based on business model type. Ensures every metric ladders up to revenue and strategic goals.

## When to Use This Skill

Activate automatically when:
- Starting any new product initiative and need to define success criteria
- Creating PRDs and need metrics that tie to company goals
- Prioritizing work and need to justify impact on top-line metrics
- `metrics-definition` workflow requires company-level metric alignment
- Evaluating trade-offs between competing priorities
- User asks "how does this tie to company goals?"

**When NOT to use:**
- Metrics are purely operational (deployment frequency, bug counts)
- Working on internal tools with no revenue connection
- Company mission/business model is unknown (gather context first)

## The 5 Business Model Types

Every product metric must correlate with one of these North Star patterns:

### 1. User-Generated Content + Ads
**Examples:** Facebook, Twitter, Reddit, Google, Snapchat, YouTube

**North Star Metrics:**
- **Monthly Active Users (MAU)** - universal gold standard
- **Time on Site (TOS)** - more time = more ads shown = more revenue

**When to use:**
- Company monetizes through advertising
- User attention directly drives revenue
- Content keeps users engaged

### 2. Consumer Freemium
**Examples:** Mobile games, Tinder, Spotify, Dropbox

**North Star Metrics:**
- **MAU** - baseline engagement
- **Free → Paid Conversion Rate** - % of free users upgrading

**Avoid:**
- ARPU/ARPA (PMs can't control pricing directly)

### 3. Enterprise SaaS
**Examples:** Salesforce, Slack, Microsoft 365

**North Star Metrics:**
- **MAU** - product adoption
- **Free → Paid Conversion Rate** - trial to paying customer

**Additional considerations:**
- Seat expansion within accounts
- Feature adoption as leading indicator

### 4. Two-Sided Marketplaces
**Examples:** Uber, Airbnb, eBay, Facebook Marketplace

**North Star Metrics:**
- **MAU for EACH side** separately (riders AND drivers for Uber)
- **Transactions per period** - captures value exchange

**Critical:**
- Measure both sides of the market
- Balance supply and demand metrics

### 5. E-Commerce
**Examples:** Amazon, Shopify stores, Etsy

**North Star Metrics:**
- **MAU** - active shoppers
- **Average Order Value (AOV) / Basket Size** - revenue per transaction

**Revenue model:**
- Take percentage of each transaction
- Larger carts = more revenue

## Mission Statement Integration

North Star metrics are necessary but not sufficient. Also connect to mission:

**Examples:**
- Stripe: "Increase the Internet's GDP" → transaction volume, merchant success
- Google: "Organize world's information" → information accessibility, query success
- Facebook: "Connect people" → meaningful interactions, relationship building

**How to use:**
- State both financial metric AND mission impact
- Show feature serves strategic positioning, not just revenue
- Demonstrate long-term value alignment

## Creating Intermediate Metrics

Most features can't directly move company-wide North Star metrics. Create a chain:

```
Feature Metric → Intermediate Metric → North Star Metric
```

**Intermediate metric requirements:**
1. **Directly measurable** by your product/team
2. **Correlates with** North Star metric
3. **Actionable** - you can impact it with product changes

**Example: YouTube Homepage**
- North Star: Time on Site
- Intermediate Metrics:
  - % users scrolling down homepage (exploration)
  - % clicking videos from homepage (activation)
  - % watching ≥10 min after homepage click (engagement)
  - % discovering new genres (mission: broaden interests)

**Example: Uber Driver App**
- North Star: Monthly Active Drivers (supply side)
- Intermediate Metrics:
  - Profile completion rate (activation)
  - Time spent browsing app (engagement signal)
  - Ride acceptance rate (core behavior)
  - Hours driven per week (retention)
  - Driver rating + tips (quality indicator)

## Validation Checklist

Before finalizing metric selection:

1. **Business model identified?**
   - [ ] Confirmed company's primary revenue model
   - [ ] Mapped to one of 5 categories

2. **North Star mapped?**
   - [ ] Primary North Star metric identified
   - [ ] Secondary metrics noted (if applicable)

3. **Intermediate metrics created?**
   - [ ] 3-7 intermediate metrics brainstormed
   - [ ] Each is directly measurable by your team
   - [ ] Correlation to North Star explained

4. **Mission alignment stated?**
   - [ ] Feature impact on mission articulated
   - [ ] Goes beyond pure financial metrics

5. **Prioritization complete?**
   - [ ] 1-2 key metrics selected from candidates
   - [ ] Rationale for prioritization documented

## Workflow Steps

### 1. Identify Business Model

Ask clarifying questions:
- How does the company make money?
- Who pays? (users, advertisers, merchants, etc.)
- What drives revenue? (attention, subscriptions, transactions, etc.)

Map to one of 5 categories.

### 2. Map North Star Metrics

Based on business model category, identify:
- Primary North Star metric (usually MAU + one other)
- How revenue correlates with these metrics
- Why these metrics matter strategically

### 3. Define Intermediate Metrics

For the specific product/feature:
- What user behaviors can you directly measure?
- Which behaviors correlate with North Star movement?
- What's the logical chain from feature → intermediate → North Star?

Brainstorm 3-7 candidates.

### 4. Validate Mission Alignment

Ask:
- How does this feature serve the company mission?
- Does it align with strategic positioning?
- What non-financial value does it create?

Document the connection.

### 5. Prioritize Metrics

From 3-7 candidates, select 1-2 primary metrics:
- Which are most actionable?
- Which have clearest North Star correlation?
- Which can you explain in one sentence?

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "Engagement" without definition | Define precise numerator/denominator formula |
| Using ARPU when can't control pricing | Use conversion rate or usage frequency instead |
| Single-sided marketplace metrics | Measure both sides separately (supply AND demand) |
| No intermediate metrics | Create measurable proxies your team controls |
| Ignoring mission alignment | Connect to strategic goals beyond revenue |
| Too many metrics (10+) | Prioritize to 1-2 key metrics with 3-5 supporting |

## Anti-Rationalization Blocks

| Rationalization | Reality |
|-----------------|---------|
| "Engagement is obvious" | Define mathematically: numerator/denominator |
| "Everyone knows our business model" | State explicitly for clarity |
| "This doesn't map to revenue" | Everything maps to revenue; find the path |
| "We're unique, categories don't fit" | 95% of companies fit 5 categories; edge cases rare |
| "Mission doesn't matter, just revenue" | Long-term success requires mission alignment |

## Success Criteria

North Star Alignment succeeds when:
- Business model explicitly identified and categorized
- Primary North Star metric stated with mathematical formula
- Intermediate metrics defined (3-7 candidates, 1-2 prioritized)
- Each intermediate metric's correlation to North Star explained
- Mission alignment articulated beyond financial metrics
- Metrics are actionable by the team building the feature

## Real-World Examples

### Example 1: Airbnb Check-in Experience
**Business Model:** Two-sided marketplace
**North Star:** 
- MAU (guests) - primary revenue driver
- Booking value - secondary (revenue per transaction)

**Intermediate Metrics:**
- Messages sent to host (friction indicator - INVERSE metric, lower is better)
- Lag time for host responses (speed of issue resolution)
- Time from arrival to "fully set up" (aggregate friction)

**Mission Alignment:** "Belong anywhere" → Seamless check-in = feeling at home quickly

### Example 2: Facebook Dating
**Business Model:** Ads (parent company)
**North Star:**
- MAU (dating product)
- Time on Facebook platform (ads shown)

**Intermediate Metrics:**
- Number of matches per user
- Two-way conversations (quality engagement proxy)
- Off-platform connections (friend requests, status changes)
- Weekly active dating users

**Counter-metrics:**
- Timeline post frequency (cannibalization check)
- Overall Facebook engagement (ensure not cannibalizing main product)

**Mission Alignment:** "Build community and connect people" → Meaningful relationships

### Example 3: Uber Driver App Quality Features
**Business Model:** Two-sided marketplace
**North Star:**
- Monthly Active Drivers (supply side critical)
- Hours driven (depth of engagement)

**Intermediate Metrics:**
- Driver ratings (quality indicator)
- Tips received (super-quality indicator)
- Ride acceptance rate (willingness to drive)
- Cash-out frequency (value realization)

**Visualization:**
- X-axis: Driver rating buckets (4.5-4.74, 4.75-5.0, 5.0+ w/ tips)
- Y-axis: Hours driven
- Goal: Maximize hours in highest quality bucket

**Mission Alignment:** "Transportation for everyone" → High-quality reliable drivers

## Related Skills

- **proxy-metric-selection**: Creates measurable indicators when North Star is hard to measure directly
- **funnel-metric-mapping**: Decomposes North Star into lifecycle stages
- **tradeoff-evaluation**: Uses North Star to resolve conflicting metric priorities
- **metrics-definition** (workflow): Orchestrates North Star alignment with other metric skills

## Integration Points

**Called by workflows:**
- `metrics-definition` - Step 1: Establish North Star before defining feature metrics
- `metric-diagnosis` - Step 4: Assess whether metric change impacts top-line
- `tradeoff-decision` - Step 1: Determine which metric matters more strategically
- `dashboard-design` - Step 1: Anchor dashboard to company mission
- `goal-setting` - Step 1: Understand movement needed for company goals

**Calls these skills:**
- Uses `meeting-synthesis` if customer evidence needed for mission alignment
- May invoke `research-gathering` for competitive North Star benchmarks

