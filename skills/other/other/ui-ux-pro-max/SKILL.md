---
name: ui-ux-pro-max
model: fast
version: 1.1.0
description: >
  Searchable UI/UX design databases: 50+ styles, 97 palettes, 57 font pairings, 99 UX rules,
  25 chart types. CLI generates design systems from natural language. Data-driven complement to ui-design.
tags: [design, ui, ux, color, typography, style, accessibility, charts]
related: [ui-design, frontend-design, web-design]
---

# UI/UX Pro Max

Searchable design database with CLI for generating complete design systems from natural language queries.

> **See also:** `ui-design` for fundamentals and decision-making. This skill provides data-driven recommendations via CLI.

## When to Use

- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Building landing pages or dashboards
- Implementing accessibility requirements

## Rule Categories by Priority

| Priority | Category | Impact | Domain |
|----------|----------|--------|--------|
| 1 | Accessibility | CRITICAL | `ux` |
| 2 | Touch & Interaction | CRITICAL | `ux` |
| 3 | Performance | HIGH | `ux` |
| 4 | Layout & Responsive | HIGH | `ux` |
| 5 | Typography & Color | MEDIUM | `typography`, `color` |
| 6 | Animation | MEDIUM | `ux` |
| 7 | Style Selection | MEDIUM | `style`, `product` |
| 8 | Charts & Data | LOW | `chart` |

## Quick Reference

### Accessibility (CRITICAL)

- `color-contrast` — Minimum 4.5:1 ratio for normal text
- `focus-states` — Visible focus rings on interactive elements
- `alt-text` — Descriptive alt text for meaningful images
- `aria-labels` — aria-label for icon-only buttons
- `keyboard-nav` — Tab order matches visual order
- `form-labels` — Use label with for attribute

### Touch & Interaction (CRITICAL)

- `touch-target-size` — Minimum 44x44px touch targets
- `hover-vs-tap` — Use click/tap for primary interactions
- `loading-buttons` — Disable button during async operations
- `error-feedback` — Clear error messages near the problem
- `cursor-pointer` — Add cursor-pointer to clickable elements

### Performance (HIGH)

- `image-optimization` — Use WebP, srcset, lazy loading
- `reduced-motion` — Check prefers-reduced-motion
- `content-jumping` — Reserve space for async content

### Layout & Responsive (HIGH)

- `viewport-meta` — width=device-width initial-scale=1
- `readable-font-size` — Minimum 16px body text on mobile
- `horizontal-scroll` — Ensure content fits viewport width
- `z-index-management` — Define z-index scale (10, 20, 30, 50)

### Typography & Color (MEDIUM)

- `line-height` — Use 1.5-1.75 for body text
- `line-length` — Limit to 65-75 characters per line
- `font-pairing` — Match heading/body font personalities

### Animation (MEDIUM)

- `duration-timing` — Use 150-300ms for micro-interactions
- `transform-performance` — Use transform/opacity, not width/height
- `loading-states` — Skeleton screens or spinners

### Style Selection (MEDIUM)

- `style-match` — Match style to product type
- `consistency` — Use same style across all pages
- `no-emoji-icons` — Use SVG icons, not emojis

### Charts & Data (LOW)

- `chart-type` — Match chart type to data type
- `color-guidance` — Use accessible color palettes
- `data-table` — Provide table alternative for accessibility


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install ui-ux-pro-max
```


---

## Prerequisites

Python 3 is required for the search CLI.

```bash
python3 --version
```

---

## Workflow

When a user requests UI/UX work (design, build, create, implement, review, fix, improve), follow these steps.

### Step 1: Analyze Requirements

Extract from the user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page
- **Style keywords**: minimal, playful, professional, elegant, dark mode
- **Industry**: healthcare, fintech, gaming, education
- **Stack**: React, Vue, Next.js, or default to `html-tailwind`

### Step 2: Generate Design System

Always start with `--design-system` to get comprehensive recommendations:

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This searches 5 domains in parallel (product, style, color, landing, typography), applies reasoning rules from `ui-reasoning.csv`, and returns a complete design system: pattern, style, colors, typography, effects, and anti-patterns.

**Example:**

```bash
python3 scripts/search.py "beauty spa wellness service" --design-system -p "Serenity Spa"
```

### Step 2b: Persist Design System

Save the design system for hierarchical retrieval across sessions:

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

Creates:
- `design-system/MASTER.md` — Global source of truth
- `design-system/pages/` — Folder for page-specific overrides

**With page override:**

```bash
python3 scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

**Hierarchical retrieval**: When building a specific page, check `design-system/pages/<page>.md` first. If it exists, its rules override the Master file. Otherwise use `design-system/MASTER.md` exclusively.

