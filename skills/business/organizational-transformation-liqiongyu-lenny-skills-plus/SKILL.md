---
name: "organizational-transformation"
description: "Lead an organizational transformation toward a modern product operating model (not “framework adoption”). Produces an Organizational Transformation Pack (diagnostic, target operating model, pilot plan, roadmap, comms, governance). Use for org transformation, product operating model change, moving from feature teams to empowered product teams, and change management. Category: Leadership."
---

# Organizational Transformation

## Scope

**Covers**
- Designing and leading a **practical transformation plan** to move a company toward a **modern product operating model**
- “Nudging” legacy orgs: sequencing change so it’s adopted, not rejected
- Avoiding the trap of treating **framework adoption** (Spotify, SAFe, etc.) as the end goal
- Coordinating **structure + process + culture** changes (teams, decision rights, discovery/delivery, incentives, rituals)

**When to use**
- “Help me move us from **feature teams** to **empowered product teams**.”
- “We keep adopting frameworks but nothing changes—build a **real transformation plan**.”
- “Create a **90-day pilot plan** plus a roadmap for rolling out a product operating model.”
- “Our leaders want transformation; teams are skeptical. Build a **change + comms plan** that reduces rejection.”

**When NOT to use**
- You need strategy/vision first (use `defining-product-vision` or `working-backwards`).
- You only need an org chart / team topology change (use `organizational-design`).
- You need project management for a known plan (use `managing-timelines`).
- You need HR/legal guidance on comp, layoffs, labor law, or sensitive people actions (involve HR/legal).

## Inputs

**Minimum required**
- Org context: industry, size/stage, geography, regulated constraints (if any)
- Executive sponsor + decision maker(s) and the transformation “why now”
- Current operating model symptoms (with examples): decision bottlenecks, output-vs-outcome mismatch, discovery gaps, dependency chains
- Current team model (feature teams vs product teams), and where product decisions currently live
- Constraints: timelines, budget/headcount, must-keep processes, critical launches

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns.

## Outputs (deliverables)

Produce an **Organizational Transformation Pack** (Markdown in-chat, or files if requested) in this order:
1) **Transformation Charter** (why now, goals/non-goals, principles, success metrics, constraints)
2) **Current-State Diagnostic** (how work flows today; capability gaps; resistance map; failure modes)
3) **Target Product Operating Model Blueprint** (team types, roles, decision rights, cadences, core artifacts)
4) **Pilot / Nudge Plan (90 days)** (2–4 safe-to-try pilots, training/coaching, learning loop, adoption strategy)
5) **Transformation Roadmap (6–12 months)** (phases, big rocks, dependencies, sequencing, resourcing)
6) **Change + Comms Plan** (stakeholders, messages, rituals, enablement, resistance handling)
7) **Governance + Metrics** (leading indicators, review cadence, escalation, “framework hygiene” guardrails)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Align on outcomes (not frameworks)
- **Inputs:** Why now; goals; symptoms; constraints; prior attempts.
- **Actions:** Convert “adopt X framework” into outcomes + behaviors. Define non-goals (what you will not change yet). Set 3–5 transformation principles.
- **Outputs:** Transformation Charter (draft) + assumptions.
- **Checks:** Sponsors can state success as outcomes/behaviors, not “we implemented X.”

### 2) Diagnose the current operating model as a system
- **Inputs:** Team types; planning cadence; decision rights; delivery flow; examples of delays/rework.
- **Actions:** Map how work moves from idea → shipped; identify bottlenecks (dependencies, approvals, incentives, missing discovery). Capture where a feature-team model is reinforced.
- **Outputs:** Current-State Diagnostic (system map + top issues).
- **Checks:** Diagnostic explains the symptoms with concrete mechanisms (not vibes).

### 3) Pick a transformation thesis + guardrails (framework hygiene)
- **Inputs:** Diagnostic; constraints; change capacity; leadership alignment.
- **Actions:** Define the smallest set of operating model changes that would create leverage (e.g., empowered teams, dual-track discovery/delivery, outcome-oriented planning). Add “framework hygiene” rules: what you’ll borrow, what you won’t, and why.
- **Outputs:** Transformation thesis + guardrails section in the Charter.
- **Checks:** The plan is tailored to context; it avoids copying a model wholesale.

### 4) Design the target product operating model (concrete, observable)
- **Inputs:** Transformation thesis; product shape (integrated vs modular); talent maturity.
- **Actions:** Specify: team types (product/platform/enabling), roles, decision rights, intake, discovery expectations, planning cadence, and required artifacts.
- **Outputs:** Target Product Operating Model Blueprint.
- **Checks:** A leader can answer “who decides what” and “what ‘good’ looks like” on Day 1.

### 5) Create a nudge-first pilot plan (90 days)
- **Inputs:** Blueprint; candidate teams/areas; risk constraints.
- **Actions:** Design 2–4 pilots with clear hypotheses, enablement (coaching/training), and adoption tactics (nudges, rituals, templates). Define what you’ll learn and how you’ll adapt.
- **Outputs:** Pilot / Nudge Plan + pilot scorecard.
- **Checks:** Pilots are safe-to-try, measurable, and don’t require perfect org-wide alignment.

### 6) Build the transformation roadmap (6–12 months)
- **Inputs:** Pilot plan; resourcing; calendar constraints.
- **Actions:** Sequence the big rocks (structure changes, capability building, tooling/process changes). Include decision points, dependencies, and rollback triggers.
- **Outputs:** Transformation Roadmap (phases + milestones).
- **Checks:** Roadmap is implementable; it protects business continuity and in-flight commitments.

### 7) Plan change + comms (reduce rejection)
- **Inputs:** Stakeholders; resistance map; incentives.
- **Actions:** Draft a comms narrative, stakeholder-specific messages, enablement plan, and a system for handling objections. Connect the change to incentives and leadership behaviors.
- **Outputs:** Change + Comms Plan.
- **Checks:** Plan includes reinforcement mechanisms (rituals, metrics, leadership actions), not just announcements.

### 8) Quality gate + finalize
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Ensure Risks/Open questions/Next steps are present.
- **Outputs:** Final Organizational Transformation Pack + rubric score.
- **Checks:** If rubric score is low, do one more intake round (max 5 questions) and revise.

## Quality gate (required)
- Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md) before finalizing.
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1:** “VP Product at a legacy enterprise: teams ship features but outcomes don’t improve. Create a transformation plan toward empowered product teams.”  
Expected: diagnostic, target operating model blueprint, 90-day pilots, 6–12 month roadmap, governance metrics.

**Example 2:** “CEO: we tried SAFe/Spotify-style changes and got backlash. Build a nudge-first plan and comms to reduce rejection.”  
Expected: framework hygiene guardrails, small pilots, stakeholder messaging, reinforcement mechanisms.

**Boundary example:** “Write a plan to ‘implement the Spotify model’ verbatim.”  
Response: this skill treats frameworks as tools; it will instead produce a context-fit operating model and specify what (if anything) to borrow and how to validate via pilots.
