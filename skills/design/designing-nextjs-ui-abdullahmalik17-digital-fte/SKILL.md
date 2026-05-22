---
name: designing-nextjs-ui
description: |
  Create professional, attractive, and visually striking user interfaces in Next.js.
  Use when building beautiful websites, landing pages, dashboards, or any UI that needs
  to stand out. Covers Tailwind CSS utilities, typography, animations, visual effects,
  responsive layouts, and modern design patterns. Includes gradient text, glass morphism,
  hover effects, and comprehensive spacing/layout systems.
  NOT when doing basic HTML/CSS without a framework.
---

# Designing Professional Next.js UIs

Create visually stunning and highly functional interfaces using modern design patterns and Tailwind CSS.

## Design Philosophy

**Avoid generic aesthetics.** Every interface should have a clear visual identity:
- Choose distinctive fonts (avoid overused Inter, Roboto, Arial)
- Commit to a bold aesthetic direction (minimalist, maximalist, editorial, etc.)
- Use intentional color palettes with purpose
- Add visual depth through shadows, gradients, and effects
- Create memorable layouts that break from standard patterns

**Balance beauty with function.** Beautiful design serves the user experience:
- Maintain clear hierarchy and readability
- Use animations purposefully, not gratuitously
- Ensure accessibility (contrast, semantic HTML, screen readers)
- Optimize for performance (next/font, proper image handling)

## The "Gold Standard" Stack

Don't reinvent the wheel. Use this proven combination for consistency and speed.

1.  **Tailwind CSS**: For utility-first styling.
2.  **Shadcn UI**: For copy-paste accessible components (based on Radix UI).
3.  **Framer Motion**: For declarative animations.
4.  **Lucide React**: For consistent, clean iconography.

## Visual Hierarchy & Typography

### Fonts (`next/font`)
Use `next/font/google` to eliminate layout shift.
*   **Primary:** `Inter` or `Geist Sans` (clean, modern legibility).
*   **Headings (Optional):** `Playfair Display` or `Merriweather` (for "classy" contrast).

```tsx
import { Inter, Playfair_Display } from 'next/font/google'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })
const playfair = Playfair_Display({ subsets: ['latin'], variable: '--font-playfair' })

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
```

## Data Presentation Patterns

### 1. KPI / Metric Cards
Isolate key numbers. Use the "Label (Muted) -> Value (Bold) -> Context (Color)" hierarchy.

```tsx
// See references/ui-patterns.md for full component code
<Card>
  <CardHeader className="pb-2">
    <CardTitle className="text-sm font-medium text-muted-foreground">
      Total Revenue
    </CardTitle>
  </CardHeader>
  <CardContent>
    <div className="text-2xl font-bold">$45,231.89</div>
    <p className="text-xs text-emerald-500 flex items-center mt-1">
      +20.1% from last month
    </p>
  </CardContent>
</Card>
```

### 2. The "Bento Grid" Layout
Organize dashboard widgets into a grid of distinct rectangular areas.

```tsx
<div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4">
  <div className="md:col-span-2 md:row-span-2 rounded-xl border bg-card text-card-foreground shadow">
    {/* Main Chart */}
  </div>
  <div className="md:col-span-1 rounded-xl border bg-card text-card-foreground shadow">
    {/* KPI 1 */}
  </div>
  <div className="md:col-span-1 rounded-xl border bg-card text-card-foreground shadow">
    {/* KPI 2 */}
  </div>
  <div className="md:col-span-2 rounded-xl border bg-card text-card-foreground shadow">
    {/* Recent Activity List */}
  </div>
</div>
```

### 3. Professional Tables
*   **Alignment:** Text left, Numbers right.
*   **Headers:** Muted uppercase or simple gray text.
*   **Rows:** Border separators (no zebra striping usually).
*   **Font:** Monospace for tabular numbers (`font-mono`) if strict alignment is needed.

## Visual Effects & Modern UI

### Gradient Text (Eye-Catching)
Create stunning gradient text effects:

```tsx
<h1 className="text-5xl font-extrabold">
  <span className="bg-gradient-to-r from-pink-500 to-violet-500 bg-clip-text text-transparent">
    Beautiful Gradient
  </span>
</h1>
```

