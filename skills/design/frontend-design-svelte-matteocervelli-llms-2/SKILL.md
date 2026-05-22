---
name: frontend-design-svelte
description: Create distinctive, production-grade Svelte/TypeScript frontends with exceptional design quality
version: 1.0.0
framework: svelte-typescript
tools: [Read, Write, Edit, Grep, Glob, Bash]
dependencies: [svelte, '@sveltejs/kit', typescript]
---

# Frontend Design Svelte Skill

## Purpose

This skill guides the creation of **distinctive, production-grade Svelte frontends** that combine Svelte's reactive elegance with exceptional design quality. It integrates all design frameworks: intentional thinking, typography, color, motion, spatial composition, and anti-pattern awareness.

## When to Use

- Building production Svelte/SvelteKit frontends
- Creating component libraries with design personality
- Designing interactions that leverage Svelte's reactivity
- Building accessible, mobile-first web applications
- Prototyping high-fidelity designs in code

## Core Principles

### 1. Design Thinking Foundation (Pre-Coding)

Before writing any code, establish intentional design direction:

**The Four Critical Questions**:
1. **Purpose**: What problem are we solving? Who are we solving it for?
2. **Tone**: What emotional response do we want? What aesthetic direction reflects this?
3. **Constraints**: What are the real technical, temporal, or business limits?
4. **Differentiation**: What one unforgettable element makes this distinctly ours?

### 2. Anti-Generic AI Design Standards

Deliberately reject these patterns:

**Typography**:
- ❌ Avoid: Inter, Roboto, Open Sans as primary choices
- ✅ Prefer: Playfair Display, Crimson Pro, Space Grotesk, IBM Plex, Bricolage Grotesque
- ✅ Use high-contrast pairings: Display + Mono, Serif + Geometric Sans
- ✅ Use size jumps of 3x+, not incremental 1.5x scaling

