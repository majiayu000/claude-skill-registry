---
name: modern-ui-designer
description: Expert guidance for creating stunning, professional 2025 UI designs using Tailwind CSS and shadcn/ui. Ensures clean minimal aesthetics, 8px grid consistency, mobile-first responsive patterns, and WCAG accessibility compliance. Use when designing interfaces, reviewing UI, creating components, or when visual design needs modern professional standards.
license: MIT
metadata:
  author: UI Design Expert
  category: design-system
  version: 2025.1
  requires: tailwind-css, shadcn-ui-knowledge
---

# Modern UI Designer - 2025 Standards

## Overview

This skill provides comprehensive guidance for creating world-class UI designs that follow modern 2025 standards. It covers Tailwind CSS best practices, shadcn/ui component patterns, clean minimalist design principles, 8px grid spacing systems, mobile-first responsive design, and WCAG accessibility compliance.

**Core Philosophy**: Professional, minimal, accessible, and consistent.

---

## Design Principles (2025)

### 1. Clean Minimalism

**Core Rules**:
- **Remove the unnecessary**: Every element must have a clear purpose
- **Whitespace is powerful**: Generous spacing improves readability and reduces cognitive load
- **Content-first**: Design serves content, not the other way around
- **Visual hierarchy**: Use size, color, and spacing to guide attention
- **Subtle over flashy**: Professional designs use restraint

**What to Avoid**:
- ❌ Rainbow gradients or excessive colors
- ❌ Decorative elements without function
- ❌ Complex patterns or textures
- ❌ Overcrowded interfaces
- ❌ Inconsistent spacing

**What to Embrace**:
- ✅ Neutral color palette (grays + one accent color)
- ✅ Generous whitespace and breathing room
- ✅ Clean typography with clear hierarchy
- ✅ Subtle shadows and borders
- ✅ Consistent 8px grid system

### 2. Visual Hierarchy Best Practices

**Size**:
- Use dramatic size differences for headings vs body text
- Minimum 16px for body text (18px preferred for readability)
- Heading scale: 48px → 32px → 24px → 20px → 18px → 16px
- Use Tailwind's text-* utilities: text-6xl, text-4xl, text-2xl, text-xl, text-lg, text-base

**Color**:
- Use color strategically to indicate importance
- Primary actions: Accent color
- Secondary actions: Neutral gray
- Disabled states: Low contrast gray
- Error states: Red (accessible contrast)
- Success states: Green (accessible contrast)

**Weight**:
- Headings: font-bold (700) or font-semibold (600)
- Body: font-normal (400) or font-medium (500)
- Captions: font-light (300) with careful use

**Spacing**:
- Large spacing (32px+) separates major sections
- Medium spacing (16-24px) groups related content
- Small spacing (8px) for tightly related items
- Internal ≤ External rule: Space inside elements should be less than space between them

---

## 8px Grid System

### Core Concept

**All spacing, sizing, and layout must use multiples of 8**:
- Base units: 8px, 16px, 24px, 32px, 40px, 48px, 56px, 64px, 72px, 80px
- Half unit: 4px (only for icons, borders, or micro-adjustments)
- Never use: 7px, 13px, 25px, or other non-conforming values

### Why 8px?

1. **Device compatibility**: Most screen resolutions are divisible by 8
2. **Scaling**: Works perfectly across @1x, @2x, @3x displays
3. **Visual consistency**: Easy to eyeball and maintain rhythm
4. **Developer-friendly**: Reduces translation errors from design to code

### Tailwind CSS Spacing Scale

Tailwind's spacing scale aligns perfectly with 8px grid:

```
0   →  0px
0.5 →  2px   (exception for borders)
1   →  4px   (half unit)
2   →  8px   (base)
3   →  12px  (1.5 units, use sparingly)
4   →  16px  (2 units)
5   →  20px  (2.5 units, use sparingly)
6   →  24px  (3 units)
8   →  32px  (4 units)
10  →  40px  (5 units)
12  →  48px  (6 units)
16  →  64px  (8 units)
20  →  80px  (10 units)
24  →  96px  (12 units)
32  →  128px (16 units)
```

