---
name: growth-experimenter
description: Run systematic growth experiments to increase acquisition, activation, retention, and revenue. Use when optimizing conversion funnels, running A/B tests, improving metrics, or when users mention growth, experimentation, optimization, or scaling user acquisition.
license: Complete terms in LICENSE.txt
---

# Growth Experimenter

Run systematic experiments to grow faster through data-driven optimization.

## Core Philosophy

**Growth = Experimentation Velocity × Win Rate × Impact per Win**

- Run more experiments
- Increase your hit rate through better hypotheses
- Focus on high-impact areas

## Growth Model (AARRR / Pirate Metrics)

```
Acquisition → Activation → Retention → Revenue → Referral
    ↓             ↓            ↓          ↓         ↓
  Traffic      Sign Up      Day 30    Upgrade   Invites
  100%          40%          50%        20%       10%

Example: 10,000 visitors/month
→ 4,000 signups (40%)
→ 2,000 active at D30 (50%)
→ 400 paying (20%)
→ 40 referrals (10%)

Improve ANY metric by 10% = 10% more customers
```

**Where to focus first**: The leakiest bucket

- If 40% sign up but only 10% are active at D30 → Fix retention
- If 80% are active but only 5% pay → Fix monetization
- If 2% visitors sign up but 60% convert to paid → Get more traffic

## Experiment Framework

### 1. Identify the Problem

**Good problem statements**:

- "Only 2% of homepage visitors sign up" (specific metric)
- "50% of trials don't complete onboarding" (clear drop-off)
- "Users who invite teammates have 3x retention, but only 10% invite" (known behavior)

**Bad problem statements**:

- "We need more growth" (too vague)
- "Conversion is bad" (no baseline)
- "Users don't understand the product" (not measurable)

### 2. Form a Hypothesis

**Hypothesis template**:

```
We believe that [change]
will result in [outcome]
because [reason/evidence]
```

**Examples**:

```markdown
✅ Good:
We believe that adding social proof (testimonials) to the pricing page
will increase trial signups by 10%
because visitors currently have low trust and need validation.

✅ Good:
We believe that sending a Slack notification when user completes setup
will increase D7 activation by 20%
because users forget to come back after initial signup.

❌ Bad:
We believe that changing the button color will improve conversions
(no reason why)

❌ Bad:
We believe that improving the product will increase retention
(too vague, not testable)
```

### 3. Design the Experiment

**Experiment specification**:

```yaml
Experiment: Add social proof to pricing page

Hypothesis: Social proof on pricing will increase signups by 10%

Variants:
  Control: Current pricing page (no testimonials)
  Treatment: Pricing page + 3 customer testimonials

Primary Metric: Trial signup rate
Secondary Metrics:
  - Time on page
  - Scroll depth
  - CTA click rate

Sample Size: 1,000 visitors per variant
Duration: 2 weeks (or until statistical significance)
Success Criteria: >5% improvement with 95% confidence

Measurement:
  - Google Analytics
  - Mixpanel conversion tracking
  - Segment for event data
```

### 4. Run the Experiment

**A/B testing checklist**:

- [ ] Random assignment (50/50 split)
- [ ] Same time period (no day-of-week effects)
- [ ] Sufficient sample size
- [ ] No peeking (wait for significance)
- [ ] One change at a time

**Statistical significance calculator**:

```javascript
// Minimum sample size for 95% confidence
function calculateSampleSize(baseline, mde, power = 0.8, alpha = 0.05) {
  // baseline = current conversion rate (e.g., 0.02)
  // mde = minimum detectable effect (e.g., 0.10 for 10% lift)
  // Returns: visitors needed per variant

  const z_alpha = 1.96 // 95% confidence
  const z_power = 0.84 // 80% power

  const p1 = baseline
  const p2 = baseline * (1 + mde)
  const p_avg = (p1 + p2) / 2

  const n = (2 * p_avg * (1 - p_avg) * (z_alpha + z_power) ** 2) / (p2 - p1) ** 2

  return Math.ceil(n)
}

// Example: 2% baseline, detect 10% improvement
calculateSampleSize(0.02, 0.1) // ~35,000 visitors per variant
```

### 5. Analyze Results

**Interpreting results**:

