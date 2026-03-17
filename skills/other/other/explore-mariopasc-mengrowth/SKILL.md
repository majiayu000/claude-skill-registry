---
name: explore
description: "Navigate and understand the MenGrowth codebase (both curation and preprocessing pipelines). Use when asked to find where something is implemented, understand how a phase/step works, trace data flow, debug a rejection or preprocessing failure, or identify where to add new functionality."
---

# Explore — MenGrowth Codebase Navigation

## When to Use

- "Where is X implemented?"
- "How does phase/step N work?"
- "Why was patient/file X rejected?"
- "Where would I add a new quality check / modality / plot / preprocessing step?"
- "What calls what?" or "Trace the data flow for ..."
- Any task that requires understanding the codebase before modifying it

## Quick Module Map

```
mengrowth/
  cli/
    curate_dataset.py              ← Curation pipeline orchestrator
    preprocess.py                  ← Preprocessing pipeline CLI
  preprocessing/
    config.py                      ← Curation config dataclasses (grep for @dataclass)
    utils/
      reorganize_raw_data.py       ← Phase 1 (scan_source_baseline, scan_source_controls, copy_and_organize)
      filter_raw_data.py           ← Phase 2 (filter_dataset) + Phase 4 (reid_patients_and_studies)
      quality_filtering.py         ← Phase 3 (run_quality_filtering, validate_file, _validate_patient)
      metadata.py                  ← MetadataManager, PatientMetadata, Excel parsing
    quality_analysis/
      analyzer.py                  ← Phase 5 (QualityAnalyzer.run, scan_dataset, analyze_patient)
      metrics.py                   ← Per-image metric functions (SimpleITK-based)
      visualize.py                 ← Phase 6 (QualityVisualizer, generate_html_report)
    src/
      config.py                    ← Preprocessing config (StepRegistry, StepMetadata, all step configs)
      preprocess.py                ← PreprocessingOrchestrator (step execution engine)
      base.py                      ← BasePreprocessingStep ABC (execute + visualize)
      steps/
        step_registry.py           ← Re-exports StepRegistry from config
        data_harmonization.py      ← Step 1 handler
        bias_field_correction.py   ← Step 2 handler
        resampling.py              ← Step 3 handler
        cubic_padding.py           ← Step 4 handler
        registration.py            ← Step 5 handler
        skull_stripping.py         ← Step 6 handler
        intensity_normalization.py ← Step 7 handler
        longitudinal_registration.py ← Step 8 handler
      data_harmonization/          ← NRRD→NIfTI (io.py), reorientation (orient.py), head masking
      bias_field_correction/       ← N4 via SimpleITK (n4_sitk.py)
      resampling/                  ← BSpline, ECLARE, Composite
      registration/                ← ANTs registration (nipype + antspyx implementations)
      skull_stripping/             ← HD-BET (hdbet.py), SynthStrip (synthstrip.py)
      normalization/               ← Z-score, KDE, FCM, WhiteStripe, PercentileMinMax, LSQ
      checkpoint.py                ← Checkpoint/resume support
```

## Exploration Strategies

### Strategy 1: "Where is feature X?"

| Looking for... | Go to |
|----------------|-------|
| A CLI flag or argument (curation) | `cli/curate_dataset.py` → argparse section |
| A CLI flag or argument (preprocessing) | `cli/preprocess.py` → argparse section |
| A curation threshold or default | `preprocessing/config.py` → search the dataclass name |
| A preprocessing config or default | `preprocessing/src/config.py` → search the dataclass name |
| A quality check (A1–E1) | `preprocessing/utils/quality_filtering.py` → search by check ID or function |
| Modality synonym mapping | `preprocessing/config.py` → `RawDataConfig.standardize_modality()` |
| Patient ID normalization | `preprocessing/utils/reorganize_raw_data.py` → `extract_patient_id()` |
| Re-identification logic | `preprocessing/utils/filter_raw_data.py` → `reid_patients_and_studies()` |
| A curation plot or visualization | `preprocessing/quality_analysis/visualize.py` |
| Clinical metadata field | `preprocessing/utils/metadata.py` → `PatientMetadata` dataclass |
| Rejection tracking | Search for `rejected_files` or `rejection_reason` across utils/ |
| Step execution level | `preprocessing/src/config.py` → `STEP_METADATA` dict |
| Step handler registration | `preprocessing/src/preprocess.py` → `_register_step_handlers()` |
| Brain mask resolution | Step handler's `_resolve_mask_path()` or search for `brain_mask` |
| Registration diagnostics | `preprocessing/src/registration/diagnostic_parser.py` |
| Normalization methods | `preprocessing/src/normalization/` → one file per method |

### Strategy 2: "How does data flow through phase/step N?"

**Curation phases:**

| Phase | Entry Function | Key Subfunctions |
|-------|---------------|-----------------|
| 1 | `reorganize_raw_data()` | `scan_source_baseline()`, `scan_source_controls()`, `copy_and_organize()` |
| 2 | `filter_dataset()` | `normalize_study_sequences()`, `remove_non_required_sequences()` |
| 3 | `run_quality_filtering()` | `_validate_patient()` → `validate_file()`, study-level, patient-level |
| 4 | `reid_patients_and_studies()` | Inline in `filter_raw_data.py` |
| 5 | `QualityAnalyzer.run()` | `scan_dataset()`, `analyze_patient()`, `compute_*_metrics()` |
| 6 | `QualityVisualizer.generate_all()` | Individual plot methods, `generate_html_report()` |

**Preprocessing steps:**

