---
name: dealflow-sourcing-to-memo
description: "End-to-end associate workflow with time-boxed gates: thesis -> sourcing -> meetings -> diligence -> memo, ending with either IC-ready memo or explicit kill decision. Use when you need to run the full pipeline for a sector or a specific deal."
license: Proprietary
compatibility: Requires web access for research + Salesforce logging is mandatory; can be run without scripts.
metadata:
  author: evalops
  version: "0.2"
---
# Dealflow: sourcing to memo

## When to use
Use this compound skill when you need to simulate a full associate workflow:
- Build a sector view and generate targets
- Source and qualify companies
- Move a specific deal from first meeting to memo/IC
- Keep Salesforce current so the team can route work

## Inputs you should request (only if missing)
- Thesis area (or a company to start from)
- Stage focus and decision timeline
- CRM conventions (Salesforce stages/fields) if known
- Sprint length: 3-day, 5-day, or 10-day

## Outputs you must produce

**Every workflow ends with one of two outcomes:**
1. **Partner-ready memo + scheduled IC** - deal advances
2. **Explicit kill decision** with logged reason, "what would change our mind", and a follow-up reminder (e.g., "recheck in 6 months")

No deals in limbo. No "watching" without a recheck date.

## Time-boxed workflow (default: 10-day sprint)

### Phase 0: Set thesis (Day 0-1, max 8 hours)
**Deliverables:**
- Wedge + buyer + why now (1 page)
- Initial market map (50-150 companies in CSV)
- Top 10 force-ranked targets with "must be true" + fastest test
- Kill criteria for the thesis

**Gate:** Do you have a clear buyer, budget source, and trigger event? If no, iterate or kill the thesis.

Log: create Campaign `Thesis: <topic> (YYYY-MM)` in Salesforce

### Phase 1: Source (Days 1-3)
**Deliverables:**
- Top 50 humans list (network cultivation)
- Weekly pipeline update with 10 new names (all in Salesforce)
- 5 outreach targets sent
- 3 meetings scheduled

**Gate:** Did you generate 3 qualified meeting candidates? If no, the thesis is too narrow or your signals are wrong. Iterate or kill.

Log: all Leads/Accounts created with next-step Tasks

### Phase 2: First meetings (Days 3-5)
For each qualified company:
1) Write meeting brief (kill questions + wedge hypothesis + "must be true")
2) Run the meeting with structure and note-taking rules
3) Same-day follow-up (value + next steps) within 2 hours
4) 5-bullet recap logged to Salesforce within 2 hours

**Gate (per company):** Advance to diligence OR pass with reasons.

**Pass requirements:**
- Tagged reason in Salesforce
- "What would change our mind" documented
- Recheck date set (3/6/12 months)

Log: Event + Notes + Opportunity stage update

### Phase 3: Diligence sprint (Days 5-8, max 3 days per deal)
**Deliverables:**
- Ranked risk register (MAX 4 risks)
- Fastest test per risk (time-boxed)
- Customer diligence (3 buyers, 2 users, 1 churned/lost - REQUIRED)
- Anti-confirmation evidence (competitor/alternative user)
- Evidence pack

**Gate:** For each risk, did the test produce decision-changing evidence? If a critical risk remains untestable, consider killing the deal.

Log: Tasks per workstream + Activity logs for calls

### Phase 4: Memo + decision (Days 8-10)
**Deliverables:**
- Memo with clear recommendation in first line (no hedging)
- Steelman "best argument against"
- Decision log (what changed since first call)
- IC date scheduled OR explicit kill with recheck date

**Final gate:** One of two outcomes only:
1. **ADVANCE:** Partner-ready memo + IC scheduled
2. **KILL:** Pass logged with reason + "what would change our mind" + recheck date

Log: attach memo to Opportunity + update stage to "IC Scheduled" or "Passed"

## Sprint variants

### 3-day sprint (urgent deal)
- Day 0: Thesis alignment + risk register (2 hours)
- Day 1: Customer diligence (3-5 calls)
- Day 2: Product/GTM validation
- Day 3: Memo draft + decision

Gate at end of Day 2: Kill or continue? No "need more time."

### 5-day sprint (standard deal)
- Days 0-1: Risk register + diligence plan
- Days 2-3: Customer + product + GTM diligence
- Day 4: Evidence synthesis
- Day 5: Memo + decision

Gate at end of Day 3: All top 4 risks tested? If not, why?

### 10-day sprint (new thesis + deal)
- Days 0-1: Thesis + market map
- Days 1-3: Sourcing
- Days 3-5: First meetings
- Days 5-8: Diligence
- Days 8-10: Memo + decision

Gate at each phase transition.

## Decision gates (mandatory checkpoints)

At each gate, you must answer:
1. **Kill?** Is there a clear reason to stop? If yes, log it and set recheck date.
2. **Continue?** Is there enough signal to invest more time? What's the next deliverable?
3. **Escalate?** Does a partner need to weigh in before proceeding?

No "let's keep watching" without a concrete recheck date and trigger.

## Guardrails
- Do not "diligence everything." Diligence the top 4 risks.
- Always write "must be true" claims early; update with evidence.
- **Salesforce is the source of truth.** If it's not logged, it didn't happen.
- Every active opportunity must have a dated next step task.
- Every meeting must have a 5-bullet recap within 2 hours.
- Every pass must have a tagged reason + "what would change our mind" + recheck date.

## References
Use atomic skills as needed:
- thesis-market-mapping
- signal-sourcing-engine
- founder-meeting-runbook
- diligence-risk-burndown
- investment-memo-writing
- salesforce-crm-ops
