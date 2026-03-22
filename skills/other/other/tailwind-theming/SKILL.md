---
name: tailwind-theming
description: |
  Tailwind CSS theming system for this Next.js application.
  Covers CSS variables, semantic tokens, dark mode, buildSectionClasses, and theme build process.
  Use this skill when implementing UI styling or working with theme configurations.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Tailwind Theming Skill

Patterns for working with the Tailwind CSS v4 theming system, CSS variables, and semantic tokens.

## Architecture Overview

```
TAILWIND THEMING (v4):

Source Files:
contents/themes/{THEME}/
├── styles/
│   ├── globals.css         # CSS variables (light + dark)
│   └── components.css      # Component-specific styles
├── config/
│   └── theme.config.ts     # Theme settings
└── public/
    └── theme-assets/       # Images, fonts

Generated Files (DO NOT EDIT):
├── core/theme-styles.css   # Compiled theme CSS
└── public/theme/           # Copied assets

Build Script:
└── core/scripts/build/theme.mjs
```

## When to Use This Skill

- Styling components with semantic tokens
- Understanding CSS variable system
- Implementing dark mode support
- Using buildSectionClasses in blocks
- Working with background color presets

## CSS Variables (Design Tokens)

### Core Semantic Colors

```css
/* Light Mode (:root) */
:root {
  /* Backgrounds */
  --background: oklch(1 0 0);              /* Page background */
  --card: oklch(1 0 0);                    /* Card surfaces */
  --popover: oklch(1 0 0);                 /* Dropdowns, popovers */

  /* Foregrounds (text) */
  --foreground: oklch(0.145 0 0);          /* Primary text */
  --card-foreground: oklch(0.145 0 0);     /* Card text */
  --popover-foreground: oklch(0.145 0 0);  /* Popover text */

  /* Interactive */
  --primary: oklch(0.205 0 0);             /* Primary buttons/links */
  --primary-foreground: oklch(0.985 0 0);  /* Text on primary */
  --secondary: oklch(0.97 0 0);            /* Secondary elements */
  --secondary-foreground: oklch(0.205 0 0);

  /* States */
  --muted: oklch(0.97 0 0);                /* Muted backgrounds */
  --muted-foreground: oklch(0.556 0 0);    /* Muted/placeholder text */
  --accent: oklch(0.97 0 0);               /* Accent highlights */
  --accent-foreground: oklch(0.205 0 0);

  /* Feedback */
  --destructive: oklch(0.577 0.245 27.325); /* Error/danger */
  --destructive-foreground: oklch(1 0 0);

  /* Borders & Inputs */
  --border: oklch(0.922 0 0);              /* Border color */
  --input: oklch(0.922 0 0);               /* Input borders */
  --ring: oklch(0.708 0 0);                /* Focus rings */

  /* Radius */
  --radius: 0.5rem;                        /* Base border radius */
}
```

### Dark Mode Variables

```css
/* Dark Mode (.dark selector) */
.dark {
  /* Inverted - dark backgrounds, light text */
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);

  --card: oklch(0.145 0 0);
  --card-foreground: oklch(0.985 0 0);

  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);

  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);

  --border: oklch(0.269 0 0);
  --input: oklch(0.269 0 0);

  /* Destructive stays similar but adjusted for dark */
  --destructive: oklch(0.396 0.141 25.723);
  --destructive-foreground: oklch(0.985 0 0);
}
```

### Sidebar Variables

```css
:root {
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}
```

### Chart Colors

```css
:root {
  --chart-1: oklch(0.81 0.1 252);
  --chart-2: oklch(0.62 0.19 260);
  --chart-3: oklch(0.55 0.22 263);
  --chart-4: oklch(0.49 0.22 264);
  --chart-5: oklch(0.42 0.18 266);
}
```

## Semantic Token Usage

### Correct Usage

```typescript
// ✅ ALWAYS use semantic tokens
<div className="bg-background text-foreground">
<div className="bg-card text-card-foreground">
<p className="text-muted-foreground">
<button className="bg-primary text-primary-foreground">
<span className="text-destructive">

// ✅ Borders and inputs
<div className="border border-border">
<input className="border-input focus:ring-ring">

// ✅ Radius
<div className="rounded-lg">  {/* Uses --radius */}
<div className="rounded-sm">  {/* calc(--radius - 4px) */}
```

### Forbidden Patterns

