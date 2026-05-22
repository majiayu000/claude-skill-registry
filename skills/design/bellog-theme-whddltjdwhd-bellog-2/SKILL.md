---
name: bellog-theme
description: Provides theme integration guidelines and CSS variable usage patterns for the Bellog blog. Triggers when creating styled components or working with colors.
---

# Bellog Theme Integration

This skill defines how to properly integrate with Bellog's theme system using CSS variables and TailwindCSS utility classes.

## Theme System Architecture

Bellog uses **HSL-based CSS variables** for all colors, enabling seamless dark/light mode switching.

**Location:** `/src/styles/global.css`

```css
:root {
  --background: 0 0% 98%;
  --foreground: 240 10% 3.9%;
  --primary: 262 83% 58%;
  /* ... more variables */
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 263 70% 50%;
  /* ... more variables */
}
```

## Available CSS Variables

### Core Colors

```typescript
// Background & Text
--background       // Main page background
--foreground       // Main text color

// Cards & Containers
--card             // Card backgrounds
--card-foreground  // Text on cards

// Interactive Elements
--primary          // Primary brand color (purple)
--primary-foreground

--secondary        // Secondary accent
--secondary-foreground

--accent           // Tertiary accent
--accent-foreground

--muted            // Subdued elements
--muted-foreground

// UI Borders & Inputs
--border           // All border colors
--input            // Input field borders
--ring             // Focus ring color
```

### Brand Colors

```typescript
// GitHub integration
--github-bg
--github-border
--github-text
--github-subtext

// Velog integration
--velog-bg
--velog-border
--velog-text
--velog-subtext
```

### Semantic Colors

```typescript
--destructive           // Error, danger states
--destructive-foreground

// Note: Success/warning colors not defined - use primary/accent for positive states
```

## Usage Patterns

### ✅ Correct Usage

```typescript
// Background & Text
className="bg-background text-foreground"

// Cards
className="bg-card text-card-foreground"

// Primary actions
className="bg-primary text-primary-foreground hover:bg-primary/90"

// Borders
className="border-border"

// Muted/secondary text
className="text-muted-foreground"
```

### ❌ Incorrect Usage (Never Do This)

```typescript
// ❌ Hardcoded colors
className="bg-white text-black"
className="bg-gray-100 text-gray-900"
className="bg-blue-500"

// ❌ Direct color values
className="bg-[#ffffff]"
style={{ backgroundColor: "#000000" }}

// ❌ Non-semantic Tailwind colors
className="bg-slate-50 text-slate-950"
```

## Opacity Patterns

Use opacity modifiers for subtle effects:

```typescript
// 5% - Very subtle backgrounds
className="bg-primary/5"

// 10% - Hover backgrounds
className="hover:bg-primary/10"

// 20% - Active/selected states
className="bg-primary/20"

// 50% - Borders, dividers
className="border-border/50"

// 90% - Hover states for solid buttons
className="hover:bg-primary/90"
```

## Common Component Patterns

### Card Component

```typescript
<div className="
  p-6 rounded-3xl
  bg-card border border-border/50
  text-card-foreground
  shadow-sm hover:shadow-md
  hover:scale-[1.02] hover:border-primary/20
  transition-all duration-300
  backdrop-blur-xl
">
  {/* Card content */}
</div>
```

**Key elements:**
- `bg-card` - Adapts to theme automatically
- `border-border/50` - Subtle border
- `hover:border-primary/20` - Interactive feedback

### Button Component

```typescript
// Primary button
<button className="
  px-6 py-3 rounded-full
  bg-primary text-primary-foreground
  hover:bg-primary/90
  transition-colors duration-200
  focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2
">
  Click me
</button>

// Secondary button
<button className="
  px-6 py-3 rounded-full
  bg-secondary text-secondary-foreground
  hover:bg-secondary/90
  transition-colors duration-200
">
  Secondary
</button>

// Ghost button
<button className="
  px-6 py-3 rounded-full
  hover:bg-accent hover:text-accent-foreground
  transition-colors duration-200
">
  Ghost
</button>
```

### Input Component

```typescript
<input className="
  px-4 py-2 rounded-xl
  bg-background
  border border-input
  text-foreground placeholder:text-muted-foreground
  focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2
  transition-colors
" />
```

### Navigation Component

```typescript
<nav className="
  sticky top-0 z-50
  bg-background/80 backdrop-blur-xl
  border-b border-border/50
">
  <a className="
    text-foreground
    hover:text-primary
    transition-colors
  ">
    Link
  </a>
</nav>
```

### Tag/Badge Component

```typescript
<span className="
  px-3 py-1 rounded-full
  bg-primary/10 text-primary
  border border-primary/20
  text-sm
">
  Tag
</span>

// Muted version
<span className="
  px-3 py-1 rounded-full
  bg-muted text-muted-foreground
  text-sm
">
  Muted Tag
</span>
```

### Modal/Dialog Overlay

