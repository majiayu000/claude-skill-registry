---
name: tailwind-v4-shadcn
description: |
  Set up Tailwind v4 with shadcn/ui using @theme inline pattern and CSS variable architecture. Four-step pattern: CSS variables, Tailwind mapping, base styles, automatic dark mode. Prevents 8 documented errors.

  Use when initializing React projects with Tailwind v4, or fixing colors not working, tw-animate-css errors, @theme inline dark mode conflicts, @apply breaking, v3 migration issues.
user-invocable: true
---

# Tailwind v4 + shadcn/ui Production Stack

**Production-tested**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)
**Last Updated**: 2026-01-20
**Versions**: tailwindcss@4.1.18, @tailwindcss/vite@4.1.18
**Status**: Production Ready ✅

---

## Quick Start (Follow This Exact Order)

```bash
# 1. Install dependencies
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init

# 2. Delete v3 config if exists
rm tailwind.config.ts  # v4 doesn't use this file
```

**vite.config.ts**:
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

**components.json** (CRITICAL):
```json
{
  "tailwind": {
    "config": "",              // ← Empty for v4
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true
  }
}
```

---

## The Four-Step Architecture (MANDATORY)

Skipping steps will break your theme. Follow exactly:

### Step 1: Define CSS Variables at Root

```css
/* src/index.css */
@import "tailwindcss";
@import "tw-animate-css";  /* Required for shadcn/ui animations */

:root {
  --background: hsl(0 0% 100%);      /* ← hsl() wrapper required */
  --foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(221.2 83.2% 53.3%);
  /* ... all light mode colors */
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --primary: hsl(217.2 91.2% 59.8%);
  /* ... all dark mode colors */
}
```

**Critical**: Define at root level (NOT inside `@layer base`). Use `hsl()` wrapper.

### Step 2: Map Variables to Tailwind Utilities

```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  /* ... map ALL CSS variables */
}
```

**Why**: Generates utility classes (`bg-background`, `text-primary`). Without this, utilities won't exist.

### Step 3: Apply Base Styles

```css
@layer base {
  body {
    background-color: var(--background);  /* NO hsl() wrapper here */
    color: var(--foreground);
  }
}
```

**Critical**: Reference variables directly. Never double-wrap: `hsl(var(--background))`.

### Step 4: Result - Automatic Dark Mode

```tsx
<div className="bg-background text-foreground">
  {/* No dark: variants needed - theme switches automatically */}
</div>
```

---

## Dark Mode Setup

**1. Create ThemeProvider** (see `templates/theme-provider.tsx`)

**2. Wrap App**:
```typescript
// src/main.tsx
import { ThemeProvider } from '@/components/theme-provider'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
    <App />
  </ThemeProvider>
)
```

**3. Add Theme Toggle**:
```bash
pnpm dlx shadcn@latest add dropdown-menu
```

See `reference/dark-mode.md` for ModeToggle component.

---

## Critical Rules

### ✅ Always Do:

1. Wrap colors with `hsl()` in `:root`/`.dark`: `--bg: hsl(0 0% 100%);`
2. Use `@theme inline` to map all CSS variables
3. Set `"tailwind.config": ""` in components.json
4. Delete `tailwind.config.ts` if exists
5. Use `@tailwindcss/vite` plugin (NOT PostCSS)

### ❌ Never Do:

