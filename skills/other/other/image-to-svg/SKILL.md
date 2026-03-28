---
name: image-to-svg
version: 1.8.0
description: Convert raster images (photos, paintings, illustrations, line art) into SVG vector reproductions. Use when the user uploads an image and asks to reproduce, vectorize, trace, or convert it to SVG. Also use when asked to decompose an image into shapes, create an SVG version of a picture, or faithfully reproduce artwork as vector graphics. Handles graphic/line-art inputs (Kandinsky, architectural drawings, ink work) via a compositional pipeline that extracts lines as SVG strokes. Do NOT use for creating original SVG illustrations from text descriptions — only for converting existing raster images.
---
 
# Image to SVG Reproduction
 
Convert raster images into faithful SVG reproductions using data-driven color quantization and contour extraction. **Never hand-draw shapes from visual interpretation** — always extract geometry from the actual pixel data.

## Core Principle

**Trust the data, not your imagination.** Claude's visual interpretation of images is unreliable for precise color matching, shape positioning, and spatial relationships. Every shape, color, and position must come from computational analysis of the source pixels.

## Quick Start

```bash
pip install opencv-python-headless scikit-image scipy scikit-learn --break-system-packages -q
apt-get install -y librsvg2-bin -qq
```

```python
import sys
sys.path.insert(0, '/mnt/skills/user/image-to-svg/scripts')
from pipeline import image_to_svg

svg, flow = image_to_svg("source.jpg", mode="painting")

with open("output.svg", "w") as f:
    f.write(svg)

flow.summary()  # timing + status per step
```

## Mode Selection

**Look at the image** and ask: "Does this have smooth gradients or hard edges?" Gradients → higher K. Hard edges → lower K.

| Mode | K | Best for | Dark shape gating |
|------|---|----------|-------------------|
| `"graphic"` | 28 | Logos, icons, Kandinsky, flat design | Loose (keeps thin lines) |
| `"illustration"` | 40 | Comics, editorial, digital art | Moderate |
| `"painting"` | 56 | Renaissance, Impressionist, watercolor | Standard |
| `"photo"` | 64 | Portraits, landscapes, still life | Standard (prevents woodcut artifacts) |

Default is `"painting"`. When uncertain, start there.

**Tradeoffs**: K=64 produces ~2300 shapes (~1.2MB SVG) vs K=28's ~1000 shapes (~550KB). Processing time roughly doubles with K. The quality gain in tonal gradation is substantial for photos but wasted on graphic art.

All mode defaults (K, dark_lum, compactness_min, etc.) can be overridden via `**kwargs`:
```python
svg, flow = image_to_svg("source.jpg", mode="graphic", K=12, min_area=20)
```

## Compositional Pipeline (Line Art)

For images dominated by lines, strokes, and geometric shapes (Kandinsky, architectural drawings, technical illustrations, comic ink work), the standard fill-only pipeline produces jagged filled polygons instead of clean strokes. The compositional pipeline solves this with two passes:

**Pass 1 — Line Extraction**: Isolate thin features via morphological erosion → skeletonize to 1px centerlines → Hough line detection → merge collinear fragments → measure stroke width → sample color. Emits SVG `<line>` elements with `stroke-width`.

**Pass 2 — Fill Extraction**: Suppress line regions from image (replace with local background estimate via median blur) → run standard K-means quantization on the cleaned image → contour extraction → `<path>` fills.

**Composition**: Fills render behind strokes in layered `<g>` groups.

```python
# Auto-detect: classifies input and routes automatically
svg, flow = image_to_svg("kandinsky.jpg", mode="graphic")

# Force compositional pipeline
svg, flow = image_to_svg("technical_drawing.png", mode="graphic", pipeline="compositional")

# Force fill-only (previous default behavior)
svg, flow = image_to_svg("photo.jpg", mode="painting", pipeline="fill")
```

