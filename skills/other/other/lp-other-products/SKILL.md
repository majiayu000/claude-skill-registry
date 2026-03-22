---
name: lp-other-products
description: Produce a deep research prompt for adjacent product range exploration. Reads the target business's startup loop docs (offer, ICP, market intel, brand dossier) and outputs a structured deep-research-ready prompt covering customer JTBD, manufacturer accessory landscape, product candidate set with one-page cards, prioritisation rubric, 90-day MVP plan, and bundling strategy.
---

# Adjacent Product Research Prompt Generator

Produces a structured deep-research brief for evaluating what products to build next alongside the current hero product. Not a brainstorm list — a research framework with evidence requirements, scoring rubric, and MVP roadmap instruction baked in.

## When to use

Use after lp-offer (MARKET-06) completes, when the operator intends product range expansion or when GATE-PRODUCT-02-01 fires. Requires offer.user.md to exist for the target business (ICP and pain/promise map are essential inputs that naming research does not need but this skill does). Also operator-invocable at any time after offer exists.

## Operating mode

**RESEARCH BRIEF AUTHORING ONLY**

**Allowed:** read startup loop docs, synthesize context, produce research prompt artifact.

**Not allowed:** generate product concepts, make sourcing or pricing decisions, implement any changes.

## Required inputs (pre-flight)

Before writing the prompt, read and synthesize from the business's loop docs:

- `docs/business-os/startup-baselines/<BIZ>/<YYYY-MM-DD>-assessment-intake-packet.user.md` — ICP, product, region, price range, growth intent
- `docs/business-os/market-research/<BIZ>/latest.user.md` — competitor landscape, pricing benchmarks, manufacturer accessory catalogues
- `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` — emotional territory, anti-criteria, community sensitivity framing
- `docs/business-os/startup-baselines/<BIZ>/offer.md` OR `docs/business-os/strategy/<BIZ>/offer.user.md` — ICP segmentation, pain/promise map, objection map, positioning (required; this skill cannot run without it)
- `docs/business-os/contracts/<BIZ>/outcome-contract.user.md` — 90-day targets and contract window (to anchor MVP roadmap dates)

If the offer artifact is missing, halt and instruct the operator to complete lp-offer (MARKET-06) first.

If any other file is missing, note the gap in the output but proceed with available context.

## Output

Two artifacts:

**Prompt (produced by this skill):**
```
docs/business-os/strategy/<BIZ>/lp-other-products-prompt.md
```

**Results (produced by human after running in a deep research tool):**
```
docs/business-os/strategy/<BIZ>/lp-other-products-results.user.md
```
Note the results path in the completion message. The human saves the tool's output there. lp-prioritize (post-S4) picks up product candidates from Track 4's top-5 shortlist as additional go-items when that file is present.

## Prompt structure (mandatory sections)

The generated prompt must contain all of the following sections in this order:

### 1. Researcher role and output rules

Instruct the researcher to:
- Produce a structured product range strategy document, not a generic brainstorm
- Use web research and cite sources for all factual statements (competitor offerings, manufacturer catalogues, price points, materials, regulatory definitions)
- Separate clearly: (a) what was checked (with source + date), (b) what was inferred, (c) what remains unknown without supplier quotes, lab testing, or legal counsel
- Make no medical efficacy claims; propose no products whose core promise is to improve hearing outcomes

### 2. Date, locale, and currency

Encode from intake packet:
- Today's date (Europe/Rome timezone for EU-primary businesses)
- Launch market (primary and expansion)
- Currency focus (EUR primary, USD note if relevant)

### 3. Business context

Cover at minimum:
- Current hero product (physical description, function, what it does for the user)
- Positioning statement (lifestyle accessory vs medical device; no medical device claims)
- Primary customer (ICP, from offer artifact — include JTBD and buying trigger)
- Secondary customers
- Current price range and core tier
- **Emotional territory** — encode the 5 brand personality descriptors from brand dossier
- Market sizing — **label as verify-and-cite**; instruct researcher to verify figures and cite with dates

### 4. Regulatory and claim-drift guardrails

This section is mandatory for health-adjacent products. Encode:
- Cite EU MDR definitions of "intended purpose" and "accessory for a medical device" — instruct researcher to cite the relevant MDR passages, not just describe them by feel
- Require a **claim drift risk rating** (low / medium / high with rationale) for every adjacent product category proposed
- Permitted benefit language: comfort, secure wear, reduced drops/loss, everyday usability, convenience, organisation, personalisation
- Prohibited framing: restore hearing, improve hearing, therapy, treatment, necessary for the device to function

### 5. Scope definition

Define what "adjacent" means for this brand:
- Products used with or around the external processor / wearing routine / daily life of users and families
- Expand basket size and repeat purchases (sizes, colours, seasonal drops, replacements, add-ons)
- Feasible as a small DTC brand (manufacturing, compliance, shipping, returns)
- Extensible into a coherent range architecture (not one-off oddities)

