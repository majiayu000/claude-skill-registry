---
name: quality-assurance
description: Quality assurance and continuous improvement for software projects. Covers Deming's 14 Points for Management, PDCA cycle (Plan-Do-Check-Act), Six Sigma DMAIC, total quality management (TQM), quality metrics (defect density, code coverage, MTBF), testing strategies (unit, integration, system, acceptance), verification and validation (V&V), peer review and inspection, continuous improvement (kaizen), root cause analysis (5 Whys, fishbone), quality gates, definition of done, technical debt management, and Hamilton's priority display concept from Apollo as error prevention through system design.
type: skill
category: project-management
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/project-management/quality-assurance/SKILL.md
superseded_by: null
---
# Quality Assurance

Quality is not a phase. It is not something you test into a product at the end. It is a property that emerges from how you work — from design decisions, process discipline, feedback loops, and the organizational culture that either surfaces defects early or buries them until production. W. Edwards Deming spent his career demonstrating that quality and productivity are not trade-offs — improving quality improves productivity by reducing rework, reducing waste, and building trust in the process.

Margaret Hamilton's Apollo guidance software team embodied this principle. Their "priority displays" concept — designing the computer to recognize overload conditions and autonomously shed non-critical tasks — was not a testing strategy. It was a quality architecture. The system was designed so that certain classes of errors were structurally impossible, and those that remained were handled gracefully. The most powerful quality assurance is the error that cannot occur because the system will not permit it.

**Agent affinity:** deming (quality/process), hamilton (systems engineering, error prevention through design)

**Concept IDs:** bus-business-planning, bus-business-ethics, crit-problem-analysis, crit-evidence-evaluation

## Quality Framework Overview

| # | Framework | Core idea | Scope |
|---|---|---|---|
| 1 | Deming's 14 Points | Management creates quality | Organizational |
| 2 | PDCA Cycle | Iterative improvement | Process |
| 3 | Six Sigma (DMAIC) | Statistical defect reduction | Process / product |
| 4 | TQM | Everyone owns quality | Organizational |
| 5 | V&V | Verification vs. validation | Product |
| 6 | Testing pyramid | Layered confidence | Product |
| 7 | Peer review | Human defect detection | Code / design |
| 8 | Kaizen | Continuous small improvements | Organizational |

## Framework 1 — Deming's 14 Points for Management

Deming argued that 85% of quality problems are caused by the system, not by workers. Management creates the system; therefore, management is responsible for quality. His 14 Points:

1. **Create constancy of purpose** toward improvement of product and service.
2. **Adopt the new philosophy.** Management must lead the change.
3. **Cease dependence on inspection** to achieve quality. Build quality in.
4. **End the practice of awarding business on price alone.** Minimize total cost by working with fewer, trusted suppliers.
5. **Improve constantly** the system of production and service.
6. **Institute training on the job.**
7. **Institute leadership.** The aim of supervision should be to help people do a better job.
8. **Drive out fear** so everyone can work effectively.
9. **Break down barriers between departments.**
10. **Eliminate slogans and targets** that demand zero defects without providing methods.
11. **Eliminate numerical quotas.** Substitute leadership.
12. **Remove barriers to pride of workmanship.** Eliminate annual ratings.
13. **Institute a vigorous program of education and self-improvement.**
14. **Put everybody to work to accomplish the transformation.**

### Application to Software

| Point | Software interpretation |
|---|---|
| 3. Cease dependence on inspection | Don't rely on QA to find bugs. Build quality through TDD, code review, and design. |
| 5. Improve constantly | Retrospectives, refactoring, process experiments every sprint. |
| 7. Institute leadership | Tech leads mentor; they don't command. |
| 8. Drive out fear | Blameless postmortems. Psychological safety. |
| 9. Break down barriers | Cross-functional teams. DevOps. No "throw it over the wall." |
| 10. Eliminate slogans | "Zero bugs" as a goal without investing in prevention is a lie. |
| 12. Remove barriers to pride | Let developers refactor. Let them fix the code that shames them. |

**GSD connection.** Deming's Point 3 — "build quality in" — maps directly to GSD's phase structure. The verify phase (gsd-verify-work) is not an inspection gate; it is a validation that the process itself produced the right outcome. If verify consistently fails, the problem is in discuss/plan/execute, not in verify.

## Framework 2 — PDCA Cycle (Plan-Do-Check-Act)

Also called the Deming Cycle or Shewhart Cycle. The foundational improvement loop:

1. **Plan.** Identify an opportunity for improvement. Formulate a hypothesis: "If we do X, outcome Y will improve."
2. **Do.** Implement the change on a small scale. Collect data.
3. **Check.** Analyze the data. Did the change produce the expected improvement?
4. **Act.** If yes, standardize the change and expand it. If no, learn from the failure and return to Plan.

### Worked Example — Reducing Code Review Turnaround

**Problem.** Code reviews take an average of 3 days, blocking merges and slowing velocity.

**Plan.** Hypothesis: "If we set a 24-hour SLA for first review response and limit PR size to 400 lines, review turnaround will drop below 1 day."

**Do.** Implement for 2 sprints. Track review turnaround time daily. Team agrees to prioritize reviews before starting new work.

**Check.** After 2 sprints: average turnaround dropped to 18 hours. PRs over 400 lines still take 2+ days. PRs under 400 lines average 8 hours.

**Act.** Standardize the 400-line limit. Add tooling to warn when PRs exceed it. Continue monitoring. Next cycle: investigate whether pair programming reduces review need.

### PDCA and GSD

GSD's wave execution is a PDCA cycle at the phase level:
- **Plan:** PLAN.md creation (gsd-plan-phase)
- **Do:** Wave execution (gsd-execute-phase)
- **Check:** Verification (gsd-verify-work)
- **Act:** Retrospective and handoff (session report, handoff document)

Each session is a PDCA iteration. The carry-forward pattern (lessons from one session inform the next) is the "Act" step that closes the loop.

## Framework 3 — Six Sigma (DMAIC)

Six Sigma aims for 3.4 defects per million opportunities. The DMAIC methodology is the improvement cycle:

1. **Define.** What is the problem? Who is the customer? What is the defect?
2. **Measure.** What is the current baseline? How do you measure the defect rate?
3. **Analyze.** What are the root causes? (5 Whys, fishbone diagram, Pareto analysis)
4. **Improve.** What changes address the root causes? Pilot and measure.
5. **Control.** How do you sustain the improvement? Monitoring, standard procedures, control charts.

### Worked Example — Reducing Production Incidents

**Define.** Problem: 12 production incidents per month. Customer impact: 4.2 hours average downtime per incident. Goal: reduce to fewer than 4 incidents per month.

**Measure.** Baseline over 3 months:
- 36 total incidents
- Categories: deployment failures (15), database issues (8), third-party API failures (7), infrastructure (6)
- Mean time to resolution (MTTR): 2.1 hours

**Analyze.** Pareto chart shows deployment failures are 42% of incidents. Root cause analysis (5 Whys on the 3 worst deployment incidents):

*Incident: Payment service crashed after deploy.*
1. Why? New version had a null pointer exception.
2. Why? Code path not covered by tests.
3. Why? Unit tests did not cover the error branch.
4. Why? No test coverage requirement for deployments.
5. Why? CI pipeline does not enforce coverage thresholds.

**Root cause:** Missing automated quality gate in the deployment pipeline.

**Improve.**
- Add coverage threshold (80% minimum) to CI pipeline. Deployments blocked if not met.
- Add canary deployments: deploy to 5% of traffic, monitor for 15 minutes, then full rollout.
- Add automated rollback trigger: if error rate exceeds 1% in canary, auto-rollback.

**Control.**
- Monitor incident rate weekly. Alert if 3+ incidents in any week.
- Review canary rollback frequency monthly. High rollback rate means quality problems are being caught (good) but should also trigger upstream investigation (better).

**Results after 3 months.** Incidents dropped from 12/month to 3/month. Deployment-related incidents dropped from 5/month to 0.5/month. MTTR dropped from 2.1 hours to 0.8 hours (canary catches problems before full-scale impact).

## Quality Metrics

### Defect Density

**Formula:** Defects per thousand lines of code (KLOC) or defects per function point.

**Industry benchmarks:**
- Released commercial software: 1-25 defects/KLOC
- NASA flight software: 0.1 defects/KLOC
- Critical systems (medical, avionics): 0.01-0.1 defects/KLOC

**Warning.** Defect density rewards low detection, not high quality. A team that does not test has zero reported defects. Always pair defect density with test coverage and production incident rates.

### Code Coverage

**Types:**
- **Line coverage:** Percentage of lines executed by tests
- **Branch coverage:** Percentage of conditional branches tested (both true and false)
- **Path coverage:** Percentage of execution paths tested (combinatorial explosion makes 100% impractical)

