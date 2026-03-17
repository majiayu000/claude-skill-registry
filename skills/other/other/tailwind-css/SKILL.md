---
name: tailwind-css
user-invocable: false
description: This skill should be used when the user asks to "style with Tailwind", "add Tailwind classes", "fix Tailwind styles", "use tailwind-variants", "add animations with tw-animate-css", "configure Tailwind v4", "migrate to Tailwind v4", or mentions Tailwind utilities, CSS classes, responsive design, dark mode, gradients, design tokens, or CSS Modules.
---

# Tailwind CSS v4

Expert guidance for Tailwind CSS v4, CSS-first configuration, modern utility patterns, and type-safe component styling with tailwind-variants.

## CSS-First Configuration

Tailwind CSS v4 eliminates `tailwind.config.ts` in favor of CSS-only configuration. All configuration lives in CSS files using special directives.

**Core Directives:**

- `@import "tailwindcss"` - Entry point that loads Tailwind
- `@theme { }` - Define or extend design tokens
- `@theme static { }` - Define tokens that should not generate utilities
- `@utility` - Create custom utilities
- `@custom-variant` - Define custom variants

**Minimal Example:**

```css
@import "tailwindcss";

@theme {
  --color-brand: oklch(0.72 0.11 178);
  --font-display: "Inter", sans-serif;
  --spacing-edge: 1.5rem;
}
```

All theme tokens defined with `@theme` automatically become available as utility classes. For example, `--color-brand` can be used as `bg-brand`, `text-brand`, `border-brand`, etc.

## ESLint Integration

Use `eslint-plugin-better-tailwindcss` for Tailwind CSS v4 class validation and style enforcement.

**Correctness Rules (errors):**

- `no-conflicting-classes` - Detect classes that override each other
- `no-unknown-classes` - Flag classes not registered with Tailwind

**Stylistic Rules (warnings):**

- `enforce-canonical-classes` - Use standard v4 class names
- `enforce-shorthand-classes` - Use abbreviated class versions
- `no-deprecated-classes` - Remove outdated class names
- `no-duplicate-classes` - Eliminate redundant declarations
- `no-unnecessary-whitespace` - Clean up extra spacing

**Examples:**

```typescript
// ❌ Bad: separate padding
<div className="px-6 py-6">

// ✅ Good: shorthand
<div className="p-6">
```

```typescript
// ❌ Bad: separate width/height
<div className="w-6 h-6">

// ✅ Good: size utility
<div className="size-6">
```

Run the project's ESLint check after modifying Tailwind classes to validate all changes across the codebase.

## Coding Preferences

### Layout and Spacing

**Use `gap` for flex/grid spacing, not `space-x`/`space-y`:**

The `gap` utilities handle wrapping correctly, while `space-*` utilities break when flex/grid items wrap to multiple lines.

```typescript
// ✅ Good: gap handles wrapping
<div className="flex gap-4">

// ❌ Bad: breaks when items wrap
<div className="flex space-x-4">
```

**Prefer `size-*` over separate `w-*`/`h-*` for equal dimensions:**

```typescript
// ✅ Good: concise
<div className="size-16">

// ❌ Bad: redundant
<div className="w-16 h-16">
```

**Always use `min-h-dvh` instead of `min-h-screen`:**

Dynamic viewport height (`dvh`) accounts for mobile browser chrome, while `vh` units ignore it and cause layout issues on mobile Safari.

```typescript
// ✅ Good: works on mobile Safari
<main className="min-h-dvh">

// ❌ Bad: buggy on mobile Safari
<main className="min-h-screen">
```

**Prefer top/left margins over bottom/right:**

Consistent directionality improves layout predictability.

```typescript
// ✅ Good: top margin
<div className="mt-4">

// ❌ Avoid: bottom margin (unless needed)
<div className="mb-4">
```

**Use padding on parent containers instead of bottom margins on last child:**

Padding provides consistent spacing without needing `:last-child` selectors.

```typescript
// ✅ Good: padding on parent
<section className="pb-8">
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
</section>

// ❌ Avoid: margin on children
<section>
  <div className="mb-4">Item 1</div>
  <div className="mb-4">Item 2</div>
  <div>Item 3</div>
</section>
```

**For max-widths, prefer container scale over pixel values:**

```typescript
// ✅ Good: semantic container size
<div className="max-w-2xl">

// ❌ Avoid: arbitrary pixel value
<div className="max-w-[672px]">
```

### Typography

**Avoid `leading-*` classes; use line height modifiers:**

