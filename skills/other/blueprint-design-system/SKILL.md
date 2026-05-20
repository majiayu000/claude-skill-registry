---
name: blueprint-design-system
description: Apply the Personal Action Blueprint design system to websites. Implements editorial typography, minimal borders, gold accents, and responsive fluid typography for itinerary, session, and profile pages.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Personal Action Blueprint Design System

## Overview

The Blueprint Design System creates a sophisticated, editorial aesthetic for Personal Action Blueprint websites. It emphasizes:

- **Editorial Typography**: Newsreader serif for headlines, Inter sans for body
- **Minimal Borders**: Thin #E5E3DE lines for separation
- **Gold Accents**: #C5A572 for highlights and active states
- **Responsive Typography**: Using clamp() for fluid type scales
- **Hover Elevations**: Cards lift with shadow on hover

---

## When to Use This Skill

Invoke this skill when:
- Building new pages for Personal Action Blueprint products
- Applying consistent styling to itinerary or session pages
- Creating profile cards, session items, or vendor cards
- Ensuring typography and spacing follow the blueprint system
- Adding interactive elements (buttons, toggles, hover states)

---

## Pre-Implementation Steps (ALWAYS DO THIS)

Before applying styles to any page:

### 1. Read the Complete Style Guide
```
Read: .claude/skills/blueprint-design-system/style-guide.md
```

### 2. Check Existing Pages for Consistency
```
Glob: **/*.html
```
Look for pages already using the blueprint system to maintain consistency.

### 3. Verify Font Import
Ensure the Google Fonts import is present in the `<head>`:
```html
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Inter:wght@400;500;600&family=Noto+Serif+JP:wght@500&display=swap" rel="stylesheet">
```

---

## Core Design Tokens

### Color Palette

```css
:root {
  --paper: #FFFFFF;        /* Primary background */
  --paper-alt: #FAFAF8;    /* Secondary background */
  --ink-900: #0A0B0C;      /* Primary text */
  --ink-700: #1F2124;      /* Strong emphasis */
  --ink-500: #5C626B;      /* Secondary text */
  --ink-400: #8B909A;      /* Tertiary text */
  --line: #E5E3DE;         /* Borders/dividers */
  --gold: #C5A572;         /* Accent/highlights */
  --vermillion: #E03E2F;   /* Hover states/CTA */
}
```

### Spacing System

```css
:root {
  --space-1: 8px;
  --space-2: 12px;
  --space-3: 20px;
  --space-4: 32px;
  --space-5: 48px;
  --space-6: 72px;
  --space-7: 96px;
}
```

### Typography Scale

| Element | Size | Line Height |
|---------|------|-------------|
| Hero (h1) | clamp(40px, 5vw, 56px) | 1.05 |
| XXL (h2) | clamp(32px, 4vw, 42px) | 1.2 |
| XL (h3) | clamp(24px, 3vw, 32px) | 1.2 |
| Large (h4) | clamp(18px, 2.5vw, 24px) | 1.3 |
| Medium | 17px | 1.5 |
| Small (body) | 15px | 1.6 |
| Extra Small | 13px | 1.5 |

---

## Component Quick Reference

### Header
- Background: `--paper-alt` (#FAFAF8)
- Bottom border: 1px solid `--line`
- Padding: 32px 0
- Contains: Wordmark (left) + Language toggle + Back link (right)

### Profile Card
- Background: `--paper-alt`
- Padding: 32px
- Border radius: 4px
- Contains profile name, badge, details with divider

### Section Numbers
- Size: 32px × 32px
- Background: `--ink-900`
- Color: white
- Font weight: 600

### Session Items
- Grid layout: 60px | 1fr (time | content)
- Gap: 20px
- Bottom border: 1px solid `--line`
- Padding: 12px 0
- Time display: monospace font

### Vendor Cards
- Border: 1px solid `--line`
- Padding: 20px
- Hover: translateY(-2px) + shadow 0 8px 16px rgba(0,0,0,0.08)
- Transition: all 0.3s

### CTA Button
- Padding: 14px 28px
- Background: `--ink-900` → Hover: `--vermillion`
- Color: white
- Font weight: 600
- Hover transform: translateY(-2px)
- Arrow animation on hover

### Language Toggle
- Button padding: 6px 10px
- Inactive: `--ink-500` text
- Active: White text on `--gold` background
- Border radius: 2px

---

## Implementation Workflow

### 1. Set Up Base Styles
Apply the CSS reset and base typography from `style-guide.md`.

### 2. Implement Layout Container
```css
.container {
  max-width: 900px;
  margin: 0 auto;
  padding: clamp(20px, 5vw, 48px);
}
```

### 3. Add Components
Use the component patterns from the style guide. Each component follows the design tokens.

### 4. Apply Interactive States
- Buttons: background transition + translateY on hover
- Cards: shadow + lift on hover
- Links: color transitions

### 5. Verify Responsiveness
Test with clamp() typography at different viewport widths.

---

## Special Elements

| Element | Style |
|---------|-------|
| Profile badges | Gold background, uppercase, letter-spacing 0.08em |
| Section subtitles | Italic, `--ink-500` color |
| Intelligence highlights | `--gold` color, font-weight 600 |
| Category headers | Uppercase, letter-spacing 0.08em, `--gold` color |

---

## Quality Checklist

Before finalizing any page:

- [ ] Google Fonts import is in the `<head>`
- [ ] CSS variables are defined in `:root`
- [ ] Base reset is applied (`* { margin: 0; padding: 0; box-sizing: border-box; }`)
- [ ] `-webkit-font-smoothing: antialiased` is on body
- [ ] Typography uses Newsreader for headings, Inter for body
- [ ] Colors match the palette exactly (no approximations)
- [ ] Spacing uses the system variables
- [ ] Interactive elements have hover transitions
- [ ] Layout is responsive with clamp() for typography
- [ ] Cards have proper hover elevation effects

---

## Anti-Patterns to Avoid

1. **Using generic fonts** — Always import and use Newsreader + Inter
2. **Hard-coded spacing** — Use the spacing variables
3. **Missing hover states** — All interactive elements need transitions
4. **Ignoring the gold accent** — Use sparingly but consistently
5. **Skipping the base reset** — Always include the CSS reset
6. **Non-responsive typography** — Use clamp() for fluid scaling
7. **Inconsistent borders** — Always use `--line` color

---

## Usage Examples

### Apply blueprint styling to a new page
```
Apply the Personal Action Blueprint design system to this itinerary page.
```

### Style session items
```
Style these session items following the blueprint design system with time/content grid.
```

### Create a profile card
```
Create a profile card component following the blueprint design system.
```

### Add vendor cards with hover effects
```
Add vendor cards with the blueprint hover elevation effect.
```

---

## Reference Files

- **Complete Style Guide**: `.claude/skills/blueprint-design-system/style-guide.md`
