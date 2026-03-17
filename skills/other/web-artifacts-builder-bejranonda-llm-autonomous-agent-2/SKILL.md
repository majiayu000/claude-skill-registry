---
name: web-artifacts-builder
description: Modern web development patterns using React + Tailwind CSS + shadcn/ui for building production-quality, accessible, and performant web applications
version: 1.0.0
---

## Overview

This skill provides comprehensive patterns and best practices for building modern web applications using the React + Tailwind CSS + shadcn/ui stack. It emphasizes component-driven development, type safety with TypeScript, accessibility, and performance optimization.

## Stack Overview

**Core Technologies**:
- **React 18+**: Component-based UI with hooks and concurrent features
- **TypeScript**: Type-safe development with excellent IDE support
- **Tailwind CSS**: Utility-first CSS framework for rapid styling
- **shadcn/ui**: High-quality, accessible React components built on Radix UI
- **Vite**: Fast build tool with HMR and optimized production builds

**Why This Stack**:
- Type safety reduces bugs and improves maintainability
- Tailwind enables rapid UI development without context switching
- shadcn/ui provides accessible, customizable components out of the box
- Vite offers excellent developer experience and fast builds
- Modern ecosystem with active community support

**Design Considerations**:
Based on research from ["Improving frontend design through Skills"](https://claude.com/blog/improving-frontend-design-through-skills):
- **Avoid Distributional Defaults**: Don't use Inter/Roboto/Open Sans, purple gradients, or plain backgrounds
- **Distinctive Typography**: Use high-contrast font pairings with extreme weight variations (100-200 or 800-900)
- **Intentional Colors**: Move beyond generic color schemes with thoughtful palettes
- **High-Impact Motion**: One well-orchestrated page load beats a dozen random animations
- **Motion Library**: Use Framer Motion for complex animation choreography in React
- See `frontend-aesthetics` skill for comprehensive design guidance

## Project Structure

### Recommended Directory Layout

```
project-root/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   ├── features/        # Feature-specific components
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   └── ...
│   │   └── layout/          # Layout components
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── Footer.tsx
│   ├── lib/
│   │   ├── utils.ts         # Utility functions (cn, etc.)
│   │   ├── api.ts           # API client
│   │   └── hooks/           # Custom React hooks
│   ├── pages/               # Page components (if using routing)
│   ├── styles/
│   │   └── globals.css      # Global styles and Tailwind imports
│   ├── types/               # TypeScript type definitions
│   ├── App.tsx              # Main app component
│   └── main.tsx             # Entry point
├── public/                  # Static assets
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── vite.config.ts
└── components.json          # shadcn/ui configuration
```

## Component Patterns

### 1. Button Component (shadcn/ui style)

```typescript
// src/components/ui/button.tsx
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

**Usage**:
```typescript
import { Button } from "@/components/ui/button"

// Different variants
<Button>Default</Button>
<Button variant="destructive">Delete</Button>
<Button variant="outline">Cancel</Button>
<Button variant="ghost">Ghost</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
<Button disabled>Disabled</Button>
```

### 2. Card Component Pattern

```typescript
// src/components/ui/card.tsx
import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-xl border bg-card text-card-foreground shadow",
        className
      )}
      {...props}
    />
  )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-col space-y-1.5 p-6", className)}
      {...props}
    />
  )
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn("font-semibold leading-none tracking-tight", className)}
      {...props}
    />
  )
)
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
  ({ className, ...props }, ref) => (
    <p
      ref={ref}
      className={cn("text-sm text-muted-foreground", className)}
      {...props}
    />
  )
)
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex items-center p-6 pt-0", className)}
      {...props}
    />
  )
)
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

**Usage**:
```typescript
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content</p>
  </CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

### 3. Dialog/Modal Component

```typescript
// src/components/ui/dialog.tsx (simplified shadcn/ui pattern)
import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root
const DialogTrigger = DialogPrimitive.Trigger
const DialogPortal = DialogPrimitive.Portal
const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
  />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

export { Dialog, DialogPortal, DialogOverlay, DialogTrigger, DialogClose, DialogContent }
```

## Tailwind CSS Configuration

### Enhanced tailwind.config.js

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: 0 },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: 0 },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
```

### CSS Variables (globals.css)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 48%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

## Utility Functions

### cn() - Class Name Utility

```typescript
// src/lib/utils.ts
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Usage**: Merge Tailwind classes without conflicts
```typescript
cn("px-2 py-1", "px-3")  // Result: "py-1 px-3" (px-3 overrides px-2)
```

## TypeScript Best Practices

### Component Props Typing

```typescript
// Extend HTML attributes
interface CustomButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

