---
name: write-prod-strategy
description: Product strategy docs using 7-component framework
---

# Write Product Strategy Skill

Create comprehensive product strategy using a 7-component framework. Connects vision to execution.

## Quick Start

1. Tell me: "I need a product strategy for [product/initiative]"
2. I will check `context-library/strategy/`, `context-library/business-info-template.md`, and `context-library/research/` for existing context
3. I will ask about scope (company vs product), horizon (6mo/1yr/3yr), audience, and whether we are building on or replacing existing strategy
4. We work through the 7 components: Objective, Users, Superpowers, Vision, Pillars, Impact, Roadmap
5. Output goes to `outputs/analyses/strategy-[product]-[date].md`

**Output length:** A complete 7-component strategy doc should be 2,000-3,000 words with an executive summary of 200-300 words. If you want a shorter version, ask for a "1-page strategy brief" and I will generate only: Objective, Target Users, Strategic Pillars, and Key Metrics.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Existing Strategy | `context-library/strategy/*.md` | company strategy, vision, roadmap | Current strategy to build on or update |
| Business Model | `context-library/business-info-template.md` | TAM, revenue model, metrics | Objective anchor and North Star |
| User Research | `context-library/research/*.md` | user segments, JTBD, pain points | Users section and strategic fit |
| Competitive Analysis | `context-library/research/competitive-*.md` | competitor positioning | Superpowers and differentiation |
| Historical PRDs | `context-library/prds/*.md` | strategic features, decisions | Precedent for feature strategy alignment |
| Meetings | `context-library/meetings/*.md` | strategy discussion, OKRs, board feedback | Stakeholder input and constraints |

**Context Priority:**
1. Business model and company objectives FIRST
2. User research and strategic direction SECOND
3. Competitive positioning THIRD
4. Existing feature decisions FOURTH

**Cross-Skill Links:**
- If defining North Star → Link to `/define-north-star`
- If analyzing user needs → Link to `/user-research-synthesis` and `/journey-map`
- If evaluating features → Link to `/impact-sizing` for driver trees
- If creating PRDs → Ensure they reference strategic pillars from here

---

## Step 0: Understanding Your Strategic Context

Before writing strategy, let me understand where you are...

**Checking:**
- `context-library/strategy/` for existing strategy docs
- `context-library/business-info-template.md` for business model
- `context-library/research/` for user and competitive insights
- `context-library/meetings/` for stakeholder input and OKRs

**Based on what I find, I'll show you:**

### Current Strategic State

