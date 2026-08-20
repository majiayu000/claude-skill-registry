---
name: prd-v10-chasm-adoption-moore
description: >
  Assess adoption-lifecycle stage, plan the chasm crossing, and build a beachhead strategy using
  Geoffrey Moore's Crossing the Chasm framework during PRD v1.0 Market Adoption. Triggers on
  requests to assess adoption stage, plan beachhead, cross the chasm, scale from early adopters,
  or when user asks "are we in the chasm?", "crossing the chasm", "beachhead strategy", "Moore",
  "whole product", "pragmatist buyers", "from early adopters to early majority". Outputs
  ADO-STAGE-*, ADO-BEACHHEAD-*, ADO-WHOLE-*, ADO-REF-* entries.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch

execution_modes:
  default: deep
  supports: [quick, standard, deep]
---

# Crossing the Chasm (Moore) — the v1.0 Spine

Position in workflow: v0.9 Feedback Loop Setup → **v1.0 Crossing the Chasm (Moore)** → all v1.0 work

## Execution Mode

Default is **deep** (this is a major strategic decision; quick mode is for hypothesis pre-work only). See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md).

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Stage assessment only (ADO-STAGE-*); beachhead candidate hypothesis |
| **standard** | Stage assessment + beachhead segment + top 3 whole-product gaps + reference-account candidate list |
| **deep** (default) | Full stage assessment with evidence + sharpened beachhead with in/not-in criteria + complete whole-product gap analysis + reference-account cultivation plan + chasm-crossing risk register |

## Framework: Moore's Technology Adoption Lifecycle

From *Crossing the Chasm* (Geoffrey Moore, 1991, updated 2014). The bestselling tech-strategy book of the 1990s, and still the canonical model for understanding why early traction doesn't predict mass adoption.

### The lifecycle

| Stage | % of market | Buyer mindset | What they buy |
|-------|-------------|---------------|----------------|
| **Innovators** (2.5%) | Tinkerers; technology enthusiasts | Want to try new things; tolerate incomplete products | Vision, technical depth, access |
| **Early Adopters** (13.5%) | Visionaries | Want strategic advantage from non-mainstream tech | Bold vision + first-mover ROI |
| **— THE CHASM —** | — | — | — |
| **Early Majority** (34%) | Pragmatists | Want reliable productivity gains from proven solutions | **Whole product** + segment-specific references |
| **Late Majority** (34%) | Conservatives | Want safe, mature defaults | Market leadership, low risk |
| **Laggards** (16%) | Skeptics | Resist change | (Generally not worth targeting) |

### The chasm

The gap between **Early Adopters** and **Early Majority** is the chasm. Most products die here. The reason: visionary buyers (who got you to early traction) actively *want* the cutting-edge, while pragmatist buyers want to be the second penguin off the iceberg — they need to see peers in their segment succeeding first.

### The chasm-crossing playbook

1. **Pick a beachhead segment** — A single, narrowly-defined sub-segment of the early majority. Not "small businesses." Specific: "freight-forwarding firms with 50-200 employees in the US Pacific Northwest using ERP X."
2. **Build the whole product for that beachhead** — Pragmatists don't buy your core product; they buy your core + integrations + reference customers + support + training + everything else they need to deploy. Identify and close the gaps.
3. **Cultivate references in segment** — A reference from outside the beachhead is worthless to a beachhead buyer. Three references *inside* the beachhead is the unlock.
4. **Concentrate, then expand** — Don't try to cross the chasm broadly. Win the beachhead, then use it as a reference base to win adjacent segments ("bowling alley" stage).

## Consumes

- **CFD-\* customer evidence** (all stages, especially v0.9 post-launch feedback) — Composition of paying customers; stage signal
- **PER-\* personas** (sharpened by v0.9 Positioning) — Beachhead is a sharper variant of an existing PER-
- **GTM-\* positioning** (from v0.9 Positioning) — Best-fit segment is the *starting point* for beachhead selection; beachhead is usually tighter
- **GTM-\* offer card** (from v0.9 Offer Construction) — Offer must match beachhead expectations (pragmatists need different guarantees than visionaries)
- **FEA-\* features** (from v0.3) — Whole-product gap analysis cross-references current feature set
- **KPI-\* baseline metrics** (from v0.3 + v0.9) — Stage assessment uses retention shape, NPS by segment, conversion rate
- **BR-PRICING-\*** (from v0.3 + v0.9) — Pragmatist buyers expect different pricing/contract terms than visionaries

