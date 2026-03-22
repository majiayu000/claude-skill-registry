---
name: uiux
description: Dashboard design system — colors, typography, spacing, components, and visual patterns for the session dashboard UI.
user-invocable: false
---

# Dashboard Design System

## Theme

Dark theme dashboard with warm gray tones and terracotta brand accent, optimized for developer tooling and data visualization.

## Tailwind Theme

Uses Tailwind CSS v4 with CSS-first config (`@import 'tailwindcss'` in `app.css`).

Custom `@theme` block overrides default cool grays with warm grays and adds a `brand-*` terracotta accent scale.

### Colors

#### Warm Gray Scale (overrides Tailwind defaults)

| Token | Hex | Usage |
|-------|-----|-------|
| `gray-950` | `#141413` | Body/page background |
| `gray-900` | `#1c1c1a` | Card/panel background (with `/50` opacity) |
| `gray-800` | `#2a2926` | Borders, dividers |
| `gray-700` | `#3d3b36` | Subtle fills, inactive bars |
| `gray-600` | `#565349` | Disabled states |
| `gray-500` | `#7a7668` | Muted text, timestamps, labels |
| `gray-400` | `#a39e90` | Secondary text, descriptions |
| `gray-300` | `#cdc8b8` | Headings, panel titles |
| `gray-100` | `#eae6dc` | Primary text |
| `white` | | Emphasis text, hero numbers |

#### Brand Accent (terracotta)

| Token | Hex | Usage |
|-------|-----|-------|
| `brand-300` | `#f0b8a0` | Light accent text |
| `brand-400` | `#e09070` | Links, input tokens, active elements |
| `brand-500` | `#d97757` | Primary accent, tab indicators, logo highlight |
| `brand-600` | `#c4643f` | Buttons, toggles |
| `brand-700` | `#a8512e` | Dark accent |

#### Semantic Colors (unchanged)

| Token | Usage |
|-------|-------|
| `emerald-400` | Success / output tokens |
| `amber-400` / `amber-500` | Warning / cache tokens |
| `purple-400` / `purple-500` | Cache creation, system overhead |
| `red-400` | Error messages, limits |

### Data Visualization Colors

| Category | Color |
|----------|-------|
| Primary / Messages | `brand-500` (`#d97757`) |
| Input tokens | `brand-400` (`#e09070`) |
| Output tokens | `emerald-400` |
| Cache read | `amber-400` |
| Cache creation | `purple-400` |
| System overhead | `purple-500` |
| Free space | `gray-700` |

#### Chart COLORS Array

```ts
const COLORS = ['#d97757', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#b07cc5']
```

#### Heatmap Intensity Scale

```ts
const INTENSITY_COLORS = ['#2a2926', '#3d2a1e', '#a8512eb3', '#d97757cc', '#e09070']
```

#### Tooltip Styling

```ts
{ backgroundColor: '#1c1c1a', border: '1px solid #3d3b36' }
```

#### Grid/Tick Colors

- Grid stroke: `#2a2926`
- Tick fill: `#7a7668`

## Component Patterns

| Component | Classes |
|-----------|---------|
| Panel/Card | `rounded-xl border border-gray-800 bg-gray-900/50 p-4` |
| Panel title | `text-sm font-semibold text-gray-300` |
| Hero number | `text-2xl font-bold text-white` |
| Subtitle | `text-[10px] text-gray-500` |
| Label | `text-xs text-gray-400` |
| Mono value | `text-xs font-mono text-gray-300` |
| Badge | `rounded bg-gray-800 px-1.5 py-0.5 text-[10px] font-mono text-gray-400` |
| Bar track | `h-2 rounded-full bg-gray-800 overflow-hidden` |
| Link | `text-sm text-brand-400 hover:underline` |
| Muted link | `text-xs text-gray-500 hover:text-gray-300` |
| Active button | `bg-brand-600 text-white hover:bg-brand-500` |
| Focus ring | `focus:border-brand-500 focus:ring-brand-500` |
| Active tab | `border-brand-500 text-white` |
| Toggle on | `bg-brand-600` |

## Layout

- 2-column grid at `md:` breakpoint for stat panels
- Full-width panels for timeline, agents, tasks
- Consistent `gap-4` between grid items
- `mt-6` between major page sections
- `space-y-2` for list items within panels

## Header & Navigation

- Logo: `<span className="text-brand-500">Claude</span> Dashboard`
- Nav icons: inline SVG icons (16x16) instead of ASCII characters
- Footer: GitHub + npm icon links with `text-gray-500 hover:text-gray-300`

## Favicon

- SVG terminal prompt icon at `public/favicon.svg`
- Uses brand color `#d97757`
- Meta theme-color: `#141413` (matches `gray-950`)

## Typography

- Font: system monospace for values, default sans for labels
- Never use font weights heavier than `font-bold`
- Use `font-mono` for numeric values, IDs, model names
- Token counts formatted with K/M suffixes (e.g., `29.5K`, `8.3M`)

## Visual Rules

1. **Dark-first** -- all backgrounds are dark warm gray, text is light
2. **Subtle borders** -- `border-gray-800` only, no shadows
3. **Rounded panels** -- `rounded-xl` for cards, `rounded-full` for bars/badges
4. **Opacity for bars** -- colored bar segments use `opacity-60`
5. **Compact density** -- small text sizes (`text-xs`, `text-[10px]`), tight spacing
6. **Recharts styling** -- dark tooltips (`bg-gray-800`), no grid lines, subtle reference lines
7. **Brand accent** -- use `brand-*` (terracotta) instead of `blue-*` for all interactive/accent elements
