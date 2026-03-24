---
name: animation-patterns
description: Framer Motion patterns, page transitions, skeleton loading, scroll-linked animations, and gesture-based interactions for React.
---

# Animation Patterns

Framer Motion patterns for production-quality React animations.

## Framer Motion Basics (motion components, variants)

```typescript
// Install: npm install framer-motion

import { motion } from 'framer-motion'

// Basic motion component
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: 'easeOut' }}
/>

// Variants — define states, animate by name
const cardVariants = {
  hidden: { opacity: 0, y: 20, scale: 0.98 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
  hover: {
    y: -4,
    boxShadow: '0 12px 24px -4px rgb(0 0 0 / 0.15)',
    transition: { duration: 0.2 },
  },
}

function Card({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      className="rounded-lg border bg-white p-4"
    >
      {children}
    </motion.div>
  )
}
```

## Page Transitions with AnimatePresence

```typescript
import { AnimatePresence, motion } from 'framer-motion'
import { usePathname } from 'next/navigation'

const pageVariants = {
  initial: { opacity: 0, x: -8 },
  enter:   { opacity: 1, x: 0, transition: { duration: 0.2, ease: 'easeOut' } },
  exit:    { opacity: 0, x: 8,  transition: { duration: 0.15, ease: 'easeIn' } },
}

// app/layout.tsx (Next.js App Router)
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  return (
    <html>
      <body>
        <AnimatePresence mode="wait">
          <motion.main
            key={pathname}
            variants={pageVariants}
            initial="initial"
            animate="enter"
            exit="exit"
          >
            {children}
          </motion.main>
        </AnimatePresence>
      </body>
    </html>
  )
}

// Modal transitions — mount/unmount
function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            key="overlay"
            className="fixed inset-0 bg-black/40"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            key="modal"
            className="fixed inset-x-4 top-[10%] mx-auto max-w-lg rounded-xl bg-white p-6 shadow-xl"
            initial={{ opacity: 0, scale: 0.96, y: 16 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 8 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

## Layout Animations (Shared Layout, Layout ID)

```typescript
import { motion, LayoutGroup } from 'framer-motion'
import { useState } from 'react'

// Tabs with animated indicator
function AnimatedTabs({ tabs }: { tabs: string[] }) {
  const [active, setActive] = useState(tabs[0])

  return (
    <LayoutGroup>
      <div className="flex gap-1 rounded-lg bg-gray-100 p-1">
        {tabs.map(tab => (
          <button
            key={tab}
            onClick={() => setActive(tab)}
            className="relative px-4 py-2 text-sm font-medium"
          >
            {active === tab && (
              <motion.div
                layoutId="tab-indicator"      // shared across tabs
                className="absolute inset-0 rounded-md bg-white shadow-sm"
                transition={{ type: 'spring', stiffness: 400, damping: 30 }}
              />
            )}
            <span className="relative z-10">{tab}</span>
          </button>
        ))}
      </div>
    </LayoutGroup>
  )
}

// Expandable card with layout animation
function ExpandableCard({ title, body }: { title: string; body: string }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <motion.div
      layout                                // animate height changes
      className="rounded-lg border bg-white p-4 cursor-pointer"
      onClick={() => setExpanded(e => !e)}
    >
      <motion.h3 layout="position" className="font-semibold">{title}</motion.h3>
      <AnimatePresence>
        {expanded && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mt-2 text-gray-600 text-sm"
          >
            {body}
          </motion.p>
        )}
      </AnimatePresence>
    </motion.div>
  )
}
```

## Skeleton Loading Components

```typescript
// Base skeleton primitive
function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn('animate-pulse rounded bg-gray-200 dark:bg-gray-700', className)}
      aria-hidden="true"
    />
  )
}

// Shimmer variant (more polished)
function SkeletonShimmer({ className }: { className?: string }) {
  return (
    <div className={cn('relative overflow-hidden rounded bg-gray-200', className)}>
      <motion.div
        className="absolute inset-0 bg-gradient-to-r from-transparent via-white/60 to-transparent"
        animate={{ x: ['-100%', '100%'] }}
        transition={{ repeat: Infinity, duration: 1.2, ease: 'linear' }}
      />
    </div>
  )
}

// Card skeleton
function CardSkeleton() {
  return (
    <div className="rounded-lg border bg-white p-4 space-y-3" aria-busy="true" aria-label="Loading">
      <div className="flex items-center gap-3">
        <Skeleton className="size-10 rounded-full" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-3 w-1/3" />
        </div>
      </div>
      <Skeleton className="h-3 w-full" />
      <Skeleton className="h-3 w-4/5" />
      <Skeleton className="h-8 w-24 rounded-md" />
    </div>
  )
}
```

## Scroll-Linked Animations

```typescript
import { useScroll, useTransform, motion } from 'framer-motion'
import { useRef } from 'react'