## Produces

- **ADO-STAGE-\* entries** in `SoT/SoT.ADOPTION.md` — Current adoption-stage assessment with evidence
- **ADO-BEACHHEAD-\* entries** — Beachhead segment definition with strict in/not-in criteria
- **ADO-WHOLE-\* entries** — Whole-product gaps (one per gap, with owner and close date)
- **ADO-REF-\* entries** — Reference-account targets (one per candidate, with consent + placement status)
- **CFD-\* gaps surfaced** — When stage evidence is thin or beachhead selection lacks data, log as research gaps

## Execution

### Step 1: Assess current adoption stage

Audit current paying-customer composition. For each customer, classify by stage indicators:

| Indicator | Innovator/Early Adopter | Early Majority |
|-----------|------------------------|-----------------|
| Sales motion | Direct founder relationship | Asked for demo / pricing / case studies |
| Setup tolerance | "I'll figure it out" | "Show me the integration with X" |
| Reference need | None | Asked "who else in my industry uses this?" |
| Renewal motivation | "We're betting on this" | "It saves us $X/month" |
| Procurement | Single buyer | Procurement / SOC2 / contracts review |

Stage signal:
- **Innovators / Early Adopters**: >70% of paid customers show visionary indicators
- **At the chasm**: Mixed composition; new inbound asking pragmatist questions ("references", "integrations", "SOC2"); flat MRR despite growing leads
- **Bowling Alley** (post-chasm): >50% of new customers in one identifiable segment
- **Tornado**: Rapid acquisition across multiple segments
- **Main Street**: Stable growth, focus on expansion and retention

**Deliverable**: One ADO-STAGE-* entry with evidence, stage classification, and confidence score.

### Step 2: Pick the beachhead segment [standard+]

