---
name: frontend-design-fix-html
description: Fix generic HTML/CSS designs by applying aesthetic upgrades across the 5 design dimensions (typography, color, motion, spatial composition, backgrounds)
version: 1.0.0
framework: HTML/CSS
category: design-system
tools: [Read, Write, Edit, Grep, Glob, Bash]
scope: project
enabled: true
---

# Frontend Design Fix - HTML/CSS

## Overview

Transform bland, generic HTML/CSS designs into visually distinctive interfaces by systematically applying the 5 design dimensions from Anthropic's design framework.

## Core Workflow

### 1. Analysis Phase
- Read existing HTML/CSS files
- Identify generic elements (Inter/Roboto fonts, purple gradients, centered layouts, no animations, solid backgrounds)
- Score current design against anti-patterns checklist
- Generate "before" snapshot with metrics

### 2. Assessment Phase
- Understand brand/context from existing content and markup
- Identify target audience and purpose
- Determine appropriate aesthetic direction based on content

### 3. Dimension-Based Fixes

#### Typography
- Replace generic system fonts (Inter, Roboto, Arial) with distinctive typeface pairs
- Apply extreme weight ranges (100-200 for thin, 800-900 for bold)
- Increase size jumps (3x+ progression instead of 1.5x)
- Create high-contrast pairings (Display + Mono, Serif + Sans)

#### Color & Theme
- Remove default purple gradients on white backgrounds
- Introduce CSS custom properties (--primary, --accent, --surface)
- Establish dominant colors with sharp accent colors
- Avoid evenly-distributed palettes (use 70-20-10 rule)

#### Motion
- Add orchestrated page load animations (fade, scale, slide)
- Implement staggered reveals with `animation-delay`
- Add hover state surprises and micro-interactions
- Include scroll-triggered animations where appropriate

#### Spatial Composition
- Break centered, predictable layouts
- Add asymmetry or intentional overlap
- Introduce diagonal flow or grid-breaking elements
- Adjust spacing (generous negative space OR controlled density)

#### Backgrounds
- Replace solid colors with layered gradients
- Add geometric patterns or subtle noise textures
- Create atmospheric depth with multiple background layers
- Add contextual effects (blur, blend modes)

### 4. Implementation
- Apply fixes systematically per dimension
- Maintain accessibility standards (WCAG 2.1 AA)
- Preserve all existing functionality
- Test responsive behavior at key breakpoints

### 5. Validation
- Re-score against anti-patterns checklist
- Generate "after" snapshot with improved metrics
- Create before/after comparison report
- Verify accessibility compliance

## Design Audit Checklist

### Typography Audit
- [ ] Current font stack is generic (Inter, Roboto, Arial, system stack)
- [ ] Font weights are limited (only regular and bold)
- [ ] Size progression is minimal (1.25-1.5x multiplier)
- [ ] No distinctive pairing strategy
- [ ] Poor readability on colored backgrounds

### Color & Theme Audit
- [ ] Purple/blue gradient on white background (cliché)
- [ ] No CSS custom properties for theming
- [ ] Evenly distributed color palette (5+ primary colors)
- [ ] No accent color for emphasis
- [ ] Insufficient contrast in interactive elements

### Motion Audit
- [ ] No page load animations
- [ ] No staggered reveals
- [ ] Hover states missing or uninspired
- [ ] No scroll interactions
- [ ] Abrupt transitions between states

### Spatial Composition Audit
- [ ] Centered, symmetrical layouts throughout
- [ ] Predictable margins and padding
- [ ] No intentional asymmetry
- [ ] Grid-aligned everything (no breaking)
- [ ] Single-column or evenly-spaced multi-column layouts

### Background Audit
- [ ] Solid white or light gray backgrounds
- [ ] No layering or depth
- [ ] No texture or pattern application
- [ ] Generic or missing hero sections
- [ ] No atmospheric or contextual effects

## Implementation Tips

### CSS Best Practices
```css
/* Use custom properties for consistency */
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;

  --primary: #1a1a1a;
  --accent: #ff6b35;
  --surface: #fafafa;

  --transition-fast: 200ms ease-out;
  --transition-base: 400ms ease-out;
}

/* Orchestrate animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Stagger with nth-child */
[data-stagger] {
  animation: fadeInUp var(--transition-base) ease-out forwards;
}

[data-stagger]:nth-child(1) { animation-delay: 100ms; }
[data-stagger]:nth-child(2) { animation-delay: 200ms; }
[data-stagger]:nth-child(3) { animation-delay: 300ms; }
```

### Accessibility Maintenance
- Keep WCAG AA color contrast minimum 4.5:1 for text
- Maintain focus visible outlines
- Test keyboard navigation
- Preserve semantic HTML structure

## Examples

See `/examples/showcase.md` for before/after comparisons:
- Generic landing page → Distinctive landing page
- Boring dashboard → Visually striking dashboard
- Plain form → Aesthetically enhanced form

## Success Metrics

After applying fixes, the design should:
- Score 0-2 items remaining on the anti-patterns checklist
- Have distinctive typography choices
- Include motion and micro-interactions
- Feature asymmetric or broken-grid layouts
- Use layered/textured backgrounds
- Maintain or improve accessibility scores
