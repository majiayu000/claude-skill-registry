---
name: web-styling-tailwind
description: Tailwind CSS v4 - utility-first CSS framework with CSS-first configuration
---

# Tailwind CSS v4 Patterns

> **Quick Guide:** Tailwind CSS v4 uses CSS-first configuration with `@import "tailwindcss"` and `@theme` directive (NOT `tailwind.config.js`). Define design tokens as CSS variables in `@theme`, create custom utilities with `@utility`, custom variants with `@custom-variant`. Automatic content detection (no `content` array). Use `@tailwindcss/vite` plugin for Vite projects. All colors use oklch. No Sass/Less/Stylus support.

**Detailed Resources:**

- For code examples, see [examples/](examples/) folder:
  - [core.md](examples/core.md) - Setup, responsive design, dark mode, state variants, theme customization
  - [advanced.md](examples/advanced.md) - Custom utilities, custom variants, container queries, 3D transforms, animations, component extraction

---

<critical_requirements>

## ⚠️ CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@import "tailwindcss"` and `@theme` for configuration - NEVER use `tailwind.config.js`, `@tailwind base`, or `module.exports`)**

**(You MUST use `@utility` for custom utilities - NEVER use `@layer utilities {}` (v3 syntax))**

**(You MUST use oklch or CSS variable references for custom colors in `@theme` - NEVER use hex/rgb for theme tokens)**

**(You MUST use `@tailwindcss/vite` for Vite projects and `@tailwindcss/postcss` for others - NEVER use `tailwindcss` directly as PostCSS plugin)**

**(You MUST specify border colors explicitly - v4 defaults to `currentColor` not `gray-200`)**

</critical_requirements>

---

**Auto-detection:** Tailwind CSS, tailwindcss, @import "tailwindcss", @theme, @utility, @custom-variant, utility classes, bg-_, text-_, flex, grid, responsive design, dark:, hover:, focus:, @tailwindcss/vite, @tailwindcss/postcss, tailwind-merge, cn()

**When to use:**

- Styling with utility-first CSS classes directly in markup
- Configuring design tokens with CSS-first `@theme` directive
- Implementing responsive design with breakpoint variants
- Adding dark mode with `dark:` variant
- Creating custom utilities and variants in CSS
- Building component libraries with Tailwind + React
- Using container queries, 3D transforms, or modern CSS features

**Key patterns covered:**

- CSS-first setup with `@import "tailwindcss"` and `@theme`
- Responsive design with breakpoint variants (`sm:`, `md:`, `lg:`)
- Dark mode configuration (media, class, data-attribute strategies)
- State variants (`hover:`, `focus:`, `group-*:`, `peer-*:`)
- Theme customization with `@theme` namespaces
- Custom utilities with `@utility` and functional values
- Custom variants with `@custom-variant`
- Container queries (`@container`, `@sm:`, `@max-*:`)
- 3D transforms (`rotate-x-*`, `perspective-*`, `transform-3d`)
- Animation with `@starting-style` and `@keyframes`
- Component extraction with `cn()` (clsx + tailwind-merge)
- Migration notes from v3 to v4

**When NOT to use:**

- Projects requiring Sass/Less/Stylus (v4 is a standalone preprocessor, no Sass support)
- Projects needing IE11 or older browser support (requires Safari 16.4+, Chrome 111+, Firefox 128+)
- Tiny projects where a full utility framework is overkill (use plain CSS)
- Projects already using SCSS Modules with an established design system

---

<philosophy>

## Philosophy

Tailwind CSS v4 follows a **utility-first, CSS-native** approach: style directly in markup using composable utility classes, configure design tokens in CSS with `@theme`, and extend with `@utility`/`@custom-variant` directives. No JavaScript configuration files needed.

**Core Principles:**

- **Utility-first:** Compose styles from small, single-purpose classes in HTML
- **CSS-first configuration:** Design tokens defined in CSS via `@theme`, not JavaScript
- **Zero configuration defaults:** Automatic content detection, sensible default theme
- **Variant-driven states:** Responsive, dark mode, hover, focus -- all via class prefixes
- **Modern CSS foundation:** Built on cascade layers, `@property`, `color-mix()`, oklch colors
- **Performance-first:** 5x faster full builds, 100x faster incremental rebuilds vs v3

