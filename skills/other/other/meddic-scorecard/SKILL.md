---
name: meddic-scorecard
description: Create and maintain MEDDIC/MEDDPICC deal scorecards for pipeline hygiene, forecast accuracy, and deal coaching
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# MEDDIC Scorecard

> Build systematic deal scorecards using MEDDIC/MEDDPICC methodology to improve pipeline hygiene, forecast accuracy, and coaching effectiveness.

## When to Use This Skill

- Weekly pipeline reviews
- Deal coaching sessions
- Forecast call preparation
- Win/loss analysis
- Sales enablement training

## Methodology Foundation

Based on **PTC's MEDDIC** (Dick Dunkel) extended to **MEDDPICC**, creating standardized scorecards for:
- Deal qualification scoring
- Gap identification
- Coaching prioritization
- Forecast confidence

## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Creates scorecard templates | Deal stage thresholds |
| Suggests scoring criteria | Coaching priorities |
| Identifies deal gaps | Forecast commits |
| Generates coaching questions | Resource allocation |
| Tracks deal progression | Win strategy |

## Instructions

### Step 1: Define Scoring Criteria

**MEDDPICC Components:**

| Component | Definition | Scoring Weight |
|-----------|------------|----------------|
| **M**etrics | Quantified business outcomes | 15% |
| **E**conomic Buyer | Budget authority identified | 15% |
| **D**ecision Criteria | How they'll evaluate | 10% |
| **D**ecision Process | Steps to purchase | 10% |
| **P**aper Process | Legal/procurement | 10% |
| **I**dentify Pain | Business problem articulated | 15% |
| **C**hampion | Internal advocate confirmed | 15% |
| **C**ompetition | Competitive landscape known | 10% |

### Step 2: Create Scoring Rubric

**Per-Component Scoring (0-3):**

| Score | Definition | Evidence Required |
|-------|------------|-------------------|
| 0 | Unknown | No information gathered |
| 1 | Identified | Basic information, not verified |
| 2 | Validated | Confirmed with prospect |
| 3 | Leveraged | Actively using in deal strategy |

### Step 3: Build Stage Gates

**Stage-Score Alignment:**

| Stage | Minimum Score | Required 3s |
|-------|---------------|-------------|
| Discovery | 8/24 | Pain |
| Qualification | 12/24 | Pain, Champion |
| Demo/Evaluation | 16/24 | Pain, Champion, Criteria |
| Proposal | 18/24 | + Economic Buyer |
| Negotiation | 21/24 | + Paper Process |
| Commit | 22/24 | All components validated |

### Step 4: Track and Coach

**Weekly Review Focus:**
- Deals below stage threshold
- Score changes (positive/negative)
- Gaps in critical components
- Champion health check
- Competition updates

### Step 5: Analyze Patterns

**Pipeline Health Metrics:**
- Average score by stage
- Conversion rates by score threshold
- Most common gaps
- Champion strength correlation

## Examples

### Example 1: Complete Deal Scorecard

**Input:**
```
Create a MEDDPICC scorecard for:
- Deal: Enterprise software sale, $400K
- Stage: Proposal
- Champion: VP of Operations
- EB: CFO (not met)
- Timeline: Q1 close
```

