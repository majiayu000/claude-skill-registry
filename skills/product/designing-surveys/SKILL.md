---
name: "designing-surveys"
description: "Design and launch a product survey and produce a Survey Pack (brief, questionnaire/instrument, analysis plan, launch checklist, reporting outline). Use for customer surveys, onboarding surveys, NPS/CSAT/PMF, cancellation/churn, and feedback surveys."
---

# Designing Surveys

## Scope

**Covers**
- Designing product surveys that answer a specific decision (not “general feedback”)
- Choosing the right audience, sampling, and timing (including “best customers” cohorts)
- Writing clear, unbiased questions and using good scales (CSAT vs NPS guidance)
- Building an instrument that works on mobile (logic, required fields, option visibility)
- Planning analysis and turning results into decisions and follow-ups

**When to use**
- “Design a customer survey for…”
- “Create an onboarding survey to profile users / separate buyer vs user.”
- “We need a CSAT/NPS/PMF survey.”
- “Draft a cancellation / churn survey.”
- “Help me write survey questions and an analysis plan.”

**When NOT to use**
- You need deep “why” stories and context (use `conducting-user-interviews`)
- You need to measure causal impact of a change (use an experiment/A/B test, not a survey)
- Your reachable sample is extremely small (n < ~30) and you need directional insight → interviews may be better
- The topic is high-risk (legal/medical/safety) or requires formal survey science review; involve an expert

## Inputs

**Minimum required**
- Product + target user(s)/segment(s)
- The decision to make (what will change based on the survey) + deadline
- Survey type (e.g., onboarding profiling, CSAT, NPS, PMF, churn, feature discovery)
- Distribution channel(s) (in-product, email, customer success, etc.) + sampling constraints
- Privacy/compliance constraints (what data you can/can’t collect)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still missing, proceed with explicit assumptions and list **Open questions** that would change the design.

## Outputs (deliverables)

Produce a **Survey Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot** (decision, audience, channel, constraints)
2) **Survey brief** (goal, target population, sampling, timing, success criteria)
3) **Questionnaire** (questions with rationale + response types; question IDs)
4) **Survey instrument table** (copy/paste-ready for building in a survey tool)
5) **Analysis + reporting plan** (segments, cuts, coding plan, decision thresholds)
6) **Launch plan + QA checklist** (pilot, mobile QA, bias checks, comms, follow-ups)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded heuristics: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Clarify the decision, timeline, primary audience, and distribution channel(s). Name the “unknowns” the survey must resolve.
- **Outputs:** Context snapshot + survey goal.
- **Checks:** You can state the decision in one sentence (“We are deciding whether to… by <date>”).

### 2) Define the audience + sampling plan (who, when, how many)
- **Inputs:** Context snapshot.
- **Actions:** Choose primary segment(s) and a sampling frame. Prefer behavior/recency-based cohorts (e.g., “signed up 3–6 months ago and active”) when you need accurate recall.
- **Outputs:** Sampling plan (in brief) + segment cuts.
- **Checks:** You can explain why each segment is included and what decision it informs.

### 3) Choose the measurement design (metrics, scales, prioritization)
- **Inputs:** Survey goal + audience.
- **Actions:** Pick the core metric(s) (often CSAT); add 1–2 diagnostic questions that force prioritization (e.g., “pick top 3 barriers”) and frequency/impact weighting.
- **Outputs:** Measurement plan (metric + diagnostics) + draft question list.
- **Checks:** Every question maps to a decision, hypothesis, or segment cut; no “nice-to-have” questions.

### 4) Draft the questionnaire (sections, wording, and logic)
- **Inputs:** Measurement plan; templates.
- **Actions:** Write questions using neutral wording, single concepts per question, and consistent scales. Add segmentation/profile questions only if you will use them in analysis.
- **Outputs:** Questionnaire with question IDs, response types, options, and skip logic notes.
- **Checks:** No double-barreled or leading questions; completion time target ≤ 3–6 minutes for most surveys.

### 5) Build the instrument table + QA it (mobile + bias)
- **Inputs:** Questionnaire draft.
- **Actions:** Convert to an instrument table for implementation (IDs, types, options, required, logic). Check mobile rendering (all scale points visible) and option order/randomization.
- **Outputs:** Survey instrument table + QA checklist items.
- **Checks:** Scale labels are unambiguous; required questions are minimal; “Other (free text)” exists when appropriate.

### 6) Plan the launch (pilot, comms, monitoring, follow-ups)
- **Inputs:** Instrument + sampling plan.
- **Actions:** Define pilot (small n), launch dates, reminders, incentives, and a monitoring plan. If the goal is message validation, consider a behavioral “survey” via ad/landing tests instead of asking opinions.
- **Outputs:** Launch plan + monitoring metrics (response rate, drop-off, segment mix).
- **Checks:** You have a plan for low response rate and for closing the loop with respondents.

### 7) Analysis + report plan + quality gate
- **Inputs:** Final instrument + goals.
- **Actions:** Define how you’ll analyze (segments, cuts, coding of open-ended), the decision thresholds, and how results will be communicated. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final Survey Pack.
- **Checks:** A stakeholder can review async and decide “ship / adjust / investigate” without another meeting.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Onboarding):** “Design an onboarding survey to identify the buyer vs user and route leads appropriately.”  
Expected: short profiling questions (3–4 screens), clear segmentation fields, and a follow-up plan to avoid irrelevant outreach.

**Example 2 (Product friction):** “Design a CSAT survey to find the top 3 productivity blockers for active users and how often they occur.”  
Expected: CSAT + forced-ranking diagnostics + frequency weighting, plus an analysis plan that yields a ranked backlog of issues.

**Boundary example:** “We want to know if feature X caused retention to improve—send a survey.”  
Response: push back; recommend experiment/instrumentation for causality, and use a survey only for qualitative context (or run interviews).