**Preferred values for spacing**:
- Padding: p-2, p-4, p-6, p-8, p-12, p-16
- Margin: m-2, m-4, m-6, m-8, m-12, m-16
- Gap: gap-2, gap-4, gap-6, gap-8

### Spacing Hierarchy (Proximity Principle)

**Tightly related (8px - 16px)**:
```html
<div class="space-y-2">
  <h3 class="text-xl font-semibold">Heading</h3>
  <p class="text-gray-600">Subheading</p>
</div>
```

**Related content (24px - 32px)**:
```html
<div class="space-y-6">
  <section><!-- Content --></section>
  <section><!-- Content --></section>
</div>
```

**Separate sections (48px - 64px)**:
```html
<div class="space-y-12 md:space-y-16">
  <section><!-- Major section --></section>
  <section><!-- Major section --></section>
</div>
```

### Component Sizing with 8px Grid

**Buttons**:
- Small: h-8 (32px) with px-3 py-1.5
- Medium: h-10 (40px) with px-4 py-2
- Large: h-12 (48px) with px-6 py-3
- Extra Large: h-14 (56px) with px-8 py-4

**Input Fields**:
- Height: h-10 (40px) or h-12 (48px)
- Padding: px-3 py-2 or px-4 py-3

**Cards**:
- Padding: p-4, p-6, or p-8 depending on content
- Border radius: rounded-md (6px), rounded-lg (8px), rounded-xl (12px)

---

## Color System (Neutral + Accent)

### The Neutral Palette Approach

**Base Strategy**: Gray scale + ONE accent color

**Gray Scale (Tailwind)**:
```
slate-50   → Backgrounds
slate-100  → Subtle backgrounds
slate-200  → Borders, dividers
slate-300  → Disabled text
slate-400  → Placeholder text
slate-500  → Secondary text
slate-600  → Body text
slate-700  → Headings
slate-800  → Emphasis
slate-900  → Maximum contrast
```

**Accent Color Selection**:
- Choose ONE primary brand color
- Use for: Primary buttons, links, active states, highlights
- Shades needed: 50, 100, 200, 300, 400, 500, 600, 700, 800, 900
- Example: blue-600 for primary, blue-700 for hover

### Semantic Colors (Minimal Use)

```html
<!-- Success -->
<div class="bg-green-50 text-green-700 border border-green-200">

<!-- Warning -->
<div class="bg-yellow-50 text-yellow-800 border border-yellow-200">

<!-- Error -->
<div class="bg-red-50 text-red-700 border border-red-200">

<!-- Info -->
<div class="bg-blue-50 text-blue-700 border border-blue-200">
```

### Dark Mode Support

```html
<!-- Neutral backgrounds -->
<div class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50">

<!-- Borders -->
<div class="border border-slate-200 dark:border-slate-800">

<!-- Subtle backgrounds -->
<div class="bg-slate-50 dark:bg-slate-800">

<!-- Primary accent -->
<button class="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600">
```

### Color Contrast Rules (WCAG)

**Text Contrast Ratios**:
- Normal text (< 24px): Minimum 4.5:1
- Large text (≥ 24px): Minimum 3:1
- UI components & graphics: Minimum 3:1

**Safe Combinations**:
```
✅ slate-900 on white → 18.9:1
✅ slate-700 on white → 8.6:1
✅ slate-600 on white → 6.2:1
✅ blue-600 on white → 5.4:1
❌ slate-400 on white → 2.9:1 (fails)
❌ slate-300 on white → 1.7:1 (fails)
```

---

## Tailwind CSS Best Practices (2025)

### 1. Utility-First Approach

**DO**:
```html
<!-- ✅ Compose utilities directly -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
               focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
               transition-colors duration-200">
  Click me
</button>
```

**DON'T**:
```css
/* ❌ Avoid custom CSS unless absolutely necessary */
.custom-button {
  padding: 0.5rem 1rem;
  background: #3b82f6;
  /* ... */
}
```

### 2. Component Extraction with @apply (Sparingly)

**Use @apply ONLY for**:
- Components used 10+ times
- Third-party library overrides
- Print stylesheets

