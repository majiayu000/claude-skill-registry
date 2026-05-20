---
name: expansion-signals
description: Identify upsell and cross-sell opportunities through usage patterns, growth signals, and account behavior analysis
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Expansion Signals

> Detect opportunities for account expansion by analyzing usage patterns, growth indicators, and behavioral signals that predict readiness to buy more.

## When to Use This Skill

- Monthly expansion pipeline review
- Identifying upsell candidates
- Prioritizing CSM expansion efforts
- Building expansion playbooks
- Forecasting expansion revenue

## Methodology Foundation

Based on **Lincoln Murphy's Expansion Revenue Framework** and **Gainsight Expansion Playbooks**, focusing on:
- Usage ceiling signals
- Growth triggers
- Buying intent indicators
- Timing optimization

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Identifies expansion signals | Which opportunities to pursue |
| Scores expansion readiness | Pricing and packaging |
| Suggests conversation openers | Relationship approach |
| Prioritizes opportunities | Resource allocation |
| Calculates potential value | Discount/incentive offers |

## What This Skill Does

1. **Signal detection** - Identify expansion indicators
2. **Opportunity scoring** - Rank expansion readiness
3. **Sizing estimation** - Potential expansion value
4. **Timing recommendation** - When to engage
5. **Conversation guidance** - How to approach

## How to Use

```
Analyze expansion signals for:

Account: [Company Name]
Current Contract: $[ARR]
Products: [What they have]
Contract End: [Date]

Usage Data:
- Seats: [Used] / [Licensed]
- Feature usage: [Which features, how much]
- Usage trend: [Growing/Flat/Declining]
- Power users: [How many, what they do]

Account Context:
- Company growth: [Hiring, funding, news]
- Stakeholder changes: [New decision makers]
- Requests: [Feature requests, complaints about limits]

Available Expansion:
- Additional seats: $[Price]
- New modules: [List with prices]
- Higher tier: $[Price difference]
```

## Instructions

### Step 1: Identify Expansion Signal Categories

**Usage Ceiling Signals (Strong):**
| Signal | What It Means |
|--------|---------------|
| >90% seat utilization | Need more licenses |
| Hitting API limits | Need higher tier |
| Feature requests beyond plan | Ready for upgrade |
| Workarounds for limitations | Pain = opportunity |
| Power users maxing features | Champions for expansion |

**Growth Triggers (Strong):**
| Signal | What It Means |
|--------|---------------|
| Company hiring | More seats needed |
| New office/location | Geographic expansion |
| Funding announcement | Budget available |
| New initiative/project | New use case |
| M&A activity | Integration opportunity |

**Behavioral Signals (Medium):**
| Signal | What It Means |
|--------|---------------|
| Admin exploring pricing | Active evaluation |
| Repeated feature inquiries | Interest in upgrade |
| Reference/case study request | Happy, expandable |
| Executive engagement increase | Strategic priority |
| QBR agenda on "next steps" | Open to discussion |

**Timing Signals:**
| Signal | Best Timing |
|--------|-------------|
| Budget cycle approaching | 30-60 days before |
| Contract renewal | 90 days before |
| Just hit milestone | Immediately after |
| Competitor mentioned | Defensively, now |

### Step 2: Score Expansion Readiness

**Expansion Score (0-100):**

| Factor | Weight | Scoring |
|--------|--------|---------|
| Usage ceiling | 25 | >90% = 25, 80-90% = 15, <80% = 5 |
| Growth triggers | 20 | Strong = 20, Some = 10, None = 0 |
| Feature requests | 15 | Multiple = 15, Some = 8, None = 0 |
| Relationship health | 20 | Healthy = 20, OK = 10, At-risk = 0 |
| Timing fit | 20 | Perfect = 20, Good = 12, Poor = 5 |

**Readiness Bands:**
| Score | Status | Action |
|-------|--------|--------|
| 75-100 | 🔥 Hot | Engage this week |
| 50-74 | 🟢 Warm | Engage this month |
| 25-49 | 🟡 Nurture | Build toward expansion |
| 0-24 | ⏸️ Wait | Focus on adoption/health |

### Step 3: Size the Opportunity

**Expansion Sizing:**
```
Potential Value =
  (Additional Seats × Seat Price) +
  (Module Upgrade Value) +
  (Tier Upgrade Delta)

Example:
- 20 additional seats × $100/month = $24K ARR
- Premium module = $12K ARR
- Potential: $36K ARR (20% of base)
```

### Step 4: Plan the Approach

**Conversation Starters by Signal:**

| Signal | Opening |
|--------|---------|
| Seat ceiling | "I noticed you're at 95% capacity. Your team must be growing!" |
| Feature requests | "You've asked about X a few times. Let me show you how our [upgrade] handles that." |
| Company growth | "Congrats on the Series B! How is that affecting your team structure?" |
| Power users | "Sarah has become a real power user. Have you considered our advanced features?" |

