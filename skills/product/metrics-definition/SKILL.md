---
name: metrics-definition
description: Use when establishing metrics for new product, feature, or initiative - orchestrates North Star alignment, funnel mapping, proxy selection, and counter-metric identification to create comprehensive measurement framework
---

# Metrics Definition Workflow

## Purpose

Establish what to measure for a new product, feature, or initiative by systematically working from company mission → North Star → funnel stages → proxy metrics → counter-metrics. Ends with prioritized set of 1-3 metrics with clear mathematical definitions.

## When to Use This Workflow

Use this workflow when:
- Kicking off a new product or feature
- Writing a PRD and need to define success criteria
- Preparing for product review where leadership will ask "how will we know this worked?"
- Inheriting a product that lacks clear success metrics
- Establishing OKRs for team or product area
- Creating measurement plan for strategic initiative

## Skills Sequence

This workflow orchestrates 4 core skills in sequence:

```
1. North Star Alignment
   ↓ (Identifies company mission, business model, top-line metrics)
2. Funnel-Based Metric Mapping
   ↓ (Decomposes user journey into stages)
3. Proxy Metric Selection
   ↓ (Creates measurable indicators for each stage)
4. Trade-off Evaluation
   ↓ (Identifies counter-metrics and potential conflicts)
   
OUTPUT: 3-7 candidate metrics, 1-2 prioritized, counter-metrics, funnel mapping
```

## Required Inputs

Gather this information before starting:

### Company/Product Context
- **Company/product mission statement**
  - Example: "Increase the Internet's GDP" (Stripe)
- **Business model type**
  - One of: Ads, Freemium, Enterprise SaaS, Marketplace, E-commerce
- **Strategic positioning**
  - What makes you unique? Core value proposition?

### Feature/Product Context
- **Description of the feature or product**
  - What are you building?
  - What problem does it solve?
- **Target user segment**
  - Who is this for?
  - What are their characteristics?
- **Expected user journey**
  - How will users discover and use this?

## Workflow Steps

### Step 1: North Star Alignment (15 minutes)

**Use the `north-star-alignment` skill**

**Activities:**
1. Identify company business model (1 of 5 types)
2. Map to corresponding North Star metrics
3. Articulate mission statement connection
4. Define how this feature impacts North Star

**Questions to answer:**
- What business model category does the company fit?
- What are the North Star metrics for this business model?
- How does this feature connect to the mission statement?
- What's the chain: Feature → Intermediate → North Star?

**Output:**
- Business model: [Type]
- North Star metrics: [1-2 metrics with formulas]
- Mission alignment: [How feature serves mission]
- Intermediate metric hypothesis: [Initial ideas]

**Example output:**
```
Business Model: Two-sided marketplace (Uber)
North Star Metrics: 
  - Monthly Active Drivers (supply side)
  - Hours driven per driver (depth of engagement)
Mission: "Transportation for everyone"
  - Feature (driver quality ratings) → Better experiences → More riders → 
    More driver earnings → Driver retention → More transportation availability
```

### Step 2: Funnel-Based Metric Mapping (20 minutes)

**Use the `funnel-metric-mapping` skill**

**Activities:**
1. Map out user journey stages (Reach → Activation → Engagement → Retention)
2. Identify metrics for each stage
3. Calculate or estimate transition conversion rates
4. Identify any flywheel dynamics

**Questions to answer:**
- What are the sequential stages users go through?
- What defines success at each stage?
- Where do users currently drop off?
- Are there any feedback loops or flywheels?

**Output:**
- User journey stages: [4-5 stages defined]
- Metrics per stage: [1-3 metrics each]
- Conversion rates: [Estimated or actual %]
- Flywheel effects: [If any]

**Example output:**
```
Uber Driver Quality Feature Journey:

Reach: Driver awareness of quality program
  - Drivers shown quality dashboard
  
Activation: Driver engages with quality tools
  - % drivers viewing quality dashboard
  - % reading quality tips
  
Engagement: Driver improves behaviors
  - Rating trend (up/stable/down)
  - Tips received per week
  
Retention: Driver maintains high quality
  - % drivers in 4.8+ bucket over time
  - Hours driven by quality tier

Flywheel: High quality → Better rider experience → More rides → 
          More driver earnings → Driver retention
```

### Step 3: Proxy Metric Selection (20 minutes)

