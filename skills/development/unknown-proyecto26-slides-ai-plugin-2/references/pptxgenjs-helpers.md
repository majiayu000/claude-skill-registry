# PptxGenJS Helper Functions Reference

Complete API reference for bundled PptxGenJS TypeScript helper modules. Run via `npx -y bun`. All measurements in inches unless specified otherwise.

## Quick Import

```typescript
import pptxgen from 'pptxgenjs';
import * as h from '${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts';
```

Or run CLI commands directly:
```bash
npx -y bun ${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts theme list
npx -y bun ${CLAUDE_PLUGIN_ROOT}/skills/pptx-slides/scripts/main.ts validate <deck.pptx>
```

---

## text.ts

Text measurement and font sizing utilities.

### calcTextBoxHeightSimple

```typescript
calcTextBoxHeightSimple(fontSize: number, lines?: number, leading?: number, padding?: number): number
```

Returns: `number` - Height in inches
Analytical height calculation for a text box given font size and line count.
Example: `h.calcTextBoxHeightSimple(14, 2, 1.2, 0.3)` // 0.65 inches

### calcTextBox

```typescript
calcTextBox(fontSizePt: number, opts?: TextBoxOpts): TextBoxLayout
```

Returns: `TextBoxLayout` - `{ w, h, lines, contentH, margins, topInset }`
Comprehensive text box measurement with mode-based layout (by lines, width, or height).
Example: `h.calcTextBox(14, { text: 'Hello', fontFace: 'Arial', w: 4 })`

### autoFontSize

```typescript
autoFontSize(textOrRuns: string | TextRun[], fontFace: string, opts?: AutoFontSizeOpts): AutoFontSizeOpts
```

Returns: `AutoFontSizeOpts` - Options object with computed fontSize
Binary search for optimal font size to fit text in a box. Modes: 'shrink', 'enlarge', 'auto'.
Example: `h.autoFontSize('Long text', 'Arial', { w: 3, h: 1.5, mode: 'shrink' })`

### scale

```typescript
scale(min: number, max: number, density?: { bullets?: number; textLength?: number }): number
```

Returns: `number` - Scaled font size value (PPTX equivalent of CSS `clamp()`)
Example: `h.scale(theme.size.title.min, theme.size.title.max, { bullets: 0, textLength: title.length })`

---

## theme.ts

Theme creation and management with 12 curated presets.

### createTheme

```typescript
createTheme(overrides?: Partial<ThemeConfig>): SlideTheme
```

Returns: `SlideTheme` - Frozen theme object with all properties resolved
Create a new theme by merging overrides with default theme.
Example: `const theme = h.createTheme({ accent: 'ff0000' })`

### PRESETS

```typescript
PRESETS: Record<string, ThemeConfig>
```

Available presets: darkMonospace, swissModern, boldSignal, darkBotanical, cleanCorporate, neonCyber, warmMinimal, vintageEditorial, terminalGreen, gradientWave, midnightBlue, paperInk.
Use with `h.createTheme(h.PRESETS.swissModern)` to apply a preset.

### sectionBackground

```typescript
sectionBackground(slideIndex: number, sectionMap: Record<string, string>, colors: Record<string, ColorHex>): ColorHex
```

Returns: `ColorHex` - Hex color code for the slide's section
Determine background color for a slide based on section mapping.
Example: `h.sectionBackground(5, { '0-3': 'primary', '4-10': 'secondary' }, { primary: '0a0a0a', secondary: '1a1a1a' })`

### resolveFont

```typescript
resolveFont(theme: SlideTheme, role: 'heading' | 'body' | 'mono'): string
```

Returns: `string` - Font family with fallback chain
Example: `h.resolveFont(theme, 'heading')` // 'Clash Display, Arial'

---

## layout.ts

Slide layout and element positioning utilities.

### inferElementType

```typescript
inferElementType(obj: any): string
```

Returns: `string` - Type name ('text', 'image', 'shape', 'line', 'chart', 'table', etc.)
Example: `h.inferElementType(slideObjects[0])` // 'text'

### warnIfSlideHasOverlaps

```typescript
warnIfSlideHasOverlaps(slide: any, pptx: any, options?: OverlapWarningOpts): void
```

Detect and report overlapping elements with detailed geometry analysis.
Example: `h.warnIfSlideHasOverlaps(slide, pptx, { muteContainment: true })`

### warnIfSlideElementsOutOfBounds

