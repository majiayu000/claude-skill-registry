---
name: runi-design
description: Build UI components and pages following the runi design system. Use this skill when creating React components for runi—the HTTP client that catches spec drift, verifies AI-generated code, and reveals cross-API relationships. Design language reflects runi's German Shepherd nature: vigilant, protective, with ambient intelligence through subtle signal dots that demand investigation.
---

# runi Design System

This skill guides creation of UI components and pages that follow runi's design system.

**Brand:** runi is named after a German Shepherd—vigilant, protective, nose to the ground. The design reflects this: ambient intelligence through signal dots, deep inspection, tracking changes over time, and acting decisively with clear paths forward.

**Tagline:** _"See the truth about your APIs"_

**Philosophy:** _"Collapse uncertainty into truth"_

**IMPORTANT: runi uses semantic CSS variables via Tailwind utility classes.** Always use semantic color tokens (e.g., `bg-background`, `text-foreground`, `bg-card`) to ensure dark mode compatibility and consistent theming.

## Tech Stack

| Component | Technology                |
| --------- | ------------------------- |
| Runtime   | Tauri v2.9.x              |
| Backend   | Rust 1.80+                |
| Frontend  | React 19 + TypeScript 5.9 |
| Build     | Vite 7.x                  |
| Styling   | Tailwind CSS 4.x          |
| Animation | Motion 12.x               |
| Routing   | React Router 7.x          |
| State     | Zustand                   |
| Icons     | Lucide React              |

## When to Use

- Use this skill when creating or modifying React components, pages, or UI elements in runi
- Use this skill when making design decisions about color, typography, spacing, or interactions
- Use this skill when reviewing UI code to ensure it follows the design system
- Use this skill when designing AI-native features that prioritize conversation over traditional UI patterns
- Use this skill when you need guidance on when to use color vs. grayscale

## Component Library Philosophy

**Custom Components, Not External Libraries**

If a component doesn't exist in a library that perfectly fits our design system, we design it ourselves as craftsmen and artists. We build our own custom component library that integrates seamlessly with runi's design system.

**Key Principles:**

- **Craftsmanship over convenience**: We craft components that fit perfectly, not compromise with generic solutions
- **Design system integration**: Every component respects our zen, calm, book-like aesthetic
- **Performance first**: React frontend on Rust backend—components must be performant
- **Beauty and clarity**: Components work with absolute clarity, not ambiguity

**The Unreal Engine Metaphor:**
Think like game engine developers—craftsmanship, performance, clarity, not gamification. Game engines don't use generic UI libraries—they craft their own systems that fit perfectly within their architecture. We do the same.

See `../runi-planning-docs/DESIGN_IDEOLOGY.md` for the complete craftsmanship philosophy, custom component library approach, and unified material feel principles.

## Instructions

### Design Philosophy: The German Shepherd

runi's design reflects its namesake—a German Shepherd. Vigilant. Protective. Nose to the ground. _"Something's not right here."_

**The Design Language:**

| Trait              | Design Expression                                                 |
| ------------------ | ----------------------------------------------------------------- |
| Vigilant, alert    | Ambient intelligence—subtle signal dots that demand investigation |
| Protective         | Catches problems before they escape to production                 |
| Nose to the ground | Deep inspection of requests, responses, schemas                   |
| Tracks everything  | Temporal awareness—version history, diffs, change detection       |
| Acts decisively    | Not just warnings—actionable fixes, clear paths forward           |

**Core Principles:**

- **Signal System**: Yellow dots appear when something drifts. You investigate. You discover.
- **Strategic Color**: Color is functional and semantic—HTTP methods, status codes, signals. Not decoration.
- **Progressive Revelation**: Start simple, discover depth. Features reveal based on user behavior.
- **Dark Theme**: Near-black backgrounds (`#0a0a0a`)—the night watch.
- **Quiet & Focused**: Minimal visual noise. High contrast for readability.

**NOT**: Flashy animations, heavy UI chrome, color for decoration, overwhelming users with features

### Color System: The Night Watch

**runi Color Palette** (from Brand Spirit v2.1):

```text
Background (app):     #0a0a0a    Near-black—the night watch
Background (surface): #141414    Dark gray
Background (raised):  #1e1e1e    Elevated surfaces

Text (primary):       #f5f5f5
Text (secondary):     #a3a3a3
Text (muted):         #636363

Accent (primary):     #3b82f6    Blue—action, selection, focus
Accent (AI):          #a855f7    Purple—AI-generated content (suspect until verified)
Signal (success):     #22c55e    Green—valid, verified, safe
Signal (warning):     #f59e0b    Amber—drift detected, needs investigation
Signal (error):       #ef4444    Red—breaking change, critical threat
```

