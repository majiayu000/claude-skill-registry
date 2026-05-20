---
name: risk-management
description: Project risk identification, analysis, and response planning for software and systems projects. Covers probability-impact matrices, qualitative and quantitative risk analysis, Monte Carlo simulation for schedule risk, FMEA for projects, decision trees, expected monetary value, risk registers, and response strategies (avoid, mitigate, transfer, accept). Draws on NASA risk management heritage and Brooks's "no silver bullet" philosophy. Includes technical debt, dependency risk, and integration risk as first-class risk categories.
type: skill
category: project-management
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/project-management/risk-management/SKILL.md
superseded_by: null
---
# Risk Management

Risk is uncertainty that matters. Every project operates under uncertainty — requirements change, dependencies break, people leave, estimates miss. Risk management does not eliminate uncertainty; it makes uncertainty visible, quantifiable, and actionable. The goal is not a risk-free project (that project does not exist) but a project where surprises are anticipated, responses are prepared, and the team is never blindsided.

Margaret Hamilton's Apollo guidance software team did not hope their code would work during lunar descent. They engineered priority displays that could shed non-critical tasks under overload — a risk response designed before the risk materialized. When Apollo 11's computer threw 1202 alarms during the final descent, the crew landed safely because Hamilton's team had already decided what to do. That is risk management: deciding what to do before you need to.

**Agent affinity:** hamilton (systems engineering, risk architecture), brooks (organizational risk, "no silver bullet")

**Concept IDs:** bus-business-planning, bus-cost-benefit-analysis, crit-problem-analysis, crit-evidence-evaluation

## Risk Management Process Overview

| Phase | Activity | Output |
|---|---|---|
| 1. Identify | Find risks before they find you | Risk list |
| 2. Analyze | Assess probability and impact | Prioritized risk register |
| 3. Plan responses | Decide what to do about each risk | Response strategies |
| 4. Monitor | Track risks, watch for triggers, update | Living risk register |

This is a continuous cycle, not a one-time activity. The risk register is a living document — reviewed at every sprint retrospective, updated at every milestone boundary, and consulted before every major decision.

## Phase 1 — Risk Identification

### Techniques

**Brainstorming.** The team generates risks freely. No filtering during generation — quantity over quality. Sort and prioritize afterward. Works best with diverse perspectives: developers, testers, operations, business stakeholders.

**Checklist review.** Use historical checklists from similar projects. Common categories:

- **Technical:** Architecture limitations, technology maturity, integration complexity
- **Schedule:** Optimistic estimates, dependency delays, resource availability
- **Scope:** Requirement ambiguity, scope creep, stakeholder disagreement
- **External:** Vendor reliability, regulatory changes, market shifts
- **People:** Key person dependency, skill gaps, team turnover

**SWOT analysis.** Strengths, Weaknesses, Opportunities, Threats. Strengths and weaknesses are internal; opportunities and threats are external. SWOT for risk focuses on the WT quadrant (weaknesses that amplify threats).

**Assumption analysis.** Every project plan rests on assumptions. List them explicitly. Each assumption is a potential risk if it proves false.

**Worked example — Assumption surfacing.**

| Assumption | If false... | Risk |
|---|---|---|
| The payment API supports batch processing | Must process sequentially; 10x slower | Schedule slip on checkout feature |
| The senior developer stays through Q3 | Knowledge loss on auth subsystem | Quality and schedule risk |
| Staging environment available by March 1 | Cannot integration-test until March 15 | Late defect discovery |
| Client will provide test data by sprint 3 | Must generate synthetic data | Scope increase, fidelity risk |

Each "If false..." entry becomes a risk in the register.

**Pre-mortem (Klein).** Gary Klein's technique: imagine the project has failed. Ask the team "Why did it fail?" People generate causes of failure more easily than abstract risks. This is psychologically powerful because it bypasses optimism bias.

### GSD Connection — Risk Identification in Phases

GSD's discuss phase (gsd-discuss-phase) gathers context through adaptive questioning before planning. Risk identification is natural here: "What could go wrong?" and "What assumptions are we making?" belong in every discuss phase. The list-phase-assumptions command (gsd-list-phase-assumptions) makes this explicit — surfacing Claude's assumptions before they become embedded in the plan.

## Phase 2 — Risk Analysis

### Qualitative Analysis — Probability x Impact Matrix

Assign each risk a probability (Low/Medium/High or 1-5) and an impact (Low/Medium/High or 1-5). Multiply to get a risk score.

**Standard 5x5 matrix:**

