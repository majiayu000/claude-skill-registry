---
name: "behavioral-product-design"
description: "Apply behavioral science to product design and produce a Behavioral Product Design Pack (target behavior, behavioral diagnosis, intervention map, prioritized concepts, design specs, experiment + instrumentation plan, ethics/trust review). Use for retention, onboarding, habit loops, and behavior change problems."
---

# Behavioral Product Design

## Scope

**Covers**
- Turning a desired user behavior into an **executable design + experiment plan**
- Diagnosing behavior using **barriers/drivers** (motivation, ability/friction, uncertainty, habit, context)
- Designing **behavioral interventions** (e.g., defaults, commitment devices, loss aversion/progress, reducing uncertainty) with ethical guardrails
- Producing decision-ready artifacts a PM/Design/Eng team can build and test

**When to use**
- “Help me apply behavioral science / behavioral economics to this flow.”
- “We need to improve retention / activation / onboarding completion.”
- “Design a streak / habit loop / reminder system (without being spammy).”
- “Users procrastinate (present bias). How do we get them to do the thing?”
- “People stick with the status quo. How do we drive switching/adoption?”
- “Users are uncertain / anxious. How do we reduce uncertainty and move them forward?”

**When NOT to use**
- You need upstream strategy first (vision, positioning, roadmap). Use `defining-product-vision` / `prioritizing-roadmap`.
- You can’t name the target user + target behavior + success metric (this becomes generic advice).
- The goal is to create **dark patterns** (deception, coercion, addiction, hidden costs). Don’t do this.
- The domain is regulated/high-stakes (medical, financial advice, minors). Require domain/legal review and tighter safeguards.

## Inputs

**Minimum required**
- Product context + target user segment
- The **target behavior** (what user action you want more of, in what context)
- Baseline funnel/retention metrics (even rough) + where the drop happens
- Constraints: platform (web/mobile), notification channels, brand/tone, time box
- Existing evidence: user research notes, support tickets, analytics, session replays (if any)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns. Offer 2 scopes: **narrow (1 behavior)** vs **broad (journey)**.

## Outputs (deliverables)

Produce a **Behavioral Product Design Pack** (in-chat as Markdown; or as files if requested), in this order:

1) **Context snapshot** (goal, segment, constraints, baseline)
2) **Target behavior spec** (behavior statement + success metric + guardrails)
3) **Behavioral diagnosis** (barriers/drivers; where bias/friction/uncertainty shows up)
4) **Intervention map** (ideas mapped to journey moments + mechanism + risk)
5) **Prioritized intervention shortlist** (top 1–3 with rationale)
6) **Behavioral design specs** (1–3 build-ready “intervention cards”)
7) **Experiment + instrumentation plan** (events, primary/guardrail metrics, rollout/rollback)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + define the target behavior
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the user, context, and *one* primary target behavior. Define success + guardrails (what must not get worse).
- **Outputs:** Context snapshot + target behavior spec.
- **Checks:** Target behavior is observable and time-bounded (not “be more engaged”).

### 2) Map the current journey + “moments that matter”
- **Inputs:** Current flow/JTBD; baseline funnel.
- **Actions:** Sketch the steps from trigger → action → outcome. Mark drop-offs and emotional moments (uncertainty, effort, waiting, completion).
- **Outputs:** Journey map summary + top 3 friction points.
- **Checks:** Each friction point is tied to a specific step/state (not a vague complaint).

### 3) Run a behavioral diagnosis (barriers + drivers)
- **Inputs:** Journey moments; evidence; assumptions.
- **Actions:** For each friction point, identify: (a) motivation/benefit perception, (b) ability/friction, (c) prompts/forgetting, (d) uncertainty/risk perception, (e) social/context constraints. Map likely mechanisms (e.g., present bias, status quo, uncertainty aversion, loss aversion/progress).
- **Outputs:** Behavioral diagnosis table (barrier → mechanism → design implication).
- **Checks:** Each proposed mechanism has at least one supporting signal (research/quote/data) or is labeled “hypothesis”.

### 4) Generate intervention ideas (mechanism-first, not UI-first)
- **Inputs:** Diagnosis table.
- **Actions:** Brainstorm 2–4 interventions per priority barrier using the pattern library in [references/WORKFLOW.md](references/WORKFLOW.md) (defaults, reducing uncertainty, progress/loss framing, commitment devices, reminders, celebration/pause moments).
- **Outputs:** Intervention inventory (10–20 ideas) with mechanism tags.
- **Checks:** At least one idea reduces friction (ability) and one reduces uncertainty (trust), not only “add reminders”.

### 5) Add resilience + reinforcement (without manipulation)
- **Inputs:** Intervention inventory.
- **Actions:** For habit/retention loops, explicitly design: (a) **reinforcement** (“pause moments” for meaningful progress), (b) **resilience** (“bend not break” policies like grace periods), (c) ethical framing (user benefit, transparency, easy opt-out).
- **Outputs:** Updated interventions with reinforcement/resilience + ethics notes.
- **Checks:** No intervention relies on deception, forced continuity, or hidden penalties.

### 6) Prioritize and pick the top 1–3 bets
- **Inputs:** Updated inventory; constraints.
- **Actions:** Score ideas on impact, confidence, effort, and risk (trust/legal/brand). Pick 1–3 that cover different failure modes (friction vs uncertainty vs motivation).
- **Outputs:** Prioritized shortlist + “why these” rationale.
- **Checks:** Each selected bet has a clear hypothesis and measurable metric movement.

### 7) Write build-ready behavioral design specs + experiment plan
- **Inputs:** Shortlist; [references/TEMPLATES.md](references/TEMPLATES.md).
- **Actions:** For each bet, write an intervention spec: hypothesis, mechanism, UX/copy, states, edge cases, instrumentation, rollout/rollback, and guardrails.
- **Outputs:** 1–3 behavioral design specs + experiment/instrumentation plan.
- **Checks:** Engineering can implement without major missing decisions; measurement is feasible.

### 8) Quality gate + finalize
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md), score with [references/RUBRIC.md](references/RUBRIC.md), and add **Risks / Open questions / Next steps**.
- **Outputs:** Final Behavioral Product Design Pack.
- **Checks:** The pack is specific to this product and can be executed in 1–2 sprints.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Activation):** “New users abandon setup on step 3. Use behavioral science to redesign onboarding and propose 2 experiments.”  
Expected: diagnosis of the abandonment moment, intervention map, 2 intervention specs, and an experiment + instrumentation plan.

**Example 2 (Retention/habit):** “We want a 7-day habit loop for daily check-ins without annoying notifications.”  
Expected: habit/reinforcement plan (incl. bend-not-break), celebration moments, a streak spec, and guardrail metrics.

**Boundary example:** “Make the UI more addictive so people can’t stop using it.”  
Response: refuse dark patterns; reframe toward user-beneficial behaviors, transparency, and opt-out controls.

