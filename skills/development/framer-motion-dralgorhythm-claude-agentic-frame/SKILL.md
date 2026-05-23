---
name: framer-motion
description: Framer Motion animation patterns. Use when adding animations, transitions, gestures, or layout animations to React applications. Covers performance optimization and accessibility.
---

# Framer Motion

> **Platform:** Web only. For mobile animations, see the **react-native-reanimated** skill.

## Overview

Animation patterns for React using Framer Motion 12.x. Provides declarative animations, gesture handling, layout transitions, and page animations with performance and accessibility built-in.

**Install**: `pnpm add framer-motion`

## Workflows

**Adding animations:**
1. [ ] Import motion component: `import { motion } from 'framer-motion'`
2. [ ] Replace element with motion variant: `<div>` → `<motion.div>`
3. [ ] Add animation props: initial, animate, transition
4. [ ] Test with reduced motion enabled
5. [ ] Verify 60fps performance in DevTools

**Complex sequences:**
1. [ ] Define variants object with named states
2. [ ] Apply variants to parent and children
3. [ ] Use orchestration props: staggerChildren, delayChildren
4. [ ] Wrap with AnimatePresence if unmounting
5. [ ] Add accessibility fallbacks

## Animation Primitives

### Basic Motion Components

```tsx
import { motion } from 'framer-motion';

// Simple fade-in
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>

// Slide up with fade
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
>
  Content
</motion.div>
```

### Variants for Complex Animations

```tsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  },
  exit: { opacity: 0, transition: { duration: 0.15 } }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};

<motion.ul variants={containerVariants} initial="hidden" animate="visible" exit="exit">
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>
```

## Transitions

### Standard Timings

```tsx
// Use consistent timing across app
const timing = {
  fast: 0.15,    // Micro-interactions
  normal: 0.3,   // Default animations
  slow: 0.5,     // Page transitions
  stagger: 0.05  // Between items
};

// Duration and easing
<motion.div
  animate={{ x: 100 }}
  transition={{ duration: timing.normal, ease: 'easeInOut' }}
/>

// Spring physics (preferred for natural motion)
<motion.div
  animate={{ scale: 1.2 }}
  transition={{ type: 'spring', stiffness: 300, damping: 20 }}
/>

// Keyframes
<motion.div
  animate={{ scale: [1, 1.2, 1] }}
  transition={{ duration: 0.5, times: [0, 0.5, 1] }}
/>

// Repeat
<motion.div
  animate={{ rotate: 360 }}
  transition={{ duration: 2, repeat: Infinity, repeatType: 'loop' }}
/>
```

## Gestures

### Hover, Tap, Focus

```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  whileFocus={{ outline: '2px solid blue' }}
  transition={{ duration: 0.15 }}
>
  Click me
</motion.button>

// Complex hover state
<motion.div
  initial="rest"
  whileHover="hover"
  variants={{
    rest: { scale: 1, boxShadow: '0 2px 4px rgba(0,0,0,0.1)' },
    hover: { scale: 1.02, boxShadow: '0 8px 16px rgba(0,0,0,0.15)' }
  }}
>
  Card content
</motion.div>
```

### Drag with Constraints

```tsx
import { useRef } from 'react';

const constraintsRef = useRef(null);

<div ref={constraintsRef} style={{ width: 400, height: 400 }}>
  <motion.div
    drag
    dragConstraints={constraintsRef}
    dragElastic={0.1}
    whileDrag={{ scale: 1.1, cursor: 'grabbing' }}
  >
    Drag me
  </motion.div>
</div>

// Drag along single axis
<motion.div drag="x" dragConstraints={{ left: -100, right: 100 }}>
  Slide horizontal
</motion.div>
```

## Layout Animations

### Automatic Layout Animation

```tsx
// Auto-animates position/size changes
<motion.div layout>
  {expanded ? <FullContent /> : <Summary />}
</motion.div>

// Shared element transitions
<motion.div layoutId="card-123">
  <motion.img layoutId="card-image-123" src={image} />
</motion.div>

// Coordinate sibling animations
import { LayoutGroup } from 'framer-motion';

<LayoutGroup>
  {items.map(item => (
    <motion.div key={item.id} layout>
      {item.content}
    </motion.div>
  ))}
</LayoutGroup>
```

## Page Transitions

### AnimatePresence for Exit Animations

```tsx
import { AnimatePresence } from 'framer-motion';

// Single element
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>

// Route transitions (with React Router)
import { useLocation } from 'react-router-dom';

const location = useLocation();

<AnimatePresence mode="wait" initial={false}>
  <motion.div
    key={location.pathname}
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    transition={{ duration: 0.3 }}
  >
    <Routes location={location}>
      {/* routes */}
    </Routes>
  </motion.div>
</AnimatePresence>
```

## Stagger Patterns

