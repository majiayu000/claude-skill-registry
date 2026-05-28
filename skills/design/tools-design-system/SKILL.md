---
name: tools-design-system
description: Apply the repo's current design-system contracts correctly. Use semantic tokens, DS component props, and app-level Tailwind v4 `@theme` aliases where appropriate. Avoid hardcoded colors and stale HSL-only guidance.
operating_mode: GENERATE
trigger_conditions: design tokens, semantic colors, spacing, typography, borders, shadows, Tailwind tokens, app theme aliases, arbitrary values
related_skills: tools-refactor, lp-design-spec, lp-design-qa, tools-ui-contrast-sweep
---

# Apply Design System

Use the design system that exists in the target app now, not the oldest generic theming examples in the repo.

## Source Of Truth Order

When sources disagree, use this order:

1. Existing component API contracts in the code you are editing
2. App-level token registration in the target app's `globals.css` / Tailwind v4 `@theme`
3. Theme package tokens in `packages/themes/<theme>/src/tokens.ts`
4. Shared Tailwind preset/plugin wiring
5. Older handbook examples and generic docs

For example, reception exposes utilities through `apps/reception/src/app/globals.css` using `@theme { --color-surface-2: var(--surface-2) ... }`, so classes like `bg-surface-2`, `text-muted-foreground`, and `border-border-strong` are valid even when they are not literal keys in `tokens.ts`.

## Profile-Aware Defaults

Before applying any default styling, read the design profile for the target theme at `packages/themes/<theme>/src/design-profile.ts`. Profile values are authoritative over the generic examples in this skill.

### Conditional Rules

- If `defaultElevation: "flat"` — do not add shadow classes (`shadow-sm`, `shadow-md`, `shadow-lg`) unless a page-level design spec explicitly overrides. Flat means flat.
- If `defaultElevation: "subtle"` — use `shadow-sm` only. Do not escalate to `shadow-md` or `shadow-lg` without a design spec override.
- If `defaultBorder: "none"` — do not add `border` or `border-border` classes to cards or surfaces. The brand intentionally uses borderless containers.
- If `defaultBorder: "subtle"` — use `border-border-muted`, not `border-border-strong`.
- If `defaultRadius: "sm"` — use `rounded-sm`, not `rounded-lg`. The brand uses small corners.
- If `defaultRadius: "none"` — use `rounded-none`. The brand uses sharp edges.
- If `defaultRadius: "xl"` — use `rounded-xl`. The brand uses large, soft corners.
- If `colorStrategy: "monochromatic"` — do not use accent token (`bg-accent`, `text-accent-fg`). Stick to primary + neutrals only.
- If `colorStrategy: "restrained"` — use accent sparingly (CTAs and 1-2 highlights per page maximum).

**General rule:** Read the design profile before applying any default. The profile is more specific than the examples below and takes precedence when they conflict.

### Theme Asset Awareness

Before recommending specific token classes, check `packages/themes/<theme>/src/assets.ts` for available theme assets:

- **Fonts:** If `assets.fonts.heading` is defined, use that font family for headings instead of defaulting to `font-sans`. If no heading font is defined, `font-heading` or `font-sans` remains correct.
- **Gradients:** If `assets.gradients` defines named gradients (e.g., `hero`, `header`), these are available via CSS custom properties. Reference them rather than composing ad-hoc gradient values.
- **Shadows:** If `assets.shadows` defines brand-colored shadows (e.g., `brandPrimary10`), prefer them over generic `shadow-sm`/`shadow-md` for branded surfaces.
- **Keyframes:** If `assets.keyframes` defines animations (e.g., `fade-up`, `slide-down`), use them for motion instead of inventing new keyframes.
- **Brand colors:** If `assets.brandColors` defines named colors beyond the semantic palette, they are available as CSS custom properties for brand-specific use cases.

If `assets.ts` does not exist or exports empty collections, the brand has no custom assets. Use base tokens as documented below.

## Core Rules

- Prefer public DS component props over class-level restyling when the component already exposes the contract.
- Prefer semantic utility classes over raw color values.
- Prefer app/theme token aliases over ad hoc component-local CSS variables.
- Do not edit generated token artifacts directly.
- Do not assume every `hsl(var(--...))` pattern is valid in JSX utility classes; check whether the app already exposes a semantic alias first.

## Component Contracts First

Before adding classes, check whether the primitive already exposes the right contract.

Common current contracts:

- `Button`, `Tag`, `Chip`, similar action/status primitives:
  - `color="primary|accent|success|info|warning|danger"`
  - `tone="solid|soft|outline|ghost|quiet"`
  - `size="sm|md|lg"`
- Core primitives and surfaces may expose:
  - `shape="square|soft|pill"`
  - `radius="none|xs|sm|md|lg|xl|2xl|3xl|4xl|full"`

Use those props before hardcoding `rounded-*`, `bg-*`, or size classes in reusable components.

## Token Plumbing Model

This repo currently has two valid token-consumption paths:

