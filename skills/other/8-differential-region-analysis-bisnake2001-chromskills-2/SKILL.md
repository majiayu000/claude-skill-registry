---
name: differential-region-analysis
description: The differential-region-analysis pipeline identifies genomic regions exhibiting significant differences in signal intensity between experimental conditions using a count-based framework and DESeq2. It supports detection of both differentially accessible regions (DARs) from open-chromatin assays (e.g., ATAC-seq, DNase-seq) and differential transcription factor (TF) binding regions from TF-centric assays (e.g., ChIP-seq, CUT&RUN, CUT&Tag). The pipeline can start from aligned BAM files or a precomputed count matrix and is suitable whenever genomic signal can be summarized as read counts per region.
---

# Differential Region Analysis with DESeq2

## Overview

This skill performs differential region analysis between experimental conditions using DESeq2 in a count-based framework. 
Main steps include:

- Initialize the project directory.
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- **Always prompt user** if required files are missing.
- **Always prompt user** for the threshold of `qvalues` and `log2foldchange` to define significant regions.
- Merge peaks across replicates or samples to build a consensus peak set.  
- Generate read count matrix over peaks using featureCounts or bedtools.  
- Prepare sample metadata file describing conditions and replicates.  
- Perform differential analysis using DESeq2.  
- Visualize and interpret results (PCA, volcano plot). 
- Output significantly up and down accessible regions.

---

## When to use this skill
Use the differential-region-analysis pipeline when your goal is to identify genomic regions with condition-dependent changes in signal intensity, provided the signal can be represented as raw read counts per region.

Recommended scenarios include:

- Comparing treated vs. control samples to identify regulatory regions responsive to a drug, signaling molecule, or environmental change.
- Investigating cell differentiation or developmental trajectories to reveal dynamic chromatin remodeling.
- Analyzing disease vs. normal tissues to pinpoint dysregulated enhancer or promoter accessibility.
- Integrating with RNA-seq or ChIP-seq data to connect chromatin accessibility with transcriptional or epigenetic regulation.

The pipeline performs best with datasets containing biological replicates (≥2 per condition) and moderate to high sequencing depth (~20–50 million reads per sample).

---

## Inputs & Outputs

### Inputs (choose one)

- If starting from BAM files and BED peak files → Generate consensus peaks and count matrix.  
- If starting from existing count matrix → Go directly to DESeq2 analysis.  
- If multiple conditions or batches → Include batch/condition in design 

### Outputs

```bash
${sample}_DAR_analysis/ # or ${tf}_${sample}_DB_analysis in differential TF binding detection task
    tables/
      all_peaks.bed
      consensus_peaks.bed # Unified peak set
      atac_counts.txt # Count matrix of reads per peak
      samples.csv # Sample metadata
    DARs/
      DAR_results.csv # DESeq2 results (log2FC, p-values)
      DAR_sig.bed # Significantly diffential accessible regions
      DAR_up.bed
      DAR_down.bed  
    plots/ # visualization outputs
      PCA.pdf
      Volcano.pdf
    logs/ # analysis logs 
    temp/ # other temp files
```
---

## Decision Tree

### Step 0: Initialize Project

1. Make director for this project:

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: sample name (e.g. c1_vs_c2)
- `task`: DAR_analysis

The tool will:

- Create `${sample}_DAR_analysis` (or `${tf}_${sample}_DB_analysis`) directory.
- Return the full path of the `${sample}_DAR_analysis` (or `${tf}_${sample}_DB_analysis`) directory, which will be used as `${proj_dir}`.


### Step 1: Generate Consensus Peaks

Combine peaks from replicates to define a shared feature space.
Call:
- mcp__pydeseq2-tools__generate_consensus_peaks
with:
- `bed_files`: List of paths to peak BED files from replicates.
- `output_bed`: Output path for the merged consensus BED file.
- `output_saf`: Output path for the SAF file (needed for featureCounts)


Output: `consensus_peaks.bed`, `consensus_peaks.saf`

---

### Step 2: Generate Count Matrix

Call:
- mcp__pydeseq2-tools__count_reads_featurecounts

with:

- `saf_file`: SAF file output from Step 1.
- `bam_files`: List of paths to BAM files.
- `output_counts`: Path to output count matrix.
- `is_paired_end`: Whether the BAM file is pair end or not.
- `threads`

Output: `atac_counts.txt`

---

### Step 3: Prepare Metadata

Prepare `samples.csv` describing condition and replicate information.

```csv
sample,condition,replicate
sample1.bam,c1,1
sample2.bam,c1,2
sample3.bam,c2,1
sample4.bam,c2,2
```

---

### Step 4: Differential Accessibility with pyDESeq2

Call: 

- mcp__pydeseq2-tools__run_pydeseq2_analysis

with: 
- counts_file: Path to featureCounts from Step 2.
- metadata_file: Path to metadata CSV from Step 3.
- design_factors: Design formula columns (e.g. 'condition' or 'batch,condition').
- contrast_column: Column name for contrast (e.g. 'condition').
- contrast_control: Control group name (e.g. 'Control').
- contrast_treatment: Treatment group name (e.g. 'Treated').
- output_csv: Output path for results CSV.

Output: `DAR_results.csv` or `${tf}_DB_results.csv`

---

### Step 5: Visualization and QC
Call:

- mcp__pydeseq2-tools__visualize_results

with:
- `results_csv`: Path to DESeq2 results CSV.
- `counts_file`: Path to original counts file (for PCA).
- `metadata_file`: Path to metadata (for PCA grouping).
- `output_dir`: Directory to save plots.
- `condition_col`: (e.g."condition")


---

### Step 6: Output significantly up and down accessible regions

Call:

- mcp__pydeseq2-tools__filter_and_export_bed

with:

- `results_csv`: Path to DESeq2 results CSV.
- `output_prefix`: Prefix for output BED files.
- `padj_cutoff`: Provided by user
- `log2fc_cutoff`: Provided by user


Output: `DAR_sig.bed` `DAR_up.bed` `DAR_down.bed` or `${tf}_DB_sig.bed` `${tf}_DB_up.bed` `${tf}_DB_down.bed`

## Advanced Usage

- **Batch effects**: `design = ~ batch + condition`
- **Multi-group comparison**: `contrast=c("condition","A","B")`
- **Time series**: `DESeq(dds, test="LRT", reduced=~1)`
- **Filter low counts**: `dds[rowSums(counts(dds)) >= 20, ]`

---

## Notes & Troubleshooting

| Issue | Solution |
|-------|-----------|
| Very low counts | Increase threshold (`rowSums >= 20`) |
| Batch effect | Add batch term to design |
| Non-converging model | Use `fitType="local"` or `betaPrior=FALSE` |
| Mismatched sample names | Ensure count column names match metadata rows |
