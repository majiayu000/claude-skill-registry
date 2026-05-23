---
name: signal-monitoring
description: Track buying signals like funding announcements, job postings, tech changes, and company news to identify sales-ready prospects
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Signal Monitoring

> Identify high-intent prospects by monitoring buying signals including funding events, hiring patterns, technology changes, and company triggers.

## When to Use This Skill

- Building signal-based outreach campaigns
- Prioritizing outbound targets
- Identifying timing for re-engagement
- Creating trigger-based sequences
- Training SDRs on signal recognition

## Methodology Foundation

Based on **Bombora Intent Data methodology** and **6sense Buying Signal research**, categorizing:
- Funding signals (budget available)
- Hiring signals (need emerging)
- Technology signals (evaluation in progress)
- Company signals (change = opportunity)

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Categorizes signal types | Signal priority weights |
| Interprets signal meaning | Outreach timing |
| Suggests response templates | Personalization approach |
| Identifies signal sources | Tool investments |
| Creates monitoring playbooks | Team assignments |

## Instructions

### Step 1: Define Signal Categories

**Funding Signals (Strong):**
| Signal | Meaning | Response Time |
|--------|---------|---------------|
| Series A | Growth mode, building | 48 hours |
| Series B | Scaling, process needs | 24 hours |
| Series C+ | Enterprise ready | 1 week |
| IPO filing | Compliance focus | 2 weeks |

**Hiring Signals (Strong):**
| Signal | Meaning | Response Time |
|--------|---------|---------------|
| VP Sales hired | New leadership, new tools | 30 days |
| SDR team building | Scaling outbound | Immediate |
| RevOps hire | Process improvement | 1 week |
| Your buyer's title | Decision maker in seat | 48 hours |

**Technology Signals (Medium):**
| Signal | Meaning | Response Time |
|--------|---------|---------------|
| G2/Capterra research | Active evaluation | Immediate |
| Competitor uninstall | Opening created | 24 hours |
| Stack changes | Modernization | 1 week |
| Job posts w/ your tool | Already considering | 48 hours |

**Company Signals (Medium):**
| Signal | Meaning | Response Time |
|--------|---------|---------------|
| New office/expansion | Scaling | 1 week |
| M&A announcement | Integration needs | 2-4 weeks |
| New product launch | Growth initiative | 1 week |
| Leadership change | New priorities | 30 days |

### Step 2: Create Response Playbooks

For each signal:
1. Define ideal response time
2. Create outreach template
3. Specify personalization points
4. Set follow-up cadence

### Step 3: Monitor and Score

**Signal Scoring:**
```
Priority = Signal Strength × Recency × ICP Fit

Example:
- Series B (Strong) × This week (Fresh) × Tier 1 (Perfect)
- = High × High × High = TOP PRIORITY
```

## Examples

### Example 1: Signal Playbook

**Output:**
```
## Signal-Based Outreach Playbook

### Signal 1: Funding Announcement

**Signal Type:** Series A/B Funding
**Strength:** Very Strong
**Response Window:** 24-72 hours

**Why It Matters:**
- Budget just became available
- Growth mode activated
- Leadership making tool decisions
- Competitors will also reach out

**Outreach Template:**
```
Subject: Congrats on the Series [A/B], [FirstName]!

Hi [FirstName],

Just saw the news about [Company]'s Series [A/B]—congrats! $[Amount] to [stated use] is exciting.

I work with a lot of [similar companies] at your stage, and the #1 thing I hear is "[common challenge at this stage]."

Curious if that resonates? Would love to share what [similar customer] did when they hit this growth phase.

[Your name]
```

**Personalization Points:**
- Amount raised
- Stated use of funds
- Similar stage customers
- Their specific challenge

**Sequence:**
- Day 0: Email (above)
- Day 2: LinkedIn connect
- Day 4: Follow-up email
- Day 7: LinkedIn voice note
- Day 10: Final attempt

---

### Signal 2: Key Hire

**Signal Type:** VP Sales or CRO Hired
**Strength:** Very Strong
**Response Window:** 2-4 weeks post-start

**Why It Matters:**
- New leaders make changes in first 90 days
- They bring fresh perspective
- Often allocated budget for new tools
- Eager to make impact

**Outreach Template:**
```
Subject: Welcome to [Company], [FirstName]

Hi [FirstName],

Saw you just joined [Company] as [Title]—congrats! The move from [Previous Company] to [Company] looks like a great fit.

Quick question: what's on your 90-day priority list?

I ask because a lot of new [Titles] I talk to are focused on [common priority], and we help with exactly that.

No pitch—just curious if that's on your radar.

[Your name]
```

**Timing:**
- Week 2-3 after start date
- Avoid first week (onboarding chaos)
- Before 90-day planning locked in

---

### Signal 3: G2 Category Research

**Signal Type:** Product Research Intent
**Strength:** Strong
**Response Window:** Immediate

**Why It Matters:**
- Active buying signal
- They're comparing solutions
- Decision timeline is short
- First mover advantage

**Outreach Template:**
```
Subject: Saw you're researching [Category]