**Guidance:**
- 80% line coverage is a reasonable minimum for business logic
- 90%+ for critical paths (payment, authentication, data integrity)
- 100% line coverage does not mean the code is correct — it means every line was executed during testing, not that every behavior was verified
- Branch coverage matters more than line coverage: `if (a && b)` has 4 branches; line coverage only needs 1 execution to cover the line

### Mean Time Between Failures (MTBF)

**Formula:** Total operating time / Number of failures

**Worked example.** A service ran for 720 hours in a month with 3 failures. MTBF = 720/3 = 240 hours. Target MTBF: 500 hours. The service is failing twice as often as desired.

**Companion metric — MTTR (Mean Time to Recovery).** Availability = MTBF / (MTBF + MTTR). If MTBF = 240 hours and MTTR = 2 hours, availability = 240/242 = 99.17%. For 99.9% availability, need MTBF = 2000 hours (or MTTR = 0.24 hours = 14 minutes).

## Testing Strategies — The Testing Pyramid

### Unit Tests

Test individual functions or methods in isolation. Dependencies are mocked. Execution: milliseconds. Quantity: many (thousands).

**Purpose:** Verify that each unit of code does what its specification says. Catch bugs at the point of introduction.

**GSD connection.** This project runs 21,000+ Vitest tests. The test suite is the primary quality gate — every change must pass the full suite before commit. This is Deming's Point 3 in action: quality built in, not inspected in.

### Integration Tests

Test interactions between components. Real databases, real APIs (or realistic mocks). Execution: seconds to minutes. Quantity: moderate (hundreds).

**Purpose:** Verify that components work together correctly. Catch interface mismatches, protocol errors, and data flow issues that unit tests cannot detect.

### System Tests (End-to-End)

Test the complete system from the user's perspective. Browser automation, API calls through the full stack. Execution: minutes. Quantity: few (tens).

**Purpose:** Verify that the system meets user requirements as a whole. Catch integration issues that only appear in the full deployment context.

### Acceptance Tests

Verify that the system meets business requirements. Written in business language. Often automated as behavior-driven development (BDD) scenarios.

**Purpose:** Confirm that what was built is what was wanted. Close the loop between requirements and delivery.

### The Pyramid Shape

More unit tests, fewer integration tests, even fewer system tests. This is an economic decision:

| Level | Cost to write | Cost to run | Defect localization | Coverage breadth |
|---|---|---|---|---|
| Unit | Low | Very low | Exact (one function) | Narrow |
| Integration | Medium | Medium | Module-level | Medium |
| System | High | High | Poor (somewhere in the stack) | Broad |
| Acceptance | High | Medium | Business rule level | Very broad |

**Anti-pattern — the ice cream cone.** Organizations with many system tests and few unit tests have an inverted pyramid. Tests are slow, brittle, hard to maintain, and provide poor defect localization. Invert toward the pyramid shape.

## Verification and Validation (V&V)

**Verification:** "Are we building the product right?" Does the implementation match the specification?

**Validation:** "Are we building the right product?" Does the product meet the user's actual needs?

