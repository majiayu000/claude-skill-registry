---
name: "retention-engagement"
description: "Improve retention, churn, engagement, and activation by producing a Retention & Engagement Improvement Pack (diagnosis, aha moment definition, lever hypotheses, experiment backlog, measurement plan, 30/60/90 plan). Use for Growth teams."
---

# Retention & Engagement

## Scope

**Covers**
- Diagnosing retention + engagement (cohorts/curves, frequency, segments, drop-offs)
- Identifying the **activation / “aha moment”** and reducing time-to-value
- Designing habit + re-engagement interventions (daily return, reminders, content loops)
- Creating **accruing value** and ethical **switching costs** (“mounting loss”)
- Turning insights into a prioritized experiment + measurement plan

**When to use**
- “Improve retention / reduce churn”
- “Increase engagement / DAU/WAU”
- “Define our activation / aha moment”
- “D1/D7 retention is low—fix onboarding and time-to-value”
- “Create a retention experiment backlog and a 30/60/90 plan”

**When NOT to use**
- You don’t have (or can’t assume) a stable value proposition / ICP (use `problem-definition`).
- You’re primarily deciding pricing/packaging/paywalls (this skill can add retention context but won’t replace pricing work).
- You need acquisition loop design (use `designing-growth-loops`).
- You need to synthesize qualitative churn feedback before proposing experiments (use `analyzing-user-feedback` or interviews).

## Inputs

**Minimum required**
- Product + target user/ICP and 1–2 key segments
- Current stage (pre-PMF / early PMF / growth / mature)
- Best-available baseline metrics (even rough):
  - retention (D1/D7/D30 or weekly cohort), churn, engagement (DAU/WAU/MAU), activation rate, time-to-value
- Onboarding flow summary (steps/screens + where users drop)
- Constraints: timebox, engineering/design capacity, allowed channels (email/push/in-app), privacy/legal/brand limits

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If metrics are missing, proceed with explicit assumptions and label confidence.
- Do not request secrets or PII; prefer aggregated metrics and redacted funnels.

## Outputs (deliverables)

Produce a **Retention & Engagement Improvement Pack** (Markdown in-chat; or as files if requested) containing:

1) Context snapshot (goal, segments, constraints, timebox)
2) Metric definitions + guardrails (how “retention” and “engagement” are measured)
3) Retention + engagement diagnosis (cohorts/curves, segments, drop-offs, churn drivers)
4) Activation / aha moment definition (candidate behaviors + threshold + validation plan)
5) Lever hypotheses map (onboarding → habit → accruing value → re-engagement)
6) Experiment backlog (prioritized; experiment cards with success metrics + guardrails)
7) Measurement + instrumentation plan (events, dashboards, owners if known)
8) 30/60/90 execution plan
9) Risks / Open questions / Next steps (always included)

Templates and checklists:
- [references/TEMPLATES.md](references/TEMPLATES.md)
- [references/WORKFLOW.md](references/WORKFLOW.md)
- [references/CHECKLISTS.md](references/CHECKLISTS.md)
- [references/RUBRIC.md](references/RUBRIC.md)

## Workflow (7 steps)

### 1) Intake + goal framing
- **Inputs:** User prompt; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Define the retention problem (segment, time horizon, metric) and the decision this work will drive (what will change). Confirm constraints (timebox, capacity, channels, privacy/brand).
- **Outputs:** Context snapshot + metric definitions draft.
- **Checks:** Goal is a sentence with a number and a date (e.g., “Improve paid D30 retention from 18%→24% by end of Q2”).

### 2) Data + instrumentation sanity check
- **Inputs:** Current tracking/events (or best guess), funnel steps, dashboards (if any).
- **Actions:** List what you can/can’t measure today. Define the minimum event schema needed to learn (activation, engagement, churn). Identify 1–3 highest-impact instrumentation gaps.
- **Outputs:** Instrumentation gap list + “minimum viable measurement” plan.
- **Checks:** Every key metric in the goal has a data source or an explicit assumption.