### Glass Morphism (Modern Depth)
Frosted glass effect for cards and overlays:

```tsx
<div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 ring-1 ring-white/20 shadow-xl">
  <h3>Glass Card</h3>
</div>
```

### Animations & Motion
Use animations strategically for attention and feedback:

- `animate-bounce` - Scroll indicators, CTAs
- `animate-pulse` - Loading states, skeleton loaders
- `animate-spin` - Loading spinners
- Hover effects: `hover:scale-105`, `hover:shadow-xl`
- Transitions: `transition-all duration-300`

**See references/visual-effects.md** for comprehensive guide on gradients, shadows, blur effects, animations, and hover patterns.

## Advanced Typography

### Making Words Stand Out

**Color Emphasis:**
```tsx
<p className="text-gray-700">
  Normal text with <span className="font-semibold text-violet-600">highlighted words</span>
</p>
```

**Gradient Text:**
```tsx
<span className="bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent">
  Vibrant text
</span>
```

**Background Highlight:**
```tsx
<span className="bg-yellow-200 px-1 font-medium">marked text</span>
```

**Weight & Size Contrast:**
- Mix `font-light` with `font-bold` in same paragraph
- Use large numbers (`text-6xl`) with small labels (`text-xs`)
- Vary letter spacing: `tracking-tight`, `tracking-wide`, `tracking-widest`

**See references/typography-advanced.md** for font loading, hierarchy systems, responsive typography, and dark mode patterns.

## Responsive Layouts

### Mobile-First Approach
Always design for mobile first, then enhance for larger screens:

```tsx
<div className="
  grid grid-cols-1           /* Mobile: single column */
  sm:grid-cols-2             /* Tablet: 2 columns */
  lg:grid-cols-3             /* Desktop: 3 columns */
  gap-4 sm:gap-6 lg:gap-8    /* Progressive spacing */
">
  {/* Grid items */}
</div>
```

### Spacing Scale
Use consistent spacing (0.25rem increments):
- `gap-2`, `gap-4`, `gap-6`, `gap-8` - Between items
- `p-4`, `px-6`, `py-8` - Padding
- `mt-8`, `mb-4`, `mx-auto` - Margins

### Layout Patterns
- **Flexbox**: `flex items-center justify-between`
- **Grid**: `grid grid-cols-4 gap-4`
- **Container**: `max-w-6xl mx-auto px-4`
- **Aspect Ratio**: `aspect-video`, `aspect-square`

**See references/layout-patterns.md** for complete responsive patterns, Flexbox, Grid systems, spacing utilities, and container patterns.

## Micro-Interactions (Framer Motion)

Make the app feel "alive" but not noisy.

```tsx
// Subtle fade-in for page content
<motion.div
  initial={{ opacity: 0, y: 10 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {children}
</motion.div>
```

## Quick Reference

**Typography:**
- Fonts: Use `next/font/google` for zero layout shift
- Hierarchy: `text-6xl` → `text-4xl` → `text-2xl` → `text-xl` → `text-base`
- Emphasis: Gradient text, color contrast, weight variation

**Visual Effects:**
- Gradients: `bg-gradient-to-r from-{color} to-{color}`
- Shadows: `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`
- Blur: `backdrop-blur-md`, `backdrop-blur-lg`
- Animations: `animate-bounce`, `animate-pulse`, `hover:scale-105`

**Layout:**
- Responsive: `sm:`, `md:`, `lg:`, `xl:` breakpoints
- Flexbox: `flex items-center justify-between gap-4`
- Grid: `grid grid-cols-{n} gap-{size}`
- Spacing: `p-{n}`, `m-{n}`, `gap-{n}` (multiples of 0.25rem)

**Colors:**
- Text: `text-gray-900 dark:text-white`
- Background: `bg-white dark:bg-gray-800`
- Borders: `border border-gray-200 dark:border-gray-700`

## Verification

Run: `python scripts/verify.py`

## Related Skills

- **building-nextjs-apps** - Core Next.js architecture
- **styling-with-shadcn** - Deep dive into Shadcn components
