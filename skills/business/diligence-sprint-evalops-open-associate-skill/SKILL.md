---
name: diligence-sprint
description: "A time-boxed diligence sprint (3-7 days) with daily deliverables and decision gates. Burns down top 4 risks and produces IC-ready evidence. Use when a deal is live and you need speed without losing rigor."
license: Proprietary
compatibility: Works offline; improved with calls and data access; Salesforce logging recommended.
metadata:
  author: evalops
  version: "0.2"
---
# Diligence sprint

## When to use
Use this compound skill when:
- A deal is live and you have a hard decision deadline
- You need a clear risk burn-down plan and daily deliverables
- You want to coordinate multiple diligence workstreams with gates

## Inputs you should request (only if missing)
- Deadline (term sheet / IC date)
- Intended role (lead/follow) and check size
- Top 3 "must be true" claims from first meeting
- Customer access constraints
- Sprint length: 3-day, 5-day, or 7-day

## Outputs you must produce
- Day-by-day plan with owners and deliverables
- Ranked risk register (MAX 4 risks)
- Evidence pack with anti-confirmation
- Decision at each gate: kill, continue, or escalate
- Memo-ready findings or explicit kill decision

**Every sprint ends with one of two outcomes:**
1. Partner-ready memo + IC scheduled
2. Explicit kill with logged reason + "what would change our mind" + recheck date

## 5-day default sprint plan

### Day 0: Setup (2-4 hours)
**Deliverables:**
- Aligned on top 4 risks + fastest tests
- Owners assigned and calls scheduled
- Salesforce Tasks created for each workstream

**Day 0 Gate:** Can we test the top 4 risks in the time available? If not, scope down or extend timeline.

### Day 1: Customer diligence
**Deliverables:**
- 3 buyer calls completed
- 2 user calls completed
- 1 churned/lost deal call scheduled or completed (REQUIRED)
- Customer summary written

**Day 1 Gate:** Did customers validate or invalidate the core thesis? Any kill signals?

| Risk | Before Day 1 | After Day 1 | Change |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**Decision:** Kill / Continue / Escalate

### Day 2: Product diligence
**Deliverables:**
- Hands-on demo completed
- Deployment reality assessed
- Integration blockers identified
- Time-to-value documented

**Day 2 Gate:** Does the product deliver on the promise? Any kill signals?

| Risk | Before Day 2 | After Day 2 | Change |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**Decision:** Kill / Continue / Escalate

### Day 3: GTM + metrics diligence
**Deliverables:**
- Pipeline review completed
- Unit economics validated by segment
- Cycle time and pricing confirmed
- Competitor/alternative user call completed (REQUIRED)

**Day 3 Gate:** Is this repeatable? Are the economics real? Any kill signals?

| Risk | Before Day 3 | After Day 3 | Change |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**Decision:** Kill / Continue / Escalate

### Day 4: Team + competition
**Deliverables:**
- Team learning rate assessed
- Decision rights clarity confirmed
- Competitive map updated
- "Incumbent build" threat evaluated

**Day 4 Gate:** Is this team credible? Can they win vs competition? Any kill signals?

| Risk | Before Day 4 | After Day 4 | Change |
|---|---|---|---|
| 1 | | | |
| 2 | | | |

**Decision:** Kill / Continue / Escalate

### Day 5: Synthesis + decision
**Deliverables:**
- All evidence synthesized
- Memo sections drafted (market, product, traction, GTM, team, risks)
- Recommendation written (first line, no hedging)
- Steelman "best argument against" written
- IC readout prepared

**Final Gate:** One of two outcomes:
1. **ADVANCE:** Partner-ready memo + IC scheduled
2. **KILL:** Pass logged with reason + "what would change our mind" + recheck date

## 3-day sprint (urgent deal)

### Day 0: Setup + risk alignment (2 hours)
- Align on top 2-3 risks (fewer risks, faster tests)
- Schedule all calls for Days 1-2

**Gate:** Are the tests achievable in 3 days?

### Day 1: Customer + product
- 3-5 customer calls (buyers + users)
- Hands-on product eval
- Churned/lost deal call (REQUIRED)

**Gate at end of Day 1:** Kill or continue? No "need more time."

### Day 2: GTM + team + competition
- Pipeline review
- Team assessment
- Competitor validation

**Gate at end of Day 2:** Kill or continue? All top risks tested?

### Day 3: Synthesis + decision
- Evidence synthesis
- Memo draft
- IC decision

**Final gate:** Memo or kill. No limbo.

## 7-day sprint (deeper diligence)

Same structure as 5-day, with:
- Days 1-2: Customer diligence (more calls, deeper coverage)
- Day 3: Product diligence
- Days 4-5: GTM + metrics + competition
- Day 6: Team + synthesis
- Day 7: Memo + decision

## Decision gates (mandatory checkpoints)

At each gate, you must answer:
1. **Kill?** Is there evidence that this deal should not proceed?
2. **Continue?** Is there enough positive signal to invest more time?
3. **Escalate?** Does a partner need to weigh in before Day X?

**Kill criteria (stop immediately if any are true):**
- Customer calls reveal fundamental misunderstanding of ICP
- Churned customer call reveals systemic product/service issue
- Metrics don't support the stated traction
- Competitive position is weaker than pitched
- Team shows inability to change mind with evidence

**Continue criteria:**
- Evidence supports core thesis
- Risks are testable and manageable
- No kill signals triggered

**Escalate criteria:**
- Risk requires partner relationship/expertise
- Deal dynamics require partner involvement
- Unclear whether to kill or continue

## Anti-confirmation requirements (MANDATORY)

Every sprint must include:
1. **Churned customer or lost deal call** - What caused them to leave/not buy?
2. **Competitor/alternative user** - Why do they use something else?

If these calls are impossible, document why and flag the gap prominently in the memo.

## Guardrails
- If you can't get a failed customer reference, discount retention claims.
- If the deadline compresses: do fewer risks, not more shallow work.
- Never extend a sprint without a partner decision. Time-box or kill.
- Every day must produce a decision-relevant deliverable.

## Salesforce logging
- Create Tasks for each diligence workstream with owner and due date
- Log each call as Activity with notes
- Update Opportunity stage at each gate
- Attach final evidence pack and memo to Opportunity
