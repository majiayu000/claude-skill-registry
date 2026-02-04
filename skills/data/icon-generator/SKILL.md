---
name: icon-generator
description: Generate web UI/UX icon assets (favicon.ico, apple-touch-icon, PWA icons incl. maskable) and optionally Unreal Engine packaging icons (Windows .ico, macOS .iconset/.icns, Linux .png) from a single source SVG/PNG; use when you need correct multi-size icon files, safe-area guidance, manifests/head tags, or automation.
---

# Icon Generator

You generate icon asset bundles for **web UI/UX first** (favicons + PWA icons), and you can also generate **Unreal Engine packaging** icon assets when needed.

## Fast workflow

1. Pick target(s): Web UI/UX (favicon + PWA icons) and/or Unreal Engine packaging (optional).

2. Pick the source icon: prefer a **1024x1024 PNG** (square) or a clean **SVG**. If it's not square, choose whether to crop or pad (default: pad).

3. Generate the assets using [`scripts/generate_icons.py`](scripts/generate_icons.py).

Web/PWA sizes and safe-area rules: [`references/web-ui-ux.md`](references/web-ui-ux.md)

Unreal Engine formats and expectations: [`references/unreal-engine.md`](references/unreal-engine.md)

Full size tables: [`references/icon-sizes.md`](references/icon-sizes.md)

4. Verify output quality: ensure the `.ico` contains multiple sizes, and the 16/24/32 px variants are crisp.

## Quality rules (what "good" looks like)

- **Design for small sizes**: avoid thin strokes, tiny text, and busy details.
- **Prefer transparent backgrounds** for desktop icons unless you intentionally "plate" the icon.
- **Preview at 16px and 24px**. If it becomes muddy, create a simpler variant.

## Automation (recommended)

Run and customize the script:

- Script: [`scripts/generate_icons.py`](scripts/generate_icons.py)
- It supports:
  - Web/PWA set: `favicon.ico`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`, `icon-maskable-512.png`
  - UE sets (optional): Windows `.ico`, macOS `.iconset`, Linux `.png`

If you need HTML `<head>` snippets, `manifest.webmanifest` examples, and maskable safe-area guidance, read:

- [`references/web-ui-ux.md`](references/web-ui-ux.md)

## Notes

- If your input is SVG and Python SVG rasterization is unavailable on your machine, export a 1024x1024 PNG first (e.g., Inkscape), then rerun the script using the PNG.
- Keep this SKILL.md lean; detailed size tables live in the reference files.
