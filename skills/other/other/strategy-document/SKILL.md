---
name: strategy-document
description: >
  Write structured strategic documents for small and medium businesses.
  Produces SWOT analyses, lean business plans, OKRs, and competitive analyses.
  Each mode has a defined structure and quality bar. Use when a business needs
  to articulate strategy, set goals, analyse competition, or plan for growth.
  Outputs actionable documents, not generic frameworks.
---

# Strategy Document Writer

Produces strategic documents that are specific enough to act on. The quality bar: every statement should be falsifiable ("We have 3 React developers with 10+ years experience" vs "We have a strong team") and every recommendation should be implementable within a defined timeframe.

## Process

### Step 1: Determine the mode

Ask the user which document type they need:

1. **SWOT analysis** — assess current position
2. **Business plan** (lean or full) — articulate the business model
3. **OKRs / Goals** — set measurable objectives
4. **Competitive analysis** — understand the market landscape

If the user is unsure, ask what decision they are trying to make. That usually reveals the right mode:
- "Should we enter this market?" -> Competitive analysis + SWOT
- "What should we focus on this quarter?" -> OKRs
- "We need funding / a partner deck" -> Business plan
- "Something feels off but I can't pinpoint it" -> SWOT

### Step 2: Gather context

Ask for:
- Business name, industry, size (team, revenue if comfortable sharing)
- Current situation (what prompted this exercise?)
- Key competitors (if known)
- Time horizon (this quarter, this year, 3-year)
- Audience for the document (internal team, board, investors, bank, personal clarity)

The audience determines the level of detail. A bank wants financial projections. A founder wants clarity. A team wants direction.

### Step 3: Draft and validate

Write the document, then review every entry against the specificity test: could this statement apply to any business in the industry? If yes, it is too vague. Rewrite with the user's specific context.

---

## Mode 1: SWOT Analysis

### Structure

Present as a 2x2 grid with 3-5 points per quadrant. Each point is one sentence — specific and actionable.

```
             HELPFUL                    HARMFUL
          to achieving objectives    to achieving objectives

INTERNAL  STRENGTHS                  WEAKNESSES
(origin)  - ...                      - ...
          - ...                      - ...

EXTERNAL  OPPORTUNITIES              THREATS
(origin)  - ...                      - ...
          - ...                      - ...
```

**Internal** (Strengths, Weaknesses) = things the business controls: team skills, processes, technology, finances, culture, IP.

**External** (Opportunities, Threats) = things the business does not control: market trends, competitors, regulation, economic conditions, technology shifts.

### Quality bar for entries

| Too vague | Specific and useful |
|-----------|-------------------|
| "Strong team" | "3 developers with 10+ years React experience; only 1 has backend skills" |
| "Good reputation" | "4.8 Google rating from 127 reviews; 94% client retention over 3 years" |
| "Growing market" | "Australian SME SaaS market growing 12% annually (IBISWorld 2025)" |
| "Competition" | "Competitor X launched a free tier in Q4 2025, capturing 200+ of our target segment" |
| "Cash flow issues" | "Average debtor days: 58; target: 30. $120K outstanding beyond 60 days" |

Every entry should pass the "so what?" test — it must be clear why this point matters for strategic decisions.

### The "So What?" Section

After the grid, add a section that translates findings into actions:

**Strategic implications:**
- Which strengths can be leveraged against which opportunities? (attack)
- Which weaknesses are exposed by which threats? (defend)
- What should the business start doing, stop doing, or change?

This is the most valuable part of a SWOT. The grid without implications is an exercise in categorisation, not strategy.

### Anti-patterns

- Listing the same point in both Strengths and Opportunities (if it is internal, it is a strength)
- Including items the business cannot influence in Strengths/Weaknesses
- Generic entries that apply to every business in the industry
- No implications section — the grid alone is not actionable

---

## Mode 2: Business Plan

### Lean format (one page)

Use when the audience is the founder or a small team needing clarity. One paragraph per section, no padding.

| Section | What to write |
|---------|--------------|
| **Problem** | What pain exists? Who feels it? How do they cope today? |
| **Solution** | What does the business offer? In one sentence. |
| **Key Metrics** | 3-5 numbers that indicate health (MRR, churn, CAC, LTV, NPS) |
| **Unique Value Prop** | Why this business over alternatives? One sentence. |
| **Channels** | How do customers find you? Rank by effectiveness. |
| **Revenue Streams** | How does money come in? List each stream with approximate % of total. |
| **Cost Structure** | Top 5 cost categories with approximate monthly/annual figures. |
| **Unfair Advantage** | What cannot be easily copied? (team expertise, proprietary data, network effects, regulatory position) |

The test for each section: if you cannot say it in one paragraph, you do not understand it well enough yet. Rewrite until you can.

### Full format

Adds to the lean format:

- **Executive Summary** (write last — it summarises everything else)
- **Market Analysis** — TAM/SAM/SOM with sources, customer segments, market trends
- **Financial Projections** — 12-month P&L, cash flow forecast, break-even analysis
- **Team** — key people, their relevant experience, gaps to fill
- **Milestones** — what happens in the next 3, 6, and 12 months with specific deliverables

### Writing principles for plans