```css
/* ✅ Good use of @apply */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
           focus:outline-none focus:ring-2 focus:ring-blue-500;
  }
}
```

### 3. Responsive Design (Mobile-First)

**Breakpoints**:
```
sm:  640px  → Small tablets
md:  768px  → Tablets
lg:  1024px → Desktop
xl:  1280px → Large desktop
2xl: 1536px → Extra large
```

**Pattern**:
```html
<!-- Mobile first, then scale up -->
<div class="p-4 md:p-6 lg:p-8">
  <h1 class="text-2xl md:text-3xl lg:text-4xl">
    Responsive Heading
  </h1>
</div>

<!-- Grid responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
  <!-- Items -->
</div>
```

### 4. State Variants

**Hover, Focus, Active**:
```html
<button class="bg-blue-600 hover:bg-blue-700 active:bg-blue-800
               focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
               disabled:opacity-50 disabled:cursor-not-allowed">
```

**Dark Mode**:
```html
<div class="bg-white dark:bg-slate-900 
            text-slate-900 dark:text-slate-50
            border border-slate-200 dark:border-slate-800">
```

### 5. Class Organization (Consistent Order)

**Standard order**:
1. Layout (display, position, overflow)
2. Sizing (width, height)
3. Spacing (margin, padding)
4. Typography (font, text)
5. Visual (background, border)
6. Effects (shadow, opacity)
7. Transitions
8. Variants (hover, focus, dark)

```html
<!-- ✅ Organized -->
<div class="
  flex items-center justify-between
  w-full max-w-screen-lg
  px-4 py-3 my-2
  text-lg font-medium text-gray-800
  bg-white rounded shadow
  hover:shadow-md
  transition-shadow
">
```

### 6. JIT Mode & Purging

**Always enable JIT** (Just-In-Time mode):
```js
// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './components/**/*.{html,js,jsx,ts,tsx}',
  ],
  // ... rest of config
}
```

**Benefits**:
- Smaller CSS bundle
- Arbitrary values: `w-[373px]`
- All variants available
- Faster build times

---

## shadcn/ui Component Patterns

### Architecture Understanding

**shadcn/ui = Radix UI + Tailwind CSS + CVA**:
- **Radix UI**: Unstyled, accessible primitives
- **Tailwind CSS**: Utility-first styling
- **CVA (Class Variance Authority)**: Variant management

### Core Pattern: Copy, Own, Customize

**NOT a package**: You copy component source into your project
- Full ownership of code
- No breaking updates
- Complete customization
- Type-safe variants

### Component Anatomy Example

```tsx
// Button.tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  // Base styles (always applied)
  "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-slate-900 text-slate-50 hover:bg-slate-800",
        outline: "border border-slate-200 bg-transparent hover:bg-slate-100",
        ghost: "hover:bg-slate-100",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4",
        lg: "h-12 px-6 text-lg",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "md",
    },
  }
)

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = ({ className, variant, size, ...props }: ButtonProps) => {
  return (
    <button
      className={cn(buttonVariants({ variant, size }), className)}
      {...props}
    />
  )
}
```

### Best Practices for shadcn/ui

**1. Use `cn()` utility for class merging**:
```tsx
import { cn } from "@/lib/utils"

// Allows className override
<Button className={cn("custom-class", conditionalClass && "other-class")} />
```

**2. Design System Integration**:
```ts
// tailwind.config.js
module.exports = {
  theme: {
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
        // ... more design tokens
      },
    },
  },
}
```

**3. CSS Variables for Theming**:
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --border: 217.2 32.6% 17.5%;
}
```

### Common Patterns

**Form Field with Label**:
```tsx
<div className="space-y-2">
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    type="email"
    placeholder="you@example.com"
    className="w-full"
  />
  <p className="text-sm text-slate-500">
    We'll never share your email.
  </p>
</div>
```

**Card Layout**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description goes here</CardDescription>
  </CardHeader>
  <CardContent>
    <!-- Main content -->
  </CardContent>
  <CardFooter>
    <!-- Actions -->
  </CardFooter>
</Card>
```

