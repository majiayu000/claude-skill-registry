---
name: integrative-DMR-DEG
description: This skill performs correlation analysis between differential methylation and differential gene expression, identifying genes with coordinated epigenetic regulation. It provides preprocessing and integration workflows, using promoter-level methylation–expression relationships.

---

# Integrative Methylation–Expression Correlation Analysis

## Overview

This skill integrates **differential methylation** and **differential expression** datasets to reveal coordinated epigenetic regulation patterns.

- Refer to **Inputs & Outputs** to verify necessary files.
- **Always prompt user** for genome assembly used.
- Prepare the DMR regions into 6-column standard format BED file received by HOMER.
- **Annotate** the differential methylation regions to the gene promoter.
- **Preprocess** differential methylation and expression tables into a standard format.
- **Integrate** methylation and expression data by promoter proximity.
- **Calculate correlation** between methylation change and expression fold change.
- **Classify patterns** such as hypermethylation–downregulation or hypomethylation–upregulation.

---

## Inputs & Outputs

### Inputs

```bash
dmr_results.txt # DMR results output by the metilene
dge_result.csv # DEG results output by DESeq2
```

### Outputs
```bash
corr_DMR_DEG/
  stats/
    integrated_results.tsv
    pattern_counts.tsv
    summary_stats.tsv
    correlation_plot.pdf
  temp/
    homer_dmr.bed
    ... # Other temp files
```


---

## Decision Tree

### Step 1: Prepare the DMR regions into 6-column standard format BED file received by HOMER
```bash
awk -F'\t' 'BEGIN {OFS="\t"} {print $1, $2, $3, "peak_"NR, "*", "+"}' dmr_results.txt > homer_dmr.bed
```

### Step 2: Annotate the differential methylation regions to the gene promoter.
Call:

- mcp__homer-tools__homer_simple_annotate_peaks

with:
- `peaks_path`: 6-column standard format BED file from Step 1.
- `genome`: Provide by user.
- `output_path`: Output path of the annotated file


### Step 3: Preprocess differential methylation and expression tables into a standard format

Call:

- mcp__methyl-tools__preprocess_differential_table

(1) with:
- `input_path`: dmr_results.txt
- `output_path`
- `data_type`: methyl
- `source`: metilene

(2) with:
- `input_path`: dge_result.csv
- `output_path`
- `data_type`: expr
- `source`: deseq2

### Step 4: Integrate methylation and expression data by promoter proximity

Call:

- mcp__methyl-tools__integrate_methylation_expression

with:

`methyl_path`: Path to standardized methylation TSV with columns: chr,start,end,pvalue,meth_diff (from Step 3)
`methyl_annot_path`: Path to methylation annotation TSV from HOMER (from Step 2).
`expr_path`: Path to standardized expression TSV with columns: gene,pvalue,log2FoldChange (from Step 3).
`output_prefix`: Prefix for all output files (e.g. 'corr_DMR_DEG/stats/integrative').
`methyl_diff`: Absolute methylation difference threshold (fraction points).
`expr_fc`: Fold-change threshold for expression (absolute, e.g. 1.5 for 1.5x).