**Output:**
```
## MEDDPICC Deal Scorecard

### Deal Overview

| Field | Value |
|-------|-------|
| Account | [Customer Name] |
| Opportunity | Enterprise Platform |
| Value | $400,000 ARR |
| Stage | Proposal |
| Close Date | Q1 (March 30) |
| AE | [Name] |
| Last Updated | [Date] |

---

### Score Summary

**Total Score: 16/24** | Stage Requirement: 18/24

| Component | Score | Stage Req | Status |
|-----------|-------|-----------|--------|
| Metrics | 2/3 | 2 | ✅ |
| Economic Buyer | 1/3 | **3** | ❌ GAP |
| Decision Criteria | 3/3 | 2 | ✅ |
| Decision Process | 2/3 | 2 | ✅ |
| Paper Process | 1/3 | 2 | ⚠️ GAP |
| Identify Pain | 3/3 | 3 | ✅ |
| Champion | 3/3 | 3 | ✅ |
| Competition | 1/3 | 2 | ⚠️ GAP |

**Status: NOT READY FOR PROPOSAL** - 3 gaps to address

---

### Component Details

#### Metrics (2/3) ✅ On Track

**Current State:**
- ROI target: 3x in Year 1 ✓
- Primary KPI: Reduce processing time 40% ✓
- CFO business case: Not yet presented ✗

**Evidence:**
> "If we hit 40% reduction, that's $1.2M in operational savings"
> — VP Operations, Discovery Call

**To reach 3/3:**
- [ ] Present business case to CFO
- [ ] Get CFO to validate assumptions

---

#### Economic Buyer (1/3) ❌ CRITICAL GAP

**Current State:**
- EB Identified: CFO Jennifer Walsh ✓
- Access: Email only, no meeting ✗
- Engagement: Unknown priorities ✗

**Gap Analysis:**
We have not met the Economic Buyer. This is a **deal blocker**
for Proposal stage. Champion (VP Ops) reports to CFO but has
not secured meeting.

**Action Required:**
- [ ] Ask Champion for CFO meeting this week
- [ ] Prepare executive briefing deck
- [ ] Identify CFO's priorities for Q1

**Coaching Questions:**
1. "What's preventing us from meeting the CFO?"
2. "What does your champion say about CFO's priorities?"
3. "Can we propose a joint call with champion + CFO?"

---

#### Decision Criteria (3/3) ✅ Strong

**Current State:**
- Formal criteria documented ✓
- Weighted by priority ✓
- Aligned with our strengths ✓

**Evidence:**
| Criterion | Weight | Our Fit |
|-----------|--------|---------|
| Integration depth | 30% | Strong |
| Time to value | 25% | Strong |
| Total cost | 20% | Medium |
| Support | 15% | Strong |
| References | 10% | Strong |

---

#### Decision Process (2/3) ⚠️ Needs Validation

**Current State:**
- Steps identified ✓
- Timeline mapped ✓
- Approvers known ✓
- Specific dates: Partial ✗

**Process Map:**
```
Step 1: Technical evaluation ✅ Complete
Step 2: Business review ✅ Complete
Step 3: Proposal review ⏳ This week
Step 4: CFO approval ⏳ [Date TBD]
Step 5: Legal/Procurement ⏳ [Timeline unknown]
Step 6: Signature ⏳ Target: March 30
```

**To reach 3/3:**
- [ ] Confirm CFO meeting date
- [ ] Map procurement timeline
- [ ] Identify potential delays

---

#### Paper Process (1/3) ⚠️ GAP

**Current State:**
- Legal review required: Likely ✓
- Timeline: Unknown ✗
- Procurement contact: Not identified ✗
- Standard terms acceptable: Unknown ✗

**Risk Assessment:**
Paper process is a common source of deal slip at this stage.
Unknown timeline creates forecast risk.

**Action Required:**
- [ ] Ask champion about procurement process
- [ ] Identify legal/procurement contacts
- [ ] Offer to start MSA review early

---

#### Identify Pain (3/3) ✅ Strong

**Current State:**
- Pain articulated ✓
- Quantified impact ✓
- Urgency established ✓
- Consequences of inaction clear ✓

**Pain Statement:**
> "Manual processing is costing us 8,000 hours/year. We've
> missed SLAs 3 times this quarter. If we don't fix this,
> we'll lose the [Major Customer] contract."

**Business Impact:**
- 8,000 hours × $50/hr = $400K labor cost
- SLA penalties: $200K potential
- Customer retention risk: $2M contract

---

#### Champion (3/3) ✅ Strong

**Champion Profile:**
| Attribute | Assessment |
|-----------|------------|
| Name | Michael Chen, VP Operations |
| Access | Reports to CFO |
| Influence | High - owns the budget |
| Motivation | Personal - promoted if successful |
| Engagement | Weekly calls, sharing internally |

**Champion Test:**
- ✅ Sells when we're not in the room
- ✅ Shares competitive intel
- ✅ Gives us bad news
- ⚠️ Has not secured CFO meeting yet

---

#### Competition (1/3) ⚠️ GAP

**Current State:**
- Competitors identified: 1 known ✓
- Their status: Unknown ✗
- Their approach: Unknown ✗
- Our differentiation: Assumed ✗

**Known Information:**
- Competitor X was evaluated
- Champion said "we've narrowed to two"
- No pricing or proposal intel

**Action Required:**
- [ ] Ask champion directly about competitor status
- [ ] Understand competitor's proposal/pricing
- [ ] Prepare competitive positioning

---

### Gap Resolution Plan

| Gap | Priority | Action | Owner | Due |
|-----|----------|--------|-------|-----|
| Economic Buyer | P1 | Request CFO meeting | AE + Champion | This week |
| Competition | P2 | Discovery with champion | AE | Day 2 |
| Paper Process | P2 | Map procurement timeline | AE | Day 3 |

---

### Coaching Summary

**Primary Focus:** Get in front of CFO before sending proposal

**Key Questions to Ask in 1:1:**
1. Why haven't we met the Economic Buyer yet?
2. What do we actually know about the competition?
3. What could cause this deal to slip past Q1?

**Forecast Recommendation:**
- Current: In forecast at 50%
- Recommendation: Keep at 50% until CFO meeting secured
- Path to 80%: EB meeting + Competition clarity + Paper process mapped
```

