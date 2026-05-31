---
name: icon-forge
description: Generate brand icons as SVG and produce all platform assets including favicon package (ICO, SVG with dark mode, apple-touch-icon), PWA manifest icons, and mobile app icons. Use when user runs /icon-forge, requests "brand icon", "favicon generation", "app icon", or "svg logo" for a project.
allowed-tools: Bash(uv run *)
argument-hint: "[brand description or --svg <path> or --base <path>]"
---

# Icon Forge

Generate brand icons as SVG and produce all required platform assets from a single source.

## Quick Start

Follow these phases in order. Skip to Phase 4 if user provides `--svg <path>`. Use `--base <path>` to load an existing SVG as a design seed for Phase 2 iteration.

### Phase 1: Brand Discovery

Gather brand information before designing. Ask about:
- **Identity**: Brand name, industry, tagline
- **Concept**: Visual metaphor, abstract vs literal, symbol ideas
- **Colors**: Primary color (hex), secondary, accent
- **Style preset**: Present the style menu:
  1. **Geometric** — clean shapes, mathematical precision
  2. **Organic** — flowing curves, irregular blobs, natural asymmetry
  3. **Illustrative** — layered scenes, color blocks, story-driven
  4. **Symbolic** — dual-meaning line art, negative space, conceptual merges
  5. **Constellation** — connected nodes, network graphs, dot clusters
- **Depth**: Flat (default) or with gradients/shadows?

If `$ARGUMENTS` contains a brand description, extract info and minimize questions.

### Phase 2: Design Master SVG

Generate 2-3 concept variations as SVG. Apply the chosen style preset's SVG techniques from [WORKFLOW.md](WORKFLOW.md) (see Style-to-SVG Technique Table). Design for three progressive detail tiers: Glyph (16px, 2-4 shapes), Mark (192px, full logomark), Master (1024px, rich detail). Present concepts, let user choose, iterate.

**If `--base <path>` was provided**: Read the existing SVG, analyze its shapes/colors/structure, and use it as a starting point instead of generating from scratch. Present the original alongside 2 improved variations that apply the chosen style preset. See [WORKFLOW.md](WORKFLOW.md) "Design Seed Workflow" for details.

**SVG structure requirements:**
```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="icon-title">
  <title id="icon-title">Brand Name</title>
  <style>
    .primary { fill: #2563eb; }
    .accent  { fill: #1e40af; }
  </style>
  <path class="primary" d="..."/>
</svg>
```

**Validation checklist:**
- viewBox is square (`0 0 100 100` brand icons; `0 0 24 24` for UI-style marks)
- No `width`/`height` attributes on root `<svg>`
- `<title>` as first child, `role="img"` on root (accessibility)
- No `<text>` elements (text does not scale to 16px)
- Filled shapes on integer coordinates (prevents sub-pixel blur)
- No strokes thinner than 2 units in Glyph/Mark tiers
- Color count within preset limit (1-3 most; up to 5 Illustrative/Constellation)
- `xmlns` attribute present

### Phase 3: Create Dark-Mode Favicon SVG

Duplicate the master SVG and embed a `@media (prefers-color-scheme: dark)` block:

```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="fav-title">
  <title id="fav-title">Brand Name</title>
  <style>
    .bg { fill: #ffffff; }
    .fg { fill: #1a1a2e; }
    @media (prefers-color-scheme: dark) {
      .bg { fill: #1a1a2e; }
      .fg { fill: #e0e0ff; }
    }
  </style>
  <rect class="bg" width="100" height="100" rx="12"/>
  <path class="fg" d="..."/>
</svg>
```

Rules: dark foreground becomes light, light backgrounds become dark, maintain >= 4.5:1 contrast.

### Phase 3b: Monochrome Variant

Duplicate the master SVG and replace all colors with `currentColor`. Remove `<style>`, gradients, and filters — produce a single-color silhouette that inherits its color from CSS. Save as `monochrome.svg`. See [WORKFLOW.md](WORKFLOW.md) for details.

### Phase 4: Generate Platform Assets

Save master SVG and dark-mode SVG to the project.

**Framework detection** — before running the script, detect the target project:
1. If `next.config.(js|mjs|ts)` exists AND `app/layout.(tsx|jsx|js)` exists → add `--framework nextjs`
2. Otherwise → omit `--framework` (default generic output)

```bash
uv run <skill-scripts-dir>/generate_assets.py \
  --svg <master-svg-path> \
  --dark-svg <dark-svg-path> \
  --bg-color "<brand-bg-color>" \
  --name "<app-name>" \
  --framework nextjs \  # omit if not Next.js App Router
  --output-dir ./brand-assets
```

Replace `<skill-scripts-dir>` with the absolute path to this skill's `scripts/` directory.
Omit `--framework` for non-Next.js projects. With `--framework nextjs`, outputs `icon.svg` and `apple-icon.png` (Next.js App Router conventions).

**Requires** `rsvg-convert` (brew install librsvg) or `magick` (brew install imagemagick).

### Phase 5: Integration Output

Present to the user:
1. The integration guide (`_nextjs-guide.txt` for Next.js, or `_html-snippet.html` for other frameworks)
2. Framework-specific placement guidance (Next.js `app/` + `public/`, Vite `public/`, CRA `public/`)
3. Summary of all generated files

## SVG Icon Design Principles

1. **Canvas**: Square `viewBox` — `0 0 100 100` for brand icons (default), `0 0 24 24` for UI-style marks. No width/height attributes
2. **Scalability**: Must be recognizable at 16px (favicon) through 1024px (app store)
3. **Shape vocabulary**: Match shapes to the chosen style preset. See [WORKFLOW.md](WORKFLOW.md) for style-specific SVG techniques
4. **Fill vs stroke**: Prefer filled paths (scale predictably); use strokes for Symbolic line art. See [WORKFLOW.md](WORKFLOW.md) for per-preset strategy
5. **Stroke minimum**: No strokes thinner than 2 units in Glyph/Mark tiers; Master tier may use 1.5+ for decorative detail
6. **Color restraint**: 1-3 brand colors for most presets; Illustrative and Constellation may use up to 5
7. **No text**: Logomark only — text does not survive 16px rendering
8. **Progressive detail**: Design for three tiers (Glyph 16px, Mark 192px, Master 1024px). Fine detail welcome in Master tier; must simplify gracefully
9. **Pixel alignment**: Integer coordinates for filled shapes; 0.5 offset for odd stroke widths. Limit decimals to 1-2 places
10. **Accessibility**: `<title>` as first child with brand name, `role="img"` on root `<svg>`
11. **Visual weight**: Center of mass should feel balanced in the square canvas
12. **Negative space**: Use intentionally for clever dual-meaning designs
13. **currentColor**: Always generate a monochrome variant with `fill="currentColor"` alongside the branded master
14. **Depth**: Flat by default. When depth is enabled, use `<linearGradient>`, `<radialGradient>`, and subtle `<filter>` effects
15. **Rounded corners**: Use `rx`/`ry` for approachable feel when appropriate

## Output

See [WORKFLOW.md](WORKFLOW.md) for detailed workflow and [EXAMPLES.md](EXAMPLES.md) for examples.
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
