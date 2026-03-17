---
name: web-animation-css-animations
description: CSS Animation patterns - transitions, keyframes, scroll-driven animations, View Transitions API, GPU-accelerated properties, accessibility with prefers-reduced-motion
---

# CSS Animation Patterns

> **Quick Guide:** Use CSS transitions for state changes (hover, focus), CSS animations with @keyframes for autonomous/looping animations, scroll-driven animations for scroll-linked effects, and View Transitions API for page/view transitions. Animate only `transform` and `opacity` for 60fps performance.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST animate ONLY transform and opacity for GPU-accelerated 60fps performance)**

**(You MUST respect prefers-reduced-motion using media queries or @media (prefers-reduced-motion: no-preference))**

**(You MUST use named constants (CSS custom properties) for ALL timing values - NO magic numbers)**

**(You MUST use ease-out for enter animations and ease-in for exit animations - NEVER linear for UI)**

**(You MUST remove will-change after animation completes - permanent will-change wastes GPU memory)**

</critical_requirements>

---

**Auto-detection:** CSS animation, CSS transition, @keyframes, transform, opacity, transition-duration, animation-duration, prefers-reduced-motion, scroll-timeline, view-transition, animation-timeline, will-change, cubic-bezier, ease-out, ease-in

**When to use:**

- Simple state change animations (hover, focus, active states)
- Autonomous looping animations (spinners, pulses, attention grabbers)
- Scroll-linked animations and parallax effects
- Page/view transitions between routes
- Micro-interactions that don't need JavaScript control

**Key patterns covered:**

- CSS transitions for state-triggered animations
- CSS @keyframes for multi-step and looping animations
- GPU-accelerated properties (transform, opacity)
- Animation timing tokens and custom properties
- prefers-reduced-motion accessibility patterns
- Scroll-driven animations (animation-timeline: scroll/view)
- View Transitions API for page transitions
- will-change optimization and cleanup

**When NOT to use:**

- Animations requiring JavaScript control (pause, reverse, seek) - consider Web Animations API
- Complex orchestrated animations with staggered timing - consider your animation library
- Physics-based spring animations - consider your animation library
- Drag-and-drop animations - consider your animation library

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

CSS animations leverage the browser's compositor thread for smooth, 60fps animations that don't block JavaScript execution. By animating only GPU-accelerated properties (`transform` and `opacity`), animations run on a separate thread from the main JavaScript thread.

**Core principles:**

1. **Performance first** - Animate only `transform` and `opacity` to avoid layout/paint triggers
2. **Accessibility built-in** - Always respect `prefers-reduced-motion` user preferences
3. **Transitions for state changes** - Use CSS transitions for hover, focus, and state-driven animations
4. **Keyframes for autonomous motion** - Use @keyframes for animations that loop, auto-play, or have multiple steps
5. **Design tokens for consistency** - Use CSS custom properties for durations, easings, and distances

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CSS Transitions for State Changes

CSS transitions animate property changes between two states. Use for hover effects, focus states, and interactive feedback.

#### Duration Tokens

```css
:root {
  /* Duration tokens */
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-slower: 600ms;

  /* Easing tokens */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  /* Distance tokens */
  --lift-sm: -2px;
  --lift-md: -4px;
  --lift-lg: -8px;
}
```

#### Implementation

```css
/* Good Example - GPU-accelerated hover effect */
.card {
  transition:
    transform var(--duration-fast) var(--ease-out),
    opacity var(--duration-fast) var(--ease-out);
}

.card:hover {
  transform: translateY(var(--lift-md)) scale(1.02);
}

.card:active {
  transform: translateY(0) scale(0.98);
}
```

**Why good:** Only animates transform (GPU-accelerated), uses design tokens for timing, provides tactile feedback on both hover and active states

```css
/* Bad Example - Layout-triggering properties */
.card {
  transition: all 0.3s linear;
}

.card:hover {
  top: -8px;
  margin-top: -8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}
```

**Why bad:** `top` and `margin-top` trigger expensive layout recalculations every frame, `all` transitions unnecessary properties, `linear` feels robotic, magic number `0.3s`

---

### Pattern 2: CSS @keyframes for Autonomous Animations

Use @keyframes for animations that loop, auto-play on mount, or have more than two states.

#### Loading Spinner

```css
/* Good Example - Looping spinner */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  --spinner-duration: 1s;

  animation: spin var(--spinner-duration) linear infinite;
}
```

**Why good:** Uses transform (GPU-accelerated), `linear` is appropriate for continuous rotation, duration is a named token

