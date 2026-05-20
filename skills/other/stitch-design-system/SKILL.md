---
name: stitch-design-system
description: Extracts a Stitch design and generates production code artifacts — CSS custom properties with dark mode tokens, a Tailwind v4 @theme block, and a semantic design system document. Run this before framework conversion skills.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch → Design System Code Artifacts

You are a design systems engineer. You analyze Stitch designs and generate **code artifacts** — not just documentation. While the `design-md` skill produces a human-readable markdown file, this skill produces files you actually import into your codebase: CSS custom properties with dark mode, Tailwind v4 configuration, and typography tokens.

**Use this skill first, before `stitch-nextjs-components` or `stitch-svelte-components`.** The generated tokens become the foundation for all subsequent component generation.

## When to use this skill

Use this skill when:
- Starting a new project from a Stitch design
- The user mentions "design tokens", "CSS variables", "dark mode tokens", "Tailwind config"
- Running before framework conversion skills to ensure design consistency
- Updating an existing project's design system after a Stitch design update

## What this skill generates

Three output files:

| File | Purpose |
|------|---------|
| `design-tokens.css` | CSS custom properties — import this in your framework's global CSS |
| `tailwind-theme.css` | Tailwind v4 `@theme` block — paste into your `globals.css` |
| `DESIGN.md` | Extended design document (richer than `design-md`, includes dark mode + animation tokens) |

## Step 1: Retrieve the Stitch design

1. **Namespace discovery** — Run `list_tools` to find the Stitch MCP prefix.
2. **Fetch screen** — Call `[prefix]:get_screen` with `projectId` and `screenId`.
3. **Download HTML** — Run:
   ```bash
   bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "temp/source.html"
   ```
4. **Visual reference** — Check `screenshot.downloadUrl` to see the full design intent.

If multiple screens exist, retrieve all of them. Run `[prefix]:list_screens` and fetch each one to ensure the token set covers every pattern in the design.

## Step 1.5: Read project DesignTheme (ground truth)

Before parsing HTML, get the authoritative design data from the Stitch API. This eliminates guesswork — the API knows the exact primary color, fonts, and full semantic color map.

1. **Call `get_project`** with `projects/[projectId]`
2. **Check for `designMd`** — if present, it's a full markdown design system document that Stitch auto-generated. Parse it for typography rules, color philosophy, component patterns, spacing guidelines, and do's/don'ts. This is the most valuable single field.
3. **Extract `namedColors`** — a 40+ token semantic color map. This gives you the ENTIRE color system pre-computed:
   - Primary: `primary`, `on_primary`, `primary_container`, `on_primary_container`, `primary_fixed`, `primary_fixed_dim`
   - Secondary: `secondary`, `on_secondary`, `secondary_container`, `on_secondary_container`
   - Tertiary: same pattern
   - Surfaces: `surface`, `surface_dim`, `surface_bright`, `surface_container_lowest`, `surface_container_low`, `surface_container`, `surface_container_high`, `surface_container_highest`, `surface_tint`, `surface_variant`
   - Utility: `background`, `on_background`, `on_surface`, `on_surface_variant`, `outline`, `outline_variant`
   - States: `error`, `on_error`, `error_container`, `on_error_container`
   - Inverse: `inverse_surface`, `inverse_on_surface`, `inverse_primary`
4. **Extract structural values:**

| DesignTheme field | → CSS token | Mapping |
|---|---|---|
| `customColor` | `--color-primary` | Hex seed — but prefer `namedColors.primary` if available |
| `overridePrimaryColor` | `--color-primary` | Takes precedence over customColor |
| `overrideSecondaryColor` | `--color-secondary` | Exact hex override |
| `overrideTertiaryColor` | `--color-tertiary` | Exact hex override |
| `overrideNeutralColor` | `--color-neutral` | Base for surface hierarchy |
| `backgroundLight` | `--color-background` (light) | Light mode page background |
| `backgroundDark` | `--color-background` (dark) | Dark mode page background |
| `headlineFont` | `--font-sans` / heading | Map enum → font-family stack (see table below) |
| `bodyFont` | `--font-body` | Map enum → font-family stack |
| `labelFont` | `--font-label` | Map enum → font-family stack |
| `roundness` | `--radius-md` baseline | ROUND_FOUR=4px, ROUND_EIGHT=8px, ROUND_TWELVE=12px, ROUND_FULL=9999px |
| `spacingScale` | spacing multiplier | 0=tight (base 2px), 1=compact (base 4px), 2=normal (base 4px), 3=spacious (base 8px) |
| `colorVariant` | informs palette approach | e.g., FIDELITY means stick to brand colors, VIBRANT means boost saturation |

