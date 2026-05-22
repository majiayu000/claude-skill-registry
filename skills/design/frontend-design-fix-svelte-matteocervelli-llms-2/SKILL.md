---
name: frontend-design-fix-svelte
description: Fix generic Svelte component designs by applying aesthetic upgrades across the 5 design dimensions (typography, color, motion, spatial composition, backgrounds)
version: 1.0.0
framework: Svelte
category: design-system
tools: [Read, Write, Edit, Grep, Glob, Bash]
scope: project
enabled: true
---

# Frontend Design Fix - Svelte

## Overview

Transform bland, generic Svelte component designs into visually distinctive interfaces by systematically applying the 5 design dimensions from Anthropic's design framework.

## Core Workflow

### 1. Analysis Phase
- Read existing Svelte component files (.svelte)
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
- Use scoped styles with Svelte's native CSS-in-component

#### Color & Theme
- Remove default purple gradients on white backgrounds
- Introduce CSS custom properties for theming
- Establish dominant colors with sharp accent colors
- Avoid evenly-distributed palettes (use 70-20-10 rule)
- Create theme variants (light/dark) with consistent color tokens

#### Motion
- Add orchestrated page load animations (fade, scale, slide)
- Implement staggered reveals with Svelte transitions and animations
- Add hover state surprises and micro-interactions
- Include scroll-triggered animations via `svelte-use`
- Use `svelte/animate` for list transitions

#### Spatial Composition
- Break centered, predictable layouts
- Add asymmetry or intentional overlap
- Introduce diagonal flow or grid-breaking elements
- Adjust spacing (generous negative space OR controlled density)
- Use CSS Grid and Flexbox creatively with Svelte slots

#### Backgrounds
- Replace solid colors with layered gradients
- Add geometric patterns or subtle noise textures
- Create atmospheric depth with multiple background layers
- Add contextual effects (blur, blend modes)
- Use pseudo-elements for background layering

### 4. Implementation
- Apply fixes systematically per dimension
- Update component templates and styles
- Maintain accessibility standards (WCAG 2.1 AA)
- Preserve all existing functionality and component props
- Test with responsive design

### 5. Validation
- Re-score against anti-patterns checklist
- Generate "after" snapshot with improved metrics
- Create before/after comparison report
- Verify accessibility compliance with Vitest

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
- [ ] No CSS custom properties for theming
- [ ] Evenly distributed color palette (5+ primary colors)
- [ ] No accent color for emphasis
- [ ] Insufficient contrast in interactive elements
- [ ] No dark mode support

### Motion Audit
- [ ] No page load animations or transition directives
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

### Svelte Component with Scoped Styles
```svelte
<script>
  import { onMount } from 'svelte';

  let isVisible = false;

  onMount(() => {
    isVisible = true;
  });
</script>

<div class="container" class:visible={isVisible}>
  <h1>Distinctive Title</h1>
  <p>Beautifully designed with Svelte</p>
</div>

<style>
  :root {
    --font-display: 'Playfair Display', serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'IBM Plex Mono', monospace;
    --primary: #1a1a1a;
    --accent: #ff6b35;
    --surface: #fafafa;
  }

  .container {
    background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease-out;
  }

  .container.visible {
    opacity: 1;
    transform: translateY(0);
  }

  h1 {
    font-family: var(--font-display);
    font-size: 4rem;
    font-weight: 900;
    color: white;
  }

  p {
    font-family: var(--font-body);
    color: rgba(255, 255, 255, 0.8);
    margin-top: 1rem;
  }

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
</style>
```

### Staggered List with Svelte Animate
```svelte
<script>
  import { flip } from 'svelte/animate';
  import { fade } from 'svelte/transition';

  export let items = [];
</script>

<div class="list-container">
  {#each items as item, i (item.id)}
    <div
      class="list-item"
      animate:flip={{ duration: 200 }}
      transition:fade
      style="--stagger-index: {i}"
    >
      {item.content}
    </div>
  {/each}
</div>

<style>
  .list-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .list-item {
    padding: 1rem;
    border-radius: 0.5rem;
    background: var(--surface);
    color: var(--primary);
    animation: slideIn 0.4s ease-out;
    animation-delay: calc(var(--stagger-index) * 100ms);
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateX(-20px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }
</style>
```

### Theme Store with Svelte
```svelte
<!-- stores/theme.js -->
import { writable } from 'svelte/store';

export const theme = writable({
  colors: {
    primary: '#1a1a1a',
    accent: '#ff6b35',
    surface: '#fafafa',
    background: '#ffffff',
  },
  fonts: {
    display: "'Playfair Display', serif",
    body: "'Inter', sans-serif",
    mono: "'IBM Plex Mono', monospace",
  },
});

export function toggleDarkMode() {
  theme.update(t => ({
    ...t,
    colors: {
      primary: '#f5f5f5',
      accent: '#ff6b35',
      surface: '#1a1a1a',
      background: '#0a0a0a',
    },
  }));
}
```

```svelte
<!-- App.svelte -->
<script>
  import { theme } from './stores/theme.js';
</script>

<div
  style="
    --primary: {$theme.colors.primary};
    --accent: {$theme.colors.accent};
    --surface: {$theme.colors.surface};
    --font-display: {$theme.fonts.display};
    --font-body: {$theme.fonts.body};
  "
>
  <slot />
</div>

<style>
  div {
    color: var(--primary);
    background: var(--surface);
    font-family: var(--font-body);
  }
</style>
```

### Scroll-Triggered Animations
```svelte
<script>
  import { onViewportEnter } from 'svelte-use';

  let visible = false;
</script>

<div use:onViewportEnter={() => visible = true} class:visible>
  <h2>Appears when scrolled into view</h2>
</div>

<style>
  div {
    opacity: 0;
    transform: translateY(40px);
    transition: all 0.6s ease-out;
  }

  div.visible {
    opacity: 1;
    transform: translateY(0);
  }
</style>
```

### Accessibility Maintenance
- Keep WCAG AA color contrast minimum 4.5:1 for text
- Maintain focus visible outlines in interactive elements
- Use semantic HTML in Svelte templates
- Test with Vitest and accessibility libraries
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
- Include motion and micro-interactions with Svelte transitions
- Feature asymmetric or broken-grid layouts
- Use layered/textured backgrounds via pseudo-elements or gradients
- Maintain or improve accessibility scores
- Support light/dark theme variants
