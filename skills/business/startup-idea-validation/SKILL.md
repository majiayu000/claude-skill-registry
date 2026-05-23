---
name: startup-idea-validation
description: "Systematic 9-dimension validation machine for testing ideas before building. Covers problem severity, market sizing, timing, competitive moats, unit economics, founder-market fit, technical feasibility, GTM clarity, and risk profile. Makes GO/NO-GO decisions based on evidence, not assumptions."
metadata:
  globs: |
    **/*.md
    **/validation/**
    **/ideas/**
    **/hypothesis/**
---

# Startup Idea Validation

Systematic validation machine for testing ideas BEFORE building. Validate hypotheses, score opportunities, and make evidence-based GO/NO-GO decisions.

**Modern Best Practices (Dec 2025)**:
- Run a validation ladder (interviews → smoke test → concierge/MVP → paid pilots) before building.
- Pre-register decision thresholds (avoid “moving goalposts” after seeing data).
- Separate evidence quality (strong/medium/weak) from confidence and excitement.
- Test willingness-to-pay early (pricing pages, pilots, LOIs) and treat time-to-value as a constraint.
- Handle customer/market data with purpose limitation, retention, and access controls.

---

## When to Use This Skill

| Trigger | Action |
|---------|--------|
| "Validate this idea" | Run full 9-dimension validation |
| "Is this worth building?" | Run validation scorecard |
| "Test my hypothesis" | Run hypothesis canvas |
| "Market size for X" | Run market sizing |
| "Should I build X or Y?" | Run comparative validation |
| "What's the riskiest assumption?" | Run RAT analysis |

---

## Validation Ladder (Dec 2025)

| Step | Goal | Strong signal | Weak signal | Output |
|------|------|---------------|-------------|--------|
| Customer interviews | Validate problem + context | Repeated pain + real workarounds | Hypothetical enthusiasm | Notes + quotes + JTBD |
| Smoke test | Validate demand | Clicks/signups with clear intent | Survey-only interest | Landing page metrics |
| Concierge / Wizard-of-Oz | Validate workflow value | Users complete job and return | One-off curiosity | Learning report |
| Paid pilot | Validate willingness-to-pay | Paid, renewed, or expanded | “Will pay later” | Pilot results + pricing |

Use `templates/validation-experiment-planner.md` for experiment design and decision thresholds.

## 9-Dimension Validation Framework

### Quick Reference

| Dimension | Weight | Key Question | Score Range |
|-----------|--------|--------------|-------------|
| **Problem Severity** | 15% | Hair on fire or nice to have? | 0-10 |
| **Market Size** | 12% | Big enough to matter? | 0-10 |
| **Market Timing** | 10% | Why now? | 0-10 |
| **Competitive Moat** | 12% | Defensible advantage? | 0-10 |
| **Unit Economics** | 15% | Can this be profitable? | 0-10 |
| **Founder-Market Fit** | 8% | Right team for this? | 0-10 |
| **Technical Feasibility** | 10% | Can we actually build it? | 0-10 |
| **GTM Clarity** | 10% | Know how to reach customers? | 0-10 |
| **Risk Profile** | 8% | Manageable risk level? | 0-10 |

### Verdict Thresholds

| Score | Verdict | Action |
|-------|---------|--------|
| **80-100** | Strong GO | Proceed to build |
| **60-79** | Conditional GO | Validate riskiest assumptions first |
| **40-59** | PIVOT | Core hypothesis needs rework |
| **<40** | NO-GO | Fundamental issues, don't build |

---

## Dimension Deep Dives

### 1. Problem Severity (15%)

**Question**: Is this a "hair on fire" problem or a "nice to have"?

**Signal Strength Indicators**:

| Score | Description | Evidence |
|-------|-------------|----------|
| 9-10 | Hair on fire | Customers actively seeking solutions, willing to pay premium |
| 7-8 | Significant pain | Multiple workarounds in use, clear cost of problem |
| 5-6 | Real but manageable | Occasional complaints, spreadsheet solutions exist |
| 3-4 | Nice to have | Would be good but not urgent |
| 1-2 | No real pain | Solution looking for a problem |

**Evidence Sources**:
- Review mining (G2, Capterra, Reddit) → [startup-review-mining](../startup-review-mining/SKILL.md)
- Customer interviews (5-10 minimum)
- Support ticket analysis
- Search volume for solutions

### 2. Market Size (12%)

**Question**: Is this market big enough to build a venture-scale business?

**TAM/SAM/SOM Framework**:

| Metric | Definition | Minimum Threshold |
|--------|------------|-------------------|
| TAM | Total Addressable Market | $1B+ |
| SAM | Serviceable Addressable Market | $100M+ |
| SOM | Serviceable Obtainable Market (3yr) | $10M+ |

**Sizing Methods**:
- Top-down: Industry reports, analyst estimates
- Bottom-up: Customer count × ACV
- Comparable: Similar company revenue extrapolation

### 3. Market Timing (10%)

**Question**: Why now? What's changed that makes this possible/necessary?

**Timing Signal Matrix**:

| Signal | Strong | Weak |
|--------|--------|------|
| Technology enabler | Just became viable | Has existed for years |
| Regulatory change | New opportunity | No change |
| Behavior shift | COVID/platform shifts changed habits | Status quo |
| Cost curve | 10x cheaper now | Same cost |
| Competition | Market forming | Saturated |

**Integration**: Use [startup-trend-prediction](../startup-trend-prediction/SKILL.md) for timing analysis.

### 4. Competitive Moat (12%)

**Question**: What will make this defensible over time?

**Moat Type Assessment**:

| Moat Type | Strength | Build Time | Example |
|-----------|----------|------------|---------|
| Network Effects | Very Strong | 18-24mo | Marketplace, social |
| Switching Costs | Strong | 12-18mo | Workflow integration |
| Data Moats | Medium | 6-12mo | Proprietary datasets |
| Brand | Medium | 24mo+ | Trust, reputation |
| Regulatory | Strong | Variable | Licenses, compliance |
| Technology | Weak | <6mo | Can be copied |

### 5. Unit Economics (15%)

**Question**: Can this be a profitable business?

**Key Metrics**:

| Metric | Target | Red Flag |
|--------|--------|----------|
| LTV:CAC | >3:1 | <2:1 |
| Payback Period | <12 months | >24 months |
| Gross Margin | >70% (SaaS) | <50% |
| NRR | >100% | <80% |

**Formula Basics**:
```
LTV = (ARPU × Gross Margin) / Monthly Churn
CAC = Total Sales & Marketing / New Customers
```

### 6. Founder-Market Fit (8%)

**Question**: Are you the right person/team to solve this?

**Assessment Criteria**:

| Factor | Strong | Weak |
|--------|--------|------|
| Domain Expertise | 5+ years in space | No experience |
| Network | Direct access to buyers | Cold outreach only |
| Insight | Unique perspective | Generic understanding |
| Passion | Personal connection | Pure opportunity |
| Ability to Execute | Built similar before | First attempt |

### 7. Technical Feasibility (10%)

**Question**: Can we actually build this?

**Feasibility Matrix**:

| Factor | Score |
|--------|-------|
| Core technology exists | +3 |
| Similar products exist | +2 |
| Team has built similar | +2 |
| <6 month MVP possible | +2 |
| No regulatory blockers | +1 |

### 8. GTM Clarity (10%)

**Question**: Do we know how to reach and convert customers?

**GTM Readiness**:

| Element | Clear | Unclear |
|---------|-------|---------|
| ICP definition | Specific persona | "Everyone" |
| Acquisition channel | Tested, CAC known | Guessing |
| Sales motion | PLG/Sales/Hybrid decided | TBD |
| Pricing | Market-validated | Assumed |
| First 10 customers | Identified | Unknown |

### 9. Risk Profile (8%)

**Question**: What could kill this and how likely?

**Risk Categories**:

| Risk Type | Example | Mitigation |
|-----------|---------|------------|
| Market | Demand doesn't materialize | Validate with pre-sales |
| Technical | Can't build at scale | Prototype early |
| Execution | Team can't deliver | Start small |
| Regulatory | Law changes | Legal review |
| Funding | Can't raise | Bootstrap path |
| Competition | Incumbent pivots | Speed, niche |

---

## Validation Workflow

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. PROBLEM VALIDATION               │
│    - Review mining (10+ sources)    │
│    - Customer interviews (5-10)     │
│    - Pain severity scoring          │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ 2. MARKET VALIDATION                │
│    - TAM/SAM/SOM calculation        │
│    - Timing analysis (trends)       │
│    - Competitive landscape          │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ 3. SOLUTION VALIDATION              │
│    - Technical feasibility          │
│    - Moat assessment                │
│    - Unit economics modeling        │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ 4. EXECUTION VALIDATION             │
│    - Founder-market fit             │
│    - GTM clarity                    │
│    - Risk assessment                │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ 5. SCORECARD & DECISION             │
│    - 9-dimension scoring            │
│    - GO/NO-GO verdict               │
│    - RAT identification             │
└─────────────────────────────────────┘
  │
  ▼
GO / CONDITIONAL GO / PIVOT / NO-GO
```

---

## Navigation

### Resources (Deep Dives)

| Resource | Purpose |
|----------|---------|
| [validation-methodology.md](resources/validation-methodology.md) | 9-dimension scoring system details |
| [hypothesis-testing-guide.md](resources/hypothesis-testing-guide.md) | How to run validation experiments |
| [market-sizing-patterns.md](resources/market-sizing-patterns.md) | TAM/SAM/SOM calculation methods |
| [moat-assessment-framework.md](resources/moat-assessment-framework.md) | Competitive barrier analysis |

### Templates (Outputs)

| Template | Use For |
|----------|---------|
| [validation-scorecard.md](templates/validation-scorecard.md) | Full 9-dimension scoring |
| [hypothesis-canvas.md](templates/hypothesis-canvas.md) | Hypothesis testing template |
| [validation-experiment-planner.md](templates/validation-experiment-planner.md) | Hypothesis → method → metric → decision |
| [riskiest-assumption-test.md](templates/riskiest-assumption-test.md) | RAT experiment design |
| [market-sizing-worksheet.md](templates/market-sizing-worksheet.md) | TAM/SAM/SOM calculation |
| [go-no-go-decision.md](templates/go-no-go-decision.md) | Final decision template |

### Data

| File | Contents |
|------|----------|
| [sources.json](data/sources.json) | Validation resources (YC, a16z, SVPG, etc.) |

---

## Integration Points

### Receives From

- [startup-review-mining](../startup-review-mining/SKILL.md) - Pain point evidence
- [startup-trend-prediction](../startup-trend-prediction/SKILL.md) - Market timing data
- [startup-competitive-analysis](../startup-competitive-analysis/SKILL.md) - Competitor data

### Feeds Into

- [router-startup](../router-startup/SKILL.md) - Validation results
- [product-management](../product-management/SKILL.md) - Validated requirements
- [startup-business-models](../startup-business-models/SKILL.md) - Monetization decisions

---

## Quick Start

### Minimum Viable Validation

For rapid first-pass validation:

1. **Pain Check** (15 min)
   - Search G2/Capterra for competitor complaints
   - Search Reddit for problem discussions
   - Score: Is this severe enough to trigger action (not “nice to have”)?

2. **Size Check** (15 min)
   - How many potential customers?
   - What would they pay?
   - Is the market plausibly large enough for your target outcome? [Inference]

3. **Timing Check** (10 min)
   - Why now vs 2 years ago?
   - What changed?

4. **Competition Check** (15 min)
   - Who else is doing this?
   - What's wrong with existing solutions?

**If all 4 checks pass**: Proceed to full validation scorecard.
**If any fail**: Pivot or abandon.

---

## Key Principles

### Evidence Over Opinion

Every score must have evidence:
- GOOD: "Pain score 8/10: 47 reviews mention this specific complaint (sources linked)"
- BAD: "Pain score 8/10: I think this is a real problem"

### Invalidate Fast

Goal is to find reasons NOT to build:
- Cheap to kill ideas, expensive to build
- Seek disconfirming evidence
- Run the riskiest assumption test first

### Iterate the Idea, Not Just the Validation

If validation reveals issues:
- Don't just re-score, adjust the idea
- Pivot to stronger position
- Find the version that scores 80+

---

## Do / Avoid (Dec 2025)

### Do

- Validate the riskiest assumption first (RAT), not the easiest to test.
- Use the ladder: interviews → smoke → concierge → paid pilots.
- Treat willingness-to-pay as a primary signal, not an afterthought.
- Write decision thresholds before running experiments.

### Avoid

- Survey-only validation and hypothetical questions (“Would you use this?”).
- Sampling bias (friends, one subreddit, one review site) without triangulation.
- Building an MVP as “validation” without falsifiable hypotheses.

## What Good Looks Like

- ICP: one narrow segment with a clear job, pain severity, and buying trigger.
- Evidence: 10+ direct conversations in the ICP with repeatable pain patterns (not one-off anecdotes).
- WTP: explicit pricing tests and at least one “paid” signal (deposit, pilot fee, LOI with price).
- Experiments: hypotheses + success metrics + stop rules written before execution.
- Decision: a documented go/no-go with the next smallest reversible step.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Summarization/clustering: speed up synthesis, but keep raw notes + spot-checks.
- Copy drafting: generate landing page variants; humans verify claims and compliance.
