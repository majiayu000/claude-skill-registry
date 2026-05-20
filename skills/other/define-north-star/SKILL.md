---
name: define-north-star
description: Identify and validate your North Star Metric. Aligns product strategy with key business metric.
disable-model-invocation: false
user-invocable: true
---

# Define North Star Metric

**When to use:** During strategy planning, when metrics feel scattered, or when teams are optimizing different things

**Framework source:** Aakash Gupta's "Do you really need a North Star Metric?"

## Quick Start

1. Tell me: "Help me define our North Star metric" (or "Validate our current North Star")
2. I will check `context-library/business-info-template.md` and `context-library/strategy/` for your business model, growth stage, and existing metrics
3. I will ask about your core value, retention drivers, and business model to narrow candidates
4. We work through: Core Value identification, Metric formula (Frequency x Core Action x Breadth), Validation tests, Input metrics, and Guardrails
5. Output goes to `outputs/analyses/north-star-[quarter].md`

**Key decision:** Not every product needs a single North Star. Marketplaces, multi-product companies, and complex B2B may need a constellation of 2-4 metrics instead. I will help you decide which approach fits.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Strategy Docs | `context-library/strategy/*.md` | objective, business goal, success metric | Current metric direction, if any |
| Business Model | `context-library/business-info-template.md` | revenue model, growth focus, metrics | What drives the business |
| Metrics History | `context-library/metrics/*.md` | baseline, trends, retention data | Current metric baselines and movement |
| Meetings | `context-library/meetings/*.md` | "North Star", "KPI", "success metric" | Stakeholder expectations |
| PRDs | `context-library/prds/*.md` | success metric, target | Feature-level success indicators |

**Context Priority:**
1. Business model and revenue drivers FIRST
2. Current product stage and growth focus SECOND
3. Historical metrics data THIRD
4. Stakeholder expectations FOURTH

**Cross-Skill Links:**
- If building strategy → Link to `/write-prod-strategy` which uses North Star
- If defining feature metrics → Link to `/feature-metrics` which should ladder to North Star
- If analyzing retention → Link to `/retention-analysis` to identify leading indicators
- If setting up metrics framework → Link to `/metrics-framework`

---

## Step 0: Understanding Your Current Metric State

Before defining your North Star, let me understand where you are...

**Checking:**
- `context-library/business-info-template.md` for your business model
- `context-library/strategy/` for strategic direction
- `context-library/metrics/` for baseline metrics and trends
- `context-library/meetings/` for stakeholder priorities

**Based on what I find, I'll show you:**

### Current Metric State

**Business Model:**
- [How do you make money? Subscription / marketplace / ads / transactions?]
- [Growth stage: acquisition focus / retention focus / monetization focus?]
- [TAM: addressable market size]

**Existing Metrics:**
- [Current metrics dashboard: what are you tracking?]
- [Metric trends: what's moving, what's flat?]
- [Stakeholder focus: what does leadership care about?]

