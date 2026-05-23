---
name: proposal-writer
description: Templates and frameworks for creating winning sales proposals. Executive summaries, scope of work, pricing strategies, and closing elements.
allowed-tools: Read, Write, Edit, WebSearch
---

# Proposal Writer

Create proposals that close deals. Connect discovery insights to clear solutions, present pricing strategically, and make it easy for buyers to say yes.

## Input Context

Expect structured context from orchestrator:

```yaml
prospect:
  company: string
  industry: string
  size: string
deal_size: <$10K | $10-50K | $50K+
stakeholders:
  - title: string
    concern: string
pain_points: [list from discovery]
solution: string
pricing: number | range
competition:
  - name: string
    weakness: string
objections: [list to address]
timeline:
  decision_date: date
  implementation_date: date
```

## Proposal Length by Deal Size

| Deal Size | Pages | Sections |
|-----------|-------|----------|
| <$10K | 3-5 | Exec summary, Scope, Pricing, Next steps |
| $10K-$50K | 5-10 | + Understanding, Case study, Team |
| $50K-$250K | 10-15 | + Detailed timeline, Multiple options, Risk mitigation |
| >$250K | 15-25 | + Implementation methodology, Comprehensive terms, Appendix |

## Proposal Structure

### Cover Page

```markdown
# PROPOSAL

**[Your Company] → [Prospect Company]**

**Prepared for:** [Name, Title]
**Prepared by:** [Name, Title]
**Date:** [Date]
**Valid until:** [Date + 30 days]
```

### Executive Summary (Most Critical Section)

Decision-makers often read only this. Must stand alone.

```markdown
## Executive Summary

### The Challenge

Based on our conversations, [Company] is facing:

- **[Pain Point 1]**: [Quantified impact - "$X/month in lost revenue"]
- **[Pain Point 2]**: [Quantified impact - "X hours/week wasted"]
- **[Pain Point 3]**: [Quantified impact - "X% customer churn"]

### Our Solution

[Product/Service] will help [Company] achieve:

- **[Outcome 1]**: [Measurable result with number]
- **[Outcome 2]**: [Measurable result with timeframe]
- **[Outcome 3]**: [Measurable result with percentage]

### Investment & Timeline

| Component | Investment | Duration |
|-----------|------------|----------|
| [Phase/Item 1] | $X | X weeks |
| [Phase/Item 2] | $X | X weeks |
| **Total** | **$X** | **X weeks** |

### Why [Your Company]

[2-3 sentences on specific differentiators relevant to their situation]

### Next Steps

| Action | Owner | By Date |
|--------|-------|---------|
| Proposal review call | [Prospect] | [Date] |
| Contract review | [Prospect legal] | [Date] |
| Kickoff | Both teams | [Date] |
```

### Understanding & Approach

```markdown
## Understanding & Approach

### Current Situation

[Reference specific discovery conversation points]

### Desired Future State

| Metric | Current | Target | Impact |
|--------|---------|--------|--------|
| [Metric 1] | [Current] | [Goal] | [Business impact] |
| [Metric 2] | [Current] | [Goal] | [Business impact] |

### Our Approach

**Phase 1: [Name]**
[Description and deliverables]

**Phase 2: [Name]**
[Description and deliverables]

**Phase 3: [Name]**
[Description and deliverables]
```

### Scope of Work

```markdown
## Scope of Work

### Included

| Deliverable | Description | Acceptance Criteria |
|-------------|-------------|---------------------|
| [Deliverable 1] | [What it is] | [How we know it's done] |
| [Deliverable 2] | [What it is] | [How we know it's done] |

### Not Included

- [Item 1] — available as add-on
- [Item 2] — future phase
- [Item 3] — client responsibility

### Assumptions

- [Assumption 1]
- [Assumption 2]

### Client Responsibilities

- [Responsibility 1]
- [Responsibility 2]
```

### Timeline & Milestones

```markdown
## Timeline & Milestones

| Week | Milestone | Deliverable | Dependencies |
|------|-----------|-------------|--------------|
| 1 | Kickoff | Project plan | Contract signed |
| 2-3 | [Phase 1] | [Deliverable] | [Dependency] |
| 4-6 | [Phase 2] | [Deliverable] | [Dependency] |
| 7-8 | Go-Live | [Final deliverable] | [Dependency] |
```

