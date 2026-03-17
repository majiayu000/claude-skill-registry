---
name: ChIPseq-QC
description: Performs ChIP-specific biological validation. It calculates metrics unique to protein-binding assays, such as Cross-correlation (NSC/RSC) and FRiP. Use this when you have filtered the BAM file and called peaks for ChIP-seq data. Do NOT use this skill for ATAC-seq data or general alignment statistics.
---

# Comprehensive ChIP-seq QC Pipeline

## Overview

This skill performs a full ChIP-seq quality control analysis from aligned BAM files and peak files.

Main steps include:
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- **Perform cross-correlation analysis** to calculate **NSC** and **RSC**.  
- **Compute FRiP (Fraction of Reads in Peaks)** using peak files and aligned BAMs.

---

## Inputs & Outputs

### Inputs

```bash
${sample}.bam # filtered bam files
${sample}.narrowPeak # or broadPeak
```

### Outputs

```bash
all_chip_qc/
    ${sample}_spp.txt
    ${sample}_crosscorr.pdf
    ${sample}_frip.txt
```

----

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: atac_qc

The tool will:

- Create`all_chip_qc` directory.
- Return the full path of the `all_chip_qc` directory, which will be used as `${proj_dir}`.

### Step 1: Calculate Cross-Correlation Metrics (NSC, RSC)

Call:
- mcp__qc-tools__run_phantompeakqualtools
with:
- `bam_file`: Path to BAM file
- `output_dir`: ${proj_dir}/

Output: `${sample}_spp.txt`, `${sample}_crosscorr.pdf`

### Step 2: Calculate the fraction of reads falling within peak regions.

Call:
- mcp__qc-tools__calculate_frip
with:
bam_file: Path to BAM file.
peak_file: Path to Peak file (BED/narrowPeak/broadPeak).
output_dir: ${proj_dir}/

Output: `${sample}_frip.txt`