**Font enum → CSS font-family mapping:**

| Stitch enum | CSS font-family |
|---|---|
| `INTER` | `'Inter', system-ui, sans-serif` |
| `DM_SANS` | `'DM Sans', system-ui, sans-serif` |
| `GEIST` | `'Geist', system-ui, sans-serif` |
| `SPACE_GROTESK` | `'Space Grotesk', system-ui, sans-serif` |
| `MANROPE` | `'Manrope', system-ui, sans-serif` |
| `PLUS_JAKARTA_SANS` | `'Plus Jakarta Sans', system-ui, sans-serif` |
| `WORK_SANS` | `'Work Sans', system-ui, sans-serif` |
| `IBM_PLEX_SANS` | `'IBM Plex Sans', system-ui, sans-serif` |
| `RUBIK` | `'Rubik', system-ui, sans-serif` |
| `SORA` | `'Sora', system-ui, sans-serif` |
| `EPILOGUE` | `'Epilogue', system-ui, sans-serif` |
| `NUNITO_SANS` | `'Nunito Sans', system-ui, sans-serif` |
| `LEXEND` | `'Lexend', system-ui, sans-serif` |
| `PUBLIC_SANS` | `'Public Sans', system-ui, sans-serif` |
| `SOURCE_SANS_THREE` | `'Source Sans 3', system-ui, sans-serif` |
| `MONTSERRAT` | `'Montserrat', system-ui, sans-serif` |
| `HANKEN_GROTESK` | `'Hanken Grotesk', system-ui, sans-serif` |
| `ARIMO` | `'Arimo', system-ui, sans-serif` |
| `BE_VIETNAM_PRO` | `'Be Vietnam Pro', system-ui, sans-serif` |
| `SPLINE_SANS` | `'Spline Sans', system-ui, sans-serif` |
| `METROPOLIS` | `'Metropolis', system-ui, sans-serif` |
| `EB_GARAMOND` | `'EB Garamond', Georgia, serif` |
| `LITERATA` | `'Literata', Georgia, serif` |
| `SOURCE_SERIF_FOUR` | `'Source Serif 4', Georgia, serif` |
| `LIBRE_CASLON_TEXT` | `'Libre Caslon Text', Georgia, serif` |
| `NEWSREADER` | `'Newsreader', Georgia, serif` |
| `DOMINE` | `'Domine', Georgia, serif` |
| `NOTO_SERIF` | `'Noto Serif', Georgia, serif` |

5. **Use these as the baseline.** Then use HTML analysis (Step 2) only for values the API doesn't provide: motion/transition durations, exact spacing pixel values, shadow definitions, additional colors beyond the namedColors set.

**If `namedColors` is available**, skip the color extraction in Step 2 entirely — the API's color map is authoritative and complete. Only supplement with motion, spacing pixel values, and shadows from HTML.

**If `designMd` is available**, use it as the foundation for the DESIGN.md output (Step 5). Don't rewrite it — augment it with CSS variable names, Tailwind mappings, and implementation notes.

## Step 2: Extract supplementary values from HTML

If Step 1.5 provided `namedColors` and `designMd`, you only need HTML for:

### Motion
- Transition durations used (or infer: 150ms for micro, 300ms for panels)
- Easing styles (linear, ease-out, spring-like)

### Spacing pixel values
- Exact gap/padding values used in the design
- Shadow definitions

### Additional colors (rare)
Only if the design uses colors not in `namedColors` — check for gradients, overlays, or custom accent colors.

**If Step 1.5 did NOT provide namedColors** (older projects without designMd), fall back to full HTML extraction:

### Colors (fallback)
Identify every distinct color from the Tailwind config in `<head>` or infer from screenshot. For each, determine semantic role and usage frequency. Aim for 8-12 semantic tokens.

### Typography (fallback)
- Font families (heading, body, mono — if present)
- Type scale sizes (the actual `px` or `rem` values used in the design)
- Font weights used
- Line heights

### Spacing & geometry (fallback)
- Base spacing unit (usually 4px or 8px)
- Border radius values
- Shadow definitions

## Step 3: Generate `design-tokens.css`

Create `design-tokens.css` with full light + dark mode token sets.

**Naming convention:**
- `--color-*` — Color tokens
- `--font-*` — Typography
- `--spacing-*` — Spacing scale
- `--radius-*` — Border radius
- `--shadow-*` — Elevation
- `--motion-*` — Animation timing