Generate 3–5 candidate beachhead segments. Score each:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **Pragmatist density** | Is this segment mostly pragmatists (already buying mature solutions)? | High |
| **Whole-product proximity** | How close is our current product to the segment's whole-product expectation? | High |
| **Reference accessibility** | Can we get 3 references in this segment within 6 months? | High |
| **Compelling reason to buy** | Is there an urgent, segment-specific pain we solve uniquely? | High |
| **Adjacency value** | If we win this segment, what adjacent segments unlock? | Medium |
| **Competitive intensity** | How saturated is this segment with established competitors? | Medium |
| **Market size** | Is this segment large enough to support a beachhead? | Low (most beachheads are small; that's fine) |

Pick the top-scoring segment. Write strict **in-segment** and **not in-segment** criteria.

**Deliverable**: One ADO-BEACHHEAD-* entry with in/not-in criteria, rationale, target (e.g., "10 closed-won in segment within 6 months"), confidence.

### Step 3: Whole-product gap analysis

For the beachhead segment, list everything a pragmatist buyer in that segment expects to receive when they pay you:

- Core product (what you ship)
- Integrations (with their existing stack — specific)
- Compliance (SOC2, HIPAA, ISO — segment-specific)
- Support (response-time SLA, dedicated CSM if appropriate)
- Training / onboarding (videos, docs, certifications)
- References (segment-specific, named, willing to talk)
- Pricing / contract terms (annual contracts, MSAs, custom DPAs)
- Migration / data import
- Professional services (implementation help)
- Roadmap visibility

For each, score: **Ship today? / Gap?**

For each gap, create an ADO-WHOLE-* entry with severity (blocker / serious / nice-to-have), owner, target close date.

**Deliverable**: List of ADO-WHOLE-* entries. Blockers must close before sustained beachhead motion.

### Step 4: Reference-account cultivation plan [standard+]

Identify 5–10 existing or near-term customers in the beachhead segment that could become public references. For each:

| Field | Notes |
|-------|-------|
| Customer | Name + segment fit confirmation |
| Story strength | What outcome can they speak to publicly? (Quantified > qualitative) |
| Relationship | Who owns the relationship internally? |
| Consent path | What approval do they need internally to be public? |
| Target placement | Logo on pricing page / quote on landing / blog case study / on-stage / podcast |
| Confidence | 1–5 of "will become a reference within 90 days" |

**Deliverable**: 5–10 ADO-REF-* entries with cultivation plan.

### Step 5: Chasm-crossing risk register [deep only]

For each major chasm risk, log a RISK-* entry:

- **Reference-cold risk** — Can't get 3 references in beachhead within 6 months
- **Whole-product gap risk** — Critical gap can't be closed in time
- **Beachhead-too-small risk** — Segment doesn't sustain the company economically even if won
- **Competitor-incumbency risk** — Pragmatist defaults are competitor X; switching cost too high
- **Internal motion risk** — Sales / support / product can't pivot from visionary motion to pragmatist motion

Each risk gets mitigation actions tied to ADO-WHOLE-*, ADO-REF-*, or BR-* updates.

**Deliverable** (deep): Risk register with mitigations.

## Output Templates

See [`SoT/SoT.ADOPTION.md`](../../../SoT/SoT.ADOPTION.md) for the complete entry templates for ADO-STAGE-, ADO-BEACHHEAD-, ADO-WHOLE-, and ADO-REF-.

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **"We're in the chasm" without evidence** | Stage assessment based on vibes | Audit actual paying-customer composition; require ADO-STAGE-* confidence ≥ 3/5 |
| **Beachhead too broad** | "Small businesses" or "B2B SaaS" | Tighten until it disqualifies most buyers; segment of 100–10,000 prospects max |
| **Skipping whole-product gap** | "Our product is great; we just need more marketing" | Pragmatists buy whole product, not core product; list every gap |
| **Reference from wrong segment** | Touting a visionary customer to a pragmatist buyer | In-segment references only; cross-segment is worthless |
| **Crossing the chasm broadly** | "Let's just scale paid ads" | Concentrate on beachhead; broad CAC will be 5× higher and worse-converting |
| **Confusing best-fit with beachhead** | Treating Dunford best-fit as the beachhead | Beachhead is *tighter* than best-fit; usually one sub-segment of the best-fit |
| **Skipping stage assessment** | Jumping to "we need to scale" without checking where we are | Step 1 is mandatory; without it, the rest is guesswork |

## Quality Gates

Before proceeding to other v1.0 work:

- [ ] ADO-STAGE-* entry exists with evidence and confidence ≥ 3/5
- [ ] If stage is "at the chasm" or beyond: ADO-BEACHHEAD-* defined with strict in/not-in criteria
- [ ] At least 3 ADO-WHOLE-* gap entries identified (blockers + serious)
- [ ] At least 3 ADO-REF-* candidate accounts (standard+)
- [ ] RISK-* entries cover the top chasm risks (deep only)
- [ ] Beachhead does not contradict v0.9 Positioning's best-fit (or contradiction is explicit and rationalized)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Continuous Discovery (Torres)** | Beachhead segment = discovery interview pool | Weekly interviews drawn from ADO-BEACHHEAD- |
| **Mom Test Interview** | Beachhead-segment interview discipline | Validate ADO-STAGE- and ADO-WHOLE- via Mom Test |
| **Case Study Builder** | Reference candidates = case study targets | ADO-REF-* graduates to case study |
| **Testimonial Collector** | Reference candidates = testimonial targets | ADO-REF-* (lower-effort placement) |
| **v0.9 Re-runs** | Beachhead may sharpen Positioning; whole-product gaps may shift Offer | Re-run Dunford with sharper segment |
| **Feedback Loop Setup** | Pragmatist-shaped feedback signals chasm crossing | Inbound pattern shift → re-run stage assessment |

## Detailed References

- Geoffrey Moore, *Crossing the Chasm* (1991, revised 2014) — canonical source
- Geoffrey Moore, *Inside the Tornado* (1995) — post-chasm bowling alley / tornado / main street
- Eric Ries, *The Lean Startup* (incompatible motion before chasm; useful contrast)
- wondelai's `crossing-the-chasm` skill (wondelai/skills)
- (No bundled `references/` — read the book for depth)