**Dialog Pattern**:
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button variant="outline">Open Dialog</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Dialog Title</DialogTitle>
      <DialogDescription>
        Dialog description text
      </DialogDescription>
    </DialogHeader>
    <!-- Dialog content -->
    <DialogFooter>
      <Button variant="outline">Cancel</Button>
      <Button>Confirm</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

---

## Accessibility (WCAG 2.2 Compliance)

### The Four Principles (POUR)

**1. Perceivable**:
- Text alternatives for images
- Captions for videos
- Adaptable content structure
- Sufficient color contrast

**2. Operable**:
- Keyboard accessible
- No keyboard traps
- Sufficient time to interact
- No seizure-inducing content

**3. Understandable**:
- Readable text
- Predictable behavior
- Input assistance and error prevention

**4. Robust**:
- Compatible with assistive technologies
- Valid HTML
- Proper ARIA attributes

### Critical Requirements

**Keyboard Navigation**:
```html
<!-- ✅ Proper focus management -->
<button
  class="focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
>
  Accessible Button
</button>

<!-- ✅ Skip links -->
<a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0">
  Skip to main content
</a>
```

**Focus Indicators** (WCAG 2.2):
- Must be visible
- Minimum 2px thickness
- Contrast ratio of 3:1 against background
- Use `focus:ring-2` and `focus:ring-offset-2`

**Touch Targets**:
- Minimum 44x44px (WCAG 2.1)
- Minimum 24x24px spacing (WCAG 2.2)
- Use `min-h-[44px] min-w-[44px]` for interactive elements

**Color Contrast**:
```html
<!-- ✅ Good contrast -->
<p class="text-slate-700">Body text</p> <!-- 8.6:1 -->
<button class="bg-blue-600 text-white">Action</button> <!-- 5.4:1 -->

<!-- ❌ Poor contrast -->
<p class="text-slate-400">Fails WCAG</p> <!-- 2.9:1 -->
```

**Semantic HTML**:
```html
<!-- ✅ Use proper semantic elements -->
<header>
  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>

<main>
  <article>
    <h1>Page Title</h1>
    <section>
      <h2>Section Heading</h2>
      <!-- Content -->
    </section>
  </article>
</main>

<footer>
  <!-- Footer content -->
</footer>
```

**ARIA Labels**:
```html
<!-- Icon-only buttons -->
<button aria-label="Close dialog" class="...">
  <XIcon className="h-4 w-4" aria-hidden="true" />
</button>

<!-- Form labels -->
<label for="search" class="sr-only">Search</label>
<input id="search" type="search" />

<!-- Live regions -->
<div role="status" aria-live="polite" aria-atomic="true">
  Loading...
</div>
```

**Form Accessibility**:
```html
<form>
  <div>
    <label for="email" class="block text-sm font-medium mb-2">
      Email
      <span class="text-red-600" aria-label="required">*</span>
    </label>
    <input
      id="email"
      type="email"
      required
      aria-required="true"
      aria-describedby="email-error"
      aria-invalid={hasError ? "true" : "false"}
      class="w-full"
    />
    {hasError && (
      <p id="email-error" class="text-sm text-red-600 mt-1" role="alert">
        Please enter a valid email address
      </p>
    )}
  </div>
</form>
```

---

## Mobile-First Responsive Design

### Strategy

**Start with mobile (320px - 640px)**:
1. Design for smallest screen first
2. Optimize for touch interactions
3. Prioritize content hierarchy
4. Progressive enhancement for larger screens

### Responsive Patterns

**Container Width**:
```html
<!-- Responsive container -->
<div class="container mx-auto px-4 md:px-6 lg:px-8 max-w-7xl">
  <!-- Content -->
</div>
```

**Typography Scale**:
```html
<!-- Responsive text -->
<h1 class="text-3xl md:text-4xl lg:text-5xl font-bold">
  Responsive Heading
</h1>

<p class="text-base md:text-lg leading-relaxed">
  Body text with responsive sizing
</p>
```

