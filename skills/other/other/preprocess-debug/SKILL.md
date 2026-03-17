---
name: preprocess-debug
description: "Debug preprocessing pipeline failures. Guides through reading checkpoint files, checking step artifacts, interpreting QC metrics, examining visualization PNGs, and identifying which step failed and why. Use when a preprocessing run produces unexpected results, crashes, or generates poor-quality outputs."
---

# Preprocess Debug — Preprocessing Failure Diagnosis

## When to Use

- "Why did preprocessing fail for patient X?"
- "The registration output looks wrong"
- "Skull stripping removed too much / too little"
- "Intensity normalization produced weird values"
- "Which step is causing the problem?"
- Any preprocessing quality issue or crash investigation

## Diagnostic Workflow

### Step 1: Identify the failing step

Check the visualization directory for which step produced the last PNG:

```bash
ls -la {viz_root}/MenGrowth-XXXX/MenGrowth-XXXX-YYY/
# step1_data_harmonization_t1c.png  ← exists
# step2_bias_field_correction_t1c.png  ← exists
# step3_resampling_t1c.png  ← MISSING → Step 3 failed
```

Check logs for error messages (look for `ERROR` or `RuntimeError`).

### Step 2: Check step artifacts

Each step may produce artifacts in `{artifacts}/MenGrowth-XXXX/MenGrowth-XXXX-YYY/`:

| Artifact | Produced by | What to check |
|----------|-------------|---------------|
| `t1c_bias_field.nii.gz` | Bias field correction | Should be smooth, low-frequency field |
| `t1c_brain_mask.nii.gz` | Skull stripping | Load in viewer — verify mask covers brain + tumor |
| `*.h5`, `*.mat` transforms | Registration | Verify transforms exist and are non-zero |

### Step 3: Examine visualization PNGs

Each step's PNG shows before/after comparison. Look for:

| Step | What to check in visualization |
|------|-------------------------------|
| Data harmonization | Orientation correct? Background removed? |
| Bias field correction | Intensity gradients reduced? |
| Resampling | Resolution changed? No aliasing artifacts? |
| Cubic padding | Volume centered? Correct padding extent? |
| Registration | Modalities aligned? Atlas overlay reasonable? |
| Skull stripping | Mask boundary at brain surface? Tumor included? |
| Intensity normalization | Histogram shifted to expected range? |
| Longitudinal registration | Timepoints aligned? No excessive deformation? |

### Step 4: Check specific failure patterns

#### Registration failures
- **"No reference modality found"**: Check that `reference_modality_priority` matches available modalities
- **Poor alignment**: Try `engine: "antspyx"` instead of `"nipype"` (or vice versa)
- **Divergence**: Check if `use_center_of_mass_init: true` is set
- **ANTs crash**: Look for `ITK ERROR` in logs; check if input volumes have valid affine matrices
- **Quality warning**: If correlation dissimilarity > `quality_warning_threshold`, registration may have failed

#### Skull stripping failures
- **Over-stripping (tumor removed)**: HD-BET is more robust to pathology than SynthStrip; try `method: "hdbet"` with `hdbet_mode: "accurate"`
- **Under-stripping (skull remaining)**: Increase SynthStrip `border` parameter or switch methods
- **GPU OOM**: Set `hdbet_device: "cpu"` or `synthstrip_device: "cpu"`

#### Intensity normalization failures
- **All zeros output**: Check that brain mask exists and covers tissue
- **Extreme values**: Use `clip_range: [-5.0, 5.0]` for z-score
- **NaN values**: Input may contain NaN — check with `nib.load(path).get_fdata()` for NaN/Inf
- **Wrong mask source**: Check logs for "Using brain mask from:" vs "using nonzero voxels as fallback"

#### Data harmonization failures
- **Wrong orientation**: Check `reorient_to` matches expected convention (RAS vs LPS)
- **Background not removed**: Try `method: "otsu_foreground"` instead of default
- **NRRD parse error**: Check if input file is valid NRRD with `nrrd.read(path)`

#### Resampling failures
- **ECLARE environment not found**: Verify `conda_environment_eclare` matches installed env
- **GPU OOM with ECLARE**: Reduce `batch_size` or switch to `method: "bspline"`
- **Extreme anisotropy**: Use `method: "composite"` for volumes with > 5mm slice thickness

### Step 5: Check the temp-file mechanism

If a step crashes mid-write, a `.tmp.nii.gz` file may be left behind:

```bash
find {output_root} -name "*.tmp*"
```

These should be deleted before re-running.

## Key Debugging Code Locations

| Issue | File to read |
|-------|-------------|
| Step handler logic | `mengrowth/preprocessing/src/steps/{step_name}.py` |
| Brain mask resolution | Search for `brain_mask` in the step handler |
| Registration quality metrics | `mengrowth/preprocessing/src/registration/diagnostic_parser.py` |
| Checkpoint state | `mengrowth/preprocessing/src/checkpoint.py` |
| QC metrics interpretation | `mengrowth/preprocessing/src/config.py` → `QCMetricsConfig` |
| Step execution order | YAML config `steps:` list |
| Config validation errors | `mengrowth/preprocessing/src/config.py` → `__post_init__()` methods |

## Quick Config Fixes

| Problem | Config change |
|---------|--------------|
| Step taking too long | Increase `shrink_factor`, reduce iterations |
| Registration not converging | Switch `engine`, adjust `sampling_percentage`, add transform stages |
| Mask too aggressive | Adjust `fill_value`, `border`, or switch skull stripping method |
| Step crashing on GPU | Set device to `"cpu"` in step config |
| Want to skip a step | Remove from `steps:` list or set `method: null` in step config |
| Need to re-run from step N | Remove all outputs from step N onward, or use checkpoint resume |
