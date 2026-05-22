---
name: sikhaid-styling
description: Use when working on UI, styling, colors, or design in SikhAid project. Covers brand colors (navy/orange), Tailwind CSS patterns, custom animations, typography, responsive design, and the design system.
allowed-tools: Read, Edit
---

# SikhAid Design System & Styling

## Brand Colors

### Primary Colors
```css
--navy: #1a237e        /* Primary brand color - Dark blue */
--navy-dark: #0d1660   /* Darker shade for hover/active states */
--orange: #FFA617      /* Accent color - Bright orange */
--orange-dark: #e89500 /* Darker orange for hover states */
```

**Usage:**
- **Navy** - Primary buttons, headings, navigation background
- **Orange** - CTAs, highlights, active states, links
- **Navy Dark** - Hover states for navy elements
- **Orange Dark** - Hover states for orange elements

### Custom Color Classes
**Defined in:** `src/app.css`

```css
.text-orange-custom { color: var(--orange); }
.text-orange-dark { color: var(--orange-dark); }
.text-navy-custom { color: var(--navy); }
.text-navy-dark { color: var(--navy-dark); }

.bg-orange-custom { background-color: var(--orange); }
.bg-orange-dark { background-color: var(--orange-dark); }
.bg-navy { background-color: var(--navy); }
.bg-navy-dark { background-color: var(--navy-dark); }

.border-orange-custom { border-color: var(--orange); }
.border-navy { border-color: var(--navy); }
```

### Neutral Colors (Tailwind Defaults)
- Gray scale: `gray-50` through `gray-900`
- White: `white` / `#ffffff`
- Black: `black` / `#000000`

## Typography

### Font Family
**System:** Tailwind's default font stack (Inter-based sans-serif)
- No custom fonts loaded
- Uses system fonts for performance

### Font Sizes
**Tailwind scale used throughout:**
```
text-xs    → 0.75rem   (12px)
text-sm    → 0.875rem  (14px)
text-base  → 1rem      (16px)
text-lg    → 1.125rem  (18px)
text-xl    → 1.25rem   (20px)
text-2xl   → 1.5rem    (24px)
text-3xl   → 1.875rem  (30px)
text-4xl   → 2.25rem   (36px)
text-5xl   → 3rem      (48px)
text-6xl   → 3.75rem   (60px)
text-7xl   → 4.5rem    (72px)
```

### Font Weights
```
font-normal    → 400
font-medium    → 500
font-semibold  → 600
font-bold      → 700
font-extrabold → 800
```

### Responsive Typography Pattern
```svelte
<!-- Mobile → Desktop progression -->
<h1 class="text-3xl md:text-5xl lg:text-7xl font-bold">
  Heading
</h1>

<p class="text-sm md:text-base lg:text-lg">
  Body text
</p>
```

## Tailwind CSS Configuration

### Config File
**Location:** `tailwind.config.js`

```javascript
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {},  // Uses default Tailwind theme
  },
  plugins: [],
}
```

### Global Styles
**Location:** `src/app.css`

**Structure:**
```css
@tailwind base;       /* Tailwind's base styles */
@tailwind components; /* Tailwind's component classes */
@tailwind utilities;  /* Tailwind's utility classes */

:root {
  /* Custom CSS variables */
}

/* Custom utility classes */
/* Custom animations */
/* Paper texture background */
```

## Custom Animations

### Animation Definitions
**Defined in:** `src/app.css`

#### 1. Fade In
```css
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out;
}
```

**Usage:** General element entrance
**Example:** Hero text, cards appearing

#### 2. Slide Up
```css
@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out;
}
```

**Usage:** Bottom-to-top entrances
**Example:** Section content, buttons

#### 3. Bounce In
```css
@keyframes bounce-in {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-bounce-in {
  animation: bounce-in 0.8s ease-out;
}
```

**Usage:** Attention-grabbing entrances
**Example:** Impact counters, call-to-action buttons

### Animation Delays
**For staggered animations:**
```css
.delay-200 { animation-delay: 0.2s; }
.delay-400 { animation-delay: 0.4s; }
.delay-600 { animation-delay: 0.6s; }
.delay-800 { animation-delay: 0.8s; }
.delay-1000 { animation-delay: 1s; }
```

**Usage Example:**
```svelte
<div class="animate-fade-in delay-200">First</div>
<div class="animate-fade-in delay-400">Second</div>
<div class="animate-fade-in delay-600">Third</div>
```

## Paper Texture Background

### Implementation
**Defined in:** `src/app.css`

