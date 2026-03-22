---
name: metrics-framework
description: Set up leading vs lagging indicators for product decisions. Framework for metric selection and tracking.
disable-model-invocation: false
user-invocable: true
---

# Metrics Framework: Leading vs Lagging Indicators

**When to use:** Setting up metrics, designing dashboards, or when you need early signal before outcomes materialize

**Framework source:** Aakash Gupta's "Become an A/B Testing Expert" and metrics guidance

## Quick Start

1. Tell me: "Help me build a metrics framework for [product/feature]"
2. I will check `context-library/strategy/` for your North Star and `context-library/metrics/` for baseline data
3. I will ask about your North Star (lagging metric), product stage, and decision speed needs
4. We build a metric hierarchy: Lagging (quarterly) -> Leading (weekly) -> Input (daily)
5. For each key metric, we define alert thresholds (green/yellow/red) and a dashboard layout
6. Output goes to `outputs/metrics-framework-[date].md`

**Key principle:** Leading metrics should PREDICT lagging metrics. If they do not, you are tracking the wrong thing. We always validate the correlation before committing to a leading indicator.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Strategy Context | `context-library/strategy/*.md` | North Star, objective, business goal | Company-wide lagging metric target |
| Business Model | `context-library/business-info-template.md` | metrics, KPIs, growth model | Current revenue/retention/growth focus |
| Metrics History | `context-library/metrics/*.md` | baseline, trends, benchmarks | Historical leading/lagging metric data |
| PRDs | `context-library/prds/*.md` | success metrics, measurement | Feature-level metric definitions |
| Meetings | `context-library/meetings/*.md` | "metrics", "dashboard", "KPI" | Stakeholder metric priorities |

**Context Priority:**
1. Business strategy and North Star FIRST
2. Current product metrics and baselines SECOND
3. Historical trend data THIRD
4. Feature-specific metrics FOURTH

**Cross-Skill Links:**
- If defining North Star → Link to `/define-north-star`
- If setting up feature success → Link to `/feature-metrics` for STEDII framework
- If tracking product health → Link to `/retention-analysis` and `/activation-analysis`
- If analyzing test results → Link to `/feature-results`

---

## Step 0: Understanding Your Metric System

Before designing your metrics framework, let me understand what you're optimizing for...

**Checking:**
- `context-library/business-info-template.md` for business model and goals
- `context-library/strategy/*.md` for strategic priorities
- `context-library/metrics/` for existing metric baselines
- `context-library/prds/` for current feature success metrics

**Based on what I find, I'll show you:**

### Your Current Metric Health

**North Star / Lagging Metric:**
- [Current North Star metric from strategy]
- [Baseline value: X]
- [Target: Y by when]

