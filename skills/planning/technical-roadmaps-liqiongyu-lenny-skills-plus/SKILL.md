---
name: "technical-roadmaps"
description: "Turn an engineering strategy into a written Technical Roadmap Pack (Rumelt-style strategy: Diagnosis/Guiding Policy/Coherent Actions, roadmap table, initiative briefs, and alignment cadence). Use for technical roadmap, tech roadmap, engineering roadmap, architecture roadmap."
---

# Technical Roadmaps

## Scope

**Covers**
- Turning “technical work” (architecture, platform, reliability, tech debt) into a **written strategy + roadmap** that stakeholders can critique and improve.
- Applying Richard Rumelt’s strategy frame (**Diagnosis → Guiding policy → Coherent actions**) to engineering planning.
- Producing a roadmap that is **executable** (owners, milestones, dependencies, risks, metrics), not a vague wishlist.
- Aligning a technical roadmap with product/business constraints (quarters, launches, compliance/security, capacity).

**When to use**
- “Create a technical/engineering/architecture roadmap for the next 2–4 quarters.”
- “We need a written technical strategy and a roadmap we can review with leadership.”
- “We have many tech-debt/platform initiatives; turn them into a prioritized plan with dependencies and milestones.”
- “Our tech roadmap keeps being misunderstood—write it down so we can debug alignment.”

**When NOT to use**
- The problem/outcome is unclear (use `problem-definition` first).
- You need to choose *which* product bets matter most (use `prioritizing-roadmap` or `ai-product-strategy`).
- You only need delivery dates, milestone tracking, and RAG governance (use `managing-timelines`).
- You need a deep platform strategy / ecosystem design (use `platform-strategy`).

## Inputs

**Minimum required**
- **Audience + decision:** who this roadmap is for (Eng leadership, Execs, Product) and what decisions it must enable.
- **Time horizon + format:** e.g., 6 months / 12 months; Now-Next-Later vs quarterly.
- **Current-state diagnosis inputs:** top pain points, reliability/latency/cost signals, incident themes, scaling constraints, key architectural bottlenecks.
- **Constraints:** capacity assumptions, compliance/security requirements, platform constraints, non-negotiables.
- **Candidate initiatives:** known platform/architecture/tech-debt items (even a rough list).

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and list them under **Open questions**.

## Outputs (deliverables)

Produce a **Technical Roadmap Pack** in Markdown (in-chat; or as files if the user requests):

1) **Technical Strategy (Rumelt)**: Diagnosis → Guiding policy → Coherent actions (template: [references/TEMPLATES.md](references/TEMPLATES.md))
2) **Roadmap table** (Now/Next/Later or quarters) with owners, dependencies, milestones, confidence, and metrics
3) **Initiative briefs** for the top 3–6 roadmap items (1 page each)
4) **Dependency + risk register** (top cross-team deps, key risks, mitigations)
5) **Alignment + governance plan** (review cadence, update rules, decision owners, comms template)
6) **Risks / Open questions / Next steps** (always included)

Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + audience alignment
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm the audience, horizon, and roadmap “shape” (quarters vs Now/Next/Later). Identify the decision the roadmap must enable (funding, sequencing, headcount, trade-offs).
- **Outputs:** Intake summary + explicit assumptions + open questions list (if any).
- **Checks:** You can state: “This roadmap is for <audience> to decide <decision> over <horizon> using <format>.”

### 2) Write the strategy (Rumelt: Diagnosis → Guiding policy → Coherent actions)
- **Inputs:** Current-state signals; constraints; product/business context.
- **Actions:** Draft a written strategy using the Rumelt structure. Keep it concrete: name the constraints and trade-offs.
- **Outputs:** Technical Strategy section using [references/TEMPLATES.md](references/TEMPLATES.md).
- **Checks:** A reader can answer: “What’s the problem?”, “What’s our approach?”, “What actions are we taking (and not taking)?”

### 3) Build the initiative inventory (candidate “coherent actions”)
- **Inputs:** Candidate initiative list; strategy; incidents/metrics; architecture notes.
- **Actions:** Normalize initiatives into a table (theme, outcome, why now, dependencies, effort, risk). Merge duplicates; split overly broad items.
- **Outputs:** Initiative inventory (draft roadmap backlog).
- **Checks:** Each item has an outcome + a “why now” tied back to the Diagnosis/Guiding policy.

### 4) Prioritize + sequence (make trade-offs explicit)
- **Inputs:** Inventory; constraints; dependencies; capacity assumptions.
- **Actions:** Prioritize based on: (a) alignment to strategy, (b) risk reduction, (c) enabling product work, (d) cost/effort, (e) dependency criticality. Sequence via dependencies and “first unlocks.”
- **Outputs:** Ranked list + sequencing rationale + explicit non-goals/cut list.
- **Checks:** You can justify the top 3 items in 1–2 sentences each, including what you deprioritized.

### 5) Convert into a roadmap (quarters or Now/Next/Later) with execution detail
- **Inputs:** Ranked list; sequencing; calendar constraints.
- **Actions:** Create the roadmap table with owners, milestones, dependencies, confidence, and success metrics. Add “decision gates” where uncertainty is high.
- **Outputs:** Roadmap table + milestone highlights.
- **Checks:** A team could start execution without guessing owners/dependencies; high-uncertainty items have a gate (spike/RFC/prototype).

### 6) Draft initiative briefs + alignment plan
- **Inputs:** Roadmap; top items; stakeholder map.
- **Actions:** Write 1-page briefs for the top 3–6 items and a comms/governance plan (review cadence, update rules, decision owners).
- **Outputs:** Initiative briefs + alignment/governance section (templates in [references/TEMPLATES.md](references/TEMPLATES.md)).
- **Checks:** Stakeholders know when/how the roadmap will change and what inputs trigger a refresh.

### 7) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure **Risks / Open questions / Next steps** are present with owners and dates where possible.
- **Outputs:** Final Technical Roadmap Pack.
- **Checks:** The pack is “debuggable”: written, coherent, measurable, and reviewable.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (platform scaling):** “We’re seeing reliability issues and slow delivery. Create a 2-quarter technical roadmap and strategy we can review with leadership.”  
Expected: a Rumelt-structured strategy plus a sequenced roadmap with owners, dependencies, milestones, and metrics.

**Example 2 (architecture modernization):** “We need an architecture roadmap to migrate off a legacy monolith while still shipping product features.”  
Expected: explicit trade-offs, dependency-aware sequencing, decision gates, and a governance cadence to keep alignment.

**Boundary example:** “Write a detailed project plan with dates for every task for the next 6 months.”  
Response: use `managing-timelines` for delivery planning; this skill is for strategy → roadmap (themes/initiatives/milestones), not task-level scheduling.
