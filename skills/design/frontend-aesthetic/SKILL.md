---
name: frontend-aesthetic
description: UI/UX visual design, styling, and aesthetic validation
requires_mcp: playwright
integrates_with:
  - web-design-guidelines
  - playwright-automation
  - react-best-practices
---

# Frontend Aesthetic

Visual design guidance for beautiful, consistent, and accessible UIs.

## Core Principles

### 1. Visual Hierarchy
- Size, color, contrast guide the eye
- Primary actions should be obvious
- Group related elements visually

### 2. Spacing & Layout
- Use consistent spacing scale (4px, 8px, 16px, 24px, 32px, 48px, 64px)
- Whitespace is a design element, not empty space
- Align elements to a grid

### 3. Typography
- Limit to 2-3 font families max
- Use font weight for hierarchy (not just size)
- Line height: 1.4-1.6 for body, 1.2 for headings
- Max line length: 60-80 characters

### 4. Color
- Primary, secondary, accent colors
- Semantic colors: success (green), warning (yellow), error (red), info (blue)
- Ensure 4.5:1 contrast ratio for accessibility
- Dark mode: don't just invert, redesign

### 5. Motion & Animation
- Subtle, purposeful animations (200-300ms)
- Ease-out for entrances, ease-in for exits
- Reduce motion for accessibility preference

## Component Patterns

### Buttons
```css
/* Primary */
background: var(--primary);
color: white;
padding: 12px 24px;
border-radius: 8px;
font-weight: 600;

/* Hover: slight brightness change */
/* Active: scale(0.98) */
/* Disabled: opacity 0.5, cursor not-allowed */
```

### Cards
```css
background: var(--surface);
border-radius: 12px;
padding: 24px;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
/* Hover: elevate shadow */
```

### Forms
- Labels above inputs (not placeholder-only)
- Clear focus states (outline, not just color)
- Error states: red border + icon + message
- Success feedback on submission

### Navigation
- Current page indicator
- Consistent iconography
- Mobile: bottom nav or hamburger (not both)

## Aesthetic Validation with Playwright

Use Playwright MCP to validate visual design:

```
1. Navigate to the page
2. Take full-page screenshot
3. Check for:
   - Consistent spacing
   - Color contrast issues
   - Typography hierarchy
   - Alignment problems
   - Responsive breakpoints
```

## Common Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Rainbow of colors | Limited, intentional palette |
| Tiny click targets | Min 44x44px touch targets |
| Text on busy backgrounds | Overlay or solid backgrounds |
| Inconsistent border-radius | Pick one: 4px, 8px, or 12px |
| Auto-playing animations | User-triggered or subtle loops |
| Placeholder-only labels | Visible labels always |

## Design System Integration

When working with existing design systems:
- Tailwind: Use config theme values
- Material UI: Follow MD3 guidelines
- Chakra: Use theme tokens
- Custom: Document tokens in CSS variables

## Workflow

1. **Audit**: Screenshot current state
2. **Identify**: List aesthetic issues
3. **Prioritize**: Fix high-impact items first
4. **Implement**: Make CSS/component changes
5. **Validate**: Screenshot after, compare

## Integration

- **playwright-automation**: Take screenshots, inspect DOM
- **web-design-guidelines**: Technical accessibility rules
- **react-best-practices**: Component architecture
