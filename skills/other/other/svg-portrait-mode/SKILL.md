---
name: svg-portrait-mode
description: "Portrait Mode" for SVGs — foveated vectorization with 4-zone selective detail. Combines Claude vision annotations, MediaPipe segmentation/landmarks, and optional saliency. Like phone portrait mode, but vectorized.
metadata:
  version: 0.5.0
---

# SVG Portrait Mode

Foveated vectorization with four detail zones. The calling agent identifies
semantically important regions; the skill refines boundaries computationally
and processes each zone at appropriate fidelity.

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

### Backward-compatible (MP-only)

Without annotations, falls back to MediaPipe face detection (like v0.3.0):

```python
svg, stats = portrait_mode("photo.jpg")
```

## Agent Workflow

1. **Look at the image** — identify what's compositionally important
2. **Provide rough bounding boxes** as `(x1, y1, x2, y2)` pixel coordinates
   - Precision is NOT required (±30px is fine); the skill refines boundaries
   - Use `focus_targets` for where the eye goes first (face, eyes)
   - Use `focus_edges` for compositionally important areas (beard, hands, hat, props)
3. **Call `portrait_mode()`** — skill handles segmentation, refinement, and compositing
4. **Review output** — check stats for path distribution across zones

## Four Zones

| Zone | Purpose | Default K | Default Smoothing | Examples |
|------|---------|-----------|-------------------|----------|
| **Focus Target** | Where the eye goes first | 128 | None | Eyes, nose, mouth, smile |
| **Focus Edge** | Compositionally important | 64 | kuwahara:2 | Beard, hands, hat, props, hair |
| **Periphery** | Context, not focal | 32 | kuwahara:3 | Torso, clothing, limbs |
| **Background** | Atmosphere | 16 | oilpaint:12 | Sky, walls, landscape |

## Architecture

```
┌────────────────────────────────────────────────────────┐
│  1. CLAUDE VISION → rough bboxes for semantic areas    │
│  2. MEDIAPIPE → person mask, face landmarks (if avail) │
│  3. THRESHOLD REFINEMENT → precise masks from bboxes   │
│  4. SALIENCY (optional) → promote high-detail areas    │
│  5. ZONE MAP → per-zone image_to_svg → clipPath SVG    │
└────────────────────────────────────────────────────────┘
```

Zone detection priority: face landmarks > agent bboxes > MP face bbox > person mask.

For focus target zones, face landmarks (478 mesh points) provide a precise face
oval when available. When MP landmark detection fails (vintage photos, paintings),
the skill falls back to threshold-based refinement of the agent's rough bbox.

## Parameters

```python
portrait_mode(image_path,
    # Zone annotations
    focus_targets=None,   # [{'bbox': (x1,y1,x2,y2), 'label': str}, ...]
    focus_edges=None,     # [{'bbox': (x1,y1,x2,y2), 'label': str}, ...]

    # Per-zone settings
    target_K=128, target_smooth=None,
    edge_K=64,   edge_smooth="kuwahara:2",
    periphery_K=32, periphery_smooth="kuwahara:3",
    bg_K=16,     bg_smooth="oilpaint:12",

    # Options
    target_detail=True,   # Loosen pipeline extraction for more paths
    use_landmarks=True,   # Try MP face landmarks
    use_saliency=False,   # Promote high-saliency periphery to edge
    multi_pass=True,      # Multi-pass MP for soft boundaries (~1.2s)
    svg_width=800,
    image_type="auto",    # auto/photo/painting/bw/grayscale/graphic
)
```

## SVG Compositing

Each zone becomes an SVG `<g>` with a `<clipPath>` derived from its mask contours.
Layers composite back-to-front: background → periphery → edge → target.

Focus target and edge zones use opaque crops to concentrate K-means clusters on
actual content pixels, then translate paths to correct positions in the composite.

## Requirements

Cross-skill dependencies:
- `image-to-svg` pipeline (`/mnt/skills/user/image-to-svg/`)
- `seeing-images` (`/mnt/skills/user/seeing-images/`) — for agent's visual inspection

MediaPipe models (auto-downloaded on first use):
- `selfie_segmenter.tflite`
- `blaze_face_short_range.tflite`
- `face_landmarker.task`

## Addressing Sharpness

The `target_detail=True` flag passes loosened extraction thresholds to the pipeline
for focus target zones: `compactness_min=0.04, edge_density_min=0.10,
isolation_filter=False, min_area=20`. This recovers path density without changing
the pipeline's global defaults.
