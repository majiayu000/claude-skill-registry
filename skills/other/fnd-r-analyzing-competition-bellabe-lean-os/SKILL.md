---
name: fnd.r-analyzing-competition
description: Maps competitive landscape, identifies positioning gaps, and assesses competitor threats. Use when analyzing competition, finding white space, mapping alternatives, or building Canvas section 06.
allowed-tools: Read, Write, WebSearch
license: Complete terms in LICENSE.txt
---

# Competitive Analyzing

Map competitive landscape and identify positioning opportunities.

## Canvas Files

- **Reads:** 01.context.md (industry dynamics), 04.segments.md (target segment), 05.problem.md (problems being solved)
- **Writes:** 06.competitive.md

## Prerequisites

Before competitive analysis:
- `strategy/canvas/05.problem.md` must exist (problems define competitive frame)
- `strategy/canvas/04.segments.md` should exist (segment defines competitive context)

If missing:
```
"Competitive analysis requires problem definition from 05.problem.md.

Competition is framed by what problems you solve for whom.

Run fnd.r-scoring-problems skill or fnd-researcher agent first."
```

## Process

### Step 1: Load Context

Read from canvas:
- **Problems** from 05.problem.md — What problems are we solving?
- **Segment** from 04.segments.md — Who are we solving for?
- **Industry** from 01.context.md (if exists) — Industry dynamics

### Step 2: Identify Direct Competitors

Direct competitors solve the **same problem** for the **same segment** with a **similar solution**.

For each problem in 05.problem.md:
1. Search for existing solutions
2. Identify companies explicitly targeting this problem
3. Note their positioning, pricing, and target segment

**Search queries:**
- "[Problem] software"
- "[Problem] solution for [segment]"
- "[Segment] [problem] tools"
- "Alternative to [known competitor]"

**Data sources:**
- G2, Capterra, Product Hunt
- Crunchbase (funding, positioning)
- Company websites (messaging, pricing)
- LinkedIn (company size, hiring)

### Step 3: Identify Indirect Competitors

Indirect competitors solve the **same problem** with a **different approach** OR serve **adjacent needs**.

Categories:
| Type | Example |
|------|---------|
| Manual process | Spreadsheets, email, paper |
| Adjacent product | Feature in larger platform |
| Service provider | Consultants, agencies |
| DIY solution | Internal tools, scripts |
| Status quo | Do nothing |

### Step 4: Profile Each Competitor

For direct competitors, capture:

| Attribute | Source |
|-----------|--------|
| Positioning | Website headline, tagline |
| Target segment | Website copy, case studies |
| Pricing model | Pricing page |
| Price points | Pricing page, G2 |
| Key differentiators | Features page, comparisons |
| Weaknesses | G2 reviews, Reddit, complaints |
| Funding/size | Crunchbase, LinkedIn |
| Growth signals | Hiring, news, product launches |

### Step 5: Build Positioning Matrix

Create 2x2 positioning map:

**Choose axes that matter to buyers:**
| Axis Option | When to Use |
|-------------|-------------|
| Price (low/high) | Price-sensitive market |
| Complexity (simple/complex) | Workflow-heavy products |
| Target (SMB/Enterprise) | Clear segment splits |
| Approach (AI/Manual) | Technology differentiation |
| Breadth (Point/Platform) | Build vs. buy decisions |

**Map competitors:**
1. Place each competitor on the matrix
2. Identify clusters (crowded positions)
3. Find white space (unoccupied positions)

### Step 6: Identify Positioning Gaps

Gaps are unoccupied or underserved positions:

| Gap Type | Signal | Opportunity |
|----------|--------|-------------|
| Price gap | No option between $X and $Y | Mid-market play |
| Feature gap | Problem partially solved | Complete solution |
| Segment gap | Underserved buyer type | Focused positioning |
| Approach gap | Old technology dominant | Modern alternative |
| Experience gap | All options complex | Simplicity play |

**Validate gaps:**
- Is the gap intentional (unviable) or overlooked?
- Is there demand for this position?
- Can we credibly occupy this position?

### Step 7: Assess Competitive Threats

For top 3-5 competitors:

