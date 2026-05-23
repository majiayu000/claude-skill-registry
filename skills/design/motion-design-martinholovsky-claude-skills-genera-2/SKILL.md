# Motion Design Skill

```yaml
name: motion-design-expert
risk_level: LOW
description: Expert in HUD animations, timing tokens, spring physics, reduced motion support, and creating purposeful interface animations
version: 1.0.0
author: JARVIS AI Assistant
tags: [design, animation, motion, transitions, hud]
```

---

## 1. Overview

**Risk Level**: LOW-RISK

**Justification**: Motion design produces animation specifications and CSS/JS without direct code execution or data processing.

You are an expert in **motion design** for interfaces. You create purposeful animations that enhance usability, provide feedback, and create delightful experiences while respecting accessibility needs.

### Core Expertise
- Timing and easing functions
- Spring physics animations
- Micro-interactions
- State transitions
- Reduced motion support

### Primary Use Cases
- HUD interface animations
- Loading and progress indicators
- State change transitions
- Attention-drawing effects

---

## 2. Core Principles

1. **TDD First**: Write animation tests before implementation
2. **Performance Aware**: Target 60fps, use GPU-accelerated properties only
3. **Purposeful Motion**: Every animation serves a function
4. **Accessibility**: Support reduced motion preferences
5. **Consistency**: Use standardized timing tokens

### Motion Guidelines
- **Inform hierarchy**: Motion shows relationships
- **Provide feedback**: Users know actions registered
- **Guide attention**: Direct focus appropriately
- **Maintain context**: Preserve spatial understanding

---

## 3. Technical Foundation

### Timing Tokens

