---
name: "Graphic Design Skill"
description: "Patterns for visual design, SVG creation, layout composition, typography, and brand identity."
---

# Graphic Design Skill

> Patterns for visual design, SVG creation, layout composition, typography, and brand identity.

## Design Principles

### Visual Hierarchy

| Level | Purpose | Techniques |
| ----- | ------- | ---------- |
| **Primary** | First thing seen | Largest, boldest, highest contrast |
| **Secondary** | Supporting info | Medium size, moderate weight |
| **Tertiary** | Details | Smaller, lighter, subtle |

### Hierarchy Tools

- **Size** — Larger = more important
- **Weight** — Bolder = more attention
- **Color** — High contrast = focal point
- **Position** — Top/center = primary
- **Whitespace** — Isolation = emphasis

### Balance Types

| Type | Characteristics | Best For |
| ---- | --------------- | -------- |
| **Symmetrical** | Mirror image, formal | Corporate, traditional |
| **Asymmetrical** | Visual weight balanced, dynamic | Modern, creative |
| **Radial** | Elements radiate from center | Logos, icons |

## Layout & Composition

### Grid Systems

```text
┌─────┬─────┬─────┬─────┐
│  1  │  2  │  3  │  4  │   12-column grid
├─────┼─────┼─────┼─────┤   (most flexible)
│  5  │  6  │  7  │  8  │
├─────┼─────┼─────┼─────┤
│  9  │ 10  │ 11  │ 12  │
└─────┴─────┴─────┴─────┘
```

### Golden Ratio (1:1.618)

- Use for proportions that feel "right"
- Width to height relationships
- Spacing progressions
- Element sizing

### Rule of Thirds

```text
┌─────────┬─────────┬─────────┐
│         │    ●    │         │  Place key elements
├─────────┼─────────┼─────────┤  at intersection
│    ●    │         │    ●    │  points for dynamic
├─────────┼─────────┼─────────┤  composition
│         │    ●    │         │
└─────────┴─────────┴─────────┘
```

### Alignment Principles

| Principle | Rule |
| --------- | ---- |
| **Edge alignment** | Elements share common edges |
| **Center alignment** | Elements share center axis |
| **Baseline alignment** | Text shares baseline |
| **Optical alignment** | Visually aligned (may differ from mathematical) |

## Typography

### Type Scale (1.25 ratio)

| Level | Size | Use |
| ----- | ---- | --- |
| Display | 72px | Hero headlines |
| H1 | 48px | Page titles |
| H2 | 36px | Section headers |
| H3 | 28px | Subsections |
| Body | 16px | Main content |
| Caption | 12px | Supporting text |

### Font Pairing Rules

| Combination | Example | Vibe |
| ----------- | ------- | ---- |
| Serif + Sans | Georgia + Helvetica | Classic, professional |
| Sans + Sans | Montserrat + Open Sans | Modern, clean |
| Display + Body | Playfair + Source Sans | Elegant, editorial |

### Typography Best Practices

- **Line height**: 1.4–1.6× font size for body
- **Line length**: 45–75 characters optimal
- **Letter spacing**: Increase for ALL CAPS
- **Contrast**: Dark on light or light on dark
- **Hierarchy**: Max 3 font sizes per design

## Color Theory

### Color Relationships

```text
        Primary
           ●
          /|\
         / | \
        /  |  \
       ●───●───●
   Secondary  Tertiary
```

### Color Schemes

| Scheme | Description | Mood |
| ------ | ----------- | ---- |
| **Monochromatic** | One hue, varied lightness | Cohesive, elegant |
| **Complementary** | Opposite on wheel | High contrast, vibrant |
| **Analogous** | Adjacent on wheel | Harmonious, natural |
| **Triadic** | Three equidistant | Balanced, dynamic |
| **Split-complementary** | Base + two adjacent to complement | Softer contrast |

### Color Psychology

| Color | Associations | Use Cases |
| ----- | ------------ | --------- |
| **Blue** | Trust, stability, tech | Corporate, software |
| **Green** | Growth, nature, success | Health, finance |
| **Red** | Energy, urgency, passion | CTAs, alerts |
| **Purple** | Creativity, luxury | Premium, creative |
| **Orange** | Friendly, energetic | Social, youth |
| **Yellow** | Optimism, attention | Highlights, warnings |

### Contrast & Accessibility

| WCAG Level | Contrast Ratio | Use |
| ---------- | -------------- | --- |
| AA (normal) | 4.5:1 | Body text |
| AA (large) | 3:1 | 18px+ or 14px bold |
| AAA | 7:1 | Maximum accessibility |