**Pipeline selection** (`pipeline` parameter):
| Value | Behavior |
|-------|----------|
| `"auto"` (default) | Classify input via edge density + luminance bimodality + Hough line count. Route to compositional for graphic art, fill-only for photos. |
| `"fill"` | Force fill-only pipeline. Use for photos, paintings, or when compositional produces unwanted results. |
| `"compositional"` | Force two-pass pipeline. Use for line art, technical drawings, or ink work where you know lines are present. |

**Auto-classification heuristics**: An image is classified as graphic when it has high edge density (>5% edge pixels) combined with bimodal luminance distribution (>0.35 bimodality coefficient), or high straight-line density (>3 Hough lines per 10k pixels).

**SVG output structure** (compositional):
```xml
<svg ...>
  <rect ... />        <!-- background -->
  <g id="fills">      <!-- filled regions (painter's algorithm) -->
    <path ... />
  </g>
  <g id="strokes">    <!-- line strokes (on top) -->
    <line x1="..." y1="..." x2="..." y2="..." stroke="#000" stroke-width="2.5" stroke-linecap="round"/>
  </g>
</svg>
```

**Stroke width control**: Measured perpendicular to each detected line, then scaled by 0.65x and capped at 4.5 SVG units. This prevents thick features from rendering as bloated strokes while keeping thin lines crisp.

**Current limitation — straight lines only**: Hough transform detects straight segments. Curved strokes (arcs, spirals) are not yet extracted as strokes — they fall through to the fill pass. Future work: `cv2.fitEllipse` or spline fitting on skeleton branches.

## Palette Remapping (Warhol Effects)

Separate structure from color: K-means finds regions, palette remapping assigns bold colors. This produces screen-print / pop art effects.

```python
# Named preset
svg, flow = image_to_svg("photo.jpg", mode="graphic", K=4, palette="pop")

# Custom hex list (darkest → lightest mapping order)
svg, flow = image_to_svg("photo.jpg", mode="graphic", K=8,
    palette=["#000", "#dc143c", "#ff69b4", "#ffd700", "#32cd32", "#00bfff", "#ff8c00", "#f5f5f5"])

# Override background separately
svg, flow = image_to_svg("photo.jpg", mode="graphic", K=4, palette="ocean", bg_color="#000000")
```

**Built-in presets**: `bw`, `mono3`, `mono4`, `pop`, `pop2`, `neon`, `warhol4`, `warhol6`, `warhol8`, `sunset`, `ocean`

**How it works**: Unique shape colors are sorted by luminance. Palette entries are mapped proportionally — `palette[0]` replaces the darkest cluster, `palette[-1]` replaces the lightest. Background defaults to the lightest palette entry unless `bg_color` is set. Palette length doesn't need to match K exactly; colors are binned proportionally.

**Portraits**: Use K=16-24 even with bold palettes. Facial features (glasses, beard, brow) need tonal range that low K eliminates. A good rule of thumb: palette length ≈ K/3 for clean luminance binning. At K=8 with a 4-color palette, a face becomes an undifferentiated blob.

**Contrast preprocessing warning**: External contrast boosting (contrast-stretch, sigmoidal-contrast) can confuse background detection. The pipeline's edge-contact heuristic assumes untouched luminance distributions — aggressive tone-mapping pushes subject tones into background-adjacent bins, causing misclassification (e.g., dark jacket regions classified as background and mapped to the lightest palette color). If you see subject regions tearing to the background color, try without preprocessing first. The pipeline's own bilateral blur + optional kuwahara/oilpaint handles tonal separation.

### Background Detection Override (`bg_clusters`)

Control which clusters are treated as background:

```python
# Auto-detect (default) — edge-contact heuristic
svg, flow = image_to_svg("photo.jpg", mode="illustration", K=20, palette="warhol6")

# Disable — no clusters removed, no background rect color override
svg, flow = image_to_svg("photo.jpg", mode="illustration", K=20, palette="warhol6", bg_clusters=0)

# Force specific cluster indices (from quantize step's sorted_clusters output)
svg, flow = image_to_svg("photo.jpg", mode="illustration", K=20, palette="warhol6", bg_clusters=[2, 5])
```

