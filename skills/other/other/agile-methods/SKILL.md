---
name: agile-methods
description: Agile and Lean software development methodologies for iterative, adaptive project execution. Covers Scrum (roles, ceremonies, artifacts), Kanban (WIP limits, flow metrics), XP (TDD, pair programming, CI), SAFe overview, Lean Software Development (Poppendieck's 7 principles), user stories (INVEST criteria), estimation via story points and velocity, and the Agile Manifesto's values and principles. Includes Cynefin framework for methodology selection and GSD's relationship to Agile as a structured Lean variant.
type: skill
category: project-management
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/project-management/agile-methods/SKILL.md
superseded_by: null
---
# Agile Methods

Agile is not a methodology. It is a family of methodologies united by a shared value system: responding to change over following a plan, working software over comprehensive documentation, individuals and interactions over processes and tools, customer collaboration over contract negotiation. The Agile Manifesto (2001) codified these values, but the practices predate it by decades — XP emerged in the late 1990s, Lean manufacturing in the 1950s, iterative development as far back as the 1930s (Shewhart cycle). This skill catalogs the major Agile frameworks, their mechanics, their failure modes, and guidance for selecting the right approach for the problem domain.

**Agent affinity:** lei (agile/lean), brooks (systems management)

**Concept IDs:** bus-business-planning, bus-stakeholder-theory, crit-problem-analysis, crit-evidence-evaluation

## Framework Overview

| # | Framework | Core idea | Best for | Team size |
|---|---|---|---|---|
| 1 | Scrum | Time-boxed sprints with defined roles | Product development, stable teams | 5-9 |
| 2 | Kanban | Continuous flow with WIP limits | Operations, support, variable demand | Any |
| 3 | XP | Engineering discipline as survival | High-change environments, quality-critical | 4-12 |
| 4 | SAFe | Scaled Agile across portfolios | Enterprise, 50+ developers | 50-500+ |
| 5 | Lean SD | Eliminate waste, defer decisions | Any; strategic overlay | Any |
| 6 | GSD | Structured phases + autonomous execution | AI-assisted, solo/small team | 1-5 |

## Framework 1 — Scrum

### Roles

**Product Owner.** Single voice of the customer. Owns the backlog. Makes prioritization decisions. Does not tell the team *how* to build — only *what* and *why*. A committee cannot be a Product Owner; the role requires one person with authority to make trade-offs.

**Scrum Master.** Servant-leader who removes impediments, facilitates ceremonies, and protects the team from external disruption. Not a project manager. Not a boss. The Scrum Master succeeds when the team can self-organize without them.

**Development Team.** Cross-functional, self-organizing group of 5-9 people. No sub-teams, no titles within the team. Everyone shares accountability for the sprint goal.

### Ceremonies

**Sprint Planning.** The team selects work from the backlog for the upcoming sprint. Two questions: (1) What can we deliver this sprint? (2) How will we do the work? Output: sprint backlog and sprint goal. Time-box: 2 hours per sprint week (4 hours for a 2-week sprint).

**Daily Standup (Daily Scrum).** 15 minutes, same time, same place. Each person answers: What did I do yesterday? What will I do today? What's blocking me? This is a synchronization meeting, not a status report to management.

**Sprint Review.** Demonstrate completed work to stakeholders. Inspect the increment. Gather feedback. This is not a presentation — it is a working session. Stakeholders should interact with the software.

**Sprint Retrospective.** The team reflects on process: What went well? What didn't? What will we change? The retrospective is the engine of continuous improvement. Without it, Scrum degrades into mechanical ritual. (Cross-reference: retrospective-learning skill for detailed formats.)

### Artifacts

**Product Backlog.** Ordered list of everything the product might need. Owned by the Product Owner. Never complete — it evolves as the product and market evolve.

**Sprint Backlog.** Subset of the product backlog selected for the current sprint, plus the plan for delivering it. Owned by the Development Team.

**Increment.** The sum of all completed product backlog items during a sprint and all previous sprints. Must meet the Definition of Done.

### Worked Example — Sprint Planning

**Scenario.** A team of 7 has a 2-week sprint. Historical velocity: 34 story points per sprint. The product backlog has 12 stories at the top, estimated between 2 and 13 points.

**Planning session.** The Product Owner presents the top items and explains the sprint goal: "Users can complete checkout without creating an account." The team discusses each story, asking clarifying questions. They pull stories in order:

| Story | Points | Running total |
|---|---|---|
| Guest checkout flow | 8 | 8 |
| Payment validation | 5 | 13 |
| Order confirmation email | 3 | 16 |
| Address autocomplete | 5 | 21 |
| Cart persistence | 8 | 29 |
| Error handling for declined cards | 3 | 32 |

At 32 points, the team stops. The next story is 5 points (total 37), which exceeds their velocity. They commit to 6 stories, 32 points. The sprint goal is achievable.

**What can go wrong.** The Product Owner pressures the team to take the 7th story ("just stretch a little"). The Scrum Master intervenes: sustainable pace matters more than one sprint's output. Overcommitment is the most common sprint planning failure — it erodes trust in velocity as a forecasting tool.

### When Scrum Works

- The product is evolving and requirements change frequently
- A stable, cross-functional team works on a single product
- Stakeholders are available for regular feedback
- The organization respects the sprint boundary (no mid-sprint scope injection)

### When Scrum Fails

- The team is pulled across multiple products (fractured attention)
- Work items are mostly small, unpredictable interrupts (use Kanban instead)
- Leadership treats Scrum ceremonies as status meetings
- "Agile" is adopted as vocabulary without the underlying value shift ("Agile theater")

## Framework 2 — Kanban

### Core Principles

**Visualize the workflow.** A Kanban board makes invisible work visible. Columns represent stages: To Do, In Progress, Review, Done. Every work item is a card that moves left to right.

**Limit work in progress (WIP).** Each column has a maximum number of items. If the limit is reached, no new work enters that column until something exits. WIP limits are the mechanism by which Kanban controls flow.

**Manage flow.** Measure lead time (request to delivery) and cycle time (start to delivery). Optimize for smooth, predictable flow — not for utilization.

**Make policies explicit.** Definition of Done, pull criteria, escalation rules — all visible on the board.

**Improve collaboratively.** Use data (cumulative flow diagrams, lead time distributions) to identify bottlenecks and experiment with solutions.

### Flow Metrics

**Lead time.** Time from when a request enters the system to when it is delivered. This is the customer's experience.

**Cycle time.** Time from when work begins to when it is delivered. This is the team's experience.

**Throughput.** Number of items delivered per unit time.

**WIP.** Number of items in progress at any moment.

**Little's Law.** Lead Time = WIP / Throughput. This is not a heuristic — it is a mathematical law for stable systems. It means you can reduce lead time by reducing WIP *without* increasing throughput.

### Worked Example — WIP Limit Experiment

**Scenario.** A support team has 5 developers. Their board has no WIP limits. Average cycle time: 8 days. Average WIP: 20 items. Throughput: 2.5 items/day.

**Intervention.** Set WIP limit of 3 per developer (15 total for the "In Progress" column). Initially painful — developers must finish current work before starting new work.

**After 4 weeks.** WIP stabilizes at 12. Cycle time drops to 5 days. Throughput remains 2.5 items/day. By Little's Law: 12 / 2.5 = 4.8 days (close to observed 5 days). The team delivers the same volume but faster, because items spend less time waiting.

### When to Use Kanban Over Scrum

- Work arrives unpredictably (support tickets, operations)
- Items vary wildly in size and cannot be batched into uniform sprints
- The team serves multiple stakeholders with competing priorities
- You want to improve an existing process incrementally rather than adopt a new framework wholesale

## Framework 3 — Extreme Programming (XP)

### The 12 Practices

XP is built on engineering discipline, not management process. The practices reinforce each other — adopting some without others weakens the system.

1. **Planning game.** Customer and developers negotiate scope for each iteration.
2. **Small releases.** Ship frequently. Smaller releases mean faster feedback.
3. **Metaphor.** Shared vocabulary (system metaphor) to align understanding.
4. **Simple design.** Build for today's requirements, not tomorrow's speculation.
5. **Test-driven development (TDD).** Write the test before the code. Red-green-refactor.
6. **Refactoring.** Continuously improve design without changing behavior.
7. **Pair programming.** Two developers, one keyboard. Driver writes code; navigator reviews in real time.
8. **Collective code ownership.** Anyone can change any code. No gatekeepers.
9. **Continuous integration.** Merge to mainline multiple times per day. Build and test on every merge.
10. **40-hour week.** Sustainable pace. Overtime is a sign of planning failure.
11. **On-site customer.** A real customer sits with the team to answer questions.
12. **Coding standards.** Agreed conventions so code reads as if one person wrote it.

### TDD Cycle

1. **Red.** Write a failing test that specifies the desired behavior.
2. **Green.** Write the minimum code that makes the test pass.
3. **Refactor.** Clean up the code while all tests remain green.

**Why TDD matters.** The test suite is a living specification. It catches regressions immediately. It documents intent. It gives developers confidence to refactor aggressively. Without TDD, refactoring becomes terrifying and stops — technical debt accumulates.

### When XP Works

- Requirements change weekly or daily
- Quality failures are expensive (financial, safety, reputational)
- The team is co-located or has high-bandwidth communication
- Management supports the engineering investment (TDD and pairing look "slow" to uninformed observers; they are faster over project lifetime)

## Framework 4 — SAFe (Scaled Agile Framework) Overview

SAFe extends Agile to large organizations through four configurations: Essential, Large Solution, Portfolio, and Full. The core construct is the **Agile Release Train (ART)** — a long-lived team of teams (50-125 people) that plans, commits, and delivers together in **Program Increments (PIs)** of 8-12 weeks (typically 5 sprints of 2 weeks + 1 Innovation and Planning sprint).

**PI Planning.** All teams in the ART gather (physically or virtually) for a 2-day planning event. Teams identify dependencies, negotiate scope, and commit to PI objectives. This ceremony is SAFe's highest-value practice.

**When SAFe is appropriate.** Large organizations (100+ developers) building complex systems with significant cross-team dependencies. SAFe provides structure for coordination at scale.

**When SAFe is overhead.** Small organizations or autonomous teams. SAFe's ceremony load is heavy — if you can achieve alignment with lighter mechanisms (Scrum of Scrums, informal coordination), prefer them.

## Framework 5 — Lean Software Development

### Poppendieck's 7 Principles

Mary and Tom Poppendieck translated Toyota Production System principles to software:

1. **Eliminate waste.** Anything that does not add value to the customer is waste: partially done work, extra features, task switching, handoffs, delays, defects.
2. **Amplify learning.** Use feedback loops (tests, demos, retrospectives) to learn faster. Software development is a learning process, not a production process.
3. **Decide as late as possible.** Defer irreversible decisions until the last responsible moment. Earlier decisions are made with less information.
4. **Deliver as fast as possible.** Speed enables feedback. Long cycles mean stale feedback. Compress cycle time relentlessly.
5. **Empower the team.** People closest to the work make the best decisions. Push authority to the lowest level.
6. **Build integrity in.** Conceptual integrity (the system feels coherent to users) and structural integrity (the code is well-designed for change). Quality is not an afterthought.
7. **Optimize the whole.** Sub-optimizing components (e.g., maximizing developer utilization) degrades the system. Optimize end-to-end flow.

### Worked Example — Eliminating Handoff Waste

**Scenario.** A requirements analyst writes specs, hands them to developers, who hand completed code to testers, who hand bug reports back to developers. Each handoff introduces a 2-day queue wait.

**Current lead time.** 3 handoffs x 2 days queue + 5 days active work = 11 days.

**Lean intervention.** Form a cross-functional team: analyst, 2 developers, tester. They work on one feature at a time, sitting together. Handoffs become conversations. Queue time drops to near zero.

**New lead time.** 5 days active work + 0.5 days coordination = 5.5 days. A 50% reduction with no increase in capacity.

## Framework 6 — GSD's Relationship to Agile

GSD (Get Shit Done) is the project management system built into gsd-skill-creator. It shares DNA with Agile and Lean but differs in important ways:

**Structured phases.** GSD uses explicit phases (discuss, plan, execute, verify) rather than time-boxed sprints. Each phase produces defined artifacts. This is closer to staged-delivery than Scrum.

**Autonomous execution.** GSD phases can run autonomously with AI assistance. The "discuss" phase gathers context adaptively. The "plan" phase produces PLAN.md. The "execute" phase runs wave-based parallelization. This maps to Lean's "empower the team" principle — the AI operates within guardrails rather than awaiting step-by-step instruction.

**Wave execution as a Lean variant.** GSD's wave execution bundles independent tasks for parallel execution, then synchronizes at wave boundaries. This is a pull system: the next wave pulls from the plan, not pushed by a schedule. WIP is naturally limited by wave scope.

**Session-to-session retrospectives.** GSD's handoff documents (HANDOFF-SESSION-*.md) and STATE.md serve the same purpose as Agile retrospectives — they preserve context and enable continuous improvement. The difference: they are structured for AI context windows rather than human meetings.

**Dogfooding.** This project-management department exists within the system it describes. GSD's own phases, retrospectives, and estimation patterns are the working implementation of the theory cataloged here.

## The Agile Manifesto — Values and Principles

### Four Values (2001)

1. **Individuals and interactions** over processes and tools
2. **Working software** over comprehensive documentation
3. **Customer collaboration** over contract negotiation
4. **Responding to change** over following a plan

The "over" does not mean the right side is valueless — it means, when forced to choose, the left side wins.

### Twelve Principles (Selected)

- Deliver working software frequently (weeks, not months)
- Welcome changing requirements, even late in development
- Business people and developers work together daily
- Build projects around motivated individuals; trust them
- The most efficient communication is face-to-face conversation
- Working software is the primary measure of progress
- Sustainable development — sponsors, developers, and users should maintain a constant pace
- Simplicity — maximizing the amount of work not done
- The best architectures, requirements, and designs emerge from self-organizing teams
- At regular intervals, the team reflects and adjusts

## Methodology Selection — The Cynefin Framework

Dave Snowden's Cynefin framework classifies problem domains to guide methodology choice:

| Domain | Characteristics | Approach | Methodology fit |
|---|---|---|---|
| Clear (Simple) | Cause-effect obvious | Sense-Categorize-Respond | Checklists, SOPs, Kanban |
| Complicated | Cause-effect discoverable by experts | Sense-Analyze-Respond | Waterfall (if stable), Scrum |
| Complex | Cause-effect only visible in retrospect | Probe-Sense-Respond | Scrum, XP, Lean, GSD |
| Chaotic | No cause-effect relationships visible | Act-Sense-Respond | Whatever works NOW; stabilize first |
| Confused | Don't know which domain you're in | Break the problem into parts | Investigate before choosing |

**Most software is Complex.** Requirements emerge through building. Feedback loops are essential. This is why Agile methods dominate software — they are designed for complexity.

**When Agile doesn't work.** Safety-critical systems with regulatory compliance (avionics, medical devices) often require traceable, upfront requirements. Hybrid approaches work: Agile development within a V-model verification framework. Hardware-dominated systems with long lead times benefit from staged delivery rather than pure iteration.

## User Stories — INVEST Criteria

A well-formed user story is:

- **I**ndependent — Can be developed and delivered without coupling to other stories
- **N**egotiable — Not a contract; details emerge through conversation
- **V**aluable — Delivers value to the user or customer
- **E**stimable — Small enough and clear enough for the team to estimate
- **S**mall — Fits within a single sprint
- **T**estable — Has clear acceptance criteria

**Story template.** "As a [role], I want [capability], so that [benefit]."

**Worked example.** "As a returning customer, I want to see my recent orders on the dashboard, so that I can quickly reorder items I buy frequently."

**Acceptance criteria:**
- Dashboard shows the 5 most recent orders
- Each order displays date, total, and item count
- Clicking an order opens the order detail page
- Orders older than 1 year are excluded

**Anti-pattern.** "As a developer, I want to refactor the database layer." This fails INVEST: it is not valuable to the user. Reframe: "As a customer, I want search results in under 2 seconds, so that I can find products without waiting." The refactoring is the *how*, not the *what*.

## Estimation — Story Points and Velocity

**Story points** measure relative complexity, not hours. A story estimated at 5 points is roughly 2.5x the effort of a 2-point story. The Fibonacci sequence (1, 2, 3, 5, 8, 13, 21) is the standard scale — the gaps increase to reflect increasing uncertainty at larger sizes.

**Velocity** is the number of story points completed per sprint. After 3-5 sprints, velocity stabilizes and becomes a reliable forecasting tool.

**Planning poker.** Each team member privately selects a card (Fibonacci number). Cards are revealed simultaneously. If estimates diverge significantly (e.g., one person says 3, another says 13), the high and low estimators explain their reasoning. The team converges through discussion, not averaging.

**Common mistake — converting points to hours.** The moment management starts calculating "1 point = 4 hours," story points lose their purpose. They exist specifically to decouple estimation from time, because humans estimate relative complexity more accurately than absolute duration.

## When to Use / When NOT to Use

### When to use Agile methods

- Requirements are uncertain or evolving
- Feedback from real users is available and frequent
- The team is empowered to make technical decisions
- The organization values outcomes over outputs

### When NOT to use Agile methods

- Regulatory environments requiring full upfront traceability (without hybrid adaptation)
- Fixed-scope, fixed-price contracts with no flexibility (Agile requires scope negotiation)
- Teams with no access to stakeholders or users (feedback loops are essential)
- Organizations that adopt Agile vocabulary without changing management culture ("Agile in name only")
- Trivially simple projects with well-understood requirements (a checklist suffices)

## Cross-References

- **lei agent:** Primary agent for Agile and Lean methodology guidance. Lean optimization, waste identification, flow analysis.
- **brooks agent:** Department chair. Systems thinking, organizational dynamics, Brooks's Law applied to Agile team scaling.
- **goldratt agent:** Theory of Constraints applied to Agile flow — bottleneck identification, buffer management in sprints.
- **deming agent:** Quality integration within Agile — continuous improvement, PDCA cycle as the engine under retrospectives.
- **retrospective-learning skill:** Detailed retrospective formats, blameless postmortem patterns, and organizational learning theory.
- **estimation-planning skill:** Estimation techniques (PERT, reference class forecasting) that complement story point estimation.
- **quality-assurance skill:** Deming's quality framework applied to Agile Definition of Done and testing strategies.
- **stakeholder-communication skill:** Communication planning and stakeholder management in Agile contexts.

## References

- Beck, K. et al. (2001). *Manifesto for Agile Software Development*. agilemanifesto.org.
- Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide*. scrumguides.org.
- Anderson, D. J. (2010). *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press.
- Beck, K. (2004). *Extreme Programming Explained*. 2nd edition. Addison-Wesley.
- Poppendieck, M. & Poppendieck, T. (2003). *Lean Software Development: An Agile Toolkit*. Addison-Wesley.
- Snowden, D. J. & Boone, M. E. (2007). "A Leader's Framework for Decision Making." *Harvard Business Review*, 85(11), 68-76.
- Cohn, M. (2005). *Agile Estimating and Planning*. Prentice Hall.
- Scaled Agile Inc. (2023). *SAFe 6.0 Framework*. scaledagileframework.com.
- Brooks, F. P. (1975/1995). *The Mythical Man-Month*. Addison-Wesley.
