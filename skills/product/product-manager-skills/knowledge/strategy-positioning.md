# Strategy & Positioning

Compressed knowledge module covering company/market research, positioning, product strategy, prioritization, and roadmap planning.

## Company & Market Research

### Company Research Framework

Research across 7 dimensions: Company Overview, Executive Quotes, Product Insights, Transformation Strategies, Organizational Impact, Future Roadmap, Product-Led Growth.

**Research steps:**
1. Define scope: company name, research purpose, 3 key questions
2. Gather overview: headquarters, industry, founding, size, key milestones
3. Extract executive quotes: CEO (vision), COO (operations), VP Product (strategy), Group PM (initiatives). Cite source + date. Prioritize last 12-24 months.
4. Document product insights: strategy overview, recent launches with market impact, product philosophy/principles
5. Identify transformation strategies: digital (architecture shifts), AI (ML in product), Agile (methodology adoption)
6. Map organizational PM impact: PM role in strategic decisions, cross-functional collaboration model, career paths
7. Analyze future roadmap: planned initiatives, anticipated challenges, competitive threats
8. Document PLG insights: self-serve onboarding, data-driven decisions, activation/retention/expansion patterns
9. Synthesize: 3 strategic principles, 3 PM lessons, unanswered questions

**Source priority:** Earnings transcripts > podcast interviews > conference talks > executive blog posts > LinkedIn > company website. Go deeper than "About Us" pages.

### PESTEL Analysis

Six macro-environmental factors. Define scope first: product name, analysis purpose, geographic scope, time horizon.

| Factor | Key Questions | Example Sources |
|--------|--------------|-----------------|
| **Political** | Government policies, stability, trade regs, taxation | Legislative databases, trade reports |
| **Economic** | GDP growth, inflation, exchange rates, consumer spending | Census Bureau, BLS, World Bank |
| **Social** | Demographics, cultural trends, lifestyle shifts, attitudes | Pew Research, demographic studies |
| **Technological** | Advancements, R&D activity, automation, digital adoption | Gartner, industry reports |
| **Environmental** | Climate impact, sustainability, resource scarcity, green regs | If impact is minimal, say so honestly |
| **Legal** | Compliance (GDPR, AI Act), IP, employment law, safety regs | Legal databases, regulatory filings |

**For each factor:** State the specific impact on your product and what strategic action it implies. Generic statements ("regulations exist") are useless.

**Synthesis output:** Top 3 opportunities (with actions), top 3 threats (with mitigations), 3 strategic recommendations. Reassess annually or on major external events.

### TAM/SAM/SOM Calculation

Three-tier market sizing with citation-backed data.

**TAM** = Total market demand at 100% capture. Broadest possible.
**SAM** = TAM narrowed by geography, firmographics, product constraints. "Who can we actually reach?"
**SOM** = SAM narrowed by competition, GTM capacity. "What can we capture in 1-3 years?" Typically 1-20% of SAM in Year 1-3.

**Calculation process:**
1. Define problem space (B2B SaaS, consumer fintech, healthcare, etc.)
2. Select geographic region (US = Census/BLS data; EU = Eurostat; Global = World Bank/IMF)
3. Identify industry segments with population + revenue data
4. Narrow to target customer segment with firmographics/demographics

**Output format:** For each tier, show population estimate, market size ($), calculation math, source citation with URL, and key assumptions.

**Year 1-3 projections for SOM:** Include customer count and revenue. Ground in GTM constraints (sales capacity, conversion rates, marketing budget).

**Data sources:** US Census Bureau, BLS, IBISWorld, Statista, Gartner, Forrester, World Bank, Eurostat.

## Product Positioning

### Geoffrey Moore Positioning Statement

Two-part structure from *Crossing the Chasm*:

**Value Proposition:**
- **For** [specific target customer/persona]
- **that need** [underserved need -- pains, gains, JTBD]
- [product name]
- **is a** [product category]
- **that** [benefit statement -- outcomes, not features]

**Differentiation Statement:**
- **Unlike** [primary competitor or actual substitute behavior]
- [product name]
- **provides** [unique differentiation -- outcomes, not features]

### Stress Tests (apply to every draft)

1. Would the target customer recognize themselves in the "For" statement?
2. Can you point to research validating the need?
3. Does the category anchor you against the right competitors (or box you in)?
4. Is differentiation provable with a demo, case study, or data?
5. Does this positioning help answer "Should we build feature X?"

### Positioning Workshop Flow (Interactive)

5-question discovery sequence:
1. **Target customer segment** -- B2B SMB / B2B Enterprise / B2C mass / B2C niche (or custom)
2. **Underserved need** -- Adapted to segment from Q1 (time waste, lack of visibility, compliance burden, costly inefficiency)
3. **Product category** -- Anchors buyer evaluation. Pick existing category unless you have strong rationale for category creation.
4. **Key benefit** -- Outcome, not feature. Must be measurable (time saved, errors reduced, cost cut).
5. **Competitive differentiation** -- Name the actual competitor or substitute behavior. Differentiate on outcomes.

