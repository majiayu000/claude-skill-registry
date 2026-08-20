---
name: prd-v09-positioning-dunford
description: >
  Define product positioning using April Dunford's 5-step framework during PRD v0.9 Go-to-Market.
  Triggers on requests to position the product, define category, frame against competitors,
  or when user asks "what category are we?", "how do we position?", "Dunford positioning",
  "obviously awesome", "market frame of reference", "positioning statement".
  Outputs GTM-* entries with Type=Positioning and BR-POS-* positioning rules.
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

# Positioning (Dunford 5-Step)

Position in workflow: v0.8 Monitoring Setup → **v0.9 Positioning (Dunford)** → v0.9 Offer Construction (Hormozi) → v0.9 Launch Channels (ORB)

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One positioning statement; one best-fit segment; one category claim |
| **standard** | Full 5 steps; one segment + ≥3 alternatives + 3–5 attributes mapped to value; category claim with frame of reference |
| **deep** | Multiple segment variants; A/B positioning candidates to test; competitor positioning teardown; "best-fit" disqualification rules |

## Framework: Dunford's 5 Steps

From *Obviously Awesome: How to Nail Product Positioning* (April Dunford, 2019). Positioning is **the act of deliberately defining how you are the best at something a defined market cares a lot about** — not a feature list, not a tagline, not your founder's story.

The five steps run in order:

1. **Competitive alternatives** — What would your customers use if you did not exist? (Status-quo wins as often as competitor products do.)
2. **Unique attributes** — What capabilities or qualities do *you* have that those alternatives don't?
3. **Value (and proof)** — Translate each attribute into the value it delivers to a customer. Anchor in evidence, not aspiration.
4. **Customers who care a lot** — Among all possible buyers, which segment cares *most* about that value? This is your "best-fit" target.
5. **Market category** — Pick the category (the **frame of reference**) that puts your unique strengths at the center and is intelligible to your best-fit customer.

A 6th step (**relevant trends**) is optional and used only when a current market trend reinforces the positioning. Skip it in quick mode.

The work product is a **positioning statement** plus a small set of **positioning rules** that downstream skills (Offer Construction, Launch Channels, GTM messaging) must honor.

## Consumes

- **CFD-\* competitive alternatives** (from v0.2 Competitive Landscape Mapping) — Anchors step 1; without real alternatives, positioning is hypothetical
- **CFD-\* customer interviews** (from v0.1 + v0.4) — Source for "who cares a lot" in step 4; the strongest evidence for value claims in step 3
- **BR-\* product type** (from v0.2 Product Type Classification) — Clone/Unbundle/Undercut/Slice/Wrapper/Innovation shapes the kind of category claim that's credible
- **FEA-\* feature list** (from v0.3 Feature Value Planning) — Source for step 2 (unique attributes); attribute claims must trace to shipping features
- **PER-\* personas** (from v0.4 Persona Definition) — Step 4 best-fit segment is one of these PER- entries, sharpened

This skill assumes v0.2 (competitive landscape, product type) and v0.4 (personas) are complete.

## Produces

- **GTM-\* entries with Type=Positioning** — The positioning statement, the category claim, and the frame of reference. Each downstream messaging GTM- must trace to one of these.
- **BR-POS-\* positioning rules** — Constraint-style rules: *who we are*, *who we are not*, *what category we live in*. These become guardrails for v0.9 Offer Construction, Launch Channels, and v1.0 adoption work.
- **CFD-\* updates** — When step 3 reveals value claims are weakly evidenced, surface them as research gaps with confidence ≤ 2/5.

Confidence guidance per P4: a positioning statement should reach **3/5** before downstream skills consume it (i.e., grounded in actual customer interviews, not internal opinion). Quick mode may produce 2/5 outputs but must tag them.

## Execution

Run the five steps in order. Each step has a single deliverable.

### Step 1: List competitive alternatives

Inventory CFD- entries that name alternatives. Include the status quo ("spreadsheet + email"), not just competitor products. Cluster into 2–4 alternative categories.

**Deliverable**: A ranked list of competitive alternatives with rough usage volume estimates.

### Step 2: Identify unique attributes [standard+]

For each FEA- you ship, ask: "Does this alternative have it? At this quality?" Keep only attributes that are demonstrably *yours*. Quick mode picks the top 3.

**Deliverable**: 3–5 attributes that are uniquely yours vs. the alternatives.

### Step 3: Translate attributes to value

For each attribute, write the value it creates *for the customer*. Anchor in CFD- evidence (interview quotes, beta data, usage metrics). Mark each value claim with a confidence score.

