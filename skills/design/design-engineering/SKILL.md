---
name: "design-engineering"
description: "Stand up a Design Engineering practice (hybrid design+engineering) by producing a Design Engineering Execution Pack: charter, prototype→production workflow, design-to-code contract, component delivery plan, and quality bar. Use for design engineering, UI engineering, design systems engineering, and prototype-to-production processes."
---

# Design Engineering

## Scope

**Covers**
- Defining a **Design Engineering** function (hybrid design sensibility + ability to ship production code)
- Choosing an operating model: **embedded** vs **platform/design-system** vs **tiger team**
- Creating a **prototype → production** pipeline (what is throwaway vs shippable)
- Establishing a **design-to-code contract** (tokens, components, reviews, quality bar)
- Planning delivery for UI/UX-heavy work (components/flows, milestones, QA gates)

**When to use**
- “We want to create a design engineering function—write the charter and operating model.”
- “Our prototypes never make it to production—define a prototype→production workflow.”
- “We need faster UI iteration with high craft—set a design-to-code contract + quality bar.”
- “We’re building a new UI/component library—create a component delivery plan and reviews.”

**When NOT to use**
- You need UX research, discovery, or product strategy (use interviews/surveys/PRD skills)
- You’re doing mostly backend/platform architecture with minimal UI surface area
- You only need to ship a single small UI fix (just implement it)
- You need a brand/visual identity system (separate design/brand process)

## Inputs

**Minimum required**
- Product/context: what you’re building and who it’s for
- Current state: design artifacts (Figma, mockups) + codebase/stack (web/native) + existing design system (if any)
- Goal: what “better” means (speed, consistency, craft, accessibility, quality, fewer handoff bugs)
- Constraints: team composition, timeline, quality bar, accessibility/compliance requirements

**Missing-info strategy**
- Ask up to **5** questions from [references/INTAKE.md](references/INTAKE.md), then proceed with explicit assumptions.
- If the team/stack is unknown, assume a modern web stack (component library + CI) and call out assumptions.
- Do not request secrets/credentials; use redacted identifiers.

## Outputs (deliverables)

Produce a **Design Engineering Execution Pack** in Markdown (in-chat by default; write to files if requested):

1) **Context snapshot** (goals, constraints, success signals)
2) **Design Engineering charter** (mission, scope, ownership boundaries, engagement model)
3) **Prototype → production workflow** (prototype ladder + decision rules + review gates)
4) **Design-to-code contract** (tokens/components/spec handoff, PR review expectations, QA)
5) **Component/flow delivery plan** (prioritized backlog + milestones + owners)
6) **Quality bar** (checklists + rubric score)
7) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Intake + success definition
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm scope (product area), stakeholders, and what “design engineering” means here (role vs function vs project). Define success signals (e.g., faster UI iteration, fewer handoff bugs, higher consistency, improved accessibility).
- **Outputs:** Context snapshot (draft).
- **Checks:** The team can answer in one sentence: “What will change if we do this well?”

### 2) Choose the operating model (and boundaries)
- **Inputs:** Team org, roadmap pressures, existing design/engineering capabilities.
- **Actions:** Select an engagement model (embedded, platform/design system, tiger team). Define responsibilities and boundaries vs Design and Engineering (who owns interaction design, component implementation, accessibility, visual QA, performance).
- **Outputs:** Design Engineering charter (draft) with explicit boundaries.
- **Checks:** No “two owners” ambiguity for components, tokens, and UI quality sign-off.

### 3) Map the UI surface area + constraints
- **Inputs:** Key flows/screens; existing components; constraints (devices, browsers, perf, a11y, localization).
- **Actions:** Inventory the highest-leverage UI areas (top flows, shared components). Identify reuse opportunities and risk hotspots (complex interactions, animations, data density, edge cases).
- **Outputs:** UI surface map + initial component/flow backlog.
- **Checks:** Backlog is prioritized by user impact and reuse (not just what’s loudest).

### 4) Define the prototype ladder (prototype → production)
- **Inputs:** Timeline, iteration speed needs, risk tolerance.
- **Actions:** Define a “prototype ladder” (lo-fi → hi-fi → coded prototype → production). For each rung, set purpose, expected fidelity, and whether it is disposable. Add decision rules for when to “graduate” a prototype.
- **Outputs:** Prototype → production workflow (ladder + rules + gates).
- **Checks:** Every prototype has an explicit label: **throwaway** vs **shippable**.

### 5) Write the design-to-code contract (handoff + reviews)
- **Inputs:** Design artifacts; code conventions; QA expectations.
- **Actions:** Define the contract: design tokens, component API expectations, states, a11y requirements, and review gates (design review, engineering review, QA). Specify what must be in a PR (screenshots, storybook links, test plan, a11y notes).
- **Outputs:** Design-to-code contract (v1).
- **Checks:** A developer can implement a component without back-and-forth on states, spacing/typography, and acceptance criteria.

### 6) Plan delivery (milestones + ownership)
- **Inputs:** Backlog + constraints + team capacity.
- **Actions:** Convert backlog into milestones (thin slices) with owners, dependencies, and acceptance criteria. Define how work is tracked (board columns) and how design engineering work is staffed.
- **Outputs:** Component/flow delivery plan (milestones).
- **Checks:** First milestone is small enough to ship within 1–2 weeks and sets patterns for the rest.

### 7) Quality gate + alignment + finalization
- **Inputs:** Draft pack.
- **Actions:** Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add stakeholder cadence and a lightweight decision log (what was chosen, why). Finalize **Risks / Open questions / Next steps**.
- **Outputs:** Final Design Engineering Execution Pack.
- **Checks:** Quality bar is explicit; ownership is unambiguous; risks and open questions are not hidden.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (stand up the function):** “Use `design-engineering`. We’re a 12-person product team. Web app. Designers ship Figma but engineering struggles with UI polish. Create a Design Engineering Execution Pack with an embedded model and a prototype→production workflow.”

**Example 2 (design system delivery):** “Create a design engineering plan for building a component library (buttons, inputs, tables, modals). Include the design-to-code contract, PR review checklist, and a 6-week milestone plan.”

**Boundary example:** “What is design engineering?”  
Response: explain this skill produces an execution pack; ask for context (team, product, goals). If they only want a definition, give a brief definition and point them to the intake questions to proceed.
