---
name: tailwind-design-system
description: Skill for creating and managing a Design System using Tailwind CSS and shadcn/ui. Use when defining design tokens, setting up theming with CSS variables, building a consistent UI component library, initializing a design system configuration, or wrapping shadcn/ui components into design system primitives.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Tailwind CSS & shadcn/ui Design System

## Overview

Expert guide for creating and managing a centralized Design System using Tailwind CSS (v4.1+) and shadcn/ui. This skill provides structured workflows for defining design tokens, configuring themes with CSS variables, and building a consistent UI component library based on shadcn/ui primitives.

**Relationship with other skills:**
- **tailwind-css-patterns** covers utility-first styling, responsive design, and general Tailwind CSS usage
- **shadcn-ui** covers individual component installation, configuration, and implementation
- **This skill** focuses on the **system-level** orchestration: design tokens, theming infrastructure, component wrapping patterns, and ensuring consistency across the entire application

## When to Use

- Setting up a new design system from scratch with Tailwind CSS and shadcn/ui
- Defining design tokens (colors, typography, spacing, radius, shadows) as CSS variables
- Configuring `globals.css` with a centralized theming system (light/dark mode)
- Wrapping shadcn/ui components into design system primitives with enforced constraints
- Building a token-driven component library for consistent UI
- Migrating from a JavaScript-based Tailwind config to CSS-first configuration (v4.1+)
- Establishing color palettes with oklch format for perceptual uniformity
- Creating multi-theme support beyond light/dark (e.g., brand themes)

## Instructions

### Step 1: Initialize Design System Configuration

Run these commands to set up the project:

```bash
# Check if Tailwind is installed
npx tailwindcss --version

# For Tailwind v4 (recommended)
npx @tailwindcss/vite@latest init   # or: npm install -D tailwindcss @tailwindcss/vite

# Initialize shadcn/ui CLI
npx shadcn@latest init

# Install core shadcn/ui components
npx shadcn@latest add button card input -y
```

**Validation checkpoint**: After setup, verify with:
```bash
ls src/components/ui/        # Should list installed components
cat src/app/globals.css       # Should contain @tailwind directives
```

### Step 2: Define Design Tokens

Create `src/app/globals.css` with your design tokens:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Brand Colors */
    --primary: oklch(0.55 0.18 250);
    --primary-foreground: oklch(0.985 0 0);

    /* Semantic Colors */
    --background: oklch(0.99 0 0);
    --foreground: oklch(0.15 0 0);
    --secondary: oklch(0.96 0.01 250);
    --secondary-foreground: oklch(0.20 0 0);

    /* Validation: all colors must have foreground pair */
    --destructive: oklch(0.55 0.22 25);
    --destructive-foreground: oklch(0.985 0 0);
  }

  .dark {
    --primary: oklch(0.65 0.20 250);
    --background: oklch(0.14 0 0);
    --foreground: oklch(0.97 0 0);
    --secondary: oklch(0.25 0.02 250);
  }
}
```

**Validation checkpoint**: Verify tokens are valid CSS:
```bash
grep -E "^[[:space:]]*--[a-z-]+:" src/app/globals.css | wc -l
# Should return count of defined tokens (e.g., 10+)
```

### Step 3: Configure Theming Infrastructure

Bridge CSS variables to Tailwind utilities (Tailwind v4.1+):

```css
@theme inline {
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-background: var(--background);
  --color-foreground: var(--foreground);
}
```

Add dark mode class toggle in `components/providers/theme-provider.tsx`:
```tsx
import { useEffect } from "react";
export function ThemeProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.classList.toggle("dark", isDark);
  }, []);
  return <>{children}</>;
}
```

**Validation checkpoint**: Test dark mode:
```bash
document.documentElement.classList.contains("dark") // in browser console
```

### Step 4: Wrap shadcn/ui Components

Create `src/components/ds/Button.tsx`:
```tsx
import { Button as ShadcnButton } from "@/components/ui/button";

type DSVariant = "primary" | "secondary" | "destructive" | "ghost";
const variantMap: Record<DSVariant, "default" | "secondary" | "destructive" | "ghost"> = {
  primary: "default", secondary: "secondary",
  destructive: "destructive", ghost: "ghost",
};

export function Button({ variant = "primary", ...props }: { variant?: DSVariant } & React.ComponentProps<typeof ShadcnButton>) {
  return <ShadcnButton variant={variantMap[variant]} {...props} />;
}
```

**Validation checkpoint**: Verify build passes:
```bash
npx tsc --noEmit src/components/ds/Button.tsx
```

### Step 5: Validate and Document

Run the token validation script:
```bash
REQUIRED=("primary" "primary-foreground" "background" "foreground" "secondary" "secondary-foreground")
for token in "${REQUIRED[@]}"; do
  grep -q "$token:" src/app/globals.css || echo "MISSING: --$token"