**Grid Layouts**:
```html
<!-- Responsive grid -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 lg:gap-6">
  <div><!-- Card --></div>
  <div><!-- Card --></div>
  <div><!-- Card --></div>
</div>
```

**Flexbox Responsive**:
```html
<!-- Stack on mobile, row on desktop -->
<div class="flex flex-col md:flex-row gap-4 md:gap-6">
  <div class="flex-1"><!-- Content --></div>
  <div class="flex-1"><!-- Content --></div>
</div>
```

**Visibility Control**:
```html
<!-- Hide on mobile, show on desktop -->
<div class="hidden md:block">
  Desktop only content
</div>

<!-- Show on mobile, hide on desktop -->
<div class="block md:hidden">
  Mobile only content
</div>
```

**Navigation Pattern**:
```html
<!-- Mobile: Hamburger menu -->
<!-- Desktop: Horizontal nav -->
<nav>
  <!-- Mobile menu button -->
  <button class="md:hidden">
    <MenuIcon />
  </button>
  
  <!-- Desktop nav -->
  <ul class="hidden md:flex md:space-x-4">
    <li><a href="/">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```

---

## Typography System

### Font Selection

**Modern Professional Fonts**:
- **Sans-serif**: Inter, SF Pro, -apple-system, system-ui
- **Monospace**: JetBrains Mono, Fira Code, SF Mono

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
}
```

### Type Scale (8px-based)

```
text-xs   → 12px (line-height: 16px)
text-sm   → 14px (line-height: 20px)
text-base → 16px (line-height: 24px) ← Body text default
text-lg   → 18px (line-height: 28px)
text-xl   → 20px (line-height: 28px)
text-2xl  → 24px (line-height: 32px)
text-3xl  → 30px (line-height: 36px)
text-4xl  → 36px (line-height: 40px)
text-5xl  → 48px (line-height: 48px)
text-6xl  → 60px (line-height: 60px)
```

### Line Heights

**Always use 8px-aligned line heights**:
```html
<!-- Body text -->
<p class="text-base leading-6"> <!-- 16px text, 24px line-height -->

<!-- Headings -->
<h2 class="text-3xl leading-9"> <!-- 30px text, 36px line-height -->
```

### Text Hierarchy Example

```html
<article class="space-y-6">
  <!-- Main heading -->
  <h1 class="text-4xl md:text-5xl font-bold text-slate-900 leading-tight">
    Article Title
  </h1>
  
  <!-- Subtitle -->
  <p class="text-xl text-slate-600 leading-relaxed">
    Engaging subtitle or description
  </p>
  
  <!-- Meta information -->
  <div class="flex items-center gap-4 text-sm text-slate-500">
    <span>By Author Name</span>
    <span>•</span>
    <time datetime="2025-01-15">Jan 15, 2025</time>
  </div>
  
  <!-- Body content -->
  <div class="prose prose-slate max-w-none">
    <p class="text-base leading-relaxed text-slate-700">
      Body paragraph with comfortable reading size and spacing...
    </p>
  </div>
</article>
```

---

## Shadows & Elevation

### Shadow System (Subtle Professional)

```html
<!-- Subtle card elevation -->
<div class="shadow-sm"> <!-- Very subtle -->
<div class="shadow">    <!-- Default card -->
<div class="shadow-md"> <!-- Slightly raised -->
<div class="shadow-lg"> <!-- Pronounced elevation -->
<div class="shadow-xl"> <!-- Modal/dialog -->

<!-- Custom shadows (use sparingly) -->
<div class="shadow-[0_2px_8px_rgba(0,0,0,0.08)]">
```

**Modern Pattern**: Combine shadow with border
```html
<div class="border border-slate-200 shadow-sm rounded-lg">
  <!-- More refined than shadow alone -->
</div>
```

### Elevation States

```html
<!-- Card hover effect -->
<div class="border border-slate-200 shadow-sm hover:shadow-md 
            transition-shadow duration-200 rounded-lg">
  Hover me
