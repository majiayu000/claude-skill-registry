---
name: inevitability-engine
description: Systematic research protocol for discovering novel AI-native software businesses in the synthetic workforce era. Maps capability trajectories, analyzes segment-problem spaces, generates business models, and calculates inevitability scores across 3-24 month time horizons. Use when exploring AI business opportunities, conducting market research, or identifying automation-native ventures.
license: Complete terms in LICENSE
---

# The Inevitability Engine

A research protocol for discovering novel software businesses that become inevitable due to AI capability improvements.

## Core Philosophy

**Thesis**: We're witnessing the **first-ever inversion of the tool adaptation curve**. Historically, humans adapted to tools faster than tools evolved. Now, tools (LLMs) evolve faster than humans can adapt. This creates a **capability overhang** that unlocks previously impossible business models.

**Three forcing functions:**
1. **Context window explosion** (4K → 128K → 2M tokens in 24 months)
2. **Inference cost collapse** (~90% reduction/year)
3. **Tool-use reliability** (function calling: 60% → 95%+ in 18 months)

**Result**: The "synthetic worker" isn't metaphor—it's **infrastructure**. Companies will hire, fire, eval, and SLA these entities. The opportunity lies in **tooling, governance, coordination, and domain specialization** of this new workforce layer.

---

## Quick Start

**What do you want to do?**

1. **Full discovery process** → Continue to Core Workflow (execute all 6 phases)
2. **Map AI capabilities** → Jump to Phase 1: Capability Frontier Mapping
3. **Find pain points** → Jump to Phase 2: Opportunity Discovery
4. **Generate business ideas** → Jump to Phase 3: Business Model Generation
5. **Validate opportunities** → Jump to Phase 4: Market Validation
6. **Score inevitability** → Jump to Phase 5: Inevitability Scoring
7. **Create deliverable** → Jump to Phase 6: Synthesis & Output

---

## Core Workflow

### Phase 1: Capability Frontier Mapping

**Goal**: Understand what's possible now and what becomes possible at each time horizon (3mo, 6mo, 12mo, 18mo, 24mo).

Load `references/capability-mapping.md` for detailed protocol.