| | Impact 1 | Impact 2 | Impact 3 | Impact 4 | Impact 5 |
|---|---|---|---|---|---|
| **Prob 5** | 5 | 10 | 15 | 20 | 25 |
| **Prob 4** | 4 | 8 | 12 | 16 | 20 |
| **Prob 3** | 3 | 6 | 9 | 12 | 15 |
| **Prob 2** | 2 | 4 | 6 | 8 | 10 |
| **Prob 1** | 1 | 2 | 3 | 4 | 5 |

**Risk zones:**
- **Red (15-25):** Active mitigation required. Escalate to project sponsor.
- **Yellow (8-14):** Monitor closely. Mitigation plan on standby.
- **Green (1-7):** Accept or watch. Low priority.

### Worked Example — Risk Register

| ID | Risk | Prob | Impact | Score | Response | Owner |
|---|---|---|---|---|---|---|
| R01 | Payment API does not support batch | 3 | 4 | 12 | Mitigate: prototype batch call in sprint 1 | Dev lead |
| R02 | Senior developer leaves before Q3 | 2 | 5 | 10 | Mitigate: pair programming for knowledge transfer | Scrum master |
| R03 | Staging environment delayed | 4 | 3 | 12 | Avoid: provision cloud staging independently | DevOps |
| R04 | Client test data late | 3 | 3 | 9 | Accept: synthetic data generator as fallback | QA lead |
| R05 | Third-party auth library deprecated | 2 | 4 | 8 | Transfer: use vendor-supported alternative | Architect |
| R06 | Performance target (200ms p95) unreachable | 2 | 5 | 10 | Mitigate: performance spike in sprint 2 | Dev lead |

### Quantitative Analysis — Monte Carlo Simulation

For schedule and cost risks where qualitative assessment is insufficient, Monte Carlo simulation provides probability distributions.

**Process:**

1. For each task, estimate three durations: optimistic (O), most likely (M), pessimistic (P).
2. Model each task duration as a probability distribution (PERT-beta or triangular).
3. Simulate the project schedule 10,000+ times, sampling each task duration from its distribution.
4. The output is a cumulative probability curve: "There is an 80% chance the project completes by date X."

**Worked example — Three-task project.**

| Task | O (days) | M (days) | P (days) | PERT mean |
|---|---|---|---|---|
| Backend API | 5 | 8 | 20 | 9.2 |
| Frontend UI | 3 | 5 | 12 | 5.8 |
| Integration | 2 | 4 | 10 | 4.7 |

Tasks are sequential. PERT mean total: 19.7 days. But the sum of means is not the 80th percentile — variance accumulates.

After 10,000 Monte Carlo runs:
- P50 (median): 20 days
- P80: 24 days
- P95: 30 days

**Insight.** If the deadline is 20 days, you have a coin-flip chance of making it. If stakeholders need 80% confidence, plan for 24 days. The difference between P50 and P80 is the risk buffer — and it is not padding, it is mathematics.

### Decision Trees and Expected Monetary Value (EMV)

**Decision tree.** A branching diagram where each node is a decision or chance event. Branches represent options or outcomes, with probabilities and values at each terminal node.

**Worked example — Build vs. buy.**

```
Decision: Build custom auth system vs. Buy commercial
  Build:
    Success (p=0.7): -$50K (dev cost), saves $20K/year for 5 years = +$50K net
    Failure, rebuild (p=0.3): -$50K + -$30K rebuild = -$80K
    EMV(Build) = 0.7 * $50K + 0.3 * (-$80K) = $35K - $24K = +$11K

  Buy:
    Works well (p=0.9): -$15K/year * 5 = -$75K
    Vendor discontinues (p=0.1): -$75K + -$40K migration = -$115K
    EMV(Buy) = 0.9 * (-$75K) + 0.1 * (-$115K) = -$67.5K - $11.5K = -$79K
```

EMV favors Build (+$11K vs. -$79K). But note: Build has a 30% chance of -$80K outcome. If the organization cannot absorb that loss, the EMV calculation alone is insufficient — risk appetite matters.

## Phase 3 — Risk Response Strategies

### The Four Strategies

**Avoid.** Eliminate the risk by changing the plan. If a risky technology is the source, choose a different technology. If a tight deadline is the source, negotiate scope reduction. Avoidance removes the risk entirely but may change project scope or cost.

**Mitigate.** Reduce probability or impact. Pair programming mitigates key-person risk (reduces impact of departure). A spike or proof-of-concept mitigates technical risk (reduces probability of late discovery). Mitigation is the most common strategy.

