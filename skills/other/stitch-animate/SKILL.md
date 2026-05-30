---
name: stitch-animate
description: Adds a purposeful animation layer to Stitch-generated components — CSS transitions, Framer Motion (React/Next.js), or Svelte transitions. Always respects prefers-reduced-motion.
allowed-tools:
  - "Read"
  - "Write"
  - "Bash"
---

# Stitch Animation Layer

You are a motion design engineer. You add purposeful animation to existing Stitch-generated components — you don't rebuild them. Your output enhances components with the right motion for the right moment, and is always `prefers-reduced-motion` safe.

**Run this skill AFTER** component generation (`stitch-nextjs-components` or `stitch-svelte-components`), not before.

## When to use this skill

Use this skill when:
- Components are generated and working, but feel static
- User mentions "animations", "transitions", "motion", "hover effects", "scroll reveal"
- The Stitch design screenshot clearly shows motion intent (overlapping elements, hero sections, dashboards)
- Adding polish to a completed component set

## The three motion tiers

Analyze the design first. Assign animations by tier — don't animate everything:

| Tier | What | Duration | Easing | Examples |
|------|------|----------|--------|---------|
| **Micro** | Hover, focus, active states on interactive elements | 100–200ms | ease-out | Button hover, link color, icon scale |
| **Meso** | UI elements entering or leaving the viewport | 250–400ms | cubic-bezier(0,0,0.2,1) | Card reveals, sidebar slide, modal open |
| **Macro** | Full page or section transitions | 400–600ms | ease-in-out | Route transitions, hero section, onboarding |

**Rule of thumb:** If in doubt, use Micro. Over-animation is worse than no animation.

## Step 1: Audit the components

Read the generated component files. For each one, identify:

1. **Interactive elements** that need Micro tier (buttons, links, inputs, toggles, cards with `onClick`)
2. **Revealed elements** that benefit from Meso tier (page sections, cards grids, sidebars, modals, drawers, toasts)
3. **Hero or landmark elements** that warrant Macro tier (the primary headline, featured images, page-level transitions)

Only animate elements that have clear purpose. If you can't explain in one sentence *why* an element animates, don't animate it.

## Step 2: Detect the framework and choose the animation approach

Read `package.json` to determine the framework, then use the matching approach:

| Framework | Approach |
|-----------|---------|
| Next.js / React | CSS + optionally Framer Motion |
| SvelteKit / Svelte | Built-in Svelte transitions + CSS |
| Vanilla HTML | CSS only |

---

## Approach A: CSS transitions and animations (universal)

Use CSS for Micro tier and simple Meso. Zero dependencies.

### Micro tier — interactive states

Add these to `design-tokens.css` or the component's CSS:
```css
/* Base transition shorthand — use on all interactive elements */
.transition-base {
  transition:
    background-color var(--motion-duration-fast) var(--motion-ease-default),
    color var(--motion-duration-fast) var(--motion-ease-default),
    border-color var(--motion-duration-fast) var(--motion-ease-default),
    box-shadow var(--motion-duration-fast) var(--motion-ease-default),
    transform var(--motion-duration-fast) var(--motion-ease-default),
    opacity var(--motion-duration-fast) var(--motion-ease-default);
}

/* Button micro-interaction */
.btn {
  transition: transform 150ms ease-out, box-shadow 150ms ease-out, background-color 150ms ease-out;
}
.btn:hover { transform: translateY(-1px); box-shadow: var(--shadow-md); }
.btn:active { transform: translateY(0); box-shadow: var(--shadow-sm); }

/* Card lift */
.card {
  transition: transform 200ms ease-out, box-shadow 200ms ease-out;
}
.card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); }
```

### Meso tier — element reveal

Use keyframe animations with `animation-fill-mode: both`:
```css
@keyframes fade-up {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@keyframes slide-in-right {
  from { opacity: 0; transform: translateX(24px); }
  to   { opacity: 1; transform: translateX(0); }
}

.animate-fade-up    { animation: fade-up    var(--motion-duration-base) var(--motion-ease-out) both; }
.animate-fade-in    { animation: fade-in    var(--motion-duration-fast) var(--motion-ease-out) both; }
.animate-slide-in-r { animation: slide-in-right var(--motion-duration-base) var(--motion-ease-out) both; }

/* Stagger children with CSS custom property */
.stagger-children > * {
  animation-delay: calc(var(--stagger-index, 0) * 60ms);
}
```

### prefers-reduced-motion (REQUIRED)

Always add this override at the end of every animation CSS block:
```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## Approach B: Framer Motion (React / Next.js)

Use Framer Motion for Meso and Macro tier in React projects. It handles `prefers-reduced-motion` natively via `useReducedMotion`.

### Installation
```bash
npm install framer-motion
```

### Scroll-triggered reveals (most common use case)

```tsx
'use client'

import { motion, useReducedMotion } from 'framer-motion'

/**
 * Wraps children in a scroll-triggered fade+rise animation.
 * Automatically disables animation when prefers-reduced-motion is active.
 */
