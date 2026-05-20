---
name: animation-motion
description: Create smooth animations and micro-interactions with Framer Motion and CSS. Covers enter/exit animations, gestures, scroll animations, loading states, and performance optimization. Use for polished UIs, interactive elements, and engaging user experiences.
---

# Animation & Motion Design

Create smooth, purposeful animations that enhance user experience.

## Instructions

1. **Animate with purpose** - Motion should guide, not distract
2. **Keep it fast** - Most UI animations should be 150-300ms
3. **Use easing curves** - Never use linear timing for UI
4. **Respect preferences** - Honor `prefers-reduced-motion`
5. **Optimize performance** - Animate `transform` and `opacity` only

## Framer Motion (Recommended)

### Setup

```bash
npm install framer-motion
```

### Basic Animations

```tsx
import { motion } from 'framer-motion';

// Fade in on mount
function FadeIn({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {children}
    </motion.div>
  );
}

// Slide up on mount
function SlideUp({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}

// Scale on hover
function ScaleButton({ children }: { children: React.ReactNode }) {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
    >
      {children}
    </motion.button>
  );
}
```

### Enter/Exit Animations

```tsx
import { motion, AnimatePresence } from 'framer-motion';

function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/50"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            className="fixed inset-0 flex items-center justify-center p-4"
          >
            <div className="bg-white rounded-xl shadow-xl max-w-md w-full p-6">
              {children}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
```

### List Animations

```tsx
import { motion, AnimatePresence } from 'framer-motion';

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

function AnimatedList({ items }: { items: Item[] }) {
  return (
    <motion.ul variants={container} initial="hidden" animate="show">
      <AnimatePresence mode="popLayout">
        {items.map((item) => (
          <motion.li
            key={item.id}
            variants={item}
            exit={{ opacity: 0, x: -100 }}
            layout
          >
            <ItemCard {...item} />
          </motion.li>
        ))}
      </AnimatePresence>
    </motion.ul>
  );
}
```

### Layout Animations

```tsx
import { motion, LayoutGroup } from 'framer-motion';

function ExpandableCard({ id, title, content, isExpanded, onToggle }: Props) {
  return (
    <LayoutGroup>
      <motion.div
        layout
        onClick={onToggle}
        className="bg-white rounded-xl p-4 cursor-pointer"
      >
        <motion.h3 layout="position" className="font-semibold">
          {title}
        </motion.h3>

        <AnimatePresence>
          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
            >
              <p className="mt-4 text-gray-600">{content}</p>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </LayoutGroup>
  );
}
```

### Scroll Animations

```tsx
import { motion, useScroll, useTransform } from 'framer-motion';

function ParallaxHero() {
  const { scrollY } = useScroll();

  // Parallax effect - image moves slower than scroll
  const y = useTransform(scrollY, [0, 500], [0, 150]);
  const opacity = useTransform(scrollY, [0, 300], [1, 0]);

  return (
    <div className="relative h-screen overflow-hidden">
      <motion.div
        style={{ y }}
        className="absolute inset-0"
      >
        <img src="/hero.jpg" className="w-full h-full object-cover" />
      </motion.div>

      <motion.div
        style={{ opacity }}
        className="relative z-10 flex items-center justify-center h-full"
      >
        <h1 className="text-6xl font-bold text-white">Welcome</h1>
      </motion.div>
    </div>
  );
}

// Reveal on scroll
function ScrollReveal({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.6, ease: 'easeOut' }}
    >
      {children}
    </motion.div>
  );
}
```

### Gesture Animations

```tsx
import { motion, useDragControls } from 'framer-motion';

function DraggableCard() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      dragElastic={0.1}
      whileDrag={{ scale: 1.05, cursor: 'grabbing' }}
      className="w-48 h-48 bg-blue-500 rounded-xl cursor-grab"
    />
  );
}

function SwipeToDelete({ onDelete }: { onDelete: () => void }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={(_, info) => {
        if (info.offset.x < -100) {
          onDelete();
        }
      }}
      className="bg-white p-4 rounded-lg"
    >
      Swipe left to delete
    </motion.div>
  );
}
```

## Loading States

### Skeleton Loader

```tsx
function Skeleton({ className = '' }: { className?: string }) {
  return (
    <div
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded ${className}`}
    />
  );
}

function CardSkeleton() {
  return (
    <div className="bg-white rounded-xl p-6 space-y-4">
      <Skeleton className="h-6 w-3/4" />
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <div className="flex gap-4 pt-4">
        <Skeleton className="h-10 w-24" />
        <Skeleton className="h-10 w-24" />
      </div>
    </div>
  );
}
```

### Spinner

```tsx
function Spinner({ size = 'md' }: { size?: 'sm' | 'md' | 'lg' }) {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  return (
    <svg
      className={`animate-spin text-blue-600 ${sizes[size]}`}
      viewBox="0 0 24 24"
      fill="none"
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

### Progress Bar

```tsx
function ProgressBar({ value, max = 100 }: { value: number; max?: number }) {
  const percentage = Math.min((value / max) * 100, 100);

  return (
    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
      <motion.div
        className="h-full bg-blue-600"
        initial={{ width: 0 }}
        animate={{ width: `${percentage}%` }}
        transition={{ duration: 0.5, ease: 'easeOut' }}
      />
    </div>
  );
}
```

## CSS Animations

### Tailwind Animations

```tsx
// Built-in Tailwind animations
<div className="animate-spin">Spinner</div>
<div className="animate-ping">Ping</div>
<div className="animate-pulse">Pulse</div>
<div className="animate-bounce">Bounce</div>

// Custom animation in tailwind.config.js
module.exports = {
  theme: {
    extend: {
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
};
```

### CSS Transitions

```tsx
<button className="
  bg-blue-600 text-white px-4 py-2 rounded-lg
  transition-all duration-200 ease-out
  hover:bg-blue-700 hover:shadow-lg hover:-translate-y-0.5
  active:translate-y-0 active:shadow-md
">
  Hover Me
</button>
```

## Respecting User Preferences

```tsx
import { useReducedMotion } from 'framer-motion';

function AnimatedComponent() {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.4 }}
    >
      Content
    </motion.div>
  );
}

// CSS approach
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Performance Tips

1. **Animate only transform and opacity** - GPU accelerated
2. **Use `will-change` sparingly** - Only for complex animations
3. **Avoid layout thrashing** - Don't animate width/height
4. **Use `layout` prop carefully** - Can cause reflows
5. **Debounce scroll handlers** - Prevent jank

```tsx
// Good - GPU accelerated
<motion.div animate={{ x: 100, opacity: 0.5 }} />

// Bad - causes reflow
<motion.div animate={{ width: 200, marginLeft: 100 }} />
```

## When to Use

- Page transitions and navigation
- Loading and skeleton states
- Interactive UI elements
- Feedback and confirmations
- Onboarding and tutorials
- Data visualization transitions

## Notes

- Framer Motion adds ~30kb to bundle (gzipped)
- Use CSS for simple hover/focus transitions
- Test animations at 0.25x speed to verify smoothness
- Consider motion sickness - avoid excessive movement