### Applying Color Theory to Mermaid Diagrams

Color theory principles translate directly to Mermaid diagram styling. The **GitHub Pastel Palette v2** (defined in the **markdown-mermaid** skill) implements these principles:

**Semantic Color Mapping** (from color psychology):

| Semantic Purpose | Palette Color | Fill | Text | Stroke |
| ---------------- | ------------- | ---- | ---- | ------ |
| Primary actions | Blue | `#ddf4ff` | `#0550ae` | `#80ccff` |
| Success/output | Green | `#d3f5db` | `#1a7f37` | `#6fdd8b` |
| Business logic | Gold | `#fff8c5` | `#9a6700` | `#d4a72c` |
| Special/DevOps | Purple | `#d8b9ff` | `#6639ba` | `#bf8aff` |
| Errors/critical | Red | `#ffebe9` | `#cf222e` | `#f5a3a3` |
| Raw/ingestion | Bronze | `#fff1e5` | `#953800` | `#ffb77c` |
| Background | Neutral | `#eaeef2` | `#24292f` | `#d0d7de` |

**Design Principles Applied**:

1. **Triadic harmony**: Blue + Gold + Red form a balanced triad
2. **Analogous groups**: Green + Blue are adjacent, creating calm flow sections
3. **Light fills + dark text**: Ensures WCAG AA contrast (4.5:1+)
4. **Neutral arrows** (`#57606a`): Don't compete with colored nodes — visual hierarchy preserved
5. **Consistent stroke family**: Each color has a matching mid-tone stroke (not jarring black borders)

**When to Override the Palette**:
- Diagrams comparing two systems → Use just 2 contrasting colors (complementary scheme)
- Status dashboards → Green/Yellow/Red RAG mapping
- Sequential processes → Monochromatic gradient (light to dark within one hue)

## SVG Design

### SVG Structure

```xml
<svg viewBox="0 0 width height" xmlns="...">
  <defs>
    <!-- Reusable definitions -->
    <linearGradient id="grad1">...</linearGradient>
    <filter id="shadow">...</filter>
  </defs>

  <!-- Background layer -->
  <rect .../>

  <!-- Main content -->
  <g transform="translate(x, y)">
    <!-- Grouped elements -->
  </g>

  <!-- Foreground/overlay -->
</svg>
```

### Common SVG Elements

| Element | Use | Key Attributes |
| ------- | --- | -------------- |
| `<rect>` | Rectangles, backgrounds | x, y, width, height, rx (rounded) |
| `<circle>` | Circles, dots | cx, cy, r |
| `<ellipse>` | Ovals | cx, cy, rx, ry |
| `<line>` | Straight lines | x1, y1, x2, y2 |
| `<path>` | Complex shapes | d (path data) |
| `<text>` | Typography | x, y, text-anchor, dominant-baseline |
| `<g>` | Grouping | transform |

### SVG Path Commands

| Command | Meaning | Example |
| ------- | ------- | ------- |
| M | Move to | M 10 20 |
| L | Line to | L 30 40 |
| H | Horizontal line | H 50 |
| V | Vertical line | V 60 |
| Q | Quadratic curve | Q cx cy, x y |
| C | Cubic curve | C cx1 cy1, cx2 cy2, x y |
| Z | Close path | Z |

### SVG Text Alignment

```xml
<!-- Horizontal alignment -->
text-anchor="start|middle|end"

<!-- Vertical alignment -->
dominant-baseline="auto|middle|central|hanging"

<!-- Centered text -->
<text x="50%" y="50%" text-anchor="middle" dominant-baseline="central">
  Perfectly Centered
</text>
```

### SVG Gradients

```xml
<!-- Linear gradient -->
<linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stop-color="#007ACC"/>
  <stop offset="100%" stop-color="#00a8e8"/>
</linearGradient>

<!-- Radial gradient -->
<radialGradient id="glow" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#007ACC" stop-opacity="0.4"/>
  <stop offset="100%" stop-color="#007ACC" stop-opacity="0"/>
</radialGradient>
```

### SVG Transforms

| Transform | Syntax | Use |
| --------- | ------ | --- |
| Translate | translate(x, y) | Move element |
| Rotate | rotate(deg, cx, cy) | Spin around point |
| Scale | scale(x, y) | Resize |
| Skew | skewX(deg) / skewY(deg) | Shear |

## Banner & Marketing Design

### Banner Dimensions

