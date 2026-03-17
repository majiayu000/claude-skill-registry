---
name: writing-product-strategy
description: Use when defining long-term vision - creates 3-5 year product strategy with vision, strategic pillars, capability roadmap, and competitive moats.
---

# Writing Product Strategy

## Overview

Creates a multi-year (3-5 year) product strategy document. Defines vision, strategic pillars, capability roadmap, and competitive moats. Connects daily tactical work to long-term strategic direction.

## When to Use

- Annual/bi-annual strategy planning
- New product area or market entry
- Major pivot or repositioning
- Investor/board presentations
- Connecting quarterly charters to long-term vision

## Core Pattern

**Step 1: Define Scope & Horizon**

Ask user:
- "What product area is this strategy for?"
- "What time horizon? (3 years or 5 years)"
- "What existing context should I read?" (charters, VOC, competitive analysis)

**Step 2: Vision Statement**

Craft 2-3 sentences answering:
- Where should we be in N years?
- What will be different about the world/market?
- What role will our product play?

**Good vision example:**
"In 5 years, every retail buyer will use our Business Network as their primary source of truth for catalog data. Suppliers will publish once to reach all retailers. We'll be the operating system for retail product information."

**Bad vision example:**
"Be the best catalog platform" (vague, no specific outcome)

**Step 3: Market Context**

Analyze multi-year trends:
- **Trends:** What's changing in retail/CPG/catalogs over next N years?
  - Technology shifts (AI, automation, standards)
  - Buyer behavior changes
  - Regulatory changes
  - Industry consolidation

- **Opportunities:** What white space can we capture?
  - Underserved segments
  - Emerging use cases
  - Platform expansion

- **Threats:** What could disrupt us?
  - Competitive moves
  - Technology disruption
  - Market consolidation
  - Commoditization

**Step 4: Strategic Pillars**

Define 3-5 strategic pillars. Each pillar:
- **Why this matters:** Business case for investing here
- **Key capabilities:** What we need to build
- **Success looks like:** Outcome in N years

**Example pillar:**
"Pillar: Automated Catalog Quality
Why: 40% of product data is incorrect, causing returns/support burden
Capabilities: AI validation, auto-enrichment, supplier feedback loops
Success: <5% data error rate, trusted source of truth"

**Step 5: Capability Roadmap**

Map major capabilities to timeline:
- Year 1: [Foundational capabilities]
- Year 2: [Building on Year 1]
- Year 3: [Advanced capabilities]
- Dependencies: [What needs to exist first]

**Step 6: Competitive Moats**

Define what makes this defensible:
- **Network effects:** Gets better with more users?
- **Data moat:** Proprietary data/insights?
- **Switching costs:** Hard for customers to leave?
- **Brand/trust:** Reputation/relationships?
- **Technology:** Unique technical advantage?

**Step 7: Strategy Cascade**

Show how strategy connects to execution:
- **Strategy → Charters:** How quarterly charters advance pillars
- **Charters → PRDs:** How PRDs deliver capabilities
- **Metrics:** Strategy KPIs → Charter metrics → PRD acceptance criteria

**Step 8: Strategic Reasoning (Meta-Prompt)**

Before generating the main strategy document, create a "Strategic Reasoning" section following `.claude/rules/pm-core/meta-prompt-reasoning.md`:

- **Problem & Goals:** Restate what success looks like for this strategy
- **Context & Constraints:** List available evidence and gaps
- **Options Evaluated:** What strategic directions were considered? (at least 3)
- **Selection Rationale:** Why these pillars beat alternatives

This transparency helps stakeholders verify assumptions and challenge logic before committing to a multi-year direction.

**Step 9: Generate Output**

