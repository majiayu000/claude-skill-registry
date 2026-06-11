---
name: csuite
description: "C-suite executive decision support: strategy, technology, growth, competitive intelligence, project evaluation."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    # Strategy/CEO
    - "should we"
    - "evaluate opportunity"
    - "trade-off"
    - "worth it"
    - "invest in"
    - "strategy"
    # Technology/CTO
    - "build vs buy"
    - "vendor evaluation"
    - "adopt"
    - "technology choice"
    - "tech stack"
    # Growth/CMO
    - "grow audience"
    - "growth"
    - "brand"
    - "positioning"
    - "community building"
    # Competitive
    - "competitive analysis"
    - "market landscape"
    - "differentiation"
    # Evaluation
    - "feasibility"
    - "effort estimate"
    - "ROI"
    - "priority"
    - "project evaluation"
    - "go no go"
    - "viability"
  not_for: "micro library choices (use decision-helper), writing content, SEO of specific posts"
  complexity: Medium
  category: decision-support
  pairs_with:
    - customer-support
    - finance
    - hr
    - marketing
    - operations
    - sales
    - product-management
---

# C-Suite Decision Support

Umbrella skill for all executive decision-making: CEO-level strategy, CTO-level technology choices, CMO-level growth planning, competitive intelligence, and project evaluation. Each domain loads its own reference files on demand -- this skill detects the mode, loads the right references, and executes the appropriate framework.

**Scope**: Business decisions with meaningful consequences. Use decision-helper for technical architecture micro-choices, domain agents for code, voice-writer for content, and systematic-debugging for debugging.

---

## Mode Detection

Classify the user's request into exactly one mode before proceeding. If the request spans multiple modes, choose the primary one and note the secondary.

| Mode | Signal Phrases | Role Lens |
|------|---------------|-----------|
| **STRATEGY** | Market entry, partnerships, resource allocation, opportunity, "should I/we", strategic pivots, investment | CEO |
| **TECHNOLOGY** | Build vs buy, vendor, SaaS, tech stack, architecture, adopt, technology choice | CTO |
| **GROWTH** | Content strategy, audience, SEO, marketing, brand, community, positioning, channel | CMO |
| **COMPETITIVE** | Competitor, competition, market landscape, differentiation, positioning against, market share | Cross-role |
| **EVALUATION** | Feasibility, effort estimate, ROI, priority, go/no-go, viability, "is it worth it" | Cross-role |

---

## Reference Loading Table

Load references based on the detected mode. Load only the references required by the mode.

| Signal | Mode | Reference |
|--------|------|-----------|
| Market entry, partnerships, resource allocation, opportunity | STRATEGY | `references/strategic-frameworks.md`, `references/decision-matrices.md` |
| Build vs buy, vendor, SaaS, tech stack, architecture | TECHNOLOGY | `references/tco-framework.md`, `references/vendor-evaluation.md` |
| Content, audience, SEO, marketing, brand, community | GROWTH | `references/audience-segmentation.md`, `references/channel-evaluation.md` |
| Competitor, market landscape, positioning, differentiation | COMPETITIVE | `references/competitive-mapping.md`, `references/market-positioning.md` |
| Feasibility, effort, ROI, priority, go/no-go | EVALUATION | `references/feasibility-scoring.md`, `references/roi-frameworks.md` |

---

## Instructions

### Mode: STRATEGY (CEO)

**Framework**: FRAME -> ANALYZE -> DECIDE

**Phase 1: FRAME** -- Convert the user's question into a structured decision with clear stakes and timeline.

- Name the actual decision (users present symptoms; the real decision is broader)
- Identify irreversibility -- reversible decisions deserve less analysis
- Set a time horizon -- 3-month and 3-year decisions need different frameworks
- Classify the decision type: Expansion, Partnership, Allocation, Pivot, or Timing
- Get the user to state: options (2-4), default path risk, deadline, and what makes it hard

**Gate**: Decision framed as one sentence. Options listed (2-4). Type classified.

**Phase 2: ANALYZE** -- Evaluate each option through multiple lenses with evidence.

For each option, assess: Upside (best realistic + expected outcome), Downside (worst realistic + recovery path + irreversible losses), Requirements (resources, assumptions, dependencies), Opportunity Cost (what you cannot do).

Separate facts from assumptions. Quantify where possible. Load reference files for scoring matrices and strategic frameworks.

**Gate**: All options analyzed. Facts and assumptions labeled. Opportunity costs explicit.

**Phase 3: DECIDE** -- Synthesize into a clear recommendation.

- Apply the reversibility test: one-way doors need high confidence; two-way doors can act faster with a checkpoint
- Produce: Recommendation (one sentence), Confidence (High/Medium/Low), Why this option (2-3 reasons), What must be true (invalidating assumptions), First move (48-hour action), Revisit trigger
- State explicitly what would change the recommendation