- Present tense for current state, future tense for plans. Never past tense for the core model.
- Financial projections must state assumptions explicitly. "$50K MRR by month 12" needs "assuming 15% monthly growth from current $12K base and 5% churn."
- Acknowledge risks. Investors and lenders trust founders who see the dangers, not those who pretend they do not exist.
- No aspirational filler. "We aim to be the leading provider" is not a plan. "We will acquire 200 paying customers in 12 months through Google Ads ($5K/month budget, target $25 CAC)" is a plan.

---

## Mode 3: OKRs and Goals

### Structure

```
OBJECTIVE: [Qualitative, inspiring, time-bound]

  KR1: [Quantitative, measurable, has a number]
  KR2: [Quantitative, measurable, has a number]
  KR3: [Quantitative, measurable, has a number]
```

Typically 3-5 Objectives per quarter, each with 3-5 Key Results.

### Objectives

- Qualitative and inspiring — describes the desired future state
- Time-bound (usually one quarter)
- Ambitious but achievable with stretch effort (70% completion = healthy)

| Too vague | Specific |
|-----------|---------|
| "Improve our marketing" | "Establish a predictable inbound lead pipeline by end of Q2" |
| "Grow the business" | "Expand into the Brisbane market with a repeatable sales process by Q3" |
| "Be more efficient" | "Eliminate manual reporting bottlenecks across all client accounts by Q2" |

### Key Results

- Quantitative with a specific target number
- Measurable — you can check at quarter end whether it was achieved
- Outcomes, not tasks

| Task (wrong) | Outcome (right) |
|--------------|----------------|
| "Launch the new website" | "Achieve 1,000 monthly organic visitors to the new site" |
| "Hire 2 developers" | "Reduce average feature delivery time from 3 weeks to 1 week" |
| "Run Google Ads campaign" | "Generate 50 qualified leads at under $30 CAC" |
| "Write 12 blog posts" | "Grow organic traffic 40% (800 to 1,120 monthly sessions)" |

Tasks are the activities you do to achieve Key Results. They belong on a project plan, not in OKRs.

### Scoring

At quarter end, score each KR from 0.0 to 1.0:
- 0.0-0.3: Failed to make meaningful progress
- 0.4-0.6: Made progress but fell short
- 0.7-0.9: Delivered strong results (this is the target zone)
- 1.0: Hit the target exactly (may indicate the target was too easy)

If every OKR scores 1.0, the goals were not ambitious enough. If every OKR scores below 0.3, they were unrealistic or the wrong priorities.

---

## Mode 4: Competitive Analysis

### Structure

Start with a comparison matrix, then interpret it.

**Comparison matrix:**

| Factor | Your Business | Competitor A | Competitor B | Competitor C |
|--------|--------------|-------------|-------------|-------------|
| Price point | $X/mo | $Y/mo | $Z/mo | Free tier + $W/mo |
| Key feature 1 | Yes | Yes | No | Partial |
| Key feature 2 | No | Yes | Yes | Yes |
| Target market | AU SMEs | Enterprise | Startups | All segments |
| Strength | Personal service | Scale | Price | Brand recognition |
| Weakness | Small team | Impersonal | Limited features | Slow support |

### Interpretation sections

**Where you win:** Specific advantages with evidence. "Faster onboarding (3 days vs industry average of 2 weeks)" not "better service".

**Where you lose:** Honest assessment. "Competitor A has 10x our development team; we cannot match their feature velocity" is more useful than pretending the gap does not exist.

**Where you differentiate:** What you do that others structurally cannot or choose not to. This is the strategic gold — it informs positioning, messaging, and product decisions.

**Recommended actions:** Based on the analysis, what should change? New features to build, segments to target or avoid, pricing adjustments, partnership opportunities.

### Research sources

- Competitor websites (pricing pages, feature lists, case studies)
- Review sites (G2, Capterra, Google Reviews, ProductHunt)
- Job listings (reveal their priorities and gaps)
- Social media and content (positioning, audience, tone)
- Industry reports (market size, growth rates, trends)

If the user has access to competitors' actual customers (through industry networks, forums, social media), first-hand feedback is more valuable than any published report.

---

## Writing Principles (All Modes)

**Specific over vague.** Every claim needs a number, a name, or a concrete example. "Strong growth" is not strategy — "40% revenue increase from $850K to $1.19M" is strategy.

**Evidence over opinion.** "We believe the market is growing" vs "The AU SaaS market grew 12% in 2025 (source)." If you cannot find evidence, say so — an honest gap is better than a fabricated claim.

**Actionable over aspirational.** Every section should answer "what do we do with this information?" If a SWOT entry or competitive insight does not lead to a decision or action, it is not worth including.

**Honest about weaknesses.** Strategy documents that only list strengths are useless. The value is in seeing the full picture — including the uncomfortable parts. Investors, partners, and teams all trust honesty more than polish.

**Appropriate length.** A lean business plan is one page. A SWOT is one page plus implications. OKRs are a few pages at most. Competitive analysis scales with the number of competitors. Do not pad for length — every sentence must earn its place.

## Example: SWOT Strength Entry

**Too vague:**
> Strong digital presence and good online reputation.

**Right approach:**
> 4.8 average Google rating from 127 reviews (highest among Newcastle web agencies). Website generates 35 qualified leads per month organically, with a 12% conversion rate to paying clients. Social media following of 2,400 across LinkedIn and Instagram, with 6.2% average engagement rate on case study posts.

The second version gives the reader three data points they can compare against competitors, benchmark against industry averages, and track over time.
