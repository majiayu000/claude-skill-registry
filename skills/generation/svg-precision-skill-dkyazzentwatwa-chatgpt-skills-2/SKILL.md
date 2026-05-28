---
name: svg-precision
description: Deterministic SVG generation, validation, and rendering. Use for icons, diagrams, charts, UI mockups, or technical drawings requiring structural correctness and cross-viewer compatibility.
---

# svg-precision

Generate *structurally correct* SVGs from a strict JSON spec (scene graph), then validate and optionally render a PNG preview.

## Fast path

1) Turn the user request into a **Spec JSON** (use templates in `references/spec.md`).
2) Build the SVG:
   - `python scripts/svg_cli.py build spec.json out.svg`
3) Validate:
   - `python scripts/svg_cli.py validate out.svg`
4) (Optional) Render a PNG preview (requires CairoSVG):
   - `python scripts/svg_cli.py render out.svg out.png --scale 2`

## Spec design rules (for accuracy)

- Always set `canvas.viewBox` and explicit `canvas.width`/`canvas.height`.
- Prefer absolute coordinates; use transforms only when they reduce complexity.
- Keep numbers sane: no NaN/inf; round to 3-4 decimals.
- Put reusable items in `defs` (markers, gradients, clipPaths) and reference by id.
- For predictable results across viewers, avoid exotic filters unless required.
- Text varies by fonts/viewers. If you need pixel-identical results, treat text as a risk and prefer shapes.

## Using the bundled scripts

### CLI

- `python scripts/svg_cli.py build <spec.json> <out.svg>`
- `python scripts/svg_cli.py validate <svg>`
- `python scripts/svg_cli.py render <svg> <out.png> [--scale N]`
- `python scripts/svg_cli.py diff <a.svg> <b.svg> <diff.png> [--scale N]` (renders + image-diffs)

### As a library (in Python)

```py
from svg_skill import build_svg, validate_svg
svg_text = build_svg(spec_dict)
report = validate_svg(svg_text)
```

## When the request is vague

1) Identify the *kind* of SVG: icon / diagram / chart / UI / technical.
2) Pick a template from `references/spec.md` and fill in concrete numbers.
3) If dimensions are unknown, choose defaults that match the domain:
   - icons: 24x24 or 32x32
   - UI mockups: 1440x900 or 390x844 (mobile)
   - charts: 800x450
   - diagrams: 1200x800
   - technical drawings: specify units (mm/in) and scale

## References

- `references/spec.md` - schema + ready-to-copy templates per SVG type
- `references/recipes.md` - layout and styling patterns that render consistently
