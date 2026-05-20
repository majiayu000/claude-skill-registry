---
name: design
description: Entry point for design tasks. Routes to brand-guidelines (brand identity, voice, assets), design-system (tokens, component specs), or ui-styling (implementation). Use for design decisions, visual consistency, design system creation.
license: MIT
---

# Design

Umbrella skill coordinating brand-guidelines, design-system, and ui-styling.

## When to Use

- Design decisions spanning identity + implementation
- New project design setup
- Design system creation
- Visual consistency audits
- Design-to-code workflows
- Choosing between design sub-skills

## Skill Routing

| Task | Skill | Description |
|------|-------|-------------|
| Logo, colors, voice, assets | `brand-guidelines` | Brand identity system |
| Tokens, specs, CSS vars | `design-system` | Token architecture |
| shadcn/ui, Tailwind, code | `ui-styling` | Implementation |

Load: `references/design-routing.md`

## Quick Reference

### Brand Identity
→ **brand-guidelines** skill
- Logo usage rules
- Color palette management
- Typography specifications
- Voice framework
- Asset organization

### Token Architecture
→ **design-system** skill
- Primitive → Semantic → Component layers
- CSS variables
- Component state specs
- Tailwind integration

### Implementation
→ **ui-styling** skill
- shadcn/ui components
- Tailwind utilities
- Dark mode
- Responsive design

## Workflow: New Design System

1. **Brand Foundation** (brand-guidelines)
   - Define brand colors, typography
   - Establish voice and tone
   - Create logo variants

2. **Extract Tokens** (design-system)
   - Convert brand → primitive tokens
   - Create semantic mappings
   - Define component tokens

3. **Implement** (ui-styling)
   - Configure Tailwind
   - Add shadcn/ui components
   - Apply design tokens

## Workflow: Design Audit

1. Review brand consistency (brand-guidelines)
2. Validate token usage (design-system)
3. Check component implementation (ui-styling)

## Integration

**Sub-skills:** brand-guidelines, design-system, ui-styling

**Related Skills:** frontend-design, ui-ux-pro-max

**Primary Agents:** ui-ux-designer, frontend-developer, content-creator

## Decision Tree

```
Design task?
├── Brand identity → brand-guidelines
│   ├── Logo usage
│   ├── Colors/fonts
│   ├── Voice/tone
│   └── Asset management
├── Token system → design-system
│   ├── CSS variables
│   ├── Component specs
│   └── Token validation
└── UI code → ui-styling
    ├── React components
    ├── Tailwind classes
    └── Dark mode
```
