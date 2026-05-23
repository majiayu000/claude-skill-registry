---
name: "planning-under-uncertainty"
description: "Plan and lead execution when outcomes are uncertain and requirements are ambiguous. Produces an Uncertainty Planning Pack (uncertainty map, hypotheses + experiments, buffers + triggers, cadence + comms). Use for ambiguity, unknowns, hypothesis-driven planning, experimentation, contingency planning."
---

# Planning Under Uncertainty

## Scope

**Covers**
- Turning ambiguity into an executable plan via **hypotheses, experiments, and decision triggers**
- Diagnosing “what’s actually happening” before acting (especially in **crisis / wartime** situations)
- Using data as a **compass (directional checks)** rather than a GPS (false precision)
- Building **buffers and contingencies** so the plan survives chaos
- Setting a **cadence** for learning, decision-making, and stakeholder communication

**When to use**
- “We need a plan, but the requirements are unclear and the outcome is uncertain.”
- “Create a hypothesis-driven plan (experiments + decision rules) for this initiative.”
- “We’re in a crisis (drop in retention/revenue/reliability) and need a wartime diagnosis + action plan.”
- “Help us build contingencies, buffers, and pivot triggers before we commit.”

**When NOT to use**
- You don’t agree on the underlying problem/opportunity (use `problem-definition`).
- You need to choose what to do among many options (use `prioritizing-roadmap`).
- You already have a clear plan and only need dates/milestones and stakeholder cadence (use `managing-timelines`).
- You need a decision-ready PRD/spec for build execution (use `writing-prds` / `writing-specs-designs`).

## Inputs

**Minimum required**
- The initiative context and desired outcome (“what are we trying to change?”)
- Time horizon and urgency (wartime vs peacetime)
- Constraints/guardrails (quality, compliance, brand, budget, “must not worsen” metrics)
- Stakeholders and decision rights (who decides pivot/stop/scale?)
- Top unknowns/assumptions (what would change the plan?)
- Current signals (what data exists; what feels true but unproven?)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and list **Open questions** that could change the plan.

## Outputs (deliverables)

Produce an **Uncertainty Planning Pack** in Markdown (in-chat; or as files if the user requests), containing:

1) **Decision frame** (objective, “why now”, success + guardrails, time horizon, decision owner)
2) **Uncertainty map** (assumptions/unknowns, confidence, impact, validation plan)
3) **Hypotheses + experiment portfolio** (what we’ll learn, how, and what decision it enables)
4) **Plan v0 with buffers + contingencies** (phases/options, triggers, fallbacks, pivot criteria)
5) **Cadence + comms** (learning review ritual, update template, decision log)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + mode setting (wartime vs peacetime)
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify urgency, stakes, and what decision is needed. Decide whether you’re in **diagnosis-first wartime mode** or **exploration peacetime mode**.
- **Outputs:** Short decision frame draft + mode declaration.
- **Checks:** You can state: “We’re optimizing for <fast stabilization / learning / growth>. The decision we need by <date> is <pivot/stop/scale/commit>.”

### 2) Diagnose reality (humility first)
- **Inputs:** Current signals, anecdotes, dashboards, incident reports, qualitative inputs.
- **Actions:** Separate symptoms from hypotheses. Write 3–7 plausible explanations, and identify what evidence would falsify each. Avoid prematurely picking a favorite story.
- **Outputs:** “What we know / don’t know” + initial hypothesis set.
- **Checks:** At least one hypothesis contradicts the team’s initial intuition (to reduce confirmation bias).

### 3) Build the uncertainty map (assumptions → validation plan)
- **Inputs:** Hypotheses; constraints; stakeholders; time horizon.
- **Actions:** Create an uncertainty map of assumptions/unknowns with confidence and impact; prioritize the top items that would change the plan.
- **Outputs:** Uncertainty map table + prioritized “top 5 unknowns”.
- **Checks:** Every top unknown has a clear validation method and an owner.

### 4) Define hypotheses + decision rules (learning over “wins”)
- **Inputs:** Top unknowns; success/guardrails; risk tolerance.
- **Actions:** Turn unknowns into testable hypotheses. For each hypothesis, define: expected learning, success signal(s), guardrails, and the decision the result enables (stop/pivot/scale).
- **Outputs:** Hypothesis statements + decision rules.
- **Checks:** Each hypothesis ties to a decision; “winning” is defined as learning, not just positive results.

### 5) Design a reproducible testing process (many shots at bat)
- **Inputs:** Hypothesis set; available tools; team capacity.
- **Actions:** Create an experiment portfolio that balances speed vs confidence (smoke tests, prototypes, A/Bs, customer calls, operational drills). Set a cadence to run and review tests continuously.
- **Outputs:** Experiment portfolio table + review cadence.
- **Checks:** At least 1 fast test can run within the next 1–2 weeks (or faster in wartime).

### 6) Turn learning into a plan with buffers, contingencies, and triggers
- **Inputs:** Experiment portfolio; constraints; dependencies; timeline needs.
- **Actions:** Draft Plan v0 with phases/options; add buffers; define contingencies and explicit triggers for pivot/rollback/escalation. Use data as a compass: focus on directional signals and early warnings, not false certainty.
- **Outputs:** Plan v0 + buffer/contingency section + trigger list.
- **Checks:** There is a clear “if X happens, we will do Y” for the top risks/unknowns.

### 7) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure **Risks / Open questions / Next steps** exist with owners and time bounds.
- **Outputs:** Final Uncertainty Planning Pack.
- **Checks:** A stakeholder can approve the plan async and the team can execute without re-litigating the ambiguity.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (ambiguous initiative):** “We think onboarding is hurting conversion, but we’re not sure why. Create an uncertainty plan with hypotheses, experiments, and pivot triggers.”  
Expected: an uncertainty map + experiment portfolio (qual + quant) + a Plan v0 that commits to learning milestones, not premature delivery dates.

**Example 2 (wartime):** “Retention dropped 15% this week after a release. We need a wartime plan: diagnose root causes, run rapid tests, and decide whether to rollback or patch.”  
Expected: diagnosis-first workflow with falsifiable hypotheses, tight guardrails, and explicit rollback/escalation triggers.

**Boundary example:** “Write a full PRD for Feature X.”  
Response: clarify uncertainty first (this skill), then use `writing-prds` once the hypotheses, constraints, and decision gates are clear.