Output: Complete positioning statement + one-sentence summary + stress-test checklist + next steps (test with 5 customers, share with stakeholders, apply to artifacts).

### Positioning Quality Criteria

- Target specificity: describable to a recruiter
- Need clarity: emotionally resonant, not generic
- Category fit: helps buyer evaluation, not "next-generation platform"
- Outcome focus: what user gets, not what product has
- Competitor honesty: real alternative buyers consider
- Differentiation durability: not copyable in 6 months

## Product Strategy

### Strategy Session Phases (2-4 week process)

**Phase 1: Positioning & Market Context (Days 1-2)**
- Run positioning workshop. Define proto-personas. Map JTBD.
- Decision gate: Enough customer context? If NO, run 5-10 discovery interviews (+1 week).

**Phase 2: Problem Framing & Validation (Days 3-5)**
- Run problem framing canvas. Create formal problem statement. Optional: customer journey map.
- Decision gate: Problem validated? If NO, run discovery interviews (+1 week).

**Phase 3: Solution Exploration (Week 2, Days 1-3)**
- Generate opportunity solution tree (3 opportunities, 3 solutions each, POC recommendation). Define epic hypotheses.
- Decision gate: Need to test solutions? If YES (high uncertainty), run experiments (+1-2 weeks).

**Phase 4: Prioritization & Roadmap (Week 2, Days 4-5)**
- Choose prioritization framework. Score and rank epics. Sequence roadmap by release. Optional: TAM/SAM/SOM for exec presentations.

**Phase 5: Stakeholder Alignment (Week 3)**
- Present strategy: positioning + problem + solutions + prioritization + roadmap.
- Include "What's NOT on roadmap and why." Refine based on feedback.

**Phase 6: Execution Planning (Week 4)**
- Break top epic using splitting patterns (workflow, CRUD, business rules). Write user stories with acceptance criteria. Plan first sprint.

**Decision gates are mandatory.** Skipping them causes building solutions to unvalidated problems or wasting time on low-uncertainty activities.

## Prioritization

### Framework Selection Matrix

| Context | Recommended Framework | Why |
|---------|----------------------|-----|
| Pre-PMF, minimal data, small team | **ICE** or **Value/Effort matrix** | Lightweight, gut-check, fast scoring |
| Early PMF, some data, aligned team | **RICE** | Structured but not overwhelming; balances data + speed |
| Mature product, rich data | **Opportunity Scoring** or **Kano** | Leverages analytics, customer surveys |
| Multiple stakeholders, misaligned | **Weighted Scoring** or **Buy-a-Feature** | Transparent, consensus-building |
| Large org, cross-team dependencies | **Cost of Delay** or **Impact Mapping** | Handles coordination complexity |
| Strategic bets vs. quick wins | **Value/Effort matrix** | Visual, intuitive for tradeoff conversations |

### RICE Scoring

Formula: `(Reach x Impact x Confidence) / Effort`
- **Reach:** Users affected per month/quarter
- **Impact:** 1 (minimal), 2 (high), 3 (massive)
- **Confidence:** 50% (low data), 80% (good data), 100% (certain)
- **Effort:** Person-months (include design, eng, QA)

Use RICE as input, not automation. PM judgment overrides scores when strategic context requires it. Always adjust for strategic fit after raw scoring.

### Prioritization Decision Logic

4-question assessment to select framework:
1. Product stage (pre-PMF / early PMF / mature / multi-product)
2. Team context (small + focused / cross-functional aligned / stakeholders misaligned / large org)
3. Primary challenge (too many ideas / stakeholder disagreement / no data-driven process / strategic vs. tactical tradeoffs)
4. Data availability (minimal / some / rich)

Stick with one framework 6-12 months. Reassess only when stage or context changes.

## Roadmap Planning

### Roadmap Types

| Type | Structure | Best For |
|------|-----------|----------|
| **Now/Next/Later** | Committed / High confidence / Exploration | Agile teams, uncertainty, continuous discovery |
| **Theme-Based** | Strategic themes (Retention, Enterprise, Mobile) | Exec communication, strategic intent |
| **Timeline (Quarters)** | Q1: A, B; Q2: C, D; Q3: E, F | Resource planning, stakeholder comm |
| **Feature-Based** | Lists features without context | Anti-pattern. No strategic narrative. |

### Roadmap Planning Process (5 phases, 1-2 weeks)

