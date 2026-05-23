---
name: "user-onboarding"
description: "Design and improve product user onboarding (first-time user experience) to drive activation and early retention. Produces an Onboarding & Activation Pack (aha moment spec, first 30 seconds + first mile plan, onboarding journey map, experiment backlog, measurement plan). Use for Growth teams."
---

# User Onboarding

## Scope

**Covers**
- Designing the first-time user experience (FTUE) from entry/signup → first value
- Defining activation / the “aha moment” and reducing time-to-value
- Creating a “first 30 seconds” experience and a “first mile” plan (milestones to activation)
- Onboarding mechanics: progressive disclosure, guided setup, empty states, templates, checklists, feedback loops
- Instrumentation + experiments to improve activation and early retention

**When to use**
- “Activation is low” / “users drop during signup/onboarding”
- “Time-to-value is too long”
- “The first session doesn’t feel magical”
- “We need an onboarding redesign / guided setup / empty state improvements”
- “Define our aha moment and design onboarding to get users there”
- “Create an onboarding experiment backlog + measurement plan”

**When NOT to use**
- You’re onboarding employees, customers to a service process, or running training (not product onboarding).
- You don’t have a stable value proposition / ICP (use `problem-definition` or `measuring-product-market-fit` first).
- You need a full retention strategy beyond onboarding (use `retention-engagement`).
- You need to validate a prototype with real users (use `usability-testing` after creating a plan here).

## Inputs

**Minimum required**
- Product + ICP/segment(s) (1–2) and the primary job-to-be-done
- Platform + entry point (web/mobile; where FTUE starts)
- Best-available baseline metrics (even rough):
  - visit → signup → first key action → activation
  - time-to-value (time or sessions to first value)
  - D1 retention (if available)
- Current onboarding flow summary (steps/screens) and the biggest drop-off point(s)
- Constraints: timebox, eng/design capacity, allowed channels (in-app/email/push), privacy/legal/brand limits

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If metrics are missing, proceed with explicit assumptions and label confidence.
- Do not request secrets or PII; prefer aggregated funnels and redacted screenshots.

## Outputs (deliverables)

Produce an **Onboarding & Activation Pack** (Markdown in-chat; or as files if requested) containing:

1) Context snapshot (goal, segment, constraints, baseline)
2) Current FTUE map (step-by-step) + friction log
3) Activation / aha moment spec (behavioral definition + threshold + validation plan)
4) “First 30 seconds” experience spec (magic moment + success criteria)
5) “First mile” onboarding plan (milestones to activation; mechanics per milestone)
6) Experiment backlog (prioritized) + 3–5 experiment cards
7) Measurement + instrumentation plan (events, properties, dashboards, guardrails)
8) Rollout/rollback + risk plan
9) Risks / Open questions / Next steps (always included)

Templates and checklists:
- [references/TEMPLATES.md](references/TEMPLATES.md)
- [references/WORKFLOW.md](references/WORKFLOW.md)
- [references/CHECKLISTS.md](references/CHECKLISTS.md)
- [references/RUBRIC.md](references/RUBRIC.md)

## Workflow (7 steps)

### 1) Intake + goal framing (activation-first)
- **Inputs:** User prompt; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Define the primary segment and the activation outcome. Make the goal measurable (baseline → target, date). Capture constraints and guardrails (e.g., don’t increase drop-off, don’t add dark patterns).
- **Outputs:** Context snapshot + goal statement.
- **Checks:** Goal is one sentence with a metric, baseline, target, and date.

### 2) Map the current first-time journey (FTUE)
- **Inputs:** Current flow description/screens; funnel + drop-offs; support/sales notes if available.
- **Actions:** Create a step-by-step journey map from entry → first value. Log frictions (confusion, time, permissions, empty states, choice overload). Identify the single biggest leak.
- **Outputs:** FTUE map table + friction log + primary leak.
- **Checks:** Every step has a user goal, product action, and a measurable checkpoint (event or proxy).

### 3) Define the activation / “aha moment” (behavioral)
- **Inputs:** Candidate value behaviors; available events; retention definition (if any).
- **Actions:** Propose 3–5 candidate “aha” behaviors and pick one activation definition with a threshold (e.g., “creates X and shares Y within 7 days”). Specify how to validate (correlation with D7/D30; holdout if possible).
- **Outputs:** Activation/aha moment spec + validation plan + instrumentation needs.
- **Checks:** Activation is observable, repeatable, and measurable (not “understands value”).

### 4) Design the “first 30 seconds” (make it feel magical)
- **Inputs:** Primary leak + activation spec; constraints.
- **Actions:** Specify what the user should see/do/feel in the first 30 seconds:
  - Remove or defer non-essential setup (progressive disclosure).
  - Deliver a fast, native, interactive win (avoid passive carousel “tours”).
  - Provide immediate feedback and a clear next action.
- **Outputs:** First 30 seconds spec (screen/script + success criteria).
- **Checks:** A new user can reach a meaningful “win” within ~30 seconds (or you document why not and the best proxy).

### 5) Build the “first mile” plan (milestones → activation)
- **Inputs:** Activation spec; journey map; UX constraints.
- **Actions:** Break activation into 3–6 milestones (the “first mile”). For each milestone, define mechanics (guided setup, defaults, empty states, templates, checklists, feedback, progress). Ensure onboarding is “inside the product,” not detached from real actions.
- **Outputs:** First mile onboarding plan + updated journey map.
- **Checks:** Each milestone reduces time-to-value and has a leading-indicator metric.

### 6) Instrumentation + measurement plan
- **Inputs:** Current analytics/events; proposed milestones; guardrails.
- **Actions:** Define the minimum event schema and dashboards needed (funnel, time-to-value, activation rate, early retention). Add guardrails (support tickets, cancellations, performance).
- **Outputs:** Measurement plan + event list/properties + dashboard outline.
- **Checks:** Every experiment and milestone has a primary metric and at least one guardrail metric.

### 7) Prioritize experiments + quality gate
- **Inputs:** Candidate interventions; measurement plan; [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- **Actions:** Convert top opportunities into experiment cards; prioritize (Impact × Confidence ÷ Effort). Add rollout/rollback guidance. Run checklist + score rubric. Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final Onboarding & Activation Pack.
- **Checks:** Top 3 experiments are runnable within constraints and have “win/lose/learn” criteria.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS, guided setup):**  
“Use `user-onboarding`. Product: workflow automation tool for SMB ops. Segment: new self-serve admins. Baseline: 42% signup completion, 9% activation within 7 days. Problem: users stall at connecting integrations. Constraint: 3-week sprint, 1 engineer, 1 designer. Output: an Onboarding & Activation Pack with an activation spec, a first-30-seconds + first-mile plan, and a prioritized experiment backlog.”

**Example 2 (B2C app, time-to-value):**  
“Our first session feels flat. Redesign onboarding so users experience value within 30 seconds, define the activation event, and propose 5 experiments with metrics + guardrails.”

**Boundary example (not product onboarding):**  
“Create an employee onboarding program for new hires.”  
Response: this skill is for product onboarding; use an HR onboarding/training process instead.