```typescript
warnIfSlideElementsOutOfBounds(slide: any, pptx: any): void
```

Check that all slide elements stay within slide boundaries.

### alignSlideElements

```typescript
alignSlideElements(slide: any, indices: number[], alignment: string): void
```

Align selected slide elements. Alignments: 'left', 'right', 'top', 'bottom', 'horizontallyCenter', 'verticallyCenter'.
Example: `h.alignSlideElements(slide, [0, 1, 2], 'horizontallyCenter')`

### distributeSlideElements

```typescript
distributeSlideElements(slide: any, indices: number[], direction: 'horizontal' | 'vertical'): void
```

Distribute selected elements evenly.
Example: `h.distributeSlideElements(slide, [0, 1, 2, 3], 'horizontal')`

### getSlideDimensions

```typescript
getSlideDimensions(slide: any, pptx: any): SlideDimensions
```

Returns: `SlideDimensions` - `{ width, height, source }`
Detect slide dimensions from PptxGenJS internals.
Example: `const { width, height } = h.getSlideDimensions(slide, pptx)` // { width: 10, height: 5.625 }

---

## layout_builders.ts

High-level slide layout components.

### addImageTextCard

```typescript
addImageTextCard(slide: any, opts?: CardRowOpts): void
```

Create an image + caption card. Opts: `x, y, width, gap, image { path, data, boxHeight, sizing, crop }, text, textBox`.
Example: `h.addImageTextCard(slide, { x: 0.5, y: 0.5, width: 3, image: { path: 'photo.jpg', boxHeight: 2 }, text: 'Caption' })`

### addCardRow

```typescript
addCardRow(slide: any, cards: CardRowOpts[], region: { x: number; y: number; w: number; h: number }, options?: { gap?: number }): void
```

Row of image-text cards with auto-spacing.
Example: `h.addCardRow(slide, [{ image: {...}, text: 'A' }, {...}], { x: 0.5, y: 1, w: 9, h: 2 })`

### addThreeLevelTree

```typescript
addThreeLevelTree(slide: any, opts: { x: number; y: number; w: number; h: number; theme: SlideTheme; root: { title: string; children: any[] } }): void
```

Hierarchical tree layout with three levels.

### addFeatureGrid

```typescript
addFeatureGrid(slide: any, opts: FeatureGridOpts & { cols?: number; rows?: number; theme: SlideTheme }): void
```

Grid layout for features (max 6 cards).
Example: `h.addFeatureGrid(slide, { x: 0.5, y: 1.2, w: 9, h: 3.8, cols: 3, rows: 2, features: [...] })`

### addComparisonTable

```typescript
addComparisonTable(slide: any, opts: ComparisonTableOpts & { theme: SlideTheme }): void
```

Side-by-side comparison layout.

### addMetricsRow

```typescript
addMetricsRow(slide: any, opts: MetricsRowOpts & { theme: SlideTheme }): void
```

Horizontal metrics cards with large numbers and labels.

### addTimeline

```typescript
addTimeline(slide: any, opts: TimelineOpts & { theme: SlideTheme }): void
```

Horizontal timeline with markers and descriptions.

---

## decorative.ts

Decorative slide elements and styling.

### addStaircase

```typescript
addStaircase(slide: any, opts?: StaircaseOpts): void
```

Diagonal staircase pattern. Opts: `position ('bottom-right'), color, steps, stepWidth, stepHeight, opacity`.
Example: `h.addStaircase(slide, { position: 'bottom-right', color: '4a9eff', steps: 4 })`

### addSectionBadge

```typescript
addSectionBadge(slide: any, text: string, position: BadgeOpts, theme: SlideTheme): void
```

Small badge label.
Example: `h.addSectionBadge(slide, 'NEW', { x: 0.5, y: 0.3 }, theme)`

### addProgressBar

```typescript
addProgressBar(slide: any, current: number, total: number, theme: SlideTheme, opts?: ProgressBarOpts): void
```

Progress bar showing current/total.
Example: `h.addProgressBar(slide, 3, 10, theme, { position: 'bottom', height: 0.04 })`

### addSectionDivider

```typescript
addSectionDivider(slide: any, heading: string, theme: SlideTheme): void
```

Full-slide section break using theme background colors.

### addSlideNumber

```typescript
addSlideNumber(slide: any, number: number, total: number, theme: SlideTheme, opts?: { x?: number; y?: number; w?: number; h?: number }): void
```

Slide counter in corner.
Example: `h.addSlideNumber(slide, 5, 25, theme, { x: 9.2, y: 5.2 })`

