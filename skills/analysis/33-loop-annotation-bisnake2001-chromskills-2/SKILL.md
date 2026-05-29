---
name: loop-annotation
description: This skill annotates chromatin loops, including enhancer/promoter assignments, CTCF-peak overlap. It automatically constructs enhancer and promoter sets when missing and outputs standardized loop categories.
---

# Loop Annotation

## Overview

This skill performs loop annotation for Hi-C/HiChIP/ChIA-PET interaction data. It identifies regulatory and structural loop types (E–E, E–P, P–P, CTCF-CTCF).

Main steps include:

- Refer to **Inputs & Outputs** to verify necessary files.
- **Always prompt user** if required files are missing.
- **Always prompt user** for genome assembly used.
- Build enhancers.bed if absent (ATAC + H3K27ac).
- Build promoters.bed if absent (.tss annotation).
- **Always prompt user** for the column index of the interaction count in the raw BEDPE file. Never decide by yourself.
- Standardize the format of the `.bedpe` file as the input of `annotateInteractions.pl`
- Run `annotateInteractions.pl` with feature sets.
- Visualization

## When to use this skill
- Regulatory loop landscape analysis.
- Enhancer–promoter mapping from chromatin loops.
- Structural loop analysis via CTCF orientation.
- Integration with ATAC/H3K27ac/TSS/CTCF datasets.
- Upstream to differential loop testing or expression integration.

## Inputs & Outputs

### Inputs
Required:
- loops.bedpe
- ctcf_peaks.bed
- genome version (user must provide)

Optional:
- enhancers.bed
- promoters.bed
- ATAC_peaks.bed
- H3K27ac_peaks.bed
- .tss or .gtf gene annotation

### Outputs

```bash
loop_annotation/
    logs/
        annotateInteractions.log
    annotations/
        interactionAnnotation.txt
        lengthDist.txt
        featureEnrichment.txt
        pairwiseFeatureEnrichment.txt # assign feature pairs to 0x0 0x1 and so on, represent the feature pairs like CTCF-CTCF, E-P
        ... # other outputs by annotateInteractions.pl
    features/
        enhancers.bed
        promoters.bed
    plots:
        loop_type.pdf
        lengthDist.pdf
```

## Decision Tree

### Step 1 — Validate inputs

If enhancers.bed or promoters.bed missing, go on to Step 2, otherwise go on to step 4 directly.

### Step 2 — Build enhancers.bed (if missing)

```bash
bedtools intersect -a ATAC_peaks.bed -b H3K27ac_peaks.bed > enhancers_raw.bed
sort -k1,1 -k2,2n enhancers_raw.bed | bedtools merge -i - > enhancers.bed
```

### Step 3 — Build promoters.bed (if missing)

Call:

- mcp__homer-tools__build_promoters

with:

- `genome`: HOMER genome identifier, provided by user
- `output_promoters_bed`: Output path for promoters.bed

### Step 4 — Standardize the input file

- mcp__homer-tools__standardize_loops_bedpe

with:

- `input_bedpe`: Input loops.bedpe file
- `index_count_column`: Column index for interaction count, provided by user
- `output_bedpe`: Output standardized loops file


### Step 5 — Annotate the loops

Call: 

- mcp__homer-tools__run_annotate_interactions

with:

- `standardized_loops`: Path to standardized loops file for annotateInteractions.pl
- `genome`: HOMER genome identifier, provided by user
- `feature_beds`: List of feature BED files for -p (CTCF, enhancers, promoters, etc.)
- `annotations_dir`: Base output directory for loop annotation
- `logs_dir`: Output directory for logs

### Step 6 — Classify and visualize loop types

Call: 

- mcp__homer-tools__summarize_loop_annotations_and_plot

with:
- `annotations_dir`: Directory containing HOMER `interactionAnnotation.tx`t and `lengthDist.txt`
- `plots_dir`: Output directory for plots
- `feature_map`: Mapping of feature index to feature name, you can infer the dict from `pairwiseFeatureEnrichment.txt` file.
(e.g. {'0': 'CTCF','1': 'E','2': 'P'})