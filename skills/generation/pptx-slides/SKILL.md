---
name: pptx-slides
description: Used when the user asks to "create a PowerPoint", "generate PPTX slides", "make a PowerPoint presentation", "build a .pptx deck", "create editable slides", "PptxGenJS", "editable presentation", "corporate deck", "slide deck for sharing", or when the output format is PPTX for any presentation task. Also triggers on "export to PowerPoint", "pitch deck PPTX", "offline presentation", or when the context implies an editable/corporate format. Generates OOXML-compliant .pptx files with PptxGenJS, precise layout, text measurement, and overlap validation.
version: 0.4.0
---

# PPTX Slides — Programmatic PowerPoint Generation

Generate professional, editable PowerPoint presentations using PptxGenJS (Node.js). Produces OOXML-compliant `.pptx` files with precise layout, text measurement, and overlap validation.

## Bundled Helpers

Every PPTX generation script imports the bundled TypeScript helper modules via bun:

```typescript
import pptxgen from 'pptxgenjs';
import * as h from '${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts';
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9'; // 10" × 5.625"
```

Run generation scripts with bun (no build step needed):
```bash
npx -y bun ${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts theme list
```

Dependencies (`skia-canvas`, `fontkit`, `linebreak`, `prismjs`) are auto-installed by bun on first run — no manual install step needed.

### Module Summary

| Module | Key Exports | Purpose |
|--------|-------------|---------|
| **text** | `autoFontSize()`, `calcTextBoxHeightSimple()`, `scale()` | Font-aware text measurement via skia-canvas, adaptive sizing |
| **theme** | `createTheme()`, `PRESETS`, `sectionBackground()` | Design token system with 12 curated presets |
| **layout** | `warnIfSlideHasOverlaps()`, `alignSlideElements()`, `distributeSlideElements()` | Overlap detection, bounds checking, positioning |
| **layout_builders** | `addFeatureGrid()`, `addCardRow()`, `addTimeline()`, `addMetricsRow()`, `addComparisonTable()` | High-level component builders |
| **decorative** | `addStaircase()`, `addSectionBadge()`, `addProgressBar()`, `addSlideNumber()` | Visual personality elements |
| **validation** | `validateDeck()` | Consolidated pre-save quality validation |
| **code** | `codeToRuns()` | Prism.js syntax highlighting to PptxGenJS text runs |
| **image** | `getImageDimensions()`, `imageSizingCrop()`, `imageSizingContain()` | Binary dimension detection and aspect-ratio sizing |
| **svg** | `svgToDataUri()` | SVG sanitization and base64 data URI encoding |
| **util** | `safeOuterShadow()`, `normalizeColor()`, `inchesToEmu()` | Shadow effects, color/unit conversion |

## Theme Selection

Pick a curated preset or create a custom theme:

```javascript
// Use a preset
const theme = h.createTheme(h.PRESETS.darkMonospace);

// Or customize
const theme = h.createTheme({
  accent: 'ff6b35',
  font: { heading: 'Poppins', body: 'Inter' },
});
```

**Available presets**: darkMonospace, swissModern, boldSignal, darkBotanical, cleanCorporate, neonCyber, warmMinimal, vintageEditorial, terminalGreen, gradientWave, midnightBlue, paperInk.

For mixed-background decks, define a section map:
```javascript
const sectionMap = { '0': 'brand', '1-3': 'light', '4-8': 'default' };
const colors = { brand: theme.accent, light: theme.bg.secondary, default: theme.bg.primary };
slide.background = { color: h.sectionBackground(slideIndex, sectionMap, colors) };
```

### Adaptive Font Sizing

Use `scale()` instead of hardcoded font sizes — the PPTX equivalent of CSS `clamp()`:

```javascript
const titleSize = h.scale(theme.size.title.min, theme.size.title.max, { bullets: 0, textLength: title.length });
const bodySize = h.scale(theme.size.body.min, theme.size.body.max, { bullets: 5, textLength: 800 });
```

For precise text box fitting, use `autoFontSize()` with skia-canvas measurement:
```javascript
const opts = h.autoFontSize('Long paragraph text...', 'Arial', { w: 8, h: 3, minFontSize: 14, maxFontSize: 28 });
slide.addText(text, { x: 1, y: 1.5, ...opts });
```

## Generation Workflow

