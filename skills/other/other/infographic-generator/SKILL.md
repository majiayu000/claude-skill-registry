---
name: generating-infographics
description: Use when creating infographics, data visualizations, process diagrams, timelines, or comparisons - generates branded infographics using @antv/infographic with 114 templates across 7 categories. Triggers on "create infographic", "make infographic", "visualize data", "timeline", "process diagram".
version: 2.9.0
allowed-tools: Read, Write, Glob, Bash
user-invocable: false
---

# Generating Infographics

Generate branded infographics with custom themes and backgrounds using @antv/infographic.

## Prerequisites

1. Run `/brand-init` to create project structure
2. Run `/brand-extract` to generate brand-philosophy.md
3. Run `/template-infographic` to create an infographic template

### No-Brand Safeguard

If `brand-philosophy.md` is not found OR contains no `## Color Palette` section:
- **STOP generation** — inform user: "No brand colors found. Run `/brand-extract` first to analyze your brand."
- If user insists on proceeding: use deliberately bland neutrals (#1a1a1a, #666, #f5f5f5, system fonts)
- Never fall back to any recognizable brand colors

## When to Use

- "Create an infographic"
- "Make a process diagram"
- "Visualize this data"
- "Create a timeline"
- "Show comparison infographic"
- NOT for: Charts/graphs (use charting library), presentations (use visual-content skill)

## Commands

| Command | Purpose |
|---------|---------|
| `/template-infographic` | Create infographic template |
| `/infographic` | Generate infographic (guided) |
| `/infographic-quick` | Generate infographic (fast) |

## Template Categories (114 Total)

| Category | Count | Use Cases | Icons | Illustrated |
|----------|-------|-----------|-------|-------------|
| Sequence | 43 | Timelines, steps, processes, roadmaps | ✓ (2) | ✓ (5) |
| List | 23 | Features, grids, pyramids, sectors | ✓ (4) | ✓ (1) |
| Hierarchy | 25 | Org charts, tree structures | — | — |
| Compare | 17 | VS, before/after, SWOT | — | — |
| Quadrant | 3 | 2x2 matrices | — | ✓ (1) |
| Relation | 2 | Networks, connections | ✓ (1) | — |
| Chart | 1 | Bar charts | — | — |

## Template Asset Types

| Type | Count | Identifier | Data Format |
|------|-------|------------|-------------|
| **Text-only** | 100+ | (default) | `{ "label": "Cloud", "desc": "Infrastructure" }` |
| **Icon-based** | 8 | `icon` in name | `{ "label": "icon:rocket", "desc": "Fast" }` |
| **Illustrated** | 9 | `-illus` suffix | `{ "label": "Step 1", "desc": "Discovery", "illus": "step-1" }` |

**Recommendation:** Start with text-only templates. Illustrated templates require custom image files.

### Illustrated Template Workflow

When using `-illus` templates:
1. Content includes `illus` field referencing image filename
2. Supported formats: SVG (recommended), PNG, JPG
3. Options: provide your own images, find icons, or use placeholders
4. Images stored with infographic output: `infographics/{date}-{name}/illustrations/`
5. See `references/illustrations.md` for detailed workflow

## Text Guidelines (Avoiding Overlap)

| Element | Max | Good | Bad |
|---------|-----|------|-----|
| Labels | 1-2 words | "Cloud" | "Cloud Computing Services" |
| Descriptions | 2-4 words | "Infrastructure design" | "Complete infrastructure design and implementation" |

If overlap occurs: shorten text, use wider canvas (1200px+), or use column/grid templates.

## Quick Reference

| Task | How |
|------|-----|
| Generate infographic | `node generate.js --config config.json --data '{...}' --output output.png` |
| Set background | `--background "spotlight-dots"` |
| SVG output | `--format svg` |

## Background Presets

**Layered (gradient + pattern):**
| Preset | Effect |
|--------|--------|
| `spotlight-dots` | Radial spotlight + subtle dots (recommended) |
| `spotlight-grid` | Radial spotlight + grid lines |
| `diagonal-crosshatch` | Diagonal fade + crosshatch |
| `tech-matrix` | Tech gradient + dense grid |

**Simple (gradient or pattern only):**
| Preset | Effect |
|--------|--------|
| `spotlight` | Radial gradient only |
| `diagonal-fade` | Corner to corner fade |
| `top-down` | Vertical fade |
| `subtle-dots` | Light dot pattern |
| `tech-grid` | Grid lines |
| `crosshatch` | Diagonal crosshatch |
| `solid` | Plain solid color |

## Workflow

### 1. Create Template (once)
```
/template-infographic
```
Select: category → design → palette → background → style

### 2. Generate Infographic (repeat)
```
/infographic-quick
```
Select template → paste content → name → get PNG

## Accessibility & Readability (MANDATORY)

**These checks are NON-NEGOTIABLE before generating any infographic.**

### Contrast Validation (WCAG AA)

| Requirement | Value |
|-------------|-------|
| Minimum contrast ratio | **4.5:1** for all text |
| Large text (title) | 3:1 acceptable |
| Standard | WCAG 2.1 AA |

**Key principle:** Palette colors are for SHAPES and FILLS, not text. Text needs explicit high-contrast colors.

### Text Color Rules by Background

| Background Type | Title Fill | Description Fill | Label Fill |
|-----------------|------------|------------------|------------|
| **Dark** (spotlight-dots, tech-matrix) | White or near-white (WCAG >= 4.5:1) | White at ~85% opacity | White or near-white |
| **Light** (solid, subtle-dots) | Near-black (WCAG >= 4.5:1) | Dark gray | Near-black |

**Never use palette colors for text** - they're for decorative shapes only.

### Spacing & Balance Rules

| Element | Requirement |
|---------|-------------|
| **Item spacing** | Minimum 20px between items |
| **Edge margins** | Never touch canvas edges (min 5% padding) |
| **Text truncation** | Labels 1-2 words, descriptions 2-4 words |
| **Visual balance** | Equal spacing between similar elements |

### Pre-Generation Checklist

```
□ All text has 4.5:1 contrast against background
□ Labels are 1-2 words (no overlap risk)
□ Descriptions are 2-4 words
□ Content fits template capacity (check item limits)
□ Dark bg → white text, Light bg → dark text
□ No text touching edges
□ colorBg derived from brand-philosophy.md, not from skill defaults
□ colorPrimary derived from brand-philosophy.md, not from skill defaults
□ Colors traced to brand-philosophy.md (not copied from reference docs or runtime fallbacks)
□ font-family from brand-philosophy.md, not a generic default
□ Text colors WCAG-validated against actual background
```

**If ANY check fails, DO NOT generate. Fix the content or config first.**

### Config Examples

**Dark Backgrounds (spotlight-dots, tech-matrix, etc.)**
```json
{
  "colorBg": "{brand-bg-dark}",
  "colorPrimary": "{brand-primary}",
  "title": { "fill": "#FFFFFF" },
  "desc": { "fill": "rgba(255,255,255,0.85)" },
  "item": {
    "label": { "fill": "#FFFFFF" },
    "desc": { "fill": "rgba(255,255,255,0.7)" }
  }
}
```

**Light Backgrounds (solid, subtle-dots, etc.)**
```json
{
  "colorBg": "#FFFFFF",
  "colorPrimary": "{brand-primary}",
  "title": { "fill": "#1A202C" },
  "desc": { "fill": "#4A5568" },
  "item": {
    "label": { "fill": "#1A202C" },
    "desc": { "fill": "#4A5568" }
  }
}
```

**Common mistake:** Using pastel palette colors for text on light backgrounds. Pastels are for decorative shapes only.

See template-infographic.md for complete config examples.

> **Note:** The `/template-infographic` command generates correct configs from your brand-philosophy.md.
> Never copy hex values from the examples above — they are illustrative placeholders only.

## Data Structure by Type

### Sequence/List
```json
{
  "title": "Our Process",
  "items": [
    { "label": "Step 1", "desc": "Discovery" },
    { "label": "Step 2", "desc": "Design" }
  ]
}
```

### Compare
```json
{
  "title": "Before vs After",
  "items": [
    { "label": "Before", "children": [{ "label": "Slow" }] },
    { "label": "After", "children": [{ "label": "Fast" }] }
  ]
}
```

### Hierarchy
```json
{
  "title": "Organization",
  "items": [{
    "label": "CEO",
    "children": [{ "label": "CTO" }, { "label": "CFO" }]
  }]
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Text overlapping | Shorten labels (1-2 words), descriptions (2-4 words) |
| Missing illustrations | Check template ends in `-illus`, provide SVG/PNG/JPG files |
| Icon not showing | Use `icon:name` syntax, only for icon templates |
| Background not applied | Pass `--background` flag to generate.js |
| Text invisible on light bg | Add explicit `title`/`desc`/`item` fills with dark colors (#1A202C, #4A5568) |
| Pastel text unreadable | Palette colors are for shapes only; text needs high contrast (~4.5:1) |

## References

- `references/templates.md` - Complete 114 template catalog with asset requirements
- `references/theming.md` - Theme configuration details
- `references/backgrounds.md` - Background customization guide
- `references/icons.md` - Available icons for icon-based templates
- `references/illustrations.md` - Illustrated template workflow and SVG requirements

## Module Structure

```
lib/
├── renderer.js       # Main entry point
├── dom-setup.js      # JSDOM environment
├── infographic.js    # Infographic creation
├── exporter.js       # SVG/PNG export
├── backgrounds.js    # Gradient/pattern backgrounds
└── icons.js          # Icon utilities
```
