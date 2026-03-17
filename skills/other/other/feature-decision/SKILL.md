---
name: feature-decision
description: Framework for making feature prioritization decisions
role_groups: [product, leadership]
jtbd: |
  Prioritization decisions get made in meetings and forgotten, or worse - made 
  without proper framework. This guides you through key questions (impact, effort, 
  strategic fit), checks recent customer intel, and documents the decision with 
  rationale so you can reference it later.
time_investment: "15-20 minutes per decision"
---

## Purpose

Make and document feature prioritization decisions with a structured framework. Ensures key factors are considered, stakeholders are consulted, and rationale is preserved for future reference.

## Usage

- `/feature-decision [feature-name]` - Make a decision on a specific feature
- `/feature-decision` - Start decision process with guided questions

---

## Step 1: Define the Feature

Ask the user to clarify:

1. **Feature name:** What are we deciding on?
2. **Feature description:** What does it do? (1-2 sentences)
3. **Origin:** Where did this request come from?
   - Customer request (which customers?)
   - Internal idea (who proposed?)
   - Competitive response
   - Strategic initiative

---

## Step 2: Gather Context

Before asking decision questions, gather relevant intel:

### Customer Intel
- Search for mentions of this feature or related pain points
- Check `/customer-intel` output if recently run
- Look for customer quotes supporting or contradicting this feature

### Roadmap Context
- Check 04-Projects/ for related work
- Verify available capacity
- Identify potential conflicts or dependencies

### Strategic Alignment
- Read System/pillars.yaml
- Read 01-Quarter_Goals/Quarter_Goals.md (if exists)
- Check how this feature maps to strategic priorities

---

## Step 3: Decision Framework Questions

Guide the user through these questions:

### Impact Questions

1. **Customer Impact**
   - Who benefits from this? (Which customers/segments?)
   - How many users does this affect?
   - What problem does it solve for them?
   - Scale: High / Medium / Low

2. **Business Impact**
   - How does this affect revenue? (Enable new sales? Reduce churn? Upsell opportunity?)
   - Does this unblock deals?
   - Competitive positioning impact?
   - Scale: High / Medium / Low

3. **Strategic Fit**
   - Which pillar does this advance?
   - Does it support a quarterly goal?
   - Long-term value vs short-term win?
   - Scale: High / Medium / Low

### Effort Questions

4. **Engineering Effort**
   - Size estimate? (Small: <1 week, Medium: 1-4 weeks, Large: 1-3 months, XL: 3+ months)
   - Technical complexity? (Low / Medium / High)
   - Dependencies on other systems?
   - Risk level? (Low / Medium / High)

5. **Design Effort**
   - New patterns needed or existing components?
   - User research required?
   - Estimated design time?

6. **GTM/Support Effort**
   - Training needed?
   - Documentation scope?
   - Support impact?

### Trade-offs

7. **What are we NOT building if we build this?**
   - What gets deprioritized?
   - Opportunity cost?

8. **What's the downside of saying no?**
   - Lost customers?
   - Competitive risk?
   - Team morale?

---

## Step 4: Consult Stakeholders

Identify who needs to weigh in:

- **Must consult:** [Based on feature type]
  - Engineering (feasibility)
  - Design (user experience)
  - Sales/CS (customer impact)
  - Leadership (strategic fit)

- **Optional consult:** [Nice to have input]

Prompt user: "Have you consulted [stakeholders]? Want me to help prep for those conversations?"

---

## Step 5: Make the Decision

Based on the framework, present a recommendation:

### Impact/Effort Matrix

```
       HIGH IMPACT
            |
    Do Next | Do Now
------------|------------
    Later   | Quick Wins
            |
       LOW IMPACT
```

**Recommendation:** [Do Now / Do Next / Quick Wins / Later / No]

**Rationale:**
- [Key factor 1]
- [Key factor 2]
- [Key factor 3]

Ask user: "Does this recommendation make sense? Want to adjust the decision?"

---

## Step 6: Document the Decision

Create a decision document in 04-Projects/:

```markdown
# Feature Decision: [Feature Name]

**Date:** [Today]
**Decision:** [Go / No-Go / Defer]
**Owner:** [User's name from System/user-profile.yaml]

---

## Overview

**Feature:** [Feature description]
**Origin:** [Where it came from]
**Requested by:** [Customers/stakeholders]

---

## Decision Framework

### Impact Assessment

**Customer Impact:** [High/Medium/Low]
- Who benefits: [Segment/customers]
- Problem solved: [Pain point]
- Users affected: [Count/percentage]

**Business Impact:** [High/Medium/Low]
- Revenue effect: [Details]
- Competitive position: [Details]
- Deal impact: [Details]

**Strategic Fit:** [High/Medium/Low]
- Pillar: [Which pillar]
- Quarterly goal: [Which goal if applicable]
- Long-term value: [Assessment]

### Effort Assessment

**Engineering:** [Small/Medium/Large/XL]
- Size: [Time estimate]
- Complexity: [Low/Medium/High]
- Dependencies: [List]
- Risk: [Low/Medium/High]

**Design:** [Details]
**GTM/Support:** [Details]

---

## Decision Rationale

**Why [Go/No-Go/Defer]:**

1. [Primary reason]
2. [Secondary reason]
3. [Tertiary reason]

**Trade-offs accepted:**
- Deprioritizing: [What]
- Risk: [What]

---

## Supporting Evidence

**Customer quotes:**
- "[Quote 1]" - [Customer], [Date]
- "[Quote 2]" - [Customer], [Date]

**Competitive intel:**
- [Details if applicable]

**Related conversations:**
- [Link to meeting notes]
- [Link to person pages]

---

## Stakeholder Alignment

**Consulted:**
- [Name] (Engineering) - [Their input]
- [Name] (Design) - [Their input]
- [Name] (Sales) - [Their input]

**Concerns raised:**
- [Concern 1 and how addressed]

---

## Next Steps

[If Go:]
- [ ] Create project in 04-Projects/
- [ ] Add to roadmap
- [ ] Schedule kickoff
- [ ] Update stakeholders

[If No-Go:]
- [ ] Communicate decision to requesters
- [ ] Update person pages with rationale
- [ ] Add to "not now" backlog with trigger conditions

[If Defer:]
- [ ] Document trigger conditions for revisiting
- [ ] Set calendar reminder for [when]
- [ ] Communicate timeline to stakeholders

---

## Decision Log

This decision is logged for future reference. Run `/decision-log` to see all major product decisions.
```

