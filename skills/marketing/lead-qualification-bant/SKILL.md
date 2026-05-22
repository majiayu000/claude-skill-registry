---
name: lead-qualification-bant
description: Qualify leads using the BANT framework (Budget, Authority, Need, Timeline) with discovery questions and scoring criteria
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Lead Qualification: BANT

> Systematically qualify leads using the BANT framework to identify sales-ready opportunities and prioritize follow-up efforts.

## When to Use This Skill

- Discovery calls with inbound leads
- Qualifying outbound responses
- Training SDRs on qualification
- Building qualification scorecards
- Improving lead handoff quality

## Methodology Foundation

Based on the **IBM BANT Framework** (Budget, Authority, Need, Timeline), modernized with:
- Consultative discovery approach
- Scoring-based qualification
- Flexible question sequencing
- Modern buying committee awareness

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures BANT questions | Qualification threshold |
| Scores responses | Handoff criteria |
| Identifies gaps | Follow-up approach |
| Suggests next steps | Exception handling |
| Creates call guides | Disqualification rules |

## Instructions

### Step 1: Understand BANT Components

| Component | Question | Why It Matters |
|-----------|----------|----------------|
| **Budget** | Can they afford it? | No budget = no deal |
| **Authority** | Can they decide? | Need decision maker |
| **Need** | Do they need it? | Problem = urgency |
| **Timeline** | When will they decide? | Forecasting |

### Step 2: Design Discovery Questions

**Budget Questions:**
- Direct: "What budget have you allocated for this?"
- Indirect: "How are initiatives like this typically funded?"
- Value-based: "If we could solve [problem], what would that be worth?"

**Authority Questions:**
- "Who else needs to be involved in this decision?"
- "Walk me through how decisions like this are typically made."
- "Who signs off on purchases in this range?"

**Need Questions:**
- "What prompted you to look into this now?"
- "What happens if you don't solve this?"
- "How is this problem affecting [metrics/team/goals]?"

**Timeline Questions:**
- "When are you hoping to have a solution in place?"
- "What's driving that timeline?"
- "What needs to happen before a decision can be made?"

### Step 3: Score Each Component

| Score | Criteria |
|-------|----------|
| 3 | Strong - Clear, confirmed |
| 2 | Moderate - Indicated but not confirmed |
| 1 | Weak - Vague or unclear |
| 0 | None - Not present or disqualifying |

**Qualification Threshold:**
- 10-12: Sales-ready (SQL)
- 7-9: Needs development (MQL)
- <7: Not qualified (Nurture/Disqualify)

## Examples

### Example 1: Discovery Call Guide