**Transfer.** Shift the impact to a third party. Insurance. Fixed-price contracts with vendors. SLAs with penalties. The risk still exists, but the financial impact falls on someone else.

**Accept.** Acknowledge the risk and prepare no active response. Either the risk is too small to justify action, or no effective response exists. Passive acceptance does nothing. Active acceptance sets aside a contingency reserve.

### Worked Example — Response Planning

**Risk:** The new ML model may not meet accuracy targets (90% precision required, current prototype achieves 82%).

| Strategy | Action | Trade-off |
|---|---|---|
| Avoid | Drop ML feature; use rule-based system | Reduced product value |
| Mitigate | Time-box ML R&D to 3 sprints; parallel-develop fallback | Increased cost, insurance against failure |
| Transfer | Outsource ML development to specialist vendor | Dependency on vendor; IP concerns |
| Accept (active) | Continue current approach; reserve 4 sprint buffer | Schedule risk accepted; no cost to try |

**Selected response:** Mitigate. Three sprints for ML R&D with a rule-based fallback developed in parallel. If ML achieves 90% by sprint 3, ship it. If not, ship rules-based and continue ML in a future release.

## Phase 4 — Risk Monitoring

### Risk Triggers

Each risk should have defined triggers — observable conditions that indicate the risk is materializing. Triggers convert risks from abstract possibilities to concrete action items.

| Risk | Trigger | Action when triggered |
|---|---|---|
| Senior developer leaves | Developer mentions job search; engagement drops | Activate knowledge transfer plan |
| Payment API incompatible | Prototype fails in sprint 1 | Switch to sequential processing design |
| Performance target at risk | Sprint 2 benchmark exceeds 150ms p95 | Escalate to architect; allocate optimization sprint |

### Risk Burndown

Track open risks over time. A healthy project shows risks closing (resolved or expired) faster than new risks appear. If the risk count grows steadily, the project is accumulating uncertainty — a signal to pause and reassess.

## Software-Specific Risk Categories

### Technical Debt as Risk

Technical debt is not a metaphor — it is a risk with compounding interest. Every shortcut taken today increases the probability and impact of future defects, performance problems, and development slowdowns.

**Quantification.** Track debt items in the backlog with estimated remediation cost. When accumulated debt exceeds 20% of a sprint's capacity in rework, it has become a schedule risk.

**GSD connection.** GSD's audit-fix pipeline (gsd-audit-fix) systematically identifies and resolves code quality issues. This is proactive debt reduction — a mitigation strategy applied continuously rather than in panicked bursts before release.

### Dependency Risk

External dependencies (libraries, APIs, services) are risks the team does not control.

**Mitigation strategies:**
- Pin dependency versions (avoid surprise breaking changes)
- Maintain a dependency audit schedule (cross-reference: dependency-audit skill)
- Design interfaces behind abstraction layers (if vendor X breaks, swap to vendor Y)
- Identify single points of failure in the dependency graph

### Integration Risk

Integration failures are discovered late and cost the most to fix. Brooks observed in *The Mythical Man-Month* that system integration typically consumes more time than all component development combined.

