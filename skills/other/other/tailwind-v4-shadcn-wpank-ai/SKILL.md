---
name: tailwind-v4-+-shadcn/ui-stack
model: fast
---

# Tailwind v4 + shadcn/ui Stack

Production-tested setup for Tailwind v4 with shadcn/ui. Prevents 8 documented errors through a mandatory four-step architecture.

## WHAT

Complete Tailwind v4 + shadcn/ui configuration:
- Four-step theming architecture (mandatory)
- CSS variable-based color system
- Automatic dark mode switching
- Error prevention for 8 common mistakes
- Migration guide from v3
- Production-ready templates

## WHEN

- Starting a new React/Vite project with Tailwind v4
- Migrating from Tailwind v3 to v4
- Setting up shadcn/ui with Tailwind v4
- Debugging: colors not working, dark mode broken, build failures
- Fixing `@theme inline`, `@apply`, or `@layer base` issues

## KEYWORDS

tailwind v4, tailwindcss 4, shadcn, shadcn/ui, @theme inline, dark mode, css variables, vite, tw-animate-css, tailwind config, migration

**Production verified:** WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)  
**Versions:** tailwindcss@4.1.18, @tailwindcss/vite@4.1.18


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install tailwind-v4-shadcn
```


---

## Quick Start

```bash
# 1. Install dependencies
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init

# 2. Delete v3 config (v4 doesn't use it)
rm tailwind.config.ts
```

**vite.config.ts:**
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { '@': path.resolve(__dirname, './src') } }
})
```

**components.json (CRITICAL):**
```json
{
  "tailwind": {
    "config": "",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  }
}
```

---

## The Four-Step Architecture (MANDATORY)

Skipping steps breaks theming. Follow exactly:

### Step 1: Define CSS Variables at Root

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";

:root {
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
  --primary-foreground: hsl(210 40% 98%);
  /* ... all light mode colors with hsl() wrapper */
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
  --primary-foreground: hsl(222.2 47.4% 11.2%);
  /* ... all dark mode colors */
}
```

**Critical:** Define at root level (NOT inside `@layer base`). Use `hsl()` wrapper.

### Step 2: Map Variables to Tailwind

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... map ALL CSS variables */
}
```

**Why:** Generates utility classes (`bg-background`, `text-primary`). Without this, utilities don't exist.

### Step 3: Apply Base Styles

```css
@layer base {
  body {
    background-color: var(--background);
    color: var(--foreground);
  }
}
```

**Critical:** Reference variables directly. Never double-wrap: `hsl(var(--background))`.

### Step 4: Result - Automatic Dark Mode

```tsx
<div className="bg-background text-foreground">
  {/* Theme switches automatically via .dark class */}
</div>
```

No `dark:` variants needed for semantic colors.

---

## Critical Rules

### Always Do
1. Wrap colors with `hsl()` in `:root`/`.dark`: `--bg: hsl(0 0% 100%);`
2. Use `@theme inline` to map all CSS variables
3. Set `"tailwind.config": ""` in components.json
4. Delete `tailwind.config.ts` if exists
5. Use `@tailwindcss/vite` plugin (NOT PostCSS)