**Output:**
```
## BANT Discovery Call Guide

### Call Structure (30 minutes)

| Phase | Time | Focus |
|-------|------|-------|
| Opener | 3 min | Rapport, agenda |
| Context | 5 min | Situation questions |
| Need | 8 min | Problem discovery |
| Authority | 5 min | Decision process |
| Budget | 4 min | Investment capacity |
| Timeline | 3 min | Decision timing |
| Wrap-up | 2 min | Next steps |

---

### Opening Script

"Thanks for taking the time, [Name]. Before we dive in, I'd love to understand what's happening on your end so I can make this as useful as possible for you.

I'll ask some questions to understand your situation, and you can ask me anything about [Company/Product]. Sound good?

What prompted you to take this call today?"

---

### Need Discovery

**Situation Questions:**
- "Tell me about your current [process/tool/approach]."
- "How long have you been doing it this way?"
- "How many people/deals/projects does this affect?"

**Problem Questions:**
- "What's the biggest challenge you're facing with [area]?"
- "How is that impacting [team/revenue/efficiency]?"
- "What have you tried to solve this?"

**Implication Questions:**
- "What happens if this doesn't get solved this year?"
- "How does this affect your ability to [hit goals]?"
- "What's the cost of the status quo?"

**Scoring Need:**
| Signal | Score |
|--------|-------|
| Clear, urgent problem with measurable impact | 3 |
| Problem acknowledged, some urgency | 2 |
| Problem exists but low priority | 1 |
| No clear problem or "just looking" | 0 |

---

### Authority Discovery

**Questions:**
- "Who else would need to be involved in evaluating a solution like this?"
- "Walk me through how you've made similar decisions in the past."
- "If you decided to move forward, what would the approval process look like?"
- "Is there anyone who could block or slow down this decision?"

**Follow-up mapping:**
- "Besides yourself, who would use this day-to-day?"
- "Who would need to sign off on the budget?"
- "Is there a procurement or legal review process?"

**Scoring Authority:**
| Signal | Score |
|--------|-------|
| Economic buyer, can sign contract | 3 |
| Key influencer, direct access to buyer | 2 |
| User/evaluator, no budget control | 1 |
| No influence, wrong contact | 0 |

---

### Budget Discovery

**Soft Questions (Start Here):**
- "How are initiatives like this typically funded—is it department budget, or does it come from elsewhere?"
- "Have you set aside budget for solving [problem] this year?"
- "When you've purchased [similar solutions] before, how did the funding work?"

**Direct Questions (If Appropriate):**
- "What budget range are you working with?"
- "Our solutions typically range from $X to $Y—does that align with your expectations?"
- "Is budget already approved, or is that part of the process?"

**Value-Based (If Hesitant):**
- "If we could save you [X hours/dollars/etc], what would that be worth to the business?"
- "What's the cost of not solving this problem?"

**Scoring Budget:**
| Signal | Score |
|--------|-------|
| Budget allocated, confirmed range | 3 |
| Budget not set but path to funding clear | 2 |
| "We'd need to find budget" | 1 |
| No budget, no path to funding | 0 |

---

### Timeline Discovery

**Questions:**
- "When are you hoping to have a solution in place?"
- "What's driving that timeline?"
- "Is there an event or deadline that's creating urgency?"
- "What needs to happen between now and a decision?"

**Red Flags:**
- "No rush" / "Just exploring"
- "Maybe next year"
- "We'll see how this goes"

**Green Flags:**
- Specific date or quarter
- External event driving urgency
- Already evaluated competitors

**Scoring Timeline:**
| Signal | Score |
|--------|-------|
| Decision within 30 days, specific date | 3 |
| Decision within 90 days, general timeline | 2 |
| "This quarter" or "this year" | 1 |
| "No timeline" or "just exploring" | 0 |

---

### Wrap-Up & Next Steps

**If Qualified (Score 10+):**
"Based on what you've shared, I think there's a strong fit here. Here's what I'd suggest as next steps:
1. [Schedule demo with AE]
2. [Send relevant case study]
3. [Intro to additional stakeholders]

Does that work for you?"

**If Needs Development (Score 7-9):**
"I appreciate your time today. It sounds like [summarize situation].

Before we move forward, it might make sense to [address gap]. Would it help if I [offer value]?

Let's reconnect in [timeframe] to see where things stand."

**If Not Qualified (Score <7):**
"Thanks for the conversation. Based on what you've shared, it sounds like [timing/budget/need] might not be right for a deeper evaluation right now.

I'm going to add you to our newsletter so you stay in the loop, and I'll check back in [timeframe].

Sound good?"
```

### Example 2: Lead Scoring

**Input:**
```
Score this discovery call:

Lead: Sarah, VP of Sales at TechCorp (200 employees, B2B SaaS)

Call notes:
- They're struggling with sales forecasting accuracy
- Current process: spreadsheets, very manual
- Problem: missed quarters twice last year
- Sarah said "This is one of my top 3 priorities"
- Budget: "We have money set aside, around $30-40K"
- Decision: Sarah + CEO would need to approve
- Timeline: Want something in place by end of Q1
- Also evaluating one competitor
```

