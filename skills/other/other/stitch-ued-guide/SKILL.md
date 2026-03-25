---
name: stitch-ued-guide
description: Visual vocabulary, design terminology, and prompt engineering strategy for Stitch. Reference this when you need layout pattern names, aesthetic style terms, color structure formulas, or device guidelines.
allowed-tools: []
---

# Stitch UED Guide

This is a reference guide, not an action skill. Use it when:
- You need specific design terminology for a Stitch prompt (masonry, glassmorphism, split-screen)
- You're unsure how to describe a layout pattern or visual style
- You want to apply color + theme structure consistently
- You need to know device-specific constraints for prompt writing

## Prompt engineering strategy

The most effective Stitch prompts follow this 4-part structure:

```
[Context & Style] + [Layout Structure] + [Component Details] + [Content & Data]
```

**Context & Style:**
> "Mobile fitness app for gym-goers. Dark mode with neon green accents. Cyberpunk aesthetic. Rounded corners."

**Layout Structure:**
> "Bottom navigation bar (Home, Workout, Progress, Profile). Scrollable main feed. Sticky top bar with greeting."

**Component Details:**
> "Workout cards with gradient border, thumbnail, title, duration badge, and 'Start' pill button."

**Content & Data:**
> "Sample data: 'Upper Body Blast' (45 min), 'Core Destroyer' (20 min), 'Morning Run' (30 min, completed today)."

## Stitch model selection

| Model | When to use |
|-------|-------------|
| `GEMINI_3_1_PRO` | High-fidelity designs, complex layouts, when quality matters — **recommended default** |
| `GEMINI_3_FLASH` | Fast iteration, wireframes, rapid exploration, when speed matters |
| `GEMINI_3_PRO` | **Deprecated** — still works but will be removed. Use `GEMINI_3_1_PRO` instead |

## Color variant reference (colorVariant)

Controls how Stitch derives the full color palette from your `primaryColor`:

| colorVariant | Visual effect | Best for |
|---|---|---|
| `MONOCHROME` | Single-hue, editorial feel | Luxury, minimal, text-heavy, portfolios |
| `NEUTRAL` | Subdued, professional | Corporate, enterprise, medical |
| `TONAL_SPOT` | Balanced accent spots on neutral base | SaaS, productivity, dashboards |
| `VIBRANT` | Bold, energetic colors | Consumer apps, social, food |
| `EXPRESSIVE` | Multicolor, dynamic | Creative, gaming, entertainment |
| `FIDELITY` | Precise brand color matching | Brand-heavy, marketing, landing pages |
| `CONTENT` | Palette adapts to content | Media, editorial, photo-heavy |
| `RAINBOW` | Full spectrum | Kids apps, events, playful |
| `FRUIT_SALAD` | Warm multicolor | Food, lifestyle, wellness |

## Spacing scale reference (spacingScale)

| spacingScale | Effect | Best for |
|---|---|---|
| 0 | Minimal spacing — very tight, data-dense | Admin panels, data tables, terminal-style UIs |
| 1 | Compact — efficient use of space | Dashboards, dense mobile lists, SaaS tools |
| 2 | Normal — comfortable breathing room | Standard apps, consumer products |
| 3 | Spacious — generous whitespace | Landing pages, marketing, portfolios, luxury |

## DesignTheme API field reference

Quick reference for all DesignTheme fields returned by `get_project`:

| Field | Type | Description |
|---|---|---|
| `colorMode` | LIGHT / DARK | Base theme mode |
| `customColor` | hex string | Seed color for palette generation |
| `colorVariant` | enum (9 values) | How palette is derived from seed |
| `headlineFont` | font enum (28 values) | Display/headline typeface |
| `bodyFont` | font enum | Body text typeface |
| `labelFont` | font enum | Labels, captions, metadata typeface |
| `font` | font enum | **Deprecated** — use headlineFont/bodyFont/labelFont |
| `roundness` | ROUND_FOUR/EIGHT/TWELVE/FULL | Corner radius preset |
| `spacingScale` | integer 0-3 | Layout density |
| `namedColors` | object (40+ tokens) | Full semantic color map (Material 3) |
| `designMd` | string | Auto-generated design system markdown |
| `description` | string | Brief aesthetic description |
| `overridePrimaryColor` | hex | Explicit primary override |
| `overrideSecondaryColor` | hex | Explicit secondary override |
| `overrideTertiaryColor` | hex | Explicit tertiary override |
| `overrideNeutralColor` | hex | Explicit neutral base override |
| `backgroundLight` | hex | Light mode background |
| `backgroundDark` | hex | Dark mode background |