## Examples

### Example 1: Expansion Analysis

**Input:**
```
Analyze expansion for DataFlow Inc:

Current: $48K ARR (50 seats @ $80/seat/month)
Products: Core Platform only
Renewal: 8 months away

Usage:
- Seats: 48/50 (96%)
- Core features: 85% adoption
- API calls: 92% of limit
- Power users: 12 (doing advanced workflows)

Context:
- Just raised Series A ($15M)
- Hiring 20 engineers this quarter
- VP Data asked about analytics module 3 times
- NPS: 9

Available:
- Additional seats: $80/seat/month
- Analytics module: $15K ARR
- API tier upgrade: $6K ARR
- Enterprise tier: +$20K ARR (includes above)
```

**Output:**
```
## Expansion Analysis: DataFlow Inc

### 🔥 Expansion Score: 88/100 - HOT

**This account is primed for expansion.**

---

### Signal Analysis

| Signal | Strength | Points |
|--------|----------|--------|
| 96% seat utilization | 🔥 Strong | 25/25 |
| Series A + hiring 20 | 🔥 Strong | 20/20 |
| Analytics requests (3x) | 🔥 Strong | 15/15 |
| NPS 9 + healthy | 🔥 Strong | 18/20 |
| 8 months to renewal | 🟡 Medium | 10/20 |
| **Total** | | **88/100** |

---

### Opportunity Sizing

**Conservative Estimate:**
```
20 new seats × $80 × 12 = $19,200 ARR
Analytics module = $15,000 ARR
─────────────────────────────────
Conservative Total: $34,200 ARR (71% expansion)
```

**Aggressive Estimate (Enterprise Tier):**
```
20 new seats × $80 × 12 = $19,200 ARR
Enterprise upgrade = $20,000 ARR
(Includes analytics + API)
Additional seats at enterprise = $24,000 ARR
─────────────────────────────────
Aggressive Total: $63,200 ARR (132% expansion)
```

**Recommended Target: $40-50K expansion**

---

### Why Now?

1. **Capacity Ceiling** - 96% seat usage, hiring 20 more
   - They will literally run out of seats in weeks

2. **Feature Demand** - VP Data asked 3x about analytics
   - Not if, but when they'll need it

3. **Budget Available** - Series A just closed
   - Flush with cash, growth mindset

4. **Relationship Strong** - NPS 9
   - Trust is high, easy conversation

5. **Power Users as Champions** - 12 heavy users
   - Internal advocates for expansion

---

### Recommended Approach

**Timing: This week**
Don't wait. Seat ceiling + hiring = urgent need.

**Who to Engage:**
1. VP Data (analytics interest) - Decision Maker
2. Champion (current) - Internal advocate
3. Head of Engineering (new hires) - User expansion

**Conversation Strategy:**

**Opening:**
"Congrats on the Series A! I saw you're hiring 20 engineers—exciting growth. I also noticed you're at 96% seat capacity, and [VP Data] has been asking about our analytics module. I'd love to get ahead of your growth and make sure you're set up for scale."

**Value Framing:**
"Given your expansion, I want to show you our Enterprise tier. It includes the analytics module you've been interested in, unlimited API calls, and room to grow. Many companies at your stage find it's more cost-effective than à la carte."

**Offer:**
- Enterprise tier upgrade: +$20K ARR
- 30 additional seats at enterprise rate: $28.8K ARR
- **Total: $48.8K expansion** (102% growth)
- Incentive: Lock multi-year, 10% discount

---

### Next Steps

| Action | Owner | Timeline |
|--------|-------|----------|
| Email VP Data re: analytics | CSM | Tomorrow |
| Prep enterprise comparison | CSM | This week |
| Discovery call: growth plans | CSM | Within 5 days |
| Pricing approval for discount | Sales | Before call |
| Executive intro if needed | CS Director | If VP Data engaged |

---

### Risk Considerations

| Risk | Mitigation |
|------|------------|
| Budget not allocated | Reference Series A, show ROI |
| Competitor evaluation | Emphasize switching cost, existing ROI |
| VP Data not decision maker | Map buying committee |
| "We'll wait until renewal" | Show urgency (seat ceiling) |
```

### Example 2: Portfolio Expansion Prioritization

**Input:**
```
Rank these 5 accounts for expansion priority:

1. AlphaTech: 70% seats, stable usage, renewal in 3 months, asked about premium once
2. BetaCorp: 95% seats, growing 20%, just promoted champion, raised Series B
3. GammaCo: 60% seats, declining usage, renewal in 12 months, no feature requests
4. DeltaInc: 85% seats, stable, renewal next month, CFO mentioned "reviewing vendors"
5. EchoLLC: 100% seats, workarounds everywhere, renewal 6 months, NPS 4
```

