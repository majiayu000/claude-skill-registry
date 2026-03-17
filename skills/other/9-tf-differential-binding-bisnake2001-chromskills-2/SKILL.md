---
name: TF-differential-binding
description: The TF-differential-binding pipeline performs differential transcription factor (TF) binding analysis from ChIP-seq datasets (TF peaks) using the DiffBind package in R. It identifies genomic regions where TF binding intensity significantly differs between experimental conditions (e.g., treatment vs. control, mutant vs. wild-type). Use the TF-differential-binding pipeline when you need to analyze the different function of the same TF across two or more biological conditions, cell types, or treatments using ChIP-seq data or TF binding peaks. This pipeline is ideal for studying regulatory mechanisms that underlie transcriptional differences or epigenetic responses to perturbations.
---

# DiffBind TF Differential Binding Analysis

## Overview

This skill enables comprehensive differential TF binding analysis using **DiffBind** in R. DiffBind integrates read counting, normalization, and statistical modeling to identify differentially bound peaks between conditions.

To perform DiffBind differential binding analysis:
- Initialize the project directory.
- Refer to the **Inputs & Outputs** section to check inputs and build the output architecture. All the output file should located in `${proj_dir}` in Step 0.
- **Always prompt user** if required files are missing.
- Provide a sample sheet with ChIP-seq peak files and corresponding BAM files for each sample.
- Construct a `DBA` object from the sample sheet.
- Compute read counts over consensus peak regions.
- Specify experimental conditions (e.g., treatment vs. control or cell_type_A vs. cell_type_B).
- Run statistical tests to identify differentially bound regions.
- Generate correlation heatmaps, PCA plots, and volcano plots; extract significant binding events.

---

## When to use this skill
Use the TF-differential-binding pipeline when you need to analyze the different function of the same TF across two or more biological conditions, cell types, or treatments using ChIP-seq data or TF binding peaks. This pipeline is ideal for studying regulatory mechanisms that underlie transcriptional differences or epigenetic responses to perturbations.

Recommended applications include:

- Comparing treated vs. control or wild-type vs. mutant conditions to identify TF binding changes in response to stimuli, drugs, or mutations.
- Comparing TF binding profiles between two cell types or experimental conditions to identify differentially bound regions (DBRs).
- Comparing the different TF function in two conditions.
- Integrating with RNA-seq to correlate TF binding alterations with gene expression changes.
- Investigating co-factor dependencies or chromatin remodeling events linked to TF occupancy.

---

## Inputs & Outputs

### Inputs (choose one)
- If starting from BAM files and BED peak files → Generate consensus peaks and count matrix.  
- If starting from existing count matrix → Go directly to DiffBind analysis.  
- If multiple conditions or batches → Include batch/condition in design 