1. Put `:root`/`.dark` inside `@layer base` (causes cascade issues)
2. Use `.dark { @theme { } }` pattern (v4 doesn't support nested @theme)
3. Double-wrap colors: `hsl(var(--background))`
4. Use `tailwind.config.ts` for theme (v4 ignores it)
5. Use `@apply` directive (deprecated in v4, see error #7)
6. Use `dark:` variants for semantic colors (auto-handled)
7. Use `@apply` with `@layer base` or `@layer components` classes (v4 breaking change - use `@utility` instead) | [Source](https://github.com/tailwindlabs/tailwindcss/discussions/17082)
8. Wrap ANY styles in `@layer base` without understanding CSS layer ordering (see error #8) | [Source](https://github.com/tailwindlabs/tailwindcss/discussions/16002)

---

## Common Errors & Solutions

This skill prevents **8 documented errors**.

### 1. ❌ tw-animate-css Import Error

**Error**: "Cannot find module 'tailwindcss-animate'"

**Cause**: shadcn/ui deprecated `tailwindcss-animate` for v4.

**Solution**:
```bash
# ✅ DO
pnpm add -D tw-animate-css

# Add to src/index.css:
@import "tailwindcss";
@import "tw-animate-css";

# ❌ DON'T
npm install tailwindcss-animate  # v3 only
```

---

### 2. ❌ Colors Not Working

**Error**: `bg-primary` doesn't apply styles

**Cause**: Missing `@theme inline` mapping

**Solution**:
```css
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  /* ... map ALL CSS variables */
}
```

---

### 3. ❌ Dark Mode Not Switching

**Error**: Theme stays light/dark

**Cause**: Missing ThemeProvider

**Solution**:
1. Create ThemeProvider (see `templates/theme-provider.tsx`)
2. Wrap app in `main.tsx`
3. Verify `.dark` class toggles on `<html>` element

---

### 4. ❌ Duplicate @layer base

**Error**: "Duplicate @layer base" in console

**Cause**: shadcn init adds `@layer base` - don't add another

**Solution**:
```css
/* ✅ Correct - single @layer base */
@import "tailwindcss";

:root { --background: hsl(0 0% 100%); }

@theme inline { --color-background: var(--background); }

@layer base { body { background-color: var(--background); } }
```

---

### 5. ❌ Build Fails with tailwind.config.ts

**Error**: "Unexpected config file"

**Cause**: v4 doesn't use `tailwind.config.ts` (v3 legacy)

**Solution**:
```bash
rm tailwind.config.ts
```

v4 configuration happens in `src/index.css` using `@theme` directive.

---

### 6. ❌ @theme inline Breaks Dark Mode in Multi-Theme Setups

**Error**: Dark mode doesn't switch when using `@theme inline` with custom variants (e.g., `data-mode="dark"`)
**Source**: [GitHub Discussion #18560](https://github.com/tailwindlabs/tailwindcss/discussions/18560)

**Cause**: `@theme inline` bakes variable VALUES into utilities at build time. When dark mode changes the underlying CSS variables, utilities don't update because they reference hardcoded values, not variables.

**Why It Happens**:
- `@theme inline` inlines VALUES at build time: `bg-primary` → `background-color: oklch(...)`
- Dark mode overrides change the CSS variables, but utilities already have baked-in values
- The CSS specificity chain breaks

**Solution**: Use `@theme` (without inline) for multi-theme scenarios:

```css
/* ✅ CORRECT - Use @theme without inline */
@custom-variant dark (&:where([data-mode=dark], [data-mode=dark] *));

@theme {
  --color-text-primary: var(--color-slate-900);
  --color-bg-primary: var(--color-white);
}

@layer theme {
  [data-mode="dark"] {
    --color-text-primary: var(--color-white);
    --color-bg-primary: var(--color-slate-900);
  }
}
```

**When to use inline**:
- Single theme + dark mode toggle (like shadcn/ui default) ✅
- Referencing other CSS variables that don't change ✅

**When NOT to use inline**:
- Multi-theme systems (data-theme="blue" | "green" | etc.) ❌
- Dynamic theme switching beyond light/dark ❌

**Maintainer Guidance** (Adam Wathan):
> "It's more idiomatic in v4 for the actual generated CSS to reference your theme variables. I would personally only use inline when things don't work without it."

---

### 7. ❌ @apply with @layer base/components (v4 Breaking Change)

**Error**: `Cannot apply unknown utility class: custom-button`
**Source**: [GitHub Discussion #17082](https://github.com/tailwindlabs/tailwindcss/discussions/17082)

**Cause**: In v3, classes defined in `@layer base` and `@layer components` could be used with `@apply`. In v4, this is a breaking architectural change.

**Why It Happens**: v4 doesn't "hijack" the native CSS `@layer` at-rule anymore. Only classes defined with `@utility` are available to `@apply`.

**Migration**:
```css
/* ❌ v3 pattern (worked) */
@layer components {
  .custom-button {
    @apply px-4 py-2 bg-blue-500;
  }
}

/* ✅ v4 pattern (required) */
@utility custom-button {
  @apply px-4 py-2 bg-blue-500;
}

/* OR use native CSS */
@layer base {
  .custom-button {
    padding: 1rem 0.5rem;
    background-color: theme(colors.blue.500);
  }
}
```

**Note**: This skill already discourages `@apply` usage. This error is primarily for users migrating from v3.

---

### 8. ❌ @layer base Styles Not Applying

**Error**: Styles defined in `@layer base` seem to be ignored
**Source**: [GitHub Discussion #16002](https://github.com/tailwindlabs/tailwindcss/discussions/16002) | [Discussion #18123](https://github.com/tailwindlabs/tailwindcss/discussions/18123)

**Cause**: v4 uses native CSS layers. Base styles CAN be overridden by utility layers due to CSS cascade if layers aren't explicitly ordered.

**Why It Happens**:
- v3: Tailwind intercepted `@layer base/components/utilities` and processed them specially
- v4: Uses native CSS layers - if you don't import layers in the right order, precedence breaks
- Styles ARE being applied, but utilities override them

**Solution Option 1**: Define layers explicitly:
```css
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/base.css" layer(base);
@import "tailwindcss/components.css" layer(components);
@import "tailwindcss/utilities.css" layer(utilities);

@layer base {
  body {
    background-color: var(--background);
  }
}
```

**Solution Option 2** (Recommended): Don't use `@layer base` - define styles at root level:
```css
@import "tailwindcss";

:root {
  --background: hsl(0 0% 100%);
}

body {
  background-color: var(--background); /* No @layer needed */
}
```

**Applies to**: ALL base styles, not just color variables. Avoid wrapping ANY styles in `@layer base` unless you understand CSS layer ordering.

---

## Quick Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `bg-primary` doesn't work | Missing `@theme inline` | Add `@theme inline` block |
| Colors all black/white | Double `hsl()` wrapping | Use `var(--color)` not `hsl(var(--color))` |
| Dark mode not switching | Missing ThemeProvider | Wrap app in `<ThemeProvider>` |
| Build fails | `tailwind.config.ts` exists | Delete file |
| Animation errors | Using `tailwindcss-animate` | Install `tw-animate-css` |

---

## What's New in Tailwind v4

### OKLCH Color Space (December 2024)

Tailwind v4.0 replaced the entire default color palette with OKLCH, a perceptually uniform color space.
**Source**: [Tailwind v4.0 Release](https://tailwindcss.com/blog/tailwindcss-v4) | [OKLCH Migration Guide](https://andy-cinquin.com/blog/migration-oklch-tailwind-css-4-0)

**Why OKLCH**:
- **Perceptual consistency**: HSL's "50% lightness" is visually inconsistent across hues (yellow appears much brighter than blue at same lightness)
- **Better gradients**: Smooth transitions without muddy middle colors
- **Wider gamut**: Supports colors beyond sRGB on modern displays
- **More vibrant colors**: Eye-catching, saturated colors previously limited by sRGB

**Browser Support** (January 2026):
- Chrome 111+, Firefox 113+, Safari 15.4+, Edge 111+
- Global coverage: 93.1%

**Automatic Fallbacks**: Tailwind generates sRGB fallbacks for older browsers:
```css
.bg-blue-500 {
  background-color: #3b82f6; /* sRGB fallback */
  background-color: oklch(0.6 0.24 264); /* Modern browsers */
}
```

**Custom Colors**: When defining custom colors, OKLCH is now preferred:
```css
@theme {
  /* Modern approach (preferred) */
  --color-brand: oklch(0.7 0.15 250);

  /* Legacy approach (still works) */
  --color-brand: hsl(240 80% 60%);
}
```

**Migration**: No breaking changes - Tailwind generates fallbacks automatically. For new projects, use OKLCH-aware tooling for custom colors.

### Built-in Features (No Plugin Needed)

**Container Queries** (built-in as of v4.0):
```tsx
<div className="@container">
  <div className="@md:text-lg @lg:grid-cols-2">
    Content responds to container width, not viewport
  </div>
</div>
```

**Line Clamp** (built-in as of v3.3):
```tsx
<p className="line-clamp-3">Truncate to 3 lines with ellipsis...</p>
<p className="line-clamp-[8]">Arbitrary values supported</p>
<p className="line-clamp-(--teaser-lines)">CSS variable support</p>
```

**Removed Plugins**:
- `@tailwindcss/container-queries` - Built-in now
- `@tailwindcss/line-clamp` - Built-in since v3.3

---

## Tailwind v4 Plugins

Use `@plugin` directive (NOT `require()` or `@import`):

**Typography** (for Markdown/CMS content):
```bash
pnpm add -D @tailwindcss/typography
```
```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
```
```html
<article class="prose dark:prose-invert">{{ content }}</article>
```

**Forms** (cross-browser form styling):
```bash
pnpm add -D @tailwindcss/forms
```
```css
@import "tailwindcss";
@plugin "@tailwindcss/forms";
```

**Container Queries** (built-in, no plugin needed):
```tsx
<div className="@container">
  <div className="@md:text-lg">Responds to container width</div>
</div>
```

**Common Plugin Errors**:
```css
/* ❌ WRONG - v3 syntax */
@import "@tailwindcss/typography";

/* ✅ CORRECT - v4 syntax */
@plugin "@tailwindcss/typography";
```

---

## Setup Checklist

- [ ] `@tailwindcss/vite` installed (NOT postcss)
- [ ] `vite.config.ts` uses `tailwindcss()` plugin
- [ ] `components.json` has `"config": ""`
- [ ] NO `tailwind.config.ts` exists
- [ ] `src/index.css` follows 4-step pattern:
  - [ ] `:root`/`.dark` at root level (not in @layer)
  - [ ] Colors wrapped with `hsl()`
  - [ ] `@theme inline` maps all variables
  - [ ] `@layer base` uses unwrapped variables
- [ ] ThemeProvider wraps app
- [ ] Theme toggle works

---

## File Templates

Available in `templates/` directory:

- **index.css** - Complete CSS with all color variables
- **components.json** - shadcn/ui v4 config
- **vite.config.ts** - Vite + Tailwind plugin
- **theme-provider.tsx** - Dark mode provider
- **utils.ts** - `cn()` utility

---

## Migration from v3

See `reference/migration-guide.md` for complete guide.

**Key Changes**:
- Delete `tailwind.config.ts`
- Move theme to CSS with `@theme inline`
- Replace `@tailwindcss/line-clamp` (now built-in: `line-clamp-*`)
- Replace `tailwindcss-animate` with `tw-animate-css`
- Update plugins: `require()` → `@plugin`

### Additional Migration Gotchas

#### Automated Migration Tool May Fail

**Warning**: The `@tailwindcss/upgrade` utility often fails to migrate configurations.
**Source**: [Community Reports](https://medium.com/better-dev-nextjs-react/tailwind-v4-migration-from-javascript-config-to-css-first-in-2025-ff3f59b215ca) | [GitHub Discussion #16642](https://github.com/tailwindlabs/tailwindcss/discussions/16642)

**Common failures**:
- Typography plugin configurations
- Complex theme extensions
- Custom plugin setups

**Recommendation**: Don't rely on automated migration. Follow manual steps in the migration guide instead.

#### Default Element Styles Removed

Tailwind v4 takes a more minimal approach to Preflight, removing default styles for headings, lists, and buttons.
**Source**: [GitHub Discussion #16517](https://github.com/tailwindlabs/tailwindcss/discussions/16517) | [Medium: Migration Problems](https://medium.com/better-dev-nextjs-react/tailwind-v4-migration-from-javascript-config-to-css-first-in-2025-ff3f59b215ca)

**Impact**:
- All headings (`<h1>` through `<h6>`) render at same size
- Lists lose default padding
- Visual regressions in existing projects

**Solutions**:

**Option 1: Use @tailwindcss/typography for content pages**:
```bash
pnpm add -D @tailwindcss/typography
```
```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
```
```tsx
<article className="prose dark:prose-invert">
  {/* All elements styled automatically */}
</article>
```

**Option 2: Add custom base styles**:
```css
@layer base {
  h1 { @apply text-4xl font-bold mb-4; }
  h2 { @apply text-3xl font-bold mb-3; }
  h3 { @apply text-2xl font-bold mb-2; }
  ul { @apply list-disc pl-6 mb-4; }
  ol { @apply list-decimal pl-6 mb-4; }
}
```

#### PostCSS Setup Complexity

**Recommendation**: Use `@tailwindcss/vite` plugin for Vite projects instead of PostCSS.
**Source**: [Medium: Migration Problems](https://medium.com/better-dev-nextjs-react/tailwind-v4-migration-from-javascript-config-to-css-first-in-2025-ff3f59b215ca) | [GitHub Discussion #15764](https://github.com/tailwindlabs/tailwindcss/discussions/15764)

**Why Vite Plugin is Better**:
```typescript
// ✅ Vite Plugin - One line, no PostCSS config
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})

// ❌ PostCSS - Multiple steps, plugin compatibility issues
// 1. Install @tailwindcss/postcss
// 2. Configure postcss.config.js
// 3. Manage plugin order
// 4. Debug plugin conflicts
```

**PostCSS Problems Reported**:
- Error: "It looks like you're trying to use tailwindcss directly as a PostCSS plugin"
- Multiple PostCSS plugins required: `postcss-import`, `postcss-advanced-variables`, `tailwindcss/nesting`
- v4 PostCSS plugin is separate package: `@tailwindcss/postcss`

**Official Guidance**: The Vite plugin is recommended for Vite projects. PostCSS is for legacy setups or non-Vite environments.

#### Visual Changes

**Ring Width Default**: Changed from 3px to 1px
**Source**: [Medium: Migration Guide](https://medium.com/better-dev-nextjs-react/tailwind-v4-migration-from-javascript-config-to-css-first-in-2025-ff3f59b215ca)

- `ring` class is now thinner
- Use `ring-3` to match v3 appearance

```tsx
// v3: 3px ring
<button className="ring">Button</button>

// v4: 1px ring (thinner)
<button className="ring">Button</button>

// Match v3 appearance
<button className="ring-3">Button</button>
```

---

## Reference Documentation

- **architecture.md** - Deep dive into 4-step pattern
- **dark-mode.md** - Complete dark mode implementation
- **common-gotchas.md** - Troubleshooting guide
- **migration-guide.md** - v3 → v4 migration

---

## Official Documentation

- **shadcn/ui Vite Setup**: https://ui.shadcn.com/docs/installation/vite
- **shadcn/ui Tailwind v4**: https://ui.shadcn.com/docs/tailwind-v4
- **Tailwind v4 Docs**: https://tailwindcss.com/docs

---

**Last Updated**: 2026-01-20
**Skill Version**: 3.0.0
**Tailwind v4**: 4.1.18 (Latest)
**Production**: WordPress Auditor (https://wordpress-auditor.webfonts.workers.dev)

**Changelog**:
- v3.0.0 (2026-01-20): Major research update - added 3 TIER 1 errors (#6-8), expanded migration guide with community findings (TIER 2), added OKLCH color space section, PostCSS complexity warnings, and migration tool limitations
- v2.0.1 (2026-01-03): Production verification
- v2.0.0: Initial release with 5 documented errors
