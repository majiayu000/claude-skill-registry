---
name: tailwindcss-advanced-design-systems
description: Tailwind CSS advanced design systems with design tokens and @theme configuration
---

# Tailwind CSS Advanced Design Systems

## Building Design Tokens with @theme

### Complete Design Token System

```css
@import "tailwindcss";

@theme {
  /* ===== COLOR SYSTEM ===== */

  /* Disable all defaults for full control */
  --color-*: initial;

  /* Semantic color tokens */
  --color-surface-primary: oklch(1 0 0);
  --color-surface-secondary: oklch(0.98 0.002 250);
  --color-surface-tertiary: oklch(0.95 0.004 250);
  --color-surface-inverse: oklch(0.15 0.02 250);

  --color-text-primary: oklch(0.15 0.02 250);
  --color-text-secondary: oklch(0.4 0.02 250);
  --color-text-tertiary: oklch(0.55 0.015 250);
  --color-text-inverse: oklch(0.98 0 0);
  --color-text-disabled: oklch(0.7 0.01 250);

  --color-border-default: oklch(0.85 0.01 250);
  --color-border-subtle: oklch(0.92 0.005 250);
  --color-border-strong: oklch(0.7 0.02 250);

  /* Brand colors with full scale */
  --color-brand-50: oklch(0.97 0.02 250);
  --color-brand-100: oklch(0.93 0.04 250);
  --color-brand-200: oklch(0.87 0.08 250);
  --color-brand-300: oklch(0.78 0.12 250);
  --color-brand-400: oklch(0.68 0.16 250);
  --color-brand-500: oklch(0.58 0.2 250);
  --color-brand-600: oklch(0.5 0.2 250);
  --color-brand-700: oklch(0.42 0.18 250);
  --color-brand-800: oklch(0.35 0.15 250);
  --color-brand-900: oklch(0.28 0.12 250);
  --color-brand-950: oklch(0.2 0.08 250);

  /* Status colors */
  --color-success: oklch(0.6 0.18 145);
  --color-success-subtle: oklch(0.95 0.04 145);
  --color-warning: oklch(0.75 0.18 85);
  --color-warning-subtle: oklch(0.95 0.06 85);
  --color-error: oklch(0.55 0.22 25);
  --color-error-subtle: oklch(0.95 0.04 25);
  --color-info: oklch(0.6 0.18 250);
  --color-info-subtle: oklch(0.95 0.04 250);

  /* ===== TYPOGRAPHY SYSTEM ===== */

  --font-*: initial;

  --font-display: "Cal Sans", "Inter", system-ui, sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;

  /* Type scale (Major Third - 1.25) */
  --text-xs: 0.64rem;
  --text-sm: 0.8rem;
  --text-base: 1rem;
  --text-lg: 1.25rem;
  --text-xl: 1.563rem;
  --text-2xl: 1.953rem;
  --text-3xl: 2.441rem;
  --text-4xl: 3.052rem;
  --text-5xl: 3.815rem;

  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.15;
  --leading-snug: 1.3;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* Letter spacing */
  --tracking-tighter: -0.05em;
  --tracking-tight: -0.025em;
  --tracking-normal: 0;
  --tracking-wide: 0.025em;
  --tracking-wider: 0.05em;
  --tracking-widest: 0.1em;

  /* ===== SPACING SYSTEM ===== */

  --spacing-*: initial;

  /* 4px base unit */
  --spacing-0: 0;
  --spacing-px: 1px;
  --spacing-0_5: 0.125rem;
  --spacing-1: 0.25rem;
  --spacing-1_5: 0.375rem;
  --spacing-2: 0.5rem;
  --spacing-2_5: 0.625rem;
  --spacing-3: 0.75rem;
  --spacing-3_5: 0.875rem;
  --spacing-4: 1rem;
  --spacing-5: 1.25rem;
  --spacing-6: 1.5rem;
  --spacing-7: 1.75rem;
  --spacing-8: 2rem;
  --spacing-9: 2.25rem;
  --spacing-10: 2.5rem;
  --spacing-11: 2.75rem;
  --spacing-12: 3rem;
  --spacing-14: 3.5rem;
  --spacing-16: 4rem;
  --spacing-20: 5rem;
  --spacing-24: 6rem;
  --spacing-28: 7rem;
  --spacing-32: 8rem;
  --spacing-36: 9rem;
  --spacing-40: 10rem;
  --spacing-44: 11rem;
  --spacing-48: 12rem;
  --spacing-52: 13rem;
  --spacing-56: 14rem;
  --spacing-60: 15rem;
  --spacing-64: 16rem;
  --spacing-72: 18rem;
  --spacing-80: 20rem;
  --spacing-96: 24rem;

  /* ===== EFFECTS ===== */

  --shadow-*: initial;

  --shadow-xs: 0 1px 2px 0 oklch(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 oklch(0 0 0 / 0.1), 0 1px 2px -1px oklch(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px oklch(0 0 0 / 0.1), 0 2px 4px -2px oklch(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px oklch(0 0 0 / 0.1), 0 4px 6px -4px oklch(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px oklch(0 0 0 / 0.1), 0 8px 10px -6px oklch(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px oklch(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 oklch(0 0 0 / 0.05);

  /* Colored shadows */
  --shadow-brand: 0 4px 14px 0 oklch(0.58 0.2 250 / 0.3);
  --shadow-success: 0 4px 14px 0 oklch(0.6 0.18 145 / 0.3);
  --shadow-error: 0 4px 14px 0 oklch(0.55 0.22 25 / 0.3);

  --radius-*: initial;

  --radius-none: 0;
  --radius-sm: 0.125rem;
  --radius-default: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-3xl: 1.5rem;
  --radius-full: 9999px;

  /* ===== MOTION ===== */

  --ease-*: initial;
  --animate-*: initial;

  --ease-linear: linear;
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

  --duration-75: 75ms;
  --duration-100: 100ms;
  --duration-150: 150ms;
  --duration-200: 200ms;
  --duration-300: 300ms;
  --duration-500: 500ms;
  --duration-700: 700ms;
  --duration-1000: 1000ms;

  /* ===== BREAKPOINTS ===== */

  --breakpoint-*: initial;

  --breakpoint-xs: 475px;
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
  --breakpoint-3xl: 1920px;

  /* ===== Z-INDEX ===== */

  --z-auto: auto;
  --z-0: 0;
  --z-10: 10;
  --z-20: 20;
  --z-30: 30;
  --z-40: 40;
  --z-50: 50;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
}
```

