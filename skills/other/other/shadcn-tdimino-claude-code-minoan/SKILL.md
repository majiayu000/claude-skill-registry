---
name: shadcn
description: >
  This skill should be used when adding shadcn/ui components, initializing shadcn
  projects, building custom registries, theming with Tailwind v4 OKLCH colors,
  or customizing installed components. Also use when working with components.json,
  presets, monorepo setup, or shadcn CLI commands. Pairs with minoan-frontend-design
  for creative direction.
argument-hint: "[component-name or command]"
---

Install, customize, and compose shadcn/ui components with design-system awareness.
shadcn is a code distribution system — components are source files you own, not packages.

## Workflow

Every shadcn interaction follows four steps: Orient, Install, Refine, Verify.

### 1. Orient

Read project state before any CLI operation. Run `npx shadcn@latest info` to get framework, installed components, aliases, icon library, and base library. Read `components.json` directly for theme config. Never guess configuration.

### 2. Install

Add components via CLI, never by copying from docs manually.

```bash
npx shadcn@latest add button card dialog    # Multiple at once
npx shadcn@latest add @namespace/component  # From custom registry
npx shadcn@latest add --dry-run button      # Preview before writing
```

Before re-adding an existing component, run `npx shadcn@latest diff <name>` to see upstream changes. Commit local customizations first — `add` overwrites files.

### 3. Refine

This is where craft lives. After every `add`, audit the component against the project's design system:

- **Typography**: Does it use the project's font variables and scale? Replace any hardcoded font sizes.
- **Color tokens**: Does it reference the project's CSS custom properties? Convert any raw color values to semantic tokens.
- **Spacing rhythm**: Does it follow the project's spacing scale? Harmonize padding and margins.
- **Border radius**: Does it use `--radius` from the theme? Shadcn sets this globally.
- **Animation**: Does it use `tw-animate-css` classes, not `tailwindcss-animate`?
- **Composition**: Create wrapper components that compose shadcn primitives. Edit base components only for structural changes.

When `minoan-frontend-design` is active, translate its creative direction into shadcn theme variables and component customizations.

### 4. Verify

Build the project to catch type errors. Visually inspect the component in context. Check dark mode. Check mobile.

## Tailwind v4 Contract

shadcn v4 uses OKLCH color space with `@theme inline` — not HSL, not `tailwind.config.ts`.

```css
:root {
  --primary: oklch(0.205 0.03 264.05);
  --primary-foreground: oklch(0.985 0 0);
}
@theme inline {
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
}
```

Leave `tailwind.config` blank in `components.json` for v4 projects. Use `data-slot` attributes for targeted styling. Use `React.ComponentProps<>` — `forwardRef` is removed.

## Theming

Colors follow `background` + `foreground` pairs. The background suffix is omitted for the primary role:
`--primary` (background), `--primary-foreground` (text on that background).

Extend with custom semantic tokens by adding both the CSS variable and the `@theme inline` mapping:
```css
:root { --warning: oklch(0.84 0.16 84); --warning-foreground: oklch(0.14 0.04 84); }
@theme inline { --color-warning: var(--warning); --color-warning-foreground: var(--warning-foreground); }
```

Use `cn()` (clsx + tailwind-merge) for all class name composition.

## References

Consult `references/` on demand:
- `cli-v4-reference.md` — Full command reference, flags, monorepo patterns. Read for any CLI operation.
- `components-json-schema.md` — Configuration schema with all fields. Read when initializing or reconfiguring.
- `theming-oklch.md` — OKLCH color system, CSS variable conventions, dark mode, custom colors. Read when theming.
- `registry-authoring.md` — Custom registry creation, namespacing, auth, item types. Read when building registries.
- `tailwind-v4-migration.md` — Breaking changes, upgrade path, tw-animate-css, data-slot. Read when migrating or troubleshooting.
- `component-inventory.md` — 59 components by category. Read when choosing what to install.
- `customization-patterns.md` — Wrapper composition, data-slot styling, diff tracking. Read when customizing components.
