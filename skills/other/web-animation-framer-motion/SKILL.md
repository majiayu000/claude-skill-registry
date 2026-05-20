---
name: web-animation-framer-motion
description: Motion (formerly Framer Motion) animation patterns - motion components, variants, gestures, layout animations, scroll-linked animations, accessibility
---

# Motion Animation Patterns

> **Quick Guide:** Use Motion (formerly Framer Motion) for declarative React animations. motion components for basic animations, variants for orchestrated sequences, AnimatePresence for exit animations, layout/layoutId for FLIP animations, useScroll/useInView for scroll-triggered effects.

> **v11+ Note:** The package has been renamed from `framer-motion` to `motion`. Import from `"motion/react"` instead of `"framer-motion"`. Both packages are supported during migration.

> **v12 Note (Current: v12.26+):** New features include `usePageInView` for background tab detection, enhanced `stagger()` with `from`/`ease` options, `resize()` function, and `.stop()`/`.cancel()` on drag controls.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap exiting components in AnimatePresence for exit animations to work)**

**(You MUST provide unique `key` prop to direct children of AnimatePresence)**

**(You MUST animate transform properties (x, y, scale, rotate, opacity) for GPU-accelerated performance)**

**(You MUST respect reduced motion preferences using MotionConfig or useReducedMotion)**

**(You MUST use named constants for all animation timing values - NO magic numbers)**

</critical_requirements>

---

**Auto-detection:** Motion, Framer Motion, motion.div, motion.button, AnimatePresence, useAnimation, useScroll, useInView, usePageInView, variants, whileHover, whileTap, layoutId, spring, tween, stagger, "motion/react", "framer-motion"

**When to use:**

- Animating component enter/exit/presence
- Orchestrating complex multi-element animations with variants
- Implementing gesture-based interactions (hover, tap, drag)
- Creating scroll-triggered or scroll-linked animations
- Animating layout changes and shared element transitions
- Building micro-interactions and UI feedback

**Key patterns covered:**

- motion components and animation props (initial, animate, exit, transition)
- Variants for reusable, orchestrated animations
- AnimatePresence for exit animations
- Gesture props (whileHover, whileTap, whileDrag, drag)
- Layout animations (layout prop, layoutId)
- Scroll animations (useScroll, useInView, whileInView)
- Spring and tween transitions
- useAnimation for imperative control
- Reduced motion accessibility
- v12: usePageInView, enhanced stagger(), resize()

**When NOT to use:**

- Simple CSS transitions (use CSS transitions instead)
- Complex timeline-based animations requiring frame-level control (consider GSAP)
- Performance-critical animations on low-powered devices without careful optimization

**Package Migration (v11+):**

```bash
# Migrate from framer-motion to motion
npm uninstall framer-motion
npm install motion

# Update imports
# Old: import { motion } from "framer-motion"
# New: import { motion } from "motion/react"
```

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

Framer Motion is a declarative animation library for React that makes animations feel natural and accessible. It uses a physics-based approach with spring animations as defaults, creating fluid motion that matches real-world expectations.

**Core principles:**

1. **Declarative over imperative** - Describe what the animation should look like, not how to achieve it
2. **Props over keyframes** - Use `initial`, `animate`, `exit` props instead of CSS keyframes
3. **Variants for orchestration** - Group related animations and control timing with parent-child relationships
4. **Performance through transforms** - Animate GPU-accelerated properties (transform, opacity) for smooth 60fps
5. **Accessibility built-in** - Respect user preferences for reduced motion

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Motion Components

Motion components are the foundation of Framer Motion. Prefix any HTML or SVG element with `motion.` to make it animatable.

#### Animation Props

```typescript
// v11+ (recommended - motion package)
import { motion } from "motion/react";
// Legacy (framer-motion package - still works during migration)
// import { motion } from "framer-motion";

const FADE_DURATION_S = 0.3;
const SLIDE_DISTANCE_PX = 20;

// Basic animation with named constants
export const FadeIn = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: SLIDE_DISTANCE_PX }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: FADE_DURATION_S }}
    >
      {children}
    </motion.div>
  );
};
```

**Why good:** Named constants for timing values improve maintainability, declarative props clearly express animation intent, transform properties (y) are GPU-accelerated

```typescript
// Bad Example - Magic numbers and layout properties
export const FadeIn = ({ children }) => {
  return (
    <motion.div
      initial={{ opacity: 0, top: 20 }}  // Bad: 'top' triggers layout
      animate={{ opacity: 1, top: 0 }}
      transition={{ duration: 0.3 }}      // Bad: magic number
    >
      {children}
    </motion.div>
  );
};
```

**Why bad:** Magic numbers make timing changes error-prone, animating `top` triggers expensive layout recalculations instead of using GPU-accelerated `y`

---

