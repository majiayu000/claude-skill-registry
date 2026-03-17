---
name: product-management
description: Product management expertise for product strategy, roadmap planning, feature prioritization (RICE, ICE, MoSCoW), customer research, A/B testing, product analytics, and product-market fit. Use when building product roadmaps, prioritizing features, or defining product strategy.
---

# Product Management Expert

Comprehensive product frameworks for strategy, roadmapping, prioritization, and product-market fit.

## Product Strategy

### Product Vision Framework

```
VISION COMPONENTS:

TARGET CUSTOMER:
- Who are we building for?
- What segments? What personas?

CUSTOMER NEED:
- What problem are we solving?
- What job to be done?

KEY BENEFIT:
- Primary value proposition
- Why customers will choose us

DIFFERENTIATOR:
- What makes us unique?
- Competitive advantage

AMAZON PRESS RELEASE FORMAT:
- Headline
- Summary (who, what, when, where, why)
- Problem statement
- Solution description
- Customer quote
- How to get started
```

### Product-Market Fit

```
PMF INDICATORS:

QUANTITATIVE:
- 40%+ would be "very disappointed" without product (Sean Ellis)
- Strong organic growth/referrals
- Low churn, high retention
- Improving unit economics

QUALITATIVE:
- Customers actively advocating
- Word of mouth driving acquisition
- Pull from market (not push)
- Customers expanding usage

PMF SURVEY:
"How would you feel if you could no longer use [product]?"
- Very disappointed → Target 40%+
- Somewhat disappointed
- Not disappointed

PMF STAGES:
1. Problem-Solution Fit: Validated problem worth solving
2. Product-Market Fit: Solution resonates with market
3. Business Model Fit: Sustainable economics
4. Scale: Growth mechanics work
```

### Jobs to Be Done (JTBD)

```
JOB STATEMENT:
When [situation], I want to [motivation], so I can [expected outcome].

FORCES OF PROGRESS:
Push: Current pain/frustration
Pull: Attraction to new solution
Anxiety: Concerns about switching
Habit: Comfort with status quo
```

See [Customer Research Methods](./references/customer-research-methods.md) for detailed JTBD methodology and interview techniques.

## Roadmap Planning

### Roadmap Types

| Type          | Timeframe  | Audience            | Detail Level |
| ------------- | ---------- | ------------------- | ------------ |
| **Vision**    | 2-5 years  | Board, executives   | Themes       |
| **Strategic** | 1-2 years  | Leadership          | Initiatives  |
| **Release**   | 3-6 months | Teams, stakeholders | Features     |
| **Sprint**    | 2-4 weeks  | Dev team            | User stories |

### OKR Framework for Product

```
PRODUCT OKR STRUCTURE:

OBJECTIVE: [Qualitative goal]

KEY RESULT 1: [Metric] from [X] to [Y]
KEY RESULT 2: [Metric] from [X] to [Y]
KEY RESULT 3: [Metric] from [X] to [Y]

EXAMPLE:
O: Become the preferred solution for enterprise customers
KR1: Increase enterprise NPS from 40 to 60
KR2: Reduce enterprise churn from 8% to 4%
KR3: Increase enterprise ACV from $50K to $75K
```

## Feature Prioritization

### RICE Framework

```
RICE SCORE = (Reach x Impact x Confidence) / Effort

REACH: How many customers affected per quarter
- Count: Number of users, customers, transactions

IMPACT: Effect on individual customer
- 3 = Massive
- 2 = High
- 1 = Medium
- 0.5 = Low
- 0.25 = Minimal

CONFIDENCE: How sure are we
- 100% = High confidence
- 80% = Medium
- 50% = Low

EFFORT: Person-months of work
- Engineering time
- Design time
- PM time

EXAMPLE:
| Feature | Reach | Impact | Conf | Effort | RICE |
|---------|-------|--------|------|--------|------|
| A | 5000 | 2 | 80% | 3 | 2667 |
| B | 1000 | 3 | 100% | 1 | 3000 |
| C | 10000 | 1 | 50% | 5 | 1000 |
```

