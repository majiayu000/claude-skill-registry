---
name: experiment-decision
description: Decide when to A/B test vs just ship. Framework for experiment planning and prioritization.
disable-model-invocation: false
user-invocable: true
---

# Experiment Decision Framework: When to A/B Test vs Ship

## Quick Start

```
/experiment-decision
```
Then provide:
1. **What you're considering building** (feature, change, or experiment)
2. **Expected impact** (metric + estimated improvement)
3. **Your concern** (is this risky? reversible? controversial?)

I'll walk you through the decision tree: reversibility, hypothesis
strength, detectable impact, and risk level. You'll get a clear
recommendation: A/B test, ship + monitor, or just ship.

**Output:** Decision documented inline or saved to `outputs/decisions/`
**Time:** ~5 min for clear-cut cases, ~15 min for nuanced decisions

**When to use:** Before building any feature, when stakeholders demand "data-driven" decisions, or when unsure if testing is worth the effort

**Framework source:** Aakash Gupta's "When to A/B Test vs Just Ship"

---

## The Decision Framework

Use this decision tree:

### Question 1: Is it reversible?

**If YES → Ship it**
- CSS changes
- Messaging tweaks
- UI polish
- Non-destructive features

**Why:** Reversible changes have low risk. Ship, monitor, rollback if needed.

**If NO → Continue to Question 2**

---

### Question 2: Do you have a hypothesis with measurable impact?

**If NO → Don't test**
- Building "nice to haves"
- No clear success metric
- Can't measure the outcome

**Why:** Testing without a hypothesis is wasteful. Either clarify the hypothesis or don't build it.

**If YES → Continue to Question 3**

---

### Question 3: Is the expected impact large enough to detect?

**Run a power calculation:**

```
Minimum Detectable Effect (MDE) = Effect you need to see to justify the work

If your feature is expected to improve conversion by 0.5%, but you need 10M users to detect it → Don't test, just ship and monitor
```

**If impact is too small to detect → Ship without test**

**If impact is detectable → Continue to Question 4**

---

### Question 4: Is the risk of being wrong high?

**High risk scenarios:**
- Affects revenue directly (pricing, checkout)
- Impacts core user experience (onboarding, core flows)
- Controversial decision (stakeholder disagreement)
- Large engineering investment

**If HIGH risk → A/B test**

**If LOW risk → Ship without test**

---

## Decision Matrix

| Risk Level | Impact Size | Reversible? | Decision |
|------------|-------------|-------------|----------|
| High | Large | No | **A/B Test** |
| High | Large | Yes | **A/B Test** (or ship with kill switch) |
| High | Small | No | **Don't build** |
| High | Small | Yes | **Ship + Monitor** |
| Low | Large | No | **Ship + Monitor** |
| Low | Large | Yes | **Just Ship** |
| Low | Small | No | **Just Ship** |
| Low | Small | Yes | **Just Ship** |

---

## When to A/B Test

### ✅ Test When:

**1. High-stakes decisions**
- Pricing changes
- Checkout flow modifications
- Core product changes
- Revenue-impacting features

**2. Controversial hypotheses**
- Team is divided on approach
- Stakeholders disagree
- User research is conflicting

**3. Long-term bets**
- Features that are expensive to reverse
- Architectural decisions
- Platform changes

**4. Optimization work**
- Conversion rate improvements
- Engagement optimization
- Retention experiments

---

## When to Just Ship

### ✅ Ship When:

**1. Fast iteration needed**
- Competitive pressure
- Time-sensitive opportunities
- Market windows closing

**2. Low risk, high certainty**
- Bug fixes
- Obvious improvements
- User-requested features (with clear demand)

**3. Qualitative insights are strong**
- Clear user pain validated through research
- Competitive parity features
- Accessibility improvements