```css
.paper-texture-bg {
  background-color: #f5f5f0;
  background-image:
    repeating-linear-gradient(
      0deg, transparent, transparent 2px, rgba(0,0,0,.02) 2px, rgba(0,0,0,.02) 3px
    ),
    repeating-linear-gradient(
      90deg, transparent, transparent 2px, rgba(0,0,0,.02) 2px, rgba(0,0,0,.02) 3px
    ),
    radial-gradient(ellipse at 10% 20%, rgba(255,165,0,.05) 0%, transparent 50%);
  background-blend-mode: multiply;
}
```

**Effect:** Subtle paper-like texture with grain and slight warmth
**Usage:** Background for main content areas

## Responsive Design Patterns

### Breakpoints (Tailwind Defaults)
```
sm:  640px   (Mobile landscape, small tablets)
md:  768px   (Tablets)
lg:  1024px  (Laptops, small desktops)
xl:  1280px  (Desktops)
2xl: 1536px  (Large desktops)
```

### Mobile-First Approach
**Default styles target mobile, then scale up:**

```svelte
<!-- Base = Mobile, md = Tablet+, lg = Desktop+ -->
<div class="px-4 md:px-8 lg:px-16">
  <h1 class="text-2xl md:text-4xl lg:text-6xl">
    Responsive Heading
  </h1>
</div>
```

### Common Responsive Patterns

#### Grid Layouts
```svelte
<!-- 1 column mobile → 2 tablet → 3 desktop -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  {#each items as item}
    <div>...</div>
  {/each}
</div>
```

#### Flex Layouts
```svelte
<!-- Stack mobile → Row desktop -->
<div class="flex flex-col md:flex-row gap-4">
  <div>Left</div>
  <div>Right</div>
</div>
```

#### Text Alignment
```svelte
<!-- Center mobile → Left desktop -->
<div class="text-center md:text-left">
  Content
</div>
```

#### Spacing
```svelte
<!-- Smaller padding mobile → Larger desktop -->
<section class="py-8 md:py-16 lg:py-24">
  Content
</section>
```

## Button Styles

### Primary Button
```svelte
<button class="
  bg-orange-custom hover:bg-orange-dark
  text-white font-semibold
  px-6 py-3 rounded-lg
  transition-colors duration-300
  shadow-md hover:shadow-lg
">
  Primary Action
</button>
```

### Secondary Button (Navy)
```svelte
<button class="
  bg-navy hover:bg-navy-dark
  text-white font-semibold
  px-6 py-3 rounded-lg
  transition-colors duration-300
">
  Secondary Action
</button>
```

### Outline Button
```svelte
<button class="
  border-2 border-orange-custom
  text-orange-custom hover:bg-orange-custom hover:text-white
  font-semibold px-6 py-3 rounded-lg
  transition-all duration-300
">
  Outline Button
</button>
```

### Disabled Button
```svelte
<button
  disabled
  class="
    bg-gray-300 text-gray-500
    px-6 py-3 rounded-lg
    cursor-not-allowed opacity-50
  "
>
  Disabled
</button>
```

## Card Styles

### Standard Card
```svelte
<div class="
  bg-white
  rounded-lg shadow-lg
  overflow-hidden
  transition-transform duration-300
  hover:scale-105 hover:shadow-xl
">
  <img src="..." alt="..." class="w-full h-48 object-cover" />
  <div class="p-6">
    <h3 class="text-xl font-bold text-navy-custom mb-2">Title</h3>
    <p class="text-gray-600">Description</p>
  </div>
</div>
```

### Campaign Card Pattern
```svelte
<div class="
  bg-white rounded-xl shadow-md
  overflow-hidden cursor-pointer
  transform transition-all duration-300
  hover:-translate-y-2 hover:shadow-2xl
">
  <!-- Card content -->
</div>
```

## Form Input Styles

### Text Input
```svelte
<input
  type="text"
  class="
    w-full px-4 py-3
    border border-gray-300 rounded-lg
    focus:outline-none focus:ring-2 focus:ring-orange-custom
    focus:border-transparent
    transition-all
  "
  placeholder="Enter text..."
/>
```

### Text Area
```svelte
<textarea
  class="
    w-full px-4 py-3
    border border-gray-300 rounded-lg
    focus:outline-none focus:ring-2 focus:ring-orange-custom
    focus:border-transparent
    resize-none
  "
  rows="4"
></textarea>
```

### Select Dropdown
```svelte
<select class="
  w-full px-4 py-3
  border border-gray-300 rounded-lg
  focus:outline-none focus:ring-2 focus:ring-orange-custom
  bg-white
">
  <option>Option 1</option>
  <option>Option 2</option>
</select>
```

