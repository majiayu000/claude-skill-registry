---
name: retention-analysis
description: Cohort analysis and retention optimization framework. Identifies retention drivers and churn factors.
disable-model-invocation: false
user-invocable: true
---

# Retention Analysis: Measuring What Keeps Users Coming Back

## Quick Start

```
/retention-analysis
```
Then provide:
1. **Retention data** (D1, D7, D14, D30 rates -- or I'll query your analytics MCP)
2. **Product usage frequency** (daily, weekly, monthly -- how often should users return?)
3. **Known churn reasons** (if any -- from interviews, support tickets, surveys)

I'll analyze your retention curve shape, identify the biggest drop-off,
compare retained vs churned user behavior, and recommend interventions.

**Output:** Saved to `outputs/analyses/retention-analysis-[date].md`
**Time:** ~15 min with data, ~25 min with cohort deep-dive

**When to use:** When diagnosing churn problems, measuring product-market fit, or optimizing for stickiness

**Framework source:** Aakash Gupta's retention frameworks and "Ultimate Guide to Activation"

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Metrics/Analytics | `context-library/metrics/*.md` | D7, D30, retention, churn, cohort, "monthly active", DAU, WAU | Current retention curves, cohort performance, churn rates |
| User Research | `context-library/research/*.md` | churn, "stopped using", "didn't come back", "why I left", "why I switched" | Churn interview quotes, reasons users stop using product |
| Meeting Notes | `context-library/meetings/*.md` | churn, "cancelled", "downgrade", lost deal, customer feedback | CS feedback on churn, customer complaints, drop-off patterns |
| PRDs | `context-library/prds/*.md` | retention, sticky, habit, engagement, notification, reminder | Features built to improve retention |
| Business Info | `context-library/business-info-template.md` | target user, use case, frequency, engagement, core activity | How often users should use product, what drives stickiness |

**Context Priority:**
1. Internal context FIRST (business info, retention metrics, churn research)
2. Analytics MCP SECOND (if connected - query retention cohorts, churn reasons)
3. Framework guidance LAST (generic retention tactics)

**Cross-Skill Links:**
- If activation issues found → Link to `activation-analysis` (fix activation first)
- If expansion opportunity identified → Link to `expansion-strategy`
- If feature opportunity identified → Link to `prd-draft`

---

## Step 0: Understanding Your Current Retention Reality

Before diving into retention analysis, let me check what data already exists about your users...

**Checking:**
- `context-library/business-info-template.md` for expected product usage patterns
- `context-library/metrics/` for existing retention metrics and cohort data
- `context-library/research/` for churn interviews and user feedback
- `context-library/meetings/` for CS/support feedback on why users churn
- `context-library/prds/` for features built to improve retention

**[If analytics MCP connected]:** "Let me also query [Amplitude/Mixpanel] for your current retention curves, churn rates by cohort, and behavioral differences between retained vs churned users."

**Based on what I find, I'll show you:**

### Internal Intelligence Summary

**From Business Info:**
- [Your product's intended usage frequency]
- [Target users and their engagement patterns]
- Example: "Product designed for daily use by individual contributors in engineering teams"

**From Metrics/Analytics:**
- [Current D7 and D30 retention rates]
- [Retention curve shape (flattening, declining, or smiling)]
- [Churn rate and trends]
- [Retention differences by cohort or segment]
- Example: "D7: 42%, D30: 28%, declining curve, but organic cohort outperforms paid by 15%"

**From Churn Research:**
- [Top reasons users churn]
- [Churn patterns by segment]
- [Quote evidence of churn drivers]
- Example: "Enterprise users cite lack of custom integrations; SMB users cite steep learning curve"

**From Sales/CS Meetings:**
- [Customer feedback on product stickiness]
- [Feature requests from churned customers]
- [Usage patterns that predict retention]
- Example: "Customers who invite 3+ team members in week 1 have 90% D30 retention"

**From PRDs:**
- [Past retention improvements and their impact]
- [Features designed to increase engagement]
- Example: "PRD-2024-04 added daily email digest, increased WAU by 12%"

### Gaps in Knowledge

Based on internal context, we **don't yet know:**
- [Gap 1]: Specific behaviors that separate retained users from churned users
- [Gap 2]: Which segments retain best and why
- [Gap 3]: Impact of specific features on retention curves

**Should I help analyze your retention data, or would you like to provide additional metrics first?**

---

## Step 1: Retention Diagnostic Questions

Instead of generic "track retention metrics," I'll ask:

### Question 1: The Biggest Drop
**"Between Day 1, Day 7, and Day 30, where do you lose the most users?"**

This tells me whether the problem is immediate product issues (D1→D7) or habit formation (D7→D30).

### Question 2: Retained vs Churned Behavior
**"What specific actions do Day 30 retained users take in their first week that Day 7 churned users don't?"**

This is the differentiating behavior, not your opinion of what matters.

### Question 3: Churn Reasons
**"From churn interviews or feedback, what are the top 3 reasons users stop using?"**

This tells me whether it's product quality, insufficient value, or competition.

### Question 4: Usage Pattern
**"How often should active users return—daily, weekly, or monthly?"**

This determines whether D7 or L7 retention is your right metric.

### Question 5: Segment Differences
**"Do different user segments (size, industry, use case) have different retention patterns?"**

Enterprise vs SMB, solo vs team users often have very different retention curves.

---

## Key Retention Metrics

### Day 7 (D7) Retention

**Definition:** % of users active on Day 7 after signup

**Why it matters:** Early signal of product stickiness

**Benchmarks:**
- Consumer social: 40-60%
- Productivity tools: 30-50%
- B2B SaaS: 50-70%
- Marketplace: 20-40%

**Formula:**
```
D7 Retention = (Users active on Day 7) / (Users who signed up 7 days ago) × 100
```

---

### Day 30 (D30) Retention

**Definition:** % of users active 30 days after signup

**Why it matters:** Indicates habit formation

**Benchmarks:**
- Consumer social: 25-40%
- Productivity tools: 20-35%
- B2B SaaS: 40-60%
- Marketplace: 15-30%

**Formula:**
```
D30 Retention = (Users active on Day 30) / (Users who signed up 30 days ago) × 100
```

---

### L7 and L28 (Rolling Retention)

**Definition:** % of users active in a 7-day or 28-day window

**Why better than D7/D30:**
- Accounts for usage patterns (weekly tools, not daily)
- More forgiving for non-daily products
- Better for B2B products

**L7 Formula:**
```
L7 = (Users active at least once in Days 1-7) / (Total signups) × 100
```

**L28 Formula:**
```
L28 = (Users active at least once in Days 1-28) / (Total signups) × 100
```

---

### Retention Curves

**Three types of retention curves:**

**1. Flattening Curve (Good) ✅**
- Retention drops initially, then flattens
- Indicates core user base forming
- Example: Facebook, Slack

**2. Declining Curve (Bad) ❌**
- Retention keeps dropping over time
- No product-market fit
- Example: Failed consumer apps

**3. Smiling Curve (Best) ✅✅**
- Retention drops, flattens, then RISES
- Indicates habit formation
- Example: LinkedIn, Notion

**How to visualize:**
```
Plot retention % (Y-axis) vs Days since signup (X-axis)
- Day 1, Day 7, Day 14, Day 30, Day 60, Day 90
```

---

## Cohort Analysis

**What it is:** Comparing retention across different user groups

### Time-based Cohorts

**Compare by signup month:**
```
Jan 2024 cohort: 45% D30 retention
Feb 2024 cohort: 50% D30 retention
Mar 2024 cohort: 55% D30 retention
```

**What this tells you:** Product improvements are working (retention trending up)

---

### Feature-based Cohorts

**Compare users who used Feature X vs didn't:**
```
Used Feature X: 60% D30 retention
Didn't use Feature X: 30% D30 retention
```

**What this tells you:** Feature X drives retention (prioritize it)

---

### Channel Cohorts

**Compare acquisition channels:**
```
Organic search: 50% D30 retention
Paid ads: 25% D30 retention
Referrals: 70% D30 retention
```

**What this tells you:** Referrals bring highest quality users

---

## How to Improve Retention

### Step 1: Identify the Drop-off Point

**Run retention analysis:**
```
Use /retention-analysis and reference context-library/business-info-template.md

Help me analyze our retention:
- D1 retention: ___%
- D7 retention: ___%
- D14 retention: ___%
- D30 retention: ___%

Where's the biggest drop? What should we focus on?
```

**Common patterns:**
- **Big drop D1 → D7:** Activation problem (users don't reach Aha)
- **Big drop D7 → D30:** Habit formation problem (no triggers to return)
- **Gradual decline:** Value delivery problem (product isn't solving the problem)

---

### Step 2: Compare Retained vs Churned Users

**Find the differentiating behaviors:**

**Questions to ask:**
1. What did retained users do that churned users didn't?
2. How fast did retained users complete key actions?
3. Which features did retained users adopt?
4. How many team members did retained users invite?

**Example analysis:**
```
Retained users (D30):
- Completed setup in <5 minutes: 80%
- Created 3+ projects in first week: 75%
- Invited 2+ team members: 90%
- Used core feature 5+ times: 100%

Churned users (D30):
- Completed setup in <5 minutes: 30%
- Created 3+ projects in first week: 10%
- Invited 2+ team members: 5%
- Used core feature 5+ times: 20%
```

**Insight:** Focus on setup speed, project creation, team invites, and core feature usage

---

### Step 3: Test Retention Improvements

**Hypothesis format:**
```
If we [intervention], then [metric] will improve by [amount] because [reason]
```

**Example hypotheses:**
- "If we send Day 3 email reminder, D7 retention will improve by 10% because users forgot to return"
- "If we reduce setup time to <3 min, D30 retention will improve by 15% because more users reach Aha"
- "If we add team invite prompt, D30 retention will improve by 20% because social products are stickier"

---

## Retention Drivers by Product Type

### Social Products (Facebook, Instagram, TikTok)

**Key retention drivers:**
- Friend/follower count
- Content consumption (feed engagement)
- Content creation (posts, stories)
- Social interactions (likes, comments)

**Metric to optimize:** Daily Active Users (DAU)

---

### Productivity Tools (Notion, Figma, Asana)

**Key retention drivers:**
- Depth of content created (docs, files, projects)
- Team collaboration (shared workspaces)
- Integration adoption (Slack, Google Drive)
- Weekly usage habits

**Metric to optimize:** Weekly Active Users (WAU)

---

### Marketplaces (Airbnb, Uber, Etsy)

**Key retention drivers:**
- First transaction success
- Repeat purchase quality
- Trust signals (reviews, ratings)
- Supply availability

**Metric to optimize:** Monthly transactions per user

---

### B2B SaaS (Salesforce, HubSpot, Stripe)

**Key retention drivers:**
- Account setup completion
- Admin + end-user activation
- Data integration depth
- Team expansion

**Metric to optimize:** Active paid seats

---

## Advanced: Resurrection Analysis

**What it is:** Analyzing users who churned then came back

### Why Resurrected Users Matter

**Resurrection rate:**
```
Resurrection = (Churned users who returned) / (Total churned users) × 100
```

**Questions to answer:**
1. What brought them back? (email campaign, new feature, external trigger)
2. How long were they gone? (1 week, 1 month, 3 months)
3. What's their retention after returning? (do they stick this time?)

**Example insights:**
- Win-back emails work best at Day 14 of inactivity
- Users who return after 1 month have 50% D30 retention
- New feature launches resurrect 10% of dormant users

---

## Retention Dashboard Template

Track these weekly:

| Metric | This Week | Last Week | 4 Weeks Ago | Target |
|--------|-----------|-----------|-------------|--------|
| D1 Retention | ___% | ___% | ___% | 80%+ |
| D7 Retention | ___% | ___% | ___% | 40%+ |
| D14 Retention | ___% | ___% | ___% | 35%+ |
| D30 Retention | ___% | ___% | ___% | 25%+ |
| L28 (28-day) | ___% | ___% | ___% | 30%+ |
| Weekly Active | _____ | _____ | _____ | Growing |
| Churn Rate | ___% | ___% | ___% | <10% |

**Cohort comparison:**
- This month's cohort vs last month
- Organic vs paid retention
- Feature adopters vs non-adopters

---

## Common Mistakes

❌ **Only tracking signup growth**
- Problem: Vanity metric, doesn't predict success
- Fix: Track cohort retention curves

❌ **Using only D30 retention**
- Problem: Too slow for decision-making
- Fix: Add D7 and leading indicators

❌ **Not segmenting retention**
- Problem: Miss important patterns
- Fix: Analyze by channel, feature usage, user type

❌ **Ignoring resurrection**
- Problem: Write off churned users too early
- Fix: Test win-back campaigns

❌ **Confusing D7 with L7**
- Problem: D7 is too strict for weekly products
- Fix: Use L7 for non-daily usage patterns

---

## Real-World Examples

### Example 1: Facebook's "7 Friends in 10 Days"

**Discovery:** Users who added 7 friends in first 10 days had 90% D30 retention

**Action:** Optimized onboarding for friend connections

**Result:** Explosive user growth with strong retention

---

### Example 2: Slack's 2,000 Messages

**Discovery:** Teams sending 2,000+ messages had 93% retention

**Action:** Focused activation on reaching 2,000 messages

**Result:** Clear activation metric, high retention

---

### Example 3: LinkedIn's Connection Analysis

**Discovery:** Users with 5+ connections had 70% higher D30 retention

**Action:** Aggressive prompts to make connections early

**Result:** Improved early engagement and long-term retention

---

## Retention Analysis Worksheet

Use this with your data:

### 1. Current Retention Metrics
- D1: ___%
- D7: ___%
- D14: ___%
- D30: ___%
- Biggest drop: Between Day ___ and Day ___

### 2. Cohort Analysis
- Best performing cohort: ___________ (___% D30)
- Worst performing cohort: ___________ (___% D30)
- Trend: [ ] Improving [ ] Declining [ ] Flat

### 3. Behavioral Analysis
**Retained users typically:**
- Action 1: ___________
- Action 2: ___________
- Action 3: ___________

**Churned users typically:**
- Missing action 1: ___________
- Missing action 2: ___________

### 4. Hypothesis to Test
- If we ___________, then retention will improve by ___% because ___________

---

## Output Integration

### Where to Save Your Retention Analysis

**Research & Findings:**
- Save to: `outputs/analyses/retention-analysis-[date].md`
- When finalized, move to: `context-library/research/retention-[product].md`

**Retention Metrics & Dashboards:**
- Update `context-library/metrics/` with your retention dashboard
- Include retention curves, cohort analysis, and trend notes
- Link retention findings to broader business metrics

**Retention Features & Improvements:**
- Create PRD in `context-library/prds/` for each retention initiative
- Link this retention analysis as context
- Track impact in PRD success metrics

### Cross-Skill Integration

**Feeds into:**
- `/activation-analysis` - Activation rates predict retention (low activation = low retention)
- `/expansion-strategy` - Retention is prerequisite for expansion (retain before upselling)
- `/prd-draft` - Retention features become product roadmap items
- `/experiment-decision` - Test retention improvements (email cadence, notifications, features)
- `/metrics-framework` - Retention and churn as leading indicators of business health
- `/define-north-star` - Retention often ties to North Star metric

**Pulls from:**
- `/activation-analysis` - Aha moment and habit formation data
- `/user-research-synthesis` - Churn interview synthesis and user feedback
- `/competitor-analysis` - Understand if churn is to competitors
- `/expansion-strategy` - Expansion cohort retention patterns

### Key Questions to Revisit

After analyzing retention, ask:
- Is our Aha moment definition (from activation-analysis) actually tied to retention?
- Which user segments have best vs worst retention, and why?
- What's our specific drop-off point (D1, D7, D30) and should we optimize differently?
- Which features, when adopted early, have the strongest retention correlation?
- Do we have data on resurrection campaigns—can we win back churned users?

---

## Win-Back Playbook

For users who churned or went dormant:

### Timing Windows

| Dormancy Period | Channel | Message Type | Expected Win-Back Rate |
|----------------|---------|-------------|----------------------|
| 1-7 days | In-app nudge + email | "We noticed you haven't been back..." | 15-25% |
| 7-30 days | Personal email from PM/CS | Value reminder with specific use case | 8-15% |
| 30-90 days | Win-back campaign | New feature highlights since they left | 3-8% |
| 90+ days | Re-engagement email | New value prop or offer | 1-3% |

### Win-Back Message Framework

1. **Acknowledge the gap** (don't pretend it didn't happen)
   - "It's been a while since you last used [Product]..."
2. **Lead with NEW value** (what's changed since they left)
   - "Since you've been away, we've shipped [feature that addresses their likely churn reason]..."
3. **Lower the barrier to return** (one-click action, no re-onboarding)
   - "Pick up right where you left off -- your [workspace/data] is still here."
4. **Include social proof** (what similar users are achieving)
   - "Teams like yours are saving [X hours/week] with [specific feature]."

### Win-Back Experiment Design

- **Segment by churn reason** before sending win-back campaigns. Users who churned due to price need a different message than users who churned due to missing features.
- **Track resurrection retention** -- do win-back users retain at the same rate as organic users? If not, the win-back isn't truly working.
- **Set a "dead" threshold** -- after how many months of dormancy do you stop trying? (Usually 6-12 months.)

### Resurrection Analysis: Do Win-Back Users Actually Stick?

After running win-back campaigns, track whether resurrected users retain at the same rate as organic active users.

**Resurrection Cohort Tracking:**

| Cohort | N | D7 Post-Return | D30 Post-Return | D90 Post-Return | Comparison to Organic |
|--------|---|---------------|----------------|----------------|----------------------|
| Win-back (1-7 day dormancy) | [N] | [%] | [%] | [%] | [% vs organic D7/D30/D90] |
| Win-back (7-30 day dormancy) | [N] | [%] | [%] | [%] | [% vs organic D7/D30/D90] |
| Win-back (30-90 day dormancy) | [N] | [%] | [%] | [%] | [% vs organic D7/D30/D90] |
| Win-back (90+ day dormancy) | [N] | [%] | [%] | [%] | [% vs organic D7/D30/D90] |
| Organic active (baseline) | [N] | [%] | [%] | [%] | -- |

**Key questions this answers:**
1. At what dormancy duration does win-back retention drop below 50% of organic? (That's your "point of no return" -- users dormant beyond this are probably gone for good)
2. Do short-dormancy win-backs (1-7 days) retain as well as organic users? (If yes, fast intervention pays off)
3. Is the cost of win-back campaigns justified by the retained revenue? (Compare campaign cost vs LTV of resurrected users)

**Decision framework:**
- Win-back retention > 70% of organic → Keep investing in win-back campaigns for this dormancy tier
- Win-back retention 40-70% of organic → Optimize the win-back message/offer, then re-measure
- Win-back retention < 40% of organic → Stop targeting this dormancy tier. Focus resources on earlier intervention.

---

## Early Churn Signals

Monitor these leading indicators to catch at-risk users before they churn:

| Signal | Threshold | Risk Level | Intervention |
|--------|-----------|------------|-------------|
| Login frequency drop | >50% decrease week-over-week | High | Automated email + CS outreach |
| Feature usage narrowing | Using only 1 feature (was using 3+) | Medium | In-app prompt for underused features |
| Support ticket spike | 3+ tickets in a week | Medium | Proactive CS call |
| Team member departures | Admin removes users | High | Executive-level check-in |
| Core action stopped | 14+ days without core activity | High | "What's blocking you?" email |
| Session duration declining | >40% shorter sessions over 2 weeks | Medium | Check for UX issues, survey |
| Export activity spike | Bulk data export | High | Immediate CS outreach (likely switching) |

### Building a Churn Risk Score

Combine signals into a composite score:

```
Churn Risk Score = (Login frequency weight x login signal)
                 + (Feature breadth weight x narrowing signal)
                 + (Support weight x ticket signal)
                 + (Team size weight x departure signal)
                 + (Core action weight x inactivity signal)

Score 0-30: Low risk (monitor)
Score 31-60: Medium risk (automated intervention)
Score 61-100: High risk (human intervention)
```

**Calibrate weights** using historical data: which signals best predicted actual churn in the past 6 months?

---

## Output Quality Self-Check

Before delivering the retention analysis, verify:

- [ ] **Retention curve shape** is identified (flattening, declining, or smiling) with data
- [ ] **Biggest drop-off point** is specified (D1->D7, D7->D30, etc.) with magnitude
- [ ] **Retained vs churned behavior** comparison uses actual behavioral data, not assumptions
- [ ] **Segment analysis** covers at least 2 dimensions (channel, user type, feature usage, etc.)
- [ ] **Cohort trends** show whether retention is improving, declining, or flat over time
- [ ] **Benchmarks** are industry-appropriate (B2B SaaS vs consumer vs marketplace)
- [ ] **Churn reasons** are grounded in data (interviews, surveys, support tickets)
- [ ] **Recommendations** are prioritized and tied to the specific drop-off identified
- [ ] **Hypotheses** are in If/Then/Because format with measurable success criteria
- [ ] **Connected to activation** -- is the retention problem actually an activation problem in disguise?
- [ ] **Win-back strategy** is addressed for already-churned users, not just prevention
- [ ] **Resurrection analysis template** referenced (if win-back campaigns exist)
- [ ] **No generic advice** -- all recommendations reference this specific product and data

---

## Related Skills

- `activation-analysis` - Improve activation to boost retention (activation -> retention pipeline)
- `metrics-framework` - Leading indicators of retention (D7, L28, feature adoption)
- `experiment-decision` - Test retention improvements (engagement features, notifications)
- `define-north-star` - Align retention metrics to North Star metric
- `user-research-synthesis` - Understand why users churn (synthesis of churn interviews)
- `expansion-strategy` - Retention enables expansion (can't expand churned users)
- `competitor-analysis` - Understand competitive churn factors

---

**Framework credit:** Adapted from Aakash Gupta's retention frameworks. Read: https://www.news.aakashg.com/p/ultimate-guide-activation (habit formation section)
