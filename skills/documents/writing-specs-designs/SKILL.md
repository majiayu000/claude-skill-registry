---
name: "writing-specs-designs"
description: "Create a build-ready spec + design doc pack (low-fi diagram, user flows/states, prototype brief, acceptance criteria) for a feature or UX change. Use for spec, design doc, feature spec, technical spec, interaction spec."
---

# Writing Specs & Designs

## Scope

**Covers**
- Producing a **Spec & Design Doc Pack** that helps product, design, and engineering quickly reach shared clarity
- Converting “insights” into **concrete artifacts**: a low‑fidelity diagram, flows/states, prototype plan, and testable acceptance criteria
- Mobile-specific **tap economy** (when relevant): explicitly optimizing taps and interaction cost

**When to use**
- “Write a spec / feature spec / technical spec for this feature.”
- “Turn these notes into a design doc that engineering can build from.”
- “Create a shaping-style doc with a diagram of the moving pieces.”
- “We need a prototype plan to evaluate the feel of this interaction.”

**When NOT to use**
- You’re still validating *what problem to solve* (do discovery / problem definition first).
- You need a high-level strategy/vision document (do product vision / north star work first).
- You need a deep engineering architecture design (APIs, schemas, scaling, reliability) rather than product interaction clarity.
- You only need pixel-perfect UI mocks (this produces specs and structured guidance, not final visuals).

## Inputs

**Minimum required**
- Feature/change: 1–2 sentence description
- Target users + primary use case (happy path)
- Platform(s): web / iOS / Android / desktop (call out mobile explicitly)
- Goals + non-goals (v1 boundaries)
- Constraints: timeline, dependencies, policy/legal/privacy, technical constraints
- Success metrics (1–3) + guardrails (2–5)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md), then proceed.
- If key info remains missing, state assumptions explicitly and provide 2–3 options (scope/flows/prototype approach).

## Outputs (deliverables)

Produce a **Spec & Design Doc Pack** in Markdown (in-chat; or as files if the user requests):

1) **Context snapshot** (problem, why now, goals/non-goals, constraints, stakeholders)
2) **Low‑fidelity diagram** of the moving pieces (≤10) + key decisions
3) **User flows + states** (happy path + top edge cases) with clear entry/exit points
4) **Prototype brief** (what to prototype, fidelity, timebox, data realism, success criteria)
5) **Requirements + acceptance criteria** (testable; must/should/could)
6) **Measurement plan** (metrics → data/events → owner → cadence)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Choose the smallest artifact set that unblocks the team
- **Inputs:** User request + constraints.
- **Actions:** Decide whether to deliver: (a) Spec & Design Doc only, or (b) Spec & Design Doc + Prototype Brief emphasis (feel-critical).
- **Outputs:** Artifact selection + rationale.
- **Checks:** Artifacts match the decision being made (alignment vs build execution vs interaction feel).

### 2) Intake + context snapshot
- **Inputs:** [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Ask up to 5 questions; confirm audience/DRI, platform(s), constraints, and success metrics/guardrails.
- **Outputs:** Context snapshot section.
- **Checks:** You can state the problem, user, and success measure in 1–2 sentences.

### 3) Lock scope boundaries (and define “tap budget” if mobile)
- **Inputs:** Context snapshot.
- **Actions:** Write goals, non-goals, out-of-scope, assumptions, dependencies. For mobile flows, define a “tap budget” (max taps to value) and where attention is most fragile.
- **Outputs:** Scope boundaries + (optional) tap budget.
- **Checks:** “What we are NOT doing” is explicit; mobile value path has a clear tap target.

### 4) Draft the low‑fidelity diagram (the “shaping” output)
- **Inputs:** Scope + constraints.
- **Actions:** Produce a diagram that shows the moving pieces (≤10), data/hand-offs, and where UX decisions matter. Avoid pixel-level UI; prefer clarity of structure.
- **Outputs:** Low‑fidelity diagram + annotated decisions.
- **Checks:** A partner can say “I know what to build” without a meeting.

### 5) Specify user flows + states (make edge cases concrete)
- **Inputs:** Diagram + use case(s).
- **Actions:** Document entry points, happy path, and top edge cases; include error/empty/loading states, permissions, and copy notes where ambiguity causes bugs.
- **Outputs:** Flow + state table(s).
- **Checks:** Another person can role-play the flow; each edge case has an intended outcome.

### 6) Write the prototype brief (only where “feel” matters)
- **Inputs:** Flows/states + unknowns.
- **Actions:** Identify the 1–3 riskiest interaction uncertainties; specify prototype type (low-fi, hi-fi, or in-code), timebox, realism (use real data where possible), and what “good” feels like.
- **Outputs:** Prototype brief.
- **Checks:** Prototype plan is testable (scenarios + success criteria), and explicitly disposable if using throwaway code.

### 7) Convert into testable requirements + acceptance criteria
- **Inputs:** Flows/states + prototype learnings (if any).
- **Actions:** Write requirements with acceptance criteria (must/should/could). Include non-functional needs (accessibility, performance, privacy) and instrumentation needs.
- **Outputs:** Requirements section.
- **Checks:** Engineering/QA can derive test cases without re-interpreting intent.

### 8) Quality gate + finalize for circulation
- **Inputs:** Full draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps and clearly mark decisions vs assumptions.
- **Outputs:** Final Spec & Design Doc Pack (shareable as-is).
- **Checks:** Owners, metrics, and open questions are explicit; the diagram + flows remove the biggest ambiguities.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (mobile flow):** “Write a spec + design doc for a new ‘invite friends’ flow in our iOS app. Goal: increase successful invites; minimize taps to first value.”  
Expected: tap budget + flow/state tables, a low-fi diagram of screens/transitions, and a prototype brief for the critical interaction.

**Example 2 (B2B web feature):** “Create a design doc/spec for ‘bulk edit roles’ for admins. Include edge cases and acceptance criteria.”  
Expected: permissions-focused flows/states, requirements with acceptance criteria, and a measurement plan.

**Boundary example:** “Write a spec to ‘improve engagement’ (no product context, no user, no success metric).”  
Response: ask the minimum intake questions; if still missing, provide 2–3 scoped options + assumptions and recommend upstream discovery before committing to a spec.

