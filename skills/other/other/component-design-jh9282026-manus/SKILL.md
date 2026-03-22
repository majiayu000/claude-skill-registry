---
name: component-design
description: "Design reusable UI components and design system elements with consistent styling and behavior. Use for: building design systems, creating component libraries, establishing UI patterns, and ensuring design consistency across products."
---

# Component Design

## Description

Component Design creates reusable, consistent UI building blocks. A well-designed component library ensures visual consistency, speeds up design/development, and maintains quality across all interfaces.

## When to Use

- After foundational design tokens (colors, type, spacing) are defined
- Before designing full pages
- Building a design system
- When UI needs consistency audit
- Creating handoff documentation

---

## Instructions for AI Agents

### Step 1: Identify Component Needs

**Prompt to inventory components:**
```
Based on the wireframes for [PROJECT], list all UI components needed:

**Actions**
- Buttons (primary, secondary, etc.)
- Links
- Icon buttons

**Inputs**
- Text inputs
- Select/dropdowns
- Checkboxes/radios
- Toggles
- Text areas

**Display**
- Cards
- Tables
- Lists
- Badges/tags
- Avatars
- Progress indicators

**Navigation**
- Tabs
- Breadcrumbs
- Pagination
- Menus

**Feedback**
- Alerts/toasts
- Modals
- Tooltips
- Empty states

**Layout**
- Headers
- Sidebars
- Footers
```

### Step 2: Define Component States

**Standard interactive states:**

| State | When | Visual Change |
|-------|------|---------------|
| Default | Normal state | Base appearance |
| Hover | Mouse over | Slight change (lighter/darker, shadow) |
| Focus | Keyboard focus | Visible focus ring |
| Active | Being clicked | Pressed appearance |
| Disabled | Not available | Reduced opacity, no interaction |
| Loading | Processing | Spinner, skeleton |
| Error | Validation failed | Error styling |
| Success | Action completed | Success styling |

### Step 3: Component Specification Template

**For each component, document:**

```markdown
## Success Criteria

### Minimum Requirements
- [ ] Core components designed (buttons, inputs, cards)
- [ ] All interactive states defined
- [ ] Size variants specified
- [ ] Colors reference design tokens
- [ ] Touch targets minimum 44px

### Quality Indicators
- [ ] Consistent across all components
- [ ] Accessible (contrast, focus states)
- [ ] Developer-ready specifications
- [ ] Covers all wireframe needs

---

## Related Skills

- **Previous**: `color_palettes.md`, `typography.md`, `spacing_rhythm.md`
- **Next**: `interaction_design.md` - Add micro-interactions
- **Related**: `design_documentation.md` - Full specification


## Using the Reference Files

**`/references/component_examples.md`** — Detailed component examples including buttons, inputs, cards, navigation, and badges.

**`/references/prompts_and_templates.md`** — Prompts library and component specification templates.