## Layout patterns

### Mobile patterns
- **Vertical scroll feed** — infinite scroll of content cards, sticky header, bottom nav
- **Tab navigation** — segmented control or tab bar, content switches inline
- **Bottom sheet** — slide-up panel for secondary content or actions
- **Full-screen form** — single-column, large touch targets, sticky submit
- **Detail → action** — hero content at top, description below, sticky CTA at bottom

### Desktop patterns
- **Left sidebar + main** — persistent side nav (200-280px), main content area, top bar
- **Top nav + content** — horizontal navigation bar, sectioned main content below
- **Split screen** — two equal halves (form/preview, signup/product screenshot)
- **Dashboard grid** — KPI strip, charts, tables, widgets in responsive grid
- **Landing page** — full-width hero, feature sections, pricing, footer CTA

### Universal patterns
- **Masonry grid** — variable-height cards, Pinterest-style layout
- **Bento grid** — asymmetric boxes of varying sizes, each containing different content
- **Hero section** — full-width/height with background image, headline, CTA
- **Card grid** — uniform cards in responsive column grid

## Visual styles

| Style | Description | Use for |
|-------|-------------|---------|
| **Flat** | No shadows, bold colors, simple shapes | Mobile apps, illustrations |
| **Material** | Cards with elevation, clear hierarchy, ripple effects | Android-style apps |
| **Neumorphism** | Extruded elements on same-color bg, soft shadows | Luxury, subtle UIs |
| **Glassmorphism** | Frosted glass effect, blur + transparency + border | Modern SaaS, overlays |
| **Brutalism** | Raw, high-contrast, purposefully rough, grid-breaking | Editorial, bold brands |
| **Minimalism** | Maximum whitespace, single accent color, typographic focus | Portfolios, landing pages |
| **Cyberpunk** | Dark bg, neon accents, glitch elements, monospace fonts | Gaming, tech, dark mode |

## Color structure formula

For consistent, professional palettes in prompts:

```
[Domain/mood description] + [Background hex] + [Primary hex] + [Secondary hex] + [Text hex] + [Aesthetic mood]
```

**Example:**
> "Modern SaaS productivity app. Slate-50 (#F8FAFC) background. Indigo (#6366F1) primary. Violet (#8B5CF6) secondary. Zinc-900 (#18181B) text. Clean, structured, professional."

**Dark mode example:**
> "Premium dark dashboard. Zinc-900 (#18181B) background. Indigo-400 (#818CF8) primary on dark. Zinc-800 (#27272A) card surface. Zinc-100 (#F4F4F5) text. Focused, high-contrast, developer-friendly."

## Device guidelines

| Device | Dimensions | Key constraints |
|--------|-----------|-----------------|
| **MOBILE** | ~375px wide | Bottom navigation, thumb-friendly tap targets (44px min), single-column layouts, larger type |
| **DESKTOP** | ~1440px wide | Multi-column layouts, sidebar navigation, dense data tables, hover interactions |
| **TABLET** | ~768-1024px | Hybrid: 2-column grids, collapsible sidebar, touch-friendly but more space |
| **AGNOSTIC** | Fluid | Responsive/fluid layout — not tied to a specific device, adapts to viewport |

## Accessibility in prompts

Include these phrases in prompts to guide Stitch toward accessible output:
- "High contrast text, WCAG AA compliant colors"
- "Touch-friendly tap targets, minimum 44px height"
- "Clear visual hierarchy, strong heading sizes"
- "Sufficient color contrast between text and background"

## Quick reference — UI component names for Stitch prompts

Use these precise names (vague descriptions produce worse results):

- "Floating action button (FAB)" not "button in corner"
- "Segmented control" not "toggle group"
- "Bottom sheet" not "popup from bottom"
- "Skeleton loader" not "loading placeholder"
- "Snackbar" not "notification at bottom"
- "Breadcrumb trail" not "navigation path"
- "Stepper / wizard" not "multi-step form indicator"
- "Data table with sortable columns" not "list of data"
- "Autocomplete input" not "search with suggestions"

## Related skills

- `stitch-ui-design-spec-generator` — produces the structured JSON this guide helps you describe
- `stitch-ui-prompt-architect` — applies this vocabulary to build final Stitch prompts