### Never Do
1. Put `:root`/`.dark` inside `@layer base`
2. Use `.dark { @theme { } }` (v4 doesn't support nested @theme)
3. Double-wrap: `hsl(var(--background))`
4. Use `tailwind.config.ts` for theme
5. Use `@apply` with `@layer base/components` classes
6. Use `dark:` variants for semantic colors

---

## Common Errors & Solutions

### Error 1: tw-animate-css Import

**Error:** `Cannot find module 'tailwindcss-animate'`

```bash
# Wrong (v3 package)
npm install tailwindcss-animate

# Correct (v4 package)
pnpm add -D tw-animate-css
```

```css
@import "tailwindcss";
@import "tw-animate-css";
```

### Error 2: Colors Not Working

**Error:** `bg-primary` doesn't apply styles

**Cause:** Missing `@theme inline` mapping

```css
@theme inline {
  --color-primary: var(--primary);
  /* Map ALL variables */
}
```

### Error 3: Dark Mode Not Switching

**Cause:** Missing ThemeProvider

See `templates/theme-provider.tsx` and wrap your app.

### Error 4: Build Fails

**Error:** `Unexpected config file`

```bash
rm tailwind.config.ts  # v4 doesn't use this
```

### Error 5: @theme inline Breaks Multi-Theme

**Cause:** `@theme inline` bakes values at build time

Use `@theme` (without inline) for multi-theme systems:

```css
/* For multi-theme (not just light/dark) */
@theme {
  --color-text-primary: var(--color-slate-900);
}

@layer theme {
  [data-theme="dark"] {
    --color-text-primary: var(--color-white);
  }
}
```

### Error 6: @apply Breaking

**Error:** `Cannot apply unknown utility class`

v4 changed `@apply` behavior:

```css
/* Wrong (v3 pattern) */
@layer components {
  .custom-button { @apply px-4 py-2; }
}

/* Correct (v4 pattern) */
@utility custom-button {
  @apply px-4 py-2;
}
```

### Error 7: @layer base Styles Ignored

**Cause:** CSS layer cascade issues

```css
/* Better: Don't use @layer base for critical styles */
body {
  background-color: var(--background);
}
```

---

## Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bg-primary` doesn't work | Missing `@theme inline` | Add mapping |
| Colors black/white | Double `hsl()` | Use `var(--color)` not `hsl(var(--color))` |
| Dark mode stuck | Missing ThemeProvider | Wrap app |
| Build fails | `tailwind.config.ts` exists | Delete file |
| Animation errors | Wrong package | Use `tw-animate-css` |

---

## Tailwind v4 New Features

### OKLCH Color Space

v4 uses OKLCH for perceptually uniform colors. Automatic sRGB fallbacks generated.

```css
@theme {
  /* Modern approach */
  --color-brand: oklch(0.7 0.15 250);
  
  /* Legacy (still works) */
  --color-brand: hsl(240 80% 60%);
}
```

### Container Queries (Built-in)

```tsx
<div className="@container">
  <div className="@md:text-lg @lg:grid-cols-2">
    Content responds to container width
  </div>
</div>
```

### Line Clamp (Built-in)

```tsx
<p className="line-clamp-3">Truncate to 3 lines...</p>
```

### Plugins

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
```

---

## Migration from v3

### Key Changes

1. Delete `tailwind.config.ts`
2. Move theme to CSS with `@theme inline`
3. Replace `tailwindcss-animate` → `tw-animate-css`
4. Replace `require()` → `@plugin`
5. `@apply` in `@layer components` → `@utility`

### Color Migration

```tsx
// Before: Hardcoded + dark variants
<div className="bg-blue-50 dark:bg-blue-950 text-blue-700 dark:text-blue-300">

// After: Semantic + automatic
<div className="bg-info/10 text-info">
```

### Visual Changes

- Ring width default: 3px → 1px (use `ring-3` to match v3)
- Heading styles removed from Preflight (add via `@tailwindcss/typography` or custom)

---

## Files

- `templates/index.css` - Complete CSS with all variables
- `templates/theme-provider.tsx` - Dark mode provider
- `templates/vite.config.ts` - Vite configuration
- `templates/components.json` - shadcn/ui v4 config
- `templates/utils.ts` - `cn()` utility
- `references/architecture.md` - Deep dive on four-step pattern
- `references/migration-guide.md` - Semantic color migration
- `references/dark-mode.md` - Complete dark mode setup

---

## Setup Checklist

- [ ] `@tailwindcss/vite` installed
- [ ] `vite.config.ts` uses `tailwindcss()` plugin
- [ ] `components.json` has `"config": ""`
- [ ] NO `tailwind.config.ts` exists
- [ ] `src/index.css` follows 4-step pattern
- [ ] ThemeProvider wraps app
- [ ] Theme toggle works

---

## NEVER

- Put `:root` or `.dark` inside `@layer base`
- Use `tailwind.config.ts` with v4 (it's ignored)
- Double-wrap colors: `hsl(var(--background))`
- Use `tailwindcss-animate` (use `tw-animate-css`)
- Use `@apply` on `@layer base/components` classes in v4
- Skip the `@theme inline` step