### ICE Framework

```
ICE SCORE = Impact x Confidence x Ease

IMPACT (1-10):
How much will this move our key metric?

CONFIDENCE (1-10):
How sure are we about impact estimate?

EASE (1-10):
How easy to implement?

Note: Simpler than RICE, good for quick decisions
```

### MoSCoW Method

| Category        | Definition                  | Guidance              |
| --------------- | --------------------------- | --------------------- |
| **Must Have**   | Non-negotiable for release  | Core functionality    |
| **Should Have** | Important but not critical  | High value, can defer |
| **Could Have**  | Nice to have                | If time permits       |
| **Won't Have**  | Out of scope (this release) | Future consideration  |

### Kano Model

```
CATEGORIES:

BASIC (Must-be):
- Expected features
- Absence causes dissatisfaction
- Example: Login functionality

PERFORMANCE (Linear):
- More is better
- Satisfaction proportional to fulfillment
- Example: Speed, capacity

DELIGHTERS (Excitement):
- Unexpected features
- Absence doesn't cause dissatisfaction
- Presence greatly increases satisfaction
- Example: Innovative features
```

## Customer Research

### Research Methods

| Method              | When to Use              | Sample Size | Time      |
| ------------------- | ------------------------ | ----------- | --------- |
| **User Interviews** | Deep understanding       | 5-15        | 2-4 weeks |
| **Surveys**         | Quantify findings        | 100-1000+   | 1-2 weeks |
| **Usability Tests** | Validate designs         | 5-8         | 1-2 weeks |
| **A/B Tests**       | Compare options          | 1000+       | 2-4 weeks |
| **Analytics**       | Understand behavior      | N/A         | Ongoing   |
| **Card Sorting**    | Information architecture | 15-30       | 1 week    |
| **Diary Studies**   | Long-term behavior       | 10-20       | 2-4 weeks |

See [Customer Research Methods](./references/customer-research-methods.md) for detailed interview frameworks, persona templates, and usability testing protocols.

## Product Analytics

### Key Metrics Framework

```
PIRATE METRICS (AARRR):

ACQUISITION:
- How do users find us?
- Metrics: Traffic, signups, installs

ACTIVATION:
- First positive experience
- Metrics: Onboarding completion, first value

RETENTION:
- Do they come back?
- Metrics: DAU/MAU, cohort retention

REVENUE:
- Do they pay?
- Metrics: Conversion, ARPU, LTV

REFERRAL:
- Do they tell others?
- Metrics: NPS, referral rate, viral coefficient
```

### Product Health Metrics

| Metric               | Formula                           | Target   |
| -------------------- | --------------------------------- | -------- |
| **DAU/MAU**          | Daily users / Monthly users       | 20-50%+  |
| **Activation Rate**  | Completed setup / Signups         | 40-60%+  |
| **Feature Adoption** | Users using feature / Total users | Varies   |
| **Time to Value**    | Days to first value               | Minimize |
| **Power Users**      | Heavy users / Total users         | 15-25%   |

See [Analytics and Experimentation](./references/analytics-and-experimentation.md) for detailed cohort analysis, retention benchmarks, and event tracking strategies.

## A/B Testing

### Experiment Framework

```
EXPERIMENT DESIGN:

HYPOTHESIS:
If we [change], then [metric] will [improve/decrease] because [rationale].

METRICS:
- Primary: The metric you're trying to move
- Secondary: Other metrics to monitor
- Guardrails: Metrics that shouldn't degrade

SAMPLE SIZE:
Use calculator based on:
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical significance (usually 95%)
- Power (usually 80%)

DURATION:
- At least 1 business cycle
- Adequate sample size
- Account for novelty effects
```

### Decision Framework

- **Ship**: Stat sig + practical sig + no negative guardrails
- **Iterate**: Directionally positive but not stat sig, or mixed results
- **Kill**: No effect or negative impact
- **Investigate**: Unexpected results, large variance, segment differences

