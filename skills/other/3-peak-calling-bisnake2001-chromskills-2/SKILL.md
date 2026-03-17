---
name: peak-calling
description: Perform peak calling for ChIP-seq or ATAC-seq data using MACS3, with intelligent parameter detection from user feedback. Use it when you want to call peaks for ChIP-seq data or ATAC-seq data.
---

# Peak Calling

## Overview

This skill automatically performs core **peak calling** with **MACS2** for **ChIP-seq** and **ATAC-seq** data, based on the BAM files in the current directory. It includes automatic experiment recognition and parameter selection.

Main steps include:
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- **Always prompt user** for `genome_size` to use (e.g. hs or mm). **Never decide by yourself**.
- **Always prompt user** if required control files are missing for ChIP-seq data.
- **Always prompt user** for the q value cutoff for peak calling.
- **Detect experiment type** (TF, histone mark, or ATAC-seq).
- **Automatically decide** whether to call narrow or broad peaks.
- Always use filtered BAM file (`filtered.bam`) if available.
- **Detect sequencing type** (single-end or paired-end) using SAM/BAM flags.  
- **Perform MACS3 peak calling** accordingly.
- **Generate a parameter log file** (`${sample}_used_parameters.txt`) with justification for each chosen option.
 
---

## Inputs & Outputs

### Inputs

```bash
${sample}.bam # filtered bam files
```

### Outputs

```bash
all_peak_calling/
  peaks/
    ${sample}.narrowPeak # or ${sample}.broadPeak
  temp/
  logs/
    ${sample}_used_parameters.txt
```
----

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: peak_calling
- `genome`: provided by user

The tool will:

- Create `${sample}_peak_calling` directory.
- Return the full path of the `${sample}_peak_calling` directory, which will be used as `${proj_dir}`.

### Step 1. Identify and Classify BAM Files

**Command Example**
```bash
find . -name "*.bam" | sort
```
- **Treatment BAMs**: filenames contain TF names or histone marks (e.g., `CTCF`, `H3K27me3`, `ATAC`).
- **Control BAMs**: filenames contain “input”, “control”, or “IgG”.
- Prefer **filtered** BAMs (`*.filtered.bam`) if available.

---

### Step 2. Detect Sequencing Type (Single-End or Paired-End)

**Command Example**
```bash
samtools flagstat sample.bam | egrep "properly paired|singletons"
```

- If `properly paired > 0` → Paired-end (`-f BAMPE`)
- If `singletons ≈ total` → Single-end (`-f BAM`)

---

### Step 3. Detect Experiment Type and Choose Peak Mode

| Detected Pattern | Experiment Type | Peak Type | Parameter Key Options |
|------------------|-----------------|------------|------------------------|
| TF name (CTCF, GATA1, MYC, TP53…) | TF ChIP-seq | Narrow | `--call-summits -q 0.01` |
| Active histone marks (H3K4me3, H3K27ac, H3K9ac) | Histone (sharp) | Narrow | `--call-summits -q 0.05` |
| Broad histone marks (H3K27me3, H3K9me3, H3K36me3) | Histone (broad) | Broad | `--broad --broad-cutoff 0.1 -q 0.05` |
| H3K4me1 | Intermediate | Narrow | `--call-summits -q 0.05` (optional `--broad`) |
| ATAC | ATAC-seq | Narrow | `--nomodel --shift -100 --extsize 200 -q 0.05` |

---

### Step 4. Execute MACS3 with Auto Parameters

Call:

- mcp__macs2-tools__run_macs2

with: 
- `treatment_file`: Path to treatment BAM file.
- `control_file`: Path to control/input BAM file. Required for ChIP-seq data. **Prompt the user for the required file if not provided**.
- `genome_size`: Always provided by user.
- `name`: Experiment name (prefix for output files).
- `out_dir`: ${proj_dir}/peaks
- `broad`: If True, call broad peaks (for histone marks).
- `broad_cutoff`: Cutoff for broad region calling.
- `qvalue`: Q-value cutoff for peak detection. **Prompt the user for the q value cutoff**.
- `format`: use BAMPE for pair-end data, BAM for single-end data.
- `nomodel`: True for ATAC-seq, False for ChIP-seq.
- `shift`: Shift size in bp (e.g., -100 for ATAC-seq).
- `extsize`:"Extension size in bp (e.g., 200 for ATAC-seq).

---

### Step 5. Generate Parameter Log File

After auto-selection, the skill writes a log file:

**Example content:**
```
Genome detected: 
Experiment type: H3K27me3 (broad histone)
Sequencing type: paired-end
Control used: input_control.bam
MACS3 mode: --broad --broad-cutoff 0.1 -q 0.05
Reasoning:
- Broad mark (H3K27me3) requires domain-level detection
- Control detected and applied
- Genome identified as <*>; using -g <*>
- Paired-end library; use -f BAMPE
```