**Metric Gaps:**
- [Metrics that aren't connecting to decisions: vanity metrics?]
- [Decisions being made without data: where are you flying blind?]

### PM-Specific Diagnosis Questions

1. **Business Model Clarity:** Are you clear on what drives revenue/value in your business?
2. **Growth Focus:** Are you optimizing for growth, engagement, retention, or monetization?
3. **Team Alignment:** Do all teams agree on what success looks like?
4. **Data Quality:** Do you trust your existing metrics data?
5. **Decision Speed:** How quickly do you need to make decisions? (Hourly, daily, weekly, monthly?)

---

## What is a North Star Metric?

**Definition:** The single metric that best captures the core value your product delivers to customers.

---

## Do You Actually Need One?

### When a North Star Metric Works Well:

✅ **Product-led growth (PLG) companies**
- Self-serve product
- Clear activation moment
- Example: Slack's "Teams sending 2,000+ messages"

✅ **Consumer products with network effects**
- Value increases with usage
- Example: Facebook's "Daily Active Users"

✅ **Early-stage companies (Seed to Series B)**
- Need focus and alignment
- Limited resources require prioritization

---

### When a North Star Can Be Misleading:

❌ **Marketplace/multi-sided platforms**
- Optimizing for buyers might hurt sellers
- Need balanced metrics for both sides
- Example: Airbnb tracks host AND guest metrics

❌ **Complex B2B enterprise products**
- Multiple stakeholders with different needs
- Example: Salesforce has different success metrics by user role

❌ **Companies with multiple business models**
- Each line of business may need different metrics
- Example: Amazon (retail vs AWS vs ads)

---

## The North Star Framework

A good North Star Metric has three components:

### 1. Core Action
What is the one thing users do that indicates they're getting value?

**Examples:**
- Spotify: Time spent listening
- Airbnb: Nights booked
- Slack: Messages sent
- LinkedIn: Weekly active users
- Notion: Documents created

---

### 2. Frequency
How often should this action happen to indicate real value?

**Examples:**
- Daily: Social apps (Instagram, TikTok)
- Weekly: Productivity tools (Notion, Figma)
- Monthly: Marketplace (Airbnb, Uber)
- Per-session: E-commerce (Amazon)

---

### 3. Breadth
Who needs to do this action for it to count?

**Examples:**
- Individual users: Netflix (hours watched per user)
- Teams: Slack (active teams sending messages)
- Multi-sided: Uber (completed trips)

---

## Formula: [Frequency] × [Core Action] × [Breadth]

**Examples:**

**Slack:**
- Frequency: Daily
- Core Action: Messages sent
- Breadth: Active teams
- **North Star:** Daily Active Teams sending 2,000+ messages

**Airbnb:**
- Frequency: Per transaction
- Core Action: Nights booked
- Breadth: Guests
- **North Star:** Nights booked

**Spotify:**
- Frequency: Weekly
- Core Action: Time listening
- Breadth: Active users
- **North Star:** Weekly Active Users × Hours listened

---

## How to Find Your North Star

### Step 1: Identify Your Core Value

Answer these questions:

1. **What problem does your product solve?**
   - Not features, but the actual problem

2. **When do users say "aha, this is valuable"?**
   - Look at retention data: what do retained users do differently?

3. **What action most correlates with retention?**
   - Run cohort analysis
   - Compare churned vs retained users

Use this prompt:
```
Use /define-north-star and reference context-library/business-info-template.md

Help me identify our core value:
- Product: [describe your product]
- Customer problem: [what problem you solve]
- Retention data: [describe retained vs churned user behavior]

What action best captures when users get value?
```

---

### Step 2: Validate Against Criteria

Your North Star should be:

✅ **Measurable**
- Can you track it accurately?
- Do you have the data infrastructure?

✅ **Actionable**
- Can teams influence it with their work?
- Are there levers to pull?

✅ **Leading indicator**
- Does it predict revenue/retention?
- Or is it just a vanity metric?

✅ **Understandable**
- Can everyone in the company explain it?
- Does it pass the "grandma test"?

✅ **Captures sustainable value**
- Not gameable
- Reflects real customer value

---

### Step 3: Test for Tradeoffs

**The real test:** Does it help you make hard decisions?

**Example decision scenarios:**

**Scenario 1:** You can either:
- A) Improve conversion rate +10% (more signups)
- B) Improve Day 7 retention +5% (better activation)

Which moves your North Star more?

**Scenario 2:** Marketing wants to:
- Run a campaign that brings 10K new users (low quality)
- Or 1K highly-targeted users (high quality)

Which aligns with your North Star?

**If your North Star doesn't help you choose, it's not working.**

---

## Common North Star Metrics by Category

### Social / Community Products
- **Facebook:** Daily Active Users (DAU)
- **Instagram:** Daily Active Users sharing stories
- **TikTok:** Time spent watching videos
- **Discord:** Weekly Active Servers

### Productivity / Collaboration
- **Slack:** Daily Active Teams (2,000+ messages)
- **Notion:** Weekly Active Users creating docs
- **Figma:** Weekly Active Designers
- **Asana:** Tasks completed per week

### Marketplace / Transaction
- **Airbnb:** Nights booked
- **Uber:** Completed trips
- **Etsy:** Gross Merchandise Value (GMV)
- **DoorDash:** Orders completed

### Media / Content
- **Netflix:** Hours watched per member
- **Spotify:** Hours listened per subscriber
- **Medium:** Time reading articles
- **YouTube:** Watch time

### SaaS / B2B
- **Salesforce:** Active users per account
- **HubSpot:** Weekly active contacts managed
- **Stripe:** Payment volume processed
- **Dropbox:** Active files shared

---

## Red Flags: Bad North Star Metrics

### ❌ Revenue as North Star

**Problem:** Revenue is an outcome, not a value metric
- Doesn't tell you WHY customers pay
- Can go up even if product value decreases (price increases)
- Lagging indicator (slow to respond)

**Exception:** Marketplaces where GMV = value delivered

---

### ❌ Number of Features Used

**Problem:** More features ≠ more value
- Can be gamed by adding trivial features
- Doesn't capture depth of value

**Better:** Usage of core feature

---

### ❌ Vanity Metrics (Signups, Downloads, Page Views)

**Problem:** No correlation to actual value or retention
- Can grow while business dies
- Doesn't reflect customer success

**Better:** Activation rate, active users

---

## From North Star to Execution

Once you have your North Star, break it down into input metrics:

### Example: Airbnb's "Nights Booked"

