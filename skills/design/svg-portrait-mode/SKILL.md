---
name: svg-portrait-mode
description: "Portrait Mode" for SVGs — foveated vectorization with 4-zone selective detail. Combines Claude vision annotations, MediaPipe segmentation/landmarks, and optional saliency. Like phone portrait mode, but vectorized.
metadata:
  version: 0.6.0
---

# SVG Portrait Mode

Selective simplification: one pipeline pass at high K → zone-aware contour
simplification → optional per-zone style transforms. Like phone portrait mode,
but vectorized — not blur, but stylistic separation of foreground and background.

## Quick Start

### Agent-annotated (recommended)

The agent looks at the image first, identifies important regions with rough
bounding boxes, then calls:

```python
from portrait_mode import portrait_mode

svg, stats = portrait_mode("photo.jpg",
    focus_targets=[
        {'bbox': (215, 125, 295, 195), 'label': 'face'},
    ],
    focus_edges=[
        {'bbox': (214, 170, 310, 290), 'label': 'beard'},
        {'bbox': (210, 415, 300, 505), 'label': 'hands'},
        {'bbox': (195, 95, 330, 140), 'label': 'hat'},
    ])
```

### With style transforms

```python
svg, stats = portrait_mode("photo.jpg",
    focus_targets=[{'bbox': (215, 125, 295, 195), 'label': 'face'}],
    focus_edges=[{'bbox': (214, 170, 310, 290), 'label': 'beard'}],
    style_transforms={
        'background': 'desaturate:0.7',
        'periphery': 'desaturate:0.3',
    })
```

### Backward-compatible (MP-only)

Without annotations, falls back to MediaPipe face detection:

```python
svg, stats = portrait_mode("photo.jpg")
```

## How It Works

```
image-to-svg pipeline (K=96, unified palette)
    → zone detection (agent bboxes + optional MediaPipe landmarks)
    → assign contours to zones (by centroid)
    → per-zone simplification (epsilon, min_area)
    → optional per-zone style transforms
    → single SVG output (zone-labeled <g> groups, no clipPaths)
```

**Subtractive, not additive.** One pipeline pass produces full detail everywhere.
Zones that don't need detail get simplified by coarsening contour approximation
and raising minimum area thresholds. Subject stays sharp; background gets abstract.

### Why This Works

v0.5.0 ran four independent pipelines (one per zone) with different K-means
palettes, then composited via clipPaths. This produced tonal discontinuities
at zone boundaries and was 4-7x slower. v0.6.0 uses a single palette so colors
harmonize naturally, and simplification is a cheap post-process on contours the
pipeline already extracted.

## Agent Workflow

1. **Look at the image** — identify what's compositionally important
2. **Provide rough bounding boxes** as `(x1, y1, x2, y2)` pixel coordinates
   - Precision is NOT required (±30px is fine)
   - Use `focus_targets` for where the eye goes first (face, eyes)
   - Use `focus_edges` for compositionally important areas (beard, hands, hat, props)
3. **Call `portrait_mode()`** — skill handles zone detection, extraction, and assembly
4. **Review output** — check stats for path distribution across zones

## Four Zones

| Zone | Purpose | Epsilon | Min Area | Examples |
|------|---------|---------|----------|----------|
| **Target** | Where the eye goes first | 0.5× (tight) | 15 px² | Face, eyes, key subject |
| **Edge** | Compositionally important | 1.0× (default) | 40 px² | Beard, hands, hat, props |
| **Periphery** | Context, not focal | 2.5× (loose) | 100 px² | Torso, clothing, limbs |
| **Background** | Atmosphere | 5.0× (very loose) | 200 px² | Sky, walls, landscape |

Epsilon multiplies the base simplification factor (0.002 × perimeter). Higher =
fewer vertices = more abstract. Min area filters out small shapes entirely.

### Zone Assignment