### Outputs
```bash
${sample}_TF_DB_analysis/
    DBs/
      DB_results.csv # DESeq2 results (log2FC, p-values)
      DB_up.bed
      DB_down.bed  
    plots/ # visualization outputs
      PCA.pdf
      volcano.pdf
      heatmap.pdf
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
- `task`: TF_DB

The tool will:

- Create `${sample}_TF_DB` directory.
- Return the full path of the `${sample}_TF_DB` directory, which will be used as `${proj_dir}`.

### Step 1: Prepare Input Data

Create a CSV sample sheet (`samplesheet.csv`) with the following columns:

| SampleID | Tissue | Factor | Condition | bamReads | Peaks | PeakCaller |
|-----------|------------|------------|-----------|--------|-------------|-------------|
| TF_A_1    | A    | TF   | Control       | Control1.bam | Control1_peaks.narrowPeak | narrow |
| TF_A_2    | A    | TF   | Control       | Control2.bam | Control2_peaks.narrowPeak | narrow |
| TF_B_1    | A    | TF   | Treated       | Treated1.bam | Treated1_peaks.narrowPeak | narrow |
| TF_B_2    | A    | TF   | Treated       | Treated2.bam | Treated2_peaks.narrowPeak | narrow |

### Step 2: Load Data and Build the DiffBind Object

```r
library(DiffBind)
samples <- read.csv("samplesheet.csv")
dbObj <- dba(sampleSheet=samples)
```

**Key parameters:**
- `sampleSheet`: CSV file with BAM and peak information
- Supports both narrowPeak and broadPeak formats


### Step 3: Read Counting and Consensus Peak Generation

Count reads overlapping consensus peaks across samples:

```r
# Generate a consensus peakset
dbObj <- dba.count(dbObj, summits=250)
```

**Notes:**
- `summits`: re-centers peaks ±250 bp around summits for consistency.
- The resulting matrix contains normalized counts for all samples.

---

### Step 4: Contrast Definition

Define conditions for comparison:

```r
# Define experimental contrasts (e.g., Treated vs Control)
dbObj <- dba.contrast(dbObj, categories=DBA_CONDITION, minMembers=2)
```

**Alternatives:**
- For multifactor experiments: use `DBA_TISSUE`, `DBA_TREATMENT`, or custom metadata.
- Check contrasts:
  ```r
  dba.show(dbObj, bContrasts=TRUE)
  ```

---

### Step 5: Differential Binding Analysis

```r
# Perform analysis
dbObj <- dba.analyze(dbObj, method=DBA_DESEQ2)
```

**Parameters:**
- `method`: choose `DBA_DESEQ2` (default) or `DBA_EDGER`
- `th`: FDR threshold (default 0.05)
- `fold`: minimum log2 fold change
- `bUsePval=TRUE`: use p-values instead of FDR cutoff

---

### Step 6: Visualization and Quality Control

#### Correlation Heatmap

```r
dba.plotHeatmap(dbObj, correlations=TRUE, scale="row")
```

#### PCA Plot

```r
dba.plotPCA(dbObj, attributes=DBA_CONDITION, label=DBA_ID)
```

#### Volcano Plot

```r
# Volcano plot
allResults <- dba.report(dbObj, method=DBA_DESEQ2, th=1)
with(allResults, plot(Fold, -log10(FDR),
     col=ifelse(FDR < 0.05 & abs(Fold) > 1, "red", "grey"),
     pch=16, main="Volcano Plot"))
```
Output: `heatmap.pdf`  `Volcano.pdf` `PCA.pdf` 

---

### Step 7: Result Extraction

Export significant differential peaks:

```r
write.csv(as.data.frame(allResults), "DB_results.csv", row.names = FALSE)
library(rtracklayer)
# Extract results with FDR < 0.05 and |log2FC| > 1
sigSites <- dba.report(dbObj, method=DBA_DESEQ2, th=0.05, fold=1)
print("Differential binding results summary:")
print(summary(sigSites))

# get the peaks that up or down in treated condition
diff_up <- sigSites[sigSites$Fold > 0]
diff_down <- sigSites[sigSites$Fold < 0]
export(diff_up, "DB_up_${treated_condition}.bed")
export(diff_down, "DB_down_${treated_condition}.bed")
```
Output: `DB_results.csv`  `DB_up_${treated_condition}.bed` `DB_down_${treated_condition}.bed` 


---

## Interpretation and Biological Insights

### Significance Criteria

- **FDR < 0.05** → statistically significant  
- **|log2FC| > 1** → biologically meaningful difference  
- **Consistent replicates** → at least two replicates per condition recommended

### Typical Biological Interpretations

- **Increased binding** in treated condition → potential activation or recruitment of TFs
- **Decreased binding** → loss of TF affinity or chromatin closing
- Combine with RNA-seq to correlate with target gene expression.

---

## Troubleshooting

| Problem | Possible Cause | Solution |
|----------|----------------|-----------|
| No differential peaks found | Insufficient replicates or low coverage | Increase sequencing depth or lower FDR threshold |
| Errors in sample sheet | Column names incorrect or missing | Use standard DiffBind column format |
| Inconsistent genome build | Mixed genome assemblies | Ensure all BAM and peak files use the same genome reference |
| Over-normalization | Strong batch effects | Include batch term in design or run `dba.contrast(..., block=...)` |