</div>
```

---

## Border Radius Guidelines

### Consistent Rounding

```
rounded-none → 0px
rounded-sm   → 2px   (subtle, modern)
rounded      → 4px   (default)
rounded-md   → 6px   (cards)
rounded-lg   → 8px   (buttons, inputs) ← Preferred
rounded-xl   → 12px  (large cards)
rounded-2xl  → 16px  (hero sections)
rounded-full → 9999px (circles, pills)
```

**2025 Trend**: Larger, softer corners (8px - 12px)

```html
<!-- Modern button -->
<button class="px-4 py-2 bg-blue-600 text-white rounded-lg">

<!-- Card -->
<div class="border border-slate-200 rounded-xl p-6">

<!-- Avatar -->
<img class="h-10 w-10 rounded-full" />
```

---

## Component Design Examples

### Modern Button

```html
<!-- Primary -->
<button class="
  inline-flex items-center justify-center
  h-10 px-4
  text-base font-medium
  bg-blue-600 text-white
  rounded-lg
  hover:bg-blue-700
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
  active:bg-blue-800
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200
">
  Primary Action
</button>

<!-- Secondary -->
<button class="
  inline-flex items-center justify-center
  h-10 px-4
  text-base font-medium
  border border-slate-300 bg-white text-slate-700
  rounded-lg
  hover:bg-slate-50
  focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-colors duration-200
">
  Secondary Action
</button>

<!-- Ghost -->
<button class="
  inline-flex items-center justify-center
  h-10 px-4
  text-base font-medium text-slate-700
  rounded-lg
  hover:bg-slate-100
  focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2
  transition-colors duration-200
">
  Ghost Button
</button>
```

### Modern Input Field

```html
<div class="space-y-2">
  <label 
    for="email" 
    class="block text-sm font-medium text-slate-700"
  >
    Email address
  </label>
  <input
    id="email"
    type="email"
    placeholder="you@example.com"
    class="
      w-full h-10 px-3
      text-base text-slate-900 placeholder:text-slate-400
      bg-white
      border border-slate-300 rounded-lg
      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
      disabled:bg-slate-50 disabled:text-slate-500 disabled:cursor-not-allowed
      transition-colors duration-200
    "
  />
  <p class="text-sm text-slate-500">
    We'll never share your email with anyone else.
  </p>
</div>
```

### Modern Card

```html
<div class="
  bg-white
  border border-slate-200
  rounded-xl
  shadow-sm hover:shadow-md
  transition-shadow duration-200
  overflow-hidden
">
  <!-- Card header with image -->
  <div class="aspect-video bg-slate-100">
    <img 
      src="..." 
      alt="..."
      class="w-full h-full object-cover"
    />
  </div>
  
  <!-- Card content -->
  <div class="p-6 space-y-4">
    <!-- Heading -->
    <h3 class="text-xl font-semibold text-slate-900">
      Card Title
    </h3>
    
    <!-- Description -->
    <p class="text-base text-slate-600 leading-relaxed">
      Card description goes here with comfortable reading spacing.
    </p>
    
    <!-- Actions -->
    <div class="flex items-center gap-3">
      <button class="...">Primary</button>
      <button class="...">Secondary</button>
    </div>
  </div>
</div>
```

### Modern Navigation

```html
<header class="sticky top-0 z-50 bg-white border-b border-slate-200">
  <nav class="container mx-auto px-4 md:px-6">
    <div class="flex items-center justify-between h-16">
      <!-- Logo -->
      <a href="/" class="flex items-center gap-2">
        <img src="logo.svg" alt="Logo" class="h-8 w-8" />
        <span class="text-xl font-bold text-slate-900">Brand</span>
      </a>
      
      <!-- Desktop navigation -->
      <ul class="hidden md:flex items-center gap-8">
        <li>
          <a href="/" class="text-sm font-medium text-slate-700 hover:text-slate-900">
            Home
          </a>
        </li>
        <li>
          <a href="/about" class="text-sm font-medium text-slate-700 hover:text-slate-900">
            About
          </a>
        </li>
        <li>
          <a href="/contact" class="text-sm font-medium text-slate-700 hover:text-slate-900">
            Contact
          </a>
        </li>
      </ul>
      
      <!-- CTA -->
      <button class="hidden md:inline-flex ...">
        Get Started
      </button>
      
      <!-- Mobile menu button -->
      <button class="md:hidden" aria-label="Open menu">
        <MenuIcon class="h-6 w-6" />
      </button>
    </div>
  </nav>
