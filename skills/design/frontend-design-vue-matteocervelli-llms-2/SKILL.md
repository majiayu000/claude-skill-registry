---
name: frontend-design-vue
description: Create distinctive, production-grade Vue 3/TypeScript frontends with exceptional design quality
version: 1.0.0
framework: vue3-typescript
tools: [Read, Write, Edit, Grep, Glob, Bash]
dependencies: [vue, @vue/compiler-sfc, @vueuse/motion, typescript, vite]
---

# Frontend Design Vue Skill

Create distinctive, production-grade Vue 3 frontends with TypeScript and exceptional design quality. This skill integrates the complete design system framework with Vue 3/TypeScript implementation patterns.

## Overview

This skill enables you to build Vue 3 applications that avoid generic AI design patterns through:
- Intentional typography, color, and motion choices
- Production-grade Vue 3 + TypeScript architecture
- Vue Use Motion animations for orchestrated interactions
- Scoped styles with CSS variables for theme management
- Accessibility-first semantic HTML and ARIA
- Mobile-first responsive design

## Core Design Framework

### Base Aesthetics Framework

The core 5-dimension framework for creating intentional, non-generic design that avoids the homogenized aesthetic of default AI outputs.

#### 1. Typography Dimension

**Purpose**: Typography is the primary carrier of voice and personality in digital design.

**Core Principles**:
- Typeface selection creates immediate emotional context
- Font pairings establish visual hierarchy and rhythm
- Weight and size extremes create contrast and emphasis
- Avoid: Inter, Roboto, Open Sans, Lato, system fonts (these are default AI outputs)
- Prefer: JetBrains Mono, Fira Code, Space Grotesk, Playfair Display, Crimson Pro, IBM Plex, Bricolage Grotesque

**Implementation**:
- Use high-contrast pairings: Display + Mono, Serif + Geometric Sans
- Employ weight extremes: 100/200 vs 800/900 (not mid-range weights)
- Apply size jumps of 3x or more, not incremental 1.5x steps
- Create visual hierarchy through deliberate typographic choices

**Example Pattern**:
- Display: Playfair Display (300, 400, 700)
- Body: IBM Plex Sans (400, 600)
- Mono: JetBrains Mono (400, 500)

#### 2. Color & Theme Dimension

**Purpose**: Color sets mood and creates visual coherence while avoiding cliché palettes.

**Core Principles**:
- Move beyond default color systems (Material Design, Tailwind defaults)
- Use unexpected but harmonious color relationships
- Consider context: what emotional response do you want?
- Saturation and tone matter as much as hue

