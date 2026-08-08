---
name: dev-ai-coding-metrics
description: Measure and optimize AI coding agent impact — adoption tracking, DORA/SPACE for AI teams, ROI frameworks, DX surveys, benchmarking. Use when measuring AI tool effectiveness or building metrics programs.
---

# AI Coding Agent Metrics for Engineering Teams

Measure what matters when adopting AI coding tools. This skill provides metrics frameworks, measurement methodology, ROI models, and reporting templates for engineering managers, VPs of Engineering, and CTOs evaluating or scaling AI coding agents.

## When to Use This Skill

- Evaluating AI coding tool ROI before or after purchase
- Building a metrics program for AI-assisted development
- Reporting AI tool impact to leadership or board
- Designing controlled experiments to measure AI effectiveness
- Comparing productivity across AI-equipped and traditional teams
- Tracking adoption health and identifying stall patterns
- Assessing quality impact of AI-generated code
- Running developer experience surveys for AI tools

## Quick Reference

| Task | Reference | Asset |
|------|-----------|-------|
| **Track tool adoption** | adoption-metrics.md | adoption-survey-template.md |
| **Measure productivity** | productivity-metrics.md | metric-dashboard-template.md |
| **Monitor code quality** | quality-metrics.md | metric-dashboard-template.md |
| **Calculate ROI** | roi-framework.md | roi-calculator-template.md |
| **Assess developer experience** | developer-experience-metrics.md | adoption-survey-template.md |
| **Design experiments** | benchmarking-methodology.md | experiment-design-template.md |
| **Report to executives** | roi-framework.md | executive-report-template.md |
| **Measure AI coding impact** | this skill | — |
| **Context engineering for AI** | dev-context-engineering | — |
| **Per-task agent ROI** | ai-agents | — |
| **Observability for systems** | qa-observability | — |

---

## Core Metrics Taxonomy

Five measurement categories. Start with Adoption (you can't optimize what people aren't using), then layer in the others.

### 1. Adoption Metrics

Track whether and how developers use AI tools.

| Metric | Formula | Target (Mature) | Source |
|--------|---------|-----------------|--------|
| License Utilization | active_users / licensed_seats | >85% | License admin |
| DAU/WAU Ratio | daily_active / weekly_active | >0.6 | Tool telemetry |
| Feature Breadth | features_used / features_available | >0.5 | Tool telemetry |
| Acceptance Rate | suggestions_accepted / suggestions_shown | 25-35% | Copilot API / tool logs |
| Organic Usage Ratio | voluntary_sessions / total_sessions | >0.8 | Survey + telemetry |

**Deep dive**: references/adoption-metrics.md — 8 additional metrics, adoption curve phases, tool-specific tracking, stall patterns.

### 2. Velocity Metrics

Measure speed and throughput changes.

| Metric | Formula | Expected AI Impact | Source |
|--------|---------|-------------------|--------|
| Deploy Frequency | deploys / time_period | +15-30% | CI/CD pipeline |
| Lead Time for Changes | commit_to_production | -20-40% | Git + CI/CD |
| Cycle Time | ticket_start_to_deploy | -15-35% | Project management + Git |
| PR Throughput | merged_PRs / developer / week | +20-40% | Git platform |
| Time to First Commit | onboard_date_to_first_commit | -30-50% | Git + HR data |

**Deep dive**: references/productivity-metrics.md — DORA adaptations, SPACE framework, cycle time decomposition, confounding variables.

### 3. Quality Metrics

Track whether AI helps or hurts code quality.

| Metric | Formula | Watch Direction | Source |
|--------|---------|----------------|--------|
| Bug Density | bugs / KLOC | Should decrease | Issue tracker |
| Defect Escape Rate | prod_bugs / total_bugs | Should decrease | Issue tracker |
| Rework Rate | followup_PRs / total_PRs | Watch for increase | Git platform |
| Test Coverage | covered_lines / total_lines | Should increase | CI coverage |
| Vulnerability Rate | new_vulns / sprint | Watch for increase | SAST tools |

