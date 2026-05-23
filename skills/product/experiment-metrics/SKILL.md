---
name: experiment-metrics
description: STEDII framework for selecting trustworthy experiment metrics. Ensures metric validity and reliability.
disable-model-invocation: false
user-invocable: true
---

# Experiment Metrics Selection: STEDII Framework

**When to use:** Before launching any experiment, when metrics feel unreliable, or when experiment results are confusing

**Framework source:** Aakash Gupta's "How to Choose the Right Metrics to Evaluate Experiments"

---

## The STEDII Framework

Choose experiment metrics that are:

1. **S**ensitive
2. **T**imely
3. **E**fficient
4. **D**ebuggable
5. **I**nterpretable
6. **I**solated

---

## 1. Sensitive (Detects Small But Meaningful Changes)

**What it means:** The metric moves when your feature actually improves the experience

**Bad example:**
- Metric: Monthly Active Users (MAU)
- Problem: Too coarse. A good onboarding improvement might not move MAU for months.

**Good example:**
- Metric: Day 7 activation rate
- Why: Sensitive enough to detect onboarding improvements within a week

**How to check:**
Ask: "If this experiment succeeds, will this metric move within the experiment window?"

**Common mistake:** Using metrics that are too aggregated (MAU, total revenue) when you need something more granular (daily activation, conversion rate by cohort).

---

## 2. Timely (Results Available Quickly)

**What it means:** You get signal fast enough to make decisions

**Bad example:**
- Metric: 90-day retention
- Problem: Takes 90 days to know if your experiment worked

**Good example:**
- Metric: Day 7 retention + leading indicators
- Why: Faster feedback, correlates with long-term retention

**Tradeoff alert:** Sometimes you NEED slow metrics (LTV, annual retention). In those cases:
- Use leading indicators to get fast signal
- Run smaller experiments to validate
- Accept longer experiment duration for critical decisions

**How to check:**
Ask: "Can I get actionable results within [1 week / 2 weeks / 1 month]?"

---

## 3. Efficient (High Statistical Power)

**What it means:** You can detect the effect with reasonable sample size and time

**Bad example:**
- Metric: Revenue per user
- Problem: High variance, need massive sample sizes

**Good example:**
- Metric: Conversion rate
- Why: Lower variance, reaches significance faster

**Statistical power explained:**
- Power = ability to detect a real effect
- Higher variance metrics = lower power = longer experiments
- Formula: Sample size needed ∝ (Variance / Expected Effect Size)²

**How to check:**
Run a power calculation:
```
Minimum sample size = (Z + Z)² × (σ² / δ²)
Where:
- Z = confidence level (usually 1.96 for 95%)
- σ = standard deviation of metric
- δ = minimum detectable effect
```

**Practical tip:** If you need >1M users to detect a 5% lift, your metric isn't efficient enough.

---

## 4. Debuggable (Easy to Diagnose Issues)

**What it means:** When something goes wrong, you can figure out why

**Bad example:**
- Metric: "Engagement score" (black box formula)
- Problem: If it drops, you don't know what broke

**Good example:**
- Metric: Click-through rate (CTR)
- Why: Simple, transparent, easy to debug

**How to check:**
Ask: "If this metric tanks, can I quickly understand what happened?"

**What makes metrics debuggable:**
- ✅ Simple calculations
- ✅ Can be broken down by segments
- ✅ Can view user-level data
- ✅ Clear numerator and denominator

**Red flags:**
- ❌ Proprietary "engagement scores"
- ❌ Complex weighted formulas
- ❌ Metrics with 5+ variables
- ❌ Black box ML model outputs

---

## 5. Interpretable (Easy to Understand and Explain)

**What it means:** Stakeholders can understand what the metric represents

**Bad example:**
- Metric: "Quality-adjusted sessions per visitor"
- Problem: What does "quality-adjusted" mean?

**Good example:**
- Metric: "% of users who complete onboarding"
- Why: Crystal clear what it measures

**The grandma test:** Can you explain this metric to your grandma? If not, it fails interpretability.

**How to check:**
- Can you explain it in one sentence?
- Would a new PM understand it immediately?
- Can executives grasp it without training?

---

## 6. Isolated (Measures Only What You Changed)

**What it means:** The metric moves because of your experiment, not external factors

**Bad example:**
- Metric: Total signups
- Problem: Could move due to marketing campaigns, seasonality, competitor changes

