---
name: tailwindcss
description: "Utility-first CSS framework for rapid UI development. Responsive design, custom utilities, configuration, component composition. Trigger: When styling with Tailwind CSS utility classes, creating responsive designs, or configuring Tailwind."
skills:
  - conventions
  - a11y
  - css
  - humanizer
dependencies:
  tailwindcss: ">=3.0.0 <5.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Tailwind CSS Skill

## Overview

Utility-first CSS framework for building custom designs with composable utility classes.

## Objective

Enable developers to build responsive, maintainable UIs using Tailwind's utility classes and configuration system.

---

## When to Use

Use this skill when:

- Styling components with utility-first CSS
- Creating responsive designs with Tailwind breakpoints
- Configuring Tailwind theme (colors, spacing, typography)
- Building custom utilities or plugins
- Using JIT mode for performance

Don't use this skill for:

- Material-UI styling (use mui skill)
- Plain CSS without Tailwind (use css skill)
- Complex animations requiring custom CSS (use css skill)

---

## Critical Patterns

### ✅ REQUIRED: Use Utility Classes

```html
<!-- ✅ CORRECT: Utility classes -->
<button
  class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
>
  Click Me
</button>

<!-- ❌ WRONG: Custom CSS for basic styling -->
<button class="custom-button">Click Me</button>
<style>
  .custom-button {
    background: blue;
    padding: 8px 16px;
  }
</style>
```

### ✅ REQUIRED: Configure Theme in tailwind.config

```javascript
// ✅ CORRECT: Extend theme
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: '#1976d2',
      },
    },
  },
};

// ❌ WRONG: Hardcoding hex colors in classes
<div class="bg-[#1976d2]"> // Use theme colors instead
```

### ❌ NEVER: Overuse @apply

```css
/* ❌ WRONG: Defeats utility-first purpose */
.btn {
  @apply bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded;
}

/* ✅ CORRECT: Use utilities directly in HTML */
<button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
```

### ✅ REQUIRED: Define Themes with @theme (Tailwind 4+)

```css
/* ✅ CORRECT: Define theme tokens with @theme */
@theme {
  --color-primary: #4f46e5;
  --color-secondary: #9333ea;
  --font-sans: "Inter", sans-serif;
  --radius-md: 0.375rem;
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --spacing-4: 1rem;
}

/* Use in HTML: <div class="bg-primary text-secondary shadow-md"> */

/* ❌ WRONG: Hardcoding values in config (Tailwind 4+) */
tailwind.config.js:
module.exports = {
  theme: {
    colors: { primary: '#4f46e5' } // Use @theme instead
  }
}
```

### ✅ ALLOWED: Use @apply for Custom Component Classes

```css
/* ✅ CORRECT: @apply for reusable component patterns */
.bg-custom-screen {
  @apply bg-slate-100 transition-colors duration-300;

  &:hover {
    @apply bg-blue-500;
  }
}

.card-base {
  @apply rounded-lg shadow-md p-6 bg-white;
}

/* Use when: Multiple components share the same utility pattern */
/* ❌ AVOID: Single-use classes (use utilities directly instead) */
```

---

## Conventions

Refer to conventions for:

- Code organization

Refer to a11y for:

- Color contrast
- Focus indicators

Refer to css for:

- Custom CSS when needed

### Tailwind Specific

- Use utility classes over custom CSS
- Configure theme in tailwind.config
- Use @apply for component classes sparingly
- Leverage JIT mode for performance
- Use responsive modifiers (sm:, md:, lg:)
- **Enable dark mode** with `class` or `media` strategy
- **Configure content paths** properly to avoid purging used classes
- **Use arbitrary values** `[value]` only when necessary (prefer theme extension)
- **Combine utilities** with `@apply` for reusable component patterns
- **Optimize bundle size** with proper content configuration

---

## Decision Tree

**Tailwind class exists?** → Use utility class: `className="bg-blue-500"`.

**Dynamic value?** → Use inline style: `style={{ width: `${percent}%` }}` or arbitrary values: `w-[${value}px]`.

**Conditional styles?** → Use clsx/cn helper: `cn("base", condition && "variant")`.

**Reusable component style?** → Create component with utilities, avoid @apply.

**Custom color/spacing?** → Add to `theme.extend` in tailwind.config.js.

**Responsive design?** → Use breakpoint prefixes: `md:flex lg:grid`.

**Dark mode?** → Enable in config, use `dark:` prefix: `dark:bg-gray-800`.

**Production build?** → Ensure all template paths in `content` array or classes will be purged. Check for dynamic class names.

**Custom animations?** → Extend `theme.animation` and `theme.keyframes` in tailwind.config rather than custom CSS.

**Complex component style?** → Use `@apply` with `@layer components` for reusable patterns, but keep most styles as utilities in HTML.

---

## Example

```html
<div class="max-w-4xl mx-auto p-6">
  <h1 class="text-3xl font-bold text-gray-900 mb-4">Title</h1>
  <button
    class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
  >
    Click Me
  </button>
</div>
```

tailwind.config.js:

```javascript
module.exports = {
  content: ["./src/**/*.{astro,html,js,jsx,ts,tsx,vue,svelte}"], // ⚠️ CRITICAL
  darkMode: "class", // or 'media'
  theme: {
    extend: {
      colors: {
        brand: "#1976d2",
      },
    },
  },
};
```

### Dark Mode

```html
<!-- Enable with 'class' strategy -->
<html class="dark">
  <!-- dark: prefix works -->
  <div class="bg-white dark:bg-gray-900 text-black dark:text-white">
    Content adapts to dark mode
  </div>
</html>
```

```javascript
// Toggle dark mode
document.documentElement.classList.toggle("dark");
```

---

## Edge Cases

**Arbitrary values:** Use square brackets for one-off values: `w-[137px]`, `top-[117px]`. Avoid overuse—extend theme instead.

**Specificity conflicts:** Tailwind utilities have same specificity. Order in HTML matters. Use `!` prefix for important: `!mt-0`.

**Purge/content configuration:** Ensure all template paths are in `content` array or classes will be purged in production.

**Third-party component styling:** Some libraries use inline styles that override Tailwind. Use `!important` sparingly or wrapper divs.

**@layer directive:** Use `@layer components` for custom component styles, `@layer utilities` for custom utilities. Ensures proper ordering.

---

## References

- https://tailwindcss.com/docs
- https://tailwindcss.com/docs/configuration