| Threat | Assessment |
|--------|------------|
| Response speed | How fast can they copy us? |
| Resource advantage | Funding, team, distribution |
| Switching costs | How locked-in are their users? |
| Brand strength | Trust, recognition |
| Expansion likelihood | Are they moving toward us? |

**Threat level:**
- **High:** Well-funded, fast, overlapping roadmap
- **Medium:** Capable but distracted or slow
- **Low:** Resource-constrained, different focus

### Step 8: Write Output

Write to `strategy/canvas/06.competitive.md` using output format below.

## Output Format

```markdown
# 06. Competitive Landscape

## Competitive Frame

**Problem being solved:** [From 05.problem — primary problem]
**Segment served:** [From 04.segments — primary segment]
**Category:** [Market category name]

## Direct Competitors

### [Competitor 1]

| Attribute | Value |
|-----------|-------|
| Positioning | [Their headline/tagline] |
| Target | [Who they serve] |
| Pricing | [Model and price points] |
| Strengths | [What they do well] |
| Weaknesses | [Gaps, complaints] |
| Threat Level | High/Medium/Low |

**Source:** [G2, website, etc.]

---

### [Competitor 2]

[Same structure]

---

### [Competitor 3]

[Same structure]

---

## Indirect Competitors

| Alternative | Type | How Used | Limitation |
|-------------|------|----------|------------|
| [Spreadsheets] | Manual | [How] | [Why inadequate] |
| [Platform X] | Adjacent | [How] | [Why inadequate] |
| [Agency Y] | Service | [How] | [Why inadequate] |

## Positioning Matrix

**Axes:**
- X-axis: [Dimension 1] (low → high)
- Y-axis: [Dimension 2] (low → high)

**Map:**
```
              HIGH [Dimension 2]
                    │
    [Competitor A]  │  [Competitor B]
                    │
LOW ────────────────┼──────────────── HIGH
[Dimension 1]       │           [Dimension 1]
                    │
    [Gap: ?]        │  [Competitor C]
                    │
              LOW [Dimension 2]
```

## Positioning Gaps

| Gap | Position | Why Valuable | Our Fit |
|-----|----------|--------------|---------|
| [Gap 1] | [Description] | [Demand signal] | High/Med/Low |
| [Gap 2] | [Description] | [Demand signal] | High/Med/Low |

## Recommended Position

**Position:** [Specific position statement]
**Rationale:** [Why this gap + why we can own it]

## Competitive Response Prediction

| If We... | They Likely... | Our Counter |
|----------|----------------|-------------|
| Enter market | [Response] | [Strategy] |
| Win customers | [Response] | [Strategy] |
| [Specific move] | [Response] | [Strategy] |

## Competitive Intelligence Gaps

| Unknown | Why It Matters | How to Learn |
|---------|----------------|--------------|
| [Gap 1] | [Impact] | [Method] |
| [Gap 2] | [Impact] | [Method] |
```

## Quality Criteria

Before finalizing, verify:

- [ ] At least 3 direct competitors profiled
- [ ] Indirect competitors documented
- [ ] Positioning matrix has clear axes
- [ ] At least 1 actionable gap identified
- [ ] Threat assessment for top competitors
- [ ] Recommended position stated

## Competitor Profile Template

Quick capture format for research:

```markdown
## [Competitor Name]

**Website:** [URL]
**Founded:** [Year]
**Funding:** $[X] ([Stage])
**Size:** [Employees]

**Positioning:** "[Their tagline]"
**Target:** [Segment]
**Pricing:** [Model] — $[X]-$[Y]

**Strengths:**
- [Strength 1]
- [Strength 2]

**Weaknesses (from reviews):**
- [Weakness 1]
- [Weakness 2]

**Recent moves:**
- [News, launches, hires]
```

## Boundaries

- Does NOT predict competitor strategy with certainty
- Does NOT guarantee positioning gap is viable
- Does NOT validate market demand for gap
- Competitor data is point-in-time — markets shift
- Review complaints are selection-biased
- Does NOT handle patent/IP competitive analysis
- Requires problem definition before meaningful analysis
- Positioning recommendation is hypothesis until validated