**Existing Leading Indicators:**
- [What you're already tracking]
- [Historical effectiveness: does this predict the lagging metric?]

**Metric Gaps:**
- [Metrics you're missing that would help you move faster]
- [Decision-making gaps: where you're flying blind]

### PM-Specific Diagnosis Questions

1. **Decision Speed:** How long do you need to make go/no-go decisions? (Days vs weeks vs months)
2. **Product Stage:** Are you focused on growth, retention, monetization, or operational efficiency?
3. **Team Alignment:** Do different teams use different success metrics? (Problem!)
4. **Data Quality:** Do you have reliable tracking for the metrics you care about?
5. **Stakeholder Expectations:** Does your executive team care about your current metrics?

---

---

## Leading vs Lagging Metrics

### Lagging Metrics (Outcome Indicators)

**Definition:** Metrics that measure final outcomes - what already happened

**Characteristics:**
- Slow to respond
- High certainty (accurate)
- Ultimate measure of success
- Hard to influence directly

**Examples:**
- Revenue
- Customer lifetime value (LTV)
- Annual retention rate
- Net Promoter Score (NPS)
- Market share
- Profit margins

**When to use:**
- Board reporting
- Annual/quarterly goals
- Validating long-term bets
- Measuring ultimate success

---

### Leading Metrics (Predictive Indicators)

**Definition:** Metrics that predict future outcomes - early signals

**Characteristics:**
- Fast to respond
- Lower certainty (probabilistic)
- Actionable in real-time
- Directly influenceable

**Examples:**
- Day 7 activation rate (predicts retention)
- Weekly active users (predicts revenue)
- Feature adoption rate (predicts stickiness)
- Time to first value (predicts churn)
- Support ticket volume (predicts satisfaction)

**When to use:**
- Day-to-day decisions
- Experiment evaluation
- Early problem detection
- Sprint planning

---

## The Connection

**Leading metrics should PREDICT lagging metrics.**

If they don't, you're tracking the wrong leading metrics.

### Example 1: E-commerce

**Lagging:** Monthly revenue
**Leading:**
- Add-to-cart rate (faster signal)
- Checkout start rate
- Payment success rate

**Logic:** If add-to-cart drops today, revenue drops next week.

---

### Example 2: SaaS Product

**Lagging:** 90-day retention
**Leading:**
- Day 7 activation rate
- Weekly active usage
- Feature adoption in first 14 days

**Logic:** Users who activate in 7 days have 10x better 90-day retention.

---

### Example 3: Marketplace

**Lagging:** GMV (Gross Merchandise Value)
**Leading:**
- Search-to-view rate
- View-to-cart rate
- Seller response time
- Inventory depth

**Logic:** More searches + better inventory = more transactions = higher GMV

---

## How to Identify Your Leading Metrics

### Step 1: Start with Your North Star (Lagging Metric)

What's the ultimate outcome you care about?

Examples:
- Revenue
- User retention
- Engagement
- Customer satisfaction

---

### Step 2: Work Backwards to Find Predictors

Use this prompt pattern:

```
Use /metrics-framework and reference context-library/business-info-template.md

Our North Star / main outcome metric is: [your lagging metric]

Help me identify 3-5 leading indicators that:
1. Happen BEFORE this outcome
2. Predict this outcome with data
3. Are actionable (we can influence them)
4. Give us signal within 1-2 weeks

Our product: [describe product]
User journey: [describe key actions]
Current metrics: [what you track today]
```

---

### Step 3: Validate the Correlation

**Run analysis to prove the connection:**

1. **Cohort analysis:**
   - Users with high leading metric → retention/revenue outcome
   - Users with low leading metric → churn outcome

2. **Time-series correlation:**
   - Leading metric moves up Week 1
   - Lagging metric moves up Week 4-6
   - Correlation coefficient > 0.7

**If no correlation exists, it's not a leading indicator.**

### Minimum Data Quality Bar

Before trusting any correlation between leading and lagging metrics:

**Minimum thresholds:**
- **Sample size:** At least 1,000 users (or 100 accounts for B2B) in each comparison group
- **Time period:** At least 6 weeks of data (2 full product cycles minimum)
- **Event frequency:** Each user should have 5+ events of the measured behavior (avoid drawing conclusions from single actions)
- **Segment stability:** The user segments being compared should be stable (not changing composition) during the measurement period

**Data quality red flags:**
- Correlation based on fewer than 500 users -- mark as "Directional only, not statistically reliable"
- Correlation from a single week of data -- mark as "Preliminary, needs confirmation over 4+ weeks"
- Correlation that only holds for one segment but not others -- note the segment-specific caveat
- Correlation that reverses direction when a confounding variable is controlled for -- do not report as a finding

**How to communicate data quality:**
- High confidence: "Based on 3,200 users over 8 weeks, X predicts Y with r=0.72"
- Medium confidence: "Directional signal from 800 users over 4 weeks. Needs more data to confirm."
- Low confidence: "Preliminary observation from 200 users. Not yet actionable."

---

## Metric Hierarchy

Build a metric tree from lagging → leading:

```
LAGGING (Outcome)
    ↑
LEADING (Predictive)
    ↑
INPUT METRICS (Drivers)
```

### Example: Slack

**Tier 1 - Lagging (Annual):**
- Revenue
- Logo retention

**Tier 2 - Leading (Monthly):**
- Monthly Active Teams (MAT)
- Teams sending 2,000+ messages

**Tier 3 - Input Metrics (Weekly):**
- Weekly Active Users
- Messages sent per user
- Channels created
- Integrations added

**Tier 4 - Activation Metrics (Daily):**
- Day 1 setup completion
- First message sent
- Team invites sent

**How it works:**
- Day 1 activation → predicts Week 1 usage
- Week 1 usage → predicts Month 1 engagement
- Month 1 engagement → predicts annual retention
- Annual retention → drives revenue

---

## Dashboard Design

**Problem:** Most dashboards show only lagging metrics

**Solution:** Split your dashboard into sections:

### 1. North Star (Top of Dashboard)
- The ONE lagging metric that matters most
- Monthly/Quarterly trend

### 2. Leading Indicators (Middle)
- 3-5 metrics that predict North Star
- Weekly trends
- Alert thresholds

### 3. Input Metrics (Bottom)
- 5-10 levers you can pull
- Daily/Weekly monitoring
- Team-specific metrics

### Example Dashboard: SaaS Product

**North Star:**
- 📊 MRR (Monthly Recurring Revenue): $250K (+12% MoM)

**Leading Indicators:**
- ⚡ Weekly Active Accounts: 2,500 (+8% WoW)
- ⚡ Day 7 Activation Rate: 45% (+5pp vs last week)
- ⚡ Feature Adoption (core feature): 72% (+3pp)

**Input Metrics:**
- Signups this week: 320
- Setup completion rate: 75%
- Time to first value: 8 minutes (median)
- Support tickets: 45 (-10 vs last week)
- Invited users per account: 3.2 avg

---

## Real-World Examples

### Netflix

**Lagging:** Subscriber growth, Revenue
**Leading:**
- New user activation (% watching 2+ titles in first month)
- Weekly streaming hours per member
- Content completion rates

**Why it works:** High engagement predicts low churn predicts revenue growth

---

### Airbnb

**Lagging:** Nights booked (GMV)
**Leading:**
- Search-to-booking conversion rate
- Average search results quality
- Host response time
- New listings added

**Why it works:** More supply + faster responses = more bookings

---

### Spotify

**Lagging:** Premium subscriber growth
**Leading:**
- Free user engagement (hours listened)
- Playlist saves per user
- Weekly active users

**Why it works:** Highly engaged free users convert to paid

---

## Common Patterns

### Pattern 1: Activation → Retention → Revenue

**Chain:**
1. **Input:** Signup rate
2. **Leading:** Day 7 activation
3. **Leading:** Day 30 retention
4. **Lagging:** LTV

**Application:** Focus on activation to drive long-term revenue

---

### Pattern 2: Engagement → Monetization

**Chain:**
1. **Input:** Feature usage
2. **Leading:** Weekly active usage
3. **Leading:** Feature depth (# features used)
4. **Lagging:** Conversion to paid

**Application:** Drive engagement before asking for money

---

### Pattern 3: Quality → Virality → Growth

**Chain:**
1. **Input:** User satisfaction score
2. **Leading:** Invite/referral rate
3. **Leading:** Viral coefficient (invites per user)
4. **Lagging:** Organic user growth

**Application:** Build quality product → users refer friends

---

## When Leading Metrics Fail

### Red Flag #1: No Correlation with Outcomes

**Problem:** Your "leading" metric moves, but lagging metric doesn't

**Example:**
- Leading (claimed): Page views
- Lagging: Revenue
- Reality: Page views don't predict revenue

**Fix:** Find a different leading metric with proven correlation

---

### Red Flag #2: Too Slow to Be Leading

**Problem:** Your leading metric takes 6 months to show signal

**Example:**
- Claiming "Q1 signups" is a leading indicator for "Q3 revenue"
- That's still lagging (too slow)

**Fix:** Find faster signals (weekly, not quarterly)

---

### Red Flag #3: Vanity Metrics Disguised as Leading

**Problem:** Metric looks good but doesn't predict anything

**Examples:**
- Social media followers (doesn't predict revenue)
- App downloads (doesn't predict active users)
- Website traffic (doesn't predict conversions)

**Fix:** Validate with cohort analysis

---

## Practical Application

### For Product Decisions:

**Question:** Should we build Feature X?

**Bad answer:** "It might increase revenue"
**Good answer:** "It will increase [leading metric] by X%, which historically drives [lagging metric] by Y%"

---

### For Experiments:

**Question:** Should we run an A/B test for 4 weeks?

**Bad answer:** "We need to measure revenue impact"
**Good answer:** "We can measure activation rate in Week 1, which predicts retention in Month 1"

---

### For Team Goals:

**Bad goal:** "Increase revenue 20%"
**Good goal:** "Increase activation rate from 45% → 60%, which drives revenue +20%"

**Why better:** Team can influence activation daily, can't directly influence revenue

---

## Metric Selection Checklist

Use this for any metric you're considering:

**Leading Metric Criteria:**
- [ ] Responds within 1-2 weeks (not months)
- [ ] Predicts lagging outcome (proven with data)
- [ ] Actionable (team can influence it)
- [ ] Measurable (reliable tracking)
- [ ] Understandable (team knows what it means)

**Lagging Metric Criteria:**
- [ ] Ultimate outcome you care about
- [ ] Aligns with business goals
- [ ] Can't be gamed
- [ ] Measures real value delivery

---

## Example Workflow: Building Your Metric System

### Step 1: Define North Star (Lagging)
"What's the ultimate outcome?"
→ Answer: Customer lifetime value (LTV)

### Step 2: Identify Leading Indicators
"What predicts LTV?"
→ Analysis shows: 90-day retention predicts LTV
→ Leading metric: 90-day retention rate

### Step 3: Find Faster Signals
"What predicts 90-day retention?"
→ Analysis shows: Day 7 activation predicts 90-day retention
→ Leading metric: Day 7 activation rate

### Step 4: Identify Input Drivers
"What drives Day 7 activation?"
→ Analysis shows:
- Time to first value
- Feature adoption in first session
- Invite completion
→ Input metrics: TTV, first-session features used, invites sent

### Step 5: Build Dashboard
- **North Star:** LTV
- **Leading (slow):** 90-day retention
- **Leading (fast):** Day 7 activation
- **Inputs:** TTV, feature adoption, invites

---

## Common Mistakes

❌ **Only tracking lagging metrics**
- Problem: No early warning system
- Fix: Add 3-5 leading indicators

❌ **Claiming correlation without data**
- Problem: "Trust me, this predicts that"
- Fix: Run cohort analysis to prove it

❌ **Too many leading metrics**
- Problem: Analysis paralysis
- Fix: Pick 3-5 that matter most

❌ **Optimizing leading metrics that don't matter**
- Problem: Increase page views, revenue doesn't move
- Fix: Validate correlation first

---

## Output Template

### Metrics Framework: [Feature/Product Name]

**North Star:** [Metric]
**Framework Type:** [Leading/Lagging Hierarchy or Input/Output Model]

#### Metric Hierarchy

| Tier | Metric | Current | Target | Cadence | Owner |
|------|--------|---------|--------|---------|-------|
| Lagging (Quarterly) | [e.g., Revenue, LTV, 90-day retention] | [Baseline] | [Goal] | Quarterly review | [Executive/PM] |
| Leading (Weekly) | [e.g., Day 7 activation, WAU, feature adoption] | [Baseline] | [Goal] | Weekly review | [PM/Growth] |
| Leading (Weekly) | [e.g., Time to first value, invite rate] | [Baseline] | [Goal] | Weekly review | [PM/Growth] |
| Input (Daily) | [e.g., Signups, setup completion, first action] | [Baseline] | [Goal] | Daily monitoring | [Team lead] |
| Input (Daily) | [e.g., Support tickets, error rate] | [Baseline] | [Goal] | Daily monitoring | [Engineering] |

#### Correlation Validation Plan

| Hypothesis | Test Method | Data Needed | Timeline |
|-----------|------------|-------------|----------|
| [Leading metric X] predicts [Lagging metric Y] | Cohort analysis: compare high-X vs low-X users on Y outcome | 3 months of user-level data | 2 weeks to validate |
| [Input metric A] drives [Leading metric B] | Time-series correlation: does A movement precede B movement? | 6 weeks of daily data | 1 week to validate |

#### Alert Thresholds

| Metric | Green (On Track) | Yellow (Attention) | Red (Intervention) | Action on Red |
|--------|-----------------|-------------------|-------------------|---------------|
| [Lagging metric] | [Above target] | [Within 1 SD or 10% below target] | [2 SD or 20%+ below target] | [Who gets alerted; what investigation to run; what corrective action] |
| [Leading metric] | [Above target] | [Within 1 SD or 10% below target] | [2 SD or 20%+ below target] | [Who gets alerted; what investigation to run; what corrective action] |
| [Input metric] | [Above target] | [Within 1 SD or 10% below target] | [2 SD or 20%+ below target] | [Who gets alerted; what investigation to run; what corrective action] |

#### Dashboard Design

**Section 1 - North Star (top of dashboard):**
[The ONE lagging metric, shown as a large number with monthly/quarterly trend line and target overlay]

**Section 2 - Leading Indicators (middle):**
[3-5 weekly metrics shown as sparkline charts with alert thresholds marked. Each metric includes a comparison to prior week and target.]

**Section 3 - Input Metrics (bottom):**
[5-10 daily levers shown as a table with current value, WoW change, and status indicator (green/yellow/red). Grouped by team ownership.]

---

## Alert Threshold Guidance

For each key metric, define three thresholds:

- **Green (On Track):** Metric is at or above target. No action needed. Keep monitoring at standard cadence.
- **Yellow (Needs Attention):** Metric is trending down or below target by a small margin (typically 1 standard deviation below target, or 10% miss). Action: Increase monitoring cadence (e.g., daily instead of weekly), investigate root cause, prepare a response plan.
- **Red (Intervention Needed):** Metric has dropped significantly (typically 2 standard deviations below target, or missing by more than 20%). Action: Immediate investigation.

**For each Red threshold, specify three things:**
1. **Who gets alerted:** Name the person or team (e.g., "PM + Engineering Lead + VP Product")
2. **What investigation to run:** Specific analysis (e.g., "Run cohort breakdown by acquisition channel and device type to isolate the drop")
3. **What action to take:** Concrete response (e.g., "If caused by a recent release, initiate rollback decision within 24 hours. If caused by external factor, schedule war room within 48 hours.")

**Calibration tip:** Start with thresholds based on historical variance. After 4-6 weeks, adjust based on actual alert volume. If you get Yellow alerts every week, your threshold is too sensitive. If you never get Yellow alerts, it is too loose.

---

## Metric Retirement

Leading indicators don't last forever. Retire or replace them when:

**Signals it's time to retire a metric:**
- The correlation to the lagging outcome has weakened for 2+ consecutive quarters
- The metric has flatlined (no movement despite product changes) -- it may have reached a natural ceiling
- The metric is being gamed (teams optimize for the number rather than the underlying behavior)
- The product has evolved and the metric no longer captures the core user behavior

**Retirement process:**
1. **Flag it:** Add a "Under Review" tag to the metric in your dashboard and alert stakeholders
2. **Run a replacement analysis:** What metric better predicts the lagging outcome now? Use the correlation validation plan to test candidates.
3. **Overlap period:** Run old and new metrics in parallel for 4-6 weeks to validate the replacement
4. **Sunset:** Remove old metric from primary dashboard. Archive in a "Retired Metrics" section with retirement rationale and replacement metric.
5. **Document:** Add to the learning log -- "Metric X retired because [reason]. Replaced by Metric Y because [evidence]."

**Common retirement patterns:**
- Activation metric retires when onboarding flow changes fundamentally
- Feature adoption metric retires when feature reaches saturation (>80% adoption)
- NPS retires when replaced by a more predictive satisfaction measure (e.g., task completion rate)

---

## Multi-Product Guidance

For products with multiple value streams (e.g., separate features for creation, analytics, and collaboration), do not try to force everything into one flat metric hierarchy. Instead:

1. **Define a shared North Star** that captures overall product value (e.g., "Weekly Active Organizations").
2. **Build a metric hierarchy for each value stream:**
   - Stream A (Creation): Leading metrics specific to creation (e.g., documents created, time to first publish)
   - Stream B (Analytics): Leading metrics specific to analytics (e.g., dashboards viewed, insights exported)
   - Stream C (Collaboration): Leading metrics specific to collaboration (e.g., comments posted, shared workspaces)
3. **Show how each stream rolls up to the North Star:** Each stream contributes to the shared North Star through a specific mechanism. Make this explicit (e.g., "Users who use both Creation and Collaboration have 2x higher weekly activity than single-stream users").
4. **Each stream needs its own leading indicators,** but guardrail metrics can be shared across streams (e.g., NPS, support ticket volume).
5. **Avoid averaging across streams.** If one stream is thriving and another is declining, an average masks the problem. Report each stream independently and then show the aggregate.

---

## Output Integration

### Where Files Go

**Metric framework documentation:**
- Active work: `outputs/metrics-framework-[date].md` (living document for your team)
- When finalized: Move to `context-library/metrics/metric-hierarchy-[quarter].md` for historical reference
- Dashboard spec: Share with analytics team for instrumentation

### Link to Other Work

After building your framework:
- **Reference in strategy** - "Our metric hierarchy connects [lagging] to [leading] to [input]"
- **Use in feature PRDs** - "This feature's success metric is [X], a leading indicator for [lagging]"
- **Guide experiments** - Teams use leading metrics to evaluate experiments faster
- **Inform roadmap** - Identify which product work drives which leading metrics

### Cross-Skill Integration

**Feeds into:**
- `/define-north-star` - Your lagging metric becomes (or informs) the North Star
- `/feature-metrics` - Feature success metrics are leading indicators in this framework
- `/retention-analysis` - Leading metrics for retention are identified here
- `/activation-analysis` - Activation metrics are leading indicators for engagement

**Pulls from:**
- `/write-prod-strategy` - Strategy determines what you're optimizing for
- `context-library/metrics/` - Historical data validates correlations
- `/define-north-star` - What is your ultimate success metric?

---

## Related Skills

- `/define-north-star` - Choose your North Star (lagging metric)
- `/activation-analysis` - Find leading activation indicators
- `/feature-metrics` - Choose experiment metrics with STEDII
- `/retention-analysis` - Analyze retention predictors

---

---

## Output Quality Self-Check

Before delivering the metrics framework, verify:

- [ ] **North Star is anchored:** The framework starts from a clearly defined North Star or lagging metric. If none exists, recommend running `/define-north-star` first.
- [ ] **Three tiers defined:** The hierarchy includes at least one metric at each tier: Lagging (quarterly), Leading (weekly), and Input (daily). A framework with only lagging metrics is just a scorecard, not a decision tool.
- [ ] **Correlation hypotheses stated:** For each leading-to-lagging connection, the hypothesis is explicit and a validation method is described. Do not claim "X predicts Y" without explaining how to prove it.
- [ ] **Alert thresholds set:** At least the top 3-5 metrics have green/yellow/red thresholds defined with specific actions for Red. A metric without an alert threshold is decoration, not instrumentation.
- [ ] **Owners assigned:** Every metric has a team or person responsible. Unowned metrics do not get watched.
- [ ] **Dashboard design described:** The output includes a dashboard layout description showing what goes where and at what cadence. The PM should be able to hand this to an analyst and get a working dashboard.
- [ ] **No vanity metrics:** Every metric in the framework has a clear connection to either a lagging outcome or an actionable input. If a metric "looks good but does not drive decisions," remove it.
- [ ] **Multi-stream handled:** If the product has multiple value streams, each stream has its own leading indicators with explicit roll-up to the shared North Star. If the product is single-stream, this is not needed.
- [ ] **Metric retirement guidance included:** For any existing metrics being reviewed, include signals for when to retire them and a replacement process. New frameworks should note that metrics have a shelf life.
- [ ] **Data quality bar stated:** For any correlation claims between leading and lagging metrics, state the sample size, time period, and confidence level. Do not present low-confidence correlations as validated findings.

---

**Framework credit:** Adapted from Aakash Gupta's metrics frameworks. Read: https://www.news.aakashg.com/p/become-an-ab-testing-expert-advanced