Write to `outputs/strategy/product-strategy-YYYY.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: writing-product-strategy
horizon: [3-year / 5-year]
sources:
  - outputs/roadmap/Q1-2026-charters.md (modified: YYYY-MM-DD)
  - outputs/insights/voc-synthesis-latest.md (modified: YYYY-MM-DD)
  - (market research from [source])
downstream:
  - outputs/roadmap/Qx-YYYY-charters.md (should align with pillars)
---

# Product Strategy: [Product Area] ([Start Year]-[End Year])

## Strategic Reasoning

### Problem & Goals
**Problem:** [One-sentence restatement of strategic challenge]
**Success Criteria:** [What makes this strategy high-quality]

### Context & Constraints
**Available Evidence:**
- [Source 1 with key findings]
- [Source 2 with key findings]

**Constraints:**
- [Resource/market/technical limitations]

**Gaps:**
- [What we don't know that matters]

### Strategic Options Evaluated

| Option | Strengths | Weaknesses | Evidence Score |
|--------|-----------|------------|----------------|
| [Direction A] | [Pros] | [Cons] | High/Medium/Low |
| [Direction B] | [Pros] | [Cons] | High/Medium/Low |
| [Direction C] | [Pros] | [Cons] | High/Medium/Low |

### Selection Rationale
**Chosen:** [Strategic pillars selected]

**Why chosen beats alternatives:**
1. [Reason 1 with evidence]
2. [Reason 2 with evidence]
3. [Reason 3 with evidence]

**What would change this strategy:**
- [Market/competitive condition that would shift direction]

---

## Vision Statement

[2-3 sentences: Where we'll be in N years, what will be different, our role]

## Market Context

### Trends (Next [N] Years)

| Trend | Impact on Our Market | Our Response |
|-------|---------------------|--------------|
| [Technology trend] | [How it changes things] | [How we'll adapt/capitalize] |
| [Buyer behavior trend] | [How it changes things] | [How we'll adapt/capitalize] |
| [Industry trend] | [How it changes things] | [How we'll adapt/capitalize] |

### Opportunities (White Space)

| Opportunity | Market Size | Why Now | Why Us |
|-------------|-------------|---------|--------|
| [Underserved segment] | [TAM if known] | [Market timing] | [Our advantage] |
| [Emerging use case] | [TAM if known] | [Market timing] | [Our advantage] |

### Threats (Risks to Vision)

| Threat | Impact if Realized | Mitigation |
|--------|-------------------|------------|
| [Competitive threat] | High/Med/Low | [How we'll counter] |
| [Technology disruption] | High/Med/Low | [How we'll adapt] |
| [Market shift] | High/Med/Low | [How we'll pivot] |

## Strategic Pillars

### Pillar 1: [Name]

**Why This Matters:**
[Business case - what problem does this solve? What value does it create?]

**Key Capabilities:**
- [Capability 1]: [What it enables]
- [Capability 2]: [What it enables]
- [Capability 3]: [What it enables]

**Success Looks Like (Year [N]):**
- [Outcome metric 1]: [Target]
- [Outcome metric 2]: [Target]
- [Outcome metric 3]: [Target]

### Pillar 2: [Name]

**Why This Matters:**
[Business case]

**Key Capabilities:**
- [Capability 1]: [What it enables]
- [Capability 2]: [What it enables]
- [Capability 3]: [What it enables]

**Success Looks Like (Year [N]):**
- [Outcome metric 1]: [Target]
- [Outcome metric 2]: [Target]
- [Outcome metric 3]: [Target]

### Pillar 3: [Name]

**Why This Matters:**
[Business case]

**Key Capabilities:**
- [Capability 1]: [What it enables]
- [Capability 2]: [What it enables]
- [Capability 3]: [What it enables]

**Success Looks Like (Year [N]):**
- [Outcome metric 1]: [Target]
- [Outcome metric 2]: [Target]
- [Outcome metric 3]: [Target]

## Capability Roadmap

| Capability | Year 1 | Year 2 | Year 3 | Dependencies | Pillar |
|------------|--------|--------|--------|--------------|--------|
| [Cap 1] | [Milestone] | [Milestone] | [Milestone] | [What needs to exist first] | Pillar 1 |
| [Cap 2] | [Milestone] | [Milestone] | [Milestone] | [What needs to exist first] | Pillar 2 |
| [Cap 3] | [Milestone] | [Milestone] | [Milestone] | [What needs to exist first] | Pillar 1 |

**Key:**
- Year 1: [Current year] - [Current year]
- Year 2: [Current year + 1]
- Year 3: [Current year + 2]

## Competitive Moats

### Moat 1: [Type - Network Effect / Data / Switching Cost / Brand]
**What:** [Description of the moat]
**How We Build It:** [Actions to strengthen]
**Defensibility:** [Why competitors can't replicate]

### Moat 2: [Type]
**What:** [Description]
**How We Build It:** [Actions to strengthen]
**Defensibility:** [Why hard to replicate]

### Moat 3: [Type]
**What:** [Description]
**How We Build It:** [Actions to strengthen]
**Defensibility:** [Why hard to replicate]

## Strategy Cascade to Execution

### How Strategy Drives Quarterly Work

```
Strategy (3-5 years)
    ↓ (Advance strategic pillars)
Quarterly Charters (This quarter)
    ↓ (Deliver capabilities)
PRDs (This sprint)
    ↓ (Build features)