### Input with Error State
```svelte
<input
  type="email"
  class="
    w-full px-4 py-3 rounded-lg
    border-2
    {hasError ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-orange-custom'}
    focus:outline-none focus:ring-2
  "
/>
{#if hasError}
  <p class="text-red-500 text-sm mt-1">Error message</p>
{/if}
```

## Shadow & Depth System

### Shadow Utilities (Tailwind)
```
shadow-sm   → Small shadow
shadow      → Default shadow
shadow-md   → Medium shadow
shadow-lg   → Large shadow (common for cards)
shadow-xl   → Extra large shadow
shadow-2xl  → Maximum shadow
```

### Hover Shadow Pattern
```svelte
<div class="shadow-lg hover:shadow-2xl transition-shadow duration-300">
  Card with hover effect
</div>
```

## Border Radius System

### Tailwind Utilities
```
rounded-sm   → 0.125rem (2px)
rounded      → 0.25rem  (4px)
rounded-md   → 0.375rem (6px)
rounded-lg   → 0.5rem   (8px)  ← Most common
rounded-xl   → 0.75rem  (12px)
rounded-2xl  → 1rem     (16px)
rounded-full → 9999px   (circular)
```

### Usage Pattern
```svelte
<!-- Cards -->
<div class="rounded-lg">...</div>
<div class="rounded-xl">...</div>

<!-- Buttons -->
<button class="rounded-lg">...</button>

<!-- Circular elements -->
<div class="rounded-full">...</div>
```

## Layout Containers

### Standard Container
```svelte
<div class="container mx-auto px-4 md:px-8 lg:px-16">
  <!-- Content with responsive padding -->
</div>
```

### Full-Width Section
```svelte
<section class="w-full py-16 md:py-24">
  <div class="container mx-auto px-4">
    <!-- Centered content -->
  </div>
</section>
```

### Hero Section Pattern
```svelte
<section class="
  relative h-screen
  bg-cover bg-center bg-no-repeat
  flex items-center justify-center
">
  <div class="absolute inset-0 bg-black bg-opacity-50"></div>
  <div class="relative z-10 text-center text-white">
    <!-- Hero content -->
  </div>
</section>
```

## Common Spacing Values

### Padding/Margin (Tailwind Scale)
```
p-2  → 0.5rem   (8px)
p-4  → 1rem     (16px)  ← Common
p-6  → 1.5rem   (24px)
p-8  → 2rem     (32px)
p-12 → 3rem     (48px)
p-16 → 4rem     (64px)
```

### Gap (for Flex/Grid)
```
gap-2  → 0.5rem
gap-4  → 1rem    ← Common
gap-6  → 1.5rem
gap-8  → 2rem
```

## Transition Patterns

### Standard Transition
```svelte
<div class="transition-all duration-300">
  <!-- All properties transition smoothly -->
</div>
```

### Specific Property Transitions
```svelte
<button class="transition-colors duration-300">Color change</button>
<div class="transition-transform duration-300">Transform change</div>
<div class="transition-shadow duration-300">Shadow change</div>
```

### Ease Timing
```
ease-in      → Slow start
ease-out     → Slow end (most common)
ease-in-out  → Slow start and end
```

## Icon Styling (Iconify)

### Basic Usage
```svelte
<script>
  import { Icon } from '@iconify/svelte';
</script>

<Icon icon="mdi:heart" class="text-2xl text-orange-custom" />
<Icon icon="mdi:email" class="text-3xl text-navy-custom" />
```

### Common Icon Classes
```svelte
<!-- Size -->
<Icon icon="mdi:icon" class="text-xl" />   <!-- 20px -->
<Icon icon="mdi:icon" class="text-2xl" />  <!-- 24px -->
<Icon icon="mdi:icon" class="text-4xl" />  <!-- 36px -->

<!-- Color -->
<Icon icon="mdi:icon" class="text-orange-custom" />
<Icon icon="mdi:icon" class="text-navy-custom" />

<!-- Inline with text -->
<Icon icon="mdi:icon" class="inline-block mr-2" />
```

## When to Use This Skill
- Styling new components or pages
- Applying brand colors and design system
- Creating animations or transitions
- Building responsive layouts
- Designing forms or buttons
- Working with Tailwind utilities
- Adding custom CSS styles

## Related Skills
- `sikhaid-components` - Component structure and patterns
- `sikhaid-overview` - Project setup and configuration
