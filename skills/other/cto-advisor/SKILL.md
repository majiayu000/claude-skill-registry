---
name: cto-advisor
description: CTO-level advisory - build vs buy decisions, tech debt quantification, team scaling, ADRs, technology evaluation (RICE), budget planning, TCO, vendor management, DORA/SPACE metrics
---

# CTO Advisor

## Build vs Buy Decision Framework

### Decision Matrix

```markdown
## Build vs Buy Analysis: [Feature/System Name]

### Scoring (1-5 each)

| Factor | Build | Buy | Weight |
|--------|-------|-----|--------|
| Core competency alignment | [1-5] | [1-5] | 3x |
| Time to market | [1-5] | [1-5] | 2x |
| Total cost (3 year) | [1-5] | [1-5] | 2x |
| Customization needs | [1-5] | [1-5] | 2x |
| Maintenance burden | [1-5] | [1-5] | 1x |
| Data control | [1-5] | [1-5] | 1x |
| Integration complexity | [1-5] | [1-5] | 1x |
| Vendor risk | [1-5] | [1-5] | 1x |
| **Weighted Total** | [sum] | [sum] | |

### Decision: BUILD / BUY / HYBRID
```

### Decision Rules

| Condition | Recommendation |
|-----------|---------------|
| Core differentiator | BUILD (competitive advantage) |
| Commodity capability | BUY (focus on core) |
| Strict compliance / data sovereignty | BUILD (control) |
| Team has no domain expertise | BUY (faster, less risk) |
| Vendor lock-in risk > 7/10 | BUILD or multi-vendor |
| Time to market < 3 months | BUY (speed) |
| Budget constrained, long-term | BUILD (lower TCO) |

### Build vs Buy Anti-Patterns

| Anti-Pattern | Neden Yanlis | Dogru Yol |
|-------------|-------------|-----------|
| "Not invented here" | Wasted engineering time | Evaluate vendors objectively |
| "We'll build it in 2 weeks" | Always takes 5x longer | Realistic estimation with buffer |
| Buying everything | No differentiation | Build core, buy commodity |
| Ignoring maintenance cost | Build looks cheaper initially | Include 3-5 year maintenance TCO |
| No exit strategy from vendor | Lock-in trap | Evaluate migration cost upfront |

## Tech Debt Quantification & Prioritization

### Tech Debt Classification

| Type | Description | Impact | Example |
|------|-------------|--------|---------|
| **Code debt** | Poor code quality | Developer velocity | No types, huge functions, no tests |
| **Architecture debt** | Wrong architectural decisions | Scalability | Monolith that should be microservice |
| **Test debt** | Insufficient test coverage | Reliability | No integration tests, flaky tests |
| **Dependency debt** | Outdated dependencies | Security | 3 major versions behind, CVEs |
| **Documentation debt** | Missing/outdated docs | Onboarding | No API docs, stale README |
| **Infrastructure debt** | Manual processes, legacy infra | Reliability | No CI/CD, manual deployments |
| **Design debt** | UX inconsistencies | User experience | 5 different button styles |

### Tech Debt Scorecard

```markdown
## Tech Debt Assessment: [Project Name]

| Area | Score (1-10) | Trend | Priority |
|------|-------------|-------|----------|
| Code quality | [X] | [up/down/flat] | [H/M/L] |
| Test coverage | [X%] | [up/down/flat] | [H/M/L] |
| Dependency freshness | [X] | [up/down/flat] | [H/M/L] |
| Build/deploy time | [X min] | [up/down/flat] | [H/M/L] |
| Documentation | [X] | [up/down/flat] | [H/M/L] |
| Security posture | [X] | [up/down/flat] | [H/M/L] |

### Cost of Delay
[If we don't address debt area X, what happens in 6 months?]

### Investment Request
| Initiative | Effort | Impact | ROI Period |
|-----------|--------|--------|------------|
| [debt 1] | [weeks] | [description] | [months] |
| [debt 2] | [weeks] | [description] | [months] |
```

### Prioritization Formula

```
Priority Score = (Impact * Urgency * Spread) / Effort

Impact (1-5):    How much does it slow the team?
Urgency (1-5):   How quickly will it get worse?
Spread (1-5):    How many areas does it affect?
Effort (1-5):    How hard is it to fix? (inverse: 1=hard, 5=easy)
```

### Tech Debt Budget Rule

```
RULE: 20% of sprint capacity reserved for tech debt reduction

Sprint capacity: 10 story points
├── 8 points: Feature work
└── 2 points: Tech debt reduction (ZORUNLU, negotiable degil)
```

## Team Scaling Strategies

### Hiring Framework