**Use the `proxy-metric-selection` skill**

**Activities:**
1. For each funnel stage, identify outcomes that are hard to measure directly
2. Design proxy metrics with clear mathematical formulas
3. Create both sophisticated and simplified versions
4. Validate correlation logic

**Questions to answer:**
- Which outcomes are delayed or hard to measure?
- What observable behaviors correlate with success?
- Can we define precise numerator/denominator?
- Do we have both complex and simple versions?

**Output:**
- Proxy metrics: [3-7 candidates with formulas]
- Numerator/denominator: [Clearly defined for each]
- Correlation logic: [Why proxy indicates true outcome]
- Simplified alternatives: [Easier-to-explain versions]

**Example output:**
```
Feature: Airbnb Check-in Experience

True Outcome: Seamless, stress-free check-in (subjective)

Sophisticated Proxy:
  - Aggregate time from geolocation arrival to WiFi connected
  - Plus: Sum of informational message lag times
  - Formula: (Arrival timestamp - WiFi timestamp) + Σ(Message → Response lag)

Simplified Proxy:
  - W-questions sent to host
  - Formula: Messages containing {who/what/when/where/why/how} / Guest stays
  - Correlation: Questions indicate confusion or missing information

Alternative:
  - Total informational messages (not social)
  - Formula: Informational messages / Guest stays
  - Use ML to classify message types
```

### Step 4: Trade-off Evaluation (15 minutes)

**Use the `tradeoff-evaluation` skill**

**Activities:**
1. Identify counter-metrics (what could go down if main metric goes up?)
2. List potential unintended consequences
3. Define acceptable trade-off ranges
4. Plan monitoring approach

**Questions to answer:**
- What could go wrong if we optimize for these metrics?
- What parts of the product might suffer?
- Are there cannibalization risks?
- What counter-metrics should we monitor?

**Output:**
- Counter-metrics: [2-3 per primary metric]
- Cannibalization risks: [Identified concerns]
- Acceptable ranges: [Thresholds for concern]
- Monitoring plan: [How often, what triggers action]

**Example output:**
```
Primary Metrics:
  - Driver rating distribution (goal: more in 4.8+ bucket)
  - Hours driven by quality tier

Counter-Metrics:
  1. Driver churn rate (if quality standards too strict)
  2. Ride acceptance rate (if drivers become pickier about riders)
  3. Supply availability (if too many drivers deactivated)
  4. Surge pricing frequency (supply/demand balance)

Acceptable Ranges:
  - Driver churn: <5% increase acceptable
  - Acceptance rate: Must stay >85%
  - Surge frequency: <10% increase acceptable

Monitoring:
  - Weekly dashboard review
  - Alert if counter-metric exceeds threshold
  - Monthly deep-dive analysis
```

### Step 5: Prioritization and Output (10 minutes)

**Activities:**
1. Review all candidate metrics (3-7 identified)
2. Apply prioritization criteria
3. Select 1-2 primary metrics
4. Document rationale

**Prioritization criteria:**
- **Actionability:** Can team directly impact this?
- **Clarity:** Can explain in one sentence?
- **North Star correlation:** Clear link to company goals?
- **Leading indicator:** Provides early signal vs. lagging?

**Final output document:**

```markdown
# Success Metrics: [Feature Name]

## Business Context
- Business Model: [Type]
- North Star Metrics: [Company-level]
- Mission Alignment: [How feature serves mission]

## User Journey & Funnel
[Stage 1] → [Stage 2] → [Stage 3] → [Stage 4]
[Conversion rates and metrics per stage]

## Primary Metrics (Prioritized)

### 1. [Metric Name]
- **Formula:** [Numerator] / [Denominator]
- **Rationale:** [Why this metric matters]
- **North Star connection:** [How it ladders up]
- **Target:** [Goal value or % improvement]

### 2. [Metric Name]
- **Formula:** [Numerator] / [Denominator]
- **Rationale:** [Why this metric matters]
- **North Star connection:** [How it ladders up]
- **Target:** [Goal value or % improvement]

## Supporting Metrics
- [3-5 additional metrics to monitor]

## Counter-Metrics
- [2-3 metrics to watch for unintended effects]
- [Acceptable ranges for each]

## Monitoring Plan
- Dashboard review: [Frequency]
- Alert thresholds: [What triggers escalation]
- Deep-dive schedule: [When to analyze deeply]
```

