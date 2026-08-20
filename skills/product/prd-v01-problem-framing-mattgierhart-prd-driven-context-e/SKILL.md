---
name: prd-v01-problem-framing
description: >
  Transform vague product ideas into evidence-anchored problem statements for PRD v0.1 Spark.
  Triggers on starting new products/features, validating market opportunities, drafting PRD Why sections,
  or requests like "frame the problem", "define pain points", "write problem statement", "start v0.1",
  "what problem are we solving". Outputs structured problem tables with CFD evidence IDs.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# Problem Framing Skill

Transform market signals into evidence-anchored problem statements.

## Consumes

This skill assumes you have **zero prior research**. It is the starting point.

- No prior CFD- entries needed
- No prior PR D required
- Assumes: Founder/PM has observed market signals but hasn't validated them

## Produces

This skill creates/updates:

- **CFD-\* entries** (customer feedback) — 1-5 per problem dimension, with confidence scoring (see PRINCIPLES.md)
- **PRD.md Why section** — Evidence-anchored problem statement table
- **MVP scope signal** — Identifies which problem dimensions will drive MVP feature scope (handed to v0.3)

All CFD- entries should include:
- `confidence: 1-3/5` (pre-product research, no usage data)
- Evidence source (competitive analysis, interviews, workarounds, etc.)
- Forward target: "Would move to 4/5 if we observe 10+ paying customers with this pain"

## Workflow Overview

1. **Assess gaps** → Identify what evidence is missing before you can confidently state a problem
2. **Anchor evidence** → Create CFD- entries for each pain point dimension with confidence scoring
3. **Extract dimensions** → Pull multiple distinct problems from each source
4. **Quantify costs** → Add time/money/risk numbers to make pain concrete
5. **Draft statement** → Populate the problem table, tied to CFD- entries

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

Create CFD entries for each pain point with confidence scoring:

```
CFD-###: [Pain Point Name]
Source: [Where this evidence came from]
Tier: [1-5 evidence quality]
Confidence: [1-5]/5 (pre-product research)
Quote: "[Verbatim from source]"
Dimensions: [List distinct problems extracted from this source]
Next Target: "Would move to 3/5 if we interview X more customers"
```

**Evidence Tier Hierarchy** (strength of observation):
- **Tier 1**: Buying behavior (invoices, subscriptions, job budgets) — users spend money to solve this
- **Tier 2**: Active workarounds (spreadsheets, hired help, manual processes) — users invest labor
- **Tier 3**: Complaints with cost ("costs me X hours/week") — users quantify the pain
- **Tier 4**: General complaints ("this is annoying") — users acknowledge it but haven't quantified
- **Tier 5**: Speculation — **REJECT** ("users probably want...")

**Confidence Scoring** (pre-product, see PRINCIPLES.md):
- **1/5**: PM assumption or single data point
- **2/5**: Secondary research (competitive analysis, market reports)
- **3/5**: Pre-product interviews (3-5 user conversations)
- **4/5**: Beta cohort validation (observed behavior, not questions)
- **5/5**: Production usage (reserved for post-launch)

**Example entry with confidence**:
```
CFD-001: Sales teams waste 5+ hours/week on spreadsheet workflow

Source: 3 customer interviews (SaaS sales director, SMB sales rep, enterprise sales manager)
Tier: 2-3 (workaround + cost quantification)
Confidence: 3/5 (source: 3-customer-interviews-jan-2026)
Quote: "I spend 5 hours every Friday reconciling our pipeline with the actual numbers in our CRM"
Dimensions:
  - Manual data reconciliation between systems (workaround)
  - Inventory work (scheduling impact)
  - Single source of truth fragmentation (data quality risk)
Next Target: "Would move to 4/5 if we validate with 5 more sales leaders or observe workflows directly"
```

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
