---
name: "evaluating-trade-offs"
description: "Evaluate trade-offs and produce a Trade-off Evaluation Pack (trade-off brief, options+criteria matrix, all-in cost/opportunity cost table, impact ranges, recommendation, stop/continue triggers). Use for tradeoff/trade-off, pros and cons, cost-benefit, opportunity cost, build vs buy, ship fast vs ship better, continue vs stop (sunk costs). Category: Leadership."
---

# Evaluating Trade-offs

## Scope

**Covers**
- Turning an ambiguous “pros/cons” debate into a decision-ready **trade-off evaluation**
- Comparing options using **all-in cost** (not just dollars) and explicit **opportunity cost**
- Using **order-of-magnitude estimates** (ranges + confidence) instead of false precision
- Stress-testing decisions with **thought experiments** (pre-mortems, reversibility, “worse first” dips)
- Avoiding sunk-cost traps with a clean **stop/continue** decision rule

**When to use**
- “Help me evaluate this trade-off and recommend a path.”
- “Create a pros/cons that actually leads to a decision.”
- “Compare options with cost/impact ranges and key assumptions.”
- “We’re debating speed vs quality—what’s the right trade and how do we manage the dip?”
- “Should we keep investing in this project, or stop? (Sunk cost question.)”

**When NOT to use**
- You need to clarify what problem you’re solving (use `problem-definition`).
- You need a full cross-functional decision process (use `running-decision-processes`).
- You’re prioritizing across many initiatives (use `prioritizing-roadmap`).
- You’re cutting scope to hit a date/timebox (use `scoping-cutting`).
- The decision is personal/legal/HR/financial advice (escalate to qualified humans).

## Inputs

**Minimum required**
- The trade-off / decision statement (one sentence) and a decision date (or “by EOW”)
- 2–4 options you’re choosing between (include “do nothing” if plausible)
- Constraints + non-negotiables (budget, headcount, policy, deadlines, customer commitments)
- What “good” means (success metrics + guardrails) and the time horizon you care about
- What you already know (evidence) + biggest unknowns (assumptions that drive the choice)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md) (3–5 at a time).
- If inputs are unavailable, proceed with explicit assumptions and label unknowns that would change the recommendation.

## Outputs (deliverables)

Produce a **Trade-off Evaluation Pack** in Markdown (in-chat; or as files if requested) in this order:
1) **Trade-off brief** (decision, why now, options, constraints, horizon, stakeholders)
2) **Options + criteria matrix** (criteria + weights/guardrails; option notes)
3) **All-in cost + opportunity cost table** (money, people/time, eng effort, complexity, displacement)
4) **Impact ranges (order-of-magnitude)** (upside/downside ranges, confidence, key assumptions)
5) **Worse-first + mitigation plan** (expected dip, leading indicators, mitigations, comms)
6) **Recommendation + stop/continue triggers** (decision, rationale, review date, kill/continue criteria)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (7 steps)

### 1) Frame the trade-off (make it decidable)
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Write the decision in one sentence (“We are choosing X vs Y by DATE to achieve GOAL”). List constraints/non-negotiables. Confirm the decision owner and who must live with the outcome.
- **Outputs:** Trade-off brief (decision, why now, constraints, stakeholders).
- **Checks:** You can answer: “What exactly are we deciding, by when, and for what outcome?”

### 2) Define what you’re optimizing (criteria + horizon)
- **Inputs:** Goals, metrics, guardrails; time horizon.
- **Actions:** Pick 4–8 criteria (include at least one *guardrail* like trust/reliability/cost). Decide weights only if it changes the decision. Explicitly name what you’re *not* optimizing for.
- **Outputs:** Options + criteria matrix (criteria definitions + weights/guardrails).
- **Checks:** Criteria reflect real trade-offs (not “everything is important”); horizon is explicit (e.g., 90 days vs 2 years).

### 3) Build the all-in cost + opportunity cost view
- **Inputs:** Team capacity, budget, dependencies, timelines.
- **Actions:** Estimate **all-in cost** (cash, headcount time, eng effort, maintenance, coordination). List the **opportunity cost**: what won’t be done if you choose each option.
- **Outputs:** All-in cost + opportunity cost table.
- **Checks:** Costs include “hidden” items (maintenance/on-call, tooling, cross-team coordination, switching costs).

### 4) Estimate impact with ranges (avoid false precision)
- **Inputs:** Any baseline numbers; evidence; assumptions.
- **Actions:** For each option, estimate upside/downside as **ranges** and note confidence. Prefer **order-of-magnitude** comparisons (10× vs 1.1×). Identify the 2–3 assumptions that drive the model.
- **Outputs:** Impact ranges table (range, confidence, key assumptions).
- **Checks:** No fake decimals; uncertainty is explicit; the decision is driven by a few key drivers you can name.

### 5) Run “thought experiments” (think more, build less)
- **Inputs:** Options, assumptions, risks.
- **Actions:** Do a pre-mortem for the top 1–2 options (“It failed—why?”). Identify the cheapest evidence to de-risk the biggest assumption (data pull, customer calls, small prototype, timeboxed spike). Decide if this should be a **thought experiment only** (no build) vs a real experiment.
- **Outputs:** Assumption list + minimal validation plan (if needed).
- **Checks:** Proposed tests are the smallest that could change your mind; you’re not shipping an “obvious loser” experiment.

### 6) Account for “worse first” + sunk costs
- **Inputs:** Expected short-term impacts; current investment/sunk costs.
- **Actions:** Name any “worse-first” dip (short-term pain) and plan mitigations/leading indicators. Apply a sunk-cost reset: “If we weren’t already doing this, would we start today?” Define stop/continue triggers and a review date.
- **Outputs:** Worse-first plan + stop/continue triggers.
- **Checks:** The plan anticipates the dip; continuation logic ignores sunk costs and focuses on future ROI and strategic fit.

### 7) Recommend, commit, and quality-gate
- **Inputs:** All artifacts above.
- **Actions:** Write the recommendation with rationale and explicit trade-offs (what you will stop doing). Add risks, open questions, and next steps with owners/dates. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md).
- **Outputs:** Final Trade-off Evaluation Pack.
- **Checks:** A stakeholder can read this async and make (or support) the decision without re-litigating the debate.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (resource allocation):** “Should we invest in SEO or paid acquisition for the next 2 quarters? Build a trade-off pack with all-in cost, ROI speed, and assumptions.”  
Expected: all-in cost vs alternatives, order-of-magnitude impact ranges, and a clear recommendation + review date.

**Example 2 (speed vs quality):** “We can ship v1 next week with rough edges or delay 3 weeks to ship ‘noteworthy’. Evaluate the trade-off and propose a worse-first mitigation plan if we ship now.”  
Expected: explicit criteria/guardrails (trust/support load), dip plan, and stop/continue triggers if metrics degrade.

**Boundary example:** “Help me decide if I should leave my job.”  
Response: this skill is for organizational/product leadership trade-offs; suggest a personal decision framework or coach instead.