**The Foundation:** Most of runi's interface should be grayscale—using semantic grays for backgrounds, text, borders, and structure. Color is reserved for **meaningful, functional elements** that need to stand out.

**Semantic Colors (Dark Mode Compatible):**

Use these Tailwind classes for the **grayscale foundation**:

| Tailwind Class                                   | Usage                                               |
| ------------------------------------------------ | --------------------------------------------------- |
| `bg-background` / `text-foreground`              | Page backgrounds, primary text                      |
| `bg-card` / `text-card-foreground`               | Cards, elevated surfaces                            |
| `bg-muted` / `text-muted-foreground`             | Secondary text, disabled states                     |
| `bg-primary` / `text-primary-foreground`         | Primary buttons, CTAs                               |
| `bg-secondary` / `text-secondary-foreground`     | Secondary buttons                                   |
| `bg-accent` / `text-accent-foreground`           | Hover states, highlights                            |
| `bg-destructive` / `text-destructive-foreground` | Errors, delete actions                              |
| `border-border`                                  | Borders, dividers                                   |
| `bg-input` / `border-input`                      | Form inputs, selectors                              |
| `ring-ring`                                      | Focus rings (default, use `accent-blue` explicitly) |

**Strategic Color: When and Where**

Color should be used **sparingly and purposefully**. These are your "blue eyes" moments—elements that need to draw attention and convey meaning:

1. **HTTP Methods** - Semantic, functional (they define what the request does)
2. **Status Codes** - Semantic, functional (they communicate response state)
3. **Critical Feedback** - Errors, warnings (they need immediate attention)
4. **AI Interactions** - Prompts, suggestions, intelligence (this is the "conversation")
5. **Key Actions** - Very sparingly, for primary CTAs only

**Everything else should be grayscale** using semantic tokens.