**Good example:**
- Metric: Signup conversion rate (for signup flow experiment)
- Why: Isolated to the signup flow you're testing

**Common isolation failures:**
- Network effects (social features affect all users)
- Cross-contamination (treatment bleeds to control)
- Seasonality (holiday effects)
- Marketing campaigns running simultaneously

**How to check:**
Ask: "Could something OTHER than my experiment cause this metric to move?"

---

## How to Use This Framework

### Step 1: List Your Candidate Metrics

```
Use /experiment-metrics

I'm running an experiment to: [describe your experiment]

Help me brainstorm 5-10 candidate metrics we could measure.
```

---

### Step 2: Score Each Metric Against STEDII

Create a table:

| Metric | Sensitive? | Timely? | Efficient? | Debuggable? | Interpretable? | Isolated? | Total Score |
|--------|------------|---------|------------|-------------|----------------|-----------|-------------|
| Metric 1 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 2/3 | 15/18 |
| Metric 2 | 3/3 | 1/3 | 3/3 | 2/3 | 3/3 | 3/3 | 15/18 |

Scoring:
- 3 = Excellent
- 2 = Acceptable
- 1 = Poor
- 0 = Fails this criterion

---

### Step 3: Select Primary + Guardrail Metrics

**Primary metric:** The ONE metric your experiment is designed to move
- Should score 15+/18 on STEDII
- The metric you'll make decisions on