**Anti-Patterns to Avoid**:
- Primaries: Blue, Red, Green (default AI trinity)
- Neutrals: Pure grays (#999999, #CCCCCC) without personality
- Monochrome gradients that feel soulless
- Color palettes that match "flat design" clichés

**Implementation**:
- Define color intent: Is this a warm, cool, energetic, or calm system?
- Use color psychology intentionally
- Create contrast through saturation, not just hue
- Reserve one unexpected accent color for personality

**Example Approach**:
- Warm palette: Cognac browns, terracotta, warm neutrals with olive undertones
- Cool palette: Deep indigos, soft teals, cool grays with blue undertones
- Accent: Single unexpected color for UI elements (e.g., sulfur yellow, coral pink)

#### 3. Motion Dimension

**Purpose**: Motion reveals personality and guides user attention with intentionality.

**Core Principles**:
- Motion should feel deliberate, not random
- Orchestrate page loads with staggered timing
- Use scroll triggers for engaged scrolling experiences
- Hover states should surprise, not just respond

**Implementation**:
- **Vue: @vueuse/motion** for orchestrated, state-driven animation
- Page load: Stagger reveals with animation-delay (100ms, 200ms, 300ms)
- Scroll triggers: Elements animate in when viewport enters
- Hover: Add transforms, color shifts, or subtle scale changes

**Anti-Patterns**:
- Linear timing on everything (feels robotic)
- Instantaneous interactions (feels cold)
- Animation-heavy design that distracts from content

#### 4. Spatial Composition Dimension

**Purpose**: Space and layout create rhythm and guide the eye through intentional composition.

**Core Principles**:
- Use asymmetrical layouts when possible (more interesting than grid-perfect)
- Create breathing room with generous whitespace
- Build visual rhythm through consistent spacing systems
- Avoid centered, symmetrical layouts unless purposeful

**Implementation**:
- Define a spacing scale: 8px, 12px, 16px, 24px, 32px, 48px, 64px
- Use odd-numbered layouts: 3-column, 5-item, 7-section
- Create focal points through compositional weight
- Consider micro-interactions within spatial relationships

**Anti-Patterns**:
- Everything centered (feels safe but predictable)
- Uniform padding everywhere
- Layouts that could describe "generic SaaS dashboard"

#### 5. Backgrounds & Visual Details Dimension

**Purpose**: The foundation layer that can transform a generic design into something memorable.

**Core Principles**:
- Background should support, not distract
- Add subtle details that reward close observation
- Use gradients intentionally, not as default effects
- Create texture through digital or illustrated means

**Implementation**:
- Subtle gradients: Use 2-3 colors with minimal contrast (40-60° angles)
- Illustrated patterns: Geometric, organic, or custom SVG elements
- Texture overlays: Subtle noise or grain (2-5% opacity)
- Micro-illustrations: Small graphics that reinforce brand voice

**Anti-Patterns**:
- Bland white backgrounds (consider soft colors instead)
- Obvious gradients (rainbow, neon contrasts)
- Busy patterns that compete with content
- Decorative elements that serve no purpose

### Typography Guidance

Typography is the primary carrier of personality and voice in design.

**Typefaces to Avoid**:
- Inter: Google's modern sans-serif, used everywhere in AI-generated design
- Roboto: Android's default, synonymous with generic design
- Open Sans: Neutral and safe, but overused
- Lato: Round and friendly, but lacks personality
- System fonts: Default OS fonts (SF Pro Display, Segoe UI) feel lazy

If you use any of these, pair them with something unexpected and deliberately break the generic pattern.

**Typefaces to Prefer**:

Display & Decorative:
- Playfair Display: Elegant serif, high contrast, sophisticated
- Bricolage Grotesque: Modern sans with personality, handcrafted feel
- Space Grotesk: Geometric sans with character, works for display or body
- Crimson Pro: High-contrast serif, literary and elegant

Body & Copy:
- IBM Plex Sans: Humanist sans with warmth, works at all sizes
- Space Grotesk: Geometric sans that reads well in small sizes
- Crimson Pro: Serif for long-form content, distinctive personality

Monospace (Technical, Quotes, Code):
- JetBrains Mono: Designed for code, readable and stylish
- Fira Code: Open source, ligatures for programming
- IBM Plex Mono: Humanist monospace, readable at any size

**Pairing Strategy**:

High-Contrast Pairings (Recommended):

Pattern 1: Display + Mono
```
Headline: Playfair Display (elegant serif)
Body: JetBrains Mono (technical monospace)
Result: Sophisticated + Modern
```

Pattern 2: Serif + Geometric Sans
```
Headline: Crimson Pro (high-contrast serif)
Body: Space Grotesk (geometric sans)
Result: Elegant + Contemporary
```

Pattern 3: Decorative + Humanist
```
Headline: Bricolage Grotesque (handcrafted sans)
Body: IBM Plex Sans (warm humanist sans)
Result: Crafted + Approachable
```

**Font Weights & Extremes**:

Use weight extremes to create contrast, not mid-range weights:

Good:
- Display: 300 (thin) or 700/800 (heavy)
- Body: 400 (regular) or 600 (semi-bold)
- Emphasis: 800/900 for strong hierarchy

Avoid:
- Middle weights everywhere (400, 500, 500) feels muddled
- Limited weight range (only 400, 500, 600) lacks contrast
- No visual distinction between hierarchy levels

**Size Jumps: Extreme Over Incremental**:

Use 3x+ jumps between hierarchy levels, not incremental 1.5x steps:

Generic (Linear Scaling):
```
H1: 48px
H2: 36px (75% of H1)
H3: 28px (78% of H2)
Body: 16px
Small: 14px
```
Result: Feels predictable, every size feels similar distance apart.

Intentional (3x+ Jumps):
```
Display: 96px (3x body)
Headline: 48px (3x body)
Sub-headline: 28px (1.75x body)
Body: 16px
Caption: 12px (0.75x body)
```
Result: Creates clear visual hierarchy, extreme sizes make smaller sizes feel intentional.

**Line Height & Letter Spacing**:

Line Height Strategy:
- Display (90px+): 1.0-1.1 (tight, confident)
- Headline (40px+): 1.1-1.2 (tight)
- Sub-headline (24px+): 1.2-1.3 (moderate)
- Body (14px-20px): 1.4-1.6 (loose for readability)
- Small text (<14px): 1.5-1.7 (extra loose for clarity)

Letter Spacing Strategy:
- Display (90px+): -0.5 to -1px (negative space tightens)
- Headline (40px+): -0.25px (subtle tightening)
- Body: 0px (default)
- Emphasis/Caps: +0.5px to +1px (opens up all-caps)

### Motion & Animation Guidance

Motion reveals personality and guides user attention with intentionality.

**Core Principles**:
1. Orchestration: Animations should feel planned, not random
2. Purpose: Every animation should serve a functional or emotional purpose
3. Timing: Easing functions matter more than duration
4. Context: Page loads, scrolls, and hovers each have different animation strategies

**Vue Use Motion Implementation**:

@vueuse/motion provides excellent Vue 3 integration for orchestrated animations:

```typescript
import { useMotion } from '@vueuse/motion'
import { ref } from 'vue'

const target = ref()

useMotion(target, {
  initial: { opacity: 0, y: 100 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 100,
      delay: 100
    }
  }
})
```

**Page Load Animation Strategy**:

Orchestrated Reveal - Don't animate everything at once. Create a sequence that guides the user's eye:

Timing Sequence:
```
0ms    - Background/Hero fades in
200ms  - Headline slides in from top
400ms  - Sub-headline fades in
600ms  - Primary CTA appears
800ms  - Supporting content staggered reveal
```

**Staggered Reveals**:

Using staggerChildren with @vueuse/motion:

```typescript
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
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { duration: 0.6 },
  },
};
```

**Scroll Trigger Animations**:

Using Intersection Observer with Vue:

```typescript
import { ref, onMounted } from 'vue'

const elementRef = ref()

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
        observer.unobserve(entry.target)
      }
    })
  })

  if (elementRef.value) {
    observer.observe(elementRef.value)
  }
})
```

**Hover State Surprises**:

Hover interactions should be delightful, not just functional:

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref } from 'vue'