See [Analytics and Experimentation](./references/analytics-and-experimentation.md) for detailed statistical concepts, common pitfalls, and segmentation analysis.

## Product Launches

### Launch Checklist

```
PRE-LAUNCH:
- [ ] Feature complete and tested
- [ ] Documentation ready
- [ ] Support team trained
- [ ] Marketing materials prepared
- [ ] Sales team enabled
- [ ] Beta feedback incorporated
- [ ] Success metrics defined

LAUNCH:
- [ ] Staged rollout plan
- [ ] Monitoring dashboards live
- [ ] War room established
- [ ] Communication sent
- [ ] Feature flags enabled

POST-LAUNCH:
- [ ] Monitor metrics and feedback
- [ ] Address critical issues
- [ ] Gather early learnings
- [ ] Celebrate wins
- [ ] Retrospective scheduled
```

### Go-to-Market Plan

| Element               | Description                  |
| --------------------- | ---------------------------- |
| **Target Segment**    | Who is this for?             |
| **Value Proposition** | Why will they care?          |
| **Pricing**           | How will we charge?          |
| **Distribution**      | How will they get it?        |
| **Messaging**         | What will we say?            |
| **Enablement**        | How will teams sell/support? |
| **Measurement**       | How will we track success?   |

## Product Discovery

### Discovery Techniques

| Technique               | Purpose              | When to Use       |
| ----------------------- | -------------------- | ----------------- |
| **Opportunity Mapping** | Identify problems    | Early discovery   |
| **Story Mapping**       | Visualize journeys   | Planning releases |
| **Design Sprints**      | Rapid prototyping    | Big bets          |
| **Fake Door Tests**     | Validate demand      | Before building   |
| **Wizard of Oz**        | Test concepts        | Complex features  |
| **Concierge MVP**       | Manual service first | New markets       |

### Opportunity Assessment

```
OPPORTUNITY CANVAS:

PROBLEM:
What problem are we solving?
Who has this problem?
How do they solve it today?

EVIDENCE:
What data supports this?
Customer quotes/feedback?
Market research?

SOLUTION:
What are we proposing?
Why will it work?
What's the MVP?

ASSUMPTIONS:
What must be true?
What risks exist?
How will we validate?

OUTCOME:
Success metrics?
Business impact?
Customer impact?
```

## Deliverable Templates

### PRD Structure (One-Pager)

```
1. EXECUTIVE SUMMARY (3-4 sentences)
- What: One-line description
- Why: Core problem being solved
- Who: Target users
- Success: How we'll measure it

2. BACKGROUND & CONTEXT
- Current situation and pain points
- Supporting data
- Strategic alignment

3. GOALS & SUCCESS METRICS
- Primary goal and success metric
- Secondary goals and metrics
- Guardrail metrics

4. USER STORIES
Format: "As a [persona], I want to [action], so that [benefit]"
- Acceptance criteria
- Priority (Must/Should/Could Have)

5. SOLUTION OVERVIEW
- High-level description
- Key user flows
- Out of scope

6. DESIGN & TECHNICAL CONSIDERATIONS
- Mockups/wireframes
- Dependencies
- Scalability

7. LAUNCH PLAN
- Rollout strategy
- Success criteria
- Risk mitigation

8. OPEN QUESTIONS
- Unresolved decisions
- Areas needing research
```

## Additional Resources

For comprehensive product management frameworks and methodologies:

- [Product Strategy Expert](./references/product-strategy-expert.md) - Complete PM reference guide
- [Customer Research Methods](./references/customer-research-methods.md) - Interview frameworks, personas, usability testing
- [Analytics and Experimentation](./references/analytics-and-experimentation.md) - Retention analysis, A/B testing, event tracking

## See Also

- [Data Science](../data-science/SKILL.md) - Analytics and ML
- [Marketing](../marketing/SKILL.md) - Go-to-market strategy
- [Business Strategy](../business-strategy/SKILL.md) - Strategic planning