### 3) Diagnose: where retention fails (and why)
- **Inputs:** Baseline metrics, cohorts/curves, funnel drop-offs, segments, any churn feedback.
- **Actions:** Build a diagnosis across three failure modes:
  - **Activation failure** (users never reach value)
  - **Engagement decay** (users get value once, don’t build a habit)
  - **Monetization churn** (value exists, but price/packaging/friction drives churn)
  Segment results (at least 2 segments) and identify the largest “leak.”
- **Outputs:** Retention + engagement diagnosis table + primary failure mode(s).
- **Checks:** Diagnosis points to one primary lever to test first (onboarding vs habit vs value vs comms).

### 4) Define the activation / “aha moment” (data-backed)
- **Inputs:** Candidate value behaviors + journey; usage events; retention outcome definition.
- **Actions:** Propose 3–5 candidate “aha” behaviors, then define an activation threshold (e.g., “uses X feature twice within 7 days” or “invites 2 teammates + uses 2 key features within 14 days”). Document how you’ll validate (correlation with D30/D60 retention; holdout if possible).
- **Outputs:** Activation/aha moment spec + validation plan + tracking requirements.
- **Checks:** The activation definition is behavioral and measurable (not a survey response or opinion).

### 5) Generate lever hypotheses (convert insights → rules)
- **Inputs:** Diagnosis + activation spec; constraints.
- **Actions:** Create a lever map with hypotheses tied to failure modes:
  - **Onboarding/time-to-value:** get users to aha faster and more reliably
  - **Habit/daily return:** design cues, routines, rewards; reduce friction to “come back tomorrow”
  - **Accruing value + mounting loss (ethical):** personalization, progress/history, saved work, identity/data repository
  - **Re-engagement:** lifecycle messaging, winback, content reminders, in-product nudges
  Convert each hypothesis into a rule + check (see [references/SOURCE_SUMMARY.md](references/SOURCE_SUMMARY.md)).
- **Outputs:** Lever hypotheses map + candidate interventions.
- **Checks:** Every hypothesis ties to (a) a failure mode, and (b) a measurable leading indicator.

### 6) Design + prioritize experiments (with measurement)
- **Inputs:** Hypotheses; measurement plan; capacity.
- **Actions:** Turn top hypotheses into experiment cards (1–2 weeks each). Prioritize using a simple score (Impact × Confidence ÷ Effort). Define success metrics and guardrails; note required instrumentation and rollout/rollback.
- **Outputs:** Prioritized experiment backlog + experiment cards + metric/guardrail spec.
- **Checks:** Top 3 experiments are runnable with current constraints and have unambiguous “win/lose/learn” criteria.

### 7) Build the 30/60/90 plan + quality gate
- **Inputs:** Draft pack; [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- **Actions:** Sequence work into a 30/60/90 plan (instrumentation, experiments, analysis cadence). Run the checklist and score the rubric. Always include **Risks / Open questions / Next steps**.
- **Outputs:** Final Retention & Engagement Improvement Pack.
- **Checks:** Next 2 weeks of work are unblocked; measurement is in place to learn.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2C subscription, churn reduction):**  
“Use `retention-engagement`. Product: meditation app. Segment: paid subscribers. Baseline: D30 paid retention 22%, churn spikes after week 2. Constraint: 4-week sprint, no major redesign. Output: a Retention & Engagement Improvement Pack with an activation/aha definition, a diagnosis, and a prioritized experiment backlog + 30/60/90 plan.”

**Example 2 (B2B SaaS, activation + habit):**  
“New users activate but don’t return weekly. Define our aha moment, identify the biggest engagement decay point, and propose 5 experiments (in-product + email) with success metrics and guardrails.”

**Boundary example (upstream problem):**  
“Write a brand new value prop and pick an ICP for our product.”  
Response: that’s upstream strategy/problem definition; use `problem-definition` (and optionally PMF measurement) before retention optimization.