**Existing Strategy:**
- [If you have one: what's your current strategy, when was it last updated?]
- [Key strategic pillars: what are you focusing on?]
- [Are we refreshing, evolving, or starting from scratch?]

**Business Context:**
- [North Star metric: what measures success?]
- [Growth stage: early product, scaling, or maturing?]
- [Revenue model: how do you make money?]

**User & Competitive Landscape:**
- [Primary user segments: who are you building for?]
- [Competitive position: what makes you different?]
- [Unmet needs: what gaps exist in the market?]

### PM-Specific Diagnosis Questions

1. **Scope:** Company-level strategy or product-line strategy?
2. **Horizon:** 6 months, 1 year, or 3 years out?
3. **Constraints:** Resource limitations, market conditions, organizational changes?
4. **Stakeholder Input:** What does leadership expect? What are investor priorities?
5. **Current Momentum:** What's working well? What's not working?

---

## When to Use This Skill

- Annual/quarterly strategy planning
- New product launch planning
- Investor/board presentations
- Cross-functional alignment on direction
- When leadership asks "what's the strategy?"

## The 7-Component Framework

A complete product strategy answers:

1. **Objective** - What are we trying to achieve and how will we measure it?
2. **Users** - Who are we serving and what jobs do they need done?
3. **Superpowers** - What unique advantages do we have?
4. **Vision** - What does the future look like if we succeed?
5. **Pillars** - What are our 2-4 strategic focus areas?
6. **Impact** - What value will we create (users + business)?
7. **Roadmap** - What's the plan to get there?

## Workflow

### Step 1: Gather Context

Ask the PM:

```
Strategy Scope:
- Company or product strategy?
- Timeframe: 6 months / 1 year / 3 years?
- Audience: Team / Exec / Board / Investors?
- Current strategy exists? (building on or replacing?)

Context to review:
- Company mission/vision
- Current OKRs
- User research
- Competitive landscape
- Market trends
- Past strategy docs (if any)
```

### Step 2: Component 1 - Objective

**Objective = Mission + Measure**

Mission: What problem are we solving?
Measure: How will we know if we're winning?

```
## Objective

### Mission
[One-sentence statement of what we're trying to accomplish]

Example: "Help product teams ship better features faster by reducing the time from idea to launch"

### North Star Metric
[The one metric that best captures value delivered]

Metric: [Metric name]
Current: [Baseline value]
Target: [Goal value by when]

Why this metric:
- Captures value for users: [Explanation]
- Drives business outcomes: [Explanation]
- Team can influence it: [Explanation]

### Supporting Metrics
1. [Metric 1]: [Current] → [Target]
2. [Metric 2]: [Current] → [Target]
3. [Metric 3]: [Current] → [Target]

### Guardrails
Metrics we won't sacrifice for growth:
- [Guardrail 1: e.g., "User satisfaction score stays above 4.0"]
- [Guardrail 2: e.g., "Response time under 200ms"]
```

### Step 3: Component 2 - Users

**Users = JTBD + Journey Map**

Who are we serving and what do they need?

```
## Users

### Primary User Segments

**Segment 1: [Name]**
- Who: [Description - role, company size, industry]
- Size: [TAM - how many of these users exist]
- Pain: [Primary pain point]
- Job to be done: [What they're trying to accomplish]

**Segment 2: [Name]**
- Who: [Description]
- Size: [TAM]
- Pain: [Primary pain point]
- Job to be done: [What they're trying to accomplish]

### Jobs to Be Done Canvas

For primary segment:

**Job Statement:**
When [situation], I want to [motivation], so I can [expected outcome].

Example: "When I'm planning my product roadmap, I want to quickly prioritize features based on impact, so I can focus the team on what matters most."

**Current Alternatives:**
- [Alt 1]: [What they use today + why it's insufficient]
- [Alt 2]: [What they use today + why it's insufficient]

**Success Criteria:**
- Speed: [How fast does it need to be?]
- Quality: [How good does the outcome need to be?]
- Cost: [What's their budget?]
- Ease: [How simple must it be?]

### User Journey

[Reference existing journey map or create simplified version]

Key stages:
1. [Stage 1]: [User goal] → [Current pain point]
2. [Stage 2]: [User goal] → [Current pain point]
3. [Stage 3]: [User goal] → [Current pain point]

Biggest friction points:
- [Friction 1]: Causes [X% drop-off or Y time waste]
- [Friction 2]: Causes [impact]
```

### Step 4: Component 3 - Superpowers

**Superpowers = 7 Powers Framework**

What unique advantages do we have?

```
## Superpowers

Our durable competitive advantages:

**Power 1: [Name]** ([Type from 7 Powers])

[Description of advantage]

Why it's durable:
- [Reason 1: Why competitors can't easily copy]
- [Reason 2: How it compounds over time]

Evidence:
- [Data point or example]

**Power 2: [Name]** ([Type from 7 Powers])

[Description]

Why it's durable:
- [Reason]

Evidence:
- [Data/example]

### 7 Powers Reference:

1. **Scale Economies** - Unit costs decline as volume increases
2. **Network Effects** - Value increases as users increase
3. **Counter-Positioning** - Business model incumbents can't copy
4. **Switching Costs** - Value loss when switching to alternative
5. **Branding** - Durable attribution of higher value to objectively identical offering
6. **Cornered Resource** - Preferential access to coveted asset
7. **Process Power** - Embedded company organization/activity set
```

### Step 5: Component 4 - Vision

**Vision = Visiontype + Prototype**

What does the future look like if we succeed?

```
## Vision

### Vision Statement (3-5 Years Out)

[Paragraph describing the future state]

Example: "In 3 years, product teams using our platform ship features 10x faster than industry average. Instead of spending months in planning, teams validate ideas in days using AI-powered prototyping and instant user feedback loops. The default workflow becomes: idea → prototype → test → ship, all within a single week. Our platform becomes the nervous system of product development."

### Future User Experience

**A day in the life** (future state):

[Narrative of how a user will experience your product]

Example:
"Sarah, a PM at a fast-growing startup, has an idea for a new feature at 9am. By 9:15am, she's used our AI to generate three prototype variants. By 10am, she's running an A/B test with 1,000 users. By 3pm, she has statistically significant results. By 5pm, engineering has the winning design and technical spec. What used to take 6 weeks now takes 8 hours."

### Visiontype (Prototype of Vision)

[If possible, create visual representation:]
- Mockup of future product state
- Diagram of ecosystem
- User flow in future state
- Before/after comparison

[Or generate using `/generate-ai-prototype` or `/napkin-sketch`]

### What Changes?

| Today | Future (Vision State) |
|-------|----------------------|
| [Current state 1] | [Future state 1] |
| [Current state 2] | [Future state 2] |
| [Current state 3] | [Future state 3] |
```

### Step 6: Component 5 - Pillars

**Pillars = 2-4 Strategic Focus Areas**

Where will we concentrate our efforts?

```
## Strategic Pillars

The 2-4 areas where we'll focus investment and energy:

### Pillar 1: [Name]

**What:** [Description of this focus area]

**Why:** [Why this is strategically important]

**How we'll win:**
- [Approach 1]
- [Approach 2]
- [Approach 3]

**Key initiatives:**
- [Initiative 1]: [Brief description]
- [Initiative 2]: [Brief description]

**Success looks like:**
- [Metric/outcome 1]
- [Metric/outcome 2]

### Pillar 2: [Name]

[Same structure as Pillar 1]

### Pillar 3: [Name]

[Same structure as Pillar 1]

### What We're NOT Doing

Explicit non-goals for this strategy period:
- ❌ [Non-goal 1]: [Why we're explicitly not doing this]
- ❌ [Non-goal 2]: [Reason]
- ❌ [Non-goal 3]: [Reason]
```

### Step 7: Component 6 - Impact

**Impact = Value Estimation with Driver Trees**

What value will we create?

```
## Impact

### User Impact

**Users affected:** [Number or percentage]

**Pain severity:** [Critical / High / Medium]

**Value delivered:**
- [Benefit 1]: [Quantified if possible]
- [Benefit 2]: [Quantified if possible]
- [Benefit 3]: [Quantified if possible]

**Workaround cost eliminated:**
- Time saved: [X hours per user per week]
- Money saved: [$ per user per year]
- Frustration reduced: [Qualitative description + quotes]

### Business Impact

**Driver Tree: Feature → Metric → Revenue/Profit**

```
Strategy Success
    ↓
North Star Metric: [Metric name] increases by [X%]
    ↓
    ├─→ Driver 1: [Leading indicator] increases by [Y%]
    │       ↓
    │       ├─→ Initiative A contributes [Z%]
    │       └─→ Initiative B contributes [W%]
    │
    └─→ Driver 2: [Leading indicator] increases by [Y%]
            ↓
            └─→ Initiative C contributes [Z%]
```

**Revenue Impact:**
- New revenue: [$ from new customers/use cases]
- Retained revenue: [$ from reduced churn]
- Expansion revenue: [$ from upsells/cross-sells]

**Total projected impact:** $[X]M ARR by [Date]

**Cost to execute:**
- Engineering: [FTE or $]
- Design: [FTE or $]
- Other: [FTE or $]

**ROI:** [Revenue impact / Cost] = [X]x

### Strategic Value

Beyond numbers:

**OKR Alignment:**
- Company OKR 1: [How this strategy supports it]
- Company OKR 2: [How this strategy supports it]

**Competitive Positioning:**
- [How this changes competitive landscape]
- [New moat created or existing moat strengthened]

**Market Opportunity:**
- TAM: $[X]M
- SAM: $[Y]M
- SOM (achievable): $[Z]M over [timeframe]

### Confidence Levels

**Data Quality:**
- High confidence: [What we're certain about]
- Medium confidence: [What we have some data on]
- Low confidence: [What we're assuming]

**Key Risks:**
- [Risk 1]: [Probability × Impact]
- [Risk 2]: [Probability × Impact]
- [Risk 3]: [Probability × Impact]

**How we'll de-risk:**
- [Validation approach for each major assumption]
```

### Step 8: Component 7 - Roadmap

**Roadmap = 0-3mo Fixed, 3-6mo Loose, 6+ Exploratory**

How will we execute?

```
## Roadmap

### Now (0-3 Months) - Fixed Commitments

**Q[X] [Year]:**

| Initiative | Pillar | Impact | Team | Status |
|-----------|--------|--------|------|--------|
| [Initiative 1] | [Pillar name] | [Metric target] | [Team] | [Status] |
| [Initiative 2] | [Pillar name] | [Metric target] | [Team] | [Status] |
| [Initiative 3] | [Pillar name] | [Metric target] | [Team] | [Status] |

**Milestones:**
- [Month 1]: [Milestone]
- [Month 2]: [Milestone]
- [Month 3]: [Milestone]

### Next (3-6 Months) - Directional Plan

**Q[X+1] [Year]:**

Focus areas (subject to change based on learnings):
- [Focus area 1]: [General direction]
- [Focus area 2]: [General direction]

Potential initiatives (not committed):
- [Potential initiative 1]
- [Potential initiative 2]

Decision points:
- [Month 4]: Decide on [Key decision]
- [Month 5]: Decide on [Key decision]

### Later (6+ Months) - Exploratory

**Q[X+2] [Year] and beyond:**

Strategic bets to explore:
- [Exploratory bet 1]: [What we need to learn]
- [Exploratory bet 2]: [What we need to learn]

Research questions:
- [Question 1]
- [Question 2]

Open questions:
- [Question 1]
- [Question 2]

### Trade-Offs Made

What we're NOT doing (and why):

- **[Alternative path 1]:**
  - Why we considered: [Reason]
  - Why we chose not to: [Trade-off]

- **[Alternative path 2]:**
  - Why we considered: [Reason]
  - Why we chose not to: [Trade-off]
```

## Complete Output Format

```markdown
# [Product Name] Strategy
## [Timeframe: e.g., 2026 Annual Strategy]

**Author:** [Name]
**Date:** [Date]
**Status:** [Draft / Review / Approved]
**Audience:** [Who this is for]

---

## Executive Summary

[2-3 paragraph summary of entire strategy]

**TL;DR:**
- Objective: [One sentence]
- Target: [North Star Metric goal]
- Approach: [Strategic pillars in one sentence]
- Impact: [Business outcome]

---

## 1. Objective

### Mission
[What we're trying to accomplish]

### North Star Metric
[Metric + target]

### Supporting Metrics
[List of 3-5 metrics]

---

## 2. Users

### Primary Segments
[Description of who we serve]

### Jobs to Be Done
[JTBD canvas]

### User Journey
[Key stages + friction points]

---

## 3. Superpowers

[2-3 durable competitive advantages from 7 Powers]

---

## 4. Vision

### Vision Statement
[Future state description]

### Visiontype
[Prototype or mockup of vision]

---

## 5. Strategic Pillars

### Pillar 1: [Name]
[Details]

### Pillar 2: [Name]
[Details]

### Pillar 3: [Name]
[Details]

### Non-Goals
[What we're NOT doing]

---

## 6. Impact

### User Impact
[Value to users]

### Business Impact
[Revenue/profit driver tree]

### Strategic Value
[OKR alignment, competitive positioning]

### Confidence & Risks
[What we're certain/uncertain about]

---

## 7. Roadmap

### Now (0-3mo)
[Fixed commitments]

### Next (3-6mo)
[Directional plan]

### Later (6+mo)
[Exploratory bets]

### Trade-Offs
[What we chose not to do]

---

## Appendix

### References
- [PRD links]
- [Research docs]
- [Competitive analysis]
- [Market data]

### Feedback & Iteration
- Last updated: [Date]
- Feedback from: [Stakeholders]
- Next review: [Date]
```

## Pro Tips

1. **Start with Objective:** North Star Metric anchors everything
2. **Users before solutions:** Understand JTBD before defining strategy
3. **Be specific:** "Improve UX" is not a pillar, "Reduce time-to-first-value by 50%" is
4. **Quantify impact:** Use driver trees to connect strategy to revenue
5. **Say no explicitly:** Non-goals matter as much as goals
6. **Visual visiontype:** Show, don't just tell
7. **Update quarterly:** Strategy is living document, not set-and-forget

## Common Mistakes to Avoid

❌ Vague objectives ("be the best")
✅ Measurable targets ("reduce churn from 5% to 2% by Q4")

❌ No user insight ("we'll build features")
✅ JTBD-driven ("users need to X, currently they do Y which wastes Z time")

❌ Copying competitor strategy
✅ Leveraging unique superpowers

❌ Wishful thinking ("we'll 10x revenue")
✅ Driver trees with realistic assumptions

❌ Feature roadmap masquerading as strategy
✅ Outcome-driven pillars with example initiatives

## Output Integration

### Where Files Go

**Strategy documents:**
- Active work: `outputs/analyses/strategy-[product]-[date].md` (living document)
- When finalized: Move to `context-library/strategy/[product]-strategy-[year].md` for reference
- Executive version: Can be adapted for board/investor presentations

### Link to Other Work

After writing strategy:
- **Reference in PRDs** - "This feature supports Strategic Pillar [X]" from this document
- **Roadmap alignment** - "Q# roadmap focuses on Pillar [Y]"
- **Team alignment** - Share with cross-functional teams for guidance
- **Status updates** - Track progress against strategic goals in `/status-update`

### Cross-Skill Integration

**Feeds into:**
- `/prd-draft` - All PRDs should reference and support strategic pillars
- `/status-update` - Track progress against strategy in weekly updates
- Board/investor communications - Strategy is the foundation for pitches
- Quarterly planning - Use strategy to guide roadmap prioritization

**Pulls from:**
- `/define-north-star` - Your North Star becomes the Objective component
- `/user-research-synthesis` - User insights inform Users component
- `/impact-sizing` - Feature impact sizing informs Impact component
- `/competitor-analysis` - Competitive insights inform Superpowers component

---

## Integration with Other Skills

**Inputs:**
- `/define-north-star` - Component 1: Objective
- `/journey-map` - Component 2: Users
- `/impact-sizing` - Component 6: Impact
- `/user-research-synthesis` - Component 2: User insights

**Outputs:**
- `/prd-draft` - PRDs align with strategic pillars
- `/status-update` - Progress against strategy
- Board/investor decks - Executive summary

## Questions to Ask Before Writing

1. **Scope:** Company-level or product-level strategy?
2. **Horizon:** 6 months, 1 year, 3 years?
3. **Current state:** Building on existing strategy or creating from scratch?
4. **Data available:** User research, market data, competitive intel?
5. **Audience:** Who will read and act on this strategy?

## Output Length Guidance

**Full strategy (default):** 2,000-3,000 words covering all 7 components with an executive summary of 200-300 words. This is what you need for quarterly/annual planning, cross-functional alignment, and investor/board communication.

**1-page strategy brief (on request):** When the PM asks for a shorter version, generate only:
1. **Objective:** Mission + North Star Metric + target
2. **Target Users:** Primary segment + JTBD (one paragraph)
3. **Strategic Pillars:** 2-4 focus areas with one sentence each
4. **Key Metrics:** 3-5 metrics with current baseline and targets

This brief should fit on a single page (~500 words). Use it for quick alignment, team kickoffs, or when the full strategy is being drafted elsewhere.

---

## Output Quality Self-Check

Before delivering the strategy document, verify:

- [ ] **Executive summary stands alone:** Someone reading only the exec summary understands the objective, approach, and expected impact. Test: cover everything below the summary and ask "do I know what we are doing and why?"
- [ ] **North Star is defined:** A specific, measurable North Star metric with baseline and target is stated in the Objective section. Not "grow revenue" but "increase MRR from $250K to $400K by Q4."
- [ ] **Users are real, not abstract:** User segments include specific roles, company types, and pain points grounded in research. At least one user quote or data point is referenced if research exists.
- [ ] **Superpowers pass the competitor test:** Each superpower explains why competitors cannot easily replicate it. If a competitor could copy it in 6 months, it is not a superpower.
- [ ] **Pillars are outcome-driven:** Each pillar describes an outcome to achieve, not a feature to build. "Reduce time-to-first-value by 50%" not "Build onboarding wizard."
- [ ] **Non-goals are real tradeoffs:** The non-goals section lists things you actually considered doing but chose not to. "We will not build a spaceship" is not a tradeoff.
- [ ] **Impact is quantified:** Revenue impact, user impact, or both are estimated with driver trees or ranges, not just qualitative statements.
- [ ] **Roadmap has three horizons:** Now (0-3mo) is fixed, Next (3-6mo) is directional, Later (6+mo) is exploratory. If all three horizons are equally detailed, the roadmap is too speculative.
- [ ] **Length is appropriate:** Full strategy: 2,000-3,000 words. Brief: ~500 words. If significantly over, cut redundancy. If significantly under, check for missing components.

Remember: A good strategy is a clear "no" to many things and a committed "yes" to a few. Strategy is about choices, not wishes.