const card = ref()

useMotion(card, {
  initial: { y: 0 },
  hover: {
    y: -8,
    transition: {
      type: 'spring',
      stiffness: 200,
      damping: 20
    }
  }
})
</script>

<template>
  <div ref="card" class="card">
    <!-- Content -->
  </div>
</template>
```

**Easing Functions**:

Recommended Easing Values:
- ease-out: 0.16, 0.04, 0.04, 1 (default snappy)
- ease-in-out: 0.42, 0, 0.58, 1 (smooth, balanced)
- elastic: cubic-bezier(0.34, 1.56, 0.64, 1) (playful overshoot)
- sharp: cubic-bezier(0.4, 0, 0.6, 1) (quick and direct)

**Anti-Patterns to Avoid**:
- Linear timing: Feels robotic, use easing instead
- Instant interactions: Feels cold, add 0.2-0.4s minimum transitions
- Animation-heavy: Don't animate everything; be selective
- Slow animations: >1s feels sluggish unless intentional
- Predictable patterns: Vary easing, duration, and delay

### Anti-Patterns: What to Avoid

These are the predictable defaults that appear in generic AI-generated design.

**Typography Anti-Patterns**:
- Generic Font Choices: Inter, Roboto, Open Sans, Lato everywhere
- Incremental Size Jumps: H1 48px, H2 40px, H3 32px (feels too close)
- Mid-Range Font Weights Only: Using 400, 500, 600 (all feel samey)

**Color & Theme Anti-Patterns**:
- Cliché Color Schemes: Material Design Trinity (Blue, Red, Green)
- Default SaaS Colors: Cool blues everywhere
- Monochrome Everything: Just grays and blues
- Oversaturated Accent Colors: Neon at 100% saturation
- Predictable "Dark Mode": Just inverted black/white

**Layout & Spatial Anti-Patterns**:
- Cookie-Cutter Centered Layout: Everything centered and symmetrical
- Uniform Padding Everywhere: Same spacing on all elements
- Predictable Component Patterns: Card with image on top (default)

**Motion & Animation Anti-Patterns**:
- Linear Timing: Feels robotic and mechanical
- No Animation at All: Instant page loads (feels cold)
- Animation-Heavy Design: Animating every element
- Slow, Sluggish Motion: >1s transitions feel like the app is struggling

**Background & Visual Details Anti-Patterns**:
- Bland White Background: Pure white with no texture
- Obvious Gradients: Rainbow gradients or high-contrast (0% to 100%)
- Busy, Distracting Patterns: High contrast or competing with content
- Generic Illustration Style: Adobe Illustrator defaults or 3D isometric cubes

**Checklist: Have You Avoided These?**:
- [ ] Rejected Inter, Roboto, Open Sans as primary fonts?
- [ ] Chosen typefaces with personality and intention?
- [ ] Used size jumps of 3x+, not incremental scaling?
- [ ] Avoided Material Design color trinity?
- [ ] Created custom color palette with personality?
- [ ] Rejected centered, symmetrical layouts?
- [ ] Used easing functions, not linear timing?
- [ ] Added motion that serves a purpose?
- [ ] Avoided generic gradients and patterns?
- [ ] Would you describe this as "generic" or "intentional"?

### Design Thinking: Pre-Coding Workflow

Before writing code or generating design, establish the intentional foundation.

**The Pre-Design Checklist**:

Don't design until you answer these four questions:
1. Purpose: What problem are we solving? Who are we solving it for?
2. Tone: What emotional response do we want? What aesthetic direction reflects this?
3. Constraints: What are the real technical, temporal, or business limits?
4. Differentiation: What one unforgettable element makes this distinctly ours?

**Purpose: Problem & Users**:

Before choosing any visual element, define what you're solving:
- What specific problem does this design solve?
- Who are the primary users? (age, technical skill, context)
- What emotions are they bringing to this interface? (frustrated, excited, skeptical)
- What's the desired outcome after interaction?
- What makes this problem unique vs. competitors?

**Tone: Emotional Intent**:

Based on your purpose, what emotional response should the design evoke?

Emotional Directions:
- Trustworthy: Professional, calm, reliable (finance, healthcare)
- Energetic: Playful, bold, surprising (creator tools, social)
- Sophisticated: Elegant, refined, literary (luxury, editorial)
- Direct: Minimal, fast, no-nonsense (productivity tools)
- Warm: Inviting, personable, human (community, education)
- Bold: Confident, unconventional, statement-making (startups, innovation)

**Constraints: Reality Check**:

Before designing, know your boundaries:
- Technical: Browser support, performance budget, framework limitations
- Temporal: How long do you have to build?
- Business: Brand guidelines, compliance requirements, market positioning
- Creative: Audience expectations, competitive landscape

**Differentiation: The Unforgettable Element**:

Every intentional design has one element that makes it memorable and distinctly yours.

Types of Differentiation:
1. Typography Signature: Distinctive typeface pairing or unusual hierarchy
2. Color Signature: Unexpected color choice in an expected place
3. Motion Signature: Particular animation pattern no one else uses
4. Layout/Composition Signature: Unusual spatial arrangement
5. Micro-interaction Signature: Delight that appears on interaction
6. Visual Detail Signature: Illustration style or specific visual treatment

## Vue 3 Implementation Patterns

### Composition API with TypeScript

Always use Composition API with `<script setup>` and TypeScript for type safety and clarity:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  title: string
  items: string[]
}

const props = withDefaults(defineProps<Props>(), {
  items: () => []
})

const count = ref<number>(0)

const doubled = computed<number>(() => count.value * 2)

const increment = (): void => {
  count.value++
}
</script>

<template>
  <div class="container">
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
    <p>Doubled: {{ doubled }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<style scoped>
/* Scoped styles with CSS variables */
</style>
```