Use `bg_clusters=0` when palette remapping already controls all colors explicitly and background detection is getting in the way. Use `bg_clusters=[list]` when you know which clusters are background but the heuristic misidentifies them.

### Portrait Pop-Art Recipe (Warhol Style)

```python
# Key: enough K for facial features, palette length ~K/3, modest smoothing
# Do NOT apply contrast preprocessing — it breaks background detection.
results = image_to_svg_batch("portrait.jpg", [
    {"name": "hot",   "mode": "illustration", "K": 20, "smooth": "kuwahara:6",
     "palette": ["#000", "#D4145A", "#FF6B9D", "#FF85C0", "#FFD700", "#FFEF82", "#FFF8DC"]},
    {"name": "cool",  "mode": "illustration", "K": 20, "smooth": "kuwahara:6",
     "palette": ["#0D0035", "#4A00E0", "#7B68EE", "#00D4FF", "#7FFFD4", "#B0FFE0", "#E0FFFF"]},
    {"name": "earth", "mode": "illustration", "K": 20, "smooth": "kuwahara:6",
     "palette": ["#1a0a00", "#8B4513", "#CD853F", "#DEB887", "#F5DEB3", "#FAEBD7", "#FFF8DC"]},
    {"name": "neon",  "mode": "illustration", "K": 20, "smooth": "kuwahara:6",
     "palette": ["#0d0d0d", "#ff00ff", "#00ff00", "#ffff00", "#00ffff", "#ff69b4", "#f5f5f5"]},
], svg_width=700)
```

Why this works: K=20 preserves enough tonal clusters for facial structure (glasses, beard, brow ridge). 7-color palettes give ~K/3 luminance bins — enough variation to separate features without muddying. `kuwahara:6` smooths texture without dissolving edges (`:12` erases glasses). Raw source → pipeline smoothing only; no external contrast manipulation.

## ImageMagick Preprocessing (smooth)

Reduce shape count and SVG file size by 20-45% using ImageMagick edge-preserving filters before quantization. Requires ImageMagick on PATH (pre-installed on Claude.ai containers).

```python
# Oilpaint: bold, painterly smoothing (default strength=8)
svg, flow = image_to_svg("photo.jpg", mode="photo", smooth="oilpaint")

# Stronger smoothing = fewer shapes, more stylized
svg, flow = image_to_svg("photo.jpg", mode="illustration", K=32, smooth="oilpaint:12")

# Kuwahara: subtler, preserves more structure (default strength=5)
svg, flow = image_to_svg("photo.jpg", mode="painting", smooth="kuwahara:7")

# Works with batch API too
results = image_to_svg_batch("photo.jpg", [
    {"name": "raw",      "mode": "photo"},
    {"name": "smooth",   "mode": "photo", "smooth": "oilpaint"},
    {"name": "stylized", "mode": "illustration", "K": 32, "smooth": "oilpaint:12", "palette": "pop"},
])
```

**Available filters**: `oilpaint` (ImageMagick `-paint`), `kuwahara` (ImageMagick `-kuwahara`). Append `:N` for custom strength.

**How it works**: The IM filter runs before the pipeline's bilateral+Gaussian blur. Both are edge-preserving smoothers at different scales — IM handles coarse texture, bilateral handles fine detail. The result is cleaner K-means regions with fewer fragmented shapes.

**Measured impact** (1206×1597 photo, K=32):

| smooth | Shapes | SVG size | Reduction |
|--------|--------|----------|-----------|
| none | 3381 | 1868KB | — |
| oilpaint (8) | 2385 | 1329KB | -29% |
| oilpaint:12 | 1842 | 1065KB | -43% |
| kuwahara (5) | 2719 | 1453KB | -22% |
| kuwahara:7 | 2000 | 1152KB | -38% |

## Pipeline Architecture

Uses the [flowing](/mnt/skills/user/flowing/SKILL.md) DAG runner. Steps with independent inputs run in parallel.

### Fill-only pipeline (`pipeline="fill"`)

