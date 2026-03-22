---
name: ui-animation
description: Motion design and animation for user interfaces. Use when creating micro-interactions, page transitions, loading states, or any UI animation across web and mobile platforms.
---

# UI Animation & Motion Design

Comprehensive guide for creating purposeful, performant animations in user interfaces.

## Animation Principles

### The 12 Principles of Animation (Applied to UI)

| Principle            | UI Application                        |
| -------------------- | ------------------------------------- |
| **Timing**           | Duration reflects importance/distance |
| **Easing**           | Natural acceleration/deceleration     |
| **Anticipation**     | Visual preparation for action         |
| **Follow-through**   | Momentum continues after stop         |
| **Secondary Action** | Supporting elements respond           |
| **Staging**          | Draw attention to key element         |
| **Squash & Stretch** | Bouncy, playful interactions          |
| **Exaggeration**     | Emphasize important feedback          |
| **Arc**              | Natural curved motion paths           |
| **Overlap**          | Elements move at different rates      |
| **Solid Drawing**    | Maintain consistent 3D space          |
| **Appeal**           | Engaging, delightful motion           |

### Why Animate?

```
FUNCTIONAL PURPOSES:
✓ Guide attention to important changes
✓ Show relationships between elements
✓ Provide feedback for actions
✓ Communicate system status
✓ Ease cognitive load
✓ Create spatial orientation

NOT FOR:
✗ Pure decoration
✗ Showing off skills
✗ Making things "feel modern"
✗ Distracting from content
```

---

## Timing & Duration

### Duration Guidelines

```
INSTANT (0-100ms):
└─→ Button state changes
└─→ Toggle switches
└─→ Micro-feedback

FAST (100-200ms):
└─→ Hover effects
└─→ Simple fades
└─→ Small movements

STANDARD (200-300ms):
└─→ Most UI transitions
└─→ Modal open/close
└─→ Dropdown menus

SLOW (300-500ms):
└─→ Complex transitions
└─→ Page transitions
└─→ Large element movement

DELIBERATE (500ms+):
└─→ Hero animations
└─→ Skeleton loading
└─→ Onboarding sequences
```

### Distance-Based Timing

```
Rule: Longer distance = Longer duration

Small (< 100px):   150-200ms
Medium (100-300px): 200-300ms
Large (300-500px):  300-400ms
Full screen:        400-500ms

Formula:
duration = baseTime + (distance × factor)
```

---

## Easing Functions

### Standard Easings

```
LINEAR
├────────────────────────────┤
Constant speed. Rarely natural.
Use: Progress bars, clock hands

EASE-OUT (Deceleration)
├═══════════────────────────┤
Fast start, slow end.
Use: Elements entering the screen

EASE-IN (Acceleration)
├────────────────═══════════┤
Slow start, fast end.
Use: Elements leaving the screen

EASE-IN-OUT (S-curve)
├────═══════════════────────┤
Slow start and end, fast middle.
Use: On-screen transitions

EASE-OUT-BACK (Overshoot)
├═══════════────────────╗───┤
Overshoots, settles back.
Use: Playful entrances, bounces
```

### CSS Easing Values

```css
/* Built-in keywords */
linear: cubic-bezier(0, 0, 1, 1)
ease: cubic-bezier(0.25, 0.1, 0.25, 1)
ease-in: cubic-bezier(0.42, 0, 1, 1)
ease-out: cubic-bezier(0, 0, 0.58, 1)
ease-in-out: cubic-bezier(0.42, 0, 0.58, 1)

/* Material Design standard */
standard: cubic-bezier(0.4, 0, 0.2, 1)
decelerate: cubic-bezier(0, 0, 0.2, 1)
accelerate: cubic-bezier(0.4, 0, 1, 1)

/* Custom: Snappy */
snappy: cubic-bezier(0.5, 0, 0, 1)

/* Custom: Bouncy */
bouncy: cubic-bezier(0.68, -0.55, 0.27, 1.55)

/* Spring-like (use JS libraries) */
spring: { stiffness: 300, damping: 20 }
```

### When to Use Each

| Scenario           | Easing        | Why                            |
| ------------------ | ------------- | ------------------------------ |
| Element entering   | ease-out      | Arrives energetically, settles |
| Element leaving    | ease-in       | Gathers momentum to exit       |
| On-screen change   | ease-in-out   | Smooth state change            |
| Attention grabbing | bounce/spring | Playful, noticeable            |
| Background/subtle  | ease-out      | Unobtrusive                    |

---

## Animation Patterns

### Micro-interactions

