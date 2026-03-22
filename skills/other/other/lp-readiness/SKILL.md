---
name: lp-readiness
description: Startup preflight gate (S1). Lightweight readiness check before entering the offer-building stage. Validates offer clarity, distribution feasibility, and measurement plan against minimal startup criteria.
---

# lp-readiness — Startup Preflight Gate (S1)

Pre-offer readiness check for startups entering the loop. Validates that the business has enough context to proceed to S2 (offer building) without blocking on missing fundamentals.

## Invocation

```
/lp-readiness --business <BIZ>
```

Required:
- `--business <BIZ>` — business identifier (e.g., BRIK, SEG, INT)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

READ + AUDIT + GATE

This skill:
- Reads business context from `docs/business-os/strategy/<BIZ>/` and `docs/business-os/startup-baselines/`
- Audits against 3 lightweight startup readiness gates
- Produces a binary go/no-go verdict with specific fail reasons
- Does NOT modify any files
- Does NOT ask follow-up questions (fails fast if gates don't pass)

## Relationship to ASSESSMENT GATE

When `start-point=problem`, the **ASSESSMENT GATE** (GATE-ASSESSMENT-00) runs before ASSESSMENT-10 (brand profiling) and ASSESSMENT-11 (brand identity), which precede S1. GATE-ASSESSMENT-00 validates all ASSESSMENT-01 through ASSESSMENT-08 sub-stage artifacts including distribution feasibility (ASSESSMENT-06) and measurement plan (ASSESSMENT-07). After the gate passes, ASSESSMENT-10 (brand profiling) and ASSESSMENT-11 (brand identity) run in sequence before lp-readiness is reached. In this path, lp-readiness serves as a confirmation pass — RG-01, RG-02, and RG-03 should already be satisfied by ASSESSMENT artifacts and the gate checks should return PASS quickly.

When `start-point=product`, operators bypass ASSESSMENT entirely. lp-readiness performs the full RG-01/RG-02/RG-03 checks from scratch against whatever strategy docs exist.

## Scope Boundaries

This startup readiness skill targets early-stage businesses and lightweight launch validation. It differs from heavier enterprise readiness flows in:

1. **3 gates vs 7 gates**: Only checks (a) offer clarity, (b) distribution feasibility, (c) measurement plan — NOT business-plan freshness, outcome clarity, code-to-plan traceability, tooling/data prereqs, decision context, or market research freshness
2. **No existing business data required**: Works from zero — no historical data, no active plan targets, no BOS cards/stage-docs needed
3. **Simpler output**: Binary go/no-go verdict with fail reasons, not a comprehensive readiness report with question cycles and missing-context registers
4. **No agent API dependency**: Doesn't need BOS APIs for cards, ideas, or stage-docs
5. **Lighter validation**: Accepts hypothesis-level clarity vs. requiring validated outcomes and traceability

## Inputs

Required files (at least ONE must exist):
- `docs/business-os/strategy/<BIZ>/*.user.md` — any strategy doc (revenue architecture, business model, etc.)
- `docs/business-os/startup-baselines/<BIZ>/*.md` — baseline docs (offer, distribution, measurement, research)

Optional:
- `docs/business-os/People.md` — team context
- Product specs, brand docs, or other strategy artifacts

## Readiness Gates

### RG-01: Offer Clarity

Does an offer hypothesis exist with enough specificity to build a test?

**Pass criteria:**
- Product/service described (what is being sold)
- Target customer identified (who is buying)
- Value proposition articulated (why they buy)
- Price intent stated (rough price point or pricing model)

**Fail examples:**
- "We'll sell something online" (no product specificity)
- "Everyone who needs X" (no customer segmentation)
- "High-quality service" (no differentiated value prop)
- "We'll figure out pricing later" (no price anchor)

### RG-02: Distribution Feasibility

Are ≥2 distribution channels identified with plausibility checks?

**Pass criteria:**
- At least 2 channels named (e.g., direct web, marketplace, referral, paid ads, content)
- Basic cost/effort estimate for each (order of magnitude: low/medium/high)
- No fatal blockers identified (e.g., "requires $500k upfront budget we don't have")
- Channel-to-customer fit is plausible (matches target customer behavior)

**Fail examples:**
- Only 1 channel identified (single point of failure)
- "TBD" or "we'll test everything" (no prioritization)
- Channels require infeasible resources (e.g., TV ads for bootstrapped startup)
- Mismatch (e.g., targeting B2B enterprise via Instagram influencers)

### RG-03: Measurement Plan

Can we measure whether the offer is working?

**Pass criteria:**
- Tracking method identified (analytics tool, manual log, spreadsheet, etc.)
- Key metrics named (≥2 metrics: e.g., conversion rate, CAC, retention, revenue)
- Baseline approach described (how to establish "success" threshold)
- Data collection is feasible with current resources

**Fail examples:**
- "We'll know if it works" (no specific metrics)
- Metrics require unavailable tooling (e.g., "need Salesforce" but don't have it)
- No baseline plan (can't tell if 5% conversion is good or bad)
- Data collection requires prohibited access (GDPR violations, scraping, etc.)

### DEP Capture Advisory (informational — not an S1 gate)

S1 is the recommended start of Demand Evidence Pack (DEP) capture. DEP is not a blocking gate at S1 — readiness is intentionally hypothesis-tolerant — but early capture reduces S6B activation lag.

When producing the S1 verdict, include this advisory section:

```
## Demand Evidence Pack (DEP) Capture

DEP is required before GATE-S6B-ACT-01 (spend authorization). Starting capture at S1 reduces channel activation lag by 1-2 weeks.

To start now:
- Register at least 1 message hypothesis (channel + audience_slice + asset_ref)
- Set up source-tagged tracking before any test impressions
- Schema: docs/business-os/startup-loop/schemas/demand-evidence-pack-schema.md

Current DEP status: [Not started | In progress | Pass-floor met]
```

If DEP is already in progress, note its status in the Context Summary. If DEP is not started, include the above advisory — do not block GO verdict for its absence.

## Workflow

### Stage 1: Load Context (READ)

1. Scan `docs/business-os/strategy/<BIZ>/` for strategy docs
2. Scan `docs/business-os/startup-baselines/<BIZ>/*.md` for baseline docs
3. Load `docs/business-os/People.md` if it exists
4. Aggregate offer, distribution, measurement context from all sources

### Stage 2: Run Gates (AUDIT)

For each gate (RG-01, RG-02, RG-03):
1. Extract relevant evidence from loaded context
2. Check pass criteria explicitly (all must be satisfied)
3. Record verdict: PASS or FAIL with specific reason
4. Do NOT attempt to fix failures — fail fast with clear reason

### Stage 3: Produce Verdict (GATE)

1. Aggregate gate results
2. Determine overall go/no-go:
   - **GO** if all 3 gates pass
   - **NO-GO** if any gate fails
3. Output verdict in contract format (see below)
4. If NO-GO, list all fail reasons and recommend next action

## Output Contract

```markdown
# Startup Readiness Verdict — <BIZ>

**Overall**: [GO | NO-GO]

## Gate Results

### RG-01: Offer Clarity
**Status**: [PASS | FAIL]
**Evidence**: [1-2 sentences citing specific docs/sections]
**Reason**: [If FAIL: specific missing element]

### RG-02: Distribution Feasibility
**Status**: [PASS | FAIL]
**Evidence**: [1-2 sentences citing specific docs/sections]
**Reason**: [If FAIL: specific missing element]

### RG-03: Measurement Plan
**Status**: [PASS | FAIL]
**Evidence**: [1-2 sentences citing specific docs/sections]
**Reason**: [If FAIL: specific missing element]

## Verdict

[If GO]:
✅ All gates pass. Ready to proceed to S2 (lp-offer).

[If NO-GO]:
❌ Cannot proceed to S2. Address the following:
- [Gate ID]: [Fail reason with actionable fix]
- [Gate ID]: [Fail reason with actionable fix]

**Recommended next action**: [Specific task to unblock, e.g., "Create offer baseline doc", "Add 2nd distribution channel to strategy doc"]

## Context Summary

**Files scanned**: [List of files read]
**Strategy docs found**: [Count]
**Baseline docs found**: [Count]
```

## Quality Checks

Before producing output, verify:
- QC-01: All 3 gates (RG-01, RG-02, RG-03) have explicit PASS/FAIL verdicts
- QC-02: Every FAIL has a specific reason citing what's missing (not generic "needs more detail")
- QC-03: Evidence cites actual file paths and sections (not hallucinated)
- QC-04: Overall verdict matches gate results (if any FAIL → NO-GO)
- QC-05: Files scanned list is accurate and complete

## Red Flags

Invalid outputs:
- Generic reasons ("needs more clarity" without stating what's unclear)
- Passing RG-01 when no price intent exists
- Passing RG-02 with <2 channels or no cost/effort estimates
- Passing RG-03 when metrics are "TBD"
- GO verdict with any gate in FAIL state
- Evidence citing files that don't exist
- Skipping any of the 3 gates

## Integration

### Upstream (S0)
- Preceded by optional `/lp-do-idea-forecast` or manual strategy doc creation
- Does NOT require BOS card/stage-doc setup

### Downstream (S2)
- If GO → proceed to `/lp-offer --business <BIZ>` (S2B)
- If NO-GO → user must address fail reasons, then re-run `/lp-readiness`
- lp-offer skill expects offer clarity from RG-01 as input

### Parallel Skills
- Does NOT block or depend on `/idea-scan` or other BOS workflows