#### Pulse Animation

```css
/* Good Example - Attention-grabbing pulse */
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.notification-dot {
  --pulse-duration: 1.5s;

  animation: pulse var(--pulse-duration) ease-in-out infinite;
}
```

**Why good:** Only animates opacity (GPU-accelerated), uses ease-in-out for smooth oscillation

#### Slide-In Animation

```css
/* Good Example - Enter animation */
@keyframes slide-in {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.modal {
  --modal-enter-duration: 300ms;

  animation: slide-in var(--modal-enter-duration) var(--ease-out) forwards;
}
```

**Why good:** Uses `forwards` to retain final state, ease-out for enter animation, combines transform and opacity

---

### Pattern 3: GPU-Accelerated Shadow Animation

Animating `box-shadow` triggers expensive repaints. Use a pseudo-element with animated opacity instead.

#### Implementation

```css
/* Good Example - Pseudo-element shadow technique */
.card {
  position: relative;
}

.card::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity var(--duration-fast) var(--ease-out);
  pointer-events: none;
}

.card:hover::after {
  opacity: 1;
}
```

**Why good:** Shadow is always rendered on pseudo-element, only opacity is animated (GPU-accelerated), no repaint on every frame

```css
/* Bad Example - Direct shadow animation */
.card {
  transition: box-shadow 0.3s;
}

.card:hover {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}
```

**Why bad:** box-shadow animation triggers repaint on every frame, causing jank on complex pages

---

### Pattern 4: Staggered List Animations

Use CSS custom properties with `animation-delay` for staggered effects without JavaScript.

#### Implementation

```css
/* Good Example - CSS-only stagger */
@keyframes fade-slide-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.list-item {
  --stagger-delay: 50ms;
  --item-duration: 300ms;

  animation: fade-slide-in var(--item-duration) var(--ease-out) backwards;
  animation-delay: calc(var(--index) * var(--stagger-delay));
}
```

```html
<!-- Set index via inline style or data attribute -->
<li class="list-item" style="--index: 0">First</li>
<li class="list-item" style="--index: 1">Second</li>
<li class="list-item" style="--index: 2">Third</li>
```

**Why good:** `backwards` fill mode shows initial state before animation starts, CSS handles timing cascade, minimal JavaScript (just setting index)

---

### Pattern 5: Prefers-Reduced-Motion Accessibility

Always respect user motion preferences. Two approaches: remove motion or provide safe alternatives.

#### Approach 1: Progressive Enhancement (Recommended)

```css
/* Good Example - Motion opt-in approach */
.element {
  /* Base state - no animation */
  opacity: 1;
  transform: translateY(0);
}

/* Only apply motion when user has no preference */
@media (prefers-reduced-motion: no-preference) {
  .element {
    animation: fade-slide-in var(--duration-normal) var(--ease-out);
  }
}
```

**Why good:** Motion is opt-in, users who prefer reduced motion see static content immediately

#### Approach 2: Global Disable

```css
/* Alternative - Disable all motion */
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

**Why good:** Nuclear option that catches all animations, useful as a fallback

#### Approach 3: Safe Alternative Animations

```css
/* Good Example - Provide alternative */
.notification {
  --notification-duration: 400ms;
}

/* Full motion experience */
@media (prefers-reduced-motion: no-preference) {
  .notification {
    animation: slide-in-bounce var(--notification-duration) var(--ease-spring);
  }
}

/* Reduced motion alternative - fade only */
@media (prefers-reduced-motion: reduce) {
  .notification {
    animation: fade-in calc(var(--notification-duration) * 0.5) var(--ease-out);
  }
}