// Or use type
type CustomButtonProps = {
  variant?: 'primary' | 'secondary' | 'outline'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
} & React.ButtonHTMLAttributes<HTMLButtonElement>
```

### API Response Typing

```typescript
// Define API response types
interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user'
}

interface ApiResponse<T> {
  data: T
  message: string
  status: 'success' | 'error'
}

// Usage
const fetchUser = async (id: string): Promise<ApiResponse<User>> => {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}
```

## Accessibility Patterns

### Keyboard Navigation

```typescript
// Focus management
const handleKeyDown = (e: React.KeyboardEvent) => {
  if (e.key === 'Escape') {
    onClose()
  }
  if (e.key === 'Enter' || e.key === ' ') {
    onSelect()
    e.preventDefault()
  }
}

// Trap focus in modal
import { useFocusTrap } from '@/lib/hooks/use-focus-trap'

function Modal({ children }: { children: React.ReactNode }) {
  const modalRef = useFocusTrap()

  return (
    <div ref={modalRef} role="dialog" aria-modal="true">
      {children}
    </div>
  )
}
```

### ARIA Labels

```typescript
// Screen reader support
<button
  aria-label="Close dialog"
  aria-pressed={isPressed}
  aria-expanded={isExpanded}
>
  <X className="h-4 w-4" />
</button>

// Form accessibility
<div>
  <label htmlFor="email" className="sr-only">Email</label>
  <input
    id="email"
    type="email"
    aria-required="true"
    aria-invalid={hasError}
    aria-describedby={hasError ? "email-error" : undefined}
  />
  {hasError && <p id="email-error" role="alert">Invalid email</p>}
</div>
```

## Performance Optimization

### Code Splitting

```typescript
// Lazy load routes
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('./pages/Dashboard'))
const Settings = lazy(() => import('./pages/Settings'))

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  )
}
```

### Memoization

```typescript
import { memo, useMemo, useCallback } from 'react'

// Memo component
const ExpensiveComponent = memo(({ data }: { data: Data[] }) => {
  return <div>{/* Render data */}</div>
})

// Memo computation
function Component({ items }: { items: Item[] }) {
  const sortedItems = useMemo(
    () => items.sort((a, b) => a.name.localeCompare(b.name)),
    [items]
  )

  const handleClick = useCallback(() => {
    console.log('Clicked')
  }, [])

  return <List items={sortedItems} onClick={handleClick} />
}
```

## Animation with Framer Motion

### Installation

```bash
npm install framer-motion
```

### Core Principles

**High-Impact Moments Over Random Motion**:
- One well-orchestrated page load with staggered reveals > dozen random micro-animations
- Focus on: page load, route transitions, major state changes
- Use CSS for simple transitions, Framer Motion for complex choreography
- Always respect `prefers-reduced-motion`

### Page Transitions

```typescript
// app/layout.tsx or page wrapper
import { motion, AnimatePresence } from 'framer-motion'