```
BUTTON STATES:
┌─────────────────────────────────────────┐
│ Rest → Hover: scale(1.02), 100ms        │
│ Hover → Active: scale(0.98), 50ms       │
│ Active → Rest: scale(1), 150ms ease-out │
└─────────────────────────────────────────┘

TOGGLE SWITCH:
┌─────────────────────────────────────────┐
│ Thumb: translateX, 200ms ease-out       │
│ Track: background-color, 200ms          │
│ State: slight bounce at end             │
└─────────────────────────────────────────┘

CHECKBOX:
┌─────────────────────────────────────────┐
│ Check mark: stroke-dashoffset animation │
│ Background: scale from center, 150ms    │
│ Ripple: expanding circle, 300ms         │
└─────────────────────────────────────────┘
```

### Loading States

```
SKELETON SCREENS:
┌──────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░░░  │ Shimmer effect
│ ▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░  │ Linear gradient
│ ▓▓▓▓▓▓░░░░░░░░░░░░░░░░  │ Moving left to right
└──────────────────────────┘

CSS:
background: linear-gradient(
  90deg,
  #f0f0f0 25%,
  #e0e0e0 50%,
  #f0f0f0 75%
);
background-size: 200% 100%;
animation: shimmer 1.5s infinite;

SPINNER:
- Duration: 1-2 seconds per rotation
- Easing: linear (consistent motion)
- Style: Match brand identity
```

### Page Transitions

```
CROSSFADE:
├──────────────────────────────────────────┤
│ Old page: opacity 1 → 0, 200ms           │
│ New page: opacity 0 → 1, 200ms           │
│ Timing: Sequential or overlapping        │
└──────────────────────────────────────────┘

SLIDE:
├──────────────────────────────────────────┤
│ Direction follows navigation hierarchy   │
│ Forward: Slide left (new from right)     │
│ Back: Slide right (prev from left)       │
│ Duration: 300-400ms                      │
└──────────────────────────────────────────┘

SHARED ELEMENT:
├──────────────────────────────────────────┤
│ Element morphs between states            │
│ Position, size, border-radius change     │
│ Creates continuity between screens       │
│ Duration: 300-500ms                      │
└──────────────────────────────────────────┘
```

### List Animations

```
STAGGERED ENTRANCE:
┌─ Item 1 ────────────────┐  delay: 0ms
├─ Item 2 ────────────────┤  delay: 50ms
├─ Item 3 ────────────────┤  delay: 100ms
├─ Item 4 ────────────────┤  delay: 150ms
└─ Item 5 ────────────────┘  delay: 200ms

Max total duration: 500ms
Stagger: 30-50ms per item
Animation: translateY + opacity

REORDER:
- Use FLIP technique
- Duration: 200-300ms
- Ease: ease-out
```

---

## Performance

### GPU-Accelerated Properties

```
FAST (Compositor only):
✓ transform: translate, scale, rotate
✓ opacity
✓ filter (with will-change)

SLOW (Triggers layout/paint):
✗ width, height
✗ margin, padding
✗ top, left, right, bottom
✗ border, border-radius
✗ font-size
✗ box-shadow (repaints)

OPTIMIZATION:
will-change: transform, opacity;
/* Use sparingly! */
```

### Performance Guidelines

```css
/* Good: GPU-accelerated */
.animated-element {
  transform: translateX(0);
  transition: transform 300ms ease-out;
}
.animated-element.moved {
  transform: translateX(100px);
}

/* Bad: Layout thrashing */
.animated-element {
  left: 0;
  transition: left 300ms ease-out;
}
.animated-element.moved {
  left: 100px;
}
```

### FLIP Technique

```javascript
// First: Get initial position
const first = element.getBoundingClientRect();

// Last: Apply change, get final position
element.classList.add("moved");
const last = element.getBoundingClientRect();

// Invert: Calculate delta, apply inverse transform
const deltaX = first.left - last.left;
const deltaY = first.top - last.top;
element.style.transform = `translate(${deltaX}px, ${deltaY}px)`;

// Play: Remove transform with transition
requestAnimationFrame(() => {
  element.style.transition = "transform 300ms ease-out";
  element.style.transform = "";
});
```

---

## CSS Animation Techniques

### Keyframe Animation

```css
@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: fadeSlideIn 300ms ease-out forwards;
}

/* With steps */
@keyframes typewriter {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

.typing-text {
  animation: typewriter 2s steps(20) forwards;
}
```

### Transition

```css
.button {
  background: var(--primary);
  transform: scale(1);
  transition:
    background 150ms ease-out,
    transform 100ms ease-out;
}

.button:hover {
  background: var(--primary-hover);
  transform: scale(1.02);
}

.button:active {
  transform: scale(0.98);
  transition-duration: 50ms;
}
```

### Animation Shorthand

```css
/* animation: name duration timing-function delay
              iteration-count direction fill-mode play-state */

animation: slideIn 300ms ease-out 100ms 1 normal forwards running;

/* Common patterns */
animation: spin 1s linear infinite;
animation: pulse 2s ease-in-out infinite alternate;
animation: fadeIn 300ms ease-out forwards;
```