```typescript
// ❌ NEVER hardcode colors
<div className="bg-white text-black">
<div className="bg-gray-100">
<p className="text-gray-500">
<button className="bg-blue-500 text-white">

// ❌ NEVER use arbitrary color values
<div className="bg-[#ffffff]">
<p className="text-[rgb(107,114,128)]">
```

## Background Color Presets (Blocks)

### Available Values

```typescript
type BackgroundColor =
  | 'transparent'   // bg-transparent
  | 'white'         // bg-white
  | 'gray-50'       // bg-gray-50
  | 'gray-100'      // bg-gray-100
  | 'gray-900'      // bg-gray-900 text-white
  | 'primary'       // bg-primary text-primary-foreground
  | 'primary-light' // bg-primary/10
  | 'primary-dark'  // bg-primary-dark text-white
  | 'secondary'     // bg-secondary text-secondary-foreground
  | 'accent'        // bg-accent text-accent-foreground
```

### getBackgroundClasses Function

```typescript
// core/types/blocks.ts

export function getBackgroundClasses(backgroundColor?: BackgroundColor): string {
  const bgMap: Record<BackgroundColor, string> = {
    transparent: 'bg-transparent',
    white: 'bg-white',
    'gray-50': 'bg-gray-50',
    'gray-100': 'bg-gray-100',
    'gray-900': 'bg-gray-900 text-white',
    primary: 'bg-primary text-primary-foreground',
    'primary-light': 'bg-primary/10',
    'primary-dark': 'bg-primary-dark text-white',
    secondary: 'bg-secondary text-secondary-foreground',
    accent: 'bg-accent text-accent-foreground',
  }
  return bgMap[backgroundColor || 'transparent']
}
```

## buildSectionClasses Helper

### Function Signature

```typescript
// core/types/blocks.ts

export function buildSectionClasses(
  baseClasses: string,
  props: Partial<{
    backgroundColor?: BackgroundColor
    className?: string
  }>
): string
```

### Usage in Blocks

```typescript
import { buildSectionClasses } from '@/core/types/blocks'
import type { HeroProps } from './schema'

export function HeroBlock({
  title,
  content,
  backgroundColor,
  className,
  id,
}: HeroProps) {
  // Combine base classes + background + custom
  const sectionClasses = buildSectionClasses(
    'relative flex min-h-[600px] items-center justify-center px-4 py-20',
    { backgroundColor, className }
  )

  return (
    <section id={id} className={sectionClasses}>
      {/* ... */}
    </section>
  )
}
```

### Output Examples

```typescript
buildSectionClasses('py-16 px-4', {})
// "py-16 px-4"

buildSectionClasses('py-16 px-4', { backgroundColor: 'gray-900' })
// "py-16 px-4 bg-gray-900 text-white"

buildSectionClasses('py-16 px-4', {
  backgroundColor: 'primary',
  className: 'custom-class'
})
// "py-16 px-4 bg-primary text-primary-foreground custom-class"
```

## Dark Mode Implementation

### Architecture

```
1. CSS Variables → Define light/dark values in :root and .dark
2. @custom-variant → Tell Tailwind to use .dark class (NOT prefers-color-scheme)
3. next-themes  → Manages .dark class on <html>
4. Tailwind     → Reads CSS variables and applies dark: variants via class
```

### CRITICAL: Tailwind v4 Dark Mode Configuration

**By default, Tailwind v4 uses `@media (prefers-color-scheme: dark)` for `dark:` variants.**

This causes a mismatch with `next-themes` which uses the `.dark` class on `<html>`.

**Required in every theme's `globals.css`:**

```css
@import "tailwindcss";

/* REQUIRED: Use class selector instead of prefers-color-scheme */
@custom-variant dark (&:where(.dark, .dark *));

/* ... rest of imports */
```

**Without this configuration:**
- User sets theme to "light" in app
- OS has dark mode enabled
- Tailwind ignores the HTML class and uses OS preference
- `dark:bg-slate-800` applies even though app should be light

**With this configuration:**
- Tailwind respects the `.dark` class from next-themes
- App theme setting is honored regardless of OS preference

### Theme Provider Setup

```typescript
// core/providers/theme-provider.tsx
import { ThemeProvider as NextThemeProvider } from 'next-themes'

export function ThemeProvider({ children }) {
  return (
    <NextThemeProvider
      attribute="class"           // Adds .dark to <html>
      defaultTheme={defaultTheme} // light | dark | system
      enableSystem                // Respects OS preference
      disableTransitionOnChange   // No color flash
    >
      {children}
    </NextThemeProvider>
  )
}
```