## Dark Mode Design Tokens

### Automatic Dark Mode with CSS Variables

```css
@import "tailwindcss";

@theme {
  /* Light mode tokens (default) */
  --color-surface: oklch(1 0 0);
  --color-surface-raised: oklch(0.98 0 0);
  --color-text: oklch(0.15 0 0);
  --color-text-muted: oklch(0.45 0 0);
  --color-border: oklch(0.9 0 0);
}

/* Dark mode overrides using native CSS */
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: oklch(0.12 0.02 260);
    --color-surface-raised: oklch(0.18 0.02 260);
    --color-text: oklch(0.95 0 0);
    --color-text-muted: oklch(0.65 0 0);
    --color-border: oklch(0.28 0.02 260);
  }
}

/* Selector-based dark mode */
@custom-variant dark (&:where(.dark, .dark *));

.dark {
  --color-surface: oklch(0.12 0.02 260);
  --color-surface-raised: oklch(0.18 0.02 260);
  --color-text: oklch(0.95 0 0);
  --color-text-muted: oklch(0.65 0 0);
  --color-border: oklch(0.28 0.02 260);
}
```

### Usage

```html
<!-- These classes work in both light and dark automatically -->
<div class="bg-[var(--color-surface)] text-[var(--color-text)]">
  <p class="text-[var(--color-text-muted)]">Muted text</p>
  <div class="border border-[var(--color-border)]">Bordered</div>
</div>

<!-- Or create semantic utility classes -->
```

```css
@utility bg-surface {
  background-color: var(--color-surface);
}

@utility bg-surface-raised {
  background-color: var(--color-surface-raised);
}

@utility text-default {
  color: var(--color-text);
}

@utility text-muted {
  color: var(--color-text-muted);
}

@utility border-default {
  border-color: var(--color-border);
}
```

## Multi-Theme Systems

### Theme Switching with Data Attributes

```css
@import "tailwindcss";

@custom-variant theme-ocean (&:where([data-theme="ocean"], [data-theme="ocean"] *));
@custom-variant theme-forest (&:where([data-theme="forest"], [data-theme="forest"] *));
@custom-variant theme-sunset (&:where([data-theme="sunset"], [data-theme="sunset"] *));

@theme {
  /* Default theme */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.7 0.15 200);
  --color-accent: oklch(0.75 0.18 30);
}

[data-theme="ocean"] {
  --color-primary: oklch(0.55 0.2 220);
  --color-secondary: oklch(0.65 0.15 200);
  --color-accent: oklch(0.7 0.18 180);
}

[data-theme="forest"] {
  --color-primary: oklch(0.5 0.18 145);
  --color-secondary: oklch(0.6 0.12 120);
  --color-accent: oklch(0.75 0.15 85);
}

[data-theme="sunset"] {
  --color-primary: oklch(0.6 0.22 25);
  --color-secondary: oklch(0.7 0.2 45);
  --color-accent: oklch(0.8 0.18 65);
}
```