---

## JavaScript Animation Libraries

### Comparison

| Library                | Best For             | Bundle Size |
| ---------------------- | -------------------- | ----------- |
| **CSS**                | Simple transitions   | 0kb         |
| **Web Animations API** | Native, performant   | 0kb         |
| **GSAP**               | Complex, precise     | ~60kb       |
| **Framer Motion**      | React ecosystem      | ~50kb       |
| **anime.js**           | Timeline, SVG        | ~17kb       |
| **Motion One**         | Modern, lightweight  | ~18kb       |
| **Lottie**             | After Effects export | ~50kb       |

### Framer Motion (React)

```jsx
import { motion, AnimatePresence } from "framer-motion";

// Basic animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
>
  Content
</motion.div>;

// Variants for complex animations
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible">
  {items.map((item) => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>;
```

### GSAP

```javascript
import { gsap } from "gsap";

// Basic tween
gsap.to(".element", {
  x: 100,
  opacity: 1,
  duration: 0.3,
  ease: "power2.out",
});

// Timeline
const tl = gsap.timeline();
tl.from(".header", { y: -100, duration: 0.5 })
  .from(".content", { opacity: 0, duration: 0.3 }, "-=0.2")
  .from(".button", { scale: 0.8, duration: 0.2 });

// ScrollTrigger
gsap.registerPlugin(ScrollTrigger);
gsap.to(".parallax", {
  y: -100,
  scrollTrigger: {
    trigger: ".section",
    start: "top center",
    end: "bottom center",
    scrub: true,
  },
});
```

---

## Accessibility

### Respecting User Preferences

```css
/* Reduce motion for users who prefer it */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Or provide simpler alternatives */
@media (prefers-reduced-motion: reduce) {
  .animated-element {
    /* Replace motion with opacity */
    animation: none;
    transition: opacity 200ms ease;
  }
}
```

### Safe Animation Practices

```
AVOID for vestibular disorders:
✗ Parallax scrolling effects
✗ Zooming/scaling animations
✗ Spinning/rotating elements
✗ Auto-playing animations
✗ Flashing (>3 times/second)

SAFE alternatives:
✓ Opacity fades
✓ Color transitions
✓ Subtle position changes
✓ User-initiated animations
```

### WCAG Guidelines

```
2.2.2 Pause, Stop, Hide:
- Auto-updating content can be paused
- No time limits on reading

2.3.1 Three Flashes:
- Nothing flashes more than 3x per second

2.3.3 Animation from Interactions:
- Motion can be disabled
- Triggered animations respect preferences
```

---

## Mobile Considerations

### Touch Feedback

```css
/* iOS-style tap feedback */
.button {
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.button:active {
  opacity: 0.7;
  transition: opacity 50ms;
}

/* Ripple effect */
.ripple {
  position: relative;
  overflow: hidden;
}

.ripple::after {
  content: "";
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: scale(0);
  animation: ripple 400ms ease-out;
}
```

### Platform Conventions

| Platform    | Animation Style                        |
| ----------- | -------------------------------------- |
| **iOS**     | Spring physics, 300-500ms, subtle      |
| **Android** | Material motion, 200-300ms, emphasized |
| **Web**     | Varies, typically 200-400ms            |

---

## Design System Integration

### Animation Tokens

```css
:root {
  /* Durations */
  --duration-instant: 100ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 400ms;
  --duration-slower: 600ms;

  /* Easings */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55);

  /* Combined */
  --transition-default: var(--duration-normal) var(--ease-default);
  --transition-fast: var(--duration-fast) var(--ease-out);
}

/* Usage */
.element {
  transition: transform var(--transition-default);
}
```

---

## Best Practices

### DO:

- Animate with purpose (feedback, guidance)
- Use GPU-accelerated properties
- Keep durations under 500ms
- Match animation to brand personality
- Respect prefers-reduced-motion
- Test on low-end devices
- Use consistent timing system

### DON'T:

- Animate for decoration alone
- Block user interaction
- Use excessive bounce/overshoot
- Create motion sickness triggers
- Forget exit animations
- Ignore performance metrics
- Delay essential content

---

## Animation Checklist

### Pre-Implementation

- [ ] Animation serves a purpose
- [ ] Duration appropriate for action
- [ ] Easing matches motion intent
- [ ] Performance impact assessed

### Implementation

- [ ] Uses GPU-accelerated properties
- [ ] prefers-reduced-motion respected
- [ ] Works on target devices
- [ ] No layout thrashing

### Quality Check

- [ ] Feels natural and responsive
- [ ] Doesn't delay user
- [ ] Consistent with design system
- [ ] Accessible to all users
