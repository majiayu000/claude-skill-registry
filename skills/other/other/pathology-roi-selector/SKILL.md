---
name: pathology-roi-selector
description: Select and extract regions of interest (ROI) from whole slide images (WSI) for AI training data preparation and pathology research.
license: MIT
skill-author: AIPOCH
status: beta
---
# Pathology ROI Selector

Select and extract regions of interest from whole slide images (WSI) for AI model training, tissue microarray creation, and pathology research.

## Input Validation

This skill accepts: whole slide image files (SVS, NDPI, TIFF, or compatible WSI formats) for automated region of interest selection and extraction.

If the request does not involve selecting ROIs from a whole slide image — for example, asking to perform cell segmentation, run stain normalization, or analyze non-pathology images — do not proceed. Instead respond:

> "pathology-roi-selector is designed to select and extract regions of interest from whole slide images. Your request appears to be outside this scope. Please provide a WSI file path with tissue type parameters, or use a more appropriate tool for your task."

## When to Use

- Extracting tumor-rich or tissue-specific regions from whole slide images for AI training datasets
- Creating tissue microarray sampling coordinates
- Generating quality-controlled crops for pathology education or research
- Automating ROI selection with reproducible, documented parameters

## Quick Check

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
```

## Workflow

1. **Validate input first** — confirm the request involves a WSI file and is within scope before any processing.
2. Confirm the user objective, required inputs, and non-negotiable constraints.
3. Validate `--image` path: resolve with `Path.resolve()` and verify it is within the workspace (no `../` traversal).
4. Use the packaged script path or the documented reasoning path with only the inputs that are actually available.
5. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
6. If execution fails or inputs are incomplete, switch to the fallback path and state exactly what blocked full completion.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--image` / `-i` | path | Yes | Whole slide image file path |
| `--type` | str | No | Tissue type filter: `tumor`, `normal`, `stroma` |
| `--output` | path | No | Output directory for ROI crops and coordinates |

## Usage

```text
# Basic ROI selection from WSI
python scripts/main.py --image slide.svs --output ./rois

# Filter for tumor regions only
python scripts/main.py --image slide.svs --type tumor --output ./tumor_rois

# Check available options
python scripts/main.py --help
```

## Output

- ROI coordinates (JSON with bounding boxes)
- Tissue percentage per ROI
- Quality metrics (tissue coverage, artifact score)
- Export-ready image crops at specified magnification

**Artifact Score:** When quality metrics are requested, the output must include an explicit `artifact_score` field (0–1 scale, where 0 = no artifacts, 1 = severe artifacts). This is required alongside tissue coverage when `--type` filtering is used.

## Example

Input: Whole slide image (100K x 100K pixels, H&E stained)
Output: 12 tumor-rich ROIs identified, coordinates exported, crops saved at 20x magnification

## Error Handling

- If `--image` is missing, state this and request the WSI file path.
- If the image file path contains `../` or resolves outside the workspace, reject with a path traversal warning. The script enforces this via `Path(args.image).resolve()`.
- If the WSI format is not supported (e.g., DICOM), list supported formats (SVS, NDPI, TIFF) and stop.
- If both an unsupported format and a missing required flag are detected, use the Fallback Template with both issues listed under `Blocked by`.
- If the task goes outside the documented scope, stop instead of guessing or silently widening the assignment.
- If `scripts/main.py` fails, report the failure point, summarize what still can be completed safely, and provide a manual fallback.
- Do not fabricate ROI coordinates, tissue percentages, or quality metrics.

**Note on script implementation:** `scripts/main.py` currently returns mock ROI coordinates (placeholder). Real WSI analysis requires OpenSlide integration. Until implemented, the skill operates in reasoning mode — providing parameter plans and workflow guidance without fabricating actual coordinates.

## Fallback Template

When execution fails or inputs are incomplete, respond with this structure:

```
FALLBACK REPORT
───────────────────────────────────────
Objective      : [restate the goal]
Blocked by     : [exact missing input or error — list multiple if applicable]
Partial result : [what can be completed — e.g., parameter plan]
Assumptions    : [magnification, tissue type, output format assumed]
Constraints    : [WSI format requirements, memory limits]
Risks          : [large file processing time, artifact regions]
Unresolved     : [what still needs user input]
Next step      : [minimum action needed to unblock]
───────────────────────────────────────
```

## Response Template

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

If the request is simple, compress the structure but keep assumptions and limits explicit when they affect correctness.

## Prerequisites

```bash
pip install openslide-python  # required for real WSI analysis
```

No additional Python packages required for mock/reasoning mode.
