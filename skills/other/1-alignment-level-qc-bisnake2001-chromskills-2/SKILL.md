---
name: alignment-level-QC
description: Calculates technical mapping statistics for any aligned BAM file (ChIP or ATAC). It assesses the performance of the aligner itself by generating metrics on read depth, mapping quality, error rates, and read group data using samtools and Picard.Use this skill to check "how well the reads mapped" or to validate BAM formatting/sorting before further processing. Do NOT use this skill for biological signal validation (like checking for peaks or open chromatin) or for filtering/removing reads.
---

# Alignment Quality Control for ChIP-seq/ATAC-seq

## Overview

Perform comprehensive **preliminary alignment-level quality control** for ChIP-seq and ATAC-seq BAM files using **samtools**, **Picard**, and **MultiQC**.  

Main steps include:
- Initialize the project directory.
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- Sort and add read groups if missing in the BAM file.
- Run preliminary QC metrics
- **Generate MultiQC report**  

---

## When to use this skill

- Use skill when you want to perform alignment-level quality control for ChIP-seq or ATAC-seq BAM files.

---

## Inputs & Outputs

### Inputs

<sample>.bam

### Outputs

```bash
alignment_qc/
  ${sample}.bam                        # Original input
  ${sample}.sorted.bam                 # (Optional) Created if sorting was needed
  ${sample}.RG.bam                     # (Optional) Created if RG was needed
  ${sample}.RG.bam.bai                 # Index file
  qc_results/
    ${sample}.flagstat.txt
    ${sample}.stats.txt
    ${sample}.insertsize_metrics.txt
    ${sample}.dup_metrics.txt
    alignment_qc_report.html      # Visual MultiQC report
    qc_summary.txt                # Pass/Warn/Fail table
  temp/
    ${sample}.markdup.bam            # Intermediate file (safe to delete later)
    ...
```
---

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: alignment_qc

The tool will:

- Create `${sample}_alignment_qc` directory.
- Return the full path of the `${sample}_alignment_qc` directory, which will be used as `${proj_dir}`.

### Step 1: Check and Fix BAMs
- Ensure all BAM files are coordinate-sorted, have Read Groups, and are indexed.
*This tool will skip files that are already correct and only create temporary files when fixes are needed.*

Call: 

- mcp__qc-tools__check_and_fix_bams

with:
- `bam_files`: List of BAM files to process.
- `temp_dir`: ${proj_dir}/temp

### Step 2: Run Alignment QC Metrics

Call:

- mcp__qc-tools__run_bam_qc

with:
- `bam_files`: List of BAM files to process.
- `qc_dir`: ${proj_dir}/qc_results
- `temp_dir`: ${proj_dir}/temp

Step 3: Generate Summary Report

Call:

- mcp__qc-tools__generate_qc_report

with:
- `qc_dir`: ${proj_dir}/qc_results

---

## Quality Assessment

### Key QC Metrics

- **Total reads** – overall sequencing depth  
- **Mapped reads (%)** – alignment efficiency  
- **Properly paired (%)** – valid pair fraction (paired-end)  
- **Duplicate rate (%)** – PCR duplication estimate  
- **Mitochondrial reads (%)** – mitochondrial contamination  
- **Insert size distribution** – fragment length profile  

All metrics are derived from `samtools`/`Picard` and summarized by MultiQC.

---

### Quality Thresholds

| Category | Criteria | Interpretation |
|-----------|-----------|----------------|
| **Pass** | All metrics within recommended thresholds | Suitable for downstream analysis |
| **Warn** | One or more borderline metrics | Likely acceptable; review recommended |
| **Fail** | Critical metrics outside acceptable ranges | Re-sequencing or reprocessing suggested |

---

## Report Generation

After MultiQC completes, generate a sample-wise summary (PASS/WARN/FAIL) per thresholds in `references/qc_metrics.md` and save it as:

```
qc_results/qc_summary.txt
```

---

## Resources

Use `references/qc_metrics.md` for:
- Metric definitions and recommended thresholds  
- Troubleshooting guidance  
- Readiness criteria for peak calling  
- Pointers to ENCODE/nf-core QC standards
