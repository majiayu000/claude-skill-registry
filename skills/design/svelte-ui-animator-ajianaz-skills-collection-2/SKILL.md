---
name: svelte-ui-animator
description: Analyze and implement purposeful UI animations for Svelte/SvelteKit + Tailwind projects. Specialized in Svelte transitions, actions, and animation patterns. Use when user asks to add animations, enhance UI motion, animate pages/components, or improve visual feedback. Triggers on "add animations", "animate UI", "motion design", "hover effects", "scroll animations", "page transitions", "micro-interactions".
---

# Svelte UI Animator

Implement purposeful, performant animations using Svelte's built-in transitions and actions. Focus on key moments: hero intros, hover feedback, content reveals, and navigation transitions with Svelte's reactive nature.

## Core Philosophy

**"You don't need animations everywhere"** - Prioritize:

| Priority | Area | Purpose |
|----------|------|---------|
| 1 | Hero Intro | First impression, brand personality |
| 2 | Hover Interactions | Feedback, discoverability |
| 3 | Content Reveal | Guide attention, reduce cognitive load |
| 4 | Background Effects | Atmosphere, depth |
| 5 | Navigation Transitions | Spatial awareness, continuity |

## Workflow

Execute phases sequentially. Complete each before proceeding.

### Phase 1: Analyze

1. **Scan project structure** - Identify all pages in `src/routes/` and components in `src/lib/components/`
2. **Check existing setup** - Review `tailwind.config.js` and `app.html` for existing animations/keyframes
3. **Identify animation candidates** - List components by priority category
4. **Document constraints** - Note installed animation libraries (svelte/transition, auto-animate, motion, etc.)

Output: Animation audit table. See `references/component-checklist.md`.

### Phase 2: Plan

1. **Map animations to components** - Assign specific animation patterns
2. **Determine triggers** - Load, scroll (intersection), hover, click
3. **Estimate effort** - Low (CSS only), Medium (hooks needed), High (library required)
4. **Propose phased rollout** - Quick wins first

Output: Implementation plan with component → animation mapping.

### Phase 3: Implement

1. **Extend Tailwind config** - Add keyframes and animation utilities
2. **Add reduced-motion support** - Accessibility first
3. **Create reusable actions** - `scrollReveal`, `mousePosition`, `staggerAnimate` if needed
4. **Apply animations per component** - Follow patterns in `references/animation-patterns.md`

**Performance rules:**
```svelte
<!-- ✅ DO: Use transforms and opacity only -->
<div style="transform: translateY(20px); opacity: 0.5; filter: blur(4px);" />

<!-- ❌ DON'T: Animate layout properties -->
<div style="margin-top: 20px; height: 100px; width: 200px;" />
```

### Phase 4: Verify

1. Test in browser - Visual QA all animations
2. Test reduced-motion - Verify `prefers-reduced-motion` works
3. Check CLS - No layout shifts from animations
4. Performance audit - No jank on scroll animations

## Quick Reference

### Animation Triggers

| Trigger | Implementation |
|---------|----------------|
| Page load | CSS `animation` with `animation-delay` for stagger |
| Scroll into view | Svelte actions with `IntersectionObserver` or `on:viewportenter` |
| Hover | Tailwind `hover:` utilities or Svelte `mouseenter/mouseleave` |
| Click/Tap | State-driven with Svelte reactive statements (`$:`) |

### Common Patterns

**Staggered children with Svelte transitions:**
```svelte
<script>
  import { flip, fly } from 'svelte/transition';
</script>

{#each items as item, i (item.id)}
  <div
    in:fly={{ y: 20, delay: i * 50 }}
    out:fly={{ y: -20 }}
  >
    {item.content}
  </div>
{/each}
```

**Advanced scroll reveal action:**
```svelte
<!-- actions/scrollReveal.js -->
export function scrollReveal(node, options = {}) {
  const {
    threshold = 0.1,
    animation = 'fade-slide-up',
    delay = 0
  } = options;

  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          node.classList.add('animate-' + animation);
        }, delay);
      }
    },
    { threshold }
  );

  observer.observe(node);

  return {
    destroy() => observer.disconnect()
  };
}
```

**Usage with reactive state:**
```svelte
<script>
  import { scrollReveal } from '$lib/actions/scrollReveal.js';
  import { onMount } from 'svelte';

  let isVisible = false;
  let element;

  onMount(() => {
    const observer = new IntersectionObserver(
      ([entry]) => isVisible = entry.isIntersecting
    );
    observer.observe(element);
    return () => observer.disconnect();
  });
</script>

<div
  bind:this={element}
  use:scrollReveal={{ animation: 'fade-in', delay: 100 }}
  class:visible={isVisible}
>
  Content here
</div>
```

## Resources

- **Animation patterns**: See `references/animation-patterns.md`
- **Audit template**: See `references/component-checklist.md`
- **Tailwind presets**: See `references/tailwind-presets.md`

## Technical Stack

- **Svelte transitions**: Primary choice - `fade`, `fly`, `slide`, `scale`, `blur`, `crossfade`
- **CSS animations**: For complex keyframe animations not covered by Svelte transitions
- **Tailwind utilities**: For hover states and basic animations
- **Auto-animate**: For automatic layout animations (if installed)
- **Svelte actions**: For custom scroll-triggered and interactive animations
- **Motion**: For advanced gesture-based animations (if installed)
- **GSAP**: For timeline-based sequences (if already installed)

## Accessibility (Required)

Always include in global CSS:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
  }
}
```