```html
<html data-theme="ocean">
  <body>
    <button class="bg-primary theme-forest:bg-primary">
      Uses ocean primary, unless explicitly overridden
    </button>
  </body>
</html>
```

### JavaScript Theme Switcher

```javascript
const themes = ['default', 'ocean', 'forest', 'sunset'];

function setTheme(theme) {
  if (theme === 'default') {
    document.documentElement.removeAttribute('data-theme');
  } else {
    document.documentElement.setAttribute('data-theme', theme);
  }
  localStorage.setItem('theme', theme);
}

function initTheme() {
  const saved = localStorage.getItem('theme') || 'default';
  setTheme(saved);
}

// Theme picker component
function ThemePicker() {
  return `
    <select onchange="setTheme(this.value)">
      ${themes.map(t => `<option value="${t}">${t}</option>`).join('')}
    </select>
  `;
}

initTheme();
```

## Component Token System

### Design Tokens for Components

```css
@theme {
  /* Button tokens */
  --button-padding-x: var(--spacing-4);
  --button-padding-y: var(--spacing-2);
  --button-radius: var(--radius-lg);
  --button-font-weight: 500;
  --button-transition: all 150ms ease;

  /* Input tokens */
  --input-padding-x: var(--spacing-3);
  --input-padding-y: var(--spacing-2);
  --input-radius: var(--radius-md);
  --input-border-width: 1px;
  --input-focus-ring-width: 2px;
  --input-focus-ring-offset: 2px;

  /* Card tokens */
  --card-padding: var(--spacing-6);
  --card-radius: var(--radius-xl);
  --card-shadow: var(--shadow-md);
  --card-border-width: 1px;

  /* Modal tokens */
  --modal-padding: var(--spacing-6);
  --modal-radius: var(--radius-2xl);
  --modal-max-width: 32rem;
  --modal-backdrop-opacity: 0.5;
}
```

```css
@layer components {
  .btn {
    padding: var(--button-padding-y) var(--button-padding-x);
    border-radius: var(--button-radius);
    font-weight: var(--button-font-weight);
    transition: var(--button-transition);
  }

  .input {
    padding: var(--input-padding-y) var(--input-padding-x);
    border-radius: var(--input-radius);
    border-width: var(--input-border-width);
  }

  .input:focus {
    outline: none;
    ring-width: var(--input-focus-ring-width);
    ring-offset: var(--input-focus-ring-offset);
  }

  .card {
    padding: var(--card-padding);
    border-radius: var(--card-radius);
    box-shadow: var(--card-shadow);
    border-width: var(--card-border-width);
  }
}
```

## Responsive Design Tokens

### Fluid Typography

```css
@theme {
  /* Fluid type scale using clamp() */
  --text-fluid-xs: clamp(0.64rem, 0.5rem + 0.5vw, 0.75rem);
  --text-fluid-sm: clamp(0.8rem, 0.7rem + 0.5vw, 0.875rem);
  --text-fluid-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-fluid-lg: clamp(1.25rem, 1rem + 1vw, 1.5rem);
  --text-fluid-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2rem);
  --text-fluid-2xl: clamp(2rem, 1.5rem + 2vw, 3rem);
  --text-fluid-3xl: clamp(2.5rem, 1.8rem + 3vw, 4rem);
  --text-fluid-4xl: clamp(3rem, 2rem + 4vw, 5rem);
}

@utility text-fluid-xs { font-size: var(--text-fluid-xs); }
@utility text-fluid-sm { font-size: var(--text-fluid-sm); }
@utility text-fluid-base { font-size: var(--text-fluid-base); }
@utility text-fluid-lg { font-size: var(--text-fluid-lg); }
@utility text-fluid-xl { font-size: var(--text-fluid-xl); }
@utility text-fluid-2xl { font-size: var(--text-fluid-2xl); }
@utility text-fluid-3xl { font-size: var(--text-fluid-3xl); }
@utility text-fluid-4xl { font-size: var(--text-fluid-4xl); }
```

### Fluid Spacing