**v4 vs v3 -- Key Differences:**

| Aspect             | v3                                    | v4                      |
| ------------------ | ------------------------------------- | ----------------------- |
| Config             | `tailwind.config.js`                  | `@theme` in CSS         |
| Import             | `@tailwind base/components/utilities` | `@import "tailwindcss"` |
| Custom utilities   | `@layer utilities {}`                 | `@utility name {}`      |
| Custom variants    | `addVariant()` plugin                 | `@custom-variant`       |
| Content detection  | Manual `content: []`                  | Automatic               |
| Colors             | sRGB hex/rgb                          | oklch (P3 gamut)        |
| Border default     | `gray-200`                            | `currentColor`          |
| Ring default       | `3px blue-500`                        | `1px currentColor`      |
| Important modifier | `!flex`                               | `flex!`                 |
| Arbitrary vars     | `bg-[--var]`                          | `bg-(--var)`            |
| Container queries  | Plugin required                       | Built-in                |
| 3D transforms      | Not available                         | Built-in                |

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: CSS-First Setup and Configuration

Tailwind v4 replaces JavaScript config with CSS-first configuration. Use `@import "tailwindcss"` instead of `@tailwind` directives, and `@theme` instead of `tailwind.config.js`.

#### Installation Options

**Vite projects** (recommended): Use `@tailwindcss/vite` for optimal performance.
**Other bundlers**: Use `@tailwindcss/postcss` as PostCSS plugin.
**CLI**: Use `@tailwindcss/cli` for standalone builds.

#### Key Concepts

- `@import "tailwindcss"` replaces the three `@tailwind` directives
- `@theme` defines design tokens that generate utility classes AND CSS variables
- `@source` adds paths not caught by automatic content detection
- No `content` array needed -- Tailwind auto-detects template files respecting `.gitignore`