**Template (when namedColors is available from API — preferred):**
```css
/* =============================================================
   Design Tokens — extracted from Stitch project: [Project Name]
   Generated by stitch-design-system skill
   Source: DesignTheme API (namedColors) + HTML supplementary
   ============================================================= */

/* ---- Light mode (default) ---- */
:root {
  /* Colors: Direct mapping from Stitch namedColors API response */
  --color-primary:          [namedColors.primary];
  --color-on-primary:       [namedColors.on_primary];
  --color-primary-container: [namedColors.primary_container];
  --color-secondary:        [namedColors.secondary];
  --color-on-secondary:     [namedColors.on_secondary];
  --color-tertiary:         [namedColors.tertiary];
  --color-on-tertiary:      [namedColors.on_tertiary];
  --color-error:            [namedColors.error];
  --color-on-error:         [namedColors.on_error];
  --color-background:       [namedColors.background];
  --color-on-background:    [namedColors.on_background];
  --color-surface:          [namedColors.surface];
  --color-on-surface:       [namedColors.on_surface];
  --color-surface-variant:  [namedColors.surface_variant];
  --color-on-surface-variant: [namedColors.on_surface_variant];
  --color-surface-container: [namedColors.surface_container];
  --color-surface-container-low: [namedColors.surface_container_low];
  --color-surface-container-high: [namedColors.surface_container_high];
  --color-surface-container-highest: [namedColors.surface_container_highest];
  --color-outline:          [namedColors.outline];
  --color-outline-variant:  [namedColors.outline_variant];
  --color-inverse-surface:  [namedColors.inverse_surface];
  --color-inverse-on-surface: [namedColors.inverse_on_surface];
  --color-inverse-primary:  [namedColors.inverse_primary];
  --color-surface-tint:     [namedColors.surface_tint];

  /* Typography */
  --font-sans:    [font-family-stack];   /* Heading and UI font */
  --font-body:    [font-family-stack];   /* Body text font (may equal --font-sans) */
  --font-mono:    [monospace-stack];     /* Code, technical content */

  /* Type scale */
  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg:   1.125rem;  /* 18px */
  --text-xl:   1.25rem;   /* 20px */
  --text-2xl:  1.5rem;    /* 24px */
  --text-3xl:  1.875rem;  /* 30px */
  --text-4xl:  2.25rem;   /* 36px */

  /* Spacing scale (base 4px) */
  --space-1:  0.25rem;   /* 4px */
  --space-2:  0.5rem;    /* 8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-6:  1.5rem;    /* 24px */
  --space-8:  2rem;      /* 32px */
  --space-12: 3rem;      /* 48px */
  --space-16: 4rem;      /* 64px */

  /* Geometry */
  --radius-sm: [value];  /* Small elements: badges, chips */
  --radius-md: [value];  /* Buttons, inputs */
  --radius-lg: [value];  /* Cards, panels */
  --radius-xl: [value];  /* Modals, drawers */
  --radius-full: 9999px; /* Pills, avatars */

  /* Shadows */
  --shadow-sm: [value];  /* Subtle card lift */
  --shadow-md: [value];  /* Dropdown, tooltip */
  --shadow-lg: [value];  /* Modal, sheet */

  /* Motion tokens */
  --motion-duration-fast:   150ms;   /* Hover states, micro interactions */
  --motion-duration-base:   250ms;   /* Typical UI transitions */
  --motion-duration-slow:   400ms;   /* Page-level, large panel */
  --motion-ease-default:    cubic-bezier(0.4, 0, 0.2, 1);  /* Material ease */
  --motion-ease-out:        cubic-bezier(0, 0, 0.2, 1);    /* Entries */
  --motion-ease-in:         cubic-bezier(0.4, 0, 1, 1);    /* Exits */
  --motion-ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1); /* Bouncy open */
}

/* ---- Dark mode ---- */
/* Applied via .dark class (Next.js + next-themes) or [data-theme="dark"] (Svelte) */
.dark,
[data-theme="dark"] {
  --color-background:       [dark-hex];
  --color-surface:          [dark-hex];
  --color-surface-elevated: [dark-hex];
  --color-primary:          [dark-hex];  /* Same hue, lighter for dark bg contrast */
  --color-primary-hover:    [dark-hex];
  --color-primary-fg:       [dark-hex];
  --color-secondary:        [dark-hex];
  --color-secondary-fg:     [dark-hex];
  --color-text:             [dark-hex];
  --color-text-muted:       [dark-hex];
  --color-text-disabled:    [dark-hex];
  --color-border:           [dark-hex];
  --color-border-focus:     [dark-hex];
  --color-error:            [dark-hex];
  --color-success:          [dark-hex];
  --color-warning:          [dark-hex];
  /* Typography, spacing, geometry, motion tokens: unchanged in dark mode */
}
```