### Pattern 2: Variants for Orchestrated Animations

Variants define reusable animation states and enable parent-child orchestration with staggered timing.

#### Defining Variants

```typescript
import { motion, type Variants } from "framer-motion";

const STAGGER_DELAY_S = 0.1;
const ITEM_SLIDE_DISTANCE_PX = 20;
const ITEM_DURATION_S = 0.4;

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: STAGGER_DELAY_S,
    },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: ITEM_SLIDE_DISTANCE_PX },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: ITEM_DURATION_S },
  },
};

export const StaggeredList = ({ items }: { items: string[] }) => {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {items.map((item) => (
        <motion.li key={item} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
};
```

**Why good:** Variants are reusable across components, staggerChildren creates natural cascading effect, children automatically inherit animation state from parent, named constants for all timing

**When to use:** Lists with staggered entry, multi-step animations, coordinated UI transitions

---

### Pattern 3: AnimatePresence for Exit Animations

AnimatePresence enables exit animations for components being removed from the React tree.

#### Basic Exit Animation

```typescript
import { AnimatePresence, motion } from "framer-motion";

const MODAL_DURATION_S = 0.2;
const MODAL_SCALE_HIDDEN = 0.95;

type ModalProps = {
  isOpen: boolean;
  onClose: () => void;
  children: React.ReactNode;
};

export const Modal = ({ isOpen, onClose, children }: ModalProps) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          key="modal"
          initial={{ opacity: 0, scale: MODAL_SCALE_HIDDEN }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: MODAL_SCALE_HIDDEN }}
          transition={{ duration: MODAL_DURATION_S }}
          role="dialog"
          aria-modal="true"
        >
          {children}
          <button onClick={onClose} aria-label="Close modal">
            Close
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

**Why good:** Exit animation plays before component unmounts, unique key ensures AnimatePresence tracks the element, scale and opacity are GPU-accelerated, accessibility attributes included

#### Animation Modes

```typescript
// mode="wait" - wait for exit before enter
<AnimatePresence mode="wait">
  <motion.div key={currentPage}>
    {/* New page waits for old page to exit */}
  </motion.div>
</AnimatePresence>

// mode="sync" (default) - enter and exit simultaneously
<AnimatePresence mode="sync">
  {/* Elements animate at the same time */}
</AnimatePresence>

// mode="popLayout" - for shared layout transitions
<AnimatePresence mode="popLayout">
  {/* Animates layout changes during exit */}
</AnimatePresence>
```

**When to use:** Page transitions (mode="wait"), modals, toasts, conditional UI elements

---

### Pattern 4: Gesture Animations

Gesture props enable hover, tap, focus, and drag interactions.

#### Hover and Tap States

```typescript
import { motion } from "framer-motion";

const HOVER_SCALE = 1.05;
const TAP_SCALE = 0.95;
const GESTURE_SPRING = { type: "spring" as const, stiffness: 400, damping: 17 };

type ButtonProps = React.ComponentProps<typeof motion.button>;

export const AnimatedButton = ({ children, ...props }: ButtonProps) => {
  return (
    <motion.button
      whileHover={{ scale: HOVER_SCALE }}
      whileTap={{ scale: TAP_SCALE }}
      transition={GESTURE_SPRING}
      {...props}
    >
      {children}
    </motion.button>
  );
};
```

**Why good:** Spring physics create natural bounce, scale transforms are GPU-accelerated, gesture states are declarative

#### Drag Interactions

```typescript
import { motion } from "framer-motion";

const DRAG_ELASTIC = 0.2;

export const DraggableCard = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div
      drag
      dragConstraints={{ left: 0, right: 0, top: 0, bottom: 0 }}
      dragElastic={DRAG_ELASTIC}
      whileDrag={{ scale: 1.1, cursor: "grabbing" }}
    >
      {children}
    </motion.div>
  );
};
```

**When to use:** Interactive buttons, draggable elements, swipeable cards, hover effects

---

### Pattern 5: Layout Animations

The `layout` prop animates layout changes automatically using FLIP technique.

#### Basic Layout Animation

```typescript
import { motion } from "framer-motion";

const LAYOUT_SPRING = { type: "spring" as const, stiffness: 500, damping: 30 };

type ExpandableCardProps = {
  isExpanded: boolean;
  onToggle: () => void;
};

export const ExpandableCard = ({ isExpanded, onToggle }: ExpandableCardProps) => {
  return (
    <motion.div
      layout
      transition={LAYOUT_SPRING}
      onClick={onToggle}
      style={{ width: isExpanded ? 300 : 150 }}
    >
      <motion.h2 layout="position">Title</motion.h2>
      {isExpanded && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          Expanded content here
        </motion.p>
      )}
    </motion.div>
  );
};
```

**Why good:** `layout` prop handles FLIP calculations automatically, `layout="position"` on children prevents distortion, spring transition feels natural

#### Shared Element Transitions with layoutId

```typescript
import { motion, AnimatePresence } from "framer-motion";