### Single File Components (.vue)

All Vue components should be Single File Components with semantic structure:

```vue
<script setup lang="ts">
// 1. Imports
// 2. Types & Interfaces
// 3. Props & Emits
// 4. State (ref, reactive)
// 5. Computed Properties
// 6. Methods
// 7. Watchers
// 8. Lifecycle Hooks
</script>

<template>
  <!-- Semantic HTML with proper ARIA -->
</template>

<style scoped>
/* Scoped styles, CSS variables for theming */
</style>
```

### Vue Use Motion for Animations

@vueuse/motion provides composable animations that integrate seamlessly with Vue 3:

```vue
<script setup lang="ts">
import { useMotion } from '@vueuse/motion'
import { ref } from 'vue'

const target = ref()

useMotion(target, {
  initial: { opacity: 0, y: 100 },
  enter: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 100,
      delay: 100
    }
  }
})
</script>

<template>
  <div ref="target" class="animated-element">
    Content animates in on mount
  </div>
</template>

<style scoped>
.animated-element {
  will-change: opacity, transform;
}
</style>
```

### Scoped Styles with CSS Variables

Use CSS variables for theme management and avoid style leakage:

```vue
<style scoped>
:root {
  --color-primary: #ff6b35;
  --color-text: #1a1a1a;
  --color-background: #fffbf7;
  --spacing-base: 16px;
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
}

.component {
  color: var(--color-text);
  background: var(--color-background);
  padding: var(--spacing-base);
  font-family: var(--font-body);
}

.heading {
  font-family: var(--font-display);
  color: var(--color-primary);
}
</style>
```

