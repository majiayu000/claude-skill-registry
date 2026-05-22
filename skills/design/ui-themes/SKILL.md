---
name: ui-themes
description: Theme generation with tweakcn for shadcn/ui and Magic UI animations. Use when setting up project themes, customizing color schemes, adding dark mode, or integrating animated components.
---

# UI Themes

Generate and customize shadcn/ui themes using **tweakcn** and enhance with **Magic UI** animated components. This skill covers theme selection, dark mode setup, and animation integration.

## When to Use This Skill

- Setting up a new project's visual theme
- Customizing shadcn/ui color schemes
- Adding dark mode support
- Integrating animated UI components
- Choosing a design direction for a project

---

# Part 1: Theme Generation with tweakcn

[tweakcn](https://tweakcn.com) is a visual theme editor for shadcn/ui that exports production-ready CSS variables.

## Workflow

1. Visit [tweakcn.com/editor/theme](https://tweakcn.com/editor/theme)
2. Select a preset that matches your design direction
3. Customize colors, typography, and radius if needed
4. Export CSS variables to your project
5. Update `globals.css` with the exported theme

## Preset Selection Guide

Choose a preset based on your product's personality:

| Design Direction | Recommended Presets | When to Use |
|-----------------|---------------------|-------------|
| **Precision & Density** | graphite, mono, darkmatter | Dev tools, power user apps, terminals |
| **Sophistication & Trust** | vercel, cosmic night, claude | Finance, enterprise, B2B |
| **Warmth & Approachability** | modern minimal, notebook, soft pop | Collaboration tools, note apps |
| **Boldness & Clarity** | neo brutalism, bold tech, clean slate | Marketing sites, modern dashboards |
| **Dark Professional** | graphite, darkmatter, cosmic night | Any dark-first application |
| **Light Professional** | modern minimal, clean slate, vercel | Light-first applications |

## Export Options

tweakcn supports multiple export formats:

- **OKLCH** (recommended) - Best color accuracy across displays
- **HSL** - Traditional CSS format, widest compatibility
- **RGB/Hex** - Direct color values

## Integration Steps

### 1. Replace globals.css Theme

Replace the `:root` and `.dark` sections in `globals.css` with tweakcn export:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* tweakcn exported variables go here */
    --background: 0 0% 100%;
    --foreground: 224 71% 4%;
    /* ... rest of light theme */
  }

  .dark {
    /* tweakcn exported dark variables */
    --background: 224 71% 4%;
    --foreground: 210 20% 98%;
    /* ... rest of dark theme */
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

### 2. Set Default Theme

For dark mode default, add `className="dark"` to the html element:

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  )
}
```

### 3. Sidebar Colors (Optional)

If using a sidebar layout, tweakcn includes sidebar-specific variables:

```css
--sidebar-background: ...;
--sidebar-foreground: ...;
--sidebar-primary: ...;
--sidebar-primary-foreground: ...;
--sidebar-accent: ...;
--sidebar-accent-foreground: ...;
--sidebar-border: ...;
--sidebar-ring: ...;
```

---

# Part 2: Magic UI Components

[Magic UI](https://magicui.design) provides 150+ animated React components that integrate with shadcn/ui.

## Installation

Magic UI uses the shadcn CLI for installation:

```bash
# Install individual components
pnpm dlx shadcn@latest add @magicui/component-name

# Examples
pnpm dlx shadcn@latest add @magicui/magic-card
pnpm dlx shadcn@latest add @magicui/shimmer-button
```

Components install to `components/ui/` alongside existing shadcn components.

## Essential Components for Themes

### Animated Theme Toggler

Smooth dark/light mode toggle with animation:

```bash
pnpm dlx shadcn@latest add @magicui/animated-theme-toggler
```

```tsx
import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler"

<AnimatedThemeToggler />
```

### Magic Card

Hover effects with gradient tracking - perfect for cards and grid items:

```bash
pnpm dlx shadcn@latest add @magicui/magic-card
```

```tsx
import { MagicCard } from "@/components/ui/magic-card"

<MagicCard className="p-6">
  <h3>Card Title</h3>
  <p>Card content with gradient hover effect</p>
</MagicCard>
```

### Shimmer Button

Premium CTA buttons with shimmer loading state:

```bash
pnpm dlx shadcn@latest add @magicui/shimmer-button
```

```tsx
import { ShimmerButton } from "@/components/ui/shimmer-button"

<ShimmerButton>Get Started</ShimmerButton>
```

### Blur Fade

Smooth entrance animations for content:

```bash
pnpm dlx shadcn@latest add @magicui/blur-fade
```

```tsx
import { BlurFade } from "@/components/ui/blur-fade"