```markdown
## Hiring Plan: [Quarter/Year]

### Current State
| Role | Headcount | Capacity | Gap |
|------|-----------|----------|-----|
| Backend | [X] | [Y features/quarter] | [shortfall] |
| Frontend | [X] | [Y features/quarter] | [shortfall] |
| DevOps | [X] | [Y deploys/week] | [shortfall] |
| QA | [X] | [Y tests/sprint] | [shortfall] |

### Ratios
- Engineer : Manager = 6-8 : 1
- Senior : Mid : Junior = 2 : 3 : 1
- Backend : Frontend = project-dependent
- Engineer : QA = 4-6 : 1

### Onboarding Milestones
| Day | Milestone |
|-----|-----------|
| 1 | Dev environment running, first commit |
| 7 | First PR merged |
| 14 | First feature shipped to staging |
| 30 | Independent task completion |
| 60 | Contributing to architecture discussions |
| 90 | Fully productive, mentoring others |
```

### Team Topology Patterns

| Pattern | When to Use | Size |
|---------|-------------|------|
| Stream-aligned | Product features | 5-8 people |
| Platform | Internal tooling, infrastructure | 3-5 people |
| Enabling | Coach other teams, remove blockers | 2-3 people |
| Complicated subsystem | Deep expertise (ML, security) | 2-4 people |

## Architecture Decision Records (ADR)

### ADR Template

```markdown
# ADR-[number]: [decision title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[What is the issue? What forces are at play?]
[Include constraints, requirements, team capabilities]

## Decision
[What is the change that we're proposing and/or doing?]

## Alternatives Considered
### Option A: [name]
- Pros: [list]
- Cons: [list]

### Option B: [name]
- Pros: [list]
- Cons: [list]

## Consequences
### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [tradeoff 1]
- [tradeoff 2]

### Risks
- [risk 1]: [mitigation]
- [risk 2]: [mitigation]

## Decision Date
[YYYY-MM-DD]

## Decision Makers
[names/roles]
```

### ADR Index

```markdown
## Architecture Decision Log

| # | Decision | Status | Date | Impact |
|---|---------|--------|------|--------|
| 001 | Use PostgreSQL over MongoDB | Accepted | 2025-01-15 | High |
| 002 | Adopt microservices for billing | Accepted | 2025-02-01 | High |
| 003 | Use React over Vue | Accepted | 2025-02-15 | Medium |
| 004 | Monolith-first for MVP | Deprecated | 2025-03-01 | High |
```

## Technology Evaluation Framework

### RICE Scoring

```markdown
## Technology Evaluation: [Technology Name]

### RICE Score

| Factor | Score | Weight | Weighted |
|--------|-------|--------|----------|
| **Reach** (how many people/teams affected) | [1-10] | 1x | [X] |
| **Impact** (how much improvement per person) | [1-3: minimal/medium/massive] | 2x | [X] |
| **Confidence** (how sure are we) | [50-100%] | 1x | [X] |
| **Effort** (person-months) | [X] | divisor | [X] |

**RICE Score = (Reach * Impact * Confidence) / Effort = [score]**
```

### Weighted Scoring Matrix

```markdown
## Vendor/Technology Comparison

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| Performance | 20% | [1-5] | [1-5] | [1-5] |
| Community/support | 15% | [1-5] | [1-5] | [1-5] |
| Learning curve | 15% | [1-5] | [1-5] | [1-5] |
| Cost | 15% | [1-5] | [1-5] | [1-5] |
| Scalability | 10% | [1-5] | [1-5] | [1-5] |
| Security | 10% | [1-5] | [1-5] | [1-5] |
| Integration | 10% | [1-5] | [1-5] | [1-5] |
| Maturity | 5% | [1-5] | [1-5] | [1-5] |
| **Weighted Total** | | [sum] | [sum] | [sum] |

### Recommendation: [Option X]
### Reasoning: [1-2 sentences]
```

### Technology Evaluation Anti-Patterns

| Anti-Pattern | Risk | Dogru Yol |
|-------------|------|-----------|
| Resume-driven development | Wrong tool for the job | Evaluate against actual needs |
| Hype-driven adoption | Immature ecosystem | Wait for version 2.0+ |
| Single vendor evaluation | No comparison baseline | Always evaluate 3+ options |
| Ignoring exit cost | Future lock-in | Calculate migration cost |
| No POC/prototype | Unknown unknowns | Build spike before committing |

## Budget Planning & TCO Analysis

### TCO Template (3-Year)

```markdown
## Total Cost of Ownership: [System/Technology]

### Year 1 (Setup + Operations)
| Category | Cost |
|----------|------|
| Licenses/subscriptions | $[X] |
| Infrastructure (cloud/hardware) | $[X] |
| Implementation/migration | $[X] |
| Training | $[X] |
| Integration development | $[X] |
| **Year 1 Total** | **$[X]** |

### Year 2-3 (Ongoing)
| Category | Annual Cost |
|----------|------------|
| Licenses/subscriptions (+ annual increase) | $[X] |
| Infrastructure | $[X] |
| Maintenance engineering (FTE fraction) | $[X] |
| Support contracts | $[X] |
| Upgrades/patches | $[X] |
| **Annual Ongoing** | **$[X]** |

### 3-Year TCO: $[Year 1 + Year 2 + Year 3]

### Hidden Costs (often missed)
- Context switching overhead
- On-call/incident response time
- Documentation maintenance
- Vendor management overhead
- Compliance/audit costs
```

