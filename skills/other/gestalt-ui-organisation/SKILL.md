---
name: gestalt-ui-organisation
description: UI layout and grouping should follow Gestalt principles so users immediately understand which controls, commands, and elements belong together. Use when designing or reviewing component layout, navigation, toolbars, forms, dashboards, or any UI where visual grouping communicates relationships.
metadata:
  priority: 7
  docs:
    - "https://www.interaction-design.org/literature/topics/gestalt-principles"
  pathPatterns:
    - "**/*.tsx"
    - "**/*.jsx"
    - "**/*.vue"
    - "**/*.svelte"
    - "components/**"
    - "src/components/**"
    - "design-system/**"
    - "ui/**"
  promptSignals:
    phrases:
      - "gestalt"
      - "grouping"
      - "visual hierarchy"
      - "ui layout"
      - "component organisation"
      - "related controls"
      - "ui clarity"
retrieval:
  aliases:
    - gestalt
    - visual grouping
    - ui organisation
    - proximity
    - similarity
    - figure ground
  intents:
    - group related controls
    - make ui clearer
    - organise components
    - show which elements belong together
    - improve visual hierarchy
  examples:
    - group these buttons so users know they're related
    - make it clearer which commands belong together
    - organise this toolbar using gestalt
---

# Gestalt UI Organisation

UI should be organised so that the visual structure communicates relationships — which commands, controls, and elements belong together — without requiring users to read labels or documentation.

## Core Gestalt Principles for UI Layout

### 1. Proximity
Elements that are close together are perceived as a group.

- Place related controls (e.g. Bold / Italic / Underline) close together with minimal gap between them
- Separate unrelated groups with larger whitespace
- Do not use lines or borders as the primary grouping mechanism — proximity alone should convey the relationship

**Example:** A toolbar with `[Cut] [Copy] [Paste]` grouped tightly, then a wider gap before `[Undo] [Redo]`, communicates two distinct command groups without any visual divider.

### 2. Similarity
Elements that look alike are perceived as related.

- Use consistent colour, shape, size, and iconography within a functional group
- Differentiate groups through visual contrast (shape, fill, size) — not just position
- Primary actions and secondary actions should look visually distinct from each other

**Example:** Destructive actions (Delete, Remove) use a different colour than constructive actions (Save, Add), signalling different intent groups.

### 3. Common Region
Elements enclosed in a shared region are perceived as a group.

- Use cards, panels, or background fills to enclose logically related content
- Avoid wrapping unrelated elements in the same container
- Nested regions should reflect nested logical hierarchy

**Example:** Form sections grouped in bordered cards signal that fields inside each card form a logical unit.

### 4. Connectedness
Elements connected by lines or visual links are perceived as related.

- Use connectors, lines, or flow arrows only when a genuine relationship exists
- In navigation trees or node-based editors, visible connections should match data relationships exactly

### 5. Figure / Ground
Users distinguish foreground interactive elements from background context.

- Interactive controls should have sufficient contrast against their background
- Disabled or contextual information should visually recede (lower contrast, smaller weight)
- Modals and overlays must clearly separate from the underlying content layer

### 6. Continuity
The eye follows smooth paths and lines.

- Align related controls along a consistent axis (left edge, baseline, or centre line)
- Avoid breaking alignment within a logical group
- Grid-aligned layouts reinforce groupings through shared axis continuity

## Review Checklist

When reviewing a UI layout for Gestalt compliance:

- [ ] Can a new user identify which controls belong together without reading labels?
- [ ] Is proximity used as the primary grouping signal (not only borders/lines)?
- [ ] Do visually similar elements share a functional purpose?
- [ ] Are unrelated groups separated by meaningful whitespace?
- [ ] Does visual hierarchy match interaction hierarchy (primary > secondary > tertiary)?
- [ ] Are destructive or irreversible actions visually distinct from constructive ones?
- [ ] Is the figure/ground contrast sufficient for all interactive elements?

## Common Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| All buttons same size and colour regardless of function | Similarity principle violated — implies all actions are equivalent | Differentiate primary, secondary, destructive visually |
| Related controls spread across distant areas of the screen | Proximity violated — user cannot perceive the relationship | Co-locate related controls |
| Overuse of divider lines to group elements | Relies on decoration rather than spatial logic | Use whitespace and proximity instead |
| Identical whitespace between all elements | No grouping signal — everything reads as a flat list | Apply 8pt/4pt spacing scale: tight within group, loose between groups |
| Mixed icon styles within one toolbar | Similarity broken — implies different functional families | Use a single consistent icon set and weight per toolbar |
