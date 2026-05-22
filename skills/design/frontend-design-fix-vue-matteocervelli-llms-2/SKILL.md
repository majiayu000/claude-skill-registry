---
name: frontend-design-fix-vue
description: Fix generic Vue component designs by applying aesthetic upgrades across the 5 design dimensions (typography, color, motion, spatial composition, backgrounds)
version: 1.0.0
framework: Vue
category: design-system
tools: [Read, Write, Edit, Grep, Glob, Bash]
scope: project
enabled: true
---

# Frontend Design Fix - Vue

## Overview

Transform bland, generic Vue component designs into visually distinctive interfaces by systematically applying the 5 design dimensions from Anthropic's design framework.

## Core Workflow

### 1. Analysis Phase
- Read existing Vue component files (.vue, CSS modules, styles)
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
- Use scoped styles with CSS-in-JS (styled-components, emotion) or Tailwind

#### Color & Theme
- Remove default purple gradients on white backgrounds
- Introduce CSS custom properties or Vue provide/inject for theming
- Establish dominant colors with sharp accent colors
- Avoid evenly-distributed palettes (use 70-20-10 rule)
- Create theme variants (light/dark) with consistent color tokens

#### Motion
- Add orchestrated page load animations (fade, scale, slide)
- Implement staggered reveals with `v-transition` or Vue Transition Group
- Add hover state surprises and micro-interactions
- Include scroll-triggered animations via `vue-observe-visibility`
- Use `vue-motion` or `@vue/composable` for complex sequences

#### Spatial Composition
- Break centered, predictable layouts
- Add asymmetry or intentional overlap
- Introduce diagonal flow or grid-breaking elements
- Adjust spacing (generous negative space OR controlled density)
- Use CSS Grid and Flexbox creatively with Vue slots

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
- Verify accessibility compliance with Vue Testing Library

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
- [ ] No CSS custom properties or provide/inject for theming
- [ ] Evenly distributed color palette (5+ primary colors)
- [ ] No accent color for emphasis
- [ ] Insufficient contrast in interactive elements
- [ ] No dark mode support

### Motion Audit
- [ ] No page load animations or v-enter/v-leave transitions
- [ ] No staggered reveals for lists with TransitionGroup
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

### Vue 3 + Composition API + Tailwind
```vue
<template>
  <div class="
    bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900
    min-h-screen
    font-body
  ">
    <h1 class="
      font-display
      text-6xl font-black
      animate-fade-in-up
    ">
      Distinctive Title
    </h1>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isVisible = ref(false);
</script>

<style scoped>
:root {
  --font-display: 'Playfair Display', serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
  --primary: #1a1a1a;
  --accent: #ff6b35;
}

.font-display {
  font-family: var(--font-display);
}

.font-body {
  font-family: var(--font-body);
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

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out;
}
</style>
```

### Vue Transition Group for Staggered Lists
```vue
<template>
  <TransitionGroup
    tag="div"
    class="grid gap-4"
    name="stagger"
  >
    <div
      v-for="(item, index) in items"
      :key="item.id"
      :style="{ '--stagger-index': index }"
    >
      {{ item.content }}
    </div>
  </TransitionGroup>
</template>

<script setup>
import { TransitionGroup } from 'vue';

defineProps({
  items: Array,
});
</script>

<style scoped>
.stagger-enter-active,
.stagger-leave-active {
  transition: all 0.4s ease-out;
  transition-delay: calc(var(--stagger-index, 0) * 100ms);
}

.stagger-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.stagger-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
```

### Vue Provide/Inject for Theme
```vue
<!-- ThemeProvider.vue -->
<template>
  <div :style="themeStyles">
    <slot />
  </div>
</template>

<script setup>
import { provide, computed } from 'vue';

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

const themeStyles = computed(() => ({
  '--primary': theme.colors.primary,
  '--accent': theme.colors.accent,
  '--surface': theme.colors.surface,
}));

provide('theme', theme);
</script>
```

### Accessibility Maintenance
- Keep WCAG AA color contrast minimum 4.5:1 for text
- Maintain focus visible outlines in interactive elements
- Use semantic HTML with Vue components
- Test with Vue Testing Library
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
- Include motion and micro-interactions with Vue Transitions
- Feature asymmetric or broken-grid layouts
- Use layered/textured backgrounds via pseudo-elements or gradients
- Maintain or improve accessibility scores
- Support light/dark theme variants