```typescript
<div className="
  fixed inset-0 z-50
  bg-background/80 backdrop-blur-sm
">
  <div className="
    bg-card border border-border
    text-card-foreground
    rounded-3xl shadow-2xl
  ">
    {/* Modal content */}
  </div>
</div>
```

## Gradient Patterns

When gradients are needed (sparingly):

```typescript
// Primary gradient background
className="bg-gradient-to-br from-primary/20 to-primary/5"

// Muted gradient
className="bg-gradient-to-br from-muted/50 to-background"

// Border gradient (use pseudo-elements)
className="relative before:absolute before:inset-0 before:rounded-3xl before:p-[1px] before:bg-gradient-to-br before:from-primary/50 before:to-transparent"
```

## Dark Mode Handling

**Important:** You DO NOT need to manually handle dark mode. CSS variables automatically adapt.

```typescript
// ✅ Correct - Variables handle it
className="bg-background text-foreground"

// ❌ Wrong - Manual dark mode classes
className="bg-white dark:bg-black text-black dark:text-white"
```

**Exception:** When you need different behavior between modes:

```typescript
className="shadow-sm dark:shadow-xl"
className="opacity-100 dark:opacity-80"
```

## Hover States

Standard hover patterns:

```typescript
// Color shift
className="text-foreground hover:text-primary"

// Background change
className="hover:bg-accent hover:text-accent-foreground"

// Opacity change
className="opacity-70 hover:opacity-100"

// Border emphasis
className="border-border/50 hover:border-primary/50"

// Multiple effects
className="hover:bg-primary/10 hover:text-primary hover:border-primary/20"
```

## Focus States

Always include focus states for accessibility:

```typescript
className="
  focus:outline-none
  focus-visible:ring-2
  focus-visible:ring-primary
  focus-visible:ring-offset-2
  focus-visible:ring-offset-background
"
```

## Text Hierarchy

```typescript
// Headings
className="text-foreground"

// Body text
className="text-foreground"

// Secondary text
className="text-muted-foreground"

// Disabled text
className="text-muted-foreground/50"

// Links
className="text-primary hover:text-primary/80"
```

## Border Radius Conventions

Bellog uses consistent border radius:

```typescript
// Standard cards, containers
className="rounded-3xl"

// Buttons, inputs, tags
className="rounded-full"

// Smaller elements
className="rounded-xl"

// Images with subtle rounding
className="rounded-2xl"
```

## Shadow Patterns

```typescript
// Default state
className="shadow-sm"

// Hover state
className="hover:shadow-md"

// Elevated elements
className="shadow-lg"

// Modal/dialog
className="shadow-2xl"

// Colored shadow (rare)
className="shadow-lg shadow-primary/20"
```

## Backdrop Blur

For glass-morphism effects:

```typescript
// Strong blur (modals, navbars)
className="backdrop-blur-xl"

// Medium blur (cards)
className="backdrop-blur-lg"

// Light blur (overlays)
className="backdrop-blur-sm"
```

## Theme Integration Checklist

When creating a new component:

- [ ] No hardcoded colors (no #hex, rgb, or specific Tailwind colors)
- [ ] Uses semantic CSS variables (background, foreground, primary, etc.)
- [ ] Opacity modifiers for subtle effects (/5, /10, /20, /50)
- [ ] Hover states defined
- [ ] Focus states for interactive elements
- [ ] Consistent border radius (rounded-3xl or rounded-full)
- [ ] Text hierarchy uses muted-foreground for secondary text
- [ ] Works in both light and dark modes (test by toggling)

## Common Mistakes

### Mistake 1: Using Generic Tailwind Colors

```typescript
// ❌ Wrong
className="bg-slate-100 text-slate-900"

// ✅ Correct
className="bg-background text-foreground"
```

### Mistake 2: Hardcoding Dark Mode

```typescript
// ❌ Wrong
className="bg-white dark:bg-gray-900"

// ✅ Correct
className="bg-background"
```

### Mistake 3: Mixing Color Systems

```typescript
// ❌ Wrong
className="bg-card text-gray-700"

// ✅ Correct
className="bg-card text-card-foreground"
```

### Mistake 4: Forgetting Opacity

```typescript
// ❌ Less flexible
className="bg-primary"

// ✅ More subtle
className="bg-primary/10"
```

## Quick Reference

```typescript
// Page background
bg-background

// Card background
bg-card

// Primary action
bg-primary text-primary-foreground

// Text colors
text-foreground              // Primary text
text-muted-foreground        // Secondary text
text-primary                 // Accent text

// Borders
border-border                // Standard
border-border/50             // Subtle

// Hover patterns
hover:bg-primary/10          // Background highlight
hover:text-primary           // Text accent
hover:border-primary/20      // Border accent

// Focus
focus-visible:ring-2 focus-visible:ring-primary

// Complete card
bg-card border border-border/50 text-card-foreground rounded-3xl
```

Remember: Always use CSS variables through Tailwind classes. The theme system will handle light/dark mode automatically.