</header>
```

---

## Anti-Patterns to Avoid

### ❌ DON'T DO THESE

**1. Inconsistent Spacing**:
```html
<!-- ❌ Bad: Random spacing values -->
<div class="mt-3 mb-5 px-7">

<!-- ✅ Good: 8px grid aligned -->
<div class="my-4 px-6">
```

**2. Poor Color Contrast**:
```html
<!-- ❌ Bad: Fails WCAG -->
<p class="text-slate-400">Important text</p>

<!-- ✅ Good: Passes WCAG -->
<p class="text-slate-700">Important text</p>
```

**3. Missing Focus Styles**:
```html
<!-- ❌ Bad: No focus indicator -->
<button class="outline-none">

<!-- ✅ Good: Clear focus ring -->
<button class="focus:outline-none focus:ring-2 focus:ring-blue-500">
```

**4. Non-Semantic HTML**:
```html
<!-- ❌ Bad: Divs for everything -->
<div onClick="navigate()">Home</div>

<!-- ✅ Good: Semantic elements -->
<a href="/home">Home</a>
```

**5. Tiny Touch Targets**:
```html
<!-- ❌ Bad: Too small for touch -->
<button class="p-1">×</button>

<!-- ✅ Good: Minimum 44x44px -->
<button class="p-3 min-h-[44px] min-w-[44px]">×</button>
```

**6. Over-Styled Designs**:
```html
<!-- ❌ Bad: Rainbow chaos -->
<div class="bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 
            shadow-2xl border-4 border-yellow-400 rounded-3xl">

<!-- ✅ Good: Minimal & professional -->
<div class="bg-white border border-slate-200 rounded-lg shadow-sm">
```

**7. Fixed Pixel Widths**:
```html
<!-- ❌ Bad: Breaks on small screens -->
<div class="w-[800px]">

<!-- ✅ Good: Responsive -->
<div class="w-full max-w-3xl">
```

---

## Quick Review Checklist

### Design Review (Before Development)

**Visual Design**:
- [ ] Uses neutral color palette (grays + 1 accent)
- [ ] Follows 8px grid for all spacing and sizing
- [ ] Maintains consistent border radius (8px - 12px)
- [ ] Uses subtle shadows (not heavy drop shadows)
- [ ] Typography hierarchy is clear
- [ ] Whitespace is generous and purposeful

**Responsiveness**:
- [ ] Mobile-first design approach
- [ ] Touch targets are minimum 44x44px
- [ ] Text is readable without zooming
- [ ] Content reflows properly at all breakpoints
- [ ] Navigation works on mobile

**Accessibility**:
- [ ] Color contrast meets WCAG 2.2 (4.5:1 minimum)
- [ ] Focus indicators are visible (2px ring)
- [ ] Semantic HTML used correctly
- [ ] ARIA labels on icon-only buttons
- [ ] Form labels are properly associated

**Components**:
- [ ] Buttons have hover, focus, and active states
- [ ] Form inputs have validation states
- [ ] Loading states are designed
- [ ] Error states are clear and helpful
- [ ] Empty states are friendly

### Development Review (After Implementation)

**Technical**:
- [ ] Tailwind classes follow consistent order
- [ ] JIT mode enabled and purging configured
- [ ] No custom CSS unless absolutely necessary
- [ ] Dark mode support implemented
- [ ] Performance optimized (lazy loading, etc.)

**Accessibility Testing**:
- [ ] Keyboard navigation works completely
- [ ] Screen reader tested (NVDA/VoiceOver)
- [ ] Color contrast verified with tool
- [ ] Forms are fully accessible
- [ ] ARIA attributes used correctly

**Responsive Testing**:
- [ ] Tested on mobile (375px, 414px)
- [ ] Tested on tablet (768px, 1024px)
- [ ] Tested on desktop (1280px, 1920px)
- [ ] Touch interactions work properly
- [ ] No horizontal scroll at any size

---

## Advanced Techniques

### 1. Tailwind CSS Variables for Theming

```css
@layer base {
  :root {
    /* Spacing */
    --spacing-xs: 0.5rem;  /* 8px */
    --spacing-sm: 1rem;    /* 16px */
    --spacing-md: 1.5rem;  /* 24px */
    --spacing-lg: 2rem;    /* 32px */
    
    /* Colors */
    --color-primary: 220 90% 56%;
    --color-primary-hover: 220 90% 48%;
    
    /* Border radius */
    --radius-sm: 0.5rem;  /* 8px */
    --radius-md: 0.75rem; /* 12px */
    --radius-lg: 1rem;    /* 16px */
  }
}
```

### 2. Custom Utility Classes

```css
@layer utilities {
  /* Text balance for headings */
  .text-balance {
    text-wrap: balance;
  }
  
  /* Smooth scroll */
  .scroll-smooth {
    scroll-behavior: smooth;
  }
  
  /* Focus visible only */
  .focus-visible-ring {
    @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500;
  }
}
```

### 3. Component Composition Pattern

```tsx
// Compose smaller components into larger ones
<Card>
  <CardHeader>
    <div className="flex items-center justify-between">
      <div className="space-y-1">
        <CardTitle>Dashboard</CardTitle>
        <CardDescription>Welcome back</CardDescription>
      </div>
      <Button variant="outline" size="sm">
        <SettingsIcon className="h-4 w-4" />
      </Button>
    </div>
  </CardHeader>
  <CardContent>
    <Tabs defaultValue="overview">
      <TabsList>
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="analytics">Analytics</TabsTrigger>
      </TabsList>
      <TabsContent value="overview" className="space-y-4">
        {/* Content */}
      </TabsContent>
    </Tabs>
  </CardContent>