### 1. Shared preset/plugin utilities

Many apps rely on shared semantic utilities such as:

- Backgrounds: `bg-bg`, `bg-primary`, `bg-accent`, `bg-muted`, `bg-panel`, `bg-surface`
- Text: `text-fg`, `text-primary-fg`, `text-muted-foreground`
- Borders: `border-border`, `border-input`, `ring-ring`

These are commonly wired through shared Tailwind config/plugin layers that still use `hsl(var(--...))` under the hood.

### 2. App-level Tailwind v4 `@theme` aliases

Some apps, including reception, register additional semantic aliases in app `globals.css`.

Examples of valid app-level utilities:

- `bg-surface-2`
- `bg-surface-3`
- `text-foreground`
- `text-muted-foreground`
- `border-border`
- `border-border-strong`
- `bg-input`

When working in an app with `@theme`, treat those aliases as first-class utilities.

## Color Guidance

Prefer these kinds of semantic utilities:

- Backgrounds:
  - `bg-bg`
  - `bg-panel`
  - `bg-surface`
  - `bg-surface-2`
  - `bg-surface-3`
  - `bg-primary`
  - `bg-primary-soft`
  - `bg-accent`
  - `bg-muted`
- Text:
  - `text-fg`
  - `text-foreground`
  - `text-muted-foreground`
  - `text-primary-fg`
  - `text-primary-foreground` when that alias already exists in the target app
- Borders/rings:
  - `border-border`
  - `border-border-strong`
  - `border-border-muted`
  - `ring-ring`

Use opacity modifiers when they are part of a semantic class, for example:

- `bg-primary/90`
- `bg-surface-2/60`
- `text-foreground/80`

Those are not the same thing as hardcoded colors.

## Spacing, Radius, Shadow, Typography

Prefer the repo scales:

- Spacing: `0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16`
- Radius: `rounded-none|xs|sm|md|lg|xl|2xl|3xl|4xl|full`
- Shadow: `shadow-sm|md|lg`
- Typography:
  - sizes: `text-xs|sm|base|lg|xl|2xl|3xl|4xl`
  - weights: `font-normal|medium|semibold|bold`
  - families: `font-sans|heading|mono`

If a primitive already exposes `size`, `shape`, or `radius`, use the prop instead of duplicating the class at call sites.

## Common Patterns

Prefer patterns like:

```tsx
<div className="rounded-lg border border-border bg-surface text-foreground shadow-sm p-6" />
```

```tsx
<div className="rounded-lg border border-border-strong bg-surface-2 text-foreground shadow-lg" />
```

```tsx
<Button color="primary" tone="solid" size="lg">Save</Button>
```

```tsx
<Input className="bg-input text-foreground" />
```

## Bracket Syntax: Allowed Vs Not Allowed

Do not treat all bracket syntax as invalid.

Usually acceptable:

- `data-[state=open]:...`
- `aria-[selected=true]:...`
- valid layout values with no DS utility equivalent, such as viewport-safe units
- targeted selectors needed to style DS primitives when no prop/API exists

Usually not acceptable:

- `bg-[#ff0000]`
- `text-[rgb(255,0,0)]`
- `border-[oklch(...)]` in component JSX when a semantic token should exist
- arbitrary spacing/sizing when the repo scale already covers it

## When Tokens Do Not Exist

Use the narrowest correct layer.

1. Reuse an existing semantic utility if one already expresses the intent.
2. If the app needs a new alias for an existing theme token, add it in the target app's `globals.css` `@theme` block.
3. If the theme truly needs a new semantic token value, add it in `packages/themes/<theme>/src/tokens.ts`.
4. Regenerate any derived artifacts when the theme pipeline requires it.
5. Only update shared token/preset layers when the token is genuinely cross-app design-system surface area.

Do not jump straight to `packages/design-tokens/` or Tailwind config for app-local needs.

## Anti-Patterns

- Hardcoded hex/RGB/HSL/OKLCH colors in component JSX
- Default Tailwind palette classes such as `bg-red-500`
- Editing generated `tokens.css` directly
- Replacing DS component props with local class hacks in reusable primitives
- Assuming handbook examples are authoritative when the target app's `globals.css` and current components say otherwise

## Quick Checks Before Editing

- Which app am I in?
- Does this app expose extra semantic aliases in `globals.css`?
- Does the component already expose `color`, `tone`, `size`, `shape`, or `radius`?
- Is this a theme-token change, an app-alias change, or just a component usage change?
- Am I about to introduce a raw value where a semantic token already exists?

## Integration

This skill is a supporting reference, not a pipeline stage.

- **Role:** Current-state design-system guidance for token usage, DS component contracts, and app-level alias handling.
- **Consumers:** `lp-design-spec`, `tools-ui-frontend-design`, `lp-design-qa`, `tools-refactor`, and UI implementation/review work generally.
- **Not a pipeline stage:** consult it when UI work touches tokens, classes, component props, or design-system contract decisions.
