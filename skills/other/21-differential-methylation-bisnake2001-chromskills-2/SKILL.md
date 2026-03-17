---
name: differential-methylation
description: This skill performs differential DNA methylation analysis (DMRs and DMCs) between experimental conditions using WGBS methylation tracks (BED/BedGraph). It standardizes input files into per-sample four-column Metilene tables, constructs a merged methylation matrix, runs Metilene for DMR detection, filters the results, and generates quick visualizations.
---

# WGBS Differential Methylation with metilene

## Overview

- Refer to the **Inputs & Outputs** section to check available inputs and design the output structure.
- **Always prompt user** for which columns in the BED files are methylation fraction/percent. Never decide by yourself.
- Convert heterogeneous inputs to a **per‑sample 4‑column Metilene table** (chrom, start, end, methylation_fraction). Sort the BED files after conversion.
- Generate the merged bed file as the input of metilene.
- **Run metilene**: call DMRs and DMCs with tunable parameters
- **Visualize**: quick plots (Δmethylation vs –log10(q), length histograms).

---

## Inputs & Outputs

### Inputs

```bash
sample1.bed # raw methylation BED files, standardize it according to the following steps
sample2.bed
```

**Assumptions**: All samples share the same reference genome build and chromosome naming scheme.

### Outputs
```bash
DMR_DMC_detection/
  stats/
    dmr_results.txt # raw metilene output.
    dmc_results.txt
    significant_dmrs.txt # filtered significant DMRs (TSV).
    significant_dmrs.bed # BED for genome browser.
    significant_dmcs.txt
    significant_dmcs.bed
    dmr_summary.txt # counts and length statistics.
  plots/
    volcano.pdf
    length_hist.pdf
  temp/
    sample1.sorted.bed
    ... # other sorted BED files
    merged_input.bed
```

---

## Decision Tree

### Step 1: Standardize BED file
- extract information from input BED files into **per‑sample 4‑column Metilene table** and sort

```bash
for sample in samples;do
  awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $2, $3, $<n>/100}' sample.bed | sort -V -k1,1 -k2,2n # n is provide by user, devided by 100 if is percentage
done
```


### Step 2: Build the merged methylation matrix (fractions per sample)

Call:
- `mcp__methyl-tools__generate_metilene_input`

with:
- `group1_files`: Comma-separated group 1 bedGraph/BED files (from Step 1, must be sorted)
- `group1_files`: Comma-separated group 2 bedGraph/BED files (from Step 1, must be sorted)
- `output_path`: Output file path for generated metilene input
- `group1_name`: Identifier of group 1
- `group2_name`: Identifier of group 2

This tool will:
- Generate a input file for metilene

### Step 3:  Run metilene (DMR mode)
Call:
- `mcp__methyl-tools__run_metilene`

with:
- `merged_bed_path`: file path for metilene input
- `group_a_name`: name of group A (e.g. `"case"`)
- `group_b_name`: name of group B (e.g. `"control"`)
- `mode`: Mode for metilene CLI (e.g. 1: de-novo, 2: pre-defined regions, 3: DMCs), assign 1 for DMR analysis
- `threads`: Always use 1 threads to avoid error
- `output_results_path`: Output path for the DMR results


### Step 4:  Run metilene (DMC mode)
Call:
- `mcp__methyl-tools__run_metilene`

with:
- `merged_bed_path`: file path for metilene input
- `group_a_name`: name of group A (e.g. `"case"`)
- `group_b_name`: name of group B (e.g. `"control"`)
- `mode`: Mode for metilene CLI (e.g. 1: de-novo, 2: pre-defined regions, 3: DMCs), assign 3 for DMR analysis
- `output_results_path`: Output path for the DMC results

### Step 5: Filter significant DMRs and export BED
Call:
- `mcp__methyl-tools__filter_dmrs` 
with:
- `metilene_results_path`: DMR results from Step 3
- `significant_tsv_path`: Output path for the DMR results (e.g. significant_dmrs.tsv)
- `significant_bed_path`: Output path for the DMR results (e.g. significant_dmrs.bed)
- `q_threshold`, `delta_threshold` as agreed.


### Step 6: Filter significant DMCs and export BED
Call:
- `mcp__methyl-tools__filter_dmrs` 
with:
- `metilene_results_path`: DMC results from Step 4
- `significant_tsv_path`: Output path for the DMC results (e.g. significant_dmcs.tsv)
- `significant_bed_path`: Output path for the DMC results (e.g. significant_dmcs.bed)
- `q_threshold`, `delta_threshold` as agreed.


### Step 6: Visualization (quick, optional)

**Volcano-like plot (Δmethylation vs –log10(q))**

1. Call:
- `mcp__methyl-tools__plot_dmr_volcano` 
with:
- `metilene_results_path`: DMR results from Step 3
- `output_pdf_path`
- `q_threshold`, `delta_threshold` as agreed.
- Optional tuning of `point_size`, `alpha` as needed.

**DMR length histogram**
Call:
- `mcp__methyl-tools__plot_dmr_length_hist` 

with:
- `significant_bed_path`: Path for the signimicant DMRs (BED format from Step 5)
- `output_pdf_path`

---


## Troubleshooting
- **Chromosome naming mismatches**: standardize to a single scheme (`chr1` vs `1`) across all samples.
