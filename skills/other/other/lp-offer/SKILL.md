---
name: lp-offer
description: Startup offer design skill (MARKET-06). Consolidates ICP, positioning, pricing, and offer design into one artifact with 6 sections. Produces a validated offer hypothesis ready for forecasting and channel selection.
---

# lp-offer — Startup Offer Design (MARKET-06)

Produces a comprehensive offer artifact for startups. Defines ICP, pain/promise mapping, offer structure, positioning, pricing hypothesis, and objection handling in one document.

## Invocation

```
/lp-offer --business <BIZ>
```

Required:
- `--business <BIZ>` — business identifier (e.g., BRIK, SEG, INT)

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

## Operating Mode

RESEARCH + DESIGN + DOCUMENT

This skill:
- Researches competitor offerings, pricing, and customer reviews
- Designs a structured offer hypothesis with 6 sections
- Documents the offer artifact at `docs/business-os/startup-baselines/<BIZ>/offer.md`
- Does NOT make final pricing decisions (produces hypothesis to validate)
- Does NOT skip sections (all 6 MUST be present)

## Inputs

Required:
- `lp-readiness` output (offer clarity gaps from RG-01 gate)
- Business context from `docs/business-os/strategy/<BIZ>/` or user-provided description
- What the business does, what it sells, who it targets