Save to: `04-Projects/Decision_[Feature-Name]_[Date].md`

---

## Step 7: Follow-Up Actions

Offer to help with next steps:

> "Decision documented! Want me to:
> 1. Create a project file if we're building this?
> 2. Draft stakeholder communication?
> 3. Add to roadmap review?
> 4. Update relevant person pages with this decision?"

---

## Integration with Other Skills

- **Before running:** Suggest `/customer-intel` to gather feedback
- **Before running:** Suggest `/roadmap` to check capacity
- **After No-Go decision:** Update person pages so you remember why you said no
- **After Go decision:** Link to `/project-health` for tracking

---

## Example: Real-time Dashboards Decision

```markdown
# Feature Decision: Real-time Dashboards

**Date:** 2026-01-28
**Decision:** Go - Q1 Priority
**Owner:** Dave (CPO)

---

## Overview

**Feature:** Real-time dashboards that auto-refresh every 5 minutes, eliminating manual report compilation
**Origin:** Customer request (repeated pattern from 4 customers)
**Requested by:** Acme Corp (Sarah), TechStart (Mike), GlobalCo (Lisa), DataFlow

---

## Decision Framework

### Impact Assessment

**Customer Impact:** High
- Who benefits: All customers with reporting workflows (60% of user base)
- Problem solved: Manual report compilation taking 2 days/month per customer
- Users affected: ~500 users across our customer base

**Business Impact:** High
- Revenue effect: Unblocks 2 pending deals (TechStart, NewCorp) - $180K ARR
- Competitive position: ProductX has this, we don't - closing gap
- Deal impact: Sales team reports dashboards are #3 objection in demos

**Strategic Fit:** High
- Pillar: Product Quality
- Quarterly goal: Q1-2 (Reduce customer effort)
- Long-term value: Platform capability, enables future dashboard types

### Effort Assessment

**Engineering:** Medium (3-4 weeks)
- Size: 3-4 weeks
- Complexity: Medium (real-time data pipeline + UI refresh)
- Dependencies: Data infrastructure team (capacity confirmed)
- Risk: Medium (performance at scale needs testing)

**Design:** Small (1 week) - using existing components
**GTM/Support:** Medium - training needed, support documentation

---

## Decision Rationale

**Why Go:**

1. **Strong customer signal** - 4 customers in 30 days, increasing trend, 2 called it blocker
2. **Business impact** - Unblocks $180K in pipeline, closes competitive gap
3. **Strategic alignment** - Directly advances Q1 goal (reduce customer effort)
4. **Feasible scope** - 3-4 weeks, no major blockers, team has capacity

**Trade-offs accepted:**
- Deprioritizing: Mobile app performance improvements slide from Feb to March
- Risk: Need to validate performance at scale during beta

---

## Supporting Evidence

**Customer quotes:**
- "Takes 2 days/month to compile reports manually. Need real-time dashboards." - Sarah (Acme), Jan 24
- "Reporting pain is my team's #1 complaint. They avoid the system because of it." - Lisa (GlobalCo), Jan 15

**Competitive intel:**
- "ProductX's dashboards are way ahead of yours. We're evaluating a switch." - Mike (TechStart), Jan 20

**Related conversations:**
- 00-Inbox/Meetings/2026-01-24_Acme_Quarterly_Review.md
- People/External/Sarah_Chen_Acme.md

---

## Stakeholder Alignment

**Consulted:**
- Mike (Engineering Lead) - Feasible, 3-4 weeks, needs data team sync
- Sarah (Design Lead) - Can use existing components, 1 week effort
- John (Sales VP) - Would unblock 2 deals, closes demo objection

**Concerns raised:**
- Performance at scale (Mike) - Addressed: Beta test with 3 high-volume customers before general launch

---

## Next Steps

- [x] Create project in 04-Projects/Real_Time_Dashboards.md
- [ ] Add to roadmap (Q1 priority)
- [ ] Schedule kickoff for Feb 1
- [ ] Update stakeholders (Acme, TechStart, GlobalCo, NewCorp)
- [ ] Communicate timeline to sales team

---

## Decision Log

This decision is logged for future reference. Run `/decision-log` to see all major product decisions.
```