**Mitigation strategies:**
- Integrate early, integrate often (XP's continuous integration)
- Build the skeleton first — a walking skeleton that exercises all integration points end-to-end
- Allocate explicit integration sprints in the schedule
- Use contract testing to verify interface compatibility before integration

### Critical Path Risk

Any task on the critical path that slips causes the entire project to slip. Critical path tasks have zero float.

**Mitigation strategies:**
- Identify the critical path explicitly (CPM analysis — cross-reference: estimation-planning skill)
- Apply buffers only to the critical path (Goldratt's critical chain method)
- Assign the strongest team members to critical path tasks
- Avoid dependencies on external parties for critical path items

## NASA Risk Management Heritage

NASA's risk management framework, forged through decades of mission-critical operations, offers principles applicable to any project:

**Probabilistic Risk Assessment (PRA).** NASA quantifies risk using fault trees and event trees, computing the probability of mission failure from component-level failure probabilities. For software projects, the analog is failure mode analysis across integration points.

**Hamilton's Priority Displays.** Margaret Hamilton's Apollo Guidance Computer team designed the system to recognize overload conditions and shed low-priority tasks to preserve mission-critical functions. This is risk response through architecture — the system itself implements the risk mitigation, not a human in a crisis.

**Lesson.** The best risk management is embedded in the system design, not in a spreadsheet. A well-designed system degrades gracefully; a poorly designed system fails catastrophically. Design for failure is the highest form of risk management.

### FMEA for Projects (Failure Mode and Effects Analysis)

Originally from reliability engineering, FMEA can be adapted for project risk:

1. **List failure modes.** What can go wrong? (scope creep, integration failure, key person leaves)
2. **Assess severity (S).** If it happens, how bad? (1-10)
3. **Assess occurrence (O).** How likely? (1-10)
4. **Assess detection (D).** How likely are we to catch it before impact? (1-10, where 10 = undetectable)
5. **Calculate RPN.** Risk Priority Number = S x O x D.
6. **Act on high-RPN items first.**

**Worked example.**

| Failure mode | S | O | D | RPN | Action |
|---|---|---|---|---|---|
| Requirements misunderstood | 8 | 6 | 4 | 192 | Sprint demos with stakeholder sign-off |
| Performance regression in production | 7 | 5 | 7 | 245 | Automated performance benchmarks in CI |
| Data migration corrupts records | 9 | 3 | 5 | 135 | Dry-run migration with checksum verification |
| Security vulnerability in dependency | 8 | 4 | 6 | 192 | Weekly dependency scan (npm audit) |

Note that detection (D) is the often-overlooked dimension. A high-severity, low-probability risk that is also hard to detect (high D) may score higher than an obvious, high-probability risk.

## Brooks's "No Silver Bullet" as Risk Philosophy

Fred Brooks argued in 1986 that there is no single technique that will produce an order-of-magnitude improvement in software productivity. The "essential complexity" of software — the irreducible difficulty of the problem domain — cannot be eliminated by tools, languages, or methodologies.

**Risk implication.** Any project plan that assumes a new tool or technique will solve a fundamental complexity problem is carrying an unacknowledged risk. When management bets the schedule on a technology they have not used before ("the new framework will make this twice as fast"), that is a risk that must be surfaced in the register.

**Mitigation.** Time-boxed technology evaluation. Spike stories. Proof of concept before commitment. The schedule must include learning time for any unfamiliar technology.

## When to Use / When NOT to Use

### When to use formal risk management

- Projects longer than 4 weeks with multiple stakeholders
- Projects with external dependencies or regulatory requirements
- Projects where failure has significant financial, safety, or reputational consequences
- Any project where the team has said "I hope this works" — hope is not a strategy

### When NOT to use formal risk management

- Trivial tasks with well-understood scope (a risk register for a one-day bug fix is overhead)
- When risk management becomes risk theater — elaborate spreadsheets that nobody reads or updates
- When the process generates more risk (analysis paralysis, delayed decisions) than it mitigates

### The Goldilocks principle

A risk register with 3-5 items for a small project, 10-20 for a medium project, and no more than 50 for a large project. If you have 200 risks, you have a list, not a management tool. Prioritize ruthlessly.

## Cross-References

- **hamilton agent:** Systems engineering risk architecture. Priority-based degradation. NASA heritage.
- **brooks agent:** Department chair. Organizational risk, team scaling risk, essential vs. accidental complexity.
- **goldratt agent:** Theory of Constraints applied to schedule risk — critical chain buffering.
- **deming agent:** Quality risk — defects as risk events, PDCA for risk response improvement.
- **estimation-planning skill:** Monte Carlo simulation, PERT estimation, critical path method — the quantitative tools for schedule risk analysis.
- **quality-assurance skill:** FMEA, testing strategies, verification and validation — risk reduction through quality.
- **retrospective-learning skill:** Lessons learned databases, after-action reviews — feeding risk knowledge back into future projects.
- **rca department (blameless-postmortem skill):** Root cause analysis when risks materialize — turning incidents into prevention.

## References

- Hillson, D. & Simon, P. (2020). *Practical Project Risk Management*. 3rd edition. Berrett-Koehler.
- Hubbard, D. W. (2009). *The Failure of Risk Management*. Wiley.
- Klein, G. (2007). "Performing a Project Premortem." *Harvard Business Review*, 85(9), 18-19.
- Hamilton, M. H. (1986). "Higher Order Software — A Methodology for Defining Software." *IEEE Transactions on Software Engineering*, SE-12(9), 9-25.
- Brooks, F. P. (1986). "No Silver Bullet — Essence and Accident in Software Engineering." *Information Processing 1986*, Elsevier.
- NASA. (2011). *NASA Risk Management Handbook*. NASA/SP-2011-3422.
- Stamatis, D. H. (2003). *Failure Mode and Effect Analysis: FMEA from Theory to Execution*. ASQ Quality Press.
- Vose, D. (2008). *Risk Analysis: A Quantitative Guide*. 3rd edition. Wiley.
