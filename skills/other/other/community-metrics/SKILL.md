---
date: 2026-02-07
created: 2026-02-07
name: community-metrics
version: 1.0.0
description: "When the user wants to measure community health, build dashboards, create reports, or understand what metrics to track. Also use when the user mentions 'community metrics,' 'community analytics,' 'engagement metrics,' 'community health,' 'community ROI,' 'community report,' 'dashboard,' or 'KPIs for community.' For growth-specific metrics, see community-growth."
tags:
  - community-metrics
  - skill
---

# Community Metrics

You are an expert in community analytics and measurement. Your goal is to help users track the metrics that matter, avoid vanity metrics, and build reporting that connects community activity to business outcomes.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current Measurement
- What metrics do you currently track?
- What tools are you using for analytics?
- Who sees community reports? (team, leadership, stakeholders)

### 2. Business Context
- What business outcomes does the community need to prove?
- What's the relationship between community and revenue?
- What do stakeholders care about?

### 3. Platform
- Which platform? (determines available data)
- Do you have access to analytics APIs?
- Can you export data?

---

## The Metrics That Matter

Most community managers track vanity metrics (total members, total posts) that don't tell you if the community is healthy.

**Vanity metrics:** Make you feel good but don't drive decisions.
**Health metrics:** Tell you if the community is working.
**Business metrics:** Connect community to organizational value.

---

## Community Health Metrics

### Engagement Depth

| Metric | Formula | Healthy Range |
|--------|---------|--------------|
| DAU/MAU ratio | Daily active / Monthly active | 15-30% |
| Posts per active member | Total posts / Active members | 2-5/month |
| Reply rate | Threads with replies / Total threads | >60% |
| Average replies per thread | Total replies / Total threads | >3 |
| Content creation ratio | Members who post / Total active | >10% |

### Growth Health

| Metric | Formula | Healthy Range |
|--------|---------|--------------|
| Net member growth | New members - Churned members | Positive |
| Activation rate | Active in week 1 / Joined | >50% |
| 30-day retention | Active at day 30 / Joined | >40% |
| 90-day retention | Active at day 90 / Joined | >25% |
| Referral rate | Members who invited / Total active | >5% |

### Community Vitality

| Metric | What It Measures |
|--------|-----------------|
| Time to first response | How quickly questions get answered |
| Member-to-member ratio | % of engagement that's peer-to-peer vs. team-initiated |
| Unique contributors/week | How many distinct people are contributing |
| Lurker-to-participant conversion | % of readers who become posters over time |
| Returning member rate | % of active members from last period who are active again |

---

## Business Impact Metrics

These connect community to outcomes stakeholders care about.

### For Product Communities

| Metric | How to Measure |
|--------|---------------|
| Support deflection | Questions answered in community vs. support tickets |
| Product feedback generated | Ideas/bugs surfaced through community |
| Feature adoption | Community members vs. non-members using new features |
| NPS lift | NPS of community members vs. non-members |

### For Marketing/Growth

| Metric | How to Measure |
|--------|---------------|
| Community-influenced signups | Signups attributed to community content or referrals |
| Content generated | External content created from community discussions |
| Brand awareness | Community mentions, external shares, earned media |
| SEO value | Traffic to public community content |

### For Customer Success

| Metric | How to Measure |
|--------|---------------|
| Retention lift | Churn rate of community members vs. non-members |
| Expansion revenue | Upsell rate of community members vs. non-members |
| Time to value | Onboarding speed of community members vs. non-members |
| Customer satisfaction | CSAT of community members vs. non-members |

### Calculating Community ROI

```
Community ROI = (Value Generated - Community Cost) / Community Cost

Value Generated =
  Support deflection savings ($X per ticket deflected)
  + Revenue from community-influenced conversions
  + Retention lift (reduced churn * avg revenue per customer)
  + Content value (equivalent ad spend or production cost)
  + Product improvement value (features shipped from community feedback)

Community Cost =
  Team salaries + Platform costs + Event costs + Tool costs
```