**Color & Theme**:
- ❌ Avoid: Material Design trinity (blue, red, green)
- ❌ Avoid: Default SaaS blue (#0099ff) everywhere
- ✅ Prefer: Intentional palettes with one unexpected accent
- ✅ Prefer: Warm or cool personality, never neutral grays

**Layout & Space**:
- ❌ Avoid: Centered, symmetrical "cookie-cutter" layouts
- ✅ Prefer: Asymmetrical compositions with intentional whitespace
- ✅ Use consistent spacing scale: 8px, 12px, 16px, 24px, 32px, 48px, 64px

**Motion**:
- ❌ Avoid: Linear timing, instantaneous interactions
- ✅ Prefer: Orchestrated animations with easing functions
- ✅ Prefer: Staggered reveals, delightful hover surprises

## Svelte-Specific Guidance

### TypeScript Setup

Always use TypeScript in Svelte components:

```svelte
<script lang="ts">
  import type { ComponentProps } from 'svelte'

  interface Props {
    title: string
    count: number
    onAction?: () => void
  }

  let { title, count, onAction }: Props = $props()
</script>
```

### Reactivity with `$:`

Leverage Svelte's reactive declarations for dynamic styling and state:

```svelte
<script lang="ts">
  let theme: 'light' | 'dark' = $state('light')
  let isHovered = $state(false)

  // Reactive computed values
  let backgroundColor = $derived(
    theme === 'light' ? 'var(--color-bg-light)' : 'var(--color-bg-dark)'
  )

  let shadowIntensity = $derived(isHovered ? '0.2' : '0.1')
</script>
```

### Scoped Styles with CSS Variables

Svelte's scoped styles are default. Use CSS custom properties for theming:

```svelte
<style>
  :global(:root) {
    --color-primary: #8b4513;
    --color-accent: #d4a574;
    --color-bg: #faf8f3;
    --font-display: 'Playfair Display', serif;
    --font-body: 'IBM Plex Sans', sans-serif;
    --spacing-unit: 8px;
  }

  .card {
    background: var(--color-bg);
    padding: calc(var(--spacing-unit) * 3);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, var(--shadow-intensity));
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .card:hover {
    --shadow-intensity: 0.15;
    transform: translateY(-4px);
  }
</style>
```

### Svelte Transitions & Animations

Use Svelte's built-in transitions for elegant animations:

```svelte
<script lang="ts">
  import { fade, fly, scale, slide } from 'svelte/transition'
  import { cubicOut, elasticOut } from 'svelte/easing'

  let isVisible = $state(true)
  let showDetails = $state(false)
</script>

<!-- Fade in on mount -->
<div in:fade={{ duration: 300 }} out:fade={{ duration: 200 }}>
  Content
</div>

<!-- Orchestrated entrance with stagger -->
<div
  in:fly={{ y: 50, duration: 600, delay: 100, easing: cubicOut }}
  out:fly={{ y: 20, duration: 300 }}
>
  Hero section
</div>

<!-- Elastic expand on interaction -->
{#if showDetails}
  <div
    in:scale={{ start: 0.95, duration: 400, easing: elasticOut }}
    out:scale={{ duration: 200 }}
  >
    Detailed content
  </div>
{/if}

<!-- Slide for list items (staggered) -->
<ul>
  {#each items as item (item.id)}
    <li
      in:slide={{ duration: 400, delay: index * 50 }}
      out:slide={{ duration: 200 }}
    >
      {item.name}
    </li>
  {/each}
</ul>
```

### Stores for Global State & Theme Management

Use Svelte stores for theme, animations, and global UI state:

```svelte
<!-- lib/stores/theme.ts -->
import { writable, derived } from 'svelte/store'

export const isDarkMode = writable(false)

export const themeVariables = derived(isDarkMode, ($isDarkMode) => ({
  bgColor: $isDarkMode ? '#1a1a1a' : '#faf8f3',
  textColor: $isDarkMode ? '#f5f5f5' : '#333333',
  accentColor: '#d4a574',
  shadows: $isDarkMode ? 'rgba(0,0,0,0.4)' : 'rgba(0,0,0,0.1)',
}))

<!-- Usage in component -->
<script lang="ts">
  import { isDarkMode, themeVariables } from '$lib/stores/theme'
</script>

<div style:background-color={$themeVariables.bgColor}>
  Content
</div>
```

### Accessibility & Semantic HTML

Svelte's approach to accessibility:

```svelte
<script lang="ts">
  let isMenuOpen = $state(false)
  let focusedIndex = $state(-1)
</script>

<!-- Semantic structure -->
<nav aria-label="Main navigation">
  <button
    aria-expanded={isMenuOpen}
    aria-controls="main-menu"
    aria-label="Toggle navigation menu"
  >
    Menu
  </button>

  <ul id="main-menu" role="menubar" hidden={!isMenuOpen}>
    {#each menuItems as item (item.id)}
      <li role="none">
        <a href={item.href} role="menuitem">
          {item.label}
        </a>
      </li>
    {/each}
  </ul>
</nav>

<!-- Form accessibility -->
<form>
  <label for="email">Email address</label>
  <input
    id="email"
    type="email"
    required
    aria-required="true"
    aria-describedby="email-hint"
  />
  <small id="email-hint">We'll never share your email.</small>
</form>
```

### Mobile-First Responsive Design

Use Svelte's class directives and media queries:

```svelte
<script lang="ts">
  let viewport: 'mobile' | 'tablet' | 'desktop' = $state('mobile')
  let windowWidth = $state(0)

  $effect(() => {
    if (windowWidth < 640) viewport = 'mobile'
    else if (windowWidth < 1024) viewport = 'tablet'
    else viewport = 'desktop'
  })
</script>

<svelte:window bind:innerWidth={windowWidth} />

<div class="container" class:is-mobile={viewport === 'mobile'}>
  <header class:is-compact={viewport === 'mobile'}>
    <!-- Mobile-optimized header -->
  </header>
</div>

<style>
  .container {
    padding: calc(var(--spacing-unit) * 4);
  }

  .container.is-mobile {
    padding: calc(var(--spacing-unit) * 2);
  }

  header.is-compact {
    font-size: 18px;
  }

  @media (min-width: 640px) {
    header {
      font-size: 24px;
    }
  }
</style>
```

## 8-Phase Development Workflow

### Phase 1: Design Thinking & Intent Definition

**Input**: Feature requirements, target users, problem statement

**Actions**:
- Answer the 4 Critical Questions (Purpose, Tone, Constraints, Differentiation)
- Define emotional intent (trustworthy, energetic, sophisticated, direct, warm, bold)
- Document design constraints (technical, temporal, business, creative)
- Identify the unforgettable element that makes this distinctly yours

**Deliverable**: Design brief with clear direction

### Phase 2: Design System & Token Definition

**Input**: Design brief and tone direction

**Actions**:
- Define typography: Display font, Body font, Monospace font
- Create color palette: Base colors, accents, semantic colors (success, error, warning)
- Establish spacing scale: 8px increments (8, 12, 16, 24, 32, 48, 64)
- Define motion easing curves and durations
- Plan component system structure

**Deliverable**: Design tokens in CSS variables and Svelte stores

```svelte
<!-- $lib/styles/tokens.css -->
:root {
  /* Typography */
  --font-display: 'Playfair Display', serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --size-display: 88px;
  --size-h1: 48px;
  --size-h2: 28px;
  --size-body: 16px;
  --size-small: 12px;

  /* Colors */
  --color-bg: #faf8f3;
  --color-text: #2a2a2a;
  --color-accent: #d4a574;
  --color-accent-dark: #8b4513;

  /* Motion */
  --easing-out: cubic-bezier(0.16, 0.04, 0.04, 1);
  --easing-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);
  --duration-quick: 200ms;
  --duration-standard: 400ms;
  --duration-slow: 600ms;
}
```

### Phase 3: Component Architecture & TypeScript Contracts

**Input**: Design tokens and feature requirements

**Actions**:
- Define component props with TypeScript interfaces
- Create component hierarchy (atoms → molecules → organisms)
- Plan state management strategy
- Define event handling patterns
- Document component accessibility requirements

**Deliverable**: Typed component structure

```svelte
<!-- lib/components/Button.svelte -->
<script lang="ts">
  import { cubicOut } from 'svelte/easing'

  interface Props {
    variant?: 'primary' | 'secondary' | 'outline'
    size?: 'small' | 'medium' | 'large'
    disabled?: boolean
    ariaLabel?: string
    onclick?: () => void
  }

  let {
    variant = 'primary',
    size = 'medium',
    disabled = false,
    ariaLabel,
    onclick,
  }: Props = $props()
</script>

<button
  class="button {variant} {size}"
  {disabled}
  aria-label={ariaLabel}
  on:click={onclick}
  in:scale={{ start: 0.95, duration: 200, easing: cubicOut }}
>
  <slot />
</button>
```

### Phase 4: Interaction & Motion Design

**Input**: Component structure and design tokens

**Actions**:
- Map Svelte transitions to design intent
- Plan orchestrated page load sequences (staggered reveals)
- Define hover/focus states with motion
- Plan scroll trigger animations
- Create state-based animations for interactions

**Deliverable**: Transition patterns and animation sequences

### Phase 5: Responsive Design & Layout System

**Input**: Component library and motion patterns

**Actions**:
- Build mobile-first CSS grid/flex layout system
- Define breakpoints and responsive behaviors
- Create viewport-aware components
- Test touch interactions on mobile
- Ensure all animations perform well on mobile devices

**Deliverable**: Responsive component library

### Phase 6: Theming & Color Implementation

**Input**: Design tokens and component library

**Actions**:
- Implement CSS variable theming system
- Create light/dark mode support (if needed)
- Apply color palette to components
- Ensure sufficient color contrast (WCAG AA minimum)
- Create dynamic theme switcher

**Deliverable**: Fully themed component system

### Phase 7: Accessibility & ARIA Implementation

**Input**: All components and interactions

**Actions**:
- Add semantic HTML structure
- Implement ARIA labels and roles
- Test keyboard navigation
- Ensure focus states are visible
- Validate against WCAG 2.1 AA standards
- Test with screen readers

**Deliverable**: Fully accessible component library

### Phase 8: Polish & Performance

**Input**: Complete feature implementation

**Actions**:
- Optimize animation performance (use `will-change`, GPU acceleration)
- Add micro-interactions and easter eggs
- Test on real devices and browsers
- Measure Core Web Vitals
- Refine motion based on performance data
- Final design review against intent

**Deliverable**: Production-ready application

## Anti-Generic-AI Checklist

Use these checks before finalizing any design or component:

**Typography**:
- [ ] YES to high-contrast font pairings (Display + Mono, Serif + Sans)
- [ ] YES to size jumps of 3x+ (88px, 48px, 28px, 16px)
- [ ] YES to weight extremes (300/700 vs 400/600)
- [ ] NO to Inter, Roboto, Open Sans as primary choice

**Color & Theme**:
- [ ] YES to intentional palette with personality
- [ ] YES to one unexpected accent color
- [ ] YES to warm or cool personality (not neutral)
- [ ] NO to Material Design trinity or default SaaS blue

**Layout & Space**:
- [ ] YES to asymmetrical compositions
- [ ] YES to generous whitespace with intent
- [ ] YES to consistent spacing scale (8px increments)
- [ ] NO to centered, symmetrical "cookie-cutter" layouts

**Motion & Animation**:
- [ ] YES to Svelte transitions for smooth animations
- [ ] YES to orchestrated/staggered reveals
- [ ] YES to easing functions (elastic, cubic-bezier)
- [ ] YES to reactive declarations for dynamic styling
- [ ] YES to scoped styles with CSS variables
- [ ] NO to linear timing or instant interactions
- [ ] NO to animation-heavy design that distracts

**Svelte-Specific**:
- [ ] YES to TypeScript in `<script lang="ts">`
- [ ] YES to reactive declarations with `$:`
- [ ] YES to scoped styles with CSS variables
- [ ] YES to Svelte transitions for elegant motion
- [ ] YES to stores for global state and theme
- [ ] YES to semantic HTML and ARIA attributes

## Example Component Patterns

### Animated Card with Hover Delight

```svelte
<script lang="ts">
  import { fly, scale } from 'svelte/transition'
  import { cubicOut, elasticOut } from 'svelte/easing'

  let isHovered = $state(false)

  interface Props {
    title: string
    description: string
    image?: string
  }

  let { title, description, image }: Props = $props()
</script>

<article
  in:fly={{ y: 40, duration: 500, easing: cubicOut }}
  class="card"
  on:mouseenter={() => (isHovered = true)}
  on:mouseleave={() => (isHovered = false)}
>
  {#if image}
    <img src={image} alt="" class="card-image" />
  {/if}

  <div class="card-content">
    <h3>{title}</h3>
    <p>{description}</p>

    {#if isHovered}
      <button
        in:scale={{ start: 0.8, duration: 300, easing: elasticOut }}
        class="card-action"
      >
        Learn More
      </button>
    {/if}
  </div>
</article>

<style>
  .card {
    background: var(--color-bg);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
  }

  .card:hover {
    transform: translateY(-12px);
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.15);
  }

  .card-image {
    width: 100%;
    height: 240px;
    object-fit: cover;
  }

  .card-content {
    padding: calc(var(--spacing-unit) * 3);
  }

  h3 {
    font-family: var(--font-display);
    font-size: var(--size-h2);
    font-weight: 700;
    margin: 0 0 calc(var(--spacing-unit) * 2) 0;
    color: var(--color-text);
  }

  p {
    font-family: var(--font-body);
    font-size: var(--size-body);
    line-height: 1.6;
    color: rgba(0, 0, 0, 0.7);
    margin: 0;
  }

  .card-action {
    margin-top: calc(var(--spacing-unit) * 2);
    padding: calc(var(--spacing-unit) * 1.5) calc(var(--spacing-unit) * 3);
    background: var(--color-accent);
    color: white;
    border: none;
    border-radius: 6px;
    font-family: var(--font-body);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease-out;
  }

  .card-action:hover {
    background: var(--color-accent-dark);
    transform: scale(1.05);
  }
</style>
```

### Staggered List Animation

```svelte
<script lang="ts">
  import { slide } from 'svelte/transition'
  import { cubicOut } from 'svelte/easing'

  interface ListItem {
    id: string
    label: string
  }

  interface Props {
    items: ListItem[]
  }

  let { items }: Props = $props()
</script>

<ul class="list">
  {#each items as item, index (item.id)}
    <li
      in:slide={{
        duration: 400,
        delay: index * 50,
        easing: cubicOut,
      }}
      out:slide={{ duration: 200 }}
    >
      <span class="list-number">{index + 1}</span>
      <span class="list-label">{item.label}</span>
    </li>
  {/each}
</ul>

<style>
  .list {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  li {
    display: flex;
    align-items: center;
    padding: calc(var(--spacing-unit) * 2) calc(var(--spacing-unit) * 3);
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease-out;
  }

  li:hover {
    background-color: rgba(0, 0, 0, 0.02);
  }

  .list-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    margin-right: calc(var(--spacing-unit) * 2);
    background: var(--color-accent);
    color: white;
    border-radius: 50%;
    font-weight: 600;
    font-size: 13px;
  }

  .list-label {
    font-family: var(--font-body);
    font-size: var(--size-body);
    color: var(--color-text);
  }
</style>
```

## Svelte-Specific Best Practices

1. **Type Safety**: Always use TypeScript in component scripts
2. **Reactivity**: Leverage `$derived` for computed values and `$effect` for side effects
3. **Transitions**: Use built-in `svelte/transition` for all animations
4. **Scoped Styles**: Rely on Svelte's default scoped styling; use `:global()` sparingly
5. **CSS Variables**: Store design tokens as CSS variables for dynamic theming
6. **Stores**: Use `writable` for theme, animation state, and global UI state
7. **Accessibility**: Always include semantic HTML, ARIA labels, and proper focus management
8. **Performance**: Use `bind:` carefully, memoize expensive computations with `$derived`

## Resources & References

- **Svelte Documentation**: https://svelte.dev
- **SvelteKit**: https://kit.svelte.dev
- **Design System Prompts**: See design-thinking.md, aesthetics-base.md, motion.md, typography.md, anti-patterns.md
- **WCAG 2.1 Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/

---

**Ready to build distinctive, intentional Svelte frontends?** Start with Phase 1: Design Thinking & Intent Definition. Never skip the pre-coding work.