Tailwind v4 supports inline line height modifiers with the `text-{size}/{leading}` syntax.

```typescript
// ✅ Good: combined size and line height
<p className="text-base/7">

// ❌ Bad: separate utilities
<p className="text-base leading-7">
```

**Font Size Reference:**

| Class       | Size |
| ----------- | ---- |
| `text-xs`   | 12px |
| `text-sm`   | 14px |
| `text-base` | 16px |
| `text-lg`   | 18px |
| `text-xl`   | 20px |

### Colors and Opacity

**Use opacity modifier syntax, not separate opacity utilities:**

All `*-opacity-*` utilities were removed in Tailwind v4. Use the modifier syntax instead.

```typescript
// ✅ Good: opacity modifier
<div className="bg-red-500/60">

// ❌ Bad: removed in v4
<div className="bg-red-500 bg-opacity-60">
```

**Prefer design tokens over arbitrary hex values:**

Check the project's `@theme` configuration before using arbitrary color values.

```typescript
// ✅ Good: theme token
<div className="bg-brand">

// ❌ Avoid: arbitrary hex (check theme first)
<div className="bg-[#4f46e5]">
```

### Border Radius

Tailwind v4 renamed border radius utilities:

| v3           | v4 (equivalent) | Size |
| ------------ | --------------- | ---- |
| `rounded-sm` | `rounded-xs`    | 2px  |
| `rounded`    | `rounded-sm`    | 4px  |
| `rounded-md` | `rounded`       | 6px  |
| `rounded-lg` | `rounded-md`    | 8px  |

Use the v4 names when writing new code.

### Gradients

Tailwind v4 renamed gradient utilities and added new gradient types.

**Use `bg-linear-*`, not `bg-gradient-*`:**

```typescript
// ✅ Good: v4 syntax
<div className="bg-linear-to-r from-blue-500 to-purple-500">

// ❌ Bad: removed in v4
<div className="bg-gradient-to-r from-blue-500 to-purple-500">
```

**New gradient types:**

- `bg-radial` - Radial gradients
- `bg-conic` - Conic gradients

**Example:**

```typescript
<div className="bg-radial from-blue-500 to-purple-500">
<div className="bg-conic from-red-500 via-yellow-500 to-green-500">
```

### Arbitrary Values

**Always prefer Tailwind's predefined scale:**

Check the project's `@theme` configuration for available tokens before using arbitrary values.

```typescript
// ✅ Good: predefined scale
<div className="ml-4">

// ❌ Avoid: arbitrary pixel value
<div className="ml-[16px]">
```

**General rule:** Prefer sizing scale over pixel values. Three similar lines of code is better than a premature abstraction.

### Class Merging

The common pattern is a `cn` utility combining `clsx` + `tailwind-merge`.

**Use `cn` for:**

- Static constants: `const CARD_BASE = cn("fixed classes")`
- Conditional classes: `cn("base", condition && "conditional")`
- Dynamic merging: `cn(baseClasses, className)`
- Conflict resolution: `cn("p-4", "p-6")` → `"p-6"`

**Do NOT use `cn` for:**

- Static strings in `className` attributes: `className="fixed classes"`

**Examples:**

```typescript
// ✅ Good: static string in className
<button className="rounded-lg px-4 py-2 font-medium bg-blue-600">

// ✅ Good: static constant with cn
const CARD_BASE = cn("rounded-lg border border-gray-300 p-4");
<div className={CARD_BASE} />

// ✅ Good: conditional with cn
<button className={cn(
  "rounded-lg px-4 py-2 font-medium",
  isActive ? "bg-blue-600" : "bg-gray-700",
  disabled && "opacity-50"
)} />

// ❌ Bad: unnecessary cn for static className attribute
<button className={cn("rounded-lg px-4 py-2 font-medium")} />
```

### Image Sizing

Use Tailwind size classes instead of pixel values for `Image` components.

```typescript
// ✅ Good: Tailwind units
<Image src={src} alt={alt} className="size-16" />
<Image src={src} alt={alt} className="w-24 h-auto" />

// ❌ Bad: pixel values
<Image src={src} alt={alt} width={64} height={64} />
```

### Z-Index

Define z-index values as CSS custom properties in `@theme`, then reference them with the `z-(--z-*)` syntax.

**Never use arbitrary z-index numbers:**

```typescript
// ✅ Good: theme z-index value
<div className="z-(--z-modal)">
<div className="z-(--z-sticky)">

// ❌ Bad: arbitrary z-index numbers
<div className="z-[100]">
<div className="z-[9999]">
```

