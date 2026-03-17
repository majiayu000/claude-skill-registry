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

1. **Assess the project**: Check if Tailwind CSS and shadcn/ui are already installed
2. **Create the globals.css**: Set up the central CSS file with design tokens
3. **Configure Tailwind**: Use the `@theme` directive (v4.1+) or `tailwind.config.js` (v3)
4. **Install shadcn/ui**: Initialize with the CLI and configure the theme

### Step 2: Define Design Tokens

Design tokens are the foundation. Define them as CSS custom properties in `globals.css`:

- **Colors**: Brand palette, semantic colors, surface colors
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Consistent spacing scale
- **Borders**: Radius, widths
- **Shadows**: Elevation levels
- **Animations**: Transition durations and easing functions

### Step 3: Configure Theming Infrastructure

Set up light/dark mode support and expose tokens to Tailwind via `@theme inline`.

### Step 4: Wrap shadcn/ui Components

Create design system primitives that enforce token usage and provide consistent API.

### Step 5: Document and Validate

Create a living style guide and validate token usage across the codebase.

## Examples

### Complete globals.css with Design Tokens

See `references/globals.css.example` for a complete, production-ready `globals.css` with all design tokens configured.

Quick example for adding custom tokens:

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

Create constrained design system components that enforce token usage.
See `references/component-wrapping.md` for complete examples including Button, Text, and Stack primitives.

Quick example:

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
- **@theme inline vs @theme**: Use `@theme inline` when bridging CSS variables to Tailwind utilities; use `@theme` for direct token definition
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
