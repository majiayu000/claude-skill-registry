---
name: aico-frontend-design
description: |
  Transform PRD or story into complete page/component designs with ASCII layouts, component specs, interaction flows, and frontend implementation prompts.

  Use this skill when:
  - User asks to "design the page", "design component", "create page design"
  - User mentions "page design", "component design", "UI design", "layout design"
  - Running /frontend.design command
  - PRD or story is ready and need visual/interaction design before implementation
  - Need to create design spec that frontend developer can implement from

  Prerequisites: Design system must exist at docs/reference/frontend/design-system.md
  Output: ALWAYS write design files to docs/reference/frontend/designs/{name}.md
---

# Design

## ⚠️ CRITICAL RULES - READ FIRST

1. **CHECK EXISTING DESIGNS**: Always check `docs/reference/frontend/designs/` first
2. **READ DESIGN SYSTEM**: Must read `docs/reference/frontend/design-system.md` before designing
3. **READ CONSTRAINTS**: Must read `docs/reference/frontend/constraints.md` for tech stack
4. **SAVE TO CORRECT PATH**: `docs/reference/frontend/designs/{name}.md`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read design system**: Load `docs/reference/frontend/design-system.md`
2. **Read constraints**: Load `docs/reference/frontend/constraints.md`
3. **Read PRD/story**: Load the source document from `docs/reference/pm/`
4. **For each page/feature**:
   - Define user flow (entry → actions → outcome)
   - Create ASCII layout
   - List all components with variants and props
   - Write content/copy
   - Document all interactions
   - Generate frontend prompt
5. **Save output**: ALWAYS write to `docs/reference/frontend/designs/{name}.md`

## Design File Template

```markdown
# [Name] Design Spec

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD

## User Flow

1. User enters from [entry point]
2. User sees [initial state]
3. User can [actions]
4. Success: [outcome]

## Layout (ASCII)

┌─────────────────────────────────────┐
│ Header │
├─────────────────────────────────────┤
│ Content │
└─────────────────────────────────────┘

## Sections

### 1. [Section Name]

- **Purpose**: What this section achieves
- **Components**: List of UI components used
- **Content**: Actual text/copy
- **Design notes**: Specific styling details

## Component List

| Component | Variants           | Props          | Notes        |
| --------- | ------------------ | -------------- | ------------ |
| Button    | primary, secondary | size, disabled | Use for CTAs |

## Responsive

- **Desktop**: [layout notes]
- **Tablet**: [layout notes]
- **Mobile**: [layout notes]

## Interactions

| Trigger   | Action      | Feedback                     |
| --------- | ----------- | ---------------------------- |
| Click CTA | Submit form | Show loading → success toast |

---

## Frontend Prompt

<context>
You are implementing [page/component name] for [project].
</context>

<constraints>
Read and follow:
- Design system: docs/reference/frontend/design-system.md
- Frontend constraints: docs/reference/frontend/constraints.md
</constraints>

<requirements>
1. Follow the design system tokens exactly
2. Implement all sections as specified
3. Handle all responsive breakpoints
4. Implement all interactions listed
</requirements>
```

## Key Rules

- ALWAYS define user flow with entry point and success state
- MUST list specific props and variants for each component
- ALWAYS document all triggers and feedback for interactions
- Reference design system, don't duplicate it

## Common Mistakes

- ❌ Skip user flow → ✅ Always define entry point and success state
- ❌ Vague component specs → ✅ List specific props and variants
- ❌ Forget interactions → ✅ Document all triggers and feedback
- ❌ Duplicate design system → ✅ Reference it, don't copy
