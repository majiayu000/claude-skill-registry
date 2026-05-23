---
name: startup-trend-prediction
description: "Analyze 2-3 year historical trends in technology, market, and business models to predict 1-2 years ahead. Uses pattern recognition, adoption curves, and cycle analysis to identify timing windows and emerging opportunities. History is cyclical - products and markets follow predictable patterns."
metadata:
  globs: |
    **/*.md
    **/research/**
    **/trends/**
    **/analysis/**
---

# Startup Trend Prediction

Systematic framework for analyzing historical trends to predict future opportunities. Look back 2-3 years to predict 1-2 years ahead.

**Modern Best Practices (Dec 2025)**:
- Triangulate: require 3+ independent signals, including at least 1 primary source (standards, regulators, platform docs).
- Separate leading vs lagging indicators; don’t overfit to social/media noise.
- Add hype-cycle defenses: falsification, base rates, and adoption constraints (distribution, budgets, compliance).
- Tie trends to a decision (enter / wait / avoid) with explicit assumptions and a review cadence.

---

## When to Use This Skill

| Trigger | Action |
|---------|--------|
| "When should I enter this market?" | Run timing analysis |
| "What's trending in [technology/market]?" | Run trend identification |
| "Is this trend rising or peaking?" | Run adoption curve analysis |
| "What comes after [current trend]?" | Run cycle prediction |
| "Historical patterns for [topic]" | Run pattern recognition |
| "2-3 year trends" or "predict 1-2 years" | Full trend prediction workflow |

---

## Quick Reference: Building a Trend View (Dec 2025)

### 1) Define the Decision

- What decision are we supporting: enter / wait / avoid?
- Horizon: {{HORIZON}}
- Buyer and market: {{BUYER}} / {{MARKET}}

### 2) Collect Signals (Leading vs Lagging)

| Signal | Type | What it indicates | Examples | Failure mode |
|--------|------|-------------------|----------|--------------|
| Regulation/standards | Leading | Constraints or enabling changes | Sector regulation, privacy law, ISO standards | Misreading scope/timeline |
| Platform primitives | Leading | New capability baseline | API/OS/cloud releases | Confusing announcement with adoption |
| Buyer behavior | Leading | Willingness to buy | Procurement patterns, RFPs | Sampling bias |
| Usage/revenue | Lagging | Real adoption | Public metrics, cohorts | Too slow to catch inflection |
| Media/social | Weak | Attention | Mentions, posts | Hype amplification |

### 3) Hype-Cycle Defenses

- Falsification: what evidence would prove the trend is not real?
- Base rates: how often do similar trends reach mass adoption?
- Adoption constraints: distribution, budget, switching costs, compliance, implementation complexity.

### 4) Market Sizing Sanity Checks

- Bottom-up first: #customers × willingness-to-pay × realistic penetration.
- Explicit assumptions: who pays, how much, and why you can reach them.

---

## Adoption Curve Framework

### Rogers Diffusion Model

```
                    ADOPTION CURVE
    │
    │                          ╭────────╮
    │                      ╭───╯Late    │
    │                  ╭───╯Majority    │
    │              ╭───╯Early          │
    │          ╭───╯Majority           │
    │      ╭───╯Early                  │
    │  ╭───╯Adopters                   │
    │──╯Innovators                     ╰──────
    │     │      │      │      │      │
    │   2.5%   13.5%   34%    34%    16%
    └─────────────────────────────────────────▶
                     TIME
```

### Position Identification

| Position | Market Penetration | Characteristics | Strategy |
|----------|-------------------|-----------------|----------|
| **Innovators** | <2.5% | Tech enthusiasts, high risk tolerance | Enter now, shape market |
| **Early Adopters** | 2.5-16% | Visionaries, want competitive edge | Enter now, premium pricing |
| **Early Majority** | 16-50% | Pragmatists, need proof | Enter with differentiation |
| **Late Majority** | 50-84% | Conservatives, follow herd | Compete on price/features |
| **Laggards** | 84-100% | Skeptics, forced adoption | Avoid or disrupt |

### Gartner Hype Cycle Mapping

```
                    HYPE CYCLE
    │
    │        Peak of
    │     Inflated        ╭─────────────
    │   Expectations  ╭───╯ Plateau of
    │            ╭────╯   Productivity
    │       ╭────╯
    │  ╭────╯         Slope of
    │──╯              Enlightenment
    │  Technology    ╲_____╱
    │   Trigger     Trough of
    │              Disillusionment
    └─────────────────────────────────────▶
                     TIME
```

| Phase | Duration | Action |
|-------|----------|--------|
| Technology Trigger | 0-2 years | Monitor, experiment |
| Peak of Inflated Expectations | 1-3 years | Caution, don't overbuild |
| Trough of Disillusionment | 1-3 years | Build foundations |
| Slope of Enlightenment | 2-4 years | Scale solutions |
| Plateau of Productivity | 5+ years | Optimize, commoditize |

---

## Cycle Pattern Library

### Technology Cycles (7-10 years)

| Cycle | Previous Instance | Current Instance | Pattern |
|-------|------------------|------------------|---------|
| Client → Cloud → Edge | Desktop → Web → Mobile | Cloud → Edge → On-device compute | Compute moves to data |
| Monolith → Services → Composables | SOA → Microservices | Microservices → Composable workflows | Decomposition continues |
| Batch → Stream → Real-time | ETL → Streaming | Streaming → Real-time decisioning | Latency shrinks |
| Manual → Assisted → Automated | CLI → GUI | Scripts → Workflow automation | Automation increases |

### Market Cycles (5-7 years)

| Cycle | Previous Instance | Current Instance | Pattern |
|-------|------------------|------------------|---------|
| Fragmentation → Consolidation | 2015-2020 point solutions | 2020-2025 platforms | Bundling/unbundling |
| Horizontal → Vertical | Horizontal SaaS | Vertical platforms | Specialization wins |
| Self-serve → High-touch → Hybrid | PLG pure | PLG + Sales | Motion evolves |

### Business Model Cycles (3-5 years)

| Cycle | Previous Instance | Current Instance | Pattern |
|-------|------------------|------------------|---------|
| Perpetual → Subscription → Usage | License → SaaS | SaaS → Usage-based | Payment follows value |
| Direct → Marketplace → Embedded | Direct sales | Marketplace → Embedded | Distribution evolves |

---

## Signal vs Noise Framework

### Strong Signals (High Confidence)

| Signal Type | Detection Method | Weight |
|-------------|-----------------|--------|
| VC funding patterns | Track quarterly investment | High |
| Big tech acquisitions | Monitor M&A announcements | High |
| Job posting trends | Analyze LinkedIn/Indeed data | High |
| GitHub activity | Stars, forks, contributors | High |
| Enterprise adoption | Gartner/Forrester reports | Very High |

### Moderate Signals (Validate)

| Signal Type | Detection Method | Weight |
|-------------|-----------------|--------|
| Conference talk themes | Track KubeCon, AWS re:Invent | Medium |
| Hacker News sentiment | Algolia search trends | Medium |
| Reddit discussions | Subreddit growth, sentiment | Medium |
| Influencer adoption | Key voices tweeting about | Medium |

### Weak Signals (Monitor)

| Signal Type | Detection Method | Weight |
|-------------|-----------------|--------|
| ProductHunt launches | Daily tracking | Low |
| Blog post frequency | Content analysis | Low |
| Podcast mentions | Episode scanning | Low |
| Media hype | TechCrunch, Wired articles | Low (often lagging) |

### Noise Filters

**Exclude from prediction**:
- Single viral tweet without follow-up
- PR-driven announcements without product
- Predictions from parties with financial interest
- Old data recycled as "new trend"

---

## Prediction Methodology

### Step 1: Define Scope

```markdown
Domain: [Technology / Market / Business Model]
Lookback Period: [2-3 years]
Prediction Horizon: [1-2 years]
Geography: [Global / Region-specific]
Industry: [Horizontal / Specific vertical]
```

### Step 2: Gather Historical Data

| Year | State | Key Events | Metrics |
|------|-------|------------|---------|
| {{YEAR-3}} | | | |
| {{YEAR-2}} | | | |
| {{YEAR-1}} | | | |
| {{NOW}} | | | |

### Step 3: Identify Patterns

- [ ] Linear growth/decline
- [ ] Exponential growth/decline
- [ ] Cyclical pattern
- [ ] S-curve adoption
- [ ] Plateau reached
- [ ] Disruption event

### Step 4: Generate Prediction

```markdown
## Prediction: [TOPIC]

**Thesis**: [1-2 sentence prediction]
**Confidence**: High / Medium / Low
**Timing**: [When this will happen]
**Evidence**: [3-5 supporting data points]
**Counter-evidence**: [What could invalidate]
```

### Step 5: Identify Opportunities

| Opportunity | Timing Window | Competition | Action |
|-------------|---------------|-------------|--------|
| {{OPP_1}} | {{WINDOW}} | Low/Med/High | Build/Watch/Avoid |
| {{OPP_2}} | {{WINDOW}} | | |

---

## Navigation

### Resources (Deep Dives)

| Resource | Purpose |
|----------|---------|
| [technology-cycle-patterns.md](resources/technology-cycle-patterns.md) | Technology adoption curves and cycles |
| [market-cycle-patterns.md](resources/market-cycle-patterns.md) | Market evolution and consolidation patterns |
| [business-model-evolution.md](resources/business-model-evolution.md) | Revenue model cycles and transitions |
| [signal-vs-noise-filtering.md](resources/signal-vs-noise-filtering.md) | Separating hype from substance |
| [prediction-accuracy-tracking.md](resources/prediction-accuracy-tracking.md) | Validating predictions over time |

### Templates (Outputs)

| Template | Use For |
|----------|---------|
| [trend-analysis-report.md](templates/trend-analysis-report.md) | Full trend prediction report |
| [technology-adoption-curve.md](templates/technology-adoption-curve.md) | Adoption stage mapping |
| [market-timing-assessment.md](templates/market-timing-assessment.md) | When to enter decision |
| [cyclical-pattern-map.md](templates/cyclical-pattern-map.md) | Historical pattern matching |
| [prediction-hypothesis.md](templates/prediction-hypothesis.md) | Prediction with evidence |
| [trend-opportunity-matrix.md](templates/trend-opportunity-matrix.md) | Trends → Opportunities |

### Data

| File | Contents |
|------|----------|
| [sources.json](data/sources.json) | Trend data sources (analyst reports, market data, filings, etc.) |

---

## Key Principles

### History Rhymes

Past patterns repeat with new technology:
- Client-server → Web apps → Mobile → On-device
- Mainframe → PC → Cloud → Distributed
- Manual → Scripted → Automated → Autonomous

### Timing Beats Being Right

Being right about a trend but wrong about timing = failure:
- Too early: Market not ready, burn runway
- Too late: Established players, commoditized
- Just right: Ride the wave

### Multiple Signals Required

Never bet on single signal:
- Funding + Hiring + GitHub activity = Strong signal
- Just media coverage = Hype, validate further
- Just VC interest = May be speculative

### Update Predictions

Predictions are living documents:
- Revisit quarterly
- Track accuracy over time
- Adjust for new data
- Document what changed and why

---

## Do / Avoid (Dec 2025)

### Do

- Use a decision horizon (enter/wait/avoid) and revisit quarterly.
- Track leading indicators and adoption constraints, not just hype.
- Write assumptions explicitly and update them when data changes.

### Avoid

- Extrapolating from a single platform, influencer, or funding headline.
- Treating “attention” as “adoption”.
- Market sizing without assumptions and bottom-up checks.

## What Good Looks Like

- Decision: one clear enter/wait/avoid call with horizon and owner.
- Evidence: 3+ independent signal types (not just media) and explicit confidence (strong/medium/weak).
- Assumptions: TAM/SAM/SOM with assumptions + sensitivity ranges; falsification criteria documented.
- Constraints: adoption blockers listed (distribution, budget, switching, compliance, implementation) with mitigations.
- Cadence: quarterly refresh with “what changed” and accuracy notes.

## Optional: AI / Automation

Use only when explicitly requested and policy-compliant.

- Topic modeling/clustering for large corpora; validate with primary sources and spot-checks.
- Summarization of reports; keep links and dates to avoid stale claims.

---

## Integration Points

### Feeds Into

- [startup-idea-validation](../startup-idea-validation/SKILL.md) - Market timing score
- [router-startup](../router-startup/SKILL.md) - Trend context for analysis
- [product-management](../product-management/SKILL.md) - Roadmap prioritization

### Receives From

- [startup-review-mining](../startup-review-mining/SKILL.md) - Pain point trends over time
- [startup-competitive-analysis](../startup-competitive-analysis/SKILL.md) - Competitor movement patterns
