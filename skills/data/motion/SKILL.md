---
name: motion
description: >
  Motion animation library for React - essential patterns for components, transitions, gestures, and performance.
  Trigger: When animating React components, motion, whileHover, whileTap, layout animations, transitions.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## Core Patterns

### Basic Animation

```tsx
import { motion } from "motion/react"

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0 }}
  transition={{ duration: 0.3 }}
/>
```

### Gestures

```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  whileInView={{ opacity: 1 }}
/>
```

### Layout Animations

```tsx
// Auto-animate position/size changes
<motion.div
  layout
  layoutDependency={isOpen} // Performance: only measure when this changes
/>
```

Use for: expanding panels, grid reordering, responsive shifts, tab switching.

### Variants (Reusable States)

```tsx
const variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

<motion.div
  variants={variants}
  initial="hidden"
  animate="visible"
/>
```

### Stagger Children

```tsx
<motion.ul
  variants={{
    visible: { transition: { staggerChildren: 0.1 } }
  }}
  initial="hidden"
  animate="visible"
>
  {items.map(item => (
    <motion.li
      key={item.id}
      variants={{
        visible: { opacity: 1, x: 0 },
        hidden: { opacity: 0, x: -20 }
      }}
    />
  ))}
</motion.ul>
```

### Exit Animations

```tsx
import { AnimatePresence } from "motion/react"

<AnimatePresence>
  {isVisible && (
    <motion.div
      key="modal" // REQUIRED
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    />
  )}
</AnimatePresence>
```

### Scroll Triggers

```tsx
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.5 }}
/>
```

## Performance

### GPU-Accelerated Properties

✅ **Use:** `x`, `y`, `scale`, `rotate`, `opacity`  
❌ **Avoid:** `width`, `height`, `top`, `left`

```tsx
// ✅ Good
<motion.div animate={{ x: 100, scale: 1.2 }} />

// ❌ Bad - triggers layout
<motion.div animate={{ width: 200 }} />
```

### Motion Values (No Re-renders)

```tsx
import { useMotionValue } from "motion/react"

const x = useMotionValue(0)
x.set(100) // Updates without React re-render

return <motion.div style={{ x }} />
```

### Transition Types

| Type | Use Case | Example |
|------|----------|---------|
| `spring` | Natural, bouncy (default) | `{ type: "spring", stiffness: 100 }` |
| `tween` | Precise, duration-based | `{ type: "tween", duration: 0.5 }` |

## Common Mistakes

❌ **Missing key in AnimatePresence**
```tsx
<AnimatePresence>
  {show && <motion.div />} // Missing key!
</AnimatePresence>
```

✅ **Always add unique key**
```tsx
<AnimatePresence>
  {show && <motion.div key="unique" />}
</AnimatePresence>
```

❌ **Animating layout properties**
```tsx
<motion.div animate={{ width: 200 }} />
```

✅ **Use transforms**
```tsx
<motion.div animate={{ scaleX: 2 }} />
```

## Resources

- **Docs**: [motion.dev/docs/react](https://motion.dev/docs/react)
- **Context7**: `/websites/motion_dev_react`