```yaml
Control: 1,000 visitors → 20 conversions (2.0%)
Treatment: 1,000 visitors → 25 conversions (2.5%)

Lift: +25% relative (+0.5% absolute)
P-value: 0.04 (statistically significant if <0.05)
Confidence Interval: [-0.2%, +1.2%]

Decision: WIN - Ship it!
```

**When results are inconclusive**:

- **No movement**: Hypothesis was wrong or change too small
- **Not significant**: Need more data or larger effect
- **Negative impact**: Roll back immediately
- **Contradictory secondary metrics**: Investigate trade-offs

### 6. Scale What Works

```javascript
// After successful experiment, roll out to 100%
if (experimentResult.lift > 0.05 && experimentResult.pValue < 0.05) {
  rolloutFeature({
    feature: 'social_proof_on_pricing',
    rollout: '100%',
    monitor: ['signup_rate', 'trial_starts']
  })

  // Log the learning
  logExperimentLearning({
    learning: 'Social proof increased signups by 25%',
    application: 'Add social proof to all high-intent pages'
  })
}
```

## Growth Experiments by Stage

### Acquisition Experiments

**Goal**: Get more traffic or improve traffic quality

**High-impact experiments**:

1. **Landing page optimization**:

```yaml
Control: Generic homepage
Test: Tailored landing pages by traffic source
  - /for-startups (Product Hunt traffic)
  - /for-agencies (Google Ads)
  - /for-developers (GitHub referrals)

Expected lift: 20-50% on signup rate
```

2. **Headline testing**:

```yaml
Current: 'Project Management Software'
Test A: 'Ship Projects 2x Faster'
Test B: 'The Project Management Tool Teams Love'
Test C: "Finally, Project Management That Doesn't Suck"

Test: Value prop clarity, specificity, emotion
Expected lift: 10-30% on engagement
```

3. **Social proof**:

```yaml
Current: No social proof
Test: Add testimonials, logos, user count
  - "Join 10,000+ teams..."
  - Customer logos (recognizable brands)
  - Video testimonial from power user

Expected lift: 15-25% on trust/signups
```

### Activation Experiments

**Goal**: Get users to "aha moment" faster

**High-impact experiments**:

1. **Onboarding simplification**:

```yaml
Current: 7-step onboarding flow
Test: 3-step flow, delay advanced setup
  Step 1: Name + email
  Step 2: Create first project
  Step 3: Invite team (optional, skippable)

Expected lift: 30-50% completion rate
```

2. **Time-to-value reduction**:

```yaml
Current: Users must create project from scratch
Test: Pre-populated template
  - Sample project with tasks
  - Example data to explore
  - Guided tutorial

Expected lift: 25-40% in D1 activation
```

3. **Progress indicators**:

```yaml
Current: No feedback during setup
Test: Progress bar + completion checklist
  [✓] Account created
  [✓] First project
  [ ] Invite teammates (2 left)
  [ ] Complete first task

Expected lift: 15-25% completion rate
```

### Retention Experiments

**Goal**: Keep users coming back

**High-impact experiments**:

1. **Email re-engagement**:

```yaml
Current: No emails after signup
Test: 3-email onboarding sequence
  Day 1: "Here's how to get started"
  Day 3: "Tips from power users"
  Day 7: "You're only 1 step away from [value]"

Expected lift: 20-35% in D30 retention
```

2. **Habit building**:

```yaml
Current: No reminders
Test: Daily digest email
  "Your daily update: 3 tasks due today"
  - Creates daily habit
  - Drives return visits

Expected lift: 25-40% in daily active users
```

3. **Feature discovery**:

```yaml
Current: All features visible, overwhelming
Test: Progressive disclosure
  - Week 1: Core features only
  - Week 2: Unlock integrations
  - Week 3: Unlock advanced features
  - Tooltip hints for new features

Expected lift: 15-25% feature adoption
```

### Revenue Experiments

**Goal**: Convert free users to paying customers

**High-impact experiments**:

1. **Paywall optimization**:

```yaml
Current: Hard limit at 5 projects
Test: Soft limit + banner
  "You've created 5 projects! Upgrade to Pro for unlimited"
  - Allow them to continue
  - Show banner on every page
  - Show upgrade modal on 6th project

Expected lift: 20-30% in upgrade rate
```

