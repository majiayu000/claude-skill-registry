---
name: prd-v10-continuous-discovery-torres
description: >
  Establish weekly customer-discovery cadence and Opportunity Solution Tree practice using Teresa
  Torres's Continuous Discovery Habits framework during PRD v1.0 Market Adoption. Triggers on
  requests to set up discovery cadence, build opportunity solution tree, run weekly customer
  interviews, or when user asks "Torres", "continuous discovery", "opportunity solution tree",
  "outcomes vs outputs", "weekly interviews", "assumption mapping". Outputs CFD-* discovery
  entries and updates to ADO-STAGE-* and PER-* with new evidence.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Continuous Discovery (Torres)

Position in workflow: v1.0 Crossing the Chasm (Moore) → **v1.0 Continuous Discovery (Torres)** → v1.0 Mom Test, Case Study Builder

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | One outcome + 3–5 opportunities + interview cadence proposal |
| **standard** | Full Opportunity Solution Tree (outcome → opportunities → solutions → assumption tests); weekly 3-interview cadence; assumption-mapping for top solution |
| **deep** | Multi-outcome tree; per-opportunity confidence scoring; full assumption tests with experiment plans; cross-discipline trio (PM/design/eng) participation rules |

## What This Does

Establishes **continuous discovery** as a weekly habit, not a one-time research phase. The shift from "we do research before building" to "we talk to customers every week" is what separates teams that find PMF from teams that drift.

The work product is the **Opportunity Solution Tree** — a structured artifact that connects a measurable business outcome to opportunities (customer needs), to candidate solutions, to assumption tests. The tree is *living*: it grows and prunes as interviews accumulate.

This skill assumes [prd-v10-mom-test-interview](../prd-v10-mom-test-interview/SKILL.md) is the discipline for *how* to interview; this skill is the discipline for *what to do with* the interviews.

## How It Works

1. **Define one measurable outcome** — Not an output ("ship feature X"), but an outcome ("activated users in beachhead segment grow 20% MoM"). Anchor in [ADO-STAGE-*](../prd-v10-chasm-adoption-moore/SKILL.md) and KPI-*.
2. **Set up weekly cadence** — 3+ customer interviews per week, ongoing. Not "until we feel done." Continuous.
3. **Map opportunities under the outcome** — Each opportunity is a customer pain or need (not a feature). Phrased in customer words. Grouped under the outcome. Sourced from interviews.
4. **Pick top opportunity** — Score by outcome-impact × evidence-strength × addressability. Focus on one at a time.
5. **Brainstorm solutions** — Multiple candidate solutions per opportunity. Not "the obvious one." Force divergent options.
6. **Assumption-map the top solution** — What must be true for this solution to work? Three categories: desirability (do they want it?), viability (will it grow our outcome?), feasibility (can we build it?).
7. **Test the riskiest assumption first** — Smallest experiment that disproves the assumption if it's wrong. Update tree.

## Example

**Outcome**: "Activated users in beachhead segment grow 20% MoM" (anchored in KPI-103 + ADO-BEACHHEAD-001).

**Opportunities** (from 8 weekly interviews):
- O1: "I don't know what to do first when I sign up" (4 mentions)
- O2: "Integration with [our stack tool] is missing" (3 mentions, all beachhead)
- O3: "Pricing is confusing — I don't know which tier I need" (5 mentions)
- O4: "I'd recommend it but I'm afraid teammates won't get the value" (2 mentions, low confidence)

Pick top: **O3** (highest mentions, blocks revenue conversion, addressable in product).

**Candidate solutions** (force divergence):
- S1: Simplify to 1 tier
- S2: Pricing wizard (3 questions → recommendation)
- S3: Annotated comparison page with "most popular" anchor
- S4: Self-serve trial extended to all features

**Top solution**: S2 (pricing wizard).

**Assumptions** for S2:
- D1 (desirability): Users will engage with a wizard before signing up
- D2: The wizard's recommendation will feel right (no "this isn't me")
- V1 (viability): Self-selected tier through wizard → fewer downgrades
- V2: Doesn't tank conversion overall
- F1 (feasibility): Engineering can ship 3-question wizard in 2 weeks

**Riskiest**: D1 — without engagement, nothing else matters.

**Test for D1**: Add wizard to /pricing for 50% of traffic. Measure engagement rate. Threshold: ≥30% engage = D1 valid. If <15%, drop S2.

## What You Get Back

- **Opportunity Solution Tree** in `temp/<epic>_discovery-tree.md` (or harvested to UJ-/CFD- when stable) — Living structured artifact
- **CFD-\* discovery insights** (one per interview) with confidence ≥ 3/5 per the Mom Test discipline
- **CFD-\* opportunity entries** with frequency + evidence + outcome-link
- **CFD-\* assumption-test results** as experiments run
- **PER-\* / ADO-STAGE-\* / ADO-BEACHHEAD-\* updates** when discovery accumulates contradicting evidence

## When to Use It

| Trigger | Mode |
|---------|------|
| Post-launch standard practice | standard (ongoing) |
| Pre-chasm crossing research push | deep |
| Investigating a specific stalled metric | quick (focused on one outcome) |
| New team member onboarding to discovery | standard (with mentorship) |
| Outcome target is unclear | **stop** — go fix the outcome definition first |

## Consumes

