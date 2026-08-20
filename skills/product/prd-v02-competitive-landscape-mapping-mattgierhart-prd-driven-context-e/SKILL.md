---
name: prd-v02-competitive-landscape-mapping
description: >
  Map the competitive landscape before positioning your product for PRD v0.2 Market Definition.
  Triggers on completing v0.1 Spark, analyzing competitors, researching market, or requests like
  "competitive analysis", "who else solves this", "market landscape", "what alternatives exist",
  "competitor research", "feature comparison". Outputs CFD- entries for competitive intelligence
  and BR- entries for positioning rules.
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

# Competitive Landscape Mapping

Understand market reality before defining your position.

## Workflow Position

```
v0.1 Spark (Problem + Value) → Competitive Landscape Mapping → Product Type Classification
       (what hurts)                 (who else solves it)           (how we compete)
```

## Consumes

This skill requires prior work from v0.1:

- **CFD-\* entries (problem statements, from Problem Framing) — Evidence for what users need/want
- **CFD-\* entries (value hypotheses, from User Value Articulation) — Desired outcomes users are seeking
- **PRD.md Why section** — Problem framing and market signals

This skill assumes v0.1 Spark is complete (both problem and value).

## Produces

This skill creates/updates:

- **CFD-\* entries** (competitive intelligence) — Analysis of direct competitors, adjacent solutions, workarounds
- **BR-\* entries** (positioning rules) — Constraints derived from landscape analysis
- **Landscape map artifact** — Current behavior documentation, feature matrix, 1% better hypothesis

All CFD competitive intelligence entries should include:
- `confidence: 2-3/5` (based on evidence tier from public sources + user validation)
- Evidence source (G2 reviews, pricing pages, user interviews, etc.)
- Forward target: "Would move to 4/5 if we validate gap with 5+ target users"

Example competitive intelligence entry:
```markdown
CFD-042: Competitive Intelligence — Competitor Landscape Analysis

Type: Competitive Intelligence
Date: 2026-02-01
Confidence: 3/5 (source: public-research + 3-customer-interviews)
Competitors Analyzed: 4 direct + 2 adjacent
Primary Gap: All competitors require enterprise licensing; SMB segment underserved

Feature Matrix: [Link to matrix]
1% Hypothesis: "SMB sales teams can get 80% of [Competitor A] features for 40% of price"
Evidence:
  - CFD-001: 3 SMB teams paying $500/mo but using only 5 of 20 features
  - CFD-015: Value hypothesis shows $12,500/year need for core 5 features only
Next Target: "Would move to 4/5 if we validate with 5+ SMB prospects willing to pay $200/mo"
```

## Workflow Overview

1. **Document current behavior** → What users do TODAY (before competitor search)
2. **Discover alternatives** → Direct, adjacent, workarounds, "do nothing"
3. **Analyze gaps** → Industry/geography gaps, underserved segments
4. **Compare features** → Build comparison matrix
5. **Form hypothesis** → 1% better hypothesis with evidence

## Core Output Template

| Element | Definition | Evidence |
|---------|------------|----------|
| **Current Behavior** | How users solve this today | Observed workflow |
| **Direct Competitors** | Products solving same problem | Revenue/funding proof |
| **Adjacent Solutions** | Products solving related problems | User overlap |
| **Workarounds** | DIY solutions (spreadsheets, manual) | Forum/reddit mentions |
| **Feature Matrix** | Side-by-side capability comparison | Product documentation |
| **Gap Analysis** | Where competition is weak | Reviews, complaints |
| **1% Hypothesis** | How we win | Evidence-anchored |

See `assets/landscape.md` for copy-paste template.

## Step 1: Document Current Behavior

**Before searching competitors**, document what target users do TODAY.

### Capture Format

```
Current Behavior: [What they do]
Tools Used: [Existing tools, if any]
Time Investment: [Hours/week on workaround]
Pain Points: [From v0.1 CFD-IDs]
```

### Why First?
- Prevents solution bias from competitor features
- Reveals workarounds competitors might miss
- Establishes true baseline for improvement claims

## Step 2: Competitor Discovery

### Discovery Categories

| Category | Definition | Search Strategy |
|----------|------------|-----------------|
| **Direct** | Same problem, same segment | "[problem] software" |
| **Adjacent** | Related problem, potential pivot | "[related workflow] tool" |
| **Workarounds** | DIY solutions | Reddit: "how I [task]" |
| **Do Nothing** | Accept status quo | Why hasn't this been solved? |

### Minimum Discovery Checklist
- [ ] 3+ direct competitors (or document why fewer exist)
- [ ] 2+ adjacent solutions
- [ ] 1+ workaround documented
- [ ] "Do nothing" cost quantified

### Create CFD Entry Per Competitor