2. **Trial length**:

```yaml
Current: 14-day trial
Test A: 7-day trial (more urgency)
Test B: 30-day trial (more time to get hooked)
Test C: Usage-based trial (100 tasks)

Expected: Depends on product complexity
```

3. **Pricing page**:

```yaml
Current: 3 tiers without highlight
Test: Highlight "Most Popular" tier
  - Green border
  - "Most popular" badge
  - Slightly larger

Expected lift: 10-20% on middle tier selection
```

### Referral Experiments

**Goal**: Turn users into advocates

**High-impact experiments**:

1. **Invite mechanics**:

```yaml
Current: "Invite" link in settings
Test: Contextual invite prompts
  - After completing first task: "Invite your team to help!"
  - When tagging someone: "user@example.com isn't on your team yet. Invite them?"

Expected lift: 50-100% in invites sent
```

2. **Referral incentives**:

```yaml
Current: No incentive
Test: Double-sided reward
  - Referrer: 1 month free
  - Referred: 20% off first year
  - Must convert to paid

Expected lift: 30-50% in referred signups
```

3. **Public profiles**:

```yaml
Current: All projects private
Test: Optional public project sharing
  - "Made with [Product]" badge
  - Share project publicly
  - View-only link with signup CTA

Expected lift: 10-20% referred traffic
```

## Advanced Techniques

### Sequential Testing

When traffic is low, use sequential testing instead of fixed-sample A/B:

```python
def sequential_test(control_conversions, control_visitors,
                    test_conversions, test_visitors):
    """
    Evaluate experiment continuously instead of waiting for sample size.
    Stop early if clear winner or clear loser.
    """
    log_likelihood_ratio = calculate_llr(
        control_conversions, control_visitors,
        test_conversions, test_visitors
    )

    if log_likelihood_ratio > 2.996:  # 95% confidence winner
        return "WINNER"
    elif log_likelihood_ratio < -2.996:  # 95% confidence loser
        return "LOSER"
    else:
        return "CONTINUE"
```

### Multi-Armed Bandit

Automatically allocate more traffic to winning variants:

```python
class MultiArmedBandit:
    def select_variant(self, variants):
        """
        Thompson Sampling:
        - Start with equal probability
        - As data comes in, shift traffic to winners
        - Explore new variants occasionally
        """
        samples = []
        for v in variants:
            # Sample from beta distribution
            sample = np.random.beta(
                v.successes + 1,
                v.failures + 1
            )
            samples.append(sample)

        return variants[np.argmax(samples)]
```

### Cohort Analysis

Segment results by user attributes:

```yaml
Overall lift: +10%

By segment:
  Mobile users: +25%  (big win!)
  Desktop users: +2%   (no effect)
  Organic traffic: +30%  (huge!)
  Paid traffic: -5%   (negative!)

Action: Roll out to mobile + organic only
```

### North Star Metric

Define one metric that represents customer value:

```yaml
Examples:
  Slack: Weekly Active Users (WAU)
  Airbnb: Nights Booked
  Facebook: Daily Active Users (DAU)
  Spotify: Time Listening
  Shopify: GMV (Gross Merchandise Value)

Your North Star should: ✅ Correlate with revenue
  ✅ Measure value delivery
  ✅ Be measurable frequently
  ✅ Rally the entire team
```

## Experiment Ideas Library

### Quick Wins (1 week effort)

```yaml
1. Homepage CTA text: "Start Free Trial" vs "Get Started Free"
2. Signup button color: Blue vs Green vs Red
3. Email subject lines: A/B test 2 variations
4. Pricing page order: Starter-Pro-Business vs Business-Pro-Starter
5. Social proof location: Above fold vs below fold
```

### Medium Effort (2-4 weeks)

```yaml
1. Redesign onboarding flow (reduce steps)
2. Add email drip campaign
3. Create upgrade prompts in-app
4. Build referral program
5. Redesign pricing page
```

### Big Bets (1-3 months)

```yaml
1. Launch freemium model
2. Build marketplace/app store
3. Add AI-powered features
4. Redesign entire product (better UX)
5. Build mobile apps
```

## Experiment Tracking

### Document Every Experiment

