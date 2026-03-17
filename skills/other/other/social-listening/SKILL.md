---
name: social-listening
description: Monitor social media and online mentions for brand sentiment, emerging issues, and conversation trends
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Social Listening

> Systematically monitor social media and online conversations to track brand sentiment, identify emerging issues, and spot opportunities.

## When to Use This Skill

- Brand health monitoring
- Crisis early warning
- Competitor tracking
- Campaign performance
- Customer insight gathering

## Methodology Foundation

Based on **Sprout Social methodology** and **Brandwatch analytics**, combining:
- Keyword monitoring
- Sentiment analysis
- Trend identification
- Influencer tracking

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Designs monitoring strategy | Tool selection |
| Creates keyword lists | Alert thresholds |
| Analyzes sentiment patterns | Response strategy |
| Identifies trends | Resource allocation |
| Suggests response approaches | Escalation calls |

## Instructions

### Step 1: Define Monitoring Scope

**Monitoring Categories:**

| Category | What to Track | Examples |
|----------|---------------|----------|
| Brand | Company name, products | "@CompanyName", "CompanyProduct" |
| People | Executives, spokespeople | CEO name, founder |
| Industry | Sector terms, trends | Industry keywords |
| Competitors | Competitor mentions | Competitor names |
| Issues | Potential crises | Product issues, service complaints |

### Step 2: Build Keyword Matrix

**Keyword Types:**
| Type | Purpose | Examples |
|------|---------|----------|
| Primary | Direct brand mentions | Brand name, product names |
| Secondary | Related conversations | Industry terms, use cases |
| Negative | Crisis indicators | "problem", "issue", "broken" |
| Competitor | Competitive intelligence | Competitor names, comparison |

### Step 3: Set Up Alerts

**Alert Levels:**

| Level | Trigger | Response Time |
|-------|---------|---------------|
| Green | Normal volume, positive/neutral | Daily review |
| Yellow | Elevated volume, mixed sentiment | Same-day review |
| Orange | High volume spike, negative trend | Hours |
| Red | Viral negative, crisis indicators | Immediate |

### Step 4: Analyze Findings

**Analysis Framework:**
- Volume trends (up/down/stable)
- Sentiment distribution (positive/neutral/negative)
- Key themes and topics
- Influential voices
- Geographic patterns

### Step 5: Report and Act

**Reporting Cadence:**
| Report | Frequency | Audience |
|--------|-----------|----------|
| Real-time alerts | As triggered | Crisis team |
| Daily digest | Daily | Marketing |
| Weekly summary | Weekly | Leadership |
| Monthly deep dive | Monthly | Strategy |

## Examples

### Example 1: Social Listening Strategy

**Input:**
```
Create a social listening strategy for:
- B2B SaaS company (project management)
- Main competitors: Asana, Monday, Notion
- Recent product launch: AI features
```

**Output:**
```
## Social Listening Strategy: Project Management SaaS

### Monitoring Objectives

| Objective | Priority | Key Questions |
|-----------|----------|---------------|
| Brand health | High | How are we perceived? |
| Product feedback | High | What do users say about AI features? |
| Competitive intel | Medium | What are competitors doing? |
| Industry trends | Medium | Where is PM software heading? |
| Crisis detection | High | Any emerging issues? |

---

### Keyword Matrix

#### Brand Keywords

| Category | Keywords | Platforms |
|----------|----------|-----------|
| Company Name | "[Company]", "@company" | All |
| Product Name | "[Product]", "[Product] app" | All |
| Misspellings | Common variants | All |
| Hashtags | #[Company], #[Product] | Twitter, LinkedIn |

#### Product Keywords

| Category | Keywords | Why Monitor |
|----------|----------|-------------|
| AI Features | "[Company] AI", "AI project management" | Launch feedback |
| Core Features | "[Company] tasks", "[Company] boards" | Product sentiment |
| Integrations | "[Company] Slack", "[Company] integration" | Partnership health |

#### Competitive Keywords

| Competitor | Keywords | What to Track |
|------------|----------|---------------|
| Asana | "Asana vs [Company]", "switching from Asana" | Win/loss signals |
| Monday | "Monday.com", "Monday vs [Company]" | Competitive positioning |
| Notion | "Notion for projects", "Notion PM" | Category overlap |
| General | "best project management", "PM tool 2026" | Category conversations |

#### Crisis Keywords

| Category | Keywords | Alert Level |
|----------|----------|-------------|
| Outage | "[Company] down", "[Company] not working" | Red |
| Security | "[Company] hack", "[Company] breach" | Red |
| Pricing | "[Company] expensive", "[Company] price increase" | Orange |
| Churn | "leaving [Company]", "cancelled [Company]" | Yellow |
| Bugs | "[Company] bug", "[Company] broken" | Yellow |

---

### Platform Strategy

| Platform | Focus | Keywords | Frequency |
|----------|-------|----------|-----------|
| Twitter/X | Real-time sentiment | All brand, crisis | Continuous |
| LinkedIn | B2B discussions | Industry, competitor | Daily |
| Reddit | Deep user feedback | r/projectmanagement, product | Daily |
| G2/Capterra | Review sentiment | Product reviews | Weekly |
| Hacker News | Tech community | Product, competitor | As trending |

---

### Alert Configuration

#### Red Alerts (Immediate Response)

**Triggers:**
- Volume spike >300% normal
- Sentiment shift >50% negative
- Viral post (>1000 engagements)
- Keywords: "outage", "down", "breach", "hack"

**Response:**
- Slack #crisis-alerts channel
- SMS to on-call team
- Auto-pause scheduled posts

---

#### Orange Alerts (Same-Day Response)

**Triggers:**
- Volume spike >100% normal
- Negative sentiment >30%
- Trending competitor comparison
- Keywords: "expensive", "worse", "frustrated"

**Response:**
- Slack #social-alerts
- Email to marketing lead
- Review within 4 hours

---

#### Yellow Alerts (Next-Day Review)

**Triggers:**
- Volume spike >50% normal
- Notable influencer mention
- Competitor activity spike
- Keywords: "considering", "alternative", "switching"

**Response:**
- Daily digest inclusion
- Assign for monitoring
- Review within 24 hours

---

### Analysis Template

#### Daily Report

```
## Social Listening Daily Digest
Date: [Date]

