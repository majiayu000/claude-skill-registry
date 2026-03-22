---
name: tools-ui-frontend-design
description: Create distinctive, production-grade frontend interfaces grounded in this repo's design system. Use when asked to build web components, pages, or applications. Combines bold creative direction with token-constrained implementation.
operating_mode: GENERATE
trigger_conditions: build UI, web components, pages, frontend interface, design system implementation, production UI, React components
related_skills: tools-design-system, lp-design-spec, lp-design-qa, tools-bos-design-page
---

# Frontend Design

Build distinctive UI that is both creatively intentional and design-system-compliant.

This skill bridges the Claude `frontend-design` plugin's creative philosophy with this repo's concrete design token system, brand language, and component library. The plugin provides the "think boldly" mindset; this skill constrains it to the actual design system.

## Philosophy (from the Claude frontend-design plugin)

- Commit to a BOLD aesthetic direction before coding
- Avoid generic AI aesthetics (purple gradients, Inter/Roboto, predictable grid layouts)
- Every design choice should be intentional and defensible
- High-impact micro-interactions and motion where they serve the user
- Atmosphere and depth through composition, not through arbitrary values

## Constraints (this repo's design system)

ALL design work MUST use the repo's token system. The tokens and brand dossier define the creative canvas — boldness comes from HOW you compose them, not from bypassing them.

### Mandatory References

Load these before any design work:

| What | Where | Load when |
|------|-------|-----------|
| Token quick-ref | `.claude/skills/tools-design-system/SKILL.md` | Always — first thing |
| Brand dossier | `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md` | If it exists for the business |
| Design profile | `packages/themes/<theme>/src/design-profile.ts` | Before any themed surface |
| Theme assets | `packages/themes/<theme>/src/assets.ts` | Before any themed surface |
| Recipes | `packages/themes/<theme>/src/recipes.ts` | Before any themed surface |
| Theme tokens | `packages/themes/<theme>/src/tokens.ts` | Before any design |
| Base tokens | `packages/themes/base/src/tokens.ts` | Always (fallback + reference) |
| Component catalog | `docs/design-system-handbook.md` | When composing layouts |
| Typography & color | `docs/typography-and-color.md` | When choosing fonts/colors |
| Business registry | `docs/business-os/strategy/businesses.json` | To resolve app → business |

### Hard Rules

1. ALL colors via semantic tokens (`bg-primary`, `text-fg`, `bg-accent`, etc.) or theme asset brand colors — never arbitrary hex
2. ALL typography via theme asset fonts (from `assets.ts`) or font tokens (`font-sans`, `font-heading`, `font-mono`) — never import external fonts
3. ALL spacing via profile-derived gaps (`sectionGap`, `componentGap`, `cardPadding` from `design-profile.ts`) or 8-pt rhythm — never arbitrary px
4. ALL radius via profile `defaultRadius` (e.g., `rounded-sm` when profile says `"sm"`) — never arbitrary. Do not default to `rounded-lg` when the profile specifies a different value
5. ALL shadows via profile `defaultElevation` — use `shadow-sm` for `"subtle"`, no shadow for `"flat"`, `shadow-md` for `"moderate"`. Do not default to `shadow-md` when the profile says `"flat"`
6. Use `cn()` from `@acme/design-system/utils/style` for class merging
7. Use existing `@acme/design-system` components before creating new ones
8. Mobile-first responsive: base → `md:` (768px) → `lg:` (1024px) → `xl:` (1280px)

### Precedence

> **Rule 1:** Profile overrides component defaults.
> **Rule 2:** Design spec overrides profile.
> When in doubt, the more specific source wins.

If the design profile says `defaultRadius: "sm"` and the component defaults to `rounded-lg`, use `rounded-sm`. If a page-level design spec then says "use large radius for hero cards," that overrides the profile for those cards only.

### Where Boldness Lives

The plugin's creative philosophy applies to:
- **Composition**: How you arrange components, use whitespace, create visual hierarchy — asymmetry, overlap, and diagonal flow are encouraged through layout choices (grid-cols, order, absolute positioning), not through arbitrary spacing values
- **Motion**: CSS transitions/animations on existing token values (opacity, transform, scale) — use `transition-*` utilities and `@keyframes` with token-derived values
- **Density context**: Choose `.context-operations` / `.context-consumer` / `.context-hospitality` intentionally — this changes the entire feel without breaking the system
- **Brand expression**: Each business has a distinct brand dossier — lean into its personality, voice, and visual identity. The dossier IS the aesthetic direction
- **Component selection**: Choose the right atom/molecule from the design system, don't default to the obvious choice. A `StatCard` grid tells a different story than a `DataGrid` table
- **Surface layering**: Use `surface-1`, `surface-2`, `surface-3` to create depth and hierarchy — this is how the design system provides atmosphere

