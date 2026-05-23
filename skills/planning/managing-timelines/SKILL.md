---
name: "managing-timelines"
description: "Turn a deadline, launch date, or delivery target into an executable Timeline Management Pack (deadline type + commitments, phase plan, milestone tracker, RAG cadence, scope/change control, stakeholder comms). Use for timeline/deadline/schedule/milestones."
---

# Managing Timelines

## Scope

**Covers**
- Turning a deadline or target date into a clear **commitment model** (commit vs forecast vs target)
- Building a phase-based plan (Discovery → Solutioning → Build → Launch) with **decision gates**
- Creating a milestone tracker with simple **RAG** (red/amber/green) status and escalation triggers
- Protecting the team when a deadline is real (treat it like **P0**, reduce distractions, control scope)
- Setting a governance + comms cadence so stakeholders get **early risk signals**, not surprises
- Handling “fast demo, slow production” cadence (especially for AI/ML features) via explicit outer-loop work

**When to use**
- “We need to ship by <date>. Create a timeline/milestone plan and status cadence.”
- “We have a launch date; convert this into phases, milestones, and a comms plan.”
- “Stakeholders keep asking for dates; define what we can actually commit to and when.”
- “The project feels off-track; set up RAG status + weekly exec review and escalation.”
- “We can demo quickly, but production will take longer—help set expectations and plan the outer loop.”

**When NOT to use**
- You haven’t defined the problem/outcome yet (use `problem-definition`)
- You need to pick which initiatives matter most (use `prioritizing-roadmap`)
- You primarily need to cut scope to fit an appetite/timebox (use `scoping-cutting`)
- You need a decision-ready PRD or build-ready spec/design doc (use `writing-prds` / `writing-specs-designs`)

## Inputs

**Minimum required**
- The deliverable and success bar (“done means…”) + key users/stakeholders
- The date type: **fixed deadline** (external) vs **target** (internal) vs **window** (e.g., “late March”)
- Constraints and non-negotiables (quality, compliance, privacy/security, platform, budget)
- Team shape + capacity assumptions (who’s building; availability; parallel work)
- Known dependencies and risks (other teams, vendors, data availability, approvals)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and list **Open questions** that could change the date or scope.

## Outputs (deliverables)

Produce a **Timeline Management Pack** in Markdown (in-chat; or as files if the user requests):

1) **Deadline & commitment model** (what’s fixed, what’s variable; commit vs forecast vs target language)
2) **Phase plan** (Discovery/Solutioning/Build/Launch) with outputs + decision gates + next commitment date
3) **Milestone tracker** (owners, dependencies, dates, confidence, RAG) + RAG definitions
4) **Governance cadence** (weekly review agenda, escalation triggers, decision log)
5) **Scope & change-control plan** (cut list, non-goals, “trade don’t add” rule, freeze points)
6) **Stakeholder comms pack** (weekly update template + escalation note)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)  
Expanded guidance: [references/WORKFLOW.md](references/WORKFLOW.md)

## Workflow (8 steps)

### 1) Intake + deadline classification
- **Inputs:** User request; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Identify the deadline type (fixed vs target vs window), the “why now”, and what variable can move (scope, resources, quality, or date).
- **Outputs:** Deadline classification + constraints snapshot.
- **Checks:** You can state: “The date is <fixed/target/window> because <reason>. The variable we will trade is <scope/resources/etc>.”

### 2) Define the commitment model (“commit vs forecast vs target”)
- **Inputs:** Deadline classification; current knowledge of scope/unknowns.
- **Actions:** Define what you will **commit** to now (usually a phase output), what you will **forecast**, and what remains a **target**. Set confidence levels and language rules for stakeholders.
- **Outputs:** Commitment model section + communication rules.
- **Checks:** Stakeholders can tell which dates are promises vs estimates.

### 3) Build a phase plan with decision gates
- **Inputs:** Deliverable; known unknowns; constraints.
- **Actions:** Break the work into Discovery → Solutioning → Build → Launch. Define the output of each phase and the decision gate (what must be true to move forward). Only commit to dates that are within control (near-term).
- **Outputs:** Phase plan with dates, outputs, and gates; “next commitment date” (when you’ll re-forecast).
- **Checks:** Every phase ends with a tangible artifact and a go/no-go decision.

### 4) Create the milestone tracker (+ “demo vs production” outer loop when relevant)
- **Inputs:** Phase plan; dependencies; team capacity.
- **Actions:** Translate phases into milestones with owners, dependencies, dates, confidence, and RAG. If AI/ML is involved, separate “first demo” from “production-ready” and explicitly add evaluation, data, safety, and reliability work.
- **Outputs:** Milestone tracker table + RAG definitions.
- **Checks:** Milestones are outcome-based (deliverables), not just activities; critical dependencies are explicit.

### 5) Set governance: RAG + weekly reviews + escalation
- **Inputs:** Milestone tracker; stakeholder map.
- **Actions:** Define update cadence (weekly by default), who reviews, and escalation triggers (what turns yellow/red). Use a simple RAG system and a short weekly review agenda to unblock work.
- **Outputs:** Governance cadence + weekly review agenda + escalation triggers.
- **Checks:** A “red” status produces a concrete ask/decision, not just a warning.

### 6) Protect the deadline: scope control + distraction shield
- **Inputs:** Deadline type; milestone risks; incoming requests.
- **Actions:** If the deadline is real, treat it like P0: define what gets deprioritized, reduce WIP, and implement change control (“trade, don’t add”). Create a cut list and freeze points (e.g., scope freeze, QA freeze).
- **Outputs:** Scope/change-control plan + cut list + freeze points.
- **Checks:** New scope cannot enter without an explicit trade-off and decision owner approval.

### 7) Stakeholder comms + expectation management
- **Inputs:** Commitment model; tracker; risks.
- **Actions:** Write a weekly update template and an escalation note. Pre-wire stakeholders about uncertainty (especially the demo→production gap). Ensure comms use correct language (commit/forecast/target) and highlight asks/decisions.
- **Outputs:** Comms pack (templates + initial draft update).
- **Checks:** Updates include “what changed since last week” and “what decision is needed by when”.

### 8) Quality gate + finalize
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure **Risks / Open questions / Next steps** exist with owners and dates.
- **Outputs:** Final Timeline Management Pack.
- **Checks:** A stakeholder can approve the plan async and the team can execute without re-litigating dates every week.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (fixed external date):** “We’re launching at an industry event on May 15. Create a milestone plan, RAG cadence, and a comms template for Sales/Marketing/Execs.”  
Expected: a fixed-deadline plan that treats the date as P0, with change control and clear escalation triggers.

**Example 2 (AI uneven cadence):** “We can demo an AI support agent in 2 weeks, but production will be risky. Build a plan that separates first demo vs production-ready and sets expectations.”  
Expected: milestones that include evaluation, safety/reliability, and rollout steps; explicit commit vs forecast language.

**Boundary example:** “Decide what we should build this quarter and set dates for everything.”  
Response: use `prioritizing-roadmap` first; then apply this skill to the chosen initiative(s).