```css
@theme {
  /* Fluid spacing using clamp() */
  --space-fluid-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-fluid-sm: clamp(0.5rem, 0.4rem + 0.5vw, 1rem);
  --space-fluid-md: clamp(1rem, 0.8rem + 1vw, 2rem);
  --space-fluid-lg: clamp(2rem, 1.5rem + 2vw, 4rem);
  --space-fluid-xl: clamp(4rem, 3rem + 4vw, 8rem);
  --space-fluid-2xl: clamp(6rem, 4rem + 6vw, 12rem);
}

@utility p-fluid-xs { padding: var(--space-fluid-xs); }
@utility p-fluid-sm { padding: var(--space-fluid-sm); }
@utility p-fluid-md { padding: var(--space-fluid-md); }
@utility p-fluid-lg { padding: var(--space-fluid-lg); }
@utility p-fluid-xl { padding: var(--space-fluid-xl); }

@utility gap-fluid-xs { gap: var(--space-fluid-xs); }
@utility gap-fluid-sm { gap: var(--space-fluid-sm); }
@utility gap-fluid-md { gap: var(--space-fluid-md); }
@utility gap-fluid-lg { gap: var(--space-fluid-lg); }
```

## Brand Color Generation

### Generating Color Scales from Brand Color

```css
@theme {
  /* Start with your brand color */
  --brand-hue: 250;
  --brand-chroma: 0.2;

  /* Generate full scale */
  --color-brand-50: oklch(0.97 calc(var(--brand-chroma) * 0.1) var(--brand-hue));
  --color-brand-100: oklch(0.93 calc(var(--brand-chroma) * 0.2) var(--brand-hue));
  --color-brand-200: oklch(0.87 calc(var(--brand-chroma) * 0.4) var(--brand-hue));
  --color-brand-300: oklch(0.78 calc(var(--brand-chroma) * 0.6) var(--brand-hue));
  --color-brand-400: oklch(0.68 calc(var(--brand-chroma) * 0.8) var(--brand-hue));
  --color-brand-500: oklch(0.58 var(--brand-chroma) var(--brand-hue));
  --color-brand-600: oklch(0.5 var(--brand-chroma) var(--brand-hue));
  --color-brand-700: oklch(0.42 calc(var(--brand-chroma) * 0.9) var(--brand-hue));
  --color-brand-800: oklch(0.35 calc(var(--brand-chroma) * 0.75) var(--brand-hue));
  --color-brand-900: oklch(0.28 calc(var(--brand-chroma) * 0.6) var(--brand-hue));
  --color-brand-950: oklch(0.2 calc(var(--brand-chroma) * 0.4) var(--brand-hue));
}
```

## Monorepo Design System

### Shared Design Tokens Package

```
packages/
  design-tokens/
    tokens.css
    package.json
  ui-components/
    src/
    package.json
apps/
  web/
  mobile/
```

**packages/design-tokens/tokens.css:**
```css
/* Exportable design tokens */
@theme {
  /* All your design tokens here */
  --color-brand-500: oklch(0.58 0.2 250);
  /* ... */
}
```

**packages/design-tokens/package.json:**
```json
{
  "name": "@mycompany/design-tokens",
  "version": "1.0.0",
  "exports": {
    ".": "./tokens.css"
  }
}
```

**apps/web/app.css:**
```css
@import "tailwindcss";
@import "@mycompany/design-tokens";
```

## Best Practices

### 1. Use Semantic Naming

```css
/* Good - Semantic names */
--color-text-primary
--color-surface-elevated
--color-action-primary

/* Avoid - Raw values */
--color-gray-900
--color-white
--color-blue-500
```

### 2. Document Token Purpose

```css
@theme {
  /*
   * Surface colors for backgrounds
   * primary: Main page background
   * raised: Cards and elevated elements
   * sunken: Inset areas like inputs
   */
  --color-surface-primary: oklch(1 0 0);
  --color-surface-raised: oklch(0.98 0 0);
  --color-surface-sunken: oklch(0.96 0 0);
}
```

### 3. Create Token Aliases

```css
@theme {
  /* Base tokens */
  --color-blue-500: oklch(0.58 0.2 250);

  /* Semantic aliases */
  --color-primary: var(--color-blue-500);
  --color-link: var(--color-blue-500);
  --color-focus-ring: var(--color-blue-500);
}
```

### 4. Version Your Design System

Keep design tokens in version control and document changes:

```css
/*
 * Design System v2.0.0
 * Breaking changes:
 * - Renamed --color-gray-* to --color-neutral-*
 * - Updated primary color to new brand guidelines
 */
```
