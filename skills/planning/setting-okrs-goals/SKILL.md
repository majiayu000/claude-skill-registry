---
name: "setting-okrs-goals"
description: "Set aligned, measurable OKRs/goals and produce an OKR & Goals Pack (objectives, key results, anti-gaming guardrails, systems/habits, review cadence, grading plan)."
---

# Setting OKRs & Goals

## Scope

**Covers**
- Turning strategy (or a North Star) into a small set of team/company OKRs
- Writing objectives that drive weekly execution (not just aspirational statements)
- Designing robust key results (prefer absolute counts; guard against gaming)
- Adding “default-on” systems/habits that make progress inevitable
- Defining review cadence + end-of-cycle grading to create a learning loop

**When to use**
- “Set our Q2 OKRs.”
- “Write objectives and key results for this team.”
- “We need quarterly goals that actually change behavior week-to-week.”
- “Our metrics are getting gamed / teams are optimizing the wrong thing.”
- “We need an OKR review + grading process.”

**When NOT to use**
- You don’t have an agreed strategy/North Star at all (use `writing-north-star-metrics` or `defining-product-vision` first)
- You need sprint planning or a delivery plan (tickets, estimates, timelines)
- You’re using OKRs primarily for individual performance evaluation
- You only need a single experiment metric for one test
- You need an analytics/event tracking implementation plan from scratch

## Inputs

**Minimum required**
- Planning cycle + horizon (e.g., Q2; annual; 6 weeks) and the team(s) in scope
- Strategy anchor: company goal, North Star, or “why now” narrative for the cycle
- Current baseline for key metrics (or best-available proxy) + where the numbers come from
- Constraints: capacity, must-do commitments, dependencies, risk tolerance
- Stakeholders: decider(s), contributors, approvers, review cadence participants

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If still missing, proceed with clearly labeled assumptions and provide 2–3 OKR set options (conservative/base/ambitious).

## Outputs (deliverables)

Produce an **OKR & Goals Pack** in Markdown (in-chat; or as files if the user requests), in this order:

1) **Context snapshot** (strategy anchor, horizon, scope, constraints, stakeholders)
2) **Alignment map** (company goal → team objective(s), no more than one step away)
3) **Draft OKRs** (1–3 Objectives; 2–5 Key Results each) with metric definitions, baselines, targets, owners, cadence
4) **Metric robustness + guardrails** (anti-gaming checks; ratio/denominator rules; quality guardrails)
5) **Systems & habits plan** (“default-on” behaviors/processes that make progress recurring)
6) **Review + grading plan** (weekly check-in; mid-cycle checkpoint; end-of-cycle scoring + learning retro)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + decision framing
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm horizon, scope, strategy anchor, baseline availability, constraints, and decision-maker(s).
- **Outputs:** Context snapshot.
- **Checks:** Everyone agrees what OKRs are for (alignment + learning), and what they are not (performance evaluation).

### 2) Establish alignment (“one step away”)
- **Inputs:** Strategy anchor; current company goal/North Star.
- **Actions:** Write a one-sentence company goal for the cycle; map each proposed team objective to it (no deep cascading).
- **Outputs:** Alignment map.
- **Checks:** For every team objective, you can answer: “How does this move the company goal within this horizon?”

### 3) Draft 1–3 Objectives (outcome-first)
- **Inputs:** Alignment map; key problems/opportunities.
- **Actions:** Draft objectives as outcomes + intent (not projects). Keep the set small.
- **Outputs:** Objective list with short rationale (“why now / why this”).
- **Checks:** An objective can be understood without reading its KRs; it changes what the team prioritizes weekly.

### 4) Generate candidate KRs (robust, measurable)
- **Inputs:** Objectives; baselines (or proxies).
- **Actions:** Draft 2–5 KRs per objective; define baseline, target, time window, metric owner, and data source. Prefer **absolute** metrics; if you use a ratio, also include its absolute numerator/denominator KRs or guardrails.
- **Outputs:** KR table(s) with metric definitions.
- **Checks:** Two analysts would compute the same number; targets are directionally ambitious but not fantasy.

### 5) Add systems/habits (default-on execution)
- **Inputs:** OKRs draft; team operating model.
- **Actions:** Specify the recurring mechanisms that will produce progress (cadences, routines, gates, customer touchpoints), not just one-off initiatives.
- **Outputs:** Systems & habits plan.
- **Checks:** At least one “default-on” system exists per objective, with an owner and cadence.

### 6) Anti-gaming + guardrails
- **Inputs:** KRs + systems plan.
- **Actions:** Identify how each KR could be gamed or cause harm. Add guardrails (quality, trust, margin, volume) and ratio/denominator checks.
- **Outputs:** Guardrails section + anti-gaming notes per KR.
- **Checks:** You can name 1–2 failure modes per KR and how you’ll detect them early.

### 7) Review cadence + grading plan (learning loop)
- **Inputs:** Full draft OKRs + guardrails.
- **Actions:** Define weekly review format, mid-cycle checkpoint rules, and end-of-cycle grading (scoring + retrospective questions).
- **Outputs:** Review + grading plan.
- **Checks:** The plan produces learning, not blame; it specifies who reviews, when, and what decisions can change mid-cycle.

### 8) Quality gate + finalize the pack
- **Inputs:** Entire OKR & Goals Pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final OKR & Goals Pack.
- **Checks:** Pack is shareable as-is; alignment, metrics, guardrails, and cadence are unambiguous.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (B2B SaaS):** “Set Q2 OKRs for Activation to improve time-to-first-value for new teams.”  
Expected: 1–2 objectives focused on new-team success, KRs with baselines/targets, a weekly review cadence, and guardrails (e.g., support tickets/new team).

**Example 2 (Growth):** “Set quarterly OKRs for Growth; we keep arguing about conversion rate vs volume.”  
Expected: KRs expressed as absolute numbers (e.g., activated users) plus denominator/quality guardrails to prevent ‘ratio gaming’.

**Boundary example:** “Write OKRs, but we don’t have a company goal or baseline metrics.”  
Response: ask for the minimum strategy anchor + baselines; if unavailable, produce 2–3 draft OKR options with explicit assumptions and recommend doing North Star/vision first.

