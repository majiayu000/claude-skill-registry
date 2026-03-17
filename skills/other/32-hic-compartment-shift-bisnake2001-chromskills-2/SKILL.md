---
name: hic-compartment-shift
description: This skill performs A/B compartment shift analysis between two Hi-C samples.
---

# Compartment shift Analysis 
---

## Overview

This skill performs A/B compartment shift analysis using PC1 eigenvector values extracted from Hi-C data, following the HOMER framework. It supports two conditions, each with two or more replicates, and uses the PC1 values (E1 column) from user-provided TSV files.

Major steps include:
- Refer to **Inputs & Outputs** to verify necessary files.
- **Always prompt user** for genome assembly used. Never decide by yourself.
- Convert TSV (Chrom, start, end, weight, E1) into HOMER-compatible PC1 bedGraph files.
- Generate a unified genomic bin list for annotatePeaks.
- Extract PC1 values across all samples.
- Perform differential PC1 analysis with replicate-aware limma statistics.
- Produce differential compartment tables and stitched compartment-shift domains.
---

## When to use this skill

Use this skill when you want to:
- Detect compartment shifts between two conditions (e.g., cell type 1 vs cell type 2)
- Identify statistically significant changes in PC1 values across genomic bins
- Determine regions that flip between A and B compartments
- Integrate compartment shift results with other genomic datasets

---

## Inputs & Outputs

### Inputs

Example input set:
- `CT1_rep1.tsv`
- `CT1_rep2.tsv`
- `CT2_rep1.tsv`
- `CT2_rep2.tsv`

Additional requirements:
- All TSVs must share identical bins.

---

### Outputs
```bash
compartments_shift_analysis/
    shift_regions/
        diff_PC1_CT2_vs_CT1.txt
        regions.*.txt # other region files output by the tools used.
    temp/
        bins_PC1.txt
        PC1_all_samples.txt
        *.bedGraph # other bedGraph file
```

---

## Decision Tree

### Step 1: Convert TSV files to PC1 bedGraph

```bash
awk 'BEGIN{OFS="	"} NR>1 && NF==5 {print $1, $2, $3, $5}' CT1_rep1.tsv > CT1_rep1.PC1.bedGraph

```

### Step 2: Create a bin list for annotatePeaks

Use any one TSV as the template:

```bash
awk 'BEGIN{OFS="	"} NR>1 && NF==5 {print $1, $2, $3}' CT1_rep1.tsv > bins_PC1.txt
```

The resulting `bins_PC1.txt` defines genomic intervals for PC1 extraction.

### Step 3: Compartment shift analysis

Call:

- `mcp_homer-tools__homer_differential_PC1`

with:
- `bins_pc1_path`: Path to the bins_PC1.txt file generated earlier,
- `genome`: HOMER genome identifier, **provided by user**.
- `bedgraph_paths`: List of PC1 bedGraph files in the exact replicate order (e.g., CT1_rep1, CT1_rep2, CT2_rep1, CT2_rep2).
- `experiment_labels`: List of experiment group labels matching bedGraph order (e.g. ['CT1','CT1','CT2','CT2']).
- `merged_output_path`: Output path for merged PC1 table. Empty → '<bins_pc1_path>.merged_PC1.txt'.
- `diff_output_path`: Output path for differential PC1 table. Empty → 'diff_PC1.txt'.

