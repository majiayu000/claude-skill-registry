---
name: design-to-code
description: Figma-to-code translation, design tokens, spacing/typography scales, responsive breakpoints, and design system bridge patterns.
---

# Design to Code

Translating Figma designs to production-ready React/Tailwind code with consistent tokens.

## Design Token Structure

```typescript
// tokens/index.ts — single source of truth
export const tokens = {
  color: {
    // Primitive palette (don't use directly in components)
    blue: { 50: '#eff6ff', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8' },
    red:  { 50: '#fef2f2', 500: '#ef4444', 600: '#dc2626' },
    gray: { 50: '#f9fafb', 100: '#f3f4f6', 200: '#e5e7eb', 500: '#6b7280', 900: '#111827' },

    // Semantic tokens (use these in components)
    semantic: {
      primary:         '#2563eb',
      primaryHover:    '#1d4ed8',
      primarySubtle:   '#eff6ff',
      danger:          '#dc2626',
      dangerSubtle:    '#fef2f2',
      success:         '#16a34a',
      successSubtle:   '#f0fdf4',
      warning:         '#d97706',
      text:            '#111827',
      textSecondary:   '#6b7280',
      textMuted:       '#9ca3af',
      surface:         '#ffffff',
      surfaceRaised:   '#f9fafb',
      border:          '#e5e7eb',
    },
  },
  spacing: {
    1: '0.25rem',   // 4px
    2: '0.5rem',    // 8px
    3: '0.75rem',   // 12px
    4: '1rem',      // 16px
    5: '1.25rem',   // 20px
    6: '1.5rem',    // 24px
    8: '2rem',      // 32px
    10: '2.5rem',   // 40px
    12: '3rem',     // 48px
    16: '4rem',     // 64px
  },
  radius: {
    sm: '0.25rem', md: '0.375rem', lg: '0.5rem',
    xl: '0.75rem', '2xl': '1rem',  full: '9999px',
  },
  shadow: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
    focus: '0 0 0 3px rgb(37 99 235 / 0.25)',
  },
} as const
```

## Tailwind CSS Custom Theme from Design Tokens

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563eb',
          hover:   '#1d4ed8',
          subtle:  '#eff6ff',
        },
        danger: { DEFAULT: '#dc2626', subtle: '#fef2f2' },
        success: { DEFAULT: '#16a34a', subtle: '#f0fdf4' },
        surface: {
          DEFAULT: '#ffffff',
          raised:  '#f9fafb',
          sunken:  '#f3f4f6',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
      },
      boxShadow: {
        focus: '0 0 0 3px rgb(37 99 235 / 0.25)',
      },
    },
  },
} satisfies Config
```

## Spacing Scale (4px base)

```
Token   rem     px      Use case
──────────────────────────────────────────
space-1  0.25   4px     Icon gap, tight badges
space-2  0.5    8px     Input padding-y, icon margin
space-3  0.75   12px    Button padding-y, small gap
space-4  1.0    16px    Card padding, list gap
space-5  1.25   20px    Section gap (small)
space-6  1.5    24px    Card padding (comfortable)
space-8  2.0    32px    Section gap (medium)
space-10 2.5    40px    Page section gap
space-12 3.0    48px    Hero padding, large section
space-16 4.0    64px    Page padding-y, hero gap

Rule: components use 4/6/8, layouts use 8/12/16
```

## Typography Scale

```typescript
// Tailwind classes mapped to use cases
const typographyScale = {
  'text-xs':   '0.75rem / 1rem',      // labels, captions, meta
  'text-sm':   '0.875rem / 1.25rem',  // secondary text, helper text
  'text-base': '1rem / 1.5rem',       // body text, default
  'text-lg':   '1.125rem / 1.75rem',  // lead text, subheadings
  'text-xl':   '1.25rem / 1.75rem',   // card title, section heading
  'text-2xl':  '1.5rem / 2rem',       // page subheading
  'text-3xl':  '1.875rem / 2.25rem',  // page heading
  'text-4xl':  '2.25rem / 2.5rem',    // hero heading
  'text-5xl':  '3rem / 1',            // display / marketing
}