**Phase 1: Gather Inputs (Days 1-2)**
- Business goals: top 3 company priorities, key metrics, strategic bets
- Customer problems: top 3-5 validated pain points (from discovery)
- Technical constraints: blockers, enabling investments, migrations
- Stakeholder requests: sales, marketing, CS inputs (not yet committed)

**Phase 2: Define Initiatives (Days 3-4)**
- Write epic hypotheses: "We believe [building X] for [persona] will achieve [outcome] because [assumption]."
- T-shirt size effort: S (1-2 wk), M (3-4 wk), L (2-3 mo), XL (3+ mo)
- Map each epic to primary business outcome

**Phase 3: Prioritize (Day 5)**
- Select framework using prioritization advisor
- Score all epics collaboratively (PM + eng + product leadership)
- Adjust scores for strategic fit (strategic overrides are legitimate)

**Phase 4: Sequence (Days 6-7)**
- Map dependencies (technical and logical)
- Assign to Now (committed), Next (high confidence), Later (exploration)
- Validate sequence with engineering for feasibility

**Phase 5: Communicate (Week 2)**
- Presentation structure: strategic context, roadmap overview, per-quarter deep dive, what's NOT on roadmap (and why), dependencies and risks
- Focus on strategic narrative: "Here's why X over Y"
- Frame as plan, not commitment: "Subject to change based on learning"
- Gather feedback, refine, publish internally (and optionally externally in Now/Next/Later format)

## Quality Gates

### Positioning Anti-Patterns
- **"For Everyone"** -- No one feels it's for them. Pick the first segment; expand later.
- **Feature Creep in Benefits** -- "AI, automation, analytics" is a feature list. Lead with outcome.
- **Imaginary Competitor** -- "Unlike outdated legacy systems" is a straw man. Name the actual alternative.
- **Category Confusion** -- "Next-generation platform for digital transformation" has no mental shelf. Pick a known category or commit to category creation.
- **Differentiation Without Proof** -- "Revolutionary AI" without evidence is noise. Make it falsifiable.

### Research Anti-Patterns
- **Surface-Level Research** -- Find executive interviews and product blogs, not just "About Us" pages.
- **No Citations** -- Always cite source + date. Unverifiable = low credibility.
- **Analysis Without Action** -- PESTEL and company research must end in strategic recommendations, not just lists.
- **Outdated Information** -- Prioritize sources from last 12-24 months.

### Market Sizing Anti-Patterns
- **TAM Without Citations** -- Cite industry reports (Gartner, IBISWorld, Statista) with URLs.
- **SOM = SAM** -- No market has zero competition. SOM = 1-20% of SAM in Year 1-3.
- **No Population Estimates** -- Always include customer counts alongside dollar amounts.
- **Ignoring GTM Constraints** -- Ground SOM in sales capacity, conversion rates, marketing budget.

### Prioritization Anti-Patterns
- **Wrong Framework for Stage** -- Pre-PMF startup using weighted scoring with 10 criteria kills speed.
- **Framework Whiplash** -- Switching frameworks every quarter causes confusion. Stick for 6-12 months.
- **Scores as Gospel** -- Scores are input, not automation. Strategic context overrides.
- **Solo PM Scoring** -- Collaborative scoring (PM + design + eng) builds buy-in.
- **HiPPO Prioritization** -- Any framework beats "who shouts loudest."

### Roadmap Anti-Patterns
- **Feature-Driven Roadmap** -- Frame epics as hypotheses with success metrics, not feature names.
- **Roadmap as Commitment** -- Communicate as strategic plan, subject to change based on learning.
- **No Dependencies Mapped** -- Validate sequence with engineering. Unmapped deps = blocked quarters.
- **Solo PM Roadmap** -- Gather inputs from all stakeholders (Phase 1), present draft for feedback (Phase 5).
- **Strategy Without Exec Sponsorship** -- Secure exec commitment upfront. Schedule alignment presentation before starting.

---

## Interaction Rules (Coaching Mode)

When coaching is active for strategy and positioning topics, use these rules.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| Positioning statement uses generic differentiators ("best", "leading", "innovative") | Push: "Your competitor could paste this on their site. What's the one thing only you can claim?" | User names a concrete, verifiable differentiator |
| Roadmap has no evidence link to user outcomes | Challenge: "Which items on this roadmap came from user research vs. stakeholder requests?" | User identifies the evidence source per item |
| Prioritization uses a single framework without context | Push: "Why this framework? What stage is the product at, and does this framework fit?" | User justifies framework choice for their stage |
| TAM/SAM/SOM uses top-down estimates only | Challenge: "What's your bottom-up estimate? How many specific customers can you name today?" | User provides bottom-up calculation or named accounts |
| Strategy session has no "what we're NOT doing" | Push: "Strategy is as much about what you cut. Name 3 things you're explicitly choosing not to do." | User names specific exclusions |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
