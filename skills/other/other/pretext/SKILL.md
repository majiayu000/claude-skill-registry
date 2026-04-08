---
name: pretext
description: Create text effects impossible with CSS alone — kinetic typography, flowing text around animated obstacles, calligrams, shrinkwrap chat bubbles, typographic ASCII art, glyph path animation, variable font waves, glyph morphing, and illuminated manuscripts. This skill should be used when building single-file HTML pages with advanced text layout, proportional character measurement, per-glyph SVG rendering, text-on-path, animated text reflow, or letter art. Powered by @chenglou/pretext + opentype.js. All output is a single HTML file with zero build step.
argument-hint: [effect description or category]
---

# Pretext Text Effects

Generate browser pages powered by Pretext (`@chenglou/pretext`)—a pure-arithmetic text measurement library that bypasses DOM layout reflow entirely. Pretext measures text with proportional font precision using canvas `measureText`, enabling effects impossible with CSS alone.

**Companion library: opentype.js** (`opentype.js@1.3.4`) — direct font binary parsing for per-glyph SVG path rendering, Bezier control point access, kerning tables, and variable font axes. Pretext handles line breaking; opentype.js handles what happens *inside* each glyph. Together they unlock effects neither can achieve alone.

Output is always a **single self-contained HTML file**. No build step, no framework, runs in any modern browser.

## Quick Start

Describe a text effect. Claude picks the right Pretext pattern and generates a complete HTML file.

Examples:
- `/pretext fluid smoke ASCII art with gold characters on black`
- `/pretext chat bubbles that shrinkwrap tighter than CSS`
- `/pretext calligram — the word "ocean" shaped like a wave`
- `/pretext editorial layout with text flowing around draggable circles`
- `/pretext masonry grid of shower thoughts with instant height prediction`
- `/pretext glyph path art — SVG letterforms with stroke animation`
- `/pretext animated dragon cursor that pushes text aside as it moves`
- `/pretext illuminated manuscript with live vine growth reflow`
- `/pretext variable font wave — per-character weight animation`
- `/pretext glyph morph — letterform interpolation from A to Z`
- `/pretext letterbox gallery of "BEACON" in Playfair Display italic on dark background`
- `/pretext glyph-mask calligram — letter R filled with lorem ipsum in Georgia`

## Do NOT Use This Skill When

- Simple CSS `text-shadow`, `text-stroke`, or gradient text effects
- CSS Shapes level 1 (`shape-outside` on floated elements) for static layouts
- Basic `@keyframes` text animation (fade, slide, typewriter)
- Monospace ASCII art (no proportional measurement needed)
- SVG `<text>` without per-glyph control
- Rich text editing (`contenteditable`, ProseMirror, TipTap)
- PDF generation or markdown rendering

These are all achievable without Pretext or opentype.js.

## Effect Categories

### Pretext-Only Effects

| Category | Pretext APIs Used | When to Use |
|----------|-------------------|-------------|
| **Height Prediction** | `prepare` + `layout` | Accordion, masonry, virtualized lists — anywhere you need text height without DOM reads |
| **Shrinkwrap** | `walkLineRanges` + binary search | Chat bubbles, tooltips, labels — finding the exact tightest width for multiline text |
| **Obstacle Routing** | `layoutNextLine` (variable width) | Text flowing around images, logos, draggable orbs — editorial layouts |
| **Animated Obstacles** | `layoutNextLine` + `carveTextLineSlots` | Moving creatures/orbs that displace text at 60fps — slot-carving fills BOTH sides of obstacle |
| **Typographic ASCII** | `prepareWithSegments` (char measurement) | Fluid simulations, 3D wireframes, particle systems rendered as proportional characters |
| **Calligrams** | `prepareWithSegments` + SDF | Words rendered as shapes using their own letters — hearts, stars, spirals |
| **Glyph-Mask Calligrams** | Canvas `measureText` + `getImageData` pixel mask | Any font glyph as calligram shape — fill a large letter with small text using pixel-mask technique (no SDF needed, no opentype.js) |
| **Letterbox Gallery** | Glyph-mask + per-letter `<canvas>` grid | Each character in a string gets its own canvas with text fill, cursor displacement, and independent interaction |
| **Multi-column Editorial** | All rich APIs combined | Magazine-style layouts with headline fitting, pull quotes, drop caps, column flow |

### Pretext + opentype.js Effects

| Category | APIs Used | When to Use |
|----------|-----------|-------------|
| **Glyph Path Art** | opentype `glyph.getPath()` | SVG letterforms with fill/stroke/control point modes, stroke-draw animation |
| **Text on Path** | opentype `getPath()` + arc-length sampling | Per-glyph placement along Bezier curves with tangent rotation |
| **Variable Font Animation** | opentype `font.tables.fvar.axes` + CSS `font-variation-settings` | Per-character weight/width waves, breathe, ripple, cascade effects |
| **Glyph Morphing** | opentype paths + flubber `interpolate()` | Letterform interpolation between glyphs with contour-aware morphing |
| **Outline Calligrams** | Pretext `layoutNextLine` + opentype glyph mask | Text fills the interior of a large glyph's actual contour (not SDF approximation) |
| **Illuminated Manuscript** | All Pretext + opentype combined | Living medieval pages: wet ink, vine reflow, capital inflation, aging, erasure poetry |

