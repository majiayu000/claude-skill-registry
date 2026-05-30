---
name: opportunity-solution-tree
description: "Build an Opportunity Solution Tree (OST) to structure product discovery — map a desired outcome to customer opportunities, possible solutions, and experiments. Based on Teresa Torres' Continuous Discovery Habits. Use when the team is unclear what to build next, when multiple opportunities compete, or before writing a PRD for a complex feature space."
when_to_use: |
  Apply when:
  - The team knows the outcome to improve but not which opportunity to chase
  - Multiple feature ideas exist and the team isn't sure which solves the right problem
  - CTO asks "what should we build to improve retention / conversion / NPS?"
  - Starting discovery on a new product area
  Guards — do NOT apply when:
  - The feature and problem are already well-defined (go straight to /prd)
  - You have a single, validated user story (use /prd directly)
  - This is a bug fix or technical debt item
effort: medium
allowed-tools: Read, Write, WebFetch, WebSearch
paths:
  - "docs/discovery/**"
---

# Opportunity Solution Tree (OST)

Structures product discovery by connecting a desired outcome → customer opportunities → solutions → experiments. Prevents jumping to solutions before validating the problem space.

Based on Teresa Torres, *Continuous Discovery Habits* (2021).

---

## The 4-level structure

```
                    ┌─────────────────────┐
                    │   DESIRED OUTCOME   │  ← single measurable metric
                    └──────────┬──────────┘
               ┌───────────────┼────────────────┐
        ┌──────┴─────┐  ┌──────┴─────┐  ┌──────┴─────┐
        │Opportunity │  │Opportunity │  │Opportunity │  ← customer pain/need
        │     A      │  │     B      │  │     C      │
        └──────┬─────┘  └──────┬─────┘  └────────────┘
        ┌──────┴───┐    ┌──────┴───┐
    ┌───┴──┐ ┌───┴──┐ ┌───┴──┐ ┌───┴──┐
    │Sol 1 │ │Sol 2 │ │Sol 3 │ │Sol 4 │  ← possible solutions
    └───┬──┘ └──────┘ └───┬──┘ └──────┘
  ┌────┴────┐         ┌───┴────┐
  │ Exp 1   │         │ Exp 2  │          ← fast experiments
  └─────────┘         └────────┘
```

**Key principles:**
- One desired outcome at a time — don't try to solve everything
- Opportunities are customer problems/needs, never solutions
- Generate ≥3 solutions per opportunity before choosing one
- Experiments are the cheapest way to validate an assumption
- The tree is a living document — update weekly as you learn

---

## How to build an OST

### Step 1 — Define the desired outcome

Confirm or help the user articulate one measurable outcome at the top of the tree.

Good outcomes:
- "Increase 7-day retention from 20% to 35%"
- "Reduce time-to-first-value from 3 days to 1 day"
- "Increase conversion from free to paid from 2% to 5%"

Bad outcomes (reject these):
- "Build a better onboarding" — that's a solution
- "Improve the product" — unmeasurable
- "Launch feature X" — that's an output

If the user can't state a metric: ask "What would need to be true for you to consider this effort a success?"

### Step 2 — Map opportunities from research

From customer interviews, analytics, support tickets, or NPS feedback, identify 3–7 customer opportunities (pain points, unmet needs, desires).

**Frame each from the customer's perspective:**
- ✅ "I struggle to understand which plan is right for me"
- ✅ "I can't find past purchases quickly"
- ✅ "I feel anxious about whether my data is safe"
- ❌ "Users need a better search" — that's a solution

**Prioritise using Opportunity Score (Dan Olsen, *The Lean Product Playbook*):**
```
Opportunity Score = Importance × (1 − Satisfaction)
```
Survey customers: rate each need on Importance (0–1) and current Satisfaction (0–1).
- High Importance + Low Satisfaction = highest score = best opportunity
- Plot on Importance vs Satisfaction chart — upper-left quadrant is the sweet spot

### Step 3 — Generate solutions (diverge before converging)

For each top-priority opportunity, brainstorm ≥3 solutions from three angles:
- **PM perspective**: What UX/product change addresses this?
- **Designer perspective**: What interaction or visual change?
- **Engineer perspective**: What technical approach? (often the most creative)

Rules:
- Don't commit to the first idea — compare and contrast
- "Best ideas often come from engineers" — include technical solutions
- Solutions should be independent (different solutions for the same opportunity)

### Step 4 — Design experiments

For the most promising solutions, design 1–2 fast experiments:

| Experiment | Assumption tested | Method | Success metric | Effort |
|------------|------------------|--------|---------------|--------|
| <experiment name> | <what belief this validates> | <A/B test / fake door / prototype / interview> | <metric + threshold> | <1d / 3d / 1w> |

**Assumption categories (prioritise in this order):**
1. **Value**: Will users want this? (most important to test first)
2. **Usability**: Can users figure it out?
3. **Feasibility**: Can we build it?
4. **Viability**: Does the business case work?

**Cheap experiment types:**
- Existing product: A/B test, fake door, prototype, user interview, data analysis
- New product: XYZ hypothesis ("At least X% of Y will do Z"), landing page, concierge MVP

### Step 5 — Visualise and document

Write `docs/discovery/OST-<outcome-slug>.md`:

```markdown
# Opportunity Solution Tree: <Outcome>

**Desired outcome**: <metric> from <current> to <target> by <date>
**Last updated**: <date>

## Opportunity map

| # | Opportunity | Importance | Satisfaction | Opportunity Score | Priority |
|---|------------|-----------|-------------|-------------------|---------|
| A | <customer need> | 0.8 | 0.3 | 0.56 | 1st |
| B | <customer need> | 0.7 | 0.6 | 0.28 | 3rd |
| C | <customer need> | 0.6 | 0.2 | 0.48 | 2nd |

## Solutions for top opportunities

### Opportunity A: <name>
| Solution | Description | Experiment |
|---------|-------------|-----------|
| Sol A1 | <description> | <experiment> |
| Sol A2 | <description> | <experiment> |
| Sol A3 | <description> | <experiment> |

## Active experiments

| Experiment | Assumption | Status | Result |
|-----------|-----------|--------|--------|
| <name> | <assumption> | Running / Done | <result or pending> |

## Learning log

- <date>: Discovered <insight> from <source>. Killed <solution> / promoted <opportunity>.
```

---

## Integration with /prd

Once an opportunity is validated and a solution is chosen:
→ Run `/prd` with the validated opportunity as the problem statement
→ The OST's Opportunity Score data feeds directly into PRD §3 (Success Metrics) and §4 (Target Users)

---

## Anti-patterns

❌ **Opportunity = solution in disguise**: "Users need a search bar" is a solution. "Users can't find past purchases" is an opportunity.

❌ **Skipping divergence**: Picking the first solution for each opportunity. Always generate ≥3 before choosing.

❌ **Experiments that take >1 week**: If it takes longer than a week to learn, it's not an experiment — it's a feature.

❌ **Updating the tree once**: OST is a continuous practice. Update weekly as you learn.

❌ **Too many outcomes**: One outcome per tree. If you have multiple outcomes, run multiple trees or pick the highest priority.