@keyframes slide-in-bounce {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  70% {
    transform: translateX(-10px);
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
```

**Why good:** Provides graceful degradation with meaningful visual feedback, reduced motion users still see the notification appear

---

### Pattern 6: Will-Change Optimization

Use `will-change` sparingly and remove it after animation completes.

#### Correct Usage

```css
/* Good Example - Apply only when needed */
.card {
  /* No will-change by default */
}

.card:hover {
  will-change: transform;
  transform: scale(1.05);
}

/* Or use a class for animation state */
.card.is-animating {
  will-change: transform, opacity;
}
```

**Why good:** will-change creates GPU layer only when needed, removed after hover ends

```css
/* Bad Example - Permanent will-change */
.card {
  will-change: transform, opacity; /* Always active */
}

/* Worse - Global will-change */
* {
  will-change: transform; /* Memory disaster */
}
```

**Why bad:** Each element with will-change creates a GPU layer (~307KB per 320x240px element), permanent will-change wastes GPU memory, can crash mobile browsers

---

### Pattern 7: @property for Animating Custom Properties

Use CSS Houdini's @property to animate custom properties like gradient angles.

#### Implementation

```css
/* Good Example - Animated gradient */
@property --gradient-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.gradient-border {
  --gradient-duration: 3s;

  background: linear-gradient(var(--gradient-angle), #ff0080, #7928ca);
  animation: rotate-gradient var(--gradient-duration) linear infinite;
}

@keyframes rotate-gradient {
  to {
    --gradient-angle: 360deg;
  }
}
```

**Why good:** @property allows CSS to understand the type and interpolate correctly, enables effects previously requiring JavaScript

**Browser support:** Chrome 85+, Edge 85+, Safari 15.4+, Firefox 128+

</patterns>

---

<performance>

## Performance Optimization

### The 16.67ms Budget

For 60fps, each frame must complete in 16.67ms. Layout-triggering animations often exceed this budget.

### Properties by Performance Impact

| Category                   | Properties                                | Impact                               |
| -------------------------- | ----------------------------------------- | ------------------------------------ |
| **Composite only (Best)**  | transform, opacity                        | No layout, no paint, GPU-accelerated |
| **Paint only (Okay)**      | color, background-color, visibility       | No layout, but repaints              |
| **Layout + Paint (Avoid)** | width, height, margin, padding, top, left | Full page recalculation              |

### Duration Guidelines

| Animation Type     | Duration   | Reason                    |
| ------------------ | ---------- | ------------------------- |
| Micro-interactions | 100-200ms  | Feels instant             |
| UI transitions     | 200-300ms  | Sweet spot for perception |
| Page transitions   | 300-500ms  | Noticeable but not slow   |
| Complex sequences  | 500-1000ms | Story-telling moments     |

### Transform Mapping

Instead of animating layout properties, use equivalent transforms:

| Instead of...       | Use...                            |
| ------------------- | --------------------------------- |
| `top`, `left`       | `translate(x, y)`                 |
| `width`, `height`   | `scale()`                         |
| `margin`, `padding` | `translate()` or layout animation |

</performance>

---

<decision_framework>

## Decision Framework

### When to Use Transitions vs Animations

```
Is the animation triggered by user interaction?
├─ YES → Is it a simple A→B state change?
│   ├─ YES → CSS Transition ✓
│   └─ NO → Does it need multiple steps?
│       ├─ YES → CSS Animation with @keyframes
│       └─ NO → CSS Transition is fine
└─ NO → Does it auto-play or loop?
    ├─ YES → CSS Animation with @keyframes ✓
    └─ NO → CSS Transition (triggered by class toggle)
```

### When to Use which Easing

```
What type of motion?
├─ Element entering → ease-out (fast start, slow end) ✓
├─ Element exiting → ease-in (slow start, fast end) ✓
├─ Symmetric motion → ease-in-out
├─ Continuous rotation → linear ✓
├─ Playful/bouncy → custom cubic-bezier with overshoot
└─ Default UI → ease-out ✓
```

### Which Property to Animate

```
Need movement?
├─ Position change → transform: translate()
├─ Grow/shrink → transform: scale()
├─ Rotation → transform: rotate()
└─ Visibility → opacity

Need to avoid?
├─ Size change → Never animate width/height (use scale)
├─ Position → Never animate top/left (use translate)
└─ Shadow → Use pseudo-element opacity technique
```

</decision_framework>

---

<integration>

## Integration Guide

**CSS animations are framework-agnostic.** They work with any styling solution and component architecture.

**Works with:**

- **Any component framework**: Apply via className or style attribute
- **CSS Modules**: Animation classes compose naturally
- **Utility CSS**: Combine with utility classes
- **Design systems**: Animation tokens integrate into token systems

**CSS animations complement JavaScript animation libraries:**

- Use CSS for simple state transitions
- Use your animation library for complex orchestration
- Both can coexist in the same application

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST animate ONLY transform and opacity for GPU-accelerated 60fps performance)**

**(You MUST respect prefers-reduced-motion using media queries or @media (prefers-reduced-motion: no-preference))**

**(You MUST use named constants (CSS custom properties) for ALL timing values - NO magic numbers)**

**(You MUST use ease-out for enter animations and ease-in for exit animations - NEVER linear for UI)**

**(You MUST remove will-change after animation completes - permanent will-change wastes GPU memory)**

**Failure to follow these rules will cause jank, accessibility issues, and degraded user experience.**

</critical_reminders>
