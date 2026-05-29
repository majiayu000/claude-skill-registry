---
name: ATACseq-QC
description:Performs ATAC-specific biological validation. It calculates metrics unique to chromatin accessibility assays, such as TSS enrichment scores and fragment size distributions (nucleosome banding patterns). Use this skill when you have filtered BAM file and have called peak for the file. Do NOT use this skill for ChIP-seq data or general alignment statistics.
---

# ATAC-seq Quality Control

## Overview

This skill performs complete ATAC-seq data quality control from BAM and peak files.

Main steps include:
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- **Always prompt user** for genome assembly used. Never decide by yourself. 
- Generate TSS files according to genome assembly.
- Compute TSS enrichment, fragment distribution and FRiP. 

---

## Inputs & Outputs

### Inputs

```bash
${sample}.bam # filtered bam files
${sample}.narrowPeak
```

### Outputs

```bash
all_atac_qc/
    ${sample}_qc_results/
        ataqv_metrics.json
        ataqv_report.html/
    temp/
```

---

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: atac_qc
- `genome`: provided by user

The tool will:

- Create`all_atac_qc` directory.
- Return the full path of the `all_atac_qc` directory, which will be used as `${proj_dir}`.

### Step 1: Detect the name logic of the chromosomes in BAM file (have "chr" as prefix or not)

`samtools view <sample>.bam | head -n 10 | cut -f 3`

### Step 2: Generate reference files

Call:
- mcp__qc-tools__generate_reference

with:
- `genome`: Genome name (e.g., hg38), provided by user
- `temp_dir`: ${proj_dir}/temp
- `bam_uses_chr`: True if BAM uses 'chr' prefix (chr1), False if not (1).

### Step 3: Peform quality control for the ATAC-seq data

Call:
- mcp__qc-tools__run_ataqv_qc

- `bam_file`: Path to filtered BAM file
- `peak_file`: Path to peak file (narrowPeak) corresponding to the BAM file
- `tss_file`: ${proj_dir}/temp/${genome}.tss
- `species`: Species used, choose from (fly, human, mouse, rat, worm, yeast)
- `bam_uses_chr`: True if BAM uses 'chr' prefix (chr1), False if not (1).
- `output_dir`: ${proj_dir}/${sample}_qc_results
- `autosomal_ref_path`: Provided if `bam_uses_chr` is False, ${proj_dir}/temp/${genome}.autosomal.ref