**Deliverable**: An attribute → value table with evidence and confidence per row.

### Step 4: Identify customers who care a lot

Cross-reference the value claims against your PER- personas. Which persona's pains are *most* addressed by your unique values? That is your best-fit segment. Write a "best-fit characteristics" list (firmographics, behaviors, triggers).

**Deliverable**: One sharpened best-fit PER- variant with "ideal customer" characteristics.

### Step 5: Pick a market category

Choose the **frame of reference** — the category that puts your strengths at the center and is meaningful to your best-fit customer. Test against three checks:
- Does it make the value claims feel inevitable?
- Does it disqualify alternatives that aren't a good fit?
- Would your best-fit customer recognize the category name?

**Deliverable**: One category claim ("we are the X for Y who need Z") and a one-paragraph positioning statement.

### Step 6: Trends [deep only]

If a current market trend reinforces the positioning (e.g., "AI-native", "compliance-first"), name it. Otherwise skip — trends without product fit are noise.

**Deliverable** (deep mode): One sentence connecting the positioning to a current trend, with citation.

## Output Template

```
GTM-XXX: Positioning Statement
Type: Positioning
Owner: Founder / Product Marketing
Status: Ready

Best-fit segment: PER-XXX (sharpened — see characteristics below)
Category: [the frame of reference, e.g., "Conversion-rate optimization platform"]
Statement:
  For [best-fit customer]
  Who [trigger / pain]
  [Product name] is the [category]
  That [unique value]
  Unlike [primary alternative], we [unique attribute → value].

Best-fit characteristics:
  - [Firmographic 1]
  - [Behavior 1]
  - [Trigger 1]

Competitive alternatives considered: CFD-001, CFD-002, CFD-003
Unique attributes: FEA-001, FEA-005, FEA-008
Value claims (with evidence):
  - [Attribute] → [Value] (CFD-XXX, confidence: X/5)

Linked IDs: PER-XXX (best-fit), CFD-XXX (alternatives + interviews), FEA-XXX (attributes), BR-POS-XXX (rules)
```

```
BR-POS-XXX: Positioning Rule
Type: Constraint
Status: Active

Rule: [What this rule says, e.g., "We do not market to enterprise procurement teams"]
Rationale: [Why — usually traces to the best-fit segment OR a positioning attribute]
Enforced by:
  - GTM-* messaging skills (no enterprise language)
  - Offer Construction (no procurement-friendly contract terms)
  - Launch Channels (no Gartner/analyst channels in launch wave)
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Feature-list positioning** | "We have X, Y, Z" | Translate each to value (step 3); cut what doesn't translate |
| **Aspirational alternatives** | Only listing competitors as alternatives | Include status quo and non-purchase ("spreadsheet + manual") |
| **Best-fit = everyone** | "We're for SMBs and enterprise and individual users" | Pick one; the others become "not for us" |
| **Category claim too broad** | "We're the platform for X" (where X is huge) | Tighten the frame of reference until it disqualifies bad-fit buyers |
| **No evidence in step 3** | Value claims with confidence 1/5 across the board | Stop and run more interviews before launching |
| **Skipping step 1** | "Our positioning is..." without alternatives discussion | Step 1 is mandatory — positioning without alternatives is internal monologue |

## Quality Gates

Before proceeding to Offer Construction:

- [ ] All 5 steps have a deliverable (Step 6 optional, deep only)
- [ ] Best-fit segment is one sharpened PER- (not 3 personas)
- [ ] At least 3 competitive alternatives listed (including status quo)
- [ ] At least 3 unique attributes, each with a value translation
- [ ] Each value claim has CFD- evidence and confidence ≥ 2/5 (standard) or ≥ 3/5 (deep)
- [ ] One positioning statement and one category claim, both ≤ 3 sentences
- [ ] At least one BR-POS-* rule encoded (a "we do not" constraint)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Offer Construction (Hormozi)** | Best-fit segment + value claims | Hormozi's value equation anchors on the value claims here |
| **Launch Channels (ORB)** | Best-fit characteristics + category claim | Channel selection must reach the sharpened best-fit segment |
| **Launch Metrics** | Positioning statement = KPI- attribution baseline | "Did messaging at category X drive signups?" |
| **v1.0 Crossing the Chasm (Moore)** | Best-fit segment = beachhead anchor | Moore's "bowling-alley beachhead" = Dunford's best-fit |

## Detailed References

- April Dunford, *Obviously Awesome: How to Nail Product Positioning* (2019) — canonical source
- Dunford's blog: [aprildunford.com/positioning](https://aprildunford.com)
- (No bundled `references/` — read the book for depth)