```
preprocess → quantize → ┬─ detect_background ─┬─ extract_contours → assemble_svg
                        └─ edge_map           ─┘
```

### Compositional pipeline (`pipeline="compositional"`)

```
classify_input ──→ extract_lines ──→ suppress_line_regions ──→ [fill pipeline on cleaned image]
                        │                                              │
                        └──────────── lines ───────────────────→ assemble_compositional ←── fills
```

Steps (fill-only):
1. **preprocess** — Bilateral + Gaussian blur (edge-preserving texture removal)
2. **quantize** — K-means color quantization at chosen K
3. **detect_background** — Identifies background clusters by edge contact (parallel with edge_map)
4. **edge_map** — Sobel edge detection via `cv2.Sobel` (parallel with detect_background)
5. **extract_contours** — Per-cluster contour extraction with dark territory awareness and woodcut prevention (d=1 dilation; stroke handles gaps)
6. **assemble_svg** — Z-ordered painter's algorithm assembly with stroke=fill gap coverage

Additional steps (compositional):
1. **classify_input** — Edge density + bimodality + Hough line count analysis
2. **extract_lines** — Morphological thin-feature isolation → skeletonize → Hough → merge collinear → measure stroke width → sample color
3. **suppress_line_regions** — Replace line pixels with median-blur background estimate
4. **assemble_compositional** — Layer fills behind strokes in grouped SVG

### Resume on failure

```python
svg, flow = image_to_svg("source.jpg", mode="photo")
# If extract_contours failed:
flow.override(extract_contours, corrected_shapes)
flow.resume()  # quantize, detect_background, edge_map stay cached
```


## Batch API

Generate multiple variants from one image, sharing computation across runs with the same K:

```python
from pipeline import image_to_svg_batch

results = image_to_svg_batch("photo.jpg", [
    {"name": "photo",   "mode": "photo"},
    {"name": "warhol",  "mode": "graphic", "K": 12, "palette": "warhol4"},
    {"name": "neon",    "mode": "graphic", "K": 12, "palette": "neon"},
    {"name": "sunset",  "mode": "graphic", "K": 12, "palette": "sunset"},
    {"name": "bw",      "mode": "graphic", "K": 16, "palette": "bw"},
], svg_width=1400)

for name, svg in results.items():
    with open(f"{name}.svg", "w") as f:
        f.write(svg)
```

Variants sharing the same K run the pipeline (preprocess → quantize → edge_map → extract_contours) **once**, then fan out at assembly for palette remapping. This guarantees structural identity across palette variants (same shapes, same paths) and saves ~20-60s per shared K group.

**Verification still applies in batch mode.** The turnkey feel of batch processing makes it easy to skip the side-by-side comparison — don't. Render at least one variant per K group and verify before delivering. Background detection failures and palette mapping issues are invisible without rendering.

## Verification Protocol

**After EVERY run, render and visually compare side-by-side.** This is non-negotiable.

```python
import subprocess
from PIL import Image

subprocess.run(['rsvg-convert', '-w', '1400', 'output.svg', '-o', 'output.png'])

orig = Image.open('source.jpg')
rendered = Image.open('output.png')
target_h = 800
orig_r = orig.resize((int(orig.width * target_h / orig.height), target_h))
rend_r = rendered.resize((int(rendered.width * target_h / rendered.height), target_h))
gap = 20
comp = Image.new('RGB', (orig_r.width + rend_r.width + gap, target_h), (255,255,255))
comp.paste(orig_r, (0, 0))
comp.paste(rend_r, (orig_r.width + gap, 0))
comp.save('comparison.png')
# LOOK AT comparison.png BEFORE claiming success
```

## Manual Post-Processing

### Handling Subtle Color Differences

When two regions have similar luminance but different hue/saturation, K-means in RGB space merges them. Use **HSV multispectral analysis**:

