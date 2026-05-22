---
name: bellog-animations
description: Provides Framer Motion animation patterns and best practices specific to the Bellog blog project. Triggers when implementing animated components or interactions.
---

# Bellog Animation Patterns

This skill provides the animation patterns and best practices used throughout the Bellog blog project.

## Core Animation Principles

1. **Organic movement** - Use easing curves, never linear
2. **Stagger for rhythm** - Create visual flow with staggered animations
3. **Living elements** - Ambient animations that breathe life
4. **Consistent timing** - Follow project timing standards

## Animation Timing Standards

```typescript
// Interaction timings
const INTERACTION_FAST = 0.2;    // Button press, hover start
const INTERACTION_NORMAL = 0.3;  // Standard hover effects
const INTERACTION_SLOW = 0.5;    // Modal open, drawer slide

// Transition timings
const TRANSITION_FAST = 0.3;     // Quick state changes
const TRANSITION_NORMAL = 0.4;   // Page transitions (standard)
const TRANSITION_SLOW = 0.6;     // Heavy content transitions

// Ambient timings
const AMBIENT_SLOW = 3;          // Slow blob movement
const AMBIENT_NORMAL = 4;        // Standard blob rhythm
const AMBIENT_FAST = 5;          // Faster ambient motion
```

## Pattern 1: Stagger Children

Use for lists, grids, and groups of elements.

**When to use:** Animating multiple items that should appear in sequence

**Example from Intro.tsx:**
```typescript
const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,  // 100ms delay between each child
      delayChildren: 0.2      // Start after 200ms
    }
  }
};

const item = {
  hidden: { y: 20, opacity: 0 },
  show: {
    y: 0,
    opacity: 1,
    transition: {
      duration: 0.5,
      ease: "easeInOut"
    }
  }
};

// Usage
<motion.div
  variants={container}
  initial="hidden"
  animate="show"
>
  {items.map(item => (
    <motion.div key={item.id} variants={item}>
      {item.content}
    </motion.div>
  ))}
</motion.div>
```

## Pattern 2: Living Blob Animations

Use for decorative elements, background shapes, ambient animations.

**When to use:** Creating organic, perpetual movement

**Example from Intro.tsx:**
```typescript
const blobVariants = {
  initial: {
    scale: 1,
    x: 0,
    y: 0
  },
  hover: {
    scale: [1, 1.2, 0.9, 1.1, 1],    // Keyframes
    x: [0, 20, -10, 5, 0],
    y: [0, -15, 10, -5, 0],
    transition: {
      duration: 4,
      repeat: Infinity,
      repeatType: "mirror",
      ease: "easeInOut"
    }
  }
};

// Multiple blobs with different rhythms
const blob1 = { duration: 3, ... };
const blob2 = { duration: 4.5, ... };
const blob3 = { duration: 5.2, ... };
```

**Best practices:**
- Layer multiple blobs with different durations for organic feel
- Use `repeatType: "mirror"` for smooth loops
- Keep movements subtle (scale: 0.9-1.2 range)
- Use blur and opacity to create depth

## Pattern 3: Page Transitions

Use for route changes, content swapping.

**When to use:** Navigating between pages or major content changes

**Example from template.tsx:**
```typescript
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: 20 }}
  transition={{
    ease: "easeInOut",
    duration: 0.4
  }}
>
  {children}
</motion.div>
```

**Variations:**
```typescript
// Fade only
initial={{ opacity: 0 }}
animate={{ opacity: 1 }}

// Slide from right
initial={{ opacity: 0, x: 20 }}
animate={{ opacity: 1, x: 0 }}

// Scale + fade
initial={{ opacity: 0, scale: 0.95 }}
animate={{ opacity: 1, scale: 1 }}
```

## Pattern 4: Hover Interactions

Use for buttons, cards, clickable elements.

**When to use:** Adding interactivity to user-actionable elements

```typescript
const cardVariants = {
  initial: { scale: 1 },
  hover: {
    scale: 1.02,
    transition: {
      duration: 0.3,
      ease: "easeInOut"
    }
  },
  tap: {
    scale: 0.98
  }
};

<motion.div
  variants={cardVariants}
  initial="initial"
  whileHover="hover"
  whileTap="tap"
>
```

**Common hover patterns:**
- **Cards:** scale(1.02) + shadow increase
- **Buttons:** scale(1.05) + slight lift
- **Icons:** rotate or scale
- **Links:** underline expand