```tsx
// Parent orchestration
const listVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 }
};

<motion.ul variants={listVariants} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.name}
    </motion.li>
  ))}
</motion.ul>

// Custom stagger with useAnimate
import { useAnimate, stagger } from 'framer-motion';

const [scope, animate] = useAnimate();

useEffect(() => {
  animate('.item', { opacity: 1 }, { delay: stagger(0.05) });
}, []);
```

## Performance

### GPU-Accelerated Properties

```tsx
// ✅ FAST: Only transform and opacity
<motion.div
  animate={{
    opacity: 1,
    scale: 1.2,
    x: 100,
    rotate: 45
  }}
/>

// ❌ SLOW: Layout-affecting properties
<motion.div
  animate={{
    width: 300,    // Triggers layout
    height: 200,   // Triggers layout
    top: 50        // Triggers layout
  }}
/>
```

### willChange Optimization

```tsx
// Hint browser before expensive animations
<motion.div
  style={{ willChange: 'transform' }}
  whileHover={{ scale: 1.1 }}
>
  Content
</motion.div>

// Auto willChange with layout animations
<motion.div layout transition={{ layout: { duration: 0.3 } }}>
  Content
</motion.div>
```

## Accessibility

### Reduced Motion Support

```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      Content
    </motion.div>
  );
}

// Disable animations completely
const prefersReducedMotion = useReducedMotion();

<motion.div
  {...(prefersReducedMotion ? {} : {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    transition: { duration: 0.3 }
  })}
>
  Content
</motion.div>
```

### Focus Management

```tsx
// Maintain focus during animations
<AnimatePresence>
  {isOpen && (
    <motion.dialog
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      onAnimationComplete={() => {
        // Focus first input after enter animation
        dialogRef.current?.querySelector('input')?.focus();
      }}
    >
      <form>...</form>
    </motion.dialog>
  )}
</AnimatePresence>
```

## Scroll Animations

### useScroll and useInView

```tsx
import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { useRef } from 'react';

// Scroll progress indicator
function ScrollProgress() {
  const { scrollYProgress } = useScroll();

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-blue-600 origin-left"
      style={{ scaleX: scrollYProgress }}
    />
  );
}

// Parallax effect
function ParallaxSection() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  });

  const y = useTransform(scrollYProgress, [0, 1], [100, -100]);

  return (
    <div ref={ref}>
      <motion.div style={{ y }}>
        Parallax content
      </motion.div>
    </div>
  );
}

// Trigger animation when element enters viewport
function AnimateOnScroll({ children }: { children: React.ReactNode }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.5 }}
    >
      {children}
    </motion.div>
  );
}
```

## MotionConfig

### Global Animation Settings

```tsx
import { MotionConfig } from 'framer-motion';

// Apply global settings to all descendants
function App() {
  return (
    <MotionConfig
      reducedMotion="user"  // Respect prefers-reduced-motion
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <YourApp />
    </MotionConfig>
  );
}

// Override transitions for a section
function FastSection() {
  return (
    <MotionConfig transition={{ duration: 0.15 }}>
      <motion.div animate={{ scale: 1.1 }}>
        Uses fast transition
      </motion.div>
    </MotionConfig>
  );
}
```

## Best Practices

- **Use variants** for complex multi-step animations instead of inline objects
- **Prefer spring physics** over duration-based easing for natural motion
- **Only animate transform and opacity** for 60fps performance
- **Always test with reduced motion** enabled (System Preferences → Accessibility)
- **Use layoutId** for shared element transitions between routes/states
- **Wrap exit animations** in AnimatePresence with unique keys
- **Set willChange** on elements with frequent animations
- **Use staggerChildren** instead of manual delays for list animations
- **Combine layout + whileHover** for dynamic interactive layouts
- **Keep transitions under 500ms** for perceived performance

## Anti-Patterns

- ❌ Animating width/height directly (use scale + layout instead)
- ❌ Forgetting AnimatePresence around conditional renders
- ❌ Hardcoding timing values (use constants)
- ❌ Ignoring prefers-reduced-motion
- ❌ Animating non-GPU properties (top, left, width, height, margin)
- ❌ Using motion on every element (overhead for static content)
- ❌ Deep nesting of layout animations (performance hit)
- ❌ Missing keys on AnimatePresence children
- ❌ Using exit without AnimatePresence
- ❌ Animating during SSR (causes hydration mismatches)

## Feedback Loops

**Animation quality:**
```bash
# Check frame rate in Chrome DevTools
# Performance → Record → Look for dropped frames
# Target: 60fps (16.67ms per frame)
```

**Reduced motion test:**
```bash
# macOS: System Settings → Accessibility → Display → Reduce Motion
# Test all animations with this enabled
```

**Performance profiling:**
```tsx
// Use React DevTools Profiler
// Measure commit duration with/without animations
// Aim for <16ms commits
```
