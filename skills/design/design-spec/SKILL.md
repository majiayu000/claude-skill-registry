---
name: design-spec
description: Create UI/UX design specifications from requirements or Figma designs. Use when creating design specs, documenting UI components, or extracting design from Figma. Triggers on keywords like "design spec", "ui spec", "component spec", "mockup", "wireframe".
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch
---

# Design Specification

Create comprehensive UI/UX specifications for implementation.

## When to Use
- PBI needs design documentation
- Figma design ready for handoff
- Component specification required

## Quick Reference

### Workflow
1. Read source (PBI or Figma URL)
2. If Figma URL -> run `/figma-extract` first
3. Document component inventory
4. Define states and interactions
5. Extract design tokens
6. Create design spec artifact
7. Save to `team-artifacts/design-specs/`

### Spec Structure
1. **Overview:** Feature summary
2. **Component Inventory:** List all UI components
3. **States:** Default, hover, active, disabled, error
4. **Design Tokens:** Colors, typography, spacing
5. **Accessibility:** ARIA, keyboard nav
6. **Responsive:** Breakpoints, adaptations

### Output
- **Path:** `team-artifacts/design-specs/{YYMMDD}-designspec-{feature}.md`

### Design Token Format
```scss
// Colors
$primary: #1976D2;
$error: #D32F2F;

// Typography
$heading: 24px/1.2 'Inter';

// Spacing
$gap-sm: 8px;
$gap-md: 16px;
```

### Related
- **Role Skill:** `ux-designer`
- **Command:** `/design-spec`
- **Helper:** `/figma-extract`

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
