---
name: thinking-fermi-estimation
description: Make order-of-magnitude estimates for unknown quantities by decomposing into known or estimable factors. Use for capacity planning, cost estimation, market sizing, and technical feasibility assessment.
---

# Fermi Estimation

## Overview

Fermi estimation, named after physicist Enrico Fermi, is the art of making reasonable estimates for quantities that seem impossible to know without direct measurement. By decomposing a question into factors you can estimate, then multiplying, you often get surprisingly accurate order-of-magnitude results.

**Core Principle:** Break the unknown into known (or estimable) pieces. Even rough estimates combine to reasonable accuracy due to errors canceling out.

## When to Use

- Capacity planning ("How much storage will we need?")
- Cost estimation ("What will this infrastructure cost?")
- Market sizing ("How many potential users exist?")
- Feasibility assessment ("Is this even plausible?")
- Sanity checking ("Does this number make sense?")
- Interview questions ("How many piano tuners in Chicago?")
- Quick prioritization ("Is this worth pursuing?")

Decision flow:

```
Need a number you don't have? → yes → Can you measure it directly? → no → FERMI ESTIMATE
                                                                   ↘ yes → Measure
                              ↘ no → You might not need it
```

## The Fermi Process

### Step 1: Clarify What You're Estimating

Be precise about the quantity:

```
Vague: "How big is the market?"
Precise: "How many SaaS companies with 50-500 employees in the US
         would pay $1000/month for our product?"
```

### Step 2: Decompose into Estimable Factors

Break into pieces you can estimate:

```
Storage needs for user data:
= (Number of users)
  × (Data per user per day)
  × (Days of retention)
  × (Overhead factor)
```

**Decomposition strategies:**

| Strategy | Example |
|----------|---------|
| By component | Total = Sum of parts |
| By rate × time | Total = Rate × Duration |
| By population × fraction | Target = Base × Percentage |
| By analogy × adjustment | New ≈ Similar × Ratio |

### Step 3: Estimate Each Factor

For each factor, estimate based on:

| Source | Example |
|--------|---------|
| Known data | "We have 10,000 DAU" |
| Industry benchmarks | "Average SaaS churn is 5%" |
| Physical constraints | "A human can make ~50 decisions/day" |
| Logical bounds | "At least 1, at most 1 million" |
| Personal experience | "I've seen systems handle 1000 req/s" |

**When estimating:**
- Use ranges, not point estimates: "10,000 to 50,000"
- Prefer geometric mean for order-of-magnitude: √(10,000 × 50,000) = 22,360
- Round to one significant figure: ~20,000

### Step 4: Combine Factors

Multiply (or add) factors together:

```
Storage = 50,000 users × 10 KB/user/day × 365 days × 1.5 overhead
        = 50,000 × 10,000 × 365 × 1.5 bytes
        = 274 billion bytes
        ≈ 270 GB/year
```

### Step 5: Sanity Check

Verify reasonableness:
- Does the order of magnitude make sense?
- Is it physically possible?
- Does it match any known data points?
- Would a 10x error change the decision?

### Step 6: State Confidence and Implications

```
Estimate: ~270 GB/year
Confidence: Within 3-5x (80-1,500 GB)
Implication: Standard database tier sufficient; no special infrastructure needed
```

## Fermi Estimation Template

```markdown
# Fermi Estimate: [Question]

## Question (Precise)
[Exactly what we're estimating]

## Decomposition
[Quantity] = [Factor 1] × [Factor 2] × ... × [Factor N]

## Factor Estimates

### Factor 1: [Name]
- Estimate: [Value]
- Source/Reasoning: [Why this number]
- Confidence: High / Medium / Low

### Factor 2: [Name]
- Estimate: [Value]
- Source/Reasoning: [Why this number]
- Confidence: High / Medium / Low

[Continue for all factors...]

## Calculation
[Show the math]

## Result
- Point estimate: [Value]
- Range: [Low] to [High] (representing Xx uncertainty)

## Sanity Check
- Physical plausibility: [Check]
- Comparison to known data: [Check]
- Order of magnitude reasonable: [Check]

## Implications
[What does this estimate mean for the decision?]
```

## Example 1: Data Storage Needs

**Question:** How much storage will our new feature need in Year 1?

```markdown
## Decomposition
Storage = Users × Events/User/Day × Event Size × Days × Replication

## Factor Estimates

### Users (DAU)
- Estimate: 100,000 (current) growing to 200,000 (end of year)
- Average over year: ~150,000
- Confidence: High (we have current data)

### Events per User per Day
- Estimate: 50 events (based on current feature usage patterns)
- Confidence: Medium (new feature might differ)

### Event Size
- Estimate: 500 bytes (JSON with typical payload)
- Confidence: High (we can measure similar events)

### Days in Year
- Estimate: 365
- Confidence: Certain

### Replication Factor
- Estimate: 3x (standard for durability)
- Confidence: High (architectural requirement)

## Calculation
Storage = 150,000 × 50 × 500 × 365 × 3
        = 150,000 × 50 × 500 × 365 × 3
        = 4.1 × 10^12 bytes
        = 4.1 TB

## Result
- Point estimate: ~4 TB
- Range: 1 TB (pessimistic assumptions) to 15 TB (growth beats expectations)

## Sanity Check
- 4 TB for 150K users = ~27 MB/user/year = reasonable
- Similar feature at other company uses "several TB" = consistent
- Standard database can handle 4 TB = feasible

## Implications
- Standard managed database tier sufficient
- No need for sharding or special storage architecture in Year 1
- Budget ~$500/month for storage costs
```