- **ADO-STAGE-\* and ADO-BEACHHEAD-\*** (from prd-v10-chasm-adoption-moore) — Defines the segment to interview
- **KPI-\* outcome targets** (from v0.3 + v0.9) — Anchors the outcome at the top of the tree
- **PER-\* personas** (from v0.4 + v0.9) — Interview pool definition
- **CFD-\* existing evidence** (all prior stages) — Inputs that need fresh validation in this stage
- **GTM-\* positioning** (from v0.9) — Discovery should reveal whether positioning lands with pragmatists

## Produces

- **Opportunity Solution Tree** in `temp/` while active, harvested to durable IDs at EPIC close
- **CFD-\* entries** with discovery interview content (confidence 3/5+ via Mom Test discipline)
- **Updates to**: PER-* (sharpened by interviews), ADO-STAGE-* (evidence accumulation), ADO-BEACHHEAD-* (refined criteria)
- **EPIC-\* recommendations** — When an opportunity becomes high-confidence + high-impact, it becomes an EPIC candidate

## Output Templates

### Opportunity Solution Tree (temp/ artifact)

```
# Opportunity Solution Tree — [Date / EPIC]

## Outcome
KPI-XXX: [measurable outcome statement]

Anchored in: ADO-STAGE-AAA (stage assessment), ADO-BEACHHEAD-BBB (segment)
Time-bound: [timeframe]

## Opportunities

### O1: [Customer pain in their words]
- Frequency: [N interviews mention this]
- Confidence: X/5
- Outcome-link: [How does solving this move the outcome?]
- CFD-* sources: CFD-XXX, CFD-YYY
- Status: [Active | Deprioritized | Solved]

  #### Solutions for O1

  - S1.1: [Candidate solution]
    - Outcome-impact: [Predicted lift]
    - Effort: [Rough scope]
    - Status: [Brainstormed | Assumption-mapped | Experimenting | Validated | Killed]

    ##### Assumptions for S1.1
    - D1 [desirability]: [Must be true about user wanting it]
    - V1 [viability]: [Must be true about business impact]
    - F1 [feasibility]: [Must be true about building it]

    Test plan for [riskiest assumption]:
    - Experiment: [Smallest test]
    - Success threshold: [Specific metric]
    - Failure path: [What we do if it fails]
    - Status: [Planned | Running | Result]
```

### CFD-* discovery entry

```
CFD-XXX: Discovery Interview — [interview title]
Type: Discovery-Interview
Date: YYYY-MM-DD
Interviewee segment: [PER-XXX] [in-beachhead: yes/no]
Interviewer: [Name]

Key story (specific past behavior, not opinion):
  [Mom Test-disciplined quote — what they DID, not what they THINK]

Pain mentioned: [One concrete pain in their words]
Workaround used: [What they currently do]
Feature requests (discounted): [What they asked for — note as IDEA, not data]

Confidence: [3/5 — qualitative single interview; 4/5 — pattern across cohort]
Linked outcomes / opportunities: [KPI-XXX, O1, O3]
Tree position: [Which opportunity this evidence supports]

Linked IDs: PER-XXX, ADO-BEACHHEAD-XXX, KPI-XXX
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Discovery as project, not habit** | "We did discovery in Q1" | Weekly cadence, ongoing. Tree is living. |
| **Outcome = output** | "Outcome: ship feature X" | Outputs are what you make; outcomes are what changes for the customer/business |
| **Skipping divergent solutions** | One solution per opportunity, no alternatives considered | Force ≥3 solution candidates per opportunity |
| **Solution-first thinking** | Brainstorming features before opportunities are mapped | Tree top-down: outcome → opportunities → solutions, not reverse |
| **Treating feature requests as opportunities** | "Add dark mode" treated as a customer need | That's a solution; the opportunity is the underlying job |
| **No assumption test before building** | "We'll just ship it and see" | At least one assumption test (smallest experiment) before significant engineering |
| **Solo discovery** | One PM doing all interviews; eng/design unaware | Continuous discovery is a *trio* practice (PM + design + eng); rotating attendance |

## Quality Gates

For ongoing discovery to count:

- [ ] 3+ customer interviews per week (standard cadence)
- [ ] Outcome (not output) at top of tree
- [ ] Opportunities phrased in customer words with frequency data
- [ ] One opportunity is "active" focus at a time
- [ ] Top solution has assumption map (D/V/F) before engineering work begins
- [ ] Riskiest assumption has a planned test
- [ ] CFD-* entries follow Mom Test discipline (confidence ≥ 3/5)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Mom Test Interview** | Interview discipline for the actual conversations | Every CFD-discovery entry follows Mom Test rules |
| **Case Study Builder** | High-engagement interviewees become case-study candidates | Strong CFD- → ADO-REF- → case study |
| **Chasm Adoption (Moore)** | Discovery evidence updates ADO-STAGE- and ADO-BEACHHEAD- | Pattern shifts trigger stage re-assessment |
| **EPIC-* planning** | Validated solutions become EPIC candidates | S2 wizard validated → EPIC-XX delivery |
| **Feedback Loop Setup** | Continuous discovery is the structured arm of feedback loop | Discovery = scheduled interview; feedback loop = inbound channels |

## Detailed References

- Teresa Torres, *Continuous Discovery Habits* (2021) — canonical source
- Teresa Torres, productchats.com (blog and tools)
- Marty Cagan, *Inspired* + *Empowered* (complementary product-leadership reading)
- wondelai's `continuous-discovery` skill (wondelai/skills)
- (No bundled `references/` — read the book for depth)