## Integration with PRD Creation

When used during PRD creation:

**In PRD "Goals and Success Criteria" section:**
- Primary metrics become success metrics
- Supporting metrics go in monitoring plan
- Counter-metrics documented as risks
- Funnel analysis informs use cases

**Quality gate:**
- PRD validation requires success metrics defined
- Must have clear formulas (numerator/denominator)
- Must show North Star connection

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with metrics, not mission | Always begin with North Star alignment |
| Vague metric definitions ("engagement") | Define precise mathematical formulas |
| Only measuring final outcome | Map full funnel from reach to retention |
| Ignoring counter-metrics | Always identify what could go wrong |
| Too many metrics (15+) | Prioritize to 1-2 primary, 3-5 supporting |
| No connection to company goals | Explicitly show how metrics ladder up |

## Success Criteria

Metrics definition succeeds when:
- North Star alignment explicitly documented
- User journey mapped with 4-5 stages
- 3-7 candidate metrics identified with precise formulas
- 1-2 primary metrics selected and prioritized
- Rationale for prioritization clearly stated
- Counter-metrics identified (2-3 per primary metric)
- Monitoring plan established
- Output document created and shared
- Stakeholders understand and accept metrics

## Real-World Example: Uber Driver Quality Program

### Step 1: North Star Alignment
```
Business Model: Two-sided marketplace
North Star Metrics:
  - Monthly Active Drivers (MAD)
  - Hours driven per month (depth)
Mission: "Transportation for everyone"
Feature Impact: Better driver quality → Better rider experience → 
                More rides → More driver earnings → Driver retention
```

### Step 2: Funnel Mapping
```
Reach: All active drivers (baseline)
Activation: Drivers view quality dashboard (70% within first week)
Engagement: Drivers take quality actions (read tips, improve behavior)
  - Tip acceptance increase: 15%
  - Response time improvement: 10%
Retention: Drivers maintain/improve ratings
  - Month-over-month rating stability: 85%
```

### Step 3: Proxy Selection
```
Primary (Sophisticated):
  - Driver quality distribution by hours driven
  - X-axis: Rating buckets (4.5-4.74, 4.75-5.0, 5.0+ w/ tips)
  - Y-axis: Total hours driven
  - Formula: Σ(Hours driven by drivers in bucket) / Total hours

Primary (Simplified):
  - Average driver rating weighted by activity
  - Formula: Σ(Rating × Rides completed) / Total rides

Supporting:
  - % drivers receiving tips (quality indicator)
  - Formula: Drivers with ≥1 tip per week / Total active drivers
```

### Step 4: Counter-Metrics
```
1. Driver churn rate
   - Current: 8% monthly
   - Acceptable: <10% monthly
   - Alert if: >12%

2. Ride acceptance rate
   - Current: 92%
   - Acceptable: >85%
   - Alert if: <85%

3. Driver complaints about rating system
   - Current: 50/month
   - Acceptable: <100/month
   - Alert if: >150/month
```

### Step 5: Final Output
```
PRIMARY METRICS:
1. Hours driven in 4.8+ rating bucket
   - Current: 45% of total hours
   - Target: 60% within 6 months
   - Measures: Quality × Volume

COUNTER-METRICS:
1. Driver churn <10%
2. Acceptance rate >85%
3. Complaints <100/month

MONITORING:
- Weekly dashboard (all metrics)
- Monthly deep-dive (rating distributions, cohort analysis)
- Quarterly review (strategic alignment)
```

## Related Skills

This workflow orchestrates these skills:
- **north-star-alignment** (Step 1)
- **funnel-metric-mapping** (Step 2)
- **proxy-metric-selection** (Step 3)
- **tradeoff-evaluation** (Step 4)

## Related Workflows

- **prd-creation**: Uses metrics-definition for PRD success criteria
- **dashboard-design**: Uses similar skill sequence for ongoing monitoring
- **goal-setting**: Uses these metrics to set targets

## Time Estimate

**Total: 70-90 minutes**
- Step 1 (North Star): 15 min
- Step 2 (Funnel): 20 min
- Step 3 (Proxy): 20 min
- Step 4 (Trade-off): 15 min
- Step 5 (Output): 10 min
- Buffer: 10 min

Can be done in single session or broken into two sessions (Steps 1-2, then Steps 3-5).