### Volume Summary
| Metric | Today | vs. Yesterday | vs. 7-Day Avg |
|--------|-------|---------------|---------------|
| Total Mentions | X | +/-Y% | +/-Z% |
| Brand Mentions | X | +/-Y% | +/-Z% |
| Sentiment Score | X | +/-Y | +/-Z |

### Sentiment Breakdown
- Positive: X%
- Neutral: Y%
- Negative: Z%

### Top Conversations
1. [Summary + Link]
2. [Summary + Link]
3. [Summary + Link]

### Competitor Activity
- Asana: [Notable activity]
- Monday: [Notable activity]
- Notion: [Notable activity]

### Action Items
- [ ] [Action if needed]

### Alert Status: GREEN/YELLOW/ORANGE/RED
```

---

### AI Feature Launch Monitoring

**Specific Keywords:**
- "[Company] AI"
- "AI project management"
- "[Company] automation"
- "AI features PM tool"

**What to Track:**
| Metric | Target | Alert If |
|--------|--------|----------|
| Mention volume | 2x normal | <50% or >300% |
| Sentiment | >60% positive | <40% positive |
| Feature requests | Document all | - |
| Bug reports | <5/day | >10/day |

**Competitor Response Monitoring:**
- Are competitors announcing similar features?
- How is our positioning being compared?
- What gaps are users identifying?
```

### Example 2: Quick Sentiment Analysis

**Input:**
```
Analyze this week's social mentions:
- Total mentions: 450 (up 30%)
- Positive: 40%
- Neutral: 35%
- Negative: 25%
- Top negative theme: "pricing"
- One viral tweet (15K RT): "Just discovered [Company] raised prices 40%"
```

**Output:**
```
## Quick Sentiment Analysis

### Alert Level: ORANGE

---

### Summary

| Metric | Value | Status |
|--------|-------|--------|
| Volume | 450 (+30%) | Elevated |
| Sentiment | 40% positive | Below target |
| Negative | 25% | Above normal |
| Viral Content | Yes | Action needed |

---

### Key Finding

**Pricing is dominating the conversation**

The viral tweet about 40% price increase is:
- Driving 30% volume spike
- Shifting sentiment negative
- Spreading misinformation (if price increase was different)

---

### Immediate Actions

| Action | Owner | Timeline |
|--------|-------|----------|
| Verify price increase details | Product/Biz | Immediate |
| Draft response to viral tweet | Comms | 2 hours |
| Prepare pricing FAQ | Support | Today |
| Monitor for escalation | Social | Ongoing |

---

### Response Options

**If price increase was less than 40%:**
```
Hi [Name], thanks for the feedback. Just to clarify—our
recent update increased [specific] pricing by [X%], not 40%.
Here's what changed and why: [link]

Happy to discuss if you have questions.
```

**If price increase was accurate:**
```
Hi [Name], we hear you. We know pricing changes are never
easy to absorb. Here's why we made this decision and what
you're getting in return: [link]

Our team is available if you'd like to discuss your account.
```

---

### Escalation Watch

Monitor for:
- Influencer pile-on
- Media pickup
- Support ticket spike
- Churn mentions
```

## Skill Boundaries

### What This Skill Does Well
- Designing monitoring strategies
- Creating keyword frameworks
- Analyzing sentiment patterns
- Structuring alert systems

### What This Skill Cannot Do
- Access social platforms
- Monitor in real-time
- Automatically respond
- Know your specific tools

## Iteration Guide

**Follow-up Prompts:**
- "Create response templates for [scenario]"
- "How should we handle [specific mention]?"
- "Design a competitor monitoring dashboard"
- "What should we track for [campaign]?"

## References

- Sprout Social Listening Guide
- Brandwatch Analytics Methodology
- Hootsuite Social Listening
- Meltwater Media Intelligence

## Related Skills

- `crisis-detector` - Early warning escalation
- `response-coordinator` - Crisis response
- `reputation-recovery` - Post-crisis rebuild

## Skill Metadata

- **Domain**: Crisis / Marketing
- **Complexity**: Intermediate
- **Mode**: cyborg
- **Time to Value**: 1-2 hours for strategy
- **Prerequisites**: Platform access, brand context