type TabsProps = {
  tabs: string[];
  activeTab: string;
  onTabChange: (tab: string) => void;
};

export const Tabs = ({ tabs, activeTab, onTabChange }: TabsProps) => {
  return (
    <div role="tablist">
      {tabs.map((tab) => (
        <button
          key={tab}
          role="tab"
          aria-selected={activeTab === tab}
          onClick={() => onTabChange(tab)}
        >
          {tab}
          {activeTab === tab && (
            <motion.div
              layoutId="tab-underline"
              style={{ height: 2, background: "currentColor" }}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </button>
      ))}
    </div>
  );
};
```

**Why good:** `layoutId` creates seamless shared element transitions, underline smoothly slides between tabs, ARIA attributes for accessibility

**When to use:** Tabs, expanding cards, shared element transitions, list reordering

---

### Pattern 6: Scroll-Triggered Animations

Use `whileInView` for scroll-triggered animations and `useScroll` for scroll-linked effects.

#### Scroll-Triggered with whileInView

```typescript
import { motion } from "framer-motion";

const REVEAL_DURATION_S = 0.6;
const REVEAL_DISTANCE_PX = 50;

export const ScrollReveal = ({ children }: { children: React.ReactNode }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: REVEAL_DISTANCE_PX }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: REVEAL_DURATION_S }}
    >
      {children}
    </motion.div>
  );
};
```

**Why good:** `viewport.once` ensures animation only plays once, negative margin triggers animation before element fully enters viewport, declarative scroll trigger

#### Scroll-Linked with useScroll

```typescript
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

const PARALLAX_RANGE = [-100, 100];

export const ParallaxSection = ({ children }: { children: React.ReactNode }) => {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], PARALLAX_RANGE);

  return (
    <div ref={ref}>
      <motion.div style={{ y }}>
        {children}
      </motion.div>
    </div>
  );
};
```

**Why good:** `useTransform` maps scroll progress to animation values, offset controls when tracking starts/ends, motion values update without React re-renders

#### useInView for Custom Logic

```typescript
import { useInView } from "framer-motion";
import { useRef, useEffect } from "react";

export const LazyVideo = ({ src }: { src: string }) => {
  const ref = useRef<HTMLVideoElement>(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (isInView && ref.current) {
      ref.current.play();
    }
  }, [isInView]);

  return <video ref={ref} src={src} />;
};
```

**When to use:** Scroll reveal effects, parallax, progress indicators, lazy loading

---

### Pattern 7: Spring and Tween Transitions

Configure transition physics for different animation feels.

#### Spring Transitions

```typescript
import { motion } from "framer-motion";

// Bouncy spring for playful interactions
const BOUNCY_SPRING = {
  type: "spring" as const,
  stiffness: 300,
  damping: 10,
};

// Snappy spring for responsive UI
const SNAPPY_SPRING = {
  type: "spring" as const,
  stiffness: 500,
  damping: 30,
};

// Gentle spring for subtle movements
const GENTLE_SPRING = {
  type: "spring" as const,
  stiffness: 100,
  damping: 20,
};
```

#### Tween Transitions

```typescript
// Linear for constant speed
const LINEAR_TWEEN = {
  type: "tween" as const,
  duration: 0.3,
  ease: "linear",
};

// Ease out for entering elements
const EASE_OUT_TWEEN = {
  type: "tween" as const,
  duration: 0.3,
  ease: "easeOut",
};

// Ease in for exiting elements
const EASE_IN_TWEEN = {
  type: "tween" as const,
  duration: 0.2,
  ease: "easeIn",
};

// Custom cubic bezier
const CUSTOM_TWEEN = {
  type: "tween" as const,
  duration: 0.4,
  ease: [0.25, 0.1, 0.25, 1],
};
```

**When to use:** Springs for interactive elements (buttons, cards), tweens for UI transitions (modals, page changes)

---

### Pattern 8: useAnimation for Imperative Control

Use `useAnimation` when you need programmatic control over animations.

```typescript
import { motion, useAnimation } from "framer-motion";
import { useEffect } from "react";

const SHAKE_DISTANCE_PX = 10;
const SHAKE_DURATION_S = 0.1;
const SHAKE_TIMES = 3;