Hi [FirstName],

I noticed [Company] has been looking into [Category] solutions.

Rather than add to the noise, I'll just say: we work with [X] companies like [Similar Customer], and the main reason they chose us was [key differentiator].

If you're still evaluating, happy to share a quick comparison or even just the questions you should be asking vendors (even if you don't pick us).

Worth a 15-minute call?

[Your name]
```

**Urgency:** High—competitors seeing same signal
```

### Example 2: Signal Analysis

**Input:**
```
Analyze these signals for TargetCo:

Recent signals:
1. Series B funding ($25M) announced yesterday
2. Posted VP Sales job 2 weeks ago
3. Showing on G2 for "sales engagement" category
4. CEO posted about "scaling the sales team" last week
5. Currently uses Salesforce (good fit)
```

**Output:**
```
## Signal Analysis: TargetCo

### Signal Summary

| Signal | Type | Strength | Recency |
|--------|------|----------|---------|
| Series B ($25M) | Funding | 🔥 Very Strong | Yesterday |
| VP Sales posting | Hiring | 🔥 Very Strong | 2 weeks |
| G2 research | Intent | 🔥 Strong | Active |
| CEO post on scaling | Social | 🟢 Medium | Last week |
| Salesforce user | Tech | 🟢 Good fit | Current |

### Composite Score: 95/100 🎯 IMMEDIATE ACTION

---

### Signal Interpretation

**1. Series B + VP Sales = Perfect Storm**
- Money is available (Series B)
- They're building sales leadership (VP Sales)
- New VP will want to bring tools (90-day window)
- This is the exact moment to engage

**2. G2 Research = Active Buyer**
- They're not just thinking about it
- They're actively evaluating solutions
- Decision timeline: likely 30-60 days
- Competitors are also seeing this signal

**3. CEO Public Signal = Top-Down Priority**
- CEO talking about scaling = company priority
- Budget will be allocated
- Leadership alignment likely

---

### Recommended Approach

**Timing:** Engage TODAY
This combination of signals is rare. Every day delayed = competitor advantage.

**Multi-Channel Attack:**

**Day 0 (Today):**
- [ ] Email CEO with funding congrats
- [ ] Email VP Sales job inbox (if can find)
- [ ] LinkedIn connection to CEO
- [ ] LinkedIn connection to current Head of Sales

**Day 1:**
- [ ] Follow-up to anyone who opened
- [ ] LinkedIn voice note to CEO

**Day 3:**
- [ ] Second email with customer proof point
- [ ] Find other contacts in sales org

**Day 7:**
- [ ] Final push before VP Sales hire arrives

---

### Outreach Template (Priority)

```
Subject: Re: Series B + sales team scaling

Hi [CEO Name],

Congrats on the Series B! $25M to scale the team is exciting.

I noticed you're also hiring a VP Sales and researching sales engagement tools on G2—that's a perfect trifecta for building a world-class sales org.

Quick thought: a lot of CEOs I talk to say their biggest regret was waiting until the VP joined to evaluate tools. The VP inherits whatever you've already decided, and you lose 30-60 days.

Would you want to see what [Similar Company] did before their VP started? 15 minutes?

[Your name]
```

---

### Competitive Alert

**Assumption:** Competitors see same G2 signal.

**Response:**
- Move faster than competition
- Lead with insight, not pitch
- Offer value before they engage others
- Name-drop similar customers

---

### Success Probability

| Scenario | Probability |
|----------|-------------|
| Meeting booked in 7 days | 35% |
| Meeting booked in 30 days | 55% |
| Eventual opportunity | 70% |
| No engagement | 30% |

**Why High Probability:**
- Multiple strong signals aligned
- Timing is perfect
- Tech fit confirmed
- Active research behavior
```

## Skill Boundaries

### What This Skill Does Well
- Categorizing signal types
- Creating response playbooks
- Interpreting signal combinations
- Prioritizing outreach timing

### What This Skill Cannot Do
- Access signal databases
- Monitor signals automatically
- Know internal buying dynamics
- Guarantee signal accuracy

### When to Escalate to Human
- Strategic accounts
- Signal interpretation unclear
- Competitive situation
- Executive engagement

## References

- Bombora Intent Data Methodology
- 6sense Buying Signal Research
- ZoomInfo Intent Data Guide
- SalesLoft Signal-Based Selling

## Related Skills

- `icp-matching` - Qualify signal accounts
- `outbound-sequencer` - Build signal sequences
- `prospecting-research` - Deep dive on signals

## Skill Metadata

- **Domain**: SDR Automation
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 30 min per signal playbook
- **Prerequisites**: Signal source access