### Reactive Design with ref() and reactive()

Use ref() for primitives and objects, reactive() sparingly for deeply nested objects:

```typescript
import { ref, reactive } from 'vue'

// For primitives and shallow objects
const count = ref<number>(0)
const name = ref<string>('Vue')
const user = ref<{ id: number; name: string }>({ id: 1, name: 'John' })

// Accessing values in script
count.value++

// For complex nested objects (use sparingly)
const state = reactive({
  nested: {
    deeply: {
      value: 'hello'
    }
  }
})

// No .value needed with reactive
state.nested.deeply.value = 'world'
```

### Provide/Inject for Theme Management

Use Provide/Inject to pass theme configuration down the component tree:

```vue
<!-- App.vue -->
<script setup lang="ts">
import { provide } from 'vue'

interface Theme {
  primaryColor: string
  secondaryColor: string
  fontSize: number
}

const theme: Theme = {
  primaryColor: '#ff6b35',
  secondaryColor: '#004e89',
  fontSize: 16
}

provide('theme', theme)
</script>

<!-- Child Component -->
<script setup lang="ts">
import { inject, computed } from 'vue'

interface Theme {
  primaryColor: string
  secondaryColor: string
  fontSize: number
}

const theme = inject<Theme>('theme')!

const styles = computed(() => ({
  color: theme.primaryColor,
  fontSize: theme.fontSize + 'px'
}))
</script>
```

### Accessibility with ARIA & Semantic HTML

Always use semantic HTML and proper ARIA attributes:

```vue
<template>
  <nav class="navbar" role="navigation" aria-label="Main navigation">
    <button
      class="menu-toggle"
      type="button"
      aria-label="Toggle menu"
      :aria-expanded="menuOpen"
      @click="menuOpen = !menuOpen"
    >
      ☰
    </button>
  </nav>

  <main id="main-content" role="main">
    <h1>Page Title</h1>

    <form @submit.prevent="handleSubmit">
      <label for="email-input">Email Address</label>
      <input
        id="email-input"
        v-model="email"
        type="email"
        placeholder="you@example.com"
        aria-required="true"
        aria-describedby="email-help"
      >
      <p id="email-help" class="help-text">We'll never share your email.</p>
    </form>

    <section aria-labelledby="features-heading">
      <h2 id="features-heading">Features</h2>
      <!-- Content -->
    </section>
  </main>
</template>
```

### Mobile-First Responsive Design

Always start with mobile styles and enhance for larger screens:

```vue
<style scoped>
.container {
  /* Mobile: default 1 column */
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-base);
  padding: var(--spacing-base);
}

/* Small devices (tablets) */
@media (min-width: 640px) {
  .container {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Medium devices (desktops) */
@media (min-width: 1024px) {
  .container {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Large devices */
@media (min-width: 1280px) {
  .container {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
```

## Workflow: 8-Phase Implementation

Follow these phases for consistent, intentional frontend development:

### Phase 1: Design Thinking & Strategy

- [ ] Answer the 4 pre-design questions (Purpose, Tone, Constraints, Differentiation)
- [ ] Define target users and their context
- [ ] Establish emotional intent and visual direction
- [ ] Document technical and business constraints
- [ ] Identify the one unforgettable design element

### Phase 2: Typography System

- [ ] Select 2-3 typefaces (avoid defaults like Inter/Roboto)
- [ ] Define size scale with 3x+ jumps, not incremental steps
- [ ] Set font weight extremes (300-900, avoid mid-range only)
- [ ] Create CSS custom properties for all typographic values
- [ ] Test readability at all sizes (mobile, tablet, desktop)