</Card>
```

---

## Resources & Tools

### Design Tools
- **Figma**: Primary design tool
- **Tailwind CSS IntelliSense**: VS Code extension
- **Headless UI**: Unstyled accessible components
- **Radix UI**: Primitive components for shadcn/ui

### Accessibility Testing
- **WAVE**: Browser extension for accessibility testing
- **axe DevTools**: Automated accessibility testing
- **Contrast Checker**: Verify WCAG color contrast
- **NVDA/VoiceOver**: Screen reader testing

### Color Tools
- **Coolors**: Color palette generator
- **Tailwind Shades**: Generate Tailwind color scales
- **Contrast Ratio**: WebAIM contrast checker

### Typography
- **Typescale**: Generate type scales
- **Modular Scale**: Calculate harmonious sizes
- **Google Fonts**: Free web fonts

### Learning Resources
- **Tailwind CSS Documentation**: Official docs
- **shadcn/ui Documentation**: Component library docs
- **WCAG Guidelines**: W3C accessibility standards
- **Refactoring UI**: Design tips by Tailwind creators

---

## Summary

**Modern UI Design in 2025 means**:

1. **Clean Minimalism**: Remove the unnecessary, embrace whitespace
2. **8px Grid System**: Consistent, scalable spacing and sizing
3. **Neutral + Accent**: Grays with one primary color
4. **Tailwind CSS**: Utility-first, JIT-enabled, responsive
5. **shadcn/ui**: Copy-and-own accessible components
6. **WCAG 2.2**: Full keyboard support and color contrast
7. **Mobile-First**: Design small screens first, scale up
8. **Professional Polish**: Subtle shadows, soft corners, smooth transitions

**Remember**: The goal is not to impress with flashy design, but to create interfaces that are beautiful, functional, accessible, and a pleasure to use.

---

## When to Use This Skill

**Activate this skill when**:
- Designing new UI components or pages
- Reviewing existing designs for modern standards
- Creating design systems or component libraries
- Implementing Tailwind CSS or shadcn/ui
- Ensuring accessibility compliance
- Optimizing responsive layouts
- Troubleshooting visual design issues
- Teaching or documenting UI best practices

**Output Format**: Always provide code examples, explain design decisions, and reference specific Tailwind utilities or shadcn/ui components when applicable.