**4. Testing would take too long**
- Small user base (can't reach significance)
- Slow conversion cycles (months to convert)
- Complex setup (weeks to build test infrastructure)

---

## The Cost of A/B Testing

**Time costs:**
- Engineering: 2-4 weeks to build test infrastructure
- Analysis: 1-2 weeks to run experiment + analyze
- **Total: 3-6 weeks delay**

**Engineering costs:**
- Feature flagging system
- Analytics instrumentation
- A/A test validation
- Test maintenance

**Opportunity costs:**
- Could have shipped 3-5 other features
- Delayed value delivery to users
- Competitors may ship first

**When testing costs exceed value → Just ship**

---

## Real-World Examples

### Example 1: Amazon's "Add to Cart" Button Color

**Decision: A/B Test**
- High traffic (millions of users)
- Direct revenue impact
- Easy to detect small improvements
- **Result:** +2% conversion = $100M+ annually

---

### Example 2: Slack's Message Threading

**Decision: Just Ship**
- Highly requested feature
- Strong qualitative signal from users
- Reversible (users can ignore threads)
- **Result:** Successful launch, became core feature

---

### Example 3: Netflix's "Are you still watching?" prompt

**Decision: A/B Test**
- Controversial (could annoy users)
- Impact on engagement unclear
- Risk of hurting retention
- **Result:** Test showed improved engagement (prevented zombie sessions)

---

## Common Mistakes

❌ **Testing everything "to be data-driven"**
- Problem: Slows down velocity
- Fix: Reserve tests for high-stakes decisions

❌ **Shipping without monitoring**
- Problem: Bad changes go unnoticed
- Fix: Ship with dashboards and alerts

❌ **Running underpowered tests**
- Problem: Waste time on inconclusive results
- Fix: Calculate sample size before starting

❌ **Testing when qualitative data is clear**
- Problem: Delays obvious improvements
- Fix: Trust strong user research signals

---

## Quick Reference Checklist

Before building any feature, ask:

- [ ] Is this reversible? (If yes → ship)
- [ ] Do I have a clear hypothesis? (If no → don't build)
- [ ] Can I measure the impact? (If no → don't test)
- [ ] Is the expected impact large enough to detect? (Power calculation)
- [ ] What's the risk of being wrong? (High risk → test)
- [ ] What's the cost of testing vs shipping? (ROI check)
- [ ] Do I have strong qualitative data? (If yes → consider shipping)

---

## Statistical Power Guidance

Before committing to an A/B test, estimate whether you have enough traffic to detect a meaningful difference.

### Power Calculation Essentials

**Three inputs you need:**

1. **Minimum Detectable Effect (MDE)** -- what's the smallest improvement worth detecting?
   - For checkout conversion: 1-2% relative change matters (high revenue impact)
   - For feature adoption: 5-10% relative change is typical MDE
   - For engagement metrics: 3-5% relative change is reasonable

2. **Baseline conversion rate** -- what's the current rate you're trying to improve?
   - Higher baselines need more samples to detect small changes
   - Lower baselines are easier to move (but may need larger sample)

3. **Daily traffic to the experiment** -- how many users will enter the test per day?

### Rule of Thumb

**You need approximately 1,000 conversions per variant to detect a 5% relative change at 80% power (95% confidence).**

| Baseline Rate | MDE (Relative) | Conversions Needed Per Variant | At 1K daily visitors, days needed |
|--------------|----------------|-------------------------------|----------------------------------|
| 50% | 5% | ~3,200 | ~7 days |
| 20% | 5% | ~12,500 | ~63 days |
| 5% | 10% | ~15,000 | ~300 days |
| 2% | 10% | ~40,000 | ~800 days |

### When Traffic Is Too Low

If your power calculation shows the test would take longer than 4-6 weeks:

1. **Accept a larger MDE** -- only test if you expect a big swing (15%+ improvement)
2. **Use a composite metric** -- combine multiple success signals into one metric for higher sensitivity
3. **Run a qualitative test** -- 5-10 user tests instead of a statistical A/B test
4. **Just ship and monitor** -- launch with clear success criteria, compare before/after with caveats
5. **Use Bayesian methods** -- more forgiving with small samples, give probability ranges instead of p-values

### Common Pitfalls

- **Peeking at results early** -- checking before reaching sample size inflates false positive rate. Commit to a runtime upfront.
- **Stopping at first significant result** -- random fluctuations can look significant early. Use sequential testing if you must peek.
- **Testing too many variants** -- each variant divides your traffic. Stick to 2-3 variants max.

---

## When to Skip the Framework

Some decisions don't need the full decision tree:

### 1. Regulatory/Compliance Requirement
**Action:** Just ship it. You don't have a choice.
**But:** Document the change, set up monitoring, track any user impact.

### 2. Bug Fix
**Action:** Just fix it. No one A/B tests bug fixes.
**But:** If the "bug fix" changes user behavior significantly, monitor post-fix metrics.

### 3. CEO/Board Mandate
**Action:** Document the decision and ship. Set up measurement so you can report on impact.
**But:** Frame your measurement as "proving the impact" rather than "testing whether to do it." This builds credibility for future data-driven decisions.

### 4. Competitive Response
**Action:** If a competitor just shipped a similar feature and your users are asking for it, speed matters more than experimentation. Ship fast, measure after.
**But:** Don't use "competitive pressure" as an excuse for every feature. Reserve this for genuine market urgency.

### 5. Sunset/Deprecation
**Action:** If you're removing a feature that <1% of users touch, just remove it with advance notice.
**But:** If the feature has any paying customers relying on it, communicate early and provide alternatives.

---

## Output Quality Self-Check

Before delivering the experiment decision, verify:

- [ ] **Decision is clear** -- the recommendation is explicitly "A/B test," "Ship + Monitor," or "Just Ship"
- [ ] **Reversibility** is assessed with specific reasoning (not just "yes/no")
- [ ] **Hypothesis** is stated in If/Then/Because format
- [ ] **Power calculation** is included if recommending a test (MDE, baseline, sample size, duration)
- [ ] **Risk level** is justified with specific stakes (revenue impact, user count affected)
- [ ] **Cost of testing** is weighed against cost of being wrong
- [ ] **Edge cases** are checked (compliance, bug fix, mandate, competitive response)
- [ ] **Stakeholder consensus** is noted -- does the team agree on the approach?
- [ ] **Monitoring plan** exists regardless of decision (even "just ship" needs dashboards)
- [ ] **Next step** is clear -- if testing, what metrics? If shipping, what success criteria?
- [ ] **Connected to past decisions** -- have we made similar decisions before? What happened?

---

## Related Skills

- `/experiment-metrics` - Choose the right metrics to measure
- `/activation-analysis` - Test activation improvements
- `/metrics-framework` - Understand leading vs lagging metrics
- `/define-north-star` - Align tests to North Star

---

**Framework credit:** Adapted from Aakash Gupta's experiment decision frameworks. Read: https://www.news.aakashg.com/p/when-to-ab-test

---

## Context Routing Strategy

When the PM uses `/experiment-decision`, I automatically:

### 1. Check Historical Reversibility Precedent
**Source:** `context-library/decisions/`, past decisions
- **What I look for:** Similar decisions, how reversibility was judged
- **How I use it:** Ensure consistent reversibility assessment
- **Example:** "Last time we shipped CSS changes without testing; this is similar"

### 2. Extract Success Metrics Framework
**Source:** `context-library/metrics/`, active PRDs
- **What I look for:** What metrics you typically measure, variance patterns
- **How I use it:** Calculate minimum detectable effect (MDE) more accurately
- **Example:** "Based on your metrics history, conversion rate variance is 3%, so MDE = 2%"

### 3. Route to Experiment Metrics if Testing
**Source:** Connection to `/experiment-metrics` skill
- **What I look for:** Whether decision routes to testing
- **How I use it:** If decision is "test", auto-suggest next step with `/experiment-metrics`
- **Example:** "Now that you've decided to test, let's pick the right metrics using STEDII"

### 4. Check Stakeholder Consensus on Risk
**Source:** `context-library/stakeholder-template.md`, recent discussions
- **What I look for:** Stakeholder risk tolerance, veto power
- **How I use it:** Surface if high-risk decision needs executive approval
- **Example:** "CEO is risk-averse, so even medium-risk decisions should be tested"

### 5. Calculate Cost of Testing vs Shipping
**Source:** Team capacity, past experiment timelines
- **What I look for:** How long experiments take, engineering cost
- **How I use it:** ROI calculation in the framework
- **Example:** "Last experiment took 3 weeks; if we ship in 1 week and monitor, ROI favors shipping"