**Input Metrics (things that drive Nights Booked):**
1. **Supply side:**
   - Active listings
   - Listing quality score
   - Host responsiveness

2. **Demand side:**
   - Search-to-booking conversion
   - Repeat booking rate
   - Average trip length

3. **Trust & safety:**
   - Review ratings
   - Dispute rate
   - Insurance claims

**Each team owns input metrics that ladder up to North Star.**

---

## How Teams Use the North Star

### Product Team:
"Will this feature increase Nights Booked?"
- If yes → prioritize
- If no → deprioritize

### Marketing Team:
"Will this campaign bring users who book nights?"
- Focus on qualified traffic, not just signups

### Engineering Team:
"Will improving performance increase Nights Booked?"
- Faster search → more bookings → prioritize

### Customer Success:
"Are our customers booking nights regularly?"
- If not, something's wrong with value delivery

---

## Evolving Your North Star

**Your North Star should evolve as your company matures:**

**Early stage (0-100K users):**
- Focus: Activation and retention
- North Star: Weekly Active Users

**Growth stage (100K-1M users):**
- Focus: Sustainable growth loops
- North Star: Weekly Active Users engaging with core feature

**Scale stage (1M+ users):**
- Focus: Monetization and expansion
- North Star: Revenue per active user OR engagement + monetization hybrid

**Enterprise stage:**
- Multiple North Stars for different business units

---

## Real-World Example: Slack

**Slack's North Star Evolution:**

**2014-2015 (Early):**
- North Star: Teams sending 2,000+ messages
- Why: Indicated real team adoption

**2016-2018 (Growth):**
- North Star: Daily Active Teams (2,000+ messages)
- Why: Added frequency dimension

**2019-2021 (Scale):**
- North Star: Weekly Active Users + Messages sent
- Why: Balance growth with engagement

**2022+ (Enterprise):**
- North Star: Active paid seats
- Why: Focus on monetization at scale

**Key insight:** North Star evolved with company stage

---

## Worksheet: Define Your North Star

### 1. Core Value
What problem do you solve? ___________

### 2. Core Action
What do users do when they get value? ___________

### 3. Retention Correlation
What action correlates most with retention? ___________

### 4. Frequency
How often should users do this action? ___________

### 5. Breadth
Who needs to do this? (Individual, team, transaction) ___________

### 6. North Star Candidate
**Formula:** [Frequency] × [Core Action] × [Breadth]
___________

### 7. Validation Checks
- [ ] Measurable? (Can we track it?)
- [ ] Actionable? (Can teams influence it?)
- [ ] Leading indicator? (Predicts retention/revenue?)
- [ ] Understandable? (Everyone gets it?)
- [ ] Sustainable? (Reflects real value?)

### 8. Tradeoff Test
Describe 2-3 hard decisions your North Star should help you make:
___________

---

## Alternative: Constellation of Metrics

**If a single North Star doesn't work for you, use a constellation:**

