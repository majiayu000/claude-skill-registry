---
name: design-spec
version: 2.0.0
description: '[Project Management] Create UI/UX design specifications from requirements, PBIs, or user stories. Produces structured design spec documents with layout, typography, colors, interactions, and responsive breakpoints. Triggers on design spec, design specification, UI specification, component spec, layout spec, wireframe, mockup.'
allowed-tools: Read, Write, Edit, Grep, Glob
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

## Quick Summary

**Goal:** Create structured UI/UX design specification documents from requirements or PBIs for developer handoff.

**Workflow:**

1. **Read Source** — Extract UI requirements from PBI, story, or Figma URL
2. **Determine Complexity** — Quick Spec (sections 1-4) vs Full Spec (all 7 sections)
3. **Build Component Inventory** — List new vs existing components
4. **Define States & Tokens** — Interactions, design tokens, responsive breakpoints
5. **Save Artifact** — Output to `team-artifacts/design-specs/`

**Key Rules:**

- If Figma URL provided → auto-routes to `/figma-design` for context extraction
- If wireframe image provided → auto-routes to `/wireframe-to-spec` for structured analysis
- If screenshot provided → uses `ai-multimodal` for design extraction
- Reference existing design system tokens from `docs/project-reference/design-system/`
- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Include accessibility requirements (keyboard nav, ARIA labels, contrast)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

# Design Specification

Create structured UI/UX design specification documents from requirements or PBIs for developer handoff.

## When to Use

- A PBI or user story needs a design spec before implementation
- Translating requirements into concrete UI layout, states, and tokens
- Documenting component inventory and interaction patterns
- Creating responsive breakpoint specifications

## When NOT to Use

- This skill auto-routes Figma URLs to `/figma-design` and wireframes to `/wireframe-to-spec` — no need to call those skills separately
- Building the actual UI -- use `frontend-design`
- Full UX research and design process -- use `ux-designer`
- Reviewing existing UI code -- use `web-design-guidelines`

## Prerequisites

Read before executing:

- The source PBI, user story, or requirements document
- `docs/project-reference/design-system/` -- project design tokens (if applicable)
- Existing design specs in `team-artifacts/design-specs/` for format consistency

### Frontend/UI Context

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Frontend patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

## Workflow

1. **Read source input & route by type**

    | Input Detected           | Detection                                      | Action                                                                   |
    | ------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------ |
    | Figma URL                | `figma.com/design` or `figma.com/file` in text | Activate `/figma-design` to extract context, then continue               |
    | Image/screenshot         | Image file attached to prompt                  | Use `ai-multimodal` to extract design guidelines, then continue          |
    | Hand-drawn wireframe     | Image + "wireframe"/"sketch" keyword           | Activate `/wireframe-to-spec` to generate structured spec, then continue |
    | PBI/story text           | Acceptance criteria present                    | Extract UI requirements from text, continue                              |
    | Verbal/text requirements | No image, no URL, no PBI                       | Clarify with user, then continue                                         |

    For ANY visual input: extract design context FIRST, then proceed to spec generation.

2. **Determine spec complexity**

    ```
    IF single form or simple component → Quick Spec (sections 1-4 only)
    IF full page or multi-component view → Full Spec (all 7 sections)
    IF multi-page flow → Full Spec + Flow Diagram
    ```

3. **Build component inventory**
    - List all UI components needed
    - Identify reusable vs feature-specific components
    - Note existing components from shared component library or design system

4. **Define states and interactions**
    - Default, hover, active, disabled, error, loading, empty states
    - User interactions (click, drag, keyboard shortcuts)
    - Transitions and animations

5. **Extract design tokens**
    - Colors, typography, spacing, shadows, border-radius
    - Reference existing design system tokens where possible

6. **Document responsive behavior**
    - Mobile (320-767px), Tablet (768-1023px), Desktop (1024px+)
    - What changes at each breakpoint (layout, visibility, sizing)

7. **Save artifact**
    - Path: `team-artifacts/design-specs/{YYMMDD}-designspec-{feature-slug}.md`

## Output Format

```markdown
# Design Spec: {Feature Name}

**Source:** {PBI/story reference}
**Date:** {YYMMDD}
**Status:** Draft | Review | Approved

## 1. Overview

{1-2 sentence summary of what this UI does}

## 2. Component Inventory

| Component | Type     | Source           | Notes                       |
| --------- | -------- | ---------------- | --------------------------- |
| UserCard  | New      | Feature-specific | Displays user avatar + name |
| DataTable | Existing | shared library   | Reuse with custom columns   |

## 3. Layout

{Description or ASCII wireframe of layout structure}

- Desktop: {layout description}
- Tablet: {layout changes}
- Mobile: {layout changes}

## 4. Design Tokens

| Token      | Value          | Usage                 |
| ---------- | -------------- | --------------------- |
| $primary   | #1976D2        | Action buttons, links |
| $text-body | 14px/1.5 Inter | Body text             |
| $gap-md    | 16px           | Section spacing       |

## 5. States & Interactions

| Element  | Default    | Hover      | Active     | Disabled         | Error |
| -------- | ---------- | ---------- | ---------- | ---------------- | ----- |
| Save btn | Blue/white | Darken 10% | Scale 0.98 | Gray/50% opacity | --    |

## 6. Accessibility

- Keyboard navigation order
- ARIA labels for interactive elements
- Color contrast compliance notes

## 7. Open Questions

- {Any unresolved design decisions}
```

## Examples

### Example 1: Simple form spec

**Input:** "Design spec for employee onboarding form"

**Output:** Quick Spec with sections 1-4 covering form fields (name, email, department dropdown, start date picker), validation rules, submit/cancel actions, and mobile stacking behavior.

### Example 2: Complex dashboard spec

**Input:** "Design spec for recruitment pipeline dashboard with drag-and-drop columns"

**Output:** Full Spec covering Kanban board layout, candidate cards (component inventory), drag-and-drop interactions, column states (empty, populated, over-limit), filter bar, responsive collapse to list view on mobile, and accessibility for keyboard drag operations.

## Related Skills

| Skill                   | When to use instead                  |
| ----------------------- | ------------------------------------ |
| `ux-designer`           | Full UX design process with research |
| `figma-design`          | Extract specs from Figma designs     |
| `frontend-design`       | Build the actual UI implementation   |
| `interface-design`      | Product UI design (dashboards, apps) |
| `web-design-guidelines` | Review existing UI for compliance    |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements

---

## Workflow Recommendation

> **IMPORTANT MUST:** If you are NOT already in a workflow, use `AskUserQuestion` to ask the user:
>
> 1. **Activate `design-workflow` workflow** (Recommended) — design-spec → code-review
> 2. **Execute `/design-spec` directly** — run this skill standalone
