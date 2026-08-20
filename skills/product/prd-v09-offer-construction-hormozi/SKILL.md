---
name: prd-v09-offer-construction-hormozi
description: >
  Construct a high-conversion offer using Alex Hormozi's value equation and Grand Slam Offer
  mechanics during PRD v0.9 Go-to-Market. Triggers on requests to design the offer, set up the
  pitch, build bonuses or guarantees, or when user asks "how do we package this?", "what's the
  offer?", "build a grand slam offer", "Hormozi", "$100M offers", "guarantee", "bonus stack".
  Outputs GTM-* entries with Type=Offer / Type=Guarantee and BR-PRICING-* updates.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Offer Construction (Hormozi $100M Offers)

Position in workflow: v0.9 Positioning (Dunford) → **v0.9 Offer Construction (Hormozi)** → v0.9 Launch Channels (ORB)

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One offer; 1–2 named bonuses; one simple guarantee; price anchor |
| **standard** | Full value equation calibrated; 3–5 bonuses with anchored values; one named guarantee; scarcity / urgency rule |
| **deep** | Multi-tier offers (entry / mid / premium); guarantee experimentation plan; price anchor A/B; bonus value validation plan |

## Framework: Value Equation and Grand Slam Offer

From *$100M Offers: How To Make Offers So Good People Feel Stupid Saying No* (Alex Hormozi, 2021). An offer is the **complete commercial proposition** — what they get, what it costs, what's guaranteed, what's bundled, what's urgent — not just the product or the price.

### The Value Equation

Perceived Value = **(Dream Outcome × Perceived Likelihood of Achievement)** / **(Time Delay × Effort & Sacrifice)**

Four levers — increase the numerator, decrease the denominator:

1. **Dream Outcome** — What does the customer actually want? Express in their words. (Higher = better.)
2. **Perceived Likelihood of Achievement** — How sure are they it will work? (Higher = better. Anchored by guarantees, social proof, case studies.)
3. **Time Delay** — How long until they get the outcome? (Lower = better.)
4. **Effort & Sacrifice** — How much work do they have to do? (Lower = better.)

If perceived value < price, the offer fails regardless of product quality.

### Grand Slam Offer Components

A complete offer stacks five things:

1. **Core promise** — the headline outcome (anchored in the value equation)
2. **Bonus stack** — additional named items, each with anchored monetary value, that increase perceived value without proportionally increasing cost-to-deliver
3. **Guarantee** — one of: unconditional refund, conditional ("if X doesn't happen, we Y"), anti-guarantee ("we don't refund — here's why we're so confident"), implied (case studies, results), or service-level
4. **Scarcity** — limited supply (real: capacity, beta seats, custom service slots)
5. **Urgency** — limited time (real: cohort start, price increase, bonus expiration)

Scarcity and urgency must be **real**. Manufactured scarcity erodes trust and is incompatible with Dunford's positioning ([prd-v09-positioning-dunford](../prd-v09-positioning-dunford/SKILL.md)).

## Consumes

- **GTM-\* positioning statement** (from v0.9 Positioning) — Dream Outcome and Likelihood of Achievement language comes from the positioning's value claims; the offer cannot promise more than the positioning supports
- **BR-\* pricing model** (from v0.3 Pricing Model) — Existing price tiers; offer can stack on top but should not silently change the model
- **FEA-\* features** (from v0.3 Feature Value Planning) — Bonuses must be real product features or real services, not vapor
- **CFD-\* value evidence** (from v0.1–v0.4) — "Dream Outcome" wording comes from customer interviews; "Likelihood of Achievement" anchors come from case studies and usage data
- **PER-\* best-fit segment** (sharpened by Positioning) — Determines what "Dream Outcome" actually means to this buyer

This skill assumes Positioning is complete (positioning statement at confidence ≥ 3/5) and v0.3 Pricing Model is set.

## Produces

- **GTM-\* with Type=Offer** — The full offer card: core promise, bonus stack with anchored values, guarantee reference, scarcity/urgency rule, price anchor
- **GTM-\* with Type=Guarantee** (separate ID) — The guarantee in standalone form so messaging can reference it directly
- **BR-PRICING-\* updates** — If the offer changes the pricing model (e.g., adds a one-time payment option, changes refund policy), update the BR- entries
- **CFD-\* gaps surfaced** — If the offer's Likelihood-of-Achievement claims can't be substantiated, log a CFD- research gap

## Execution

### Step 1: Calibrate the Value Equation

Write down each lever in the customer's words. Score each on a 1–5 scale:

| Lever | Current | Target | Gap |
|-------|---------|--------|-----|
| Dream Outcome | | | |
| Likelihood of Achievement | | | |
| Time Delay | | | |
| Effort & Sacrifice | | | |

The largest gap = the lever to attack first.

### Step 2: Design the core promise

State the headline outcome in one sentence: *"You will [Dream Outcome] in [Time Delay] without [Effort & Sacrifice]."* Test the sentence against the positioning statement — if they conflict, fix the offer, not the positioning.

### Step 3: Build the bonus stack [standard+]

Aim for 3–5 bonuses. For each:
- Name it concretely (not "additional support" — "1:1 setup call with founder, 30 min")
- Assign an anchored value (what would this cost separately?)
- Confirm it's deliverable at near-zero marginal cost (or factor cost into pricing)