Optional (enhances quality):
- Competitor websites, pricing pages, product listings
- Customer reviews (competitor products/services)
- Market research docs from `docs/business-os/market-research/`
- Existing offer drafts or positioning statements
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` — enhances Positioning One-Pager (Section 4) voice and personality

## Workflow

### Stage 1: Load Context (RESEARCH)

1. Read `lp-readiness` output to understand offer clarity gaps
2. Load business context from strategy docs
3. Identify 3-5 direct competitors
4. **Dispatch ONE subagent per competitor in a SINGLE message (parallel).** Each subagent receives `.claude/skills/lp-offer/competitor-research-brief.md` as its brief. Subagents run read-only Mode A (analysis phase only — no file writes). Protocol: `_shared/subagent-dispatch-contract.md`.
   - Hard limit: **200 words max per subagent output**
   - If a subagent returns > 200 words: orchestrator truncates to structured schema fields, discards prose before synthesis
   - If a subagent returns `status: fail`: quarantine result, continue with remaining, flag gap in Evidence Register
5. Merge all structured extracts into the Evidence Register. Then proceed to Stage 2.

### Stage 2: Build Offer Artifact (DESIGN)

Create artifact with 6 mandatory sections:

#### Section 1: ICP Segmentation

Define 1-2 Ideal Customer Profiles (ICPs). Each ICP includes:
- **Demographics**: Age, location, income, job title, company size (B2B)
- **Psychographics**: Values, fears, aspirations, buying style
- **Jobs-to-be-done**: What functional/emotional/social job does the offer solve?
- **Buying triggers**: What event/pain/threshold prompts them to buy NOW?

**Specificity test**: If "everyone" qualifies, the ICP is too broad. Narrow it.

#### Section 2: Pain/Promise Mapping

For each ICP, map top 3 pains to specific promises:

| Pain (Customer Language) | Promise (Our Solution) | Evidence Source |
|--------------------------|------------------------|-----------------|
| [Exact pain from reviews/research] | [Specific outcome we deliver] | [Competitor review, research doc, customer interview] |

**Review mining guidance**:
- Search competitor reviews for: "I wish...", "frustrating", "difficult", "doesn't work", "missing"
- Extract verbatim customer language (use their words, not marketing speak)
- Note patterns: if 5+ reviews mention same pain, it's a top priority

#### Section 3: Offer Structure

Define what the customer receives:
- **Core offer**: The main product/service (be specific: "12-week coaching program" not "coaching")
- **Bundles**: Any package variants (basic/pro/enterprise)
- **Included deliverables**: What tangible/intangible items are included?
- **Exclusions**: What's NOT included (set boundaries)
- **Guarantees**: Money-back, satisfaction, performance guarantees
- **Risk reversals**: Free trial, sample, audit, assessment, no-commit first session

**Concreteness test**: Could a competitor easily copy this structure? If not specific enough, add detail.

#### Section 4: Positioning One-Pager

Positioning statement using Geoffrey Moore's template:

```
For [target customer segment]
Who [have this specific need/pain]
[Product/service name] is [category]
That [key differentiated benefit]
Unlike [primary alternative/competitor]
Because [reason to believe / unique capability]
```

**Additional elements**:
- **Category creation**: Are we defining a new category or claiming position in existing one?
- **Competitive frame**: What do customers compare us to? (Not always direct competitors)
- **Key message**: One-sentence elevator pitch derived from positioning statement

#### Section 5: Pricing/Packaging Hypothesis

**THIS IS A HYPOTHESIS TO VALIDATE, NOT A FINAL PRICE.**

Pricing analysis:
- **Proposed price point(s)**: Primary offer price + any tier variants
- **Pricing model**: One-time, subscription, usage-based, value-based, freemium
- **Competitor price comparison**: List 3-5 competitors with their pricing (create comparison table)
- **Anchor pricing**: What higher-priced alternative sets the reference point?
- **Price positioning**: Premium, mid-market, value/budget?
- **Rationale**: Why this price? (Cost-plus, value-based, competitive parity, penetration, skimming)

**Confidence level**: State LOW/MEDIUM/HIGH confidence and what evidence is missing.

**Validation plan**: What experiments will test pricing hypothesis? (Landing page test, pre-sales, tiered offers, etc.)

#### Section 6: Objection Map + Risk Reversal

Top 5 objections with responses:

| Objection | Response | Proof/Risk Reversal |
|-----------|----------|---------------------|
| [Common reason not to buy] | [Logical/emotional counter] | [Guarantee, case study, testimonial, free trial] |

**Sources for objections**:
- Competitor reviews (what customers complain about)
- Sales conversations (if available)
- Price sensitivity ("too expensive")
- Credibility gaps ("never heard of you")
- Comparison anxiety ("how do I know you're better than X?")

**Risk reversal mechanisms**:
- Money-back guarantee (30/60/90 day)
- Free trial or freemium tier
- Performance guarantee ("results or refund")
- Satisfaction guarantee ("love it or leave")
- Pilot/sample/audit (B2B)
- No-contract/cancel-anytime (subscription)

### Stage 3: Document Artifact (DOCUMENT)

1. Write complete offer artifact to `docs/business-os/startup-baselines/<BIZ>/offer.md`
2. Include metadata header:
   ```yaml
   ---
   business: <BIZ>
   artifact: offer-design
   created: <date>
   status: hypothesis
   confidence: [low/medium/high]
   ---
   ```
3. Append evidence register at end: list all sources consulted (competitor URLs, review sites, research docs)
4. Self-audit against Quality Checks (see below)

## Output Contract

Produces single file: `docs/business-os/startup-baselines/<BIZ>/offer.md`

**Artifact registry**: Canonical path defined in `docs/business-os/startup-loop/artifact-registry.md` (artifact ID: `offer`).

**Structure**:
1. Metadata frontmatter (YAML)
2. Executive summary (2-3 sentences: what is the offer, who is it for, what makes it different)
3. Section 1: ICP Segmentation (1-2 ICPs with all 4 elements)
4. Section 2: Pain/Promise Mapping (table format, 3 pains per ICP)
5. Section 3: Offer Structure (core offer, bundles, guarantees, risk reversals)
6. Section 4: Positioning One-Pager (Moore template filled, category/frame/message)
7. Section 5: Pricing/Packaging Hypothesis (price points, competitor comparison table, rationale, confidence, validation plan)
8. Section 6: Objection Map + Risk Reversal (table format, 5 objections)
9. Evidence Register (sources cited with URLs or file paths)

**Downstream compatibility**:
- `lp-forecast` consumes: ICP (for TAM/SAM estimation), pricing hypothesis (for revenue modeling), confidence level (for scenario ranges)
- `lp-channels` consumes: ICP (for channel-customer fit), positioning (for messaging), objections (for content strategy)
- `lp-do-critique` (DS-14 offer mode) consumes: entire artifact for critique

## Quality Checks

Before finalizing, verify:
- QC-01: All 6 sections present and complete (ICP, pain/promise, structure, positioning, pricing, objections)
- QC-02: ICP is specific (not "everyone" or "small businesses")
- QC-03: Pricing hypothesis includes competitor comparison (≥3 competitors with prices)
- QC-04: At least 3 objections mapped with responses
- QC-05: At least 1 risk reversal mechanism defined
- QC-06: Confidence level stated explicitly (low/medium/high)
- QC-07: Evidence register cites ≥3 sources (competitor sites, reviews, or research docs)
- QC-08: Pain/promise mapping uses customer language from reviews/research (not marketing speak)
- QC-09: Positioning statement fills all 6 blanks in Moore template
- QC-10: Pricing rationale explains WHY this price (not just "seems right")

## Red Flags

Invalid outputs that MUST be rejected:
- Missing any of the 6 sections
- ICP says "everyone", "anyone who needs X", "small to medium businesses" (too broad)
- No competitor pricing cited (makes pricing hypothesis ungrounded)
- Pricing shows final decision confidence ("this IS the price") instead of hypothesis to validate
- Pain/promise mapping uses generic pains ("wants better results") not specific customer language
- Positioning statement has blanks or says "TBD"
- <3 objections mapped
- No risk reversal mechanism (no guarantee, trial, or reversal)
- Evidence register empty or cites non-existent files
- Confidence level missing

## Integration

### Upstream (MARKET-01 + readiness context)
- Preceded by `/lp-readiness --business <BIZ>` (must pass RG-01 offer clarity gate)
- Consumes offer clarity gaps from readiness output
- Reads business context from `docs/business-os/strategy/<BIZ>/`

### Downstream (S3, SELL-01)
- `/lp-forecast --business <BIZ>` (S3) reads ICP and pricing hypothesis for revenue modeling
- `/lp-channels --business <BIZ>` (SELL-01) reads ICP, positioning, and objections for channel selection
- `lp-do-critique` (DS-14 offer mode) critiques this artifact for logical gaps

### Parallel Skills
- Can run after or parallel to `/lp-market` (market research baseline) if it exists
- Does NOT depend on `/lp-forecast` or `/lp-channels` (this skill is prerequisite for those)