**Output:**
```
## BANT Qualification Score: Sarah @ TechCorp

### Overall Score: 11/12 ⭐ SALES QUALIFIED

---

### Component Breakdown

#### Need: 3/3 ✅
**Evidence:**
- Specific problem: forecasting accuracy
- Measurable impact: missed quarters twice
- Priority confirmed: "top 3 priorities"
- Current solution: manual spreadsheets (pain point)

**Assessment:** Clear, urgent, quantifiable need.

---

#### Authority: 3/3 ✅
**Evidence:**
- VP of Sales = key decision maker
- Identified CEO as co-decider
- No mention of procurement blockers

**Assessment:** Strong authority. Champion and economic buyer access.

---

#### Budget: 3/3 ✅
**Evidence:**
- Budget explicitly set aside
- Range provided: $30-40K
- Indicates planning and approval

**Assessment:** Confirmed budget, specific range, ready to purchase.

---

#### Timeline: 2/3 ⚠️
**Evidence:**
- "End of Q1" = specific deadline
- Evaluating competitor = active process
- But: Q1 could be 3-4 months out

**Assessment:** Good timeline but not immediate. Slight risk of delay.

---

### Qualification Summary

| Component | Score | Status |
|-----------|-------|--------|
| Need | 3/3 | ✅ Strong |
| Authority | 3/3 | ✅ Strong |
| Budget | 3/3 | ✅ Strong |
| Timeline | 2/3 | ⚠️ Good |
| **Total** | **11/12** | **SQL** |

---

### Recommendation

**Status: Sales Qualified Lead (SQL)**

**Handoff Notes for AE:**
- Strong pain point: forecasting failures costing them quarters
- Budget confirmed at $30-40K
- Key stakeholders: Sarah (VP Sales) + CEO
- Timeline: EOQ1 (track for potential slip)
- Competition: 1 competitor being evaluated

**Suggested Next Steps:**
1. Immediately warm handoff to AE
2. Schedule demo within 48 hours
3. Send forecasting case study
4. Identify CEO meeting opportunity

**Risk to Monitor:**
- Timeline could slip if Q1 pressure eases
- Competitor evaluation ongoing—need to differentiate

---

### Handoff Email Template

```
Subject: SQL Handoff: TechCorp - Sarah (VP Sales)

Hi [AE],

Qualified lead ready for you:

**Account:** TechCorp (200 employees, B2B SaaS)
**Contact:** Sarah, VP of Sales
**BANT Score:** 11/12

**Key Points:**
- Problem: Missed 2 quarters due to bad forecasting
- Current: Manual spreadsheets
- Budget: $30-40K set aside
- Timeline: End of Q1
- Decision: Sarah + CEO
- Competition: Evaluating 1 competitor

**Why They'll Buy:**
This is a "top 3 priority" per Sarah. They have budget, authority, and urgency. Main risk is timeline slip.

**Suggested Approach:**
Lead with forecasting accuracy story. Ask to meet CEO early.

[Your calendar link for warm intro call]

— [SDR Name]
```
```

## Skill Boundaries

### What This Skill Does Well
- Structuring qualification calls
- Scoring leads objectively
- Identifying qualification gaps
- Creating handoff documentation

### What This Skill Cannot Do
- Replace conversation skills
- Know your specific thresholds
- Handle objections in real-time
- Guarantee lead quality

## References

- IBM BANT Original Framework
- TOPO SDR Qualification Guide
- Gartner B2B Buying Research
- SalesHacker Discovery Call Guide

## Related Skills

- `lead-qualification-meddic` - Enterprise qualification
- `icp-matching` - Pre-call fit assessment
- `outbound-sequencer` - Pre-qualification outreach

## Skill Metadata

- **Domain**: SDR Automation
- **Complexity**: Beginner-Intermediate
- **Mode**: cyborg
- **Time to Value**: 30 min per call
- **Prerequisites**: Basic discovery skills
