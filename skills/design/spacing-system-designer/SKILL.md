---
name: spacing-system-designer
description: Creates spacing and sizing systems including margins, padding, gaps, and consistent spacing scales. Defines spacing tokens and usage guidelines for consistent layouts.
---

# Spacing System Designer Skill

## Instructions

1. Analyze spacing requirements from task
2. Create spacing scale (4px, 8px, 16px base or similar)
3. Define spacing tokens for margins, padding, gaps
4. Specify spacing usage guidelines
5. Consider responsive spacing adjustments
6. Return structured spacing system specifications with:
   - Spacing scale
   - Spacing tokens
   - Usage guidelines
   - Responsive variations

## Examples

**Input:** "Create spacing system"
**Output:**
```markdown
### Spacing System

**Base Unit:** 4px

**Spacing Scale:**
- xs: 4px (0.25rem)
- sm: 8px (0.5rem)
- md: 16px (1rem)
- lg: 24px (1.5rem)
- xl: 32px (2rem)
- 2xl: 48px (3rem)
- 3xl: 64px (4rem)

**Spacing Tokens:**
- `spacing.xs`: 4px - Tight spacing, icon padding
- `spacing.sm`: 8px - Small gaps, compact layouts
- `spacing.md`: 16px - Standard spacing, component padding
- `spacing.lg`: 24px - Section spacing, larger gaps
- `spacing.xl`: 32px - Major section spacing
- `spacing.2xl`: 48px - Page section spacing
- `spacing.3xl`: 64px - Large page sections

**Usage Guidelines:**
- Component padding: md (16px)
- Component margins: lg (24px)
- Section spacing: xl (32px)
- Page margins: 2xl (48px)
- Grid gaps: md (16px)

**Responsive Spacing:**
- Mobile: Reduce spacing by 25% (md becomes 12px)
- Tablet: Standard spacing
- Desktop: Standard spacing
```

## Spacing Types

- **Padding**: Internal spacing within components
- **Margins**: External spacing between components
- **Gaps**: Spacing in grid/flex layouts
- **Gutters**: Column spacing in grid systems
- **Section Spacing**: Spacing between major sections
- **Component Spacing**: Spacing between UI components

## Spacing Scale Approaches

- **4px Base**: 4, 8, 12, 16, 24, 32, 48, 64px
- **8px Base**: 8, 16, 24, 32, 48, 64, 96px
- **Fibonacci**: 4, 8, 12, 20, 32, 52px
- **Custom**: Based on design needs

## Responsive Considerations

- **Mobile**: Tighter spacing (reduce by 20-25%)
- **Tablet**: Standard spacing
- **Desktop**: Standard or slightly increased spacing