// Parallax hero
function ParallaxHero() {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] })

  const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%'])
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])

  return (
    <div ref={ref} className="relative h-screen overflow-hidden">
      <motion.div style={{ y, opacity }} className="absolute inset-0">
        <img src="/hero.jpg" alt="" className="w-full h-full object-cover" />
      </motion.div>
      <div className="relative z-10 flex h-full items-center justify-center">
        <h1 className="text-6xl font-bold text-white">Hero Title</h1>
      </div>
    </div>
  )
}

// Fade-in on scroll (section reveal)
function FadeInSection({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 0.9', 'start 0.6'] })
  const opacity = useTransform(scrollYProgress, [0, 1], [0, 1])
  const y = useTransform(scrollYProgress, [0, 1], [24, 0])

  return (
    <motion.div ref={ref} style={{ opacity, y }}>
      {children}
    </motion.div>
  )
}
```

## Staggered Children Animations

```typescript
const listVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.06,     // 60ms between each child
      delayChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden:  { opacity: 0, x: -12 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.25, ease: 'easeOut' } },
}

function AnimatedList({ items }: { items: string[] }) {
  return (
    <motion.ul variants={listVariants} initial="hidden" animate="visible" className="space-y-2">
      {items.map(item => (
        <motion.li key={item} variants={itemVariants} className="rounded border p-3">
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

## Gesture Interactions (Drag, Tap, Hover)

```typescript
import { motion, useDragControls } from 'framer-motion'

// Draggable card
function DraggableCard() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
      dragElastic={0.1}
      whileDrag={{ scale: 1.05, rotate: 2, cursor: 'grabbing' }}
      className="cursor-grab rounded-lg bg-white p-4 shadow"
    >
      Drag me
    </motion.div>
  )
}

// Bottom sheet (drag to dismiss)
function BottomSheet({ onClose }: { onClose: () => void }) {
  return (
    <motion.div
      drag="y"
      dragConstraints={{ top: 0 }}
      onDragEnd={(_, info) => {
        if (info.offset.y > 100) onClose()
      }}
      initial={{ y: '100%' }}
      animate={{ y: 0 }}
      exit={{ y: '100%' }}
      transition={{ type: 'spring', damping: 30, stiffness: 300 }}
      className="fixed bottom-0 inset-x-0 rounded-t-2xl bg-white p-6 shadow-lg"
    >
      <div className="mx-auto mb-4 h-1 w-12 rounded-full bg-gray-300" />
      {/* content */}
    </motion.div>
  )
}

// Press / tap feedback
function PressButton({ children, onClick }: ButtonProps) {
  return (
    <motion.button
      whileTap={{ scale: 0.97 }}
      whileHover={{ scale: 1.02 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      onClick={onClick}
      className="btn btn-primary"
    >
      {children}
    </motion.button>
  )
}
```

## Reduced Motion Respect

```typescript
import { useReducedMotion, motion } from 'framer-motion'

// Hook-based — apply conditionally
function FadeIn({ children }: { children: React.ReactNode }) {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.div
      initial={{ opacity: prefersReducedMotion ? 1 : 0 }}
      animate={{ opacity: 1 }}
      transition={prefersReducedMotion ? { duration: 0 } : { duration: 0.3 }}
    >
      {children}
    </motion.div>
  )
}

// Global — wrap app with MotionConfig
import { MotionConfig } from 'framer-motion'

export function Providers({ children }: { children: React.ReactNode }) {
  const prefersReducedMotion = useReducedMotion()
  return (
    <MotionConfig reducedMotion={prefersReducedMotion ? 'always' : 'never'}>
      {children}
    </MotionConfig>
  )
}

// CSS fallback (always include alongside JS animations)
// @media (prefers-reduced-motion: reduce) { .animated { animation: none !important; } }
```

## Performance Tips

```typescript
// 1. Use transform properties — GPU accelerated
// GOOD: x, y, scale, rotate, opacity (compositor layer)
// BAD: width, height, top, left, margin (layout thrash)

// 2. will-change for known animations (use sparingly)
<motion.div style={{ willChange: 'transform' }} />

// 3. layout prop only when needed — triggers LayoutAnimation (expensive)
<motion.div layout />          // layout: expensive, triggers every render
<motion.div layout="position"> // layout="position": cheaper, only position

// 4. LazyMotion — reduces bundle size (removes unused features)
import { LazyMotion, domAnimation, m } from 'framer-motion'

<LazyMotion features={domAnimation}>  {/* load only DOM animations */}
  <m.div animate={{ opacity: 1 }} />  {/* use m instead of motion */}
</LazyMotion>

// 5. Avoid animating inside virtualized lists
// AnimatePresence + virtualization = bugs. Use CSS transitions for list items.

// 6. Spring physics vs duration — springs feel more natural
const spring = { type: 'spring', stiffness: 300, damping: 25 }
const duration = { duration: 0.3, ease: [0.16, 1, 0.3, 1] }
// Springs: interactive elements (drag release, hover)
// Duration: page transitions, content reveal
```