done
```

**Validation checkpoint**: Ensure all shadcn components use DS tokens:
```bash
grep -r "bg-primary\|text-primary\|bg-background" src/components/ds/
```

## Examples

### Adding Custom Tokens

Extend the base tokens in `globals.css`:

```css
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}

.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}

@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

Usage: `<div className="bg-warning text-warning-foreground">Warning</div>`

### Wrapping shadcn/ui Components as Design System Primitives

See `references/component-wrapping.md` for complete examples including Button, Text, and Stack primitives with full TypeScript types.

Create constrained design system components that enforce token usage.
Inline example:

```tsx
import { Button as ShadcnButton } from "@/components/ui/button";

export function Button({ variant = "primary", size = "md", ...props }) {
  const variantMap = { primary: "default", secondary: "secondary" };
  const sizeMap = { sm: "sm", md: "default", lg: "lg" };
  return (
    <ShadcnButton
      variant={variantMap[variant]}
      size={sizeMap[size]}
      {...props}
    />
  );
}
```

### Multi-Theme Support

For applications requiring multiple brand themes beyond light/dark:

```css
[data-theme="ocean"] {
  --primary: oklch(0.55 0.18 230);
  --primary-foreground: oklch(0.985 0 0);
}

[data-theme="forest"] {
  --primary: oklch(0.50 0.15 145);
  --primary-foreground: oklch(0.985 0 0);
}
```

```tsx
const [theme, setTheme] = useState("light");
useEffect(() => {
  document.documentElement.setAttribute("data-theme", theme);
}, [theme]);
```

### Design Token Validation

Verify all required tokens are defined:

```bash
#!/bin/bash
REQUIRED=("--background" "--foreground" "--primary" "--primary-foreground")
for token in "${REQUIRED[@]}"; do
  grep -q "$token:" src/styles/globals.css || echo "Missing: $token"
done
```

## Constraints and Warnings

- **oklch color format**: Use oklch for perceptual uniformity. Not all browsers support oklch natively; check compatibility if targeting older browsers
- **Token naming**: Follow the shadcn/ui convention (`--primary`, `--primary-foreground`) for seamless integration
- **`@`theme inline vs `@`theme**: Use `@theme inline` when bridging CSS variables to Tailwind utilities; use `@theme` for direct token definition
- **Component wrapping**: Keep wrapper components thin. Only add constraints that enforce design system rules; avoid duplicating shadcn/ui logic
- **Dark mode**: Always define dark mode values for every token in `:root`. Missing dark tokens cause visual regressions
- **CSS variable scoping**: Tokens defined in `:root` are global. Use `[data-theme]` selectors for multi-theme without conflicts
- **Performance**: Avoid excessive CSS custom property chains. Each `var()` lookup adds minimal but non-zero overhead
- **Tailwind v4 vs v3**: The `@theme` directive and `@theme inline` are v4.1+ features. For v3 projects, use `tailwind.config.js` with `theme.extend`

## Best Practices

1. **Single source of truth**: All design tokens live in `globals.css`. Never hardcode color values in components
2. **Semantic naming**: Use purpose-based names (`--primary`, `--destructive`) not appearance-based (`--blue-500`, `--red-600`)
3. **Foreground pairing**: Every background token must have a matching `-foreground` token for contrast compliance
4. **Token scale**: Define a complete scale for custom palettes (50-950) to provide flexibility
5. **Component barrel exports**: Export all DS components from a single `index.ts` for clean imports
6. **Accessibility**: Ensure all token pairs (background/foreground) meet WCAG AA contrast (4.5:1 for text, 3:1 for large text)
7. **Document tokens**: Maintain a visual reference of all tokens for the team
8. **Consistent spacing**: Use Tailwind's spacing scale (`gap-2`, `gap-4`, `gap-6`) through DS components rather than arbitrary values

## References

- Tailwind CSS v4 Theme Configuration: https://tailwindcss.com/docs/theme
- Tailwind CSS Functions and Directives: https://tailwindcss.com/docs/functions-and-directives
- shadcn/ui Theming Guide: https://ui.shadcn.com/docs/theming
- shadcn/ui Installation (Manual): https://ui.shadcn.com/docs/installation/manual
- oklch Color Space: https://oklch.com