These are different questions. A product can pass verification (meets every requirement) and fail validation (users don't want what the requirements specified). Both are necessary.

| Activity | Verification | Validation |
|---|---|---|
| Code review | Reviews implementation against design | — |
| Unit testing | Tests code against unit spec | — |
| Integration testing | Tests interfaces against interface spec | — |
| User acceptance testing | — | Tests product against user needs |
| Usability testing | — | Tests product against user expectations |
| Sprint demo | Partial | Partial (stakeholder feedback) |
| Production usage metrics | — | Real-world validation |

### Hamilton's Priority Displays — Quality Through Architecture

Margaret Hamilton's Apollo team did not rely on testing alone to ensure quality. They designed the software architecture so that certain failure modes were structurally impossible:

- **Priority scheduling.** Critical tasks (navigation, guidance) always preempted non-critical tasks (displays). The computer could not run out of resources for essential functions.
- **Restart protection.** If a task was interrupted by a higher-priority task, it could resume exactly where it left off. No data corruption from preemption.
- **Error detection and recovery.** The system monitored its own behavior. When the 1202 alarms fired during Apollo 11's descent, the software correctly identified that it was overloaded and shed low-priority tasks. The crew landed safely because the error recovery was part of the design, not a test case.

**Lesson for software projects.** The highest form of quality assurance is designing the system so that errors either cannot occur or are handled automatically. Rate limiting, circuit breakers, idempotent operations, immutable data structures — these are quality features, not just engineering preferences.

## Peer Review and Inspection

### Code Review

**Purpose:** Catch defects before they reach testing. Transfer knowledge across the team. Maintain code quality standards.

**Effectiveness data.** Fagan (1976) demonstrated that inspections find 60-90% of defects before testing begins. Code review is the single most cost-effective quality practice — cheaper than any form of testing on a per-defect basis.

**Review checklist (minimal):**
- Does the code do what the PR description says?
- Are there obvious bugs (off-by-one, null dereference, race conditions)?
- Is error handling present and correct?
- Are tests present and meaningful?
- Is the code readable to someone unfamiliar with this module?
- Are there security concerns (injection, authentication bypass, sensitive data exposure)?

### Design Review

Review architecture and design decisions before implementation begins. Cheaper to change a design document than to refactor code.

**Format:** The author presents the design. Reviewers ask "What happens when...?" questions — edge cases, failure modes, scale limits, security boundaries. Output: a list of issues classified as "must fix before implementation," "should address," or "noted for future."

## Continuous Improvement (Kaizen)

Kaizen is the Japanese philosophy of continuous, incremental improvement. In software, it manifests as:

- **Process improvements.** Retrospective action items actually implemented (not just recorded and forgotten).
- **Code improvements.** The Boy Scout Rule: leave the code cleaner than you found it.
- **Tool improvements.** Automating manual steps. Improving CI/CD pipelines. Better monitoring.
- **Knowledge improvements.** Documentation, pairing, tech talks, skill development.

### The Improvement Kata (Mike Rother)

1. **Understand the direction.** What is the long-term target condition?
2. **Grasp the current condition.** Where are we now? Measure.
3. **Establish the next target condition.** Where do we want to be by the next checkpoint?
4. **Experiment toward the target.** PDCA cycles to close the gap.

**Worked example.**
- Direction: Zero production incidents.
- Current: 3 incidents/month.
- Next target: 1 incident/month by end of Q3.
- Experiments: Canary deployments (PDCA cycle 1), coverage requirements (PDCA cycle 2), chaos engineering (PDCA cycle 3).

## Root Cause Analysis in Quality Context

### 5 Whys

Ask "Why?" repeatedly until you reach a systemic root cause. (Cross-reference: rca department for full treatment.)

**Worked example — Build failure.**
1. Why did the build fail? — A test assertion failed.
2. Why did the assertion fail? — The API returned a different date format.
3. Why was the format different? — The upstream service changed their API.
4. Why didn't we know about the change? — No contract test between our service and theirs.
5. Why is there no contract test? — We assumed the API was stable; no policy requiring contract tests for external dependencies.

**Root cause:** Missing policy for contract testing external dependencies. Fix the policy, not just the test.

### Fishbone (Ishikawa) Diagram

Categorize potential causes of a quality problem:

```
Methods ──────┐
               │
Machines ─────├──── [Defect]
               │
Materials ────├────
               │
Measurement ──├────
               │
Manpower ─────├────
               │
Mother Nature ─┘
```

For software, translate the categories:
- **Methods:** Development process, testing strategy, deployment procedure
- **Machines:** Infrastructure, CI/CD tools, development environments
- **Materials:** Code quality, dependencies, documentation
- **Measurement:** Metrics, monitoring, alerting
- **Manpower:** Skills, training, team composition
- **Environment:** Production environment, network, third-party services

## Quality Gates and Definition of Done

### Quality Gates

A quality gate is a checkpoint that work must pass before proceeding to the next phase. Gates prevent defective work from propagating downstream, where it becomes exponentially more expensive to fix.

**Standard gates:**

| Gate | Checks |
|---|---|
| **Pre-commit** | Linting, formatting, type checking |
| **Pre-merge** | All tests pass, code review approved, coverage threshold met |
| **Pre-deploy** | Integration tests pass, security scan clear, performance benchmark within tolerance |
| **Post-deploy** | Canary health check, error rate < threshold, latency < SLA |

**GSD's quality gates.** GSD implements quality gates through its phase structure. The verify phase is a mandatory gate between execute and completion. PreToolUse hooks enforce commit conventions. The audit-fix pipeline (gsd-audit-fix) is an automated quality sweep.

### Definition of Done (DoD)

A shared agreement on what "done" means. Without it, "done" means something different to every team member.

**Example DoD:**
- Code reviewed and approved by at least one peer
- All unit tests pass; new code has tests
- Branch coverage above 80% for changed files
- No P1/P2 defects open against the feature
- Documentation updated (API docs, README, changelog)
- Deployed to staging and smoke-tested
- Product Owner accepted the story

**Why DoD matters.** Without DoD, "done" means "it works on my machine." With DoD, "done" means "it is ready for production." The gap between these two definitions is where defects live.

## Technical Debt Management

### Debt as Quality Metric

Technical debt is the implied cost of future rework caused by choosing an expedient solution now instead of a better approach that would take longer.

**Types:**
- **Deliberate debt.** "We know this is a shortcut. We'll fix it in sprint 5." (Acceptable if tracked.)
- **Inadvertent debt.** "We didn't know there was a better way." (Inevitable; addressed through learning.)
- **Bit rot.** Accumulates silently as the codebase evolves around unchanged code. (Detected through regular audits.)

### Tracking and Paying Down

1. **Track debt items in the backlog** with estimated remediation cost.
2. **Allocate 10-20% of sprint capacity** to debt reduction — every sprint, not "someday."
3. **Pay high-interest debt first.** Debt in frequently-modified code costs more than debt in stable code.
4. **Measure debt impact.** Track the percentage of sprint time spent on rework caused by technical debt. If it exceeds 20%, the debt has become a schedule risk (cross-reference: risk-management skill).

### Worked Example — Debt Quadrant Assessment

| | Reckless | Prudent |
|---|---|---|
| **Deliberate** | "We don't have time for tests." | "We must ship now; we'll add tests next sprint." |
| **Inadvertent** | "What's a design pattern?" | "Now we know how this should have been built." |

Prudent/deliberate debt is healthy engineering trade-off. Reckless debt (either deliberate or inadvertent) signals a quality culture problem that management must address (Deming's Point 7: institute leadership).

## When to Use / When NOT to Use

### When to use formal quality assurance

- Projects with production users who depend on reliability
- Systems where defects have financial, safety, or reputational consequences
- Teams larger than 2 people (peer review requires peers)
- Any project that will be maintained beyond initial delivery

### When NOT to use formal quality assurance

- Throwaway prototypes and spikes (build fast, learn, discard)
- When QA process becomes quality theater — elaborate procedures that catch nothing and slow everything
- When 100% coverage becomes the goal instead of confidence (the last 5% of coverage costs more than the first 80% and catches fewer bugs)
- When "quality" becomes an excuse to never ship

### The quality paradox

The highest-quality teams ship the fastest. This is counterintuitive only if you equate quality with slow, careful, bureaucratic processes. In reality, quality practices (TDD, CI, code review, small PRs) reduce rework, reduce debugging time, and increase confidence to refactor and deploy. Deming was right: quality and productivity are allies, not enemies.

## Cross-References

- **deming agent:** Primary agent for quality management. Deming's 14 Points, PDCA, statistical process control, continuous improvement philosophy.
- **hamilton agent:** Systems engineering quality — error prevention through architecture, priority-based degradation, V&V for complex systems.
- **brooks agent:** Department chair. Quality at scale — why adding people does not improve quality, organizational structures that support or undermine quality.
- **lei agent:** Lean quality — eliminating waste (defects as waste), building quality into the flow rather than inspecting at the end.
- **risk-management skill:** Defects as risk events, quality metrics as risk indicators, FMEA for systematic defect prevention.
- **retrospective-learning skill:** Retrospectives as the engine for quality improvement, lessons learned feeding back into process.
- **agile-methods skill:** Definition of Done, TDD, continuous integration — Agile practices that embed quality into the development flow.
- **rca department (root-cause-analysis, blameless-postmortem skills):** Full treatment of 5 Whys, fishbone diagrams, and blameless postmortem methodology.

## References

- Deming, W. E. (1986). *Out of the Crisis*. MIT Press.
- Juran, J. M. (1988). *Juran on Planning for Quality*. Free Press.
- Fagan, M. E. (1976). "Design and Code Inspections to Reduce Errors in Program Development." *IBM Systems Journal*, 15(3), 182-211.
- Hamilton, M. H. & Hackler, W. R. (2008). "Universal Systems Language: Lessons Learned from Apollo." *IEEE Computer*, 41(12), 34-43.
- Rother, M. (2009). *Toyota Kata*. McGraw-Hill.
- Pyzdek, T. & Keller, P. A. (2014). *The Six Sigma Handbook*. 4th edition. McGraw-Hill.
- Humble, J. & Farley, D. (2010). *Continuous Delivery*. Addison-Wesley.
- McConnell, S. (2004). *Code Complete*. 2nd edition. Microsoft Press.
- Cunningham, W. (1992). "The WyCash Portfolio Management System." *OOPSLA Experience Report*.
