---
name: icon-forge
description: Generate brand icons as SVG and produce all platform assets including favicon package (ICO, SVG with dark mode, apple-touch-icon), PWA manifest icons, and mobile app icons. Use when user runs /icon-forge, requests "brand icon", "favicon generation", "app icon", or "svg logo" for a project.
disable-model-invocation: true
allowed-tools: Bash(uv run *)
argument-hint: "[brand description or --svg <path>]"
---

# Icon Forge

Generate brand icons as SVG and produce all required platform assets from a single source.

## Quick Start

Follow these 5 phases in order. Skip to Phase 4 if user provides `--svg <path>`.

### Phase 1: Brand Discovery

Gather brand information before designing. Ask about:
- **Identity**: Brand name, industry, tagline
- **Concept**: Visual metaphor, abstract vs literal, symbol ideas
- **Colors**: Primary color (hex), secondary, accent
- **Style**: Minimal, playful, corporate, bold, elegant, techy

If `$ARGUMENTS` contains a brand description, extract info and minimize questions.

### Phase 2: Design Master SVG

Generate 2-3 concept variations as SVG. Apply the design principles below. Present concepts, let user choose, iterate.

**SVG structure requirements:**
```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- No width/height attributes -->
  <!-- Colors as CSS classes for dark mode adaptability -->
  <style>
    .primary { fill: #2563eb; }
    .accent  { fill: #1e40af; }
  </style>
  <path class="primary" d="..."/>
</svg>
```

**Validation checklist:**
- viewBox is `0 0 100 100` (square, clean coordinates)
- No `width`/`height` attributes on root `<svg>`
- No `<text>` elements (text does not scale to 16px)
- No strokes thinner than 2 units
- Maximum 3 distinct colors
- `xmlns` attribute present

### Phase 3: Create Dark-Mode Favicon SVG

Duplicate the master SVG and embed a `@media (prefers-color-scheme: dark)` block:

```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
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

1. **Canvas**: `viewBox="0 0 100 100"`, no width/height attributes
2. **Scalability**: Must be recognizable at 16px (favicon) through 1024px (app store)
3. **Geometric simplicity**: Prefer circles, rectangles, clean bezier curves
4. **Stroke minimum**: No strokes thinner than 2 units at 100x100 scale
5. **Color restraint**: 1-3 brand colors maximum
6. **No text**: Logomark only — text does not survive 16px rendering
7. **No fine detail**: Avoid thin lines, small gaps, intricate patterns
8. **Visual weight**: Center of mass should feel balanced in the square canvas
9. **Negative space**: Use intentionally for clever dual-meaning designs
10. **currentColor**: Support monochrome use via `fill="currentColor"` variant
11. **Flat design**: Avoid gradients unless central to brand concept
12. **Rounded corners**: Use `rx`/`ry` for approachable feel when appropriate

## Output

See [WORKFLOW.md](WORKFLOW.md) for detailed workflow and [EXAMPLES.md](EXAMPLES.md) for examples.
See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