Each contour is assigned to the highest-priority zone covering >30% of its area.
This prevents focal shapes that straddle a zone boundary from getting simplified.
Small contours (<500 px²) use centroid lookup for speed.

### Periphery Generation

When focus targets or edges are specified, periphery is automatically generated
as a buffer zone around the foreground (dilated union of target + edge zones).
This creates a smooth detail gradient from subject to background.

## Per-Zone Style Transforms

With zone-tagged shapes sharing a unified palette, backgrounds can be
independently styled without affecting subject colors:

```python
style_transforms={
    'background': 'desaturate:0.7',   # 70% desaturated
    'periphery': 'mute:0.3',          # 30% toward mid-gray
}
```

Available transforms:

| Transform | Effect |
|-----------|--------|
| `desaturate:N` | Shift toward gray (0=none, 1=grayscale) |
| `grayscale` | Full grayscale |
| `mute:N` | Shift toward mid-gray (0=none, 1=flat gray) |
| `warm:N` | Warmer color temperature |
| `cool:N` | Cooler color temperature |
| `opacity:N` | Group opacity (0=invisible, 1=full) |

## Parameters

```python
portrait_mode(image_path,
    # Zone annotations
    focus_targets=None,   # [{'bbox': (x1,y1,x2,y2), 'label': str}, ...]
    focus_edges=None,     # [{'bbox': (x1,y1,x2,y2), 'label': str}, ...]

    # Pipeline settings
    K=96,                 # Color clusters (higher = more tonal detail)
    smooth=None,          # ImageMagick preprocessing ("oilpaint", "kuwahara:N")
    svg_width=800,

    # MediaPipe options
    use_landmarks=True,   # Try MP face landmarks for precise face geometry

    # Per-zone simplification overrides
    zone_simplification=None,  # {ZONE_TARGET: {'epsilon_mult': 0.3, 'min_area': 10}}

    # Per-zone style transforms
    style_transforms=None,  # {'background': 'desaturate:0.7'}
)
```

## Performance

Single pipeline pass (~8-12s for a typical photo at K=96) vs v0.5.0's four
independent passes (~40-60s). Zone detection and contour assignment add <1s.
Style transforms are string operations with zero computational cost.

## Requirements

Cross-skill dependencies:
- `image-to-svg` pipeline (`/mnt/skills/user/image-to-svg/`)
- `flowing` DAG runner (`/mnt/skills/user/flowing/`)
- `seeing-images` (`/mnt/skills/user/seeing-images/`) — for agent's visual inspection

Optional MediaPipe models (auto-downloaded on first use):
- `blaze_face_short_range.tflite` — face detection fallback
- `face_landmarker.task` — precise face oval (478 mesh points)

Note: MediaPipe selfie segmenter is NOT used in v0.6.0. Zone detection comes from
agent bboxes, with MP used only for face landmark refinement.

```bash
pip install opencv-python-headless scikit-image scipy scikit-learn --break-system-packages -q
apt-get install -y librsvg2-bin -qq
```

## Verification Protocol

**After EVERY run, render and visually compare side-by-side.** Same as image-to-svg.

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
```

## What Changed from v0.5.0

### Deleted
- Per-zone image-to-svg calls (4 pipeline runs)
- Per-zone smoothing (kuwahara, oilpaint per zone)
- ClipPath compositing
- Opaque crop + translate trick
- Multi-pass segmentation (21 IM transforms × MP segmenter)
- MediaPipe selfie segmenter dependency

### Kept
- Agent annotation API (focus_targets, focus_edges with bboxes)
- MediaPipe face landmarks for precise face ovals
- Four-zone concept (target / edge / periphery / background)

### Added
- Single-pass pipeline with unified palette
- Zone-aware contour simplification (epsilon + min_area per zone)
- Per-zone style transforms (desaturate, mute, warm/cool, opacity)
- Automatic periphery generation (dilated foreground buffer)
- Zone-tagged shapes in SVG output (<g> groups)
