---
name: animation-motion
description: Create smooth animations and micro-interactions with Framer Motion and CSS. Covers enter/exit animations, gestures, scroll animations, loading states, and performance optimization. Use for polished UIs, interactive elements, and engaging user experiences.
---

# Animation & Motion Design

Create smooth, purposeful animations that enhance user experience.

## Instructions

1. **Animate with purpose** - Every animation should serve a function
2. **Keep it subtle** - 200-400ms for most UI transitions
3. **Respect reduced motion** - Honor user preferences
4. **Optimize performance** - Use transform and opacity
5. **Use consistent easing** - Create a motion language

## Framer Motion Basics

### Simple Animations

```tsx
import { motion } from 'framer-motion';

// Fade in on mount
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>

// Slide up with spring
<motion.div
  initial={{ y: 20, opacity: 0 }}
  animate={{ y: 0, opacity: 1 }}
  transition={{
    type: 'spring',
    stiffness: 300,
    damping: 30,
  }}
>
  Content
</motion.div>
```

### Exit Animations

```tsx
import { AnimatePresence, motion } from 'framer-motion';

function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Modal content */}
          <motion.div
            className="fixed inset-0 flex items-center justify-center"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### Gesture Animations

```tsx
import { motion } from 'framer-motion';

<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{ type: 'spring', stiffness: 400, damping: 17 }}
>
  Click me
</motion.button>

// Drag
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
  dragElastic={0.1}
  whileDrag={{ scale: 1.1 }}
>
  Drag me
</motion.div>
```

### List Animations

```tsx
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

function List({ items }) {
  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="show"
    >
      {items.map((data) => (
        <motion.li key={data.id} variants={item}>
          {data.title}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Layout Animations

```tsx
import { motion, LayoutGroup } from 'framer-motion';

function Tabs({ tabs, activeTab, onTabChange }) {
  return (
    <LayoutGroup>
      <div className="flex space-x-2">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className="relative px-4 py-2"
          >
            {tab.label}
            {activeTab === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-blue-100 rounded-lg"
                style={{ zIndex: -1 }}
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            )}
          </button>
        ))}
      </div>
    </LayoutGroup>
  );
}
```

### Scroll Animations

```tsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxHero() {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, 150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  return (
    <motion.div
      style={{ y, opacity }}
      className="h-screen flex items-center justify-center"
    >
      <h1 className="text-6xl font-bold">Welcome</h1>
    </motion.div>
  );
}

// Scroll-triggered animation
import { useInView } from 'framer-motion';

function FadeInSection({ children }) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

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

## CSS Animations

### Keyframe Animations

```css
/* Tailwind config */
animation: {
  'fade-in': 'fadeIn 0.3s ease-out',
  'slide-up': 'slideUp 0.3s ease-out',
  'spin-slow': 'spin 3s linear infinite',
  'pulse-subtle': 'pulse 2s ease-in-out infinite',
},
keyframes: {
  fadeIn: {
    '0%': { opacity: '0' },
    '100%': { opacity: '1' },
  },
  slideUp: {
    '0%': { transform: 'translateY(10px)', opacity: '0' },
    '100%': { transform: 'translateY(0)', opacity: '1' },
  },
}
```

### Transition Classes

```tsx
// Hover transitions
<button className="
  transition-all duration-200 ease-out
  hover:scale-105 hover:shadow-lg
  active:scale-95
">
  Click me
</button>

// Color transitions
<div className="
  transition-colors duration-300
  bg-gray-100 hover:bg-gray-200
  dark:bg-gray-800 dark:hover:bg-gray-700
">
  Content
</div>
```

## Loading States

### Skeleton Loading

```tsx
function SkeletonCard() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-200 rounded-lg" />
      <div className="mt-4 space-y-3">
        <div className="h-4 bg-gray-200 rounded w-3/4" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
      </div>
    </div>
  );
}
```

### Spinner Component

```tsx
function Spinner({ size = 'md' }) {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  return (
    <svg
      className={`animate-spin ${sizes[size]} text-blue-600`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>
  );
}
```

## Reduced Motion Support

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

// CSS approach
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Performance Tips

1. **Animate transform and opacity only** - GPU accelerated
2. **Use `will-change` sparingly** - For complex animations
3. **Avoid layout thrashing** - Don't animate width/height
4. **Use `AnimatePresence` mode="wait"** - Prevent animation overlap
5. **Lazy load animations** - For below-fold content

```tsx
// GPU-optimized animation
<motion.div
  animate={{ x: 100 }}  // Good: transform
  // animate={{ left: 100 }}  // Bad: layout property
/>

// will-change for complex animations
<div style={{ willChange: 'transform' }}>
  Heavy animation here
</div>
```

## Best Practices

1. **200-400ms for transitions** - Feels responsive
2. **Spring for interactive elements** - Natural feel
3. **Ease-out for enter** - Elements arrive and settle
4. **Ease-in for exit** - Elements accelerate away
5. **Stagger lists** - 50-100ms between items
6. **Match motion to meaning** - Slide for navigation, fade for content

## When to Use

- Page transitions and navigation
- Modal and dialog animations
- Loading and progress states
- Micro-interactions and feedback
- Scroll-driven effects
- Interactive data visualizations

## Notes

- Test on lower-end devices
- Always respect prefers-reduced-motion
- Keep animations consistent across the app
- Don't animate everything - be selective