<BlurFade delay={0.1}>
  <div>Content fades in with blur effect</div>
</BlurFade>
```

### Typing Animation

AI-like text reveal for generated content:

```bash
pnpm dlx shadcn@latest add @magicui/typing-animation
```

```tsx
import { TypingAnimation } from "@/components/ui/typing-animation"

<TypingAnimation text="AI-generated content appears here..." />
```

### Border Beam

Subtle animated border glow:

```bash
pnpm dlx shadcn@latest add @magicui/border-beam
```

```tsx
import { BorderBeam } from "@/components/ui/border-beam"

<div className="relative">
  <BorderBeam />
  <div>Content with glowing border</div>
</div>
```

## Component Categories

| Category | Components | Use Case |
|----------|------------|----------|
| **Effects** | Magic Card, Border Beam, Shine Border | Cards, containers |
| **Buttons** | Shimmer Button, Rainbow Button, Pulsating Button | CTAs, actions |
| **Animations** | Blur Fade, Typing Animation, Text Animate | Content reveal |
| **Backgrounds** | Dot Pattern, Grid Pattern, Particles | Hero sections |
| **Navigation** | Dock, Smooth Cursor | App navigation |
| **Theme** | Animated Theme Toggler | Dark/light mode |

---

# Part 3: Dark Mode Setup

## Next.js App Router

### Option 1: Static Dark Mode (Default)

Set dark mode as the default without toggle:

```tsx
// app/layout.tsx
<html lang="en" className="dark">
```

### Option 2: Theme Provider (Toggle)

For user-controlled theme switching, use `next-themes`:

```bash
pnpm add next-themes
```

```tsx
// components/theme-provider.tsx
"use client"

import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="dark"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  )
}
```

```tsx
// app/layout.tsx
import { ThemeProvider } from "@/components/theme-provider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

### Theme Toggle Component

Combine with Magic UI's Animated Theme Toggler:

```tsx
"use client"

import { useTheme } from "next-themes"
import { AnimatedThemeToggler } from "@/components/ui/animated-theme-toggler"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  
  return (
    <AnimatedThemeToggler
      checked={theme === "dark"}
      onCheckedChange={(checked) => setTheme(checked ? "dark" : "light")}
    />
  )
}
```

---

# Part 4: Quick Setup Recipes

## Recipe: Dark Professional Theme

Best for: Dev tools, dashboards, professional apps

```bash
# 1. Get theme from tweakcn (use "graphite" preset)
# 2. Install components
pnpm dlx shadcn@latest add @magicui/magic-card
pnpm dlx shadcn@latest add @magicui/shimmer-button
pnpm dlx shadcn@latest add @magicui/blur-fade
```

Set dark default:
```tsx
<html lang="en" className="dark">
```

## Recipe: Light with Dark Mode Toggle

Best for: Content apps, documentation, general purpose

```bash
# 1. Get theme from tweakcn (use "modern minimal" preset)
# 2. Install dependencies
pnpm add next-themes
pnpm dlx shadcn@latest add @magicui/animated-theme-toggler
```

Use ThemeProvider with default light.

## Recipe: AI Product Theme

Best for: AI tools, chat apps, generative products

```bash
# 1. Get theme from tweakcn (use "claude" or "cosmic night" preset)
# 2. Install components
pnpm dlx shadcn@latest add @magicui/typing-animation
pnpm dlx shadcn@latest add @magicui/magic-card
pnpm dlx shadcn@latest add @magicui/blur-fade
pnpm dlx shadcn@latest add @magicui/shimmer-button
```

Use typing animation for AI-generated content.

---

# Part 5: Best Practices

## Do

- Pick a preset that matches your product's personality
- Commit to dark OR light as primary (with optional toggle)
- Use OKLCH color format for best accuracy
- Keep animations subtle (150-250ms)
- Use Magic Card sparingly (1-2 per view)

## Don't

- Mix multiple accent colors
- Use heavy animations on every element
- Override shadcn component styles directly
- Skip the theme provider if you need toggle
- Use spring/bouncy animations in professional apps

## Performance

- Magic UI components are tree-shakable
- Only install components you actually use
- Blur Fade adds minimal overhead
- Typing Animation should be used sparingly

---

# Reference Links

- [tweakcn Theme Editor](https://tweakcn.com/editor/theme)
- [tweakcn Presets](https://tweakcn.com/#examples)
- [Magic UI Components](https://magicui.design/docs/components)
- [Magic UI Installation](https://magicui.design/docs/installation)
- [shadcn/ui Theming](https://ui.shadcn.com/docs/theming)
- [next-themes](https://github.com/pacocoursey/next-themes)