export function RevealOnScroll({ children, delay = 0 }: {
  children: React.ReactNode
  delay?: number
}) {
  const shouldReduce = useReducedMotion()

  return (
    <motion.div
      initial={shouldReduce ? false : { opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-50px' }}
      transition={{
        duration: 0.4,
        ease: [0, 0, 0.2, 1],
        delay,
      }}
    >
      {children}
    </motion.div>
  )
}
```

### Staggered card grid

```tsx
'use client'

import { motion, useReducedMotion } from 'framer-motion'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 }
  }
}

const item = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { ease: [0, 0, 0.2, 1], duration: 0.35 } }
}

export function AnimatedGrid({ cards }: { cards: CardProps[] }) {
  const shouldReduce = useReducedMotion()

  if (shouldReduce) {
    return <div className="grid">{cards.map(c => <Card key={c.id} {...c} />)}</div>
  }

  return (
    <motion.div className="grid" variants={container} initial="hidden" whileInView="show" viewport={{ once: true }}>
      {cards.map(c => (
        <motion.div key={c.id} variants={item}>
          <Card {...c} />
        </motion.div>
      ))}
    </motion.div>
  )
}
```

### Page transition wrapper (App Router)

```tsx
// app/template.tsx — wraps every page with a transition
'use client'

import { motion } from 'framer-motion'

export default function Template({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      {children}
    </motion.div>
  )
}
```

---

## Approach C: Svelte transitions (Svelte / SvelteKit)

Svelte's built-in transitions are the cleanest option for Svelte projects — zero dependencies.

### Intersection Observer for scroll reveals

Svelte doesn't have a built-in scroll reveal, but the `use:` directive makes this clean:

```svelte
<script lang="ts">
  import { fade, fly } from 'svelte/transition'
  import { cubicOut } from 'svelte/easing'

  /**
   * Svelte action that triggers a fade-up animation when the element
   * enters the viewport. Respects prefers-reduced-motion.
   */
  function revealOnScroll(node: HTMLElement) {
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches

    if (prefersReduced) return {}

    node.style.opacity = '0'
    node.style.transform = 'translateY(16px)'

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          node.style.transition = `opacity 400ms cubic-bezier(0,0,0.2,1), transform 400ms cubic-bezier(0,0,0.2,1)`
          node.style.opacity = '1'
          node.style.transform = 'translateY(0)'
          observer.unobserve(node)
        }
      },
      { threshold: 0.1, rootMargin: '-50px' }
    )
    observer.observe(node)

    return {
      destroy() { observer.disconnect() }
    }
  }
</script>

<!-- Use on any element -->
<section use:revealOnScroll>
  <h2>This section fades in on scroll</h2>
</section>
```

### Animated list entries

```svelte
<script lang="ts">
  import { fly } from 'svelte/transition'
  import { quintOut } from 'svelte/easing'

  let items = $state<Item[]>([...])
</script>

{#each items as item, i (item.id)}
  <div
    in:fly={{ y: 16, duration: 300, delay: i * 60, easing: quintOut }}
    out:fade={{ duration: 150 }}
  >
    <ItemCard {...item} />
  </div>
{/each}
```

### Modal/drawer with enter/exit

```svelte
<script lang="ts">
  import { fade, fly } from 'svelte/transition'
  let { isOpen = false } = $props()
</script>

{#if isOpen}
  <!-- Backdrop -->
  <div
    class="backdrop"
    transition:fade={{ duration: 200 }}
    role="presentation"
  />

  <!-- Drawer -->
  <aside
    class="drawer"
    transition:fly={{ x: 320, duration: 300, easing: cubicOut }}
    role="dialog"
    aria-modal="true"
  >
    {@render children()}
  </aside>
{/if}
```

## Step 3: Apply animations to existing components

When modifying existing files:

1. **Read each component file** first — understand the current structure
2. **Add CSS classes** for Micro tier only (never change the component's logic for Micro)
3. **Wrap with motion components** for Meso/Macro (React) or **add transition directives** (Svelte)
4. **Add the reduced-motion override** to the main CSS file if not already present
5. **Test both states** — with and without animation (use browser DevTools to simulate reduced motion)

## What NOT to animate

- Navigation links — stick to color/underline transitions only
- Scrolling behavior — only `scroll-behavior: smooth` where appropriate, and even that needs the reduced-motion override
- Data tables — distract from reading; use subtle row hover only
- Every element on a page — choose 2-3 anchor animations per screen

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Animation not playing | Check the element is in the DOM before the animation fires |
| Framer Motion hydration error | Ensure component has `'use client'` directive |
| Svelte transition plays twice | Check for double-render in dev mode (StrictMode equivalent) |
| Animation jank/lag | Add `will-change: transform, opacity` sparingly to animated elements |
| Reduced motion not stopping animation | Ensure `@media (prefers-reduced-motion)` is loaded AFTER animation CSS |

## References

- `resources/animation-patterns.md` — Catalog of copy-paste ready patterns for common UI components
