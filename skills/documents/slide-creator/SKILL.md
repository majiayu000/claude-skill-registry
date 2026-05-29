---
name: slide-creator
description: Use when creating slide decks with Marp/Marpit Markdown (marp), including authoring slide content, designing slide color schemes, and building SVG diagrams or illustrations for the deck.
---

# Slide Creation Toolkit

Create professional Marp/Marpit presentations, diagrams, and color systems with a consistent design language.

## Core rules

- **Use `bg` (background) syntax for all images** - Reduces manual resizing with `fit` modifier
- Define one 7-role color palette and reuse it in slides and SVGs.
- Define one spacing unit (e.g., 8px or 16px) and reuse it across layouts.
- Define text hierarchy tiers (title/section/body) with sizes and weights; use them consistently.
- For SVGs, use one stroke width and one corner radius across shapes.

## Design guidance (non-enforceable)

- Aim for clear visual hierarchy with size, weight, and saturation.
- Prefer one visual language (fill vs outline, emphasis rules).
- Minimize visual noise; keep one primary visual anchor per section.

## Working directory

This umbrella skill does not own module assets or scripts.
Use the focused skills (`marp-authoring`, `slide-color-design`, `svg-illustration`) for paths and commands.

## Start here (task entry)

**Entry skills (fast routing)**:
- `marp-authoring` → Marp/Marpit authoring rules, layouts, themes
- `slide-color-design` → palette workflow and color roles
- `svg-illustration` → SVG diagram rules, patterns, embedding

Pick one task and follow the exact reading path:

- **Color palette only** → `slide-color-design`
- **Slides only (no diagrams)** → `marp-authoring`
- **Diagram only** → `svg-illustration`
- **Slides + diagrams** → `marp-authoring` → `svg-illustration`
- **Full deck (colors + slides + diagrams)** → `slide-color-design` → `marp-authoring` → `svg-illustration`

## One-page quick reference

**Minimal steps (fast path)**:
1. Pick a palette → `slide-color-design`.
2. Draft slides → `marp-authoring`.
3. Add SVG diagrams → `svg-illustration`.
4. Validate via the module skills.

**Common commands**:
- `slide-color-design` → palette scripts
- `marp-authoring` → Marp validation/preview
- `svg-illustration` → SVG linting

**Output summary**: Use module-specific output examples via the entry skills.

## Quick Start

### Two Ways to Start

**Option 1: Use scripts** (automated):
```bash
uv run skills/marp-authoring/scripts/init_presentation.py technical-dark my-deck.md "My Title" "Author"
```

**Option 2: Work manually** (full control):
- Copy a template from `marp-authoring` → `assets/templates/` → customize
- Design colors via `slide-color-design`
- Write slides via `marp-authoring`
- Add diagrams via `svg-illustration`

**Study examples first**: Read `marp-authoring` → `assets/examples/` to see working presentations before starting.

### Script Commands

Use `slide-color-design` for palette scripts and outputs.

**Templates** (starting points - copy and fill in your content):
- Use `marp-authoring` → `assets/templates/`.

**Examples** (learning references - study patterns and copy techniques):
- `marp-authoring` → `assets/examples/` for slide patterns.
- `svg-illustration` → `assets/examples/` for diagram examples.
- `slide-color-design` → `assets/examples/` for palette examples.

**Common icons** (ready to use in slides):
- `marp-authoring` → `assets/icons/`.

## Quick index (where to look)

- **Reference hub**: `references/index.md`
- **Color design**: `slide-color-design`
- **Marpit authoring**: `marp-authoring`
- **SVG illustration**: `svg-illustration`
- **Decision guide**: `references/decision-guide.md`

## Modules

Use the focused skills for module-specific rules and references:

- **Color design** → `slide-color-design`
- **Marpit authoring** → `marp-authoring`
- **SVG illustration** → `svg-illustration`

## Workflow

### Single tasks

Draw a diagram:
1. Use `svg-illustration` for core rules and patterns.
2. Choose colors via `slide-color-design` or existing palette.

Design slide colors:
1. Use `slide-color-design` for workflow and templates.

Write slides:
1. Use `marp-authoring` for syntax and layout patterns.
2. Apply a palette from `slide-color-design`.

### Full presentation

1. Establish a palette with the color module.
2. Outline slides and author via `marp-authoring`.
3. Add diagrams via `svg-illustration`.
4. Keep palette, spacing, and hierarchy consistent.

## Decision guide

See [references/decision-guide.md](references/decision-guide.md) for a flowchart and loading strategy.

Quick rules:
```
Slides or deck -> marp-authoring
Slides + colors -> slide-color-design -> marp-authoring
Slides + diagrams -> marp-authoring + svg-illustration
Diagram only -> svg-illustration
```

Scale reference loading:
```
Simple request -> core rules only
Complex request -> add patterns and best-practices
```

## Output formats

Use the focused skills for module-specific output formats:
- `slide-color-design` → `references/output-examples.md`
- `marp-authoring` → `references/output-examples.md`
- `svg-illustration` → `references/output-examples.md`

## Integration rules

- Use palette hex values in SVG `fill` and `stroke`.
- Keep border radius and stroke widths consistent between Marpit and SVG.
- Embed SVGs with Markdown images or file references.

## Troubleshooting

Common cross-cutting issues:
- [references/troubleshooting-common.md](references/troubleshooting-common.md)
- [svg-illustration](../svg-illustration/SKILL.md) → `references/troubleshooting.md`

## Common mistakes

- Using absolute paths instead of relative paths for assets.
- Using multiple palettes across one deck or between slides and SVGs.
- Skipping validation checks (Marp, SVG lint, contrast).

See `marp-authoring`, `slide-color-design`, and `svg-illustration` for module-specific mistakes.

## Quick check (minimal)

Use module-specific quick checks:
- `marp-authoring` → validation/preview workflow
- `svg-illustration` → SVG lint checks
- `slide-color-design` → contrast checks

## Validation

Use the module-specific validation guides:
- `marp-authoring` → `references/preview-workflow.md`
- `svg-illustration` → `references/troubleshooting.md`
- `slide-color-design` → `references/color-design/workflow.md` (validation checklist)

Always validate before committing files using the focused skills.

## Constraints

- Output Marpit Markdown only; do not generate PowerPoint/Keynote files.
- Output SVG only; do not generate raster images.
- Avoid interactive animations; keep slides static.
- Preserve provided brand colors; adapt them into the palette.
