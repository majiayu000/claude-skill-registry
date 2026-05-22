---
name: "design-systems"
description: "Build or evolve a design system by producing a Design System Operating Pack: charter, token model (incl. depth/elevation), component inventory + roadmap, blockframe-to-component mapping, documentation plan, and governance/adoption plan. Use for design systems, component libraries, design tokens, UI kits, and pattern libraries."
---

# Design Systems

## Scope

**Covers**
- Creating or upgrading a **design system** (tokens + components + guidelines)
- Using **blockframes** (lo-fi, system-aware wireframes) to lock logic before hi-fi execution
- Designing a **future-ready visual foundation** (depth/elevation, motion, texture) without breaking consistency
- Making the system **easy for non-experts** to use (guardrails, examples, starter templates)
- Driving **adoption + governance** (contribution model, champions, release cadence)

**When to use**
- “We need a design system / component library and a plan to build it.”
- “Our UI is inconsistent—define tokens + components + documentation to standardize.”
- “We want to refresh our UI style (more depth/texture/motion) without chaos.”
- “We need to scale design across teams or support enterprise customers with customization.”
- “We want faster hi-fi output by locking flows in lo-fi first.”

**When NOT to use**
- You’re defining a brand identity or logo system (different process).
- You need user research/discovery to decide *what* to build.
- You only need to ship one isolated UI change (just implement it).
- You’re doing pure front-end architecture unrelated to UI consistency.

## Inputs

**Minimum required**
- Product + surfaces: web/iOS/Android; key flows
- Current state: existing UI kit/design system (if any), design tool (e.g., Figma), code stack (if relevant)
- Goals: speed, consistency, accessibility, scalability, customization, enterprise adoption
- Constraints: timeline, team ownership, level of engineering support, compliance/a11y needs

**Missing-info strategy**
- Ask up to **5** questions from [references/INTAKE.md](references/INTAKE.md), then proceed with explicit assumptions.
- If platform/stack is unknown, assume a modern web product with a component library and design tokens.
- Do not request secrets or credentials.

## Outputs (deliverables)

Produce a **Design System Operating Pack** in Markdown (in-chat by default; write to files if requested):

1) **Context snapshot** (goals, constraints, success signals)
2) **Design system charter** (mission, scope, principles, audiences, in/out)
3) **UI audit + operational blockers** (what’s slowing teams down; what must standardize first)
4) **Blockframe-to-component map** (lo-fi flows + mapping to components/tokens)
5) **Token model** (taxonomy, naming rules, and initial token backlog—include elevation/depth)
6) **Component inventory + roadmap** (tiers, prioritization, milestones)
7) **Documentation + enablement plan** (non-designer-friendly, “teaches by structure”)
8) **Governance + adoption plan** (contribution workflow, decision rights, champions, release cadence)
9) **Quality gate** (checklists + rubric score) + **Risks / Open questions / Next steps**

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (7 steps)

### 1) Intake + success definition (who is this for?)
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Confirm primary users of the system (designers, engineers, PMs, “non-designers”). Define success signals (cycle time, consistency, adoption, fewer UI bugs, faster onboarding).
- **Outputs:** Context snapshot (draft).
- **Checks:** Success is measurable or at least falsifiable (e.g., “80% of new screens use system components”).

### 2) Audit the current UI and find the operational “hook”
- **Inputs:** Screens/flows, existing components, pain points, enterprise needs (if any).
- **Actions:** Inventory inconsistencies (spacing/type/color/components), identify the **operational blocker** the system will remove (e.g., slow production, inconsistent UI, customization needs). Choose the first high-leverage slice.
- **Outputs:** UI audit + operational blockers list; initial scope slice.
- **Checks:** The first slice is narrow enough to ship but broad enough to set patterns.

### 3) Lock logic with blockframes (separate thinking from styling)
- **Inputs:** Key flows; current IA; constraints.
- **Actions:** Create or specify “blockframes” (lo-fi, system-aware wireframes). Map each block to intended components and token usage so hi-fi execution becomes faster and more consistent.
- **Outputs:** Blockframe-to-component map (v1).
- **Checks:** A reviewer can validate flow/IA without debating visual details.

### 4) Define the token model (make the future style changeable)
- **Inputs:** Brand constraints, accessibility targets, desired direction (e.g., depth/texture/motion).
- **Actions:** Define token taxonomy + naming; include elevation/depth and state tokens. If doing a visual refresh, design the token model so style can evolve without rewriting components.
- **Outputs:** Token model + token backlog (v1).
- **Checks:** Tokens support theming and states; accessibility constraints are addressed (contrast, focus, motion).

### 5) Define the component model + delivery plan
- **Inputs:** Audit + blockframes + token model; engineering constraints.
- **Actions:** Tier components (primitives → composites → patterns). Prioritize by reuse and user impact. Define milestones, owners, and acceptance criteria.
- **Outputs:** Component inventory + roadmap (milestones).
- **Checks:** Milestone 1 ships within 1–2 weeks and establishes “golden path” patterns.

### 6) Make it easy to use (guardrails for non-experts)
- **Inputs:** Target user types; common mistakes; documentation needs.
- **Actions:** Design documentation and component guidelines so they “teach by structure”: sensible defaults, constrained options, examples, do/don’t. Provide starter templates for common layouts.
- **Outputs:** Documentation + enablement plan (v1).
- **Checks:** A non-expert can assemble a consistent screen using templates with minimal training.

### 7) Governance + adoption + quality gate
- **Inputs:** Draft pack; stakeholder map; toolchain (Figma/Storybook/etc.).
- **Actions:** Define decision rights, contribution workflow, review gates, and release cadence. Create a champion/office-hours plan to drive adoption. Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Finalize **Risks / Open questions / Next steps**.
- **Outputs:** Final Design System Operating Pack.
- **Checks:** Ownership is unambiguous; adoption plan exists; quality bar is explicit and repeatable.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples
See [references/EXAMPLES.md](references/EXAMPLES.md).