### Phase 3: Color System & Theme

- [ ] Define color intent (warm, cool, energetic, calm)
- [ ] Create palette with primary, secondary, accent colors
- [ ] Reserve one unexpected accent color for personality
- [ ] Implement CSS variables for all colors
- [ ] Define light/dark mode with intentional adjustments (not just inversion)

### Phase 4: Spacing & Layout

- [ ] Define spacing scale (8px, 12px, 16px, 24px, 32px, 48px, 64px)
- [ ] Create asymmetrical, non-centered layouts
- [ ] Implement responsive grid system (mobile-first)
- [ ] Test whitespace and breathing room
- [ ] Define focus and visual hierarchy through space

### Phase 5: Motion & Animation Strategy

- [ ] Plan page load animation sequence (0ms → 800ms+)
- [ ] Design staggered reveals for lists/grids
- [ ] Create hover state surprises (not just scale 1.05)
- [ ] Implement scroll trigger animations
- [ ] Use easing functions (avoid linear), 0.4-0.8s durations

### Phase 6: Component Architecture

- [ ] Build reusable components with Composition API
- [ ] Use TypeScript for full type safety
- [ ] Implement Provide/Inject for theme management
- [ ] Create design tokens as Vue composables
- [ ] Document component APIs and usage examples

### Phase 7: Accessibility & Semantics

- [ ] Use semantic HTML (nav, main, section, article, etc.)
- [ ] Add proper ARIA attributes (aria-label, aria-expanded, etc.)
- [ ] Test keyboard navigation (Tab, Enter, Escape)
- [ ] Validate contrast ratios (WCAG AA minimum 4.5:1)
- [ ] Test with screen readers

### Phase 8: Polish & Performance

- [ ] Optimize animations with will-change and transform
- [ ] Verify performance (Lighthouse score 90+)
- [ ] Test across devices and browsers
- [ ] Create comprehensive component showcase/storybook
- [ ] Document design decisions and rationale

## Anti-Generic-AI Checklist

Use this checklist to ensure your Vue design is intentional, not defaulted:

### Vue 3-Specific
- [ ] YES to Composition API with `<script setup>`
- [ ] YES to @vueuse/motion for orchestrated animations
- [ ] YES to scoped styles with CSS variables
- [ ] YES to TypeScript with full type safety
- [ ] NO to inline styles or untyped data

### Typography
- [ ] Rejected Inter, Roboto, Open Sans as primary?
- [ ] Chosen typefaces with personality and intention?
- [ ] Used size jumps of 3x+, not incremental scaling?
- [ ] Font weights span full range (300-900)?
- [ ] Would you describe typography as "distinctive" or "generic"?

### Color
- [ ] Avoided Material Design color trinity?
- [ ] Created custom palette with personality?
- [ ] Is there one unexpected accent color?
- [ ] Intentional light/dark mode (not just inversion)?
- [ ] Could this palette exist in Material Design?

### Motion
- [ ] Animations orchestrated (staggered) or simultaneous?
- [ ] Easing functions used (not linear)?
- [ ] At least one delightful hover surprise?
- [ ] Durations 0.4-0.8s (snappy, not sluggish)?
- [ ] Animation serving design, not competing?

### Layout
- [ ] Asymmetrical or centered for purpose?
- [ ] Generous whitespace or cramped?
- [ ] Could layout be described as "generic SaaS"?
- [ ] Mobile-first responsive design?
- [ ] Visual hierarchy through space?

### Accessibility
- [ ] Semantic HTML throughout?
- [ ] ARIA attributes for interactive elements?
- [ ] Keyboard navigation fully supported?
- [ ] Contrast ratios WCAG AA or better?
- [ ] Tested with actual screen readers?

## Examples

See the `examples/` directory for complete Vue component examples demonstrating:
1. Hero section with orchestrated animations
2. Feature card grid with hover surprises
3. Form with motion-enhanced interactions
4. Navigation with theme management
5. Scroll-triggered reveals

## Resources

- Vue 3 Documentation: https://vuejs.org
- @vueuse/motion: https://motion.vueuse.org
- TypeScript Handbook: https://www.typescriptlang.org/docs/
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Easing functions: https://easings.net/
