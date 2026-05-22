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

## Aesthetic Validation with Playwright MCP

Use the actual Playwright MCP tools to validate visual design:

### Step 1: Navigate and Screenshot
```
mcp__playwright__browser_navigate(url: "http://localhost:3000")
mcp__playwright__browser_take_screenshot(fullPage: true, filename: "full-page.png")
```

### Step 2: Check Spacing & Alignment
```
mcp__playwright__browser_evaluate(function: `
  // Check computed margins/paddings
  const elements = document.querySelectorAll('*');
  const spacings = new Set();
  elements.forEach(el => {
    const style = getComputedStyle(el);
    ['margin', 'padding'].forEach(prop => {
      ['Top', 'Right', 'Bottom', 'Left'].forEach(dir => {
        const val = parseInt(style[prop + dir]);
        if (val > 0) spacings.add(val);
      });
    });
  });
  return [...spacings].sort((a,b) => a-b);
`)
```
Check: Does it follow 4px/8px grid?

### Step 3: Check Color Palette
```
mcp__playwright__browser_evaluate(function: `
  const colors = new Set();
  document.querySelectorAll('*').forEach(el => {
    const style = getComputedStyle(el);
    colors.add(style.color);
    colors.add(style.backgroundColor);
  });
  return [...colors].filter(c => c !== 'rgba(0, 0, 0, 0)');
`)
```
Check: Limited palette? Consistent use?

### Step 4: Check Typography
```
mcp__playwright__browser_evaluate(function: `
  const fonts = new Set();
  document.querySelectorAll('*').forEach(el => {
    fonts.add(getComputedStyle(el).fontFamily);
  });
  return [...fonts];
`)
```
Check: Max 2-3 font families?

### Step 5: Responsive Test
```
mcp__playwright__browser_resize(width: 375, height: 667)
mcp__playwright__browser_take_screenshot(filename: "mobile.png")
mcp__playwright__browser_resize(width: 1280, height: 800)
mcp__playwright__browser_take_screenshot(filename: "desktop.png")
```

### Step 6: Check Console for Errors
```
mcp__playwright__browser_console_messages(level: "error")
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