---

## validation.ts

Deck-level validation and diagnostics.

### validateDeck

```typescript
validateDeck(pptx: any, opts?: Record<string, any>): ValidationReport
```

Returns: `ValidationReport` - `{ passed, issues, warnings, stats }`
Validate entire presentation. Checks: font sizes (14pt min), bullet counts (6 max), bounds, speaker notes.
Example: `const report = h.validateDeck(pptx); console.log(report.issues)`

---

## code.ts

Syntax-highlighted code formatting.

### codeToRuns

```typescript
codeToRuns(code: string, lang?: string): CodeRun[]
```

Returns: `CodeRun[]` - Array of text runs with syntax highlighting
Convert code string to syntax-highlighted text runs for PptxGenJS.
Example: `const runs = h.codeToRuns('const x = 1;', 'javascript')`

### buildThemeMap

```typescript
buildThemeMap(themeCssModule?: string): Record<string, string>
```

Returns: Token type to color mapping from Prism.js theme CSS.

---

## image.ts

Image handling and sizing utilities.

### getImageDimensions

```typescript
getImageDimensions(source: string | Buffer): ImageDimensions
```

Returns: `ImageDimensions` - `{ width, height, aspectRatio, type }`
Read image dimensions from file path, data URI, or buffer. Auto-detects PNG, JPEG, GIF, WebP, SVG.
Example: `const dims = h.getImageDimensions('photo.jpg')` // { width: 1920, height: 1080, aspectRatio: 1.778 }

### imageSizingCrop

```typescript
imageSizingCrop(source: string | Buffer, x: number, y: number, w: number, h: number, cx?: number, cy?: number, cw?: number, ch?: number): ImageSizingCropResult
```

Create crop sizing to fill bounds. Crop center (cx, cy) and crop box (cw, ch) optional.

### imageSizingContain

```typescript
imageSizingContain(source: string | Buffer, x: number, y: number, w: number, h: number): ImageSizingContainResult
```

Create contain sizing to fit within bounds preserving aspect ratio.

---

## svg.ts

SVG utilities and data URI conversion.

### svgToDataUri

```typescript
svgToDataUri(svg: string): string
```

Sanitize SVG and convert to base64 data URI in one step.
Example: `const uri = h.svgToDataUri('<svg>...</svg>')`

### sanitizeSvg

```typescript
sanitizeSvg(svg: string): string
```

Clean and normalize SVG: add xmlns, remove XML declaration, convert em/ex units to px, replace currentColor.

---

## util.ts

Utility functions for color, unit, and shadow handling.

### safeOuterShadow

```typescript
safeOuterShadow(color?: ColorHex, opacity?: number, angle?: number, blur?: number, offset?: number): ShadowConfig
```

Create a safe outer shadow object for slide elements.
Example: `h.safeOuterShadow('000000', 0.2, 45, 3, 2)`

### inchesToEmu

```typescript
inchesToEmu(inches: number): number
```

Convert inches to English Metric Units (914400 per inch).

### emuToInches

```typescript
emuToInches(emu: number): number
```

Convert EMU to inches.

### normalizeColor

```typescript
normalizeColor(color: string): ColorHex
```

Validate and normalize hex color string (strips `#` prefix).
Example: `h.normalizeColor('#4a9eff')` // '4a9eff'

### clampValue

```typescript
clampValue(value: number, min: number, max: number): number
```

Constrain a value between min and max.

---

## TypeScript Types

All shared types are defined in `scripts/types.ts`. Key interfaces:

- `SlideTheme` — Fully resolved theme with bg, text, accent, font, size, spacing, radius, shadow
- `ThemeConfig` — Partial theme for overrides / presets
- `ValidationReport` — `{ passed, issues, warnings, stats }`
- `ValidationIssue` — `{ slide, type, message, severity }`
- `AutoFontSizeOpts` — Options for text fitting (w, h, mode, minFontSize, maxFontSize)
- `TextBoxLayout` — Calculated text box dimensions
- `ImageDimensions` — `{ width, height, aspectRatio, type }`
- `StaircaseOpts`, `BadgeOpts`, `ProgressBarOpts` — Decorative element options
- `FeatureGridOpts`, `CardRowOpts`, `TimelineOpts`, `MetricsRowOpts`, `ComparisonTableOpts` — Layout builder options
- `ColorHex`, `InchesUnit`, `PointsUnit` — Branded type aliases