```
CFD-###: Competitor — [Name]
Type: Competitive Intelligence
Source: [Website, G2, Crunchbase]
Date: YYYY-MM-DD

Overview: [1-2 sentences]
Target Segment: [Who they serve]
Pricing: [Model and range]
Revenue/Funding: [If available]
Key Differentiator: [Their claim]
Weakness Signals: [Reviews, complaints]
```

## Step 3: Gap Analysis

### Industry/Geography Gap Table

| Industry | Competitors Serving | Gap Level |
|----------|--------------------:|-----------|
| [Industry 1] | X of Y | None / Small / Large |
| [Industry 2] | X of Y | None / Small / Large |

### Segment Gap Table

| Segment | Served By | Underserved Signal |
|---------|-----------|-------------------|
| Enterprise | [List] | [Signal or "Well served"] |
| Mid-Market | [List] | [Signal or "Well served"] |
| SMB | [List] | [Signal or "Well served"] |
| Prosumer | [List] | [Signal or "Well served"] |

### Underserved Signals
- Tier 1: Users paying but complaining (G2 reviews)
- Tier 2: Users building workarounds (Reddit, forums)
- Tier 3: Users asking for solutions (community posts)
- Tier 4: No apparent demand (caution)

## Step 4: Feature Comparison Matrix

Build side-by-side comparison:

| Feature | Us (Planned) | Competitor A | Competitor B | Gap |
|---------|:------------:|:------------:|:------------:|-----|
| [Feature 1] | ✅/❌/🔄 | ✅/❌ | ✅/❌ | [Our advantage] |
| [Feature 2] | ✅/❌/🔄 | ✅/❌ | ✅/❌ | [Our advantage] |

**Legend:** ✅ = Has | ❌ = Missing | 🔄 = Planned

### Matrix Requirements
- [ ] Include all "table stakes" features (what everyone has)
- [ ] Identify 1-3 differentiating features
- [ ] Note pricing tier where features unlock
- [ ] Flag features competitors are building (roadmap signals)

## Step 5: 1% Better Hypothesis

### Template

```
We can be 1% better than [Competitor X] by [specific improvement] for [specific segment].

Evidence:
- [CFD-ID]: [Supporting evidence]
- [CFD-ID]: [Supporting evidence]

Why This Matters:
- [Segment] cares about this because [reason]
- Current solutions fail at this because [reason]

Risk:
- [What could invalidate this hypothesis]
```

### Hypothesis Quality Check
- [ ] "1% better" is specific and measurable
- [ ] References CFD-IDs for evidence
- [ ] Targets a defined segment
- [ ] Explains WHY this gap exists
- [ ] Acknowledges risks

## Quality Gates

### Pass Checklist
- [ ] ≥3 competitors documented with CFD-IDs
- [ ] Feature matrix with ≥5 compared features
- [ ] ≥1 gap identified with Tier 1-2 evidence
- [ ] 1% better hypothesis formed
- [ ] Current behavior documented FIRST

### Testability Check
- [ ] Can validate 1% hypothesis in <30 days?
- [ ] Can find 10 people in target segment?
- [ ] Gap evidence is from users, not assumptions?

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| Competitor-first thinking | Started with competitor features | Document current behavior first |
| False uniqueness | "No competitors" claim | Include workarounds and adjacent |
| Feature bloat | Matrix has 20+ features | Focus on differentiators |
| Vague gaps | "Better UX" without evidence | Add specific user complaint |
| 10x claims | "10x better than X" | Start with 1% provable claim |
| Ignored workarounds | Only listed software competitors | Include spreadsheets, manual |

## CFD/BR Output Format

### CFD Entry (Competitive Intelligence)

```
CFD-###: Competitive Intelligence — [Market/Segment]
Type: Competitive Intelligence
Date: YYYY-MM-DD

Competitors Analyzed: [Count]
Primary Gap: [Description]
Evidence Tier: [1-5]

Feature Matrix: [Link or inline]
1% Hypothesis: [Statement]
```

### BR Entry (Positioning Rule)

```
BR-###: Positioning Rule — [Title]
Type: Business Rule
Source: CFD-###
Date: YYYY-MM-DD

Rule: [Specific constraint derived from landscape]
Rationale: [Why this matters]
Applies To: [Scope]
```

## Bundled Resources

- **`references/research-prompts.md`** — Deep research templates for competitor discovery and gap analysis.
- **`references/examples.md`** — Good/bad competitive analysis examples.
- **`assets/landscape.md`** — Copy-paste template for landscape mapping.
- **`assets/feature-matrix.md`** — Feature comparison matrix template.

## Handoff

Competitive landscape complete when quality gates pass. Landscape map informs:
- **Product Type Classification** (next skill) — What type are we? Clone, Slice, etc.
- **v0.3 Pricing** — Competitive pricing anchors
- **v0.3 Moat** — Where competitors are weak

Next: Product Type Classification (How should we compete based on landscape?)
