---
name: svg-mascot-animator
description: "Generate animated pixel-art SVG mascots from images or descriptions. This skill should be used when creating pixel-art characters, animating SVG sprites, building walking/bouncing/waving mascots, converting images to pixel-art SVGs, or generating GSAP-animated character components. Triggers on: pixel art, SVG animation, mascot, sprite animation, walking character, animated icon, pixel mascot, GSAP SVG."
argument-hint: "[character description or image path] [--animation preset] [--output format]"
---

# SVG Mascot Animator

Generate sophisticated animated pixel-art SVG mascots — characters built entirely from `<rect>` elements, animated via GSAP timelines and frame-by-frame sprite switching. Reverse-engineered from ayotomcs.me/claude-mascot (creator: Ayotomi Adewuyi).

## When to Use

- Converting an image into a pixel-art SVG character
- Adding walk, bounce, lean, wave, or typing animations to SVG mascots
- Generating self-contained HTML demos with animated SVG characters
- Creating React components with GSAP-animated pixel mascots
- Building sprite-based frame-by-frame SVG animations

## Character Design Principles

The ayotomcs reference uses two approaches to character creation:

1. **Hand-drawn in Figma** → exported as SVG → embedded as JSX. Evidence: rect IDs follow Figma naming (`Rectangle 117`, `dgreen 251`), non-integer coordinates (e.g., `x="92.9004"`), and `<path>` elements for complex silhouettes like hats.

2. **AI-generated sprite sheets** (EDH Series project) → Nano Banana Pro (Gemini) generates character poses matching an illustration style → converted to sprite sheets for frame-by-frame animation.

**Design constraints for animatable characters:**
- **Standing pose, side view** — legs must be distinct rectangular blocks at the bottom for walk cycles to work. Sitting characters should use `idle` or `bounce` presets instead.
- **4-6 colors max** — produces cleaner, more iconic pixel art. The ayotomcs Claude mascot uses only 4: `#DD775B` (body), `black` (eyes), `#1A4C81` (code), `#5D5B56` (details).
- **Symmetric body parts** — left/right hands and front/back leg pairs enable alternating animation.
- **Grid size 16-24** — too small and the character loses detail; too large and it stops looking like pixel art.

## Pipeline

### 1. Generate or Convert Character SVG

**From a description (via nano-banana-pro):**
```bash
# Step 1: Generate pixel-art reference image
python3 ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  "16-bit pixel art character of a fox standing, side view, white background, 4 colors only, simple blocky shapes like minecraft" \
  --output /tmp/fox-pixel.png

# Step 2: CRITICAL — trim whitespace with ImageMagick before converting
# Without this, the character occupies <10% of the grid and most pixels are background
magick /tmp/fox-pixel.png/generated_image_0_0.jpg -fuzz 15% -trim +repage /tmp/fox-trimmed.png

# Step 3: Convert to SVG rects
python3 scripts/pixel_art_generator.py /tmp/fox-trimmed.png --grid 20 --colors 4 --merge --remove-bg -o mascot.svg

# Step 4: Add SVG id for GSAP targeting
sed -i '' 's/<svg /<svg id="mascot" /' mascot.svg
```

**From an existing image:**
```bash
magick input.png -fuzz 15% -trim +repage /tmp/trimmed.png
python3 scripts/pixel_art_generator.py /tmp/trimmed.png --grid 24 --colors 6 --merge --remove-bg -o mascot.svg
```

### 2. Add Animation

**GSAP timeline presets** — continuous motion for simple animations:
```bash
python3 scripts/animation_builder.py --preset walk-and-bounce --svg-id mascot
python3 scripts/animation_builder.py --list  # show all presets
```

Available presets: `idle`, `bounce`, `lean`, `wave`, `walk`, `walk-and-bounce`, `walk-and-wave`, `typing`

**Frame-by-frame** — for complex choreography, generate N SVG frames as separate `<g>` groups inside the SVG, then use `generate_frame_switcher()` from `animation_builder.py` with variable timing per frame.

### 3. Assemble Output

```bash
python3 scripts/template_renderer.py --format standalone --svg mascot.svg --animation walk.js -o mascot.html
```

Output formats:
- **standalone** — Self-contained HTML with GSAP CDN (open in browser)
- **react** — TSX component with useRef/useEffect/GSAP
- **svg-only** — Pure SVG with SMIL bounce fallback

### Key Techniques

**Pixel-perfect rendering:** All shapes use `<rect>` elements on a grid (no `<path>`, no curves). Add `shapeRendering="crispEdges"` to prevent anti-aliasing.

**GSAP walk cycle:** Alternating leg pairs squash via `scaleY: 0.45` while body translates. Walk distance is dynamically calculated from parent container width for responsive behavior.

**Frame switching:** Multiple `<g>` groups with `display: none/inline` toggled by setTimeout. Variable timing per frame creates natural rhythm — fast default (85ms), with pauses at key poses (270-1500ms).

**Body part auto-grouping:** `pixel_art_generator.py` assigns `id` attributes (head, body, legs, eyes, left-hand, right-hand) by position heuristics, enabling GSAP to target individual parts.

## Gotchas

**ImageMagick trim is mandatory.** AI-generated images have large white borders. Without `magick -fuzz 15% -trim`, the character occupies <10% of the grid and becomes a few scattered pixels. Always trim before converting.

**Walk animation requires standing characters.** The auto-grouping puts the bottom 30% of rects into `legs`. For sitting characters, this cuts the body in half during `scaleY` squash. Use `idle`, `bounce`, or `wave` for non-standing poses.

**Near-white quantization.** JPEG sources produce multiple near-white colors (#FEFEFE, #FEFFFF, #FFFFFD) that background removal misses. Using `--colors 4` instead of 6 forces cleaner quantization. For best results, use PNG sources with true transparent backgrounds.

**SVG id required.** Add `id="mascot"` to the root `<svg>` element before animation — GSAP targets `document.getElementById("mascot")`. The pipeline does not add this automatically.

## Dependencies

- **Python**: Pillow (`uv pip install Pillow`)
- **ImageMagick 7**: For pre-processing (`magick -trim`, `-fuzz`)
- **Browser**: GSAP 3 via CDN (included in standalone template)
- **Optional**: nano-banana-pro skill for AI image generation

## Reference

- `references/gsap-timeline-patterns.md` — GSAP animation recipes and easing functions
- `references/pixel-art-svgs.md` — Pixel grid to SVG rect conversion techniques
- `references/ayotomcs-deconstruction.md` — Full deconstruction of the ayotomcs.me/claude-mascot reference implementation