The plugin's creative philosophy does NOT override:
- Color values (use tokens or theme asset brand colors)
- Font choices (use theme asset fonts or font tokens)
- Spacing values (use profile-derived gaps or 8-pt rhythm)
- Border radius (use profile default radius)
- Creating custom CSS properties outside the design system

## Profile, Assets, and Recipes Loading

Before building any themed surface, load the three expression layers for the target theme:

1. **Read `design-profile.ts`** — art-direction defaults (radius, elevation, border, spacing, typography scale, guidance on color strategy, whitespace, motion). State which theme you are using.
2. **Read `assets.ts`** — available fonts, gradients, shadow palettes, keyframes, named brand colors. If empty, the brand has no custom assets; fall back to base tokens.
3. **Read `recipes.ts`** — branded surface compositions (hero panels, CTA styles, content sections). If empty, compose from profile defaults and tokens.

These files live at `packages/themes/<theme>/src/`. If any file does not exist for the target theme, treat that layer as empty (use base defaults).

**Example:** For Caryina, `design-profile.ts` might specify `defaultRadius: "sm"`, `defaultElevation: "flat"`, `colorStrategy: "restrained"`. This means: small rounded corners, no drop shadows on cards, and a primary-plus-one-accent palette. The agent applies these defaults to every surface unless a page-level design spec overrides them.

## Surface Mode Selection

A single profile is too coarse for an entire app. Pick the right surface mode before building:

### Mode Criteria

| Mode | Use when building | Key signals |
|------|------------------|-------------|
| **marketing** | Hero sections, landing pages, conversion-focused flows, above-fold CTAs | Persuasion-oriented, high visual impact, brand expression at maximum |
| **editorial** | Long-form content, guides, blogs, documentation | Readability-first, single-column prose, generous line-height |
| **operations** | Dashboards, admin panels, data tables, staff-facing tools | Information density, compact spacing, flat surfaces, restrained color |
| **campaign** | Time-limited promotions, seasonal pages, launch announcements | Bold color, dramatic motion, pervasive accent, high urgency |

### How to Choose

Mode is determined in priority order:

1. **Design spec (explicit, authoritative).** If a `/lp-design-spec` output exists for the feature, its `Surface-Mode` field is authoritative. Use it.
2. **Route convention (structural).** If the app maps route patterns to modes in its config, use the matching mode. Example: `/guides/*` maps to `editorial`, `/admin/*` maps to `operations`.
3. **Agent inference (fallback).** When no design spec exists and no route mapping applies, select a mode based on the criteria table above. **State which mode you selected and why.** If the operator disagrees, they specify the correct mode and you rebuild.

The selected mode merges over the baseline profile — unspecified fields inherit from baseline.

## Recipe Catalogue Check

Before inventing new surface compositions, check `recipes.ts` for branded compositions that match the surface you are building:

1. Read the recipe catalogue for the target theme.
2. For each recipe, check `applicableModes` — does it match your selected surface mode?
3. Check `usage` and `doNotUseWhen` — does the recipe fit the context?
4. If a recipe matches, apply its `classes` and `css` fields directly. Do not reinvent the composition.
5. If no recipe matches, compose from profile defaults and tokens. Good compositions that emerge can be promoted to recipes afterward.

**Example:** Building a hero section for Brikette in `marketing` mode? Check `recipes.ts` for `heroPanel` — it provides gradient, blur, and ring classes purpose-built for that surface. Use it instead of composing from scratch.

## Style Movement Translation Table

When the user or design spec requests a specific visual movement, use this table to set profile baseline and mode:

| Movement | Profile baseline | Mode suggestion | Key characteristics |
|----------|-----------------|-----------------|---------------------|
| **Swiss/International** | `scaleRatio: 1.333`, `defaultRadius: "sm"`, `defaultElevation: "flat"`, `defaultBorder: "defined"` | marketing or editorial | Tight tracking on labels, uppercase transforms, grid tension via asymmetry, restrained palette with spot accent, generous whitespace |
| **Editorial** | `scaleRatio: 1.5+`, `displayWeight: 300` (light) or `900` (black), `bodyMeasure: "58ch"` | editorial | Dramatic size contrast between display and body, single-column prose, full-bleed images, extreme whitespace, dramatic motion (staggered entry) |
| **Minimalist** | `scaleRatio: 1.125`, `defaultElevation: "flat"`, `defaultBorder: "none"`, `defaultRadius: "sm"` | editorial or marketing | Flat everything, monochromatic palette, spot accent on CTA only, extreme whitespace, no motion or instant transitions |
| **Brutalist** | `scaleRatio: 1.414`, `displayWeight: 900`, `defaultRadius: "none"`, `defaultBorder: "bold"` | marketing | All-caps display, sharp edges, heavy borders, high-contrast colors, no shadows, no motion |
| **Material/Soft** | `defaultRadius: "xl"`, `defaultElevation: "layered"`, `defaultBorder: "none"` | any | Rounded surfaces, layered shadows, no borders, playful motion (spring easing), expressive color |
| **Glass/Atmospheric** | `defaultElevation: "subtle"`, `defaultRadius: "xl"` | campaign | Backdrop blur, translucent surfaces, high background contrast, subtle ring borders, precise motion |

