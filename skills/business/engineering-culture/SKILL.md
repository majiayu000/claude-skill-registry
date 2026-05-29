---
name: "engineering-culture"
description: "Build or refresh engineering culture and produce an Engineering Culture Operating System Pack (capability map, culture code, org↔architecture alignment, clock-speed/DevEx backlog, workflow contract, rollout + measurement). Use for engineering culture, DevOps capabilities, DevEx, clock speed, Conway's Law, and engineering principles. Category: Engineering."
---

# Engineering Culture

## Scope

**Covers**
- Diagnosing the current engineering culture *and* delivery system (technical, architectural, cultural, and management capabilities)
- Defining a clear **engineering culture code** (principles → behaviors → decision rules → anti-patterns)
- Aligning org structure with architecture (Conway’s Law) and reducing cross-team friction
- Increasing **clock speed** (safe shipping + experimentation throughput) and improving DevEx
- Creating a practical cross-functional workflow contract (how engineering + PM/Design/Marketing collaborate in the same toolchain)
- Making AI-assisted development safe and effective (humans as “architects”: spec, review, and oversight)

**When to use**
- “Help me improve engineering culture / DevEx and make it concrete.”
- “Our delivery is slow—build a plan to increase shipping speed without breaking things.”
- “Our org structure fights our architecture—analyze Conway’s Law and propose changes.”
- “We want tighter processes and faster experimentation (higher clock speed).”
- “Non-engineering functions struggle to work with engineering—define a shared workflow contract.”
- “We’re adopting AI coding tools/agents—set norms so engineers shift toward higher-level design and review.”

**When NOT to use**
- You need to respond to an active incident or outage (use incident response/runbooks)
- You need HR/legal policy, investigations, or employee relations handling (involve HR/legal)
- You only need to implement a specific technical improvement (e.g., “set up CI”) without culture/org/process work
- You need a full company strategy/roadmap prioritization across many bets (use `prioritizing-roadmap`)

## Inputs

**Minimum required**
- Org context: product(s), stage, engineering size, team topology, on-call model
- Current symptoms + 2–5 examples (e.g., slow delivery, flaky deploys, low ownership, poor collaboration, high toil)
- Current delivery system snapshot (release cadence, CI/CD maturity, test strategy, environments)
- Architecture constraints (e.g., monolith vs services; coupling hotspots; ownership boundaries)
- Cross-functional workflow reality (where work is tracked, how decisions are made, how releases happen)
- Desired outcomes (what should be *more true* in 4–12 weeks?) + timeline constraints

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time), then proceed with explicit assumptions.
- If metrics are missing, use best-effort ranges and label confidence; list instrumentation gaps.
- Do not request secrets, credentials, or proprietary identifiers; use redacted summaries.

## Outputs (deliverables)

Produce an **Engineering Culture Operating System Pack** in Markdown (in-chat; or as files if requested):

1) **Culture + capability snapshot** (what’s true today; evidence; capability gaps)
2) **Engineering culture code (v1)** (3–7 principles with behaviors, do/don’t, decision rules, anti-patterns)
3) **Org ↔ architecture alignment brief** (Conway’s Law analysis + proposed operating model changes)
4) **Clock speed + DevEx improvement backlog** (prioritized initiatives with owners, sequencing, metrics)
5) **Cross-functional workflow contract** (GitHub/issue/PR/release norms; how non-engineers contribute; AI norms)
6) **Rollout + measurement plan** (30/60/90, rituals, metrics + guardrails, feedback loops)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + boundary setting
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm scope (team vs org), decision owner(s), timeline, and constraints. Identify any HR/legal or active-incident concerns and route appropriately. Confirm which deliverables to produce.
- **Outputs:** Context snapshot + assumptions/unknowns list.
- **Checks:** Scope boundaries are explicit; success definition is stated in observable terms.

### 2) Diagnose the current culture as a delivery system (capability map)
- **Inputs:** Symptoms/examples; current process/tooling; architecture context.
- **Actions:** Build a capability map across **technical**, **architectural**, **cultural**, and **management** capabilities. Capture evidence and gaps (not platitudes). Distinguish stated culture vs lived culture.
- **Outputs:** Culture + capability snapshot (draft).
- **Checks:** Each claimed problem has at least one piece of evidence (example, metric, observed behavior) or is labeled “needs data”.

### 3) Define the target culture (culture code v1)
- **Inputs:** Snapshot; constraints; what already works.
- **Actions:** Pick 2–4 priority shifts, then write a culture code: 3–7 principles with behaviors, do/don’t, decision rules, and anti-patterns. Prefer rules that increase autonomy while reducing ambiguity.
- **Outputs:** Engineering culture code (v1).
- **Checks:** Every principle includes a concrete “how we work” example and at least one measurable/observable signal.

### 4) Align org structure with architecture (Conway’s Law)
- **Inputs:** Current team topology; architecture coupling/ownership hotspots; dependency pain.
- **Actions:** Map org → architecture fit. Propose changes: team boundaries, ownership, interfaces, and standardization (e.g., leveling definitions, incident policies, review expectations) where misalignment causes friction.
- **Outputs:** Org ↔ architecture alignment brief.
- **Checks:** Proposed changes include migration/transition steps and explicit trade-offs (what gets worse).

### 5) Increase clock speed (safe shipping + experimentation throughput)
- **Inputs:** Current shipping/experiment cadence; pipeline constraints; quality constraints.
- **Actions:** Define “clock speed” targets and bottlenecks. Propose initiatives that raise throughput safely (small batches, CI reliability, test strategy, progressive delivery, observability). Convert into a prioritized backlog.
- **Outputs:** Clock speed + DevEx improvement backlog (draft).
- **Checks:** Each initiative has an owner, an effort range, a dependency note, and a metric/leading indicator.

### 6) Create the workflow contract (including AI norms)
- **Inputs:** Collaboration pain points; tool constraints; roles.
- **Actions:** Specify how work flows from idea → issue → PR → deploy → learn. Define cross-functional participation (where PM/Design/Marketing contribute) and working agreements (review SLAs, merge/deploy policy, experiment ownership). Add AI-assisted development norms: where agents help, human review requirements, and safe data handling.
- **Outputs:** Cross-functional workflow contract.
- **Checks:** The contract reduces common failure modes (stalled PRs, unclear ownership, “drive-by” requests) and is teachable to new hires.

### 7) Rollout + measurement + quality gate
- **Inputs:** Draft pack.
- **Actions:** Create a 30/60/90 rollout plan with rituals/cadence and training. Define metrics and guardrails (e.g., DORA + quality + DevEx). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Finalize **Risks / Open questions / Next steps**.
- **Outputs:** Final Engineering Culture Operating System Pack.
- **Checks:** The first 1–2 actions can start this week; measurement is feasible; risks/trade-offs are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (slow delivery + DevEx):** “Use `engineering-culture`. Context: B2B SaaS, 35 engineers, monolith + a few services, weekly releases, rising incidents. Goal: increase shipping speed without quality regressions. Output: an Engineering Culture Operating System Pack with a clock-speed backlog and a workflow contract.”

**Example 2 (Conway misalignment):** “We have 6 teams but architecture ownership is unclear and everything depends on platform. Analyze Conway’s Law issues and propose a new operating model + standardization (leveling, code ownership, on-call) plus a rollout plan.”

**Boundary example:** “Write a generic essay about what engineering culture is.”  
Response: explain this skill produces a concrete operating system pack; ask for context/symptoms/timeline or provide the intake checklist and an example template from [references/TEMPLATES.md](references/TEMPLATES.md).
