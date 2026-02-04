---
name: framer-motion
description: Comprehensive Framer Motion animation library for React. Covers motion components, variants, gestures, page transitions, and scroll animations. Use when adding animations to React/Next.js applications.
---

# Framer Motion Skill

Production-ready animations for React applications.

## Quick Start

### Installation

```bash
npm install framer-motion
# or
pnpm add framer-motion
```

### Basic Usage

```tsx
import { motion } from "framer-motion";

// Simple animation
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>
```

## Core Concepts

| Concept | Guide |
|---------|-------|
| **Motion Component** | [reference/motion-component.md](reference/motion-component.md) |
| **Variants** | [reference/variants.md](reference/variants.md) |
| **Gestures** | [reference/gestures.md](reference/gestures.md) |
| **Hooks** | [reference/hooks.md](reference/hooks.md) |

## Examples

| Pattern | Guide |
|---------|-------|
| **Page Transitions** | [examples/page-transitions.md](examples/page-transitions.md) |
| **List Animations** | [examples/list-animations.md](examples/list-animations.md) |
| **Scroll Animations** | [examples/scroll-animations.md](examples/scroll-animations.md) |
| **Micro-interactions** | [examples/micro-interactions.md](examples/micro-interactions.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/page-transition.tsx](templates/page-transition.tsx) | Page transition wrapper |
| [templates/animated-list.tsx](templates/animated-list.tsx) | Animated list component |

## Quick Reference

### Basic Animation

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

### Hover & Tap

```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: "spring", stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>
```

### Variants

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

<motion.ul variants={container} initial="hidden" animate="show">
  {items.map(i => (
    <motion.li key={i} variants={item}>{i}</motion.li>
  ))}
</motion.ul>
```

### AnimatePresence (Exit Animations)

```tsx
import { AnimatePresence, motion } from "framer-motion";

<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

### Scroll Trigger

```tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ duration: 0.5 }}
>
  Animates when scrolled into view
</motion.div>
```

### Drag

```tsx
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  dragElastic={0.1}
>
  Drag me
</motion.div>
```

### Layout Animation

```tsx
<motion.div layout layoutId="shared-element">
  Content that animates when layout changes
</motion.div>
```

## Transition Types

```tsx
// Tween (default)
transition={{ duration: 0.3, ease: "easeOut" }}

// Spring
transition={{ type: "spring", stiffness: 300, damping: 20 }}

// Spring presets
transition={{ type: "spring", bounce: 0.25 }}

// Inertia (for drag)
transition={{ type: "inertia", velocity: 50 }}
```

## Easing Functions

```tsx
// Built-in easings
ease: "linear"
ease: "easeIn"
ease: "easeOut"
ease: "easeInOut"
ease: "circIn"
ease: "circOut"
ease: "circInOut"
ease: "backIn"
ease: "backOut"
ease: "backInOut"

// Custom cubic-bezier
ease: [0.17, 0.67, 0.83, 0.67]
```

## Reduced Motion

Always respect user preferences:

```tsx
import { motion, useReducedMotion } from "framer-motion";

function Component() {
  const prefersReducedMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: prefersReducedMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
    >
      Respects motion preferences
    </motion.div>
  );
}

// Or use media query
const variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
};

<motion.div
  variants={variants}
  initial="initial"
  animate="animate"
  className="motion-reduce:transition-none"
>
```

## Common Patterns

### Fade In Up

```tsx
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4 }
};

<motion.div {...fadeInUp}>Content</motion.div>
```

### Staggered List

```tsx
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

const item = {
  hidden: { opacity: 0, x: -20 },
  show: { opacity: 1, x: 0 }
};
```

### Modal

```tsx
<AnimatePresence>
  {isOpen && (
    <>
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/50"
        onClick={onClose}
      />
      {/* Modal */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="fixed inset-x-4 top-1/2 -translate-y-1/2 ..."
      >
        Modal content
      </motion.div>
    </>
  )}
</AnimatePresence>
```

### Accordion

```tsx
<motion.div
  initial={false}
  animate={{ height: isOpen ? "auto" : 0 }}
  transition={{ duration: 0.3, ease: "easeInOut" }}
  className="overflow-hidden"
>
  <div className="p-4">Accordion content</div>
</motion.div>
```

## Best Practices

1. **Use variants**: Cleaner code, easier orchestration
2. **Respect reduced motion**: Always check `useReducedMotion`
3. **Use `layout` sparingly**: Can be expensive, use only when needed
4. **Exit animations**: Wrap with `AnimatePresence`
5. **Spring for interactions**: More natural feel for hover/tap
6. **Tween for page transitions**: More predictable timing
7. **GPU-accelerated properties**: Prefer `opacity`, `scale`, `x`, `y` over `width`, `height`