// Font weight pairings
// font-normal (400) — body text
// font-medium (500) — labels, button text
// font-semibold (600) — headings, emphasis
// font-bold (700) — hero text, strong emphasis
```

## Responsive Breakpoint Mapping

```typescript
// Mobile-first breakpoints (Tailwind defaults)
const breakpoints = {
  sm:  '640px',   // landscape phone, 2-col grids
  md:  '768px',   // tablet, sidebar appears
  lg:  '1024px',  // laptop, full layout
  xl:  '1280px',  // desktop, wider content
  '2xl': '1536px' // wide monitor, max-width content
}

// Grid progression pattern
// 1col (mobile) → 2col (sm) → 3col (lg) → 4col (xl)
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

// Sidebar layout: stacked → side-by-side
<div className="flex flex-col lg:flex-row gap-6">
  <main className="flex-1 min-w-0">{children}</main>
  <aside className="w-full lg:w-72 lg:shrink-0">{sidebar}</aside>
</div>

// Max-width content container
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
```

## Component Anatomy

```typescript
// Standard component regions
interface ComponentAnatomy {
  container: 'outermost wrapper, handles layout/spacing'
  header:    'title + optional subtitle + actions'
  content:   'main slot, variable height'
  footer:    'actions, secondary info, pagination'
}

// Example: Card with all regions
export function Card({
  title,
  subtitle,
  actions,
  footer,
  children,
  className,
}: CardProps) {
  return (
    <div className={cn('rounded-lg border bg-white shadow-sm', className)}>
      {(title || actions) && (
        <div className="flex items-start justify-between gap-4 px-6 py-4 border-b">
          <div>
            {title && <h3 className="text-sm font-semibold text-gray-900">{title}</h3>}
            {subtitle && <p className="text-xs text-gray-500 mt-0.5">{subtitle}</p>}
          </div>
          {actions && <div className="flex items-center gap-2">{actions}</div>}
        </div>
      )}
      <div className="px-6 py-4">{children}</div>
      {footer && (
        <div className="px-6 py-3 border-t bg-gray-50 rounded-b-lg">{footer}</div>
      )}
    </div>
  )
}
```

## Figma Auto-Layout → Flexbox/Grid Translation

```
Figma Auto-Layout direction + settings  →  CSS
──────────────────────────────────────────────────────────────────
Horizontal, gap 16                      →  flex gap-4
Vertical, gap 8                         →  flex flex-col gap-2
Horizontal, space-between               →  flex justify-between
Horizontal, align center                →  flex items-center
Wrap, gap 8                             →  flex flex-wrap gap-2
Fixed width columns (3 × 320px)         →  grid grid-cols-3 gap-6
Fill container                          →  flex-1 or w-full
Hug contents                            →  inline-flex or w-fit
Fixed size                              →  w-[320px] h-[240px]
Padding: 24 16                          →  px-4 py-6
```

## Color System (Semantic Tokens)

```typescript
// Component colors always use semantic tokens, not primitives
// WRONG: className="bg-blue-600 text-white"
// RIGHT: className="bg-primary text-white"

const semanticUsage = {
  // Backgrounds
  'bg-white / bg-surface':          'default card/modal background',
  'bg-surface-raised':              'elevated elements',
  'bg-surface-sunken':              'inset/recessed areas',
  'bg-primary':                     'primary action backgrounds',
  'bg-primary-subtle':              'tinted highlight areas',
  'bg-danger-subtle':               'error state backgrounds',

  // Text
  'text-gray-900':                  'primary text',
  'text-gray-600':                  'secondary text',
  'text-gray-400':                  'placeholder / muted',
  'text-primary':                   'links, active state',
  'text-danger-600':                'error messages',
  'text-success-600':               'success messages',

  // Borders
  'border-gray-200':                'default border',
  'border-gray-300':                'strong border, inputs',
  'border-primary':                 'focused input ring',
  'border-danger-300':              'error state border',
}
```

## Icon System Setup

```typescript
// Install: npm install lucide-react
// or: npm install @heroicons/react

