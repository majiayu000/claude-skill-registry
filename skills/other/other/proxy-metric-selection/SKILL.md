---
name: proxy-metric-selection
description: Use when outcomes are difficult to measure directly - designs proxy metrics that correlate with true outcomes, with clear mathematical formulas and counter-metrics for unintended effects
---

# Proxy Metric Selection

## Purpose

Create measurable proxy metrics when true outcomes are delayed, abstract, or influenced by many confounding variables. Ensures teams can measure progress toward goals even when the ultimate outcome isn't directly observable.

## When to Use This Skill

Activate automatically when:
- True outcome is delayed (dating app "successful relationships" take months/years)
- Outcome is abstract ("user satisfaction", "product quality")
- Direct measurement is impossible (cash transactions in marketplace)
- Too many confounding variables affect outcome (can't isolate your impact)
- `metrics-definition` workflow identifies hard-to-measure goals
- Need leading indicators for lagging outcomes
- Creating success metrics for PRDs

**When NOT to use:**
- Outcome is directly measurable in reasonable timeframe
- Simple event tracking covers the need (button clicks, page views)
- Proxy would be more complex than measuring actual outcome

## Core Principles

### 1. Mathematical Precision Required

Every metric must have:
- **Clear numerator** - what you're counting
- **Clear denominator** - over what population/time
- **Precise formula** - no ambiguity in calculation

**Good examples:**
- "Stories created per person per day"
- "Two-message conversations per weekly active user"
- "Listings added per day"

**Bad examples:**
- "Engagement" (undefined)
- "Better experience" (not measurable)
- "User satisfaction" (without survey instrument)

### 2. Correlation Validation

Proxy must actually correlate with desired outcome:
- **Hypothesis:** What's the logical connection?
- **Validation:** How will you test correlation?
- **Monitoring:** Track both proxy and outcome when possible

### 3. Offer Multiple Levels

Provide both sophisticated and simplified versions:

**Sophisticated (Scientific):**
- Complex estimations with multiple signals
- Subpopulation analysis
- Statistical rigor

**Simplified (Actionable):**
- Easy to explain in one sentence
- Rally teams around quickly
- Fewer assumptions

## Proxy Design Patterns

### Pattern 1: Behavioral Signals as Proxies

**When:** Outcome involves user intent or satisfaction

**Examples:**

**Facebook Marketplace Sales**
- **Outcome:** Number of sales completed (unknown - cash transactions)
- **Sophisticated Proxy:** Messages sent by seller → buyer → item delisted within 24 hours
- **Simple Proxy:** Listings added per day
- **Validation:** Survey sample of users who delisted items

**Dating App Relationships**
- **Outcome:** Successful long-term relationships (takes years)
- **Sophisticated Proxy:** Two-way conversations (≥2 messages each) + off-platform connection (friend request or status change)
- **Simple Proxy:** Number of matches per user
- **Why:** Reciprocal interest is leading indicator; one-sided messages indicate failure

### Pattern 2: Time-Based Aggregates

**When:** Individual events are noisy but patterns matter

**Examples:**

**Airbnb Check-in Quality**
- **Outcome:** Seamless check-in experience (subjective)
- **Sophisticated Proxy:** Aggregate time from geolocation arrival to WiFi connection + sum of informational message lag times
- **Simple Proxy:** Number of W-questions sent to host (who/what/when/where/why)
- **Why:** Friction manifests as questions and waiting

### Pattern 3: Quality Indicators

**When:** Quantity is easy but quality matters more

**Examples:**

**Uber Driver Quality**
- **Outcome:** High-quality reliable drivers
- **Sophisticated Proxy:** Rating buckets (4.5-4.74, 4.75-5.0, 5.0+ with tips) weighted by tips adding 0.1-0.25% to rating
- **Simple Proxy:** Average driver rating
- **Why:** Tips indicate exceptional service beyond 5-star baseline

**Snapchat Engagement Quality**
- **Outcome:** Meaningful social connections
- **Sophisticated Proxy:** Stories shared + messages sent (peer-to-peer) vs. time on creator content (passive consumption)
- **Simple Proxy:** Messages sent per DAU
- **Why:** Social interaction drives retention flywheel; passive consumption competes with TikTok/YouTube

## Counter-Metrics: Detecting Cannibalization

**Purpose:** Identify when proxy improvement causes unintended harm

**How to identify:**
1. Ask: "What could go DOWN if this goes UP?"
2. Check metrics in other parts of the product
3. Monitor for substitution effects

**Examples:**

**Instagram Stories**
- Primary Metric: Stories created per user per day
- **Counter-Metric:** Timeline posts per day
- **Why:** Stories might cannibalize traditional posts (net-zero value)
- **Outcome:** Stories captured users who wouldn't post otherwise (no cannibalization)

**Facebook Dating**
- Primary Metric: Weekly active dating users
- **Counter-Metrics:** 
  - Overall Facebook MAU (ensure not cannibalizing main product)
  - Time on main feed (ensure dating doesn't reduce core engagement)
- **Why:** New feature might just shift activity, not add value

**Snapchat Redesign**
- Primary Metric: Time on site (increased)
- **Counter-Metrics:**
  - Messages sent (decreased - BAD)
  - Stories shared (decreased - BAD)
- **Why:** Passive content consumption broke social engagement flywheel

## Workflow Steps

### 1. Define True Outcome

Ask:
- What are we ultimately trying to achieve?
- Why is this hard to measure directly?
- What's the timeframe for knowing success?

Document the ideal metric if it were measurable.

### 2. Identify Observable Behaviors

Brainstorm:
- What user behaviors correlate with the outcome?
- What events can we track in the product?
- What patterns indicate success vs. failure?

List 5-10 observable signals.

### 3. Design Proxy Formula

For each candidate proxy:
- Define numerator (what you're counting)
- Define denominator (per user? per day? per session?)
- Write mathematical formula
- Explain logical connection to outcome

### 4. Create Simplified Version

Ask:
- Can I explain this in one sentence?
- Would a non-technical stakeholder understand?
- Can I rally a team around this?

Trade precision for clarity if needed.

### 5. Identify Counter-Metrics

For each proxy metric:
- What could decrease if this increases?
- What parts of the product might suffer?
- What substitution effects could occur?

List 2-3 counter-metrics per primary metric.

### 6. Validate Correlation

Plan:
- How will you test if proxy correlates with outcome?
- What data would disprove the correlation?
- How often will you check the relationship?

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague metric names ("engagement") | Define precise formula with numerator/denominator |
| Measuring inputs not outcomes | Track user value, not team activity |
| Ignoring counter-metrics | Always list what could go wrong |
| Only offering complex version | Provide simple alternative for stakeholder buy-in |
| Assuming correlation without testing | Plan validation approach |
| Single-sided metrics for two-sided markets | Measure both sides of marketplace |

## Anti-Rationalization Blocks

| Rationalization | Reality |
|-----------------|---------|
| "We'll measure the real thing eventually" | Define proxy now, can't wait months/years |
| "Engagement is self-explanatory" | Define mathematical formula or it doesn't count |
| "Counter-metrics don't apply here" | Every metric has potential unintended effects |
| "The simple version is too simple" | Simple version rallies teams; sophistication comes later |
| "Correlation is obvious, no need to test" | Validate assumptions with data |

## Success Criteria

Proxy metric selection succeeds when:
- True outcome clearly articulated (even if unmeasurable)
- Proxy metric has precise mathematical formula
- Logical correlation to outcome explained
- Both sophisticated and simplified versions exist
- 2-3 counter-metrics identified
- Validation approach documented
- Team can explain the metric in plain language

## Real-World Examples

### Example 1: Facebook Dating Success

**True Outcome:** Long-term successful relationships (takes years to measure)

**Proxy Metrics (Prioritized):**

**Primary:**
- **Two-message conversations per weekly active user**
- Formula: (Conversations where both users sent ≥2 messages) / Weekly active dating users
- Why: Reciprocal interest is leading indicator of relationship potential
- Sophisticated: Track progression to off-platform (friend requests, status changes)
- Simple: Number of matches per user (easier to explain)

**Counter-Metrics:**
- Timeline posts per day (cannibalization check)
- Overall Facebook engagement time (ensure not harming main product)

**Validation:**
- Survey users who had 2+ message conversations
- Track relationship status changes over 6 months
- Compare dating vs. non-dating user retention

### Example 2: Marketplace Transaction Estimation

**True Outcome:** Sales completed on Facebook Marketplace (unmeasurable - cash)

**Proxy Metrics:**

**Sophisticated:**
- Messages: Seller → Buyer → Item delisted within 24 hours
- Formula: (Items delisted ≤24h after buyer-seller exchange) / Total active listings
- Subpopulations: Adjust timeframe by category (furniture 72h, electronics 12h)

**Simplified:**
- Listings added per day
- Formula: New listings / Day
- Why: Sellers return when they successfully sell (retention proxy)

**Counter-Metrics:**
- Buyer complaints (fraud indicator)
- Average listing duration (if too short, could indicate spam)

**Validation:**
- Sample survey of users who delisted items
- "Did you complete a sale?" yes/no
- Test correlation between proxy and survey results

### Example 3: Airbnb Check-in Experience

**True Outcome:** Seamless, stress-free check-in (subjective experience)

**Proxy Metrics:**

**Sophisticated:**
- Aggregate time: (Geolocation arrival vicinity) → (WiFi connected)
- Plus: Sum of (informational message sent → host response) lag times
- Formula requires: Geolocation permissions + WiFi connection tracking

**Simplified:**
- W-questions sent to host (parsed via ML/keywords)
- Formula: Messages containing {who/what/when/where/why/how} / Guest stays
- Why: Questions indicate missing information or confusion

**Alternative:**
- Total messages sent to host (informational, not social)
- Use ML to classify: Informational vs. social ("Thanks!" vs. "Where are the keys?")

**Counter-Metrics:**
- Host response time (ensure not just shifting burden to hosts)
- Check-in abandonment rate (users who book but don't check in)

**Validation:**
- Post-check-in survey: "Check-in was seamless" 1-5 scale
- Correlate survey scores with proxy metrics
- A/B test features that should improve proxy, measure survey impact

### Example 4: Uber Driver Quality

**True Outcome:** High-quality, reliable driver network

**Proxy Metrics:**

**Sophisticated:**
- Driver quality score: Base rating + tip bonus
- Buckets: 4.5-4.74, 4.75-5.0, 5.0+ with tips
- Tips add: +0.1 to +0.25% to average rating (tuned by data science)
- Visualization: X-axis = quality bucket, Y-axis = hours driven
- Goal: Maximize hours in highest bucket

**Simplified:**
- Average driver rating (standard 5-star)
- Formula: Sum of all ratings / Number of ratings

**Counter-Metrics:**
- Ride acceptance rate (ensure quality focus doesn't reduce availability)
- Driver churn (ensure standards aren't too harsh)
- Surge pricing frequency (supply/demand balance)

**Validation:**
- Correlate driver ratings with rider retention
- Track tipped drivers' impact on repeat usage
- A/B test driver quality thresholds and measure rider satisfaction

## Related Skills

- **north-star-alignment**: Identifies company-level metrics that proxies should correlate with
- **funnel-metric-mapping**: Places proxy metrics within user lifecycle stages
- **tradeoff-evaluation**: Resolves conflicts when proxies disagree
- **metrics-definition** (workflow): Uses proxy selection as Step 3 in metric definition process
- **goal-setting** (workflow): Validates proxy is movable by team before setting targets

## Integration Points

**Called by workflows:**
- `metrics-definition` - Step 3: Create proxy metrics for each funnel stage
- `dashboard-design` - Step 3: Define measurable indicators per lifecycle stage
- `goal-setting` - Step 2: Validate metric is movable by team

**May call:**
- `north-star-alignment` to ensure proxy correlates with company goals
- `meeting-synthesis` to find customer evidence of what matters