1. **Plan layout** — Map content outline to slide types from `references/slide-patterns.md`
2. **Select theme** — Pick preset or define custom theme tokens
3. **Generate slides** — Build with helpers: `addFeatureGrid()`, `addCardRow()`, etc.
4. **Validate** — Run `h.validateDeck(pptx)` before saving
5. **Fix issues** — Adjust based on validation report, re-validate
6. **Deliver** — Provide `.pptx` file with speaker notes on every content slide

## Core Design Rules

### Typography
- **Minimum body text**: 18pt (24-28pt preferred). Use `scale()` for adaptive sizing.
- **Title text**: 36-44pt
- **Caption/footnote**: 14-16pt minimum (absolute floor: 14pt)
- **Font families**: Use `h.resolveFont(theme, 'heading')` for proper fallback chains

### Layout
- **Slide dimensions**: 10" × 5.625" (widescreen 16:9)
- **Safe margins**: 0.5" from all edges (`theme.spacing.margin`)
- **White space**: Target 40-50% empty space per slide
- **Alignment**: Use `h.alignSlideElements()` and `h.distributeSlideElements()` for precision

### Color & Accessibility
- **Contrast ratio**: WCAG AA minimum (4.5:1 body, 3:1 large text)
- **Color-blind safe**: Wong or IBM palettes for data visualization
- **Theme tokens**: Always use `theme.text.primary`, `theme.accent` — never hardcode colors

## Validation Workflow

Run `h.validateDeck(pptx)` before saving every deck. It checks:
- Element overlaps on every slide
- Elements within slide boundaries
- Font sizes above 14pt minimum
- Bullet count per slide (max 6)
- Speaker notes presence

## Anti-Patterns

- Text smaller than 14pt anywhere
- More than 6 bullets per slide
- Elements extending beyond slide boundaries
- Hardcoded colors instead of theme tokens
- Hardcoded font sizes instead of `scale()` or `autoFontSize()`
- Skipping `validateDeck()` before saving
- Missing speaker notes on content slides
- Using PptxGenJS `fit` or `autoFit` instead of `h.autoFontSize()`

## Editability Guidance

Design for editability — recipients must be able to modify the deck:
- **Native text boxes** — Click and edit directly. Never flatten text into images.
- **Group related elements** — Card layouts move as a unit.
- **Native shapes** — Use rounded rectangles, circles, lines instead of embedded SVG where possible.
- **Speaker notes** — Add talking points via `slide.addNotes('...')` on every content slide.
- **Master layouts** — For template decks, define slide layouts for consistent new slides.

## Architecture Diagrams with Shapes

Build architecture diagrams using PptxGenJS native shapes rather than images:
- **Rectangles** for services/components: `slide.addShape('rect', { ... })`
- **Lines and arrows** for connections: `slide.addShape('line', { ... })`
- **Color coding**: Use `theme.accent` for active components, `theme.text.secondary` for inactive
- **Progressive revelation**: Build the same diagram across 2-3 slides, adding complexity

## Reference Files

- **`references/pptxgenjs-helpers.md`** — Full API reference for bundled helper modules
- **`references/slide-patterns.md`** — Detailed slide type patterns with dimensions and positioning

## Script Files

- **`scripts/main.ts`** — TypeScript CLI entry point and library re-exports (run via `npx -y bun`)
- **`scripts/types.ts`** — Shared TypeScript interfaces for all helper modules
- **`scripts/theme.ts`** — 12 curated theme presets with `createTheme()` and `resolveFont()`
- **`scripts/text.ts`** — Font-aware text measurement via skia-canvas, `autoFontSize()`, `scale()`
- **`scripts/layout.ts`** — Overlap detection, element alignment, bounds checking
- **`scripts/layout_builders.ts`** — `addFeatureGrid()`, `addCardRow()`, `addTimeline()`, etc.
- **`scripts/decorative.ts`** — `addStaircase()`, `addSectionBadge()`, `addProgressBar()`
- **`scripts/validation.ts`** — `validateDeck()` pre-save quality validation
- **`scripts/code.ts`** — Prism.js syntax highlighting to PptxGenJS text runs
- **`scripts/image.ts`** — Binary dimension detection and aspect-ratio sizing
- **`scripts/svg.ts`** — SVG sanitization and base64 data URI encoding
- **`scripts/util.ts`** — Shadow effects, color normalization, unit conversion