**Example: Amazon**
- Customer satisfaction (NPS)
- Selection (# of products)
- Price (value for money)
- Convenience (delivery speed)

**Rule:** No more than 4 metrics in your constellation
- More than 4 = unfocused strategy

---

## Guardrail Metric Guidance

**Every North Star needs 2-3 guardrail metrics to prevent destructive optimization.**

Without guardrails, teams will find ways to game the North Star that hurt the business. The question to ask: "If we aggressively optimized [North Star], what could go wrong? That is your guardrail."

**Common guardrail patterns:**

1. **Quality metric** (e.g., NPS, CSAT, support ticket volume) -- Prevents growth at the expense of user satisfaction. Example: If North Star is "Weekly Active Users," a guardrail of "NPS stays above 40" prevents acquiring low-quality users who churn immediately.

2. **Revenue/monetization metric** (e.g., ARPU, conversion rate, LTV) -- Prevents engagement optimization that does not generate revenue. Example: If North Star is "time spent in app," a guardrail of "ARPU stays above $12/mo" prevents building addictive features that do not convert to paid.

3. **Efficiency metric** (e.g., CAC, cost per transaction, infrastructure cost per user) -- Prevents growth that is not sustainable. Example: If North Star is "completed transactions," a guardrail of "CAC stays below $50" prevents buying growth that does not pay back.

**How to define guardrails:**
- Set a minimum threshold (floor), not a target. Guardrails are "do not go below X," not "try to reach Y."
- Define what happens if breached: who gets alerted, what investigation to run, and what corrective action to take.
- Review guardrails quarterly. As the product matures, guardrail thresholds may need adjustment.

---

## Output Template

### North Star Metric Analysis: [Company Name]

**Recommended North Star:** [Metric Name]
**Formula:** [How it is calculated]
**Current Value:** [Baseline]
**Target:** [Goal + timeline]

#### Validation
- Core Value Test: [Pass/Fail + reasoning]
- Leading Indicator Test: [Pass/Fail + reasoning]
- Tradeoff Test: [Pass/Fail + reasoning]

#### Input Metrics (Driver Tree)

| Input Metric | Current | Target | Owner | Leading Indicator For |
|-------------|---------|--------|-------|----------------------|
| [Metric 1] | [Value] | [Goal] | [Team/Person] | [What it predicts] |
| [Metric 2] | [Value] | [Goal] | [Team/Person] | [What it predicts] |
| [Metric 3] | [Value] | [Goal] | [Team/Person] | [What it predicts] |

#### Guardrail Metrics

| Guardrail | Why | Threshold | Action if Breached |
|-----------|-----|-----------|-------------------|
| [Quality metric] | [Prevents what failure mode] | [Do not drop below X] | [Who investigates + what they do] |
| [Revenue metric] | [Prevents what failure mode] | [Do not drop below X] | [Who investigates + what they do] |
| [Efficiency metric] | [Prevents what failure mode] | [Do not drop below X] | [Who investigates + what they do] |

#### Recommendation
[2-3 sentences on whether to adopt/keep/change the North Star, with timeline for review. Example: "Adopt Weekly Active Teams as your North Star for the next 6 months. Review at the end of Q3 to determine if the metric still reflects core value delivery as you move into enterprise. Schedule a North Star review meeting for September."]

---

## Common Mistakes

❌ **Changing your North Star every quarter**
- Causes whiplash across teams
- Choose one and stick with it for 6-12 months

❌ **Having different North Stars by team**
- Defeats the purpose of alignment
- Everyone should rally around one metric

❌ **Making it too complex**
- If it requires a 10-minute explanation, it's too complex
- Should fit in one sentence

❌ **Ignoring guardrails**
- Optimize for North Star, but don't break the product
- Always have 3-5 guardrail metrics

---

## Output Integration

### Where Files Go

**North Star definition:**
- Active work: `outputs/analyses/north-star-[quarter].md` (your working definition)
- When finalized: Move to `context-library/metrics/north-star-[year].md` for reference
- Share widely: This becomes the basis for all team metrics

### Link to Other Work

After defining North Star:
- **Reference in strategy** - "Our North Star metric is [X]" in `/write-prod-strategy`
- **Guide PRDs** - All feature PRDs should explain how they support North Star
- **Inform roadmap** - Roadmap priorities are evaluated by North Star impact
- **Dashboard anchor** - North Star sits at top of your metrics dashboard

### Cross-Skill Integration

**Feeds into:**
- `/write-prod-strategy` - North Star becomes the Objective component
- `/metrics-framework` - North Star is your lagging metric anchor
- `/feature-metrics` - Feature success metrics should ladder to North Star
- `/status-update` - Progress toward North Star is tracked in updates

**Pulls from:**
- `context-library/business-info-template.md` - Business model informs what matters
- `context-library/metrics/` - Historical data validates metric choices
- `/retention-analysis` - Understand what drives long-term success
- `/activation-analysis` - Early indicators of North Star movement

---

## Related Skills

- `/activation-analysis` - Find your activation metric
- `/feature-metrics` - Choose experiment metrics that ladder to North Star
- `/metrics-framework` - Understand leading vs lagging metrics
- `/retention-analysis` - Measure what drives retention and North Star
- `/write-prod-strategy` - Connect North Star to strategy

---

---

## Output Quality Self-Check

Before delivering the North Star analysis, verify:

- [ ] **Metric is one sentence:** The North Star can be stated in a single clear sentence (e.g., "Weekly Active Teams sending 2,000+ messages"). If it needs a paragraph to explain, it is too complex.
- [ ] **Formula is explicit:** The calculation is defined precisely enough that an analyst could implement it in SQL. No ambiguity about what counts and what does not.
- [ ] **Baseline and target are included:** Current value and target value with timeline are both specified. "Improve engagement" is not a North Star.
- [ ] **Three validation tests passed:** Core Value Test, Leading Indicator Test, and Tradeoff Test are each explicitly addressed with pass/fail and reasoning.
- [ ] **Input metrics defined:** At least 3 input metrics are identified with owners, showing how teams can influence the North Star.
- [ ] **Guardrails defined:** 2-3 guardrail metrics are specified with thresholds and breach actions. A North Star without guardrails is dangerous.
- [ ] **Tradeoff scenario tested:** At least one real decision scenario is described where the North Star helps choose between two options. If it does not help decide, it is not working.
- [ ] **Review timeline set:** A specific date to revisit the North Star is recommended (typically 6-12 months).

---

**Framework credit:** Adapted from Aakash Gupta's North Star Metric framework. Read the full article: https://www.news.aakashg.com/p/do-you-really-need-a-north-star-metric
