---
name: figma-mcp-layout-builder
description: Pull frames/components via Figma MCP, normalize messy or non-autolayout designs, and generate faithful HTML/CSS (or Shopify Liquid) layouts with inferred spacing and responsiveness.
---

# Figma MCP → Layout Builder

allowed-tools:

- extract_design_tokens

Use this to fetch Figma design data via MCP, clean it up (even when designers skipped Auto Layout), and produce a code layout that matches the design.

## Quick Start

- Confirm Figma MCP is configured; gather file key, page name/ID, frame IDs, target widths (desktop/mobile), and desired output stack (HTML/CSS vs. Liquid/section/snippet).
- Fetch data: pull JSON for target frame (geometry, fills, text styles) and an image export for visual reference.
- Normalize spacing/structure, map to flex/grid, and emit code plus a short QA checklist.

## Fetching Figma Data with MCP

- Request: file key, page, frame IDs. If missing, ask for a shared link and which frame(s) to target.
- Pull both **structure** (nodes with bounding boxes, text styles, fills, strokes, effects) and **preview** (PNG/JPEG) to cross-check.
- If the design changes, re-fetch the affected frames before coding.

## Heuristics When Auto Layout Is Missing

- **Group detection**: Cluster nodes whose edges align within 4–8px tolerance to identify rows/columns/cards.
- **Stack direction**: For a cluster, sort by Y (potential column) vs. X (potential row); pick the axis with smaller gap variance.
- **Gap inference**: Compute deltas between sorted positions; use the mode/median as the intended gap. Snap to 4/8px steps when plausible.
- **Padding**: Use the distance from child bounds to parent frame edges; if asymmetric, pick the common side value as base padding.
- **Alignment cleanup**: Round positions/sizes to nearest 2/4px to remove jitter; unify repeated widths/heights across siblings.
- **Grid guess**: If cards repeat, derive columns from min horizontal gap and card width; set `grid-template-columns: repeat(n, minmax(0, 1fr))`.
- **Typography/colors**: Collect distinct font families/weights/line-heights and hex colors; map recurring values to tokens.
- **Overlaps**: Preserve intentional overlays; otherwise prefer stacking with z-index only where overlap is clearly intended.

## Layout Synthesis

- Choose layout model per cluster: flex (single row/column) or grid (cards, galleries). Use absolute positioning only as a last resort.
- Derive spacing tokens (e.g., 4/8/12/16/24) from inferred gaps; reuse them consistently.
- Set breakpoints: start with desktop frame; add mobile by stacking columns to rows and reducing gaps/padding by one token step.
- Images: export asset URLs (or placeholders) and set aspect-ratio from node bounds.
- Text: apply Figma styles (font, size, weight, line-height, letter-spacing); preserve casing and truncation.
- Shopify notes: keep structure inside existing sections/snippets, avoid new folders, and prefer existing CSS variables if present.

## Output Plan

1. List sections/snippets/files to touch and where to place CSS/JS.
2. Define tokens (spacing, colors, font sizes).
3. Emit markup with meaningful data-\* hooks for future JS.
4. Add CSS (flex/grid) with the inferred gaps/padding and breakpoints.

## QA Checklist

- Counts match design (cards, buttons, list items).
- Typography and colors align with extracted tokens.
- Spacing matches inferred gaps/padding (spot-check a few pairs).
- Responsive: columns collapse as intended; no overflow on mobile width.
- Accessible: semantic tags, alt text, focusable controls.

## If Data Is Thin or Messy

- Ask for: specific frame export (PNG), list of target widths, and any must-keep tokens.
- If positions conflict, prefer consistent 4/8px rhythm over pixel-perfect noise and note any deliberate deviations.