### Example 2: Pipeline Review Summary

**Input:**
```
Summarize MEDDPICC health for these 5 deals:
1. Deal A: 22/24 (Commit stage)
2. Deal B: 14/24 (Proposal stage)
3. Deal C: 18/24 (Demo stage)
4. Deal D: 10/24 (Qualification stage)
5. Deal E: 16/24 (Negotiation stage)
```

**Output:**
```
## Pipeline MEDDPICC Health Summary

### Overview

| Deal | Stage | Score | Req'd | Status |
|------|-------|-------|-------|--------|
| Deal A | Commit | 22/24 | 22 | ✅ On track |
| Deal B | Proposal | 14/24 | 18 | ❌ 4 pts below |
| Deal C | Demo | 18/24 | 16 | ✅ Above req |
| Deal D | Qualification | 10/24 | 12 | ❌ 2 pts below |
| Deal E | Negotiation | 16/24 | 21 | ❌ 5 pts below |

**Pipeline Health: 2/5 deals on track (40%)**

---

### Priority Attention

| Priority | Deal | Issue | Recommended Action |
|----------|------|-------|-------------------|
| P1 | Deal E | 5 pts below in Negotiation | Pull back to Proposal |
| P2 | Deal B | 4 pts below in Proposal | Hold proposal, fill gaps |
| P3 | Deal D | 2 pts below in Qualification | Accelerate discovery |

---

### Deal E (CRITICAL)

**Problem:** In Negotiation stage with 16/24 score (req: 21)

This deal is at high risk. Likely gaps in:
- Economic Buyer (not confirmed?)
- Paper Process (not mapped?)
- Competition (unknown?)

**Recommendation:** Do not forecast this deal. Move back to
Proposal stage and address gaps before continuing negotiation.

---

### Common Gaps Across Pipeline

| Component | Avg Score | Concern |
|-----------|-----------|---------|
| Paper Process | 1.2/3 | Most common gap |
| Competition | 1.4/3 | Frequent blind spot |
| Economic Buyer | 1.8/3 | Access issue |

**Coaching Focus:** Paper Process discovery earlier in cycle
```

## Skill Boundaries

### What This Skill Does Well
- Creating structured scorecards
- Identifying deal gaps
- Generating coaching questions
- Tracking deal progression

### What This Skill Cannot Do
- Access your CRM data
- Know specific deal context
- Make forecast decisions
- Replace sales judgment

## Iteration Guide

**Follow-up Prompts:**
- "Create coaching questions for [component]"
- "What should we ask about [specific gap]?"
- "Design stage gate criteria for our process"
- "Analyze win/loss patterns from scorecards"

## References

- PTC MEDDIC Methodology (Dick Dunkel)
- Force Management MEDDICC
- Winning by Design Sales Process
- Gong Sales Coaching Research

## Related Skills

- `lead-qualification-meddic` - Full qualification framework
- `deal-risk-scoring` - Risk assessment
- `pipeline-forecasting` - Forecast methodology

## Skill Metadata

- **Domain**: Sales
- **Complexity**: Intermediate
- **Mode**: centaur
- **Time to Value**: 15-30 min per deal
- **Prerequisites**: Deal information, CRM access