```python
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
h_ch, s_ch, v_ch = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

# Separate gray (low saturation) from red (high saturation) at similar brightness
red_mask = ((h_ch < 12) | (h_ch > 168)) & (s_ch > 120) & (v_ch > 80)
gray_mask = (s_ch < 80) & (v_ch > 40) & (v_ch < 120) & spatial_constraint
```

**Saturation is the key discriminator** for colors that look similar in grayscale but are visually distinct.

### Positioning Overlays

When adding shapes not captured by quantization, **derive coordinates from the SVG render**, not the source image. The extraction pipeline shifts positions due to contour simplification.

```python
# WRONG: extract from source, insert into SVG (coordinate mismatch)
# RIGHT: render SVG → detect gap in render → create shape in render coords → insert
svg_render = cv2.imread('rendered_svg.png')
```

## Gap Coverage: stroke=fill

Every `<path>` element gets `stroke="{fill}" stroke-width="4" stroke-linejoin="round"`. This bleeds each shape outward by 2px with its own fill color, covering inter-cluster gaps with the locally correct color.

**Why stroke beats dilation for gaps**: Dilation operates on binary masks *before* contour simplification — it blurs detail. Stroke operates on final polygons *after* `approxPolyDP` — it catches all gaps including those introduced by simplification. Pure vector, no file size penalty beyond attribute bytes (~12%).

**Background fallback**: When `detect_background` finds no clusters, the bg rect uses `#000000` (black) instead of white. Black reads as shadow; white reads as absence.

**Dilation** is reduced to `iterations=1` — just enough for morphological noise cleanup. Gap coverage is fully handled by stroke.

## Anti-Patterns

1. **Never hand-draw shapes** from visual interpretation. Use CV extraction.
2. **Never claim a fix works without rendering and comparing.** A rendered comparison is the only verification.
3. **Never use geometric primitives** (circles, rectangles) to approximate extracted contours.
4. **Never extract coordinates from the source image and insert into the SVG** without verifying alignment.
5. **Never boost saturation globally.** Do targeted per-color adjustments based on measured ΔE.
6. **Never aggressively merge near-background colors.** Only merge colors <10 RGB distance from background AND heavily touching edges.
7. **Don't use bezier smoothing unless requested.** Simple L polygons produce smaller SVGs.
8. **Don't use a dilation kernel larger than 3×3.** Use `iterations=1` on a 3×3 kernel — stroke=fill handles gap coverage in vector space, so dilation only needs to close noise holes.

## Known Limitations

- **Thin linework** (fill-only): The dark shape gating that prevents woodcut artifacts in photos can filter deliberate thin lines in graphic art. The `"graphic"` mode loosens this, but very fine crosshatching may still degrade. Use `pipeline="compositional"` for line-art inputs — it extracts thin features as SVG strokes instead.
- **Curved lines** (compositional): Hough transform only detects straight line segments. Curved strokes (arcs, spirals, freehand curves) fall through to the fill pass and render as filled polygons. Future work: `cv2.fitEllipse` or spline fitting on skeleton branches.
- **Ring/arc structures**: Large dark rings (like Kandinsky's outer circle) fragment across multiple K-means clusters. Each cluster's contours are independent, so the ring doesn't form one smooth shape. A dark-cluster-merging step would help.
- **Gradient transitions**: At any K, smooth gradients produce staircase banding. Higher K reduces this but never eliminates it.
- **Parallel line groups** (compositional): Dense hatching or ruled lines may merge incorrectly if the perpendicular distance between adjacent lines is below the merge threshold (6px). The merge step currently doesn't detect parallel-but-offset lines as distinct strokes.

## Dependencies

```bash
pip install opencv-python-headless scikit-image scipy scikit-learn --break-system-packages
apt-get install -y librsvg2-bin  # for rsvg-convert
```

**Compiled acceleration**: `nn_assign.c` is auto-compiled on first use if `gcc` is available (27x faster label assignment). Falls back to numpy if unavailable.

**Cross-skill dependencies** (resolved automatically by pipeline.py):
- [flowing](/mnt/skills/user/flowing/SKILL.md) — DAG workflow runner