These are starting points, not prescriptions. The agent adapts based on brand identity and page context.

## Workflow

### Step 1: Resolve the Business

Read `docs/business-os/strategy/businesses.json` to find the target business for the work.

**Quick-reference only (may become stale):** The table below is illustrative. Always read `docs/business-os/strategy/businesses.json` for the authoritative app → business → theme mapping.

| Business | Key Apps | Theme |
|----------|----------|-------|
| BRIK | brikette, reception, prime | `packages/themes/prime/` |
| PLAT | platform-core, design-system, cms, dashboard | `packages/themes/base/` |
| BOS | business-os | `packages/themes/base/` |
| PIPE | product-pipeline | `packages/themes/base/` |
| XA | xa | `packages/themes/base/` |
| HEAD | cochlearfit | `packages/themes/base/` |
| PET | (no apps yet) | `packages/themes/base/` |
| HBAG | cover-me-pretty, handbag-configurator | `packages/themes/base/` |

Load the brand dossier: `docs/business-os/strategy/<BIZ>/<YYYY-MM-DD>-brand-identity-dossier.user.md`

**If no brand dossier exists** (common for PLAT, BOS, PIPE, XA): use base theme tokens directly from `packages/themes/base/src/tokens.ts` as the design reference. No redirection needed — the design system tokens provide a complete and correct palette. Reserve `/lp-assessment-bootstrap <BIZ>` for operating businesses that will have a distinct brand identity.

### Step 2: Load Design System Context

1. Read `.claude/skills/tools-design-system/SKILL.md` for the token quick-reference
2. Read `packages/themes/<theme>/src/design-profile.ts` for art-direction defaults and guidance
3. Read `packages/themes/<theme>/src/assets.ts` for available fonts, gradients, shadows, keyframes, brand colors
4. Read `packages/themes/<theme>/src/recipes.ts` for branded surface compositions
5. Read `packages/themes/<theme>/src/tokens.ts` for the business's concrete token values
6. Read `docs/design-system-handbook.md` for available components
7. If the feature is complex, also read `docs/typography-and-color.md`

### Step 3: Design Direction

With the brand dossier and tokens loaded, establish a creative direction:

- What density context fits? (`operations` for dashboards, `consumer` for marketing, `hospitality` for booking)
- What surface layering creates the right depth? (flat vs elevated vs deeply layered)
- What motion principles serve the user? (subtle transitions vs dramatic reveals)
- How does the brand personality translate to composition choices?

### Step 4: Build

Implement using:
- `@acme/design-system` components (atoms, molecules, primitives)
- Semantic Tailwind tokens (never arbitrary values)
- `cn()` for conditional class merging
- Proper TypeScript types for all props

### Step 5: Verify

After building, run `/lp-design-qa` to audit:
- Token compliance (no arbitrary values)
- Brand dossier alignment
- Accessibility (contrast ratios, keyboard navigation, ARIA)
- Responsive behavior across breakpoints

### Step 6: Document (optional)

For significant features that benefit from visual documentation, suggest `/tools-bos-design-page` to create diagrams showing the component architecture, state flows, or interaction patterns.

## Integration

- **Upstream:** `lp-design-spec` (design spec document — provides layout, component, and token decisions); `lp-do-plan` (IMPLEMENT task with `Execution-Track: code` and UI component scope).
- **Downstream:** `lp-design-qa` (design and token compliance audit of the built UI); `lp-do-build` (built components committed and verified before QA).
- **Loop position:** S9A (UI Build) — post-design-spec, pre-design-qa.

## Anti-Patterns

| Do NOT | Do instead |
|--------|------------|
| `bg-[#FF6B35]` | `bg-primary` (resolved from theme tokens) |
| `font-['Plus Jakarta Sans']` | `font-heading` (resolved from theme tokens) |
| `p-[13px]` | `p-3` (8-pt rhythm: 12px) |
| `rounded-[7px]` | `rounded-md` (token scale) |
| Import Google Fonts | Use `font-sans`, `font-heading`, `font-mono` |
| Create new CSS custom properties | Add tokens to `packages/themes/base/src/tokens.ts` |
| `style={{ color: '#333' }}` | `className="text-fg"` |
| Build a custom button | Use `@acme/design-system/shadcn/Button` |