### Investment & Pricing

**Strategy:** Present 2-3 options with recommended highlighted. Anchor high.

```markdown
## Investment Options

### Option A: Comprehensive
[Full solution with premium features]
- [Feature 1]
- [Feature 2]
- [Bonus: Feature 3]

**Investment: $XX,XXX**

### Option B: Recommended ⭐
[Core solution, best value for most situations]
- [Feature 1]
- [Feature 2]

**Investment: $XX,XXX**

### Option C: Essentials
[Minimum viable solution]
- [Feature 1]

**Investment: $XX,XXX**

---

**Payment Terms:** [50% upfront, 50% on completion | Monthly | etc.]
```

### ROI Justification

Use when price is a concern:

```markdown
## Return on Investment

**Current Cost of Problem:**
| Issue | Monthly Cost | Annual Cost |
|-------|--------------|-------------|
| [Problem 1] | $X | $X |
| [Problem 2] | $X | $X |
| **Total cost of inaction** | **$X** | **$X** |

**With [Solution]:**
| Improvement | Monthly Savings | Annual Savings |
|-------------|-----------------|----------------|
| [Outcome 1] | $X | $X |
| [Outcome 2] | $X | $X |
| **Total savings** | **$X** | **$X** |

**Payback Period:** X months
**First-Year ROI:** X.Xx
```

### Social Proof

```markdown
## Why [Your Company]

### Relevant Experience

| Client | Challenge | Result |
|--------|-----------|--------|
| [Similar company] | [Similar problem] | [Quantified outcome] |
| [Similar company] | [Similar problem] | [Quantified outcome] |

### Client Testimonial

> "[Quote about working with you and results achieved]"
> — [Name, Title, Company]

### By the Numbers

- X years in [industry]
- X clients served
- X% client satisfaction
- $Xm in [results delivered]
```

### Team & Support

```markdown
## Your Team

| Role | Name | Responsibility |
|------|------|----------------|
| Project Lead | [Name] | Overall delivery, your primary contact |
| [Specialist] | [Name] | [Specific responsibility] |
| [Support] | [Name] | [Ongoing support] |

### Support Model

**During Implementation:**
- [Support type and availability]

**Post-Implementation:**
- [Ongoing support included]
```

### Terms & Next Steps

```markdown
## Next Steps

| Step | Action | Owner | Target Date |
|------|--------|-------|-------------|
| 1 | Proposal review call | [Prospect] | [Date] |
| 2 | Final questions addressed | [You] | [Date] |
| 3 | Contract review | [Prospect legal] | [Date] |
| 4 | Signed agreement | Both | [Date] |
| 5 | Kickoff meeting | Both | [Date] |

### Terms Summary

- **Proposal valid until:** [Date]
- **Payment terms:** [Terms]
- **Contract length:** [Duration]
- **Cancellation:** [Policy]

---

**To proceed:** [Clear instruction — sign and return, schedule call, etc.]

**Questions?** Contact [Name] at [email/phone]
```

## One-Pager Template (Quick Deals)

For deals <$5K or early-stage exploration:

```markdown
# [Your Company] + [Prospect Company]

## The Problem
- [Pain point 1 - quantified]
- [Pain point 2 - quantified]

## Our Solution
- [Outcome 1 - measurable]
- [Outcome 2 - measurable]

## Investment
$[Amount] for [scope] delivered in [timeframe]

## Next Step
[Single clear action with date]

---
Valid until [Date] | [Your contact info]
```

## Tone Guidelines

- **Confident, not arrogant**: "We will deliver" not "We're the best"
- **Consultative**: Trusted advisor solving their problem
- **Specific**: Reference their words, their situation
- **Action-oriented**: Every section moves toward next step
- **Clean**: White space, scannable, professional

## Anti-Patterns

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Lead with company history | They don't care yet | Lead with their pain |
| Generic scope | Feels like template | Reference specific discovery |
| Bury pricing | Seems evasive | Put in exec summary |
| Feature lists | Doesn't resonate | Focus on outcomes |
| No next steps | Deal stalls | Action table with dates |
| Wall of text | Won't be read | Headers, tables, bullets |