| Step | Handler Location | Key Implementation |
|------|-----------------|-------------------|
| 1 | `steps/data_harmonization.py` | `data_harmonization/io.py`, `orient.py`, `head_masking/` |
| 2 | `steps/bias_field_correction.py` | `bias_field_correction/n4_sitk.py` |
| 3 | `steps/resampling.py` | `resampling/bspline.py`, `eclare.py`, `composite.py` |
| 4 | `steps/cubic_padding.py` | Inline padding logic |
| 5 | `steps/registration.py` | `registration/multi_modal_coregistration.py`, `intra_study_to_atlas.py` |
| 6 | `steps/skull_stripping.py` | `skull_stripping/hdbet.py`, `synthstrip.py` |
| 7 | `steps/intensity_normalization.py` | `normalization/zscore.py`, `kde.py`, etc. |
| 8 | `steps/longitudinal_registration.py` | `registration/longitudinal_registration.py` |

### Strategy 3: "Why was patient/file X rejected?"

1. Open `quality/rejected_files.csv`
2. Filter by `patient_id` or `filename`
3. Check `stage` column:
   - **0** → Phase 1 (reorganization): file excluded by glob pattern, unrecognized modality, or duplicate
   - **1** → Phase 2 (completeness): missing sequences or insufficient studies
   - **2** → Phase 3 (quality): failed a blocking check
4. If stage=2, cross-reference with `quality/quality_issues.csv` for the specific `check_name`
5. To find the check implementation: search `quality_filtering.py` for the `check_name` value

### Strategy 4: "Where do I add a new ___?"

| Adding... | Steps |
|-----------|-------|
| **Quality check** | 1. Add config `@dataclass` in `config.py` under `QualityFilteringConfig`. 2. Add function in `quality_filtering.py` returning `ValidationResult`. 3. Wire into `validate_file()` or study/patient level. |
| **Preprocessing step** | 1. Create handler in `src/steps/`. 2. Add `StepMetadata` entry in `src/config.py`. 3. Add config `@dataclass` in `src/config.py`. 4. Register handler in `preprocess.py` → `_register_step_handlers()`. |
| **Modality** | Add synonyms in `configs/raw_data.yaml` → `modality_synonyms`. If required, add to `FilteringConfig.sequences`. |
| **Source directory** | Add scanner function in `reorganize_raw_data.py`. Call from `reorganize_raw_data()`. |
| **Plot** | Add method to `QualityVisualizer`. Add toggle in `PlotConfig`. Call from `generate_all()`. |
| **Metric** | Add function in `metrics.py`. Wire into `analyze_patient()` in `analyzer.py`. |
| **Normalization method** | Add class in `src/normalization/`. Import in `preprocess.py`. Add to config dispatch. |
| **Registration variant** | Add implementation in `src/registration/`. Update factory in `factory.py`. |

## Key Patterns to Recognize

### Configuration Pattern
Every tunable parameter is a field in a `@dataclass` with a default value, parsed from YAML:
```python
@dataclass
class SomeCheckConfig:
    enabled: bool = True
    threshold: float = 5.0
    action: str = "block"
```

### Validation Result Pattern (Curation)
Every quality check returns:
```python
ValidationResult(passed=bool, check_name=str, message=str, action="warn"|"block", details=dict)
```

### Step Execution Pattern (Preprocessing)
```python
StepExecutionContext(patient_id, study_dir, modality, paths, orchestrator, step_name, step_config)
```
Handlers receive context and dispatch to implementation classes (e.g., `ZScoreNormalizer`, `BSplineResampler`).

### Parallel Execution Pattern
- CPU-bound → `ProcessPoolExecutor` at patient granularity
- I/O-bound → `ThreadPoolExecutor` at file granularity
- Results sorted by ID after collection for determinism
- All arguments must be picklable (pure dataclasses, Paths, primitives)

### Temp-File Pattern (Preprocessing)
```python
temp_path = output_path.with_suffix('.tmp.nii.gz')
# ... write to temp_path ...
temp_path.rename(output_path)
```

## Grep Cheatsheet

```bash
# Find a quality check by ID
grep -n "check_name.*snr\|B1" mengrowth/preprocessing/utils/quality_filtering.py

# Find all blocking checks
grep -n 'action.*=.*"block"' mengrowth/preprocessing/utils/quality_filtering.py

# Find all curation config dataclasses
grep -n "@dataclass" mengrowth/preprocessing/config.py

# Find all preprocessing config dataclasses
grep -n "@dataclass" mengrowth/preprocessing/src/config.py

# Find step execution levels
grep -n "StepMetadata" mengrowth/preprocessing/src/config.py

# Find where a patient gets rejected
grep -rn "mark_excluded\|rejection_reason" mengrowth/preprocessing/utils/

# Find parallel execution points
grep -rn "ProcessPoolExecutor\|ThreadPoolExecutor" mengrowth/

# Find all CLI flags
grep -n "add_argument" mengrowth/cli/curate_dataset.py mengrowth/cli/preprocess.py

# Find brain mask resolution
grep -rn "brain_mask" mengrowth/preprocessing/src/

# Find normalization implementations
grep -rn "class.*Normalizer" mengrowth/preprocessing/src/normalization/
```

## File Format Reference

| File | Location | Schema |
|------|----------|--------|
| `rejected_files.csv` | `quality/` | `source_path, filename, patient_id, study_name, rejection_reason, source_type, stage` |
| `quality_issues.csv` | `quality/` | `patient_id, study_id, modality, file_path, check_name, action, message, level, details` |
| `id_mapping.json` | `dataset/` | `{P*: {new_id: MenGrowth-*, studies: {old_idx: new_id}}}` |
| `quality_metrics.json` | `quality/` | Hierarchical: patient → study → modality → metric values |
| `per_study_metrics.csv` | `qc_analysis/` | One row per (study, sequence) with all computed metrics |
| `metadata_enriched.csv` | `dataset/` | `patient_id, age, sex, ..., included, exclusion_reason, MenGrowth_ID` |