export const ShakeOnError = ({
  hasError,
  children,
}: {
  hasError: boolean;
  children: React.ReactNode;
}) => {
  const controls = useAnimation();

  useEffect(() => {
    if (hasError) {
      controls.start({
        x: [0, -SHAKE_DISTANCE_PX, SHAKE_DISTANCE_PX, -SHAKE_DISTANCE_PX, 0],
        transition: { duration: SHAKE_DURATION_S * SHAKE_TIMES },
      });
    }
  }, [hasError, controls]);

  return <motion.div animate={controls}>{children}</motion.div>;
};
```

**Why good:** Imperative control for complex sequencing, keyframe array creates shake effect, effect triggers on error state change

**When to use:** Animations triggered by external events, complex sequences, animations that need to be started/stopped programmatically

---

### Pattern 9: Reduced Motion Accessibility

Always respect user preferences for reduced motion.

#### Site-Wide with MotionConfig

```typescript
import { MotionConfig } from "framer-motion";

export const App = ({ children }: { children: React.ReactNode }) => {
  return (
    <MotionConfig reducedMotion="user">
      {children}
    </MotionConfig>
  );
};
```

**Why good:** Automatically disables transform/layout animations when reduced motion is preferred, opacity and color animations still work

#### Custom Handling with useReducedMotion

```typescript
import { motion, useReducedMotion } from "framer-motion";

const SLIDE_DISTANCE_PX = 50;
const SLIDE_DURATION_S = 0.5;
const FADE_DURATION_S = 0.3;

export const AccessibleReveal = ({ children }: { children: React.ReactNode }) => {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={{ opacity: 0, y: shouldReduceMotion ? 0 : SLIDE_DISTANCE_PX }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: shouldReduceMotion ? FADE_DURATION_S : SLIDE_DURATION_S,
      }}
    >
      {children}
    </motion.div>
  );
};
```

**Why good:** Provides graceful degradation instead of no animation, maintains visual feedback while respecting preferences, hook reactively updates if setting changes

**When to use:** Always - reduced motion support is a requirement for accessible applications

---

### Pattern 10: v12 Features

New features introduced in Motion v12.

#### usePageInView Hook (v12.19+)

Detect when the page/tab is visible to pause animations or videos in background tabs.

```typescript
import { usePageInView } from "motion/react";
import { useRef, useEffect } from "react";

export const AutoPausingVideo = ({ src }: { src: string }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const isPageVisible = usePageInView();

  useEffect(() => {
    if (!videoRef.current) return;

    if (isPageVisible) {
      videoRef.current.play();
    } else {
      videoRef.current.pause();
    }
  }, [isPageVisible]);

  return <video ref={videoRef} src={src} muted loop />;
};
```

**Why good:** Automatically pauses resource-intensive animations when user switches tabs, improves performance and battery life

#### Enhanced stagger() with from and ease (v12+)

The `stagger()` function now supports staggering from any child and eased staggering.

```typescript
import { motion, stagger, type Variants } from "motion/react";

const STAGGER_DELAY_S = 0.05;

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      // Stagger from center with easing
      staggerChildren: stagger(STAGGER_DELAY_S, {
        from: "center",
        ease: "easeOut",
      }),
    },
  },
};

// Alternative: stagger from a specific index
const fromIndexVariants: Variants = {
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: stagger(STAGGER_DELAY_S, {
        from: 3, // Start from 4th child (0-indexed)
      }),
    },
  },
};

// Options: "first" (default), "center", "last", or number (index)
```

**Why good:** Enables ripple-out effects from center or specific elements, eased staggering creates more polished animations

#### Drag Controls with stop/cancel (v12+)

```typescript
import { motion, useDragControls } from "motion/react";

export const CancellableDrag = () => {
  const controls = useDragControls();

  const handleEmergencyStop = () => {
    controls.stop(); // Stop drag immediately
    // or controls.cancel(); // Cancel and revert
  };

  return (
    <motion.div
      drag
      dragControls={controls}
      onDragEnd={() => console.log("Drag ended")}
    >
      Drag me
    </motion.div>
  );
};
```

**When to use:** When you need programmatic control to stop or cancel drag operations

</patterns>

---

<integration>

## Integration Guide

**Framer Motion is React-specific.** It provides animation primitives that work with any React component architecture and styling solution.

**Works with:**

- **React components**: Wrap any component with motion() or use motion.element
- **Any styling solution**: Apply styles via className prop, motion handles animation
- **Form libraries**: Animate form validation states, error messages
- **Routing solutions**: Use AnimatePresence for page transitions

**Animation state is separate from React state:**

- Motion values update without React re-renders
- Use `useAnimation` for imperative control from effects
- Variants propagate animation state to children automatically

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap exiting components in AnimatePresence for exit animations to work)**

**(You MUST provide unique `key` prop to direct children of AnimatePresence)**

**(You MUST animate transform properties (x, y, scale, rotate, opacity) for GPU-accelerated performance)**

**(You MUST respect reduced motion preferences using MotionConfig or useReducedMotion)**

**(You MUST use named constants for all animation timing values - NO magic numbers)**

**Failure to follow these rules will break exit animations, cause performance issues, and create inaccessible experiences.**

</critical_reminders>