### Theme Toggle

```typescript
import { useTheme } from 'next-themes'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()

  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      Toggle theme
    </button>
  )
}
```

### Default Theme Resolution

```typescript
// Priority order:
// 1. User preference (stored in DB: uiPreferences.theme)
// 2. Theme config default (theme.config.ts → defaultMode)
// 3. System preference
// 4. Fallback: 'light'
```

## Theme Build Process

### Build Commands

```bash
# Rebuild theme CSS
pnpm theme:build

# Or manually
node core/scripts/build/theme.mjs

# Watch mode (auto-rebuild)
node core/scripts/build/theme.mjs --watch
```

### What Build Does

1. **Reads** `NEXT_PUBLIC_ACTIVE_THEME` from `.env`
2. **Finds** `contents/themes/{theme}/styles/globals.css`
3. **Finds** `contents/themes/{theme}/styles/components.css`
4. **Copies** assets from `contents/themes/{theme}/public/` → `public/theme/`
5. **Copies** block thumbnails → `public/theme/blocks/{slug}/`
6. **Generates** `core/theme-styles.css`

### Generated File

```css
/*
 * Generated Theme CSS
 * Theme: default
 * Build time: 2025-12-30T12:00:00.000Z
 * DO NOT EDIT - Auto-generated by theme.mjs
 */

/* Contents of globals.css */
:root {
  --background: ...
}

/* Contents of components.css */
.custom-component {
  ...
}
```

## @theme Mapping (Tailwind v4)

```css
/* In globals.css - Maps CSS vars to Tailwind */
@theme inline {
  /* Colors */
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-card: var(--card);
  --color-primary: var(--primary);
  /* ... */

  /* Fonts */
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);

  /* Radius */
  --radius-sm: calc(var(--radius) - 4px);
  --radius-md: calc(var(--radius) - 2px);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) + 4px);

  /* Shadows */
  --shadow-sm: var(--shadow-sm);
  --shadow-md: var(--shadow-md);
}
```

## Theme File Structure

```
contents/themes/default/
├── config/
│   ├── theme.config.ts       # Theme metadata
│   ├── app.config.ts         # App settings
│   ├── permissions.config.ts # Role permissions
│   └── plans.config.ts       # Billing plans
├── styles/
│   ├── globals.css           # CSS variables (light + dark)
│   └── components.css        # Custom component styles
├── blocks/
│   └── {slug}/
│       └── thumbnail.png     # Block preview image
├── public/
│   └── theme-assets/         # Static assets
└── messages/
    ├── en.json               # English translations
    └── es.json               # Spanish translations
```

## Anti-Patterns

```typescript
// NEVER: Hardcode colors
<div className="bg-white text-gray-900">

// CORRECT: Use semantic tokens
<div className="bg-background text-foreground">

// NEVER: Use arbitrary colors
<div className="bg-[#1a1a1a]">

// CORRECT: Define in CSS variables if needed
<div className="bg-background">

// NEVER: Hardcode dark mode classes
<div className="bg-white dark:bg-gray-900">

// CORRECT: Use variables that auto-switch
<div className="bg-background">  {/* Switches automatically */}

// NEVER: Skip buildSectionClasses in blocks
<section className={`py-16 ${backgroundColor === 'gray-900' ? 'bg-gray-900 text-white' : ''}`}>

// CORRECT: Use helper function
<section className={buildSectionClasses('py-16', { backgroundColor })}>

// NEVER: Modify generated CSS files
// core/theme-styles.css - DO NOT EDIT

// CORRECT: Modify source files and rebuild
// contents/themes/default/styles/globals.css
```

## Checklist

Before finalizing theme implementation:

- [ ] Using semantic tokens (bg-background, not bg-white)
- [ ] No hardcoded colors
- [ ] Dark mode works automatically (variables switch)
- [ ] Blocks use buildSectionClasses helper
- [ ] Background color uses BackgroundColor type
- [ ] Theme rebuilt after CSS changes
- [ ] Assets copied to public/theme/
- [ ] No modifications to generated files

## Related Skills

- `shadcn-components` - Component styling patterns
- `page-builder-blocks` - Block styling with buildSectionClasses
- `accessibility` - Color contrast requirements