**Gate**: Recommendation stated. First action identified. Revisit trigger set.

---

### Mode: TECHNOLOGY (CTO)

**Framework**: SCOPE -> EVALUATE -> RECOMMEND

**Phase 1: SCOPE** -- Define the capability needed, stripped of solution bias.

- Start with the need, not the product ("we need reliable async delivery" not "we need Kafka")
- Quantify hard requirements (latency, throughput, compliance)
- Identify the real driver (build vs buy is sometimes "convince management" or "hire someone")
- List actual options: build from scratch, build on OSS, buy SaaS, buy + customize, do nothing

**Gate**: Capability defined without solution bias. Options enumerated. Hard requirements quantified.

**Phase 2: EVALUATE** -- Score options on dimensions that matter for technology decisions.

- Total cost of ownership at Year 3, not sticker price (the "free" OSS needing a full-time engineer is expensive)
- Score on: Fit (5), TCO (4), Operational burden (4), Team capability (3), Lock-in risk (3), Time to value (3), Flexibility (2)
- Apply the build-vs-buy heuristic: core competency, requirements stability, team capacity, timeline, scale, compliance

Load `references/tco-framework.md` for TCO templates and `references/vendor-evaluation.md` for vendor scorecards.

**Gate**: TCO estimated. Dimensions scored. Build-vs-buy heuristic applied.

**Phase 3: RECOMMEND** -- Deliver a clear recommendation with reasoning.

- Present the weighted scoring matrix
- State: Decision, Confidence, Why this option, Watch-for risks, Migration path, First step
- Define exit criteria: when to reconsider for each option type

**Gate**: Recommendation stated. Exit criteria defined. First step identified.

---

### Mode: GROWTH (CMO)

**Framework**: ASSESS -> STRATEGIZE -> PLAN

**Phase 1: ASSESS** -- Understand current state before recommending.

- Audit: publications, content volume, existing audience, active channels, performance data
- Identify the binding constraint: Discovery, Content, Conversion, Retention, or Capacity
- Creator capacity is the binding constraint -- recommend what one person can sustain

**Gate**: Current state audited. Binding constraint identified.

**Phase 2: STRATEGIZE** -- Design an approach matching capacity and constraint.

- Solve the constraint, not everything -- address one binding constraint well
- Prefer compound strategies (SEO, evergreen, community) over one-shot campaigns
- Recommend maximum 3 active channels with format, cadence, success metric, and effort estimate

Load `references/audience-segmentation.md` for ICP scoring and `references/channel-evaluation.md` for channel matrices.

**Gate**: Strategy selected. Maximum 3 channels. Effort estimated against capacity.

**Phase 3: PLAN** -- Convert strategy into a 90-day executable plan.

- Define one primary metric and 2-3 secondary metrics
- Break into 30-day phases: Foundation (days 1-30), Execution (31-60), Evaluate (61-90)
- Set explicit abandon criteria, pivot triggers, and double-down conditions

**Gate**: 90-day plan with checkpoints. Primary metric defined. Abandon criteria explicit.

---

### Mode: COMPETITIVE

**Framework**: MAP -> ANALYZE -> POSITION

**Phase 1: MAP** -- Build a structured picture of the competitive landscape.

- Define the competitive arena: what you compete on, who you serve, where you compete
- Tier competitors: Direct (full analysis), Adjacent (positioning only), Aspirational (strategy extraction), Emerging (watch list)
- Map the landscape before zooming in -- analyzing one competitor in isolation misses gaps

**Gate**: Arena defined. Competitors identified and tiered. At least 2 direct competitors mapped.

**Phase 2: ANALYZE** -- Extract actionable intelligence from behavior, not surface impressions.

- Focus on what they DO, not what they SAY (pricing, launches, cadence reveal strategy)
- Analyze for gaps, not imitation -- find what competitors miss or do poorly
- For each direct competitor: product/content analysis, audience analysis, strategy signals

Load `references/competitive-mapping.md` for landscape templates and `references/market-positioning.md` for positioning frameworks.

**Gate**: Direct competitors analyzed. Gaps and weaknesses identified.

**Phase 3: POSITION** -- Convert intelligence into defensible differentiation.

- Build a positioning map on two dimensions where you can differentiate
- Define: positioning statement, defensible advantages, vulnerable advantages, strategic gaps to exploit
- Set monitoring cadence: monthly (direct competitors), quarterly (full landscape), trigger-based (major moves)

**Gate**: Positioning map built. Differentiation strategy defined. Monitoring cadence set.

---

### Mode: EVALUATION

