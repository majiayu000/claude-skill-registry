---
name: pretext
description: Generate self-contained HTML pages using the Pretext text measurement & layout library. This skill should be used when creating text effects that CSS cannot achieve — proportional typographic ASCII art, calligrams, shrinkwrap bubbles, obstacle-aware text reflow, masonry layouts, and multi-column editorial engines. All output is a single HTML file with zero build step.
argument-hint: [effect description or category]
---

# Pretext Text Effects

Generate browser pages powered by Pretext (`@chenglou/pretext`)—a pure-arithmetic text measurement library that bypasses DOM layout reflow entirely. Pretext measures text with proportional font precision using canvas `measureText`, enabling effects impossible with CSS alone.

Output is always a **single self-contained HTML file**. No build step, no framework, runs in any modern browser.

## Quick Start

Describe a text effect. Claude picks the right Pretext pattern and generates a complete HTML file.

Examples:
- `/pretext fluid smoke ASCII art with gold characters on black`
- `/pretext chat bubbles that shrinkwrap tighter than CSS`
- `/pretext calligram — the word "ocean" shaped like a wave`
- `/pretext editorial layout with text flowing around draggable circles`
- `/pretext masonry grid of shower thoughts with instant height prediction`

## Effect Categories

| Category | Pretext APIs Used | When to Use |
|----------|-------------------|-------------|
| **Height Prediction** | `prepare` + `layout` | Accordion, masonry, virtualized lists — anywhere you need text height without DOM reads |
| **Shrinkwrap** | `walkLineRanges` + binary search | Chat bubbles, tooltips, labels — finding the exact tightest width for multiline text |
| **Obstacle Routing** | `layoutNextLine` (variable width) | Text flowing around images, logos, draggable orbs — editorial layouts |
| **Typographic ASCII** | `prepareWithSegments` (char measurement) | Fluid simulations, 3D wireframes, particle systems rendered as proportional characters |
| **Calligrams** | `prepareWithSegments` + SDF | Words rendered as shapes using their own letters — hearts, stars, spirals |
| **Multi-column Editorial** | All rich APIs combined | Magazine-style layouts with headline fitting, pull quotes, drop caps, column flow |

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
Import from CDN → prepare/prepareWithSegments → layout/layoutWithLines/walkLineRanges/layoutNextLine
                                                        ↓
                                              Position DOM elements or draw to canvas
                                                        ↓
                                              requestAnimationFrame (if animated)
                                              resize handler (always)
```

### CDN Import (required in every output file)

```html
<script type="module">
import { prepare, layout, prepareWithSegments, layoutWithLines, walkLineRanges, layoutNextLine, clearCache } from 'https://esm.sh/@chenglou/pretext@0.0.2'
</script>
```

Import only the functions you need. Pin the version.

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
| Orb count | 1–6 | 3 |
| Orb radius | 30–120px | 60–90 |

## References

| Working on... | Load |
|---|---|
| Full API surface, types, caveats | `references/api-reference.md` |
| Typographic palette, brightness, ASCII grid | `references/typographic-ascii.md` |
| Column flow, obstacles, headline fitting | `references/obstacle-routing.md` |
| SDF shapes, proportional spacing, animation | `references/calligram-shapes.md` |
| Working accordion template | `assets/templates/height-prediction.html` |
| Working bubbles template | `assets/templates/shrinkwrap-bubbles.html` |
| Working editorial template | `assets/templates/editorial-engine.html` |
| Working ASCII art template | `assets/templates/typographic-ascii.html` |
| Working calligram template | `assets/templates/calligram.html` |

## Anti-Patterns

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