**HTTP Method Colors (Strategic Splash #1):**

HTTP methods get color because they're **functional and semantic**—they communicate meaning:

| Method  | Text Color            | Background (for badges) | Meaning          |
| ------- | --------------------- | ----------------------- | ---------------- |
| GET     | `text-accent-blue`    | `bg-accent-blue/10`     | Read, safe       |
| POST    | `text-signal-success` | `bg-signal-success/10`  | Create, positive |
| PUT     | `text-signal-warning` | `bg-signal-warning/10`  | Update, caution  |
| PATCH   | `text-signal-warning` | `bg-signal-warning/10`  | Update, caution  |
| DELETE  | `text-signal-error`   | `bg-signal-error/10`    | Destructive      |
| HEAD    | `text-text-muted`     | `bg-text-muted/10`      | Meta/secondary   |
| OPTIONS | `text-text-muted`     | `bg-text-muted/10`      | Meta/secondary   |

**2026 Zen Aesthetic:** Color the text, use subtle background tints. No solid colored backgrounds—muted surfaces with selective emphasis.

**Signal Colors (from Design Vision v8.1):**

| Signal | Hex       | Meaning                               |
| ------ | --------- | ------------------------------------- |
| Green  | `#22c55e` | Verified, safe, all clear             |
| Amber  | `#f59e0b` | Drift detected, needs investigation   |
| Red    | `#ef4444` | Breaking change, critical issue       |
| Purple | `#a855f7` | AI-generated (suspect until verified) |
| Blue   | `#3b82f6` | Suggestion available                  |

**HTTP Status Code Colors (Strategic Splash #2):**

Status codes get color because they're **functional and semantic**—they communicate response state:

| Range | Text Color            | Background (for badges) | Meaning       |
| ----- | --------------------- | ----------------------- | ------------- |
| 2xx   | `text-signal-success` | `bg-signal-success/10`  | Success       |
| 3xx   | `text-accent-blue`    | `bg-accent-blue/10`     | Redirects     |
| 4xx   | `text-signal-warning` | `bg-signal-warning/10`  | Client errors |
| 5xx   | `text-signal-error`   | `bg-signal-error/10`    | Server errors |
| Other | `text-text-muted`     | `bg-text-muted/10`      | Unknown       |

**Strategic Color Guidelines:**

```tsx
// BAD - using color for decoration
<div className="bg-blue-500 text-white"> {/* Color without purpose */}
<button className="bg-purple-600">Secondary action</button> {/* Color for non-critical element */}

// BAD - hardcoded colors break dark mode
<div className="bg-white text-black">

// GOOD - grayscale foundation
<div className="bg-background text-foreground"> {/* Monochrome */}
<div className="bg-card border border-border"> {/* Semantic grays */}
<button className="bg-muted hover:bg-muted/80"> {/* Grayscale interaction */}

// GOOD - strategic color for meaning (using design system tokens)
<span className="text-accent-blue bg-accent-blue/10 px-1.5 py-0.5 rounded">GET</span> {/* HTTP method */}
<span className="text-signal-error">500</span> {/* Status code */}
<div className="bg-signal-error/10 border-signal-error/20 text-signal-error">Error</div> {/* Critical feedback */}
```

**Key Rule:** When in doubt, use grayscale. Color is reserved for signals that demand attention—drift warnings, verification status, HTTP methods.

### Typography: Clean and Readable

Typography should be clear, readable, and purposeful. High contrast for readability in the dark theme.

**Font Families:**

```css
/* Code and data (monospaced) */
font-family: 'JetBrains Mono', 'SF Mono', Consolas, monospace;

/* UI text (system fonts) */
font-family:
  Inter,
  -apple-system,
  BlinkMacSystemFont,
  sans-serif;
```

**Type Hierarchy:**

| Element        | Font      | Weight  | Size      | Usage                    |
| -------------- | --------- | ------- | --------- | ------------------------ |
| Headings       | Inter     | Medium  | `text-lg` | Section titles           |
| UI Text        | Inter     | Regular | `text-sm` | Body text, labels        |
| Code/Data      | Monospace | Regular | `text-sm` | Request/response content |
| Secondary Text | Inter     | Regular | `text-xs` | Metadata, hints          |

**Typography Patterns:**

```tsx
{
  /* UI Text */
}
<div className="text-sm text-foreground">UI Text</div>;

{
  /* Code/Data (always monospaced) */
}
<pre className="font-mono text-sm text-foreground bg-muted/30">Code</pre>;

{
  /* Secondary Text */
}
<span className="text-xs text-muted-foreground">Secondary info</span>;

{
  /* Headings */
}
<h3 className="text-lg font-medium text-foreground">Section Title</h3>;
```

### Component Architecture

**Import from UI Components:**

Always use components from `src/components/ui/`:

```typescript
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
```

**Button Variants:**

```typescript
// Use these variants
variant: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
size: 'default' | 'sm' | 'lg' | 'icon';
```

**Card Patterns:**

- Use `rounded-xl` for larger cards
- Subtle borders: `border border-border`
- Background: `bg-card`
- Shadow: `shadow-sm` (subtle elevation)

### Design Patterns

**Rounded Corners:**

runi uses consistent border radius:

- Small elements: `rounded-md` (default)
- Cards/containers: `rounded-xl`
- Pill shapes: `rounded-full` (when needed)

**Hover States:**

```tsx
{
  /* Subtle background change */
}
<div className="hover:bg-muted/50 transition-colors duration-200">Content</div>;

{
  /* Only use cursor-pointer on actual links/buttons */
}
<button className="cursor-pointer">Button</button>;
```

**Key Rule:** Only use `cursor-pointer` on actual clickable/interactive elements. Use `hover:bg-muted/50` for hover feedback on list items and containers.

**Transitions:**

Always use smooth transitions for state changes:

- Color transitions: `transition-colors duration-200`
- All transitions: `transition-all duration-200 ease-in-out`
- Standard duration: 200ms for smooth, responsive feel

**Shadows:**

Use subtle shadows for elevation:

- `shadow-xs` - Buttons, inputs
- `shadow-sm` - Cards, elevated surfaces
- `shadow-md` - Modals, popovers (when needed)

**Spacing:**

- Use consistent padding: `p-4`, `p-6`, `p-8`
- Card gaps: `gap-4` or `gap-6`
- Section margins: `my-4`, `my-6`, `my-8`

### React 19 + Motion 12 Patterns

**Functional Components with TypeScript:**

```tsx
import { motion } from 'motion/react';
import { cn } from '@/lib/utils';

interface CardProps {
  title: string;
  description?: string;
  className?: string;
  onAction?: () => void;
}

export const Card = ({ title, description, className, onAction }: CardProps): JSX.Element => {
  return (
    <motion.div
      className={cn('p-6 bg-card border border-border rounded-xl', className)}
      whileHover={{ scale: 1.01 }}
      transition={{ duration: 0.2 }}
    >
      <h3 className="text-lg font-medium text-card-foreground mb-2">{title}</h3>
      {description && <p className="text-sm text-muted-foreground mb-4">{description}</p>}
      {onAction && (
        <Button variant="default" onClick={onAction}>
          Action
        </Button>
      )}
    </motion.div>
  );
};
```

**Zustand Store Pattern:**

```typescript
import { create } from 'zustand';

interface RequestState {
  url: string;
  method: string;
  loading: boolean;
  setUrl: (url: string) => void;
  setMethod: (method: string) => void;
  setLoading: (loading: boolean) => void;
}

export const useRequestStore = create<RequestState>((set) => ({
  url: '',
  method: 'GET',
  loading: false,
  setUrl: (url) => set({ url }),
  setMethod: (method) => set({ method }),
  setLoading: (loading) => set({ loading }),
}));
```

**Required:**

- `TypeScript` on all components
- Explicit return types on functions
- Use Zustand for global state, useState for local state
- Type all props with interfaces

**Motion 12 Animation:**

```tsx
import { motion, AnimatePresence } from 'motion/react';

// Animated element
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.2 }}
>
  Content
</motion.div>

// AnimatePresence for enter/exit
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div key="modal" /* ... */>
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

### Component Construction Patterns

**Building New Components:**

```tsx
import { motion } from 'motion/react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface RequestCardProps {
  title: string;
  method: string;
  url: string;
  className?: string;
  onSend?: () => void;
}

export const RequestCard = ({
  title,
  method,
  url,
  className,
  onSend,
}: RequestCardProps): JSX.Element => {
  // Strategic color: HTTP method gets color (functional/semantic)
  // Using design system tokens for consistency
  const methodTextColors: Record<string, string> = {
    GET: 'text-accent-blue',
    POST: 'text-signal-success',
    PUT: 'text-signal-warning',
    PATCH: 'text-signal-warning',
    DELETE: 'text-signal-error',
  };
  const methodBgColors: Record<string, string> = {
    GET: 'bg-accent-blue/10',
    POST: 'bg-signal-success/10',
    PUT: 'bg-signal-warning/10',
    PATCH: 'bg-signal-warning/10',
    DELETE: 'bg-signal-error/10',
  };
  const textColor = methodTextColors[method] || 'text-text-muted';
  const bgColor = methodBgColors[method] || 'bg-text-muted/10';

  return (
    <motion.div
      className={cn('p-4 bg-card border-border rounded-xl', className)}
      whileHover={{ scale: 1.005 }}
    >
      <h3 className="text-base font-medium text-card-foreground">{title}</h3>
      <div className="flex items-center gap-2 mt-2">
        {/* Strategic splash: method color (zen aesthetic - text color with subtle bg) */}
        <span
          className={cn(
            'px-1.5 py-0.5 rounded text-xs font-semibold font-mono',
            textColor,
            bgColor
          )}
        >
          {method}
        </span>
        {/* Grayscale: URL (monochrome) */}
        <code className="flex-1 text-sm font-mono text-foreground bg-muted/30 px-2 py-1 rounded">
          {url}
        </code>
        {/* Grayscale: Button (semantic, not colored) */}
        {onSend && (
          <Button variant="outline" size="sm" onClick={onSend}>
            Send
          </Button>
        )}
      </div>
    </motion.div>
  );
};
```

**Accessibility Patterns:**

- Always include proper aria attributes
- Use semantic HTML (`<nav>`, `<main>`, `<aside>`)
- Focus management with proper tabIndex

**Focus Ring Standard:**

All interactive elements must have visible focus indicators that meet WCAG 2.1 AA requirements:

- **Color**: `accent-blue` (oklch(0.623 0.214 259.1)) - aligns with design system "Blue—action, selection, focus"
- **Width**: `2px` (`ring-2`)
- **Offset**: `2px` (`ring-offset-2`)
- **Offset Color**: `bg-app` (`ring-offset-bg-app`)
- **Pseudo-class**: `:focus-visible` (only shows on keyboard focus, not mouse clicks)

**Tailwind Classes**:

```typescript
'outline-none focus-visible:ring-2 focus-visible:ring-accent-blue focus-visible:ring-offset-2 focus-visible:ring-offset-bg-app';
```

**Reusable Utility**: Use `focusRingClasses` from `@/utils/accessibility` for consistency.

**Hover-Only Elements**: Use `useFocusVisible` hook from `@/utils/accessibility` for elements that are hidden by default and shown on hover, but must be visible when focused.

**Error Handling:**

Always display Rust/Tauri errors in UI:

```tsx
{
  error && (
    <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg text-destructive">
      {error}
    </div>
  );
}
```

### Implementation Checklist

1. **Default to grayscale** - Use semantic grays (`bg-background`, `bg-card`, `text-foreground`, `bg-muted`) for most UI
2. **Color is strategic** - Only use color for HTTP methods, status codes, critical feedback, AI interactions, and key actions
3. **Never hardcode colors** - No `bg-white`, `text-black`, `blue-500` (use semantic tokens or strategic color utilities)
4. **Test dark mode** - All components must work in both light and dark modes
5. **Use UI components** - Import from `@/components/ui/`
6. **Use React 19 patterns** - Functional components, hooks, TypeScript
7. **Use Zustand for global state** - Not Redux, not Context for shared state
8. **Type everything** - TypeScript strict mode, explicit types
9. **Smooth transitions** - 200ms duration, `transition-colors` for hover
10. **No pointer cursor on non-clickable** - Only use `cursor-pointer` on actual buttons/links
11. **Monospaced fonts for code/data** - Use `font-mono` for request/response content
12. **Display errors** - Always show Tauri command errors in UI
13. **Use Motion for animations** - Import from `motion/react`, not `framer-motion`

### Example Components

**HTTP Method Badge:**

```tsx
import { cn } from '@/lib/utils';

interface MethodBadgeProps {
  method: string;
  className?: string;
}

// Design system colors - text with subtle background (zen aesthetic)
const methodTextColors: Record<string, string> = {
  GET: 'text-accent-blue',
  POST: 'text-signal-success',
  PUT: 'text-signal-warning',
  PATCH: 'text-signal-warning',
  DELETE: 'text-signal-error',
  HEAD: 'text-text-muted',
  OPTIONS: 'text-text-muted',
};

const methodBgColors: Record<string, string> = {
  GET: 'bg-accent-blue/10',
  POST: 'bg-signal-success/10',
  PUT: 'bg-signal-warning/10',
  PATCH: 'bg-signal-warning/10',
  DELETE: 'bg-signal-error/10',
  HEAD: 'bg-text-muted/10',
  OPTIONS: 'bg-text-muted/10',
};

export const MethodBadge = ({ method, className }: MethodBadgeProps): JSX.Element => {
  const textColor = methodTextColors[method] ?? 'text-text-muted';
  const bgColor = methodBgColors[method] ?? 'bg-text-muted/10';

  return (
    <span
      className={cn(
        'px-1.5 py-0.5 rounded text-xs font-semibold font-mono',
        textColor,
        bgColor,
        className
      )}
    >
      {method}
    </span>
  );
};
```

**Status Badge:**

```tsx
import { cn } from '@/lib/utils';

interface StatusBadgeProps {
  status: number;
  className?: string;
}

// Design system colors - text only for zen aesthetic
const getStatusColor = (status: number): string => {
  if (status >= 200 && status < 300) return 'text-signal-success';
  if (status >= 300 && status < 400) return 'text-accent-blue';
  if (status >= 400 && status < 500) return 'text-signal-warning';
  if (status >= 500) return 'text-signal-error';
  return 'text-text-muted';
};

export const StatusBadge = ({ status, className }: StatusBadgeProps): JSX.Element => {
  const colorClass = getStatusColor(status);

  return (
    <span className={cn('text-sm font-mono font-semibold', colorClass, className)}>{status}</span>
  );
};
```

**AI Interaction (The "Blue Eyes" Moment):**

AI prompts and suggestions are where color can shine—this is the conversational, intelligent moment:

```tsx
import { Button } from '@/components/ui/button';
import { motion } from 'motion/react';

interface AISuggestionProps {
  suggestion: string;
  onAccept?: () => void;
}

export const AISuggestion = ({ suggestion, onAccept }: AISuggestionProps): JSX.Element => {
  return (
    <motion.div
      className="bg-primary/5 border-primary/20 border rounded-lg p-3"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <p className="text-sm text-foreground mb-2">{suggestion}</p>
      {/* Primary action: strategic color */}
      <Button variant="default" size="sm" onClick={onAccept}>
        Use suggestion
      </Button>
    </motion.div>
  );
};
```

## Related Documentation

For detailed technical implementation:

- **Design Ideology**: `../runi-planning-docs/DESIGN_IDEOLOGY.md` - Craftsmanship philosophy, custom component library approach, Unreal Engine metaphor
- **Design Vision**: `../runi-planning-docs/runi-design-vision-v8.1.md`
- **Component Library**: `src/components/ui/`
- **Stores**: `src/stores/`
- **CSS Variables**: `src/index.css`
- **Tauri Commands**: `src-tauri/src/commands/`
- **Project Structure**: `CLAUDE.md`
