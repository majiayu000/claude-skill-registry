---
name: tailwind-4
description: >
  Tailwind CSS 4 patterns and best practices.
  Trigger: When styling with Tailwind classes, especially when dynamic styling or CSS variables are involved (no var() in class names).
license: Apache-2.0
metadata:
  author: prowler-cloud
  version: "1.0"
  scope: [root, ui]
  auto_invoke: "Working with Tailwind classes"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

# Styling Decision Tree

```md
Tailwind class exists?  → class="..."
Dynamic value?          → style attribute (e.g., style="width: ${x}%")
Conditional styles?     → Use framework utility (cn(), clsx, etc.)
Static only?            → class="..." (no utility needed)
Library can't use class?→ style attribute with var() constants
```

## Critical Rules

### Never Use var() in class Names

```html
<!-- ❌ NEVER: var() in class names -->
<div class="bg-[var(--color-primary)]"></div>
<div class="text-[var(--text-color)]"></div>

<!-- ✅ ALWAYS: Use Tailwind semantic classes -->
<div class="bg-primary"></div>
<div class="text-slate-400"></div>
```

### Never Use Hex Colors

```html
<!-- ❌ NEVER: Hex colors in class names -->
<p class="text-[#ffffff]"></p>
<div class="bg-[#1e293b]"></div>

<!-- ✅ ALWAYS: Use Tailwind color classes -->
<p class="text-white"></p>
<div class="bg-slate-800"></div>
```

## Conditional Classes

For conditional class logic, use class-merging utilities like `clsx` or `tailwind-merge` (often combined as `cn()`).

### When to Use Class Merging

```html
<!-- ✅ Conditional classes - use utility -->
<div class="base-class active-class"></div>

<!-- ✅ Multiple conditions -->
<div class="rounded-lg border bg-blue-500 text-white"></div>
```

### When NOT to Use Class Merging

```html
<!-- ❌ Static classes - no utility needed -->
<div class="flex items-center gap-2"></div>

<!-- ✅ Just use class directly -->
<div class="flex items-center gap-2"></div>
```

### Common Utility Implementation

```javascript
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
```

## Style Constants for Libraries with Limited Class Support

When libraries don't accept class names or have limited styling options, use CSS custom properties:

```javascript
// ✅ Constants with var() - ONLY for library props that can't use classes
const CHART_COLORS = {
  primary: "var(--color-primary)",
  secondary: "var(--color-secondary)",
  text: "var(--color-text)",
  gridLine: "var(--color-border)",
};

// Usage depends on the library's API
// Example: Chart.js configuration object
const chartConfig = {
  scales: {
    y: {
      grid: { color: CHART_COLORS.gridLine }
    }
  }
};
```

## Dynamic Values

For truly dynamic values, use inline styles:

```html
<!-- ✅ style attribute for dynamic values -->
<div style="width: 75%"></div>
<div style="opacity: 0.5"></div>

<!-- ✅ CSS custom properties for theming -->
<div style="--progress: 75%"></div>
```

## Common Patterns

### Flexbox

```html
<div class="flex items-center justify-between gap-4"></div>
<div class="flex flex-col gap-2"></div>
<div class="inline-flex items-center"></div>
```

### Grid

```html
<div class="grid grid-cols-3 gap-4"></div>
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"></div>
```

### Spacing

```html
<!-- Padding -->
<div class="p-4"></div>           <!-- All sides -->
<div class="px-4 py-2"></div>     <!-- Horizontal, vertical -->
<div class="pt-4 pb-2"></div>     <!-- Top, bottom -->

<!-- Margin -->
<div class="m-4"></div>
<div class="mx-auto"></div>       <!-- Center horizontally -->
<div class="mt-8 mb-4"></div>
```

### Typography

```html
<h1 class="text-2xl font-bold text-white"></h1>
<p class="text-sm text-slate-400"></p>
<span class="text-xs font-medium uppercase tracking-wide"></span>
```

### Borders & Shadows

```html
<div class="rounded-lg border border-slate-700"></div>
<div class="rounded-full shadow-lg"></div>
<div class="ring-2 ring-blue-500 ring-offset-2"></div>
```

### States

```html
<button class="hover:bg-blue-600 focus:ring-2 active:scale-95"></button>
<input class="focus:border-blue-500 focus:outline-none">
<div class="group-hover:opacity-100"></div>
```

### Responsive

```html
<div class="w-full md:w-1/2 lg:w-1/3"></div>
<div class="hidden md:block"></div>
<div class="text-sm md:text-base lg:text-lg"></div>
```

### Dark Mode

```html
<div class="bg-white dark:bg-slate-900"></div>
<p class="text-gray-900 dark:text-white"></p>
```

## Arbitrary Values (Escape Hatch)

```html
<!-- ✅ OK for one-off values not in design system -->
<div class="w-[327px]"></div>
<div class="top-[117px]"></div>
<div class="grid-cols-[1fr_2fr_1fr]"></div>

<!-- ❌ Don't use for colors - use theme instead -->
<div class="bg-[#1e293b]"></div>  <!-- NO -->
```