## Pattern 5: Scroll-Based Animations

Use for parallax, fade-ins, progress indicators.

**When to use:** Animations triggered by scroll position

```typescript
import { useScroll, useTransform } from "framer-motion";

const { scrollYProgress } = useScroll();
const opacity = useTransform(scrollYProgress, [0, 0.5], [0, 1]);
const y = useTransform(scrollYProgress, [0, 0.5], [50, 0]);

<motion.div style={{ opacity, y }}>
  {/* Content */}
</motion.div>
```

**Example: Progress bar**
```typescript
const { scrollYProgress } = useScroll();

<motion.div
  style={{ scaleX: scrollYProgress }}
  className="fixed top-0 left-0 right-0 h-1 bg-primary origin-left"
/>
```

## Pattern 6: Enter/Exit Animations

Use with AnimatePresence for conditional rendering.

**When to use:** Elements that appear and disappear

```typescript
import { AnimatePresence } from "framer-motion";

const variants = {
  hidden: { opacity: 0, y: -10 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 }
};

<AnimatePresence>
  {isVisible && (
    <motion.div
      variants={variants}
      initial="hidden"
      animate="visible"
      exit="exit"
      transition={{ duration: 0.3 }}
    >
      {content}
    </motion.div>
  )}
</AnimatePresence>
```

## Easing Functions

**Use these, not "linear":**

```typescript
// Bellog standard
ease: "easeInOut"  // Default for most animations

// Other options
ease: "easeOut"    // For entrances
ease: "easeIn"     // For exits
ease: [0.43, 0.13, 0.23, 0.96]  // Custom cubic-bezier
```

## Animation Checklist

Before finalizing animations:

- [ ] Timing follows project standards (0.2-0.5s for interactions)
- [ ] Uses `variants` pattern (not inline animation props)
- [ ] Easing is `easeInOut` or appropriate alternative
- [ ] No linear easing
- [ ] Stagger delay appropriate for number of items
- [ ] Exit animations defined if using AnimatePresence
- [ ] Performance: No layout thrashing (avoid animating width/height)
- [ ] Accessibility: Respects `prefers-reduced-motion` if critical

## Performance Tips

1. **Transform over top/left:**
   ```typescript
   // ✅ Good (GPU accelerated)
   { x: 100 }
   { translateX: "100px" }
   { scale: 1.1 }

   // ❌ Bad (layout recalc)
   { left: 100 }
   { width: "100%" }
   ```

2. **Will-change hint:**
   ```typescript
   style={{ willChange: "transform" }}
   ```

3. **Layout animations (use sparingly):**
   ```typescript
   <motion.div layout>
   ```

## Reduced Motion

Respect user preferences:

```typescript
import { useReducedMotion } from "framer-motion";

const shouldReduceMotion = useReducedMotion();

const variants = {
  hidden: { opacity: 0, y: shouldReduceMotion ? 0 : 20 },
  visible: { opacity: 1, y: 0 }
};
```

## Common Mistakes to Avoid

❌ **Don't:** Inline animation props
```typescript
<motion.div animate={{ opacity: 1 }} initial={{ opacity: 0 }}>
```

✅ **Do:** Use variants
```typescript
const variants = { hidden: { opacity: 0 }, visible: { opacity: 1 } };
<motion.div variants={variants} initial="hidden" animate="visible">
```

---

❌ **Don't:** Linear easing
```typescript
transition={{ duration: 0.3, ease: "linear" }}
```

✅ **Do:** Use curves
```typescript
transition={{ duration: 0.3, ease: "easeInOut" }}
```

---

❌ **Don't:** Animate width/height directly
```typescript
animate={{ width: "100%" }}
```

✅ **Do:** Use scale or layout
```typescript
animate={{ scaleX: 1 }}
// or
<motion.div layout>
```

## Quick Reference

```typescript
// Standard fade + slide in
{ initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 } }

// Standard hover
{ whileHover: { scale: 1.02 }, transition: { duration: 0.3 } }

// Standard stagger
{
  variants: {
    container: { transition: { staggerChildren: 0.1 } },
    item: { hidden: { y: 20, opacity: 0 }, show: { y: 0, opacity: 1 } }
  }
}

// Standard exit
{ exit: { opacity: 0, y: -10 }, transition: { duration: 0.2 } }
```

Remember: Animations should enhance the experience, not distract from it. When in doubt, keep it subtle and fast.