**Named ROI examples:**
- **Salesforce Trailblazer:** $3.1B in influenced pipeline, 2.5M questions answered (vs. ~$50M/yr investment = 60x ROI on support deflection alone)
- **HubSpot Community:** Community members show 2x higher retention and 1.4x higher expansion revenue vs. non-community customers
- **Atlassian Community:** 70% peer-to-peer answer rate deflects ~$20M/yr in support costs
- **Gainsight Pulse:** Community members have 15% lower churn and 20% higher NPS
- **MongoDB:** Community saves an estimated $15M/yr in support costs through 65% peer answer rate

**Typical cost benchmarks:**
- Platform costs: $500-5,000/mo (Circle, Discourse, Khoros)
- CM salary: $75-110K/yr (US market, 2024)
- Average community team size at scale: 3-7 FTEs for 10K-100K member communities
- Support ticket cost avoided: $15-25 per ticket deflected to community

---

## Reporting Framework

### Weekly Pulse (Internal Team)
Quick check on community health. 5 minutes to review.

```
## Weekly Community Pulse — Week of [date]

### Key Numbers
- Active members: [X] (vs. [X] last week)
- New members: [X]
- Posts/messages: [X]
- Events held: [X] (attendance: [X])

### Highlights
- [Notable discussion or achievement]
- [Member win or contribution]

### Concerns
- [Any issues needing attention]

### This Week's Focus
- [Priority for the coming week]
```

### Monthly Report (Stakeholders)
Connects community metrics to business outcomes.

```
## Monthly Community Report — [Month Year]

### Summary
[2-3 sentence overview of community health and trends]

### Growth
| Metric | This Month | Last Month | Trend |
|--------|-----------|------------|-------|
| Total members | | | |
| New members | | | |
| Activation rate | | | |
| 30-day retention | | | |

### Engagement
| Metric | This Month | Last Month | Trend |
|--------|-----------|------------|-------|
| DAU/MAU | | | |
| Posts | | | |
| Active contributors | | | |
| Avg response time | | | |

### Business Impact
| Metric | This Month | Last Month | Trend |
|--------|-----------|------------|-------|
| Support tickets deflected | | | |
| Community-sourced feedback | | | |
| Community-attributed signups | | | |

### Top Wins
1. [Win with business context]
2. [Win with business context]

### Challenges & Plans
- [Challenge and what you're doing about it]

### Next Month Priorities
1. [Priority]
2. [Priority]
```

### Quarterly Business Review
Deep dive connecting community to business strategy.

- Trend analysis over 3 months
- ROI calculation
- Comparison to goals/OKRs
- Strategy adjustments
- Resource needs and requests

---

## Setting Community OKRs

### Framework

**Objective:** What you want to achieve (qualitative)
**Key Results:** How you'll measure it (quantitative)

### Example OKRs

**Objective: Build an active, self-sustaining community**
- KR1: Increase DAU/MAU from 15% to 25%
- KR2: Grow member-to-member reply ratio from 40% to 60%
- KR3: Launch 3 member-led programs

**Objective: Drive measurable business impact through community**
- KR1: Deflect 500 support tickets through community answers
- KR2: Generate 50 product feature requests from community discussions
- KR3: Achieve 20% higher retention for community members vs. non-members

---

## Analytics Tools

| Tool | Best For | Works With |
|------|----------|-----------|
| Platform native analytics | Basic engagement data | Your platform |
| Common Room | Unified community analytics | Multi-platform |
| Orbit | Member journey tracking | Developer communities |
| Google Analytics | Website/public community traffic | Web-based communities |
| Custom dashboards (Looker, Metabase) | Advanced cross-platform analysis | API-accessible platforms |

---

## Task-Specific Questions

1. What metrics are you currently tracking?
2. Who needs to see community reports, and what do they care about?
3. What business outcome are you trying to prove with community?
4. What analytics tools do you have access to?
5. How often do you report on community?

---

## Related Skills

- **community-strategy**: For aligning metrics with strategy
- **community-growth**: For growth-specific measurement
- **community-led-growth**: For connecting community to business growth metrics
- **community-ops**: For analytics tooling and infrastructure
- **retention-reactivation**: For retention measurement
