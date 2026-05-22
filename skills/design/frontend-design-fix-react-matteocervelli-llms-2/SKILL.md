---
name: frontend-design-fix-react
description: Fix generic React component designs by applying aesthetic upgrades across the 5 design dimensions (typography, color, motion, spatial composition, backgrounds)
version: 1.0.0
framework: React
category: design-system
tools: [Read, Write, Edit, Grep, Glob, Bash]
scope: project
enabled: true
---

# Frontend Design Fix - React

## Overview

Transform bland, generic React component designs into visually distinctive interfaces by systematically applying the 5 design dimensions from Anthropic's design framework.

## Core Workflow

### 1. Analysis Phase
- Read existing React component files and CSS/CSS-in-JS
- Identify generic elements (Inter/Roboto fonts, purple gradients, centered layouts, no animations, solid backgrounds)
- Score current design against anti-patterns checklist
- Generate "before" snapshot with metrics

### 2. Assessment Phase
- Understand brand/context from existing content and component props
- Identify target audience and purpose
- Determine appropriate aesthetic direction based on component usage

### 3. Dimension-Based Fixes

#### Typography
- Replace generic system fonts (Inter, Roboto, Arial) with distinctive typeface pairs
- Apply extreme weight ranges (100-200 for thin, 800-900 for bold)
- Increase size jumps (3x+ progression instead of 1.5x)
- Create high-contrast pairings (Display + Mono, Serif + Sans)
- Use CSS-in-JS (Tailwind, styled-components, emotion) for responsive typography

#### Color & Theme
- Remove default purple gradients on white backgrounds
- Introduce CSS custom properties or theme provider context
- Establish dominant colors with sharp accent colors
- Avoid evenly-distributed palettes (use 70-20-10 rule)
- Create theme variants (light/dark) with consistent color tokens

#### Motion
- Add orchestrated page load animations (fade, scale, slide)
- Implement staggered reveals with `animation-delay` or Framer Motion
- Add hover state surprises and micro-interactions
- Include scroll-triggered animations via `react-intersection-observer`
- Use Framer Motion for complex animation sequences

#### Spatial Composition
- Break centered, predictable layouts
- Add asymmetry or intentional overlap
- Introduce diagonal flow or grid-breaking elements
- Adjust spacing (generous negative space OR controlled density)
- Use CSS Grid and Flexbox creatively

#### Backgrounds
- Replace solid colors with layered gradients
- Add geometric patterns or subtle noise textures
- Create atmospheric depth with multiple background layers
- Add contextual effects (blur, blend modes)
- Use pseudo-elements for background layering

### 4. Implementation
- Apply fixes systematically per dimension
- Update component props and styling
- Maintain accessibility standards (WCAG 2.1 AA)
- Preserve all existing functionality and component APIs
- Test with responsive design

### 5. Validation
- Re-score against anti-patterns checklist
- Generate "after" snapshot with improved metrics
- Create before/after comparison report
- Verify accessibility compliance with React testing library

## Design Audit Checklist

### Typography Audit
- [ ] Current font stack is generic (Inter, Roboto, Arial, system stack)
- [ ] Font weights are limited (only regular and bold)
- [ ] Size progression is minimal (1.25-1.5x multiplier)
- [ ] No distinctive pairing strategy
- [ ] Poor readability on colored backgrounds
- [ ] No responsive typography scaling

### Color & Theme Audit
- [ ] Purple/blue gradient on white background (cliché)
- [ ] No theme provider or CSS custom properties
- [ ] Evenly distributed color palette (5+ primary colors)
- [ ] No accent color for emphasis
- [ ] Insufficient contrast in interactive elements
- [ ] No dark mode support

### Motion Audit
- [ ] No page load animations
- [ ] No staggered reveals for lists
- [ ] Hover states missing or uninspired
- [ ] No scroll interactions
- [ ] Abrupt transitions between states
- [ ] Missing micro-interactions on buttons/forms

### Spatial Composition Audit
- [ ] Centered, symmetrical layouts throughout
- [ ] Predictable margins and padding
- [ ] No intentional asymmetry in component layouts
- [ ] Grid-aligned everything (no breaking)
- [ ] Single-column or evenly-spaced multi-column layouts

### Background Audit
- [ ] Solid white or light gray backgrounds
- [ ] No layering or depth in backgrounds
- [ ] No texture or pattern application
- [ ] Generic or missing hero sections
- [ ] No atmospheric or contextual effects in components

## Implementation Tips

### React + Tailwind Example
```jsx
// Use CSS custom properties with Tailwind
const theme = {
  colors: {
    display: "'Playfair Display', serif",
    body: "'Inter', sans-serif",
    mono: "'IBM Plex Mono', monospace",
  }
};

export function DesignedComponent() {
  return (
    <div className="
      bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900
      min-h-screen
      font-[family-name:var(--font-body)]
    ">
      <h1 className="
        font-[family-name:var(--font-display)]
        text-6xl font-black
        animate-fade-in-up
      ">
        Distinctive Title
      </h1>
    </div>
  );
}
```

### Framer Motion for Orchestration
```jsx
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

export function StaggeredList({ items }) {
  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={itemVariants}>
          {item.content}
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Theme Provider Pattern
```jsx
import { createContext, useContext } from 'react';

const ThemeContext = createContext({});

export function ThemeProvider({ children }) {
  const theme = {
    colors: {
      primary: '#1a1a1a',
      accent: '#ff6b35',
      surface: '#fafafa',
    },
    fonts: {
      display: "'Playfair Display', serif",
      body: "'Inter', sans-serif",
    },
  };

  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

### Accessibility Maintenance
- Keep WCAG AA color contrast minimum 4.5:1 for text
- Maintain focus visible outlines in interactive elements
- Use semantic React components (Button, Link, etc.)
- Test with React Testing Library
- Preserve ARIA attributes

## Examples

See `/examples/showcase.md` for before/after comparisons:
- Generic landing page → Distinctive landing page
- Boring dashboard → Visually striking dashboard
- Plain form → Aesthetically enhanced form

## Success Metrics

After applying fixes, the design should:
- Score 0-2 items remaining on the anti-patterns checklist
- Have distinctive typography choices in components
- Include motion and micro-interactions with Framer Motion
- Feature asymmetric or broken-grid layouts
- Use layered/textured backgrounds via pseudo-elements or gradients
- Maintain or improve accessibility scores
- Support light/dark theme variants
