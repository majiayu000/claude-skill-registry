---
name: diligence-risk-burndown
description: "Run diligence as a fast risk burn-down: build a ranked risk register (max 4), execute the fastest tests, and produce decision-changing evidence. Use when a deal advances past first meeting."
license: Proprietary
compatibility: Works offline; improved with web access and customer calls; optional Salesforce logging.
metadata:
  author: evalops
  version: "0.2"
---
# Diligence risk burn-down

## When to use
Use this skill when:
- A company is past first meeting and needs structured diligence
- You need to answer "what could kill this?" quickly
- You need customer, product, GTM, and team evidence for an IC memo

## Inputs you should request (only if missing)
- Stage + round dynamics (lead? follow? timeline?)
- A draft "must be true" list from the first meeting
- Access to customer references (including churned / lost deals if possible)
- Data room or key docs (deck, pipeline, financial model, product docs)

## Outputs you must produce
1) **Ranked risk register** (MAX 4 RISKS - force prioritization)
2) **Diligence plan** (one fastest test per risk, time-boxed)
3) **Evidence pack** (notes + quotes + data)
4) **Anti-confirmation evidence** (required: churned customer or lost deal call, competitor validation)
5) **Go/No-go recommendation** with rationale

Templates:
- assets/risk-register.md
- assets/diligence-plan.md
- assets/customer-call-script.md
- assets/product-eval-checklist.md

## Hard rules

### Max 4 risks (non-negotiable)
- If you have more than 4 risks, you haven't prioritized.
- The discipline is choosing: what are the 4 things that would actually kill this deal?
- Other concerns go in "watch list" but don't get active diligence time.

### One fastest test per risk
- For each risk, define the single fastest test that generates decision-changing evidence.
- "More research" is not a test. A test has a clear pass/fail outcome.
- Examples of fast tests:
  - 1 buyer call with a specific question
  - Pipeline inspection: stage aging, sources, cycle time
  - Hands-on product evaluation with a "blank sheet" re-explain test
  - Churned / lost prospect reference call

### Time-box per test
- Every test must have a deadline (hours or days, not weeks).
- If you can't complete the test in the time-box, the risk is either not testable or you need a different test.

### Evidence standard
- For each risk, write: "What evidence would convince us this risk is manageable?"
- And: "What evidence would kill the deal?"
- Be specific. "Good retention" is not an evidence standard. "Net retention >110% with cohort data" is.

## Procedure

### 1) Build the ranked risk register (MAX 4)
List risks in these buckets (pick the 4 that matter most):
- Market risk
- Product risk
- GTM risk
- Team risk
- Competitive/moat risk
- Deal/term risk (if relevant)

Rank by: *decision impact* x *uncertainty*.

**Hard rule:** If you can't name the top 4 ways this fails, you aren't diligencing yet.

### 2) Define the fastest falsification test for each risk
For each of the 4 risks, write:

| Risk | Evidence that increases conviction | Evidence that kills | Fastest test | Time-box | Owner |
|---|---|---|---|---|---|
| 1. | | | | hours/days | |
| 2. | | | | hours/days | |
| 3. | | | | hours/days | |
| 4. | | | | hours/days | |

### 3) Run anti-confirmation diligence (REQUIRED)

**At least one churned customer or lost deal call:**
- If the company has churned customers, you must talk to one.
- If no churn yet, talk to a lost deal (prospect who didn't buy).
- If neither exists, document why and discount retention claims heavily.

**At least one competitor/alternative validation:**
- Talk to someone using a competitor or the "do nothing" alternative.
- Understand: why didn't they choose this company? What would change their mind?
- If you can't do this, explain why it's impossible and document the gap.

### 4) Run customer diligence (buyers first)
Do at least:
- 3 buyer calls (people who sign)
- 2 user calls (people who use daily)
- 1 "failed" call (lost deal, churn, or disqualified) - REQUIRED

On calls, capture:
- Trigger event
- Alternatives considered
- What would make them churn
- Expansion path and constraints
- Procurement/security blockers

### 5) Product diligence (can it survive reality?)
- Request a live demo, then ask the founder to re-explain from scratch.
- Ask for 2-3 hard examples where the product broke and how they fixed it.
- Identify integration points and estimate real deployment cost.

### 6) GTM diligence (repeatability)
- Validate ICP specificity (not "mid-market enterprises").
- Validate cycle time and onboarding (time-to-value).
- Validate pricing logic and unit economics *by segment*.

### 7) Team diligence (learning rate + decision rights)
- Look for:
  - ability to change mind with evidence
  - clear ownership of GTM/product/eng
  - healthy conflict resolution

### 8) Competitive diligence (why incumbents don't win)
- Identify:
  - direct competitors
  - incumbent "good enough" substitutes
  - internal build threat

Ask: "If an incumbent shipped a V1 in 6 months, what still makes you win?"

## Salesforce logging (recommended)
- Ensure an **Opportunity** exists with a "Diligence" stage.
- Log each reference call as an Activity and tag it (buyer/user/churn/lost-deal).
- Create Tasks for diligence workstreams with owners and due dates.
- Attach/record the risk register + evidence pack (as Notes or Files).

Use `salesforce-crm-ops` if you need API patterns.

## Edge cases
- If the process is rushed: focus only on top 2 risks and explicitly document what you *did not* validate.
- If references are all friendly: insist on at least one "failed" reference; otherwise discount the signal.
- If you can't get anti-confirmation evidence: document this as a major gap and flag it in the memo.