### Step 3: Supplement with Domain Searches

After generating the design system, use domain searches for additional detail:

```bash
python3 scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

| Need | Domain | Example |
|------|--------|---------|
| More style options | `style` | `--domain style "glassmorphism dark"` |
| Chart recommendations | `chart` | `--domain chart "real-time dashboard"` |
| UX best practices | `ux` | `--domain ux "animation accessibility"` |
| Alternative fonts | `typography` | `--domain typography "elegant luxury"` |
| Landing structure | `landing` | `--domain landing "hero social-proof"` |

### Step 4: Stack Guidelines

Get implementation-specific best practices. Default to `html-tailwind` if unspecified.

```bash
python3 scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Search Reference

### Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, fintech |
| `landing` | Page structure, CTA strategies | hero, testimonial, pricing, social-proof |
| `chart` | Chart types, library recs | trend, comparison, timeline, funnel |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Stacks

| Stack | Focus |
|-------|-------|
| `html-tailwind` | Tailwind utilities, responsive, a11y (DEFAULT) |
| `react` | State, hooks, performance, patterns |
| `nextjs` | SSR, routing, images, API routes |
| `vue` | Composition API, Pinia, Vue Router |
| `svelte` | Runes, stores, SvelteKit |
| `swiftui` | Views, State, Navigation, Animation |
| `react-native` | Components, Navigation, Lists |
| `flutter` | Widgets, State, Layout, Theming |
| `shadcn` | shadcn/ui components, theming, forms |
| `jetpack-compose` | Composables, Modifiers, State Hoisting |

### Output Formats

```bash
# ASCII box (default) — best for terminal display
python3 scripts/search.py "fintech crypto" --design-system

# Markdown — best for documentation
python3 scripts/search.py "fintech crypto" --design-system -f markdown
```

---

## Example Workflow

**User request:** "Build a landing page for a professional skincare service"

**Step 1 — Analyze:** Beauty/Spa service, elegant/professional, html-tailwind default.

**Step 2 — Design system:**

```bash
python3 scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

**Step 3 — Supplement:**

```bash
python3 scripts/search.py "animation accessibility" --domain ux
python3 scripts/search.py "elegant luxury serif" --domain typography
```

**Step 4 — Stack:**

```bash
python3 scripts/search.py "layout responsive form" --stack html-tailwind
```

Then synthesize design system + detailed searches and implement.

---

## Search Tips

1. **Be specific** — "healthcare SaaS dashboard" beats "app"
2. **Search multiple times** — Different keywords reveal different insights
3. **Combine domains** — Style + Typography + Color = complete system
4. **Always check UX** — Search "animation", "z-index", "accessibility" for common issues
5. **Use the stack flag** — Get implementation-specific best practices
6. **Iterate** — If first search misses, try different keywords

---

## Common Rules for Professional UI

### Icons & Visual Elements

| Rule | Do | Don't |
|------|-----|-------|
| No emoji icons | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis as UI icons |
| Stable hover states | Use color/opacity transitions | Use scale transforms that shift layout |
| Correct brand logos | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| Consistent icon sizing | Fixed viewBox (24x24) with w-6 h-6 | Mix different icon sizes |

### Interaction & Cursor

| Rule | Do | Don't |
|------|-----|-------|
| Cursor pointer | `cursor-pointer` on all clickable elements | Leave default cursor on interactive elements |
| Hover feedback | Visual feedback (color, shadow, border) | No indication element is interactive |
| Smooth transitions | `transition-colors duration-200` | Instant changes or >500ms |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|-----|-------|
| Glass card (light) | `bg-white/80` or higher opacity | `bg-white/10` (too transparent) |
| Text contrast (light) | `#0F172A` (slate-900) for text | `#94A3B8` (slate-400) for body text |
| Muted text (light) | `#475569` (slate-600) minimum | gray-400 or lighter |
| Border visibility | `border-gray-200` in light mode | `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Don't |
|------|-----|-------|
| Floating navbar | `top-4 left-4 right-4` spacing | Stick to `top-0 left-0 right-0` |
| Content padding | Account for fixed navbar height | Let content hide behind fixed elements |
| Consistent max-width | Same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

## Pre-Delivery Checklist

### Visual Quality

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent set (Heroicons/Lucide)
- [ ] Brand logos verified (Simple Icons)
- [ ] Hover states don't cause layout shift
- [ ] Theme colors used directly (`bg-primary` not `var()` wrapper)

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are 150-300ms
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode

- [ ] Light mode text has 4.5:1 minimum contrast
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Both modes tested before delivery

### Layout

- [ ] Floating elements have proper edge spacing
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

### Accessibility

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