**Output:**
```
## Expansion Prioritization: Top 5 Accounts

### Ranked by Expansion Readiness

| Rank | Account | Score | Opportunity | Priority |
|------|---------|-------|-------------|----------|
| 1 | BetaCorp | 92 | High | 🔥 This week |
| 2 | EchoLLC | 68* | High | ⚠️ Fix first |
| 3 | AlphaTech | 55 | Medium | 🟢 This month |
| 4 | DeltaInc | 45 | Low | 🛡️ Defend first |
| 5 | GammaCo | 22 | Low | ⏸️ Adopt first |

---

### Detailed Analysis

#### #1: BetaCorp 🔥 Score: 92
**Status: HOT - Engage immediately**

| Signal | Value |
|--------|-------|
| Seat usage | 95% ✅ |
| Growth | 20% ✅ |
| Champion | Just promoted ✅ |
| Funding | Series B ✅ |
| Health | High ✅ |

**Why #1:** Perfect storm—growth, budget, champion momentum.
**Action:** Schedule this week. Lead with growth planning.

---

#### #2: EchoLLC ⚠️ Score: 68 (with asterisk)
**Status: FIX HEALTH FIRST, then expand**

| Signal | Value |
|--------|-------|
| Seat usage | 100% ✅ |
| Workarounds | Everywhere ✅ |
| Health | NPS 4 ⚠️ |
| Renewal | 6 months |

**Why #2:** High expansion potential BUT health issue.
NPS 4 suggests frustration, likely from hitting limits.

**Action:**
1. First: Address frustration (call, understand issues)
2. Then: Position upgrade as solution to pain
3. Risk: If we don't fix, they'll churn

---

#### #3: AlphaTech 🟢 Score: 55
**Status: WARM - Nurture this month**

| Signal | Value |
|--------|-------|
| Seat usage | 70% ⚠️ |
| Feature ask | Once (weak) |
| Renewal | 3 months |
| Health | Stable |

**Why #3:** Interest exists but not urgent.
**Action:** Explore premium interest, build case before renewal.
**Risk:** Don't push too hard before adoption improves.

---

#### #4: DeltaInc 🛡️ Score: 45
**Status: DEFEND - Not expansion, retention**

| Signal | Value |
|--------|-------|
| Seat usage | 85% OK |
| Renewal | Next month! |
| CFO signal | "Reviewing vendors" 🚨 |

**Why #4:** Expansion is wrong play here.
"Reviewing vendors" before renewal = churn risk.

**Action:**
1. Defensive posture
2. ROI documentation
3. Executive outreach
4. Do NOT discuss expansion until secured

---

#### #5: GammaCo ⏸️ Score: 22
**Status: WAIT - Focus on adoption**

| Signal | Value |
|--------|-------|
| Seat usage | 60% ⚠️ |
| Usage trend | Declining ⚠️ |
| Feature requests | None |
| Renewal | 12 months |

**Why #5:** Not ready—fix adoption first.
Declining usage + low utilization = at-risk, not expandable.

**Action:**
1. Adoption review call
2. Success planning
3. Understand declining usage
4. Table expansion for 6+ months

---

### Summary Matrix

| Account | Expansion | Timing | Play |
|---------|-----------|--------|------|
| BetaCorp | ✅ Yes | Now | Growth planning |
| EchoLLC | ✅ Yes | After fix | Solve + expand |
| AlphaTech | 🟡 Maybe | 30 days | Build interest |
| DeltaInc | ❌ No | N/A | Retention |
| GammaCo | ❌ No | 6+ mo | Adoption |

### This Week's Actions

1. **BetaCorp**: Schedule growth planning call
2. **EchoLLC**: Urgent health check call
3. **DeltaInc**: Pull ROI data, prep retention
4. **AlphaTech**: Send premium feature case study
5. **GammaCo**: Assign to adoption review queue
```

## Skill Boundaries

### What This Skill Does Well
- Identifying expansion signals systematically
- Scoring and prioritizing opportunities
- Sizing potential value
- Suggesting conversation approaches

### What This Skill Cannot Do
- Access actual usage data
- Know competitive dynamics
- Make pricing decisions
- Replace relationship judgment

### When to Escalate to Human
- Pricing exceptions
- Multi-product bundles
- Strategic accounts
- At-risk accounts needing expansion

## Iteration Guide

### Follow-up Prompts
- "Draft the expansion email for BetaCorp."
- "What objections might VP Data raise?"
- "Compare enterprise vs. à la carte for this account."
- "Build a 30-day expansion plan."

## References

- Lincoln Murphy Expansion Revenue
- Gainsight Expansion Playbooks
- SaaStr Expansion Revenue Guide
- ChurnZero Expansion Signals

## Related Skills

- `account-health` - Health context for expansion
- `churn-prediction` - Don't expand at-risk
- `qbr-preparation` - Discuss expansion in QBR

## Skill Metadata

- **Domain**: Customer Success
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 15-20 min per account
- **Prerequisites**: Usage data, account context
