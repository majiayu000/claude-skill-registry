---
name: "organizational-design"
description: "Design or redesign an org structure and operating model by producing an Organizational Design Pack (design brief, current-state map, operating-model decision, target org blueprint, transition plan). Use for org design, reorgs, team topology, functional vs divisional structures, and centralized vs decentralized decision-making. Category: Leadership."
---

# Organizational Design

## Scope

**Covers**
- Designing or redesigning an organization’s **structure + operating model** to improve speed, accountability, and customer outcomes
- Choosing between **centralized vs decentralized** models (Apple ↔ Amazon spectrum) and **functional vs divisional/value-stream** orientations
- Reducing coordination tax by **minimizing dependencies** and clarifying **decision rights**
- Setting management roles/layers so leaders **know the work** and can drive craft, not just process

**When to use**
- “Propose a reorg / org design for my product + engineering organization.”
- “We’re slow due to dependencies—redesign teams so we can run in parallel.”
- “Our UX is fragmented—should we centralize decisions or strengthen functional leadership?”
- “We grew fast and added layers—help us simplify and get back to startup speed.”

**When NOT to use**
- You need product strategy/vision first (use `defining-product-vision` or `working-backwards`).
- This is mainly a people-performance issue (use coaching/feedback workflows, not a reorg).
- You need compensation bands, leveling, hiring plans, or legal/HR guidance (involve HR/legal).
- You need a single high-stakes decision process (use `running-decision-processes`).

## Inputs

**Minimum required**
- Org context: company stage, domain, size, and which functions are in-scope (e.g., Product/Eng/Design/Data)
- Current structure: teams, reporting lines (rough is fine), and how work is currently organized
- Primary goals: what must improve (e.g., speed, quality, integrated UX, ownership, cost)
- Key symptoms with examples (e.g., slow decisions, rework, unclear ownership, fragmented UX)
- Constraints/non-negotiables (headcount, timeline, critical launches, regulatory/compliance, leadership preferences)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If answers aren’t available, proceed with explicit assumptions and label unknowns.

## Outputs (deliverables)

Produce an **Organizational Design Pack** (Markdown in-chat, or files if requested) in this order:
1) **Org Design Brief** (goal, constraints, design principles, success metrics)
2) **Current-State Map** (teams/charters, dependency hotspots, decision rights, layers)
3) **Operating Model Decision** (centralized ↔ decentralized + functional ↔ divisional rationale)
4) **Target Org Blueprint** (team topology + charters + leadership roles + interfaces)
5) **Operating Mechanisms** (decision rights, planning cadence, cross-team interfaces)
6) **Transition Plan** (sequencing, comms, staffing moves, risk mitigations, measurement)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Define what you’re optimizing for (and the constraints)
- **Inputs:** Goals; symptoms; constraints; timeline.
- **Actions:** Translate “we need a reorg” into a design problem: what outcomes must improve and by when. Pick 3–5 design principles (e.g., “minimize dependencies”, “one UX owner for critical journeys”, “reduce layers”).
- **Outputs:** Org Design Brief (draft) + success metrics.
- **Checks:** Stakeholders can agree on the top tradeoffs (e.g., speed vs UX coherence) and what would count as success.

### 2) Map the current org-as-a-system (work, dependencies, decisions)
- **Inputs:** Current teams; roadmap/work streams; known friction examples.
- **Actions:** Document team charters, dependencies, and decision rights. Identify dependency hotspots, duplicated ownership, and surprise approvers. Capture management layers and where managers don’t know the work.
- **Outputs:** Current-State Map + “top 5 friction loops” list.
- **Checks:** The map explains most observed delays/rework with concrete dependency/decision bottlenecks.

### 3) Choose an operating model posture (centralize vs decentralize; functional vs divisional)
- **Inputs:** Product architecture/coupling; UX integration needs; talent maturity; risk tolerance.
- **Actions:** Place the org on two spectrums: (1) centralized (Apple-like) ↔ decentralized (Amazon-like), and (2) functional ↔ divisional/value-stream. Write the rationale and guardrails (what must be standardized vs allowed to diverge).
- **Outputs:** Operating Model Decision + guardrails.
- **Checks:** The choice matches product coupling: integrated experiences have explicit owners; independent surfaces can run in parallel with clear interfaces.

### 4) Generate 2–3 viable org options (not one)
- **Inputs:** Current-state map; operating model posture; constraints.
- **Actions:** Draft 2–3 options (A/B/(C hybrid)), each with team list, charters, leadership roles, interfaces, and expected dependency changes. Make management layers explicit; avoid “people managers” without domain/craft context.
- **Outputs:** Options table + option narratives.
- **Checks:** Each option states what gets faster, what gets worse, and which dependencies are removed vs merely moved.

### 5) Score options and pick a recommendation (with a fallback)
- **Inputs:** Options; stakeholder priorities; risk constraints.
- **Actions:** Score with [references/RUBRIC.md](references/RUBRIC.md). Pick a recommended option + a fallback. Identify “Day 1 changes” vs “follow-on refactors” and the required operating-mechanism changes (decision rights, cadence, standards).
- **Outputs:** Recommendation + scorecard + key decisions to align on.
- **Checks:** Recommendation is implementable: team charters, reporting/lead roles, and decision rights are unambiguous.

### 6) Design the transition (change plan, comms, and safety rails)
- **Inputs:** Recommendation; people constraints; launch calendar.
- **Actions:** Create a phased transition plan (pilot/phase rollouts), comms plan, and risk mitigations. Define success metrics + check-in points (Day 30/60/90). Add rollback triggers for high-risk changes.
- **Outputs:** Transition Plan + comms outline.
- **Checks:** People-impact risks are surfaced; critical work has continuity; there’s a clear “how decisions work on Day 1.”

### 7) Quality gate + finalize
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Finalize the pack and include Risks/Open questions/Next steps.
- **Outputs:** Final Organizational Design Pack + rubric score.
- **Checks:** If rubric score is low, do one more intake round (max 5 questions) and revise.

## Quality gate (required)
- Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md) before finalizing.
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1:** “I’m a VP Product at a ~200-person company. Teams are slow due to cross-team dependencies; propose an org redesign to increase parallelism.”  
Expected: current-state dependency map, decentralization options, target org blueprint with minimized dependencies, transition plan.

**Example 2:** “Founder/CEO: we added layers and lost speed. Help us move toward a more functional model and ensure managers know the work.”  
Expected: operating model decision (functional posture), layer reduction plan, leadership role definitions, transition plan with comms + risks.

**Boundary example:** “Create a reorg to justify cutting headcount.”  
Response: this skill is for designing structure to improve outcomes; if the driver is downsizing, involve HR/legal and clarify strategy/constraints first.