## Step 4: Generate `tailwind-theme.css`

For projects using **Tailwind v4** (no `tailwind.config.js`), generate a `@theme` block.

**Important:** Tailwind v4 uses `@theme` in CSS, not a JS config file. Map tokens to Tailwind's namespace:

```css
/* tailwind-theme.css — paste into your globals.css or import it */
@import "tailwindcss";

@theme {
  /* Wire Tailwind color utilities to your CSS variables */
  --color-background: var(--color-background);
  --color-surface: var(--color-surface);
  --color-primary: var(--color-primary);
  --color-primary-hover: var(--color-primary-hover);
  --color-text: var(--color-text);
  --color-text-muted: var(--color-text-muted);
  --color-border: var(--color-border);

  /* Fonts */
  --font-sans: var(--font-sans);
  --font-mono: var(--font-mono);

  /* Radius */
  --radius-sm: var(--radius-sm);
  --radius-md: var(--radius-md);
  --radius-lg: var(--radius-lg);

  /* Animation duration utilities */
  --animate-duration-fast: var(--motion-duration-fast);
  --animate-duration-base: var(--motion-duration-base);
  --animate-duration-slow: var(--motion-duration-slow);
}
```

For **Tailwind v3** projects (with `tailwind.config.js`), instead generate a `tailwind.config.js` section using the extracted hex values directly.

## Step 5: Generate `DESIGN.md`

Produce an extended design document. It has all sections from the standard `design-md` skill plus:

```markdown
# Design System: [Project Name]

> Generated by stitch-design-system from Stitch project [ID]
> Screens analyzed: [list]

## 1. Visual Theme & Atmosphere
[Mood, density, aesthetic philosophy — 2-3 sentences]

## 2. Color Palette & Roles
| Token | Light | Dark | Role |
|-------|-------|------|------|
| --color-primary | #... | #... | Main CTA, key actions |
| --color-background | #... | #... | Page background |
| ... | | | |

## 3. Typography
- **Heading font**: [Family, weights used, where]
- **Body font**: [Family, weights used, where]
- **Type scale**: xs (12px) → sm (14px) → base (16px) → lg (18px) → ... → 4xl (36px)

## 4. Geometry & Elevation
- **Border radius**: sm [Xpx] | md [Xpx] | lg [Xpx] | xl [Xpx]
- **Shadows**: [describe the elevation system]

## 5. Motion System
- **Micro** (hovers, toggles): [duration]ms [easing]
- **Meso** (panels, drawers): [duration]ms [easing]
- **Macro** (page transitions): [duration]ms [easing]
- **Spring** (playful elements): cubicOut spring

## 6. Stitch Prompt Copy-Paste Block
Use this block in every Stitch prompt for design consistency:

```
[Primary color: NAME (#HEX)] — used for buttons and key actions
[Background: #HEX] — clean and [mood adjective]
[Typography: FONT NAME] — [weight] weight for headings, regular for body
[Aesthetic: 2-3 adjectives describing the visual style]
[Border radius: SIZE — rounded/sharp/pill-shaped elements]
```

## 7. Dark Mode Notes
[Specific notes on how the dark theme differs — any color roles that change significantly, any elements that need special treatment in dark mode]
```

## Step 6: Output & integration

Write all three files to the project root (or wherever the user specifies):
- `design-tokens.css`
- `tailwind-theme.css`
- `DESIGN.md`

Then tell the user how to use them:

**For Next.js:**
```tsx
// app/globals.css
@import '../design-tokens.css';
@import '../tailwind-theme.css';
```

**For SvelteKit:**
```svelte
<!-- src/app.css -->
@import '$lib/design-tokens.css';
```

**For the Stitch loop:**
> Copy Section 6 from `DESIGN.md` into every Stitch prompt to maintain design consistency across generated screens.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Can't determine dark mode hex values | Use the light-mode hue, desaturate slightly, and increase lightness by 30-40% |
| Font not loading | Add Google Fonts `@import` to `design-tokens.css` |
| Tailwind v3 vs v4 confusion | Check `package.json` — v4 uses `"tailwindcss": "^4"` and no config file |
| Tokens not applying | Ensure `design-tokens.css` is imported BEFORE component CSS |

## Integration with other skills

- Run this skill **before** `stitch-nextjs-components` or `stitch-svelte-components`
- The framework skills will import `design-tokens.css` instead of hardcoding values
- The `DESIGN.md` Section 6 feeds into `stitch-loop` for multi-page consistency

## References

- `resources/tokens-template.css` — Full template with all token categories