| Platform | Size | Aspect |
| -------- | ---- | ------ |
| VS Code Marketplace | 1280×640 | 2:1 |
| GitHub Social | 1280×640 | 2:1 |
| Twitter Header | 1500×500 | 3:1 |
| LinkedIn Banner | 1584×396 | 4:1 |
| Open Graph | 1200×630 | ~1.9:1 |

### Banner Composition

```text
┌─────────────────────────────────────────┐
│  ┌─────────────────────────────────┐    │
│  │         VISUAL ELEMENT          │    │  Top third: Logo/Icon
│  └─────────────────────────────────┘    │
│                                         │
│           MAIN HEADLINE                 │  Middle: Primary message
│           Subtitle Text                 │
│                                         │
│  [Badge 1]  [Badge 2]  [Badge 3]        │  Bottom third: CTAs/Details
└─────────────────────────────────────────┘
```

### Badge/Pill Design

```xml
<!-- Rounded pill badge -->
<g>
  <rect x="-50" y="-16" width="100" height="32" rx="16"
        fill="#007ACC" opacity="0.15"/>
  <text x="0" y="0" text-anchor="middle" dominant-baseline="central"
        font-size="12" fill="#94a3b8">Label</text>
</g>
```

## Icon Design

### Icon Grid

```text
┌────────────────────┐
│ ┌──────────────┐   │  Outer: Padding zone
│ │              │   │  Inner: Safe area
│ │   CONTENT    │   │  Content: Icon artwork
│ │              │   │
│ └──────────────┘   │  Standard: 24×24, 16×16
└────────────────────┘
```

### Icon Principles

- **Simplicity** — Recognize at small sizes
- **Consistency** — Same stroke weight, style
- **Optical balance** — Visually centered, not mathematically
- **Metaphor** — Universally understood symbols

### Icon Styles

| Style | Characteristics | Use |
| ----- | --------------- | --- |
| **Outlined** | Stroke only, no fill | Light, modern UI |
| **Filled** | Solid shapes | Bold, clear visibility |
| **Duotone** | Two tones/colors | Distinctive, branded |
| **Glyph** | Single color, simplified | System icons |

## Design Systems

### Spacing Scale (8px base)

| Token | Value | Use |
| ----- | ----- | --- |
| xs | 4px | Tight spacing |
| sm | 8px | Default gap |
| md | 16px | Section spacing |
| lg | 24px | Component gaps |
| xl | 32px | Major sections |
| 2xl | 48px | Hero spacing |

### Elevation/Shadow

| Level | Shadow | Use |
| ----- | ------ | --- |
| 0 | None | Flat elements |
| 1 | 0 1px 2px | Subtle lift |
| 2 | 0 2px 4px | Cards |
| 3 | 0 4px 8px | Dropdowns |
| 4 | 0 8px 16px | Modals |

### Border Radius Scale

| Token | Value | Use |
| ----- | ----- | --- |
| none | 0 | Sharp corners |
| sm | 4px | Subtle rounding |
| md | 8px | Standard buttons |
| lg | 16px | Cards, pills |
| full | 9999px | Circles, pills |

## Design Review Checklist

### Visual Quality

- [ ] Consistent spacing throughout
- [ ] Aligned elements (check edges)
- [ ] Balanced composition
- [ ] Clear visual hierarchy
- [ ] Appropriate whitespace

### Typography

- [ ] Readable font sizes
- [ ] Proper line height
- [ ] Consistent font usage
- [ ] Good contrast ratios
- [ ] Appropriate letter spacing

### Color

- [ ] Consistent color palette
- [ ] Sufficient contrast
- [ ] Meaningful color use
- [ ] Works in different contexts
- [ ] Accessible (WCAG compliant)

### Technical

- [ ] Optimized file size
- [ ] Correct dimensions
- [ ] Responsive/scalable
- [ ] Cross-platform compatible
- [ ] Proper naming conventions

## Synapses

### High-Strength Connections

- [creative-writing] (High, Complements, Bidirectional) — "Visual storytelling"
- [vscode-extension-patterns] (High, Applies, Forward) — "Extension branding and UI"

### Medium-Strength Connections

- [markdown-mermaid] (Medium, Extends, Bidirectional) — "Diagram visualization"
- [cognitive-load] (Medium, Applies, Forward) — "Visual information processing"
- [ascii-art-alignment] (Medium, Complements, Bidirectional) — "Text-based visual design"

### Supporting Connections

- [writing-publication] (Low, Supports, Forward) — "Document visual design"
- [meditation-facilitation] (Low, Uses, Forward) — "Reflective design iteration"