## Vendor Management

### Vendor Assessment Checklist

- [ ] Financial stability (will they exist in 3 years?)
- [ ] Security certifications (SOC2, ISO 27001)
- [ ] SLA guarantees (uptime, response time)
- [ ] Data portability (can you export everything?)
- [ ] API quality (documentation, versioning, reliability)
- [ ] Support quality (response time, escalation path)
- [ ] Pricing transparency (no surprise costs)
- [ ] Contract flexibility (monthly vs annual, exit clause)
- [ ] Reference customers (talk to existing users)
- [ ] Roadmap alignment (are they building what you need?)

### Vendor Risk Matrix

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Vendor acquired/shutdown | Low | Critical | Data export procedure, backup vendor |
| Price increase > 30% | Medium | High | Multi-year contract, alternative evaluation |
| SLA breach | Medium | High | Credits, contractual remedies |
| Data breach at vendor | Low | Critical | Encryption, contractual liability |
| Feature deprecation | Medium | Medium | API abstraction layer |

## Engineering Metrics

### DORA Metrics

| Metric | Elite | High | Medium | Low |
|--------|-------|------|--------|-----|
| **Deployment Frequency** | On-demand (multiple/day) | Daily-weekly | Weekly-monthly | Monthly-6monthly |
| **Lead Time for Changes** | < 1 hour | 1 day - 1 week | 1 week - 1 month | 1 - 6 months |
| **Change Failure Rate** | 0-15% | 16-30% | 16-30% | 16-30% |
| **Mean Time to Recovery** | < 1 hour | < 1 day | 1 day - 1 week | > 1 week |

### SPACE Framework

| Dimension | Metrics | How to Measure |
|-----------|---------|---------------|
| **S**atisfaction | Developer satisfaction survey | Quarterly survey (1-5 scale) |
| **P**erformance | Code review turnaround, incident resolution | Tooling metrics |
| **A**ctivity | PRs merged, deploys, commits | Git/CI data (NOT for evaluation) |
| **C**ommunication | Knowledge sharing, documentation | Survey + doc metrics |
| **E**fficiency | Dev environment setup time, build time | Measure and track |

### Engineering Health Dashboard

```markdown
## Engineering Health: [Quarter]

### DORA Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Deploy frequency | Daily | [X/week] | [on/off track] |
| Lead time | < 1 day | [X hours] | [on/off track] |
| Change failure rate | < 15% | [X%] | [on/off track] |
| MTTR | < 1 hour | [X min] | [on/off track] |

### Team Health
| Area | Score (1-10) | Trend |
|------|-------------|-------|
| Developer satisfaction | [X] | [up/down/flat] |
| On-call burden | [X] | [up/down/flat] |
| Tech debt sentiment | [X] | [up/down/flat] |
| Tooling satisfaction | [X] | [up/down/flat] |

### Actionable Insights
1. [Insight + recommended action]
2. [Insight + recommended action]
```

## Board/Investor Technical Reporting

### Quarterly Tech Report Template

```markdown
## Technology Report: Q[X] [Year]

### Executive Summary
[2-3 sentences: key wins, risks, requests]

### Key Metrics
| Metric | Q-1 | Q0 | Target | Trend |
|--------|-----|-----|--------|-------|
| Uptime | [X%] | [X%] | 99.9% | [arrow] |
| Page load time | [Xs] | [Xs] | < 2s | [arrow] |
| Active users | [X] | [X] | [target] | [arrow] |
| Deploy frequency | [X/mo] | [X/mo] | Daily | [arrow] |

### Achievements
1. [Milestone/launch/improvement]
2. [Milestone/launch/improvement]

### Risks & Challenges
| Risk | Severity | Mitigation | Status |
|------|----------|-----------|--------|
| [risk] | [H/M/L] | [plan] | [active/mitigated] |

### Budget
| Category | Budget | Actual | Variance |
|----------|--------|--------|----------|
| Infrastructure | $[X] | $[X] | [+/-X%] |
| Licenses | $[X] | $[X] | [+/-X%] |
| Headcount | $[X] | $[X] | [+/-X%] |

### Next Quarter Focus
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

### Resource Request
[If applicable: what do we need and why]
```

### Board Communication Anti-Patterns

| Anti-Pattern | Neden Yanlis | Dogru Yol |
|-------------|-------------|-----------|
| Too much jargon | Board members aren't engineers | Translate to business impact |
| Only good news | Erodes trust | Honest + solution-oriented |
| No metrics | Unverifiable | Data-driven with trends |
| Feature list only | No business context | Connect features to revenue/growth |
| Asking for budget without ROI | Unlikely approval | Show expected return |