**Critical warning**: Early studies show mixed quality results. AI can increase velocity while *also* increasing bug density if guardrails are missing. Monitor both.

**Deep dive**: references/quality-metrics.md — complexity tracking, security metrics, technical debt, quality guardrails.

### 4. Economic Metrics

Calculate costs, benefits, and ROI.

| Metric | Formula | Benchmark | Source |
|--------|---------|-----------|--------|
| Cost per Seat | (license + infra + training) / developers | $20-50/dev/month | Finance |
| Hours Saved/Dev/Week | measured_or_estimated_time_savings | 2-8 hrs (varies widely) | Survey + telemetry |
| ROI | (net_benefits - costs) / costs × 100 | 100-300% yr1 (vendor data) | Calculated |
| Payback Period | total_investment / monthly_net_benefit | 2-6 months | Calculated |
| Break-Even Adoption | cost / (max_benefit × developers) | 25-40% of team | Calculated |

**Caveat**: Most published ROI figures come from tool vendors. Independent studies show lower but still positive returns. Always triangulate.

**Deep dive**: references/roi-framework.md — cost model, value model, formulas, executive reporting, benchmarks with caveats.

### 5. Experience Metrics

Measure developer satisfaction and cognitive impact.

| Metric | Formula | Target | Source |
|--------|---------|--------|--------|
| AI Tool Satisfaction | survey_score (1-5 Likert) | >3.8/5.0 | Quarterly survey |
| Tool NPS | promoters% - detractors% | >30 | Quarterly survey |
| Cognitive Load | NASA-TLX adaptation (1-7) | <4.0/7.0 | Post-task survey |
| Give-Up Rate | started_AI_finished_manual / total | <20% | Telemetry |
| Trust Calibration | appropriate_review_rate | >80% | Code review data |

**Deep dive**: references/developer-experience-metrics.md — survey design, cognitive load measurement, friction indicators, trust metrics.

---

## Measurement Maturity Model

Where is your organization in measuring AI coding impact?

| Level | Name | Characteristics | Key Action |
|-------|------|----------------|------------|
| **L0** | No Measurement | No tracking beyond license count | Install basic telemetry, run first survey |
| **L1** | Basic Tracking | License utilization + adoption rate tracked | Add DORA metrics baseline, first ROI estimate |
| **L2** | Structured Program | DORA + adoption + quality metrics active, quarterly survey | Design controlled experiment, build dashboard |
| **L3** | Evidence-Based | Controlled experiments, statistical rigor, executive reporting | Cross-team benchmarking, predictive models |
| **L4** | Optimized | Continuous measurement, automated dashboards, data-driven tool selection | Industry benchmarking, publish findings |

### L0 → L1 Quick Start (2 hours)

1. Pull license utilization from admin console
2. Run the adoption survey (assets/adoption-survey-template.md)
3. Calculate basic ROI estimate (assets/roi-calculator-template.md)
4. Present 1-page summary to leadership (assets/executive-report-template.md)

### L1 → L2 (2-4 weeks)

1. Establish DORA metric baselines (references/productivity-metrics.md)
2. Set up quality tracking (references/quality-metrics.md)
3. Build three-tier dashboard (assets/metric-dashboard-template.md)
4. Schedule quarterly developer experience surveys

### L2 → L3 (1-3 months)

1. Design first controlled experiment (assets/experiment-design-template.md)
2. Apply statistical rigor (references/benchmarking-methodology.md)
3. Create executive reporting cadence (assets/executive-report-template.md)
4. Cross-reference with dev-context-engineering maturity model for context quality impact

### L3 → L4 (ongoing)

1. Automate data collection and dashboards
2. Build predictive models (adoption → productivity correlation)
3. Benchmark against industry data
4. Contribute findings to community (conference talks, blog posts)

---

## Metric Selection Decision Tree

Not every org needs every metric. Start from what you're trying to prove.

