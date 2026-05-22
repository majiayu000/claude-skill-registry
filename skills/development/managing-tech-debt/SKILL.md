---
name: "managing-tech-debt"
description: "Manage technical debt by producing a Tech Debt Management Pack (debt register, scoring/prioritization, refactor vs rewrite decision memo, incremental paydown plan, migration/rollback plan, metrics, and stakeholder cadence). Use for tech debt, refactoring, legacy modernization, and migrations."
---

# Managing Tech Debt

## Scope

**Covers**
- Identifying and making technical debt **visible** (including user-visible symptoms)
- Prioritizing debt work using a **transparent scoring model**
- Deciding **refactor vs migrate vs rebuild vs deprecate** with explicit criteria
- Planning **incremental modernization** (avoid “rewrite traps”)
- Building a **business case** for hard-to-measure investments (metrics + small tests)
- Creating an execution-ready **paydown plan** with risks, milestones, and comms

**When to use**
- “Create a tech debt register and prioritize what to fix next quarter.”
- “We’re considering a rewrite/migration—help us make the call and plan it safely.”
- “Our legacy system slows delivery—build a paydown plan with milestones and metrics.”
- “Leadership won’t fund refactors—quantify impact and propose a measurable plan.”

**When NOT to use**
- You need to respond to an active incident (use incident response/runbooks)
- You only need to fix a small localized bug or a single refactor (just do the work)
- You need a full architecture redesign from scratch without existing constraints (separate architecture/design process)
- You need roadmap prioritization across many product bets (use `prioritizing-roadmap`)

## Inputs

**Minimum required**
- System/service(s) in scope + brief description
- Primary pain: reliability risk, velocity tax, scalability/perf, security/compliance, operability, UX fragmentation, cost
- Time horizon (e.g., “6 weeks”, “next quarter”, “12 months”) + any fixed deadlines
- Stakeholders + decision-maker(s) (Eng/PM/Design/Leadership)
- Constraints: team capacity, freeze windows, compliance/security requirements

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed with explicit assumptions.
- If estimates are unavailable, use **ranges** and label confidence.
- Do not request secrets/credentials; use redacted or synthetic identifiers if needed.

## Outputs (deliverables)

Produce a **Tech Debt Management Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (scope, pains, constraints, stakeholders, success definition)
2) **Tech Debt Register** (inventory table with owners, symptoms, impact, effort range, risks)
3) **Scoring + prioritization** (model + ranked list + rationale)
4) **Strategy decision(s)** (refactor/migrate/rebuild/deprecate) with explicit criteria
5) **Execution plan** (incremental milestones, sequencing, resourcing, decommission plan)
6) **Migration + rollback plan** (if applicable; includes “dual-run” cost/plan)
7) **Metrics plan** (baseline, targets, leading indicators, instrumentation gaps, small tests)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the decision(s) to be made, scope boundaries, time horizon, and constraints. Define what “success” means (e.g., fewer incidents, faster deploys, simpler UX integration).
- **Outputs:** Context snapshot (draft).
- **Checks:** A stakeholder can answer: “What will we decide/do differently after reading this?”

### 2) Surface the “debt symptoms” (user + engineering)
- **Inputs:** Known pain points; incident/perf history if available; qualitative reports.
- **Actions:** List user-visible symptoms (inconsistent UX, broken integrations, slow workflows) and engineering symptoms (deploy pain, flaky tests, high MTTR, brittle dependencies). Map symptoms → suspected debt sources.
- **Outputs:** Symptoms → suspected causes map (bullet list).
- **Checks:** At least 1 symptom is tied to a measurable signal (latency, errors, cycle time, support volume) or explicitly marked “needs instrumentation”.

### 3) Build the Tech Debt Register (inventory)
- **Inputs:** Repos/services/components in scope; symptoms map.
- **Actions:** Create a debt register with a consistent schema (type, location, current workaround, impact, risk, rough effort, dependencies, owner). Separate “must fix” from “nice to have.”
- **Outputs:** Tech Debt Register (table).
- **Checks:** Every item has an owner, an impact statement, and an effort **range** (even if coarse).

### 4) Score and prioritize (make trade-offs explicit)
- **Inputs:** Debt register.
- **Actions:** Score items on impact and risk (user harm, reliability, security, velocity tax) vs effort and sequencing constraints. Produce a ranked list and explain the top 5–10.
- **Outputs:** Scoring model + prioritized list.
- **Checks:** Top-ranked items are defensible: rationale references symptoms/signals and constraints, not “taste”.

### 5) Decide strategy per top item: refactor vs migrate vs rebuild vs deprecate
- **Inputs:** Top-ranked debt items; constraints; required capabilities (incl. operational flexibility).
- **Actions:** For each top item, pick a strategy and document options + criteria. If proposing a rebuild, include a plan to avoid the rewrite trap: migration phases, parallel support cost, cutover and decommission.
- **Outputs:** Strategy decision(s) + decision memo(s).
- **Checks:** For any “rebuild/migrate” decision, the plan includes a **decommission path** and acknowledges **dual-run** cost.

### 6) Create the incremental execution plan
- **Inputs:** Strategy decisions; constraints; dependencies.
- **Actions:** Convert work into milestones (thin slices), define sequencing, and set resourcing/capacity (e.g., % per sprint). Add explicit “done means decommissioned” criteria for migrations.
- **Outputs:** Execution plan (milestones + owners + timeline).
- **Checks:** Each milestone has a measurable acceptance criterion and a rollback/stop condition.

### 7) Quantify value: metrics + small tests
- **Inputs:** Baselines (or estimates); execution plan.
- **Actions:** Define metrics that make the investment fundable (e.g., incident rate, MTTR, p95 latency, deploy frequency, lead time, cost). Where impact is hard to measure, propose a small test (limited rollout, canary, instrumentation spike).
- **Outputs:** Metrics plan (baseline → target → measurement method).
- **Checks:** Metrics include at least 1 leading indicator and 1 guardrail; instrumentation gaps are listed with owners.

### 8) Align stakeholders + quality gate + finalization
- **Inputs:** Draft pack.
- **Actions:** Add stakeholder cadence (updates, review gates). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score using [references/RUBRIC.md](references/RUBRIC.md). Finalize **Risks / Open questions / Next steps**.
- **Outputs:** Final Tech Debt Management Pack.
- **Checks:** Plan is incrementally executable, risks are explicit, and the first milestone can start immediately.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (quarterly planning):** “Use `managing-tech-debt`. System: payments-service. Pain: frequent incidents + slow delivery. Horizon: next quarter. Output: a Tech Debt Management Pack with a prioritized register and paydown plan.”

**Example 2 (rewrite decision):** “We want to rebuild our pricing engine. Compare refactor vs rebuild, include migration phases, dual-run costs, rollback plan, and a metrics-based justification.”

**Boundary example:** “Tell me whether tech debt is bad and how to avoid it.”  
Response: explain this skill produces an actionable pack; ask for system + pain + horizon; otherwise provide a minimal intake checklist and an example register schema.