**Framework**: SCOPE -> EVALUATE -> VERDICT

**Phase 1: SCOPE** -- Define the project and what success looks like.

- Define done before estimating effort ("build an app" is not a project)
- Separate the vision from the MVP -- evaluate the minimum viable version
- Name the binding constraint (time, money, skills, attention)
- Define success criteria, the problem it solves, who benefits, and why now

**Gate**: Project defined with measurable success criteria. MVP scope identified. Binding constraint named.

**Phase 2: EVALUATE** -- Assess feasibility, estimate effort, calculate ROI.

- Feasibility across three dimensions: Technical, Resource, Market (each High/Medium/Low confidence)
- Effort in ranges, not points ("2-5 weeks, most likely 3")
- Include hidden costs: learning curve, integration, testing, documentation (add 20-40%)
- ROI: direct value, indirect value, strategic value vs. build cost, ongoing cost, opportunity cost

Load `references/feasibility-scoring.md` for the three-dimension model and `references/roi-frameworks.md` for estimation templates.

**Gate**: Feasibility assessed. Effort estimated in ranges. ROI calculated with confidence level.

**Phase 3: VERDICT** -- Deliver a clear go/no-go recommendation.

- Verdict: GO, GO WITH CONDITIONS, DEFER, or NO-GO
- Include: summary, key factors, conditions (if conditional), what would change the verdict, recommended next step
- For multiple projects: rank using RICE scoring (Reach * Impact * Confidence / Effort)

**Gate**: Verdict stated with confidence. Conditions specified. Next step identified.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Too many options | 5+ options creating paralysis | Eliminate obviously inferior options first. Get to 2-4 before running full framework. |
| Not enough information | User cannot answer framing questions | Identify 2-3 critical unknowns. Recommend time-boxed research sprint before deciding. |
| Analysis paralysis | Keeps adding criteria or second-guessing | Apply reversibility test. If reversible, recommend best current option with checkpoint. |
| Emotional attachment | User has already decided, wants validation | Name the pattern directly. Ask: stress-test the choice, or genuinely evaluate all options? |
| Comparing apples to oranges | Options at different abstraction levels | Normalize to the capability level. Compare what each option gives for the specific need. |
| Vendor lock-in fear | Over-weights lock-in, under-weights time-to-value | Quantify actual switching cost. Compare concrete switching cost against concrete speed benefit. |
| Build bias (NIH) | Team wants to build because it is more interesting | Apply core competency test: "If this disappeared, would customers notice?" |
| Vanity metrics | Optimizes followers/likes instead of outcomes | Redirect to "one metric that matters" -- what action should the audience take? |
| Scope creep during evaluation | Keeps adding features to project definition | Freeze scope at end of Phase 1. Additional features evaluate as v2. |
| Optimism bias | Effort estimates too low | Apply reference class test. If no similar project, add 50% to pessimistic estimate. |

---

## References

| Reference | When to Load | Content |
|-----------|-------------|---------|
| `references/strategic-frameworks.md` | STRATEGY mode: market entry, competitive dynamics, SWOT, OKR alignment | Porter's Five Forces, SWOT scoring, OKR alignment matrices |
| `references/decision-matrices.md` | STRATEGY mode: structured scoring, comparison, pre-mortem | Weighted decision matrices, ICE/RICE scoring, pre-mortem templates |
| `references/tco-framework.md` | TECHNOLOGY mode: TCO modeling, cost projections, build vs buy scorecard | TCO templates, hidden cost checklists, migration cost models |
| `references/vendor-evaluation.md` | TECHNOLOGY mode: vendor comparison, RFP criteria, integration complexity | Vendor scorecards, RFP criteria, red flag detection, contract checklist |
| `references/audience-segmentation.md` | GROWTH mode: audience analysis, ICP definition, persona development | ICP scoring matrix, persona templates, segmentation frameworks |
| `references/channel-evaluation.md` | GROWTH mode: channel selection, CAC/LTV modeling, content funnel | Channel scoring matrices, CAC/LTV models, funnel stage mapping |
| `references/competitive-mapping.md` | COMPETITIVE mode: landscape mapping, feature comparison, competitor profiling | Landscape map templates, feature matrices, activity tracker |
| `references/market-positioning.md` | COMPETITIVE mode: positioning strategy, differentiation scoring | Positioning maps, differentiation scoring, win/loss frameworks |
| `references/feasibility-scoring.md` | EVALUATION mode: feasibility assessment, risk evaluation, go/no-go | Three-dimension feasibility model, confidence calibration, decision tree |
| `references/roi-frameworks.md` | EVALUATION mode: effort estimation, ROI calculation, project comparison | T-shirt sizing, three-point estimation, risk-adjusted NPV |
