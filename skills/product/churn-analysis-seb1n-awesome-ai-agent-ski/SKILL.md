---
name: churn-analysis
description: Identify at-risk customer accounts by analyzing usage patterns, engagement signals, and support history to generate churn risk scores and intervention recommendations. Use when the user requests churn analysis or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Churn Analysis

Detect early warning signs of customer churn by aggregating usage telemetry, support interactions, billing history, and engagement metrics into a composite risk score per account. This skill segments accounts into risk tiers and produces actionable intervention playbooks tailored to each tier, enabling CS teams to proactively retain revenue.

## Workflow

1. **Collect usage and engagement data** — Pull metrics across product analytics (DAU, feature adoption, session duration), support history (ticket volume, CSAT scores, escalations), billing signals (late payments, downgrade requests, contract end dates), and engagement touchpoints (email opens, webinar attendance, QBR participation). Normalize all metrics to a consistent time window (typically 90 days trailing).

2. **Define churn signals** — Establish the leading indicators that correlate with churn in your specific context. Common signals include: login frequency dropping below 50% of the account's historical average, a spike in support tickets (3x baseline) within 30 days, missed or late renewal payment, champion contact leaving the company, feature adoption plateau (no new features used in 60 days), and declining NPS scores on consecutive surveys.

3. **Score risk per account** — Compute a weighted composite score from 0 (healthy) to 100 (imminent churn) for each account. Weight signals by their predictive power — usage decline typically carries 35% weight, support sentiment 25%, billing signals 20%, and engagement metrics 20%. Adjust weights based on historical churn correlation data if available. Accounts missing data for a signal category receive a neutral score for that dimension with a data-quality flag.

4. **Segment into risk tiers** — Bucket accounts into four tiers based on their composite score: **Critical** (75-100) — immediate intervention required, likely to churn within 30 days. **High** (50-74) — concerning trends, intervention needed within 2 weeks. **Medium** (25-49) — early warning signs, monitor and engage proactively. **Healthy** (0-24) — on track, maintain regular cadence.

5. **Generate intervention recommendations** — For each tier, produce specific action plans. Critical: executive sponsor outreach, emergency success plan, potential concessions or credits. High: CSM-led deep dive call, custom training session, product roadmap preview. Medium: automated check-in email sequence, in-app tips targeting underused features, invite to community events. Healthy: upsell/cross-sell opportunity identification, referral program invitation.

## Usage

Provide account data or describe the account portfolio you want analyzed. The agent will compute risk scores and return tiered recommendations.

```
Analyze the churn risk for our Q1 cohort of 200 accounts. Here's the usage
data export. Identify the top 10 at-risk accounts and recommend interventions.
```

## Examples

### Example 1: Cohort risk analysis with scoring table

**Input:** Usage and engagement data for 8 accounts over the past 90 days.

**Output:**

| Account | Plan | Risk Score | Tier | Key Signals | Recommended Action |
|---------|------|-----------|------|-------------|-------------------|
| Acme Corp | Enterprise | 88 | Critical | Logins down 72%, 14 tickets in 30d, renewal in 18d | Exec sponsor call within 48h, offer dedicated onboarding reset, prepare 2-month extension |
| Bolt Inc | Pro | 71 | High | Feature adoption stalled, champion left org, NPS dropped from 8→4 | CSM deep-dive on use cases, identify new champion, schedule product roadmap session |
| Cedar Ltd | Enterprise | 63 | High | API usage down 45%, 2 escalated tickets, QBR declined | Technical health check, assign SE for integration review, CSM outreach to new stakeholder |
| Dash Co | Pro | 42 | Medium | Session duration declining, stopped attending webinars | Trigger re-engagement email series, in-app walkthrough for new features launched in Q4 |
| Echo LLC | Starter | 38 | Medium | Login frequency down 30%, no support contact in 60d | Automated check-in email, offer free training session |
| Forge Inc | Enterprise | 22 | Healthy | Stable usage, positive CSAT, expanding seat count | Propose enterprise add-on package, invite to advisory board |
| Grid Corp | Pro | 15 | Healthy | Growing feature adoption, 2 referrals made | Send referral program upgrade incentive, case study candidate |
| Haven Ltd | Starter | 8 | Healthy | High engagement, recent plan upgrade | Monitor, include in customer spotlight newsletter |

**Summary:** 2 accounts critical (25% of ARR at risk), 2 high, 2 medium, 2 healthy. Recommended immediate action on $480K combined ARR in critical tier.

### Example 2: Individual account churn risk deep dive

**Input:** "Analyze churn risk for Acme Corp — enterprise account, $240K ARR, 18 days to renewal."

**Output:**

**Acme Corp — Risk Score: 88/100 (Critical)**

| Signal Category | Weight | Score | Evidence |
|----------------|--------|-------|----------|
| Usage Decline | 35% | 92 | Daily active users dropped from 145 to 41 over 60 days. Core workflow (report generation) usage down 80%. |
| Support Sentiment | 25% | 85 | 14 tickets in past 30 days (baseline: 3/month). Two P1 escalations unresolved. CSAT on last 3 tickets: 2, 1, 2. |
| Billing Signals | 20% | 78 | Renewal in 18 days, no renewal discussion initiated. Finance team requested contract terms doc (often precedes vendor evaluation). |
| Engagement | 20% | 90 | Declined last two QBR invites. Zero email opens in past 30 days. Primary champion (VP Ops) left the company 6 weeks ago. |

**Intervention Plan:**
1. **Day 0-2:** VP of CS calls Acme's CTO directly. Acknowledge the degraded experience and unresolved escalations.
2. **Day 2-5:** Assign a dedicated SE to resolve the two open P1 tickets. Provide daily status updates.
3. **Day 5-10:** Schedule an on-site success planning session with the new decision-maker. Present a 90-day recovery roadmap.
4. **Day 10-15:** Offer a concession package: 60-day contract extension at no cost, dedicated Slack channel for real-time support.
5. **Day 15-18:** Secure verbal renewal commitment or escalate to CRO for executive negotiation.

## Best Practices

- Recalculate risk scores weekly for critical and high-tier accounts, monthly for medium and healthy tiers to balance signal freshness with noise reduction.
- Validate your signal weights quarterly by back-testing against actual churn events — the default 35/25/20/20 split is a starting point, not a universal truth.
- Combine quantitative signals with qualitative CSM notes — a CSM flagging "bad vibes on the last call" is a legitimate signal that models miss.
- Track intervention outcomes to build a feedback loop: which actions actually prevented churn vs. delayed it vs. had no effect.
- Separate voluntary churn (dissatisfaction) from involuntary churn (payment failure, company closure) in your analysis, as they require completely different interventions.
- Account for seasonality — some industries have natural usage dips (retail post-holiday, education during summer) that should not inflate risk scores.

## Edge Cases

- **New accounts (under 90 days)** — Insufficient historical data to compute meaningful trends. Use onboarding milestone completion rate as a proxy signal instead of usage decline.
- **Accounts with a single power user** — All usage is concentrated in one person. If that person's activity drops, the risk score should weight this more heavily than a distributed usage decline across many users.
- **Free-to-paid conversion cohort** — Recently converted accounts may show low engagement compared to established accounts but are actually ramping up. Apply a different baseline for accounts in their first renewal cycle.
- **Multi-product accounts** — Churn risk should be assessed per product line, not just at the account level. An account may be healthy on Product A but churning on Product B, and a blended score hides this.
- **Accounts in active expansion** — A temporary dip in per-seat usage metrics might reflect rapid seat additions (denominator growth) rather than actual disengagement. Normalize usage by active seats, not total seats.
