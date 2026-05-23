---
name: "product-operations"
description: "Design and implement Product Operations systems that help product teams scale (cadences, standard artifacts, insights pipelines, release enablement). Produces a Product Ops Operating System Pack (charter, operating model, rituals, templates, implementation plan). Use for product ops, product org scaling, standardizing roadmaps/check-ins, release management enablement."
---

# Product Operations

## Scope

**Covers**
- Defining a **Product Ops charter** that clarifies accountability, boundaries, and “how we work”
- Building **systems that help PMs thrive**: cadences, standardized artifacts, and decision support (not decision-making)
- Creating **cross-functional interfaces** (Product ↔ Ops/Sales/CS/Eng/Data/Support) to reduce friction and surprises
- Standing up an **insights pipeline** (qual + quant) so product teams get the right signals at the right time
- Operationalizing **shipping + enablement**: release readiness, internal comms, training, and feedback loops

**When to use**
- “We need **Product Ops**—define what it is here and what it owns.”
- “Our product team is scaling; we need **standard roadmaps/check-ins** and better operating cadence.”
- “PMs are drowning in coordination; set up a **system** to reduce overhead.”
- “Create a **release enablement** process (readiness, comms, training, feedback).”
- “We need a repeatable **insights → decisions** pipeline across Product/CS/Sales.”

**When NOT to use**
- You need to choose *what to build* (use `prioritizing-roadmap` / `defining-product-vision`)
- You need to define metrics/OKRs from scratch (use `writing-north-star-metrics` / `setting-okrs-goals`)
- You need to write a decision-ready PRD (use `writing-prds`) or build-ready spec (use `writing-specs-designs`)
- You need deep customer discovery, interviews, or usability testing (use `conducting-user-interviews` / `usability-testing`)

## Inputs

**Minimum required**
- Product org context: stage, team shape, main frictions (“what’s breaking at scale?”)
- Current planning/shipping rhythm (if any): roadmap/OKR cadence, release process, comms touchpoints
- Primary stakeholders: Product/Eng/Data/Ops/Sales/CS/Support + decision owners
- Desired outcomes: what should be easier/faster/clearer after Product Ops exists
- Constraints: compliance/privacy, tooling limits, resourcing, timelines

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns.

## Outputs (deliverables)

Produce a **Product Ops Operating System Pack** in Markdown (in-chat; or as files if the user requests):

1) **Product Ops charter** (mission, scope, non-goals, success metrics)
2) **Operating model** (engagement model, RACI/ownership, embedded vs centralized approach)
3) **Cadences + rituals** (calendar of key reviews/check-ins with agendas + outputs)
4) **Standard artifact set** (templates for roadmap updates, decision logs, product updates, launch enablement)
5) **Insights pipeline** (sources, taxonomy, intake/triage, dashboards, feedback loops)
6) **Release enablement system** (readiness checklist, comms plan, training, post-launch capture)
7) **30/60/90 implementation plan** (pilot, rollout, measurement, iteration)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + problem framing (what’s breaking at scale?)
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify: org stage, top 3 friction points, stakeholders, existing cadences, and desired outcomes.
- **Outputs:** Context snapshot + top problems to solve (ranked).
- **Checks:** You can state a 1-sentence problem: “Product Ops exists to reduce <friction> and improve <outcome> for <teams>.”

### 2) Define the Product Ops charter (boundaries + success)
- **Inputs:** Context snapshot; constraints; stakeholders.
- **Actions:** Draft mission, scope, non-goals, and success metrics. Explicitly state: **Product Ops informs decisions; PMs keep decision rights**.
- **Outputs:** Product Ops charter (v1).
- **Checks:** Charter answers: what we own, what we don’t, how to engage, and how we measure value.

### 3) Map interfaces + ownership (make collaboration explicit)
- **Inputs:** Current workflow; stakeholder map.
- **Actions:** Map interfaces (Product ↔ Eng/Data/Ops/Sales/CS/Support). Define RACI and “who decides what” for planning, releases, comms, and insights.
- **Outputs:** Operating model (draft) + RACI table.
- **Checks:** No “shadow ownership”: every recurring decision/artifact has a clear owner and escalation path.

### 4) Design the operating cadence (rituals that produce artifacts)
- **Inputs:** Charter; RACI; current calendar.
- **Actions:** Define a minimal cadence set (weekly/biweekly/monthly/quarterly) with agendas, attendees, and required outputs.
- **Outputs:** Cadence calendar + meeting output spec(s).
- **Checks:** Each ritual produces a concrete artifact/update; anything that’s “just a meeting” gets removed or redesigned.

### 5) Standardize artifacts (make product work legible)
- **Inputs:** Existing docs; stakeholder needs; cadence outputs.
- **Actions:** Define the standard artifact set (roadmap update, decision log, weekly product update, launch brief, enablement bundle). Provide templates + ownership.
- **Outputs:** Artifact library + templates list.
- **Checks:** Artifacts are lightweight, repeatable, and tailored to the audiences that consume them.

### 6) Build the insights pipeline (right signal → right forum)
- **Inputs:** Data sources; feedback channels; research process.
- **Actions:** Create intake/triage, taxonomy, and routing to the right forum (product area owners, planning cycle, release retro). Specify dashboards/recurring reporting.
- **Outputs:** Insights pipeline spec + backlog triage mechanism.
- **Checks:** New signal has an owner, a place to land, and a defined “decision path” (no orphan feedback).

### 7) Operationalize shipping + enablement (release readiness system)
- **Inputs:** Current release process; artifact set.
- **Actions:** Define readiness checklist, comms/enablement workflow, and post-launch capture (escapes, support load, learning). Keep it proportionate to release tier.
- **Outputs:** Release enablement system + checklists + comms template(s).
- **Checks:** For any release, you can answer: who needs to know, what changes, how we monitor, and how we roll back/mitigate.

### 8) Implement + iterate (pilot → rollout → measure)
- **Inputs:** Full draft pack; resourcing; timeline.
- **Actions:** Create 30/60/90 plan, choose a pilot area, run the cadence for 2–4 cycles, gather feedback, and adjust.
- **Outputs:** 30/60/90 plan + measurement plan + iteration backlog.
- **Checks:** At least 1 measurable improvement is targeted (cycle time, stakeholder satisfaction, fewer surprises, less PM overhead).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (scaling):** “We grew from 6 to 18 PMs and things feel chaotic. Set up a Product Ops operating cadence, standardized roadmap updates, and an insights pipeline.”  
Expected: charter + cadences + templates + 30/60/90 rollout plan.

**Example 2 (shipping + enablement):** “Our launches surprise Support and Sales. Create a release enablement system with readiness checks and a comms workflow.”  
Expected: release tiering + readiness checklist + enablement bundle template + post-launch capture loop.

**Boundary example:** “Decide which initiatives we should prioritize next quarter.”  
Response: use `prioritizing-roadmap` first; then apply this skill to operationalize the chosen plan.

