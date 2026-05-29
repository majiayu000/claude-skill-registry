---
name: replicates-incorporation
description: This skill manages experimental reproducibility, pooling, and consensus strategies. This skill operates in two distinct modes based on the input state. (1) Pre-Peak Calling (BAM Mode): It merges all BAMs, generate the merge BAM file to prepare for track generation and (if provided with >3 biological replicates) splits them into 2 balanced "pseudo-replicates" to prepare for peak calling. (2) Post-Peak Calling (Peak Mode): If provided with peak files (only support two replicates, derived from either 2 true replicates or 2 pseudo-replicates), it performs IDR (Irreproducible Discovery Rate) analysis, filters non-reproducible peaks, and generates a final "conservative" or "optimal" consensus peak set. Trigger this skill when you need to handle more than two replicates (creating pseudo-reps) OR when you need to merge peak lists.
---

# Replicates Incorporation Skill

## Overview

This skill provides two modes for replicates incorporation:

- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- Always use filtered BAM file (`*.filtered.bam`) if available.
- Pre-Peak Calling (BAM Mode): If provided with >3 biological replicates, it merges all BAMs, generate the merge BAM file to prepare for track generation and splits them into 2 balanced "pseudo-replicates" to prepare for peak calling.
- Post-Peak Calling (Peak Mode): If provided with peak files (only support two replicates, derived from either 2 true replicates or 2 pseudo-replicates), it performs IDR (Irreproducible Discovery Rate) analysis, filters non-reproducible peaks, and generates a final "conservative" or "optimal" consensus peak set

---

## Decision Tree

### Step 0: Initialize Project

Call:

- `mcp__project-init-tools__project_init`

with:

- `sample`: all
- `task`: rep_merge

The tool will:

- Create `all_rep_merge` directory.
- Return the full path of the `all_rep_merge` directory, which will be used as `${proj_dir}`

### Pre-Peak Calling (BAM Mode)

Call:
- `mcp__bw_tools__pool_bams`
with:
- `bam_files`: `[${rep1_bam}, ${rep2_bam}, ${rep3_bam}]` (Add as many as needed)
- `output_bam`: `${proj_dir}/temp/${sample}.pooled.bam`

Call: (call this only when more than two replicates are provided)
- `mcp__bw_tools__split_pseudo_replicates`
with:
bam_file: `${proj_dir}/temp/${sample}.pooled.bam`
output_rep1: `${proj_dir}/temp/${sample}.pseudo1.bam`
output_rep2: `${proj_dir}/temp/${sample}.pseudo2.bam`


---

### Post-Peak Calling (Peak Mode)

**A. Narrow Peaks / ATAC (IDR)**
Use this to combine reproducible peaks. You should ideally run IDR on:
1.  True Replicates
2.  Pseudo-Replicates

Call:
- `mcp__bw_tools__filter_idr_peaks`
with:
- `peak_file_a`: Path to Replicate 1 narrowPeak file.
- `peak_file_b`: Path to Replicate 2 narrowPeak file.
- `output_optimal`: `${proj_dir}/peaks/${sample}.idr.narrowPeaks`
- `output_raw_idr`: `${proj_dir}/temp/${sample}_idr_results.tsv`
- `input_file_type`: narrowPeak
- `rank_measure`: q.value


**B. Broad Peaks (Consensus)**
Call:
- `mcp__bw_tools__merge_consensus_peaks`
with:
`peak_file_a`: Path to Replicate 1 broadPeak file.
`peak_file_b`: Path to Replicate 2 broadPeak file.
`output_peak`: `${proj_dir}/peaks/${sample}.consensus.broadPeaks`
`overlap_fraction`: 0.5


---

## Best Practices

- **Use pooled tracks** for visualization and differential analysis.
- **Keep individual replicate tracks** for QC and reproducibility evaluation.
- **Use IDR ≤ 0.05** for reproducible narrow ChIP-seq peaks and ATAC-seq.
- **Use overlap ≥50% ** for broad histone mark peaks.