```yaml
Experiment Log:

Exp-001:
  Name: Add social proof to homepage
  Start Date: 2024-01-15
  End Date: 2024-02-01
  Status: ✅ WIN
  Hypothesis: Social proof will increase signups by 10%
  Result: +18% signup rate, p=0.02
  Learnings: Customer logos work better than testimonials
  Actions: Roll out to 100%, add logos to pricing page too

Exp-002:
  Name: 7-day trial instead of 14-day
  Start Date: 2024-02-05
  Status: ❌ LOSS
  Hypothesis: Shorter trial creates urgency
  Result: -12% trial-to-paid conversion, p=0.01
  Learnings: Users need more time to integrate product
  Actions: Keep 14-day trial, don't test shorter

Exp-003:
  Name: Onboarding simplification
  Start Date: 2024-02-15
  Status: ⏳ RUNNING
  Hypothesis: 3-step flow will improve completion by 30%
  Current: +22% completion, n=850, p=0.08 (not yet significant)
```

### Experiment Prioritization

**ICE Score Framework**:

```yaml
Impact (1-10): How much could this move the needle?
Confidence (1-10): How sure are we it will work?
Ease (1-10): How easy is it to implement?

Score = (Impact × Confidence × Ease) / 100

Example:
  Experiment: Add testimonials to homepage
  Impact: 7 (could boost signups 15-20%)
  Confidence: 8 (social proof is proven)
  Ease: 9 (just add HTML)
  ICE Score: 504 / 100 = 5.04

Sort by ICE score, run highest first
```

## Growth Metrics Dashboard

```typescript
interface GrowthMetrics {
  // Acquisition
  traffic_sources: {
    organic: number
    paid: number
    referral: number
    direct: number
  }
  cost_per_click: number
  cost_per_signup: number

  // Activation
  signup_to_activation_rate: number
  time_to_activation_p50: string // "2 days"
  onboarding_completion_rate: number

  // Retention
  dau: number // Daily Active Users
  wau: number // Weekly Active Users
  mau: number // Monthly Active Users
  dau_mau_ratio: number // Stickiness (should be >20%)
  churn_rate_monthly: number
  retention_d1: number
  retention_d7: number
  retention_d30: number

  // Revenue
  trial_to_paid_conversion: number
  average_revenue_per_user: number
  customer_lifetime_value: number
  ltv_cac_ratio: number

  // Referral
  referral_invites_sent: number
  viral_coefficient: number // Should be >1 for viral growth
  nps: number // Net Promoter Score

  // Experiments
  active_experiments: number
  experiments_shipped_this_month: number
  win_rate: number // % experiments that improve metrics
}
```

## Common Pitfalls

❌ **Testing too many things at once**: Change one variable at a time
❌ **Stopping test too early**: Wait for statistical significance
❌ **Ignoring segments**: Results vary by user type/traffic source
❌ **P-hacking**: Don't cherry-pick favorable metrics
❌ **Small sample sizes**: Need 1,000+ conversions per variant minimum
❌ **Seasonal effects**: Don't test during holidays/anomalies
❌ **Novelty effect**: Some changes work for 2 weeks then regress

## Quick Start Checklist

### Week 1: Foundation

- [ ] Set up analytics (Mixpanel, Amplitude, GA4)
- [ ] Define North Star Metric
- [ ] Map current funnel (AARRR)
- [ ] Identify biggest leak in funnel
- [ ] Set up A/B testing tool (Optimizely, VWO, Google Optimize)

### Week 2-3: First Experiments

- [ ] Run 3 quick-win experiments
- [ ] Document results in spreadsheet
- [ ] Pick one big-bet experiment to design
- [ ] Calculate required sample sizes

### Ongoing

- [ ] Run 5-10 experiments per month
- [ ] Review metrics weekly
- [ ] Document all learnings
- [ ] Focus on highest-ICE experiments
- [ ] Ship winning experiments to 100%

## Summary

Great growth teams:

- ✅ Run 10+ experiments per month (high velocity)
- ✅ Focus on one North Star Metric
- ✅ Document everything (wins and losses)
- ✅ Prioritize by ICE score
- ✅ Wait for statistical significance
- ✅ Scale what works, kill what doesn't
