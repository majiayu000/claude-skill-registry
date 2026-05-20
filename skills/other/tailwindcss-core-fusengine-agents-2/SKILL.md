---
name: tailwindcss-core
description: "Configuration and directives Tailwind CSS v4.1. @theme, @import, @source, @utility, @variant, @apply, @config. CSS-first mode without tailwind.config.js."
user-invocable: false
---

# Tailwind CSS Core v4.1

## Overview

Tailwind CSS v4.1 introduces a **CSS-first** approach that eliminates the need for a traditional `tailwind.config.js` file. All configuration is now done directly in your CSS files via specialized directives.

## Key Concepts

### 1. @import "tailwindcss"

Entry point to load Tailwind CSS. Place at the beginning of your main CSS file.

```css
@import "tailwindcss";
```

This directive automatically loads:
- Base utilities
- Responsive variants
- Layers (theme, base, components, utilities)

### 2. @theme

Directive to define or customize theme values via CSS custom properties.

```css
@theme {
  --color-primary: #3b82f6;
  --color-secondary: #ef4444;
  --spacing-custom: 2.5rem;
  --radius-lg: 1rem;
}
```

Variables are accessible in generated utilities:
- `--color-*` → classes `bg-primary`, `text-primary`, etc.
- `--spacing-*` → classes `p-custom`, `m-custom`, etc.
- `--radius-*` → classes `rounded-lg`, etc.

### 3. @source

Directive to include additional source files with glob patterns.

```css
@source "./routes/**/*.{ts,tsx}";
@source "./components/**/*.{tsx,jsx}";
@source "../packages/ui/src/**/*.{ts,tsx}";
```

Tailwind will scan these files to generate utilities used in your project.

### 4. @utility and @variant

Directives to create custom utilities and variants.

```css
@utility truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@variant group-hover {
  .group:hover &
}
```

### 5. @apply

Directive to apply Tailwind classes in your custom CSS rules.

```css
.btn {
  @apply px-4 py-2 rounded-lg font-semibold;
}

.btn-primary {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}
```

### 6. @config

Directive to load external configuration if needed.

```css
@config "./tailwind.config.js";
```

(Optional in v4.1, mainly used for backward compatibility)

## Dark Mode

Dark mode configuration in Tailwind v4.1:

```css
@import "tailwindcss";

/* Use system preference */
@variant dark (&:is(.dark *));
```

Or via manual class:

```css
@variant dark (&.dark);
```

## Responsive Breakpoints

Breakpoints are defined via `@theme`:

```css
@theme {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}
```

Responsive variants are used with utilities:

```html
<div class="text-sm md:text-base lg:text-lg"></div>
```

## Layer Hierarchy

```css
@layer theme, base, components, utilities;

@import "tailwindcss";

/* Your customizations */
@layer components {
  .btn { @apply px-4 py-2 rounded; }
}

@layer utilities {
  .text-shadow { text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
}
```

## Plugin Integration

Load Tailwind plugins:

```css
@import "tailwindcss";
@plugin "flowbite/plugin";
@source "../node_modules/flowbite";
```

## Specificity Order

In CSS-first, import and declaration order determines specificity:

1. `@import "tailwindcss"` - Base utilities
2. `@theme { ... }` - Theme variables
3. `@layer components { ... }` - Custom components
4. `@layer utilities { ... }` - Custom utilities

## CSS-first Mode Benefits

- No complex JavaScript config file
- Type-safe via CSS variables
- Declarative and readable configuration
- Better integration with CSS preprocessors
- Simplified maintenance for large projects

## Detailed References

See specific files for:
- `theme.md` - Complete theme variable configuration
- `directives.md` - Syntax and examples of all directives
- `config.md` - Advanced configuration and use cases