## Concept-to-Effect

Every design decision derives from the concept. Do not default—derive.

**Choose the API tier from the effect complexity:**
- Static height only → `prepare()` + `layout()` (fastest, opaque)
- Need line text/positions → `prepareWithSegments()` + `layoutWithLines()`
- Need per-line width variation → `layoutNextLine()` (iterator, variable width per line)
- Need aggregate geometry without strings → `walkLineRanges()` (no string materialization)
- Need individual character widths → `prepareWithSegments()` on single chars

**Choose the rendering target from the output type:**
- DOM elements (`.line { position: absolute }`) → editorial, accordion, masonry
- Canvas 2D (`ctx.fillText`) → calligrams, some ASCII art
- HTML spans with inline styles → typographic ASCII (weight/style/opacity per character)

## Architecture

```
Pretext CDN → prepare/prepareWithSegments → layout/layoutNextLine → line positions
                                                                          ↓
opentype.js CDN → font.parse(buffer) → glyph.getPath() ──────────> SVG <path> elements
                                                                          ↓
                                                              requestAnimationFrame (if animated)
                                                              resize handler (always)
```

**Two-library split:** Pretext decides WHERE text goes (line breaking, obstacle routing). opentype.js decides HOW each glyph looks (SVG paths, Bezier curves, contour data). Use Pretext alone for DOM-positioned text. Add opentype.js when you need per-glyph SVG rendering, path animation, or glyph contour access.

### CDN Imports

```html
<!-- Pretext (ESM, required) -->
<script type="module">
import { prepare, layout, prepareWithSegments, layoutWithLines, walkLineRanges, layoutNextLine, clearCache } from 'https://esm.sh/@chenglou/pretext@0.0.2'
</script>

<!-- opentype.js (UMD, optional — only for glyph path effects) -->
<script src="https://cdn.jsdelivr.net/npm/opentype.js@1.3.4/dist/opentype.min.js"></script>

<!-- Font binary for opentype.js (Inter .woff — confirmed working) -->
<!-- const FONT_URL = 'https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.8/files/inter-latin-400-normal.woff' -->

<!-- flubber (optional — only for glyph morphing) -->
<!-- <script src="https://cdn.jsdelivr.net/npm/flubber@0.4.2/build/flubber.min.js"></script> -->
```

Import only the functions you need. Pin the version. opentype.js cannot parse `.woff2` — use `.woff` or `.ttf` only.

## Composition Parameters

### All Effects
| Parameter | Default | Notes |
|-----------|---------|-------|
| Font | `'18px Georgia, Palatino, serif'` | Never use `system-ui` — unreliable with Pretext |
| Line height | `28` (px) | Must match CSS `line-height` for height prediction |
| Background | `#08080e` or `#f5f1ea` | Dark or light — never pure black `#000` |

### Typographic ASCII
| Parameter | Range | Default |
|-----------|-------|---------|
| Font size | 10–18px | 14 |
| Font family | serif preferred | `Georgia, Palatino, "Times New Roman", serif` |
| Charset | printable ASCII | ` .,:;!+-=*#@%&a-zA-Z0-9` |
| Weights | 1–3 | `[300, 500, 800]` |
| Styles | normal, italic | both |
| Opacity levels | 6–10 | 10 CSS classes `.a1`–`.a10` |

### Calligrams
| Parameter | Range | Default |
|-----------|-------|---------|
| Canvas size | 200–800px | 400 |
| Char density | 6–24px | 14 |
| Shapes | heart, circle, star, wave, spiral | heart |
| Animation | spring entrance | `springK: 0.08, damping: 0.75` |

### Editorial / Obstacle Routing
| Parameter | Range | Default |
|-----------|-------|---------|
| Columns | 1–4 | 2 |
| Column gap | 20–60px | 40 |
| Gutter | 30–80px | 48 |
| Orb count | 1–6 | 5 |
| Orb radius | 30–120px | 65–110 |
| hPad (horizontal padding around obstacle) | 8–20px | 14 |
| vPad (vertical padding) | 2–8px | 4 |
| MIN_SLOT_WIDTH | 30–80px | 50 |