For implementation examples, see [examples/core.md](examples/core.md#pattern-1-css-first-setup-and-configuration).

---

### Pattern 2: Responsive Design with Breakpoint Variants

Tailwind v4 uses mobile-first responsive design with breakpoint variants. Default breakpoints: `sm` (40rem), `md` (48rem), `lg` (64rem), `xl` (80rem), `2xl` (96rem).

#### Key Concepts

- Mobile-first: base styles apply to all, breakpoint variants add overrides
- Custom breakpoints defined in `@theme` with `--breakpoint-*` namespace
- Stack breakpoints for ranges: `md:max-lg:hidden` (hide between md and lg)
- Use `max-*` variants for max-width queries: `max-md:hidden`

For implementation examples, see [examples/core.md](examples/core.md#pattern-2-responsive-design).

---

### Pattern 3: Dark Mode

Tailwind v4 supports three dark mode strategies: media query (default), class-based toggle, and data-attribute toggle. Override the `dark` variant with `@custom-variant`.

#### Strategies

1. **Media query** (default): Uses `prefers-color-scheme: dark` -- zero config
2. **Class-based**: Add `.dark` class to `<html>` -- use `@custom-variant dark`
3. **Data-attribute**: Use `data-theme="dark"` -- use `@custom-variant dark`

#### Key Concepts

- Default dark mode works with system preference, no config needed
- For manual toggle, override the `dark` variant with `@custom-variant`
- Use `(&:where(.dark, .dark *))` selector for class strategy
- Theme variables in `@theme` can reference CSS variables set by theme class

For implementation examples, see [examples/core.md](examples/core.md#pattern-3-dark-mode).

---

### Pattern 4: State Variants

Tailwind v4 provides comprehensive state variants for interactive styling. The `not-*` variant is new in v4.

#### Available Variants

- **Pseudo-classes:** `hover:`, `focus:`, `active:`, `visited:`, `first:`, `last:`, `odd:`, `even:`, `disabled:`, `required:`, `invalid:`
- **Group/Peer:** `group-hover:`, `group-focus:`, `peer-checked:`, `peer-invalid:`
- **Data attributes:** `data-[state=active]:`, `data-current:`
- **New in v4:** `not-hover:`, `not-focus:`, `inert:`, `starting:` (for `@starting-style`)
- **Container queries:** `@sm:`, `@md:`, `@lg:`, `@max-sm:`

#### Key v4 Changes

- `hover:` only applies on devices with hover capability (no more mobile ghost hovers)
- `not-*` variant styles when condition is NOT met
- Variant stacking is left-to-right (CSS order): `dark:hover:bg-gray-700`

For implementation examples, see [examples/core.md](examples/core.md#pattern-4-state-variants).

---

### Pattern 5: Theme Customization with @theme

The `@theme` directive defines design tokens that generate both utility classes and CSS variables. Each namespace maps to specific utility types.

#### Namespaces

| Namespace         | Generates           | Example                          |
| ----------------- | ------------------- | -------------------------------- |
| `--color-*`       | Color utilities     | `bg-brand-500`, `text-brand-500` |
| `--font-*`        | Font family         | `font-display`                   |
| `--text-*`        | Font size           | `text-display`                   |
| `--spacing-*`     | Spacing             | `px-compact`                     |
| `--breakpoint-*`  | Responsive variants | `3xl:flex`                       |
| `--radius-*`      | Border radius       | `rounded-card`                   |
| `--shadow-*`      | Box shadows         | `shadow-card`                    |
| `--ease-*`        | Timing functions    | `ease-fluid`                     |
| `--animate-*`     | Animations          | `animate-fade-in`                |
| `--blur-*`        | Blur filters        | `blur-card`                      |
| `--perspective-*` | 3D perspective      | `perspective-card`               |
| `--aspect-*`      | Aspect ratios       | `aspect-cinema`                  |

#### Key Concepts

- `--color-*: initial` resets all default colors before defining custom ones
- `--*: initial` resets the entire default theme
- `@theme inline` prevents CSS variable resolution issues when referencing other variables
- `@theme static` generates CSS variables even when utilities are unused
- `@keyframes` can be defined inside `@theme` for animation tokens

For implementation examples, see [examples/core.md](examples/core.md#pattern-5-theme-customization).

---

### Pattern 6: Custom Utilities with @utility

The `@utility` directive replaces v3's `@layer utilities {}`. Supports static utilities, functional utilities with `--value()`, and modifiers with `--modifier()`.

#### Types of Custom Utilities

1. **Static:** Fixed CSS declarations (`@utility content-auto { content-visibility: auto; }`)
2. **Functional:** Accept values via `--value()` (`@utility tab-* { tab-size: --value(integer); }`)
3. **With modifiers:** Optional modifiers via `--modifier()` for secondary values

#### Value Resolution

- `--value(--namespace-*)` matches theme variables
- `--value(integer)` matches bare integer values
- `--value([length])` matches arbitrary values in brackets
- Multiple `--value()` declarations cascade (last match wins)

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-6-custom-utilities).

---

### Pattern 7: Custom Variants with @custom-variant

The `@custom-variant` directive replaces v3's `addVariant()` plugin API. Define conditional styling rules in CSS.

#### Syntax Forms

- **Shorthand:** `@custom-variant name (selector);`
- **Block:** `@custom-variant name { /* rules with @slot */ }`
- **Complex:** Supports `@media`, `@supports`, nested selectors with `@slot` placeholder

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-7-custom-variants).

---

### Pattern 8: Container Queries

Container queries are built into v4 core (no plugin needed). Style elements based on container size, not viewport.

#### Key Concepts

- `@container` makes an element a query container
- `@sm:`, `@md:`, `@lg:` apply at container breakpoints (not viewport)
- `@max-sm:`, `@max-md:` for max-width container queries
- `@min-md:@max-xl:` for range queries
- Named containers with `@container/name` and `@sm/name:`

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-8-container-queries).

---

### Pattern 9: 3D Transforms and Modern CSS

Tailwind v4 adds first-class 3D transform utilities and leverages modern CSS features.

#### 3D Transform Utilities

- `rotate-x-*`, `rotate-y-*`, `rotate-z-*` for 3D rotation
- `translate-z-*` for depth translation
- `scale-z-*` for depth scaling
- `perspective-*` and `perspective-origin-*` for 3D perspective
- `transform-3d` to enable 3D transform context
- `backface-hidden` / `backface-visible` for card-flip effects

#### Other Modern Features

- `@starting-style` via `starting:` variant for enter/exit animations
- `field-sizing-content` for auto-resizing textareas
- `color-scheme-dark` for native dark mode scrollbars
- `inset-shadow-*` and `inset-ring-*` for layered box shadows

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-9-3d-transforms-and-modern-css).

---

### Pattern 10: Component Extraction with cn()

For React components, use `cn()` (clsx + tailwind-merge) to handle class composition and conflict resolution. Works with CVA for variant-based components.

#### Key Concepts

- `cn()` combines `clsx` (conditional classes) with `twMerge` (conflict resolution)
- External `className` prop should always be last in `cn()` to allow overrides
- Use CVA for variant-heavy components, `cn()` for simple composition
- Never use `@apply` for component extraction in React (use `cn()` instead)

For implementation examples, see [examples/advanced.md](examples/advanced.md#pattern-10-component-extraction).

</patterns>

---

<decision_framework>

## Decision Framework

### When to Use Which Styling Approach

```
Need component variants (size, intent, state)?
|-- YES --> Use CVA + cn() + Tailwind classes
|-- NO --> Just utility classes in markup

Need custom utility not in Tailwind?
|-- YES --> Is it a single fixed style?
|   |-- YES --> @utility name { declarations }
|   |-- NO --> @utility name-* { --value() }
|-- NO --> Use built-in utilities

Need conditional styling based on parent/sibling state?
|-- YES --> Is parent state?
|   |-- YES --> group/group-* pattern
|   |-- NO --> peer/peer-* pattern
|-- NO --> Direct state variants (hover:, focus:)

Need responsive behavior based on...?
|-- Viewport size --> sm:/md:/lg: breakpoint variants
|-- Container size --> @container + @sm:/@md: variants
|-- Neither --> Static styling
```

### Dark Mode Strategy

```
Is dark mode automatic (system preference only)?
|-- YES --> No config needed (default prefers-color-scheme)
|-- NO --> Need manual toggle?
    |-- YES --> Using class on <html>?
    |   |-- YES --> @custom-variant dark (&:where(.dark, .dark *))
    |   |-- NO --> @custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *))
    |-- NO --> Default media query
```

### Theme Customization Scope

```
Need to add a few custom tokens?
|-- YES --> Add to @theme alongside defaults

Need to replace an entire namespace?
|-- YES --> --namespace-*: initial; then define custom tokens

Need fully custom theme (no defaults)?
|-- YES --> --*: initial; then define everything

Need to share theme across projects?
|-- YES --> Create shared theme.css, import with @import
```

### v3 to v4 Migration Decision

```
Is the project actively maintained?
|-- YES --> Does it use tailwind.config.js plugins?
|   |-- YES --> Can plugins be replaced with @utility/@custom-variant?
|   |   |-- YES --> Migrate to v4
|   |   |-- NO --> Keep v3 or use @config/@plugin compatibility
|   |-- NO --> Migrate to v4 (run npx @tailwindcss/upgrade)
|-- NO --> Stay on v3.4 (stable, still supported)
```

</decision_framework>

---

<integration>

## Integration Guide

**Works with:**

- **React:** Use `cn()` for class composition, `className` prop forwarding, CVA for variants
- **CVA (class-variance-authority):** Define Tailwind classes in variant objects, use `tailwind-merge` for conflict resolution
- **Next.js:** Use `@tailwindcss/postcss` (App Router) or `@tailwindcss/vite` (if Vite-based)
- **Vite:** Use `@tailwindcss/vite` plugin for best performance
- **PostCSS:** Use `@tailwindcss/postcss` for non-Vite bundlers
- **tailwind-merge:** Resolves class conflicts when composing/overriding Tailwind classes
- **Prettier plugin:** `prettier-plugin-tailwindcss` for automatic class sorting

**Replaces / Conflicts with:**

- **SCSS Modules:** Tailwind replaces SCSS Modules entirely -- do not mix in the same project
- **CSS-in-JS (styled-components, Emotion):** Tailwind replaces runtime CSS-in-JS solutions
- **PostCSS plugins:** `autoprefixer` and `postcss-import` are NOT needed with v4

**Does NOT replace:**

- **CSS animations / @keyframes:** Use `@theme` to define animation tokens, but complex animations may still need custom CSS
- **CSS variables for runtime values:** Use `var()` or arbitrary values `bg-(--my-var)` alongside Tailwind

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `tailwind.config.js` without `@config` directive (v4 does NOT auto-detect JS config)
- Using `@tailwind base; @tailwind components; @tailwind utilities;` (v3 syntax, use `@import "tailwindcss"`)
- Using `@layer utilities {}` for custom utilities (use `@utility` directive)
- Using `tailwindcss` directly as PostCSS plugin (use `@tailwindcss/postcss`)
- Using `!flex` important syntax (v4 uses `flex!` -- trailing not leading)
- Using `bg-[--my-var]` for CSS variables (v4 uses `bg-(--my-var)` with parentheses)
- Using hex/rgb colors in `@theme` (use oklch for P3 gamut support)
- Assuming `border` defaults to `gray-200` (v4 defaults to `currentColor`)
- Assuming `ring` defaults to `3px` (v4 defaults to `1px`)

**Medium Priority Issues:**

- Using `@apply` for React component extraction (use `cn()` with tailwind-merge instead)
- Not specifying `@source` for node_modules UI libraries (automatic detection skips node_modules)
- Using Sass/Less/Stylus with Tailwind v4 (not supported -- v4 is a standalone preprocessor)
- Using `autoprefixer` or `postcss-import` (not needed with v4)
- Using `transform-none` to reset transforms (v4 uses individual properties, use `scale-none` / `rotate-0`)

**Common Mistakes:**

- Forgetting `@custom-variant dark` when using class-based dark mode toggle
- Using `content: ['./src/**/*.tsx']` (v4 auto-detects, no `content` array)
- Mixing v3 and v4 syntax in the same project
- Not running `npx @tailwindcss/upgrade` for automated migration

**Gotchas and Edge Cases:**

- Variant stacking order changed: v3 was right-to-left, v4 is left-to-right (follows CSS cascade)
- `hover:` only triggers on devices with hover capability (no phantom hover on touch devices)
- `space-y-*` / `divide-*` changed selectors: v3 used `:not([hidden]) ~ :not([hidden])`, v4 uses `:not(:last-child)` -- prefer `gap-*` with flex/grid
- Grid template values use underscores for spaces: `grid-cols-[max-content_auto]` (not commas)
- `shadow-sm` in v3 = `shadow-xs` in v4, `shadow` in v3 = `shadow-sm` in v4 (whole scale shifted)
- `rounded-sm` in v3 = `rounded-xs` in v4, `rounded` in v3 = `rounded-sm` in v4
- `outline-none` in v3 = `outline-hidden` in v4 (accessibility improvement)
- `ring` in v3 (3px) = `ring-3` in v4 (default is now 1px)
- Browser requirements: Safari 16.4+, Chrome 111+, Firefox 128+ (no IE11, no older browsers)

</red_flags>

---

<critical_reminders>

## ⚠️ CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@import "tailwindcss"` and `@theme` for configuration - NEVER use `tailwind.config.js`, `@tailwind base`, or `module.exports`)**

**(You MUST use `@utility` for custom utilities - NEVER use `@layer utilities {}` (v3 syntax))**

**(You MUST use oklch or CSS variable references for custom colors in `@theme` - NEVER use hex/rgb for theme tokens)**

**(You MUST use `@tailwindcss/vite` for Vite projects and `@tailwindcss/postcss` for others - NEVER use `tailwindcss` directly as PostCSS plugin)**

**(You MUST specify border colors explicitly - v4 defaults to `currentColor` not `gray-200`)**

**Failure to follow these rules will produce v3 code that does not work with Tailwind CSS v4.**

</critical_reminders>
