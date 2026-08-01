---
name: model-compare
description: Compare 3D CAD models using boolean operations (IoU, Dice, precision/recall).
  Use when evaluating generated models against gold references, diffing CAD revisions,
  or computing similarity metrics for M
---

---
name: model-compare
description: Compare 3D CAD models using boolean operations (IoU, Dice, precision/recall). Use when evaluating generated models against gold references, diffing CAD revisions, or computing similarity metrics for ML training. Triggers on: model diff, compare models, IoU, intersection over union, model similarity, CAD comparison, STEP diff, 3D evaluation, gold reference, generated model, precision recall 3D.
---

# 3D Model Comparison Tool

Compare CAD models using boolean operations to compute similarity metrics like IoU, Dice, precision, and recall. Useful for:

- Evaluating ML-generated models against gold references
- Comparing revisions of CAD designs
- Computing metrics for training 3D generative models
- Visualizing geometric differences

## Quick Start

```bash
# Compare two STEP files
uvx --from build123d python scripts/model_diff.py reference.step generated.step

# JSON output for training pipelines
uvx --from build123d python scripts/model_diff.py ref.step gen.step --json --no-export

# Demo mode (no files needed)
uvx --from build123d python scripts/model_diff.py --demo
```

## Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| STEP | `.step`, `.stp` | Recommended - full CAD fidelity |
| BREP | `.brep` | OpenCASCADE native format |
| STL | `.stl` | Mesh format - may have boolean issues |

## Output Metrics

### Primary Metrics (for ML training)

| Metric | Range | Description |
|--------|-------|-------------|
| **IoU** (Jaccard) | 0-1 | `|A∩B| / |A∪B|` - standard similarity |
| **Dice** (F1) | 0-1 | `2|A∩B| / (|A|+|B|)` - more sensitive to small overlaps |
| **Precision** | 0-1 | `|A∩B| / |B|` - how much of generated is correct |
| **Recall** | 0-1 | `|A∩B| / |A|` - how much of reference was captured |

### Diagnostic Metrics

| Metric | Description |
|--------|-------------|
| `volume_ratio` | B/A volume ratio (1.0 = same size) |
| `center_offset` | Distance between centers of mass |
| `bbox_iou` | Bounding box IoU (coarse alignment) |
| `size_ratio_x/y/z` | Per-axis scale comparison |
| `surface_ratio` | Surface area comparison |

### Interpretation

The tool provides automatic interpretation:
- **Over-generating**: Low precision, high extra geometry
- **Under-generating**: Low recall, missing geometry
- **Size issues**: Volume ratio far from 1.0
- **Position issues**: Large center offset

## CLI Options

```
usage: model_diff.py [-h] [-o OUTPUT_DIR] [--json] [--no-export] [--demo]
                     [reference] [generated]

positional arguments:
  reference          Reference/gold model file (STEP, BREP, or STL)
  generated          Generated/predicted model file to compare

options:
  -o, --output-dir   Output directory for GLB files (default: .)
  --json             Output only JSON metrics (for pipelines)
  --no-export        Skip exporting GLB visualization files
  --demo             Run with built-in demo models
```

## Output Files

When `--no-export` is not set, produces GLB files for visualization:

| File | Description |
|------|-------------|
| `diff_reference.glb` | The reference model (A) |
| `diff_generated.glb` | The generated model (B) |
| `diff_missing.glb` | Geometry in A but not B (under-generation) |
| `diff_extra.glb` | Geometry in B but not A (over-generation) |
| `diff_common.glb` | Geometry in both (correct match) |

## Example: Training Pipeline Integration

```bash
# Batch evaluation
for gen in outputs/*.step; do
    uvx --from build123d python model_diff.py gold.step "$gen" --json --no-export
done | jq -s '{
    avg_iou: (map(.iou) | add / length),
    avg_precision: (map(.precision) | add / length),
    avg_recall: (map(.recall) | add / length)
}'
```

## Example: Loss Function

```python
# In your training code, use metrics for loss:
loss = (
    (1 - metrics['iou']) * 1.0 +           # Primary shape match
    abs(1 - metrics['volume_ratio']) * 0.5 + # Scale accuracy
    metrics['center_offset'] * 0.1           # Position accuracy
)
```

## How It Works

The tool uses boolean operations from OpenCASCADE (via build123d):

```
Missing  = Reference - Generated  (A - B)
Extra    = Generated - Reference  (B - A)
Common   = Reference & Generated  (A ∩ B)
Union    = Reference + Generated  (A ∪ B)

IoU      = volume(Common) / volume(Union)
Dice     = 2 * volume(Common) / (volume(A) + volume(B))
Precision = volume(Common) / volume(B)
Recall    = volume(Common) / volume(A)
```

## Sample Output

```
=================================================================
  3D MODEL COMPARISON REPORT
  Reference (A) vs Generated (B)
=================================================================

──────────────────────────── VOLUMES ────────────────────────────
  Reference (A):          51,433.629
  Generated (B):          45,904.426
  Intersection (A∩B):     42,292.031
  Missing (A-B):           9,141.598  (17.8% of A)
  Extra (B-A):             3,612.395  (7.9% of B)

──────────────────────── PRIMARY METRICS ────────────────────────
  IoU (Jaccard):              0.7683  (1.0 = identical)
  Dice (F1):                  0.8690  (1.0 = identical)
  Precision:                  0.9213  (correctness of B)
  Recall:                     0.8223  (coverage of A)

──────────────────────── INTERPRETATION ─────────────────────────
  △ Partial match (IoU > 50%)
  → Under-generating: 17.8% of A is missing
  → Undersized by 10.8%
=================================================================
```