Engineering Execution
```

**Example:**
- **Strategy Pillar:** Automated Catalog Quality
- **Q1 Charter:** Ship AI validation for top 5 error types
- **PRD:** AI validation service for missing attributes
- **Success Metric Cascade:**
  - Strategy KPI: <5% data error rate (Year 3)
  - Charter Metric: Reduce error rate from 40% to 30% (Q1)
  - PRD Acceptance: Validate 10K products, catch 90% of missing attributes

### Alignment Check

Every quarterly charter should answer:
- **Which pillar does this advance?** [Pillar name]
- **Which capabilities does this build?** [Capability from roadmap]
- **How does this move us toward vision?** [Connection to vision]

If a charter doesn't advance a pillar → question whether it belongs on roadmap.

## Investment Allocation (Target)

| Pillar | % of Engineering | Rationale |
|--------|-----------------|-----------|
| Pillar 1 | [%] | [Why this allocation] |
| Pillar 2 | [%] | [Why this allocation] |
| Pillar 3 | [%] | [Why this allocation] |
| KTLO/Tech Debt | [%] | [Maintenance baseline] |
| **Total** | 100% | |

## Key Assumptions

| Assumption | Impact if Wrong | Validation Plan |
|------------|----------------|-----------------|
| [Market grows at X%] | [Impact] | [How we'll validate] |
| [Customers will pay for Y] | [Impact] | [How we'll validate] |
| [Technology Z will be viable] | [Impact] | [How we'll validate] |

## Unknowns / Open Questions

- [What market data is missing?]
- [What customer validation needed?]
- [What technical feasibility unclear?]

## Sources Used
- [file paths]
- [market research sources]
- [customer interview data]

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [Market trend X] | Evidence | [Analyst report or article] |
| [Customer pain Y] | Evidence | [VOC:line or interviews] |
| [Technology feasibility Z] | Assumption | [Needs tech spike] |
| [Market size $A] | Evidence/Unknown | [Source or "Need research"] |
```

**Step 10: Copy to History & Update Tracker**

- Run `pm-os mirror --quiet` to copy to `history/writing-product-strategy/product-strategy-YYYY-MM-DD.md`
- Update `nexa/state.json` and append to `outputs/audit/auto-run-log.md`

**Step 11: Post-Skill Reflection (MANDATORY)**

Follow protocol in `.claude/rules/pm-core/post-skill-reflection.md`:

1. **Extract key learnings** (3-5 insights):
   - What strategic options were evaluated vs selected?
   - How did meta-prompt reasoning help clarify choices?
   - What evidence gaps existed?
   - What pillars emerged as most defensible?
   - Connections to past strategies or charters?

2. **Create learning entry:**
   - Write to `history/learnings/YYYY-MM-DD-writing-product-strategy.md`
   - Use template from post-skill-reflection rule

3. **Create insight beads:**
   - For each significant, reusable insight
   - Append to `.beads/insights.jsonl`
   - Types: insight (strategic learning), pattern (recurring), question (validation needed)

4. **Request output rating:**
   ```
   Rate this strategy doc (1-5, or 'skip'):
   1 - Needs major revision
   2 - Below expectations
   3 - Meets expectations
   4 - Exceeds expectations
   5 - Outstanding, exactly what I needed
   ```
   - If rated: Create output-rating bead
   - Capture any qualitative feedback

5. **Detect decisions:**
   - Strategy creation = high confidence decision
   - Auto-log: "Chose strategic pillars: [list] based on [evidence]"
   - Write to `outputs/decisions/YYYY-MM-DD-product-strategy-[horizon].md`

6. **Report completion:**
   ```
   ✅ Product strategy complete → outputs/strategy/product-strategy-YYYY.md
      Mirrored to history/writing-product-strategy/product-strategy-YYYY-MM-DD.md

   📝 Captured learnings: [N] insights, [N] beads → history/learnings/YYYY-MM-DD-writing-product-strategy.md
   📋 Logged decision: [Horizon] product strategy → outputs/decisions/

   Rate this strategy doc (1-5, or 'skip'): [prompt for rating]
   ```

## Quick Reference

### Good vs Bad Strategic Pillars

| Bad Pillar | Why Bad | Good Pillar |
|------------|---------|-------------|
| "Improve quality" | Vague, no specific outcome | "Automated catalog quality: <5% error rate via AI validation" |
| "Faster performance" | Generic | "Sub-second search: 500ms p95 for 100M SKUs enabling real-time buyer workflows" |
| "Better UX" | Unmeasurable | "Zero-training onboarding: 80% task completion without docs/support" |

### Common Strategy Mistakes

- **Too tactical:** Listing features, not capabilities/outcomes
- **No moats:** Strategy can be copied easily
- **Disconnected from reality:** Vision ignores current state/constraints
- **No cascade:** Strategy doesn't connect to quarterly charters
- **Assumes linear growth:** Ignores market shifts/disruption
- **Missing evidence:** Based on assumptions, not customer/market data

## Verification Checklist

- [ ] Vision statement clear (2-3 sentences)
- [ ] Market context documented (trends, opportunities, threats)
- [ ] 3-5 strategic pillars defined
- [ ] Each pillar has why/capabilities/success criteria
- [ ] Capability roadmap maps to years
- [ ] Competitive moats identified
- [ ] Strategy cascade to execution shown
- [ ] Investment allocation defined
- [ ] Key assumptions documented
- [ ] Metadata header complete
- [ ] Copied to history, tracker updated

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Market trend] | Evidence | [Research source] |
| [Customer need] | Evidence | [VOC or interviews] |
| [Competitive position] | Evidence/Assumption | [Analysis or assessment] |
| [Technology feasibility] | Assumption | [Needs validation] |
