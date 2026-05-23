---
name: "systems-thinking"
description: "Apply systems thinking to leadership decisions and produce a Systems Thinking Pack (system boundary, actors & incentives map, feedback loops, second-order effects ledger, leverage points, intervention plan). Use for complex ecosystems, trade-offs, org/process redesign, and preventing unintended consequences."
---

# Systems Thinking

## Scope

**Covers**
- Seeing the “whole system” behind a problem (actors, incentives, feedback loops, culture/rules)
- Anticipating second- and third-order effects (including time delays)
- Finding leverage points (small changes with outsized impact)
- Converting recurring pain into a reusable system (process, automation, or operating mechanism)

**When to use**
- “This is a complex ecosystem; we’re missing the bigger picture.”
- “What are the second-order effects if we do X?”
- “We keep solving symptoms—what’s the system causing this?”
- “Map the players + incentives and how they interact.”
- “We need to redesign a process/org without unintended consequences.”

**When NOT to use**
- The problem is simple/linear and mostly execution (use a project plan/timeline).
- You need primary user research or data you don’t have (do discovery first).
- You need deep quantitative forecasting/simulation (this skill produces a qualitative map + risks, not a full model).
- The decision is low-impact and fully reversible (don’t over-invest).

## Inputs

**Minimum required**
- The focal decision or problem statement (1–2 sentences)
- Desired outcome + time horizon (default: 6–12 months)
- Known constraints/guardrails (trust, safety, compliance, budget, headcount)
- Known actors/stakeholders (teams, users, partners, regulators, vendors)
- What has been tried already (and what happened)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with clearly labeled assumptions and provide 2–3 alternative system framings/boundaries.

## Outputs (deliverables)

Produce a **Systems Thinking Pack** in Markdown (in-chat; or as files if requested) in this order:

1) **Context + System boundary** (goal, scope, non-scope, time horizon)
2) **Actors & incentives map** (players, goals, constraints, power, conflicts)
3) **System map** (key variables + causal links) + **feedback loops** (reinforcing/balancing) + **time delays**
4) **Second-/third-order effects ledger** for the top 1–3 decisions
5) **Leverage points** + **intervention plan** (actions, owners, sequencing, guardrails)
6) **System-build opportunities** (what to automate/standardize to reduce recurring pain)
7) **Risks / Open questions / Next steps** (required)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + pick the focal decision/problem
- **Inputs:** User context; use [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Restate the focal decision/problem, desired outcome, and time horizon; list constraints/guardrails.
- **Outputs:** Draft **Context + System boundary**.
- **Checks:** The problem is not a solution in disguise; scope and non-scope are explicit.

### 2) Define the system boundary (what’s “in” vs “out”)
- **Inputs:** Problem statement + constraints.
- **Actions:** Choose a boundary that is useful (not everything). Name the primary outcome metric(s) and a few leading indicators.
- **Outputs:** Boundary statement + success measures.
- **Checks:** Boundary is tight enough to act on, but wide enough to include key externalities.

### 3) Map actors + incentives (multi-agent reality)
- **Inputs:** Boundary + stakeholder list.
- **Actions:** Enumerate actors/players; capture incentives, constraints, power, and likely behaviors.
- **Outputs:** **Actors & incentives map** (table).
- **Checks:** Includes at least 1–2 “invisible” actors (e.g., policies, culture norms, platform constraints) if relevant.

### 4) Build a simple system map (variables + causal links)
- **Inputs:** Actors map + known dynamics.
- **Actions:** List key variables; map causal links (“A increases B”, “C decreases D”); mark time delays.
- **Outputs:** **System map** (text/table) with 10–20 high-signal links.
- **Checks:** Links are directional and testable; avoids buzzwords (“alignment”, “quality”) without definition.

### 5) Identify feedback loops + time delays
- **Inputs:** System map.
- **Actions:** Extract reinforcing and balancing loops; note where delays create overshoot/oscillation; flag common traps.
- **Outputs:** **Feedback loops** section (2–6 loops) + delays list.
- **Checks:** Each loop has a short “so what” describing the pattern it creates.

### 6) Run second-/third-order effects on 1–3 candidate moves
- **Inputs:** Candidate decisions/actions.
- **Actions:** For each move, enumerate first-, second-, and third-order effects; include who wins/loses and what constraints tighten over time.
- **Outputs:** **Second-/third-order effects ledger**.
- **Checks:** Includes at least one unintended consequence + one mitigating action per move.

### 7) Choose leverage points + design interventions (including “build a system”)
- **Inputs:** Loops + effects ledger.
- **Actions:** Identify leverage points (policy, incentives, information flows, tooling, process); propose interventions; include at least one system-build/automation opportunity for recurring pain.
- **Outputs:** **Leverage points + intervention plan** + **System-build opportunities**.
- **Checks:** Each intervention has an owner, a measurable leading indicator, and a guardrail.

### 8) Quality gate + finalize pack
- **Inputs:** All draft sections.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add **Risks / Open questions / Next steps**.
- **Outputs:** Final **Systems Thinking Pack**.
- **Checks:** A reader can act without a live meeting; trade-offs and uncertainties are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Org/process):** “Our on-call load keeps rising and teams are burned out. Map the system and propose leverage points.”  
Expected: an actors/incentives map (teams, incidents, incentives), feedback loops (firefighting loop), effects ledger for candidate changes, and an intervention plan with guardrails.

**Example 2 (Product ecosystem):** “We’re changing API pricing; what are the second-order effects across partners and customer segments?”  
Expected: system boundary + actors map (customers/partners/internal), loops and delays, effects ledger, and a sequencing/mitigation plan.

**Boundary example:** “Write a status update about this week’s tasks.”  
Response: this skill is for complex systems/decisions. Suggest a project update format instead; only use this skill if there’s a systemic pattern to diagnose.