**Guardrail metrics (3-5):** Metrics you DON'T want to hurt
- Revenue (don't tank it)
- Core engagement (don't break the product)
- Quality metrics (don't hurt user experience)

**Example:**
- **Primary:** Day 7 activation rate
- **Guardrails:** Revenue per user, Daily active users, Customer satisfaction score, Page load time

---

### Step 4: Run Pre-Experiment Checks

Before launching:

1. **A:A Test** - Run experiment with no actual change
   - Both groups should be identical
   - If metrics differ, you have a setup problem

2. **Sample Ratio Check** - Verify 50/50 split is actually 50/50
   - If you see 52/48 or worse, investigate

3. **Metric Stability** - Check historical variance
   - High variance = longer experiment needed

---

## Common Metric Selection Mistakes

### Mistake #1: Using Only One Metric

**Problem:** Optimize one thing, break another

**Solution:** Always have guardrail metrics
- Primary: what you're trying to improve
- Guardrails: what you don't want to hurt

---

### Mistake #2: Confusing Leading and Lagging Metrics

**Lagging metrics:**
- Slow to respond
- Ultimate outcome you care about
- Example: LTV, annual retention, NPS

**Leading metrics:**
- Fast signal
- Predictive of lagging metrics
- Example: Day 7 retention, activation rate

**Best practice:** Use leading metrics to get fast signal, validate with lagging metrics on a sample.

---

### Mistake #3: Metric Dilution

**Problem:** Testing a small feature but measuring site-wide metrics

**Example:**
- Test: New checkout button color
- Metric: Monthly revenue
- Issue: Only 5% of users even see checkout, signal is too diluted

**Solution:** Measure metrics scoped to exposed users
- Better metric: Revenue per checkout visitor
- Or: Conversion rate (checkout started → completed)

---

### Mistake #4: Simpson's Paradox

**Problem:** Aggregate metric moves one way, segments move the opposite way

**Example:**
- Overall conversion rate: +5% ✅
- Mobile conversion: -10% ❌
- Desktop conversion: -5% ❌
- Why? More cheap mobile traffic shifted the mix

**Solution:** Always segment your metrics (new vs returning, mobile vs desktop, etc.)

---

## Real-World Examples

### Example 1: Netflix Thumbnail Test

**Experiment:** Testing new thumbnail images

**Bad metric:** Monthly viewing hours
- Not sensitive (too aggregated)
- Not timely (takes too long)
- Not isolated (affected by content releases)

**Good metric:** Click-through rate on thumbnails
- Sensitive: Directly measures thumbnail appeal
- Timely: Results in 1-2 days
- Efficient: Lots of impressions = fast significance
- Debuggable: Can see which thumbnails work
- Interpretable: "% of people who click"
- Isolated: Measures only thumbnail change

---

### Example 2: Booking.com Pricing Test

**Experiment:** Showing "Only 2 rooms left!" urgency message

**Bad metric:** Bookings per visitor
- Not efficient (high variance)
- Not timely (slow conversion cycle)

**Good metrics:**
- Primary: Booking conversion rate
- Guardrail: Customer satisfaction (don't annoy users)
- Guardrail: Return visit rate (don't hurt trust)

**Result:** +2.5% conversion, but -5% satisfaction and -3% return visits
**Decision:** Don't ship. Guardrails caught a bad long-term tradeoff.

---

## Quick Reference: Metric Selection Checklist

Before you launch an experiment, verify:

- [ ] **Primary metric clearly defined**
  - What are you measuring?
  - How is it calculated?
  - What's the minimum detectable effect?

- [ ] **STEDII checklist passed**
  - [ ] Sensitive enough to detect improvements
  - [ ] Results available within [X] days
  - [ ] Sample size achievable
  - [ ] Can be debugged if issues arise
  - [ ] Stakeholders understand it
  - [ ] Isolated from external factors

- [ ] **Guardrails defined (3-5 metrics)**
  - Revenue metrics
  - Engagement metrics
  - Quality metrics

- [ ] **Statistical plan complete**
  - Significance level (usually 95%)
  - Minimum sample size calculated
  - Experiment duration estimated
  - A:A test passed

- [ ] **Segmentation plan**
  - How will you break down results?
  - New vs returning users
  - Mobile vs desktop
  - Geographic segments

---

## Related Skills

- `/experiment-decision` - Decide when to A/B test vs ship
- `/metrics-framework` - Understand leading vs lagging metrics
- `/define-north-star` - Choose your North Star Metric
- `/retention-analysis` - Measure long-term impact

---

**Framework credit:** Adapted from Aakash Gupta's STEDII framework. Read the full article: https://www.news.aakashg.com/p/metrics-experiments

---

## Context Routing Strategy

When the PM uses `/experiment-metrics`, I automatically:

### 1. Pull Metrics from PRDs & Strategy
**Source:** `context-library/prds/`, success metrics defined there
- **What I look for:** Feature's pre-defined success metrics, targets
- **How I use it:** Pre-populate primary and secondary metrics for STEDII evaluation
- **Example:** "Your PRD says success = conversion >60%, let's test if that's STEDII-compliant"

### 2. Query Analytics MCPs for Historical Data
**Source:** Amplitude, Mixpanel, Posthog (if connected)
- **What I look for:** Variance of potential metrics, time-to-signal data
- **How I use it:** Validate metrics are Sensitive and Timely with real data
- **Example:** "Metric X has 12% variance historically, so needs N=5000 sample size"

### 3. Check for Metric Conflicts with Guardrails
**Source:** `context-library/metrics/`, company guardrails
- **What I look for:** Metrics that must not decline, company KPIs
- **How I use it:** Ensure secondary metrics include guardrails
- **Example:** "NPS is a company guardrail, must include in secondary metrics"

### 4. Reference Past Experiments for Benchmarks
**Source:** `context-library/metrics/`, A/B test results
- **What I look for:** What worked in past experiments, surprising metric learnings
- **How I use it:** Suggest metrics that detected real impacts before
- **Example:** "In past experiments, page load time was poorly Sensitive, don't use it"

### 5. Route to Experiment Decision Framework
**Source:** Connection to `/experiment-decision` skill
- **What I look for:** Is testing even the right call?
- **How I use it:** If you should ship without testing, auto-flag before selecting metrics
- **Example:** "CSS changes are reversible, don't need this full STEDII analysis"

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **Context was checked:** Reviewed `context-library/metrics/` for existing experiments and baselines, and `context-library/prds/` for pre-defined success metrics
- [ ] **Each metric evaluated against all 6 STEDII dimensions:** Every candidate metric has a score (0-3) for Sensitive, Timely, Efficient, Debuggable, Interpretable, and Isolated, with reasoning for each score
- [ ] **Sample size requirements calculated:** The output includes a minimum sample size estimate for the primary metric based on expected effect size and variance
- [ ] **Metric sensitivity analysis included:** The output states whether the expected change is detectable given current traffic, variance, and experiment duration
- [ ] **Guardrail metrics identified:** At least 3 guardrail metrics are defined with acceptable ranges to prevent unintended harm
- [ ] **No vanity metrics without justification:** If any metric could be considered a vanity metric (e.g., page views, total signups), the output explains why it is valid for this specific experiment
