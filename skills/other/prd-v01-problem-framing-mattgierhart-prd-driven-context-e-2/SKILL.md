---
name: prd-v01-problem-framing
description: >
  Transform vague product ideas into evidence-anchored problem statements for PRD v0.1 Spark.
  Triggers on starting new products/features, validating market opportunities, drafting PRD Why sections,
  or requests like "frame the problem", "define pain points", "write problem statement", "start v0.1",
  "what problem are we solving". Outputs structured problem tables with CFD evidence IDs.
---

# Problem Framing Skill

Transform market signals into evidence-anchored problem statements.

## Workflow Overview

1. **Assess gaps** → Identify what evidence is missing
2. **Anchor evidence** → Create CFD-IDs for each pain point
3. **Extract dimensions** → Pull multiple problems from each source
4. **Quantify costs** → Add time/money/risk numbers
5. **Draft statement** → Populate the problem table

## Core Output Template

Populate this table for every problem statement:

| Element | Definition | Evidence |
|---------|------------|----------|
| **Who is hurting?** | Specific, findable, countable persona | Segment size |
| **What pain exists?** | Observable behavior or workflow friction | CFD-ID |
| **Cost of problem** | Time, money, or opportunity lost | Quantified |
| **Why now?** | Market trigger creating urgency | Trend/event |
| **What's impossible?** | Opportunity cost—what can't they do | User quote |

See `assets/problem-statement.md` for copy-paste template.

## Step 1: Gap Assessment

Before drafting, create this status table:

| Element | Status | Source |
|---------|--------|--------|
| Who is hurting? | ⚠️ Hypothesis / ✅ Validated / ❌ Missing | |
| What pain exists? | ⚠️ / ✅ / ❌ | |
| Cost of problem | ⚠️ / ✅ / ❌ | |
| Why now? | ⚠️ / ✅ / ❌ | |
| What's impossible? | ⚠️ / ✅ / ❌ | |

**Gate**: Require ≥2 elements ✅ Validated before drafting. If ≥3 elements ❌ Missing, run deep research first. See `references/research-prompts.md` for research templates.

## Step 2: Evidence Anchoring

Create CFD entries for each pain point:

```
CFD-###
Source: [Platform/Person]
Tier: [1-5]
Quote: "[Verbatim]"
Dimensions: [List problems extracted]
```

**Evidence Tier Hierarchy**:
- **Tier 1**: Buying behavior (invoices, subscriptions, job budgets)
- **Tier 2**: Active workarounds (spreadsheets, hired help)
- **Tier 3**: Complaints with cost ("costs me X hours")
- **Tier 4**: General complaints ("this is annoying")
- **Tier 5**: Speculation — **REJECT**

## Step 3: Pain Dimension Extraction

Extract multiple problems from each source. One quote often contains 3-4 distinct pain dimensions.

**Example**: "USB sticks removed for every update, no scheduling, screens don't communicate, priced for 100+ displays"
→ Sneakernet workflow, No dynamic scheduling, No centralization, Price mismatch

## Step 4: Cost Quantification

Every problem needs a number:

| Type | Calculation |
|------|-------------|
| Time | Hours/week × hourly rate |
| Money | Current spend on workaround |
| Opportunity | Revenue/outcomes missed |
| Risk | Penalty × probability |

## Step 5: Draft Problem Statement

Use the core output template. Reference CFD-IDs for every claim.

See `references/examples.md` for good/bad examples with explanations.

## Quality Gates

### Pass Checklist
- [ ] ≥1 Tier 1-2 evidence item
- [ ] Cost quantified (time, money, or risk)
- [ ] "Who" specific enough to build prospect list
- [ ] "Why now" has at least Tier 3 hypothesis

### Testability Check
- [ ] Can find 10 people with this problem in 48 hours?
- [ ] Can observe the pain behavior?
- [ ] Can quantify cost without leading questions?

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Vague "Who" | "Small businesses" | → "SMBs with 1-10 screens" |
| Feature-as-problem | "Need a dashboard" | → "Can't see status" |
| Solution creep | "MVP must solve X" | → Stay on problem (v0.4) |
| Missing cost | "This is annoying" | → "Costs X hrs/week" |
| Speculation | "Users might want" | → Find evidence or reject |

## Bundled Resources

- **`references/research-prompts.md`** — Deep research templates by gap type. Use when gap assessment shows ≥3 missing elements.
- **`references/examples.md`** — Good/bad problem statement examples with explanations.
- **`assets/problem-statement.md`** — Copy-paste template for problem tables and CFD entries.

## Handoff

Problem statement complete when quality gates pass. Next: v0.2 Market Definition (segments, sizing, ICP).