```text
WHAT ARE YOU TRYING TO PROVE?
  │
  ├─ "Should we buy AI coding tools?"
  │   └─ START: roi-framework.md → roi-calculator-template.md
  │       Metrics: cost per seat, estimated hours saved, break-even adoption rate
  │
  ├─ "Are developers actually using the tools?"
  │   └─ START: adoption-metrics.md → adoption-survey-template.md
  │       Metrics: DAU/WAU, acceptance rate, feature breadth, organic usage
  │
  ├─ "Are we shipping faster?"
  │   └─ START: productivity-metrics.md → metric-dashboard-template.md
  │       Metrics: DORA metrics, cycle time, PR throughput
  │
  ├─ "Is code quality suffering?"
  │   └─ START: quality-metrics.md → metric-dashboard-template.md
  │       Metrics: bug density, defect escape rate, rework rate, vulnerability rate
  │
  ├─ "Are developers happy with AI tools?"
  │   └─ START: developer-experience-metrics.md → adoption-survey-template.md
  │       Metrics: satisfaction, NPS, cognitive load, give-up rate
  │
  ├─ "How do we compare to industry?"
  │   └─ START: benchmarking-methodology.md → experiment-design-template.md
  │       Metrics: DORA benchmarks, adoption curves, ROI ranges
  │
  └─ "Should we expand or cut the program?"
      └─ COMBINE: roi-framework.md + adoption-metrics.md + executive-report-template.md
          Metrics: ROI trend, adoption trajectory, satisfaction trend, quality delta
```

---

## Dashboard Design Principles

### Three-Tier Hierarchy

| Tier | Audience | Refresh | Metrics | Purpose |
|------|----------|---------|---------|---------|
| **Executive** | C-Suite, VP Eng | Monthly | 4-6 KPIs | Investment decision, program health |
| **Team Lead** | Eng Managers | Weekly | 8-10 metrics | Team optimization, coaching |
| **Developer** | Individual devs | Real-time | Personal stats | Self-improvement (opt-in only) |

### Design Rules

1. **Lead with outcomes, not activity** — show deploy frequency, not lines of code
2. **Always show trend lines** — a single number is meaningless without direction
3. **Include confidence indicators** — mark metrics with low sample sizes or high variance
4. **Never rank individuals** — aggregate to team level minimum (team size ≥5)
5. **Pair speed with quality** — never show velocity without adjacent quality metrics
6. **Show cost alongside benefit** — ROI is a ratio, not a cherry-picked benefit number

See: assets/metric-dashboard-template.md for full layout.

---

## Anti-Patterns

| Anti-Pattern | Why It's Harmful | Fix |
|-------------|-----------------|-----|
| **Lines of Code as productivity** | AI inflates LOC; rewards verbosity over clarity | Use outcome metrics (features shipped, bugs resolved) |
| **Individual developer tracking** | Creates surveillance culture, erodes trust | Aggregate to team level, minimum team size 5 |
| **Vanity metrics only** | "90% adoption!" means nothing if output quality drops | Always pair adoption with quality and satisfaction |
| **Measuring too early** | First 4 weeks are learning curve, not steady state | Allow 8-12 week adoption curve before measuring impact |
| **Vendor benchmarks as gospel** | Vendor studies select favorable conditions | Triangulate with independent research; discount vendor data 30-50% |
| **Ignoring the denominator** | "Shipped 40% more PRs" — but were they smaller? | Normalize metrics (features/sprint, not PRs/sprint) |
| **Correlation → causation** | Team adopted AI *and* got a new senior dev | Use controlled experiments (benchmarking-methodology.md) |
| **Surveying without acting** | Developers report friction → nothing changes | Close the loop: share results + action plan within 2 weeks |
| **One metric to rule them all** | Single metric always gets gamed | Use balanced scorecard (adoption + velocity + quality + experience) |
| **Comparing incomparable teams** | Frontend team vs infra team → meaningless comparison | Segment by project type, stack, and task complexity |

---

## Cross-References