**Quick execution:**
1. Map current AI capabilities on Wardley evolution axis (Genesis → Custom → Product → Commodity)
2. Identify constraint removals (what was impossible 12 months ago that's trivial now?)
3. Project forward using scaling laws and roadmaps
4. Build capability unlock timeline

**Key research queries:**
- "GPT-4 capabilities vs GPT-5 predictions site:openai.com OR site:anthropic.com"
- "context window roadmap LLM 2024 2025"
- "agent orchestration frameworks production deployment"
- "inference cost trends 2024 2025"

**Output**: Capability timeline showing what becomes automatable at each horizon

---

### Phase 2: Opportunity Discovery (Segment-Problem Analysis)

**Goal**: Build exhaustive matrix of segments × problems to find high-value automation targets.

Load `references/opportunity-discovery.md` for detailed protocol.

**Target segments:**
- SMBs (1-50 employees)
- Mid-market (51-500 employees)
- Enterprise (500-5000 employees)
- Megacorps (5000+ employees)
- Knowledge workers (writers, designers, programmers, engineers, managers, finance, legal, healthcare, educators, researchers)

**For EACH segment, discover:**
1. Top 10 time-consuming tasks
2. Top 10 frustrations with current tools
3. Information work bottlenecks
4. Manual workarounds
5. Budget allocated to solutions

**Key research pattern:**
- "[segment] biggest time wasters 2024"
- "[segment] workflow automation pain points"
- "[segment] AI adoption barriers"
- "site:reddit.com [segment] productivity challenges"

**Output**: Segment-problem matrix with 50-100+ pain points identified

---

### Phase 3: Business Model Generation

**Goal**: Transform high-potential opportunities into concrete business models with synthetic worker roles.

Load `references/business-model-generation.md` for detailed protocol.

**Process:**
1. **Define synthetic worker primitives** (10 atomic job functions)
   - Continuous Monitor
   - Research Synthesizer
   - Document Processor
   - Communication Coordinator
   - Compliance Auditor
   - Creative Collaborator
   - Knowledge Curator
   - Workflow Orchestrator
   - Analysis Generator
   - Relationship Maintainer

2. **Cross with segments** to generate business ideas
   - Example: Research Synthesizer × Legal = AI-powered legal research assistant

3. **Map to time horizons** based on capability unlocks
   - 3mo: Document workspace agents
   - 6mo: Research automation platforms
   - 12mo: Synthetic operations teams
   - 18mo: Executive co-pilots
   - 24mo: Synthetic departments

**For each opportunity, define:**
- Synthetic worker role & SLA
- Economic leverage (cost reduction multiplier)
- Eval framework
- Human-in-loop points

**Output**: 25-50 business concepts with role definitions

---

### Phase 4: Market Validation

**Goal**: Validate demand, size markets, analyze competition, identify differentiation.

Load `references/validation-refinement.md` for detailed protocol.

**For top opportunities:**

1. **Search existing solutions**
   - "[business idea] startup 2024"
   - "[business idea] AI tool"
   - Assess: AI-native or bolt-on?

2. **Find buyer intent**
   - "[segment] looking for [solution]" (Twitter, Reddit, HN)
   - Count mentions, upvotes, engagement

3. **Estimate TAM/SAM**
   - "[segment] market size 2024"
   - "[job function] salary [geography]"
   - Calculate: # workers × % replaceable × willingness to pay

4. **Analyze competition**
   - What's their wedge? (product-led, sales-led, platform)
   - What's their constraint? (tech debt, sales cycle, capital)
   - What's the orthogonal attack?

**Output**: Validated opportunities with market sizing and competitive analysis

---

### Phase 5: Inevitability Scoring

**Goal**: Quantify which opportunities are inevitable and when.

Load `references/inevitability-framework.md` for detailed formulas and examples.

**Inevitability formula:**

```
Inevitability = (Economic_Pressure × Technical_Feasibility × Market_Readiness) / Adoption_Friction

Where:
E = (current_cost / ai_cost) - 1  [scale 0-10]
T = % of workflow automatable  [scale 0-10]
M = (existing_budget + behavior_change_readiness) / 2  [scale 0-10]
F = integration_cost + trust_gap + regulatory_barrier  [scale 1-10]
```

**Threshold**: Score > 25 = inevitable within stated horizon

**For each opportunity:**
1. Calculate economic pressure (cost ratio)
2. Assess technical feasibility (% automatable)
3. Gauge market readiness (budget + willingness)
4. Estimate adoption friction (barriers)
5. Compute score
6. Rank by inevitability

**Output**: Ranked list of opportunities with inevitability scores

---

### Phase 6: Synthesis & Output

**Goal**: Create structured deliverable with actionable insights.

Load `references/output-templates.md` for formatting examples.

**Standard deliverable structure:**

1. **Executive Summary** (2 pages)
   - Capability trajectory overview
   - Top 10 opportunities by inevitability score
   - Recommended actions

2. **Opportunity Matrix** (spreadsheet/table)
   - 25-50 businesses ranked by horizon and score
   - Segment, problem, solution, economics, competition
   - Time to revenue estimates

3. **Deep Dives** (5-10 pages each, top 5 opportunities)
   - Market analysis
   - Technical feasibility
   - Business model canvas
   - Go-to-market strategy
   - Risk factors
   - SLA definitions

4. **Research Appendix**
   - All search queries executed
   - Key sources and citations
   - Assumption log
   - Uncertainty flags

**Output**: Comprehensive research report ready for decision-making

---

## Key Frameworks

### Wardley Evolution Axis

Map capabilities across evolution stages:

```
GENESIS → CUSTOM → PRODUCT → COMMODITY
├─ Multimodal reasoning (custom→product)
├─ Long-horizon planning (genesis→custom)
├─ Reliable tool orchestration (product→commodity)
├─ Real-time learning loops (genesis)
├─ Inter-agent coordination (genesis→custom)
├─ Domain-specific fine-tuning (custom→product)
└─ Eval frameworks (custom→product)
```

Load `references/wardley-mapping.md` for detailed methodology.

---

### Time-Horizon Capability Unlocks

|Horizon|Context|Cost/1M tokens|Tool Reliability|New Unlock|
|-------|-------|--------------|----------------|----------|
|**3mo**|200K|$0.15|96%|Real-time document workspace agents|
|**6mo**|500K|$0.08|97%|Multi-hour autonomous research|
|**12mo**|1M|$0.04|98%|Cross-platform orchestration|
|**18mo**|2M|$0.02|98.5%|Long-context strategic planning|
|**24mo**|5M+|$0.01|99%|Synthetic PM/analyst roles|

---

### Synthetic Worker Primitives

**10 atomic job functions that become commoditized:**

1. **Continuous Monitor** - Watches systems, alerts on anomaly
2. **Research Synthesizer** - Gathers sources, summarizes, cites
3. **Document Processor** - Extracts, validates, transforms
4. **Communication Coordinator** - Drafts, routes, tracks
5. **Compliance Auditor** - Checks rules, flags violations
6. **Creative Collaborator** - Generates variants, iterates on feedback
7. **Knowledge Curator** - Organizes, tags, retrieves
8. **Workflow Orchestrator** - Manages multi-step processes
9. **Analysis Generator** - Runs reports, identifies patterns
10. **Relationship Maintainer** - Tracks context, personalizes outreach

Cross these with target segments to generate business ideas.

---

## Research Protocol Patterns

Load `references/research-protocols.md` for complete query library.

**Capability tracking:**
- "GPT-5 capabilities predictions 2025"
- "Claude context window roadmap"
- "LLM tool use reliability production"

**Pain point mining:**
- "[segment] workflow inefficiencies reddit"
- "[segment] biggest productivity challenges"
- "[job function] time tracking studies"

**Market validation:**
- "[business idea] startup funding 2024"
- "[segment] software spending trends"
- "[task] automation ROI case studies"

**Competitive intelligence:**
- "AI [task] automation companies"
- "[competitor] customer reviews G2 Capterra"

---

## First Principles Decomposition

For each high-value task:

1. **Irreducible cognitive work?**
   - Reading, synthesizing, deciding, creating, coordinating?

2. **% automatable TODAY?**
   - Use current LLM benchmarks (MMLU, HumanEval, etc.)

3. **% automatable at each horizon?**
   - 3mo, 6mo, 12mo, 18mo, 24mo

4. **What remains human-in-loop?**
   - Judgment, taste, stakeholder management, ethical choice

5. **Economic leverage?**
   - Calculate: (human_cost - ai_cost) / ai_cost

---

## Quality Signals

**Good opportunity has:**
- [ ] Economic pressure > 10x cost reduction
- [ ] Technical feasibility > 70% automatable within horizon
- [ ] Market readiness (existing budget + proven pain)
- [ ] Low adoption friction (easy integration, low trust gap)
- [ ] Clear SLA definition
- [ ] Measurable eval framework
- [ ] Validated buyer intent (social proof)
- [ ] Differentiated positioning vs incumbents
- [ ] AI-native architecture (not bolt-on)
- [ ] Workflow replacement (not just enhancement)

**Red flags:**
- Only 10-20% cost reduction (not compelling)
- High human-in-loop requirements (doesn't scale)
- Unclear eval criteria (can't measure success)
- Heavy regulatory burden (slow adoption)
- Strong incumbents with AI-native approaches
- No clear buyer intent signals
- Requires behavior change AND new budget

---

## Execution Checklist

When running full discovery process:

- [ ] Phase 1: Capability Frontier Mapping (2-3 hours)
- [ ] Phase 2: Segment-Problem Discovery (8-10 hours, 15 segments)
- [ ] Phase 3: Business Model Generation (6-8 hours, top 25 opportunities)
- [ ] Phase 4: Market Validation (10-12 hours, top 50 opportunities)
- [ ] Phase 5: Inevitability Scoring (2-3 hours)
- [ ] Phase 6: Synthesis & Output (8-10 hours)

**Total estimated research time: 40-50 hours**

Can execute in iterations:
- **Sprint 1**: Phases 1-2 (discover landscape)
- **Sprint 2**: Phases 3-4 (generate and validate)
- **Sprint 3**: Phases 5-6 (score and synthesize)

---

## Meta-Instructions

**Prioritize businesses where:**
- AI is **native infrastructure**, not bolted on
- 10-100x cost reductions, not 10-20%
- **Workflow replacement** over enhancement
- Synthetic workers are **competitive advantage**, not just efficiency

**Constraints:**
- No crypto/web3 businesses
- No consumer social (focus B2B, prosumer)
- No hardware-dependent models
- Prefer high-margin software (>70% gross margin potential)
- Prefer businesses that scale with inference, not headcount

**Success criteria:**
- At least 10 opportunities with inevitability score > 30
- At least 3 opportunities actionable within 90 days
- At least 1 opportunity worth spinning out as venture-backed startup
- Clear time-to-revenue estimates for each

---

## Integration Points

**With web research capabilities:**
- Use WebSearch extensively for pain point mining
- Use WebFetch for detailed competitive analysis
- Use Grep for local codebase capability assessment

**With other skills:**
- **process-mapper**: Validate automation feasibility for specific workflows
- **research-to-essay**: Transform findings into thought leadership content
- **strategy-to-artifact**: Convert opportunity analysis into pitch decks

**With business context:**
- Flag opportunities with **BetterUp synergy** (internal tool → external product)
- Highlight **Catalyst packaging potential** (repeatable, teachable, scalable)
- Identify unfair advantages from domain expertise

---

## Common Use Cases

**Trigger patterns:**
- "Find AI business opportunities in [industry]"
- "What becomes possible with 2M context windows?"
- "Map the synthetic workforce opportunity space"
- "Identify inevitable AI-native businesses"
- "Where can we apply AI to replace entire job functions?"
- "What workflows become automatable in 6 months?"
- "Validate this AI business idea"
- "Calculate inevitability score for [opportunity]"

**Example execution:**

User: "Find AI business opportunities in legal services"

Response:
1. Load Phase 2: Opportunity Discovery
2. Focus on legal segment
3. Execute pain point research queries
4. Build problem matrix
5. Map to synthetic worker primitives
6. Generate 5-10 business concepts
7. Validate top 3 with market research
8. Calculate inevitability scores
9. Deliver ranked opportunities with GTM strategies

---

## Anti-Patterns

**Don't:**
- Chase 10-20% efficiency gains (not venture-scale)
- Bolt AI onto existing workflows (prefer replacement)
- Ignore adoption friction (score honestly)
- Skip competitive analysis (surprises kill startups)
- Assume capabilities without validation (use benchmarks)
- Create businesses requiring massive behavior change
- Focus on technology demos vs business models
- Ignore unit economics (must have path to profitability)

**Do:**
- Look for 10-100x cost reductions
- Design AI-native workflows from scratch
- Score inevitability rigorously
- Deep dive competitive landscape
- Validate capabilities with current benchmarks
- Find natural adoption paths
- Build real businesses, not features
- Model unit economics from day one

---

## Success Metrics

**Research succeeds when:**
- At least 10 high-scoring opportunities identified (>30)
- Market validation confirms buyer intent
- TAM/SAM estimates are defensible
- Competitive analysis reveals clear wedge
- Time-to-revenue is realistic
- Technical feasibility validated with benchmarks
- Economic models show path to profitability

**Business succeeds when:**
- Inevitability score proves accurate
- Market adopts faster than projected
- Unit economics improve with scale
- Synthetic workers deliver promised SLAs
- Customers achieve 10x+ ROI
- Competition validates space
- Clear path to market leadership

---

Ready to discover what's inevitable?

Choose your starting phase above, or ask: "Run full inevitability engine research on [domain/segment/opportunity]"