## Example 2: API Rate Capacity

**Question:** Can our API handle Black Friday traffic?

```markdown
## Decomposition
Required RPS = Peak Daily Users × Requests/User/Session × Sessions/Day × Peak Multiplier / Seconds in Peak Hour

## Factor Estimates

### Peak Daily Users
- Estimate: 500,000 (3x normal 170K)
- Source: Last year's Black Friday
- Confidence: Medium

### Requests per Session
- Estimate: 30 API calls (measured)
- Confidence: High

### Sessions per Day
- Estimate: 2 (mobile + desktop)
- Confidence: Medium

### Peak Multiplier
- Estimate: 5x (traffic concentrated in 4-hour window, spiky within that)
- Confidence: Medium

### Seconds in Peak Hour
- Estimate: 3,600
- Confidence: Certain

## Calculation
Required RPS = (500,000 × 30 × 2 × 5) / 3,600
             = 150,000,000 / 3,600
             = 41,667 RPS
             ≈ 40,000 RPS peak

## Result
- Point estimate: 40,000 RPS
- Range: 15,000 to 100,000 RPS

## Sanity Check
- Current capacity: 10,000 RPS
- Gap: 4x capacity needed
- Similar scale companies report 20-50K RPS on peak days = consistent

## Implications
- Need 4x capacity increase
- Auto-scaling must handle 40K+ RPS
- Load test to 60K RPS (1.5x safety margin)
```

## Example 3: Market Size

**Question:** How many potential customers for our developer tool?

```markdown
## Decomposition
TAM = Software Companies × Avg Developers × Adoption Rate × Price Tolerance

## Factor Estimates

### Software Companies (US)
- Estimate: ~500,000 (SBA data: tech companies)
- Confidence: Medium

### With 10+ Developers (our target)
- Estimate: 10% = 50,000 companies
- Confidence: Low (rough estimate)

### Developers per Target Company
- Estimate: 30 average
- Confidence: Medium

### Adoption Rate (would consider)
- Estimate: 20% (dev tools are crowded)
- Confidence: Low

### Price Point
- Estimate: $50/developer/month
- Confidence: Medium (based on similar tools)

## Calculation
Addressable Users = 50,000 × 30 × 20% = 300,000 developers
Revenue = 300,000 × $50 × 12 = $180M/year TAM

## Result
- TAM: ~$180M/year
- Realistic serviceable market: 5-10% = $10-20M/year

## Sanity Check
- Similar dev tools (Datadog, etc.) have $100M+ revenue = plausible ceiling
- 300K potential users in a niche = reasonable

## Implications
- Market size justifies investment if we can capture 5%+
- Need differentiation in crowded space
```

## Common Decomposition Patterns

### Capacity Planning
```
Needed = Users × Usage/User × Factor/Usage × Growth × Safety
```

### Cost Estimation
```
Cost = Resources × Unit Cost × Duration × Overhead
```

### Time Estimation
```
Time = Tasks × Time/Task × (1 + Risk Factor)
```

### Market Sizing
```
Market = Population × Segment% × Adoption% × Price × Frequency
```

## Tips for Better Estimates

### Use Multiple Approaches

Estimate the same thing different ways:

```
Website traffic estimate:
Method 1: Bottom-up from user base
Method 2: Top-down from market share
Method 3: Analogy to similar company

If methods agree within 3x, confidence increases
If they diverge wildly, investigate assumptions
```

### Bound First

Start with upper and lower bounds:

```
"Definitely more than 1,000, definitely less than 10 million"
"So somewhere in 10,000-1,000,000 range"
"Let me narrow from there..."
```

### Watch for Correlated Errors

If factors are correlated, errors don't cancel:

```
BAD: Users × Revenue/User (both depend on same growth assumption)
BETTER: Estimate revenue directly, or use independent factors
```

### One Significant Figure

Don't false precision:

```
Calculation: 47,832,519 bytes
Report: ~50 MB (not "47.8 MB")
```

## Verification Checklist

- [ ] Question stated precisely
- [ ] Decomposed into 3-6 estimable factors
- [ ] Each factor has reasoning/source
- [ ] Factors are relatively independent
- [ ] Calculation shown and checked
- [ ] Result sanity-checked against reality
- [ ] Uncertainty range stated
- [ ] Implications for decision clarified

## Key Questions

- "Can I break this into smaller, estimable pieces?"
- "What do I already know that constrains this?"
- "What's the upper bound? Lower bound?"
- "Does this number pass the smell test?"
- "Would being off by 10x change my decision?"
- "Can I estimate this a different way to cross-check?"

## Fermi's Wisdom

When asked how many piano tuners were in Chicago, Fermi didn't look it up—he estimated from population, households, pianos, tuning frequency, and tuner capacity. His estimate was reportedly within 20% of the actual number.

The lesson: You know more than you think. Decompose, estimate, combine. The errors often cancel, and you get surprisingly close to truth.

"Never make a calculation until you know the answer." — John Wheeler (Fermi's colleague)

Meaning: Estimate first to know what answer to expect, then calculate to verify.