### 6. Research tracks

Always include all six tracks:

**Track 1 — Customer JTBD and moments map (evidence-led):**
Map the user journey across: morning routine / school / play / sport; sleep / bedtime; travel / beach / rain / sweat; storage, organisation, cleaning, "where did it go?" Identify the top 10 recurring problems that adjacent products could solve. Require citations from community discussions, manufacturer guidance, or reputable resources.

**Track 2 — Competitor and manufacturer accessory landscape:**
Build a structured map with two separate classes: (A) independent accessory brands, (B) manufacturer official accessory catalogues (fixation, clips, covers, cases, drying/cleaning, sports solutions). For each: product types, naming/positioning style (functional vs lifestyle), typical price bands (cited), notable gaps. Cite primary sources.

**Track 3 — Adjacent product candidate set (range blueprint):**
Generate 12–20 product concepts grouped into a range architecture (e.g. core extensions, add-ons, retention ecosystem, storage/organisation, care/maintenance, parent convenience). For each concept, require a one-page card with these 11 fields:
1. What it is (plain description)
2. Primary customer + use moment
3. Value proposition (non-medical framing)
4. Expected ASP range (EUR) with citations
5. Suggested materials / form factor and why
6. Size/fit complexity (low/med/high)
7. Manufacturing complexity (low/med/high)
8. Returns risk (low/med/high)
9. Compliance/claim-drift risk (low/med/high) with rationale
10. Competitive references (who sells something similar; cite)
11. Range role (entry add-on / premium / replenishment / bundle anchor)

**Track 4 — Prioritisation and MVP roadmap:**
Require a scoring rubric with explicit weights, e.g.:
- Customer impact (30%)
- Differentiation / whitespace (20%)
- Manufacturability + supply chain simplicity (20%)
- Margin potential at target ASP (15%)
- Claim-drift / compliance risk (15%; inverted — higher risk = lower score)

Output:
- Top 5 adjacent products to explore next (with rubric scores)
- Top 3 to build first with a 90-day MVP plan: prototyping approach, sampling, minimum viable variants (SKUs), basic QA, photography needs, launch bundle strategy
- 12-month range roadmap: how the catalogue expands without becoming incoherent

**Track 5 — Bundling, pricing, and merchandising strategy:**
Propose: bundle archetypes (starter kit, school kit, sport kit, sleep kit, travel kit); cross-sell logic on PDP and cart; replenishment / replacement triggers (growth, lost items, wear-and-tear). Keep price points consistent with the base product range.

**Track 6 — Brand and community sensitivity check:**
For each adjacent category, flag: concealment framing risk (avoid); disability-identity misstep risk (flag if not validated); language guidelines with copy do/don't examples.

### 7. Deliverables format

Require the researcher to produce a research document (en-GB) with:
1. Executive summary — range thesis and top opportunities
2. JTBD map — top 10 problems with evidence
3. Competitive and manufacturer accessory landscape — structured table with citations
4. Range blueprint — 12–20 product cards grouped by range role
5. Prioritised shortlist — scoring table with weights shown
6. 90-day MVP plan — top 3 products
7. 12-month range roadmap and bundling strategy
8. Risk register — claim-drift/compliance risks and operational risks

### 8. Reminders

Always end the prompt with:
- No medical claims; avoid implying improved hearing
- Cite everything factual
- Clearly separate checked vs inferred vs unknown
- Use Italy-first lens (language accessibility, pricing expectations, channels)

## Quality gate

- [ ] Offer artifact read and ICP/pain-map encoded in business context section
- [ ] EU MDR claim-drift guardrails encoded with low/medium/high rating instruction per product category
- [ ] JTBD map across all 6 user moments requested (Track 1)
- [ ] Manufacturer official accessory catalogues listed as a separate comparator class from independent brands (Track 2)
- [ ] Product card format with all 11 fields specified (Track 3)
- [ ] Scoring rubric with percentage weights present in prioritisation (Track 4)
- [ ] 90-day MVP plan and 12-month range roadmap explicitly requested (Track 4)
- [ ] Bundle archetypes and replenishment triggers requested (Track 5)
- [ ] Community sensitivity check covering both concealment risk and disability-identity risk (Track 6)
- [ ] Checked/inferred/unknown separation required throughout
- [ ] Market sizing flagged as verify-and-cite

## Completion message

> "Product range research prompt ready: `docs/business-os/strategy/<BIZ>/lp-other-products-prompt.md`. Drop into a deep research tool (OpenAI Deep Research or equivalent). When results are returned, save to `docs/business-os/strategy/<BIZ>/lp-other-products-results.user.md` — lp-prioritize (post-S4) will pick up product candidates from Track 4's top-5 shortlist as additional go-items when that file is present."