import { Search, Plus, ChevronRight, X } from 'lucide-react'

// Consistent sizing: match text scale
const iconSizes = {
  xs: 'size-3',   // 12px — inline with text-xs
  sm: 'size-4',   // 16px — inline with text-sm (most common)
  md: 'size-5',   // 20px — standalone icons, buttons
  lg: 'size-6',   // 24px — nav icons, prominent
  xl: 'size-8',   // 32px — empty states
}

// Button with icon (left icon pattern)
function Button({ icon: Icon, children, ...props }: ButtonProps) {
  return (
    <button className="inline-flex items-center gap-2 px-4 py-2" {...props}>
      {Icon && <Icon className="size-4 shrink-0" />}
      {children}
    </button>
  )
}

// Icon-only button (needs aria-label)
<button aria-label="Close dialog" className="p-2 rounded hover:bg-gray-100">
  <X className="size-4" />
</button>
```

## Accessibility Requirements per Component Type

```typescript
// Form inputs
<label htmlFor="email">Email</label>                    // always explicit label
<input
  id="email"
  type="email"
  aria-required="true"
  aria-invalid={!!error}
  aria-describedby={error ? 'email-error' : undefined}
/>
{error && <p id="email-error" role="alert">{error}</p>}

// Interactive elements
// min touch target: 44x44px
// focus-visible ring: always, not just focus
// disabled: opacity-50 + cursor-not-allowed + pointer-events-none

// Modals / dialogs
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Dialog Title</h2>
</div>

// Lists of items
<ul role="list" aria-label="Tasks">
  {tasks.map(t => <li key={t.id}>{t.title}</li>)}
</ul>

// Loading states
<div aria-live="polite" aria-busy={isLoading}>
  {isLoading ? <Spinner /> : <Content />}
</div>

// Images: always alt, empty alt for decorative
<img src={avatar} alt={`${user.name}'s avatar`} />
<img src={decoration} alt="" role="presentation" />
```

## 3-Layer Token Architecture (Detay)

Design token'lari 3 katmanli organize et. Hicbir component primitive token'a direkt referans vermemeli.

```
Layer 1: PRIMITIVE (Ham degerler, isim = renk/sayi)
  --blue-500, --gray-200, --space-4

Layer 2: SEMANTIC (Anlam tasiyan, isim = amac)
  --color-primary: var(--blue-600)
  --color-danger: var(--red-500)
  --color-bg: var(--white)

Layer 3: COMPONENT (Kullanim yeri, isim = component+property)
  --btn-bg: var(--color-primary)
  --card-border: var(--color-border)
  --input-focus: var(--color-primary)
```

### Tailwind Token Mapping

```typescript
// tailwind.config.ts - CSS variable'lari Tailwind'e bagla
theme: {
  extend: {
    colors: {
      primary: {
        DEFAULT: 'var(--color-primary)',
        hover: 'var(--color-primary-hover)',
        subtle: 'var(--color-primary-subtle)',
      },
    },
  },
}

// Kullanim: className="bg-primary text-white hover:bg-primary-hover"
// Dark mode token switch CSS variable'dan otomatik gelir
```

### Dark Mode Token Strategy

```css
/* Light mode (default) */
:root {
  --color-bg: #ffffff;
  --color-text: #111827;
  --color-border: #e5e7eb;
  --color-primary: #2563eb;
}

/* Dark mode - SADECE semantic token'lari override et */
.dark {
  --color-bg: #111827;
  --color-text: #f9fafb;
  --color-border: #374151;
  --color-primary: #3b82f6;
}

/* Component token'lari DEGiSMEZ - semantic'ten inherit eder */
/* --card-bg: var(--color-bg) hem light hem dark'ta dogru calisir */
```

### Referans

- Detayli design system uretimi icin: `design-system-generator` skill
- Brand tutarliligi icin: `brand-identity` skill