export default function PageTransition({ children }: { children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{
          duration: 0.5,
          ease: [0.22, 1, 0.36, 1] // Custom ease (easeOutExpo)
        }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

### Staggered List Animation

```typescript
import { motion } from 'framer-motion'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1 // Delay between each child animation
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

export function StaggeredList({ items }: { items: string[] }) {
  return (
    <motion.ul
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-2"
    >
      {items.map((item, i) => (
        <motion.li
          key={i}
          variants={item}
          className="p-4 bg-card rounded-lg"
        >
          {item}
        </motion.li>
      ))}
    </motion.ul>
  )
}
```

### Card Hover Effects

```typescript
import { motion } from 'framer-motion'

export function AnimatedCard({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02, y: -4 }}
      whileTap={{ scale: 0.98 }}
      transition={{ type: "spring", stiffness: 400, damping: 17 }}
      className="rounded-xl border bg-card p-6 shadow-sm cursor-pointer"
    >
      {children}
    </motion.div>
  )
}
```

### Layout Animations (Shared Layout)

```typescript
import { motion, LayoutGroup } from 'framer-motion'

export function TabsWithAnimation({ tabs }: { tabs: Tab[] }) {
  const [activeTab, setActiveTab] = useState(0)

  return (
    <LayoutGroup>
      <div className="flex gap-2">
        {tabs.map((tab, i) => (
          <motion.button
            key={i}
            onClick={() => setActiveTab(i)}
            className="relative px-4 py-2 rounded-md"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {tab.label}
            {activeTab === i && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 bg-primary rounded-md"
                style={{ zIndex: -1 }}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}
          </motion.button>
        ))}
      </div>
    </LayoutGroup>
  )
}
```

### Scroll-Based Animations

```typescript
import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'

export function ParallaxSection() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"]
  })

  const y = useTransform(scrollYProgress, [0, 1], [0, -100])
  const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0])

  return (
    <motion.section
      ref={ref}
      style={{ y, opacity }}
      className="min-h-screen flex items-center justify-center"
    >
      <h2 className="text-4xl font-bold">Parallax Content</h2>
    </motion.section>
  )
}
```

### Modal / Dialog Animations

```typescript
import { motion, AnimatePresence } from 'framer-motion'

export function AnimatedDialog({
  open,
  onClose,
  children
}: {
  open: boolean
  onClose: () => void
  children: React.ReactNode
}) {
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/80 z-50"
          />

          {/* Dialog content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 bg-background p-6 rounded-lg shadow-lg max-w-md w-full"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### Gesture Animations

```typescript
import { motion, useDragControls } from 'framer-motion'

export function DraggableCard() {
  const controls = useDragControls()

  return (
    <motion.div
      drag
      dragControls={controls}
      dragConstraints={{ left: 0, right: 300, top: 0, bottom: 300 }}
      dragElastic={0.1}
      whileDrag={{ scale: 1.05, cursor: "grabbing" }}
      className="w-32 h-32 bg-primary rounded-lg cursor-grab"
    />
  )
}

// Swipe to dismiss
export function SwipeableBanner({ onDismiss }: { onDismiss: () => void }) {
  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={(e, { offset, velocity }) => {
        if (Math.abs(offset.x) > 100 || Math.abs(velocity.x) > 500) {
          onDismiss()
        }
      }}
      className="p-4 bg-card border rounded-lg"
    >
      Swipe to dismiss
    </motion.div>
  )
}
```

### Loading States with Animation

```typescript
import { motion } from 'framer-motion'

export function LoadingSpinner() {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
      className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full"
    />
  )
}

export function PulseLoader() {
  return (
    <div className="flex gap-2">
      {[0, 1, 2].map((i) => (
        <motion.div
          key={i}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 1,
            repeat: Infinity,
            delay: i * 0.2
          }}
          className="w-3 h-3 bg-primary rounded-full"
        />
      ))}
    </div>
  )
}
```

### Respecting Reduced Motion

```typescript
import { motion, useReducedMotion } from 'framer-motion'

export function AccessibleAnimation({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion()

  return (
    <motion.div
      initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
      animate={shouldReduceMotion ? false : { opacity: 1, y: 0 }}
      transition={shouldReduceMotion ? { duration: 0 } : { duration: 0.5 }}
    >
      {children}
    </motion.div>
  )
}
```

### Performance Best Practices

**What to Animate (GPU-Accelerated)**:
- `opacity`
- `transform` (translate, scale, rotate)
- `filter` (blur, brightness)

**What to Avoid Animating**:
- `width`, `height` (causes layout thrashing)
- `top`, `left`, `margin`, `padding` (use `transform: translate` instead)
- `color`, `background-color` (expensive, use sparingly)

**Optimization Tips**:
```typescript
// Use will-change for smoother animations
<motion.div style={{ willChange: "transform" }}>

// Lazy load motion components
import { motion, LazyMotion, domAnimation } from "framer-motion"

<LazyMotion features={domAnimation}>
  <motion.div />
</LazyMotion>

// Reduce animation complexity on low-end devices
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
```

### When to Use Framer Motion vs CSS

**Use CSS Animations**:
- Simple hover effects
- Basic transitions
- Static keyframe animations
- Better performance for simple cases

**Use Framer Motion**:
- Complex orchestration (staggered lists, sequences)
- Gesture-based interactions (drag, swipe)
- Layout animations (morphing between states)
- Scroll-based animations
- Dynamic animations based on state
- Need for easier control and declarative API

## When to Apply

Use this skill when:
- Building modern React applications with TypeScript
- Implementing accessible, production-quality UI components
- Using Tailwind CSS for styling
- Integrating shadcn/ui component library
- Setting up new projects with Vite + React
- Creating reusable component libraries
- Implementing design systems with consistent patterns
- Building dashboards, admin panels, or web applications

This stack provides excellent developer experience, type safety, accessibility, and performance for modern web development.
