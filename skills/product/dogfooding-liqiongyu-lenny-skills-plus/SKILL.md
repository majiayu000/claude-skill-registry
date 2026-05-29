---
name: "dogfooding"
description: "Run an internal dogfooding program/sprint and produce a Dogfooding Pack (charter, scenario map, routines, dogfooding log + triage board spec, weekly report, ship/no-ship gate). Use for “dogfooding”, “eat our own dog food”, internal beta, and product teams using the product daily to find friction before shipping."
---

# Dogfooding

## Scope

**Covers**
- Designing and running a **dogfooding loop** where the product team uses the product like a real user would
- Creating “**creator commitments**” when the product is for creators (e.g., publish a podcast, ship a workflow, run weekly reports)
- Capturing issues as **reproducible artifacts** (not vibes): logs, severity, decisions, owners, and follow-through

**When to use**
- “Set up a dogfooding program / dogfooding sprint for our product team.”
- “We’re shipping soon—make sure we’re using the product daily and fixing the biggest pain.”
- “We built this for creators; our team needs to *be creators* to understand the workflow.”
- “Create an internal beta plan and a weekly dogfooding report template.”

**When NOT to use**
- You need to validate **market demand** or solve **who is the customer / what is the problem** (do discovery first)
- The product team cannot realistically represent the workflow (e.g., regulated roles, hardware constraints) without proxies
- You’re looking for user research replacement (dogfooding complements—not replaces—external user feedback)
- The only goal is “QA everything” (use a QA/test plan; dogfooding is for **experience + value + workflow realism**)

## Inputs

**Minimum required**
- Product summary + target user persona (who it’s for; what job it does)
- 1–3 core workflows to dogfood (end-to-end)
- Time box + cadence (e.g., 1 week sprint; 20 min/day; weekly triage)
- Participants (roles) + any “creator commitments” required
- Environment constraints (prod vs staging; data/privacy constraints; access constraints)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns. Offer 2 scope options (lean vs thorough).

## Outputs (deliverables)

Produce a **Dogfooding Pack** in Markdown (in-chat; or as files if requested):

1) **Context snapshot** (product, persona, workflows, constraints, time box)
2) **Dogfooding charter** (goals, participants, rules, cadence, definitions)
3) **Scenario map + routines** (daily/weekly tasks + “creator commitments”)
4) **Dogfooding log + triage board spec** (fields, severity scale, decision rules)
5) **Weekly dogfooding report** (insights, decisions, shipped fixes, next experiments)
6) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Frame the dogfooding goal (experience, not just bugs)
- **Inputs:** Product summary; desired outcomes; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Define what “success” means for this cycle (e.g., “team can complete workflow A in <10 min without workarounds”). Set constraints (environment, data, access).
- **Outputs:** Context snapshot + explicit success criteria.
- **Checks:** Success criteria are measurable and tied to a real workflow outcome (not “feel better”).

### 2) Define representative scenarios + “creator commitments”
- **Inputs:** Target persona + workflows.
- **Actions:** Create 3–8 scenarios that represent real user goals. If the product is for creators, define a publish cadence (e.g., “each PM publishes 1 artifact/week”).
- **Outputs:** Scenario map + routine plan.
- **Checks:** At least 1 scenario is “from scratch → shipped/published” end-to-end.

### 3) Set up the capture system (log, severity, triage)
- **Inputs:** Existing tools (Jira/Linear/Notion/Sheets) or “none”.
- **Actions:** Define the dogfooding log schema, severity scale, and triage rules. Decide labels/tags to link issues to scenarios and workflow steps.
- **Outputs:** Dogfooding log + triage board spec.
- **Checks:** Any issue can be reproduced with a clear “steps to reproduce + expected vs actual + evidence”.

### 4) Run daily dogfooding sessions (time-boxed)
- **Inputs:** Scenario map + routines.
- **Actions:** Each participant runs 1–2 scenarios/day, captures friction immediately, and attaches evidence (screens, logs, timestamps). Record “workarounds used”.
- **Outputs:** Daily log entries + a rolling “top pains” list.
- **Checks:** Entries are concrete (repro steps) and prioritized by impact on completing the workflow.

### 5) Triage weekly: decide, assign, and protect focus
- **Inputs:** Log + top pains.
- **Actions:** Run triage: cluster duplicates, classify (bug/UX debt/gap/docs), assign owners, and decide “fix now / schedule / won’t fix (with reason)”. Update scenario map if it was unrealistic.
- **Outputs:** Prioritized backlog + decision notes.
- **Checks:** Top 3–5 issues map directly to blocked/slow scenarios and have an owner + next action.

### 6) Ship loop: verify fixes by dogfooding again (no-ship gate)
- **Inputs:** “Fix now” items + release plan.
- **Actions:** For each fix, re-run the scenario end-to-end. Apply a simple gate: “We can complete the scenario with no hidden workarounds in the chosen environment.”
- **Outputs:** Verified fixes list + any regressions.
- **Checks:** The gate is based on completing scenarios, not just closing tickets.

### 7) Report + quality gate + next cycle plan
- **Inputs:** Final log + triage outcomes.
- **Actions:** Produce the weekly report. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps and propose the next dogfooding cycle focus.
- **Outputs:** Final Dogfooding Pack.
- **Checks:** Report contains decisions (what changed) and shows evidence-backed learning (not just a bug list).

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Creator product):** “We’re building a podcast creation tool. Create a dogfooding program where the whole team publishes 1 short episode/week, and produce a weekly report template.”  
Expected: scenarios from “idea → published episode”, creator commitments, log schema, triage cadence, and ship gate tied to publishing.

**Example 2 (B2B workflow product):** “Set up a 2-week dogfooding sprint for our AI meeting notes tool focused on ‘record → summary → share → action items’.”  
Expected: scenario map, daily routine, severity scale, triage rules, weekly report, and a verified-fixes list.

**Boundary example:** “Dogfood this idea we haven’t built yet.”  
Response: dogfooding requires a usable artifact; propose discovery + prototype/usability testing first, then a dogfooding sprint once there’s something to run end-to-end.