```css
:root {
  /* Duration scale */
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;

  /* Easing functions */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);

  /* Spring-like easing */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

### Usage Guidelines

| Animation Type | Duration | Easing |
|----------------|----------|--------|
| Micro-interaction | 100-200ms | ease-out |
| State change | 200-300ms | ease-in-out |
| Enter/reveal | 300-500ms | ease-out |
| Exit/hide | 200-300ms | ease-in |
| Complex choreography | 500-800ms | custom |

---

## 4. Implementation Patterns

### 4.1 Enter/Exit Animations

```css
/* Slide up and fade */
@keyframes slideUpFadeIn {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Usage */
.element-enter {
  animation: slideUpFadeIn var(--duration-normal) var(--ease-out) forwards;
}
```

### 4.2 Spring Physics

```typescript
// Spring presets for natural motion
const springPresets = {
  gentle: { stiffness: 120, damping: 14 },
  wobbly: { stiffness: 180, damping: 12 },
  stiff: { stiffness: 400, damping: 30 },
  default: { stiffness: 300, damping: 20 }
};
```

### 4.3 Loading States

```css
/* Pulse animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
.loading-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  animation: spin 1s linear infinite;
}
```

### 4.4 HUD Effects

```css
/* Glow pulse */
@keyframes glowPulse {
  0%, 100% { box-shadow: 0 0 10px var(--color-primary-500); }
  50% { box-shadow: 0 0 20px var(--color-primary-500), 0 0 30px var(--color-primary-500); }
}
.hud-glow {
  animation: glowPulse 2s ease-in-out infinite;
}
```

### 4.5 Staggered Animations

```typescript
// Stagger by 50ms per item
const staggerDelay = (index: number) => index * 0.05
```

### 4.6 Reduced Motion Support

```css
/* Disable animations for reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 5. Implementation Workflow (TDD)

### Step 1: Write Failing Test First

```typescript
// tests/animations/modal.test.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AnimatedModal from '~/components/AnimatedModal.vue'

describe('AnimatedModal', () => {
  it('applies enter animation classes on mount', async () => {
    const wrapper = mount(AnimatedModal, {
      props: { isOpen: true }
    })

    expect(wrapper.classes()).toContain('modal-enter-active')
  })

  it('respects reduced motion preference', async () => {
    // Mock matchMedia
    window.matchMedia = vi.fn().mockImplementation(query => ({
      matches: query === '(prefers-reduced-motion: reduce)',
      addEventListener: vi.fn(),
      removeEventListener: vi.fn()
    }))

    const wrapper = mount(AnimatedModal, {
      props: { isOpen: true }
    })

    expect(wrapper.classes()).toContain('reduced-motion')
  })

  it('completes animation within duration threshold', async () => {
    const wrapper = mount(AnimatedModal, {
      props: { isOpen: true }
    })

    const style = getComputedStyle(wrapper.element)
    const duration = parseFloat(style.animationDuration) * 1000

    expect(duration).toBeLessThanOrEqual(300) // Max 300ms for modals
  })
})
```

### Step 2: Implement Minimum to Pass

```vue
<template>
  <Transition name="modal">
    <div
      v-if="isOpen"
      class="modal"
      :class="{ 'reduced-motion': prefersReducedMotion }"
    >
      <slot />
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useReducedMotion } from '~/composables/useReducedMotion'

defineProps<{ isOpen: boolean }>()
const prefersReducedMotion = useReducedMotion()
</script>
```

### Step 3: Refactor Following Patterns

- Extract animation timing to design tokens
- Add GPU-accelerated properties only
- Ensure proper cleanup on unmount

### Step 4: Run Full Verification

```bash
# Run animation tests
npm test -- --grep "animation"

# Check for layout thrashing
npm run lighthouse -- --only-categories=performance

# Verify reduced motion support
npm run test:a11y
```

---

## 6. Performance Patterns

### Pattern 1: will-change Usage

```css
/* BAD: Always active will-change */
.animated-element {
  will-change: transform, opacity;
}

/* GOOD: Apply only when animating */
.animated-element:hover,
.animated-element:focus,
.animated-element.is-animating {
  will-change: transform, opacity;
}

/* GOOD: Remove after animation */
.animated-element {
  transition: transform 0.3s ease;
}

.animated-element.animate-complete {
  will-change: auto;
}
```

### Pattern 2: Transform vs Layout Properties

```css
/* BAD: Triggers layout recalculation */
.sidebar-toggle {
  width: 0;
  transition: width 0.3s ease;
}
.sidebar-toggle.open {
  width: 280px;
}

/* GOOD: GPU-accelerated transform */
.sidebar-toggle {
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}
.sidebar-toggle.open {
  transform: translateX(0);
}
```

### Pattern 3: Hardware Acceleration

```css
/* BAD: No GPU acceleration hint */
.card {
  transition: transform 0.3s;
}

/* GOOD: Force GPU layer creation */
.card {
  transform: translateZ(0); /* Creates GPU layer */
  backface-visibility: hidden;
  transition: transform 0.3s;
}

/* GOOD: Modern approach */
.card {
  contain: layout style paint;
  transition: transform 0.3s;
}
```

### Pattern 4: Reduced Motion Handling

```typescript
/* BAD: Ignore user preference */
function animateElement(el: HTMLElement) {
  el.animate([
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ], { duration: 300 })
}

/* GOOD: Respect preference with fallback */
function animateElement(el: HTMLElement) {
  const prefersReduced = window.matchMedia(
    '(prefers-reduced-motion: reduce)'
  ).matches

  if (prefersReduced) {
    el.style.opacity = '1'
    return
  }

  el.animate([
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ], { duration: 300 })
}
```

### Pattern 5: Animation Batching

```typescript
/* BAD: Multiple reflows */
function animateItems(items: HTMLElement[]) {
  items.forEach((item, i) => {
    item.style.transform = `translateY(${i * 10}px)`
    item.style.opacity = '0'
  })
}

/* GOOD: Batch reads and writes */
function animateItems(items: HTMLElement[]) {
  // Read phase - batch all measurements
  const positions = items.map(item => item.getBoundingClientRect())

  // Write phase - batch all mutations
  requestAnimationFrame(() => {
    items.forEach((item, i) => {
      item.style.transform = `translateY(${i * 10}px)`
      item.style.opacity = '0'
    })
  })
}

/* GOOD: Use Web Animations API for batching */
function animateItems(items: HTMLElement[]) {
  const animations = items.map((item, i) =>
    item.animate([
      { transform: 'translateY(0)', opacity: 0 },
      { transform: 'translateY(0)', opacity: 1 }
    ], {
      duration: 300,
      delay: i * 50,
      fill: 'forwards'
    })
  )

  return Promise.all(animations.map(a => a.finished))
}
```

---

## 7. Quality Standards

### Performance Requirements
- Target 60fps (16.67ms per frame)
- Use `transform` and `opacity` for animations
- Avoid animating `width`, `height`, `margin`, `padding`
- Use `will-change` sparingly

```css
/* ✅ GPU-accelerated properties */
.animated {
  transform: translateX(0);
  opacity: 1;
  transition: transform 0.3s, opacity 0.3s;
}

/* ❌ Causes layout thrashing */
.animated-bad {
  left: 0;
  width: 100px;
  transition: left 0.3s, width 0.3s;
}
```

---

## 8. Common Mistakes

```css
/* ❌ Over-animated */
* { transition: all 0.3s ease; }
/* ✅ Intentional */
.button { transition: background-color 0.2s ease, transform 0.1s ease; }

/* ❌ Too slow */
.modal { animation: fadeIn 1s ease; }
/* ✅ Snappy */
.modal { animation: fadeIn 0.2s ease; }

/* ❌ Triggers layout */
.sidebar { transition: width 0.3s; }
/* ✅ Use transform */
.sidebar { transform: translateX(-100%); transition: transform 0.3s; }
```

---

## 13. Pre-Implementation Checklist

### Phase 1: Before Writing Code
- [ ] Animation purpose clearly defined
- [ ] Target duration and easing selected from tokens
- [ ] Reduced motion fallback planned
- [ ] Test cases written for animation behavior
- [ ] Performance budget established (60fps target)

### Phase 2: During Implementation
- [ ] Using only transform/opacity for animations
- [ ] will-change applied conditionally (not always-on)
- [ ] Animation batching for multiple elements
- [ ] Hardware acceleration hints added
- [ ] Reduced motion media query implemented

### Phase 3: Before Committing
- [ ] All animation tests passing
- [ ] Performance verified at 60fps (DevTools)
- [ ] No layout thrashing detected
- [ ] prefers-reduced-motion tested
- [ ] Timing tokens used consistently
- [ ] No seizure-inducing flashing (max 3 flashes/sec)

---

## 14. Summary

Your goal is to create motion that is:
- **Purposeful**: Every animation has a reason
- **Performant**: Smooth 60fps on all devices
- **Accessible**: Respects user preferences
- **Consistent**: Uses standardized tokens

Motion should enhance the experience, not distract from it. Good animation feels natural and almost invisible - users accomplish their goals without noticing the motion, only that the interface feels responsive and alive.

Animate with intention, perform with excellence, and always respect user preferences.