**Define z-index tokens in CSS:**

```css
@theme {
  --z-base: 0;
  --z-sticky: 10;
  --z-modal: 100;
  --z-tooltip: 1000;
}
```

### Dark Mode

Use the plain `dark:` variant for dark mode styles.

**Pattern:**

Write light mode styles first, then add dark mode overrides.

```typescript
// ✅ Good: light mode first, then dark override
<div className="bg-white text-gray-900 dark:bg-gray-900 dark:text-white">

// ❌ Avoid: dark mode first (less readable)
<div className="dark:bg-gray-900 dark:text-white bg-white text-gray-900">
```

## CSS Modules

Use CSS Modules only as a last resort for complex CSS that cannot be easily written with Tailwind classes.

All `.module.css` files must include `@reference "#tailwind";` at the top to enable Tailwind utilities and theme tokens inside the module.

**Example:**

```css
/* component.module.css */
@reference "#tailwind";

.component {
  /* Complex CSS that can't be expressed with Tailwind utilities */
  /* Can still use Tailwind utilities and theme tokens */
}
```

## Common Tasks

### Adding a Component with Variants

1. Read `references/tailwind-variants.md` for patterns
2. Check the project's `@theme` configuration for available tokens
3. Use `tv()` from `tailwind-variants` for type-safe variants

**Example:**

```typescript
import { tv } from "tailwind-variants";

const button = tv({
  base: "rounded-lg px-4 py-2 font-medium",
  variants: {
    color: {
      primary: "bg-blue-600 text-white",
      secondary: "bg-gray-600 text-white",
    },
    size: {
      sm: "text-sm",
      md: "text-base",
      lg: "text-lg",
    },
  },
});
```

### Debugging Styles

1. Check `references/tailwind-v4-rules.md` for breaking changes
2. Verify gradient syntax (`bg-linear-*`, not `bg-gradient-*`)
3. Verify CSS variable syntax (`bg-my-color`, not `bg-[--var-my-color]`)
4. Check if arbitrary value exists in the project's `@theme` configuration

### Working with Colors

1. Check the project's `@theme` configuration first to see available colors
2. Use semantic color names when available
3. Use opacity modifiers for transparency (`/20`, `/50`, etc.)
4. Avoid arbitrary colors unless absolutely necessary

**Example:**

```typescript
// ✅ Good: theme token with opacity
<div className="bg-brand/20 text-brand">

// ❌ Avoid: arbitrary hex
<div className="bg-[#4f46e5]/20 text-[#4f46e5]">
```

### Adding Animations

1. Read `references/tw-animate-css.md` for available animations
2. Combine a base class (`animate-in` or `animate-out`) with effect classes
3. Note decimal spacing gotcha: use `[0.625rem]` syntax, not `2.5`

**Example:**

```typescript
// Enter: fade + slide up
<div className="fade-in slide-in-from-bottom-4 duration-300 animate-in">

// Exit: fade + slide down
<div className="fade-out slide-out-to-bottom-4 duration-200 animate-out">
```

## Quick Reference Table

| Aspect             | Pattern                                           |
| ------------------ | ------------------------------------------------- |
| Configuration      | CSS-only: `@theme`, `@utility`, `@custom-variant` |
| Gradients          | `bg-linear-*`, `bg-radial`, `bg-conic`            |
| Opacity            | Modifier syntax: `bg-black/50`                    |
| Line Height        | Modifier syntax: `text-base/7`                    |
| Font Features      | `font-features-zero`, `font-features-ss01`, etc.  |
| CSS Variables      | `bg-my-color` (auto-created from `@theme`)        |
| CSS Modules        | `@reference "#tailwind";` at top                  |
| Class Merging      | `cn()` for conditionals; plain string for static  |
| Viewport           | `min-h-dvh` (not `min-h-screen`)                  |
| Component Variants | `references/tailwind-variants.md`                 |
| Animations         | `references/tw-animate-css.md`                    |
| V4 Rules           | `references/tailwind-v4-rules.md`                 |

## Reference Documentation

- **Tailwind v4 Rules & Best Practices:** `references/tailwind-v4-rules.md` — Breaking changes, removed/renamed utilities, layout rules, typography, gradients, CSS variables, new v4 features, common pitfalls
- **tailwind-variants Patterns:** `references/tailwind-variants.md` — Component variants, slots API, composition, TypeScript integration, responsive variants
- **tw-animate-css Reference:** `references/tw-animate-css.md` — Enter/exit animations, slide/fade/zoom utilities, spacing gotchas