### opentype.js — Glyph Path Effects
| Parameter | Range | Default |
|-----------|-------|---------|
| Font URL | `.woff` or `.ttf` only | `@fontsource/inter@5.0.8` |
| Font size | 10–200px | 14 (body), 42 (display) |
| Stroke-dashoffset draw speed | 30–150ms per glyph | 80ms |
| Wet ink amplitude | 0.5–3px | 1.8 |
| Wet ink decay (tau) | 800–3000ms | 1500 |
| Glyph morph easing | linear, ease-in-out, spring | ease-in-out |

### Glyph-Mask Calligrams / Letterbox Gallery
| Parameter | Range | Default |
|-----------|-------|---------|
| Canvas size (per letter) | 200–1000px | 500 |
| Fill font size | 8–24px | 11 |
| Fill model | `self`, `lorem`, `alphabet`, `custom` | `lorem` |
| Fill case | `upper`, `lower`, `mixed` | `upper` |
| Fill columns | 1–4 | 1 |
| Grid columns (gallery) | 2–6 | 3 |
| Cursor displacement radius | 50–250px | 100 |
| Cursor displacement force | 10–50 | 35 |
| Displacement damping | 0.85–0.98 | 0.94 |

### opentype.js + flubber — Glyph Morphing
| Parameter | Range | Default |
|-----------|-------|---------|
| Morph duration | 300–2000ms | 800 |
| Flubber maxSegmentLength | 5–20 | 10 |
| Contour strategy | equal, 1-to-many, many-to-1 | auto-detect |

## References

| Working on... | Load |
|---|---|
| Full API surface, types, caveats | `references/api-reference.md` |
| Typographic palette, brightness, ASCII grid | `references/typographic-ascii.md` |
| Column flow, obstacles, headline fitting, slot-carving, animated physics | `references/obstacle-routing.md` |
| SDF shapes, proportional spacing, animation | `references/calligram-shapes.md` |
| Pixel-mask technique, glyph-mask calligrams, cursor displacement, letterbox gallery | `references/calligram-shapes.md` (Pixel-Mask section) |
| opentype.js + Pretext integration patterns | `references/opentype-integration.md` |
| Working accordion template | `assets/templates/height-prediction.html` |
| Working bubbles template | `assets/templates/shrinkwrap-bubbles.html` |
| Working editorial template | `assets/templates/editorial-engine.html` |
| Working ASCII art template | `assets/templates/typographic-ascii.html` |
| Working calligram template | `assets/templates/calligram.html` |
| Working letterbox gallery template | `assets/templates/letterbox-gallery.html` |
| GlyphKit demos (6 working demos, local) | `~/Desktop/Programming/glyphkit/demos/` (machine-specific) |

## Anti-Patterns

### Pretext
- Never use `system-ui` as font — canvas and DOM can resolve different fonts on macOS
- Never use React/Vue/framework — vanilla JS + HTML only
- Never omit `<meta name="viewport">` — proportional measurement depends on correct device pixels
- Never use `setInterval` for animation — always `requestAnimationFrame`
- Never skip the resize handler — text layout depends on container width
- Never call `prepare()` inside the animation loop — it's the expensive one-time pass. Cache it.
- Never omit `document.fonts.ready.then(...)` — measure after fonts load, not before
- Never use pure black (`#000000`) — use rich off-blacks (`#06060a`, `#08080e`, `#0a0a0c`)
- Never build line strings when you only need geometry — use `walkLineRanges` instead of `layoutWithLines`
- Never position text with CSS flow — use `position: absolute` and place lines from Pretext coordinates
- Never pick one side of an obstacle when the obstacle is in the middle — use `carveTextLineSlots` to fill both sides
- Never create/destroy DOM elements per frame — use element pooling (`syncPool`)

### opentype.js
- Never use `.woff2` files — opentype.js cannot parse them. Use `.woff` or `.ttf` only
- Never use `opentype.load()` — use `fetch().then(r => r.arrayBuffer()).then(opentype.parse)` for better error handling
- Never render glyphs at absolute positions then try to move them — render at `(0,0)` and position via `<g transform="translate(x,y)">`
- Never forget `font.unitsPerEm` — the scale factor is `fontSize / font.unitsPerEm`
- Never call `glyph.getPath()` inside a tight loop without caching — cache the pathData string, regenerate only when position changes
- Never skip kerning — always check `font.getKerningValue(glyph, nextGlyph) * scale` between adjacent glyphs
- Never use Google Fonts TTF CDN URLs (they return 404 for programmatic access) — use `@fontsource` via jsdelivr

## Post-Generation QA

```bash
python3 ~/.claude/skills/pretext/scripts/validate_pretext.py output.html
```

Checklist:
1. ESM import from `esm.sh/@chenglou/pretext` present
2. `<script type="module">` tag
3. Named font declaration (no `system-ui`)
4. `<meta name="viewport">` present
5. Window resize handler
6. `document.fonts.ready` awaited before measurement
7. `requestAnimationFrame` loop (for animated effects)
8. Touch event handlers (for interactive effects)
9. No `setInterval` for animation
10. No framework imports