Total stacked value should be ≥ 3× the price. If it isn't, the offer's perceived value is too low.

### Step 4: Choose a guarantee

Pick the strongest guarantee you can deliver:

| Guarantee Type | When to Use | Risk |
|----------------|-------------|------|
| Unconditional refund | Confident in product; low-touch sale | Refund-fraud exposure |
| Conditional ("if X doesn't happen, we Y") | Specific outcome promised | Requires clear measurement |
| Anti-guarantee | Premium / high-status positioning | Loses risk-averse buyers |
| Implied (case studies) | Long sales cycle, B2B | Slower trust-building |
| Service-level | Ongoing relationship | Operational commitment |

Write the guarantee in the customer's words. If you cannot stand behind it, choose a weaker one or fix the product.

### Step 5: Add scarcity and urgency [standard+]

| Type | Examples |
|------|----------|
| **Scarcity (supply)** | Beta seats (real cap), capacity-limited service tier, founding-member pricing |
| **Urgency (time)** | Cohort start date, price increase scheduled, bonus expiration |

Both must be real. Document the *mechanism* — what triggers the cap or deadline — in the GTM- entry. If you can't document the mechanism, drop the claim.

### Step 6: Anchor the price [deep only]

Present the offer in this order: **Dream Outcome → Stack value → Guarantee → Scarcity → Price**. The price should feel inevitable given everything before it.

If running multiple offer tiers in deep mode, design the middle tier as the anchor (most buyers pick the option positioned next to the highest-priced option they almost-picked).

## Output Template

```
GTM-XXX: Offer Card
Type: Offer
Owner: Founder / Sales
Status: Ready

Core promise: [One-sentence headline outcome]
Best-fit segment: PER-XXX
Linked positioning: GTM-YYY (Positioning Statement)

Value equation:
  Dream Outcome: [In customer words]
  Likelihood of Achievement: [What anchors this — case studies, guarantees]
  Time Delay: [Target]
  Effort & Sacrifice: [Target]

Bonus stack:
  1. [Bonus name] — anchored value: $X (real cost: ~$Y) — FEA-ZZZ or service
  2. [Bonus name] — ...
  3. ...

Total stacked value: $X (vs. price $Y — ratio ≥ 3:1)

Guarantee: GTM-ZZZ (separate entry)

Scarcity: [Real mechanism — beta cap, capacity limit, etc.]
Urgency: [Real deadline — cohort start, price change, etc.]

Price: $X (anchored against stacked value)
Payment terms: [One-time / monthly / annual / split]

Linked IDs: PER-XXX, GTM-YYY (positioning), FEA-ZZZ (bonus features), BR-PRICING-AAA, CFD-BBB (value evidence)
```

```
GTM-XXX: Guarantee
Type: Guarantee
Owner: Founder / Legal
Status: Approved

Guarantee type: [Unconditional refund | Conditional | Anti-guarantee | Implied | Service-level]
Stated in customer words: "[The exact wording]"
Eligibility: [Who, when, how]
Measurement: [How "did it work?" is determined]
Failure procedure: [What happens if invoked — refund process, etc.]

Linked IDs: GTM-YYY (Offer Card), BR-PRICING-ZZZ (if affects pricing model)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Manufactured scarcity** | "Only 7 spots left" reset every week | Drop the claim or make the cap real (e.g., one cohort per quarter) |
| **Vapor bonuses** | Bonus = "lifetime access" to a thing that costs you nothing | Replace with something that has anchored value, even if cheap to deliver |
| **Promise mismatch** | Offer promises more than positioning supports | Fix the offer down; do not quietly upgrade positioning |
| **Guarantee you can't honor** | "100% refund anytime" with 60% refund-fraud rate | Pick a stronger conditional guarantee instead |
| **Stack ratio < 2:1** | Stacked value barely beats price | Either add more bonuses or drop the price; thin stacks don't convert |
| **No best-fit segment** | Offer designed for "everyone" | Pull the PER- from positioning and design for them |

## Quality Gates

Before proceeding to Launch Channels:

- [ ] Value equation calibrated with current vs. target per lever
- [ ] Core promise written in one sentence
- [ ] Stack value ≥ 3× price (standard+); ≥ 2× (quick)
- [ ] Guarantee chosen and writable in customer's words
- [ ] Scarcity and urgency mechanisms are real and documented
- [ ] Offer does not contradict positioning statement
- [ ] All bonuses trace to real FEA- or service deliverables

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Offer card = the unit being distributed | Owned-channel emails sell the offer, not the product |
| **Launch Metrics** | Offer becomes KPI- conversion target | KPI: offer page → purchase rate |
| **Cold Outreach (Tactical)** | Tier 1/2/3 cold sequences end on the guarantee | Guarantee = reply-friction killer |
| **v1.0 Crossing the Chasm (Moore)** | Offer shifts as adoption stage shifts | Early-adopter offer ≠ early-majority offer |

## Detailed References

- Alex Hormozi, *$100M Offers* (2021) — canonical source
- Acquisition.com offer-construction resources
- (No bundled `references/` — read the book for depth)
