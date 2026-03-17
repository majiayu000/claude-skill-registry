---
name: component-designer
description: Designs reusable UI components including buttons, inputs, cards, modals, and other interface elements. Specifies states, variations, and usage guidelines. Considers accessibility and responsive behavior.
---

# Component Designer Skill

## Instructions

1. Analyze component requirements from task
2. Design component structure and appearance
3. Define all component states (default, hover, active, disabled, focus, error)
4. Specify component variations (sizes, styles, types)
5. Consider accessibility requirements
6. Define responsive behavior
7. Return structured component specifications with:
   - Component description
   - Visual specifications (colors, sizes, spacing)
   - State variations
   - Usage guidelines
   - Accessibility requirements
   - Responsive behavior

## Examples

**Input:** "Design a button component"
**Output:**
```markdown
### Component: Button

**Variations:**
- Primary Button
- Secondary Button
- Tertiary Button
- Danger Button

**Sizes:**
- Small: padding 8px 16px, font 14px
- Medium: padding 12px 24px, font 16px (default)
- Large: padding 16px 32px, font 18px

**Primary Button States:**
- Default: Background #007bff, Text #ffffff, Border none
- Hover: Background #0056b3, Transform scale(1.02)
- Active: Background #004085
- Focus: Outline 2px solid #007bff, Outline offset 2px
- Disabled: Background #6c757d, Opacity 0.6, Cursor not-allowed

**Accessibility:**
- Minimum touch target: 44x44px
- Color contrast: 4.5:1 (WCAG AA)
- Keyboard accessible
- Focus indicator visible
- ARIA labels when needed

**Responsive:**
- Mobile: Full width on screens < 480px
- Tablet+: Auto width with min-width 120px
```

## Component Types

- **Buttons**: Primary, secondary, icon buttons
- **Inputs**: Text, email, password, textarea, select
- **Cards**: Content cards, product cards, feature cards
- **Modals**: Dialogs, popups, confirmations
- **Navigation**: Menus, breadcrumbs, pagination
- **Forms**: Form layouts, field groups, validation
- **Lists**: Ordered, unordered, definition lists
- **Tables**: Data tables, comparison tables
- **Alerts**: Success, error, warning, info messages
- **Badges**: Status badges, notification badges
- **Tooltips**: Hover tooltips, popover tooltips

## Component States

- **Default**: Initial appearance
- **Hover**: Mouse over state
- **Active**: Click/press state
- **Focus**: Keyboard focus state
- **Disabled**: Non-interactive state
- **Loading**: Loading/processing state
- **Error**: Error state
- **Success**: Success state
- **Selected**: Selected/checked state

## Accessibility Requirements

- **Touch Targets**: Minimum 44x44px for mobile
- **Color Contrast**: WCAG AA minimum (4.5:1)
- **Keyboard Navigation**: All interactive elements keyboard accessible
- **Focus Indicators**: Visible focus states
- **ARIA Labels**: Proper ARIA attributes
- **Semantic HTML**: Use appropriate HTML elements