| Skill | Relationship |
|-------|-------------|
| [dev-context-engineering](../dev-context-engineering/SKILL.md) | Context quality directly affects AI tool effectiveness — L0-L4 maturity model correlates with metric outcomes |
| [ai-agents](../ai-agents/SKILL.md) | Per-task token economics and agent ROI (this skill covers team/org-level metrics) |
| [qa-observability](../qa-observability/SKILL.md) | OpenTelemetry integration for automated metric collection |
| [product-management](../product-management/SKILL.md) | OKR integration — AI metrics feed into engineering OKRs |
| [startup-business-models](../startup-business-models/SKILL.md) | Unit economics context for ROI calculations |
| [dev-workflow-planning](../dev-workflow-planning/SKILL.md) | Cycle time and planning metrics overlap |

---

## Do / Avoid

**Do**:
- Start with adoption metrics — you can't optimize what people aren't using
- Establish baselines *before* rolling out AI tools (8-week minimum)
- Use the balanced scorecard approach (adoption + velocity + quality + experience)
- Run quarterly developer experience surveys
- Report with confidence intervals, not point estimates
- Cross-reference with context maturity (dev-context-engineering) — structured repos get more AI benefit

**Avoid**:
- Don't track individual developer productivity with AI tools
- Don't use lines of code as a metric for anything
- Don't measure impact in the first 4 weeks (adoption curve)
- Don't rely on vendor-published benchmarks without independent validation
- Don't survey developers without acting on the results
- Don't compare teams without controlling for confounding variables
- Don't present ROI without showing the cost model assumptions

---

## Web Verification

55 curated sources in `data/sources.json` across 7 categories:

| Category | Sources | Key Items |
|----------|---------|-----------|
| Developer Productivity Research | ~10 | DORA, SPACE, METR, ETH Zurich, McKinsey, Nicole Forsgren |
| AI Tool Adoption Data | ~8 | GitHub Copilot studies, Stack Overflow, GitClear, Harvard BS |
| Industry Case Studies | ~8 | Block/Square, Stripe, Klarna, Coinbase, Shopify, Amazon |
| Frameworks & Methodologies | ~8 | DX Company, LinearB, Haystack, Jellyfish, Swarmia |
| Measurement Tools | ~7 | Copilot Metrics API, OpenTelemetry, Grafana, PostHog |
| Consulting Reports | ~7 | McKinsey, BCG, HBR, Gartner, Forrester |
| Academic Research | ~7 | arXiv (Peng et al., Ziegler et al., METR), ACM, IEEE |

Verify current data before final answers. Priority areas:
- DORA State of DevOps report updates (annual)
- GitHub Copilot Metrics API changes
- New independent productivity studies (academic, not vendor)
- ETH Zurich context effectiveness research updates
- METR evaluation methodology updates

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, tool features, or published benchmarks before final answers.
- Prefer independent/academic sources over vendor marketing; report source links and dates.
- If web access is unavailable, state the limitation and mark guidance as unverified.

---

## Navigation

### References

| File | Content | Lines |
|------|---------|-------|
| adoption-metrics.md | Adoption tracking, curve phases, tool-specific data sources, stall patterns | ~300 |
| productivity-metrics.md | DORA for AI teams, SPACE framework, cycle time decomposition | ~350 |
| quality-metrics.md | Defect metrics, complexity, test coverage, security, technical debt | ~280 |
| roi-framework.md | Cost/value models, ROI formulas, executive reporting, benchmarks | ~320 |
| developer-experience-metrics.md | Satisfaction surveys, cognitive load, friction, trust, onboarding | ~260 |
| benchmarking-methodology.md | A/B comparison, before/after design, statistical rigor, reporting | ~300 |

### Assets (Copy-Ready Templates)

| File | Purpose |
|------|---------|
| metric-dashboard-template.md | Three-tier dashboard layout (Executive / Team Lead / Developer) |
| adoption-survey-template.md | 15-question developer survey with Likert scales and scoring |
| roi-calculator-template.md | Spreadsheet-ready ROI formulas and sensitivity analysis |
| executive-report-template.md | Monthly 1-page + quarterly deep-dive report templates |
| experiment-design-template.md | Controlled experiment planning with statistical requirements |
